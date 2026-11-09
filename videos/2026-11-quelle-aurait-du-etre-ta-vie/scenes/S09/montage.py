"""S09 · la vie adulte (15 à 60 ans). Montage, motion design et son.

Bruno (09/11/2026) : « je veux vraiment un montage dynamique et fluide […] animations, transitions, modèles viraux
et mécanismes qui marchent ». Donc :
  - l'âge CLAQUE au centre (gros chiffre, secousse, souffle grave) puis file se ranger dans le coin ;
  - chaque choix : les cartes arrivent en cascade, le curseur rouge hésite (tics), le clic, la carte choisie devient
    rouge et l'on TRAVERSE la carte pour entrer dans la vie choisie (zoom à travers) ;
  - « la mer, les bêtes ou la terre » : trois coupes sèches sur les mots, en coups de fouet (whip) ;
  - images fixes jamais immobiles : poussées, dérives, recadrages serrés sur les mots (punch-in) ;
  - les grappes de vie sur le tempo de la musique (coupes au temps, montée en trois cadrages pour la maison) ;
  - un fil rouge apparaît au moment de la dette, sous toute la suite, et palpite à 60 ans (« vous devez encore ») ;
  - silences francs avant les choix et avant « À trente-neuf ans, il ment » ; la musique coupe net.
Trois plans animés par Seedance 2.0 (le bateau plein, le théâtre, la barque à 60 ans) ; le reste en images fixes.

Usage : python montage.py   ->  medias/S09/S09_v1.mp4     (--test <dossier> ; TEMPS=1.0,2.5 ; SON_SEUL=1)
"""
import math
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..", "..", "..")
sys.path.insert(0, os.path.join(RACINE, "shared", "outils", "son"))
sys.path.insert(0, os.path.join(ICI, "..", "S08"))
from pas import SR, boucle, ecrire_normalise, lire_audio  # noqa: E402
import hf  # noqa: E402

M = os.path.join(ICI, "..", "..", "medias")
HFD = os.path.join(M, "S09", "higgsfield")
D3 = os.path.join(M, "S09", "3d")
SONS = os.path.join(M, "sons", "epidemic")
OUT = os.path.join(M, "S09")
W, H, FPS = 1920, 1080, 24
FONTS = "C:/Windows/Fonts/"
CREME = (238, 230, 216)
ROUGE = (214, 72, 46)          # RVB


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def expo_out(p):
    p = min(1.0, max(0.0, p))
    return 1 - 2 ** (-10 * p) if p < 1 else 1.0


def expo_in(p):
    p = min(1.0, max(0.0, p))
    return 0.0 if p == 0 else 2 ** (10 * p - 10)


def expo_inout(p):
    p = min(1.0, max(0.0, p))
    if p in (0.0, 1.0):
        return p
    return 2 ** (20 * p - 10) / 2 if p < 0.5 else (2 - 2 ** (-20 * p + 10)) / 2


# ---------------------------------------------------------------- la voix (prise 1, une seule génération ; coupée en phrases)
VOIX_F = os.path.join(M, "voix", "S09_prise1.mp3")
P_ = {  # phrase : (début, fin) dans la prise
    "15a": (4.37, 8.19), "15b": (8.56, 12.61), "ecart": (13.35, 14.27), "pecheur": (15.17, 15.78),
    "salaire": (16.14, 19.58), "rien": (20.73, 21.46), "regarde": (22.43, 23.70), "nuits": (24.41, 27.61),
    "plein": (28.18, 32.54), "24": (33.33, 36.86), "cher": (37.73, 38.84), "pharma": (39.49, 41.86),
    "hopital": (43.06, 43.77), "guerit": (44.43, 46.36), "freres": (46.83, 48.74), "32": (49.29, 50.53),
    "49": (51.14, 52.73), "preeti": (53.87, 56.86), "maries": (57.65, 59.59), "pradeep": (60.41, 63.71),
    "usha": (64.52, 67.77), "maison": (68.60, 73.40), "ment": (74.24, 76.28), "appris": (77.24, 80.65),
    "pardon": (81.73, 83.76), "confiance": (84.44, 86.23), "th27": (87.58, 90.20), "th53": (91.10, 95.55),
    "60": (96.80, 97.93), "argent": (98.33, 100.03), "continue": (100.86, 101.56), "question": (102.16, 105.28),
}
POS = {  # phrase : position dans la scène (s)
    "15a": 0.55, "15b": 4.6, "ecart": 11.2, "pecheur": 12.95,
    "salaire": 14.5, "rien": 18.35, "regarde": 19.5, "nuits": 21.9, "plein": 25.5,
    "24": 32.0, "cher": 35.9, "pharma": 37.25, "hopital": 41.75, "guerit": 43.0, "freres": 45.4, "32": 47.6, "49": 49.3,
    "preeti": 52.3, "maries": 59.0,
    "pradeep": 61.3, "usha": 64.9, "maison": 68.5,
    "ment": 74.1, "appris": 76.7, "pardon": 80.5, "confiance": 83.0,
    "th27": 85.4, "th53": 88.4,
    "60": 99.0, "argent": 100.45, "continue": 105.6, "question": 108.6,
}
DUREE = 115.0
N = int(round(DUREE * FPS))


def fin(nom):
    a, b = P_[nom]
    return POS[nom] + b - a


def mot(nom, q):
    """L'instant où tombe la fraction q de la phrase (pour couper sur un mot)."""
    a, b = P_[nom]
    return POS[nom] + q * (b - a)


# ---------------------------------------------------------------- les sources
_img = {}


