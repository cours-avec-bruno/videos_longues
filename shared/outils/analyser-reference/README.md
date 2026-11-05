# analyser-reference

Transforme une vidéo de référence (lien YouTube ou fichier) en **matière analysable** :
- **image** : planches contact horodatées, découpage plan par plan, rythme du montage et couleurs mesurés ;
- **son** : sonie, dynamique, voix, respirations, silences, tempo, événements sonores (impacts, whooshes…), synchronisation du montage avec le son, et des frises sonores alignées sur le temps.

```powershell
npm run analyser-reference -- https://www.youtube.com/watch?v=XXXXXXXXXXX
```

Avec la séparation voix / accompagnement, recommandée quand le son compte :

```powershell
npm run analyser-reference -- https://www.youtube.com/watch?v=XXXXXXXXXXX --separer --demucs "py -m demucs"
```

Vérifier que tout fonctionne sur une machine (sans rien télécharger) :

```powershell
npm run tester-analyse
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
6. **Son** (voir plus bas).
7. **Rapport** `resume.md`, avec la durée des plans, les coupes par minute tranche par tranche, les plans les plus longs (moments contemplatifs), les rafales de montage, la part de fondus, la palette et toute la partie son.

## Le son

Claude ne peut pas écouter. L'outil transforme donc la bande sonore en **mesures** et en **images** lisibles :

| Mesure | Ce qu'elle dit | Méthode |
|---|---|---|
| Sonie intégrée, plage dynamique (LRA), crête vraie | Le niveau global par rapport aux −14 LUFS de YouTube, et le degré de compression | EBU R128 (FFmpeg `ebur128`) |
| Sonie par tranche + vue globale | Où ça monte, où ça respire | Sonie court terme (3 s) |
| **Voix** : temps de parole, voix au-dessus de la musique, *ducking* | La place de la voix et la façon dont la musique s'efface derrière elle | Séparation IA **Demucs** (`--separer`). Sans séparation, les sous-titres YouTube servent de repère approximatif |
| **Respirations** | Les passages sans voix (≥ 2,5 s), et ce que fait le son pendant ce temps | Voix détectée |
| **Silences** | Les vrais trous de son (≥ 0,6 s) | Niveau du mixage |
| **Tempo** | Le BPM dominant, et la part du temps avec une pulsation nette | Autocorrélation des attaques |
| **Synchronisation** | La part des coupes franches qui tombent sur une attaque sonore, comparée au hasard | Coupes image × attaques son |
| **Événements marquants** | Impacts, whooshes, chocs : position et force | Saut d'énergie soudain d'un son « bruité », hors pulsation musicale. Détectés sur l'accompagnement si séparation |

**Frises** (`frises/`) : une image par tranche de 1 à 2 min, avec de haut en bas :
- la courbe de sonie ;
- la voix (bleu) et l'accompagnement (orange) ;
- le spectrogramme : la voix y forme des bandes horizontales serrées, les impacts des traits verticaux, une nappe une couleur continue dans les graves ;
- les coupes image : blanc pour une coupe franche, gris pour un fondu ;
- les événements sonores (rouge) ;
- le temps.

C'est ce qui permet de voir le lien entre montage et son.

Plus `son-global.png` (toute la vidéo) et `son.csv` (une ligne par seconde).

### Installer Demucs (optionnel, pour `--separer`)

Demucs est gratuit et tourne en local. Il nécessite Python :

```powershell
winget install --id Python.Python.3.12 -e
```

Si le PC a une carte graphique **NVIDIA**, installer d'abord la version GPU de PyTorch. La séparation est alors environ 10 fois plus rapide :

```powershell
py -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
```

Puis :

```powershell
py -m pip install demucs soundfile
```

Ensuite, ajouter `--separer --demucs "py -m demucs"` à la commande. Le modèle (environ 80 Mo) se télécharge au premier usage.

**Durée** : sur processeur seul, environ 1/3 de la durée de la vidéo (≈ 25 min pour 70 min). Avec une carte NVIDIA, quelques minutes. Le résultat est gardé en cache : une relance ne refait pas la séparation.

Versions testées ici : Python 3.13, torch 2.15 (CPU), torchaudio 2.11, demucs 4.1.0, soundfile 0.14.

## Où vont les fichiers

| Emplacement | Contenu | Git |
|---|---|---|
| `.cache/references/<id>/` | Vidéo et audio téléchargés, métadonnées, sous-titres, pistes séparées, vignettes brutes | **Non** (médias lourds, droits d'auteur) |
| `docs/direction-artistique/extractions/<id>/` | `resume.md`, `plans.csv`, `planches/`, `palette.png`, `barcode.png`, `son.csv`, `son-global.png`, `frises/` | Oui : c'est ce que Claude analyse, y compris depuis le cloud |

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
--sans-son                 N'analyse pas la bande sonore
--separer                  Sépare voix / accompagnement avec Demucs
--demucs "<commande>"      Commande Demucs (défaut demucs ; sous Windows : "py -m demucs")
--tranche-son <s>          Durée couverte par une frise sonore
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
| Piste son synthétique (pulsation 120 BPM, 2 impacts, 10 s de silence) | 120 BPM, 2/2 impacts, silence à ± 0,1 s, avec et sans Demucs |
| Piste réaliste (musique de Sintel + voix de synthèse sur 3 segments + 3 impacts) | Voix : 95 % d'exactitude, respiration de 29,0 → 51,9 s (réel : 28,9 → 52) ; impacts : 3/3 avec séparation, 2/3 sans (le 3e est masqué par la voix) |
| 30 min de vidéo, image + son, sans séparation | 69 s de traitement |

**Limites connues (image)** :
- deux plans liés par une transition très rapide et floue (*whip pan*, mouvement violent) peuvent rester regroupés ;
- un texte qui apparaît en fondu sur un fond noir identique n'est pas toujours séparé ;
- la position d'une transition progressive est approximative (± 0,5 s) ;
- les flashs et glitchs très courts (moins de 0,12 s) sont fusionnés avec le plan voisin.

En cas de doute, les vignettes supplémentaires des plans longs (`1/3`, `2/3`…) montrent ce qui s'y passe.

**Limites connues (son)** :
- sans séparation, un bruitage noyé sous la voix peut passer inaperçu. Utiliser `--separer` quand le son compte ;
- une musique avec des chœurs ou un chant peut être comptée en partie comme de la voix ;
- le tempo peut être donné au double ou à la moitié ; il n'existe pas pour une musique sans pulsation (orchestral, nappes) ;
- les mesures disent **où** et **combien**, pas **quoi** : le genre musical, les instruments ou le timbre de la voix demandent une écoute. Pour cela, l'analyse vidIQ (25 crédits) avec une consigne centrée sur le son reste utile.

## Usage et droits

C'est un outil d'**analyse privée de références**. Les vidéos téléchargées restent sur la machine, hors Git, et ne sont jamais réutilisées dans nos productions. Seules les planches réduites et les mesures sont versionnées, pour l'analyse.

La police des étiquettes est JetBrains Mono, © JetBrains, sous licence libre (`police/`).
