"""S06 · passage 1 (0 -> 5 ans) : les années de Manoj, regardées dans une fenêtre de l'interface de l'opérateur.

Retours de Bruno (08/11/2026) : la voix décrit les scènes ; transitions plus lentes ; on regarde depuis l'ordinateur
du protagoniste, mais comme une interface de PC (sa capture de référence) : une fenêtre aux petits bords ronds qui ne
prend pas tout l'écran, un léger quadrillage de pixels ; plus de portrait à la fin.

Déroulé :
  - le noir, puis la fenêtre s'ouvre (elle grandit un peu en apparaissant) ;
  - les cinq tableaux (vignettes.py) passent dedans, chacun sur sa phrase (voix S06_prise3) ; l'âge s'y inscrit ;
  - à la fin, sur le coucher de soleil, la fenêtre se referme.
Le son des tableaux sort de l'ordinateur (un peu étouffé quand la fenêtre s'ouvre ou se ferme) ; dessous, la pièce.

Usage : python passage.py     ->  medias/S06/S06a_v1.mp4      (SON_SEUL=1 : ne refait que le son ; --test <dossier>)
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
sys.path.insert(0, ICI)
from pas import SR, boucle, ecrire_normalise, lire_audio  # noqa: E402
from temps_s06 import AVANT, DUREE, FPS, N, N_SCENES, PHRASES, SORTIE, TENUES, TRAJET, VOIX, arrivee  # noqa: E402

M = os.path.join(ICI, "..", "..", "medias")
IMG3D = os.path.join(M, "S06", "3d")
SONS = os.path.join(M, "sons", "epidemic")
OUT = os.path.join(M, "S06")
W, H = 1920, 1080

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def doux(p):
    p = min(1.0, max(0.0, p))
    return p * p * p * (p * (p * 6 - 15) + 10)


FIN = DUREE - 2.0                 # le montage s'arrête un peu avant la fin du rendu 3D (le recul n'existe plus)
N_M = int(round(FIN * FPS))
T_FIN = FIN - 1.0                 # la fenêtre commence à se refermer

# ---------------------------------------------------------------- la fenêtre de l'interface
FW, FH = 1680, 945                # elle ne prend pas tout l'écran
RAYON = 16                        # de petits bords ronds
FOND = np.float32([13, 12, 12])


def masque_arrondi(w, h, r, k=4):
    m = Image.new("L", (w * k, h * k), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * k - 1, h * k - 1], radius=r * k, fill=255)
    return np.asarray(m.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255


MASQUE = masque_arrondi(FW, FH, RAYON)
LISERE = np.clip(MASQUE - cv2.erode(MASQUE, np.ones((5, 5), np.uint8)), 0, 1)     # un fin liseré, à peine plus clair
gy, gx = np.mgrid[0:FH, 0:FW]
QUADRILLAGE = (1 - 0.13 * ((gx % 4) == 0) - 0.13 * ((gy % 4) == 0)).astype(np.float32)[..., None]   # le léger quadrillage
VIG_F = (1 - 0.12 * (((gx - FW / 2) / (FW / 2)) ** 2 + ((gy - FH / 2) / (FH / 2)) ** 2)).astype(np.float32)[..., None]


def ouverture(t):
    """0 : fenêtre fermée ; 1 : ouverte."""
    return doux((t - 0.2) / 0.8) * (1 - doux((t - T_FIN) / 0.9))


# ---------------------------------------------------------------- l'âge, inscrit sur l'écran
F_AGE = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 104)
CREME = (238, 230, 216)
AGES = ["1 an", "2 ans", "3 ans", "4 ans", "5 ans"]


def calque_age(i):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((140, 870), AGES[i], font=F_AGE, fill=(*CREME, 255))
    a = np.asarray(c).astype(np.float32)
    return a[..., :3][..., ::-1].copy(), a[..., 3] / 255, cv2.GaussianBlur(a[..., 3], (0, 0), 10) / 255


CALQUES = [calque_age(i) for i in range(N_SCENES)]


def opacite_age(i, t):
    a = arrivee(i)
    entree = lisse((t - (a + 0.3)) / 0.6)
    fin = (a + TENUES[i] - 0.5) if i < N_SCENES - 1 else (T_FIN - 0.4)
    return entree * (1 - lisse((t - fin) / 0.5))


def contenu(n, t):
    f = cv2.imread(os.path.join(IMG3D, f"{min(n + 1, N):04d}.png")).astype(np.float32)
    for i in range(N_SCENES):
        o = opacite_age(i, t)
        if o <= 0:
            continue
        rgb, alpha, ombre = CALQUES[i]
        dy = int(round(12 * (1 - lisse((t - (arrivee(i) + 0.3)) / 0.6))))
        if dy:
            rgb, alpha, ombre = (np.roll(v, dy, axis=0) for v in (rgb, alpha, ombre))
        f = f * (1 - 0.45 * o * ombre[..., None])
        f = f * (1 - o * alpha[..., None]) + rgb * (o * alpha[..., None])
    return f


def image(n):
    t = n / FPS
    o = ouverture(t)
    out = np.empty((H, W, 3), np.float32)
    out[:] = FOND
    if o > 0.001:
        c = cv2.resize(contenu(n, t), (FW, FH), interpolation=cv2.INTER_AREA)
        c = c * QUADRILLAGE * VIG_F
        li = 0.6 * LISERE[..., None]
        fen = c * (1 - li) + np.float32([58, 56, 56]) * li
        # la fenêtre apparaît en grandissant un peu, et disparaît de même
        s_ = 0.95 + 0.05 * o
        w_, h_ = int(round(FW * s_)), int(round(FH * s_))
        fen = cv2.resize(fen, (w_, h_), interpolation=cv2.INTER_AREA)
        m = cv2.resize(MASQUE, (w_, h_), interpolation=cv2.INTER_AREA)[..., None] * o
        x0, y0 = (W - w_) // 2, (H - h_) // 2
        zone = out[y0:y0 + h_, x0:x0 + w_]
        out[y0:y0 + h_, x0:x0 + w_] = zone * (1 - m) + fen * m
    rng = np.random.default_rng(n)
    out += rng.normal(0, 1.8, out.shape).astype(np.float32)
    return out


SON_SEUL = os.environ.get("SON_SEUL") == "1"
if not SON_SEUL:
    if "--test" in sys.argv:
        for t in (0.6, 3.0, arrivee(2) + 2.0, T_FIN + 0.5):
            n = min(N_M - 1, int(t * FPS))
            cv2.imwrite(os.path.join(sys.argv[-1], f"s06_{t:05.2f}.png"), np.clip(image(n), 0, 255).astype(np.uint8))
        sys.exit()
    ecr_ = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                             os.path.join(OUT, "S06a_image.mp4")], stdin=subprocess.PIPE)
    for n in range(N_M):
        ecr_.stdin.write(np.clip(image(n), 0, 255).astype(np.uint8).tobytes())
    ecr_.stdin.close()
    ecr_.wait()
    print("image :", round(FIN, 2), "s")

# ---------------------------------------------------------------- le son
Ns = int(FIN * SR)
ts = np.arange(Ns) / SR
ecran_son = np.zeros((Ns, 2))          # ce qui sort de l'ordinateur
piece = np.zeros((Ns, 2))              # la pièce


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


def poser(bus, son, t0, gain=1.0):
    j = int(t0 * SR)
    if j >= Ns or j + len(son) <= 0:
        return
    a, b = max(0, -j), min(len(son), Ns - j)
    bus[j + a:j + b] += son[a:b] * gain


def lire(nom, dossier=SONS):
    return lire_audio(os.path.join(dossier, nom), mono=False).astype(np.float64)


def stereo(nom, debut, n, dossier=SONS):
    return boucle(lire(nom, dossier)[int(debut * SR):], n)


def env(t0, t1, e=0.25, s=0.3):
    return np.clip((ts - t0) / max(e, 1e-3), 0, 1) * np.clip((t1 - ts) / max(s, 1e-3), 0, 1)


def crete(a):
    return int(np.argmax(np.abs(a).mean(1)))


def passe_bas(x, fc):
    """Filtre passe-bas doux (par FFT), pour le son « dans l'ordinateur »."""
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (1 / np.sqrt(1 + (f / fc) ** 4))[:, None]
    return np.fft.irfft(X, n=len(x), axis=0)


