"""S05 · Les conditions de départ (≈ 37 s), construite le 07/11/2026 d'après le plan validé par Bruno.

Déroulé (temps de la scène) :
   0,0  noir, « manoj » en gros pixels lumineux (comme « commençons ») ; « Il s'appelle Manoj. »
   2,4  l'aube au village de pêcheurs : on tire les filets, en contre-jour ; la musique entre, à peine
   5,6  sa fiche de naissance (fiche.py : HUD cyan, nom, champs tapés, les aînés en pictos) ; « Avant lui… »
  11,0  des enfants devant une maison
  13,8  la cuisine sombre, le feu de bois, la fumée ; « On cuisine au feu de bois. Quand la fumée… »
  17,8  le feu de près ; « …ça lui pique les yeux, et il tousse. » (toux)
  20,6  une femme puise l'eau dans un lit de rivière à sec ; « L'eau, il faut aller la chercher… »
  25,6  le dossier d'inscription à l'école : la case « OBC » se coche toute seule
  29,4  retour sur la fiche : son portrait remplit le cadre en gros pixels ambrés (l'humain), la caméra s'approche ;
        jauge de netteté au premier cran : la même photo sera nette à sa mort (S11)
  32,6  l'opérateur seul dans le noir : « Je n'ai rien choisi de tout ça. Lui non plus. »
Images réelles : Pexels (étalonnage documentaire). Portrait : Pexels 16067431. Voix : prise 1, choisie par Bruno.

Usage : python montage.py
"""
import math
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..", "..", "..")
sys.path.insert(0, os.path.join(RACINE, "shared", "outils", "son"))
sys.path.insert(0, os.path.join(RACINE, "shared", "outils", "image"))
from pas import SR, boucle, ecrire_normalise, lire_audio  # noqa: E402
from effets import carton_pixel, etalonnage_doc, glitch, scan_cyan  # noqa: E402

M = os.path.join(ICI, "..", "..", "medias")
PX = os.path.join(M, "pexels", "s05")
SONS = os.path.join(M, "sons", "epidemic")
OUT = os.path.join(M, "S05")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1920, 1080, 24
FONTS = "C:/Windows/Fonts/"

# ---------------------------------------------------------------- le déroulé
PLANS = [  # (début, fin, genre, source)
    (0.0, 2.4, "carton", "manoj"),
    (2.4, 5.6, "video", ("4440945.mp4", 3.0, 1.0)),
    (5.6, 11.0, "fiche", None),
    (11.0, 13.8, "video", ("31700496.mp4", 2.0, 1.0)),
    (13.8, 17.8, "video", ("856779.mp4", 3.0, 1.0)),
    (17.8, 20.6, "video", ("4113114.mp4", 4.0, 1.0)),
    (20.6, 25.6, "video", ("38994414.mp4", 1.0, 1.0)),
    (25.6, 29.4, "formulaire", None),
    (29.4, 32.6, "portrait", None),
    (32.6, 37.0, "bureau", None),
]
DUREE = PLANS[-1][1]
N = int(round(DUREE * FPS))
VOIX = os.path.join(M, "voix", "S05_prise1.mp3")   # prise 1, choisie et verrouillée par Bruno
PHRASES = [  # (début, fin dans la prise, position)
    ((6.97, 8.25), 0.30),     # Il s'appelle Manoj.
    ((8.71, 11.46), 8.60),    # Avant lui, il y a déjà quatre enfants dans la maison.
    ((12.32, 13.40), 14.00),  # On cuisine au feu de bois.
    ((14.07, 18.38), 15.55),  # Quand la fumée remplit la cuisine, ça lui pique les yeux, et il tousse.
    ((19.47, 23.34), 21.00),  # L'eau, il faut aller la chercher, plus loin les mois où il ne pleut pas.
    ((24.84, 26.09), 33.20),  # Je n'ai rien choisi de tout ça.
    ((26.57, 27.12), 35.00),  # Lui non plus.
]


def lire_extrait(chemin, debut, vitesse, duree):
    n = int(math.ceil(duree * FPS)) + 2
    vf = f"setpts=PTS/{vitesse},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(debut), "-i", chemin, "-vf", vf, "-frames:v", str(n),
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(im) < n:
        im = np.concatenate([im, np.repeat(im[-1:], n - len(im), 0)])
    return im


def police(nom, t):
    return ImageFont.truetype(FONTS + nom, t)


F_MONO = police("consola.ttf", 46)


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


# ---------------------------------------------------------------- les écrans de la simulation
# la fiche de naissance et le portrait vivent dans fiche.py (refaits le 08/11/2026 d'après les références)
from fiche import CHAMPS, CPS, LIGNES_M, NOM, fiche  # noqa: E402
T_PORTRAIT = 1.3          # durée du balayage qui remplit le cadre du portrait


