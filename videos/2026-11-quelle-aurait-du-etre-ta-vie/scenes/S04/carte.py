"""S04 · La carte du monde des densités de population (« plus de dix-sept pour cent de la population mondiale vit ici »).

Données :
  - population : Kontur Population 2023, hexagones H3 de ~22 km (r4), CC BY 4.0 (crédit à l'écran, en bas à gauche, et en description) ;
  - pays : Natural Earth 1:50m (domaine public).
Projection : Equal Earth (méridiens courbes, surfaces respectées : honnête pour une densité), puis une légère courbure
d'écran. Procédés : I03 (la carte se construit au rythme de la voix), I02 (un seul accent : l'humain en rouge-ambre),
H01 (source en bas à gauche). Le glitch d'entrée (T02) est fait au montage.

Animation (≈ 4,4 s) : les lumières de l'humanité s'allument, des plus denses aux moins denses ; la caméra glisse vers
l'Inde ; le reste du monde s'éteint un peu ; le contour de l'Inde se dessine ; une pulsation sur « vit ici ».

Usage : python carte.py --sortie ../../medias/S04/S04_carte.mp4
"""
import argparse
import json
import math
import os
import sqlite3
import subprocess

import cv2
import h3
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(ICI, "..", "..", "medias", "donnees")
ap = argparse.ArgumentParser()
ap.add_argument("--sortie", required=True)
ap.add_argument("--controle", default="")
A = ap.parse_args()

W, H, FPS = 1920, 1080, 24
DUREE = 4.4
# carte de travail en haute définition (on zoome dedans)
CW = 4400
A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
XMAX, YMAX = 2.70663, 1.31733
CH = int(CW * YMAX / XMAX)


def equal_earth(lon, lat):
    lam, phi = np.radians(lon), np.radians(lat)
    th = np.arcsin(np.sqrt(3) / 2 * np.sin(phi))
    t2 = th * th; t6 = t2 ** 3
    x = 2 * np.sqrt(3) * lam * np.cos(th) / (3 * (9 * A4 * t6 * t2 + 7 * A3 * t6 + 3 * A2 * t2 + A1))
    y = th * (A4 * t6 * t2 * t2 * 1.0 + A3 * t6 + A2 * t2 + A1) if False else A4 * th ** 9 + A3 * th ** 7 + A2 * th ** 3 + A1 * th
    px = (x / XMAX + 1) / 2 * CW
    py = (1 - (y / YMAX + 1) / 2) * CH
    return px, py


# ---------------------------------------------------------------- données
con = sqlite3.connect(os.path.join(D, "kontur_r4.gpkg"))
rows = con.execute("select h3, population from population").fetchall()
lat = np.empty(len(rows)); lon = np.empty(len(rows)); pop = np.empty(len(rows)); aire = np.empty(len(rows))
for i, (c, p) in enumerate(rows):
    lat[i], lon[i] = h3.cell_to_latlng(c)
    pop[i] = p
    aire[i] = h3.cell_area(c, unit="km^2")
dens = pop / aire
TOTAL = pop.sum()

pays = json.load(open(os.path.join(D, "ne_pays_50m.geojson"), encoding="utf-8"))


