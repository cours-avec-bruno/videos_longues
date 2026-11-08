"""S06 · Les années qui passent : « le journal des années » (piste choisie par Bruno le 08/11/2026).

Sans voix. L'écran du simulateur (même interface que la fiche de S05) :
  - à gauche, le compteur d'âge en grand, qui avance d'un an à chaque pulsation ;
  - sous lui, le journal : pour chaque année, une ligne du vrai récit de la simulation (prompts/partie/7-…json) ;
  - à droite, une fenêtre d'archive : une vraie vidéo qui fait écho à la ligne (Pexels, étalonnage documentaire) ;
  - la fenêtre s'ouvre et se referme sur le portrait de Manoj, qui gagne un cran de netteté à chaque passage.
Le même script sert aux quatre passages (0 -> 5, 10 -> 11, 11 -> 15, 60 -> 75 ans) : voir PASSAGES.

Usage : python journal.py a        ->  medias/S06/S06a_v1.mp4      (SON_SEUL=1 : ne refait que le son)
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
sys.path.insert(0, os.path.join(ICI, "..", "S05"))
from pas import SR, boucle, ecrire_normalise, lire_audio  # noqa: E402
from effets import etalonnage_doc, glitch  # noqa: E402
from fiche import (AMBRE, BLANC, CYAN, CYAN_D, CYAN_DD, F_LABEL, F_LOG, F_TETE, FOND, FONTS, H, W,  # noqa: E402
                   _bahn, coins, espace, largeur_espace, lisse, panneau_portrait, post)

M = os.path.join(ICI, "..", "..", "medias")
PX = os.path.join(M, "pexels", "s06")
SONS = os.path.join(M, "sons", "epidemic")
OUT = os.path.join(M, "S06")
os.makedirs(OUT, exist_ok=True)
FPS = 24

# ---------------------------------------------------------------- les passages
# (âge, ligne du journal, (vidéo d'archive, début en s, cadrage vertical 0-1), ambiance)
PASSAGES = {
    "a": dict(age0=0, annee0=2026, crans=(1, 2), annees=[
        (1, "Vous avez dit votre premier mot : un mot qui voulait dire « Maman ».", ("16270511.mp4", 0.3, 0.42), None),
        (2, "En jouant dans la boue, vous avez complètement sali vos vêtements.", ("5451849.mp4", 4.0, 0.5), "village"),
        (3, "Votre grand-mère paternelle vous racontait des histoires d’autrefois.", ("40379978.mp4", 0.5, 0.4), "village"),
        (4, "Le goût du dal avec des rotis que vous préparait votre mère, vous ne l’oublierez sans doute jamais.",
         ("36100216.mp4", 3.0, 0.5), "feu"),
        (5, "Vous avez couru et joué avec les enfants du quartier jusqu’au coucher du soleil.", ("3978429.mp4", 2.0, 0.6),
         "village"),
    ]),
}
CLE = sys.argv[1] if len(sys.argv) > 1 else "a"
P = PASSAGES[CLE]
ANNEES = P["annees"]
T0 = 0.7                   # première année
PAS = 1.9                  # une année
T_FIN = T0 + len(ANNEES) * PAS          # la fenêtre revient au portrait
T_CRAN = (T_FIN + 0.35, T_FIN + 1.55)   # le portrait se redivise
DUREE = T_FIN + 2.6
N = int(round(DUREE * FPS))
CPS = 64                   # frappe du journal (lettres par seconde)

F_AGE = _bahn(196, "Bold")
F_JOUR = ImageFont.truetype(FONTS + "consola.ttf", 35)
F_PREF = _bahn(24)

# la fenêtre d'archive (4:3)
FX0, FY0, FX1, FY1 = 1100, 190, 1780, 700
FW, FH = FX1 - FX0, FY1 - FY0


def age_txt(a):
    return f"{a} AN" if a <= 1 else f"{a} ANS"


def lire_extrait(chemin, debut, duree, cy):
    n = int(math.ceil(duree * FPS)) + 2
    vf = (f"fps={FPS},scale={FW}:{FH}:force_original_aspect_ratio=increase,"
          f"crop={FW}:{FH}:(iw-{FW})/2:(ih-{FH})*{cy}")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(debut), "-i", chemin, "-vf", vf, "-frames:v", str(n),
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(-1, FH, FW, 3)
    if len(im) < n:
        im = np.concatenate([im, np.repeat(im[-1:], n - len(im), 0)])
    return im


def lignes(texte, font, largeur, d):
    """Coupe le texte en lignes qui tiennent dans `largeur`."""
    mots, out, cour = texte.split(" "), [], ""
    for m in mots:
        essai = (cour + " " + m).strip()
        if d.textlength(essai, font=font) <= largeur:
            cour = essai
        else:
            out.append(cour)
            cour = m
    out.append(cour)
    return out


def teinte(col, f):
    return tuple(int(c * f) for c in col)


# ---------------------------------------------------------------- l'écran
_mesure = ImageDraw.Draw(Image.new("RGB", (8, 8)))
X_TXT, L_TXT = 268, 780
JOURNAL = [(a, lignes(t, F_JOUR, L_TXT, _mesure)) for a, t, _, _ in ANNEES]
H_LIGNE, ECART = 46, 30


def hauteur(i):
    return len(JOURNAL[i][1]) * H_LIGNE + ECART


def positions(n):
    """Positions verticales des n premières entrées, la plus récente en haut."""
    y, out = 520, {}
    for i in range(n - 1, -1, -1):
        out[i] = y
        y += hauteur(i)
    return out


def annee_en_cours(t):
    """Indice de l'année affichée (-1 avant la première) et temps depuis son arrivée."""
    i = int(np.floor((t - T0) / PAS))
    i = min(i, len(ANNEES) - 1)
    return i, t - (T0 + max(i, 0) * PAS)