def ecran_formulaire(tl):
    im = Image.new("RGB", (W, H), (205, 210, 205))
    d = ImageDraw.Draw(im)
    encre = (40, 45, 55)
    d.text((220, 120), "ÉCOLE  ·  DOSSIER D'INSCRIPTION", font=police("consolab.ttf", 44), fill=encre)
    d.line([(220, 185), (W - 220, 185)], fill=encre, width=3)
    d.text((220, 240), "Nom de l'élève :  Manoj Mohanty", font=F_MONO, fill=encre)
    d.text((220, 320), "Année de naissance :  2026", font=F_MONO, fill=encre)
    d.text((220, 430), "Catégorie de caste :", font=F_MONO, fill=encre)
    choix = ["Catégorie générale", "Autres classes défavorisées (OBC)", "Castes répertoriées (SC)", "Tribus répertoriées (ST)"]
    for i, c in enumerate(choix):
        y = 520 + i * 90
        d.rectangle([300, y, 350, y + 50], outline=encre, width=4)
        d.text((380, y), c, font=F_MONO, fill=encre)
        if i == 1 and tl >= 1.6:                 # la case se coche toute seule
            p = lisse((tl - 1.6) / 0.25)
            d.line([(306, y + 6), (306 + 38 * p, y + 6 + 38 * p)], fill=(20, 20, 30), width=7)
            if p > 0.5:
                q = (p - 0.5) * 2
                d.line([(344, y + 6), (344 - 38 * q, y + 6 + 38 * q)], fill=(20, 20, 30), width=7)
    img = np.asarray(im)[:, :, ::-1].astype(np.float32)
    # la caméra s'approche de la case cochée
    z = 1 + 0.35 * lisse((tl - 1.2) / 2.0)
    Mz = cv2.getRotationMatrix2D((330, 615), 0, z)
    return cv2.warpAffine(img, Mz, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


# ---------------------------------------------------------------- fabrication des images
videos = {}
for deb, fin, genre, src in PLANS:
    if genre == "video":
        f, s0, vit = src
        videos[deb] = lire_extrait(os.path.join(PX, f), s0, vit, fin - deb + 0.2)
bureau = lire_extrait(os.path.join(M, "S02", "S02_p05.mp4"), 0.0, 1.0, 4.6)
cartes = {}


def image(tg):
    for deb, fin, genre, src in PLANS:
        if deb <= tg < fin + 1e-6:
            tl = tg - deb
            k = int(round(tl * FPS))
            if genre == "carton":
                if src not in cartes:
                    cartes[src] = carton_pixel(src)
                return cartes[src] + np.random.default_rng(k).normal(0, 2, (H, W, 3))
            if genre == "video":
                ims = videos[deb]
                z = 1 + 0.04 * tl / (fin - deb)
                f = ims[min(k, len(ims) - 1)].astype(np.float32)
                f = cv2.warpAffine(f, cv2.getRotationMatrix2D((W / 2, H / 2), 0, z), (W, H), borderMode=cv2.BORDER_REFLECT)
                return etalonnage_doc(f, k)
            if genre == "fiche":
                return fiche(tl, 0.0, 0.0, k)
            if genre == "formulaire":
                return scan_cyan(ecran_formulaire(tl), k, force=0.75)
            if genre == "portrait":
                # retour sur la fiche, complète : le visage remplit le cadre, la caméra s'en approche
                return fiche(20.0 + tl, lisse(tl / T_PORTRAIT), lisse((tl - 0.4) / 2.8), k)
            if genre == "bureau":
                return bureau[min(k, len(bureau) - 1)].astype(np.float32)
    return np.zeros((H, W, 3), np.float32)


# coupes entre le réel et la simulation : un court glitch ; entre images réelles : coupe franche
types = [p[2] for p in PLANS]
coupes_glitch = [PLANS[i][0] for i in range(1, len(PLANS))
                 if (types[i] in ("fiche", "formulaire", "portrait")) != (types[i - 1] in ("fiche", "formulaire", "portrait", "carton"))]
SON_SEUL = os.environ.get("SON_SEUL") == "1"
if not SON_SEUL:
    ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", os.path.join(OUT, "S05_image.mp4")],
                           stdin=subprocess.PIPE)
    for n in range(N):
        tg = n / FPS
        img = image(tg)
        for c in coupes_glitch:
            d_ = round((tg - c) * FPS)
            if d_ in (-1, 0, 1):
                img = glitch(img, n, {-1: 0.6, 0: 1.0, 1: 0.5}[d_])
        ecr.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
    ecr.stdin.close(); ecr.wait()
print("image :", DUREE, "s ; coupes glitch à", coupes_glitch)

# ---------------------------------------------------------------- le son
Ns = int(DUREE * SR)
ts = np.arange(Ns) / SR
mix = np.zeros((Ns, 2))


def db(x):
    return 10 ** (x / 20)


def fondu(n, e=0.0, s=0.0):
    g = np.ones(n); ne, ns = int(e * SR), int(s * SR)
    if ne:
        g[:ne] = np.linspace(0, 1, ne) ** 2
    if ns:
        g[-ns:] = np.linspace(1, 0, ns) ** 2
    return g


def poser(son, t0, gain=1.0):
    j = int(t0 * SR); f = min(Ns, j + len(son))
    if j < f:
        mix[j:f] += son[:f - j] * gain


