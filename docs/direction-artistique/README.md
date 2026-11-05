# Direction artistique

> En construction. La DA sera définie à partir des références que Bruno fournira.

## Analyser une référence

1. Sur le PC : `npm run analyser-reference -- <lien YouTube>`. Cela produit des planches contact et des mesures dans `extractions/<id>/`.
2. Pousser le dossier généré, puis demander l'analyse à Claude, dans le cloud ou en local. L'analyse se rédige dans `analyses/`.

## Comment déposer des références

- Les images vont dans `references/`, avec un nom explicite (ex. `lumiere-clair-obscur-film-x.jpg`).
- Les vidéos lourdes ne vont pas dans Git : notez plutôt le lien (YouTube, Drive) et le timecode dans la liste ci-dessous.
- Pour chaque référence, une ligne sur **ce qui plaît** : la lumière, le rythme, la typo, les transitions, l'ambiance…

## Références

| Réf. | Vidéo | Analyse | Ce qui plaît |
|---|---|---|---|
| 01 | [Le diable s'habille en Yoda](https://www.youtube.com/watch?v=5zQ8Yn11Kp8) | [`analyses/ref01-mareko-scarla.md`](analyses/ref01-mareko-scarla.md) | *à compléter par Bruno* |
| 02 | [Le Panoptique](https://www.youtube.com/watch?v=K8Ugw48gnNk) | [`analyses/ref02-panoptique.md`](analyses/ref02-panoptique.md) | *à compléter par Bruno* |
| 03 | [Le paradoxe de l'intelligence (CroustiJu)](https://www.youtube.com/watch?v=CG2jTExMv88) | [`analyses/ref03-paradoxe-intelligence.md`](analyses/ref03-paradoxe-intelligence.md) | *à compléter par Bruno* |
| 04 | [Le Vertige Infini de la Bibliothèque de Babel (ASTRE)](https://www.youtube.com/watch?v=J3JsyxABi0g) | [`analyses/ref04-bibliotheque-babel.md`](analyses/ref04-bibliotheque-babel.md) | *à compléter par Bruno* |

Synthèse croisée : [`analyses/synthese-ref01-ref02.md`](analyses/synthese-ref01-ref02.md).

## Procédés et méthode

- **Mode d'emploi des procédés** : [`procedes/README.md`](procedes/README.md) (couches, fonctions, règles d'usage, grammaire d'une vidéo).
- **Catalogue** : [`procedes/catalogue.md`](procedes/catalogue.md). 55 procédés en couche 1, 3 en couche 2, 1 écarté (tri de Bruno du 05/11/2026). Le storyboard s'en sert via la skill `.claude/skills/storyboard-procedes/`.
- **Signatures possibles de la chaîne** (récurrentes dans les 4 références, à décider) : lieu ou objet-concept (N04, N07), lumière unique sur fond sombre (I18), une couleur d'accent, silences écrits (S01, M05), fin en miroir (N14).
- **Méthode de rétro-ingénierie** (inspirée de REA) : [`methode-retro-ingenierie.md`](methode-retro-ingenierie.md), appliquée par la skill `.claude/skills/retro-ingenierie-video/`.
- **Composants prêts** : `shared/remotion/components/` (démo `Outils/Bibliotheque-Procedes`).

## À définir ensuite

Palette, typographies, traitement de l'image (grain, contraste, étalonnage), style d'animation, transitions types, identité sonore, habillage (titres, sous-titres, chapitres).