def source(nom):
    if nom not in _img:
        for d, ext in ((HFD, ".png"), (HFD, ".jpg"), (D3, ".png")):
            p = os.path.join(d, nom + ext)
            if os.path.exists(p):
                _img[nom] = cv2.imread(p).astype(np.float32)
                break
        else:
            alt = {"betes": os.path.join(M, "S08", "higgsfield", "betes_restyle.png"),
                   "portail": os.path.join(M, "S08", "higgsfield", "portail_debut_restyle.png"),
                   "classe": os.path.join(M, "S07", "higgsfield", "t_classe.png"),
                   "bureau": os.path.join(M, "S02", "S02_p06_bureau.png")}[nom]
            _img[nom] = cv2.imread(alt).astype(np.float32)
    return _img[nom]


def cadre(nom, z=1.0, cx=0.5, cy=0.5, rot=0.0):
    """Un cadrage dans une image fixe : zoom z autour du point (cx, cy) de la source (fractions), sans bord."""
    s_ = source(nom)
    hs, ws = s_.shape[:2]
    s = max(W / ws, H / hs) * z
    cx = min(max(cx, W / (2 * s * ws)), 1 - W / (2 * s * ws))
    cy = min(max(cy, H / (2 * s * hs)), 1 - H / (2 * s * hs))
    m = cv2.getRotationMatrix2D((cx * ws, cy * hs), rot, s)
    m[0, 2] += W / 2 - cx * ws
    m[1, 2] += H / 2 - cy * hs
    return cv2.warpAffine(s_, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def video(nom, t, duree, vitesse=1.0):
    """Une vidéo Seedance, recadrée en 1920x1080 ; sinon l'image fixe correspondante (poussée lente)."""
    p = os.path.join(HFD, nom + ".mp4")
    if os.path.exists(p):
        return hf.image(p, duree, max(0.0, t) * vitesse)
    return cadre(nom, 1.04 + 0.08 * t / duree)


# ---------------------------------------------------------------- les effets
def flou_mouvement(f, dx, dy=0):
    """Flou de bougé directionnel (coups de fouet, zooms)."""
    n = int(max(abs(dx), abs(dy)))
    if n < 2:
        return f
    k = np.zeros((2 * n + 1, 2 * n + 1), np.float32)
    cv2.line(k, (n - int(dx / 2), n - int(dy / 2)), (n + int(dx / 2), n + int(dy / 2)), 1.0, 1)
    return cv2.filter2D(f, -1, k / k.sum())


def decaler(f, dx, dy=0):
    m = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(f, m, (W, H), borderMode=cv2.BORDER_REFLECT)


def zoom_radial(f, z, flou=0.0):
    """Zoom centré, avec un flou radial (plusieurs zooms superposés) : la traversée."""
    acc = np.zeros_like(f)
    k = 5 if flou > 0.01 else 1
    for i in range(k):
        zi = z * (1 + flou * i / max(1, k - 1))
        m = cv2.getRotationMatrix2D((W / 2, H / 2), 0, zi)
        acc += cv2.warpAffine(f, m, (W, H), borderMode=cv2.BORDER_REFLECT)
    return acc / k


def secousse(t, t0, force=14.0, duree=0.35):
    if not (t0 <= t < t0 + duree):
        return 0.0, 0.0
    d = 1 - (t - t0) / duree
    r = np.random.default_rng(int(t * 1000))
    return float(r.normal(0, force * d)), float(r.normal(0, force * d))


def flash(f, t, t0, force=0.55, duree=0.16, couleur=(1.0, 0.92, 0.82)):
    if t0 <= t < t0 + duree:
        q = (1 - (t - t0) / duree) ** 2 * force
        f = f * (1 - q) + 255 * np.float32(couleur[::-1]) * q
    return f


_xx, _yy = np.meshgrid(np.linspace(-1, 1, W), np.linspace(-1, 1, H))
VIGNETTE = (1 - 0.32 * (_xx ** 2 + _yy ** 2) / 2).astype(np.float32)[..., None]


def lueur(f, t, t0, t1, couleur=(1.0, 0.62, 0.3), force=0.35):
    """Une fuite de lumière chaude qui traverse le cadre de gauche à droite (les moments de joie)."""
    if not (t0 <= t < t1):
        return f
    q = (t - t0) / (t1 - t0)
    cx = -0.6 + 2.4 * q
    g = np.exp(-(((_xx - cx) / 0.55) ** 2 + ((_yy + 0.4) / 0.9) ** 2)).astype(np.float32)[..., None]
    a = force * math.sin(math.pi * q)
    return f + g * a * 255 * np.float32(couleur[::-1])


def etalonner(f, chaud=0.0, froid=0.0, sature=1.0, expo=1.0):
    if chaud:
        f = f * np.float32([1 - 0.06 * chaud, 1 + 0.02 * chaud, 1 + 0.10 * chaud])
    if froid:
        f = f * np.float32([1 + 0.12 * froid, 1 + 0.03 * froid, 1 - 0.08 * froid])
    if sature != 1.0:
        g = f.mean(2, keepdims=True)
        f = g + (f - g) * sature
    return f * expo


def rvb_decale(f, d):
    d = int(d)
    if d == 0:
        return f
    o = f.copy()
    o[..., 2] = np.roll(f[..., 2], d, axis=1)
    o[..., 0] = np.roll(f[..., 0], -d, axis=1)
    return o


# ---------------------------------------------------------------- la typographie
F_AGE_GRAND = ImageFont.truetype(FONTS + "georgia.ttf", 300)
F_AGE_PETIT = ImageFont.truetype(FONTS + "georgia.ttf", 92)
F_CARTE = ImageFont.truetype(FONTS + "georgia.ttf", 60)
F_PHRASE = ImageFont.truetype(FONTS + "georgiai.ttf", 64)
F_CHIFFRE = ImageFont.truetype(FONTS + "georgia.ttf", 150)
_calques = {}


def calque(texte, font, couleur=CREME):
    """Un texte en calque (RVB, alpha, ombre douce), centré sur son propre cadre."""
    cle = (texte, font.size, couleur)
    if cle not in _calques:
        d0 = ImageDraw.Draw(Image.new("L", (10, 10)))
        x0, y0, x1, y1 = d0.textbbox((0, 0), texte, font=font)
        w, h = x1 - x0 + 80, y1 - y0 + 80
        c = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(c).text((40 - x0, 40 - y0), texte, font=font, fill=(*couleur, 255))
        a = np.asarray(c).astype(np.float32)
        _calques[cle] = (a[..., :3][..., ::-1].copy(), a[..., 3] / 255, cv2.GaussianBlur(a[..., 3], (0, 0), 14) / 255)
    return _calques[cle]


def poser_calque(f, cal, cx, cy, ech=1.0, opac=1.0, flou=0.0, ombre=0.5):
    rgb, al, om = cal
    if ech != 1.0:
        rgb, al, om = (cv2.resize(v, None, fx=ech, fy=ech, interpolation=cv2.INTER_LINEAR) for v in (rgb, al, om))
    if flou > 0.5:
        rgb, al = cv2.GaussianBlur(rgb, (0, 0), flou), cv2.GaussianBlur(al, (0, 0), flou)
    h, w = al.shape
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return f
    sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0))
    zone = f[ya:yb, xa:xb]
    o = om[sl][..., None] * ombre * opac
    a = al[sl][..., None] * opac
    zone = zone * (1 - o)
    f[ya:yb, xa:xb] = zone * (1 - a) + rgb[sl] * a
    return f