videos = {}


def ecran(t, k):
    im = Image.new("RGB", (W, H), FOND)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(3)
    for x, y, a in rng.random((140, 3)):                  # la poussière du fond
        xx, yy = (x * W + 6 * t) % W, (y * H - 3 * t) % H
        d.rectangle([xx, yy, xx + 2, yy + 2], fill=teinte(CYAN_D, 0.25 + 0.35 * a))
    ouv = lisse(t / 0.4)
    coins(d, 70, 52, W - 70, H - 52, int(44 * ouv), CYAN_DD, 2)
    i, dt = annee_en_cours(t)
    age = P["age0"] if i < 0 else ANNEES[i][0]
    espace("SIMULATION   ·   VIE N° 1 284 177", d, (140, 86), F_TETE, CYAN_D)
    tx = f"ANNÉE   {P['annee0'] + age}"
    espace(tx, d, (W - 140 - largeur_espace(tx, d, F_TETE), 86), F_TETE, CYAN_D)
    xl = 140 + (W - 280) * ouv
    d.line([(140, 134), (xl, 134)], fill=CYAN_DD, width=2)
    for x in range(140, int(xl), 41):
        d.line([(x, 134), (x, 141 if (x - 140) % 205 else 148)], fill=CYAN_DD, width=2)

    # le compteur d'âge : l'ancien chiffre monte et s'éteint, le nouveau arrive d'en bas
    espace("ÂGE", d, (142, 190), F_LABEL, CYAN_D)
    cpt = Image.new("RGB", (900, 230), FOND)
    dc = ImageDraw.Draw(cpt)
    p = lisse(dt / 0.22) if i >= 0 else 1.0
    if i >= 0 and p < 1:
        ancien = P["age0"] if i == 0 else ANNEES[i - 1][0]
        dc.text((0, 10 - 90 * p), age_txt(ancien), font=F_AGE, fill=teinte(BLANC, 1 - p))
    dc.text((0, 10 + 90 * (1 - p)), age_txt(age), font=F_AGE, fill=teinte(BLANC, p))
    im.paste(cpt, (132, 222))
    # le trait sous le compteur s'allume à chaque pulsation
    eclat = math.exp(-dt / 0.25) if i >= 0 and dt >= 0 else 0
    d.line([(140, 462), (1040, 462)], fill=teinte(CYAN, 0.35 + 0.65 * eclat), width=2)

    # le journal : la ligne de l'année se tape en haut, les précédentes descendent et pâlissent
    if i >= 0:
        pos_av, pos_ap = positions(i), positions(i + 1)
        glis = lisse(dt / 0.3)
        for j in range(i + 1):
            y = pos_ap[j] if j not in pos_av else pos_av[j] + (pos_ap[j] - pos_av[j]) * glis
            rang = i - j
            f = max(0.0, 1 - 0.28 * rang) * (glis if j == i else 1)
            f *= float(np.clip((1000 - y) / 140, 0, 1))
            if f <= 0.02:
                continue
            a_j, ls = JOURNAL[j]
            espace(age_txt(a_j), d, (142, y + 8), F_PREF, teinte(CYAN_D if rang else CYAN, f))
            n = len(" ".join(ls)) if j < i else int(max(0, (dt - 0.15) * CPS))
            reste = n
            for li, l_ in enumerate(ls):
                if reste <= 0:
                    break
                d.text((X_TXT, y + li * H_LIGNE), l_[:reste], font=F_JOUR, fill=teinte(BLANC, f))
                if j == i and reste < len(l_) and int(t * 4) % 2 == 0:
                    xc = X_TXT + d.textlength(l_[:reste], font=F_JOUR) + 3
                    d.rectangle([xc, y + li * H_LIGNE + 6, xc + 17, y + li * H_LIGNE + 40], fill=CYAN)
                reste -= len(l_) + 1

    # la fenêtre d'archive, ou le portrait (au début et à la fin)
    portrait = i < 0 or t >= T_FIN
    lab = "PORTRAIT" if portrait else "ARCHIVE"
    d.rectangle([FX0, FY0, FX1, FY1], fill=(5, 10, 14))
    a = np.asarray(im).copy()
    if portrait:
        c0, c1 = P["crans"]
        cran = c0 + (c1 - c0) * lisse((t - T_CRAN[0]) / (T_CRAN[1] - T_CRAN[0])) if t >= T_FIN else c0
        pw = int(FH * 3 / 4)
        px = panneau_portrait(pw, FH, cran)
        xa = FX0 + (FW - pw) // 2
        a[FY0:FY1, xa:xa + pw] = np.clip(px, 0, 255).astype(np.uint8)
    else:
        ims = videos[i]
        kk = min(int(dt * FPS), len(ims) - 1)
        v = etalonnage_doc(ims[kk].astype(np.float32), k)
        z = 1 + 0.05 * dt / PAS                               # une lente poussée
        v = cv2.warpAffine(v, cv2.getRotationMatrix2D((FW / 2, FH / 2), 0, z), (FW, FH), borderMode=cv2.BORDER_REFLECT)
        if round(dt * FPS) in (0, 1):
            v = glitch(v, k, 0.8 if round(dt * FPS) == 0 else 0.4)
        a[FY0:FY1, FX0:FX1] = np.clip(v[:, :, ::-1], 0, 255).astype(np.uint8)
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    coins(d, FX0 - 10, FY0 - 10, FX1 + 10, FY1 + 10, 34, CYAN, 3)
    espace(lab, d, (FX0, FY1 + 28), F_LABEL, CYAN_D)
    if not portrait:
        tx = f"ANNÉE {P['annee0'] + age}"
        espace(tx, d, (FX1 - largeur_espace(tx, d, F_LABEL), FY1 + 28), F_LABEL, CYAN_DD)
    # la jauge de netteté : un cran de plus quand le portrait s'est redivisé
    allumes = P["crans"][1] if t >= T_CRAN[1] else P["crans"][0]
    espace("NETTETÉ", d, (FX0, FY1 + 66), F_LABEL, CYAN_DD)
    xg = FX1 - 7 * 28 + 8
    for g in range(7):
        on = g < allumes
        neuf = on and g == allumes - 1 and t >= T_CRAN[1] and (t - T_CRAN[1]) < 0.5 and int((t - T_CRAN[1]) * 8) % 2
        col = BLANC if neuf else AMBRE
        d.rectangle([xg + g * 28, FY1 + 70, xg + g * 28 + 20, FY1 + 90], outline=col if on else CYAN_DD, width=2,
                    fill=col if on else None)

    # pied de page
    log = f"> {len(ANNEES)} années simulées · aucune décision"
    nl = int(np.clip((t - T_FIN) * 40, 0, len(log)))
    if nl:
        d.text((140, H - 118), log[:nl], font=F_LOG, fill=CYAN_DD)
    tx = "UNE VIE SUR HUIT MILLIARDS"
    espace(tx, d, (W - 140 - largeur_espace(tx, d, F_TETE), H - 120), F_TETE, CYAN_DD)

    img = np.asarray(im).astype(np.float32)[:, :, ::-1].copy()
    # à la fin, la caméra s'approche du portrait
    zf = lisse((t - T_FIN) / (DUREE - T_FIN))
    if zf > 0:
        s = 1 + 0.14 * zf
        cx, cy = W / 2 + 120, (FY0 + FY1) / 2       # zoom presque centré : le compteur reste entier
        tx_, ty_ = cx - s * cx, (cy + (H / 2 - cy) * 0.3 * zf) - s * cy
        img = cv2.warpAffine(img, np.float32([[s, 0, tx_], [0, s, ty_]]), (W, H), borderValue=FOND[::-1])
    img = post(img, k)
    if k < 3:                                              # l'entrée depuis le bureau : un éclat de glitch
        img = glitch(img, k, (1.0, 0.6, 0.3)[k])
    return img


