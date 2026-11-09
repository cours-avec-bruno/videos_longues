"""S09 · la vie adulte (15 à 60 ans) : les images de départ en 3D (Blender, Eevee), une image par lieu.

Méthode (Bruno, 09/11/2026) : Blender pose la composition, les personnages et la lumière de base ; Higgsfield
l'embellit (restylage dans la DA) ; Seedance n'anime que les quelques plans qui doivent bouger. Le reste est
monté en images fixes, travaillées au montage.

Manoj est le seul en rouge laqué ; Preeti en safran ; les autres en satin gris. Sans visage.

Lancer sur le PC :
  "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b -P tableaux.py -- [--test] [--plans mer_nuit,mere]
Sorties (hors Git) : medias/S09/3d/<plan>.png
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
from mannequin import POSES  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--test", action="store_true")
ap.add_argument("--plans", default="")
A = ap.parse_args(argv)
SORTIE = os.path.join(VIDEO, "medias", "S09", "3d")
os.makedirs(SORTIE, exist_ok=True)

sc = P.scene(test=A.test, fps=24, images=1)
M = P.materiaux()
P.sol(centre=(180, 0), taille=(480, 120))
ESP = 30.0


def laque(nom, couleur, rugosite=0.1, vernis=0.03):
    m = P.materiau(nom, couleur, rugosite, 0.6)
    b = m.node_tree.nodes["Principled BSDF"]
    for cle, v in (("Coat Weight", 1.0), ("Coat Roughness", vernis)):
        if cle in b.inputs:
            b.inputs[cle].default_value = v
    return m


ROUGE = laque("manoj_laque", (0.62, 0.05, 0.025), 0.16)
SAFRAN = laque("preeti_laque", (0.85, 0.42, 0.05), 0.2)
GRIS = laque("satin_gris", (0.55, 0.52, 0.49), 0.38, 0.2)
NOIR = laque("noir_laque", (0.02, 0.02, 0.025), 0.12)
BLANC = laque("blouse", (0.85, 0.86, 0.88), 0.3)
EAU = P.materiau("eau", (0.006, 0.03, 0.04), 0.06, 0.8)
BRIQUE = P.materiau("brique", (0.45, 0.17, 0.08), 0.8, 0.2)
LANTERNE = P.emission("lanterne", (1.0, 0.62, 0.25), 18)[0]
GUIRLANDE = P.emission("guirlande", (1.0, 0.75, 0.4), 12)[0]
POISSON = P.materiau("poisson", (0.7, 0.72, 0.75), 0.2, 0.7, metal=0.8)


def pose(*parts, **extra):
    d = {}
    for p in parts:
        d.update(p)
    d.update(extra)
    return d


BAS = {"epaule_g": (-8, -6, 0), "epaule_d": (-8, 6, 0), "coude_g": (-12, 0, 0), "coude_d": (-12, 0, 0)}
CHANTE = pose(BAS, cou=(-14, 0, 0), epaule_g=(-150, -14, 0), epaule_d=(-150, 14, 0), coude_g=(-10, 0, 0), coude_d=(-10, 0, 0))
TIRE = pose(BAS, taille=(28, 0, 0), cou=(10, 0, 0), epaule_g=(-70, -4, 0), epaule_d=(-70, 4, 0), coude_g=(-20, 0, 0), coude_d=(-20, 0, 0))
ASSIS_BAS = pose(POSES["assis"], cou=(12, 0, 0))
ASSIS_TETE = pose(POSES["assis"], cou=(30, 0, 0), taille=(14, 0, 0), epaule_g=(-50, 0, 0), epaule_d=(-50, 0, 0),
                  coude_g=(-70, 0, 0), coude_d=(-70, 0, 0))
OFFRE = pose(BAS, cou=(8, 0, 0), epaule_d=(-62, 6, 0), coude_d=(-34, 0, 0), epaule_g=(-50, -6, 0), coude_g=(-40, 0, 0))
DROIT = pose(BAS)
TETE_BASSE = pose(BAS, cou=(30, 0, 0), taille=(8, 0, 0))
PORTE = pose(BAS, epaule_g=(-46, -6, 0), epaule_d=(-46, 6, 0), coude_g=(-78, 0, 0), coude_d=(-78, 0, 0), cou=(16, 0, 0))
SALUT = pose(BAS, epaule_g=(-110, -40, 0), epaule_d=(-110, 40, 0), coude_g=(-6, 0, 0), coude_d=(-6, 0, 0), cou=(-10, 0, 0))
POUSSE = pose(BAS, taille=(38, 0, 0), torse=(10, 0, 0), cou=(-6, 0, 0), epaule_g=(-85, -6, 0), epaule_d=(-85, 6, 0),
              coude_g=(-10, 0, 0), coude_d=(-10, 0, 0), hanche_g=(-30, 0, 0), genou_g=(30, 0, 0), hanche_d=(20, 0, 0))
DOS = pose(BAS, cou=(4, 0, 0))

PLANS = {}     # nom -> (n° du tableau, position caméra, visée, focale) ; relatifs au centre du tableau


def tableau(k):
    return k * ESP


def bateau(nom, x, y, ech=1.0, poissons=0):
    """Une barque de pêche en bois : coque, liston clair, deux bancs, un petit mât, une lanterne."""
    P.boite(nom + "_coque", (4.2 * ech, 1.35 * ech, 0.42 * ech), (x, y, 0.22 * ech), M["bois"], biseau=0.18 * ech)
    P.boite(nom + "_liston", (4.3 * ech, 1.42 * ech, 0.06 * ech), (x, y, 0.45 * ech), M["bois_clair"], biseau=0.02)
    P.boite(nom + "_proue", (0.5 * ech, 0.25 * ech, 0.5 * ech), (x + 2.2 * ech, y, 0.5 * ech), M["bois"], rot=(0, -30, 0), biseau=0.05)
    for k, dx in enumerate((-1.0, 0.6)):
        P.boite(f"{nom}_banc{k}", (0.22 * ech, 1.25 * ech, 0.05 * ech), (x + dx * ech, y, 0.42 * ech), M["bois_clair"])
    P.cylindre(nom + "_mat", 0.035 * ech, 2.4 * ech, (x - 0.2 * ech, y, 1.6 * ech), M["bambou"], sommets=8)
    P.sphere(nom + "_lanterne", 0.07 * ech, (x - 0.2 * ech, y - 0.12 * ech, 2.1 * ech), LANTERNE)
    P.lampe(nom + "_feu", (x - 0.2 * ech, y - 0.2 * ech, 2.05 * ech), 160 * ech, (1.0, 0.6, 0.28), 0.1)
    for k in range(poissons):
        P.sphere(f"{nom}_p{k}", 0.09, (x + 0.7 + 0.16 * (k % 6), y - 0.4 + 0.16 * (k // 6), 0.5 + 0.03 * (k % 3)),
                 POISSON, echelle=(2.2, 0.7, 0.6), sub=1)


# ---------------------------------------------------------------- 0 · la terre (l'autre voie à 15 ans)
x = tableau(0)
for k in range(9):
    P.boite(f"sillon_{k}", (7.0, 0.22, 0.12), (x + 0.5, -1.4 + 0.55 * k, 0.06), M["terre"], biseau=0.05)
P.perso("manoj_terre", DROIT, 0.92, False, ROUGE, (x - 1.4, -2.0, 0), 20)
P.cylindre("houe", 0.02, 1.3, (x - 1.0, -2.1, 0.62), M["bambou"], rot=(0, 18, 0), sommets=6)
P.projecteur("terre_soleil", (x + 6, 6, 3.0), (x, -1, 0), 5200, (1.0, 0.66, 0.38), 40, 0.3)
P.projecteur("terre_ciel", (x - 4, -6, 5), (x, 0, 0), 300, (0.4, 0.75, 1.0), 50, 0.6)
PLANS["terre"] = (0, (-3.2, -6.2, 1.3), (0.2, 0.6, 0.4), 32)

# ---------------------------------------------------------------- 1 · la mer, la nuit : presque sans poisson
x = tableau(1)
P.boite("eau_1", (40, 30, 0.02), (x, 6, 0.01), EAU)
bateau("barque_nuit", x, 0.5)
P.perso("manoj_nuit", TIRE, 0.95, False, ROUGE, (x + 0.9, 0.2, 0.12), 180)
P.perso("pecheur_nuit_1", ASSIS_BAS, 0.95, False, GRIS, (x - 1.0, 0.5, 0.12), 0)
P.perso("pecheur_nuit_2", TETE_BASSE, 0.95, False, GRIS, (x - 1.7, 0.6, 0.12), 30)
P.boite("filet_vide", (0.7, 0.5, 0.06), (x + 0.4, 0.5, 0.48), M["linge"], biseau=0.05)
P.projecteur("lune", (x - 6, 12, 7), (x, 0.5, 0.4), 900, (0.45, 0.72, 1.0), 30, 0.4)
P.projecteur("nuit_contre", (x + 4, 8, 2.5), (x, 0.5, 0.6), 600, (0.3, 0.9, 1.0), 26, 0.3)
PLANS["mer_nuit"] = (1, (-2.6, -7.2, 1.6), (0.0, 0.6, 0.8), 40)

# ---------------------------------------------------------------- 2 · le bateau revient plein, tout le monde chante
x = tableau(2)
P.boite("eau_2", (40, 30, 0.02), (x, 6, 0.01), EAU)
bateau("barque_plein", x, 0.5, poissons=24)
P.perso("manoj_chante", CHANTE, 0.95, False, ROUGE, (x - 0.2, 0.55, 0.12), 10)
P.perso("pecheur_ch_1", CHANTE, 0.95, False, GRIS, (x - 1.2, 0.5, 0.12), -15)
P.perso("pecheur_ch_2", pose(BAS, epaule_d=(-150, 14, 0), cou=(-10, 0, 0)), 0.95, False, GRIS, (x + 0.8, 0.6, 0.12), 25)
P.perso("pecheur_ch_3", ASSIS_BAS, 0.95, False, GRIS, (x - 1.9, 0.6, 0.12), 0)
for k in range(5):
    P.sphere(f"lanterne_pl_{k}", 0.06, (x - 1.8 + 0.9 * k, 0.5, 2.0 - 0.15 * abs(k - 2)), LANTERNE)
P.lampe("plein_feu", (x, -0.4, 2.2), 380, (1.0, 0.62, 0.3), 0.4)
P.projecteur("aube", (x + 8, 14, 3), (x, 0.5, 0.8), 2600, (1.0, 0.55, 0.3), 30, 0.3)
P.projecteur("plein_cyan", (x - 6, 8, 5), (x, 0.5, 0.8), 500, (0.3, 0.85, 1.0), 30, 0.4)
PLANS["bateau_plein"] = (2, (0.8, -5.4, 1.2), (0.0, 0.5, 1.2), 32)

# ---------------------------------------------------------------- 3 · le cadeau à sa mère
x = tableau(3)
P.boite("mur_mere", (6, 0.2, 3.2), (x, 1.6, 1.6), M["chaux"])
P.boite("porte_mere", (0.9, 0.22, 2.1), (x + 1.6, 1.55, 1.05), M["fonte"])
P.boite("tabouret", (0.45, 0.45, 0.42), (x - 0.5, 0.3, 0.21), M["bois"], biseau=0.03)
P.perso("mere", ASSIS_BAS, 0.9, False, GRIS, (x - 0.5, 0.3, 0), -60)
P.perso("manoj_offre", OFFRE, 0.95, False, ROUGE, (x + 0.55, 0.0, 0), 120)
P.boite("cadeau", (0.16, 0.12, 0.1), (x + 0.12, 0.05, 1.0), SAFRAN, biseau=0.01)
P.lampe("lampe_mere", (x - 0.1, -0.4, 1.9), 120, (1.0, 0.6, 0.3), 0.1)
P.projecteur("fenetre_mere", (x - 3.5, -2, 2.8), (x, 0.3, 0.8), 700, (0.4, 0.8, 1.0), 30, 0.5)
PLANS["mere"] = (3, (0.4, -3.6, 1.15), (0.0, 0.4, 0.95), 45)

# ---------------------------------------------------------------- 4 · l'hôpital (24 ans, la toux)
x = tableau(4)
P.boite("mur_hop", (7, 0.2, 3.2), (x, 1.8, 1.6), BLANC)
P.boite("fenetre_hop", (1.8, 0.24, 1.3), (x - 1.2, 1.75, 1.7), P.emission("fen_hop", (0.6, 0.9, 1.0), 6)[0])
P.boite("lit", (2.0, 0.95, 0.5), (x + 0.4, 0.6, 0.25), M["inox"], biseau=0.02)
P.boite("drap", (2.0, 0.98, 0.1), (x + 0.4, 0.6, 0.55), M["linge"], biseau=0.04)
P.perso("manoj_lit", ASSIS_TETE, 0.95, False, ROUGE, (x + 0.1, -0.05, 0), 0)
P.perso("medecin", DROIT, 1.0, False, BLANC, (x - 1.1, 0.0, 0), 50)
P.projecteur("hop_jour", (x - 2.5, 4, 2.6), (x, 0.4, 0.7), 1200, (0.55, 0.88, 1.0), 40, 0.6)
P.projecteur("hop_haut", (x + 0.3, -0.5, 3.2), (x + 0.2, 0.4, 0.6), 500, (0.9, 0.95, 1.0), 40, 0.5)
PLANS["hopital"] = (4, (1.6, -4.2, 1.3), (-0.2, 0.4, 0.8), 38)

# ---------------------------------------------------------------- 5 · les trois frères devant la mer, au crépuscule
x = tableau(5)
P.boite("eau_5", (40, 30, 0.02), (x, 16, 0.01), EAU)
for k, (dx, mat, ech) in enumerate(((-0.9, GRIS, 1.0), (-0.1, GRIS, 0.98), (0.75, ROUGE, 0.95))):
    P.perso(f"frere_{k}", DOS, ech, False, mat, (x + dx, 0.0, 0), 180)
P.projecteur("crepuscule", (x, 20, 1.6), (x, 0, 1.0), 9000, (1.0, 0.5, 0.25), 20, 0.3)
P.projecteur("freres_cyan", (x - 3, -4, 3), (x, 0, 0.8), 260, (0.3, 0.85, 1.0), 30, 0.5)
PLANS["freres"] = (5, (0.0, -4.6, 1.0), (0.0, 2.0, 1.0), 40)

# ---------------------------------------------------------------- 6 · Preeti (26 ans) : face à face, le soir
x = tableau(6)
P.perso("manoj_preeti", DROIT, 0.95, False, ROUGE, (x - 0.45, 0.2, 0), -80)
P.perso("preeti", pose(BAS, cou=(8, 0, 0)), 0.88, False, SAFRAN, (x + 0.45, 0.2, 0), 80)
P.cylindre("arbre", 0.18, 3.6, (x + 1.9, 1.4, 1.8), M["bois"], sommets=12)
P.sphere("feuillage", 1.4, (x + 1.7, 1.4, 3.6), P.materiau("feuille", (0.05, 0.16, 0.08), 0.7), echelle=(1.3, 1, 0.7))
P.projecteur("soir_preeti", (x + 5, 5, 2.0), (x, 0.2, 1.0), 3600, (1.0, 0.58, 0.3), 30, 0.3)
P.projecteur("preeti_cyan", (x - 4, -2, 3), (x, 0.2, 1.0), 420, (0.35, 0.85, 1.0), 30, 0.5)
PLANS["preeti"] = (6, (0.0, -3.4, 1.15), (0.0, 0.4, 1.05), 50)

# ---------------------------------------------------------------- 7 · le mariage : guirlandes de soucis, lumières
x = tableau(7)
P.perso("manoj_mariage", DROIT, 0.95, False, ROUGE, (x - 0.3, 0.3, 0), 0)
P.perso("preeti_mariage", pose(BAS, cou=(10, 0, 0)), 0.88, False, SAFRAN, (x + 0.3, 0.3, 0), 0)
for k in range(28):
    t = k / 27
    P.sphere(f"souci_{k}", 0.06, (x - 2.2 + 4.4 * t, 0.9, 2.6 - 0.6 * math.sin(math.pi * t)), M["souci"], sub=1)
    if k % 3 == 0:
        P.sphere(f"ampoule_{k}", 0.03, (x - 2.4 + 4.8 * t, 1.6, 3.0 - 0.5 * math.sin(math.pi * t)), GUIRLANDE, sub=1)
for k in range(6):
    P.perso(f"invite_{k}", DROIT, 0.9 + 0.04 * (k % 2), False, GRIS, (x - 2.5 + k * 1.0 + (0.4 if k > 2 else 0), 2.6, 0), 0)
P.projecteur("mariage_face", (x, -4, 3), (x, 0.3, 1.0), 1400, (1.0, 0.72, 0.45), 26, 0.4)
P.projecteur("mariage_cyan", (x + 4, 5, 3), (x, 1, 1.0), 600, (0.35, 0.85, 1.0), 40, 0.4)
PLANS["mariage"] = (7, (0.0, -4.4, 1.2), (0.0, 0.8, 1.2), 40)

# ---------------------------------------------------------------- 8 · Pradeep, puis Usha
x = tableau(8)
P.boite("banc_nais", (1.2, 0.45, 0.42), (x - 0.2, 0.3, 0.21), M["bois"], biseau=0.03)
P.perso("preeti_nais", pose(POSES["assis"], cou=(30, 0, 0), epaule_g=(-50, 0, 0), epaule_d=(-50, 0, 0),
                            coude_g=(-90, 0, 0), coude_d=(-90, 0, 0)),
        0.88, False, SAFRAN, (x - 0.35, 0.3, 0), 0)
P.sphere("bebe", 0.12, (x - 0.35, 0.05, 0.85), M["linge"], echelle=(1.5, 1, 1))
P.perso("manoj_nais", pose(BAS, cou=(24, 0, 0)), 0.95, False, ROUGE, (x + 0.45, 0.35, 0), -20)
P.perso("pradeep", DROIT, 0.5, True, GRIS, (x + 0.2, -0.2, 0), 10)
P.lampe("nais_lampe", (x, -0.6, 1.8), 140, (1.0, 0.65, 0.35), 0.2)
P.projecteur("nais_cyan", (x - 3, 3, 3), (x, 0.3, 0.8), 500, (0.35, 0.85, 1.0), 40, 0.5)
PLANS["naissance"] = (8, (0.2, -3.6, 1.0), (0.0, 0.3, 0.75), 42)

# ---------------------------------------------------------------- 9 · la maison qu'ils construisent (30 ans)
x = tableau(9)
for r in range(7):                               # deux murs à moitié montés, en briques
    for c in range(14 - (r // 2)):
        P.boite(f"bq_a{r}_{c}", (0.24, 0.11, 0.08), (x - 1.8 + c * 0.25 + (0.12 if r % 2 else 0), 1.2, 0.04 + r * 0.085), BRIQUE)
    for c in range(8 - r):
        P.boite(f"bq_b{r}_{c}", (0.11, 0.24, 0.08), (x - 1.85, 1.0 - c * 0.25 - (0.12 if r % 2 else 0), 0.04 + r * 0.085), BRIQUE)
P.perso("manoj_maison", PORTE, 0.95, False, ROUGE, (x + 0.3, 0.3, 0), -30)
P.boite("brique_main", (0.24, 0.11, 0.08), (x + 0.16, 0.05, 1.0), BRIQUE)
P.perso("preeti_maison", pose(BAS, epaule_d=(-60, 6, 0), coude_d=(-40, 0, 0)), 0.88, False, SAFRAN, (x - 0.6, 0.6, 0), 30)
P.perso("pradeep_m", DROIT, 0.55, True, GRIS, (x + 1.2, -0.1, 0), -40)
P.perso("usha_m", DROIT, 0.45, True, GRIS, (x + 1.55, 0.2, 0), -50)
P.projecteur("maison_soleil", (x + 5, 4, 5), (x, 0.6, 0.5), 5200, (1.0, 0.72, 0.45), 40, 0.3)
P.projecteur("maison_ciel", (x - 4, -4, 4), (x, 0.4, 0.6), 400, (0.4, 0.8, 1.0), 50, 0.5)
PLANS["maison"] = (9, (1.6, -4.4, 1.5), (-0.2, 0.6, 0.6), 34)

# ---------------------------------------------------------------- 10 · le mensonge (39 ans) : chacun de son côté
x = tableau(10)
P.boite("mur_mens", (7, 0.2, 3.2), (x, 1.8, 1.6), M["chaux"])
P.boite("fenetre_mens", (1.0, 0.24, 1.4), (x + 1.4, 1.75, 1.6), P.emission("fen_mens", (0.45, 0.8, 1.0), 4)[0])
P.perso("preeti_mens", DOS, 0.88, False, SAFRAN, (x + 1.4, 1.1, 0), 180)
P.perso("manoj_mens", TETE_BASSE, 0.95, False, ROUGE, (x - 1.5, 0.0, 0), 20)
P.perso("pradeep_mens", DROIT, 0.7, True, GRIS, (x + 0.1, 0.9, 0), 120)
P.perso("usha_mens", DROIT, 0.62, True, GRIS, (x + 0.45, 1.05, 0), 140)
P.projecteur("mens_fen", (x + 1.4, 3.5, 2.2), (x + 1.2, 0.5, 0.8), 900, (0.4, 0.8, 1.0), 26, 0.4)
P.projecteur("mens_lui", (x - 1.5, -1.5, 3.4), (x - 1.5, 0, 0.5), 160, (1.0, 0.55, 0.3), 16, 0.6)
PLANS["mensonge"] = (10, (-0.2, -4.6, 1.2), (0.0, 0.6, 0.9), 34)

# ---------------------------------------------------------------- 11 · la petite scène de théâtre (53 ans), vue depuis la salle
x = tableau(11)
VELOURS = P.materiau("velours", (0.25, 0.02, 0.03), 0.9, 0.1)
P.boite("planches", (5.0, 2.4, 0.6), (x, 1.4, 0.3), M["bois_clair"], biseau=0.02)
P.boite("rideau_fond", (5.2, 0.15, 3.6), (x, 2.6, 1.8), VELOURS)
for s in (-1, 1):
    P.boite(f"rideau_{s}", (0.8, 0.2, 3.6), (x + 2.4 * s, 1.0, 1.8), VELOURS)
P.perso("manoj_scene", SALUT, 0.95, False, ROUGE, (x, 1.0, 0.6), 0)
P.perso("acteur_2", DROIT, 0.92, False, GRIS, (x - 1.3, 1.8, 0.6), 20)
P.perso("acteur_3", DROIT, 0.9, False, GRIS, (x + 1.4, 1.9, 0.6), -20)
for r in range(3):
    for c in range(9):
        P.perso(f"spect_{r}_{c}", ASSIS_BAS, 0.95, False, NOIR, (x - 3.2 + c * 0.8 + 0.3 * (r % 2), -1.6 - r * 1.0, 0), 180)
P.projecteur("poursuite", (x, -5, 5), (x, 1.0, 1.4), 9000, (1.0, 0.86, 0.66), 12, 0.25)
P.projecteur("rampe", (x, -0.4, 0.9), (x, 1.6, 1.4), 700, (1.0, 0.6, 0.3), 50, 0.6)
P.projecteur("salle_cyan", (x - 4, -6, 4), (x, -2, 0.6), 300, (0.3, 0.85, 1.0), 50, 0.5)
PLANS["theatre"] = (11, (0.0, -6.6, 1.5), (0.0, 1.2, 1.3), 34)

# ---------------------------------------------------------------- 12 · 60 ans : à l'aube, il pousse encore la barque
x = tableau(12)
P.boite("eau_12", (40, 30, 0.02), (x, 8.5, 0.01), EAU)
P.boite("sable", (40, 8, 0.03), (x, -1.5, 0.015), M["terre_seche"])
bateau("barque_aube", x + 0.4, 1.4, ech=0.9)
P.perso("manoj_vieux", POUSSE, 0.92, False, ROUGE, (x - 2.2, 1.4, 0), -90)
P.projecteur("aube_60", (x + 14, 22, 1.8), (x, 1, 0.7), 9000, (1.0, 0.6, 0.35), 18, 0.3)
P.projecteur("aube_cyan", (x - 6, -6, 5), (x, 1, 0.5), 700, (0.35, 0.85, 1.0), 40, 0.5)
PLANS["vieux"] = (12, (-0.8, -6.0, 0.9), (0.0, 1.4, 0.7), 35)

# ---------------------------------------------------------------- rendu : une image par plan
bpy.ops.object.camera_add()
cam = bpy.context.object
sc.camera = cam
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.8
os.makedirs(os.path.join(VIDEO, "medias", "blender"), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(VIDEO, "medias", "blender", "S09_tableaux.blend"))
noms = [p.strip() for p in A.plans.split(",") if p.strip()] or list(PLANS)
for nom in noms:
    k, pos, vise, focale = PLANS[nom]
    xb = tableau(k)
    p = Vector(pos) + Vector((xb, 0, 0))
    v = Vector(vise) + Vector((xb, 0, 0))
    cam.location = p
    cam.rotation_euler = P.viser(p, v)
    cam.data.lens = focale
    cam.data.dof.focus_distance = (v - p).length
    sc.render.filepath = os.path.join(SORTIE, f"{nom}{'_test' if A.test else ''}.png")
    bpy.ops.render.render(write_still=True)
    print("[S09]", nom)
print("[S09] terminé")
