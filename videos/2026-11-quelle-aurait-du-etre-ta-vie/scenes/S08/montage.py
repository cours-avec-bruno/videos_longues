"""S08 · 11 à 14 ans : le bon choix ne suffit pas. Montage, motion design et son.

Grammaire (voir scene.md) :
  - la salle = ceux qui regardent (bleu nuit, chrome) ; l'écran central y affiche ce qui arrive à Manoj ;
  - on ENTRE dans l'écran : ses quatre coins s'envolent jusqu'à devenir la fenêtre d'interface (la vie de Manoj),
    et l'on en RESSORT par le même chemin ; on entre une dernière fois, en plein écran, dans les données ;
  - les données : 200 silhouettes sur un noir chaud, crème et rouge, comme « ingénieur » en S07 ; Manoj est la rouge.
  - un élément rouge porte la continuité : la carte « Continuer l'école » choisie en S07 se replie en un curseur rouge,
    qui écrit la conséquence ; plus tard, la silhouette rouge reste seule, et le spectateur apparaît à côté d'elle.

Usage : python montage.py   ->  medias/S08/S08_v1.mp4     (--test <dossier> : images fixes ; TEMPS=1.0,2.5 ; SON_SEUL=1)
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
from fenetre import FH, FOND, FW, fenetre  # noqa: E402

M = os.path.join(ICI, "..", "..", "medias")
SALLE = os.path.join(M, "S08", "salle")
D3 = os.path.join(M, "S08", "3d")
PX = os.path.join(M, "pexels", "s08")
SONS = os.path.join(M, "sons", "epidemic")
OUT = os.path.join(M, "S08")
W, H, FPS = 1920, 1080, 24
FONTS = "C:/Windows/Fonts/"
CREME = (238, 230, 216)
ROUGE = (214, 72, 46)          # RVB
NOIR_CHAUD = (9, 9, 10)


def lisse(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def doux(p):
    p = min(1.0, max(0.0, p))
    return p * p * p * (p * (p * 6 - 15) + 10)


def expo_out(p):
    p = min(1.0, max(0.0, p))
    return 1 - 2 ** (-10 * p) if p < 1 else 1.0


def expo_inout(p):
    p = min(1.0, max(0.0, p))
    if p in (0.0, 1.0):
        return p
    return 2 ** (20 * p - 10) / 2 if p < 0.5 else (2 - 2 ** (-20 * p + 10)) / 2


# ---------------------------------------------------------------- le déroulé
T_RECUL = 10.3            # plan de côté : il se recule
T_ENTRE = 14.8           # on entre dans l'écran (0,9 s) -> la fenêtre : le portail
D_ENTRE = 0.9
T_CHEVRES = 20.6         # plein écran : le garçon et ses chèvres
T_BETES = 24.6           # la fenêtre : 14 ans
T_SORT = 31.2            # on ressort de la fenêtre -> la salle, elle de profil
D_SORT = 0.9
T_PLONGE = 34.8          # on entre dans l'écran, en plein écran : les données
D_PLONGE = 0.8
T_SEUL = 40.4            # les autres vies s'effacent ; la rouge reste ; vous apparaissez
T_NOIR = 48.4
DUREE = 49.2
T_MORPH = 0.42

# les voix : (fichier, [((début, fin) dans la prise, position)], dans la salle ?)
V = os.path.join(M, "voix")
VOIX = [
    (os.path.join(V, "S07_elle_prise2.mp3"), [((11.68, 12.12), 0.3), ((13.14, 15.20), 0.95)], True),  # Bon choix. Reste à savoir…
    (os.path.join(V, "S08_lui_prise1.mp3"), [((4.57, 5.44), 12.75)], True),                       # … Même ça.                        # … Même ça.
    (os.path.join(V, "S08_prise1.mp3"), [((5.32, 6.83), 21.15),                                  # Il passe ses journées avec les bêtes.
                                         ((8.15, 11.09), 25.8),                                  # À quatorze ans, il envie ses amis qui vont à l'école.
                                         ((12.22, 15.44), 43.6)], False),                        # Et vous, à onze ans… qui payait…
    (os.path.join(V, "S08_elle_prise1.mp3"), [((3.99, 6.24), 32.25),                             # Les choix changent les probabilités.
                                              ((7.08, 9.62), 37.0)], True),                      # Ils ne décident jamais du résultat.
]
N = int(round(DUREE * FPS))

# ---------------------------------------------------------------- les sources
_salle, _d3, _videos = {}, {}, {}


def salle(plan, k):
    d = os.path.join(SALLE, plan)
    if plan not in _salle:
        _salle[plan] = (sorted(f for f in os.listdir(d) if f.endswith(".png")), json.load(open(os.path.join(d, "coins.json"))))
    fs, coins = _salle[plan]
    k = max(0, min(int(k), len(fs) - 1))
    img = cv2.imread(os.path.join(d, fs[k])).astype(np.float32)
    m = cv2.imread(os.path.join(d, "masque", fs[k]), cv2.IMREAD_GRAYSCALE)
    m = cv2.resize(m, (W, H)).astype(np.float32) / 255 if m is not None else np.zeros((H, W), np.float32)
    return img, m, np.float32(coins[str(k + 1)])


def image_3d(plan, k):
    d = os.path.join(D3, plan)
    if plan not in _d3:
        _d3[plan] = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    fs = _d3[plan]
    return cv2.imread(os.path.join(d, fs[max(0, min(int(k), len(fs) - 1))])).astype(np.float32)


def lire_extrait(nom, debut, vitesse, duree, cy=0.5):
    cle = (nom, debut, vitesse)
    if cle not in _videos:
        n = int(math.ceil(duree * FPS)) + 8
        vf = (f"setpts=PTS/{vitesse},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}:(iw-{W})/2:(ih-{H})*{cy}")
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(debut), "-i", os.path.join(PX, nom), "-vf", vf,
                              "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
        im = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
        if len(im) < n:
            im = np.concatenate([im, np.repeat(im[-1:], n - len(im), 0)])
        _videos[cle] = im
    return _videos[cle]


# ---------------------------------------------------------------- l'écran central : la carte choisie devient le curseur
F_UI_T = ImageFont.truetype(FONTS + "georgia.ttf", 64)
F_UI_E = ImageFont.truetype(FONTS + "bahnschrift.ttf", 30)
F_LIGNE = ImageFont.truetype(FONTS + "georgiai.ttf", 66)
LIGNES = ["Votre famille n'a pas pu payer", "les frais de scolarité ; vous avez dû", "renoncer à poursuivre vos études."]
O_ECRAN = 2.8            # Sara parle d'abord (« Bon choix… ») ; la carte se replie ensuite
T_TAPE = (1.45 + O_ECRAN, 5.0 + O_ECRAN)
CARTE = (160, 330, 940, 690)                       # la carte « Continuer l'école », comme à la fin de S07
NB_CAR = sum(len(l) for l in LIGNES)


def ecran_ligne(t):
    """t : temps de la scène ; la carte reste telle qu'à la fin de S07 pendant la réplique de Sara."""
    tl = t - O_ECRAN
    im = Image.new("RGB", (W, H), (12, 14, 18))
    d = ImageDraw.Draw(im)
    d.text((140, 110), "MANOJ  ·  10 ANS  ·  PREMIER CHOIX", font=F_UI_E, fill=(130, 140, 150))
    d.line([(140, 165), (W - 140, 165)], fill=(60, 66, 74), width=2)
    # la carte non choisie (déjà éteinte à la fin de S07) se fond dans le fond de l'écran
    a_autre = 1 - lisse(tl / 0.55)
    if a_autre > 0:
        fond = (12, 14, 18)
        k = 0.45
        d.rounded_rectangle([980, 330, 1760, 690], radius=24,
                            fill=_melange(fond, tuple(int(v * k) for v in (22, 26, 32)), a_autre),
                            outline=_melange(fond, tuple(int(v * 0.8 * k) for v in CREME), a_autre), width=3)
        for j, l_ in enumerate(("Travailler pour", "aider sa famille")):
            d.text((1370 - d.textlength(l_, font=F_UI_T) / 2, 440 + j * 80), l_, font=F_UI_T,
                   fill=_melange(fond, tuple(int(v * k) for v in CREME), a_autre))
    # la carte choisie se replie en un curseur rouge, à l'endroit où la ligne va s'écrire
    q = expo_inout((tl - 0.45) / 0.85)
    x_tape, y_tape = 160, 400
    cur = (x_tape, y_tape + 6, x_tape + 6, y_tape + 72)
    r = [CARTE[i] + (cur[i] - CARTE[i]) * q for i in range(4)]
    if q < 1:
        d.rounded_rectangle(r, radius=max(2, int(24 * (1 - q))), fill=(ROUGE[0], ROUGE[1], ROUGE[2]))
        if q < 0.35:
            a_txt = 1 - q / 0.35
            txt = "Continuer l'école"
            tw = d.textlength(txt, font=F_UI_T)
            d.text(((CARTE[0] + CARTE[2]) / 2 - tw / 2, 475), txt, font=F_UI_T, fill=tuple(int(c * a_txt + ROUGE[i] * (1 - a_txt))
                                                                                                for i, c in enumerate(CREME)))
    # la ligne qui s'écrit, lettre à lettre ; le curseur rouge la précède
    n = int(NB_CAR * np.clip((t - T_TAPE[0]) / (T_TAPE[1] - T_TAPE[0]), 0, 1)) if t >= T_TAPE[0] else 0
    reste = n
    x_c, y_c = x_tape, y_tape
    for j, ligne in enumerate(LIGNES):
        y = y_tape + j * 96
        part = ligne[:max(0, reste)]
        if part:
            d.text((x_tape, y), part, font=F_LIGNE, fill=CREME)
        if reste <= len(ligne):
            x_c, y_c = x_tape + d.textlength(part, font=F_LIGNE) + 8, y
            break
        reste -= len(ligne)
    if q >= 1:
        allume = t < T_TAPE[1] or (int((t - T_TAPE[1]) * 2.2) % 2 == 0)
        if allume:
            d.rectangle([x_c, y_c + 8, x_c + 6, y_c + 74], fill=ROUGE)
    return np.asarray(im).astype(np.float32)[:, :, ::-1]


