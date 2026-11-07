"""S02 · On s'assoit. Images clés des plans 3D, à partir de la scène de S01.

Ouvre medias/blender/S01_bureau.blend (créé par scenes/S01/bureau.py), puis ajoute :
  - une lampe de bureau qui peut s'allumer (lumière chaude, petite, qui s'ajoute au froid) ;
  - une silhouette assise, de dos (formes simples lissées : on ne la voit qu'en contre-jour) ;
  - l'écran au choix : « ancien » (la fenêtre claire de S01, que scenes/S01/ecran.py sait suivre et
    remplacer) ou « interface » (l'image des vies simulées posée directement sur la dalle) ;
  - une caméra par plan.

Plans rendus (hors Git, dans medias/S02/) :
  p01_fin       vue subjective, assis face à l'écran (fin du mouvement « on s'assoit » ; le début est S01_arrivee)
  p02           face à l'écran, un peu plus près (base du lent travelling avant, écran remplacé ensuite)
  p04_eteinte   la lampe de bureau, éteinte
  p04_allumee   la même, allumée
  p05           plan large depuis le noir : l'îlot de lumière, la silhouette de dos

Lancer sur le PC :
  "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b -P plans.py -- --plans p01_fin,p02,p04_eteinte,p04_allumee,p05
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

ICI = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.abspath(os.path.join(ICI, "..", ".."))
BLEND_S01 = os.path.join(VIDEO, "medias", "blender", "S01_bureau.blend")
BLEND = os.path.join(VIDEO, "medias", "blender", "S02_plans.blend")
SORTIE = os.path.join(VIDEO, "medias", "S02")
INTERFACE = os.path.join(SORTIE, "interface_ecran.png")   # exportée par scenes/S01/ecran.py --image

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--plans", default="p01_fin,p04_eteinte,p04_allumee,p05")
ap.add_argument("--echantillons", type=int, default=128)
ap.add_argument("--largeur", type=int, default=1920)
ap.add_argument("--hauteur", type=int, default=1080)
A = ap.parse_args(argv)
rad = math.radians

bpy.ops.wm.open_mainfile(filepath=BLEND_S01)
sc = bpy.context.scene
O = bpy.data.objects
EX, EY, BZ, BY = 0.08, 0.14, 0.74, 0.0
ECRAN_C = Vector((EX, EY - 0.0235, BZ + 0.355))        # centre de la dalle
for c in bpy.data.collections:
    if c.name in ("ENV", "PRP", "LGT", "CAM"):
        globals()["C_" + c.name] = c


def noeuds(m):
    m.use_nodes = True
    return m.node_tree.nodes, m.node_tree.links


# ---------------------------------------------------------------- l'écran : deux matières au choix
MAT_ANCIEN = bpy.data.materials["MAT_ecran"]
MAT_INTERFACE = bpy.data.materials.new("MAT_ecran_interface")
n, l = noeuds(MAT_INTERFACE)
for x in list(n):
    n.remove(x)
out = n.new("ShaderNodeOutputMaterial"); em = n.new("ShaderNodeEmission"); tex = n.new("ShaderNodeTexImage")
tex.image = bpy.data.images.load(INTERFACE); tex.interpolation = "Cubic"
l.new(tex.outputs["Color"], em.inputs["Color"]); em.inputs["Strength"].default_value = 0.9
l.new(em.outputs[0], out.inputs["Surface"])
dalle = O["PRP_ecran_dalle"]


def ecran(mode):
    dalle.data.materials[0] = MAT_INTERFACE if mode == "interface" else MAT_ANCIEN


# ---------------------------------------------------------------- la lampe de bureau : une ampoule et sa lumière
tete = O["PRP_lampe_tete"]
bpy.context.view_layer.update()
mw = tete.matrix_world
bas_tete = mw @ Vector((0, 0, -0.05))                  # l'ouverture de l'abat-jour
ampoule_m = bpy.data.materials.new("MAT_ampoule")
n, l = noeuds(ampoule_m)
for x in list(n):
    n.remove(x)
o_ = n.new("ShaderNodeOutputMaterial"); e_ = n.new("ShaderNodeEmission")
e_.inputs["Color"].default_value = (1.0, 0.72, 0.45, 1); e_.inputs["Strength"].default_value = 0.0
l.new(e_.outputs[0], o_.inputs["Surface"])
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.022, location=bas_tete + Vector((0, 0, 0.012)))
ampoule = bpy.context.active_object; ampoule.name = "PRP_lampe_ampoule"; ampoule.data.materials.append(ampoule_m)
ld = bpy.data.lights.new("LGT_lampe_bureau", "SPOT")
ld.energy = 0.0; ld.color = (1.0, 0.74, 0.5); ld.spot_size = rad(95); ld.spot_blend = 0.6; ld.shadow_soft_size = 0.03
lampe_l = bpy.data.objects.new("LGT_lampe_bureau", ld); C_LGT.objects.link(lampe_l)
lampe_l.location = bas_tete
cible_lampe = Vector((-0.3, -0.12, BZ))
lampe_l.rotation_euler = (cible_lampe - bas_tete).to_track_quat("-Z", "Y").to_euler()


def lampe(allumee):
    ld.energy = 45.0 if allumee else 0.0
    e_.inputs["Strength"].default_value = 18.0 if allumee else 0.0


# ---------------------------------------------------------------- la silhouette assise, de dos
tissu = bpy.data.materials["MAT_tissu_chaise"]
peau = bpy.data.materials.new("MAT_silhouette")
n, l = noeuds(peau)
for x in list(n):
    n.remove(x)
bs = n.new("ShaderNodeBsdfPrincipled"); l.new(bs.outputs[0], n.new("ShaderNodeOutputMaterial").inputs["Surface"])
bs.inputs["Base Color"].default_value = (0.022, 0.02, 0.019, 1); bs.inputs["Roughness"].default_value = 0.9
CH = O["PRP_chaise"]
corps = bpy.data.objects.new("PRP_silhouette", None); C_PRP.objects.link(corps)
corps.location = (0.12, BY - 0.80, 0.0)
morceaux = []


def forme(nom, prim, dims, pos, rot=(0, 0, 0), mat=None, sub=2):
    if prim == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=32, ring_count=16)
    else:
        bpy.ops.mesh.primitive_cube_add(size=2)
    o = bpy.context.active_object; o.name = nom
    o.scale = dims; o.location = pos; o.rotation_euler = [rad(a) for a in rot]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if prim != "sphere":
        b = o.modifiers.new("arrondi", "BEVEL"); b.width = min(dims) * 0.9; b.segments = 4
    s = o.modifiers.new("lisse", "SUBSURF"); s.levels = sub; s.render_levels = sub
    o.data.materials.append(mat or tissu)
    for p in o.data.polygons:
        p.use_smooth = True
    for c in o.users_collection:
        c.objects.unlink(o)
    C_PRP.objects.link(o)
    o.parent = corps
    morceaux.append(o)
    return o


# repère local : x à droite, y vers l'écran, z vers le haut ; le haut du corps penché vers l'écran
forme("SIL_bassin", "cube", (0.19, 0.17, 0.09), (0, 0.03, 0.6))
forme("SIL_torse", "cube", (0.2, 0.12, 0.27), (0, 0.06, 0.88), rot=(10, 0, 0))
forme("SIL_epaules", "cube", (0.23, 0.11, 0.07), (0, 0.10, 1.11), rot=(10, 0, 0))
forme("SIL_cou", "cube", (0.05, 0.05, 0.06), (0, 0.13, 1.2), mat=peau)
forme("SIL_tete", "sphere", (0.085, 0.1, 0.115), (0, 0.15, 1.33), rot=(8, 0, 0), mat=peau)
forme("SIL_cheveux", "sphere", (0.093, 0.104, 0.098), (0, 0.125, 1.365), rot=(14, 0, 0), mat=tissu)
forme("SIL_col", "cube", (0.09, 0.07, 0.03), (0, 0.11, 1.16), rot=(10, 0, 0))
for sx in (-1, 1):
    forme(f"SIL_bras_{sx}", "cube", (0.05, 0.05, 0.15), (sx * 0.24, 0.12, 0.98), rot=(28, sx * 6, 0))
    forme(f"SIL_avantbras_{sx}", "cube", (0.045, 0.16, 0.045), (sx * 0.2, 0.36, 0.84), rot=(-8, 0, -sx * 12))
    forme(f"SIL_cuisse_{sx}", "cube", (0.075, 0.22, 0.075), (sx * 0.1, 0.25, 0.6))


def silhouette(visible):
    for o in morceaux:
        o.hide_render = not visible
    O["PRP_veste"].hide_render = visible       # la veste est sur ses épaules, pas sur le dossier


# ---------------------------------------------------------------- caméras
def viser(depuis, vers):
    return (Vector(vers) - Vector(depuis)).to_track_quat("-Z", "Y").to_euler()


cam = O["CAM_pov"]
cam.animation_data_clear()
focus = O["CAM_point_net"]; focus.animation_data_clear()
sc.camera = cam

PLANS = {
    # nom : (position, visée, focale, ouverture, point net, écran, lampe, silhouette)
    "p01_fin": ((0.12, BY - 0.80, 1.18), (0.08, BY + 0.1, 1.03), 30, 2.8, ECRAN_C, "ancien", False, False),
    "p02": ((0.11, BY - 0.38, 1.17), (0.08, BY + 0.12, 1.08), 30, 2.8, ECRAN_C, "ancien", False, False),
    "p04_eteinte": ((-0.02, BY - 0.80, 1.16), (-0.42, BY + 0.12, 0.93), 35, 2.8, (-0.38, BY + 0.2, 0.95), "interface", False, False),
    "p04_allumee": ((-0.02, BY - 0.80, 1.16), (-0.42, BY + 0.12, 0.93), 35, 2.8, (-0.38, BY + 0.2, 0.95), "interface", True, False),
    "p05": ((-1.7, BY - 5.6, 2.05), (0.05, BY - 0.25, 0.95), 50, 4.0, (0.1, BY - 0.8, 1.1), "interface", True, True),
}

try:
    pref = bpy.context.preferences.addons["cycles"].preferences
    pref.compute_device_type = "OPTIX"; pref.get_devices()
    for d in pref.devices:
        d.use = d.type == "OPTIX"
    sc.cycles.device = "GPU"
except Exception as e:
    print("[S02] GPU indisponible :", e)
sc.cycles.samples = A.echantillons
sc.render.resolution_x, sc.render.resolution_y = A.largeur, A.hauteur
os.makedirs(SORTIE, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
for nom in [x.strip() for x in A.plans.split(",") if x.strip()]:
    pos, vise, focale, f, net, mode, allumee, sil = PLANS[nom]
    cam.location = pos; cam.rotation_euler = viser(pos, vise)
    cam.data.lens = focale; cam.data.dof.aperture_fstop = f
    focus.location = net
    ecran(mode); lampe(allumee); silhouette(sil)
    sc.frame_set(1)
    sc.render.filepath = os.path.join(SORTIE, f"S02_{nom}.png")
    bpy.ops.render.render(write_still=True)
    print("[S02] rendu :", sc.render.filepath)
