"""S07 · L'enfance (5 à 10 ans), puis la salle des simulateurs : le premier choix.

Version 2 (retours de Bruno, 08/11/2026) :
  - la voix de narration est la prise 1 (S07_prise1) ;
  - plus de choix à 7 ans (le premier choix arrive dans la salle des simulateurs) ; plus de coups de baguette :
    « À l'école, il est plutôt timide. Souvent au fond de la classe, à écouter. » ;
  - « À dix ans, le premier gros évènement de sa vie arrive. » : les funérailles du grand-père, puis l'on recule :
    c'était un écran, dans une salle de surveillance où deux « simulateurs » décident de la vie des autres (salle.py).
    Ils parlent de lui, décident de « reprendre les rênes », et posent le premier choix au spectateur.

Les phrases qui n'ont pas encore de voix (crédits ElevenLabs épuisés) sont des sous-titres provisoires, calés sur une durée
estimée (VOIX_A_VENIR) ; dès qu'elles seront générées, on remplace l'entrée par le fichier et ses temps.

Usage : python montage.py      ->  medias/S07/S07_v2.mp4     (SON_SEUL=1 : le son seul ; --test <dossier> : images fixes)
"""
import json
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
SALLE = os.path.join(M, "S07", "salle")
SONS = os.path.join(M, "sons", "epidemic")
OUT = os.path.join(M, "S07")
W, H, FPS = 1920, 1080, 24
FONTS = "C:/Windows/Fonts/"
CREME = (238, 230, 216)


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def doux(p):
    p = min(1.0, max(0.0, p))
    return p * p * p * (p * (p * 6 - 15) + 10)


# ---------------------------------------------------------------- les repères du déroulé
T_HUIT = 6.40
T_ING = 12.80            # « ingénieur », le rêve et les 200 vies (8,8 s)
T_ETEINT = T_ING + 6.3
T_CLASSE = 21.60
T_BILLET = 26.20
T_DETTE = 27.20
T_FLEUVE = 29.40
T_FUN = 32.50
T_DIYA = 39.50
T_REVELE = 41.60         # on recule : c'était un écran
T_LARGE = 47.60
T_EPAULE = 57.60
T_REGARD = 63.60
T_CLIC_P = 69.00         # retour par-dessus l'épaule : le clic
T_NOIR = 73.60
DUREE = 73.60            # Bruno (09/11) : plus d'écran noir ; S08 reprend sur l'écran, avec « Bon choix… »
T_CHOIX = T_EPAULE + 1.0             # le choix s'affiche sur l'écran central
T_DECOMPTE = (65.8, 68.8)            # trois secondes : le spectateur choisit
T_CLIC = 70.60