# ---------------------------------------------------------------- les données : 200 vies nées comme lui
COLS, LIGNES_G = 20, 10
PAS_X, PAS_Y = 62, 57
GX0 = (W - (COLS - 1) * PAS_X) // 2
GY0 = (H - (LIGNES_G - 1) * PAS_Y) // 2 + 14
MANOJ = (9, 4)
_rng = np.random.default_rng(11)
_cases = [(c, r) for r in range(LIGNES_G) for c in range(COLS) if (c, r) != MANOJ]
_rng.shuffle(_cases)
JAMAIS = set(_cases[:19])                 # ne rencontrent jamais ce choix (mortes jeunes, ou pas d'école du tout)
TRAVAIL = set(_cases[19:24])              # choisissent de travailler
ECHEC = set(_cases[24:43]) | {MANOJ}      # choisissent l'école… et n'y vont pas (une vingtaine, dont lui)
T_GRILLE = 33.4           # elles apparaissent sur l'écran de la salle
T_ALLUME = 35.7           # celles qui choisissent l'école s'allument (une vague qui part de lui)
T_ETEINT = 38.15          # « … jamais du résultat » : une vingtaine s'éteignent, lui aussi


def silhouette(d, x, y, col, s=1.0):
    r = 6 * s
    d.ellipse([x - r, y - 17 * s - r, x + r, y - 17 * s + r], fill=col)
    d.rounded_rectangle([x - 9 * s, y - 9 * s, x + 9 * s, y + 13 * s], radius=int(7 * s), fill=col)


