"""Les données du motion design du dialogue (S07) : qui parle, où sont les têtes, la voix image par image.

Bruno (09/11/2026) : « pendant le dialogue, un motion design qui illustre le fait que les gens parlent ».
Ce script lit le déroulé de montage.py (les plans de la salle, les répliques), les positions des têtes exportées
par salle.py (--tetes) et l'enveloppe des voix ; il écrit public/dialogue/s07.json, que lit la composition
Remotion « Dialogue » (videos/<slug>/remotion/Dialogue.tsx), rendue en PNG transparents puis posée au montage.

Usage : python dialogue.py
"""
import json
import os
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ICI, "montage.py"), encoding="utf-8").read()
src = src[:src.index("SON_SEUL = ")]
__file__ = os.path.join(ICI, "montage.py")
exec(src)                                    # PLANS, FPS, SALLE, M, les répliques, lire_audio, SR…

RACINE_PROJET = os.path.abspath(os.path.join(ICI, "..", "..", "..", ".."))
SORTIE = os.path.join(RACINE_PROJET, "public", "dialogue")
os.makedirs(SORTIE, exist_ok=True)

# les répliques des deux simulateurs : (qui, fichier, [((a, b), position)])
REPLIQUES = [("lui", VOIX_LUI, PHRASES_LUI), ("lui", VOIX_LUI2, PHRASES_LUI2), ("elle", VOIX_ELLE, PHRASES_ELLE)]
debut = min(p[0] for p in PLANS if p[2] == "salle")
fin = DUREE
n0, n1 = int(round(debut * FPS)), int(round(fin * FPS))

# l'enveloppe de chaque voix, image par image (RMS sur 1/24 s), normalisée par voix
niveau = {"lui": np.zeros(n1 + 1), "elle": np.zeros(n1 + 1)}
parle = [None] * (n1 + 1)
for qui, fichier, phrases in REPLIQUES:
    a_ = lire_audio(fichier, mono=True).astype(np.float64)
    ref = np.percentile(np.abs(a_[np.abs(a_) > 0.01]), 95) or 1.0
    for (a, b), pos in phrases:
        seg = a_[int(a * SR):int(b * SR)]
        h = SR // FPS
        for i in range(len(seg) // h):
            n = int(round(pos * FPS)) + i
            if n <= n1:
                rms = np.sqrt((seg[i * h:(i + 1) * h] ** 2).mean())
                niveau[qui][n] = min(1.0, rms / (0.45 * ref))
                parle[n] = qui

_tetes = {}


def tetes(plan, k):
    if plan not in _tetes:
        _tetes[plan] = json.load(open(os.path.join(SALLE, plan, "tetes.json")))
    d = _tetes[plan]
    return d.get(str(max(1, min(int(k) + 1, len(d)))), {})


images = []
for n in range(n0, n1):
    t = n / FPS
    i = max(j for j, p in enumerate(PLANS) if p[0] <= t + 1e-6)
    t0, t1, genre, src_, plein, entree = PLANS[i]
    tt = tetes(src_[0], (t - t0) * FPS + src_[1] * FPS) if genre == "salle" else {}
    # la parole tient quelques images après la fin du son (on ne coupe pas le repère au milieu d'un souffle)
    qui = next((parle[m] for m in range(n, max(n0, n - 6), -1) if parle[m]), None)
    images.append({
        "lui": tt.get("lui"), "elle": tt.get("elle"), "parle": qui,
        "niveau": round(float(niveau[qui][n]) if qui else 0.0, 3),
        "plan": src_[0] if genre == "salle" else None,
    })
json.dump({"fps": FPS, "debut": n0, "images": images}, open(os.path.join(SORTIE, "s07.json"), "w"))
print("écrit :", os.path.join(SORTIE, "s07.json"), len(images), "images, à partir de l'image", n0)