# ---------------------------------------------------------------- les voix
VOIX = os.path.join(M, "voix", "S07_prise1.mp3")          # la prise 1 (Bruno)
PHRASES = [  # ((début, fin) dans la prise, position dans la scène)
    ((5.00, 8.47), 2.0),        # Ses parents l'inscrivent dans une école privée. Ça leur coûte cher.
    ((15.38, 20.27), 6.7),      # À huit ans, quand les grands lui demandent ce qu'il veut faire plus tard, il répond toujours la même chose.
    ((30.03, 32.22), 27.4),     # La même année, la famille s'endette.
    ((35.76, 37.84), 35.4),     # Il regarde longtemps les adultes pleurer.
]
# le rêve : la version d'hier, telle quelle (choix de Bruno, 08/11/2026)
VOIX_REVE = os.path.join(M, "voix", "S07_reve_prise1.mp3")
PHRASES_REVE = [
    ((2.40, 3.96), T_ING + 2.0),     # Un rêve plutôt ambitieux.
    ((4.58, 6.53), T_ING + 3.9),     # Sur deux cents vies nées comme lui,
    ((6.85, 8.80), T_ING + 6.05),    # deux seulement font des études d'ingénieur.
]
# « timide » : génération du 08/11 dans la continuité, prise 1
VOIX_B = os.path.join(M, "voix", "S07b_prise1.mp3")
PHRASES_B = [
    ((12.00, 13.72), 21.9),          # À l'école, il est plutôt timide.
    ((14.10, 15.96), 24.0),          # Souvent au fond de la classe, à écouter.
]
# « dix ans » et « Il perd son grand-père » : une seule génération, prise 1
VOIX_C = os.path.join(M, "voix", "S07c_prise1.mp3")
PHRASES_C = [
    ((2.36, 7.28), 29.9),            # À dix ans, le premier gros évènement de sa vie arrive. Il perd son grand-père.
]
# les deux simulateurs (dans la salle : un peu de pièce autour de leur voix)
VOIX_LUI = os.path.join(M, "voix", "S07_lui_prise1.mp3")      # Nori, eleven_v3
PHRASES_LUI = [
    ((0.10, 2.06), 44.2),     # Tiens, regarde. C'est lui, Manoj.
    ((2.74, 5.08), 46.6),     # Je lui ai laissé la vie douce, jusqu'à maintenant.
    ((5.86, 7.46), 49.6),     # Il vient de perdre son grand-père.
]
VOIX_LUI2 = os.path.join(M, "voix", "S07_lui2_prise1.mp3")    # Nori, dans la continuité
PHRASES_LUI2 = [
    ((0.12, 3.67), 55.3),     # L'an prochain, il finit l'école primaire. Ses parents sont endettés.
    ((4.05, 5.46), 69.0),     # Il faut qu'il continue l'école.
    ((5.81, 7.92), 71.1),     # Ses frères et sœurs n'ont pas eu cette chance.
]
VOIX_ELLE = os.path.join(M, "voix", "S07_elle_prise2.mp3")    # Sara, eleven_v3
PHRASES_ELLE = [
    ((0.06, 2.78), 52.0),     # Je pense que c'est le moment de reprendre les rênes.
    ((4.34, 4.62), 59.4),     # Alors ?
    ((5.82, 6.78), 60.0),     # Il continue l'école…
    ((7.72, 9.50), 61.2),     # … ou il va travailler pour les aider ?
    ((10.40, 10.98), 64.4),   # À toi de voir.
]
VOIX_A_VENIR = []         # toutes les phrases ont leur voix

# ---------------------------------------------------------------- le déroulé : (début, fin, genre, source, plein, entrée)
PLANS = [
    (0.00, 0.95, "reel", ("35724453.mp4", 1.0, 1.0, 0.5), 1, "coupe"),
    (0.95, 1.75, "reel", ("15957335.mp4", 2.0, 1.0, 0.5), 1, "coupe"),
    (1.75, 4.75, "d3", ("ecole", 0.6), 0, "morph"),
    (4.75, T_HUIT, "reel", ("4112783.mp4", 3.0, 1.0, 0.5), 1, "morph"),
    (T_HUIT, T_ING, "d3", ("huit_ans", 0.0), 0, "morph"),
    (T_ING, T_CLASSE, "ingenieur", None, 1, "coupe"),
    (T_CLASSE, T_BILLET, "d3", ("classe", 0.0), 0, "coupe"),
    (T_BILLET, T_DETTE, "reel", ("18070270.mp4", 10.0, 1.0, 0.5), 1, "morph"),
    (T_DETTE, T_FLEUVE, "fixe", ("dette",), 0, "morph"),
    (T_FLEUVE, T_FUN, "reel", ("20143634.mp4", 3.0, 0.8, 0.5), 1, "morph"),
    (T_FUN, T_DIYA, "d3", ("funerailles", 0.0), 1, "fondu"),
    (T_DIYA, T_REVELE, "reel", ("34630320.mp4", 1.0, 0.8, 0.45), 1, "fondu"),
    (T_REVELE, T_LARGE, "salle", ("revele", 0.0), 1, "coupe"),
    (T_LARGE, T_EPAULE, "salle", ("large", 0.0), 1, "coupe"),
    (T_EPAULE, T_REGARD, "salle", ("epaule", 0.0), 1, "coupe"),
    (T_REGARD, T_CLIC_P, "salle", ("regard", 0.0), 1, "coupe"),
    (T_CLIC_P, DUREE, "salle", ("epaule", 3.0), 1, "coupe"),
]
N = int(round(DUREE * FPS))
T_MORPH = 0.42
AGES = [("5 ans", 0.15, 1.70), ("8 ans", T_HUIT + 0.3, T_ING - 0.5), ("10 ans", T_FLEUVE + 0.1, T_FUN - 0.3)]

# ---------------------------------------------------------------- lecture des sources
_videos, _d3, _salle = {}, {}, {}


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


