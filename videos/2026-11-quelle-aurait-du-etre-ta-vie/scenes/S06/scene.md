# S06 · Les années qui passent (interlude)

| | |
|---|---|
| **Durée** | premier passage : 36,6 s (avec la voix) ; les suivants plus courts |
| **Fabrication** | Blender (Eevee, `vignettes.py`, mannequins de `shared/blender/mannequin.py`) + montage Python (`passage.py`) |
| **Fonction** | TRANSITIONNER |
| **Procédé principal** | I07 : figurines sans visage sur un plateau (les années comme de petits tableaux de théâtre) |
| **Procédés secondaires** | M04 (une année, un tableau), I18 (une lumière par tableau), I13 (le portrait gagne un cran) |
| **Statut** | refaite en 3D (08/11/2026), puis : regardée sur l'écran de l'opérateur, avec la voix, transitions lentes, sans le portrait final |
| **Production** | passage 1 (0 → 5 ans) monté le 08/11/2026 (`medias/S06/S06a_v1.mp4`), à valider ; passages 2 à 4 à faire |

## Intention

Les premières années de Manoj, regardées sur l'écran de l'opérateur : on est assis à son bureau, l'écran s'allume, on s'en approche, et les années passent dedans. Cinq petits tableaux en 3D, comme sur une scène de théâtre dans le noir, sur un sol sombre qui reflète : chaque année s'allume quand la caméra arrive, s'éteint quand elle repart, lentement. La voix les décrit, une phrase par année. Manoj est le seul personnage rouge (la couleur chaude de la vidéo, l'humain) ; les autres sont en argile grise, sans visage (références de Bruno : figurines rouges à facettes). L'âge s'inscrit sur l'écran. À la fin, on recule : le bureau revient.

Quatre passages : 0 → 5 ans (après S05), 10 → 11 (après S07), 11 → 15 (après S08), 60 → 75 (après S09, en accélérant).

## Script / son

- **Voix off** : (repris de `script.md`)
- **Sons / musique** :

## Découpage en plans

Matières : **3D** Blender · **UI** interface du simulateur recréée (Remotion, monospace) · **MD** motion design / animation Remotion · **IMG** vraie photo (banque libre ou archive, voir `../../references/photos.md`), animée dans Remotion · **NOIR**.

| Plan | Durée | Matière | Contenu | Animation / mouvement | Procédé | Son |
|---|---|---|---|---|---|---|
| S06-P01 | 5 s | MD | Frise d'âge (0 → espérance de vie du pays), le curseur avance | Défilement continu | M04 | Pulsation régulière |
| S06-P02 | 6 s | IMG | Six vignettes de l'année, une seconde chacune (objets, lieux, saisons) | Coupes métronomiques sur le tempo | M04 | Sur le tempo |
| S06-P03 | 4 s | 3D | Le bureau : la lumière a tourné sur le mur | Accéléré de la lumière | I16 | Ambiance |

## Cadrage et mise en scène

- **Plan(s)** : large, moyen, serré, insert…
- **Angle** : face, plongée, contre-plongée, subjectif…
- **Mouvement** : fixe, travelling, panoramique, zoom…
- **Rythme / transitions** : entrée et sortie de la scène.

## Références

Images, liens, timecodes (déposer les fichiers dans `../../references/`).

## Fabrication

1. `vignettes.py` (Blender 5.2, Eevee, ≈ 2 s par image sur la carte NVIDIA) : construit les cinq tableaux, les lumières, la caméra, et rend `medias/S06/3d/####.png` (313 images). `--test` : une image par tableau.
2. `passage.py` : le bureau (image fixe `medias/S02/S02_p06_bureau.png`, rendue par `scenes/S02/plans.py --plans p06_bureau`), l'écran remplacé par les tableaux, l'approche et le recul, l'âge, la voix, le son.
3. `temps_s06.py` : le minutage commun (chaque tableau dure le temps de sa phrase).

| Âge | Tableau | Voix (prise 3) | Son |
|---|---|---|---|
| 1 an | sur une natte, sa mère penchée vers lui, il lève les bras | À un an, il dit son premier mot. Maman. | babil de bébé |
| 2 ans | accroupi au bord d'une flaque de boue (qui reflète) | À deux ans, il rentre le soir couvert de boue. | mains dans la boue, village |
| 3 ans | la nuit, sa grand-mère sur un tabouret raconte, une lampe à huile entre eux | Sa grand-mère lui raconte des histoires d'autrefois. | grillons |
| 4 ans | le foyer de terre, les rotis, sa mère accroupie ; lui, une assiette en métal | Il y a le dal et les rotis de sa mère. Un goût qu'il n'oubliera sans doute jamais. | feu de bois |
| 5 ans | il court avec les autres enfants, au coucher du soleil | Et il court avec les enfants du quartier, jusqu'au coucher du soleil. | enfants le soir |

Chaque tableau s'allume avec le claquement d'un projecteur ; un souffle accompagne les passages dans le noir. Ces sons sortent de l'ordinateur : étouffés quand on est loin de l'écran, pleins quand on est dedans ; dessous, la pièce de S01-S02. La musique de S05 revient, très bas. Les phrases viennent du journal de la simulation (`prompts/partie/7-vie-la-plus-probable.json`). Le portrait qui gagnait un cran à la fin a été retiré (Bruno ne le comprenait pas).

La première version (le « journal des années » en interface, avec de vraies vidéos) a été abandonnée : les vidéos Pexels de `medias/pexels/s06/` ne servent plus.

## Points à revoir