SON_SEUL = os.environ.get("SON_SEUL") == "1"
if not SON_SEUL:
    for i, (_, _, (f, s0, cy), _) in enumerate(ANNEES):
        videos[i] = lire_extrait(os.path.join(PX, f), s0, PAS + 0.2, cy)
    if "--test" in sys.argv:
        for t in (0.3, T0 + 0.1, T0 + 1.2, T0 + 3 * PAS + 1.5, T_FIN + 0.9, DUREE - 0.05):
            cv2.imwrite(os.path.join(sys.argv[-1], f"s06_{t:05.2f}.png"), np.clip(ecran(t, int(t * FPS)), 0, 255).astype(np.uint8))
        sys.exit()
    ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                            os.path.join(OUT, f"S06{CLE}_image.mp4")], stdin=subprocess.PIPE)
    for n in range(N):
        ecr.stdin.write(np.clip(ecran(n / FPS, n), 0, 255).astype(np.uint8).tobytes())
    ecr.stdin.close()
    ecr.wait()
    print("image :", round(DUREE, 2), "s")

# ---------------------------------------------------------------- le son
Ns = int(DUREE * SR)
mix = np.zeros((Ns, 2))
ts = np.arange(Ns) / SR


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


def stereo(nom, debut, n):
    a = lire_audio(os.path.join(SONS, nom), mono=False).astype(np.float64)
    return boucle(a[int(debut * SR):], n)


