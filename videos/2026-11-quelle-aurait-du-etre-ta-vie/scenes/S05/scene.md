# S05 · Les conditions de départ

| | |
|---|---|
| **Durée** | ≈ 0:40 |
| **Fabrication** | Vraies vidéos (Pexels) + interface et mosaïque en Python (`montage.py`) |
| **Fonction** | INCARNER |
| **Procédé principal** | I13 : le portrait en très gros pixels (la personne n'existe presque pas encore), un cran de netteté à chaque étape |
| **Procédés secondaires** | I04 |
| **Statut** | à valider (recalée sur la vie de Manoj, 06/11/2026) |
| **Production** | V1 montée le 08/11/2026 (`medias/S05/S05_v1.mp4`, 37 s), à valider par Bruno |

## Intention

La famille et le point de départ, sans rien choisir : le village, le petit dernier de cinq enfants, le 3e cinquième de revenus (ni pauvre ni aisé pour l'Inde), hindou, et la case « caste : OBC » sur le dossier d'école. La cuisine au feu de bois, dont la fumée pique les yeux ; l'eau qu'on va chercher plus loin les mois sans pluie. « Je n'ai rien choisi de tout ça. Lui non plus. » (C'est un double sens, compris en S13.)

Vraies photos d'un village côtier indien, unifiées (grain photo, ton chaud), sans aucune mention à l'écran. Le portrait apparaît en très gros pixels.

## Script / son

- **Voix off** : voir `../../script.md`, section S05 (version 1 du 07/11/2026, relue avec humanizer)
- **Voix** : `S05_prise1`, verrouillée par Bruno.
- **Sons / musique** : les vagues et le village sous les vraies images, le feu de bois, une toux d'enfant sous la fumée, une frappe douce par lettre sur la fiche, un clic quand la case se coche. Musique discrète (Bhimpalasi) qui entre avec le village et s'efface sur le bureau. Sources : `../../references/sons.md`.

## Découpage en plans

Matières : **3D** Blender · **UI** interface du simulateur recréée (Remotion, monospace) · **MD** motion design / animation Remotion · **IMG** vraie photo (banque libre ou archive, voir `../../references/photos.md`), animée dans Remotion · **NOIR**.

| Plan | Durée | Matière | Contenu | Animation / mouvement | Procédé | Son |
|---|---|---|---|---|---|---|
| S05-P01 | 6 s | IMG | Plan général d'un village côtier indien à l'aube : les bateaux, les filets | Lent mouvement de type Ken Burns, grain photo et ton chaud (I04) | I04 | Ambiance : mer, oiseaux, village |
| S05-P02 | 5 s | IMG | Un intérieur de maison : le foyer au feu de bois, la fumée dans la lumière, sans visage | Lent panoramique | I04 | Crépitement |
| S05-P03 | 8 s | UI | La fiche de naissance qui s'imprime : garçon · village · 3e cinquième · hindou · 4 frères et sœurs aînés · caste : OBC | Lignes tapées en monospace |  | Frappe |
| S05-P04 | 8 s | MD | Les conditions de départ de l'Inde (données du site) : espérance de vie, décès avant 5 ans (3 %), revenu par habitant | Jauges qui se remplissent |  |  |
| S05-P05 | 7 s | UI | Le portrait apparaît dans la fiche, en très gros pixels (8 blocs). C'est **la même photo** qui sera nette à la mort | Mosaïque, premier cran | I13 |  |
| S05-P06 | 6 s | 3D | L'opérateur immobile. Voix : « Je n'ai rien choisi de tout ça. Lui non plus. » | Fixe |  | Voix |

## Cadrage et mise en scène

- **Plan(s)** : large, moyen, serré, insert…
- **Angle** : face, plongée, contre-plongée, subjectif…
- **Mouvement** : fixe, travelling, panoramique, zoom…
- **Rythme / transitions** : entrée et sortie de la scène.

## Références

Images, liens, timecodes (déposer les fichiers dans `../../references/`).

## Fabrication

`montage.py` (≈ 7 min 30 de rendu ; `SON_SEUL=1` pour ne refaire que le son). Ce qui a été construit, et ce qui a changé par rapport au découpage ci-dessus :

1. carton « manoj » en gros pixels lumineux (même procédé que « commençons ») ;
2. le village au bord de la mer (vraies vidéos, étalonnage documentaire), coupé par la fiche de naissance du simulateur (`fiche.py`, refaite le 08/11 d'après les réf. 01 et 03) : nom en grand, champs étiquetés qui se tapent, les quatre aînés en pictos pixel art puis lui en ambre, cadre du portrait en attente ;
3. la maison, le feu de bois, la fumée, le chemin de l'eau, sur la voix ;
4. le formulaire : la case « OBC » se coche toute seule, la caméra se rapproche ;
5. retour sur la fiche : le visage de Manoj remplit le cadre du portrait en gros pixels ambrés (15 × 20 cases, cadrage photo d'identité sur fond noir pour qu'on lise une tête et des épaules), la caméra s'approche ; la jauge « netteté » s'allume au premier de ses 7 crans ;
6. retour au bureau, l'opérateur seul : « Je n'ai rien choisi de tout ça. Lui non plus. »

Les jauges de S05-P04 (espérance de vie, revenu) ne sont pas montées : elles alourdissaient la scène et auraient demandé des chiffres à l'écran. La voix porte l'essentiel.

## Points à revoir

- Le choix de la musique, à l'oreille (Bhimpalasi en place, Remembering en réserve).
