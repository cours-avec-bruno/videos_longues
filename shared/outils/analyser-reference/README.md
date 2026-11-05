# analyser-reference

Transforme une vidéo de référence (lien YouTube ou fichier) en **matière analysable image par image** : planches contact horodatées, découpage plan par plan, rythme du montage et couleurs **mesurés**.

```powershell
npm run analyser-reference -- https://www.youtube.com/watch?v=XXXXXXXXXXX
```

Exemple de résultat : [`docs/direction-artistique/extractions/exemple-sintel-bande-annonce/`](../../../docs/direction-artistique/extractions/exemple-sintel-bande-annonce/resume.md).

## Ce que fait l'outil

1. **Téléchargement** avec `yt-dlp` : image seule, en 720p maximum, plus les métadonnées et les chapitres YouTube. Les sous-titres sont récupérés en option, si YouTube les fournit.
2. **Détection des changements de plan**, en une seule lecture de la vidéo :
   - **coupes franches**, précises à l'image près (score de changement FFmpeg en couleur). Elle repère aussi les coupes peu contrastées, par exemple entre deux images sombres ;
   - **transitions progressives** (fondus enchaînés, fondus au noir, transitions floues), en comparant les histogrammes de couleur à 1 s d'écart.
3. **Vignettes** : une par plan, plus une toutes les ~5 s dans les plans longs, pour voir le mouvement. Chaque vignette est étiquetée **sous** l'image, pour ne masquer ni sous-titres ni textes à l'écran : `P012 2/3  03:12.4  (7.2s)`, soit numéro du plan, numéro de l'image dans le plan, timecode et durée du plan.
4. **Planches contact** : 4 × 5 vignettes par planche.
5. **Couleurs** : couleur moyenne de chaque plan, palette dominante de la vidéo (pondérée par la durée des plans), luminance et saturation, et un « barcode » qui montre l'évolution de la couleur dans le temps.
6. **Rapport** `resume.md`, avec la durée des plans, les coupes par minute tranche par tranche, les plans les plus longs (moments contemplatifs), les rafales de montage, la part de fondus et la palette.

## Où vont les fichiers

| Emplacement | Contenu | Git |
|---|---|---|
| `.cache/references/<id>/` | Vidéo téléchargée, métadonnées, sous-titres, vignettes brutes | **Non** (médias lourds, droits d'auteur) |
| `docs/direction-artistique/extractions/<id>/` | `resume.md`, `plans.csv`, `planches/`, `palette.png`, `barcode.png` | Oui : c'est ce que Claude analyse, y compris depuis le cloud |

`<id>` est l'identifiant YouTube, ou le nom passé avec `--id`. Relancer l'outil sur la même vidéo réutilise le téléchargement et régénère les sorties.

## Options

```
--id <nom>                 Nom du dossier de sortie
--seuil <0-1>              Score de coupe franche (défaut 0.30)
--seuil-bas <0-1>          Score minimal d'une coupe peu contrastée (défaut 0.08)
--colonnes / --lignes      Disposition des planches (défaut 4 × 5)
--largeur <px>             Largeur d'une vignette (défaut 400)
--hauteur-max <px>         Résolution max téléchargée (défaut 720)
--cookies-navigateur <nom> Cookies du navigateur pour yt-dlp (ex. firefox)
--paralleles <n>           Extractions simultanées (défaut 4)
```

On peut aussi passer un **fichier vidéo local** à la place d'un lien, par exemple pour analyser nos propres rendus.

## Prérequis

- Node 22 et FFmpeg, déjà nécessaires au projet.
- `yt-dlp`, seulement pour les liens. Sous Windows : `winget install --id yt-dlp.yt-dlp -e`. Pour le mettre à jour, ce qui est nécessaire régulièrement car YouTube change souvent : `yt-dlp -U`.

**YouTube bloque les serveurs cloud** : l'outil se lance sur le PC. Si YouTube demande de prouver qu'on n'est pas un robot, il faut relancer avec `--cookies-navigateur firefox`.

## Fiabilité (tests du 05/11/2026)

| Test | Résultat |
|---|---|
| Vidéo synthétique, 9 plans dont des raccords sombre/sombre, zoom fractal et animation continue | 9/9 coupes à l'image près, 0 fausse coupe |
| Vidéo synthétique de 30 min, une coupe toutes les 6 s (changement de teinte seule) | 300/300, 0 fausse coupe ; **82 s** de traitement |
| Bande-annonce de Sintel (Blender Foundation), riche en fondus | 18 plans détectés sur ≈ 20 réels |

**Limites connues** :
- deux plans liés par une transition très rapide et floue (*whip pan*, mouvement violent) peuvent rester regroupés ;
- un texte qui apparaît en fondu sur un fond noir identique n'est pas toujours séparé ;
- la position d'une transition progressive est approximative (± 0,5 s) ;
- les flashs et glitchs très courts (moins de 0,12 s) sont fusionnés avec le plan voisin.

En cas de doute, les vignettes supplémentaires des plans longs (`1/3`, `2/3`…) montrent ce qui s'y passe.

## Usage et droits

C'est un outil d'**analyse privée de références**. Les vidéos téléchargées restent sur la machine, hors Git, et ne sont jamais réutilisées dans nos productions. Seules les planches réduites et les mesures sont versionnées, pour l'analyse.

La police des étiquettes est JetBrains Mono, © JetBrains, sous licence libre (`police/`).