# l'âge : il claque au centre, puis file dans le coin (et y reste jusqu'au prochain)
AGES = [("15 ans", 0.0, 31.0), ("24 ans", 31.55, 51.7), ("26 ans", 51.75, 61.0), ("60 ans", 98.2, 108.4)]
T_COIN = 0.95


def age(f, t):
    for txt, t0, t1 in AGES:
        if not (t0 <= t < t1 + 0.3):
            continue
        dt = t - t0
        sortie = 1 - lisse((t - t1) / 0.3)
        if dt < T_COIN:                                           # le claquement : de très grand à grand, au centre
            q = expo_out(dt / 0.28)
            ech = 1.55 - 0.55 * q
            opac = min(1.0, dt / 0.06)
            f = f * (1 - 0.5 * min(1.0, dt / 0.08) * (1 - lisse((dt - 0.6) / 0.35)))     # le fond s'assombrit
            f = poser_calque(f, calque(txt, F_AGE_GRAND), W / 2, H / 2, ech, opac, flou=8 * (1 - q))
        else:                                                     # il file dans le coin bas-gauche
            q = expo_inout((dt - T_COIN) / 0.45)
            cal_g = calque(txt, F_AGE_GRAND)
            e_fin = F_AGE_PETIT.size / F_AGE_GRAND.size
            ech = 1.0 + (e_fin - 1.0) * q
            w_fin = cal_g[1].shape[1] * e_fin
            cx = W / 2 + (110 + w_fin / 2 - W / 2) * q
            cy = H / 2 + (930 - H / 2) * q
            f = poser_calque(f, cal_g, cx, cy, ech, sortie, flou=6 * math.sin(math.pi * min(1, q)))
    return f


# ---------------------------------------------------------------- les choix : cartes, curseur qui hésite, clic, traversée
class Choix:
    def __init__(self, options, t_arrive, t_clic, choisie, hesite=None, fond="terre"):
        self.options, self.t0, self.tc, self.k, self.fond = options, t_arrive, t_clic, choisie, fond
        self.hesite = hesite or []           # [(instant, carte survolée)]
        n = len(options)
        self.w = 410 if n == 4 else 500 if n == 3 else 600
        gap = 40
        tot = n * self.w + (n - 1) * gap
        self.x = [W / 2 - tot / 2 + i * (self.w + gap) for i in range(n)]
        self.y, self.h = 370, 340

    def survol(self, t):
        k = None
        for ti, kk in self.hesite:
            if t >= ti:
                k = kk
        return self.k if t >= self.tc else k

    def rendu(self, f, t):
        """Les cartes sur le fond flouté. Renvoie l'image et le rectangle de la carte choisie."""
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        sv = self.survol(t)
        for i, opt in enumerate(self.options):
            q = expo_out((t - self.t0 - 0.09 * i) / 0.5)                     # arrivée en cascade, de bas en haut
            if q <= 0:
                continue
            dy = 90 * (1 - q)
            choisie = t >= self.tc and i == self.k
            tombe = t >= self.tc and i != self.k
            a = int(255 * q * (1 - lisse((t - self.tc - 0.05) / 0.3) if tombe else q * 255) if tombe else 255 * q)
            dy += 140 * expo_in((t - self.tc) / 0.4) if tombe else 0
            pop = 1.0
            if choisie:
                pop = 1 + 0.06 * math.sin(math.pi * min(1, (t - self.tc) / 0.22))
            elif sv == i:
                pop = 1.03
            x0, y0 = self.x[i], self.y + dy
            cxm, cym = x0 + self.w / 2, y0 + self.h / 2
            ww, hh = self.w * pop, self.h * pop
            r = [cxm - ww / 2, cym - hh / 2, cxm + ww / 2, cym + hh / 2]
            fond = (ROUGE[0], ROUGE[1], ROUGE[2], a) if choisie else (16, 18, 22, int(a * 0.86))
            bord = (ROUGE[0], ROUGE[1], ROUGE[2], a) if (sv == i or choisie) else (*[int(c * 0.55) for c in CREME], a)
            d.rounded_rectangle(r, radius=22, fill=fond, outline=bord, width=4 if sv == i else 2)
            lignes = opt.split("\n")
            for j, l_ in enumerate(lignes):
                tw = d.textlength(l_, font=F_CARTE)
                yy = cym - 40 * len(lignes) + j * 78
                d.text((cxm - tw / 2, yy), l_, font=F_CARTE, fill=(*CREME, a))
        a = np.asarray(im).astype(np.float32)
        al = a[..., 3:4] / 255
        f = f * (1 - al) + a[..., :3][..., ::-1] * al
        x0 = self.x[self.k]
        return f, (x0, self.y, x0 + self.w, self.y + self.h)


