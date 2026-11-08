"""S06 · passage 1 : le minutage, partagé par vignettes.py (Blender) et passage.py (montage).

Chaque tableau dure le temps de sa phrase (voix S06_prise3), avec un peu d'air avant et après.
Les passages d'un tableau à l'autre sont lents (TRAJET), dans le noir.
"""
FPS = 24
VOIX = "S06_prise3.mp3"
# phrases de la prise 3 (début, fin en secondes dans le fichier)
PHRASES = [
    (3.95, 7.25),    # À un an, il dit son premier mot. Maman.
    (7.96, 11.15),   # À deux ans, il rentre le soir couvert de boue.
    (11.67, 14.20),  # Sa grand-mère lui raconte des histoires d'autrefois.
    (15.07, 20.05),  # Il y a le dal et les rotis de sa mère. Un goût qu'il n'oubliera sans doute jamais.
    (20.85, 24.72),  # Et il court avec les enfants du quartier, jusqu'au coucher du soleil.
]
DEBUT = 1.4          # on est au bureau, l'écran est encore noir ; le premier tableau s'allume
AVANT = 0.7          # de l'allumage d'un tableau au début de sa phrase
APRES = 1.0          # après la phrase, avant de repartir
TRAJET = 1.3         # passage d'un tableau à l'autre
SORTIE = 3.6         # à la fin : on ressort de l'écran, on revient au bureau
N_SCENES = 5
TENUES = [AVANT + (b - a) + APRES for a, b in PHRASES]
TENUES[-1] += SORTIE


def arrivee(i):
    return DEBUT + sum(TENUES[:i]) + i * TRAJET


DUREE = arrivee(N_SCENES - 1) + TENUES[-1]
N = int(round(DUREE * FPS))