# l'ordinateur : chaque tableau qui s'allume, les passages, la vie de chaque tableau
proj = lire("projecteur.wav")
o_p = crete(proj)
seg_p = proj[max(0, o_p - int(0.01 * SR)):o_p + int(1.6 * SR)]
seg_p = seg_p * fondu(len(seg_p), 0.002, 0.8)[:, None]
for i in range(N_SCENES):
    poser(ecran_son, seg_p, arrivee(i) - 0.22, db(-12))
wh = lire("whoosh_air.wav")
o_w = crete(wh)
for i in range(N_SCENES - 1):
    fin = arrivee(i) + TENUES[i]
    seg = wh[max(0, o_w - int(0.7 * SR)):o_w + int(0.7 * SR)]
    poser(ecran_son, seg * fondu(len(seg), 0.4, 0.5)[:, None], fin + TRAJET / 2 - 0.7, db(-21))
ambiances = [("bebe_babil.wav", 21.0, -19), ("village_amethi.wav", 50.0, -21), ("grillons_nuit.wav", 30.0, -17),
             ("feu_bois.wav", 25.0, -13), ("enfants_soir.wav", 40.0, -15)]
for i, (nom, deb, g) in enumerate(ambiances):
    a = arrivee(i)
    t1 = a + TENUES[i] + 0.3 if i < N_SCENES - 1 else FIN + 0.2
    ecran_son += stereo(nom, deb, Ns) * (db(g) * env(a - 0.2, t1, 0.6, 0.7))[:, None]
