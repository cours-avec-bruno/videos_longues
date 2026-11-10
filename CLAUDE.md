# CLAUDE.md | Studio de production vidéo YouTube

Refonte en cours (10/11/2026) : le workflow est à redéfinir avec Bruno.

- Communiquer en français.
- Référence conservée : `docs/direction-artistique/analyses/ref01-mareko-scarla.md` (« Le diable s'habille en Yoda »).
- Base technique conservée : Remotion (`remotion/`, `shared/remotion/`), outils (`shared/outils/`), Blender (`shared/blender/`), specs (`docs/specs-techniques.md`), installation (`docs/installation-pc.md`, `scripts/`).
- Médias jamais dans Git.

## Animation : Remotion (Bruno, 10/11/2026)

Tous les moments d'animation (motion design, typographie, graphiques, cartes, étiquettes, transitions animées) se font
dans **Remotion**, pas dans les montages Python. Stack de référence : `docs/stack-remotion.md` (pensée pour le vertical ;
ici on l'applique au **16:9, 1920 × 1080**). Principes repris :
- le visuel suit la voix : voix d'abord, transcription mot à mot, puis chaque animation se cale sur le mot qui la nomme ;
- tout est fonction du numéro d'image ; données précalculées une fois ;
- images de contrôle (`npx remotion still`) regardées avant le rendu complet ;
- rendu par segments, en parallèle, contrôles automatiques (durée vidéo = durée audio, sonie).

## Illustration 3D : Blender + Higgsfield

Pour illustrer certaines scènes : **Blender** construit la base (composition, mannequins sans visage, lumière), puis
**Higgsfield** l'embellit (restylage d'image dans la DA) et, si le plan doit bouger, l'anime (image vers vidéo). Une
image fixe bien montée suffit souvent : on n'anime que ce qui en a besoin. Prompts, identifiants et coûts archivés dans
`videos/<slug>/prompts/` ; estimation des crédits et accord de Bruno avant une série de générations.

## Le mélange

Chaque vidéo est un **mélange bien balancé** de trois matières :
- des **scènes d'illustration 3D** (Blender + Higgsfield) ;
- des **animations Remotion** (motion design, typographie, graphiques) ;
- des **images d'illustration** (photos, archives, images générées).

Chaque élément est **construit séparément**, puis tous sont **assemblés** au montage. Éviter les longues séries dans une
seule matière : on alterne selon ce que chaque moment doit faire comprendre ou ressentir.

## Direction artistique (d'après la réf. « Le diable s'habille en Yoda »)

- **Personnages** : mannequins 3D sans visage, en laque brillante ; le personnage principal en rouge, les autres en argent, noir ou satin.
- **Lumière** : de théâtre, dure, sur fonds quasi noirs ; un liseré rouge ou cyan découpe les silhouettes ; fort vignettage.
- **Palette** : noirs bleutés, cyan (froid, système), rouge (l'humain, le danger), quelques accents chauds ; le reste désaturé.
- **Graphisme** : étiquettes en cartouches qui nomment les acteurs et les enjeux ; typo linéale grasse en capitales, ou pixel pour les explications ; un peu de grain et de lueur, sans effet « IA ».
- **Décors** : des lieux réels simplifiés, mêlés à des scènes symboliques (tableaux, objets géants).

## Rythme et écriture

- La vidéo doit être **fluide** : pas de temps mort ni d'écran noir gratuit, des transitions motivées, la voix et l'image qui s'enchaînent sans à-coup.
- Le **script** s'écrit puis se relit avec la skill **/humanizer** (`.claude/skills/humanizer`) : une langue naturelle, sans tics d'écriture IA.
