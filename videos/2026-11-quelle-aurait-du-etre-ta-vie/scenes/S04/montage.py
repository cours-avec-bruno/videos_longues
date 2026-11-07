"""S03 + S04 · « Commençons. On peut atterrir n'importe où. » (version écrite par Bruno, 07/11/2026)

Déroulé (≈ 37 s) :
  1. l'écran des réglages (S03 : le monde d'aujourd'hui, une vie entière, « France ») ; « Commençons. » ; clic sur « Naître » ;
  2. on plonge dans l'écran ;
  3. douze lieux du monde, vite, reliés par des traversées (on fonce dans l'image et on ressort dans la suivante),
     le rythme s'accélère ;
  4. on sort dans l'espace : la Terre tourne jusqu'à l'Inde, puis la plongée (terre.py) ;
  5. coupe sur un village du nord de l'Inde vu du ciel : « C'est ici que nous sommes arrivés. » ;
     puis une ruelle du village : « Pas étonnant : plus de dix-sept pour cent de la population mondiale vit ici. »
Extraits : Pexels (licence Pexels, usage commercial libre, sans attribution obligatoire) ; Terre : NASA Blue Marble.
Sons : Epidemic Sound. Voix : ElevenLabs, Guillaume. Sources et identifiants : ../../references/sons.md et images.md.

Usage : python montage.py
"""
import math
import os
import subprocess
import sys

import cv2
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", "..", "shared", "outils", "son"))
from pas import SR, boucle, detecter_pas, ecrire_normalise, lire_audio  # noqa: E402

M = os.path.join(ICI, "..", "..", "medias")
PX = os.path.join(M, "pexels")
SONS = os.path.join(M, "sons", "epidemic")
W, H, FPS = 1920, 1080, 24

# ---------------------------------------------------------------- le déroulé (temps en secondes)
T_CLIC = 14.6                  # clic sur « Naître »
T_MONDE = 15.2                 # premier lieu
LIEUX = [                      # (fichier, début dans la source, vitesse) : de jour, de nuit, près, loin
    ("tokyo_6574285.mp4", 6.0, 1.0),
    ("paris_34558256.mp4", 4.0, 1.6),
    ("rio_16023860.mp4", 3.0, 1.6),
    ("newyork_5565202.mp4", 30.0, 1.6),
    ("caire_10717893.mp4", 20.0, 1.8),
    ("venise_36328559.mp4", 4.0, 1.5),
    ("kenya_7499056.mp4", 6.0, 1.5),
    ("shanghai_33009782.mp4", 5.0, 1.5),
    ("sydney_36924503.mp4", 4.0, 1.6),
    ("sahara_37523973.mp4", 1.0, 1.4),
    ("islande_29477448.mp4", 8.0, 1.8),
    ("amazonie_35969886.mp4", 12.0, 1.8),
]
DUREES = list(np.linspace(0.95, 0.55, len(LIEUX)))     # le rythme s'accélère
T_ESPACE = T_MONDE + sum(DUREES)
TERRE = os.path.join(M, "S04", "S04_terre.mp4")
D_TERRE = 112 / FPS
T_VILLAGE = T_ESPACE + D_TERRE
VILLAGE = [("inde/inde_31372348.mp4", 1.0, 1.0, 3.2), ("inde/inde_34732091.mp4", 0.5, 1.0, 4.8)]
DUREE = T_VILLAGE + sum(v[3] for v in VILLAGE)
N = int(round(DUREE * FPS))
TR = 0.20                      # durée d'une traversée (de chaque côté de la coupe)


def lire_extrait(chemin, debut, vitesse, duree):
    """Lit un extrait à 24 i/s, en 1920 x 1080 (recadré si besoin), accéléré de `vitesse`."""
    n = int(math.ceil(duree * FPS)) + 2
    vf = f"setpts=PTS/{vitesse},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(debut), "-i", chemin, "-vf", vf, "-frames:v", str(n),
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(im) < n:
        im = np.concatenate([im, np.repeat(im[-1:], n - len(im), 0)])
    return im