def scene_choix(c, t, fond_img):
    """Le fond (l'image floutée et assombrie) + les cartes ; après le clic, on traverse la carte rouge."""
    fl = cv2.GaussianBlur(fond_img, (0, 0), 18) * 0.42
    q_in = expo_out((t - c.t0) / 0.5)
    f = fond_img * (1 - q_in) + fl * q_in
    f, rect = c.rendu(f, t)
    return f, rect


def traverser(f_carte, rect, f_suite, q):
    """Zoom à travers la carte choisie : elle grandit jusqu'à remplir l'écran, la suite apparaît dedans."""
    x0, y0, x1, y1 = rect
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    z = 1 + 9 * expo_in(q)
    m = cv2.getRotationMatrix2D((cx, cy), 0, z)
    m[0, 2] += (W / 2 - cx) * expo_inout(q)
    m[1, 2] += (H / 2 - cy) * expo_inout(q)
    a = cv2.warpAffine(f_carte, m, (W, H), borderMode=cv2.BORDER_REPLICATE)
    a = zoom_radial(a, 1.0, 0.06 * q)
    b = zoom_radial(f_suite, 1.25 - 0.25 * expo_out(q), 0.05 * (1 - q))
    k = lisse((q - 0.55) / 0.4)
    return a * (1 - k) + b * k


CH15 = Choix(["Pêcheur", "Éleveur", "Paysan", "Attendre\nun meilleur\nemploi"], 8.85, 12.85, 0,
             hesite=[(9.7, 1), (10.25, 0), (10.75, 1), (11.3, 0), (11.75, 1), (12.25, 0), (12.55, 1)])
CH24 = Choix(["Se faire soigner\nà l'hôpital", "La pharmacie\net les remèdes"], 36.0, 41.6, 0,
             hesite=[(38.0, 1), (39.0, 0), (39.8, 1), (40.6, 0), (41.15, 1)])
CH26 = Choix(["Se marier", "Prendre le temps\nde mieux\nse connaître", "Refuser"], 55.5, 58.55, 0,
             hesite=[(56.4, 1), (57.4, 0)])
CH60 = Choix(["Continuer\nà travailler", "Prendre\nvotre retraite", "Passer à\ntemps partiel"], 102.4, 105.45, 0,
             hesite=[(103.0, 1), (103.8, 2), (104.4, 1), (104.95, 0)])
D_TRAV = 0.55


# ---------------------------------------------------------------- le fil rouge de la dette
T_DETTE = mot("guerit", 0.62)          # « … et il s'endette »
T_PULSE = mot("argent", 0.2)


def fil_dette(f, t):
    if t < T_DETTE or t >= 108.4:
        return f
    q = expo_out((t - T_DETTE) / 1.1)
    x1 = int(W * q)
    y = H - 46
    ep = 3
    a = 0.85
    if t >= T_PULSE:
        p = 0.5 + 0.5 * math.sin(2 * math.pi * 1.1 * (t - T_PULSE))
        ep, a = 3 + int(3 * p), 0.85 + 0.15 * p
    zone = f[y - ep:y + ep, :x1]
    f[y - ep:y + ep, :x1] = zone * (1 - a) + np.float32(ROUGE[::-1]) * a
    gl = cv2.GaussianBlur(np.pad(np.ones((2 * ep, x1), np.float32), ((24, 24), (0, 0))), (0, 0), 10)[..., None] if x1 > 4 else None
    if gl is not None:
        f[y - ep - 24:y + ep + 24, :x1] += gl * 60 * np.float32(ROUGE[::-1]) / 255 * a
    return f


# ---------------------------------------------------------------- les phrases à l'écran (mot à mot)
def phrase_ecran(f, t, texte, t0, t1, y=H - 200):
    if not (t0 <= t < t1 + 0.4):
        return f
    mots = texte.split(" ")
    sortie = 1 - lisse((t - t1) / 0.4)
    largeurs = [calque(m_, F_PHRASE)[1].shape[1] - 80 for m_ in mots]
    esp = 22
    tot = sum(largeurs) + esp * (len(mots) - 1)
    x = W / 2 - tot / 2
    for i, (m_, lw) in enumerate(zip(mots, largeurs)):
        ti = t0 + 0.13 * i
        q = expo_out((t - ti) / 0.35)
        if q > 0:
            f = poser_calque(f, calque(m_, F_PHRASE), x + lw / 2, y + 26 * (1 - q), 1.0, q * sortie, flou=5 * (1 - q), ombre=0.7)
        x += lw + esp
    return f


def gros_chiffre(f, t, txt, t0, t1, cx, cy):
    if not (t0 <= t < t1):
        return f
    q = expo_out((t - t0) / 0.3)
    s = 1 - lisse((t - (t1 - 0.3)) / 0.3)
    return poser_calque(f, calque(txt, F_CHIFFRE), cx, cy, 1.3 - 0.3 * q, q * s, flou=6 * (1 - q), ombre=0.8)


# ---------------------------------------------------------------- le déroulé, plan par plan
def whip(fa, fb, q, sens=1):
    """Coup de fouet horizontal entre deux images (q de 0 à 1)."""
    if q < 0.5:
        e = expo_in(q * 2)
        return flou_mouvement(decaler(fa, -sens * W * 0.35 * e), 160 * e)
    e = 1 - expo_out((q - 0.5) * 2)
    return flou_mouvement(decaler(fb, sens * W * 0.35 * e), 160 * e)


