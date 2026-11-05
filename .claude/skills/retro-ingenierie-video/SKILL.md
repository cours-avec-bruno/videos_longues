---
name: retro-ingenierie-video
description: Analyse méthodique d'une vidéo de référence (lien YouTube ou fichier) pour en extraire tous les procédés de fabrication (écriture, image, montage, transitions, habillage, son) et les rendre réutilisables pour la chaîne. À utiliser dès que Bruno donne une référence vidéo à analyser, demande « comment ils ont fait », veut « inverser » un procédé, enrichir la direction artistique ou comparer un de nos rendus à une référence. Méthode inspirée de REA (preuves, inconnues, reconstruction vérifiée), appliquée avec l'outil analyser-reference du studio.
---

# Rétro-ingénierie d'une vidéo de référence

Méthode complète et justification : `docs/direction-artistique/methode-retro-ingenierie.md`. Résumé opérationnel ci-dessous.

## 0. Où tourner

L'extraction se fait **sur le PC fixe** (YouTube bloque le cloud ; Demucs utilise le GPU). Depuis le cloud ou la machine sans GPU, ne lancer que l'analyse d'extractions déjà poussées.

## 1. Extraire

```powershell
npm run analyser-reference -- <lien> --separer --demucs "py -3.12 -m demucs"
```

Lancer en arrière-plan (3 à 4 min pour 25 min de vidéo). S'il y a plusieurs références, les lancer **l'une après l'autre** (4 Go de mémoire vidéo). Les sorties vont dans `docs/direction-artistique/extractions/<id>/`, les médias dans `.cache/references/<id>/`.

## 2. Lire, puis regarder

1. `resume.md` : rythme, rafales, plans longs, palette, sonie, voix, respirations, silences, synchronisation, événements.
2. **Toutes les planches** (`planches/`), sans exception. Noter les matières, les typographies, les compositions, les objets récurrents et les changements de palette.
3. Les **frises** (`frises/`) aux endroits où le son et le montage se répondent : rafales, respirations, fin.
4. La **transcription** : convertir le `.vtt` de `.cache/references/<id>/` en texte horodaté. Repérer le hook, la promesse, les plants et leurs payoffs, les refrains, les phrases-clés, la chute.
5. La **description** (`video.info.json`) : crédits, outils, musiques, équipe, sources.
6. Des **images en pleine résolution** pour les micro-détails : `ffmpeg -v error -ss <t> -i .cache/references/<id>/video.mp4 -frames:v 1 <scratchpad>/x.png`.

## 3. Écrire

- La fiche d'analyse va dans `docs/direction-artistique/analyses/refNN-<nom>.md`. Modèle : `ref03-paradoxe-intelligence.md`.
- Chaque affirmation porte une étiquette : **[MES] [OBS] [TRANS] [DESC] [HYP] [?]**.
- La fiche se termine par « Ce qu'on retient pour nous » (à prendre, à adapter, à éviter) et par un **registre des inconnues** (la question, et ce qu'il faudrait pour trancher).
- Se méfier des pièges connus de l'outil :
  - une animation dessinée à 2 ou 3 images par dessin donne de fausses rafales de coupes ;
  - un *whip pan* peut fusionner deux plans ;
  - un bruitage sous la voix peut échapper à la détection sans `--separer`.

## 4. Extraire les procédés

Ajouter ou enrichir les entrées de `docs/direction-artistique/procedes/catalogue.md` : un identifiant (famille N, I, M, T, H ou S + numéro), la source avec ses timecodes, l'effet recherché, la recette dans nos outils, l'effort et l'état. Si un procédé existe déjà, ajouter la nouvelle référence à sa ligne plutôt que de créer un doublon.

## 5. Reconstruire et vérifier

Pour les procédés à fort potentiel :
1. coder le composant (`shared/remotion/components/`) ou le script (`shared/blender/`) ;
2. l'ajouter à la démo `Outils/Bibliotheque-Procedes` ;
3. le rendre, puis **regarder** les images ;
4. si le procédé porte sur le rythme ou le son, analyser **notre** rendu avec le même outil (`npm run analyser-reference -- out/<rendu>.mp4 --id test-<procede>`) et comparer les mesures visées à celles de la référence.

## 6. Clore

- Mettre à jour `docs/direction-artistique/README.md` (tableau des références) et `docs/journal.md`.
- Commit et push.
- Résumer à Bruno : les 5 procédés les plus forts, ce qui est déjà reproduit, et les inconnues qu'il peut trancher (une écoute, un avis de goût).

## Garde-fous

- Ne jamais présenter le son comme entendu.
- Ne pas dépenser de crédits (vidIQ, Higgsfield) sans accord. Les mesures locales suffisent dans la grande majorité des cas.
- On extrait des mécanismes, on ne copie pas une œuvre. Signaler les procédés qui reposent sur des contenus sous droits (extraits de films) et proposer une matière de remplacement.
