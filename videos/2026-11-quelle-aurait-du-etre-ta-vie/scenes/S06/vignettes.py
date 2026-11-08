"""S06 · Les années qui passent, passage 1 (0 -> 5 ans) : cinq petites scènes en 3D (Blender, Eevee).

Demande de Bruno (08/11/2026) : sortir du look « interface », exploiter la 3D avec des mannequins simples sans visage
(ses deux références : figurines rouges à facettes, une pièce sombre, quelques reflets), des transitions travaillées.

Le principe : cinq îlots de lumière posés sur un grand sol sombre et brillant, alignés comme des tableaux de théâtre.
La caméra glisse de l'un à l'autre dans le noir : chaque année s'allume quand on arrive, s'éteint quand on repart.
Manoj est le seul personnage rouge (l'humain, la couleur chaude de la vidéo) ; les autres sont en argile grise.

  1 an   sur une natte, sa mère penchée vers lui : son premier mot
  2 ans  accroupi au bord d'une flaque de boue (qui reflète)
  3 ans  la nuit, sa grand-mère sur un tabouret raconte ; une petite lampe à huile entre eux
  4 ans  le foyer de terre, les rotis sur la plaque, sa mère accroupie ; lui, une assiette en métal sur les genoux
  5 ans  il court avec les autres enfants, au coucher du soleil

Lancer sur le PC :
  "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b -P vignettes.py -- [--test] [--images 1-313]
Sorties (hors Git) : medias/S06/3d/####.png ; le .blend dans medias/blender/S06_vignettes.blend
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

ICI = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.abspath(os.path.join(ICI, "..", ".."))
RACINE = os.path.abspath(os.path.join(VIDEO, "..", ".."))
sys.path.append(os.path.join(RACINE, "shared", "blender"))
from mannequin import mannequin, materiau, positions, SQUELETTE, ORDRE  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--test", action="store_true", help="une image fixe par scène, en 960 x 540")
ap.add_argument("--images", default="", help="plage d'images, ex. 1-120")
A = ap.parse_args(argv)
rad = math.radians

SORTIE = os.path.join(VIDEO, "medias", "S06", "3d")
TEST = os.path.join(VIDEO, "medias", "S06", "3d_test")
os.makedirs(SORTIE, exist_ok=True)
os.makedirs(TEST, exist_ok=True)

# ---------------------------------------------------------------- temps (partagés avec passage.py)
sys.path.append(ICI)
from temps_s06 import DEBUT, DUREE, FPS, N, N_SCENES, TENUES, TRAJET, arrivee  # noqa: E402
ECART = 8.0          # distance entre deux scènes (m)


# ---------------------------------------------------------------- scène vide
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, N
sc.render.resolution_x, sc.render.resolution_y = (960, 540) if A.test else (1920, 1080)
ee = sc.eevee
for attr, val in (("use_raytracing", True), ("taa_render_samples", 64), ("use_shadows", True),
                  ("volumetric_tile_size", "8"), ("volumetric_samples", 64), ("use_volumetric_shadows", True)):
    try:
        setattr(ee, attr, val)
    except Exception as e:
        print("[S06] réglage ignoré", attr, e)
try:
    ee.ray_tracing_options.resolution_scale = "1"
except Exception:
    pass
sc.render.use_motion_blur = True
try:
    sc.render.motion_blur_shutter = 0.6
except Exception:
    pass
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Medium High Contrast"

# le monde : presque noir, et une brume très légère pour que les faisceaux se voient
w = bpy.data.worlds.new("monde")
sc.world = w
w.use_nodes = True
nt = w.node_tree
nt.nodes["Background"].inputs[0].default_value = (0.0025, 0.0028, 0.0035, 1)
vol = nt.nodes.new("ShaderNodeVolumePrincipled")
vol.inputs["Density"].default_value = 0.012
vol.inputs["Anisotropy"].default_value = 0.55
nt.links.new(vol.outputs[0], nt.nodes["World Output"].inputs["Volume"])

# matériaux
ROUGE = materiau("manoj", (0.62, 0.07, 0.035), rugosite=0.5, brillance=0.45)
ARGILE = materiau("argile", (0.42, 0.40, 0.37), rugosite=0.62, brillance=0.3)
ARGILE_V = materiau("argile_vieille", (0.36, 0.345, 0.33), rugosite=0.7, brillance=0.25)
SOL = materiau("sol", (0.018, 0.018, 0.02), rugosite=0.16, brillance=0.6)
TERRE = materiau("terre", (0.16, 0.10, 0.06), rugosite=0.9, brillance=0.2)
TERRE_SECHE = materiau("terre_seche", (0.30, 0.20, 0.12), rugosite=0.92, brillance=0.15)
NATTE = materiau("natte", (0.30, 0.17, 0.08), rugosite=0.8, brillance=0.2)
NATTE2 = materiau("natte_raie", (0.10, 0.12, 0.20), rugosite=0.8, brillance=0.2)
EAU = materiau("eau_boue", (0.035, 0.025, 0.018), rugosite=0.03, brillance=0.9)
BOIS = materiau("bois", (0.22, 0.13, 0.07), rugosite=0.6, brillance=0.3)
GLAISE = materiau("glaise", (0.34, 0.19, 0.10), rugosite=0.85, brillance=0.2)
FONTE = materiau("fonte", (0.03, 0.03, 0.03), rugosite=0.35, brillance=0.6)
ROTI = materiau("roti", (0.78, 0.62, 0.40), rugosite=0.8, brillance=0.2)
INOX = materiau("inox", (0.8, 0.8, 0.8), rugosite=0.18, brillance=0.5)
INOX.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0


def emission(nom, couleur, force):
    m = bpy.data.materials.new(nom)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.remove(n["Principled BSDF"])
    e = n.new("ShaderNodeEmission")
    e.inputs[0].default_value = (*couleur, 1)
    e.inputs[1].default_value = force
    m.node_tree.links.new(e.outputs[0], n["Material Output"].inputs[0])
    return m, e


def boite(nom, dims, pos, mat, rot=(0, 0, 0), biseau=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos, rotation=[rad(a) for a in rot])
    o = bpy.context.object
    o.name = nom
    o.scale = dims
    bpy.ops.object.transform_apply(scale=True)
    if biseau:
        b = o.modifiers.new("biseau", "BEVEL")
        b.width, b.segments = biseau, 2
    o.data.materials.append(mat)
    return o


def cylindre(nom, r, h, pos, mat, rot=(0, 0, 0), sommets=32, echelle=(1, 1, 1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=sommets, radius=r, depth=h, location=pos, rotation=[rad(a) for a in rot])
    o = bpy.context.object
    o.name = nom
    o.scale = echelle
    o.data.materials.append(mat)
    return o


def perso(nom, pose, ech, enfant, mat, pos, angle, au_sol=True):
    o = mannequin(nom, pose, echelle=ech, enfant=enfant, mat=mat, au_sol=au_sol)
    o.location = pos
    o.rotation_euler.z = rad(angle)       # 0 : il regarde la caméra ; 90 : vers +X ; -90 : vers -X
    return o


def projecteur(nom, pos, vise, energie, couleur=(1.0, 0.9, 0.78), angle=38, flou=0.35, rayon=0.25):
    bpy.ops.object.light_add(type="SPOT", location=pos)
    L = bpy.context.object
    L.name = nom
    L.data.energy = energie
    L.data.color = couleur
    L.data.spot_size = rad(angle)
    L.data.spot_blend = flou
    L.data.shadow_soft_size = rayon
    L.rotation_euler = (Vector(vise) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
    return L


def lampe(nom, pos, energie, couleur, rayon=0.05, type_="POINT"):
    bpy.ops.object.light_add(type=type_, location=pos)
    L = bpy.context.object
    L.name = nom
    L.data.energy = energie
    L.data.color = couleur
    L.data.shadow_soft_size = rayon
    return L


def estrade(i, rayon, mat):
    """Le socle d'une scène : un disque bas, posé sur le sol brillant."""
    o = cylindre(f"socle_{i}", rayon, 0.05, (i * ECART, 0, 0.025), mat, sommets=96)
    b = o.modifiers.new("biseau", "BEVEL")
    b.width, b.segments = 0.012, 2
    return o


