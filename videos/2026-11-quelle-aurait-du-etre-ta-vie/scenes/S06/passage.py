"""S06 · passage 1 (0 -> 5 ans) : les années de Manoj, regardées sur l'écran de l'opérateur.

Retours de Bruno (08/11/2026) : la voix décrit les scènes ; transitions plus lentes ; on doit avoir l'impression
de les regarder depuis l'ordinateur du protagoniste ; plus de portrait à la fin.

Déroulé :
  - on est assis au bureau (le regard de S02, lampe allumée : medias/S02/S02_p06_bureau.png) ; l'écran est noir ;
  - le premier tableau s'allume sur l'écran, et l'on s'approche lentement jusqu'à ce qu'il remplisse presque le cadre
    (le bord du moniteur reste visible : on regarde toujours son écran) ;
  - les cinq tableaux (vignettes.py) passent, chacun sur sa phrase (voix S06_prise3) ; l'âge s'inscrit sur l'écran ;
  - à la fin, on recule : le bureau revient, le coucher de soleil reste à l'écran.
Le son des tableaux est celui de l'ordinateur : étouffé quand on est loin, plein quand on est dedans. Sous tout, la pièce.

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

# ---------------------------------------------------------------- le bureau et son écran
BUREAU_F = os.path.join(M, "S02", "S02_p06_bureau.png")
if not os.path.exists(BUREAU_F):
    BUREAU_F = os.path.join(M, "S02", "S02_p01_fin.png")
BUREAU = cv2.imread(BUREAU_F).astype(np.float32)
# les coins de la dalle (mesurés sur l'image : même caméra que p01_fin)
QUAD = np.float32([[424, 114], [1511, 112], [1479, 719], [436, 709]])
SRC = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
H0 = cv2.getPerspectiveTransform(SRC, QUAD)
masque_dalle = np.zeros((H, W), np.uint8)
cv2.fillConvexPoly(masque_dalle, QUAD.astype(np.int32), 1)
base = np.median(BUREAU[masque_dalle > 0], axis=0)
diff = np.abs(BUREAU - base).max(2)
fenetre = np.zeros((H, W), np.uint8)
fenetre[222:598, 638:1292] = 1                                  # l'ancienne fenêtre claire de S02, remplacée
postit = ((diff > 14) & (masque_dalle > 0) & (fenetre == 0)).astype(np.uint8)
postit = cv2.morphologyEx(postit, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
postit = cv2.erode(cv2.dilate(postit, np.ones((9, 9), np.uint8)), np.ones((5, 5), np.uint8))
bord = cv2.erode(masque_dalle, np.ones((7, 7), np.uint8))
postit = postit * bord
POSTIT = np.zeros((H, W), np.float32)          # (les post-it de S02 sont retirés : l'image couvre tout l'écran)
# la lumière de l'écran retombe sur le bureau, la lampe, le pied (une tache douce sous et autour de la dalle)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
DEBORD = np.exp(-(((xx - 960) / 760) ** 2 + ((yy - 820) / 260) ** 2)) * (yy > 712)
DEBORD += 0.35 * np.exp(-(((xx - 960) / 700) ** 2 + ((yy - 410) / 420) ** 2)) * (1 - masque_dalle)
DEBORD = DEBORD.astype(np.float32)
C_ECRAN = QUAD.mean(0)                                          # centre de la dalle
S_MAX = 1.5                                                     # on reste devant son écran : le bord du moniteur se voit


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def doux(p):
    p = min(1.0, max(0.0, p))
    return p * p * p * (p * (p * 6 - 15) + 10)


T_FIN = DUREE - SORTIE                                          # début du recul


def approche(t):
    """0 : assis au bureau ; 1 : l'écran remplit presque le cadre."""
    entree = doux((t - 0.5) / 4.2)
    sortie = 1 - doux((t - (T_FIN + 0.2)) / (SORTIE - 0.6))
    return entree * sortie


def camera(t):
    e = approche(t)
    s = 1 + (S_MAX - 1) * e
    # un très léger flottement de la tête, plus discret quand on est près de l'écran
    fx = (2.5 * np.sin(0.63 * t) + 1.2 * np.sin(1.7 * t + 1)) * (1 - 0.6 * e)
    fy = (1.8 * np.sin(0.51 * t + 2) + 0.9 * np.sin(1.3 * t)) * (1 - 0.6 * e)
    cx, cy = C_ECRAN
    tx = (cx + (W / 2 - cx) * e) - s * cx + fx
    ty = (cy + (H / 2 - cy) * e) - s * cy + fy
    return np.float32([[s, 0, tx], [0, s, ty], [0, 0, 1]]), e


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
    fin = (a + TENUES[i] - 0.5) if i < N_SCENES - 1 else (T_FIN - 0.2)
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