def zoom(img, z, flou=0.0):
    """Agrandit autour du centre ; `flou` ajoute un flou radial (plusieurs copies de plus en plus grandes)."""
    if z <= 1.0001 and flou <= 0:
        return img.astype(np.float32)
    M_ = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
    base = cv2.warpAffine(img, M_, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    if flou <= 0:
        return base
    acc = base.copy()
    k = 6
    for j in range(1, k + 1):
        Mj = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z * (1 + flou * j / k))
        acc += cv2.warpAffine(img, Mj, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return acc / (k + 1)


# ---------------------------------------------------------------- les plans, chacun avec son début et sa fin
plans = []      # (début, fin, images, poussée)  ; la poussée = zoom lent continu pendant le plan
DECAL = int(T_CLIC * FPS) - 4          # avant la plongée, l'écran passe tel quel (lu en flux, sans tout charger)
ecran = lire_extrait(os.path.join(M, "S03", "S03_image.mp4"), DECAL / FPS, 1.0, T_MONDE - DECAL / FPS + 0.1)
plans.append((0.0, T_MONDE, ecran, 0.0))
t = T_MONDE
for (f, deb, vit), d in zip(LIEUX, DUREES):
    plans.append((t, t + d, lire_extrait(os.path.join(PX, f), deb, vit, d + 0.3), 0.10))
    t += d
terre = lire_extrait(TERRE, 0, 1.0, D_TERRE)
plans.append((T_ESPACE, T_VILLAGE, terre, 0.0))
t = T_VILLAGE
for f, deb, vit, d in VILLAGE:
    plans.append((t, t + d, lire_extrait(os.path.join(PX, f), deb, vit, d + 0.2), 0.04))
    t += d
coupes = [p[0] for p in plans[1:]]


def image_du_plan(i, tg):
    deb, fin, ims, pousse = plans[i]
    k = min(len(ims) - 1, max(0, int(round((tg - deb) * FPS)) - (DECAL if i == 0 else 0)))
    p = (tg - deb) / max(1e-6, fin - deb)
    z = 1 + pousse * p
    flou = 0.0
    # sortie : on fonce dans l'image (sauf la Terre, qui gère sa propre plongée, et la fin)
    if i < len(plans) - 1 and fin - tg < TR and i != len(plans) - 3:
        u = 1 - (fin - tg) / TR
        z *= 1 + 0.9 * u ** 2
        flou = 0.10 * u
    # entrée : on ressort du flou, en se posant
    if i > 0 and tg - deb < TR:
        u = (tg - deb) / TR
        z *= 1 + 0.45 * (1 - u) ** 2
        flou = max(flou, 0.08 * (1 - u))
    if i == 0 and tg > T_CLIC:            # la plongée dans l'écran, plus longue
        u = min(1, (tg - T_CLIC) / (T_MONDE - T_CLIC))
        z = 1 + 2.2 * u ** 2.2
        flou = 0.12 * u ** 1.5
    return zoom(ims[k], z, flou)


SON_SEUL = os.environ.get("SON_SEUL") == "1"   # SON_SEUL=1 : ne refait que le son
ecr = None if SON_SEUL else subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                        os.path.join(M, "S04", "S03_S04_image.mp4")], stdin=subprocess.PIPE)
rng = np.random.default_rng(9)
if not SON_SEUL:
  flux = subprocess.Popen(["ffmpeg", "-v", "error", "-i", os.path.join(M, "S03", "S03_image.mp4"), "-frames:v", str(DECAL),
                         "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
  for n in range(DECAL):
    ecr.stdin.write(flux.stdout.read(W * H * 3))
  flux.wait()
for n in (range(0) if SON_SEUL else range(DECAL, N)):
    tg = n / FPS
    i = max(j for j, p in enumerate(plans) if p[0] <= tg + 1e-6)
    img = image_du_plan(i, tg)
    # fondu court autour de chaque coupe (deux images de part et d'autre), avec un éclair de lumière
    for c_ in coupes:
        if abs(tg - c_) < 2.5 / FPS:
            j = [p[0] for p in plans].index(c_)
            autre = image_du_plan(j - 1 if tg >= c_ else j, tg)
            a = 0.5 - (tg - c_) / (5 / FPS) if tg >= c_ else 0.5 - (c_ - tg) / (5 / FPS)
            img = img * (1 - a) + autre * a
            eclair = 1 - abs(tg - c_) / (2.5 / FPS)
            img = img + 60 * eclair * (0.4 if j - 1 >= 1 else 1.0)
    img += rng.normal(0, 1.0, img.shape)
    ecr.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
if ecr:
    ecr.stdin.close(); ecr.wait()
print("image :", round(DUREE, 2), "s,", N, "images ; espace à", round(T_ESPACE, 2), "; village à", round(T_VILLAGE, 2))

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


def stereo(nom, debut, n):
    a = lire_audio(os.path.join(SONS, nom), mono=False).astype(np.float64)
    return boucle(a[int(debut * SR):], n)


# 1. la pièce (les mêmes sons qu'en S01-S02), qui disparaît quand on plonge dans l'écran
pièce = stereo("ambiance_grand_hall.wav", 90.0, Ns) * db(-13)
pièce += stereo("bourdonnement_ordinateur.wav", 80.0, Ns) * db(-17)
pièce += stereo("bourdonnement_lumiere.wav", 2.0, Ns) * db(-23)
env_piece = np.clip((T_CLIC + 0.5 - ts) / 0.5, 0, 1)
mix += pièce * env_piece[:, None]

# 2. la souris et le clavier pendant les réglages (temps de la fenêtre = temps de la scène)
clics = lire_audio(os.path.join(SONS, "souris_clics.wav"), mono=False).astype(np.float64)
ons_c = detecter_pas(os.path.join(SONS, "souris_clics.wav"), seuil_db=-25, ecart_min=0.3)
for j_, tc in enumerate([0.4, 1.5, 3.5, 9.4, T_CLIC]):
    o = ons_c[(j_ * 5 + 3) % len(ons_c)]
    s_ = clics[int((o - 0.005) * SR):int((o + 0.18) * SR)]
    poser(s_ * fondu(len(s_), 0.002, 0.06)[:, None], tc - 0.005, db(-8 if tc != T_CLIC else -5))
tapis = lire_audio(os.path.join(SONS, "souris_tapis.wav"), mono=False).astype(np.float64)
for j_, (d0, d1) in enumerate([(0.0, 0.35), (0.6, 1.4), (1.8, 3.3), (4.0, 8.9), (12.6, 13.6)]):
    n_ = int((d1 - d0) * SR); o = 1.0 + j_ * 1.7
    s_ = tapis[int(o * SR):int(o * SR) + n_]
    poser(np.pad(s_, ((0, n_ - len(s_)), (0, 0))) * fondu(n_, 0.08, 0.15)[:, None], d0, db(-16))
clav = lire_audio(os.path.join(SONS, "clavier_lent.wav"), mono=False).astype(np.float64)
ons_k = detecter_pas(os.path.join(SONS, "clavier_lent.wav"), seuil_db=-22, ecart_min=0.15)
for j_, tk in enumerate([10.7, 10.9, 11.08, 11.25, 11.42, 11.6, 12.5]):
    o = ons_k[(j_ * 4 + 2) % len(ons_k)]
    s_ = clav[int((o - 0.005) * SR):int((o + 0.12) * SR)]
    poser(s_ * fondu(len(s_), 0.002, 0.04)[:, None], tk - 0.005, db(-9 if j_ < 6 else -6))

# 3. les traversées : un souffle à chaque passage, de plus en plus serré
whooshs = [lire_audio(os.path.join(SONS, n_), mono=False).astype(np.float64)
           for n_ in ("whoosh_air.wav", "whoosh_zoom.wav")]
crete = lambda a: int(np.argmax(np.abs(a).mean(1)))
poser(whooshs[1] * fondu(len(whooshs[1]), 0.01, 0.4)[:, None], T_MONDE - crete(whooshs[1]) / SR, db(-4))   # la plongée dans l'écran
for j_, c_ in enumerate(coupes[1:len(LIEUX)]):
    w_ = whooshs[j_ % 2]
    # légère variation de hauteur : on rééchantillonne
    f_ = 1 + 0.06 * ((j_ * 7) % 5 - 2)
    idx = np.arange(0, len(w_) - 1, f_)
    w2 = np.stack([np.interp(idx, np.arange(len(w_)), w_[:, c]) for c in range(2)], 1)
    poser(w2 * fondu(len(w2), 0.01, 0.3)[:, None], c_ - crete(w2) / SR, db(-12 - 0.3 * j_))

# 4. un grondement grave qui monte pendant le monde, culmine dans l'espace, se coupe à l'arrivée
drone = stereo("espace_drone.wav", 10.0, Ns)
monte = np.clip((ts - T_MONDE) / (T_ESPACE - T_MONDE), 0, 1) ** 1.5 * 0.55
monte = np.where(ts >= T_ESPACE, 1.0, monte)
monte *= np.clip((T_VILLAGE - ts) / 0.08, 0, 1)
mix += drone * (db(-9) * monte)[:, None]
fusee = lire_audio(os.path.join(SONS, "whoosh_fusee.wav"), mono=False).astype(np.float64)
poser(fusee * fondu(len(fusee), 0.3, 0.1)[:, None], T_VILLAGE - len(fusee) / SR + 0.05, db(-6))     # la plongée finale

# 5. l'arrivée : le village (enregistré à Amethi, Uttar Pradesh)
village = stereo("village_amethi.wav", 30.0, Ns) * db(-12)
env_v = np.clip((ts - T_VILLAGE) / 0.12, 0, 1)
mix += village * env_v[:, None]

# 6. la voix
VOIX_DB = -3.5
phrases = [
    ("S03_prise1.mp3", (0.00, 1.31), 1.6),      # Le monde d'aujourd'hui.
    ("S03_prise1.mp3", (1.59, 3.10), 3.6),      # Une vie entière.
    ("S03_prise1.mp3", (3.77, 7.22), 6.0),      # Le site demande aussi où je suis né, pour comparer à la fin.
    ("S03_prise1.mp3", (7.54, 8.27), 10.0),     # J'écris :
    ("S03_prise1.mp3", (8.54, 9.45), 11.0),     # France.
    ("S04_prise2.mp3", (0.00, 0.66), 13.85),    # Commençons.
    ("S04_prise2.mp3", (1.02, 3.24), T_MONDE + 0.2),   # On peut atterrir n'importe où.
    ("S04_prise2.mp3", (3.45, 4.88), T_VILLAGE + 0.5),  # C'est ici que nous sommes arrivés.
    ("S04_prise2.mp3", (5.28, 9.44), T_VILLAGE + VILLAGE[0][3] + 0.4),  # Pas étonnant : plus de dix-sept pour cent...
]
voix = np.zeros(Ns); cache = {}
for f_, (a, b), pos in phrases:
    if f_ not in cache:
        a_ = lire_audio(os.path.join(M, "voix", f_), mono=True).astype(np.float64)
        actif = np.abs(a_) > 0.01
        niveau = 20 * np.log10(np.sqrt((a_[actif] ** 2).mean()))
        cache[f_] = a_ * db(-17.2 - niveau)      # toutes les prises au niveau de la voix de S02 (prise 1)
    s_ = cache[f_][int(a * SR):int(b * SR)]
    s_ = s_ * fondu(len(s_), 0.01, 0.06)
    j = int(pos * SR); f2 = min(Ns, j + len(s_))
    voix[j:f2] += s_[:f2 - j]
env_voix = np.convolve(np.abs(voix) > 1e-3, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode="same")
mix *= (1 - 0.35 * np.clip(env_voix * 3, 0, 1))[:, None]
mix += voix[:, None] * db(VOIX_DB)
mix *= fondu(Ns, 0.05, 0.4)[:, None]
GAIN = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
wav = os.path.join(M, "S04", "S03_S04_son.wav")
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN))
final = os.path.join(M, "S04", "S03_S04_v1.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(M, "S04", "S03_S04_image.mp4"), "-i", wav, "-map", "0:v",
                "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest",
                "-movflags", "+faststart", final], check=True)
print("écrit :", final)
