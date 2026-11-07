# S03 · La mission

| | |
|---|---|
| **Durée** | ≈ 0:35 |
| **Fabrication** | L'écran de S02 (image fixe du bureau) et l'interface (`../S01/ecran.py --scenario s03`) ; monté avec S04 (`../S04/montage.py`) |
| **Fonction** | PROMETTRE |
| **Procédé principal** | N05 : le vrai lieu de naissance saisi (la France), « gardez ça en tête », payé en S14 |
| **Procédés secondaires** | H02 |
| **Statut** | à valider (proposition de storyboard) |
| **Production** | validée en V1 (07/11/2026) ; un carton « commençons » (V3, avec S04 : `S03_S04_v2.mp4`) |

## Intention

**Bruno (07/11/2026, suite) : plus d'écran ni de clic.** Coupe nette depuis le plan large de S02 sur un carton noir : « commençons », en lettres à empattements faites de gros pixels, avec une lueur blanche (style donné par Bruno ; `carton_pixel` dans `shared/outils/image/effets.py`), pendant que la voix dit le mot. Puis coupe glitchée directe sur les villes.


**Bruno (07/11/2026) : l'écran des réglages est retiré.** On va directement à « Commençons » : la fenêtre « Nouvelle vie » est déjà remplie (on y lit encore « France »), le pointeur se pose sur « Naître », clic, on plonge. Conséquence : la saisie de la France n'est plus montrée ; le rappel prévu en S14 est à repenser.


**Refaite le 07/11/2026** : on reste sur l'écran, dans la suite de S02. La fenêtre « Nouvelle vie » s'ouvre : il coche « le monde d'aujourd'hui », « une vie entière » ; une ligne dit que le lieu de naissance est tiré au sort comme les naissances dans le monde réel (sans chiffre) ; il tape « France » dans « Et vous, où êtes-vous né ? ». Le pointeur se pose sur « Naître » : « Commençons. » L'histogramme en pourcentages et l'insert de la main sont abandonnés (règle : pas de pourcentage à l'écran ; pas de nouveau rendu).

Ancienne intention :

Interface recréée (monospace) : le monde d'aujourd'hui, le tirage selon les naissances, la durée. Saisie du vrai lieu de naissance.

## Script / son

- **Voix off** : voir `../../script.md`, section S03 (version 1 du 07/11/2026, relue avec humanizer)
- **Sons / musique** :

## Découpage en plans

Matières : **3D** Blender · **UI** interface du simulateur recréée (Remotion, monospace) · **MD** motion design / animation Remotion · **IMG** vraie photo (banque libre ou archive, voir `../../references/photos.md`), animée dans Remotion · **NOIR**.

| Plan | Durée | Matière | Contenu | Animation / mouvement | Procédé | Son |
|---|---|---|---|---|---|---|
| S03-P01 | 6 s | UI | Réglages : « Le monde où vous naîtrez », sur le monde d'aujourd'hui | Curseur, sélection | H02 | Clics |
| S03-P02 | 7 s | UI | « Comment votre lieu est tiré » : histogramme des naissances (Inde 17,6 %, Chine 6,7 %, Nigeria 5,7 %…) | Barres qui poussent |  |  |
| S03-P03 | 5 s | 3D | Insert : la main sur la souris | Fixe |  |  |
| S03-P04 | 9 s | UI | « Votre vrai lieu de naissance (facultatif) » : la liste défile jusqu'à « France » | Défilement, sélection | N05 | Clic |
| S03-P05 | 8 s | 3D | Par-dessus l'épaule : l'écran, « France » sélectionné. Voix : « Gardez ça en tête, on y reviendra. » | Lent travelling avant | N05 | Voix |

## Cadrage et mise en scène

- **Plan(s)** : large, moyen, serré, insert…
- **Angle** : face, plongée, contre-plongée, subjectif…
- **Mouvement** : fixe, travelling, panoramique, zoom…
- **Rythme / transitions** : entrée et sortie de la scène.

## Références

Images, liens, timecodes (déposer les fichiers dans `../../references/`).

## Fabrication

Notes techniques : fichiers sources, prompts (`../../prompts/`), réglages, rendus.

## Points à revoir