def polygones(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    return geom["coordinates"]


terre = np.zeros((CH, CW), np.uint8)
frontieres = np.zeros((CH, CW), np.uint8)
inde = np.zeros((CH, CW), np.uint8)
inde_trait = np.zeros((CH, CW), np.uint8)
for f in pays["features"]:
    est_inde = f["properties"].get("ADM0_A3") == "IND"
    for poly in polygones(f["geometry"]):
        for k, anneau in enumerate(poly):
            a = np.array(anneau)
            px, py = equal_earth(a[:, 0], a[:, 1])
            pts = np.stack([px, py], 1).astype(np.int32)
            if k == 0:
                cv2.fillPoly(terre, [pts], 255)
                if est_inde:
                    cv2.fillPoly(inde, [pts], 255)
            cv2.polylines(frontieres, [pts], True, 255, 2, cv2.LINE_AA)
            if est_inde:
                cv2.polylines(inde_trait, [pts], True, 255, 5, cv2.LINE_AA)

# vérification : part de la population mondiale qui vit en Inde (centre de l'hexagone dans le contour)
hx, hy = equal_earth(lon, lat)
dans_inde = inde[np.clip(hy.astype(int), 0, CH - 1), np.clip(hx.astype(int), 0, CW - 1)] > 0
print(f"Inde dans les données Kontur : {pop[dans_inde].sum() / 1e9:.2f} milliards, soit {100 * pop[dans_inde].sum() / TOTAL:.1f} % "
      f"de {TOTAL / 1e9:.2f} milliards")

# couche de densité : chaque hexagone devient une petite tache, valeur = log de la densité
val = np.zeros((CH, CW), np.float32)
ordre = np.argsort(dens)
rayon = max(2, int(CW / 360 * 0.21 / 2) + 1)
for i in ordre:
    if dens[i] < 0.5:
        continue
    v = math.log10(dens[i] + 1)
    cv2.circle(val, (int(hx[i]), int(hy[i])), rayon, float(v), -1)
val = cv2.GaussianBlur(val, (0, 0), 1.2)
VMAX = np.percentile(val[val > 0], 99.7)
val = np.clip(val / VMAX, 0, 1)


def rampe(v):
    """0 -> rouge sombre, 0,5 -> rouge, 0,8 -> orange, 1 -> ambre presque blanc (BGR)."""
    reperes = [(0.0, (6, 5, 25)), (0.35, (22, 22, 150)), (0.6, (30, 60, 235)), (0.8, (60, 150, 255)), (1.0, (175, 225, 255))]
    out = np.zeros(v.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = np.interp(v, [r[0] for r in reperes], [r[1][c] for r in reperes])
    return out


couleurs = rampe(val ** 1.8)          # les zones peu peuplées restent sombres : le contraste dit la réalité
fond = np.array([12, 8, 5], np.float32)
c_terre = np.array([44, 36, 20], np.float32)
c_front = np.array([150, 130, 60], np.float32)
terre_f = cv2.GaussianBlur(terre.astype(np.float32) / 255, (0, 0), 1.0)[..., None]
front_f = (frontieres.astype(np.float32) / 255)[..., None]
inde_f = cv2.GaussianBlur(inde.astype(np.float32) / 255, (0, 0), 6)[..., None]
trait_f = inde_trait.astype(np.float32) / 255
# ordre de tracé du contour de l'Inde : par angle autour de son centre
ys, xs = np.nonzero(inde)
cx_i, cy_i = xs.mean(), ys.mean()
yy, xx = np.mgrid[0:CH, 0:CW]
angle_trait = (np.arctan2(yy - cy_i, xx - cx_i) + math.pi) / (2 * math.pi)
angle_trait = ((angle_trait - 0.25) % 1.0).astype(np.float32)
del yy, xx
cible_x, cible_y = equal_earth(np.array([79.5]), np.array([22.5]))
cible_x, cible_y = float(cible_x[0]), float(cible_y[0])

police = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 24)
source = Image.new("L", (900, 40), 0)
ImageDraw.Draw(source).text((0, 4), "Données : Kontur Population 2023 (CC BY 4.0) · Natural Earth", font=police, fill=255)
source = np.asarray(source, np.float32) / 255

# courbure d'écran : léger bombé (les bords s'éloignent un peu)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
nx, ny = (xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)
r2 = nx * nx + ny * ny
k = 0.06
mapx = (W / 2 + nx * (1 + k * r2) * (W / 2)).astype(np.float32)
mapy = (H / 2 + ny * (1 + k * r2) * (H / 2) - 0.0).astype(np.float32)
vign = np.clip(1.12 - 0.42 * r2, 0.35, 1)[..., None]


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


N = int(DUREE * FPS)
rng = np.random.default_rng(3)
ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", A.sortie], stdin=subprocess.PIPE)
for n in range(N):
    t = n / FPS
    # caméra : le monde entier, puis glissement vers l'Inde
    pz = lisse((t - 0.9) / 2.6)
    zoom = 1.0 + 1.25 * pz
    larg = CW * 1.06 / zoom
    haut = larg * H / W
    cx = CW / 2 + (cible_x - CW / 2) * pz
    cy = CH / 2 + (cible_y - CH / 2) * pz
    x0, y0 = cx - larg / 2, cy - haut / 2
    M = np.float32([[W / larg, 0, -x0 * W / larg], [0, H / haut, -y0 * H / haut]])

    def vue(couche, interp=cv2.INTER_AREA):
        return cv2.warpAffine(couche, M, (W, H), flags=interp, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

    # allumage : des plus denses vers les moins denses
    seuil = 1.0 - lisse(t / 1.3) * 1.0
    allume = np.clip((val - seuil) / 0.12, 0, 1)
    # le reste du monde s'éteint un peu quand on arrive sur l'Inde
    att = 1 - 0.45 * lisse((t - 2.0) / 1.0)
    poids = allume[..., None] * (att + (1 - att) * inde_f)
    calque = couleurs * poids
    img_hd_terre = fond + (c_terre - fond) * terre_f + c_front * front_f * 0.28
    # composition à la résolution de sortie (on ne transforme que des couches)
    terre_v = vue(img_hd_terre)
    dens_v = vue(calque)
    halo = cv2.GaussianBlur(dens_v, (0, 0), 7) * 0.9 + cv2.GaussianBlur(dens_v, (0, 0), 22) * 0.6
    img = terre_v + dens_v * 1.05 + halo
    # contour de l'Inde qui se dessine, puis pulse sur « vit ici »
    pt = lisse((t - 2.2) / 0.8)
    if pt > 0:
        trait = trait_f * (angle_trait <= pt)
        trait_v = vue(trait)
        pulse = 1 + 0.6 * math.exp(-((t - 3.05) / 0.18) ** 2)
        lueur = cv2.GaussianBlur(trait_v, (0, 0), 5)
        img += (trait_v[..., None] * np.array([210, 240, 255]) * 0.9 + lueur[..., None] * np.array([120, 200, 255]) * 1.4) * pulse
    # source en bas à gauche (H01)
    a = min(1.0, t / 0.5) * 0.7
    sh, sw = source.shape
    img[H - 20 - sh:H - 20, 30:30 + sw] = img[H - 20 - sh:H - 20, 30:30 + sw] * (1 - source[..., None] * a) + 255 * source[..., None] * a
    # écran légèrement bombé, vignette, grain
    img = cv2.remap(img.astype(np.float32), mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(5, 4, 3))
    img = img * vign + rng.normal(0, 2.5, img.shape)
    ecr.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
    if A.controle and n in (0, 12, 30, 60, 80, N - 1):
        cv2.imwrite(os.path.join(A.controle, f"carte_{n:03d}.png"), np.clip(img, 0, 255).astype(np.uint8))
ecr.stdin.close(); ecr.wait()
print("écrit :", A.sortie, N, "images")
