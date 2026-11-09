# S07 · 5 à 10 ans · l'enfance, puis la salle des simulateurs

| | |
|---|---|
| **Durée** | 77,6 s |
| **Fabrication** | Blender (`tableaux.py`, `salle.py`) + vraies vidéos (Pexels) + motion design et montage Python (`montage.py`) |
| **Fonction** | INCARNER |
| **Procédé principal** | I07 : les tableaux de la simulation (mannequins sans visage, Manoj en rouge), qui alternent avec de vraies images unifiées (I04) |
| **Procédés secondaires** | T01 |
| **Statut** | construite le 08/11/2026 à la demande de Bruno : « un mix de motion design, 3D, images d'illustration, montage dynamique qui transmet des émotions » |
| **Production** | V2 le 08/11/2026 (`medias/S07/S07_v2.mp4`) : narration en prise 1, sans la baguette ni le choix à 7 ans, avec la salle des simulateurs et le premier choix. Voix complètes (Guillaume en prise 1, Nori, Sara) |

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

- `tableaux.py` (Blender, Eevee ; module partagé `shared/blender/plateau.py`) : l'école, les grands à 8 ans, la classe (Manoj au dernier rang, qui écoute), la dette (image fixe), les funérailles. Les plans du choix à 7 ans et de la baguette restent dans le script mais ne sont plus montés.
- `salle.py` (Blender, Eevee) : la salle de surveillance, d'après l'image de référence de Bruno (bleu nuit, reflets, chrome) : un mur d'écrans où passent des instants de la vie de Manoj (`medias/S07/ecrans/`), un grand écran central, la console, deux simulateurs (costumes sombres, peau pâle). Quatre plans : `revele` (on recule depuis l'écran), `large`, `epaule` (par-dessus l'épaule, l'écran du choix), `regard` (elle se tourne vers nous). Pour chaque image : les coins de l'écran central (`coins.json`) et son masque (`masque/`), pour y incruster au montage ce qu'il montre.
- `montage.py` : le déroulé, la fenêtre d'interface (`shared/outils/image/fenetre.py`), « ingénieur » et les 200 vies, l'écran central de la salle (la lampe, les funérailles, la classe, puis le choix : deux cartes, un trait de compte à rebours, le clic), le son (la salle : souffle des machines, bourdonnement des écrans, une tension grave).

Grammaire : la simulation passe dans la fenêtre de l'interface ; les vraies images et le deuil sortent en plein écran ; la salle est le hors-champ de la simulation, ceux qui la regardent. Arc : fierté, rêve, timidité, inquiétude, deuil, puis le recul : on découvre qu'on le regardait.

Changement d'intention (demandé par Bruno, 08/11/2026) : le premier choix n'est plus un jeu à 7 ans mais l'école ou le travail à 10-11 ans, posé par les simulateurs. Il remplace l'encart de S08 ; S08 devient la conséquence (la famille peut-elle payer ?).

## Écarts au storyboard

- Retours de Bruno (09/11, soir) : la dette a sa raison (« pour continuer à payer l'école ») ; le recul de l'écran se fait sur une image fixe de la salle (l'incrustation suivie dérapait), sans dédoublement ; voix de la salle sans réverbération ; le choix passe en plein écran, chaque option présentée avec ce qu'elle apporte et ce qu'elle risque (étiquettes pixel, illustrations), d'après une vidéo de référence de Bruno. +4,8 s.

## Points à revoir

- Voix des simulateurs (Nori, Sara) à valider à l'oreille.
- S08 à réécrire en conséquence.
