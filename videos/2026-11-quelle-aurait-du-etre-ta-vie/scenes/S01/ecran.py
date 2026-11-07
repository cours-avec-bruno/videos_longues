"""S01 · Remplace ce qu'affiche l'écran dans la marche animée par Higgsfield.

À l'écran : des timelines de vies simulées. Une ligne par vie, de la naissance (à gauche) à la mort,
avec ses étapes (école, travail, mariage, enfants). En bas, la vie en cours se dessine pendant le plan,
et le compteur des vies simulées avance au rythme des naissances dans le monde (≈ 4,3 par seconde).
Discret de loin (des lignes), lisible en arrivant (âges, pays, compteur). Aucun pourcentage.

Méthode :
  1. suivi de la fenêtre claire de l'écran d'origine (jamais masquée par la chaise), à rebours depuis la
     dernière image, bords ajustés par droites, coins lissés dans le temps ;
  2. la dalle entière s'en déduit (rapport mesuré sur la vidéo) ;
  3. l'interface est dessinée (PIL), projetée sur la dalle, et ne passe pas devant la chaise
     (masque d'occultation : là où l'image d'origine est sombre, c'est la chaise).

Usage (sur le PC) :
  python ecran.py --video ../../medias/S01/S01_marche_v2.mp4 --sortie ../../medias/S01/S01_marche_v3.mp4
Dépend de numpy, opencv-python-headless, pillow, ffmpeg.
"""
import argparse
import math
import os
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
PORTRAITS = [os.path.join(ICI, "..", "..", "medias", "S01", "portraits", f"portrait_{i}.png") for i in (1, 2)]
FOND_DEFAUT, CLAIR_DEFAUT = (38, 47, 60), (167, 176, 188)   # relevés sur l'écran de S01


def arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", help="vidéo dont on remplace l'écran")
    ap.add_argument("--sortie", help="vidéo (ou image PNG avec --image)")
    ap.add_argument("--controle", default="", help="dossier où écrire quelques images de contrôle")
    ap.add_argument("--portraits", default="", help="dossier des deux portraits robots (portrait_1.png, portrait_2.png)")
    ap.add_argument("--t0", type=float, default=0.0, help="temps de l'interface au début du plan (s) : continuité entre plans")
    ap.add_argument("--duree-vie", type=float, default=0.0, help="durée (s) pendant laquelle la vie en cours se dessine ; 0 = durée du plan")
    ap.add_argument("--scenario", default=None, help="interactions de l'opérateur à l'écran (ex. s02)")
    ap.add_argument("--couleurs-s01", action="store_true", help="garde les couleurs de S01 (continuité entre plans)")
    ap.add_argument("--image", type=float, default=None, help="exporte seulement l'interface au temps donné (PNG), aux couleurs de S01")
    return ap.parse_args()


W, H = 1920, 1080
FPS = 24
# dalle exprimée dans le repère de la fenêtre claire d'origine (mesuré sur les images 160 à 239)
DALLE = np.float32([[-0.335, -0.315], [1.325, -0.315], [1.325, 1.365], [-0.335, 1.365]])


def lire_gris(video):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W)


# ---------------------------------------------------------------- 1. suivi de la fenêtre claire
def droite(xs, ys):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    a, b = np.polyfit(xs, ys, 1)
    r = ys - (a * xs + b)
    ok = np.abs(r) < max(1.0, 2.5 * np.median(np.abs(r)))
    return np.polyfit(xs[ok], ys[ok], 1)


def inter(h, v):
    a, b = h; c, d = v
    y = (a * d + b) / (1 - a * c)
    return c * y + d, y


def bords(sub, frac=0.15):
    cols = np.where(sub.any(0))[0]; rows = np.where(sub.any(1))[0]
    cA, cB, rA, rB = cols[0], cols[-1], rows[0], rows[-1]
    xs = np.arange(int(cA + frac * (cB - cA)), int(cB - frac * (cB - cA)) + 1)
    ys = np.arange(int(rA + frac * (rB - rA)), int(rB - frac * (rB - rA)) + 1)
    top = [sub[:, c].argmax() - 0.5 for c in xs]
    bot = [sub.shape[0] - sub[::-1, c].argmax() - 0.5 for c in xs]
    lef = [sub[r, :].argmax() - 0.5 for r in ys]
    rig = [sub.shape[1] - sub[r, ::-1].argmax() - 0.5 for r in ys]
    hT, hB, vL, vR = droite(xs, top), droite(xs, bot), droite(ys, lef), droite(ys, rig)
    return np.array([inter(hT, vL), inter(hT, vR), inter(hB, vR), inter(hB, vL)])


def lisse(v, f=13, p=2):
    o = np.empty_like(v); r = f // 2
    for i in range(len(v)):
        a, b = max(0, i - r), min(len(v), i + r + 1)
        t = np.arange(a, b) - i
        o[i] = np.polyval(np.polyfit(t, v[a:b], min(p, b - a - 1)), 0)
    return o


