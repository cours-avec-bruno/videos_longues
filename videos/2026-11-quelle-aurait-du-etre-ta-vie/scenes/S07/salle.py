"""S07 · La salle de surveillance des « simulateurs » (Blender, Eevee). Demande de Bruno (08/11/2026).

Après les funérailles du grand-père, on découvre qu'on regardait un écran : une salle sombre, un mur d'écrans où passent
les instants de la vie de Manoj, et deux personnes qui décident de la vie des autres. Elles parlent de lui ; c'est le
moment de « reprendre les rênes » : le premier choix posé au spectateur.

DA d'après la référence de Bruno : pénombre bleutée, reflets, personnages lisses en costume sombre, peau pâle, sans
visage détaillé ; une lumière ambrée en contrepoint. Les simulateurs sont des mannequins lisses (mannequin.py, lisse=True),
pour les distinguer des figurines à facettes de la vie de Manoj.

L'écran central est rempli au montage (montage.py) : chaque plan exporte ses quatre coins, image par image (JSON),
et un masque (rendu Workbench) pour ce qui passe devant.

Plans :
  revele   6,0 s  on recule depuis l'écran central (où brûle la lampe sur l'eau) : la salle apparaît
  large   10,0 s  derrière eux, lente dérive ; l'un montre l'écran
  epaule   8,0 s  par-dessus l'épaule : l'écran central, où le choix s'affiche
  regard   7,0 s  la seconde s'est tournée vers nous (vers le spectateur)

Plans de S08 (sorties dans medias/S08/salle) :
  s08_ecran  7,5 s  par-dessus leurs épaules, lente poussée vers l'écran central (la ligne « …n'a pas pu payer… »)
  s08_recul  4,5 s  de côté : il se recule dans sa chaise (« … Même ça. »), un mouvement continu (versions intermédiaires)
  s08_sara   4,0 s  elle, de trois quarts dos, devant l'écran (« Les choix changent les probabilités. »)

Lancer : "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b -P salle.py -- [--test] [--plans large,epaule]
"""
import argparse
import json
import math
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ICI = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.abspath(os.path.join(ICI, "..", ".."))
RACINE = os.path.abspath(os.path.join(VIDEO, "..", ".."))
sys.path.append(os.path.join(RACINE, "shared", "blender"))
import plateau as P  # noqa: E402
from mannequin import ORDRE, SQUELETTE, positions  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--test", action="store_true")
ap.add_argument("--plans", default="")
ap.add_argument("--refaire", action="store_true", help="réécrire les images déjà rendues")
A = ap.parse_args(argv)
rad = math.radians
FPS = 24
ECRANS = os.path.join(VIDEO, "medias", "S07", "ecrans")
SORTIE = os.path.join(VIDEO, "medias", "S07", "salle")
TEST = os.path.join(VIDEO, "medias", "S07", "salle_test")
os.makedirs(SORTIE, exist_ok=True)
os.makedirs(TEST, exist_ok=True)

sc = P.scene(test=A.test, fps=FPS, images=200)
M = P.materiaux()
w = sc.world.node_tree
w.nodes["Background"].inputs[0].default_value = (0.004, 0.006, 0.010, 1)
for n in w.nodes:
    if n.type == "PRINCIPLED_VOLUME":
        n.inputs["Density"].default_value = 0.012
        n.inputs["Color"].default_value = (0.7, 0.82, 1.0, 1)

COSTUME = P.materiau("costume", (0.018, 0.022, 0.032), 0.5, 0.35)
PEAU = P.materiau("peau_pale", (0.78, 0.76, 0.74), 0.42, 0.45)
CHEVEUX = P.materiau("cheveux", (0.012, 0.011, 0.011), 0.55, 0.3)
CHAISE = P.materiau("chaise", (0.62, 0.64, 0.66), 0.35, 0.4)
METAL = P.materiau("metal_sombre", (0.05, 0.05, 0.055), 0.3, 0.5, metal=1.0)
MUR = P.materiau("mur_beton", (0.012, 0.014, 0.018), 0.8, 0.2)
SOL = P.materiau("sol_salle", (0.02, 0.022, 0.028), 0.12, 0.6)
CONSOLE = P.materiau("console", (0.03, 0.033, 0.04), 0.3, 0.5)
CHROME = P.materiau("chrome", (0.9, 0.92, 0.95), 0.05, 0.8, metal=1.0)      # Bruno : un peu de chrome dans le décor


