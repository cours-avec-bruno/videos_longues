"""S02-P03 · Gros plan sur le compteur des vies simulées (l'écran filmé de très près).

L'interface est celle de S01 (scenes/S01/ecran.py), dessinée en très haute définition ; on cadre le compteur,
on lui donne l'aspect d'un écran filmé de près (léger angle, faible profondeur de champ, trame, halo),
et la caméra glisse très lentement. Le compteur avance au rythme des naissances dans le monde (≈ 4,3 par seconde),
en continuité avec S01 (--t0 = temps écoulé depuis le début de S01).

Usage : python compteur.py --t0 24 --duree 7 --sortie ../../medias/S02/S02_p03_compteur.mp4
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "S01"))
import ecran  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--t0", type=float, default=24.0)
ap.add_argument("--duree", type=float, default=7.0)
ap.add_argument("--sortie", required=True)
A = ap.parse_args()

W, H, FPS = 1920, 1080, 24
ecran.SS = 4
ui = ecran.Interface(ecran.FOND_DEFAUT, ecran.CLAIR_DEFAUT)
SS = ecran.SS
# zone cadrée (en pixels de l'interface) : le compteur, en haut à droite, avec un peu d'air
X0, X1, Y0, Y1 = 1180, 1720, -20, 280
N = int(A.duree * FPS)
rng = np.random.default_rng(5)
trame = (np.indices((H, W)).sum(0) % 3 == 0).astype(np.float32)  # trame de pixels, très discrète

ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", A.sortie],
                       stdin=subprocess.PIPE)
for k in range(N):
    t = A.t0 + k / FPS
    im = np.asarray(ui.image(t, 10.0))[:, :, ::-1].astype(np.float32)
    # la caméra glisse lentement vers le chiffre
    p = k / max(1, N - 1)
    z = 1.0 + 0.06 * (p * p * (3 - 2 * p))
    cx, cy = (X0 + X1) / 2 * SS + 30 * SS * p, (Y0 + Y1) / 2 * SS
    lw, lh = (X1 - X0) * SS / z, (X1 - X0) * SS / z * H / W
    src = np.float32([[cx - lw / 2, cy - lh / 2], [cx + lw / 2, cy - lh / 2], [cx + lw / 2, cy + lh / 2], [cx - lw / 2, cy + lh / 2]])
    # léger angle : l'écran est vu un peu de biais
    dst = np.float32([[0, -30], [W, 10], [W, H - 10], [0, H + 30]])
    M = cv2.getPerspectiveTransform(src, dst)
    f = cv2.warpPerspective(im, M, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
    # profondeur de champ : net au centre droit (le chiffre), flou vers la gauche et les bords
    flou = cv2.GaussianBlur(f, (0, 0), 9)
    xx = np.linspace(-1, 1, W)[None, :]; yy = np.linspace(-1, 1, H)[:, None]
    net = np.clip(1.25 - np.sqrt(((xx - 0.25) / 0.9) ** 2 + (yy / 0.8) ** 2), 0, 1) ** 1.5
    f = f * net[:, :, None] + flou * (1 - net[:, :, None])
    f *= (1 - 0.06 * trame)[:, :, None]
    f += 0.18 * cv2.GaussianBlur(f, (0, 0), 25)               # halo de l'écran
    vign = np.clip(1.15 - 0.55 * (xx ** 2 + yy ** 2), 0.35, 1)
    f *= vign[:, :, None]
    f += rng.normal(0, 1.6, f.shape)
    ecr.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
ecr.stdin.close(); ecr.wait()
print("écrit :", A.sortie)
