"""S04 · La Terre vue de l'espace, qui tourne jusqu'à l'Inde, puis la plongée (sans rendu 3D).

Texture : NASA Blue Marble, « Whole world - land and oceans » (24000 x 12000, domaine public, via Wikimedia Commons),
réduite à 8192 x 4096 pour le globe, et l'Inde (60-100°E, 5-40°N) gardée en pleine résolution pour la plongée.
Projection orthographique calculée image par image (numpy + remap), éclairage solaire, atmosphère au bord,
quelques étoiles, flou de mouvement (sous-images) dans les passages rapides.

Usage : python terre.py --sortie ../../medias/S04/S04_terre.mp4
"""
import argparse
import math
import os
import subprocess

import cv2
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
NASA = os.path.join(ICI, "..", "..", "medias", "nasa")
ap = argparse.ArgumentParser()
ap.add_argument("--sortie", required=True)
ap.add_argument("--controle", default="")
A = ap.parse_args()

W, H, FPS = 1920, 1080, 24
BAS = cv2.imread(os.path.join(NASA, "terre_8192.png")).astype(np.float32)
HAUT = cv2.imread(os.path.join(NASA, "inde_pleine.png")).astype(np.float32)
LON0, LON1, LAT0, LAT1 = 60.0, 100.0, 5.0, 40.0
CIBLE = (26.3, 82.6)          # plaine du Gange, est de l'Uttar Pradesh
SOLEIL = np.array([math.cos(math.radians(12)) * math.cos(math.radians(55)),
                   math.cos(math.radians(12)) * math.sin(math.radians(55)), math.sin(math.radians(12))])

rng = np.random.default_rng(2)
etoiles = np.zeros((H * 2, W * 2), np.float32)
for _ in range(1400):
    x, y = rng.integers(0, W * 2), rng.integers(0, H * 2)
    etoiles[y, x] = rng.uniform(0.25, 1.0) ** 2.5
etoiles = cv2.GaussianBlur(etoiles, (0, 0), 0.9) * 2.2

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


def vue(lat_c, lon_c, R, cx=W / 2, cy=H / 2):
    la, lo = math.radians(lat_c), math.radians(lon_c)
    f = np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)])
    e = np.array([-math.sin(lo), math.cos(lo), 0.0])
    n = np.cross(f, e)
    u = (xx - cx) / R
    v = -(yy - cy) / R
    r2 = u * u + v * v
    dedans = r2 <= 1.0
    z = np.sqrt(np.clip(1 - r2, 0, 1))
    P = u[..., None] * e + v[..., None] * n + z[..., None] * f
    lat = np.degrees(np.arcsin(np.clip(P[..., 2], -1, 1)))
    lon = np.degrees(np.arctan2(P[..., 1], P[..., 0]))
    # texture basse résolution (monde)
    mx = ((lon + 180) / 360 * BAS.shape[1]).astype(np.float32)
    my = ((90 - lat) / 180 * BAS.shape[0]).astype(np.float32)
    img = cv2.remap(BAS, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    # pleine résolution sur l'Inde, quand on s'approche
    if R > 900:
        hx = ((lon - LON0) / (LON1 - LON0) * HAUT.shape[1]).astype(np.float32)
        hy = ((LAT1 - lat) / (LAT1 - LAT0) * HAUT.shape[0]).astype(np.float32)
        hi = cv2.remap(HAUT, hx, hy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        dans = ((lon > LON0 + 0.5) & (lon < LON1 - 0.5) & (lat > LAT0 + 0.5) & (lat < LAT1 - 0.5)).astype(np.float32)
        dans = cv2.GaussianBlur(dans, (0, 0), 6)[..., None]
        img = img * (1 - dans) + hi * dans
    # lumière du soleil, nuit bleutée, léger relief des océans plus sombres au bord
    lum = np.clip(P @ SOLEIL, -1, 1)
    jour = np.clip(lum * 1.6 + 0.25, 0.04, 1.0)[..., None]
    img = img * jour * 1.05
    # atmosphère : le bord du disque bleuit
    r = np.sqrt(r2)
    bleu = np.array([255, 170, 90], np.float32)          # BGR
    bord = np.clip((r - 0.80) / 0.20, 0, 1) ** 2.2 * dedans
    img = img * (1 - 0.55 * bord[..., None]) + bleu * (0.55 * bord[..., None]) * np.clip(lum * 1.5 + 0.4, 0.1, 1)[..., None]
    out = np.zeros((H, W, 3), np.float32)
    out[dedans] = img[dedans]
    # halo autour du globe
    halo = np.exp(-np.clip(r - 1.0, 0, None) * R / 22.0) * (r > 1.0)
    out += bleu * 0.35 * halo[..., None]
    return out, dedans


def lisse(p):
    return p * p * (3 - 2 * p)


N1, N2 = 52, 60                       # rotation rapide, puis plongée
N = N1 + N2
lat_dep, lon_dep = 8.0, -38.0
ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", A.sortie], stdin=subprocess.PIPE)
for k in range(N):
    acc = np.zeros((H, W, 3), np.float32)
    sous = 3
    for s in range(sous):
        tk = k + s / sous
        if tk < N1:
            p = lisse(tk / N1)
            lat_c = lat_dep + (CIBLE[0] - lat_dep) * p
            lon_c = lon_dep + (CIBLE[1] - lon_dep) * p
            R = 300 + 90 * p
        else:
            q = (tk - N1) / N2
            lat_c, lon_c = CIBLE
            R = 390 * math.exp(math.log(9000 / 390) * (q ** 2.3))   # lent au début (l'Inde se lit), puis on tombe
        img, dedans = vue(lat_c, lon_c, R)
        acc += img
    img = acc / sous
    # étoiles (seulement autour du globe), qui glissent un peu avec la rotation
    zoom_e = 1.0 + 0.15 * (k / N)
    ex = int((k * 6) % W)
    champ = cv2.resize(etoiles[ex // 2:ex // 2 + H, :W] if False else etoiles[:H, :W], (W, H))
    img += (champ * 255 * 0.8)[..., None] * (~dedans)[..., None] * (1.0 if k < N1 + 20 else max(0, 1 - (k - N1 - 20) / 15))
    # à la fin de la plongée : voile d'atmosphère qui monte (on traverse l'air), et flou radial
    if k >= N1:
        q = (k - N1) / N2
        voile = np.clip((q - 0.72) / 0.28, 0, 1) ** 1.5
        img = img * (1 - 0.55 * voile) + np.array([235, 215, 200], np.float32) * 0.55 * voile
        if q > 0.6:
            force = ((q - 0.6) / 0.4) ** 1.5
            m = img.copy()
            for j in range(1, 9):
                zz = 1 + 0.006 * j * force * 4
                Mz = cv2.getRotationMatrix2D((W / 2, H / 2), 0, zz)
                m += cv2.warpAffine(img, Mz, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            img = m / 9
    img += rng.normal(0, 1.2, img.shape)
    ecr.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
    if A.controle and k in (0, 26, 52, 80, 100, N - 1):
        cv2.imwrite(os.path.join(A.controle, f"terre_{k:03d}.png"), np.clip(img, 0, 255).astype(np.uint8))
ecr.stdin.close(); ecr.wait()
print("écrit :", A.sortie, N, "images")