def ecran_mat(nom, image=None, force=2.4, teinte=(1, 1, 1)):
    m = bpy.data.materials.new(nom)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.remove(n["Principled BSDF"])
    e = n.new("ShaderNodeEmission")
    e.inputs[1].default_value = force
    if image:
        t = n.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(os.path.join(ECRANS, image))
        mix = n.new("ShaderNodeMixRGB")
        mix.blend_type = "MULTIPLY"
        mix.inputs[0].default_value = 1.0
        mix.inputs[2].default_value = (*teinte, 1)
        m.node_tree.links.new(t.outputs[0], mix.inputs[1])
        m.node_tree.links.new(mix.outputs[0], e.inputs[0])
    else:
        e.inputs[0].default_value = (*teinte, 1)
    m.node_tree.links.new(e.outputs[0], n["Material Output"].inputs[0])
    return m


def ecran(nom, centre, larg, image, force=2.2, teinte=(0.92, 0.96, 1.0)):
    """Un écran mural : un cadre sombre et une dalle lumineuse (16:9), face à la salle (-Y)."""
    x, y, z = centre
    h = larg * 9 / 16
    P.boite(f"cadre_{nom}", (larg + 0.06, 0.05, h + 0.06), (x, y + 0.03, z), CHROME, biseau=0.01)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y - 0.0, z), rotation=(rad(90), 0, 0))
    d = bpy.context.object
    d.name = f"dalle_{nom}"
    d.scale = (larg, h, 1)
    bpy.ops.object.transform_apply(scale=True)
    d.data.materials.append(ecran_mat(f"mat_{nom}", image, force, teinte))
    # l'UV de la dalle : l'image vue de face (le plan tourné de 90° regarde -Y)
    return d


# ---------------------------------------------------------------- la pièce
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
s_ = bpy.context.object
s_.scale = (14, 14, 1)
s_.data.materials.append(SOL)
P.boite("mur_fond", (9, 0.2, 4.2), (0, 3.6, 2.1), MUR)
P.boite("mur_g", (0.2, 8, 4.2), (-4.4, 0, 2.1), MUR)
P.boite("mur_d", (0.2, 8, 4.2), (4.4, 0, 2.1), MUR)
P.boite("plafond", (9, 8, 0.2), (0, 0, 4.2), MUR)
# le mur d'écrans : un grand au centre (rempli au montage) et des petits autour
ECRANS_MUR = [
    ("g1", (-2.25, 3.45, 2.35), 1.05, "s06_1an.png"), ("g2", (-2.25, 3.45, 1.55), 1.05, "reel_village.png"),
    ("g3", (-2.25, 3.45, 0.85), 1.05, "s06_3ans.png"), ("g4", (-1.15, 3.45, 2.55), 0.95, "s07_ecole.png"),
    ("d1", (2.25, 3.45, 2.35), 1.05, "fiche.png"), ("d2", (2.25, 3.45, 1.55), 1.05, "s06_4ans.png"),
    ("d3", (2.25, 3.45, 0.85), 1.05, "reel_feu.png"), ("d4", (1.15, 3.45, 2.55), 0.95, "s07_huit.png"),
    ("h1", (0.0, 3.45, 2.75), 0.95, "portrait.png"), ("h2", (-3.3, 3.45, 1.9), 0.9, "reel_ecole.png"),
    ("h3", (3.3, 3.45, 1.9), 0.9, "s07_dette.png"),
]
for nom, c, l, im in ECRANS_MUR:
    ecran(nom, c, l, im, force=1.6)