def _melange(a, b, q):
    return tuple(int(x + (y - x) * q) for x, y in zip(a, b))


def donnees(t):
    """La grille (BGR float). Après T_SEUL : les autres s'effacent, la rouge vient au centre, vous apparaissez."""
    im = Image.new("RGB", (W, H), NOIR_CHAUD)
    d = ImageDraw.Draw(im)
    seul = lisse((t - T_SEUL) / 0.8)
    rouge_on = 0.0
    for r in range(LIGNES_G):
        for c in range(COLS):
            dist = math.hypot(c - MANOJ[0], (r - MANOJ[1]) * 1.1)
            app = lisse((t - T_GRILLE - 0.03 * (r + c)) / 0.4)
            if app <= 0:
                continue
            base = (54, 52, 50)
            col = base
            if (c, r) in JAMAIS:
                col = (30, 29, 28)
            elif (c, r) not in TRAVAIL:
                on = lisse((t - T_ALLUME - 0.045 * dist) / 0.3)
                cible = ROUGE if (c, r) == MANOJ else (150, 144, 134)
                col = _melange(base, cible, on)
                if (c, r) in ECHEC:
                    k = sorted(ECHEC).index((c, r))
                    off = lisse((t - T_ETEINT - (0.9 if (c, r) == MANOJ else 0.035 * k)) / 0.45)
                    eteint = (96, 40, 30) if (c, r) == MANOJ else (40, 38, 36)
                    col = _melange(col, eteint, off)
                if (c, r) == MANOJ:
                    rouge_on = on
            col = _melange((0, 0, 0), col, app)
            if (c, r) == MANOJ:
                continue                       # dessinée à part (elle se déplace à la fin)
            if seul > 0:
                col = _melange(col, NOIR_CHAUD, seul)
            silhouette(d, GX0 + c * PAS_X, GY0 + r * PAS_Y, col, 1.15)
    # la rouge : à sa place dans la grille, puis seule au centre, plus grande
    if t >= T_GRILLE:
        mv = expo_inout((t - (T_SEUL + 0.4)) / 1.4)
        x0, y0 = GX0 + MANOJ[0] * PAS_X, GY0 + MANOJ[1] * PAS_Y
        xm, ym, sm = W / 2 - 210, H / 2 + 60, 1.15 + (6.5 - 1.15) * mv
        x, y = x0 + (xm - x0) * mv, y0 + (ym - y0) * mv
        if (MANOJ in ECHEC) and t > T_ETEINT:
            col_m = _melange(ROUGE, (96, 40, 30), lisse((t - T_ETEINT - 0.9) / 0.45))
        else:
            col_m = _melange((54, 52, 50), ROUGE, rouge_on)
        app_m = lisse((t - T_GRILLE - 0.03 * (MANOJ[0] + MANOJ[1])) / 0.4)
        silhouette(d, x, y, _melange((0, 0, 0), col_m, app_m), sm)
        # vous : une silhouette crème apparaît à côté (petit dépassement, puis immobile)
        v = (t - (T_SEUL + 2.6)) / 0.55
        if v > 0:
            p = min(1.0, v)
            sp = 1 + 0.05 * math.sin(math.pi * p) if p < 1 else 1.0
            a = lisse(v)
            silhouette(d, W / 2 + 210, H / 2 + 60 + 22 * (1 - expo_out(p)), _melange(NOIR_CHAUD, (196, 188, 174), a), 6.5 * sp)
    f = np.asarray(im).astype(np.float32)[:, :, ::-1]
    # la lumière : un halo sur ce qui brille, un peu plus de rouge autour de lui
    halo = cv2.GaussianBlur(np.clip(f - 110, 0, 255), (0, 0), 14)
    rouge = np.clip(f[..., 2:3] - f[..., 1:2] - 50, 0, 255)
    f = f + 0.3 * halo + 0.7 * cv2.GaussianBlur(rouge * np.float32([0.25, 0.4, 1.0]), (0, 0), 16)
    f = np.minimum(f, 245)
    # vignette douce
    return f * _VIGNETTE


