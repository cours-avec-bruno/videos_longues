"""S06 · passage 1 (0 -> 5 ans) : montage des images 3D (vignettes.py), des âges, de la fin sur le portrait, et du son.

L'habillage est volontairement sobre (Bruno, 08/11/2026 : le look « interface » faisait trop IA) :
l'âge en grand, dans un caractère à empattements, et une phrase en italique, en bas à gauche, qui apparaissent
quand la lumière de la scène s'allume et s'en vont avec elle. Pas d'interface, pas de cyan.
À la fin, le portrait de Manoj revient au centre et gagne un cran de netteté (le 2e sur 7).

Usage : python passage.py     ->  medias/S06/S06a_v1.mp4      (SON_SEUL=1 : ne refait que le son)
"""
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..", "..", "..")
sys.path.insert(0, os.path.join(RACINE, "shared", "outils", "son"))
sys.path.insert(0, os.path.join(ICI, "..", "S05"))
from pas import SR, boucle, ecrire_normalise, lire_audio  # noqa: E402
from fiche import portrait_cran  # noqa: E402

M = os.path.join(ICI, "..", "..", "medias")
IMG3D = os.path.join(M, "S06", "3d")
SONS = os.path.join(M, "sons", "epidemic")
OUT = os.path.join(M, "S06")
W, H, FPS = 1920, 1080, 24

# mêmes temps que vignettes.py
DEBUT, TENUE, TRAJET, N_SCENES = 0.3, 2.15, 0.5, 5
D3D = DEBUT + N_SCENES * TENUE + (N_SCENES - 1) * TRAJET
N3D = int(round(D3D * FPS))
NOIR = 0.3                   # le dernier tableau s'éteint
D_PORTRAIT = 2.4
DUREE = D3D + NOIR + D_PORTRAIT
N = int(round(DUREE * FPS))


def arrivee(i):
    return DEBUT + i * (TENUE + TRAJET)


AGES = ["1 an", "2 ans", "3 ans", "4 ans", "5 ans"]
PHRASES = [  # d'après le journal de la simulation (prompts/partie/7-vie-la-plus-probable.json)
    "Son premier mot : « Maman ».",
    "La boue, jusque sur ses vêtements.",
    "Les histoires d'autrefois de sa grand-mère.",
    "Le dal et les rotis de sa mère.",
    "Courir avec les autres jusqu'au coucher du soleil.",
]
F_AGE = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 92)
F_PHR = ImageFont.truetype("C:/Windows/Fonts/georgiai.ttf", 38)
CREME = (238, 230, 216)


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def titre(i):
    """L'âge et la phrase de la scène i, sur fond transparent (RGBA), avec une ombre douce."""
    calque = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)
    x, y = 150, 812
    d.text((x, y), AGES[i], font=F_AGE, fill=(*CREME, 255))
    d.text((x + 4, y + 112), PHRASES[i], font=F_PHR, fill=(*CREME, 215))
    a = np.asarray(calque).astype(np.float32)
    ombre = cv2.GaussianBlur(a[..., 3], (0, 0), 10) / 255
    return a[..., :3][..., ::-1].copy(), a[..., 3] / 255, ombre


TITRES = [titre(i) for i in range(N_SCENES)]


def opacite(i, t):
    a = arrivee(i)
    entree = lisse((t - (a + 0.35)) / 0.45)
    if i == N_SCENES - 1:
        sortie = 1 - lisse((t - (D3D - 0.35)) / 0.35)
    else:
        sortie = 1 - lisse((t - (a + TENUE - 0.45)) / 0.3)
    return entree * sortie


def image(n):
    t = n / FPS
    if t < D3D:
        f = cv2.imread(os.path.join(IMG3D, f"{min(n + 1, N3D):04d}.png")).astype(np.float32)
        for i in range(N_SCENES):
            o = opacite(i, t)
            if o <= 0:
                continue
            rgb, alpha, ombre = TITRES[i]
            dy = int(round(10 * (1 - lisse((t - (arrivee(i) + 0.35)) / 0.45))))
            if dy:
                rgb, alpha, ombre = (np.roll(v, dy, axis=0) for v in (rgb, alpha, ombre))
            f = f * (1 - 0.45 * o * ombre[..., None])
            f = f * (1 - o * alpha[..., None]) + rgb * (o * alpha[..., None])
        f += np.random.default_rng(n).normal(0, 2.4, f.shape).astype(np.float32)   # un grain discret
        return f
    if t < D3D + NOIR:
        f = cv2.imread(os.path.join(IMG3D, f"{N3D:04d}.png")).astype(np.float32)
        return f * (1 - lisse((t - D3D) / NOIR))
    tl = t - D3D - NOIR
    return portrait_cran(tl, 1, 2, n) * lisse(tl / 0.25)