PRINCIPAL = ecran("principal", (0.0, 3.42, 1.42), 2.05, "s07_funerailles.png", force=1.4, teinte=(0.75, 0.82, 0.95))
# la console et ses deux petits écrans
P.boite("console", (3.4, 0.85, 0.07), (0, 1.75, 0.76), CONSOLE, biseau=0.01)
P.boite("console_face", (3.4, 0.05, 0.7), (0, 1.35, 0.4), CONSOLE)
for k, x in enumerate((-0.6, 0.65)):
    P.boite(f"clavier_{k}", (0.46, 0.16, 0.02), (x, 1.62, 0.805), METAL, biseau=0.004)
    kl = ecran_mat(f"touches_{k}", None, 0.4, (0.35, 0.6, 1.0))
    P.boite(f"touches_{k}", (0.42, 0.12, 0.004), (x, 1.62, 0.817), kl)
    ecran(f"poste_{k}", (x + (0.35 if k == 0 else 0.05), 2.05, 1.02), 0.5, ("s06_5ans.png", "s07_priere.png")[k], force=1.2)
# le chrome : un liseré le long de la console, des montants entre les écrans, deux rails au plafond
P.boite("liseré_console", (3.42, 0.03, 0.025), (0, 1.33, 0.79), CHROME)
P.boite("liseré_console_bas", (3.42, 0.03, 0.02), (0, 1.33, 0.06), CHROME)
for k, x in enumerate((-2.85, -1.7, 1.7, 2.85)):
    P.boite(f"montant_{k}", (0.07, 0.07, 3.6), (x, 3.42, 1.8), CHROME, biseau=0.015)
for k, x in enumerate((-1.2, 1.2)):
    P.cylindre(f"rail_{k}", 0.025, 7.5, (x, 0.0, 3.95), CHROME, rot=(90, 0, 0), sommets=16)
    for j in range(3):
        P.cylindre(f"spot_rail_{k}_{j}", 0.05, 0.12, (x, -1.5 + 1.5 * j, 3.86), CHROME, sommets=20)
P.boite("plinthe_chrome", (8.8, 0.02, 0.05), (0, 3.49, 0.025), CHROME)
# une petite lampe ambrée, comme dans la référence (le seul point chaud)
P.lampe("lampe_ambre", (-3.6, 2.6, 1.1), 40, (1.0, 0.55, 0.2), 0.15)
P.sphere("ampoule_ambre", 0.05, (-3.6, 2.6, 1.1), P.emission("ambre", (1.0, 0.55, 0.2), 12)[0])
# la lueur des écrans sur les personnages, un contre-jour bleu, un peu de lumière froide d'en haut
bpy.ops.object.light_add(type="AREA", location=(0, 3.0, 1.6))
L = bpy.context.object
L.data.energy = 110
L.data.size = 4.0
L.data.color = (0.65, 0.78, 1.0)
L.rotation_euler = (rad(90), 0, 0)
P.projecteur("haut_salle", (-1.0, -1.5, 3.8), (0, 1.2, 0.8), 120, (0.6, 0.72, 1.0), 36, flou=0.6)
# S08 : la lueur de l'écran central sur leurs visages (seulement dans les plans de S08)
bpy.ops.object.light_add(type="AREA", location=(0, 2.7, 1.45))
LUEUR = bpy.context.object
LUEUR.data.energy = 38
LUEUR.data.size = 2.0
LUEUR.data.color = (0.7, 0.82, 1.0)
LUEUR.rotation_euler = (rad(-90), 0, 0)
P.projecteur("contre_salle", (2.8, 3.0, 3.0), (0, 1.0, 1.0), 260, (0.5, 0.75, 1.0), 30)


# ---------------------------------------------------------------- les simulateurs (lisses, en costume)
ASSIS_BUREAU = {"hanche_g": (-90, 0, -6), "genou_g": (90, 0, 0), "hanche_d": (-90, 0, 6), "genou_d": (90, 0, 0),
                "torse": (6, 0, 0), "epaule_g": (-62, 0, 6), "coude_g": (-45, 0, 0), "epaule_d": (-62, 0, -6), "coude_d": (-45, 0, 0)}
