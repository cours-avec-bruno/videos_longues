---
name: critique-rendu-motion
description: Protocole de revue critique chiffrée d'un rendu vidéo de motion design (MP4 Remotion ou autre) et boucle d'itération V1 → V2 → V3… jusqu'à un seuil « parfait ». À utiliser dès qu'une vidéo vient d'être rendue et qu'il faut l'évaluer, la noter sur une grille, comparer deux versions, trouver les défauts précis (frame, élément, correctif) ou décider si l'on peut rendre la version finale. Fournit un script d'analyse objective (énergie de mouvement, luminance, passages statiques, noirs, coupes, flashs, palette, barycentre vs zones sûres TikTok/Reels, planches-contact, bandes de frames consécutives) qui marche avec le ffmpeg embarqué de Remotion, sans ffmpeg système.
---

# Critique de rendu motion design — protocole

Principe : on ne peut pas « regarder » une vidéo ; on la **mesure** (courbes) puis on **inspecte**
des images choisies (planches-contact, bandes de frames consécutives aux transitions, stills aux
moments clés). Chaque note doit citer une preuve (instant, frame, image produite).

## 0. Préparer (Windows / Git Bash)

```bash
export npm_config_cache=D:/npm-cache TEMP=D:/tmp TMP=D:/tmp   # C: plein : tout sur D:
cd <projet>
npx remotion ffprobe -v error -show_entries stream=width,height,r_frame_rate,nb_frames,duration -of csv=p=0 out/<video>.mp4
npx tsc --noEmit    # le code de la version évaluée compile
```

## 1. Analyse objective (≈ 10–20 s pour 1 min de vidéo)

```bash
python ~/.claude/skills/critique-rendu-motion/scripts/analyse_rendu.py out/<video>-vN.mp4 \
  --project . --label vN --every 1.5 --safe \
  --marks "0:Intro,6.5:Visage,9.3:Explosion,..."     `# repères de la timeline (secondes)` \
  --strips 9.3,14.6,...                               `# instants de transition → 16 frames consécutives` \
  --stills 2,5.5,...                                  `# images demi-résolution des moments clés` \
  --compare out/review/v(N-1)/metrics.csv             `# superpose la courbe de la version précédente` \
  --expect "1080x1920@60:45-60"