# le grand sol sombre et brillant (les reflets)
bpy.ops.mesh.primitive_plane_add(size=1, location=(ECART * 2, 0, 0))
sol = bpy.context.object
sol.scale = (90, 60, 1)
sol.data.materials.append(SOL)

LUMIERES = {i: [] for i in range(N_SCENES)}      # (lumière, énergie pleine) par scène
H = 0.05                                          # hauteur du dessus d'un socle

# ---------------------------------------------------------------- 1 an : la natte, sa mère, son premier mot
x = 0 * ECART
estrade(0, 1.55, materiau("socle_bois", (0.07, 0.05, 0.04), rugosite=0.45, brillance=0.4))
boite("natte", (1.5, 1.0, 0.015), (x, 0.05, H + 0.008), NATTE)
for k_ in range(5):
    boite(f"natte_raie_{k_}", (1.5, 0.05, 0.016), (x, -0.35 + k_ * 0.2, H + 0.009), NATTE2)
MERE_1 = {"hanche_g": (-95, 0, 8), "genou_g": (150, 0, 0), "hanche_d": (-95, 0, -8), "genou_d": (150, 0, 0),
          "cheville_g": (-60, 0, 0), "cheville_d": (-60, 0, 0), "taille": (14, 0, 0), "torse": (18, 0, 0), "cou": (14, 0, 0),
          "epaule_g": (-55, 0, 10), "coude_g": (-45, 0, 0), "epaule_d": (-55, 0, -10), "coude_d": (-45, 0, 0)}
