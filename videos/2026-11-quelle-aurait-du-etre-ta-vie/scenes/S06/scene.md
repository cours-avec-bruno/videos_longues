# S06 · Les années qui passent (interlude)

| | |
|---|---|
| **Durée** | ≈ 0:12 × 4 (premier passage : 12,7 s) |
| **Fabrication** | Python (`journal.py`, même interface que la fiche de S05) + vraies vidéos (Pexels) |
| **Fonction** | TRANSITIONNER |
| **Procédé principal** | M04 : une année ≈ une seconde, le temps devient un rythme |
| **Procédés secondaires** | I16 |
| **Statut** | piste « le journal des années » choisie par Bruno (08/11/2026) |
| **Production** | passage 1 (0 → 5 ans) monté le 08/11/2026 (`medias/S06/S06a_v1.mp4`), à valider ; passages 2 à 4 à faire |

## Intention

Le temps qui passe entre deux étapes, sans voix : les années où il n'y a rien à décider, mais où la vie a lieu. Le compteur d'âge avance d'un an à chaque pulsation ; pour chaque année, une ligne du vrai journal de la simulation (le texte dit « vous ») ; à côté, une vraie image qui lui fait écho. La fenêtre s'ouvre et se referme sur le portrait de Manoj, qui gagne un cran de netteté à chaque passage : le temps lui donne un visage (net à sa mort, en S11).

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

`journal.py <passage>` (`a` pour 0 → 5 ans ; `SON_SEUL=1` pour ne refaire que le son). Les passages sont décrits dans `PASSAGES` : âge de départ, crans du portrait, et pour chaque année la ligne du journal, la vidéo d'archive (début, cadrage) et l'ambiance.

Passage 1 :

| Âge | Ligne du journal (texte de la simulation) | Archive (Pexels) |
|---|---|---|
| 1 an | Vous avez dit votre premier mot : un mot qui voulait dire « Maman ». | 16270511, un bébé dans des mains |
| 2 ans | En jouant dans la boue, vous avez complètement sali vos vêtements. | 5451849, trois garçons et la terre (noir et blanc) |
| 3 ans | Votre grand-mère paternelle vous racontait des histoires d'autrefois. | 40379978, une grand-mère et un garçon |
| 4 ans | Le goût du dal avec des rotis que vous préparait votre mère, vous ne l'oublierez sans doute jamais. | 36100216, des rotis sur le feu de bois |
| 5 ans | Vous avez couru et joué avec les enfants du quartier jusqu'au coucher du soleil. | 3978429, des enfants dans un champ au soleil bas |

Son : une pulsation grave à chaque année (synthétisée, comme un cœur), un tic doux pour la frappe, un éclat numérique à chaque archive, le village ou le feu très bas sous l'image, un souffle grave sous tout le passage. Le portrait se redivise sous une pluie de tics.

## Points à revoir
