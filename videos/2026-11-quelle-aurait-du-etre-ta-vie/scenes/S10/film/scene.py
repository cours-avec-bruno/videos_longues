"""S10 · Les autres — avec le skill cinematic-film (Bruno, 10/11/2026 : « utilise ce skill de fond en comble »).

Un seul monde : la carte de l'Afrique à l'Inde, sombre (DA de la chaîne), et cinq vies épinglées là où elles commencent.
La caméra part de Manoj (Inde), recule pour montrer les quatre autres naissances, puis vole de vie en vie ; chaque âge de
mort se pose sur le mot ; Raj et Manoj sont reliés par un fil ; à la fin, recul composé sur les cinq vies.
Photos réelles (Wikimedia Commons et Pexels, crédits : references/photos.md).
"""
from engine import BigText, Film, GeoMap, MapPin, Print, Route, Stamp, StringLine

ROUGE = (214, 72, 46)
CYAN = (95, 211, 230)
CREME = (238, 230, 216)
# la carte, dans la nuit de la chaîne : terres gris-bleu, mer bleu-pétrole
CARTE = dict(sheet=(12, 17, 22), water=(9, 28, 36), land=(40, 50, 56), border=(78, 98, 104), relief=0.12,
             neighbor=(26, 32, 38), neighbor_line=(56, 66, 72), dark=(20, 24, 28), dark_line=(44, 48, 52), frame=(40, 62, 70))
PW = 2400          # largeur d'une photo