BEBE = {"hanche_g": (-90, 0, 20), "genou_g": (20, 0, 0), "hanche_d": (-90, 0, -20), "genou_d": (20, 0, 0),
        "cou": (-18, 0, 0), "epaule_g": (-140, 0, 22), "coude_g": (-20, 0, 0), "epaule_d": (-140, 0, -22), "coude_d": (-20, 0, 0)}
m1 = perso("mere_1", MERE_1, 1.0, False, ARGILE, (x + 0.42, 0.18, H + 0.015), -72)
b1 = perso("manoj_1", BEBE, 0.42, True, ROUGE, (x - 0.22, 0.02, H + 0.015), 72)
cylindre("pot_1", 0.11, 0.2, (x + 0.95, 0.55, H + 0.1), GLAISE, sommets=24)
LUMIERES[0] += [(projecteur("spot_1", (x - 1.2, -1.8, 3.4), (x + 0.1, 0.1, 0.3), 900, (1.0, 0.86, 0.68), 34), 900),
                (projecteur("contre_1", (x + 1.0, 2.6, 2.2), (x, 0.1, 0.5), 260, (0.75, 0.82, 1.0), 40), 260)]

# ---------------------------------------------------------------- 2 ans : la boue
x = 1 * ECART
BOUE = materiau("boue", (0.075, 0.045, 0.025), rugosite=0.55, brillance=0.5)
estrade(1, 1.6, BOUE)
# des mottes de boue autour de la flaque
import random as _r
_r.seed(4)
for k_ in range(9):
    a_ = _r.uniform(0, 6.28)
    d_ = _r.uniform(0.45, 0.85)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=_r.uniform(0.04, 0.08),
                                          location=(x + 0.3 + d_ * math.cos(a_), 0.05 + 0.7 * d_ * math.sin(a_), H))
    o = bpy.context.object
    o.scale = (1.3, 1.0, 0.45)
    o.rotation_euler.z = a_
    o.data.materials.append(BOUE)
