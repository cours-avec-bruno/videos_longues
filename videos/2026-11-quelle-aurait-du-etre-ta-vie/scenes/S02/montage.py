"""S02 · Montage V1 : les plans calés sur la voix de Guillaume, et le son.

Image (34 s, coupes franches) :
  P01 on s'assoit 6 s · P02 face à l'écran 9 s · P03 le compteur 7 s · P04 la lampe 4 s · P05 la silhouette 8 s
Voix : prise 1, choisie par Bruno (ElevenLabs, voix Guillaume), découpée phrase par phrase et posée sur les plans ; les silences
sont faits au montage, pas dans la génération.
Son (sources : ../../references/sons.md) : l'air du grand hall et les ronflements de l'ordinateur et de la lampe
(les mêmes qu'en S01, à leur niveau « tout près ») ; la chaise quand on s'assoit ; un tic très doux à chaque
naissance pendant le gros plan du compteur (calé sur le chiffre affiché) ; le clic de la lampe ; dans le plan large,
la pièce s'éloigne (ronflements plus sourds et plus bas). Pas de musique.
Sortie : -16 LUFS intégré (la voix porte la scène), crête vraie -1,5 dBTP ; la sonie finale se règle au mastering.

Usage : python montage.py
"""
import os
import subprocess
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", "..", "shared", "outils", "son"))
from pas import SR, boucle, detecter_pas, ecrire_normalise, lire_audio  # noqa: E402

M = os.path.join(ICI, "..", "..", "medias")
S02 = os.path.join(M, "S02")
SONS = os.path.join(M, "sons", "epidemic")
VOIX = os.path.join(M, "voix", "S02_prise1.mp3")   # prise 1, choisie par Bruno
VOIX_FIN = os.path.join(M, "voix", "S02_aventure_prise1.mp3")   # dernière phrase, générée dans son contexte

PLANS = [("S02_p01_raccord.mp4", 6), ("S02_p02.mp4", 9), ("S02_p03_compteur.mp4", 7), ("S02_p04_recadre.mp4", 4), ("S02_p05.mp4", 8)]
DEBUTS = np.cumsum([0] + [d for _, d in PLANS])[:-1]   # 0, 6, 15, 22, 26
DUREE = sum(d for _, d in PLANS)
# phrases : (début et fin dans la prise, mesurés par détection des silences et vérifiés par transcription), position
PHRASES = [            # (fichier, (début, fin) dans la prise, position dans la scène)
    (VOIX, (0.00, 1.23), 6.3),     # On m'a confié quelqu'un.
    (VOIX, (1.93, 5.66), 8.6),     # Je dois le faire vivre, du premier jour jusqu'au dernier.
    (VOIX, (6.60, 8.18), 13.0),    # Je ne sais pas encore qui ce sera.
    (VOIX, (9.12, 12.47), 15.8),   # Pendant qu'on parle, il en naît à peu près quatre par seconde.
    (VOIX, (13.19, 14.15), 20.0),  # Il sera l'un d'eux.
    (VOIX, (14.93, 15.75), 24.2),  # Vous allez m'aider.
    (VOIX, (16.33, 20.63), 26.6),  # Chaque fois que la vie lui posera une question, je vous la poserai aussi.
    (VOIX_FIN, (4.36, 6.36), 31.6),  # Vous allez m'accompagner dans cette aventure. (souffle final coupé, demande de Bruno)
]
# l'opérateur utilise le logiciel pendant P02 (temps de la scène) : déplacements de la souris et le clic « nouvelle vie »
SOURIS_MOUVEMENTS = [(6.0, 6.7), (8.1, 8.7), (10.0, 10.5), (11.4, 12.2), (12.55, 13.2)]
SOURIS_CLIC = 12.5
VOIX_DB = float(os.environ.get("VOIX_DB", "-3.5"))   # niveau de la voix dans le mixage
N = int(DUREE * SR)
t = np.arange(N) / SR


def db(x):
    return 10 ** (x / 20)


def fondu(n, e=0.0, s=0.0):
    g = np.ones(n); ne, ns = int(e * SR), int(s * SR)
    if ne:
        g[:ne] = np.linspace(0, 1, ne) ** 2
    if ns:
        g[-ns:] = np.linspace(1, 0, ns) ** 2
    return g


def passe_bas(x, fc):
    """Passe-bas du premier ordre, vectorisé par blocs via un filtre IIR appliqué avec lfilter maison (numpy)."""
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); acc = np.zeros(x.shape[1])
    for k in range(len(x)):
        acc = (1 - a) * x[k] + a * acc
        y[k] = acc
    return y


def stereo(chemin, debut, n):
    a = lire_audio(chemin, mono=False).astype(np.float64)
    return boucle(a[int(debut * SR):], n)


def poser(piste, son, t0, gain=1.0):
    j = int(t0 * SR); f = min(len(piste), j + len(son))
    if j < f:
        piste[j:f] += son[:f - j] * gain


mix = np.zeros((N, 2))
loin = np.clip((t - DEBUTS[4]) / 0.6, 0, 1)            # plan large : la pièce s'éloigne

# 1. l'air du grand hall et les ronflements (mêmes points de départ dans les fichiers qu'en S01, suite directe)
amb = stereo(os.path.join(SONS, "ambiance_grand_hall.wav"), 50.0, N) * db(-13)
mix += amb * (1 + 0.6 * loin)[:, None]                  # de loin, l'espace se fait entendre davantage
for fichier, gain, debut in (("bourdonnement_ordinateur.wav", -17, 40.0), ("bourdonnement_lumiere.wav", -23, 15.0)):
    b = stereo(os.path.join(SONS, fichier), debut, N)
    sourd = passe_bas(b, 600.0)
    b = b * (1 - loin)[:, None] + sourd * loin[:, None]
    mix += b * (db(gain) * (1 - 0.75 * loin))[:, None]