def salle(plan, k):
    """Image k du plan de la salle, son masque d'écran et les coins de l'écran central."""
    d = os.path.join(SALLE, plan)
    if plan not in _salle:
        _salle[plan] = (sorted(f for f in os.listdir(d) if f.endswith(".png")), json.load(open(os.path.join(d, "coins.json"))))
    fs, coins = _salle[plan]
    k = max(0, min(k, len(fs) - 1))
    img = cv2.imread(os.path.join(d, fs[k])).astype(np.float32)
    m = cv2.imread(os.path.join(d, "masque", fs[k]), cv2.IMREAD_GRAYSCALE)
    m = cv2.resize(m, (W, H)).astype(np.float32) / 255 if m is not None else np.zeros((H, W), np.float32)
    return img, m, np.float32(coins[str(k + 1)])


# ---------------------------------------------------------------- l'âge
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


# ---------------------------------------------------------------- 8 ans : « ingénieur », le rêve, les 200 vies
F_ING = ImageFont.truetype(FONTS + "georgiai.ttf", 176)
MOT = "ingénieur"


def plan_pont():
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
COLS_V, LIGNES_V = 20, 10
PAS_X, PAS_Y = 62, 57
GX0 = (W - (COLS_V - 1) * PAS_X) // 2
GY0 = 360
ELUS = {(5, 2), (14, 7)}
ROUGE = (214, 72, 46)


def silhouette(d, x, y, col, s=1.0):
    r = 6 * s
    d.ellipse([x - r, y - 17 * s - r, x + r, y - 17 * s + r], fill=col)
    d.rounded_rectangle([x - 9 * s, y - 9 * s, x + 9 * s, y + 13 * s], radius=int(7 * s), fill=col)


def ecran_ingenieur(t):
    tl = t - T_ING
    c = Image.new("RGB", (W, H), (9, 9, 10))
    d = ImageDraw.Draw(c)
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
    e_on = 0.0
    for r in range(LIGNES_V):
        for k in range(COLS_V):
            a = lisse((tl - 2.25 - 0.045 * (r + k)) / 0.35)
            if a <= 0:
                continue
            if (k, r) in ELUS:
                v = lisse((t - (T_ETEINT + 0.25)) / 0.4)
                col = tuple(int((b + (ro - b) * v) * a) for b, ro in zip((120, 114, 106), ROUGE))
                e_on = v
            else:
                eteint = lisse((t - T_ETEINT - 0.012 * ((k * 7 + r * 13) % 23)) / 0.45)
                g = 120 - 82 * eteint
                col = (int(g * a), int(g * 0.95 * a), int(g * 0.88 * a))
            silhouette(d, GX0 + k * PAS_X, GY0 + r * PAS_Y, col, 1.15)
    f = np.asarray(c).astype(np.float32)[:, :, ::-1]
    m = lisse((tl - 1.75) / 0.8)
    calque = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(calque)
    x = (W - dc.textlength(MOT, font=F_ING)) / 2
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
    halo = cv2.GaussianBlur(np.clip(f - 90, 0, 255), (0, 0), 14)
    rouge = np.clip(f[..., 2:3] - f[..., 1:2] - 60, 0, 255)
    f = f + 0.35 * halo + 0.9 * e_on * cv2.GaussianBlur(rouge * np.float32([0.25, 0.4, 1.0]), (0, 0), 10)
    f *= 1 - lisse((tl - 8.55) / 0.25)
    return f


# ---------------------------------------------------------------- l'écran central de la salle : ce qu'il montre
F_UI_T = ImageFont.truetype(FONTS + "georgia.ttf", 64)
F_UI_P = ImageFont.truetype(FONTS + "georgiai.ttf", 44)
F_UI_E = ImageFont.truetype(FONTS + "bahnschrift.ttf", 30)
OPTIONS = ["Continuer l'école", "Travailler pour aider sa famille"]


