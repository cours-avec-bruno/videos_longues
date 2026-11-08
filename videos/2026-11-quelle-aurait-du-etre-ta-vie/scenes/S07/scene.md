# S07 · 5 ans · l'enfance

| | |
|---|---|
| **Durée** | 52,8 s |
| **Fabrication** | Blender (`tableaux.py`) + vraies vidéos (Pexels) + motion design et montage Python (`montage.py`) |
| **Fonction** | INCARNER |
| **Procédé principal** | I07 : les tableaux de la simulation (mannequins sans visage, Manoj en rouge), qui alternent avec de vraies images unifiées (I04) |
| **Procédés secondaires** | T01 |
| **Statut** | construite le 08/11/2026 à la demande de Bruno : « un mix de motion design, 3D, images d'illustration, montage dynamique qui transmet des émotions » |
| **Production** | V1 montée le 08/11/2026 (`medias/S07/S07_v1.mp4`), à valider |

## Intention

L'enfance (0 à 10 ans), en vraies photos du village : des enfants de dos ou de loin, jamais un visage identifiable.

- Le bidon d'eau avant l'aube.
- L'école privée, que ses parents paient cher ; à 9 ans, la famille s'endette.
- Les coups de baguette sur la paume : « après cela, vous n'avez plus levé la main en classe ».
- **À 8 ans : « Quand les grands vous demandaient ce que vous vouliez faire plus tard, vous répondiez toujours : ingénieur. »** C'est un plant, repris dans l'aveu (S13).

Premier encart « À VOUS », à 7 ans (ce qu'il aime faire) : **rencontres religieuses 34 %, danse 33 %, cricket 33 %**. C'est une quasi-égalité, idéale pour apprendre le jeu sans enjeu. Ici, on dit une fois, en petit : « part des vies simulées nées dans les mêmes conditions ».

## Script / son

- **Voix off** : voir `../../script.md`, section S07 (version 1 du 07/11/2026, relue avec humanizer)
- **Sons / musique** :

## Découpage en plans

Matières : **3D** Blender · **UI** interface du simulateur recréée (Remotion, monospace) · **MD** motion design / animation Remotion · **IMG** vraie photo (banque libre ou archive, voir `../../references/photos.md`), animée dans Remotion · **NOIR**.

| Plan | Durée | Matière | Contenu | Animation / mouvement | Procédé | Son |
|---|---|---|---|---|---|---|
| S07-P01 | 3 s | UI | Carton d'âge : 5 ANS | Barre à à-coups | T01 |  |
| S07-P02 | 5 s | IMG | Avant l'aube, un enfant de dos avec un bidon, sur un chemin | Lent mouvement | I04 | Pas, oiseaux |
| S07-P03 | 5 s | IMG | Une école de village : un cartable, un uniforme, des mains | Lent travelling | I04 |  |
| S07-P04 | 6 s | UI | Les lignes de l'enfance qui s'impriment : l'école privée « loin d'être négligeable », les coups de baguette, la dette de la famille | Texte tapé |  | Frappe |
| S07-P05 | 7 s | UI | **Premier encart « À VOUS »** (7 ans) : rencontres religieuses 34 % · danse 33 % · cricket 33 %, avec la mention « part des vies simulées nées dans les mêmes conditions » ; 3 s de compte à rebours, puis le clic (la plus haute) | Compte à rebours, puis clic | N02 (plant) | Tic du compte à rebours, clic |
| S07-P06 | 6 s | UI | 8 ans : « … vous répondiez toujours : ingénieur. » | Texte tapé, une ligne, tenue | | Silence relatif |
| S07-P07 | 8 s | 3D | L'opérateur penché vers l'écran. Voix | Lent travelling avant |  | Voix |
| S07-P08 | 5 s | IMG | Un plan large et calme du village, la mer au fond | Fixe, lumière qui bouge | I04 | Musique seule |

## Cadrage et mise en scène

- **Plan(s)** : large, moyen, serré, insert…
- **Angle** : face, plongée, contre-plongée, subjectif…
- **Mouvement** : fixe, travelling, panoramique, zoom…
- **Rythme / transitions** : entrée et sortie de la scène.

## Références

Images, liens, timecodes (déposer les fichiers dans `../../references/`).

## Fabrication

- `tableaux.py` (Blender, Eevee ; module partagé `shared/blender/plateau.py`) : l'école, les trois vignettes du choix (prière, danse, cricket, images fixes), les grands à 8 ans, la baguette (le bras du maître s'abat à l'image 68), la classe (les mains se lèvent une à une, pas la sienne), la dette (image fixe), les funérailles.
- `montage.py` : le déroulé, la fenêtre d'interface et le passage au plein écran (`shared/outils/image/fenetre.py`), le choix en motion design (le curseur hésite, un trait de compte à rebours, le clic, la carte qui s'agrandit), « ingénieur » sur le dessin d'un pont, l'éclair et la secousse du coup, la voix (`S07_prise2`), le son.

Grammaire : la simulation passe dans la fenêtre de l'interface ; les vraies images, le coup et le deuil sortent en plein écran. Arc : fierté, jeu, rêve, honte, inquiétude, deuil ; le piano (« Remembering ») n'entre qu'au deuil.

Changement d'intention (signalé à Bruno) : plus d'encart « À VOUS » ni de pourcentages ; le choix à 7 ans est posé par la voix, avec trois vignettes et un curseur qui hésite.

## Points à revoir
