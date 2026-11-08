"""La fenêtre d'interface (validée par Bruno en S06, d'après sa capture) : petits bords ronds, marge sombre autour,
léger quadrillage de pixels. Et le passage fluide entre la fenêtre et le plein écran.

    from fenetre import fenetre
    img = fenetre(contenu_bgr, ouverture=1.0, plein=0.0)
      ouverture : 0 -> 1, la fenêtre apparaît (en grandissant un peu) ou disparaît
      plein     : 0 = dans la fenêtre ; 1 = plein écran (coins droits, plus de quadrillage, plus de marge)
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw

W, H = 1920, 1080
FW, FH = 1680, 945
RAYON = 16
FOND = np.float32([13, 12, 12])


def _masque(w, h, r, k=3):
    if r <= 0.5:
        return np.ones((h, w), np.float32)
    m = Image.new("L", (w * k, h * k), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * k - 1, h * k - 1], radius=int(r * k), fill=255)
    return np.asarray(m.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255


_gy, _gx = np.mgrid[0:H, 0:W]
_GRILLE = (1 - 0.13 * ((_gx % 4) == 0) - 0.13 * ((_gy % 4) == 0)).astype(np.float32)[..., None]
_cache = {}


def fenetre(c, ouverture=1.0, plein=0.0, rng=None):
    """c : image BGR float (1920 x 1080) à afficher. Renvoie l'image finale (BGR float)."""
    out = np.empty((H, W, 3), np.float32)
    out[:] = FOND
    if ouverture <= 0.001:
        return out
    p = float(np.clip(plein, 0, 1))
    w_ = int(round(FW + (W - FW) * p))
    h_ = int(round(FH + (H - FH) * p))
    s_ = 0.95 + 0.05 * ouverture
    w_, h_ = int(round(w_ * s_)), int(round(h_ * s_))
    r_ = RAYON * (1 - p)
    cle = (w_, h_, round(r_, 1))
    if cle not in _cache:
        if len(_cache) > 64:
            _cache.clear()
        m = _masque(w_, h_, r_)
        li = np.clip(m - cv2.erode(m, np.ones((5, 5), np.uint8)), 0, 1) * 0.6 * (1 - p)
        _cache[cle] = (m, li)
    m, li = _cache[cle]
    im = cv2.resize(c, (w_, h_), interpolation=cv2.INTER_AREA if w_ < W else cv2.INTER_LINEAR)
    grille = 1 - (1 - _GRILLE[:h_, :w_]) * (1 - p)
    im = im * grille
    im = im * (1 - li[..., None]) + np.float32([58, 56, 56]) * li[..., None]
    x0, y0 = (W - w_) // 2, (H - h_) // 2
    mm = (m * ouverture)[..., None]
    z = out[y0:y0 + h_, x0:x0 + w_]
    out[y0:y0 + h_, x0:x0 + w_] = z * (1 - mm) + im * mm
    return out