SON_SEUL = os.environ.get("SON_SEUL") == "1"
if not SON_SEUL:
    if "--test" in sys.argv:
        for t in (arrivee(0) + 1.0, arrivee(2) + 1.2, D3D - 0.5, D3D + NOIR + 2.0):
            cv2.imwrite(os.path.join(sys.argv[-1], f"passage_{t:05.2f}.png"),
                        np.clip(image(int(t * FPS)), 0, 255).astype(np.uint8))
        sys.exit()
    ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                            os.path.join(OUT, "S06a_image.mp4")], stdin=subprocess.PIPE)
    for n in range(N):
        ecr.stdin.write(np.clip(image(n), 0, 255).astype(np.uint8).tobytes())
    ecr.stdin.close()
    ecr.wait()
    print("image :", round(DUREE, 2), "s")

# ---------------------------------------------------------------- le son
Ns = int(DUREE * SR)
mix = np.zeros((Ns, 2))
ts = np.arange(Ns) / SR


def db(x):
    return 10 ** (x / 20)


def fondu(n, e=0.0, s=0.0):
    f = np.ones(n)
    ne, ns_ = int(e * SR), int(s * SR)
    if ne:
        f[:min(ne, n)] = np.linspace(0, 1, min(ne, n))
    if ns_:
        f[-min(ns_, n):] = np.linspace(1, 0, min(ns_, n))
    return f


def poser(son, t0, gain=1.0):
    j = int(t0 * SR)
    if j >= Ns or j + len(son) <= 0:
        return
    a, b = max(0, -j), min(len(son), Ns - j)
    mix[j + a:j + b] += son[a:b] * gain


def lire(nom, dossier=SONS):
    return lire_audio(os.path.join(dossier, nom), mono=False).astype(np.float64)


def stereo(nom, debut, n, dossier=SONS):
    return boucle(lire(nom, dossier)[int(debut * SR):], n)


def env(t0, t1, e=0.25, s=0.3):
    return np.clip((ts - t0) / max(e, 1e-3), 0, 1) * np.clip((t1 - ts) / max(s, 1e-3), 0, 1)


def crete(a):
    return int(np.argmax(np.abs(a).mean(1)))


# chaque tableau s'allume : le claquement d'un projecteur dans une grande salle
proj = lire("projecteur.wav")
o_p = crete(proj)
seg_p = proj[max(0, o_p - int(0.01 * SR)):o_p + int(1.6 * SR)]
seg_p = seg_p * fondu(len(seg_p), 0.002, 0.8)[:, None]
for i in range(N_SCENES):
    poser(seg_p, arrivee(i) - 0.16, db(-11 if i else -9))
# les passages dans le noir : un souffle
wh = lire("whoosh_air.wav")
o_w = crete(wh)
for i in range(N_SCENES - 1):
    fin = arrivee(i) + TENUE
    seg = wh[max(0, o_w - int(0.35 * SR)):o_w + int(0.4 * SR)]
    poser(seg * fondu(len(seg), 0.15, 0.25)[:, None], fin + TRAJET / 2 - 0.35, db(-19))
# la vie de chaque tableau, très bas
ambiances = [
    ("bebe_babil.wav", 21.0, -18),
    ("village_amethi.wav", 50.0, -22),
    ("grillons_nuit.wav", 30.0, -16),
    ("feu_bois.wav", 25.0, -12),
    ("enfants_soir.wav", 40.0, -14),
]
for i, (nom, deb, g) in enumerate(ambiances):
    a = arrivee(i)
    t1 = a + TENUE + 0.1 if i < N_SCENES - 1 else D3D + 0.1
    mix += stereo(nom, deb, Ns) * (db(g) * env(a - 0.1, t1, 0.3, 0.3))[:, None]
boue = lire("boue_main.wav")
for k, dt in enumerate((0.55, 1.35)):
    poser(boue * fondu(len(boue), 0.005, 0.2)[:, None], arrivee(1) + dt, db(-15 - 3 * k))
# la musique de S05 revient, très discrète, sous les années
mus = stereo("bhimpalasi.wav", 95.0, Ns, os.path.join(M, "musique"))
mix += mus * (db(-22) * env(0.2, D3D + NOIR + 0.6, 1.2, 1.0))[:, None]
# le portrait se redivise : une pluie de tics, puis le cran gagné
tic = lire("tic_doux.wav")
o_t = crete(tic[:SR])
un_tic = tic[max(0, o_t - 100):o_t + int(0.05 * SR)] * fondu(o_t + int(0.05 * SR) - max(0, o_t - 100), 0.002, 0.03)[:, None]
t_p = D3D + NOIR
rng = np.random.default_rng(8)
for tt in np.sort(rng.uniform(t_p + 0.35, t_p + 1.45, 16)):
    poser(un_tic, tt, db(-26))
poser(un_tic, t_p + 1.45, db(-17))

GAIN = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
wav = os.path.join(OUT, "S06a_son.wav")
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN))
final = os.path.join(OUT, "S06a_v1.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, "S06a_image.mp4"), "-i", wav, "-map", "0:v",
                "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", final],
               check=True)
print("écrit :", final)