_yy, _xx = np.mgrid[0:H, 0:W]
_VIGNETTE = (1 - 0.35 * (((_xx - W / 2) / (W / 2)) ** 2 + ((_yy - H / 2) / (H / 2)) ** 2) / 2).astype(np.float32)[..., None]


# ---------------------------------------------------------------- l'âge
F_AGE = ImageFont.truetype(FONTS + "georgia.ttf", 92)


def calque_texte(texte, font, xy, couleur=CREME):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(c).text(xy, texte, font=font, fill=(*couleur, 255))
    a = np.asarray(c).astype(np.float32)
    return a[..., :3][..., ::-1].copy(), a[..., 3] / 255, cv2.GaussianBlur(a[..., 3], (0, 0), 10) / 255


AGES = [("11 ans", T_ENTRE + 0.7, T_CHEVRES - 0.5), ("14 ans", T_BETES + 0.3, T_SORT - 0.4)]
CAL_AGES = {a: calque_texte(a, F_AGE, (140, 880)) for a, _, _ in AGES}


def ajouter_age(f, t):
    for a, t0, t1 in AGES:
        if t0 - 0.05 <= t <= t1 + 0.4:
            o = lisse((t - t0) / 0.45) * (1 - lisse((t - t1) / 0.35))
            if o > 0:
                rgb, al, om = CAL_AGES[a]
                dy = int(round(10 * (1 - lisse((t - t0) / 0.45))))
                if dy:
                    rgb, al, om = (np.roll(v, dy, axis=0) for v in (rgb, al, om))
                f = f * (1 - 0.45 * o * om[..., None])
                f = f * (1 - o * al[..., None]) + rgb * (o * al[..., None])
    return f


