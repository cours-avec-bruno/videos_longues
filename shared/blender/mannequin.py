"""Mannequins low poly sans visage, posables par script (Blender, bpy).

Inspiré des références données par Bruno (figurines rouges à facettes, sans visage) : un squelette simple
(cinématique directe), habillé d'un modificateur Skin, lissé puis décimé pour obtenir des facettes nettes,
ombrage plat. On pose le personnage avec des angles en degrés, articulation par articulation.

    import sys; sys.path.append(".../shared/blender")
    from mannequin import mannequin, materiau
    m = mannequin("manoj", {"genou_g": (-90, 0, 0)}, echelle=0.55, enfant=True, mat=materiau("rouge", (0.6, 0.08, 0.04)))
    m.location = (0, 0, 0); m.rotation_euler.z = ...

Repère : le personnage regarde vers -Y, Z vers le haut, pieds à z = 0 au repos.
Angles (degrés, appliqués dans le repère local de l'articulation, ordre XYZ) :
  X négatif : la partie suivante part vers l'avant (cuisse levée, bras tendu devant, buste penché en avant)
  Y         : vers le côté (positif : vers la gauche du personnage pour le côté gauche… à vérifier au rendu)
  Z         : torsion
"""
import math

import bpy
import bmesh
from mathutils import Euler, Matrix, Vector

# articulation : (parent, décalage au repos depuis le parent, rayon (x, y) de la peau)
SQUELETTE = {
    "bassin": (None, (0, 0, 0.95), (0.16, 0.11)),
    "taille": ("bassin", (0, 0, 0.16), (0.135, 0.095)),
    "torse": ("taille", (0, 0, 0.19), (0.18, 0.115)),
    "cou": ("torse", (0, 0, 0.15), (0.05, 0.05)),
    "tete": ("cou", (0, 0, 0.11), (0.095, 0.105)),
    "crane": ("tete", (0, 0.0, 0.10), (0.085, 0.095)),
    "epaule_g": ("torse", (0.2, 0, 0.08), (0.065, 0.065)),
    "coude_g": ("epaule_g", (0, 0, -0.29), (0.045, 0.045)),
    "poignet_g": ("coude_g", (0, 0, -0.25), (0.035, 0.03)),
    "main_g": ("poignet_g", (0, 0, -0.09), (0.04, 0.02)),
    "epaule_d": ("torse", (-0.2, 0, 0.08), (0.065, 0.065)),
    "coude_d": ("epaule_d", (0, 0, -0.29), (0.045, 0.045)),
    "poignet_d": ("coude_d", (0, 0, -0.25), (0.035, 0.03)),
    "main_d": ("poignet_d", (0, 0, -0.09), (0.04, 0.02)),
    "hanche_g": ("bassin", (0.095, 0, -0.04), (0.088, 0.088)),
    "genou_g": ("hanche_g", (0, 0, -0.43), (0.06, 0.06)),
    "cheville_g": ("genou_g", (0, 0, -0.43), (0.04, 0.04)),
    "pied_g": ("cheville_g", (0, -0.15, -0.05), (0.04, 0.03)),
    "hanche_d": ("bassin", (-0.095, 0, -0.04), (0.088, 0.088)),
    "genou_d": ("hanche_d", (0, 0, -0.43), (0.06, 0.06)),
    "cheville_d": ("genou_d", (0, 0, -0.43), (0.04, 0.04)),
    "pied_d": ("cheville_d", (0, -0.15, -0.05), (0.04, 0.03)),
}
ORDRE = list(SQUELETTE)        # les parents sont toujours avant leurs enfants


def positions(pose, enfant=False):
    """Positions des articulations (repère du personnage) pour une pose {articulation: (x, y, z) degrés}."""
    mondes = {}
    pts = {}
    for j in ORDRE:
        parent, dec, _ = SQUELETTE[j]
        dec = Vector(dec)
        if enfant:                       # proportions d'enfant : tête plus grosse, membres plus courts
            if j in ("tete", "crane"):
                dec = dec * 1.25
            elif j not in ("bassin",):
                dec = dec * 0.92
        rot = Euler([math.radians(a) for a in pose.get(j, (0, 0, 0))], "XYZ").to_matrix().to_4x4()
        base = mondes[parent] if parent else Matrix.Identity(4)
        m = base @ Matrix.Translation(dec) @ rot
        mondes[j] = m
        pts[j] = m.to_translation()
    return pts