# une flaque irrégulière : trois ovales qui se chevauchent
for k_, (dx, dy, r, ex, ey) in enumerate(((0.3, -0.05, 0.36, 1.25, 0.8), (0.62, 0.12, 0.24, 1.2, 0.9),
                                          (0.12, 0.16, 0.2, 1.1, 0.8))):
    cylindre(f"flaque_{k_}", r, 0.004, (x + dx, dy, H + 0.002 + 0.0003 * k_), EAU, sommets=40, echelle=(ex, ey, 1))
ENF_BOUE = {"taille": (25, 0, 0), "torse": (15, 0, 0), "cou": (15, 0, 0),
            "hanche_g": (-125, 0, 15), "genou_g": (150, 0, 0), "cheville_g": (-30, 0, 0),
            "hanche_d": (-125, 0, -15), "genou_d": (150, 0, 0), "cheville_d": (-30, 0, 0),
            "epaule_g": (-70, 0, 12), "coude_g": (-20, 0, 0), "epaule_d": (-60, 0, -12), "coude_d": (-35, 0, 0)}
perso("manoj_2", ENF_BOUE, 0.52, True, ROUGE, (x - 0.42, 0.02, H), 72)
LUMIERES[1] += [(projecteur("spot_2", (x + 1.6, -1.2, 3.2), (x, 0, 0.1), 600, (0.92, 0.95, 1.0), 32), 600),
                (projecteur("contre_2", (x - 0.8, 2.4, 2.0), (x, 0, 0.3), 200, (1.0, 0.85, 0.7), 40), 200)]

# ---------------------------------------------------------------- 3 ans : la nuit, les histoires de sa grand-mère
x = 2 * ECART
estrade(2, 1.55, TERRE)
GM = {"taille": (22, 0, 0), "torse": (20, 0, 0), "cou": (12, 0, 0),
      "hanche_g": (-100, 0, 10), "genou_g": (110, 0, 0), "hanche_d": (-100, 0, -10), "genou_d": (110, 0, 0),
      "epaule_g": (-20, 0, 8), "coude_g": (-70, 0, 0), "epaule_d": (-70, 0, -25), "coude_d": (-95, 0, 0)}
# le tabouret sous son bassin : on calcule la hauteur du bassin une fois les pieds au sol
pts = positions(GM)
bas = min(pts[j].z - SQUELETTE[j][2][0] * 0.8 for j in ORDRE)
haut_bassin = (pts["bassin"].z - bas) * 0.95 - SQUELETTE["bassin"][2][1] * 0.95
gm = perso("grand_mere", GM, 0.95, False, ARGILE_V, (x + 0.5, 0.25, H), -65)
boite("tabouret", (0.36, 0.36, haut_bassin), (x + 0.5 + 0.05, 0.25 + 0.02, H + haut_bassin / 2), BOIS, biseau=0.01)
ENF_ECOUTE = {"hanche_g": (-85, 0, 50), "genou_g": (-130, 0, 0), "hanche_d": (-85, 0, -50), "genou_d": (-130, 0, 0),
              "cou": (-16, 0, 0), "epaule_g": (-25, 0, 10), "coude_g": (-50, 0, 0), "epaule_d": (-25, 0, -10), "coude_d": (-50, 0, 0)}
perso("manoj_3", ENF_ECOUTE, 0.55, True, ROUGE, (x - 0.45, -0.05, H), 70)
# la lampe à huile (diya)
cylindre("diya", 0.06, 0.035, (x + 0.02, -0.25, H + 0.018), GLAISE, sommets=20, echelle=(1, 1.3, 1))
fl_m, fl_e = emission("flamme", (1.0, 0.55, 0.15), 30)
bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.012, depth=0.05, location=(x + 0.02, -0.25, H + 0.06))
bpy.context.object.data.materials.append(fl_m)
diya = lampe("diya_feu", (x + 0.02, -0.25, H + 0.1), 30, (1.0, 0.6, 0.25), 0.02)
LUMIERES[2] += [(diya, 30),
                (projecteur("lune_3", (x - 1.5, 2.8, 3.4), (x, 0, 0.4), 260, (0.55, 0.68, 1.0), 40), 260),
                (projecteur("spot_3", (x + 0.4, -2.2, 3.0), (x, 0, 0.4), 120, (1.0, 0.8, 0.6), 30), 120)]