# ---------------------------------------------------------------- les incrustations dans la salle
PLEIN = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
X0F, Y0F = (W - FW) // 2, (H - FH) // 2
RECT_FENETRE = np.float32([[X0F, Y0F], [X0F + FW, Y0F], [X0F + FW, Y0F + FH], [X0F, Y0F + FH]])


def emettre(e):
    return e * 1.05 + 6


def dans_l_ecran(img, m, coins, contenu):
    """L'image de la salle, avec `contenu` sur l'écran central (comme en S07)."""
    Hm = cv2.getPerspectiveTransform(PLEIN, coins)
    e = emettre(cv2.warpPerspective(contenu, Hm, (W, H), flags=cv2.INTER_LINEAR))
    m = cv2.GaussianBlur(m, (0, 0), 0.8)[..., None]
    out = img * (1 - m) + e * m
    return out + 0.18 * cv2.GaussianBlur(e * m, (0, 0), 22)


def traverser(img, coins, cible, contenu, q, assombrir=True):
    """On traverse l'écran : toute l'image est reprojetée pour que l'écran (coins) aille sur `cible`
    (q : 0 = la salle telle quelle, 1 = l'écran a atteint la cible)."""
    quad = coins + (cible - coins) * q
    Hr = cv2.getPerspectiveTransform(coins, quad)
    fond = np.float32(FOND)
    salle_ = cv2.warpPerspective(img, Hr, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=tuple(float(v) for v in fond))
    if assombrir:
        salle_ = salle_ * (1 - 0.85 * q) + fond * (0.85 * q)
    Hc = cv2.getPerspectiveTransform(PLEIN, quad)
    e = cv2.warpPerspective(contenu, Hc, (W, H), flags=cv2.INTER_LINEAR)
    e = emettre(e) if q < 1 else e
    mk = np.zeros((H, W), np.float32)
    cv2.fillConvexPoly(mk, np.round(quad * 4).astype(np.int32), 1.0, lineType=cv2.LINE_AA, shift=2)
    mk = cv2.GaussianBlur(mk, (0, 0), 0.7)[..., None]
    out = salle_ * (1 - mk) + e * mk
    # un léger flou de mouvement radial pendant la traversée (vitesse max au milieu)
    v = math.sin(math.pi * q)
    if v > 0.15:
        z = 1 + 0.025 * v
        out = 0.5 * out + 0.5 * cv2.warpAffine(out, cv2.getRotationMatrix2D((float(quad[:, 0].mean()), float(quad[:, 1].mean())), 0, z),
                                                 (W, H), borderMode=cv2.BORDER_REFLECT)
    return out