MONTRE = dict(ASSIS_BUREAU, epaule_d=(-112, 0, -14), coude_d=(-4, 0, 0), cou=(-6, 0, 0), torse=(2, 0, 0))
TOURNEE = {"hanche_g": (-90, 0, -10), "genou_g": (90, 0, 0), "hanche_d": (-90, 0, 10), "genou_d": (90, 0, 0),
           "taille": (-4, 0, 0), "cou": (2, 0, 0), "epaule_g": (-30, 0, 10), "coude_g": (-70, 0, 0),
           "epaule_d": (-30, 0, -10), "coude_d": (-70, 0, 0)}


def articulations(pose_):
    pts = positions(pose_)
    bas = min(pts[k].z - SQUELETTE[k][2][0] * 0.8 for k in ORDRE)
    for k in pts:
        pts[k].z -= bas
    return pts


def simulateur(nom, pose_, pos, angle, cheveux=True):
    o = P.perso(nom, pose_, 1.0, False, COSTUME, pos, angle)
    o.modifiers["peau"].use_smooth_shade = True
    o.modifiers.remove(o.modifiers["facettes"])
    for p in o.data.polygons:
        p.use_smooth = True
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.convert(target="MESH")
    o.data.materials.append(PEAU)
    pts = articulations(pose_)
    cou_z = pts["cou"].z + 0.02
    mains = [pts["main_g"], pts["main_d"], pts["poignet_g"], pts["poignet_d"]]
    for poly in o.data.polygons:
        c = poly.center
        if c.z > cou_z or min((c - m).length for m in mains) < 0.075:
            poly.material_index = 1
        poly.use_smooth = True
    if cheveux:
        tete = o.matrix_world @ pts["crane"]
        hc = P.sphere(nom + "_cheveux", 0.105, tete + Vector((0, 0, 0.012)), CHEVEUX, echelle=(1.0, 1.08, 0.62), sub=3)
        hc.parent = o
        hc.matrix_parent_inverse = o.matrix_world.inverted()
    return o


def chaise(nom, pos, angle):
    x, y = pos
    objs = [P.boite(nom + "_assise", (0.5, 0.5, 0.08), (x, y, 0.44), CHAISE, biseau=0.03),
            P.boite(nom + "_dos", (0.48, 0.07, 0.62), (x, y + 0.27, 0.82), CHAISE, rot=(-8, 0, 0), biseau=0.03),
            P.cylindre(nom + "_pied", 0.03, 0.36, (x, y, 0.22), CHROME, sommets=16)]
    for k in range(5):
        a = rad(72 * k)
        objs.append(P.boite(f"{nom}_branche_{k}", (0.32, 0.04, 0.03), (x + 0.16 * math.cos(a), y + 0.16 * math.sin(a), 0.05),
                            CHROME, rot=(0, 0, math.degrees(a))))
    piv = bpy.data.objects.new(nom, None)
    sc.collection.objects.link(piv)
    piv.location = (x, y, 0)
    for o in objs:
        o.parent = piv
        o.matrix_parent_inverse = piv.matrix_world.inverted()
    piv.rotation_euler.z = rad(angle)
    return piv


# lui (celui qui a suivi Manoj) à gauche, elle (qui veut reprendre la main) à droite ; ils regardent le mur (+Y)
S1_POS, S2_POS = (-0.62, 0.95), (0.68, 1.0)
chaise("chaise_1", S1_POS, 0)
s1_a = simulateur("simulateur_1", ASSIS_BUREAU, (S1_POS[0], S1_POS[1] - 0.05, 0), 180)
s1_b = simulateur("simulateur_1_montre", MONTRE, (S1_POS[0], S1_POS[1] - 0.05, 0), 180)
ch2 = chaise("chaise_2", S2_POS, 0)
s2_a = simulateur("simulateur_2", ASSIS_BUREAU, (S2_POS[0], S2_POS[1] - 0.05, 0), 180)
ch2b = chaise("chaise_2_tournee", S2_POS, 150)
s2_b = simulateur("simulateur_2_tournee", TOURNEE, (S2_POS[0] + 0.03, S2_POS[1] + 0.02, 0), 180 + 150)
# S08 : il se recule dans sa chaise ; des versions intermédiaires, une par image, pour un mouvement continu
RECULE = dict(ASSIS_BUREAU, torse=(-18, 0, 0), taille=(-8, 0, 0), cou=(10, 0, 0), epaule_g=(-24, 0, 8), coude_g=(-62, 0, 0),
              epaule_d=(-24, 0, -8), coude_d=(-62, 0, 0))
