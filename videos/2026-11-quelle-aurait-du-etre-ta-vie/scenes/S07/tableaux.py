"""S07 · L'enfance (5 à 10 ans) : les tableaux 3D (Blender, Eevee), dans la grammaire validée en S06.

Manoj est le seul en rouge ; les autres, en argile ; un sol sombre qui reflète, une lumière par tableau.
Chaque plan a sa caméra, son mouvement, sa durée ; certains ont une action :
  ecole        5 ans : son père tend des billets au guichet d'une petite école ; lui, debout, avec son cartable
  choix_*      7 ans : trois vignettes fixes (prière, danse, cricket) pour le choix posé au spectateur
  huit_ans     8 ans : debout au milieu des grands assis, qui lui demandent ce qu'il veut faire plus tard
  baguette     9 ans : le maître lève la baguette et frappe sa paume tendue (le bras s'abat à l'impact)
  classe       9 ans : les autres lèvent la main, un par un ; pas lui
  dette        9 ans : la nuit, ses parents, une boîte en fer presque vide, une lampe (image fixe)
  funerailles 10 ans : le grand-père sous un drap blanc, les adultes tête basse ; lui, à l'écart

Lancer sur le PC :
  "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b -P tableaux.py -- [--test] [--plans ecole,classe]
Sorties (hors Git) : medias/S07/3d/<plan>/####.png ; tests : medias/S07/3d_test/<plan>.png
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Euler, Matrix, Vector

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
A = ap.parse_args(argv)
rad = math.radians
FPS = 24
SORTIE = os.path.join(VIDEO, "medias", "S07", "3d")
TEST = os.path.join(VIDEO, "medias", "S07", "3d_test")

sc = P.scene(test=A.test, fps=FPS, images=200)
M = P.materiaux()
P.sol(centre=(40, 0), taille=(220, 90))
H = P.H
ESP = 12.0

# ---------------------------------------------------------------- poses (X négatif = vers l'avant pour bras et jambes ;
#                                                                    X positif = penché en avant pour le buste et le cou)
TAILLEUR = {"hanche_g": (-85, 0, 50), "genou_g": (-130, 0, 0), "hanche_d": (-85, 0, -50), "genou_d": (-130, 0, 0)}
ASSIS = {"hanche_g": (-90, 0, -6), "genou_g": (90, 0, 0), "hanche_d": (-90, 0, 6), "genou_d": (90, 0, 0)}


def pose(*parts, **extra):
    d = {}
    for p in parts:
        d.update(p)
    d.update({k.replace("__", "_"): v for k, v in extra.items()})
    return d


BRAS_BAS = {"epaule_g": (-8, -6, 0), "epaule_d": (-8, 6, 0), "coude_g": (-12, 0, 0), "coude_d": (-12, 0, 0)}
MANOJ_FIER = pose(BRAS_BAS, cou=(-6, 0, 0), epaule_g=(10, -8, 0), coude_g=(-40, 0, 0))
PERE_TEND = pose(BRAS_BAS, cou=(12, 0, 0), taille=(6, 0, 0), epaule_d=(-78, 0, -12), coude_d=(-12, 0, 0))
CLERC = pose(ASSIS, cou=(14, 0, 0), epaule_g=(-55, 0, 0), coude_g=(-50, 0, 0), epaule_d=(-55, 0, 0), coude_d=(-50, 0, 0))
PRIERE = pose(TAILLEUR, cou=(16, 0, 0), epaule_g=(-42, 0, -30), coude_g=(-100, 0, 0), epaule_d=(-42, 0, 30), coude_d=(-100, 0, 0))
DANSE_A = pose(hanche_g=(-45, 0, 0), genou_g=(70, 0, 0), taille=(0, 8, 0), epaule_g=(-165, -10, 0), coude_g=(-35, 0, 0),
               epaule_d=(0, 80, 0), coude_d=(-40, 0, 0))
DANSE_B = pose(hanche_d=(-40, 0, 0), genou_d=(65, 0, 0), taille=(0, -8, 0), epaule_d=(-165, 10, 0), coude_d=(-35, 0, 0),
               epaule_g=(0, -80, 0), coude_g=(-40, 0, 0))
BATTEUR = pose(hanche_g=(-25, -14, 0), genou_g=(35, 0, 0), hanche_d=(-25, 14, 0), genou_d=(35, 0, 0), taille=(22, 0, 0),
               cou=(-10, 0, 0), epaule_g=(-55, 0, -35), coude_g=(-25, 0, 0), epaule_d=(-55, 0, 30), coude_d=(-30, 0, 0))
LANCEUR = pose(hanche_g=(-55, 0, 0), genou_g=(60, 0, 0), hanche_d=(25, 0, 0), genou_d=(40, 0, 0), taille=(10, 0, 0),
               epaule_d=(-175, 0, 0), coude_d=(-10, 0, 0), epaule_g=(-40, 0, 0), coude_g=(-50, 0, 0))
ADULTE_ASSIS = pose(TAILLEUR, cou=(-4, 0, 0), epaule_g=(-25, 0, 10), coude_g=(-50, 0, 0), epaule_d=(-25, 0, -10), coude_d=(-50, 0, 0))
ADULTE_GESTE = pose(TAILLEUR, cou=(-6, 0, 0), taille=(8, 0, 0), epaule_d=(-80, 0, -20), coude_d=(-40, 0, 0),
                    epaule_g=(-25, 0, 10), coude_g=(-50, 0, 0))
ENFANT_DEBOUT_REGARDE = pose(BRAS_BAS, cou=(-10, 0, 0))
# (le maître regarde vers -X : son bras gauche est côté caméra ; Manoj regarde vers +X : son bras droit est côté caméra)
MAITRE_HAUT = pose(BRAS_BAS, taille=(-4, 0, 0), epaule_g=(-168, 0, 0), coude_g=(-25, 0, 0), cou=(10, 0, 0))
MAITRE_BAS = pose(BRAS_BAS, taille=(10, 0, 0), epaule_g=(-50, 0, 0), coude_g=(-10, 0, 0), cou=(18, 0, 0))
PAUME = pose(BRAS_BAS, cou=(22, 0, 0), epaule_d=(-82, 0, 0), coude_d=(-6, 0, 0))
PAUME_RETIREE = pose(BRAS_BAS, cou=(28, 0, 0), taille=(8, 0, 0), epaule_d=(-30, 0, 0), coude_d=(-100, 0, 0))
ELEVE_BAS = pose(ASSIS, cou=(4, 0, 0), epaule_g=(-50, 0, 0), coude_g=(-60, 0, 0), epaule_d=(-50, 0, 0), coude_d=(-60, 0, 0))
ELEVE_HAUT = pose(ASSIS, cou=(-6, 0, 0), epaule_g=(-50, 0, 0), coude_g=(-60, 0, 0), epaule_d=(-172, 6, 0), coude_d=(-8, 0, 0))
MANOJ_BAISSE = pose(ASSIS, cou=(30, 0, 0), torse=(10, 0, 0), epaule_g=(-50, 0, 0), coude_g=(-70, 0, 0), epaule_d=(-50, 0, 0),
                    coude_d=(-70, 0, 0))
PARENT_SOUCI = pose(TAILLEUR, cou=(28, 0, 0), taille=(14, 0, 0), epaule_g=(-50, 0, -15), coude_g=(-70, 0, 0),
                    epaule_d=(-50, 0, 15), coude_d=(-70, 0, 0))
PARENT_MAIN_FRONT = pose(TAILLEUR, cou=(25, 0, 0), taille=(10, 0, 0), epaule_d=(-60, 0, -15), coude_d=(-150, 0, 0),
                         epaule_g=(-40, 0, 10), coude_g=(-60, 0, 0))
DEUIL = pose(BRAS_BAS, cou=(30, 0, 0), epaule_g=(-14, -4, 0), epaule_d=(-14, 4, 0), coude_g=(-60, 0, -20), coude_d=(-60, 0, 20))
DEUIL_VISAGE = pose(BRAS_BAS, cou=(32, 0, 0), taille=(6, 0, 0), epaule_g=(-60, 0, -20), coude_g=(-150, 0, 0),
                    epaule_d=(-60, 0, 20), coude_d=(-150, 0, 0))


def monde(obj_pos, angle, ech, pose_, enfant, j):
    """Position dans le monde d'une articulation d'un personnage posé avec P.perso (pour y attacher un objet)."""
    pts = positions(pose_, enfant)
    bas = min(pts[k].z - SQUELETTE[k][2][0] * 0.8 for k in ORDRE)
    v = (pts[j] - Vector((0, 0, bas))) * ech
    return Vector(obj_pos) + Euler((0, 0, rad(angle))).to_matrix() @ v


def versions(nom, poses_, ech, enfant, mat, pos, angle, bascule):
    """Deux versions d'un personnage ; la seconde remplace la première à l'image `bascule` (une action)."""
    a = P.perso(nom + "_a", poses_[0], ech, enfant, mat, pos, angle)
    b = P.perso(nom + "_b", poses_[1], ech, enfant, mat, pos, angle)
    return a, b, bascule


ACTIONS = []         # (plan, objet avant, objet après, image de bascule)

# ---------------------------------------------------------------- 5 ans : l'école
x = 0 * ESP
P.estrade("ecole", (x, 0), 1.9, M["terre_seche"])
P.boite("mur_ecole", (3.0, 0.22, 1.9), (x + 0.2, 1.2, H + 0.95), M["chaux"], biseau=0.02)
P.boite("porte_ecole", (0.7, 0.05, 1.3), (x - 0.6, 1.08, H + 0.65), M["bois"])
P.boite("enseigne", (1.4, 0.04, 0.32), (x + 0.6, 1.07, H + 1.55), P.materiau("enseigne", (0.08, 0.16, 0.30), 0.6, 0.3))
P.boite("guichet", (0.9, 0.5, 0.75), (x + 0.75, 0.55, H + 0.375), M["bois_clair"], biseau=0.015)
P.perso("clerc", CLERC, 0.95, False, M["argile_s"], (x + 0.8, 0.95, H), 180)
P.boite("chaise_clerc", (0.4, 0.4, 0.45), (x + 0.8, 1.0, H + 0.225), M["bois"])
for k in range(3):
    P.boite(f"billet_{k}", (0.15, 0.07, 0.004), (x + 0.6 + 0.04 * k, 0.45 - 0.03 * k, H + 0.755 + 0.002 * k), M["billet"],
            rot=(0, 0, 8 * k - 8))
P.perso("pere_ecole", PERE_TEND, 1.0, False, M["argile"], (x + 0.55, -0.15, H), 160)
P.perso("manoj_ecole", MANOJ_FIER, 0.6, True, M["rouge"], (x - 0.15, -0.3, H), 20)
P.boite("cartable", (0.2, 0.08, 0.24), (x - 0.15, -0.18, H + 0.48), P.materiau("cartable", (0.12, 0.10, 0.08), 0.7, 0.3), biseau=0.02)
P.projecteur("spot_ecole", (x - 1.6, -2.4, 3.6), (x + 0.2, 0.2, 0.6), 1100, (1.0, 0.88, 0.7), 40)
P.projecteur("contre_ecole", (x + 2.0, 2.6, 2.6), (x, 0, 0.8), 300, (0.7, 0.8, 1.0), 40)

# ---------------------------------------------------------------- 7 ans : les trois vignettes du choix
x = 1 * ESP
P.estrade("priere", (x, 0), 1.6, M["terre"])
P.boite("autel", (0.5, 0.35, 0.5), (x, 0.9, H + 0.25), M["glaise"], biseau=0.03)
P.boite("autel_haut", (0.32, 0.25, 0.4), (x, 0.92, H + 0.7), M["glaise"], biseau=0.02)
fl_m, _ = P.emission("flamme_priere", (1.0, 0.55, 0.15), 40)
for k, dx in enumerate((-0.35, 0.35)):
    P.cylindre(f"diya_p{k}", 0.05, 0.03, (x + dx, 0.6, H + 0.015), M["glaise"], sommets=16)
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.01, depth=0.045, location=(x + dx, 0.6, H + 0.06))
    bpy.context.object.data.materials.append(fl_m)
    P.lampe(f"diya_p{k}_l", (x + dx, 0.6, H + 0.1), 25, (1.0, 0.6, 0.25), 0.02)
for k in range(8):
    P.sphere(f"souci_autel_{k}", 0.03, (x - 0.21 + 0.06 * k, 0.74, H + 0.5), M["souci"], sub=1)
for k, (dx, dy, enf, mat) in enumerate(((-0.9, -0.1, False, M["argile"]), (-0.35, -0.45, True, M["rouge"]),
                                        (0.3, -0.5, False, M["argile_v"]), (0.85, -0.05, True, M["argile"]))):
    P.perso(f"prie_{k}", PRIERE, 0.6 if enf else 0.95, enf, mat, (x + dx, dy, H), 180 + (dx * -25))
P.projecteur("spot_priere", (x, -2.2, 3.4), (x, 0.2, 0.3), 600, (1.0, 0.8, 0.55), 40)

x = 2 * ESP
P.estrade("danse", (x, 0), 1.6, M["terre_seche"])
P.perso("danse_0", DANSE_A, 0.6, True, M["argile"], (x - 0.5, 0.1, H), 20)
P.perso("danse_1", DANSE_B, 0.62, True, M["argile"], (x + 0.45, -0.05, H), -25)
P.perso("danse_2", DANSE_A, 0.58, True, M["argile"], (x, 0.55, H), 0)
P.perso("tambour", pose(TAILLEUR, epaule_g=(-60, 0, -10), coude_g=(-50, 0, 0), epaule_d=(-60, 0, 10), coude_d=(-50, 0, 0)),
        0.95, False, M["argile_v"], (x + 1.0, 0.7, H), -120)
P.cylindre("dholak", 0.1, 0.32, (x + 0.82, 0.55, H + 0.32), M["bois_clair"], rot=(0, 90, 30), sommets=20)
P.projecteur("spot_danse", (x - 1.0, -2.2, 3.4), (x, 0.2, 0.6), 800, (1.0, 0.82, 0.6), 40)

x = 3 * ESP
P.estrade("cricket", (x, 0), 1.9, M["terre_seche"])
P.perso("batteur", BATTEUR, 0.62, True, M["argile"], (x - 0.7, 0.0, H), 90)
bat = P.boite("batte", (0.05, 0.03, 0.5), (0, 0, 0), M["bois_clair"])
pm = monde((x - 0.7, 0.0, H), 90, 0.62, BATTEUR, True, "main_d")
bat.location = pm + Vector((0.12, 0, -0.18))
bat.rotation_euler = (0, rad(-35), 0)
for k in range(3):
    P.cylindre(f"piquet_{k}", 0.012, 0.5, (x - 1.15, -0.06 + 0.06 * k, H + 0.25), M["bois_clair"], sommets=8)
P.perso("lanceur", LANCEUR, 0.6, True, M["argile"], (x + 1.1, 0.1, H), -90)
P.sphere("balle", 0.03, (x + 0.2, 0.0, H + 0.9), P.materiau("balle", (0.5, 0.05, 0.03), 0.4, 0.4))
P.projecteur("spot_cricket", (x, -2.6, 3.6), (x, 0, 0.4), 900, (1.0, 0.9, 0.75), 42)

# ---------------------------------------------------------------- 8 ans : « que veux-tu faire plus tard ? »
x = 4 * ESP
P.estrade("huit", (x, 0), 1.7, M["terre"])
P.perso("manoj_huit", ENFANT_DEBOUT_REGARDE, 0.65, True, M["rouge"], (x, 0, H), 0)
for k in range(5):
    a = rad(25 + k * 32.5)                          # en arc, derrière et autour de lui
    pos_ = (x + 1.15 * math.cos(a), 0.95 * math.sin(a) + 0.05, H)
    ang = math.degrees(math.atan2(-(pos_[0] - x), pos_[1]))         # il regarde Manoj
    P.perso(f"grand_{k}", ADULTE_GESTE if k == 2 else ADULTE_ASSIS, 0.95, False,
            M["argile_v"] if k % 2 else M["argile"], pos_, ang)
lampe_m, _ = P.emission("lampe_huit", (1.0, 0.7, 0.35), 18)
P.sphere("ampoule_huit", 0.05, (x + 0.1, 0.6, 1.9), lampe_m)
P.cylindre("fil_huit", 0.004, 1.2, (x + 0.1, 0.6, 2.5), M["fonte"], sommets=6)
P.lampe("lampe_huit_l", (x + 0.1, 0.6, 1.85), 160, (1.0, 0.72, 0.42), 0.05)
P.projecteur("lune_huit", (x - 2.0, 2.6, 3.4), (x, 0, 0.5), 200, (0.55, 0.68, 1.0), 40)
P.projecteur("face_huit", (x + 0.6, -2.6, 2.6), (x, 0, 0.5), 420, (1.0, 0.8, 0.6), 26)

# ---------------------------------------------------------------- 9 ans : la baguette
x = 5 * ESP
P.estrade("baguette", (x, 0), 1.5, M["chaux"])
P.boite("tableau_noir", (1.8, 0.06, 0.9), (x + 0.1, 1.05, H + 1.35), M["tableau_noir"], biseau=0.01)
maitre_pos, maitre_ang = (x + 0.75, 0.0, H), -90      # de profil, face à face
manoj_pos, manoj_ang = (x - 0.42, 0.0, H), 90
FRAPPE = int(2.85 * FPS)          # l'image où la baguette s'abat (calée sur « …sur la paume » au montage)
for etat, (pm_, pe_) in (("a", (MAITRE_HAUT, PAUME)), ("b", (MAITRE_BAS, PAUME_RETIREE))):
    m_ = P.perso(f"maitre_{etat}", pm_, 1.0, False, M["argile_s"], maitre_pos, maitre_ang)
    e_ = P.perso(f"manoj_bag_{etat}", pe_, 0.65, True, M["rouge"], manoj_pos, manoj_ang)
    bag = P.cylindre(f"baguette_{etat}", 0.008, 0.5, (0, 0, 0), M["bambou"], sommets=6)
    main = monde(maitre_pos, maitre_ang, 1.0, pm_, False, "main_g")
    poignet = monde(maitre_pos, maitre_ang, 1.0, pm_, False, "poignet_g")
    d_ = (main - poignet).normalized()
    bag.location = main + d_ * 0.25
    bag.rotation_euler = d_.to_track_quat("Z", "Y").to_euler()
    for o in (m_, e_, bag):
        ACTIONS.append(("baguette", o, etat == "b", FRAPPE))
P.projecteur("spot_baguette", (x - 1.4, -2.2, 3.2), (x, 0, 0.8), 900, (1.0, 0.92, 0.82), 34)
P.projecteur("contre_baguette", (x + 1.2, 2.2, 2.4), (x, 0, 1.0), 260, (0.75, 0.82, 1.0), 40)
P.projecteur("haut_baguette", (x + 1.9, -1.6, 3.6), (x + 0.75, 0, 2.0), 420, (0.85, 0.9, 1.0), 24, flou=0.5)

# ---------------------------------------------------------------- 9 ans : la classe, les mains qui se lèvent
x = 6 * ESP
P.estrade("classe", (x, 0), 2.6, M["chaux"])
P.boite("tableau_classe", (2.4, 0.06, 1.0), (x, 2.0, H + 1.4), M["tableau_noir"], biseau=0.01)
import random as _r  # noqa: E402
_r.seed(3)
places = [(x + dx, dy) for dy in (-0.9, -0.1, 0.7) for dx in (-1.2, -0.4, 0.4, 1.2)]
MANOJ_PLACE = 1                      # deuxième de la première rangée
for k, (px, py) in enumerate(places):
    P.boite(f"pupitre_{k}", (0.5, 0.32, 0.05), (px, py + 0.32, H + 0.52), M["bois"], biseau=0.008)
    P.boite(f"pupitre_pied_{k}", (0.46, 0.04, 0.5), (px, py + 0.46, H + 0.25), M["bois"])
    P.boite(f"banc_{k}", (0.42, 0.22, 0.04), (px, py - 0.02, H + 0.3), M["bois"])
    if k == MANOJ_PLACE:
        P.perso("manoj_classe", MANOJ_BAISSE, 0.62, True, M["rouge"], (px, py, H + 0.06), 180)
        continue
    bascule = int((0.45 + _r.uniform(0, 1.3)) * FPS)
    for etat, po in (("a", ELEVE_BAS), ("b", ELEVE_HAUT)):
        o = P.perso(f"eleve_{k}_{etat}", po, 0.6, True, M["argile"], (px, py, H + 0.06), 180)
        ACTIONS.append(("classe", o, etat == "b", bascule))
P.projecteur("spot_classe", (x, -3.6, 4.2), (x, 0, 0.6), 1400, (1.0, 0.93, 0.85), 48)
P.projecteur("contre_classe", (x + 1.0, 3.4, 3.0), (x, 0, 0.8), 300, (0.7, 0.8, 1.0), 50)

# ---------------------------------------------------------------- 9 ans : la dette (image fixe)
x = 7 * ESP
P.estrade("dette", (x, 0), 1.5, M["terre"])
P.perso("pere_dette", PARENT_MAIN_FRONT, 1.0, False, M["argile"], (x + 0.45, 0.1, H), -95)
P.perso("mere_dette", PARENT_SOUCI, 0.95, False, M["argile_v"], (x - 0.45, 0.15, H), 95)
P.boite("boite_fer", (0.24, 0.16, 0.08), (x, 0.0, H + 0.04), M["inox"], biseau=0.008)
P.boite("billet_seul", (0.15, 0.07, 0.004), (x + 0.02, 0.0, H + 0.083), M["billet"], rot=(0, 0, 14))
for k in range(4):
    P.cylindre(f"piece_{k}", 0.02, 0.004, (x - 0.08 + 0.05 * k, -0.14, H + 0.002), M["laiton"], sommets=16)
dl_m, _ = P.emission("flamme_dette", (1.0, 0.55, 0.15), 30)
P.cylindre("lampe_dette", 0.05, 0.05, (x - 0.05, 0.35, H + 0.025), M["glaise"], sommets=16)
bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.01, depth=0.045, location=(x - 0.05, 0.35, H + 0.08))
bpy.context.object.data.materials.append(dl_m)
P.lampe("lampe_dette_l", (x - 0.05, 0.35, H + 0.13), 35, (1.0, 0.6, 0.25), 0.02)
P.projecteur("lune_dette", (x - 1.5, 2.6, 3.2), (x, 0, 0.4), 160, (0.5, 0.62, 1.0), 40)

# ---------------------------------------------------------------- 10 ans : les funérailles du grand-père
x = 8 * ESP
P.estrade("funerailles", (x, 0), 2.1, M["terre"])
for k, dy in enumerate((-0.2, 0.2)):
    P.cylindre(f"brancard_{k}", 0.025, 2.0, (x, 0.3 + dy, H + 0.06), M["bambou"], rot=(0, 90, 0), sommets=10)
for k in range(5):
    P.cylindre(f"traverse_{k}", 0.015, 0.46, (x - 0.7 + 0.35 * k, 0.3, H + 0.06), M["bambou"], rot=(90, 0, 0), sommets=8)
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.17, depth=1.5, location=(x, 0.3, H + 0.2), rotation=(0, rad(90), 0))
corps = bpy.context.object
corps.scale = (1, 1, 1)
corps.data.materials.append(M["linge"])
bv = corps.modifiers.new("arrondi", "BEVEL")
bv.width, bv.segments = 0.12, 6
P.sphere("tete_linceul", 0.15, (x + 0.82, 0.3, H + 0.21), M["linge"], echelle=(1.1, 1, 0.9))
for k in range(26):
    t_ = k / 25
    P.sphere(f"guirlande_{k}", 0.03, (x - 0.65 + 1.4 * t_, 0.3 + 0.12 * math.sin(t_ * 9), H + 0.37), M["souci"], sub=1)
for k, (dx, dy, po, mat) in enumerate(((-0.8, 1.05, DEUIL, M["argile"]), (-0.2, 1.15, DEUIL_VISAGE, M["argile_v"]),
                                        (0.45, 1.1, DEUIL, M["argile"]), (1.0, 0.95, DEUIL_VISAGE, M["argile"]),
                                        (1.45, 0.35, DEUIL, M["argile_v"]))):
    ang = math.degrees(math.atan2(-dx, dy - 0.3))                    # ils regardent le corps
    P.perso(f"deuil_{k}", po, 1.0 if k != 4 else 0.95, False, mat, (x + dx, dy, H), ang)
P.perso("manoj_deuil", ENFANT_DEBOUT_REGARDE, 0.66, True, M["rouge"], (x - 1.35, -0.75, H),
        math.degrees(math.atan2(1.35, -0.75 - 0.3)))
fm, _ = P.emission("flamme_deuil", (1.0, 0.55, 0.15), 35)
for k, (dx, dy) in enumerate(((-0.95, 0.0), (0.95, 0.0), (0.0, -0.25))):
    P.cylindre(f"diya_d{k}", 0.045, 0.03, (x + dx, dy, H + 0.015), M["glaise"], sommets=16)
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.01, depth=0.045, location=(x + dx, dy, H + 0.06))
    bpy.context.object.data.materials.append(fm)
    P.lampe(f"diya_d{k}_l", (x + dx, dy, H + 0.1), 22, (1.0, 0.6, 0.25), 0.02)
P.projecteur("spot_deuil", (x + 0.5, -2.0, 3.8), (x, 0.4, 0.3), 380, (1.0, 0.85, 0.7), 36)
P.projecteur("sur_manoj", (x - 0.4, -2.4, 2.6), (x - 1.35, -0.75, 0.5), 160, (1.0, 0.78, 0.55), 14, flou=0.6)
P.projecteur("lune_deuil", (x - 2.4, 2.6, 3.0), (x, 0.3, 0.6), 220, (0.55, 0.66, 1.0), 44)

# ---------------------------------------------------------------- les plans : caméra (début, fin), visée, focale, durée
PLANS = {
    #  nom          : (position début,           position fin,              visée début,          visée fin,             focale, durée s)
    "ecole":        ((0 * ESP - 2.2, -3.6, 1.0), (0 * ESP - 1.5, -3.1, 0.9), (0.1, 0.2, 0.75), (0.25, 0.2, 0.7), 40, 5.4),
    "choix_priere": ((1 * ESP + 0.0, -3.4, 1.3), None, (0.0, 0.25, 0.4), None, 40, 0),
    "choix_danse":  ((2 * ESP - 0.4, -3.2, 1.2), None, (0.0, 0.2, 0.55), None, 40, 0),
    "choix_cricket": ((3 * ESP + 0.2, -3.6, 1.1), None, (0.0, 0.0, 0.45), None, 40, 0),
    "huit_ans":     ((4 * ESP + 1.0, -3.4, 1.7), (4 * ESP + 0.3, -2.8, 1.35), (0.0, 0.3, 0.5), (0.0, 0.2, 0.55), 38, 6.4),
    "baguette":     ((5 * ESP + 0.1, -5.0, 1.5), (5 * ESP + 0.15, -4.2, 1.3), (0.15, 0.0, 1.3), (0.1, 0.0, 1.05), 38, 4.4),
    "classe":       ((6 * ESP - 0.2, -4.4, 2.0), (6 * ESP - 0.4, -3.8, 1.6), (0.0, 0.3, 0.6), (-0.35, -0.6, 0.6), 36, 3.6),
    "dette":        ((7 * ESP + 0.0, -2.4, 1.05), None, (0.0, 0.1, 0.35), None, 42, 0),
    "funerailles":  ((8 * ESP - 2.6, -3.6, 1.35), (8 * ESP - 2.0, -3.0, 1.15), (0.1, 0.3, 0.45), (-0.4, -0.2, 0.55), 38, 7.0),
}


def ease(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


bpy.ops.object.camera_add()
cam = bpy.context.object
sc.camera = cam
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.8
foc = bpy.data.objects.new("point_net", None)
sc.collection.objects.link(foc)
cam.data.dof.focus_object = foc
os.makedirs(SORTIE, exist_ok=True)
os.makedirs(TEST, exist_ok=True)


def preparer(nom):
    p0, p1, v0, v1, focale, duree = PLANS[nom]
    xb = ESP * {"ecole": 0, "choix_priere": 1, "choix_danse": 2, "choix_cricket": 3, "huit_ans": 4, "baguette": 5,
                "classe": 6, "dette": 7, "funerailles": 8}[nom]
    cam.animation_data_clear()
    foc.animation_data_clear()
    cam.data.lens = focale
    n = max(1, int(round(duree * FPS)))
    sc.frame_start, sc.frame_end = 1, n
    for f in range(1, n + 1):
        q = ease((f - 1) / max(1, n - 1))
        pos = Vector(p0).lerp(Vector(p1 or p0), q)
        vis = Vector((xb, 0, 0)) + Vector(v0).lerp(Vector(v1 or v0), q)
        cam.location = pos
        cam.rotation_euler = (vis - pos).to_track_quat("-Z", "Y").to_euler()
        foc.location = vis
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        foc.keyframe_insert("location", frame=f)
    # les actions : chaque version n'est visible qu'avant ou après sa bascule
    for plan, o, apres, bascule in ACTIONS:
        o.animation_data_clear()
        for f in (1, bascule, bascule + 1, n + 1):
            vis_ = (f > bascule) if apres else (f <= bascule)
            o.hide_render = not vis_
            o.keyframe_insert("hide_render", frame=f)
    return n


bpy.ops.wm.save_as_mainfile(filepath=os.path.join(VIDEO, "medias", "blender", "S07_tableaux.blend"))
noms = [p.strip() for p in A.plans.split(",") if p.strip()] or list(PLANS)
for nom in noms:
    n = preparer(nom)
    if A.test:
        for f in sorted({1, n // 2 + 1, n}):
            sc.frame_set(f)
            sc.render.filepath = os.path.join(TEST, f"{nom}_{f:03d}.png")
            bpy.ops.render.render(write_still=True)
        continue
    d = os.path.join(SORTIE, nom)
    os.makedirs(d, exist_ok=True)
    for f in range(1, n + 1):
        chemin = os.path.join(d, f"{f:04d}.png")
        if os.path.exists(chemin):
            continue
        sc.frame_set(f)
        sc.render.filepath = chemin
        bpy.ops.render.render(write_still=True)
    print(f"[S07] {nom} : {n} images")
print("[S07] terminé")
