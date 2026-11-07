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
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--video", required=True)
ap.add_argument("--sortie", required=True)
ap.add_argument("--controle", default="", help="dossier où écrire quelques images de contrôle")
A = ap.parse_args()

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


def suivre(G):
    prev, win = None, []
    for k in range(len(G) - 1, -1, -1):               # à rebours : la fin, où l'écran est grand, sert d'amorce
        g = cv2.GaussianBlur(G[k], (3, 3), 0).astype(np.float32)
        if prev is None:
            y0, y1, x0, x1 = 0, int(H * 0.6), 0, W
        else:
            c = prev.mean(0); s = np.ptp(prev[:, 0]) * 1.2 + 20
            y0, y1 = max(0, int(c[1] - s)), min(H, int(c[1] + s))
            x0, x1 = max(0, int(c[0] - s)), min(W, int(c[0] + s))
        r = g[y0:y1, x0:x1]
        m = (r > 0.6 * np.percentile(r, 99.5)).astype(np.uint8)
        ksz = max(3, int(0.25 * (np.ptp(prev[:, 1]) if prev is not None else 20)) | 1)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((ksz, 3), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(m)
        best = max(range(1, n), key=lambda i: st[i, 4])
        q = bords(lab == best) + [x0, y0]
        win.append(q); prev = q
    win = np.array(win[::-1])
    for j in range(4):
        for d in range(2):
            win[:, j, d] = lisse(win[:, j, d])
    return win


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

    def __init__(self, fond, clair, graine=12):
        self.fond, self.clair = fond, clair
        self.f_titre = police("segoeuisl.ttf", 22)
        self.f_petit = police("consola.ttf", 17)
        self.f_mini = police("consola.ttf", 14)
        self.X0, self.X1 = 250, 1640           # âge 0 et âge 100
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
        self.statique = self._statique()

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
            self._vie(d, y, v, 200, teinte(c, 0.62), 2)
        return im

    def image(self, t, duree):
        im = self.statique.copy()
        d = ImageDraw.Draw(im)
        c = self.clair
        # compteur des vies simulées : au rythme des naissances dans le monde
        n = 1284093 + int(t * 4.3)
        txt = f"vies simulées  {n:,}".replace(",", " ")
        tw = d.textlength(txt, font=self.f_petit)
        d.text(((UW - 60) * SS - tw, 26 * SS), txt, font=self.f_petit, fill=teinte(c, 0.9))
        # la vie en cours se dessine
        v = self.vies[-1]
        i = self.NB - 1
        y = (self.Y0 + i * self.PAS + 10) * SS
        d.rectangle([40 * SS, y - 22 * SS, (UW - 40) * SS, y + 22 * SS], fill=teinte(self.fond, 1.18))
        p = min(1.0, max(0.0, (t - 0.4) / (duree - 1.6)))
        p = p * p * (3 - 2 * p) * 0.6 + p * 0.4
        age = v["mort"] * p
        self._vie(d, y, v, age, teinte(c, 1.0), 3, etiquette=False)
        d.text((60 * SS, y - 9 * SS), f"en cours  {n + 1:,}".replace(",", " "), font=self.f_mini, fill=teinte(c, 0.95))
        xc = self.x(age)
        if p < 1:
            r = 7 * SS
            d.ellipse([xc - r, y - r, xc + r, y + r], fill=teinte(c, 1.1))
        return im


# ---------------------------------------------------------------- 3. incrustation
def principal():
    G = lire_gris(A.video)
    N = len(G)
    duree = N / FPS
    win = suivre(G)
    U = np.float32([[0, 0], [1, 0], [1, 1], [0, 1]])
    dalles = np.array([cv2.perspectiveTransform(DALLE[None], cv2.getPerspectiveTransform(U, w.astype(np.float32)))[0]
                       for w in win])

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
            fen = cv2.getPerspectiveTransform(U, win[-1].astype(np.float32))
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
            print("couleurs relevées : fond", fond, "clair", clair)
            ui = Interface(fond, clair)
        img = ui.image(k / FPS, duree)
        q = dalles[k]
        larg = np.hypot(*(q[1] - q[0]))
        cible = int(min(UW, max(160, larg * 1.6)))
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
        if A.controle and k in (0, 60, 120, 180, 239):
            cv2.imwrite(f"{A.controle}/ecran_{k:03d}.png", np.clip(sortie, 0, 255).astype(np.uint8))
            img.save(f"{A.controle}/interface.png") if k == 239 else None
    ecr.stdin.close(); ecr.wait(); lec.wait()
    print("écrit :", A.sortie)


principal()
