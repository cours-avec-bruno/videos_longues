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
ap.add_argument("--images", default="1-144", help="pour p01_anim : plage d'images à rendre, ex. 1-144")
ap.add_argument("--refaire", action="store_true", help="pour p01_anim : rerendre les images déjà faites")
ap.add_argument("--rapide", action="store_true", help="pour p01_anim : données persistantes + processeur en renfort")
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
def animer_assis():
    """P01 « on s'assoit », animé entièrement dans Blender (Higgsfield faisait traverser la chaise).

    On tire la chaise vers soi en jetant un œil dessus, on se décale à côté, la chaise glisse sous soi,
    on s'assoit, puis on roule jusqu'au bureau. Fin = cadrage de p01_fin (raccord avec P02).
    La caméra vise un repère animé (contrainte), un léger bruit imite la tenue à la main.
    """
    CH = O["PRP_chaise"]
    visee = bpy.data.objects.new("CAM_visee_assis", None); C_CAM.objects.link(visee)
    for c in list(cam.constraints):
        cam.constraints.remove(c)
    ct = cam.constraints.new("TRACK_TO"); ct.target = visee; ct.track_axis = "TRACK_NEGATIVE_Z"; ct.up_axis = "UP_Y"
    cam.data.lens = 30; cam.data.dof.aperture_fstop = 2.8; cam.data.dof.focus_object = visee
    cles_cam = [(1, (0.18, BY - 1.85, 1.58)), (26, (0.40, BY - 1.78, 1.60)), (54, (0.33, BY - 1.20, 1.55)),
                (80, (0.21, BY - 1.10, 1.24)), (92, (0.21, BY - 1.10, 1.18)), (144, (0.12, BY - 0.80, 1.18))]
    cles_visee = [(1, (0.06, BY + 0.05, 0.74)), (26, (0.07, BY - 0.95, 0.70)), (54, (0.10, BY + 0.10, 0.95)),
                  (80, (0.09, BY + 0.10, 1.00)), (144, (0.08, BY + 0.10, 1.03))]
    cles_chaise = [(1, (0.12, BY - 0.85), -14), (26, (0.07, BY - 1.12), -26), (54, (0.09, BY - 1.15), -18),
                   (78, (0.21, BY - 1.02), -4), (92, (0.21, BY - 1.02), -4), (144, (0.12, BY - 0.70), 0)]
    for f, p in cles_cam:
        cam.location = p; cam.keyframe_insert("location", frame=f)
    for f, p in cles_visee:
        visee.location = p; visee.keyframe_insert("location", frame=f)
    for f, (x, y), r in cles_chaise:
        CH.location = (x, y, 0); CH.rotation_euler = (0, 0, rad(r))
        CH.keyframe_insert("location", frame=f); CH.keyframe_insert("rotation_euler", frame=f)
    # tenue à la main : un bruit lent et faible sur la caméra et la visée
    def courbes(ob):
        act = ob.animation_data.action
        try:
            return list(act.fcurves)
        except AttributeError:          # Blender 5 : actions en couches
            return [fc for ly in act.layers for st in ly.strips for cb in st.channelbags for fc in cb.fcurves]

    for ob, force in ((cam, 0.004), (visee, 0.012)):
        for fc in courbes(ob):
            m = fc.modifiers.new("NOISE"); m.scale = 28; m.strength = force; m.phase = hash(fc.data_path + str(fc.array_index)) % 100
    sc.frame_start, sc.frame_end = 1, 144


if A.plans.strip() == "p01_anim":
    ecran("ancien"); lampe(False); silhouette(False)
    animer_assis()
    dossier = os.path.join(SORTIE, "p01_anim")
    os.makedirs(dossier, exist_ok=True)
    debut, fin = (int(x) for x in A.images.split("-"))
    if A.rapide:
        # rendu plus rapide, même image : la scène reste en mémoire d'une image à l'autre, et le processeur aide la carte
        sc.render.use_persistent_data = True
        try:
            pref = bpy.context.preferences.addons["cycles"].preferences
            for d in pref.devices:
                d.use = d.type in ("OPTIX", "CPU")
            print("[S02] périphériques :", [d.name for d in pref.devices if d.use])
        except Exception as e:
            print("[S02] processeur non ajouté :", e)
    for f in range(debut, fin + 1):
        chemin = os.path.join(dossier, f"f{f:03d}.png")
        if os.path.exists(chemin) and not A.refaire:
            continue
        sc.frame_set(f)
        sc.render.filepath = chemin
        bpy.ops.render.render(write_still=True)
        print("[S02] image", f)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND.replace(".blend", "_assis.blend"))
    sys.exit(0)

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