def mer_mots(t):
    """« la mer, les bêtes ou la terre » : trois coupes sur les mots, poussées rapides."""
    tm, tb, tt = mot("15b", 0.36), mot("15b", 0.58), mot("15b", 0.80)
    if t < tm:      # « On vous propose » : l'école fermée (souvenir de S08), désaturée, qui s'éloigne
        dt = t - 1.9
        return etalonner(cadre("portail", 1.18 - 0.1 * lisse(dt / 4.5), 0.42, 0.5), sature=0.45, expo=0.8)
    if t < tb:
        return cadre("bateau_plein", 1.22 - 0.16 * expo_out((t - tm) / 0.6), 0.5, 0.45)
    if t < tt:
        return cadre("betes", 1.22 - 0.16 * expo_out((t - tb) / 0.6), 0.45, 0.55)
    return cadre("terre", 1.22 - 0.14 * expo_out((t - tt) / 0.6) - 0.04 * lisse((t - tt - 0.6) / 2), 0.45, 0.5)


def plan(t):
    """L'image de base (sans les surcouches communes) à l'instant t."""
    # ---------------- 15 ans
    if t < 1.9:
        return etalonner(cadre("portail", 1.3 - 0.12 * lisse(t / 1.9), 0.42, 0.5), sature=0.45, expo=0.8)
    if t < CH15.t0:
        f = mer_mots(t)
        for tc in (mot("15b", 0.36), mot("15b", 0.58), mot("15b", 0.80)):     # les coups de fouet sur les mots
            if tc - 0.1 <= t < tc + 0.1:
                q = (t - (tc - 0.1)) / 0.2
                f = whip(mer_mots(tc - 0.11), mer_mots(tc + 0.01), q, 1)
        return f
    if t < CH15.tc + D_TRAV:
        f, rect = scene_choix(CH15, t, cadre("terre", 1.04, 0.45, 0.5))
        if t >= CH15.tc + 0.12:
            q = (t - CH15.tc - 0.12) / (D_TRAV - 0.12)
            f = traverser(f, rect, cadre("mer_nuit", 1.12), q)
        return f
    # ---------------- la mer : la mère, les nuits, le bateau plein
    if t < 16.4:                                                    # on arrive en mer, la nuit (dérive)
        dt = t - (CH15.tc + D_TRAV)
        return etalonner(cadre("mer_nuit", 1.12 - 0.05 * lisse(dt / 3), 0.5 - 0.03 * dt / 3, 0.5), expo=0.95)
    if t < 18.35:                                                   # « un cadeau à sa mère »
        dt = t - 16.4
        return cadre("mere", 1.08 + 0.06 * lisse(dt / 2), 0.55, 0.45)
    if t < 19.5:                                                    # « Elle ne dit rien. » : punch-in sur elle
        dt = t - 18.35
        return cadre("mere", 1.55 + 0.04 * dt, 0.33, 0.45)
    if t < 21.9:                                                    # « Elle le regarde longtemps. » : le cadeau, lent
        dt = t - 19.5
        return cadre("mere", 1.35 + 0.18 * lisse(dt / 2.4), 0.47, 0.42)
    if t < 25.5:                                                    # les nuits sans poisson : dérive latérale lente
        dt = t - 21.9
        return etalonner(cadre("mer_nuit", 1.2, 0.36 + 0.16 * dt / 3.6, 0.5), froid=0.3, expo=0.9)
    if t < 31.0:                                                    # le bateau revient plein (Seedance)
        dt = t - 25.5
        f = video("bateau_plein", dt, 9.0)   # on ne garde que le début, ralenti (la fin pousse trop)
        return lueur(f, t, 27.6, 30.6)
    # ---------------- 24 ans : la toux, l'hôpital
    if t < 31.55:
        return np.zeros((H, W, 3), np.float32) + 6
    if t < CH24.t0:
        dt = t - 31.55
        return etalonner(cadre("hopital", 1.25 - 0.15 * lisse(dt / 4.4), 0.55, 0.45), froid=0.4)
    if t < CH24.tc + D_TRAV:
        f, rect = scene_choix(CH24, t, etalonner(cadre("hopital", 1.1, 0.55, 0.45), froid=0.4))
        if t >= CH24.tc + 0.12:
            f = traverser(f, rect, etalonner(cadre("hopital", 1.0, 0.55, 0.45), froid=0.2), (t - CH24.tc - 0.12) / (D_TRAV - 0.12))
        return f
    if t < 45.4:                                                    # « Il guérit, et il s'endette » : la lumière revient
        dt = t - (CH24.tc + D_TRAV)
        g = lisse((t - POS["guerit"]) / 1.2)
        return etalonner(cadre("hopital", 1.0 + 0.1 * lisse(dt / 3.3), 0.5, 0.45), froid=0.2 * (1 - g), expo=0.95 + 0.12 * g)
    if t < 51.7:                                                    # les frères : l'un, puis l'autre, s'effacent
        dt = t - 45.4
        z = 1.05 + 0.1 * lisse(dt / 6.3)
        f = cadre("freres", z, 0.5, 0.5)
        if os.path.exists(os.path.join(HFD, "freres_2.png")):
            k1 = lisse((t - (mot("32", 0.5))) / 0.9)
            k2 = lisse((t - (mot("49", 0.5))) / 0.9)
            f = f * (1 - k1) + cadre("freres_2", z, 0.5, 0.5) * k1
            if os.path.exists(os.path.join(HFD, "freres_1.png")):
                f = f * (1 - k2) + cadre("freres_1", z, 0.5, 0.5) * k2
        return f
    # ---------------- 26 ans : Preeti, le mariage
    if t < CH26.t0:
        dt = t - 51.7
        return cadre("preeti", 1.0 + 0.22 * lisse(dt / 3.8), 0.5, 0.5)
    if t < CH26.tc + D_TRAV:
        f, rect = scene_choix(CH26, t, cadre("preeti", 1.22, 0.5, 0.5))
        if t >= CH26.tc + 0.12:
            f = traverser(f, rect, cadre("mariage", 1.15, 0.5, 0.5), (t - CH26.tc - 0.12) / (D_TRAV - 0.12))
        return f
    if t < 61.2:                                                    # le mariage : la musique arrive
        dt = t - (CH26.tc + D_TRAV)
        return lueur(cadre("mariage", 1.15 - 0.12 * expo_out(dt / 1.5), 0.5, 0.5), t, 59.2, 61.6, force=0.3)
    # ---------------- la grappe, sur le tempo (un temps = 60/112 s)
    if t < mot("pradeep", 0.62):                                    # « Pradeep naît »
        dt = t - 61.2
        return cadre("naissance", 1.1 + 0.05 * dt, 0.5, 0.5)
    if t < 64.9:                                                    # « puis une fille, Usha » : punch-in sur le bébé
        dt = t - mot("pradeep", 0.62)
        return cadre("naissance", 1.7 + 0.06 * dt, 0.34, 0.58)
    if t < fin("usha") + 0.2:                                       # « À douze ans, il avait une amie… » : le souvenir
        dt = t - 64.9
        f = etalonner(cadre("classe", 1.15 + 0.05 * dt, 0.5, 0.5), sature=0.3, expo=0.85)
        f = rvb_decale(f, 10 * (1 - lisse(dt / 0.4)) + 3)
        if (int(dt * FPS) % 7) == 0:
            f *= 0.86
        return f
    if t < 74.0:                                                    # la maison, montée en trois cadrages sur les temps
        dt = t - (fin("usha") + 0.2)
        b = 60 / 112 * 2
        k = min(2, int(dt / b))
        if k == 0:
            return cadre("maison", 2.2, 0.32, 0.62)
        if k == 1:
            return cadre("maison", 1.6, 0.55, 0.55)
        return cadre("maison", 1.12 - 0.08 * lisse((dt - 2 * b) / 3), 0.5, 0.5)
    # ---------------- 39 ans : le mensonge (silence, froid)
    if t < 80.5:
        dt = t - 74.0
        return etalonner(cadre("mensonge", 1.12 + 0.03 * dt / 6.5, 0.4 + 0.25 * lisse((t - POS["appris"]) / 3.5), 0.5),
                         froid=0.35, sature=0.8)
    if t < 83.0:                                                    # « Il lui demande pardon, longtemps. »
        dt = t - 80.5
        return etalonner(cadre("mensonge", 1.75 + 0.05 * dt, 0.2, 0.52), froid=0.35, sature=0.8)
    if t < 85.4:                                                    # « Elle lui refait confiance. » : la lumière se réchauffe
        dt = t - 83.0
        g = lisse(dt / 2.2)
        return etalonner(cadre("mensonge", 1.12 - 0.05 * g, 0.5, 0.5), froid=0.35 * (1 - g), chaud=0.5 * g,
                         sature=0.8 + 0.2 * g, expo=1 + 0.15 * g)
    # ---------------- le théâtre
    if t < 88.4:
        dt = t - 85.4
        return cadre("theatre", 1.0 + 0.12 * lisse(dt / 3), 0.5, 0.48)
    if t < 98.0:
        dt = t - 88.4
        # image fixe (Seedance a refusé ce plan) : poussée lente vers la scène, puis sauts serrés sur les applaudissements
        if t < 91.6:
            f = cadre("theatre", 1.12 + 0.18 * lisse(dt / 3.2), 0.5, 0.42)
        else:
            k = int((t - 91.6) / (60 / 112 * 2))
            cad = [(1.55, 0.5, 0.38), (1.25, 0.5, 0.55), (2.0, 0.5, 0.33), (1.35, 0.5, 0.48), (1.7, 0.5, 0.4), (1.15, 0.5, 0.5)][min(k, 5)]
            f = cadre("theatre", cad[0] + 0.02 * ((t - 91.6) % 1.07), cad[1], cad[2])
            f = flash(f, t, 91.6 + k * 60 / 112 * 2, 0.18, 0.12)
        p = 0.5 + 0.5 * math.sin(2 * math.pi * 0.7 * t)
        return lueur(etalonner(f, chaud=0.25 * p, expo=1 + 0.06 * p), t, 93.0, 97.5, force=0.22)
    # ---------------- 60 ans
    if t < 98.2:
        return np.zeros((H, W, 3), np.float32) + 4
    if t < CH60.t0:
        dt = t - 98.2
        return etalonner(cadre("vieux", 1.3 - 0.18 * lisse(dt / 4.2), 0.42, 0.55), froid=0.25)
    if t < CH60.tc + D_TRAV:
        f, rect = scene_choix(CH60, t, etalonner(cadre("vieux", 1.12, 0.42, 0.55), froid=0.25))
        if t >= CH60.tc + 0.12:
            f = traverser(f, rect, video("vieux", 0.0, 6.0), (t - CH60.tc - 0.12) / (D_TRAV - 0.12))
        return f
    if t < 112.3:                                                   # « Il continue. » (Seedance) ; la question
        dt = t - (CH60.tc + D_TRAV)
        f = video("vieux", dt, 6.4)
        return f
    dt = t - 112.3                                                  # le bureau au crépuscule
    return etalonner(cadre("bureau", 1.12 - 0.08 * lisse(dt / 2.7), 0.5, 0.5), chaud=0.4, expo=0.85)


