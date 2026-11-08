# S06 · Les années qui passent (interlude)

| | |
|---|---|
| **Durée** | ≈ 0:15 × 4 (premier passage : 15,8 s) |
| **Fabrication** | Blender (Eevee, `vignettes.py`, mannequins de `shared/blender/mannequin.py`) + montage Python (`passage.py`) |
| **Fonction** | TRANSITIONNER |
| **Procédé principal** | I07 : figurines sans visage sur un plateau (les années comme de petits tableaux de théâtre) |
| **Procédés secondaires** | M04 (une année, un tableau), I18 (une lumière par tableau), I13 (le portrait gagne un cran) |
| **Statut** | refaite en 3D à la demande de Bruno (08/11/2026) : le « journal » en interface faisait trop IA |
| **Production** | passage 1 (0 → 5 ans) monté le 08/11/2026 (`medias/S06/S06a_v1.mp4`), à valider ; passages 2 à 4 à faire |

## Intention

Le temps qui passe entre deux étapes, sans voix : les années où il n'y a rien à décider, mais où la vie a lieu. Cinq petits tableaux en 3D, posés comme sur une scène de théâtre dans le noir, sur un sol sombre qui reflète : chaque année s'allume quand la caméra arrive, s'éteint quand elle repart. Manoj est le seul personnage rouge (la couleur chaude de la vidéo, l'humain) ; les autres sont en argile grise, sans visage (références de Bruno : figurines rouges à facettes). L'âge et une phrase tirée du journal de la simulation apparaissent en bas à gauche, en typographie sobre. À la fin, son portrait revient au centre et gagne un cran de netteté (net à sa mort, en S11).

Quatre passages : 0 → 5 ans (après S05), 10 → 11 (après S07), 11 → 15 (après S08), 60 → 75 (après S09, en accélérant). Manoj peut avoir sa passion du théâtre plus tard (27 ans) : ces tableaux la préparent sans le dire.

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
2. `passage.py` : âges et phrases, fondu au noir, le portrait qui passe au 2e cran (`scenes/S05/fiche.py`, `portrait_cran`), le son.

| Âge | Tableau | Phrase à l'écran | Son |
|---|---|---|---|
| 1 an | sur une natte, sa mère penchée vers lui, il lève les bras | Son premier mot : « Maman ». | babil de bébé |
| 2 ans | accroupi au bord d'une flaque de boue (qui reflète) | La boue, jusque sur ses vêtements. | mains dans la boue, village |
| 3 ans | la nuit, sa grand-mère sur un tabouret raconte, une lampe à huile entre eux | Les histoires d'autrefois de sa grand-mère. | grillons |
| 4 ans | le foyer de terre, les rotis, sa mère accroupie ; lui, une assiette en métal | Le dal et les rotis de sa mère. | feu de bois |
| 5 ans | il court avec les autres enfants, au coucher du soleil | Courir avec les autres jusqu'au coucher du soleil. | enfants le soir |

Chaque tableau s'allume avec le claquement d'un projecteur dans une grande salle ; un souffle accompagne les passages dans le noir ; la musique de S05 revient, très bas. Les phrases viennent du journal de la simulation (`prompts/partie/7-vie-la-plus-probable.json`), raccourcies et à la troisième personne.

La première version (le « journal des années » en interface, avec de vraies vidéos) a été abandonnée : les vidéos Pexels de `medias/pexels/s06/` ne servent plus.

## Points à revoir
