"""Les données de l'onde du dialogue de S08 (même composition Remotion que S07 : remotion/Dialogue.tsx).

Têtes : position dans l'image Blender de départ (salle.py --tetes), reportée dans la vidéo Higgsfield par la même
homographie que l'écran, et suivie par la poussée du plan. Après la plongée dans les données, l'onde de la
simulatrice reste au bord droit du cadre (hors champ).

Usage : python dialogue.py   (après les vidéos Higgsfield ; écrit public/dialogue/s08.json)
"""
import json
import os

import cv2
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ICI, "montage.py"), encoding="utf-8").read()
src = src[:src.index("SON_SEUL = ")]
__file__ = os.path.join(ICI, "montage.py")
exec(src)

RACINE_PROJET = os.path.abspath(os.path.join(ICI, "..", "..", "..", ".."))
SORTIE = os.path.join(RACINE_PROJET, "public", "dialogue")
os.makedirs(SORTIE, exist_ok=True)
n1 = int(round(DUREE * FPS))

niveau = {"lui": np.zeros(n1 + 1), "elle": np.zeros(n1 + 1)}
parle = [None] * (n1 + 1)
for fichier, phrases, salle_ in VOIX:
    qui = "elle" if "elle" in os.path.basename(fichier) else "lui" if "lui" in os.path.basename(fichier) else None
    if not qui:
        continue
    a_ = lire_audio(fichier, mono=True).astype(np.float64)
    ref = np.percentile(np.abs(a_[np.abs(a_) > 0.01]), 95) or 1.0
    for (a, b), pos in phrases:
        seg = a_[int(a * SR):int(b * SR)]
        h = SR // FPS
        for i in range(len(seg) // h):
            n = int(round(pos * FPS)) + i
            if n <= n1:
                niveau[qui][n] = min(1.0, np.sqrt((seg[i * h:(i + 1) * h] ** 2).mean()) / (0.45 * ref))
                parle[n] = qui


def tete(plan, qui, t_local):
    tt = json.load(open(os.path.join(SALLE, plan, "tetes.json"))).get("1", {}).get(qui)
    if not tt:
        return None
    x, y, r = tt
    vid, dur, ref, zf = HF_SALLE[plan]
    if ref and os.path.exists(os.path.join(HF, vid)):
        x, y = hf.report(os.path.join(HF, ref), os.path.join(HF, vid), [[x, y]], os.path.join(HF, vid + f".{qui}.json"))[0]
        if zf != 1:
            co = salle2(plan, 0)[2]
            z = 1 + (zf - 1) * doux(t_local / dur)
            Ma = cv2.getRotationMatrix2D((float(co[:, 0].mean()), float(co[:, 1].mean())), 0, z)
            x, y = Ma @ np.float32([x, y, 1])
            r *= z
    return [round(float(x), 1), round(float(y), 1), round(float(r), 1)]


images = []
for n in range(n1):
    t = n / FPS
    qui = next((parle[m] for m in range(n, max(0, n - 6), -1) if parle[m]), None)
    im = {"lui": None, "elle": None, "parle": qui, "niveau": round(float(niveau[qui][n]) if qui else 0.0, 3)}
    if qui:
        if t < T_RECUL:
            im[qui] = tete("s08_ecran", qui, t)
        elif t < T_ENTRE:
            im[qui] = tete("s08_recul", qui, t - T_RECUL)
        elif T_SORT <= t < T_PLONGE:
            im[qui] = tete("s08_sara", qui, t - T_SORT)
    images.append(im)
json.dump({"fps": FPS, "debut": 0, "images": images}, open(os.path.join(SORTIE, "s08.json"), "w"))
print("écrit :", len(images), "images")