# un reflet très doux sur la vitre de l'écran (en diagonale), dans le repère de l'image affichée
REFLET = (0.035 * np.clip(1 - np.abs((xx / W - yy / H * 0.6) - 0.25) / 0.35, 0, 1)).astype(np.float32)[..., None] * 255
VIG_ECRAN = (1 - 0.18 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)).astype(np.float32)[..., None]


def image(n):
    t = n / FPS
    A, e = camera(t)
    c = contenu(n, t)
    c = c * 0.93 * VIG_ECRAN + 5 + REFLET                       # un écran : noir pas tout à fait noir, un reflet
    # le bureau, de plus en plus flou à mesure qu'on regarde l'écran
    fond = BUREAU.copy()
    lum = cv2.resize(c, (8, 4), interpolation=cv2.INTER_AREA).mean((0, 1))
    fond += DEBORD[..., None] * lum[None, None, :] * 0.55
    fond = cv2.warpAffine(fond, A[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if e > 0.02:
        fond = cv2.GaussianBlur(fond, (0, 0), 0.5 + 3.5 * e)
    Hc = A @ H0
    ecr = cv2.warpPerspective(c, Hc, (W, H), flags=cv2.INTER_LINEAR)
    m = cv2.warpPerspective(np.ones((H, W), np.float32), Hc, (W, H), flags=cv2.INTER_LINEAR)
    pi = cv2.warpAffine(POSTIT, A[:2], (W, H), flags=cv2.INTER_LINEAR)
    m = m * (1 - pi)
    out = fond * (1 - m[..., None]) + ecr * m[..., None]
    rng = np.random.default_rng(n)
    out += rng.normal(0, 2.2, out.shape).astype(np.float32)
    # entrée depuis le noir (raccord avec la fin de S05) et petite respiration de fin
    out *= lisse(t / 0.35)
    return out


SON_SEUL = os.environ.get("SON_SEUL") == "1"
if not SON_SEUL:
    if "--test" in sys.argv:
        for t in (0.2, 1.6, 3.0, arrivee(0) + 3.5, arrivee(2) + 2.0, T_FIN + 1.0, DUREE - 0.1):
            n = min(N - 1, int(t * FPS))
            cv2.imwrite(os.path.join(sys.argv[-1], f"s06_{t:05.2f}.png"), np.clip(image(n), 0, 255).astype(np.uint8))
        sys.exit()
    ecr_ = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                             os.path.join(OUT, "S06a_image.mp4")], stdin=subprocess.PIPE)
    for n in range(N):
        ecr_.stdin.write(np.clip(image(n), 0, 255).astype(np.uint8).tobytes())
    ecr_.stdin.close()
    ecr_.wait()
    print("image :", round(DUREE, 2), "s")

# ---------------------------------------------------------------- le son
Ns = int(DUREE * SR)
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
    t1 = a + TENUES[i] + 0.3 if i < N_SCENES - 1 else DUREE + 1
    ecran_son += stereo(nom, deb, Ns) * (db(g) * env(a - 0.2, t1, 0.6, 0.7))[:, None]
boue = lire("boue_main.wav")
for k, dt in enumerate((1.0, 2.6)):
    poser(ecran_son, boue * fondu(len(boue), 0.005, 0.2)[:, None], arrivee(1) + dt, db(-16 - 3 * k))
# le son de l'ordinateur : étouffé quand on est loin de l'écran, plein quand on est dedans
e_t = np.array([approche(t) for t in np.arange(0, DUREE + 1 / FPS, 1 / FPS)])
e_s = np.interp(ts, np.arange(len(e_t)) / FPS, e_t)[:, None]
loin = passe_bas(ecran_son, 1800) * db(-4)
ecran_son = loin * (1 - e_s) + ecran_son * e_s
# la pièce, comme à la fin de S05 (un peu plus basse quand on est dans l'écran)
piece += stereo("ambiance_grand_hall.wav", 140.0, Ns) * db(-12) + stereo("bourdonnement_ordinateur.wav", 120.0, Ns) * db(-21)
piece *= (1 - 0.45 * e_s)
# la musique de S05 revient, très discrète
mus = stereo("bhimpalasi.wav", 95.0, Ns, os.path.join(M, "musique"))
mix = ecran_son + piece + mus * (db(-23) * env(1.0, DUREE + 0.5, 2.5, 1.0))[:, None]

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