# ---------------------------------------------------------------- les plans
def portail(t):
    return image_3d("portail", (t - T_ENTRE) * FPS)


def betes(t):
    return image_3d("betes", (t - T_BETES) * FPS)


def chevres(t):
    ims = lire_extrait("14275268.mp4", 0.6, 0.85, (T_BETES - T_CHEVRES) + 1.5)
    k = int((t - T_CHEVRES) * FPS)
    f = ims[max(0, min(k, len(ims) - 1))].astype(np.float32)
    z = 1.06 + 0.04 * (t - T_CHEVRES) / (T_BETES - T_CHEVRES)
    f = cv2.warpAffine(f, cv2.getRotationMatrix2D((W * 0.42, H * 0.4), 0, z), (W, H), borderMode=cv2.BORDER_REFLECT)
    f = etalonnage_doc(f, k)
    # plus chaud et plus dense que la source (midi blanc) : on rejoint la fin de journée du tableau suivant
    f = f * np.float32([0.78, 0.9, 1.06]) - 6
    return np.clip(f, 0, 255)


def contenu_sara(t):
    """L'écran pendant le plan de profil : la fin du tableau qui s'assombrit, puis la grille qui s'allume."""
    b = betes(T_SORT) * (1 - 0.6 * lisse((t - T_SORT - 0.6) / 1.2))
    if t < T_GRILLE - 0.3:
        return b
    q = lisse((t - (T_GRILLE - 0.3)) / 0.5)
    return b * (1 - q) + donnees(t) * q


def image(n):
    t = n / FPS
    if t < T_RECUL:                                                     # P01 : la ligne s'écrit sur l'écran
        img, m, co = salle("s08_ecran", t * FPS * 7.5 / T_RECUL)     # la poussée, ralentie sur toute la durée
        f = dans_l_ecran(img, m, co, ecran_ligne(t))
    elif t < T_ENTRE:                                                   # P02 : il se recule (« … Même ça. »)
        img, m, co = salle("s08_recul", (t - T_RECUL) * FPS)
        f = img
    elif t < T_ENTRE + D_ENTRE:                                         # P03a : on entre dans l'écran -> la fenêtre
        q = doux((t - T_ENTRE) / D_ENTRE)
        img, m, co = salle("s08_ecran", 10_000)
        c = ecran_ligne(T_RECUL) * (1 - lisse((t - T_ENTRE) / 0.35)) + portail(t) * lisse((t - T_ENTRE) / 0.35)
        f = traverser(img, co, RECT_FENETRE, c, q)
        f = f * (1 - lisse((q - 0.7) / 0.3)) + fenetre(ajouter_age(c, t)) * lisse((q - 0.7) / 0.3)
    elif t < T_CHEVRES:                                                 # P03 : le portail
        f = fenetre(ajouter_age(portail(t), t))
    elif t < T_BETES:                                                   # P04 : les chèvres, plein écran
        dt = t - T_CHEVRES
        c = chevres(t)
        pl = 1.0
        if dt < T_MORPH:
            q = doux(dt / T_MORPH)
            pl = q
            c = ajouter_age(portail(t), t) * (1 - lisse(dt / (T_MORPH * 0.6))) + c * lisse(dt / (T_MORPH * 0.6))
        f = fenetre(c, 1.0, pl)
    elif t < T_SORT:                                                    # P05 : 14 ans, dans la fenêtre
        dt = t - T_BETES
        c = ajouter_age(betes(t), t)
        pl = 0.0
        if dt < T_MORPH:
            q = doux(dt / T_MORPH)
            pl = 1 - q
            c = chevres(t) * (1 - lisse(dt / (T_MORPH * 0.6))) + c * lisse(dt / (T_MORPH * 0.6))
        f = fenetre(c)
    elif t < T_PLONGE:                                                  # P06 : on ressort ; elle, de profil
        img, m, co = salle("s08_sara", (t - T_SORT) * FPS)
        c = contenu_sara(t)
        if t < T_SORT + D_SORT:
            q = doux((t - T_SORT) / D_SORT)
            f = traverser(img, co, RECT_FENETRE, ajouter_age(c, t), 1 - q)
            f = f * (1 - lisse((0.3 - q) / 0.3)) + fenetre(ajouter_age(betes(t), t)) * lisse((0.3 - q) / 0.3)
        else:
            f = dans_l_ecran(img, m, co, c)
    elif t < T_PLONGE + D_PLONGE:                                       # P07a : on plonge dans les données
        q = doux((t - T_PLONGE) / D_PLONGE)
        img, m, co = salle("s08_sara", (t - T_SORT) * FPS)
        f = traverser(img, co, PLEIN, donnees(t), q, assombrir=False)
    else:                                                               # P07-P08 : les données ; la rouge, et vous
        f = donnees(t)
    f *= 1 - lisse((t - T_NOIR) / 0.12)
    f += np.random.default_rng(n).normal(0, 1.8, f.shape).astype(np.float32)
    return f


