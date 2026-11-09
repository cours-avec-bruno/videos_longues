"""Les plans embellis par Higgsfield (Blender -> restylage -> Kling), et leur raccord avec le montage.

L'IA garde la composition de l'image Blender, mais pas au pixel près. Pour incruster l'écran de la salle exactement,
on apparie l'image Blender et la première image de la vidéo (points ORB + homographie RANSAC) : les coins de l'écran
connus dans Blender sont reportés dans la vidéo. Caméra fixe demandée à Kling : ces coins valent pour tout le plan.
"""
import json
import math
import os
import subprocess

import cv2
import numpy as np

W, H, FPS = 1920, 1080, 24
_cache = {}


def lire(chemin, duree):
    """Toutes les images de la vidéo, recadrées en 1920x1080 et étirées pour durer `duree` secondes à 24 i/s."""
    cle = (chemin, round(duree, 3))
    if cle in _cache:
        return _cache[cle]
    src = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", chemin],
                               capture_output=True, text=True, check=True).stdout)
    n = int(math.ceil(duree * FPS)) + 2
    vf = (f"setpts=PTS*{duree / src:.5f},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H}")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", chemin, "-vf", vf, "-frames:v", str(n), "-f", "rawvideo",
                          "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(im) < n:
        im = np.concatenate([im, np.repeat(im[-1:], n - len(im), 0)])
    _cache[cle] = im
    return im


def image(chemin, duree, t):
    ims = lire(chemin, duree)
    return ims[max(0, min(int(t * FPS), len(ims) - 1))].astype(np.float32)


def report(blender_png, video, points, cache_json):
    """Reporte des points de l'image Blender dans la vidéo IA (homographie apprise sur les deux images)."""
    if os.path.exists(cache_json):
        return np.float32(json.load(open(cache_json)))
    a = cv2.imread(blender_png, cv2.IMREAD_GRAYSCALE)
    a = cv2.resize(a, (W, H))
    b = cv2.cvtColor(lire(video, 1.0)[0], cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(6000)
    ka, da = orb.detectAndCompute(cv2.equalizeHist(a), None)
    kb, db = orb.detectAndCompute(cv2.equalizeHist(b), None)
    m = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(da, db), key=lambda x: x.distance)[:800]
    pa = np.float32([ka[x.queryIdx].pt for x in m])
    pb = np.float32([kb[x.trainIdx].pt for x in m])
    Hm, ok = cv2.findHomography(pa, pb, cv2.RANSAC, 6.0)
    print(f"[hf] {os.path.basename(video)} : {int(ok.sum())} appariements retenus sur {len(m)}")
    out = cv2.perspectiveTransform(np.float32(points).reshape(-1, 1, 2), Hm).reshape(-1, 2)
    json.dump(out.tolist(), open(cache_json, "w"))
    return out


def suivre(video, duree, points0, cache_json):
    """Suit des points de la première image de la vidéo dans toutes les suivantes (caméra qui dérive malgré la consigne) :
    homographie image 0 -> image k sur des points ORB, lissée dans le temps. Renvoie un tableau (n, len(points), 2)."""
    if os.path.exists(cache_json):
        return np.float32(json.load(open(cache_json)))
    ims = lire(video, duree)
    orb = cv2.ORB_create(4000)
    g0 = cv2.equalizeHist(cv2.cvtColor(ims[0], cv2.COLOR_BGR2GRAY))
    k0, d0 = orb.detectAndCompute(g0, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    p0 = np.float32(points0).reshape(-1, 1, 2)
    out = []
    for im in ims:
        g = cv2.equalizeHist(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
        k, d = orb.detectAndCompute(g, None)
        m = sorted(bf.match(d0, d), key=lambda x: x.distance)[:600]
        Hm, _ = cv2.findHomography(np.float32([k0[x.queryIdx].pt for x in m]), np.float32([k[x.trainIdx].pt for x in m]),
                                   cv2.RANSAC, 4.0)
        out.append(cv2.perspectiveTransform(p0, Hm).reshape(-1, 2) if Hm is not None else (out[-1] if out else p0.reshape(-1, 2)))
    out = np.float32(out)
    # lissage temporel (fenêtre de 5 images) : pas de tremblement de l'incrustation
    k_ = np.ones(5) / 5
    lis = np.stack([np.stack([np.convolve(np.pad(out[:, i, j], 2, mode="edge"), k_, "valid") for j in range(2)], -1)
                    for i in range(out.shape[1])], 1)
    json.dump(lis.tolist(), open(cache_json, "w"))
    return np.float32(lis)