def ecran_choix(t):
    """Le premier choix, sur l'écran de la salle : deux cartes, un compte à rebours, le clic."""
    im = Image.new("RGB", (W, H), (12, 14, 18))
    d = ImageDraw.Draw(im)
    a = lisse((t - T_CHOIX) / 0.6)
    col = lambda c, k=1.0: tuple(int(v * a * k) for v in c)  # noqa: E731
    d.text((140, 110), "MANOJ  ·  10 ANS  ·  PREMIER CHOIX", font=F_UI_E, fill=col((130, 140, 150)))
    d.line([(140, 165), (W - 140, 165)], fill=col((60, 66, 74)), width=2)
    choisi = t >= T_CLIC
    for i, txt in enumerate(OPTIONS):
        x0, y0, x1, y1 = 160 + i * 820, 330, 160 + i * 820 + 780, 690
        sel = choisi and i == 0
        fond = (214, 72, 46) if sel else (22, 26, 32)
        k = 1.0 if (not choisi or sel) else 0.45
        d.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=col(fond, k), outline=col(CREME, 0.8 * k), width=3)
        tw = d.textlength(txt, font=F_UI_T)
        if tw > 700:
            mots = txt.split(" ")
            l1, l2 = " ".join(mots[:2]), " ".join(mots[2:])
            for j, l_ in enumerate((l1, l2)):
                d.text(((x0 + x1) / 2 - d.textlength(l_, font=F_UI_T) / 2, 440 + j * 80), l_, font=F_UI_T, fill=col(CREME, k))
        else:
            d.text(((x0 + x1) / 2 - tw / 2, 475), txt, font=F_UI_T, fill=col(CREME, k))
    # le compte à rebours : un trait qui se vide
    if T_DECOMPTE[0] - 0.2 <= t < T_CLIC + 0.3:
        p = 1 - np.clip((t - T_DECOMPTE[0]) / (T_DECOMPTE[1] - T_DECOMPTE[0]), 0, 1)
        d.line([(160, 790), (W - 160, 790)], fill=(60, 64, 70), width=6)
        d.line([(160, 790), (160 + (W - 320) * p, 790)], fill=CREME, width=6)
    return np.asarray(im).astype(np.float32)[:, :, ::-1]


def contenu_ecran(t):
    """Ce qui passe sur l'écran central de la salle au temps t."""
    if t < T_REVELE + 3.0:          # la lampe sur l'eau continue, puis Manoj, en direct
        ims = lire_extrait("34630320.mp4", 1.0, 0.8, (T_REVELE + 3.2 - T_DIYA) + 1.2, 0.45)
        f = etalonnage_doc(ims[min(int((t - T_DIYA) * FPS), len(ims) - 1)].astype(np.float32), 3)
        if t > T_REVELE + 2.0:
            q = lisse((t - (T_REVELE + 2.0)) / 1.0)
            f = f * (1 - q) + image_3d("funerailles", int((t - T_REVELE) * FPS) % 160) * q
        return f
    if t < T_CHOIX:
        f = image_3d("funerailles", int((t - T_REVELE) * FPS) % 160)
        if t > 54.5:                # « l'an prochain, il finit l'école » : la classe
            q = lisse((t - 54.5) / 0.8)
            f = f * (1 - q) + image_3d("classe", int((t - 54.5) * FPS) % 100) * q
        return f
    f = ecran_choix(t)
    if t < T_CHOIX + 0.6:
        q = lisse((t - T_CHOIX) / 0.6)
        f = image_3d("classe", int((t - 54.5) * FPS) % 100) * (1 - q) + f * q
    return f


# ---------------------------------------------------------------- la salle embellie par Higgsfield (Bruno, 09/11/2026)
sys.path.insert(0, os.path.join(ICI, "..", "S08"))
import hf  # noqa: E402

HF7 = os.path.join(M, "S07", "higgsfield")
HF_S07 = {  # plan : (vidéo Kling, durée du plan, image Blender de départ, image Blender correspondante)
    "revele": ("revele.mp4", 6.0, "depart/revele.png", 143),
    "large": ("large.mp4", 10.0, "depart/large.png", 0),
    "epaule": ("epaule.mp4", 8.0, "depart/epaule.png", 0),
    "regard": ("regard.mp4", 6.0, "depart/regard.png", 0),
}
PLEIN_ = np.float32([[0, 0], [W, 0], [W, H], [0, H]])