# les impacts : (instant, force de la secousse, flash)
IMPACTS = [(0.0, 16, 0.5), (31.55, 18, 0.45), (51.75, 10, 0.35), (98.2, 18, 0.45),
           (CH15.tc, 6, 0.0), (CH24.tc, 6, 0.0), (CH26.tc, 6, 0.0), (CH60.tc, 6, 0.0)]


def image(n):
    t = n / FPS
    f = plan(t)
    dx = dy = 0.0
    for t0, force, fl in IMPACTS:
        a, b = secousse(t, t0, force)
        dx, dy = dx + a, dy + b
        if fl:
            f = flash(f, t, t0, fl)
    if abs(dx) + abs(dy) > 0.5:
        f = decaler(f, dx, dy)
    f = fil_dette(f, t)
    # les phrases et les chiffres à l'écran
    f = phrase_ecran(f, t, "Tuberculose.", CH24.tc + D_TRAV + 0.1, POS["guerit"] - 0.1, y=H / 2 - 40)
    f = gros_chiffre(f, t, "32", mot("32", 0.15), 51.4, 610, 250)
    f = gros_chiffre(f, t, "49", mot("49", 0.15), 51.4, 930, 250)
    f = gros_chiffre(f, t, "49 ans", mot("maries", 0.55), 61.0, W / 2, 250)
    f = phrase_ecran(f, t, "Au rappel, les applaudissements n'en finissaient plus.", 93.4, 97.6)
    f = age(f, t)
    f = f * VIGNETTE
    f += np.random.default_rng(n).normal(0, 2.2, f.shape).astype(np.float32)
    if t > DUREE - 0.5:
        f *= 1 - lisse((t - (DUREE - 0.5)) / 0.5)
    return f