N_RECUL = 9


def melange(a, b, q):
    out = {}
    for k in set(a) | set(b):
        va, vb = a.get(k, (0, 0, 0)), b.get(k, (0, 0, 0))
        out[k] = tuple(x + (y - x) * q for x, y in zip(va, vb))
    return out


RECUL = [s1_a] + [simulateur(f"simulateur_1_recul_{k}", melange(ASSIS_BUREAU, RECULE, (k / N_RECUL) ** 1), (S1_POS[0], S1_POS[1] - 0.05, 0), 180)
                  for k in range(1, N_RECUL + 1)]
VERSIONS = {  # quels objets sont visibles dans quel plan
    "revele": [s1_a, s2_a, ch2], "large": [s1_b, s2_a, ch2], "epaule": [s1_a, s2_a, ch2], "regard": [s1_a, s2_b, ch2b],
    "s08_ecran": [s1_a, s2_a, ch2], "s08_recul": [s1_a, s2_a, ch2], "s08_sara": [RECUL[-1], s2_a, ch2],
}
TOUTES = [s1_a, s1_b, s2_a, s2_b, ch2, ch2b] + RECUL[1:]
T_RECUL = (1.15, 2.05)           # le mouvement (s), dans le plan s08_recul


def montrer(objets):
    for o in TOUTES:
        o.animation_data_clear()
        vis = o in objets
        o.hide_render = not vis
        for c in o.children:
            c.hide_render = not vis


# ---------------------------------------------------------------- les plans
PLANS = {
    #  nom      : (position début,        position fin,          visée début,          visée fin,         focale, durée)
    "revele":   ((0.0, 2.05, 1.42),       (-1.7, -1.9, 1.7),     (0.0, 3.42, 1.42),    (0.05, 2.6, 1.25), 30, 6.0),
    "large":    ((-1.9, -1.7, 1.7),       (-0.7, -2.0, 1.55),    (0.0, 2.6, 1.25),     (0.1, 2.8, 1.3),   30, 10.0),
    "epaule":   ((-1.05, 0.35, 1.62),     (-0.8, 0.75, 1.55),    (0.05, 3.42, 1.42),   (0.05, 3.42, 1.42), 35, 8.0),
    "regard":   ((1.75, -0.75, 1.3),      (1.45, -0.35, 1.25),   (0.66, 1.05, 1.12),   (0.66, 1.05, 1.15), 45, 7.0),
    "s08_ecran": ((0.05, -0.55, 1.74),    (0.02, 0.45, 1.62),    (0.0, 3.42, 1.40),    (0.0, 3.42, 1.42), 32, 7.5),
    "s08_recul": ((-2.05, 2.25, 1.26),    (-1.95, 2.1, 1.22),    (-0.6, 0.95, 1.02),   (-0.62, 0.9, 1.0), 42, 4.5),
    "s08_sara":  ((2.35, 0.9, 1.3),       (2.2, 0.95, 1.28),     (0.75, 1.55, 1.18),   (0.7, 1.65, 1.2),  32, 4.0),
}


def ease(p):
    p = min(1.0, max(0.0, p))
    return p * p * p * (p * (p * 6 - 15) + 10)


bpy.ops.object.camera_add()
cam = bpy.context.object
sc.camera = cam
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.2
foc = bpy.data.objects.new("point_net", None)
sc.collection.objects.link(foc)
cam.data.dof.focus_object = foc
COINS = [Vector(v) for v in ((-1.025, 3.40, 1.42 + 0.5766), (1.025, 3.40, 1.42 + 0.5766),
                             (1.025, 3.40, 1.42 - 0.5766), (-1.025, 3.40, 1.42 - 0.5766))]


