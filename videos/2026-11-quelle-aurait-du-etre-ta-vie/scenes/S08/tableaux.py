"""S08 · 11 à 14 ans : les tableaux 3D (Blender, Eevee), dans la grammaire de S06 et S07.

Manoj est le seul en rouge ; les autres, en argile. Deux tableaux, deux lumières qui racontent :
  portail   11 ans : les enfants entrent à l'école, le portail se referme ; lui reste dehors.
                     La lumière chaude est de l'autre côté du portail ; lui est dans la pénombre froide.
  betes     14 ans : sur un chemin de terre, au soleil rasant de fin de journée, il garde les chèvres ; des enfants
                     passent derrière avec leur cartable ; il se retourne et les suit des yeux.

Lancer sur le PC :
  "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b -P tableaux.py -- [--test] [--plans portail]
Sorties (hors Git) : medias/S08/3d/<plan>/####.png ; tests : medias/S08/3d_test/
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
import plateau as P  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--test", action="store_true")
ap.add_argument("--plans", default="")
ap.add_argument("--refaire", action="store_true")
A = ap.parse_args(argv)
rad = math.radians
FPS = 24
SORTIE = os.path.join(VIDEO, "medias", "S08", "3d")
TEST = os.path.join(VIDEO, "medias", "S08", "3d_test")
os.makedirs(SORTIE, exist_ok=True)
os.makedirs(TEST, exist_ok=True)

sc = P.scene(test=A.test, fps=FPS, images=200)
M = P.materiaux()
P.sol(centre=(10, 0), taille=(120, 80))
H = P.H
ESP = 14.0


def pose(*parts, **extra):
    d = {}
    for p in parts:
        d.update(p)
    d.update(extra)
    return d


BRAS_BAS = {"epaule_g": (-8, -6, 0), "epaule_d": (-8, 6, 0), "coude_g": (-12, 0, 0), "coude_d": (-12, 0, 0)}
MARCHE_A = pose(BRAS_BAS, hanche_g=(-24, 0, 0), genou_g=(14, 0, 0), hanche_d=(16, 0, 0), genou_d=(30, 0, 0),
                epaule_g=(16, -6, 0), epaule_d=(-20, 6, 0))
MARCHE_B = pose(BRAS_BAS, hanche_d=(-24, 0, 0), genou_d=(14, 0, 0), hanche_g=(16, 0, 0), genou_g=(30, 0, 0),
                epaule_d=(16, 6, 0), epaule_g=(-20, -6, 0))
DEHORS = pose(BRAS_BAS, cou=(6, 0, 0), epaule_d=(-14, 8, 0), coude_d=(-30, 0, 0))
GARDE = pose(BRAS_BAS, cou=(24, 0, 0), epaule_d=(-38, 4, 0), coude_d=(-28, 0, 0))          # tient le bâton, regarde les bêtes
REGARDE = pose(BRAS_BAS, cou=(-2, 0, 0), epaule_d=(-30, 4, 0), coude_d=(-24, 0, 0))         # relève la tête

ANIM = []          # fonctions (f) -> None appelées à chaque image du plan concerné : {plan: [fonctions]}
PAR_PLAN = {"portail": [], "betes": []}


def ease(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def marcheur(plan, nom, ech, mat, depart, arrivee, t0, t1, angle, cartable=True):
    """Un enfant qui marche : un pivot qui se déplace, deux poses qui alternent (un pas toutes les 7 images)."""
    piv = bpy.data.objects.new(nom, None)
    sc.collection.objects.link(piv)
    a = P.perso(nom + "_a", MARCHE_A, ech, True, mat, (0, 0, 0), angle)
    b = P.perso(nom + "_b", MARCHE_B, ech, True, mat, (0, 0, 0), angle)
    objs = [a, b]
    if cartable:
        c = P.boite(nom + "_cartable", (0.2, 0.09, 0.24), (0, 0, 0.5 * ech / 0.62), P.materiau(nom + "_cuir", (0.13, 0.10, 0.08), 0.7, 0.3),
                    rot=(0, 0, angle), biseau=0.02)
        dos = Vector((0, 0.09, 0)) if angle == 180 else Vector((-0.09, 0, 0)) if angle == 90 else Vector((0, -0.09, 0))
        c.location += dos
        objs.append(c)
    for o in objs:
        o.parent = piv
    d0, d1 = Vector(depart), Vector(arrivee)
    piv.location = d0                    # sinon, hors de son plan, il attend à l'origine (dans l'autre tableau)

    def anim(f, piv=piv, a=a, b=b):
        t = (f - 1) / FPS
        q = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
        piv.location = d0.lerp(d1, q)
        piv.keyframe_insert("location", frame=f)
        pas = int(t * FPS / 7) % 2 if 0 < q < 1 else 0
        a.hide_render = pas == 1
        b.hide_render = pas == 0
        a.keyframe_insert("hide_render", frame=f)
        b.keyframe_insert("hide_render", frame=f)
    PAR_PLAN[plan].append(anim)
    return piv


def chevre(nom, pos, angle, ech=1.0, broute=True):
    """Une chèvre en quelques volumes (corps, pattes, tête, cornes), dans la même argile que les figurines."""
    x, y, z = pos
    mat = M["argile_v"]
    piv = bpy.data.objects.new(nom, None)
    sc.collection.objects.link(piv)
    piv.location = (x, y, z)
    piv.rotation_euler.z = rad(angle)
    piv.scale = (ech, ech, ech)
    parts = [P.boite(nom + "_corps", (0.46, 0.22, 0.22), (0, 0, 0.3), mat, biseau=0.09)]
    for k, (dx, dy) in enumerate(((-0.16, -0.065), (-0.16, 0.065), (0.15, -0.065), (0.15, 0.065))):
        parts.append(P.cylindre(f"{nom}_patte_{k}", 0.024, 0.22, (dx, dy, 0.11), mat, sommets=8))
    if broute:      # la tête basse, vers l'herbe
        parts.append(P.boite(nom + "_cou", (0.16, 0.09, 0.09), (0.27, 0, 0.27), mat, rot=(0, 45, 0), biseau=0.035))
        tete_x, tete_z, rt = 0.35, 0.15, 70
    else:           # la tête haute, aux aguets
        parts.append(P.boite(nom + "_cou", (0.09, 0.09, 0.2), (0.24, 0, 0.42), mat, rot=(0, 25, 0), biseau=0.035))
        tete_x, tete_z, rt = 0.31, 0.53, 20
    parts.append(P.boite(nom + "_tete", (0.16, 0.085, 0.085), (tete_x, 0, tete_z), mat, rot=(0, rt, 0), biseau=0.035))
    for s in (-1, 1):
        parts.append(P.boite(f"{nom}_oreille_{s}", (0.06, 0.012, 0.03), (tete_x - 0.05, 0.055 * s, tete_z + 0.02), mat,
                             rot=(0, 0, 30 * s)))
        parts.append(P.cylindre(f"{nom}_corne_{s}", 0.008, 0.07, (tete_x - 0.06, 0.025 * s, tete_z + 0.06), M["fonte"],
                                rot=(0, -40, 0), sommets=6))
    parts.append(P.boite(nom + "_queue", (0.05, 0.02, 0.02), (-0.25, 0, 0.4), mat, rot=(0, -45, 0)))
    for o in parts:
        o.parent = piv
    return piv


# ---------------------------------------------------------------- 11 ans : le portail de l'école
x = 0 * ESP
P.estrade("portail", (x, 0), 2.8, M["terre_seche"])
# le mur d'enceinte, percé d'une ouverture ; derrière, la cour éclairée et le bâtiment de l'école
for s in (-1, 1):
    P.boite(f"mur_portail_{s}", (2.0, 0.22, 1.25), (x + s * 1.55, 0.9, H + 0.625), M["chaux"], biseau=0.02)
    P.boite(f"pilier_{s}", (0.24, 0.3, 1.5), (x + s * 0.62, 0.9, H + 0.75), M["chaux"], biseau=0.02)
    P.boite(f"chapeau_{s}", (0.3, 0.36, 0.06), (x + s * 0.62, 0.9, H + 1.53), M["chaux"], biseau=0.01)
P.boite("ecole_batiment", (3.6, 1.0, 1.6), (x, 2.7, H + 0.8), M["chaux"], biseau=0.02)
P.boite("ecole_toit", (3.8, 1.2, 0.08), (x, 2.7, H + 1.64), M["fonte"])
for k in range(4):
    P.boite(f"ecole_fenetre_{k}", (0.36, 0.04, 0.5), (x - 1.2 + 0.8 * k, 2.19, H + 0.95),
            P.emission(f"fen_{k}", (1.0, 0.78, 0.5), 3.5)[0])
P.boite("ecole_enseigne", (1.4, 0.04, 0.28), (x, 2.18, H + 1.42), P.materiau("enseigne_s08", (0.08, 0.16, 0.30), 0.6, 0.3))
# le portail : deux battants de barreaux, chacun pivote autour de son gond
BATTANTS = []
for s in (-1, 1):
    gond = bpy.data.objects.new(f"gond_{s}", None)
    sc.collection.objects.link(gond)
    gond.location = (x + s * 0.5, 0.9, H)
    for k in range(6):
        b = P.cylindre(f"barreau_{s}_{k}", 0.012, 1.2, (-s * (0.06 + 0.075 * k), 0, 0.62), M["fonte"], sommets=8)
        b.parent = gond
    for zz in (0.12, 0.62, 1.12):
        t = P.boite(f"traverse_{s}_{zz}", (0.46, 0.025, 0.025), (-s * 0.25, 0, zz), M["fonte"])
        t.parent = gond
    BATTANTS.append((gond, s))
FERME = 3.3          # le portail se referme entre 3,3 s et 4,5 s


def anim_portail(f):
    t = (f - 1) / FPS
    q = ease((t - FERME) / 1.2)
    for g, s in BATTANTS:
        g.rotation_euler.z = rad(s * -88 * (1 - q))           # ouvert vers la cour, puis fermé
        g.keyframe_insert("rotation_euler", frame=f)


PAR_PLAN["portail"].append(anim_portail)
# les enfants qui entrent (de dos, vers la cour)
for k, (dx, y0, t0) in enumerate(((-0.1, -0.9, 0.0), (0.3, -1.3, 0.25), (0.05, -1.8, 0.5), (0.4, -2.2, 0.75), (-0.05, -2.6, 0.95))):
    marcheur("portail", f"eleve_p{k}", 0.6 + 0.03 * (k % 2), M["argile"], (x + dx, y0, H), (x - 0.9 + 0.45 * k, 1.75 + 0.12 * (k % 2), H), t0, t0 + 2.3, 180)
# lui : à l'écart, de trois quarts dos, face au portail
P.perso("manoj_portail", DEHORS, 0.66, True, M["rouge"], (x - 1.3, -1.0, H), 160)
# la lumière : chaude dans la cour (de l'autre côté), froide et basse sur lui
P.projecteur("cour_soleil", (x + 1.5, 4.5, 4.0), (x, 1.4, 0.2), 3400, (1.0, 0.68, 0.36), 46, flou=0.4)
P.projecteur("cour_face", (x - 0.5, 0.2, 3.6), (x, 2.4, 0.8), 600, (1.0, 0.82, 0.6), 40)
P.projecteur("froid_manoj", (x - 3.0, -3.0, 2.6), (x - 1.3, -1.0, 0.5), 160, (0.55, 0.68, 1.0), 26, flou=0.6)
P.projecteur("contre_portail", (x + 2.6, -2.0, 2.4), (x, 0.9, 0.8), 140, (0.6, 0.72, 1.0), 40)

# ---------------------------------------------------------------- 14 ans : les bêtes, et ceux qui vont à l'école
x = 1 * ESP
P.estrade("betes", (x, 0), 3.0, M["terre_seche"])
P.boite("chemin", (6.0, 0.7, 0.01), (x, 1.15, H + 0.005), M["terre"])
for k in range(9):                                  # quelques touffes d'herbe sèche et pierres, pour la lumière rasante
    P.sphere(f"pierre_{k}", 0.04 + 0.02 * (k % 3), (x - 2.2 + 0.55 * k, -1.2 + 0.4 * ((k * 7) % 5) / 4, H + 0.02), M["glaise"],
             echelle=(1.3, 1, 0.6), sub=1)
manoj_b = P.perso("manoj_betes", GARDE, 0.7, True, M["rouge"], (x - 0.35, -0.35, H), 15)
manoj_c = P.perso("manoj_betes_regarde", REGARDE, 0.7, True, M["rouge"], (x - 0.35, -0.35, H), 15)
baton = P.cylindre("baton", 0.012, 1.0, (x - 0.12, -0.5, H + 0.45), M["bambou"], rot=(0, 12, 0), sommets=6)
CHEVRES = [chevre("chevre_0", (x + 0.45, -0.75, H), -30), chevre("chevre_1", (x - 1.05, -0.95, H), 40, 0.9),
           chevre("chevre_2", (x + 0.9, 0.05, H), 160, 1.05, broute=False), chevre("chevre_3", (x - 0.75, 0.25, H), 200, 0.85)]
RETOURNE = (2.4, 3.6)             # il relève la tête puis se retourne vers le chemin


def anim_manoj(f):
    t = (f - 1) / FPS
    leve = t >= RETOURNE[0]
    manoj_b.hide_render = leve
    manoj_c.hide_render = not leve
    q = ease((t - RETOURNE[0]) / (RETOURNE[1] - RETOURNE[0]))
    for o in (manoj_b, manoj_c):
        o.rotation_euler.z = rad(15 + 150 * q)
        o.keyframe_insert("rotation_euler", frame=f)
        o.keyframe_insert("hide_render", frame=f)
    baton.hide_render = leve
    baton.keyframe_insert("hide_render", frame=f)


PAR_PLAN["betes"].append(anim_manoj)
for k, (y_, t0, dx) in enumerate(((1.05, 0.6, 0.0), (1.3, 0.9, -0.5), (1.1, 1.5, -1.1))):
    marcheur("betes", f"eleve_b{k}", 0.64, M["argile"], (x - 3.2 + dx, y_, H), (x + 3.4 + dx, y_, H), t0, t0 + 6.2, 90)
# le soleil rasant de fin de journée (les ombres longues viennent vers nous), et un ciel froid en contre
P.projecteur("soleil_bas", (x + 4.5, 3.5, 1.2), (x - 0.5, -0.5, 0.2), 3800, (1.0, 0.66, 0.36), 34, flou=0.25)
P.projecteur("ciel_betes", (x - 3.0, -2.5, 3.6), (x, 0, 0.3), 180, (0.55, 0.68, 1.0), 50, flou=0.6)
P.projecteur("chemin_lum", (x + 1.0, -2.6, 3.0), (x, 1.15, 0.4), 260, (1.0, 0.8, 0.6), 30)

# ---------------------------------------------------------------- les plans
PLANS = {
    #  nom       : (caméra début,             caméra fin,                 visée début,          visée fin,            focale, durée)
    "portail":   ((-2.3, -4.7, 1.0),           (-1.85, -4.0, 0.9),         (-0.25, 0.9, 0.62),  (-0.1, 1.1, 0.6),    40, 5.8),
    "betes":     ((-0.6, -4.2, 1.05),          (0.5, -3.85, 0.95),          (-0.1, 0.1, 0.45),    (0.25, 0.3, 0.5),    40, 6.6),
}
BASE = {"portail": 0.0, "betes": ESP}

bpy.ops.object.camera_add()
cam = bpy.context.object
sc.camera = cam
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.8
foc = bpy.data.objects.new("point_net", None)
sc.collection.objects.link(foc)
cam.data.dof.focus_object = foc


def preparer(nom):
    p0, p1, v0, v1, focale, duree = PLANS[nom]
    xb = BASE[nom]
    cam.animation_data_clear()
    foc.animation_data_clear()
    cam.data.lens = focale
    n = int(round(duree * FPS))
    sc.frame_start, sc.frame_end = 1, n
    for f in range(1, n + 1):
        q = ease((f - 1) / max(1, n - 1))
        pos = Vector(p0).lerp(Vector(p1), q) + Vector((xb, 0, 0))
        vis = Vector((xb, 0, 0)) + Vector(v0).lerp(Vector(v1), q)
        cam.location = pos
        cam.rotation_euler = (vis - pos).to_track_quat("-Z", "Y").to_euler()
        foc.location = vis
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        foc.keyframe_insert("location", frame=f)
        for fn in PAR_PLAN[nom]:
            fn(f)
    return n


bpy.ops.wm.save_as_mainfile(filepath=os.path.join(VIDEO, "medias", "blender", "S08_tableaux.blend"))
noms = [p.strip() for p in A.plans.split(",") if p.strip()] or list(PLANS)
for nom in noms:
    n = preparer(nom)
    if A.test:
        for f in sorted({1, int(n * 0.45), int(n * 0.7), n}):
            sc.frame_set(f)
            if os.environ.get("DIAG"):
                for o in bpy.data.objects:
                    if o.name.startswith("eleve_") and o.type == "MESH" and not o.hide_render:
                        print("DIAG", f, o.name, tuple(round(v, 2) for v in o.matrix_world.translation))
                continue
            sc.render.filepath = os.path.join(TEST, f"{nom}_{f:03d}.png")
            bpy.ops.render.render(write_still=True)
        continue
    d = os.path.join(SORTIE, nom)
    os.makedirs(d, exist_ok=True)
    for f in range(1, n + 1):
        chemin = os.path.join(d, f"{f:04d}.png")
        if os.path.exists(chemin) and not A.refaire:
            continue
        sc.frame_set(f)
        sc.render.filepath = chemin
        bpy.ops.render.render(write_still=True)
    print(f"[S08] {nom} : {n} images")
print("[S08] terminé")
