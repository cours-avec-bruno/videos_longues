"""S01 · Le son de la marche dans le noir.

Couches (sons Epidemic Sound, registre dans ../../references/sons.md) :
  1. ambiance d'un grand hall vide, très basse, en fondu ;
  2. bourdonnements de l'ordinateur et de la lumière, qui montent et s'éclaircissent à mesure qu'on approche ;
  3. nos pas : chaque pas est découpé dans l'enregistrement et posé sur un creux du balancement de la caméra,
     avec une réverbération de grand espace vide ; le dernier pas est plus doux (on s'arrête).
Pas de musique, pas de voix.

Usage :
  python son.py --video ../../medias/S01/S01_marche_v2.mp4 --sortie ../../medias/S01/S01_son_v2.wav
"""
import argparse
import os
import subprocess
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", "..", "shared", "outils", "son"))
from pas import SR, detecter_pas, lire_audio, temps_des_pas  # noqa: E402

SONS = os.path.join(ICI, "..", "..", "medias", "sons", "epidemic")

ap = argparse.ArgumentParser()
ap.add_argument("--video", required=True)
ap.add_argument("--sortie", required=True)
ap.add_argument("--pas", default="", help="instants des pas imposés (ex. 0.6,1.6,2.6) ; sinon détectés sur la vidéo")
A = ap.parse_args()

duree = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", A.video],
                             capture_output=True, text=True, check=True).stdout.strip())
N = int(duree * SR)
t = np.arange(N) / SR
mix = np.zeros((N, 2), dtype=np.float64)


def db(x):
    return 10 ** (x / 20)


def stereo(path, debut, longueur):
    a = lire_audio(path, mono=False)
    i = int(debut * SR)
    seg = a[i:i + longueur]
    if len(seg) < longueur:
        seg = np.pad(seg, ((0, longueur - len(seg)), (0, 0)))
    return seg.astype(np.float64)


def passe_bas(x, fc):
    """Passe-bas simple du premier ordre (filtre récursif), appliqué colonne par colonne."""
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros_like(x)
    acc = np.zeros(x.shape[1])
    for k in range(len(x)):
        acc = (1 - a) * x[k] + a * acc
        y[k] = acc
    return y


def fondu(n, entree=0.0, sortie=0.0):
    g = np.ones(n)
    ne, ns = int(entree * SR), int(sortie * SR)
    if ne:
        g[:ne] = np.linspace(0, 1, ne) ** 2
    if ns:
        g[-ns:] = np.linspace(1, 0, ns) ** 2
    return g


# 1. ambiance du grand hall
amb = stereo(os.path.join(SONS, "ambiance_grand_hall.wav"), 40.0, N)
amb *= db(-13) * fondu(N, 1.5, 0.4)[:, None]
mix += amb

# 2. bourdonnements : ils montent et s'éclaircissent à l'approche (lointain = sourd, proche = net)
proche = np.clip(t / duree, 0, 1) ** 1.6
for fichier, gain, debut in (("bourdonnement_ordinateur.wav", -17, 30.0), ("bourdonnement_lumiere.wav", -23, 5.0)):
    b = stereo(os.path.join(SONS, fichier), debut, N)
    sourd = passe_bas(b, 500.0)
    b = sourd * (1 - proche)[:, None] + b * proche[:, None]
    b *= (db(gain) * (0.12 + 0.88 * proche) * fondu(N, 0.8, 0.3))[:, None]
    mix += b

# 3. les pas
source_pas = os.path.join(SONS, "pas_beton_lent.wav")
pas_src = lire_audio(source_pas, mono=False).astype(np.float64)
onsets = detecter_pas(source_pas)
if A.pas:
    instants = [float(x) for x in A.pas.split(",")]
else:
    instants, fps, _ = temps_des_pas(A.video)
print("pas posés à :", [round(x, 2) for x in instants])

LONG = int(0.55 * SR)
ATTAQUE = int(0.06 * SR)
pas_sec = np.zeros((N, 2))
rng = np.random.default_rng(7)


def force(o):
    i = int(o * SR)
    return float(np.sqrt((pas_src[i:i + ATTAQUE] ** 2).mean()))


# on ne garde que les impacts nets (les plus forts), et on égalise leur niveau : chaque pas doit se lire
nets = sorted(onsets, key=force, reverse=True)[:max(6, len(onsets) // 2)]
nets.sort()
ref = np.median([force(o) for o in nets])
for k, ti in enumerate(instants):
    o = nets[(k * 3 + 1) % len(nets)]              # pas différents de l'enregistrement, pas toujours le même
    i = max(0, int((o - 0.015) * SR))
    seg = pas_src[i:i + LONG].copy()
    seg *= fondu(len(seg), 0.003, 0.2)[:, None]
    seg *= ref / (force(o) + 1e-9)
    g = db(-3 + rng.uniform(-1.2, 0.8))
    if k == len(instants) - 1:
        g *= db(-5)                                  # dernier pas : on s'arrête, plus doux
    j = int(ti * SR)
    fin = min(N, j + len(seg))
    pas_sec[j:fin] += seg[:fin - j] * g
mix += pas_sec

# réverbération d'un grand espace vide (réponse impulsionnelle synthétique : bruit à décroissance exponentielle)
RT = 2.4
L = int(RT * SR)
env = np.exp(-6.9 * np.arange(L) / L)
ir = np.stack([rng.standard_normal(L) * env, rng.standard_normal(L) * env], axis=1)
ir[: int(0.02 * SR)] = 0                              # pré-délai
ir = passe_bas(ir, 4500.0)
ir /= np.sqrt((ir ** 2).sum(axis=0, keepdims=True))
mouillé = np.zeros_like(pas_sec)
nfft = 1 << int(np.ceil(np.log2(N + L)))
for c in range(2):
    mouillé[:, c] = np.fft.irfft(np.fft.rfft(pas_sec[:, c], nfft) * np.fft.rfft(ir[:, c], nfft), nfft)[:N]
mix += mouillé * db(-14)

# sortie : on vise un début de vidéo calme (≈ -26 LUFS), crête vraie sous -1 dBTP ; mesure ensuite avec ffmpeg
crete = np.abs(mix).max()
mix *= db(-3) / crete if crete > db(-3) else 1.0
os.makedirs(os.path.dirname(os.path.abspath(A.sortie)), exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                "-af", "loudnorm=I=-26:TP=-1.5:LRA=11", "-ar", str(SR), "-c:a", "pcm_s24le", A.sortie],
               input=mix.astype(np.float32).tobytes(), check=True)
print("écrit :", A.sortie)
