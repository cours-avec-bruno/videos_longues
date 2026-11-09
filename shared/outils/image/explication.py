"""Motion design « d'explication », d'après une référence de Bruno (09/11/2026) : fond sombre en dégradé (bordeaux / bleu
nuit), étiquettes encadrées en lettres pixel, petites valeurs rouges qui flottent, sous-titres pixel au centre,
vignettes d'illustration qui surgissent. Réutilisable dans toutes les vidéos.

Toutes les fonctions travaillent en BGR float32 (comme les montages Python du studio).
"""
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
POLICE = "C:/Windows/Fonts/georgiab.ttf"
CREME = (238, 230, 216)      # RVB
ROUGE = (226, 64, 52)
_cache = {}


def _lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def _expo_out(p):
    p = min(1.0, max(0.0, p))
    return 1 - 2 ** (-10 * p) if p < 1 else 1.0


def fond(t, chaud=0.5, rng_k=0):
    """Le fond : un dégradé radial sombre, rouge sombre en haut à gauche, bleu nuit en bas à droite, qui respire."""
    cle = ("fond", round(chaud, 2))
    if cle not in _cache:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        a = np.exp(-(((xx - W * 0.3) / (W * 0.55)) ** 2 + ((yy - H * 0.25) / (H * 0.7)) ** 2))
        b = np.exp(-(((xx - W * 0.8) / (W * 0.5)) ** 2 + ((yy - H * 0.9) / (H * 0.6)) ** 2))
        f = np.zeros((H, W, 3), np.float32) + np.float32([10, 6, 8])
        f += a[..., None] * np.float32([14, 10, 44]) * chaud * 2
        f += b[..., None] * np.float32([46, 18, 12])
        _cache[cle] = f
    f = _cache[cle] * (1 + 0.06 * math.sin(t * 0.9))
    return f + np.random.default_rng(rng_k).normal(0, 2.0, (H, W, 3)).astype(np.float32)


def pixel(texte, taille=13, echelle=4, couleur=CREME):
    """Un texte en lettres pixel (dessiné petit sans lissage, agrandi), avec sa lueur. Renvoie (RVB-BGR, alpha)."""
    cle = ("px", texte, taille, echelle, couleur)
    if cle not in _cache:
        f = ImageFont.truetype(POLICE, taille)
        # sans lissage, les lettres prennent plus de place que la mesure : on dessine large, puis on recadre sur l'encre
        petit = Image.new("L", (len(texte) * taille * 2 + 20, taille * 3), 0)
        d = ImageDraw.Draw(petit)
        d.fontmode = "1"
        d.text((4, taille // 2), texte, font=f, fill=255)
        bx = petit.getbbox() or (0, 0, 1, 1)
        petit = petit.crop((max(0, bx[0] - 2), taille // 2 - 2, bx[2] + 3, taille // 2 + int(taille * 1.3) + 2))
        a = np.kron(np.asarray(petit, np.float32) / 255, np.ones((echelle, echelle), np.float32))
        a = np.pad(a, 24)
        halo = cv2.GaussianBlur(a, (0, 0), 9) * 0.55
        al = np.clip(a + halo, 0, 1)
        rgb = np.zeros(a.shape + (3,), np.float32) + np.float32(couleur[::-1])
        _cache[cle] = (rgb, al)
    return _cache[cle]


def poser(f, calque, cx, cy, opac=1.0, ech=1.0, flou=0.0):
    rgb, al = calque
    if ech != 1.0:
        rgb = cv2.resize(rgb, None, fx=ech, fy=ech, interpolation=cv2.INTER_NEAREST)
        al = cv2.resize(al, None, fx=ech, fy=ech, interpolation=cv2.INTER_NEAREST)
    if flou > 0.5:
        al = cv2.GaussianBlur(al, (0, 0), flou)
    h, w = al.shape
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return f
    sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0))
    a = al[sl][..., None] * opac
    f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - a) + rgb[sl] * a
    return f


def etiquette(f, texte, cx, cy, q, signe="", taille=11, echelle=4):
    """Une étiquette encadrée (comme « Comptabilité mentale » dans la référence). signe : '+', '-' ou ''.
    q : 0 -> 1, l'apparition (elle glisse un peu et se pose)."""
    if q <= 0:
        return f
    coul = ROUGE if signe == "-" else CREME
    t_ = (("– " if signe == "-" else "+ " if signe == "+" else "") + texte)
    cal = pixel(t_, taille, echelle, coul)
    rgb, al = cal
    h, w = al.shape
    e = _expo_out(q)
    cy = cy + 18 * (1 - e)
    # la boîte : fond sombre translucide, bord fin
    bw, bh = w - 26, h - 34
    x0, y0 = int(cx - bw / 2), int(cy - bh / 2)
    x1, y1 = x0 + bw, y0 + bh
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if xa < xb and ya < yb:
        f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - 0.6 * e) + np.float32([30, 22, 24]) * 0.6 * e
        bord = np.float32(coul[::-1]) * (0.55 if signe != "-" else 0.8)
        for (sa, sb) in ((slice(ya, ya + 3), slice(xa, xb)), (slice(yb - 3, yb), slice(xa, xb)),
                         (slice(ya, yb), slice(xa, xa + 3)), (slice(ya, yb), slice(xb - 3, xb))):
            f[sa, sb] = f[sa, sb] * (1 - e) + bord * e
    return poser(f, cal, cx, cy, e)