def bords_coupe_haut(sub, rapport, frac=0.15):
    """La fenêtre sort par le haut de l'image : bas, gauche et droite mesurés, haut déduit du rapport l/h."""
    cols = np.where(sub.any(0))[0]; rows = np.where(sub.any(1))[0]
    cA, cB, rB = cols[0], cols[-1], rows[-1]
    xs = np.arange(int(cA + frac * (cB - cA)), int(cB - frac * (cB - cA)) + 1)
    ys = np.arange(max(0, rB - int(0.8 * (rB - rows[0]))), rB - int(0.1 * (rB - rows[0])) + 1)
    bot = [sub.shape[0] - sub[::-1, c].argmax() - 0.5 for c in xs]
    lef = [sub[r, :].argmax() - 0.5 for r in ys if sub[r].any()]
    rig = [sub.shape[1] - sub[r, ::-1].argmax() - 0.5 for r in ys if sub[r].any()]
    ys2 = [r for r in ys if sub[r].any()]
    hB, vL, vR = droite(xs, bot), droite(ys2, lef), droite(ys2, rig)
    bl, br = np.array(inter(hB, vL)), np.array(inter(hB, vR))
    h = np.linalg.norm(br - bl) / rapport
    n = np.array([hB[0], -1.0]); n /= np.linalg.norm(n)           # normale vers le haut de l'image
    return np.array([bl + n * h, br + n * h, br, bl])


def suivre(G):
    """Renvoie, pour chaque image, les 4 coins de la fenêtre claire, ou None quand l'écran est hors champ."""
    prev, rapport, win = None, None, []
    for k in range(len(G) - 1, -1, -1):               # à rebours : la fin, où l'écran est grand, sert d'amorce
        g = cv2.GaussianBlur(G[k], (3, 3), 0).astype(np.float32)
        if prev is None:
            y0, y1, x0, x1 = 0, int(H * 0.6), 0, W
        else:
            c = prev.mean(0); s = np.ptp(prev[:, 0]) * 1.2 + 20
            y0, y1 = max(0, int(c[1] - s)), min(H, int(c[1] + s))
            x0, x1 = max(0, int(c[0] - s)), min(W, int(c[0] + s))
        q = None
        r = g[y0:y1, x0:x1]
        if r.size and np.percentile(r, 99.5) > 60:
            m = (r > 0.6 * np.percentile(r, 99.5)).astype(np.uint8)
            ksz = max(3, int(0.25 * (np.ptp(prev[:, 1]) if prev is not None else 20)) | 1)
            m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((ksz, 3), np.uint8))
            n, lab, st, cen = cv2.connectedComponentsWithStats(m)
            if n > 1:
                best = max(range(1, n), key=lambda i: st[i, 4])
                bx, by, bw, bh, ba = st[best]
                haut = by + y0 <= 1
                plausible = ba > 150 and bh > 4
                if prev is not None:   # continuité : pas de saut vers un autre objet clair
                    plausible &= np.hypot(*(cen[best] + [x0, y0] - prev.mean(0))) < 0.6 * np.ptp(prev[:, 0]) + 30
                if plausible and not haut and 1.35 < bw / bh < 2.4:
                    q = bords(lab == best) + [x0, y0]
                    rapport = np.ptp(q[:, 0]) / np.ptp(q[:, 1])
                elif plausible and haut and rapport and bh > 12:
                    q = bords_coupe_haut(lab == best, rapport) + [x0, y0]
        win.append(q)
        prev = q if q is not None else None
    win = win[::-1]
    # lissage par tronçons continus
    ok = np.array([w is not None for w in win])
    A_ = np.array([w if w is not None else np.zeros((4, 2)) for w in win], float)
    k = 0
    while k < len(win):
        if not ok[k]:
            k += 1; continue
        f = k
        while f < len(win) and ok[f]:
            f += 1
        if f - k >= 3:
            for j in range(4):
                for d in range(2):
                    A_[k:f, j, d] = lisse(A_[k:f, j, d])
        k = f
    # dans les trous (écran sorti du champ), on prolonge le mouvement depuis les bords du trou, sur 14 images au plus :
    # la fenêtre d'origine encore visible en bord d'image est ainsi recouverte elle aussi
    res = [A_[i] if ok[i] else None for i in range(len(win))]
    idx = np.where(ok)[0]
    for i in range(len(win)):
        if ok[i] or not len(idx):
            continue
        avant = idx[idx < i]; apres = idx[idx > i]
        cands = []
        if len(avant) and i - avant[-1] <= 14:
            cands.append((i - avant[-1], avant[-6:]))
        if len(apres) and apres[0] - i <= 14:
            cands.append((apres[0] - i, apres[:6]))
        if not cands:
            continue
        _, pts = min(cands, key=lambda c: c[0])
        if len(pts) < 3:
            continue
        q = np.zeros((4, 2))
        for j in range(4):
            for d in range(2):
                q[j, d] = np.polyval(np.polyfit(pts, A_[pts, j, d], 1), i)
        res[i] = q
    return res