def preparer(nom):
    p0, p1, v0, v1, focale, duree = PLANS[nom]
    cam.animation_data_clear()
    foc.animation_data_clear()
    cam.data.lens = focale
    n = int(round(duree * FPS))
    sc.frame_start, sc.frame_end = 1, n
    for f in range(1, n + 1):
        q = ease((f - 1) / max(1, n - 1)) if nom in ("revele", "s08_ecran") else (f - 1) / max(1, n - 1)
        pos = Vector(p0).lerp(Vector(p1), q)
        vis = Vector(v0).lerp(Vector(v1), q)
        cam.location = pos
        cam.rotation_euler = (vis - pos).to_track_quat("-Z", "Y").to_euler()
        foc.location = vis if nom != "revele" or q > 0.5 else Vector((0, 3.42, 1.42))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        foc.keyframe_insert("location", frame=f)
    montrer(VERSIONS[nom])
    LUEUR.hide_render = not nom.startswith("s08")
    if nom == "s08_recul":             # une version par image pendant le mouvement (ease, sans à-coup)
        for f in range(1, n + 1):
            t = (f - 1) / FPS
            k = round(ease((t - T_RECUL[0]) / (T_RECUL[1] - T_RECUL[0])) * N_RECUL)
            for i, o in enumerate(RECUL):
                o.hide_render = i != k
                o.keyframe_insert("hide_render", frame=f)
                for c in o.children:
                    c.hide_render = i != k
                    c.keyframe_insert("hide_render", frame=f)
    return n


def coins_ecran():
    rx, ry = sc.render.resolution_x, sc.render.resolution_y
    out = []
    for c in COINS:
        v = world_to_camera_view(sc, cam, c)
        out.append((v.x * rx, (1 - v.y) * ry))
    return out


def rendre_masque(chemin):
    """Le masque de l'écran central (ce qui passe devant est noir) : un rendu Workbench, très rapide."""
    eng = sc.render.engine
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "FLAT"
    sh.color_type = "OBJECT"
    for o in bpy.data.objects:
        if o.type == "MESH":
            o.color = (1, 1, 1, 1) if o.name == "dalle_principal" else (0, 0, 0, 1)
    sc.render.filepath = chemin
    vt = sc.view_settings.view_transform
    sc.view_settings.view_transform = "Standard"
    bpy.ops.render.render(write_still=True)
    sc.view_settings.view_transform = vt
    sc.render.engine = eng


bpy.ops.wm.save_as_mainfile(filepath=os.path.join(VIDEO, "medias", "blender", "S07_salle.blend"))
noms = [p.strip() for p in A.plans.split(",") if p.strip()] or list(PLANS)
for nom in noms:
    n = preparer(nom)
    if A.test:
        for f in sorted({1, n // 2 + 1, n}):
            sc.frame_set(f)
            sc.render.filepath = os.path.join(TEST, f"{nom}_{f:03d}.png")
            bpy.ops.render.render(write_still=True)
        continue
    d = os.path.join(SORTIE if not nom.startswith("s08") else os.path.join(VIDEO, "medias", "S08", "salle"), nom)
    os.makedirs(d, exist_ok=True)
    os.makedirs(os.path.join(d, "masque"), exist_ok=True)
    coins = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        coins[f] = coins_ecran()
        chemin = os.path.join(d, f"{f:04d}.png")
        if A.refaire or not os.path.exists(chemin):
            sc.render.filepath = chemin
            bpy.ops.render.render(write_still=True)
        cm = os.path.join(d, "masque", f"{f:04d}.png")
        if A.refaire or not os.path.exists(cm):
            rendre_masque(cm)
    json.dump(coins, open(os.path.join(d, "coins.json"), "w"))
    print(f"[S07 salle] {nom} : {n} images")
print("[S07 salle] terminé")