def materiau(nom, couleur, rugosite=0.55, brillance=0.35):
    m = bpy.data.materials.get(nom) or bpy.data.materials.new(nom)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*couleur, 1)
    b.inputs["Roughness"].default_value = rugosite
    for cle in ("Specular IOR Level", "Specular"):
        if cle in b.inputs:
            b.inputs[cle].default_value = brillance
    return m


def mannequin(nom, pose, echelle=1.0, enfant=False, mat=None, facettes=0.09, collection=None, au_sol=True):
    """Crée le personnage posé ; renvoie l'objet. Avec au_sol, le point le plus bas touche z = 0."""
    pts = positions(pose, enfant)
    if au_sol:
        bas = min(pts[j].z - SQUELETTE[j][2][0] * 0.8 for j in ORDRE)
        for j in ORDRE:
            pts[j].z -= bas
    me = bpy.data.meshes.new(nom)
    bm = bmesh.new()
    vs = {j: bm.verts.new(pts[j]) for j in ORDRE}
    for j in ORDRE:
        parent = SQUELETTE[j][0]
        if parent:
            bm.edges.new((vs[parent], vs[j]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(nom, me)
    (collection or bpy.context.scene.collection).objects.link(ob)
    sk = ob.modifiers.new("peau", "SKIN")
    sk.use_smooth_shade = False
    sk.branch_smoothing = 0.6
    for i, j in enumerate(ORDRE):
        r = SQUELETTE[j][2]
        f = 1.0
        if enfant and j in ("tete", "crane"):
            f = 1.2
        me.skin_vertices[0].data[i].radius = (r[0] * f, r[1] * f)
    me.skin_vertices[0].data[0].use_root = True
    sub = ob.modifiers.new("lisse", "SUBSURF")
    sub.levels = sub.render_levels = 2
    dec = ob.modifiers.new("facettes", "DECIMATE")
    dec.ratio = facettes
    dec.use_collapse_triangulate = True
    ob.scale = (echelle,) * 3
    if mat:
        ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = False
    return ob


# ---------------------------------------------------------------- quelques poses de base
POSES = {
    "debout": {},
    # assis en tailleur, au sol
    "tailleur": {"hanche_g": (-80, 0, -45), "genou_g": (125, 0, 0), "hanche_d": (-80, 0, 45), "genou_d": (125, 0, 0),
                 "epaule_g": (-25, 0, 10), "coude_g": (-50, 0, 0), "epaule_d": (-25, 0, -10), "coude_d": (-50, 0, 0)},
    # accroupi, mains vers le sol
    "accroupi": {"taille": (-20, 0, 0), "torse": (-15, 0, 0), "hanche_g": (-120, 0, -12), "genou_g": (150, 0, 0),
                 "cheville_g": (-30, 0, 0), "hanche_d": (-120, 0, 12), "genou_d": (150, 0, 0), "cheville_d": (-30, 0, 0),
                 "epaule_g": (-55, 0, 0), "coude_g": (-20, 0, 0), "epaule_d": (-55, 0, 0), "coude_d": (-20, 0, 0)},
    # assis sur un siège bas (genoux à angle droit)
    "assis": {"hanche_g": (-90, 0, -6), "genou_g": (90, 0, 0), "hanche_d": (-90, 0, 6), "genou_d": (90, 0, 0),
              "epaule_g": (-20, 0, 6), "coude_g": (-60, 0, 0), "epaule_d": (-20, 0, -6), "coude_d": (-60, 0, 0)},
    # course
    "course": {"taille": (-10, 0, 0), "torse": (-8, 0, 0),
               "hanche_g": (-60, 0, 0), "genou_g": (80, 0, 0), "hanche_d": (25, 0, 0), "genou_d": (70, 0, 0),
               "cheville_d": (20, 0, 0),
               "epaule_g": (40, 0, 8), "coude_g": (-70, 0, 0), "epaule_d": (-50, 0, -8), "coude_d": (-80, 0, 0)},
}