SON_SEUL = os.environ.get("SON_SEUL") == "1"
if __name__ == "__main__" and not SON_SEUL:
    if "--test" in sys.argv:
        temps = os.environ.get("TEMPS")
        temps = [float(x) for x in temps.split(",")] if temps else [0.1, 0.4, 1.2, 3.0, 7.2, 10.0, 13.2, 17.0, 18.8, 23.0, 27.0,
                                                                     31.8, 34.0, 40.0, 42.5, 46.0, 50.5, 54.0, 57.0, 59.5,
                                                                     62.0, 64.0, 66.0, 69.5, 71.5, 77.0, 82.0, 84.5, 87.0,
                                                                     91.0, 95.0, 98.6, 101.5, 104.0, 107.0, 111.0, 114.0]
        for t in temps:
            cv2.imwrite(os.path.join(sys.argv[-1], f"s09_{t:06.2f}.jpg"), np.clip(image(int(round(t * FPS))), 0, 255).astype(np.uint8))
        sys.exit()
    os.makedirs(OUT, exist_ok=True)
    ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", os.path.join(OUT, "S09_image.mp4")],
                           stdin=subprocess.PIPE)
    for n in range(N):
        ecr.stdin.write(np.clip(image(n), 0, 255).astype(np.uint8).tobytes())
    ecr.stdin.close()
    ecr.wait()
    print("image :", DUREE, "s")

if __name__ != "__main__" or "--test" in sys.argv:
    raise SystemExit
# ---------------------------------------------------------------- le son
Ns = int(DUREE * SR)
ts = np.arange(Ns) / SR
mix = np.zeros((Ns, 2))


def db(x):
    return 10 ** (x / 20)


def fondu(n, e=0.0, s=0.0):
    f = np.ones(n)
    ne, ns_ = int(e * SR), int(s * SR)
    if ne:
        f[:min(ne, n)] = np.linspace(0, 1, min(ne, n))
    if ns_:
        f[-min(ns_, n):] = np.linspace(1, 0, min(ns_, n))
    return f


def poser(son, t0, gain=1.0):
    j = int(t0 * SR)
    if j >= Ns or j + len(son) <= 0:
        return
    a, b = max(0, -j), min(len(son), Ns - j)
    mix[j + a:j + b] += son[a:b] * gain


def lire(nom, dossier=SONS):
    a = lire_audio(os.path.join(dossier, nom), mono=False).astype(np.float64)
    return a if a.ndim == 2 else np.stack([a, a], 1)


def stereo(nom, debut, dossier=SONS):
    return boucle(lire(nom, dossier)[int(debut * SR):int(debut * SR) + Ns + SR], Ns)


def env(t0, t1, e=0.25, s=0.3):
    return np.clip((ts - t0) / max(e, 1e-3), 0, 1) * np.clip((t1 - ts) / max(s, 1e-3), 0, 1)


def crete(a):
    return int(np.argmax(np.abs(a).mean(1)))


def extrait(a, autour, avant, apres):
    j = crete(a) if autour is None else int(autour * SR)
    s = a[max(0, j - int(avant * SR)):j + int(apres * SR)]
    return s * fondu(len(s), 0.004, min(0.3, apres * 0.6))[:, None]


# la musique (Suhana, Epidemic Sound) : trois passages, coupés net
mus = lire("suhana.wav", os.path.join(M, "musique"))


def musique(t0, t1, m0, gain, e=0.8, s=0.25):
    seg = mus[int(m0 * SR):int(m0 * SR) + int((t1 - t0) * SR)]
    poser(seg * fondu(len(seg), e, s)[:, None], t0, db(gain))