boue = lire("boue_main.wav")
for k, dt in enumerate((1.0, 2.6)):
    poser(ecran_son, boue * fondu(len(boue), 0.005, 0.2)[:, None], arrivee(1) + dt, db(-16 - 3 * k))
# le son de l'ordinateur : un peu étouffé quand la fenêtre s'ouvre ou se ferme
e_t = np.array([ouverture(t) for t in np.arange(0, FIN + 1 / FPS, 1 / FPS)])
e_s = np.interp(ts, np.arange(len(e_t)) / FPS, e_t)[:, None]
loin = passe_bas(ecran_son, 1800) * db(-4)
ecran_son = loin * (1 - e_s) + ecran_son * e_s
# la pièce, comme à la fin de S05 (un peu plus basse quand la fenêtre est ouverte)
piece += stereo("ambiance_grand_hall.wav", 140.0, Ns) * db(-12) + stereo("bourdonnement_ordinateur.wav", 120.0, Ns) * db(-21)
piece *= (1 - 0.45 * e_s)
# la musique de S05 revient, très discrète
mus = stereo("bhimpalasi.wav", 95.0, Ns, os.path.join(M, "musique"))
mix = ecran_son + piece + mus * (db(-23) * env(1.0, FIN + 0.2, 2.5, 1.2))[:, None]

# la voix (prise 3, au niveau des autres scènes), chaque phrase sur son tableau
a_ = lire_audio(os.path.join(M, "voix", VOIX), mono=True).astype(np.float64)
actif = np.abs(a_) > 0.01
a_ *= db(-17.2 - 20 * np.log10(np.sqrt((a_[actif] ** 2).mean())))
voix = np.zeros(Ns)
for i, (a, b) in enumerate(PHRASES):
    s_ = a_[int(a * SR):int(b * SR)]
    s_ = s_ * fondu(len(s_), 0.01, 0.06)
    j = int((arrivee(i) + AVANT) * SR)
    f = min(Ns, j + len(s_))
    voix[j:f] += s_[:f - j]
env_voix = np.convolve(np.abs(voix) > 1e-3, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode="same")
mix *= (1 - 0.4 * np.clip(env_voix * 3, 0, 1))[:, None]
mix += voix[:, None] * db(-3.5)
mix *= fondu(Ns, 0.05, 0.3)[:, None]

GAIN = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
wav = os.path.join(OUT, "S06a_son.wav")
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN))
final = os.path.join(OUT, "S06a_v1.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, "S06a_image.mp4"), "-i", wav, "-map", "0:v",
                "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", final],
               check=True)
print("écrit :", final)