def plan_salle(plan, k, t):
    v = HF_S07.get(plan)
    c = contenu_ecran(t)
    if v and os.path.exists(os.path.join(HF7, v[0])):
        vid, dur, ref, kb = v
        chemin = os.path.join(HF7, vid)
        tl = k / FPS
        _, mb, cb = salle(plan, kb)
        co0 = hf.report(os.path.join(HF7, ref), chemin, cb, os.path.join(HF7, vid + ".coins.json"))
        suivi = hf.suivre(chemin, dur, co0, os.path.join(HF7, vid + ".suivi.json"))
        img = hf.image(chemin, dur, tl)
        co = suivi[max(0, min(int(tl * FPS), len(suivi) - 1))].copy()
        if plan == "revele":            # on recule depuis l'écran : la poussée inverse, faite au montage
            q = 1 - doux(tl / dur)
            return hf_traverser(img, co, c, q)
        m = cv2.warpPerspective(mb, cv2.getPerspectiveTransform(cb, co), (W, H))
    else:
        img, m, co = salle(plan, k)
    Hm = cv2.getPerspectiveTransform(PLEIN_, co)
    e = cv2.warpPerspective(c, Hm, (W, H), flags=cv2.INTER_LINEAR)
    m = cv2.GaussianBlur(m, (0, 0), 0.8)[..., None]
    # l'écran émet : un peu plus lumineux qu'une image, et il bave légèrement dans la pénombre
    e = e * 1.05 + 6
    out = img * (1 - m) + e * m
    out += 0.18 * cv2.GaussianBlur(e * m, (0, 0), 22)
    return out