def build_film(doc):
    L, E, W = doc.L, doc.E, doc.W
    film = Film(doc.duration, fps=24, look="charcoal")
    m = film.add(GeoMap(doc.map("monde"), 16000, look=CARTE))
    pI, pR, pK, pA, pG = (m.place(n) for n in ("Inde", "Inde2", "Kenya", "Kenya2", "Guinee"))

    # les clusters : la photo à côté de son épingle, l'âge de la mort dessous
    def grappe(cle, pin, dx, dy, nom, t_photo, t_pin, rot):
        film.add(MapPin(pin[0], pin[1], None, t_in=t_pin, size=2.2))
        x, y = pin[0] + dx, pin[1] + dy
        pr = film.add(Print(cle, x, y, PW, rot=rot, t_in=t_photo, label=nom, label_t=t_photo + 0.4, label_rgb=(176, 40, 30)))
        film.add(StringLine(pin, (x, y - PW * 0.3), t_in=t_photo + 0.1, dur=0.6, width=7, persist=True, pins=False, sfx=False))
        return pr, x, y

    # 1 · Manoj (Inde) ; puis, sur « quatre autres naissances », quatre épingles s'allument
    pM, xM, yM = grappe("MANOJ", pI, 2600, 900, "MANOJ · INDE", 0.6, 0.4, -1.0)
    t4 = W(1, "quatre")
    for i, (p, d) in enumerate(((pR, 0.0), (pK, 0.35), (pA, 0.55), (pG, 0.8))):
        film.add(MapPin(p[0], p[1], None, t_in=t4 + d, size=2.2))

    # 2-4 · Purity (Kenya)
    pP, xP, yP = grappe("PURITY", pK, -3600, -1900, "PURITY · KENYA", L(2) + 0.25, L(2), 1.2)
    film.add(BigText("JUSQU'AU LYCÉE", xP, yP + 1700, 300, W(3, "lycée") - 0.2, rgb=(10, 14, 18), bar=CYAN, bar_h=0.92, type_on=0.4))
    film.add(BigText("66 ANS", xP, yP + 2250, 520, W(4, "soixante") - 0.05, rgb=CREME, hit=0.35))

    # 5-6 · Fama (Guinée)
    pF, xF, yF = grappe("FAMA", pG, 2300, -2300, "FAMA · GUINÉE", L(5) + 0.25, L(5) - 0.6, -1.4)
    film.add(Stamp("JAMAIS D'ÉCOLE", xF + 150, yF + 250, size=330, rot=-9, t_in=W(5, "jamais") - 0.05))
    film.add(BigText("64 ANS", xF, yF + 2250, 520, W(6, "soixante") - 0.05, rgb=CREME, hit=0.35))

    # 7-8 · Andrew (Kenya) ; on revient de l'ouest à l'est en suivant une route
    film.add(Route(pG, pA, t_in=L(7) - 0.9, dur=1.0, bend=-0.18, width=26, rgb=CREME))
    pAn, xA, yA = grappe("ANDREW", pA, 3600, 1400, "ANDREW · KENYA", L(7) + 0.2, L(7) - 0.2, 1.0)
    film.add(BigText("51 ANS", xA, yA + 2250, 520, W(8, "cinquante") - 0.05, rgb=CREME, hit=0.35))

    # 9-12 · Raj (Inde) ; un fil le relie à Manoj : tous deux s'arrêtent au primaire
    film.add(Route(pA, pR, t_in=L(9) - 0.9, dur=1.0, bend=0.2, width=26, rgb=CREME))
    pRj, xR, yR = grappe("RAJ", pR, -2900, -1700, "RAJ · INDE", L(9) + 0.25, L(9) - 0.3, -1.2)
    film.add(Stamp("DALIT", xR - 300, yR + 300, size=360, rot=-7, t_in=W(10, "dalit") - 0.05))
    film.add(StringLine((xR, yR + PW * 0.32), (xM, yM - PW * 0.32), t_in=L(11) - 0.1, dur=0.8, width=12, persist=True))
    film.add(BigText("PRIMAIRE, LUI AUSSI", (xR + xM) / 2, (yR + yM) / 2 + 300, 300, W(11, "primaire") - 0.2, rgb=(10, 14, 18),
                     bar=CYAN, bar_h=0.92, type_on=0.4))
    film.add(BigText("81 ANS", xR, yR + 2250, 520, W(12, "quatre") - 0.05, rgb=CREME, hit=0.35))
    film.add(BigText("75 ANS", xM, yM + 2250, 520, L(13) - 0.2, rgb=ROUGE, hit=0.3))

    # ---------------------------------------------------------------- la caméra
    # le cadre large : calculé sur les cinq grappes (photo + âge), pour qu'aucune ne soit coupée
    xs = [x for x in (xM, xP, xF, xA, xR)]
    ys = [y for y in (yM, yP, yF, yA, yR)]
    x0, x1 = min(xs) - PW * 0.8, max(xs) + PW * 0.8
    y0, y1 = min(ys) - PW * 0.7, max(ys) + 2600
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    zl = min(3840 / (x1 - x0), 2160 / (y1 - y0))

    def cadre(a, b, marge=1.25):
        xa, xb = min(a[0], b[0]) - PW * 0.7, max(a[0], b[0]) + PW * 0.7
        ya, yb = min(a[1], b[1]) - PW * 0.6, max(a[1], b[1]) + 2600
        return (xa + xb) / 2, (ya + yb) / 2, min(3840 / (xb - xa), 2160 / (yb - ya)) / marge
    rx, ry, rz = cadre((xR, yR), (xM, yM))
    film.shot(0.0, xM, yM + 300, 0.5, rot=-0.5)
    film.shot(t4 - 0.6, xM - 500, yM, 0.5)
    film.shot(t4 + 0.6, cx, cy, zl, radius=30000, strength=0.15)          # recul : les cinq épingles sur la carte
    film.shot(E(1) + 0.1, cx + 300, cy, zl * 0.97, radius=30000, strength=0.15)
    film.shot(L(2) + 0.5, xP, yP + 300, 0.55, rot=0.6)                       # Purity
    film.shot(E(3), xP, yP + 900, 0.5)
    film.shot(L(4) + 0.3, xP, yP + 1300, 0.52, rot=-0.3)
    film.shot(E(4) + 0.6, xP + 200, yP + 1500, 0.5)
    film.shot(L(5) + 0.5, xF, yF + 300, 0.55, rot=-0.6)                      # Fama
    film.shot(E(5), xF, yF + 600, 0.52)
    film.shot(L(6) + 0.3, xF, yF + 1300, 0.52, rot=0.3)
    film.shot(E(6) + 0.6, xF + 200, yF + 1500, 0.5)
    film.shot(L(7) - 0.3, (pG[0] + pA[0]) / 2, (pG[1] + pA[1]) / 2, 0.2, radius=20000, strength=0.2)   # en route vers l'est
    film.shot(L(7) + 0.7, xA, yA + 300, 0.55, rot=0.5)                       # Andrew
    film.shot(L(8) + 0.3, xA, yA + 1300, 0.52, rot=-0.3)
    film.shot(E(8) + 0.6, xA - 200, yA + 1500, 0.5)
    film.shot(L(9) - 0.3, (pA[0] + pR[0]) / 2, (pA[1] + pR[1]) / 2, 0.2, radius=20000, strength=0.2)   # vers l'Inde
    film.shot(L(9) + 0.7, xR, yR + 300, 0.55, rot=-0.5)                      # Raj
    film.shot(E(10), xR + 200, yR + 400, 0.52)
    film.shot(L(11) + 0.4, rx, ry, rz, radius=12000, strength=0.3)        # Raj et Manoj, reliés
    film.shot(E(11) + 0.2, rx + 150, ry + 100, rz * 0.97, radius=12000, strength=0.3)
    film.shot(L(12) + 0.3, xR, yR + 1400, 0.5, rot=0.4)
    film.shot(E(12) + 0.4, xM, yM + 1300, 0.45)
    film.shot(L(13) + 0.8, cx, cy, zl, radius=30000, strength=0.12)  # recul final : les cinq vies
    film.shot(film.duration, cx + 200, cy + 100, zl * 0.95, radius=30000, strength=0.1)

    film.cue("boom", W(11, "primaire"), 0.4)
    return film