# 2. la chaise : on s'assoit (l impact du fichier, à 0,24 s, tombe à 3,3 s : on touche l assise vers l image 80)
chaise = lire_audio(os.path.join(SONS, "chaise_assis.wav"), mono=False).astype(np.float64)
poser(mix, chaise * fondu(len(chaise), 0.01, 0.2)[:, None], 3.3 - 0.24, db(-7))   # on touche l assise vers l image 80

# 3. les tics du compteur : un par naissance affichée, pendant le gros plan (temps de l'interface = 25 + (T - 15))
tic_src = lire_audio(os.path.join(SONS, "tic_doux.wav"), mono=False).astype(np.float64)
ons = detecter_pas(os.path.join(SONS, "tic_doux.wav"), seuil_db=-30, ecart_min=0.12)
L = int(0.09 * SR)
rng = np.random.default_rng(4)
debut_p03, fin_p03 = DEBUTS[2], DEBUTS[2] + 7
for k in range(int((25 + 0) * 4.3) + 1, int((25 + 7) * 4.3) + 1):
    T = debut_p03 + (k / 4.3 - 25)
    if not (debut_p03 + 0.05 < T < fin_p03 - 0.05):
        continue
    o = ons[(k * 7) % len(ons)]
    seg = tic_src[int(o * SR):int(o * SR) + L] * fondu(L, 0.002, 0.05)[:, None]
    env = min(1.0, (T - debut_p03) / 1.0, (fin_p03 - T) / 0.6)
    poser(mix, seg, T, db(-20 + rng.uniform(-1.5, 1.5)) * env)

# 4. le clic de la lampe (le clic du fichier est à 0,17 s ; la lampe s'allume à 1,6 s dans le plan)
lampe = lire_audio(os.path.join(SONS, "interrupteur_lampe.wav"), mono=False).astype(np.float64)
lampe = lampe[int(0.12 * SR):int(0.45 * SR)] * fondu(int(0.33 * SR), 0.003, 0.08)[:, None]
poser(mix, lampe, DEBUTS[3] + 1.6 - 0.05, db(-4))

# 4 bis. la souris : frottements sur le tapis quand le pointeur bouge, un clic sur « nouvelle vie »
tapis = lire_audio(os.path.join(SONS, "souris_tapis.wav"), mono=False).astype(np.float64)
ons_t = detecter_pas(os.path.join(SONS, "souris_tapis.wav"), seuil_db=-30, ecart_min=0.6)
for k, (d0, d1) in enumerate(SOURIS_MOUVEMENTS):
    o = ons_t[(k * 3) % len(ons_t)]
    n_ = int((d1 - d0) * SR)
    seg = tapis[int(o * SR):int(o * SR) + n_]
    seg = np.pad(seg, ((0, n_ - len(seg)), (0, 0))) * fondu(n_, 0.08, 0.15)[:, None]
    poser(mix, seg, d0, db(-14))
clics = lire_audio(os.path.join(SONS, "souris_clics.wav"), mono=False).astype(np.float64)
ons_c = detecter_pas(os.path.join(SONS, "souris_clics.wav"), seuil_db=-25, ecart_min=0.3)
o = ons_c[len(ons_c) // 2]
clic = clics[int((o - 0.005) * SR):int((o + 0.18) * SR)]
poser(mix, clic * fondu(len(clic), 0.002, 0.06)[:, None], SOURIS_CLIC - 0.005, db(-8))

# 5. la voix, phrase par phrase ; l'ambiance s'efface un peu sous la voix
prises = {}
piste_voix = np.zeros(N)
for fichier, (a, b), pos in PHRASES:
    if fichier not in prises:
        prises[fichier] = lire_audio(fichier, mono=True).astype(np.float64)
    seg = prises[fichier][int(a * SR):int(b * SR)]
    seg = seg * fondu(len(seg), 0.01, 0.06)
    poser(piste_voix, seg, pos)
env_voix = np.convolve(np.abs(piste_voix) > 1e-3, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode="same")
mix *= (1 - 0.3 * np.clip(env_voix * 3, 0, 1))[:, None]     # environ -3 dB sous la voix
mix += piste_voix[:, None] * db(VOIX_DB)

# légère entrée et sortie, pour les raccords avec S01 et S03
mix *= fondu(N, 0.05, 0.3)[:, None]
wav = os.path.join(S02, "S02_son_v2.wav")
# même gain général qu'en S01 (le décor sonore garde son niveau à la coupe) ; c'est la voix qui donne la sonie de la scène
GAIN_S01 = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN_S01))

# image : coupes franches, puis le son
liste = os.path.join(S02, "liste_montage.txt")
tmp = []
for nom, d in PLANS:
    sortie = os.path.join(S02, "tmp_" + nom)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(S02, nom), "-t", str(d), "-vf",
                    "fps=24,scale=1920:1080,setsar=1,format=yuv420p", "-an", "-c:v", "libx264", "-crf", "16", sortie], check=True)
    tmp.append(sortie)
open(liste, "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in tmp))
image = os.path.join(S02, "tmp_image.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", image], check=True)
final = os.path.join(S02, "S02_v2.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", image, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", "-movflags", "+faststart", final], check=True)
for p in tmp + [liste, image]:
    os.remove(p)
print("écrit :", final, "(", DUREE, "s )")
