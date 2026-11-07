"""Effets d'image réutilisables (numpy + OpenCV), image par image, en BGR float 0-255.

scan_cyan(img, k)      : bichromie bleu cyan (ombres bleu nuit, hautes lumières cyan blanc), trame de points (demi-teinte),
                         lignes de balayage, halo des hautes lumières, vignette, grain. Look « écran de surveillance »,
                         d'après une référence donnée par Bruno (07/11/2026).
glitch(img, k, force)  : coupe numérique : tranches horizontales décalées, canaux de couleur séparés.
negatif(img)           : image inversée (éclair sur une coupe).
"""
import cv2
import numpy as np

_cache = {}


def _lut_cyan():
    if "lut" not in _cache:
        x = np.arange(256, dtype=np.float32)
        # repères en BGR : noir bleuté -> bleu nuit -> cyan -> blanc cyan
        reperes = [(0, (14, 8, 4)), (60, (60, 38, 12)), (130, (175, 145, 35)), (190, (225, 215, 120)), (255, (255, 255, 235))]
        lut = np.zeros((256, 3), np.float32)
        for c in range(3):
            lut[:, c] = np.interp(x, [r[0] for r in reperes], [r[1][c] for r in reperes])
        _cache["lut"] = lut
    return _cache["lut"]


def _trame(h, w, pas=7):
    cle = ("trame", h, w, pas)
    if cle not in _cache:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        a = np.deg2rad(45)
        u = (xx * np.cos(a) + yy * np.sin(a)) / pas
        v = (-xx * np.sin(a) + yy * np.cos(a)) / pas
        d = np.sqrt((u - np.round(u)) ** 2 + (v - np.round(v)) ** 2)    # distance au centre du point (0 à 0,7)
        _cache[cle] = d
    return _cache[cle]


def _vignette(h, w):
    cle = ("vig", h, w)
    if cle not in _cache:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
        _cache[cle] = np.clip(1.15 - 0.45 * r ** 2, 0.45, 1)[..., None]
    return _cache[cle]


def scan_cyan(img, k=0, force=1.0, rng=None):
    rng = rng or np.random.default_rng(k)
    h, w = img.shape[:2]
    g = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    # contraste fort, hautes lumières qui brûlent
    g = cv2.GaussianBlur(g, (0, 0), 0.7)
    lo, hi = np.percentile(g, 3), np.percentile(g, 97)
    g = np.clip((g - lo) / max(1, hi - lo), 0, 1)
    g = g ** 0.85
    g = g * g * (3 - 2 * g)
    # demi-teinte : un point d'autant plus gros que la zone est sombre, mélangé aux tons moyens
    d = _trame(h, w)
    rayon = 0.62 * np.sqrt(np.clip(1 - g, 0, 1))
    points = (d < rayon).astype(np.float32)
    milieu = np.clip(1 - np.abs(g - 0.5) * 2.2, 0, 1)
    g = g * (1 - 0.55 * milieu * points)
    # lignes de balayage
    lignes = np.ones((h, 1), np.float32)
    lignes[::3] = 0.82
    g = g * lignes
    out = _lut_cyan()[np.clip(g * 255, 0, 255).astype(np.uint8)]
    # halo des hautes lumières
    hl = np.clip((g - 0.7) / 0.3, 0, 1)[..., None] * out
    out = out + 0.6 * cv2.GaussianBlur(hl, (0, 0), 14)
    # léger décalage des canaux sur les bords (aberration)
    out[..., 0] = np.roll(out[..., 0], 2, axis=1)
    out[..., 2] = np.roll(out[..., 2], -2, axis=1)
    out = out * _vignette(h, w)
    out += rng.normal(0, 4, out.shape)
    if force < 1:
        out = img * (1 - force) + out * force
    return out


def glitch(img, k=0, force=1.0):
    rng = np.random.default_rng(1000 + k)
    h, w = img.shape[:2]
    out = img.copy()
    y = 0
    while y < h:
        hh = int(rng.integers(6, 70))
        if rng.random() < 0.45 * force:
            dx = int(rng.normal(0, 60 * force))
            out[y:y + hh] = np.roll(img[y:y + hh], dx, axis=1)
        y += hh
    sep = int(10 * force)
    out[..., 2] = np.roll(out[..., 2], sep, axis=1)
    out[..., 0] = np.roll(out[..., 0], -sep, axis=1)
    return out


def negatif(img):
    return 255 - np.clip(img, 0, 255)