def env(t0, t1, e=0.3, s=0.3):
    return np.clip((ts - t0) / max(e, 1e-3), 0, 1) * np.clip((t1 - ts) / max(s, 1e-3), 0, 1)


# la pulsation d'une année : un coup sourd (90 -> 45 Hz) et, un peu derrière, un second plus faible, comme un cœur
def coup(f0, f1, dur, amp):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-tt / 0.05)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-tt / (dur / 4)) * amp


pulse = coup(95, 46, 0.5, 1.0)
pulse2 = coup(80, 42, 0.4, 0.45)
battement = np.zeros(len(pulse) + int(0.22 * SR))
battement[:len(pulse)] += pulse
battement[int(0.22 * SR):int(0.22 * SR) + len(pulse2)] += pulse2
battement = np.stack([battement, battement], 1)
for j in range(len(ANNEES)):
    poser(battement, T0 + j * PAS - 0.01, db(-15))
poser(battement, T_CRAN[1] - 0.01, db(-18))
# la frappe du journal : un tic doux par lettre (une sur deux : la frappe est rapide)
tic = lire_audio(os.path.join(SONS, "tic_doux.wav"), mono=False).astype(np.float64)
o_t = int(np.argmax(np.abs(tic[:SR]).mean(1)))
un_tic = tic[max(0, o_t - 100):o_t + int(0.05 * SR)] * fondu(o_t + int(0.05 * SR) - max(0, o_t - 100), 0.002, 0.03)[:, None]
for j, (_, texte, _, _) in enumerate(ANNEES):
    for c in range(0, len(texte), 2):
        poser(un_tic, T0 + j * PAS + 0.15 + c / CPS, db(-31))
# le portrait qui se redivise : une pluie de tics
rng = np.random.default_rng(8)
for tt in np.sort(rng.uniform(*T_CRAN, 14)):
    poser(un_tic, tt, db(-27))
# l'archive : une coupe numérique à chaque année, et le son du lieu, très bas
gr = lire_audio(os.path.join(SONS, "glitch_radio.wav"), mono=False).astype(np.float64)
o_g = int(np.argmax(np.abs(gr).mean(1)))
seg = gr[max(0, o_g - int(0.02 * SR)):o_g + int(0.18 * SR)]
for j in range(len(ANNEES) + 1):
    poser(seg * fondu(len(seg), 0.003, 0.08)[:, None], T0 + j * PAS - 0.02, db(-24))
poser(seg * fondu(len(seg), 0.003, 0.08)[:, None], 0.0, db(-18))
village = stereo("village_amethi.wav", 60.0, Ns)
feu = stereo("feu_bois.wav", 20.0, Ns)
for j, (_, _, _, amb) in enumerate(ANNEES):
    t0_, t1_ = T0 + j * PAS, T0 + (j + 1) * PAS
    if amb == "village":
        mix += village * (db(-23) * env(t0_, t1_, 0.05, 0.1))[:, None]
    elif amb == "feu":
        mix += feu * (db(-17) * env(t0_, t1_, 0.05, 0.1))[:, None]
# un souffle grave sous tout le passage
mix += stereo("espace_drone.wav", 30.0, Ns) * (db(-25) * env(0, DUREE, 0.4, 0.6))[:, None]

GAIN = float(open(os.path.join(M, "S01", "gain_mix.txt")).read())
wav = os.path.join(OUT, f"S06{CLE}_son.wav")
print("sonie avant / gain :", ecrire_normalise(mix, wav, gain_db=GAIN))
final = os.path.join(OUT, f"S06{CLE}_v1.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, f"S06{CLE}_image.mp4"), "-i", wav, "-map", "0:v",
                "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", final],
               check=True)
print("écrit :", final)