musique(14.2, 31.0, 4.0, -22, e=2.5, s=0.05)        # la mer : l'intro, douce ; coupée net par la toux
musique(58.55, 73.75, 77.9, -15, e=0.05, s=0.08)    # le mariage et la grappe : la musique entre au clic ; coupe net
musique(83.0, 98.0, 28.0, -21, e=2.0, s=0.05)       # la confiance revenue, le théâtre ; coupée net à 60 ans
# les ambiances
mix += stereo("barque_bois_vagues.wav", 10.0) * (db(-22) * env(13.3, 31.0, 0.6, 0.05))[:, None]
mix += stereo("vagues_plage.wav", 5.0) * (db(-24) * env(13.3, 31.0, 0.6, 0.05))[:, None]
mix += stereo("bourdonnement_lumiere.wav", 3.0) * (db(-28) * env(31.6, 45.4, 0.4, 0.6))[:, None]
mix += stereo("soir_rural.wav", 8.0) * (db(-26) * env(51.75, 58.6, 0.5, 0.3))[:, None]
mix += stereo("espace_drone.wav", 20.0) * (db(-27) * (env(36.0, 41.7, 0.8, 0.1) + env(74.0, 83.5, 0.3, 1.5)))[:, None]
mix += stereo("vagues_plage.wav", 40.0) * (db(-21) * env(98.3, 112.4, 1.0, 0.8))[:, None]
mix += stereo("espace_drone.wav", 70.0) * (db(-29) * env(102.4, 105.5, 0.6, 0.1))[:, None]
# les claquements de l'âge : un coup grave et un souffle
tb = np.arange(int(0.9 * SR)) / SR
coup = np.sin(2 * np.pi * (62 * tb - 30 * tb * tb)) * np.exp(-tb / 0.18) * 0.5
wz = lire("whoosh_zoom.wav")
for t0 in (0.0, 31.55, 51.75, 98.2):
    poser(np.stack([coup, coup], 1), t0, db(-6))
    poser(extrait(wz, None, 0.35, 0.25), t0 - 0.35, db(-18))
# les coups de fouet sur « la mer, les bêtes, la terre »
wa = lire("whoosh_air.wav")
for tc in (mot("15b", 0.36), mot("15b", 0.58), mot("15b", 0.80)):
    poser(extrait(wa, None, 0.15, 0.2), tc - 0.15, db(-17))
# les choix : les cartes arrivent (petit souffle), le curseur hésite (tics), le clic, la traversée
tic = lire("tic_doux.wav")
un_tic = extrait(tic[:SR], None, 0.005, 0.06)
cl = lire("souris_clics.wav")
un_clic = extrait(cl[:2 * SR], None, 0.01, 0.12)
for c in (CH15, CH24, CH26, CH60):
    poser(extrait(wa, None, 0.2, 0.25), c.t0 - 0.05, db(-24))
    for ti, _ in c.hesite:
        poser(un_tic, ti, db(-24))
    poser(un_clic, c.tc, db(-10))
    poser(extrait(wz, None, 0.45, 0.35), c.tc + 0.12 + D_TRAV * 0.6 - 0.45, db(-15))
# la toux : à 24 ans (et une deuxième, plus loin)
tx = lire("toux_homme.wav")
poser(tx[:int(2.4 * SR)] * fondu(int(2.4 * SR), 0.01, 0.4)[:, None], 31.05, db(-9))
poser(tx[:int(1.6 * SR)] * fondu(int(1.6 * SR), 0.01, 0.4)[:, None], 34.4, db(-22))
# les frères : un souffle grave quand chacun s'efface
tw = np.arange(int(1.4 * SR)) / SR
souffle = np.sin(2 * np.pi * (98 * tw - 18 * tw * tw)) * np.exp(-tw / 0.5) * 0.1
for t0 in (mot("32", 0.5), mot("49", 0.5)):
    poser(np.stack([souffle, souffle], 1), t0, 1.0)
# le souvenir d'Usha : un rembobinage bref
poser(extrait(wz, None, 0.3, 0.1)[::-1], 64.75, db(-20))
# le théâtre : les applaudissements montent, puis durent (deux prises superposées) ; coupés net à 60 ans
ap1 = lire("applaudissements_salle.wav")
ap2 = lire("applaudissements_grands.wav")
poser(ap1[:int(7.0 * SR)] * fondu(int(7.0 * SR), 1.2, 0.05)[:, None], 91.0, db(-15))
poser(ap2[:int(5.0 * SR)] * fondu(int(5.0 * SR), 1.5, 0.03)[:, None], 93.0, db(-17))
mix[int(98.0 * SR):int(98.2 * SR)] *= 0.0
# un vrai silence avant les phrases-clés
for t_cle in (POS["ment"], POS["argent"], POS["question"]):
    mix *= (1 - 0.8 * np.clip(1 - np.abs(ts - (t_cle - 0.45)) / 0.6, 0, 1) ** 0.7)[:, None]
mix[int(73.75 * SR):int(74.1 * SR)] *= 0.0
# la voix
a_ = lire_audio(VOIX_F, mono=True).astype(np.float64)
actif = np.abs(a_) > 0.01
a_ *= db(-17.2 - 20 * np.log10(np.sqrt((a_[actif] ** 2).mean())))
voix = np.zeros(Ns)
for nom, (a, b) in P_.items():
    s_ = a_[int(a * SR):int(b * SR)] * fondu(int(b * SR) - int(a * SR), 0.01, 0.06)
    j = int(POS[nom] * SR)
    f_ = min(Ns, j + len(s_))
    voix[j:f_] += s_[:f_ - j]
env_voix = np.convolve(np.abs(voix) > 1e-3, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode="same")
mix *= (1 - 0.45 * np.clip(env_voix * 3, 0, 1))[:, None]
mix += voix[:, None] * db(-3.5)
mix *= fondu(Ns, 0.02, 0.5)[:, None]

GAIN = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
wav = os.path.join(OUT, "S09_son.wav")
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN))
final = os.path.join(OUT, "S09_v1.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, "S09_image.mp4"), "-i", wav, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", final], check=True)
print("écrit :", final)