SON_SEUL = os.environ.get("SON_SEUL") == "1"
if not SON_SEUL:
    if "--test" in sys.argv:
        temps = os.environ.get("TEMPS")
        temps = [float(x) for x in temps.split(",")] if temps else (0.3, 1.0, 3.0, 6.5, 9.5, 12.4, 12.8, 15.5, 18.0, 19.5,
                                                                      23.5, 27.0, 28.8, 30.0, 31.5, 32.4, 34.0, 36.5, 39.0, 42.0)
        for t in temps:
            cv2.imwrite(os.path.join(sys.argv[-1], f"s08_{t:05.2f}.png"), np.clip(image(int(round(t * FPS))), 0, 255).astype(np.uint8))
        sys.exit()
    os.makedirs(OUT, exist_ok=True)
    ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", os.path.join(OUT, "S08_image.mp4")],
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
    return boucle(lire(nom, dossier)[int(debut * SR):int(debut * SR) + Ns + SR], Ns)


def env(t0, t1, e=0.25, s=0.3):
    return np.clip((ts - t0) / max(e, 1e-3), 0, 1) * np.clip((t1 - ts) / max(s, 1e-3), 0, 1)


def crete(a):
    return int(np.argmax(np.abs(a).mean(1)))


# la salle : souffle des machines, bourdonnement des écrans, une tension grave (comme la fin de S07)
salle_env = np.clip(env(0, T_ENTRE + 0.4, 0.3, 0.6) + env(T_SORT - 0.2, T_PLONGE + 0.5, 0.5, 0.8), 0, 1)
mix += stereo("ambiance_grand_hall.wav", 140.0) * (db(-15) * salle_env)[:, None]
mix += stereo("bourdonnement_ordinateur.wav", 60.0) * (db(-13) * salle_env)[:, None]
mix += stereo("espace_drone.wav", 45.0) * (db(-25) * env(0, T_PLONGE + 1.0, 1.0, 1.5))[:, None]
# P01 : la frappe, très douce, pendant que la ligne s'écrit
cl = lire("clavier_lent.wav")
poser(cl[int(2 * SR):int(2 * SR) + int((T_TAPE[1] - T_TAPE[0]) * SR)] * fondu(int((T_TAPE[1] - T_TAPE[0]) * SR), 0.05, 0.3)[:, None],
      T_TAPE[0], db(-21))
# P02 : la chaise qui grince quand il se recule
ch = lire("chaise_assis.wav")
o_ch = crete(ch)
poser(ch[max(0, o_ch - int(0.35 * SR)):o_ch + int(0.9 * SR)] * fondu(int(1.25 * SR), 0.05, 0.4)[:o_ch + int(0.9 * SR) - max(0, o_ch - int(0.35 * SR)), None],
      T_RECUL + 1.0, db(-15))