# ---------------------------------------------------------------- 4 ans : le foyer, les rotis, sa mère
x = 3 * ECART
estrade(3, 1.6, TERRE)
boite("foyer", (0.55, 0.38, 0.26), (x + 0.1, 0.25, H + 0.13), GLAISE, biseau=0.04)
braise_m, braise_e = emission("braises", (1.0, 0.35, 0.06), 25)
boite("braises", (0.2, 0.02, 0.1), (x + 0.1, 0.05, H + 0.08), braise_m)
cylindre("tawa", 0.2, 0.02, (x + 0.1, 0.25, H + 0.275), FONTE, sommets=40)
cylindre("roti", 0.13, 0.008, (x + 0.12, 0.24, H + 0.29), ROTI, sommets=32)
for k_ in range(3):
    cylindre(f"buche_{k_}", 0.025, 0.5, (x + 0.05 + k_ * 0.05, -0.12, H + 0.04), BOIS, rot=(90, 0, 10 * (k_ - 1)), sommets=10)
feu = lampe("feu", (x + 0.1, -0.02, H + 0.12), 60, (1.0, 0.45, 0.12), 0.06)
MERE_4 = {"taille": (20, 0, 0), "torse": (10, 0, 0), "cou": (10, 0, 0),
          "hanche_g": (-130, 0, 20), "genou_g": (155, 0, 0), "cheville_g": (-25, 0, 0),
          "hanche_d": (-130, 0, -20), "genou_d": (155, 0, 0), "cheville_d": (-25, 0, 0),
          "epaule_g": (-40, 0, 10), "coude_g": (-40, 0, 0), "epaule_d": (-75, 0, -10), "coude_d": (-10, 0, 0)}
perso("mere_4", MERE_4, 1.0, False, ARGILE, (x + 0.75, 0.15, H), -80)
ENF_ASSIETTE = {"hanche_g": (-85, 0, 50), "genou_g": (-130, 0, 0), "hanche_d": (-85, 0, -50), "genou_d": (-130, 0, 0),
                "torse": (8, 0, 0), "cou": (18, 0, 0),
                "epaule_g": (-45, 0, -15), "coude_g": (-70, 0, 0), "epaule_d": (-45, 0, 15), "coude_d": (-70, 0, 0)}
perso("manoj_4", ENF_ASSIETTE, 0.55, True, ROUGE, (x - 0.6, -0.05, H), 70)
cylindre("assiette", 0.11, 0.012, (x - 0.47, -0.03, H + 0.2), INOX, sommets=40)
LUMIERES[3] += [(feu, 60),
                (projecteur("spot_4", (x - 1.4, -1.6, 3.0), (x, 0.1, 0.3), 260, (1.0, 0.82, 0.62), 34), 260),
                (projecteur("contre_4", (x + 1.0, 2.6, 2.4), (x, 0.1, 0.4), 160, (0.7, 0.8, 1.0), 40), 160)]

# ---------------------------------------------------------------- 5 ans : courir jusqu'au coucher du soleil
x = 4 * ECART
estrade(4, 2.3, TERRE_SECHE)
COURSE_A = {"taille": (12, 0, 0), "torse": (6, 0, 0), "hanche_g": (-65, 0, 0), "genou_g": (85, 0, 0),
            "hanche_d": (30, 0, 0), "genou_d": (60, 0, 0), "cheville_d": (15, 0, 0),
            "epaule_g": (45, 0, 6), "coude_g": (-80, 0, 0), "epaule_d": (-55, 0, -6), "coude_d": (-80, 0, 0)}
COURSE_B = {"taille": (12, 0, 0), "torse": (6, 0, 0), "hanche_d": (-65, 0, 0), "genou_d": (85, 0, 0),
            "hanche_g": (30, 0, 0), "genou_g": (60, 0, 0), "cheville_g": (15, 0, 0),
            "epaule_d": (45, 0, -6), "coude_d": (-80, 0, 0), "epaule_g": (-55, 0, 6), "coude_g": (-80, 0, 0)}
