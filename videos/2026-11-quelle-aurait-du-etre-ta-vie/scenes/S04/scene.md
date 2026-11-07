# S04 · Naître

| | |
|---|---|
| **Durée** | ≈ 0:20 |
| **Fabrication** | Extraits réels (Pexels) + la Terre calculée d'après la NASA (`terre.py`) ; montage et son : `montage.py` |
| **Fonction** | RÉVÉLER |
| **Procédé principal** | T01 : la première apparition du carton d'âge fixe son sens (une étape de la vie simulée) |
| **Procédés secondaires** | S01, I15 |
| **Statut** | à valider (recalée sur la vie de Manoj, 06/11/2026) |
| **Production** | V3 (`S03_S04_v2.mp4`, 18 s avec S03) : six lieux, effet cyan, coupes glitch ; à valider par Bruno |

## Intention

**Ajout du 07/11/2026 (Bruno)** : sur « plus de dix-sept pour cent », glitch (T02) puis une carte du monde légèrement courbée (projection Equal Earth, qui respecte les surfaces) où la densité de population s'allume en rouge-ambre, des zones les plus denses aux moins denses (I03 : la carte se construit sur la voix ; I02 : un seul accent, l'humain). La caméra glisse vers l'Inde, le reste du monde s'éteint un peu, le contour de l'Inde se dessine et pulse sur « vit ici ». Source en bas à gauche (H01, crédit CC BY). Données : Kontur Population 2023 ; contrôle : Inde = 17,8 %. Le village reçoit un étalonnage documentaire chaud (I04). Fabrication : `carte.py`.


**Révision du 07/11/2026 (Bruno)** : moins de lieux et plus de rythme, avec un effet sur les images d'après une référence de Bruno (bichromie bleu cyan, trame de points, lignes de balayage). Six lieux (Shibuya, tour Eiffel, Christ de Rio, Gizeh, Manhattan, icebergs), un demi-plan chacun environ, coup de zoom à l'entrée, coupes glitchées avec un éclair en négatif bleu et un son numérique. Le cyan, c'est la simulation qui balaie le monde ; en sortant dans l'espace la Terre perd le cyan et retrouve ses couleurs : l'atterrissage, c'est le réel. Effet réutilisable : `shared/outils/image/effets.py`.


**Réécrite par Bruno le 07/11/2026.** Clic sur « Naître » : on plonge dans l'écran. « On peut atterrir n'importe où » : douze lieux du monde défilent vite (Tokyo, Paris, Rio, New York, Gizeh, Venise, la savane, Shanghai, Sydney, le Sahara, l'Islande, l'Amazonie), reliés par des traversées (on fonce dans l'image, on ressort dans la suivante), le rythme s'accélère et un grondement monte. On sort dans l'espace : la Terre tourne de l'Afrique à l'Asie, puis la plongée sur l'Inde (on reconnaît le sous-continent et l'Himalaya). Coupe sur un village du nord de l'Inde vu du ciel : « C'est ici que nous sommes arrivés. » Puis une ruelle du village : « Pas étonnant : plus de dix-sept pour cent de la population mondiale vit ici. » (dit, jamais écrit). Le son du village est un vrai enregistrement d'Amethi, en Uttar Pradesh.

Le carton « 0 AN », la carte des naissances et « INDE · UN VILLAGE · UN GARÇON » sont abandonnés au profit de ce voyage. « Il s'appelle Manoj » passe en S05.

Ancienne intention :

Bouton « Naître », carton 0 AN, une seconde de silence. Puis la carte des naissances du monde : des points s'allument partout, environ 4 par seconde, plus serrés là où naissent le plus de bébés. Un seul point reste allumé, **en Inde, là où ils sont le plus denses**. Ce n'est pas un hasard, mais on ne le dit pas (indice pour l'aveu de S13). Puis **INDE · UN VILLAGE · UN GARÇON**, seuls à l'écran.

Faits : l'Inde représente 17,6 % des naissances (1 sur 6) ; 68 % des bébés indiens simulés naissent à la campagne (voir `../../references/partie.md`).

## Script / son

- **Voix off** : voir `../../script.md`, section S04 (version 1 du 07/11/2026, relue avec humanizer)
- **Sons / musique** :

## Découpage en plans

Matières : **3D** Blender · **UI** interface du simulateur recréée (Remotion, monospace) · **MD** motion design / animation Remotion · **IMG** vraie photo (banque libre ou archive, voir `../../references/photos.md`), animée dans Remotion · **NOIR**.

| Plan | Durée | Matière | Contenu | Animation / mouvement | Procédé | Son |
|---|---|---|---|---|---|---|
| S04-P01 | 3 s | UI | Le bouton « Naître », le clic | Pression du bouton |  | Clic, puis la musique s'arrête |
| S04-P02 | 3 s | UI | Carton d'âge : 0 AN | Barre à à-coups (TerminalChargement, version sobre) | T01 |  |
| S04-P03 | 1 s | NOIR | Écran vide | — | S01 | Silence total |
| S04-P04 | 6 s | MD | Carte du monde schématique : des points de naissance s'allument partout, plus serrés en Inde, en Chine et en Afrique de l'Ouest ; un seul reste allumé, au plus dense de l'Inde | Points pondérés par les naissances, zoom vers le point | | Respiration, une note |
| S04-P05 | 7 s | MD | « INDE · UN VILLAGE · UN GARÇON », seuls à l'écran, en monospace | Apparition sèche, mot par mot | I15 | Musique discrète qui revient |

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
