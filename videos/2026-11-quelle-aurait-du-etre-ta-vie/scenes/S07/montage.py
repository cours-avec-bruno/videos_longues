"""S07 · L'enfance (5 à 10 ans) : un montage qui mêle tableaux 3D (tableaux.py), vraies images (Pexels), motion design
et typographie, au rythme de la voix (S07_prise2). Demande de Bruno (08/11/2026) : « un mix de motion design, 3D,
images d'illustration, montage dynamique qui transmet des émotions ».

La grammaire : les tableaux de la simulation passent dans la fenêtre de l'interface (S06) ; les vraies images, les
coups et le deuil sortent de la fenêtre, en plein écran. Arc émotionnel : la fierté (l'école), le jeu (le choix),
le rêve (ingénieur), la honte (la baguette, la main qui ne se lève plus), l'inquiétude (la dette), le deuil.

Usage : python montage.py      ->  medias/S07/S07_v1.mp4     (SON_SEUL=1 : le son seul ; --test <dossier> : images fixes)
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
sys.path.insert(0, os.path.join(RACINE, "shared", "outils", "image"))
from pas import SR, boucle, ecrire_normalise, lire_audio  # noqa: E402
from effets import etalonnage_doc  # noqa: E402
from fenetre import fenetre  # noqa: E402

M = os.path.join(ICI, "..", "..", "medias")
PX = os.path.join(M, "pexels", "s07")
D3 = os.path.join(M, "S07", "3d")
SONS = os.path.join(M, "sons", "epidemic")
OUT = os.path.join(M, "S07")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1920, 1080, 24
FONTS = "C:/Windows/Fonts/"
CREME = (238, 230, 216)


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def doux(p):
    p = min(1.0, max(0.0, p))
    return p * p * p * (p * (p * 6 - 15) + 10)


# ---------------------------------------------------------------- la voix (prise 2) : phrases et places
VOIX = os.path.join(M, "voix", "S07_prise2.mp3")
PHRASES = {  # nom : ((début, fin) dans la prise, position dans la scène)
    "ecole": ((4.85, 8.55), 2.0),        # Ses parents l'inscrivent dans une école privée. Ça leur coûte cher.
    "question": ((9.70, 13.05), 7.0),    # Vous avez sept ans. Qu'est-ce que vous aimez faire de votre temps libre ?
    "prends": ((14.07, 15.00), 13.4),    # Je prends celle-là.
    "huit": ((15.57, 21.10), 17.2),      # À huit ans, quand les grands lui demandent ce qu'il veut faire plus tard, il répond toujours la même chose.
    "neuf": ((21.81, 26.90), 32.2),      # À neuf ans, il bavarde en classe, et le maître lui donne des coups de baguette sur la paume.
    "main": ((27.62, 29.80), 38.8),      # Après ça, il ne lève plus la main.
    "dette": ((30.82, 33.07), 42.4),     # La même année, la famille s'endette.
    "dix": ((33.53, 35.70), 45.6),       # À dix ans, son grand-père meurt.
    "pleurer": ((36.43, 38.77), 49.1),   # Il regarde longtemps les adultes pleurer.
}
# Bruno (08/11/2026) : après « ingénieur », dire que c'est un rêve ambitieux. Le chiffre vient de la simulation :
# sur les 200 vies nées dans les mêmes conditions (prompts/partie/6-parts-decisions.json), 2 font des études d'ingénieur.
# Une seule prise possible (crédits ElevenLabs épuisés), un peu aiguë : baissée (rubberband 0.90, timbre préservé).
VOIX_REVE = os.path.join(M, "voix", "S07_reve_prise1_p0.90.mp3")
PHRASES_REVE = [((2.40, 3.96), 25.3),    # Un rêve plutôt ambitieux.
                ((4.58, 6.53), 27.2),    # Sur deux cents vies nées comme lui,
                ((6.85, 8.80), 29.35)]   # deux seulement font des études d'ingénieur.
T_ETEINT = 29.6                          # « deux seulement » : les autres s'éteignent
T_FRAPPE = 36.95                         # la baguette s'abat (sur « …la paume »)
T_CLIC = 14.15                           # « Je prends celle-là. » : le clic

# ---------------------------------------------------------------- le déroulé : (début, fin, genre, source, plein, entrée)
#   genre : reel (vraie vidéo) · d3 (tableau rendu) · fixe (image 3D fixe, lente poussée) · choix · ingenieur
#   plein : 0 = dans la fenêtre de l'interface, 1 = plein écran ; entrée : coupe · morph (fenêtre <-> plein) · fondu
PLANS = [
    (0.00, 0.95, "reel", ("35724453.mp4", 1.0, 1.0, 0.5), 1, "coupe"),
    (0.95, 1.75, "reel", ("15957335.mp4", 2.0, 1.0, 0.5), 1, "coupe"),
    (1.75, 4.75, "d3", ("ecole", 0.6), 0, "morph"),
    (4.75, 6.40, "reel", ("4112783.mp4", 3.0, 1.0, 0.5), 1, "morph"),
    (6.40, 14.85, "choix", None, 0, "morph"),
    (14.85, 16.90, "reel", ("28887495.mp4", 2.0, 1.0, 0.5), 1, "morph"),
    (16.90, 23.30, "d3", ("huit_ans", 0.0), 0, "morph"),
    (23.30, 32.10, "ingenieur", None, 1, "coupe"),
    (32.10, 34.10, "reel", ("16868495.mp4", 2.0, 1.0, 0.5), 1, "coupe"),
    (34.10, 38.50, "d3", ("baguette", 0.0), 1, "coupe"),
    (38.50, 42.10, "d3", ("classe", 0.0), 0, "morph"),
    (42.10, 43.10, "reel", ("18070270.mp4", 10.0, 1.0, 0.5), 1, "morph"),
    (43.10, 45.30, "fixe", ("dette",), 0, "morph"),
    (45.30, 48.40, "reel", ("20143634.mp4", 3.0, 0.8, 0.5), 1, "morph"),
    (48.40, 55.40, "d3", ("funerailles", 0.0), 1, "fondu"),
    (55.40, 58.50, "reel", ("34630320.mp4", 1.0, 0.8, 0.45), 1, "fondu"),
]
DUREE = PLANS[-1][1]
N = int(round(DUREE * FPS))
T_MORPH = 0.42
AGES = [("5 ans", 0.15, 1.70), ("7 ans", 6.7, 14.2), ("8 ans", 17.3, 22.9), ("9 ans", 32.2, 34.0), ("10 ans", 45.5, 48.2)]

# ---------------------------------------------------------------- lecture des sources
_videos, _d3 = {}, {}


def lire_extrait(nom, debut, vitesse, duree, cy=0.5):
    cle = (nom, debut, vitesse)
    if cle in _videos:
        return _videos[cle]
    n = int(math.ceil(duree * FPS)) + 8
    vf = (f"setpts=PTS/{vitesse},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H}:(iw-{W})/2:(ih-{H})*{cy}")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(debut), "-i", os.path.join(PX, nom), "-vf", vf,
                          "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(im) < n:
        im = np.concatenate([im, np.repeat(im[-1:], n - len(im), 0)])
    _videos[cle] = im
    return im


def image_3d(plan, k):
    d = os.path.join(D3, plan)
    if plan not in _d3:
        _d3[plan] = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    fs = _d3[plan]
    return cv2.imread(os.path.join(d, fs[max(0, min(k, len(fs) - 1))])).astype(np.float32)


# ---------------------------------------------------------------- l'âge, comme en S06
F_AGE = ImageFont.truetype(FONTS + "georgia.ttf", 92)


def calque_texte(texte, font, xy, couleur=CREME):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(c).text(xy, texte, font=font, fill=(*couleur, 255))
    a = np.asarray(c).astype(np.float32)
    return a[..., :3][..., ::-1].copy(), a[..., 3] / 255, cv2.GaussianBlur(a[..., 3], (0, 0), 10) / 255


CAL_AGES = {a: calque_texte(a, F_AGE, (140, 880)) for a, _, _ in AGES}


def poser_calque(f, cal, o, dy=0):
    rgb, al, om = cal
    if dy:
        rgb, al, om = (np.roll(v, dy, axis=0) for v in (rgb, al, om))
    f = f * (1 - 0.45 * o * om[..., None])
    return f * (1 - o * al[..., None]) + rgb * (o * al[..., None])


def ajouter_age(f, t):
    for a, t0, t1 in AGES:
        if t0 - 0.05 <= t <= t1 + 0.4:
            o = lisse((t - t0) / 0.45) * (1 - lisse((t - t1) / 0.35))
            if o > 0:
                f = poser_calque(f, CAL_AGES[a], o, int(round(10 * (1 - lisse((t - t0) / 0.45)))))
    return f


# ---------------------------------------------------------------- 7 ans : le choix, en motion design
CARTES = [("choix_priere", "La prière"), ("choix_danse", "La danse"), ("choix_cricket", "Le cricket")]
CW, CH, ECART_C = 576, 324, 34
CX0 = (W - (3 * CW + 2 * ECART_C)) // 2
CY = 300
F_CARTE = ImageFont.truetype(FONTS + "georgiai.ttf", 48)
_cartes = {}


def coins_ronds(w, h, r=14, k=3):
    m = Image.new("L", (w * k, h * k), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * k - 1, h * k - 1], radius=r * k, fill=255)
    return np.asarray(m.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255


MASQUE_C = coins_ronds(CW, CH)
# le curseur hésite : (temps, carte visée)
HESITE = [(10.45, 1), (11.35, 2), (12.15, 0), (12.75, 1), (13.30, 0)]


def carte_img(i):
    if i not in _cartes:
        im = image_3d(CARTES[i][0], 0)
        _cartes[i] = cv2.resize(im, (CW, CH), interpolation=cv2.INTER_AREA)
    return _cartes[i]


def cible(t):
    """Carte survolée et position du curseur au temps t."""
    pos = [(CX0 + i * (CW + ECART_C) + CW * 0.62, CY + CH * 0.62) for i in range(3)]
    if t < HESITE[0][0]:
        return None, (W * 0.5, H * 0.86)
    prec, prec_t, prec_p = None, HESITE[0][0] - 0.35, (W * 0.5, H * 0.86)
    for tt, i in HESITE:
        if t < tt:
            p = doux((t - prec_t) / (tt - prec_t))
            q = pos[i]
            return prec, (prec_p[0] + (q[0] - prec_p[0]) * p, prec_p[1] + (q[1] - prec_p[1]) * p)
        prec, prec_t, prec_p = i, tt, pos[i]
    return prec, prec_p


def dessiner_curseur(d, x, y, appui=0.0):
    s = 1 - 0.18 * appui
    pts = [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (26, 24)]
    pts = [(x + px * s, y + py * s) for px, py in pts]
    d.polygon(pts, fill=(245, 242, 236), outline=(20, 20, 20))


def ecran_choix(t):
    tl = t - 6.40
    f = np.empty((H, W, 3), np.float32)
    f[:] = (16, 15, 15)
    survol, (cx, cy) = cible(t)
    choisi = t >= T_CLIC
    agrandi = doux((t - (T_CLIC + 0.1)) / 0.55)
    calque = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)
    hesite = t >= HESITE[0][0] - 0.3
    for i in ((1, 2, 0) if choisi else (0, 1, 2)):
        a = lisse((tl - 0.15 - 0.15 * i) / 0.45)
        if a <= 0:
            continue
        sel = (survol == i) and not choisi
        s = 1.0 + (0.05 if sel else 0.0)
        luz = 1.0 if (sel or not hesite) else 0.62
        if choisi:
            luz = 1.0 if i == 0 else 0.6
            s = 1.0 + (0.05 if i == 0 else 0)
            if i != 0:
                a *= max(0.0, 1 - agrandi * 2.2)        # les deux autres s'effacent
                if a <= 0.01:
                    continue
        x0 = CX0 + i * (CW + ECART_C)
        y0 = CY + int(40 * (1 - a))
        img = carte_img(i)
        if choisi and i == 0 and agrandi > 0:
            # la carte choisie remplit l'écran
            w_ = int(CW * s + (W - CW * s) * agrandi)
            h_ = int(CH * s + (H - CH * s) * agrandi)
            xa = int((x0 - (CW * s - CW) / 2) * (1 - agrandi))
            ya = int((y0 - (CH * s - CH) / 2) * (1 - agrandi))
            plein = cv2.resize(image_3d("choix_priere", 0), (w_, h_), interpolation=cv2.INTER_AREA)
            m = cv2.resize(MASQUE_C, (w_, h_)) if agrandi < 0.98 else np.ones((h_, w_), np.float32)
            z = f[ya:ya + h_, xa:xa + w_]
            f[ya:ya + h_, xa:xa + w_] = z * (1 - m[..., None]) + plein * m[..., None]
            continue
        w_, h_ = int(CW * s), int(CH * s)
        xa, ya = int(x0 - (w_ - CW) / 2), int(y0 - (h_ - CH) / 2)
        im = cv2.resize(img, (w_, h_)) * luz
        m = cv2.resize(MASQUE_C, (w_, h_))[..., None] * a
        z = f[ya:ya + h_, xa:xa + w_]
        f[ya:ya + h_, xa:xa + w_] = z * (1 - m) + im * m
        if sel or (choisi and i == 0 and agrandi <= 0):
            d.rounded_rectangle([xa - 2, ya - 2, xa + w_ + 2, ya + h_ + 2], radius=16, outline=(*CREME, 230), width=3)
        lab_a = int(255 * a * (1 if (sel or not hesite) else 0.55) * (1 - (agrandi if choisi else 0)))
        tw = d.textlength(CARTES[i][1], font=F_CARTE)
        d.text((x0 + (CW - tw) / 2, y0 + CH + 28), CARTES[i][1], font=F_CARTE, fill=(*CREME, lab_a))
    # le compte à rebours : un trait qui se vide pendant que le curseur hésite
    if HESITE[0][0] - 0.1 <= t < T_CLIC + 0.2:
        p = 1 - np.clip((t - (HESITE[0][0] - 0.1)) / (13.4 - HESITE[0][0] + 0.1), 0, 1)
        xb0, xb1, yb = CX0, CX0 + 3 * CW + 2 * ECART_C, CY + CH + 120
        d.line([(xb0, yb), (xb1, yb)], fill=(70, 66, 62, 160), width=3)
        d.line([(xb0, yb), (xb0 + (xb1 - xb0) * p, yb)], fill=(*CREME, 220), width=3)
    if t >= HESITE[0][0] - 0.35 and agrandi < 0.3:
        appui = max(0.0, 1 - abs(t - T_CLIC) / 0.08) if abs(t - T_CLIC) < 0.08 else 0.0
        dessiner_curseur(d, cx, cy, appui)
    a = np.asarray(calque).astype(np.float32)
    al = a[..., 3:4] / 255
    f = f * (1 - al) + a[..., :3][..., ::-1] * al
    return f


# ---------------------------------------------------------------- 8 ans : « ingénieur »
F_ING = ImageFont.truetype(FONTS + "georgiai.ttf", 176)
MOT = "ingénieur"


def plan_pont():
    """Les lignes d'un pont dessiné, comme sur une planche d'ingénieur (repère écran)."""
    seg = []
    y0, x0, x1 = 760, 260, 1660
    seg.append(((x0, y0), (x1, y0)))
    n = 12
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        hh = 230 * math.sin(math.pi * k / n)
        seg.append(((x, y0), (x, y0 - hh)))
        if k < n:
            xn = x0 + (x1 - x0) * (k + 1) / n
            hn = 230 * math.sin(math.pi * (k + 1) / n)
            seg.append(((x, y0 - hh), (xn, y0 - hn)))
            seg.append(((x, y0), (xn, y0 - hn)) if k < n / 2 else ((x, y0 - hh), (xn, y0)))
    seg.append(((x0 - 120, y0 + 60), (x1 + 120, y0 + 60)))
    for x in (x0, x1):
        seg.append(((x, y0), (x - 40, y0 + 60)))
        seg.append(((x, y0), (x + 40, y0 + 60)))
    return seg


PONT = plan_pont()


# les 200 vies nées comme lui : 20 x 10 petites silhouettes ; deux feront des études d'ingénieur
COLS_V, LIGNES_V = 20, 10
PAS_X, PAS_Y = 62, 57
GX0 = (W - (COLS_V - 1) * PAS_X) // 2
GY0 = 360
ELUS = {(5, 2), (14, 7)}                 # (colonne, rangée) des deux vies allumées
ROUGE = (214, 72, 46)


def silhouette(d, x, y, col, s=1.0):
    r = 6 * s
    d.ellipse([x - r, y - 17 * s - r, x + r, y - 17 * s + r], fill=col)
    d.rounded_rectangle([x - 9 * s, y - 9 * s, x + 9 * s, y + 13 * s], radius=int(7 * s), fill=col)


def ecran_ingenieur(t):
    tl = t - 23.30
    c = Image.new("RGB", (W, H), (9, 9, 10))
    d = ImageDraw.Draw(c)
    # le pont se dessine, puis s'efface quand les vies arrivent
    p = np.clip(tl / 2.3, 0, 1)
    fade_pont = 1 - lisse((tl - 1.9) / 0.6)
    if fade_pont > 0:
        nseg = len(PONT) * p
        col_p = tuple(int(9 + (v - 9) * fade_pont) for v in (62, 58, 54))
        for k, ((xa, ya), (xb, yb)) in enumerate(PONT):
            q = np.clip(nseg - k, 0, 1)
            if q <= 0:
                break
            d.line([(xa, ya), (xa + (xb - xa) * q, ya + (yb - ya) * q)], fill=col_p, width=2)
    # les 200 vies apparaissent en vague, puis 198 s'éteignent ; deux deviennent rouges
    e_on = 0.0
    for r in range(LIGNES_V):
        for k in range(COLS_V):
            a = lisse((tl - 2.25 - 0.045 * (r + k)) / 0.35)
            if a <= 0:
                continue
            if (k, r) in ELUS:
                v = lisse((t - (T_ETEINT + 0.25)) / 0.4)
                base = (120, 114, 106)
                col = tuple(int((b + (ro - b) * v) * a) for b, ro in zip(base, ROUGE))
                e_on = v
            else:
                eteint = lisse((t - T_ETEINT - 0.012 * ((k * 7 + r * 13) % 23)) / 0.45)
                g = 120 - 82 * eteint
                col = (int(g * a), int(g * 0.95 * a), int(g * 0.88 * a))
            silhouette(d, GX0 + k * PAS_X, GY0 + r * PAS_Y, col, 1.15)
    f = np.asarray(c).astype(np.float32)[:, :, ::-1]
    # le mot, qui monte et rapetisse quand les vies apparaissent
    m = lisse((tl - 1.75) / 0.8)
    calque = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(calque)
    largeur = dc.textlength(MOT, font=F_ING)
    x = (W - largeur) / 2
    for i, ch in enumerate(MOT):
        a = lisse((tl - 0.35 - 0.09 * i) / 0.25)
        if a > 0:
            dc.text((x, 330 + 14 * (1 - a)), ch, font=F_ING, fill=(*CREME, int(255 * a)))
        x += dc.textlength(ch, font=F_ING)
    a = np.asarray(calque).astype(np.float32)
    if m > 0:
        M_ = cv2.getRotationMatrix2D((W / 2, 430), 0, 1 - 0.42 * m)
        M_[1, 2] -= 250 * m
        a = cv2.warpAffine(a, M_, (W, H), flags=cv2.INTER_LINEAR)
    al = a[..., 3:4] / 255
    f = f * (1 - al) + a[..., :3][..., ::-1] * al
    # le halo : le mot ; et une lueur rouge autour des deux vies allumées
    halo = cv2.GaussianBlur(np.clip(f - 90, 0, 255), (0, 0), 14)
    rouge = np.clip(f[..., 2:3] - f[..., 1:2] - 60, 0, 255)
    f = f + 0.35 * halo + 0.9 * e_on * cv2.GaussianBlur(rouge * np.float32([0.25, 0.4, 1.0]), (0, 0), 10)
    f *= 1 - lisse((tl - 8.55) / 0.25)             # s'éteint juste avant la coupe
    return f


# ---------------------------------------------------------------- le contenu d'un plan au temps t
def contenu(i, t):
    t0, t1, genre, src, plein, entree = PLANS[i]
    tl = t - t0
    k = int(round(tl * FPS))
    if genre == "reel":
        nom, deb, vit, cy = src
        ims = lire_extrait(nom, deb, vit, (t1 - t0) + 1.2, cy)
        f = ims[max(0, min(k, len(ims) - 1))].astype(np.float32)
        z = 1 + 0.035 * tl / (t1 - t0)
        f = cv2.warpAffine(f, cv2.getRotationMatrix2D((W / 2, H / 2), 0, z), (W, H), borderMode=cv2.BORDER_REFLECT)
        f = etalonnage_doc(f, k)
        if nom == "18070270.mp4":                    # le billet perd ses couleurs : la dette
            g = f.mean(2, keepdims=True)
            q = lisse(tl / 0.9)
            f = (f * (1 - q) + g * q) * (1 - 0.35 * q)
    elif genre == "d3":
        plan, decal = src
        f = image_3d(plan, k + int(decal * FPS))
    elif genre == "fixe":
        f = image_3d(src[0], 0)
        z = 1 + 0.07 * lisse(tl / (t1 - t0))
        f = cv2.warpAffine(f, cv2.getRotationMatrix2D((W / 2, H * 0.55), 0, z), (W, H), borderMode=cv2.BORDER_REFLECT)
    elif genre == "choix":
        f = ecran_choix(t)
    else:
        f = ecran_ingenieur(t)
    return ajouter_age(f, t)


def image(n):
    t = n / FPS
    i = max(j for j, p in enumerate(PLANS) if p[0] <= t + 1e-6)
    t0, t1, genre, src, plein, entree = PLANS[i]
    c = contenu(i, t)
    pl, ouv = float(plein), 1.0
    if i > 0 and entree in ("morph", "fondu"):
        dt = t - t0
        p_prec = PLANS[i - 1][4]
        dur = T_MORPH if entree == "morph" else 0.9
        if dt < dur:
            q = doux(dt / dur)
            pl = p_prec + (plein - p_prec) * q
            c_prec = contenu(i - 1, t)
            mix = lisse(dt / (dur * 0.6)) if entree == "morph" else q
            c = c_prec * (1 - mix) + c * mix
    # 8 ans -> « ingénieur » : la fenêtre se referme
    if genre == "d3" and src[0] == "huit_ans":
        ouv = 1 - doux((t - (t1 - 0.45)) / 0.45)
    f = fenetre(c, ouv, pl)
    # la frappe : un éclair et une secousse
    d_ = round((t - T_FRAPPE) * FPS)
    if 0 <= d_ <= 1:
        f = f * (1 - (0.65, 0.3)[d_]) + 255 * (0.65, 0.3)[d_]
    if 0 <= d_ <= 7:
        rng = np.random.default_rng(77 + d_)
        amp = 16 * (1 - d_ / 8)
        f = cv2.warpAffine(f, np.float32([[1.02, 0, -19 + rng.uniform(-amp, amp)], [0, 1.02, -11 + rng.uniform(-amp, amp)]]),
                           (W, H), borderMode=cv2.BORDER_REFLECT)
    # entrée depuis le noir et sortie au noir
    f *= lisse(t / 0.12) * (1 - lisse((t - (DUREE - 1.3)) / 1.25))
    f += np.random.default_rng(n).normal(0, 1.8, f.shape).astype(np.float32)
    return f


SON_SEUL = os.environ.get("SON_SEUL") == "1"
if not SON_SEUL:
    if "--test" in sys.argv:
        for t in (24.6, 26.0, 27.5, 29.0, 30.2, 31.5):
            cv2.imwrite(os.path.join(sys.argv[-1], f"s07_{t:05.2f}.png"), np.clip(image(int(t * FPS)), 0, 255).astype(np.uint8))
        sys.exit()
    ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", os.path.join(OUT, "S07_image.mp4")],
                           stdin=subprocess.PIPE)
    for n in range(N):
        ecr.stdin.write(np.clip(image(n), 0, 255).astype(np.uint8).tobytes())
    ecr.stdin.close()
    ecr.wait()
    print("image :", DUREE, "s")

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
    return lire_audio(os.path.join(dossier, nom), mono=False).astype(np.float64)


def stereo(nom, debut, dossier=SONS):
    return boucle(lire(nom, dossier)[int(debut * SR):], Ns)


def env(t0, t1, e=0.25, s=0.3):
    return np.clip((ts - t0) / max(e, 1e-3), 0, 1) * np.clip((t1 - ts) / max(s, 1e-3), 0, 1)


def crete(a):
    return int(np.argmax(np.abs(a).mean(1)))


def extrait(nom, avant, apres, e=0.005, s=0.1):
    a = lire(nom)
    o = crete(a)
    seg = a[max(0, o - int(avant * SR)):o + int(apres * SR)]
    return seg * fondu(len(seg), e, s)[:, None]


# 5 ans : la cloche, la cour, l'école, les billets
poser(extrait("cloche_ecole.wav", 0.05, 1.8, 0.002, 0.8), 0.0, db(-9))
mix += stereo("classe_inde.wav", 30.0) * (db(-20) * env(0, 1.9, 0.05, 0.3))[:, None]
mix += stereo("village_amethi.wav", 70.0) * (db(-25) * env(1.7, 4.9, 0.3, 0.3))[:, None]
bil = lire("billets_compter.wav")
mix[int(4.75 * SR):int(4.75 * SR) + int(1.7 * SR)] += (bil[int(2 * SR):int(3.7 * SR)] * fondu(int(1.7 * SR), 0.02, 0.3)[:, None]
                                                       * db(-10))[:len(mix[int(4.75 * SR):int(4.75 * SR) + int(1.7 * SR)])]
# 7 ans : l'interface ; les cartes arrivent, le curseur hésite (et l'on entend chaque possibilité), le clic
wh = extrait("whoosh_air.wav", 0.3, 0.3, 0.1, 0.2)
for i in range(3):
    poser(wh, 6.4 + 0.15 + 0.15 * i, db(-27))
tic = lire("tic_doux.wav")
o_t = crete(tic[:SR])
un_tic = tic[max(0, o_t - 100):o_t + int(0.06 * SR)] * fondu(o_t + int(0.06 * SR) - max(0, o_t - 100), 0.002, 0.03)[:, None]
for k in range(3):
    poser(un_tic, HESITE[0][0] + k * 1.0 - 0.02, db(-15))
apercus = {0: ("bhajan.wav", 40.0), 1: ("dholak_rue.wav", 30.0), 2: ("cricket_batte.wav", 0.0)}
for k, (tt, i) in enumerate(HESITE):
    fin = HESITE[k + 1][0] if k + 1 < len(HESITE) else T_CLIC
    nom, deb = apercus[i]
    a = lire(nom)[int(deb * SR):int((deb + fin - tt + 0.4) * SR)]
    poser(a * fondu(len(a), 0.08, 0.3)[:, None], tt - 0.05, db(-23 if i != 2 else -20))
clics = lire("souris_clics.wav")
o_c = crete(clics[int(5 * SR):int(8 * SR)]) + int(5 * SR)
poser(clics[o_c - 200:o_c + int(0.15 * SR)], T_CLIC, db(-7))
# la prière : le chant monte, puis se perd sous les 8 ans
mix += stereo("bhajan.wav", 55.0) * (db(-11) * env(14.3, 17.4, 0.5, 1.2))[:, None]
mix += stereo("grillons_nuit.wav", 50.0) * (db(-21) * env(16.9, 23.0, 0.8, 0.5))[:, None]
# « ingénieur » : presque le silence, une note tenue
tn = np.arange(int(3.0 * SR)) / SR
note = (np.sin(2 * np.pi * 220 * tn) + 0.5 * np.sin(2 * np.pi * 329.6 * tn) + 0.25 * np.sin(2 * np.pi * 440 * tn))
note *= np.minimum(1, tn / 0.4) * np.exp(-tn / 1.6) * 0.18
poser(np.stack([note, note], 1), 23.55, 1.0)
mix += stereo("ambiance_grand_hall.wav", 30.0) * (db(-28) * env(23.3, 32.1, 0.2, 0.1))[:, None]
# les vies apparaissent : un frémissement de petits tics ; elles s'éteignent : un souffle grave ; deux notes claires
for r in range(10):
    poser(un_tic, 25.55 + 0.09 * r, db(-31))
tw = np.arange(int(1.2 * SR)) / SR
souffle = np.sin(2 * np.pi * (110 * tw - 25 * tw * tw)) * np.exp(-tw / 0.5) * 0.1
poser(np.stack([souffle, souffle], 1), T_ETEINT, 1.0)
for k_, f0 in enumerate((659.3, 880.0)):
    tc = np.arange(int(1.6 * SR)) / SR
    cl = np.sin(2 * np.pi * f0 * tc) * np.exp(-tc / 0.5) * 0.05 * np.minimum(1, tc / 0.01)
    poser(np.stack([cl, cl], 1), T_ETEINT + 0.3 + 0.12 * k_, 1.0)
# 9 ans : la classe, puis le silence avant le coup, le coup, et le sifflement dans les oreilles
mix += stereo("classe_inde.wav", 60.0) * (db(-16) * env(32.1, T_FRAPPE - 0.9, 0.05, 1.2))[:, None]
poser(extrait("baguette_air.wav", 0.25, 0.1, 0.05, 0.05), T_FRAPPE - 0.25, db(-10))
poser(extrait("claque.wav", 0.003, 0.5, 0.001, 0.3), T_FRAPPE - 0.003, db(-3))
tb = np.arange(int(0.5 * SR)) / SR
coup = np.sin(2 * np.pi * (70 * tb - 30 * tb * tb)) * np.exp(-tb / 0.12) * 0.6
poser(np.stack([coup, coup], 1), T_FRAPPE, 1.0)
ts_ = np.arange(int(2.2 * SR)) / SR
sif = np.sin(2 * np.pi * 3400 * ts_) * np.exp(-ts_ / 0.8) * 0.02
poser(np.stack([sif, sif], 1), T_FRAPPE + 0.05, 1.0)
mix += stereo("classe_inde.wav", 95.0) * (db(-27) * env(38.6, 42.1, 0.6, 0.3))[:, None]
# la dette : les billets, la nuit
mix += stereo("grillons_nuit.wav", 80.0) * (db(-23) * env(42.1, 45.4, 0.4, 0.5))[:, None]
poser(bil[int(6 * SR):int(7.2 * SR)] * fondu(int(1.2 * SR), 0.05, 0.6)[:, None], 42.15, db(-17))
# 10 ans : le fleuve, le soir ; la musique (piano) entre et porte le deuil jusqu'au bout
mix += stereo("soir_rural.wav", 20.0) * (db(-19) * env(45.3, DUREE, 0.4, 2.0))[:, None]
mus = stereo("remembering.wav", 0.0, os.path.join(M, "musique"))
mix += mus * (db(-15) * env(45.0, DUREE + 0.3, 1.2, 2.5))[:, None]

# la voix (prise 2), au niveau des autres scènes
a_ = lire_audio(VOIX, mono=True).astype(np.float64)
actif = np.abs(a_) > 0.01
a_ *= db(-17.2 - 20 * np.log10(np.sqrt((a_[actif] ** 2).mean())))
voix = np.zeros(Ns)
for (a, b), pos in PHRASES.values():
    s_ = a_[int(a * SR):int(b * SR)]
    s_ = s_ * fondu(len(s_), 0.01, 0.06)
    j = int(pos * SR)
    f_ = min(Ns, j + len(s_))
    voix[j:f_] += s_[:f_ - j]
b_ = lire_audio(VOIX_REVE, mono=True).astype(np.float64)
actif = np.abs(b_) > 0.01
b_ *= db(-17.2 - 20 * np.log10(np.sqrt((b_[actif] ** 2).mean())))
for (a, b), pos in PHRASES_REVE:
    s_ = b_[int(a * SR):int(b * SR)]
    s_ = s_ * fondu(len(s_), 0.01, 0.06)
    j = int(pos * SR)
    f_ = min(Ns, j + len(s_))
    voix[j:f_] += s_[:f_ - j]
env_voix = np.convolve(np.abs(voix) > 1e-3, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode="same")
mix *= (1 - 0.4 * np.clip(env_voix * 3, 0, 1))[:, None]
mix += voix[:, None] * db(-3.5)
mix *= fondu(Ns, 0.03, 1.4)[:, None]

GAIN = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
wav = os.path.join(OUT, "S07_son.wav")
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN))
final = os.path.join(OUT, "S07_v1.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, "S07_image.mp4"), "-i", wav, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", final], check=True)
print("écrit :", final)