```
Sorties dans `out/review/vN/` : `rapport.md`, `courbes.png`, `planche_XX.png`, `strip_*.png`, `still_*.jpg`, `metrics.csv`.
Options utiles : `--freeze-thr` (seuil « quasi statique », défaut 0,12), `--freeze-min` (défaut 0,5 s), `--width` (défaut 180).

Lire ensuite, **avec l'outil Read**, dans cet ordre : `rapport.md` → `courbes.png` → toutes les planches → les strips → les stills.

Ce que disent les mesures :
- **Courbe de mouvement** = le rythme réel. La comparer au plan de rythme du brief (lent / rapide / hypnotique / montée / arrêt). Un plateau plat = monotonie ; un « mur » sans respiration = fatigue.
- **Passages quasi statiques** : interdits dans un brief « mouvement permanent » (sauf silence volontaire ≤ 0,5 s avant un impact).
- **Segments noirs** : seul le noir final (cut) est autorisé ; un noir ailleurs = fondu au noir déguisé ou trou de timeline.
- **Coupes / pops** : chaque saut d'image non voulu est un bug (apparition brutale, élément qui « pope »). Une coupe voulue doit être masquée (flash, occulteur, match-cut).
- **Flashs** : compter ; > 1 flash plein cadre / 10 s = tic.
- **Accent cyan** : médiane idéale 0,5–4 % ; p95 ≤ ~10 %.
- **Barycentre** hors zone sûre stricte > 15 % du temps = composition qui dérive vers l'UI.
- **Pixels noir pur** : > 60 % en médiane = fond « vide » (le brief exige un fond jamais vide).

## 2. Inspection visuelle (ce qu'on cherche sur les images)

Pour chaque planche / still, se demander et noter :
1. **Hiérarchie** : où va l'œil en 0,2 s ? Un seul héros ? Le reste est-il en retrait ?
2. **Profondeur** : ≥ 3 plans lisibles ? Bokeh d'avant-plan ? Perspective atmosphérique ?
3. **Lumière** : un point le plus lumineux ; glow élégant ou « néon » ; blancs brûlés ?
4. **Palette** : noir profond non bouché, blanc cassé, cyan rare et signifiant.
5. **Composition 9:16** : sujet dans la zone sûre stricte (rectangle vert), rien d'utile hors du rectangle orange.
6. **Typo** : taille ≥ 44 px (texte porteur), tracking, contraste, lisible sur mobile.
7. **Finition** : aliasing, lignes 1 px qui scintillent, banding, grain trop fort, éléments coupés au bord, artefacts.
Sur les **strips** (frames consécutives) : continuité (rien ne saute), direction du mouvement conservée à travers la transition, flou de bouger présent aux vitesses élevées, pas d'image intermédiaire « sale ».

## 3. Noter

Utiliser la grille du projet (ex. `docs/perfectionnement/grille.md`) ; à défaut la grille générique :
fluidité · profondeur · caméra · transitions · lumière · particules/matière · typographie · rythme & contraste ·
cohérence DA/palette · lisibilité mobile/zones sûres · finition · fidélité au brief. Chaque critère /10 avec
**preuve** (instant/frame/image) et **écart au niveau de référence** (ex. « Foundation d'Imaginary Forces fait X, nous faisons Y »).

Règles anti-complaisance :
- Pas de 9+ sans avoir listé au moins 2 défauts résiduels du critère et expliqué pourquoi ils sont mineurs.
- Pas de 10 sans comparaison explicite et favorable à une référence citée.
- Un seul défaut « bloquant » (texte illisible/hors zone, fondu au noir, pop, freeze > 0,5 s, noir parasite, erreur de rendu) plafonne le critère concerné à 6.
- Noter **avant** de lire la note de la version précédente (éviter l'ancrage), puis comparer.

## 4. Journal des défauts (format obligatoire)

`docs/perfectionnement/revue-vN.md` :

| ID | t (s) / frame | Scène · élément | Défaut observé | Pourquoi (principe violé) | Correctif précis (fichier, paramètre) | Impact (1–5) | Coût (1–5) | Statut |
|---|---|---|---|---|---|---|---|---|

Prioriser par `impact / coût`, corriger d'abord tout ce qui est bloquant, puis les impacts ≥ 4.
Une version = un lot cohérent (pas 40 micro-retouches dispersées) ; tester chaque correctif par un still
(`npx remotion still <Comp> out/review/f<N>.png --frame=<N> --scale=0.5`) avant le rendu complet.

## 5. Boucle d'itération

1. Corriger (code) → `npx tsc` → stills de contrôle des frames touchées → les regarder.
2. `git commit -m "vN+1: <résumé>"` (dépôt local uniquement).
3. Rendre `out/<nom>-vN+1.mp4` (segmenté si long, jamais par-dessus un fichier ouvert).
4. Relancer l'analyse avec `--compare` sur la version précédente ; noter ; journal.
5. Continuer tant que le seuil n'est pas atteint. Rendre `out/<nom>-final.mp4` seulement au seuil,
   puis vérifier `ffprobe` (dimensions, fps, durée, nb de frames).

Seuil « parfait » par défaut : **aucun critère < 8, moyenne ≥ 9, fidélité au brief ≥ 8 dans chaque section, zéro défaut bloquant**.

## 6. Rapport de version (à rendre à l'utilisateur)

Tableau des notes par version (V1, V2…), 3–5 changements majeurs par version, défauts restants,
chemin du MP4. Court, factuel, en français.

## 7. Pièges pratiques

- Un rendu segmenté (`--frames=a-b` successifs) **re-bundle le code à chaque segment** : ne jamais modifier `src/` pendant un rendu en cours (préparer la version suivante en lecture seule).
- Le ffmpeg embarqué de Remotion n'a ni `tile`, ni `select`, ni `freezedetect` : les planches se font en PIL (le script d'analyse le fait).
- Signaux qui ont révélé les défauts majeurs de la V1 de *Paréidolie* : **luminance moyenne > 90 pendant > 0,5 s** (aplat géant), **frames consécutives détectées « coupe »** autour d'un flash (flash-voile), **creux d'énergie juste avant le noir final** (fin qui retombe), **luminance qui chute juste avant un flash** (décor épuisé).
- Toujours recadrer (×2) le héros d'un still : un défaut de matière (bokeh parasite, aliasing) est invisible en planche.
