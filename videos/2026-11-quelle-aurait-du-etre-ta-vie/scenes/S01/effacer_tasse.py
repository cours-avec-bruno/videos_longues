"""Efface la tasse blanche du bureau dans un plan déjà fabriqué, sans nouveau rendu (demande de Bruno, 07/11/2026).

La tasse est suivie image par image (tache claire et peu saturée, à rebours depuis une position connue).
  - Quand elle est grande et qu'une image propre du décor existe (rendu Blender sans tasse, même point de vue),
    on aligne cette image propre sur l'image courante (alignement ECC, homographie, autour de la tasse)
    et on colle le morceau propre à la place de la tasse, avec un fondu.
  - Sinon (tasse petite ou alignement raté), on reconstitue la zone à partir de ce qui l'entoure (inpainting).

Usage :
  python effacer_tasse.py --video IN.mp4 --sortie OUT.mp4 --depart X,Y [--propre image_sans_tasse.png] [--images 0-239]
  --depart : position approximative de la tasse sur la DERNIÈRE image traitée (le suivi part de là, à rebours).
"""
import argparse
import subprocess

import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--video", required=True)
ap.add_argument("--sortie", required=True)
ap.add_argument("--depart", required=True)
ap.add_argument("--propre", default="")
ap.add_argument("--images", default="", help="plage d'images où la tasse est visible (sinon : toutes)")
ap.add_argument("--controle", default="")
ap.add_argument("--taille", type=float, default=0, help="taille attendue de la tasse en pixels sur la première image suivie (active le choix par la taille)")
ap.add_argument("--bas", type=float, default=0.0, help="prolonge le masque vers le bas (fraction de la hauteur détectée) : corps de la tasse moins éclairé que son bord")
ap.add_argument("--boite", default="", help="mode boîte : x0,y0,x1,y1 exacts de la tasse sur la première image ; la position sur les autres images vient de l'alignement du décor, pas d'une détection")
ap.add_argument("--avant", action="store_true", help="suivre dans le sens du temps (--depart = position sur la PREMIÈRE image)")
A = ap.parse_args()
W, H, FPS = 1920, 1080, 24

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", A.video, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                     capture_output=True, check=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).copy()
N = len(F)
a, b = (int(x) for x in A.images.split("-")) if A.images else (0, N - 1)
propre = cv2.imread(A.propre) if A.propre and A.propre != "auto" else None
if propre is not None and propre.shape[:2] != (H, W):
    propre = cv2.resize(propre, (W, H), interpolation=cv2.INTER_AREA)


