"""Assemble les scènes déjà montées en un seul aperçu, avec les raccords entre scènes.

  S01 -> S02 : fondu d'un quart de seconde (image et son) ; le cadrage de départ de S02 est déjà raccordé.
  S02 -> S03 : un mini-flash blanc (deux images qui montent, puis il s'éteint sur le carton « commençons »),
               avec un souffle d'air qui monte jusqu'à la coupe et un léger impact au moment du flash.
  S04 -> S05 : coupe nette de la carte au carton « manoj », marquée par un bref éclat de glitch.
  S05 -> S06a -> S07 : coupes nettes (S06 s'ouvre et se ferme dans sa fenêtre ; S07 sort du noir sur une cloche).
  S07 -> S08 : coupe nette ; S07 finit au noir sur « Reste à savoir s'ils pourront payer », S08 rouvre sur l'écran de la salle.
Les raccords vivent ici, pas dans les scènes : chaque scène reste montable seule.

Usage : python assemblage.py   ->  medias/S01_a_S08_apercu.mp4
"""
import os
import subprocess
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "shared", "outils", "son"))
from pas import SR, lire_audio  # noqa: E402

M = os.path.join(ICI, "medias")
SCENES = [  # (vidéo, son)
    (os.path.join(M, "S01", "S01_v7.mp4"), os.path.join(M, "S01", "S01_son_v4.wav")),
    (os.path.join(M, "S02", "S02_v2.mp4"), os.path.join(M, "S02", "S02_son_v2.wav")),
    (os.path.join(M, "S04", "S03_S04_v2.mp4"), os.path.join(M, "S04", "S03_S04_son.wav")),
    (os.path.join(M, "S05", "S05_v1.mp4"), os.path.join(M, "S05", "S05_son.wav")),
    (os.path.join(M, "S06", "S06a_v1.mp4"), os.path.join(M, "S06", "S06a_son.wav")),
    (os.path.join(M, "S07", "S07_v2.mp4"), os.path.join(M, "S07", "S07_son.wav")),
    (os.path.join(M, "S08", "S08_v1.mp4"), os.path.join(M, "S08", "S08_son.wav")),
]
FONDU_12 = 0.25           # S01 -> S02
FLASH_AV, FLASH_AP = 0.08, 0.16   # S02 -> S03 : montée du flash avant la coupe, extinction après
SORTIE = os.path.join(M, "S01_a_S08_apercu.mp4")


def duree(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True, check=True).stdout)


d1, d2, d3, d4, d5, d6, d7 = (duree(v) for v, _ in SCENES)
coupe_23 = d1 - FONDU_12 + d2
coupe_45 = coupe_23 + d3

# ---------------------------------------------------------------- image
filtre = (
    f"[0:v]setpts=PTS-STARTPTS[a];"
    f"[1:v]fade=t=out:st={d2 - FLASH_AV:.3f}:d={FLASH_AV}:color=white[b];"
    f"[2:v]fade=t=in:st=0:d={FLASH_AP}:color=white[c];"
    f"[a][b]xfade=transition=fade:duration={FONDU_12}:offset={d1 - FONDU_12:.3f}[ab];"
    f"[3:v]setpts=PTS-STARTPTS[d];"
    f"[4:v]setpts=PTS-STARTPTS[e];"
    f"[5:v]setpts=PTS-STARTPTS[g];"
    f"[6:v]setpts=PTS-STARTPTS[h];"
    f"[ab][c][d][e][g][h]concat=n=6:v=1:a=0[v]"
)
image = os.path.join(M, "tmp_assemblage_image.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y"] + sum([["-i", v] for v, _ in SCENES], []) +
               ["-filter_complex", filtre, "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", image], check=True)

# ---------------------------------------------------------------- son
a1, a2, a3, a4, a5, a6, a7 = (lire_audio(s, mono=False).astype(np.float64) for _, s in SCENES)
n3 = int(round(d3 * SR))         # le son de S03-S04 calé exactement sur la durée de son image
a3 = np.pad(a3, ((0, max(0, n3 - len(a3))), (0, 0)))[:n3]
n4 = int(round(d4 * SR))         # idem pour S05
a4 = np.pad(a4, ((0, max(0, n4 - len(a4))), (0, 0)))[:n4]
n5 = int(round(d5 * SR))         # idem pour S06
a5 = np.pad(a5, ((0, max(0, n5 - len(a5))), (0, 0)))[:n5]
n_f = int(FONDU_12 * SR)
g = np.linspace(0, 1, n_f)[:, None]
n6 = int(round(d6 * SR))         # idem pour S07
a6 = np.pad(a6, ((0, max(0, n6 - len(a6))), (0, 0)))[:n6]
son = np.concatenate([a1[:-n_f], a1[-n_f:] * (1 - g) + a2[:n_f] * g, a2[n_f:], a3, a4, a5, a6, a7])


def db(x):
    return 10 ** (x / 20)


# le souffle qui monte jusqu'au flash, puis s'efface vite
w = lire_audio(os.path.join(M, "sons", "epidemic", "whoosh_air.wav"), mono=False).astype(np.float64)
pic = int(np.argmax(np.abs(w).mean(1)))
seg = w[max(0, pic - int(0.55 * SR)):pic + int(0.25 * SR)].copy()
n = len(seg); avant = min(pic, int(0.55 * SR))
env = np.ones(n)
env[:avant] = np.linspace(0, 1, avant) ** 2
env[avant:] = np.linspace(1, 0, n - avant) ** 1.5
seg *= env[:, None]
j = int(coupe_23 * SR) - avant
son[j:j + n] += seg * db(-11)
# un léger impact au moment du flash (le début du « teleport », bref et sourd)
t_ = lire_audio(os.path.join(M, "sons", "epidemic", "glitch_teleport.wav"), mono=False).astype(np.float64)
p2 = int(np.argmax(np.abs(t_).mean(1)))
imp = t_[max(0, p2 - int(0.01 * SR)):p2 + int(0.18 * SR)].copy()
imp *= np.linspace(1, 0, len(imp))[:, None] ** 2
j = int(coupe_23 * SR) - int(0.01 * SR)
son[j:j + len(imp)] += imp * db(-16)

# S04 -> S05 : un bref éclat de glitch sur la coupe nette vers « manoj »
gr = lire_audio(os.path.join(M, "sons", "epidemic", "glitch_radio.wav"), mono=False).astype(np.float64)
p3 = int(np.argmax(np.abs(gr).mean(1)))
ec = gr[max(0, p3 - int(0.02 * SR)):p3 + int(0.25 * SR)].copy()
ec *= np.linspace(1, 0, len(ec))[:, None] ** 2
j = int(coupe_45 * SR) - int(0.02 * SR)
son[j:j + len(ec)] += ec * db(-14)

wav = os.path.join(M, "tmp_assemblage_son.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                "-af", "alimiter=limit=0.84:attack=2:release=60:level=disabled", "-c:a", "pcm_s24le", wav],
               input=son.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", image, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", SORTIE], check=True)
os.remove(image); os.remove(wav)
print("écrit :", SORTIE, round(d1 + d2 + d3 + d4 + d5 + d6 + d7 - FONDU_12, 2), "s ; flash à", round(coupe_23, 2), "s ; S05 à", round(coupe_45, 2), "s")