# ---------------------------------------------------------------- 2. l'interface
UW, UH = 1730, 1000          # même rapport que la dalle
SS = 2                       # suréchantillonnage du dessin
FONTS = "C:/Windows/Fonts/"


def police(nom, taille):
    try:
        return ImageFont.truetype(FONTS + nom, taille * SS)
    except OSError:
        return ImageFont.load_default()


def teinte(base, f):
    return tuple(int(c * f) for c in base)


class Interface:
    """Les couleurs sont prises sur l'écran d'origine, pour garder la même lumière dans la pièce."""

    def __init__(self, fond, clair, graine=12, scenario=None):
        self.fond, self.clair = fond, clair
        self.scenario = scenario
        self.f_titre = police("segoeuisl.ttf", 22)
        self.f_petit = police("consola.ttf", 17)
        self.f_mini = police("consola.ttf", 14)
        self.X0, self.X1 = 250, 1180           # âge 0 et âge 100 (à droite : la colonne des fiches)
        self.CX = 1290                         # colonne des deux fiches avec portrait robot
        self.Y0, self.PAS = 196, 47            # première ligne, écart entre lignes
        self.NB = 16                           # 15 vies terminées + la vie en cours
        rng = np.random.default_rng(graine)
        pays = ["IND", "CHN", "NGA", "PAK", "IDN", "ETH", "USA", "BGD", "COD", "BRA", "IND", "EGY", "PHL", "IND", "MEX"]
        self.vies = []
        for i in range(self.NB):
            mort = float(np.clip(rng.normal(72, 13), 30, 97))
            if i in (4, 11):
                mort = float(rng.uniform(1, 9))     # quelques vies très courtes
            ev = []
            ecole = rng.random() < 0.8
            fin_etudes = rng.uniform(10, 24) if ecole else 0
            if ecole:
                ev.append(("e", 6.0))
            travail = rng.uniform(max(11, fin_etudes), 26)
            ev.append(("t", travail))
            if rng.random() < 0.85:
                ev.append(("m", rng.uniform(17, 31)))
            for _ in range(int(rng.integers(0, 5))):
                ev.append(("n", rng.uniform(19, 41)))
            ev = [(c, a) for c, a in ev if a < mort]
            self.vies.append(dict(pays=pays[i % len(pays)], mort=mort, fin=min(fin_etudes, mort), ev=ev,
                                  num=1284093 - (self.NB - 1 - i) * int(rng.integers(1, 4))))
        self.vies[-1]["pays"] = "NGA"          # la vie en cours : celle de la jeune femme du portrait 2
        self.portraits = [self._portrait(p) for p in PORTRAITS]
        self.statique = self._statique()

    def _portrait(self, chemin):
        """Portrait robot passé aux couleurs de l'écran : gris → du fond sombre au clair de l'interface."""
        g = Image.open(chemin).convert("L")
        w, h = 250 * SS, 320 * SS
        r = max(w / g.width, h / g.height)
        g = g.resize((int(g.width * r), int(g.height * r)), Image.LANCZOS)
        g = g.crop(((g.width - w) // 2, 0, (g.width - w) // 2 + w, h))
        a = np.asarray(g, np.float32)[:, :, None] / 255.0
        bas, haut = np.array(teinte(self.fond, 0.75), np.float32), np.array(teinte(self.clair, 0.92), np.float32)
        return Image.fromarray((bas + (haut - bas) * a ** 1.15).astype(np.uint8))

    def _fiche(self, d, im, y, portrait, lignes, vif):
        x = self.CX * SS
        cadre = teinte(self.fond, 1.22 if vif else 1.1)
        d.rectangle([x - 20 * SS, y - 20 * SS, (UW - 40) * SS, y + 410 * SS], fill=cadre)
        im.paste(portrait, (x + 55 * SS, y))
        d.rectangle([x + 55 * SS, y, x + 305 * SS, y + 320 * SS], outline=teinte(self.clair, 0.55), width=2 * SS)
        for j, (txt, f, k) in enumerate(lignes):
            d.text((x + 55 * SS, y + (334 + 24 * j) * SS), txt, font=f, fill=teinte(self.clair, k))

    def x(self, age):
        return (self.X0 + (self.X1 - self.X0) * age / 100.0) * SS

    def _vie(self, d, y, v, age_max, couleur, epais, etiquette=True):
        c_ligne = couleur
        c_etude = teinte(couleur, 1.25)
        x0, xm = self.x(0), self.x(min(v["mort"], age_max))
        d.line([(x0, y), (xm, y)], fill=c_ligne, width=epais * SS)
        if v["fin"] > 0:
            d.line([(self.x(6), y), (self.x(min(v["fin"], age_max)), y)], fill=c_etude, width=(epais + 2) * SS)
        r = 5 * SS
        d.ellipse([x0 - r, y - r, x0 + r, y + r], outline=c_ligne, width=2 * SS)
        for code, a in v["ev"]:
            if a > age_max:
                continue
            xe = self.x(a)
            if code == "n":
                rr = 3.5 * SS; d.ellipse([xe - rr, y - rr, xe + rr, y + rr], fill=teinte(couleur, 1.3))
            elif code == "m":
                rr = 5 * SS; d.ellipse([xe - rr, y - rr, xe + rr, y + rr], outline=teinte(couleur, 1.3), width=2 * SS)
            elif code == "t":
                d.line([(xe, y - 8 * SS), (xe, y + 8 * SS)], fill=teinte(couleur, 1.2), width=2 * SS)
        if etiquette:
            d.text((60 * SS, y - 9 * SS), f'{v["pays"]}  {v["num"]:>9,}'.replace(",", " "), font=self.f_mini,
                   fill=teinte(couleur, 0.9))
        if age_max >= v["mort"]:
            d.line([(xm, y - 9 * SS), (xm, y + 9 * SS)], fill=c_ligne, width=2 * SS)
            d.text((xm + 10 * SS, y - 9 * SS), f'{int(v["mort"])}', font=self.f_mini, fill=teinte(couleur, 0.8))

    def _statique(self):
        im = Image.new("RGB", (UW * SS, UH * SS), self.fond)
        d = ImageDraw.Draw(im)
        f, c = self.fond, self.clair
        bande = teinte(f, 0.7)
        d.rectangle([0, 0, UW * SS, 74 * SS], fill=bande)
        d.text((60 * SS, 22 * SS), "Simulation · naissances 2026", font=self.f_titre, fill=teinte(c, 0.85))
        # axe des âges
        ya = 138 * SS
        for a in range(0, 101, 10):
            xa = self.x(a)
            d.line([(xa, ya), (xa, (self.Y0 + self.PAS * (self.NB - 1) + 22) * SS)], fill=teinte(f, 1.22), width=1 * SS)
            d.text((xa - 8 * SS, ya - 26 * SS), str(a), font=self.f_mini, fill=teinte(c, 0.6))
        d.text(((self.X1 + 18) * SS, ya - 26 * SS), "ans", font=self.f_mini, fill=teinte(c, 0.6))
        # légende discrète en bas
        yl = (UH - 46) * SS
        d.text((60 * SS, yl), "école   travail   mariage   enfant", font=self.f_mini, fill=teinte(c, 0.5))
        for i, v in enumerate(self.vies[:-1]):
            y = (self.Y0 + i * self.PAS) * SS
            self._vie(d, y, v, 200, teinte(c, 0.78 if i == 0 else 0.62), 2)
        # fiche 1 : une vie terminée (la première ligne), avec son portrait robot
        v = self.vies[0]
        self._fiche(d, im, 110 * SS, self.portraits[0], [
            (f'{v["pays"]}  ·  homme', self.f_petit, 0.9),
            (f'vie {v["num"]:,}'.replace(",", " "), self.f_mini, 0.6),
            (f'{int(v["mort"])} ans', self.f_mini, 0.6)], vif=False)
        return im

    # ------------------------------------------------------------ l'opérateur utilise le logiciel (S02)
    # temps de l'interface (s) : 0 = début de S01. S02-P02 couvre 16 à 25.
    T_CLIC = 22.5          # clic sur « nouvelle vie »
    BOUTON = (470, 18, 690, 58)
    PARCOURS = [           # (temps, x, y) du pointeur, en pixels de l'interface
        (16.0, 1060, 820), (16.7, 760, 290), (18.1, 790, 292), (18.7, 830, 478), (20.0, 860, 480),
        (20.5, 640, 619), (21.4, 655, 622), (22.2, 575, 40), (22.5, 578, 41), (23.2, 420, 905), (25.5, 450, 900)]
    SURVOLS = [(16.7, 18.4, 2), (18.7, 20.3, 6), (20.5, 21.6, 9)]   # (début, fin, ligne survolée)

    def _pointeur(self, t):
        P = self.PARCOURS
        if t <= P[0][0]:
            return P[0][1:]
        for (t0, x0, y0), (t1, x1, y1) in zip(P, P[1:]):
            if t0 <= t <= t1:
                u = (t - t0) / (t1 - t0); u = u * u * (3 - 2 * u)
                return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        return P[-1][1:]

    def _dessiner_pointeur(self, d, x, y, appuye=False):
        k = 1.15
        pts = [(0, 0), (0, 22), (5.5, 17), (9.5, 26), (13, 24.5), (9, 16), (16, 16)]
        poly = [((x + px * k) * SS, (y + py * k) * SS) for px, py in pts]
        d.polygon(poly, fill=teinte(self.clair, 1.25 if not appuye else 1.05), outline=teinte(self.fond, 0.4))

    def _infobulle(self, d, x, y, v, opacite):
        enfants = sum(1 for c_, _ in v["ev"] if c_ == "n")
        marie = any(c_ == "m" for c_, _ in v["ev"])
        lignes = [v["pays"] + "  ·  " + str(int(v["mort"])) + " ans",
                  ("école · " if v["fin"] > 0 else "") + "travail" + (" · mariage" if marie else ""),
                  (str(enfants) + " enfant" + ("s" if enfants > 1 else "")) if enfants else "pas d" + chr(39) + "enfant"]
        w, h = 300, 92
        x0, y0 = x + 24, y - h - 10
        d.rectangle([x0 * SS, y0 * SS, (x0 + w) * SS, (y0 + h) * SS], fill=teinte(self.fond, 0.62),
                    outline=teinte(self.clair, 0.45 * opacite + 0.1))
        for j, txt in enumerate(lignes):
            d.text(((x0 + 14) * SS, (y0 + 10 + 25 * j) * SS), txt, font=self.f_mini if j else self.f_petit,
                   fill=teinte(self.clair, (0.95 if j == 0 else 0.7) * opacite + 0.05))

    def _fiche_attente(self, d, y):
        """Fiche vide : la prochaine vie n'a encore ni visage ni pays."""
        x = self.CX * SS
        d.rectangle([x - 20 * SS, y - 20 * SS, (UW - 40) * SS, y + 410 * SS], fill=teinte(self.fond, 1.22))
        X0, Y0 = x + 55 * SS, y
        d.rectangle([X0, Y0, X0 + 250 * SS, Y0 + 320 * SS], fill=teinte(self.fond, 0.85), outline=teinte(self.clair, 0.45), width=2 * SS)
        gris = teinte(self.fond, 1.6)
        cx = X0 + 125 * SS
        d.ellipse([cx - 58 * SS, Y0 + 62 * SS, cx + 58 * SS, Y0 + 192 * SS], fill=gris)
        d.pieslice([cx - 118 * SS, Y0 + 205 * SS, cx + 118 * SS, Y0 + 420 * SS], 180, 360, fill=gris)
        d.rectangle([X0, Y0 + 320 * SS, X0 + 250 * SS, Y0 + 330 * SS], fill=teinte(self.fond, 1.22))
        d.text((cx - 16 * SS, Y0 + 92 * SS), "?", font=police("segoeuisl.ttf", 54), fill=teinte(self.clair, 0.85))
        for j, (txt, f, k) in enumerate([("en attente", self.f_petit, 0.95), ("naissance  —", self.f_mini, 0.6), ("pays  —", self.f_mini, 0.6)]):
            d.text((X0, Y0 + (334 + 24 * j) * SS), txt, font=f, fill=teinte(self.clair, k))

    # ------------------------------------------------------------ S03 : la fenêtre « nouvelle vie » (temps S03 = t - 44)
    T03 = 44.0
    PARCOURS_S03 = [(0.0, 420, 905), (0.35, 440, 908), (1.4, 714, 256), (1.6, 714, 256), (3.3, 714, 376), (3.6, 714, 376),
                    (6.0, 760, 470), (8.9, 905, 603), (9.4, 905, 603), (12.6, 930, 640), (13.6, 1150, 772), (16.0, 1158, 776)]
    CLICS_S03 = [0.4, 1.5, 3.5, 9.4]
    CLIC_NAITRE = 14.6
    FRAPPES_S03 = [10.7, 10.9, 11.08, 11.25, 11.42, 11.6]
    ENTREE_S03 = 12.5

    def _pointeur_s03(self, tau):
        P = self.PARCOURS_S03
        for (t0, x0, y0), (t1, x1, y1) in zip(P, P[1:]):
            if t0 <= tau <= t1:
                u = (tau - t0) / (t1 - t0); u = u * u * (3 - 2 * u)
                return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        return P[-1][1:] if tau > P[-1][0] else P[0][1:]

    def _fenetre_s03(self, im, d, tau):
        c, f = self.clair, self.fond
        if tau < self.CLICS_S03[0]:
            return
        ap = min(1.0, (tau - self.CLICS_S03[0]) / 0.25)
        voile = Image.new("RGB", im.size, teinte(f, 0.5))
        im.paste(Image.blend(im, voile, 0.55 * ap))
        d = ImageDraw.Draw(im)
        X0, Y0, X1, Y1 = 430, 150, 1300, 840
        d.rectangle([X0 * SS, Y0 * SS, X1 * SS, Y1 * SS], fill=teinte(f, 1.25), outline=teinte(c, 0.5), width=2 * SS)
        d.text(((X0 + 40) * SS, (Y0 + 28) * SS), "Nouvelle vie", font=self.f_titre, fill=teinte(c, 0.95))
        d.line([((X0 + 40) * SS, (Y0 + 72) * SS), ((X1 - 40) * SS, (Y0 + 72) * SS)], fill=teinte(c, 0.3), width=SS)

        def radio(x, y, txt, choisi):
            r = 11 * SS
            d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], outline=teinte(c, 0.8), width=2 * SS)
            if choisi:
                r2 = 6 * SS
                d.ellipse([x * SS - r2, y * SS - r2, x * SS + r2, y * SS + r2], fill=teinte(c, 1.1))
            d.text(((x + 24) * SS, (y - 11) * SS), txt, font=self.f_petit, fill=teinte(c, 1.0 if choisi else 0.65))

        d.text(((X0 + 40) * SS, 250 * SS), "Le monde", font=self.f_petit, fill=teinte(c, 0.75))
        radio(712, 262, "le monde d" + chr(39) + "aujourd" + chr(39) + "hui", tau >= self.CLICS_S03[1])
        radio(712, 302, "le monde de 1950", False)
        d.text(((X0 + 40) * SS, 370 * SS), "Durée", font=self.f_petit, fill=teinte(c, 0.75))
        radio(712, 382, "une vie entière", tau >= self.CLICS_S03[2])
        radio(712, 422, "jusqu" + chr(39) + "à 18 ans", False)
        d.text(((X0 + 40) * SS, 480 * SS), "Lieu de naissance", font=self.f_petit, fill=teinte(c, 0.75))
        d.text((700 * SS, 480 * SS), "tiré au sort, comme les naissances", font=self.f_petit, fill=teinte(c, 0.6))
        d.text((700 * SS, 506 * SS), "dans le monde réel", font=self.f_petit, fill=teinte(c, 0.6))
        d.text(((X0 + 40) * SS, 585 * SS), "Et vous,", font=self.f_petit, fill=teinte(c, 0.75))
        d.text(((X0 + 40) * SS, 610 * SS), "où êtes-vous né ?", font=self.f_petit, fill=teinte(c, 0.75))
        d.text(((X0 + 40) * SS, 640 * SS), "pour comparer à la fin", font=self.f_mini, fill=teinte(c, 0.5))
        actif = tau >= self.CLICS_S03[3]
        d.rectangle([700 * SS, 580 * SS, 1240 * SS, 630 * SS], fill=teinte(f, 0.8),
                    outline=teinte(c, 0.85 if actif else 0.4), width=2 * SS)
        n = sum(1 for x in self.FRAPPES_S03 if tau >= x)
        texte = "France"[:n]
        d.text((716 * SS, 591 * SS), texte, font=self.f_petit, fill=teinte(c, 1.05))
        if actif and tau < self.ENTREE_S03 and int(tau * 2.2) % 2 == 0:   # curseur de saisie qui clignote
            xc = 716 * SS + d.textlength(texte, font=self.f_petit) + 3 * SS
            d.line([(xc, 588 * SS), (xc, 622 * SS)], fill=teinte(c, 1.0), width=2 * SS)
        if n == 6 and tau < self.ENTREE_S03 + 0.15:                        # la suggestion
            d.rectangle([700 * SS, 632 * SS, 1240 * SS, 676 * SS], fill=teinte(f, 1.5), outline=teinte(c, 0.5), width=SS)
            d.text((716 * SS, 641 * SS), "France", font=self.f_petit, fill=teinte(c, 1.1))
        if tau >= self.ENTREE_S03:
            d.text((1205 * SS, 590 * SS), "✓", font=police("seguisym.ttf", 22), fill=teinte(c, 1.1))
        survol = tau >= 13.5
        presse = self.CLIC_NAITRE <= tau < self.CLIC_NAITRE + 0.25
        d.rectangle([1060 * SS, 742 * SS, 1240 * SS, 800 * SS], fill=teinte(f, 2.4 if presse else (1.7 if survol else 1.35)),
                    outline=teinte(c, 0.95 if survol else 0.6), width=2 * SS)
        tw = d.textlength("Naître", font=self.f_titre)
        d.text(((1150 * SS) - tw / 2, 755 * SS), "Naître", font=self.f_titre, fill=teinte(c, 1.1 if survol else 0.85))
        px, py = self._pointeur_s03(tau)
        appuye = any(x <= tau < x + 0.2 for x in self.CLICS_S03 + [self.CLIC_NAITRE])
        self._dessiner_pointeur(d, px, py, appuye)

    def image(self, t, duree):
        im = self.statique.copy()
        d = ImageDraw.Draw(im)
        c = self.clair
        s02 = self.scenario in ("s02", "s03")
        # compteur des vies simulées : au rythme des naissances dans le monde
        n = 1284093 + int(t * 4.3)
        txt = f"vies simulées  {n:,}".replace(",", " ")
        tw = d.textlength(txt, font=self.f_petit)
        d.text(((UW - 60) * SS - tw, 26 * SS), txt, font=self.f_petit, fill=teinte(c, 0.9))
        if s02:   # le bouton « nouvelle vie », dans le bandeau
            bx0, by0, bx1, by1 = self.BOUTON
            presse = self.T_CLIC <= t < self.T_CLIC + 0.22
            survol = 21.9 <= t < self.T_CLIC + 0.6
            d.rectangle([bx0 * SS, by0 * SS, bx1 * SS, by1 * SS],
                        fill=teinte(self.fond, 1.5 if presse else (1.15 if survol else 0.85)),
                        outline=teinte(c, 0.7 if survol else 0.4), width=2 * SS)
            d.text(((bx0 + 22) * SS, (by0 + 8) * SS), "+  nouvelle vie", font=self.f_petit, fill=teinte(c, 1.0 if survol else 0.75))
            # lignes survolées par le pointeur
            for d0, d1, li in (self.SURVOLS if self.scenario == "s02" else []):
                if d0 <= t <= d1:
                    yl = (self.Y0 + li * self.PAS) * SS
                    d.rectangle([40 * SS, yl - 20 * SS, (self.CX - 50) * SS, yl + 20 * SS], fill=teinte(self.fond, 1.14))
                    self._vie(d, yl, self.vies[li], 200, teinte(c, 1.0), 3)
        nouvelle = s02 and t >= self.T_CLIC
        v = self.vies[-1]
        i = self.NB - 1
        y = (self.Y0 + i * self.PAS + 10) * SS
        d.rectangle([40 * SS, y - 22 * SS, (self.CX - 50) * SS, y + 22 * SS], fill=teinte(self.fond, 1.18))
        if not nouvelle:
            # la vie en cours se dessine
            p = min(1.0, max(0.0, (t - 0.4) / (duree - 1.6)))
            p = p * p * (3 - 2 * p) * 0.6 + p * 0.4
            age = v["mort"] * p
            self._vie(d, y, v, age, teinte(c, 1.0), 3, etiquette=False)
            d.text((60 * SS, y - 9 * SS), f"en cours  {n + 1:,}".replace(",", " "), font=self.f_mini, fill=teinte(c, 0.95))
            xc = self.x(age)
            if p < 1:
                r = 7 * SS
                d.ellipse([xc - r, y - r, xc + r, y + r], fill=teinte(c, 1.1))
            # fiche 2 : la vie en cours, son âge avance avec la ligne
            self._fiche(d, im, 540 * SS, self.portraits[1], [
                (f'{v["pays"]}  ·  femme', self.f_petit, 1.0),
                (f'en cours  {n + 1:,}'.replace(",", " "), self.f_mini, 0.75),
                (f'{int(age)} ans' if p < 1 else f'{int(v["mort"])} ans', self.f_mini, 0.75)], vif=True)
        else:
            # nouvelle vie : une ligne vide, un point de naissance qui attend, une fiche sans visage
            tn = t - self.T_CLIC
            apparition = min(1.0, tn / 0.35)
            d.text((60 * SS, y - 9 * SS), "en attente", font=self.f_mini, fill=teinte(c, 0.95 * apparition))
            x0 = self.x(0)
            pulse = 0.5 + 0.5 * math.sin(tn * 2 * math.pi / 1.4)
            r = (6 + 4 * pulse) * SS
            d.ellipse([x0 - r, y - r, x0 + r, y + r], outline=teinte(c, (0.6 + 0.5 * pulse) * apparition), width=2 * SS)
            for k in range(10):   # le chemin à venir, en pointillés
                xa = self.x(4 + k * 9.5)
                d.line([(xa, y), (xa + 18 * SS, y)], fill=teinte(c, 0.35 * apparition), width=1 * SS)
            self._fiche_attente(d, 540 * SS)
        # infobulles et pointeur par-dessus tout
        if self.scenario == "s02" and 16.0 <= t <= 25.5:
            px, py = self._pointeur(t)
            for d0, d1, li in self.SURVOLS:
                if d0 + 0.25 <= t <= d1:
                    self._infobulle(d, px, py, self.vies[li], min(1.0, (t - d0 - 0.25) / 0.2))
            self._dessiner_pointeur(d, px, py, appuye=self.T_CLIC <= t < self.T_CLIC + 0.22)
        if self.scenario == "s03":
            tau = t - self.T03
            if tau < self.CLICS_S03[0]:
                px, py = self._pointeur_s03(tau)
                self._dessiner_pointeur(d, px, py)
            self._fenetre_s03(im, d, tau)
        return im