def tache(img, cx, cy, r, attendu=None):
    """Cherche la tasse : pixels clairs et peu saturés autour de (cx, cy) ; renvoie (x0, y0, x1, y1) ou None."""
    x0, y0 = max(0, int(cx - r)), max(0, int(cy - r))
    x1, y1 = min(W, int(cx + r)), min(H, int(cy + r))
    roi = img[y0:y1, x0:x1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    v, s = hsv[:, :, 2].astype(np.float32), hsv[:, :, 1].astype(np.float32)
    m = ((v > max(60, 0.72 * np.percentile(v, 99.7))) & (s < 70)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    if n < 2:
        return None
    def score(i):
        d = np.hypot(cen[i][0] + x0 - cx, cen[i][1] + y0 - cy)
        if attendu:   # une tache de la taille attendue (évite la flaque de lumière de la lampe, bien plus grande)
            return d + 1.5 * abs(max(st[i, 2], st[i, 3]) - attendu)
        return d - 0.5 * np.sqrt(st[i, 4])
    best = min(range(1, n), key=score)
    if st[best, 4] < 4:
        return None
    bx, by, bw, bh, _ = st[best]
    return x0 + bx, y0 + by, x0 + bx + bw, y0 + by + bh


def mode_boite():
    """Boîte exacte sur la première image ; image propre = la boîte remplie par ce qui est juste à sa droite ;
    pour chaque image, alignement du décor (enchaîné) sur cette image propre, et collage du morceau propre."""
    bx0, by0, bx1, by1 = (int(v) for v in A.boite.split(","))
    k0 = a
    base = F[k0].copy()
    propre_ = base.copy()
    dx = (bx1 - bx0) + 2
    propre_[by0:by1, bx0:bx1] = base[by0:by1, bx0 + dx:bx1 + dx]
    if A.controle:
        cv2.imwrite(f"{A.controle}/tasse_propre.png", propre_)
    E = 0.5
    Sc = np.diag([E, E, 1.0])
    def gris(img):
        g = cv2.cvtColor(cv2.resize(img, (int(W * E), int(H * E)), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        return cv2.GaussianBlur(g.astype(np.float32), (5, 5), 0)
    C = gris(propre_)
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 120, 1e-5)
    coins0 = np.float32([[bx0, by0], [bx1, by0], [bx1, by1], [bx0, by1]])
    M_prec, G_prec = np.eye(3, dtype=np.float32), None
    for k in range(a, b + 1):
        img = F[k].copy()
        Gk = gris(img)
        # zone d'alignement : autour de la boîte, telle que placée par l'alignement précédent
        inv = np.linalg.inv(np.linalg.inv(Sc) @ M_prec.astype(np.float64) @ Sc)
        boite_k = cv2.perspectiveTransform(coins0[None], inv)[0]
        cx_, cy_ = boite_k.mean(0); R = max(90, 5 * np.ptp(boite_k[:, 0]))
        m_t = np.zeros(Gk.shape, np.uint8)
        m_t[int(max(0, cy_ - R) * E):int(min(H, cy_ + R) * E), int(max(0, cx_ - R) * E):int(min(W, cx_ + R) * E)] = 255
        cv2.fillConvexPoly(m_t, np.int32(np.round(boite_k * E)), 0)
        m_t = cv2.erode(m_t, np.ones((7, 7), np.uint8))
        init = M_prec
        if G_prec is not None:
            try:
                _, Hp = cv2.findTransformECC(Gk, G_prec, np.eye(3, dtype=np.float32), cv2.MOTION_HOMOGRAPHY, crit, m_t, 1)
                init = (M_prec @ Hp).astype(np.float32)
            except cv2.error:
                pass
        try:
            cc, M = cv2.findTransformECC(Gk, C, init.copy(), cv2.MOTION_HOMOGRAPHY, crit, m_t, 1)
        except cv2.error:
            cc, M = 0, init
        if cc < 0.85:
            M = init
        Mf = np.linalg.inv(Sc) @ M.astype(np.float64) @ Sc
        boite_k = cv2.perspectiveTransform(coins0[None], np.linalg.inv(Mf))[0]
        masque = np.zeros((H, W), np.uint8)
        cv2.fillConvexPoly(masque, np.int32(np.round(boite_k)), 255)
        masque = cv2.dilate(masque, np.ones((3, 3), np.uint8))
        pro_w = cv2.warpPerspective(propre_, Mf, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)
        anneau = cv2.dilate(masque, np.ones((9, 9), np.uint8)) - masque
        sel = anneau > 0
        gain = (img[sel].astype(np.float32).mean(0) + 1) / (pro_w[sel].astype(np.float32).mean(0) + 1)
        patch = np.clip(pro_w.astype(np.float32) * gain, 0, 255)
        alpha = cv2.GaussianBlur(masque.astype(np.float32) / 255, (0, 0), 1.5)[:, :, None]
        F[k] = np.clip(img * (1 - alpha) + patch * alpha, 0, 255).astype(np.uint8)
        M_prec, G_prec = M.astype(np.float32), Gk
    if A.controle:
        for k in (a, (a + b) // 2, b):
            cv2.imwrite(f"{A.controle}/tasse_{k:03d}.png", F[k])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                    "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", A.sortie], input=F.tobytes(), check=True)
    print("écrit (mode boîte) :", A.sortie)
    raise SystemExit(0)


if A.boite:
    mode_boite()


# 1. suivi à rebours
cx, cy = (float(v) for v in A.depart.split(","))
boites = [None] * N
taille = float(A.taille) if A.taille else 60.0
for k in (range(a, b + 1) if A.avant else range(b, a - 1, -1)):
    bo = tache(F[k], cx, cy, max(25, taille * 1.6), taille if A.taille else None)
    if bo is None:
        continue
    boites[k] = bo
    cx, cy = (bo[0] + bo[2]) / 2, (bo[1] + bo[3]) / 2
    taille = max(bo[2] - bo[0], bo[3] - bo[1])
# lissage des boîtes (centre et taille), avec une marge : l'ombre et le reflet de la tasse partent aussi
idx = [k for k in range(N) if boites[k] is not None]
print("tasse trouvée sur", len(idx), "images sur", b - a + 1)
B = np.array([boites[k] for k in idx], float)
for j in range(4):
    B[:, j] = np.convolve(np.pad(B[:, j], 3, mode="edge"), np.ones(7) / 7, mode="valid")
lisses = {k: B[i] for i, k in enumerate(idx)}

# 2. effacement, à rebours : l'image propre est alignée image par image (chaîne d'alignements, un seul ré-échantillonnage)
ORIG = F.copy()
E = 0.5                                                   # alignements calculés en demi-résolution
Sc = np.diag([E, E, 1.0])
def gris(img):
    g = cv2.cvtColor(cv2.resize(img, (int(W * E), int(H * E)), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(g.astype(np.float32), (5, 5), 0)
if A.propre == "auto":
    k0 = sorted(idx, reverse=not A.avant)[0]
    x0, y0, x1, y1 = lisses[k0]
    w, h = x1 - x0, y1 - y0
    marge = max(4, 0.35 * max(w, h))
    X0, Y0 = int(max(0, x0 - marge)), int(max(0, y0 - marge * 1.2))
    X1, Y1 = int(min(W, x1 + marge)), int(min(H, y1 + marge * 0.8 + A.bas * h))
    dx = (X1 - X0) + 3
    propre = ORIG[k0].copy()
    propre[Y0:Y1, X0:X1] = ORIG[k0][Y0:Y1, X0 + dx:X1 + dx]
    # raccord doux sur les bords verticaux
    for j in range(6):
        a_ = (j + 1) / 7
        propre[Y0:Y1, X0 + j] = (ORIG[k0][Y0:Y1, X0 + j] * (1 - a_) + propre[Y0:Y1, X0 + j] * a_).astype(np.uint8)
        propre[Y0:Y1, X1 - 1 - j] = (ORIG[k0][Y0:Y1, X1 - 1 - j] * (1 - a_) + propre[Y0:Y1, X1 - 1 - j] * a_).astype(np.uint8)
    print("image propre fabriquée sur l'image", k0)
    if A.controle:
        cv2.imwrite(f"{A.controle}/tasse_propre.png", propre)
C = gris(propre) if propre is not None else None
crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 120, 1e-5)
M_suiv, G_suiv = None, None
avec_propre = 0
for k in sorted(idx, reverse=not A.avant):
    x0, y0, x1, y1 = lisses[k]
    w, h = x1 - x0, y1 - y0
    marge = max(4, 0.35 * max(w, h))
    X0, Y0 = int(max(0, x0 - marge)), int(max(0, y0 - marge * 1.2))
    X1, Y1 = int(min(W, x1 + marge)), int(min(H, y1 + marge * 0.8 + A.bas * h))
    masque = np.zeros((H, W), np.uint8)
    masque[Y0:Y1, X0:X1] = 255
    img = ORIG[k]
    fait = False
    if C is not None and max(w, h) > 6:
        Gk = gris(img)
        R = max(80, int(max(w, h) * 5))
        cx_, cy_ = (x0 + x1) / 2, (y0 + y1) / 2
        m_t = np.zeros(Gk.shape, np.uint8)
        m_t[int(max(0, cy_ - R) * E):int(min(H, cy_ + R) * E), int(max(0, cx_ - R) * E):int(min(W, cx_ + R) * E)] = 255
        m_t[int(Y0 * E) - 2:int(Y1 * E) + 2, int(X0 * E) - 2:int(X1 * E) + 2] = 0
        init = np.eye(3, dtype=np.float32)
        if M_suiv is not None:
            try:
                _, Hp = cv2.findTransformECC(Gk, G_suiv, np.eye(3, dtype=np.float32), cv2.MOTION_HOMOGRAPHY, crit, m_t, 1)
                init = (M_suiv @ Hp).astype(np.float32)
            except cv2.error:
                init = M_suiv.astype(np.float32)
        try:
            cc, M = cv2.findTransformECC(Gk, C, init.copy(), cv2.MOTION_HOMOGRAPHY, crit, m_t, 1)
        except cv2.error:
            cc, M = 0, init
        if cc < 0.85 and M_suiv is not None:
            M, cc = init, 0.85               # l'alignement direct échoue : on garde l'estimation enchaînée
        if cc >= 0.85:
            Mf = np.linalg.inv(Sc) @ M.astype(np.float64) @ Sc     # image courante -> image propre, pleine résolution
            pro_w = cv2.warpPerspective(propre, Mf, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)
            anneau = cv2.dilate(masque, np.ones((15, 15), np.uint8)) - masque
            sel = anneau > 0
            gain = (img[sel].astype(np.float32).mean(0) + 1) / (pro_w[sel].astype(np.float32).mean(0) + 1)
            patch = cv2.GaussianBlur(np.clip(pro_w.astype(np.float32) * gain, 0, 255), (0, 0), 0.7)
            patch += np.random.default_rng(k).normal(0, 1.4, patch.shape).astype(np.float32)
            alpha = cv2.GaussianBlur(masque.astype(np.float32) / 255, (0, 0), max(2, marge / 2))[:, :, None]
            F[k] = np.clip(img * (1 - alpha) + patch * alpha, 0, 255).astype(np.uint8)
            fait = True
            avec_propre += 1
            M_suiv, G_suiv = M.astype(np.float32), Gk
        else:
            M_suiv, G_suiv = None, None
    if not fait:
        rep = cv2.inpaint(img, masque, max(3, int(marge)), cv2.INPAINT_TELEA)
        rep = cv2.GaussianBlur(rep, (0, 0), 0.8)
        alpha = cv2.GaussianBlur(masque.astype(np.float32) / 255, (0, 0), max(1.5, marge / 3))[:, :, None]
        bruit = np.random.default_rng(k).normal(0, 1.5, img.shape).astype(np.float32)
        F[k] = np.clip(img * (1 - alpha) + (rep + bruit) * alpha, 0, 255).astype(np.uint8)
print("dont", avec_propre, "avec l'image propre alignée")
if A.controle:
    for k in (idx[0], idx[len(idx) // 2], idx[-1]):
        cv2.imwrite(f"{A.controle}/tasse_{k:03d}.png", F[k])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", A.sortie], input=F.tobytes(), check=True)
print("écrit :", A.sortie)