def valeur(f, texte, cx, cy, t_loc, duree=1.4):
    """Une petite valeur rouge qui monte et s'efface (le « -100$ » de la référence)."""
    if not (0 <= t_loc < duree):
        return f
    q = t_loc / duree
    a = _lisse(q / 0.15) * (1 - _lisse((q - 0.6) / 0.4))
    return poser(f, pixel(texte, 10, 4, ROUGE), cx, cy - 40 * q, a)


def sous_titre(f, texte, t_loc, duree, cy=H / 2, taille=14, echelle=5):
    """Le sous-titre pixel au centre : il apparaît d'un coup (petit rebond), tient, et s'efface vite."""
    if not (0 <= t_loc < duree):
        return f
    a = _lisse(t_loc / 0.08) * (1 - _lisse((t_loc - (duree - 0.12)) / 0.12))
    ech = 1 + 0.06 * (1 - _expo_out(t_loc / 0.25))
    return poser(f, pixel(texte, taille, echelle), W / 2, cy, a, ech)


def vignette(f, img, cx, cy, largeur, q, angle=-2.0):
    """Une image d'illustration qui surgit (cadre clair, ombre), légèrement inclinée."""
    if q <= 0:
        return f
    e = _expo_out(q)
    hs, ws = img.shape[:2]
    lw = int(largeur * (0.85 + 0.15 * e))
    lh = int(lw * hs / ws)
    v = cv2.resize(img, (lw, lh), interpolation=cv2.INTER_AREA).astype(np.float32)
    v = cv2.copyMakeBorder(v, 8, 8, 8, 8, cv2.BORDER_CONSTANT, value=(214, 222, 228))
    m = np.ones(v.shape[:2], np.float32)
    rot = cv2.getRotationMatrix2D((v.shape[1] / 2, v.shape[0] / 2), angle * e, 1.0)
    big = (int(v.shape[1] * 1.1), int(v.shape[0] * 1.15))
    rot[0, 2] += (big[0] - v.shape[1]) / 2
    rot[1, 2] += (big[1] - v.shape[0]) / 2
    v = cv2.warpAffine(v, rot, big)
    m = cv2.warpAffine(m, rot, big)
    om = cv2.GaussianBlur(m, (0, 0), 16)
    h, w = m.shape
    x0, y0 = int(cx - w / 2), int(cy - h / 2 + 30 * (1 - e))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return f
    sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0))
    z = f[ya:yb, xa:xb] * (1 - 0.6 * om[sl][..., None] * e)
    a = m[sl][..., None] * e
    f[ya:yb, xa:xb] = z * (1 - a) + v[sl] * a
    return f


def carte(f, texte, rect, choisie=False, actif=1.0, opac=1.0):
    """Une carte de choix (fond sombre, ou rouge si choisie), texte en lettres pixel."""
    x0, y0, x1, y1 = [int(v) for v in rect]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    a = int(255 * opac)
    fondc = (ROUGE[0], ROUGE[1], ROUGE[2], a) if choisie else (20, 20, 26, int(a * 0.9))
    bordc = (*[int(c * (0.35 + 0.65 * actif)) for c in CREME], a)
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=fondc, outline=bordc, width=3)
    arr = np.asarray(im).astype(np.float32)
    al = arr[..., 3:4] / 255
    f = f * (1 - al) + arr[..., :3][..., ::-1] * al
    lignes = texte.split("\n")
    for j, l_ in enumerate(lignes):
        cal = pixel(l_, 13, 4, CREME)
        f = poser(f, cal, (x0 + x1) / 2, (y0 + y1) / 2 + (j - (len(lignes) - 1) / 2) * 62, opac * (0.45 + 0.55 * actif))
    return f