# ---------------------------------------------------------------- 3. incrustation
def principal():
    global PORTRAITS
    if A.portraits:
        PORTRAITS = [f"{A.portraits}/portrait_1.png", f"{A.portraits}/portrait_2.png"]
    if A.image is not None:
        ui = Interface(FOND_DEFAUT, CLAIR_DEFAUT, scenario=A.scenario)
        ui.image(A.image, A.duree_vie or 10.0).resize((UW, UH), Image.LANCZOS).save(A.sortie)
        print("écrit :", A.sortie)
        return
    G = lire_gris(A.video)
    N = len(G)
    duree = N / FPS
    win = suivre(G)
    U = np.float32([[0, 0], [1, 0], [1, 1], [0, 1]])
    dalles = [cv2.perspectiveTransform(DALLE[None], cv2.getPerspectiveTransform(U, w.astype(np.float32)))[0]
              if w is not None else None for w in win]
    print("écran hors champ sur", sum(d is None for d in dalles), "images sur", N)
    derniere = max(i for i, w in enumerate(win) if w is not None)

    lec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", A.video, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                           stdout=subprocess.PIPE)
    ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                            A.sortie], stdin=subprocess.PIPE)
    ui = None
    rng = np.random.default_rng(3)
    for k in range(N):
        f = np.frombuffer(lec.stdout.read(W * H * 3), np.uint8).reshape(H, W, 3).astype(np.float32)
        if ui is None:
            # couleurs relevées sur l'écran d'origine, à la dernière image (la plus nette)
            fen = cv2.getPerspectiveTransform(U, win[derniere].astype(np.float32))
            fin =subprocess.run(["ffmpeg", "-v", "error", "-sseof", "-0.05", "-i", A.video, "-frames:v", "1",
                                  "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
            fin = np.frombuffer(fin, np.uint8).reshape(H, W, 3).astype(np.float32)
            Hf = fen
            def moy(u0, u1, v0, v1):
                pts = np.float32([[[u, v] for u in np.linspace(u0, u1, 12) for v in np.linspace(v0, v1, 12)]])
                p = cv2.perspectiveTransform(pts, Hf)[0].round().astype(int)
                return fin[p[:, 1], p[:, 0]]
            fond_bgr = np.median(moy(-0.25, -0.05, 0.2, 0.8), 0)
            fen_px = moy(0.05, 0.95, 0.05, 0.95)
            clair_bgr = np.percentile(fen_px, 90, axis=0)
            fond = tuple(int(x) for x in fond_bgr[::-1]); clair = tuple(int(x) for x in clair_bgr[::-1])
            if A.couleurs_s01:
                fond, clair = FOND_DEFAUT, CLAIR_DEFAUT
            print("couleurs : fond", fond, "clair", clair)
            ui = Interface(fond, clair, scenario=A.scenario)
        img = ui.image(A.t0 + k / FPS, A.duree_vie or duree)
        q = dalles[k]
        if q is None:                                   # écran hors champ : l'image passe telle quelle
            ecr.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
            continue
        larg = np.hypot(*(q[1] - q[0]))
        cible = int(min(UW * SS, max(160, larg * 1.6)))
        src = np.asarray(img.resize((cible, int(cible * UH / UW)), Image.LANCZOS))[:, :, ::-1].astype(np.float32)
        sh, sw = src.shape[:2]
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]]), q.astype(np.float32))
        proj = cv2.warpPerspective(src, M, (W, H), flags=cv2.INTER_LINEAR)
        masque = cv2.warpPerspective(np.ones((sh, sw), np.float32), M, (W, H), flags=cv2.INTER_LINEAR)
        # même douceur que l'image générée
        proj = cv2.GaussianBlur(proj, (0, 0), 0.55)
        # occultation : là où l'image d'origine est sombre dans la dalle, c'est la chaise
        g = cv2.GaussianBlur(G[k].astype(np.float32), (0, 0), 0.8)
        visible = np.clip((g - 22) / 10, 0, 1)
        a = (masque * visible)[:, :, None]
        # un léger halo, comme la lueur d'un écran
        halo = cv2.GaussianBlur(proj * a, (0, 0), max(2.0, larg / 60))
        sortie = f * (1 - a) + proj * a + 0.12 * halo * (1 - a)
        sortie += rng.normal(0, 1.2, sortie.shape).astype(np.float32) * a
        ecr.stdin.write(np.clip(sortie, 0, 255).astype(np.uint8).tobytes())
        if A.controle and k in (0, 60, 120, 180, 239, N - 1):
            cv2.imwrite(f"{A.controle}/ecran_{k:03d}.png", np.clip(sortie, 0, 255).astype(np.uint8))
            img.save(f"{A.controle}/interface.png") if k == N - 1 else None
    ecr.stdin.close(); ecr.wait(); lec.wait()
    print("écrit :", A.sortie)


if __name__ == "__main__":
    A = arguments()
    principal()