for k_, (dx, dy, pose, ech, mat) in enumerate(((-1.1, 0.5, COURSE_A, 0.58, ARGILE), (-0.35, -0.25, COURSE_B, 0.6, ROUGE),
                                               (0.45, 0.6, COURSE_B, 0.62, ARGILE), (1.15, -0.05, COURSE_A, 0.56, ARGILE))):
    perso(f"enfant_5_{k_}", pose, ech, True, mat, (x + dx, dy, H), 90)      # ils courent vers la droite, comme la caméra
# le ciel du soir : un grand panneau lumineux loin derrière, et un soleil rasant
ciel_m = bpy.data.materials.new("ciel")
ciel_m.use_nodes = True
n = ciel_m.node_tree.nodes
n.remove(n["Principled BSDF"])
em = n.new("ShaderNodeEmission")
rampe = n.new("ShaderNodeValToRGB")
coord = n.new("ShaderNodeTexCoord")
sep = n.new("ShaderNodeSeparateXYZ")
L_ = ciel_m.node_tree.links
L_.new(coord.outputs["Generated"], sep.inputs[0])
L_.new(sep.outputs["Y"], rampe.inputs[0])
el = rampe.color_ramp.elements
el[0].position, el[0].color = 0.0, (1.0, 0.42, 0.12, 1)
el[1].position, el[1].color = 1.0, (0.012, 0.016, 0.035, 1)
for pos_, col_ in ((0.3, (0.95, 0.3, 0.1, 1)), (0.42, (0.55, 0.16, 0.12, 1)), (0.62, (0.08, 0.06, 0.12, 1))):
    e_ = el.new(pos_)
    e_.color = col_
L_.new(rampe.outputs[0], em.inputs[0])
em.inputs[1].default_value = 1.6
L_.new(em.outputs[0], n["Material Output"].inputs[0])
bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 14, 2.2), rotation=(rad(90), 0, 0))
ciel = bpy.context.object
ciel.scale = (70, 10, 1)
ciel.data.materials.append(ciel_m)
bpy.ops.object.light_add(type="SUN", location=(x, 5, 2))
soleil = bpy.context.object
soleil.data.energy = 4.0
soleil.data.color = (1.0, 0.55, 0.25)
soleil.data.angle = rad(2)
soleil.rotation_euler = (Vector((x - 0.6, 0, 0)) - Vector((x + 1.5, 6, 0.75))).to_track_quat("-Z", "Y").to_euler()
LUMIERES[4] += [(soleil, 4.0), (projecteur("face_5", (x - 1.0, -3.0, 2.2), (x, 0, 0.4), 140, (0.8, 0.85, 1.0), 45), 140)]
CIEL_E = em