# P03 : on entre dans l'écran (un souffle) ; la cour, derrière le portail ; le portail claque, la cour s'étouffe
wz = lire("whoosh_zoom.wav")
o_w = crete(wz)
poser(wz[max(0, o_w - int(0.6 * SR)):o_w + int(0.5 * SR)], T_ENTRE + D_ENTRE * 0.55 - 0.6, db(-19))
cour = stereo("cour_ecole.wav", 20.0)
ferme = T_ENTRE + 4.45                                     # le portail se ferme (tableau : 3,3 s -> 4,5 s)
cour_env = env(T_ENTRE + 0.2, T_CHEVRES + 0.3, 0.6, 0.4) * (1 - 0.65 * np.clip((ts - ferme) / 0.08, 0, 1))
mix += cour * (db(-21) * cour_env)[:, None]
pf = lire("portail_fer.wav")
o_p = crete(pf)
poser(pf[max(0, o_p - int(1.1 * SR)):o_p + int(1.2 * SR)], ferme - 1.1, db(-11))
# P04-P05 : le vent dans l'herbe sèche, les chèvres et leurs cloches ; les enfants passent au loin
mix += stereo("vent_herbe_seche.wav", 30.0) * (db(-20) * env(T_CHEVRES - 0.1, T_SORT + 0.4, 0.3, 0.6))[:, None]
mix += stereo("chevres_cloches.wav", 12.0) * (db(-19) * env(T_CHEVRES - 0.1, T_SORT + 0.2, 0.3, 0.6))[:, None]
mix += stereo("cour_ecole.wav", 70.0) * (db(-31) * env(T_BETES + 0.6, T_SORT, 1.2, 0.8))[:, None]
# P06 : on ressort (un souffle inversé) ; P07 : on plonge
poser(wz[max(0, o_w - int(0.6 * SR)):o_w + int(0.5 * SR)][::-1], T_SORT - 0.1, db(-21))
poser(wz[max(0, o_w - int(0.6 * SR)):o_w + int(0.5 * SR)], T_PLONGE + D_PLONGE * 0.55 - 0.6, db(-18))
# les données : un frémissement de petits tics quand les vies s'allument ; un souffle grave quand elles s'éteignent
tic = lire("tic_doux.wav")
o_t = crete(tic[:SR])
un_tic = tic[max(0, o_t - 100):o_t + int(0.06 * SR)] * fondu(o_t + int(0.06 * SR) - max(0, o_t - 100), 0.002, 0.03)[:, None]
for k in range(14):
    poser(un_tic, T_ALLUME + 0.07 * k, db(-30 + 1.5 * (k % 3)))
tw = np.arange(int(1.6 * SR)) / SR
souffle = np.sin(2 * np.pi * (98 * tw - 18 * tw * tw)) * np.exp(-tw / 0.6) * 0.11
poser(np.stack([souffle, souffle], 1), T_ETEINT, 1.0)
# P08 : une note tenue, grave et douce, pendant la question ; puis le silence
tn = np.arange(int((T_NOIR - T_SEUL) * SR)) / SR
note = (np.sin(2 * np.pi * 110 * tn) + 0.45 * np.sin(2 * np.pi * 164.8 * tn) + 0.2 * np.sin(2 * np.pi * 220 * tn))
note *= np.minimum(1, tn / 1.5) * np.minimum(1, (tn[-1] - tn) / 0.6) * 0.045
poser(np.stack([note, note * 0.97], 1), T_SEUL, 1.0)

# les voix ; celles de la salle avec un peu de pièce (peu d'écho : retour de Bruno sur S07)
rng = np.random.default_rng(7)
tr = np.arange(int(0.35 * SR)) / SR
piece = rng.normal(0, 1, len(tr)) * np.exp(-tr / 0.05)
piece[0] = 0
piece *= 0.08 / np.sqrt((piece ** 2).sum())
voix = np.zeros(Ns)
for fichier, phrases, salle_ in VOIX:
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
mix *= fondu(Ns, 0.02, 0.6)[:, None]

GAIN = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
wav = os.path.join(OUT, "S08_son.wav")
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN))
final = os.path.join(OUT, "S08_v1.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, "S08_image.mp4"), "-i", wav, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", final], check=True)
print("écrit :", final)
