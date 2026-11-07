"""S01 · Le bureau, la nuit, en vue subjective.

Construit la scène dans Blender à partir de rien (aucun asset téléchargé, matières procédurales),
anime la caméra (une marche lente vers la chaise) et rend les images demandées.
Higgsfield donnera vie au plan à partir de ces images.

Lancer sur le PC (Blender 5.2) :
  "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b -P bureau.py -- --rendu depart,arrivee --echantillons 128

Sorties (hors Git) : videos/<slug>/medias/S01/  (images PNG) et videos/<slug>/medias/blender/S01_bureau.blend

Fiche de scène (le « passeport », version du 07/11/2026 : le bureau perdu dans le noir) :
  Sujet       : un bureau seul au milieu d'un immense espace noir. Pas de murs visibles, pas de fenêtre.
                On marche vers lui depuis l'obscurité, jusqu'à la chaise vide.
  Point focal : l'écran allumé et la chaise ; second point : le cercle de lumière au sol autour du bureau.
  Zone noire  : tout le reste. Le noir est le sujet autant que le bureau.
  Lumière     : clé = une lumière froide et étroite qui tombe d'en haut sur le bureau (un îlot) ;
                pratique = l'écran ; brume très légère, limitée au cône, pour lire le faisceau.
                Le sol, légèrement brillant, étire le reflet de l'écran vers nous et donne l'échelle.
  Détail      : un câble part du bureau et s'enfonce dans le noir.
  Caméra      : vue subjective, yeux à 1,62 m, focale 30 mm ; départ à ~7 m du bureau, dans le noir ;
                arrivée juste derrière la chaise. 5 s (120 images à 24 i/s), pas lents, léger balancement.
  Unités      : mètres, Z vers le haut. Le bureau est au centre (0, 0), face aux y positifs.
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

ICI = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.abspath(os.path.join(ICI, "..", ".."))
SORTIE = os.path.join(VIDEO, "medias", "S01")
BLEND = os.path.join(VIDEO, "medias", "blender", "S01_bureau.blend")

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--rendu", default="depart,arrivee", help="depart, arrivee, milieu, ou une liste d'images ex. 1,60,120")
ap.add_argument("--echantillons", type=int, default=128)
ap.add_argument("--largeur", type=int, default=1920)
ap.add_argument("--hauteur", type=int, default=1080)
ap.add_argument("--sans-brume", action="store_true")
ap.add_argument("--suffixe", default="")
A = ap.parse_args(argv)

rad = math.radians

# ---------------------------------------------------------------- remise à zéro
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.unit_settings.system = "METRIC"
coll = {}
for nom in ("ENV", "PRP", "LGT", "CAM"):
    c = bpy.data.collections.new(nom)
    sc.collection.children.link(c)
    coll[nom] = c


def lier(obj, groupe):
    coll[groupe].objects.link(obj)
    return obj


# ---------------------------------------------------------------- matières
def noeuds(mat):
    mat.use_nodes = True
    return mat.node_tree.nodes, mat.node_tree.links


def matiere(nom, couleur, rugo=0.6, metal=0.0, var=0.08, bosse=0.0, echelle_bosse=60.0):
    """Principled + variation de teinte par objet (Voronoi) + rugosité bruitée + bosse légère."""
    m = bpy.data.materials.get(nom)
    if m:
        return m
    m = bpy.data.materials.new(nom)
    n, l = noeuds(m)
    bsdf = n["Principled BSDF"]
    bsdf.inputs["Metallic"].default_value = metal
    coord = n.new("ShaderNodeTexCoord")
    # variation de teinte : chaque objet légèrement différent
    vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 0.6
    l.new(coord.outputs["Object"], vor.inputs["Vector"])
    bw = n.new("ShaderNodeRGBToBW"); l.new(vor.outputs["Color"], bw.inputs["Color"])
    mr = n.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = 1 - var; mr.inputs["To Max"].default_value = 1 + var
    l.new(bw.outputs["Val"], mr.inputs["Value"])
    mul = n.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"
    mul.inputs[0].default_value = 1.0
    mul.inputs[6].default_value = (*couleur, 1)
    cv = n.new("ShaderNodeCombineColor")
    for k in ("Red", "Green", "Blue"):
        l.new(mr.outputs["Result"], cv.inputs[k])
    l.new(cv.outputs["Color"], mul.inputs[7])
    l.new(mul.outputs[2], bsdf.inputs["Base Color"])
    # rugosité bruitée (poussière, traces)
    nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 9.0; nz.inputs["Detail"].default_value = 6
    l.new(coord.outputs["Object"], nz.inputs["Vector"])
    mr2 = n.new("ShaderNodeMapRange")
    mr2.inputs["To Min"].default_value = max(0.02, rugo - 0.12); mr2.inputs["To Max"].default_value = min(1.0, rugo + 0.12)
    l.new(nz.outputs["Fac"], mr2.inputs["Value"])
    l.new(mr2.outputs["Result"], bsdf.inputs["Roughness"])
    if bosse > 0:
        nz2 = n.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = echelle_bosse; nz2.inputs["Detail"].default_value = 8
        l.new(coord.outputs["Object"], nz2.inputs["Vector"])
        bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bosse; bp.inputs["Distance"].default_value = 0.002
        l.new(nz2.outputs["Fac"], bp.inputs["Height"])
        l.new(bp.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def matiere_sol():
    """Linoléum gris-bleu en dalles de 50 cm, joints sombres, usure."""
    m = bpy.data.materials.new("MAT_sol_lino")
    n, l = noeuds(m)
    bsdf = n["Principled BSDF"]
    coord = n.new("ShaderNodeTexCoord")
    brk = n.new("ShaderNodeTexBrick")
    brk.offset = 0.0; brk.squash = 1.0
    brk.inputs["Scale"].default_value = 2.0
    brk.inputs["Mortar Size"].default_value = 0.004
    brk.inputs["Brick Width"].default_value = 1.0; brk.inputs["Row Height"].default_value = 1.0
    brk.inputs["Color1"].default_value = (0.07, 0.078, 0.085, 1)
    brk.inputs["Color2"].default_value = (0.062, 0.07, 0.077, 1)
    brk.inputs["Mortar"].default_value = (0.05, 0.055, 0.06, 1)
    l.new(coord.outputs["Generated"], brk.inputs["Vector"])
    mapping = n.new("ShaderNodeMapping"); mapping.inputs["Scale"].default_value = (60 / 0.6 / 2.0, 60 / 0.6 / 2.0, 1)
    l.new(coord.outputs["Object"], mapping.inputs["Vector"])
    l.new(mapping.outputs["Vector"], brk.inputs["Vector"])
    l.new(brk.outputs["Color"], bsdf.inputs["Base Color"])
    nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.0; nz.inputs["Detail"].default_value = 10
    l.new(coord.outputs["Object"], nz.inputs["Vector"])
    mr = n.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.16; mr.inputs["To Max"].default_value = 0.42
    l.new(nz.outputs["Fac"], mr.inputs["Value"]); l.new(mr.outputs["Result"], bsdf.inputs["Roughness"])
    return m


def matiere_ecran():
    """L'écran : un fond presque noir, une fenêtre d'interface grise, une émission froide."""
    m = bpy.data.materials.new("MAT_ecran")
    n, l = noeuds(m)
    for x in list(n):
        n.remove(x)
    out = n.new("ShaderNodeOutputMaterial")
    em = n.new("ShaderNodeEmission")
    coord = n.new("ShaderNodeTexCoord")
    sep = n.new("ShaderNodeSeparateXYZ"); l.new(coord.outputs["UV"], sep.inputs["Vector"])
    # rectangle central (fenêtre) : 0.18 < u < 0.82 et 0.22 < v < 0.8
    def bande(entree, a, b):
        g = n.new("ShaderNodeMath"); g.operation = "GREATER_THAN"; g.inputs[1].default_value = a
        s = n.new("ShaderNodeMath"); s.operation = "LESS_THAN"; s.inputs[1].default_value = b
        l.new(entree, g.inputs[0]); l.new(entree, s.inputs[0])
        mm = n.new("ShaderNodeMath"); mm.operation = "MULTIPLY"
        l.new(g.outputs[0], mm.inputs[0]); l.new(s.outputs[0], mm.inputs[1])
        return mm.outputs[0]
    u = bande(sep.outputs["X"], 0.2, 0.8); v = bande(sep.outputs["Y"], 0.22, 0.82)
    fen = n.new("ShaderNodeMath"); fen.operation = "MULTIPLY"
    l.new(u, fen.inputs[0]); l.new(v, fen.inputs[1])
    # lignes de texte : des barres horizontales fines dans la fenêtre
    wave = n.new("ShaderNodeTexWave"); wave.wave_type = "BANDS"; wave.bands_direction = "Y"
    wave.inputs["Scale"].default_value = 5.0; wave.inputs["Distortion"].default_value = 0.0
    l.new(coord.outputs["UV"], wave.inputs["Vector"])
    gt = n.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.82
    l.new(wave.outputs["Fac"], gt.inputs[0])
    col = n.new("ShaderNodeMix"); col.data_type = "RGBA"
    col.inputs[6].default_value = (0.008, 0.010, 0.016, 1)   # fond
    col.inputs[7].default_value = (0.10, 0.125, 0.16, 1)     # fenêtre
    l.new(fen.outputs[0], col.inputs[0])
    col2 = n.new("ShaderNodeMix"); col2.data_type = "RGBA"
    l.new(col.outputs[2], col2.inputs[6])
    col2.inputs[7].default_value = (0.26, 0.30, 0.36, 1)     # lignes
    lt = n.new("ShaderNodeMath"); lt.operation = "MULTIPLY"
    l.new(gt.outputs[0], lt.inputs[0]); l.new(fen.outputs[0], lt.inputs[1])
    l.new(lt.outputs[0], col2.inputs[0])
    l.new(col2.outputs[2], em.inputs["Color"])
    em.inputs["Strength"].default_value = 1.6
    l.new(em.outputs[0], out.inputs["Surface"])
    return m


def matiere_emission(nom, couleur, force):
    m = bpy.data.materials.new(nom)
    n, l = noeuds(m)
    for x in list(n):
        n.remove(x)
    out = n.new("ShaderNodeOutputMaterial"); em = n.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*couleur, 1); em.inputs["Strength"].default_value = force
    l.new(em.outputs[0], out.inputs["Surface"])
    return m


M = {
    "mur": matiere("MAT_mur_peint", (0.50, 0.53, 0.55), rugo=0.85, var=0.03, bosse=0.15, echelle_bosse=120),
    "plafond": matiere("MAT_plafond", (0.55, 0.57, 0.58), rugo=0.9, var=0.02),
    "sol": matiere_sol(),
    "bureau": matiere("MAT_bureau_stratifie", (0.10, 0.105, 0.11), rugo=0.45, var=0.04, bosse=0.03, echelle_bosse=300),
    "metal": matiere("MAT_metal_laque", (0.08, 0.085, 0.09), rugo=0.38, metal=0.6, var=0.05),
    "acier": matiere("MAT_acier_brosse", (0.55, 0.56, 0.57), rugo=0.32, metal=1.0, var=0.04),
    "plastique": matiere("MAT_plastique_noir", (0.025, 0.026, 0.028), rugo=0.5, var=0.06),
    "tissu": matiere("MAT_tissu_chaise", (0.045, 0.05, 0.055), rugo=0.95, var=0.06, bosse=0.35, echelle_bosse=400),
    "papier": matiere("MAT_papier", (0.45, 0.46, 0.46), rugo=0.9, var=0.05),
    "carton": matiere("MAT_chemise_carton", (0.22, 0.30, 0.38), rugo=0.85, var=0.1),
    "ceramique": matiere("MAT_tasse", (0.55, 0.56, 0.58), rugo=0.25, var=0.03),
    "store": matiere("MAT_store_alu", (0.55, 0.57, 0.6), rugo=0.4, metal=0.7, var=0.05),
    "radiateur": matiere("MAT_radiateur", (0.6, 0.61, 0.6), rugo=0.55, var=0.04),
    "ecran": matiere_ecran(),
    "led": matiere_emission("MAT_led_veille", (0.55, 0.85, 1.0), 6.0),
    "ciel": matiere_emission("MAT_ciel_aube", (0.05, 0.09, 0.2), 1.0),
}


# ---------------------------------------------------------------- primitives
def boite(nom, dim, pos, mat, groupe="PRP", rot=(0, 0, 0), biseau=0.0, parent=None):
    me = bpy.data.meshes.new(nom)
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=dim, verts=bm.verts)   # échelle dans le maillage : biseaux et enfants restent justes
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(nom, me)
    o.location = pos; o.rotation_euler = rot
    me.materials.append(mat)
    if biseau > 0:
        b = o.modifiers.new("biseau", "BEVEL"); b.width = biseau; b.segments = 3; b.limit_method = "ANGLE"
    lier(o, groupe)
    if parent:
        o.parent = parent
    for p in me.polygons:
        p.use_smooth = True
    return o


def cylindre(nom, r, h, pos, mat, groupe="PRP", rot=(0, 0, 0), sommets=24, parent=None):
    import bmesh
    me = bpy.data.meshes.new(nom)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=sommets, radius1=r, radius2=r, depth=h)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(nom, me)
    o.location = pos; o.rotation_euler = rot
    me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    lier(o, groupe)
    if parent:
        o.parent = parent
    return o


def vide(nom, pos, groupe="PRP", rot=(0, 0, 0)):
    o = bpy.data.objects.new(nom, None)
    o.location = pos; o.rotation_euler = rot
    lier(o, groupe)
    return o


# ---------------------------------------------------------------- l'espace : un sol immense, rien d'autre
sol = boite("ENV_sol", (60, 60, 0.02), (0, 0, -0.01), M["sol"], "ENV")

# ---------------------------------------------------------------- le bureau
BY = 0.0                # centre du plateau : le bureau est au centre de l'espace
BZ = 0.74
boite("PRP_bureau_plateau", (1.6, 0.8, 0.028), (0.0, BY, BZ), M["bureau"], biseau=0.004)
for sx in (-1, 1):
    boite(f"PRP_bureau_pied_{sx}", (0.05, 0.7, 0.03), (sx * 0.75, BY, 0.015), M["metal"])
    boite(f"PRP_bureau_montant_{sx}", (0.05, 0.05, BZ - 0.03), (sx * 0.75, BY, (BZ - 0.03) / 2), M["metal"])
    boite(f"PRP_bureau_traverse_{sx}", (0.05, 0.65, 0.03), (sx * 0.75, BY, BZ - 0.035), M["metal"])
boite("PRP_bureau_voile", (1.45, 0.012, 0.32), (0, BY + 0.36, BZ - 0.2), M["metal"])
# caisson à tiroirs à droite
boite("PRP_caisson", (0.42, 0.55, 0.58), (0.52, BY + 0.05, 0.3), M["metal"], biseau=0.006)
for i in range(3):
    boite(f"PRP_caisson_poignee_{i}", (0.12, 0.012, 0.012), (0.52, BY - 0.23, 0.15 + i * 0.18), M["acier"])
# unité centrale sous le bureau, à gauche, avec sa LED de veille
boite("PRP_unite_centrale", (0.2, 0.45, 0.43), (-0.55, BY + 0.05, 0.22), M["plastique"], biseau=0.005)
boite("PRP_led_veille", (0.004, 0.004, 0.004), (-0.47, BY - 0.177, 0.4), M["led"])

# écran 27 pouces, légèrement décalé à droite
EX, EY = 0.08, BY + 0.14
boite("PRP_ecran_pied", (0.24, 0.18, 0.012), (EX, EY + 0.02, BZ + 0.02), M["metal"], biseau=0.003)
boite("PRP_ecran_colonne", (0.05, 0.03, 0.34), (EX, EY + 0.08, BZ + 0.18), M["metal"])
boite("PRP_ecran_coque", (0.625, 0.045, 0.37), (EX, EY, BZ + 0.35), M["plastique"], biseau=0.006)
me_ec = bpy.data.meshes.new("PRP_ecran_dalle")
me_ec.from_pydata([(-0.3, 0, -0.17), (0.3, 0, -0.17), (0.3, 0, 0.17), (-0.3, 0, 0.17)], [], [(0, 1, 2, 3)])
me_ec.uv_layers.new(name="UVMap")
for li, uv in zip(me_ec.uv_layers["UVMap"].data, ((0, 0), (1, 0), (1, 1), (0, 1))):
    li.uv = uv
me_ec.materials.append(M["ecran"])
dalle = lier(bpy.data.objects.new("PRP_ecran_dalle", me_ec), "PRP")
dalle.location = (EX, EY - 0.0235, BZ + 0.355)

# clavier, souris, carnet, stylo, chemises (plus de tasse), lampe éteinte, câble
cl = boite("PRP_clavier", (0.44, 0.14, 0.022), (0.02, BY - 0.18, BZ + 0.025), M["plastique"], rot=(rad(3), 0, rad(-2)), biseau=0.003)
for r in range(5):
    for c in range(15):
        boite(f"PRP_touche_{r}_{c}", (0.022, 0.02, 0.008), (-0.175 + c * 0.025, -0.05 + r * 0.024, 0.014), M["plastique"], biseau=0.002, parent=cl)
boite("PRP_souris", (0.06, 0.1, 0.03), (0.33, BY - 0.17, BZ + 0.03), M["plastique"], rot=(0, 0, rad(-8)), biseau=0.012)
boite("PRP_tapis_souris", (0.24, 0.2, 0.003), (0.33, BY - 0.16, BZ + 0.0155), M["tissu"])
boite("PRP_carnet", (0.15, 0.21, 0.012), (-0.45, BY - 0.12, BZ + 0.02), M["carton"], rot=(0, 0, rad(12)), biseau=0.002)
cylindre("PRP_stylo", 0.004, 0.14, (-0.37, BY - 0.15, BZ + 0.028), M["plastique"], rot=(0, rad(90), rad(40)))
# retiré à la demande de Bruno (07/11/2026) : # cylindre("PRP_tasse", 0.042, 0.095, (-0.62, BY + 0.05, BZ + 0.062), M["ceramique"])
# retiré à la demande de Bruno (07/11/2026) : # cylindre("PRP_tasse_fond_cafe", 0.038, 0.002, (-0.62, BY + 0.05, BZ + 0.09), M["plastique"])
for i in range(4):
    boite(f"PRP_chemise_{i}", (0.24, 0.32, 0.008), (-0.58, BY + 0.2, BZ + 0.02 + i * 0.009), M["carton"] if i % 2 else M["papier"],
          rot=(0, 0, rad(-4 + i * 3)))
boite("PRP_feuille_libre", (0.21, 0.297, 0.001), (0.62, BY - 0.12, BZ + 0.0155), M["papier"], rot=(0, 0, rad(-15)))
lampe = vide("PRP_lampe", (-0.74, BY + 0.25, BZ + 0.015))
cylindre("PRP_lampe_socle", 0.07, 0.02, (0, 0, 0.01), M["metal"], parent=lampe)
boite("PRP_lampe_bras1", (0.015, 0.015, 0.4), (0.06, 0, 0.2), M["metal"], rot=(0, rad(18), 0), parent=lampe)
boite("PRP_lampe_bras2", (0.015, 0.015, 0.35), (0.2, 0, 0.42), M["metal"], rot=(0, rad(70), 0), parent=lampe)
abat = cylindre("PRP_lampe_tete", 0.06, 0.11, (0.36, 0, 0.33), M["metal"], rot=(0, rad(-35), 0), parent=lampe)
import bmesh as _bm
_b = _bm.new(); _b.from_mesh(abat.data)
for v in _b.verts:
    if v.co.z > 0:
        v.co.x *= 0.45; v.co.y *= 0.45
_b.to_mesh(abat.data); _b.free()
boite("PRP_cable_ecran", (0.008, 0.008, 0.72), (EX + 0.05, EY + 0.12, 0.38), M["plastique"], rot=(rad(4), 0, 0))

# ---------------------------------------------------------------- la chaise
CH = vide("PRP_chaise", (0.12, BY - 0.85, 0), rot=(0, 0, rad(-14)))
for i in range(5):
    a = rad(i * 72 + 18)
    br = boite(f"PRP_chaise_branche_{i}", (0.3, 0.04, 0.03), (math.cos(a) * 0.15, math.sin(a) * 0.15, 0.075), M["plastique"],
               rot=(0, 0, a), biseau=0.008, parent=CH)
    cylindre(f"PRP_chaise_roulette_{i}", 0.025, 0.022, (math.cos(a) * 0.29, math.sin(a) * 0.29, 0.03), M["plastique"],
             rot=(rad(90), 0, a), parent=CH)
cylindre("PRP_chaise_verin", 0.024, 0.34, (0, 0, 0.26), M["acier"], parent=CH)
boite("PRP_chaise_assise", (0.5, 0.48, 0.09), (0, 0.02, 0.47), M["tissu"], biseau=0.04, parent=CH)
dos = boite("PRP_chaise_dossier", (0.46, 0.07, 0.58), (0, -0.25, 0.84), M["tissu"], rot=(rad(-9), 0, 0), biseau=0.045, parent=CH)
dos.modifiers["biseau"].segments = 5
cb = dos.modifiers.new("galbe", "SIMPLE_DEFORM"); cb.deform_method = "BEND"; cb.deform_axis = "Z"; cb.angle = rad(-28)
boite("PRP_chaise_lien", (0.06, 0.18, 0.04), (0, -0.2, 0.46), M["metal"], parent=CH)
for sx in (-1, 1):
    boite(f"PRP_chaise_accoudoir_pied_{sx}", (0.03, 0.03, 0.2), (sx * 0.27, 0.0, 0.58), M["plastique"], parent=CH)
    boite(f"PRP_chaise_accoudoir_{sx}", (0.06, 0.26, 0.025), (sx * 0.27, 0.02, 0.69), M["plastique"], biseau=0.01, parent=CH)


# ---------------------------------------------------------------- traces de vie (un bureau réel n'est jamais propre)
for i, (dx, dz, ang) in enumerate(((-0.27, 0.12, 4), (-0.27, 0.05, -6), (0.27, 0.13, 3))):
    boite(f"PRP_postit_{i}", (0.065, 0.002, 0.065), (EX + dx, EY - 0.025, BZ + 0.35 + dz), M["papier"], rot=(0, rad(ang), 0))
cylindre("PRP_corbeille", 0.13, 0.3, (0.95, BY + 0.05, 0.15), matiere("MAT_corbeille_mate", (0.03, 0.032, 0.035), rugo=0.95), sommets=32)
boite("PRP_multiprise", (0.3, 0.05, 0.035), (-0.2, BY + 0.3, 0.018), M["plastique"], rot=(0, 0, rad(8)), biseau=0.006)
for i, (x, y, l, a) in enumerate(((-0.35, BY + 0.15, 0.6, 30), (-0.05, BY + 0.2, 0.45, -50), (-0.45, BY + 0.05, 0.4, 75))):
    boite(f"PRP_cable_sol_{i}", (l, 0.007, 0.007), (x, y, 0.004), M["plastique"], rot=(0, 0, rad(a)))
# le câble d'alimentation : il quitte le bureau et s'enfonce dans le noir, loin derrière
pts = [(-0.2, BY + 0.3, 0.006), (-0.6, BY + 1.2, 0.006), (-0.4, BY + 3.0, 0.006), (-1.3, BY + 7.0, 0.006), (-1.0, BY + 18.0, 0.006)]
cu = bpy.data.curves.new("PRP_cable_long", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.006; cu.bevel_resolution = 3
sp = cu.splines.new("NURBS"); sp.points.add(len(pts) - 1)
for pt, co in zip(sp.points, pts):
    pt.co = (*co, 1)
sp.order_u = 3; sp.use_endpoint_u = True
cu.materials.append(M["plastique"])
lier(bpy.data.objects.new("PRP_cable_long", cu), "PRP")
veste = boite("PRP_veste", (0.44, 0.09, 0.42), (0.0, -0.31, 0.88), M["tissu"], rot=(rad(-6), 0, 0), biseau=0.04, parent=CH)
veste.modifiers["biseau"].segments = 4
vg = veste.modifiers.new("plis", "DISPLACE")
tx = bpy.data.textures.new("TEX_plis", "CLOUDS"); tx.noise_scale = 0.12
vg.texture = tx; vg.strength = 0.03
sub = veste.modifiers.new("lisse", "SUBSURF"); sub.levels = 2; sub.render_levels = 2
veste.modifiers.move(veste.modifiers.find("lisse"), 0)

# ---------------------------------------------------------------- lumière
w = bpy.data.worlds.new("WLD_noir")
sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.0012, 0.0015, 0.0022, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0


def lumiere(nom, type_, energie, couleur, pos, rot=(0, 0, 0), **kw):
    d = bpy.data.lights.new(nom, type_)
    d.energy = energie; d.color = couleur
    for k, v in kw.items():
        setattr(d, k, v)
    o = bpy.data.objects.new(nom, d)
    o.location = pos; o.rotation_euler = rot
    lier(o, "LGT")
    return o


# clé : une lumière froide, haute, étroite, juste au-dessus du bureau (légèrement en arrière) ; un îlot
# placée un peu derrière le bureau : elle dessine le contour de la chaise et du bureau sans écraser le plateau
lumiere("LGT_key_ilot", "SPOT", 420.0, (0.70, 0.80, 1.0), (0.05, BY + 0.95, 5.0),
        rot=(rad(-11), 0, 0), spot_size=rad(38), spot_blend=0.45, shadow_soft_size=0.2)
# pratique : l'écran, tourné vers le bureau et vers nous
lumiere("LGT_practical_ecran", "AREA", 6.0, (0.72, 0.8, 0.95), (EX, EY - 0.06, BZ + 0.355),
        rot=(rad(-90), 0, 0), shape="RECTANGLE", size=0.6, size_y=0.34)

if not A.sans_brume:
    # brume bornée au cône de lumière, pour lire le faisceau sans laiter l'image
    vol = boite("ENV_brume", (4.5, 4.5, 5.0), (0, BY, 2.5), bpy.data.materials.new("MAT_brume"), "ENV")
    mb = vol.data.materials[0]
    mb.use_nodes = True
    nn = mb.node_tree.nodes; ll = mb.node_tree.links
    nn.remove(nn["Principled BSDF"])
    pv = nn.new("ShaderNodeVolumePrincipled")
    pv.inputs["Density"].default_value = 0.014
    pv.inputs["Anisotropy"].default_value = 0.5
    pv.inputs["Color"].default_value = (0.8, 0.85, 0.95, 1)
    ll.new(pv.outputs[0], nn["Material Output"].inputs["Volume"])

# ---------------------------------------------------------------- caméra (vue subjective)
cam_d = bpy.data.cameras.new("CAM_pov")
cam_d.lens = 30
cam_d.sensor_width = 36
cam_d.clip_start = 0.05
cam_d.dof.use_dof = True
cam_d.dof.aperture_fstop = 2.8
cam = lier(bpy.data.objects.new("CAM_pov", cam_d), "CAM")
sc.camera = cam
cible_focus = vide("CAM_point_net", (EX - 0.05, EY - 0.3, BZ + 0.3), "CAM")
cam_d.dof.focus_object = cible_focus

sc.render.fps = 24
sc.frame_start, sc.frame_end = 1, 120


def viser(depuis, vers, roulis=0.0):
    d = Vector(vers) - Vector(depuis)
    q = d.to_track_quat("-Z", "Y")
    e = q.to_euler()
    e.rotate_axis("Z", rad(roulis))
    return e


DEPART = (0.55, BY - 7.2, 1.62)
ARRIVEE = (0.18, BY - 1.85, 1.58)
VISEE_D = (0.05, BY, 0.95)
VISEE_A = (0.06, BY + 0.05, 0.74)
# marche : 5 points clés, petit balancement vertical (pas) et latéral, roulis discret
pas = 7
for f in range(1, 121, 6):
    t = (f - 1) / 119
    lisse = t * t * (3 - 2 * t)
    pos = Vector(DEPART).lerp(Vector(ARRIVEE), lisse)
    phase = t * pas * 2 * math.pi
    pos.z += 0.012 * math.sin(phase) * (1 - lisse * 0.6)
    pos.x += 0.008 * math.sin(phase / 2)
    vise = Vector(VISEE_D).lerp(Vector(VISEE_A), lisse)
    cam.location = pos
    cam.rotation_euler = viser(pos, vise, roulis=0.7 * math.sin(phase / 2))
    cam.keyframe_insert("location", frame=f)
    cam.keyframe_insert("rotation_euler", frame=f)
cible_focus.location = (EX - 0.05, EY - 0.3, BZ + 0.3)
cible_focus.keyframe_insert("location", frame=1)
cible_focus.location = (0.12, BY - 0.95, 0.85)
cible_focus.keyframe_insert("location", frame=120)

# ---------------------------------------------------------------- rendu
sc.render.engine = "CYCLES"
cy = sc.cycles
cy.samples = A.echantillons
cy.use_denoising = True
cy.max_bounces = 6
cy.volume_bounces = 0
cy.volume_step_rate = 4.0
sc.render.resolution_x, sc.render.resolution_y = A.largeur, A.hauteur
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.view_settings.view_transform = "AgX"
try:
    sc.view_settings.look = "AgX - Medium High Contrast"
except TypeError:
    pass
sc.view_settings.exposure = 0.3
sc.render.image_settings.file_format = "PNG"

# processeur graphique NVIDIA si disponible
try:
    pref = bpy.context.preferences.addons["cycles"].preferences
    for dt in ("OPTIX", "CUDA"):
        try:
            pref.compute_device_type = dt
            pref.get_devices()
            gpus = [d for d in pref.devices if d.type == dt]
            if gpus:
                for d in pref.devices:
                    d.use = d.type == dt
                cy.device = "GPU"
                print(f"[S01] rendu sur {dt} : {[d.name for d in gpus]}")
                break
        except TypeError:
            continue
except Exception as e:
    print("[S01] GPU indisponible, rendu CPU :", e)

os.makedirs(SORTIE, exist_ok=True)
os.makedirs(os.path.dirname(BLEND), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("[S01] scène enregistrée :", BLEND)

noms = {"depart": 1, "milieu": 60, "arrivee": 120}
for item in [x.strip() for x in A.rendu.split(",") if x.strip()]:
    f = noms.get(item, None) or int(item)
    sc.frame_set(f)
    nom = item if item in noms else f"f{f:03d}"
    sc.render.filepath = os.path.join(SORTIE, f"S01_{nom}{A.suffixe}.png")
    bpy.ops.render.render(write_still=True)
    print("[S01] rendu :", sc.render.filepath)
