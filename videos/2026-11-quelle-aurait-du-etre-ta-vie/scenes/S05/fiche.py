"""S05 · la fiche de naissance de Manoj, écran du simulateur (refaite le 08/11/2026 à la demande de Bruno).

Inspirations (docs/direction-artistique) :
  - réf. 01 : fiches « profil » en HUD (étiquettes en capitales, données en monospace, cartouches, coins de viseur) ;
  - réf. 03 : mosaïque d'anonymat (I13), pictos en pixel art et une seule couleur d'accent (I02) ;
  - notre S04 : le simulateur est cyan, l'humain est ambre (la seule chaleur de l'écran).

fiche(tl, portrait=0, zoom=0) -> image BGR float32, 1920 x 1080.
  tl       : temps depuis l'entrée de la fiche (les lignes s'écrivent)
  portrait : 0 -> 1, le visage pixelisé remplit le cadre (ligne de balayage de haut en bas)
  zoom     : 0 -> 1, la caméra s'approche du cadre du portrait
Test : python fiche.py <dossier>  (quelques images fixes)
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(ICI, "..", "..", "medias")
W, H = 1920, 1080
FONTS = "C:/Windows/Fonts/"

# palette : le simulateur (cyan) et l'humain (ambre), en RGB
FOND = (7, 15, 21)
CYAN = (150, 228, 240)
CYAN_D = (82, 150, 168)
CYAN_DD = (34, 66, 80)
BLANC = (228, 248, 252)
AMBRE = (255, 176, 72)


def _bahn(t, style="SemiBold"):
    f = ImageFont.truetype(FONTS + "bahnschrift.ttf", t)
    try:
        f.set_variation_by_name(style)
    except Exception:
        pass
    return f


F_TETE = _bahn(26)
F_LABEL = _bahn(25)
F_NOM = _bahn(104, "Bold")
F_SOUS = _bahn(26, "Light")
F_VAL = ImageFont.truetype(FONTS + "consola.ttf", 47)
F_LOG = ImageFont.truetype(FONTS + "consola.ttf", 24)


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def espace(texte, d, xy, font, fill, pas=3):
    """Texte en capitales espacées (HUD)."""
    x, y = xy
    for c in texte:
        d.text((x, y), c, font=font, fill=fill)
        x += d.textlength(c, font=font) + pas
    return x


def largeur_espace(texte, d, font, pas=3):
    return sum(d.textlength(c, font=font) + pas for c in texte)


def coins(d, x0, y0, x1, y1, n, col, w=3):
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(x, y), (x + sx * n, y)], fill=col, width=w)
        d.line([(x, y), (x, y + sy * n)], fill=col, width=w)


# ---------------------------------------------------------------- le portrait (même photo qu'en S11, nette à sa mort)
CADRE = (140, 196, 560, 756)          # emplacement du portrait, format photo d'identité 3:4
COLS, LIGNES_M = 15, 20               # premier cran de netteté : on lit une tête et des épaules, pas une personne


def _mosaique():
    photo = np.asarray(Image.open(os.path.join(M, "pexels", "portraits", "manoj_16067431.jpg")).convert("RGB"),
                       np.float32) / 255
    ph, pw = photo.shape[:2]
    # cadrage de photo d'identité sur fond noir : la tête au milieu, les épaules en bas, du vide autour
    CW, CH = 1200, 1600
    toile = np.zeros((CH, CW, 3), np.float32)
    w = int(CW * 0.80)
    h = int(w * ph / pw)
    im = cv2.resize(photo, (w, h), interpolation=cv2.INTER_AREA)
    yy, xx = np.mgrid[0:h, 0:w]
    tete = ((xx / w - 0.50) / 0.42) ** 2 + ((yy / h - 0.33) / 0.36) ** 2 < 1
    epaules = ((xx / w - 0.5) / 0.62) ** 2 + ((yy / h - 1.05) / 0.42) ** 2 < 1
    masque = cv2.GaussianBlur((tete | epaules).astype(np.float32), (0, 0), w * 0.025)
    im = im * masque[..., None]
    x0, y0 = (CW - w) // 2, int(CH * 0.18)
    hh = min(h, CH - y0)
    toile[y0:y0 + hh, x0:x0 + w] = im[:hh]
    petit = cv2.resize(toile, (COLS, LIGNES_M), interpolation=cv2.INTER_AREA)
    # l'humain en ambre : bichromie chaude, un peu de couleur d'origine
    lum = petit @ np.array([0.30, 0.55, 0.15], np.float32)
    lum = np.clip(lum / max(1e-3, np.percentile(lum, 97)), 0, 1) ** 1.3
    noir, mi, clair = np.array([10, 5, 3], np.float32), np.array([214, 118, 40], np.float32), np.array([255, 236, 190], np.float32)
    L = lum[..., None]
    duo = np.where(L < 0.5, noir + (mi - noir) * (L * 2), mi + (clair - mi) * (L * 2 - 1))
    rgb = (0.85 * duo + 0.15 * petit * 255) * 0.84   # un peu sous le blanc : le halo ne brûle pas le visage
    return np.clip(rgb, 0, 255)


MOSA = _mosaique()                    # RGB, LIGNES_M x COLS


def _dessine_portrait(img, p, k):
    """Le visage remplit le cadre de haut en bas, case par case (RGB uint8 en place)."""
    x0, y0, x1, y1 = CADRE
    cw, ch = (x1 - x0) / COLS, (y1 - y0) / LIGNES_M
    rng = np.random.default_rng(5)
    retard = rng.random((LIGNES_M, COLS)) * 0.18
    front = p * (1.25)                  # front de balayage, en proportion de la hauteur
    for r in range(LIGNES_M):
        for c in range(COLS):
            v = np.clip((front - r / LIGNES_M - retard[r, c]) / 0.08, 0, 1)
            if v <= 0:
                continue
            col = MOSA[r, c]
            # la case s'allume : d'abord un éclat clair, puis sa vraie teinte
            col = col * v + np.array(BLANC, np.float32) * (1 - v) * 0.6 * v * 4 * (1 - v)
            xa, ya = int(round(x0 + c * cw)), int(round(y0 + r * ch))
            xb, yb = int(round(x0 + (c + 1) * cw)), int(round(y0 + (r + 1) * ch))
            img[ya:yb - 2, xa:xb - 2] = np.clip(col * v + img[ya:yb - 2, xa:xb - 2] * (1 - v), 0, 255)
    # ligne de balayage ambre sur le front
    yf = y0 + min(1.0, front) * (y1 - y0)
    if 0 < p < 0.98:
        yi = int(yf)
        img[max(y0, yi - 2):min(y1, yi + 2), x0:x1] = AMBRE


# ---------------------------------------------------------------- pictos : les quatre aînés, puis lui
FILLE = ["..###..", "..###..", "...#...", ".#####.", "#.###.#", "..###..", ".#####.", "#######", "..#.#..", "..#.#.."]
GARCON = ["..###..", "..###..", "...#...", ".#####.", "#.###.#", "#.###.#", "..###..", "..#.#..", "..#.#..", "..#.#.."]
BEBE = [".......", ".......", ".......", "..###..", "..###..", "...#...", ".#####.", "..###..", "..#.#..", "......."]


def picto(d, motif, x, y, col, px=6):
    for r, ligne in enumerate(motif):
        for c, ch in enumerate(ligne):
            if ch == "#":
                d.rectangle([x + c * px, y + r * px, x + c * px + px - 2, y + r * px + px - 2], fill=col)


# ---------------------------------------------------------------- la fiche
CHAMPS = [  # (étiquette, valeur, début de la frappe)
    ("SEXE", "garçon", 0.95),
    ("NÉ À", "Inde · un village de pêcheurs", 1.35),
    ("RELIGION", "hindou", 2.35),
    ("REVENUS", "ceux du milieu", 2.75),
    ("AVANT LUI", "2 sœurs, 2 frères", 3.20),
]
CPS = 28           # lettres par seconde
NOM = "MANOJ MOHANTY"


def _couche(tl, portrait, k):
    im = Image.new("RGB", (W, H), FOND)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(3)
    # fond : une poussière de points qui dérive à peine (le fond n'est jamais figé)
    pts = rng.random((140, 3))
    for x, y, a in pts:
        xx = (x * W + 6 * tl) % W
        yy = (y * H - 3 * tl) % H
        c = tuple(int(v * (0.25 + 0.35 * a)) for v in CYAN_D)
        d.rectangle([xx, yy, xx + 2, yy + 2], fill=c)

    ouv = lisse(tl / 0.45)                                  # le cadre s'ouvre
    coins(d, 70, 52, W - 70, H - 52, int(44 * ouv), CYAN_DD, 2)
    # en-tête
    if tl > 0.1:
        espace("SIMULATION   ·   VIE N° 1 284 177", d, (140, 86), F_TETE, CYAN_D)
        t = "NAISSANCE   ·   2026"
        espace(t, d, (W - 140 - largeur_espace(t, d, F_TETE), 86), F_TETE, CYAN_D)
    xl = 140 + (W - 280) * ouv
    d.line([(140, 134), (xl, 134)], fill=CYAN_DD, width=2)
    for x in range(140, int(xl), 41):
        d.line([(x, 134), (x, 141 if (x - 140) % 205 else 148)], fill=CYAN_DD, width=2)

    # le cadre du portrait
    x0, y0, x1, y1 = CADRE
    d.rectangle([x0, y0, x1, y1], fill=(11, 24, 32))
    if portrait < 1:
        # en attente : une silhouette éteinte, une ligne qui balaie, un « ? »
        sil = (24, 44, 56)
        cx = (x0 + x1) // 2
        d.ellipse([cx - 92, y0 + 120, cx + 92, y0 + 330], fill=sil)
        d.pieslice([x0 + 40, y0 + 370, x1 - 40, y1 + 230], 180, 360, fill=sil)
        d.rectangle([x0, y1 + 1, x1, y1 + 240], fill=FOND)
        d.text((cx - 18, y0 + 182), "?", font=_bahn(84, "Light"), fill=(50, 84, 100))
        yb = y0 + ((tl * 0.35) % 1.0) * (y1 - y0)
        d.line([(x0 + 4, yb), (x1 - 4, yb)], fill=(46, 92, 108), width=2)
    coins(d, x0 - 10, y0 - 10, x1 + 10, y1 + 10, 34, CYAN, 3)
    espace("PORTRAIT", d, (x0, y1 + 28), F_LABEL, CYAN_D)
    # jauge de netteté : 7 crans ; le premier s'allume avec le visage (il ne sera net qu'à sa mort)
    espace("NETTETÉ", d, (x0, y1 + 66), F_LABEL, CYAN_DD)
    xg = x1 - 7 * 28 + 8
    for i in range(7):
        xa = xg + i * 28
        allume = i == 0 and portrait > 0.85
        d.rectangle([xa, y1 + 70, xa + 20, y1 + 90], outline=AMBRE if allume else CYAN_DD, width=2,
                    fill=AMBRE if allume else None)

    # le nom
    xn, yn = 660, 176
    n = int(np.clip((tl - 0.35) * 22, 0, len(NOM)))
    if n:
        d.text((xn, yn), NOM[:n], font=F_NOM, fill=BLANC)
    if tl > 0.85:
        espace("DOSSIER DE NAISSANCE", d, (xn + 4, yn + 128), F_SOUS, CYAN_D, pas=5)

    # les champs
    y = 392
    for i, (lab, val, t0) in enumerate(CHAMPS):
        if tl > t0 - 0.2:
            espace(lab, d, (xn + 2, y + 14), F_LABEL, CYAN_D)
        ls = lisse((tl - (t0 - 0.35)) / 0.4)
        if ls > 0:
            d.line([(xn, y + 72), (xn + (1780 - xn) * ls, y + 72)], fill=CYAN_DD, width=1)
        nv = int(max(0, (tl - t0) * CPS))
        if nv > 0:
            d.text((960, y + 4), val[:nv], font=F_VAL, fill=BLANC)
            if nv < len(val) and int(tl * 4) % 2 == 0:
                xc = 960 + d.textlength(val[:nv], font=F_VAL) + 4
                d.rectangle([xc, y + 10, xc + 22, y + 58], fill=CYAN)
        if lab == "AVANT LUI":
            # les quatre aînés, puis lui (en ambre)
            tp = t0 + len(val) / CPS + 0.1
            motifs = [FILLE, FILLE, GARCON, GARCON]
            for j, mo in enumerate(motifs):
                if tl > tp + 0.12 * j:
                    picto(d, mo, 1440 + j * 58, y - 2, CYAN)
            if tl > tp + 0.7:
                if int((tl - tp - 0.7) * 2.5) % 2 == 0 or tl > tp + 1.9:
                    picto(d, BEBE, 1440 + 4 * 58 + 22, y - 2, AMBRE)
        y += 84

    # pied de page : le journal du simulateur
    if tl > 0.6:
        log = "> vie n° 1 284 177 : naissance enregistrée"
        nl = int(np.clip((tl - 0.6) * 40, 0, len(log)))
        d.text((140, H - 118), log[:nl], font=F_LOG, fill=CYAN_DD)
        t = "UNE VIE SUR HUIT MILLIARDS"
        espace(t, d, (W - 140 - largeur_espace(t, d, F_TETE), H - 120), F_TETE, CYAN_DD)

    a = np.asarray(im).copy()
    if portrait > 0:
        a = a.astype(np.float32)
        _dessine_portrait(a, portrait, k)
        a = np.clip(a, 0, 255).astype(np.uint8)
    return a


def _vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    return np.clip(1.08 - 0.32 * r ** 2, 0, 1)[..., None]


VIG = _vignette()
LIGNES = np.ones((H, 1, 1), np.float32)
LIGNES[::3] = 0.86


def fiche(tl, portrait=0.0, zoom=0.0, k=0):
    rgb = _couche(tl, portrait, k).astype(np.float32)
    img = rgb[:, :, ::-1].copy()                      # BGR
    if zoom > 0:
        # la caméra s'approche du portrait : son centre glisse vers le centre de l'image
        x0, y0, x1, y1 = CADRE
        s = 1 + 0.72 * zoom
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 14
        tx = (cx + (W / 2 - cx) * zoom) - s * cx
        ty = (cy + (H / 2 - cy) * zoom) - s * cy
        Mz = np.float32([[s, 0, tx], [0, s, ty]])
        img = cv2.warpAffine(img, Mz, (W, H), flags=cv2.INTER_LINEAR, borderValue=FOND[::-1])
    # halo des éléments clairs, lignes de balayage, léger décalage des couleurs, vignette, grain
    halo = cv2.GaussianBlur(np.clip(img - 90, 0, 255), (0, 0), 9)
    img = img + 0.55 * halo + 0.25 * cv2.GaussianBlur(img, (0, 0), 28)
    img = img * LIGNES
    img[..., 0] = np.roll(img[..., 0], 2, axis=1)
    img[..., 2] = np.roll(img[..., 2], -2, axis=1)
    img = img * VIG
    rng = np.random.default_rng(900 + k)
    img += rng.normal(0, 3.2, img.shape).astype(np.float32)
    img *= 1 + 0.012 * np.sin(k * 2.1)               # un scintillement d'écran, à peine
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    for nom, (tl, p, z) in {"a_frappe": (2.0, 0, 0), "b_complete": (5.2, 0, 0),
                            "c_portrait_mi": (30, 0.5, 0.1), "d_portrait_fin": (30, 1.0, 1.0),
                            "e_portrait_plein": (30, 1.0, 0.0)}.items():
        cv2.imwrite(os.path.join(out, f"fiche_{nom}.png"), np.clip(fiche(tl, p, z), 0, 255).astype(np.uint8))
    print("ok")