def stereo(nom, debut, n, dossier=SONS):
    a = lire_audio(os.path.join(dossier, nom), mono=False).astype(np.float64)
    return boucle(a[int(debut * SR):], n)


def env(t0, t1, e=0.3, s=0.3):
    return np.clip((ts - t0) / e, 0, 1) * np.clip((t1 - ts) / s, 0, 1)


# le village : la mer et la vie du village, sous les images réelles (pas sous les écrans ni au bureau)
reel = np.zeros(Ns)
for deb, fin, genre, _ in PLANS:
    if genre == "video":
        reel = np.maximum(reel, env(deb - 0.05, fin + 0.05, 0.1, 0.1))
mix += stereo("vagues_plage.wav", 20.0, Ns) * (db(-15) * reel * np.where((ts > 13.8) & (ts < 20.6), 0.35, 1.0))[:, None]
mix += stereo("village_amethi.wav", 70.0, Ns) * (db(-16) * reel)[:, None]
# le feu
mix += stereo("feu_bois.wav", 10.0, Ns) * (db(-10) * env(13.8, 20.6, 0.2, 0.3))[:, None]
toux = lire_audio(os.path.join(SONS, "toux_enfant.wav"), mono=False).astype(np.float64)
poser(toux * fondu(len(toux), 0.01, 0.3)[:, None], 19.75, db(-12))
# la simulation : un tic doux par lettre de la fiche, le clic de la case
tic = lire_audio(os.path.join(SONS, "tic_doux.wav"), mono=False).astype(np.float64)
o_t = int(np.argmax(np.abs(tic[:SR]).mean(1)))
un_tic = tic[max(0, o_t - 100):o_t + int(0.06 * SR)] * fondu(o_t + int(0.06 * SR) - max(0, o_t - 100), 0.002, 0.03)[:, None]
for i in range(len(NOM)):                       # le nom
    poser(un_tic, 5.6 + 0.35 + i / 22, db(-26))
for _, val, t0 in CHAMPS:                       # les champs
    for i in range(len(val)):
        poser(un_tic, 5.6 + t0 + i / CPS, db(-27))
for r in range(LIGNES_M):                       # le portrait : une rangée de cases, un tic
    poser(un_tic, 29.4 + T_PORTRAIT * (r / LIGNES_M) / 1.25, db(-29))
clics = lire_audio(os.path.join(SONS, "souris_clics.wav"), mono=False).astype(np.float64)
o_c = int(np.argmax(np.abs(clics[int(5 * SR):int(8 * SR)]).mean(1))) + int(5 * SR)
poser(clics[o_c - 200:o_c + int(0.15 * SR)], 25.6 + 1.6, db(-6))
# glitch aux coupes réel / simulation
gr = lire_audio(os.path.join(SONS, "glitch_radio.wav"), mono=False).astype(np.float64)
o_g = int(np.argmax(np.abs(gr).mean(1)))
for c in coupes_glitch:
    seg = gr[max(0, o_g - int(0.02 * SR)):o_g + int(0.25 * SR)]
    poser(seg * fondu(len(seg), 0.003, 0.1)[:, None], c - 0.03, db(-16))
# le bureau : la pièce de S01-S02, au loin
piece = stereo("ambiance_grand_hall.wav", 120.0, Ns) * db(-11) + stereo("bourdonnement_ordinateur.wav", 100.0, Ns) * db(-22)
mix += piece * env(32.6, DUREE + 1, 0.2, 0.1)[:, None]
# la musique : entre à l'aube, discrète, monte un peu sur le portrait, s'efface au bureau
mus = stereo("bhimpalasi.wav", 0.0, Ns, os.path.join(M, "musique"))
g_mus = db(-20) * np.clip((ts - 2.4) / 2.5, 0, 1) * (1 + 0.6 * env(29.2, 32.8, 0.8, 0.8)) * np.clip((DUREE - 0.2 - ts) / 3.5, 0, 1)
mix += mus * g_mus[:, None]

# la voix (au niveau des autres scènes)
a_ = lire_audio(VOIX, mono=True).astype(np.float64)
actif = np.abs(a_) > 0.01
a_ *= db(-17.2 - 20 * np.log10(np.sqrt((a_[actif] ** 2).mean())))
voix = np.zeros(Ns)
for (a, b), pos in PHRASES:
    s_ = a_[int(a * SR):int(b * SR)]
    s_ = s_ * fondu(len(s_), 0.01, 0.06)
    j = int(pos * SR); f = min(Ns, j + len(s_))
    voix[j:f] += s_[:f - j]
env_voix = np.convolve(np.abs(voix) > 1e-3, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode="same")
mix *= (1 - 0.4 * np.clip(env_voix * 3, 0, 1))[:, None]
mix += voix[:, None] * db(-3.5)
mix *= fondu(Ns, 0.03, 0.2)[:, None]
GAIN = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
wav = os.path.join(OUT, "S05_son.wav")
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN))
final = os.path.join(OUT, "S05_v1.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, "S05_image.mp4"), "-i", wav, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", final], check=True)
print("écrit :", final)