# ---------------------------------------------------------------- animation : lumières et caméra
def ease(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def niveau(i, t):
    """Allumage de la scène i au temps t : monte à l'arrivée, s'éteint lentement en repartant."""
    a = arrivee(i)
    monte = ease((t - (a - 0.25)) / 0.75)
    if i == N_SCENES - 1:
        return monte
    descend = 1 - ease((t - (a + TENUES[i] - 0.15)) / 0.65)
    return monte * descend


def flamme(t, graine):
    return 1 + 0.12 * math.sin(t * 23 + graine) + 0.08 * math.sin(t * 37 + 2 * graine) + 0.05 * math.sin(t * 61 + graine)


bpy.ops.object.camera_add()
cam = bpy.context.object
sc.camera = cam
cam.data.lens = 38
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.8
VISE = {0: (0.1, 0.1, 0.32), 1: (0.1, 0.05, 0.2), 2: (0.05, 0.05, 0.42), 3: (0.05, 0.1, 0.3), 4: (0.0, 0.1, 0.45)}
RECUL = {0: (-0.9, -3.3, 1.15), 1: (-0.55, -2.3, 0.7), 2: (-0.9, -3.4, 1.2), 3: (-0.9, -3.3, 1.1), 4: (-1.3, -5.2, 1.0)}
foc = bpy.data.objects.new("point_net", None)
sc.collection.objects.link(foc)
cam.data.dof.focus_object = foc


def pose_camera(t):
    """Position et visée de la caméra au temps t : une lente dérive devant chaque tableau,
    puis un passage fluide (accéléré, puis freiné) vers le suivant."""
    def devant(i, p):
        pos = Vector((i * ECART, 0, 0)) + Vector(RECUL[i]) + Vector((0.6 * p, 0.45 * p, -0.06 * p))
        vis = Vector((i * ECART, 0, 0)) + Vector(VISE[i]) + Vector((0.22 * p, 0, 0))
        return pos, vis

    for i in range(N_SCENES):
        a = arrivee(i)
        fin = a + TENUES[i]
        if t < fin or i == N_SCENES - 1:
            d0 = a - (TRAJET / 2 if i else a)
            p = (t - d0) / (fin + TRAJET / 2 - d0)
            return devant(i, max(0.0, min(1.0, p)))
        if t < fin + TRAJET:
            q = (t - fin) / TRAJET
            q = q * q * q * (q * (q * 6 - 15) + 10)          # très doux aux deux bouts
            p0, v0 = devant(i, (fin - (a - (TRAJET / 2 if i else a))) / (fin + TRAJET / 2 - (a - (TRAJET / 2 if i else a))))
            p1, v1 = devant(i + 1, 0.0)
            pos = p0.lerp(p1, q) + Vector((0, -0.35 * math.sin(math.pi * q), 0.18 * math.sin(math.pi * q)))
            return pos, v0.lerp(v1, q)
    return devant(N_SCENES - 1, 1.0)


for f in range(1, N + 1):
    t = (f - 1) / FPS
    pos, vis = pose_camera(t)
    cam.location = pos
    cam.rotation_euler = (vis - pos).to_track_quat("-Z", "Y").to_euler()
    cam.keyframe_insert("location", frame=f)
    cam.keyframe_insert("rotation_euler", frame=f)
    foc.location = vis
    foc.keyframe_insert("location", frame=f)
    for i in range(N_SCENES):
        nv = niveau(i, t)
        for L, e in LUMIERES[i]:
            extra = flamme(t, i * 3.1) if L.name in ("feu", "diya_feu") else 1.0
            L.data.energy = e * nv * extra
            L.data.keyframe_insert("energy", frame=f)
    fl_e.inputs[1].default_value = 30 * niveau(2, t) * flamme(t, 1.7)
    fl_e.inputs[1].keyframe_insert("default_value", frame=f)
    braise_e.inputs[1].default_value = 25 * niveau(3, t) * flamme(t, 4.2)
    braise_e.inputs[1].keyframe_insert("default_value", frame=f)
    CIEL_E.inputs[1].default_value = 1.6 * niveau(4, t)
    CIEL_E.inputs[1].keyframe_insert("default_value", frame=f)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(VIDEO, "medias", "blender", "S06_vignettes.blend"))
print(f"[S06] {N} images, {DUREE:.2f} s")

# ---------------------------------------------------------------- rendu
if A.test:
    for i in range(N_SCENES):
        f = int(round((arrivee(i) + 2.0) * FPS)) + 1
        sc.frame_set(f)
        sc.render.filepath = os.path.join(TEST, f"scene_{i + 1}.png")
        bpy.ops.render.render(write_still=True)
    sys.exit()
deb, fin = (int(v) for v in A.images.split("-")) if A.images else (1, N)
for f in range(deb, fin + 1):
    chemin = os.path.join(SORTIE, f"{f:04d}.png")
    if os.path.exists(chemin):
        continue
    sc.frame_set(f)
    sc.render.filepath = chemin
    bpy.ops.render.render(write_still=True)
print("[S06] rendu terminé")