def hf_traverser(img, coins, contenu, q):
    """L'écran grandit jusqu'à remplir le cadre (q = 1) : toute l'image de la salle suit la même homographie."""
    quad = coins + (PLEIN_ - coins) * q
    Hr = cv2.getPerspectiveTransform(coins, quad)
    salle_ = cv2.warpPerspective(img, Hr, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    e = cv2.warpPerspective(contenu, cv2.getPerspectiveTransform(PLEIN_, quad), (W, H), flags=cv2.INTER_LINEAR)
    e = e * 1.05 + 6
    mk = np.zeros((H, W), np.float32)
    cv2.fillConvexPoly(mk, np.round(quad * 4).astype(np.int32), 1.0, lineType=cv2.LINE_AA, shift=2)
    mk = cv2.GaussianBlur(mk, (0, 0), 0.7)[..., None]
    out = salle_ * (1 - mk) + e * mk
    v = math.sin(math.pi * q)
    if v > 0.4:                          # au plus fort du passage, le signal se dédouble un instant
        d_ = int(round(5 * (v - 0.4) / 0.6))
        if d_:
            out[..., 2] = np.roll(out[..., 2], d_, axis=1)
            out[..., 0] = np.roll(out[..., 0], -d_, axis=1)
    return out + 0.18 * (1 - q) * cv2.GaussianBlur(e * mk, (0, 0), 22)


# ---------------------------------------------------------------- les sous-titres provisoires (voix à venir)
F_ST = ImageFont.truetype(FONTS + "georgiai.ttf", 42)
F_QUI = ImageFont.truetype(FONTS + "bahnschrift.ttf", 22)
QUI = {"narration": "", "lui": "LUI", "elle": "ELLE"}


def sous_titres(f, t):
    for qui, texte, t0, dur in VOIX_A_VENIR:
        if t0 - 0.1 <= t <= t0 + dur + 0.3:
            o = lisse((t - t0 + 0.1) / 0.2) * (1 - lisse((t - (t0 + dur + 0.1)) / 0.2))
            c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(c)
            tw = d.textlength(texte, font=F_ST)
            x, y = (W - tw) / 2, 960
            d.rounded_rectangle([x - 26, y - 14, x + tw + 26, y + 62], radius=10, fill=(0, 0, 0, 150))
            if QUI[qui]:
                d.text((x, y - 40), QUI[qui], font=F_QUI, fill=(200, 200, 200, 230))
            d.text((x, y), texte, font=F_ST, fill=(*CREME, 255))
            a = np.asarray(c).astype(np.float32)
            al = a[..., 3:4] / 255 * o
            f = f * (1 - al) + a[..., :3][..., ::-1] * al
    return f


# ---------------------------------------------------------------- l'onde du dialogue (Remotion : remotion/Dialogue.tsx, dialogue.py)
DIALOGUE = os.path.join(M, "S07", "dialogue")
_dial = json.load(open(os.path.join(RACINE, "public", "dialogue", "s07.json"))) if os.path.exists(
    os.path.join(RACINE, "public", "dialogue", "s07.json")) else None


def onde_dialogue(f, n):
    if not _dial or not os.path.isdir(DIALOGUE):
        return f
    k = n - _dial["debut"]
    if not 0 <= k < len(_dial["images"]):
        return f
    fs = sorted(x for x in os.listdir(DIALOGUE) if x.endswith(".png")) if not hasattr(onde_dialogue, "fs") else onde_dialogue.fs
    onde_dialogue.fs = fs
    if k >= len(fs):
        return f
    o = cv2.imread(os.path.join(DIALOGUE, fs[k]), cv2.IMREAD_UNCHANGED)
    if o is None or o.shape[2] < 4:
        return f
    al = o[..., 3:4].astype(np.float32) / 255
    return f * (1 - al) + o[..., :3].astype(np.float32) * al


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
        if nom == "18070270.mp4":
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
    elif genre == "ingenieur":
        f = ecran_ingenieur(t)
    elif genre == "salle":
        plan, decal = src
        f = plan_salle(plan, k + int(decal * FPS), t)
    else:
        f = np.zeros((H, W, 3), np.float32)
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
    if genre == "d3" and src[0] == "huit_ans":
        ouv = 1 - doux((t - (t1 - 0.45)) / 0.45)
    if genre == "d3" and src[0] == "classe":
        ouv = doux((t - t0) / 0.45)
    f = fenetre(c, ouv, pl)
    f = sous_titres(f, t)
    f = onde_dialogue(f, n)
    f *= lisse(t / 0.12)
    f += np.random.default_rng(n).normal(0, 1.8, f.shape).astype(np.float32)
    return f


SON_SEUL = os.environ.get("SON_SEUL") == "1"
if not SON_SEUL:
    if "--test" in sys.argv:
        temps = os.environ.get("TEMPS")
        temps = [float(x) for x in temps.split(",")] if temps else (8.0, 15.0, 23.5, 28.5, 36.0, 40.5, 42.0, 44.5, 52.0, 60.0, 66.0, 70.2, 72.5)
        for t in temps:
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


tic = lire("tic_doux.wav")
o_t = crete(tic[:SR])
un_tic = tic[max(0, o_t - 100):o_t + int(0.06 * SR)] * fondu(o_t + int(0.06 * SR) - max(0, o_t - 100), 0.002, 0.03)[:, None]
bil = lire("billets_compter.wav")
# 5 ans : la cloche, la cour, l'école, les billets
poser(extrait("cloche_ecole.wav", 0.05, 1.8, 0.002, 0.8), 0.0, db(-9))
mix += stereo("classe_inde.wav", 30.0) * (db(-20) * env(0, 1.9, 0.05, 0.3))[:, None]
mix += stereo("village_amethi.wav", 70.0) * (db(-25) * env(1.7, 4.9, 0.3, 0.3))[:, None]
poser(bil[int(2 * SR):int(3.7 * SR)] * fondu(int(1.7 * SR), 0.02, 0.3)[:, None], 4.75, db(-10))
# 8 ans : la nuit, les grands
mix += stereo("grillons_nuit.wav", 50.0) * (db(-21) * env(T_HUIT, T_ING, 0.8, 0.5))[:, None]
# « ingénieur » : presque le silence, une note tenue ; les vies, un frémissement ; elles s'éteignent ; deux notes
tn = np.arange(int(3.0 * SR)) / SR
note = (np.sin(2 * np.pi * 220 * tn) + 0.5 * np.sin(2 * np.pi * 329.6 * tn) + 0.25 * np.sin(2 * np.pi * 440 * tn))
note *= np.minimum(1, tn / 0.4) * np.exp(-tn / 1.6) * 0.18
poser(np.stack([note, note], 1), T_ING + 0.25, 1.0)
mix += stereo("ambiance_grand_hall.wav", 30.0) * (db(-28) * env(T_ING, T_CLASSE, 0.2, 0.1))[:, None]
for r in range(10):
    poser(un_tic, T_ING + 2.25 + 0.09 * r, db(-31))
tw = np.arange(int(1.2 * SR)) / SR
souffle = np.sin(2 * np.pi * (110 * tw - 25 * tw * tw)) * np.exp(-tw / 0.5) * 0.1
poser(np.stack([souffle, souffle], 1), T_ETEINT, 1.0)
for k_, f0 in enumerate((659.3, 880.0)):
    tc = np.arange(int(1.6 * SR)) / SR
    cl = np.sin(2 * np.pi * f0 * tc) * np.exp(-tc / 0.5) * 0.05 * np.minimum(1, tc / 0.01)
    poser(np.stack([cl, cl], 1), T_ETEINT + 0.3 + 0.12 * k_, 1.0)
# la classe : le murmure d'une classe, lointain
mix += stereo("classe_inde.wav", 60.0) * (db(-21) * env(T_CLASSE, T_BILLET, 0.3, 0.4))[:, None]
# la dette : les billets, la nuit
mix += stereo("grillons_nuit.wav", 80.0) * (db(-23) * env(T_BILLET, T_FLEUVE, 0.4, 0.5))[:, None]
poser(bil[int(6 * SR):int(7.2 * SR)] * fondu(int(1.2 * SR), 0.05, 0.6)[:, None], T_BILLET + 0.05, db(-17))
# 10 ans : le fleuve, le soir ; le piano porte le deuil, et s'efface quand on découvre la salle
mix += stereo("soir_rural.wav", 20.0) * (db(-19) * env(T_FLEUVE, T_REVELE + 1.0, 0.4, 1.5))[:, None]
mus = stereo("remembering.wav", 0.0, os.path.join(M, "musique"))
mix += mus * (db(-15) * env(T_FLEUVE - 0.3, T_REVELE + 3.0, 1.2, 2.5))[:, None]
# la salle : le souffle des machines, le bourdonnement des écrans, une tension grave sous la discussion
mix += stereo("ambiance_grand_hall.wav", 120.0) * (db(-15) * env(T_REVELE, DUREE, 1.0, 1.0))[:, None]
mix += stereo("bourdonnement_ordinateur.wav", 40.0) * (db(-13) * env(T_REVELE, DUREE, 1.0, 1.0))[:, None]
mix += stereo("bourdonnement_lumiere.wav", 20.0) * (db(-24) * env(T_REVELE, DUREE, 1.0, 1.0))[:, None]
mix += stereo("espace_drone.wav", 30.0) * (db(-24) * env(T_LARGE, T_NOIR, 3.0, 0.3))[:, None]
# le choix : le décompte (trois tics), le clic
for k in range(3):
    poser(un_tic, T_DECOMPTE[0] + k * 1.0, db(-13))
clics = lire("souris_clics.wav")
o_c = crete(clics[int(5 * SR):int(8 * SR)]) + int(5 * SR)
poser(clics[o_c - 200:o_c + int(0.15 * SR)], T_CLIC, db(-6))

# les voix : la narration (prise 1 et phrases nouvelles), puis les deux simulateurs, dans la salle
rng = np.random.default_rng(7)
tr = np.arange(int(0.35 * SR)) / SR
piece = rng.normal(0, 1, len(tr)) * np.exp(-tr / 0.05)       # une petite pièce, sèche et proche
piece[0] = 0
piece *= 0.08 / np.sqrt((piece ** 2).sum())
voix = np.zeros(Ns)
for fichier, phrases, salle_ in ((VOIX, PHRASES, False), (VOIX_REVE, PHRASES_REVE, False), (VOIX_B, PHRASES_B, False),
                                 (VOIX_C, PHRASES_C, False), (VOIX_LUI, PHRASES_LUI, True), (VOIX_LUI2, PHRASES_LUI2, True),
                                 (VOIX_ELLE, PHRASES_ELLE, True)):
    a_ = lire_audio(fichier, mono=True).astype(np.float64)
    actif = np.abs(a_) > 0.01
    a_ *= db(-17.2 - 20 * np.log10(np.sqrt((a_[actif] ** 2).mean())))
    for (a, b), pos in phrases:
        s_ = a_[int(a * SR):int(b * SR)]
        s_ = s_ * fondu(len(s_), 0.01, 0.06)
        if salle_:
            s_ = np.concatenate([s_, np.zeros(len(piece))])
            s_ = s_ + np.convolve(s_, piece)[:len(s_)]
        j = int(pos * SR)
        f_ = min(Ns, j + len(s_))
        voix[j:f_] += s_[:f_ - j]
env_voix = np.convolve(np.abs(voix) > 1e-3, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode="same")
mix *= (1 - 0.4 * np.clip(env_voix * 3, 0, 1))[:, None]
mix += voix[:, None] * db(-3.5)
mix *= fondu(Ns, 0.03, 0.08)[:, None]

GAIN = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
wav = os.path.join(OUT, "S07_son.wav")
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN))
final = os.path.join(OUT, "S07_v2.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, "S07_image.mp4"), "-i", wav, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", final], check=True)
print("écrit :", final)
