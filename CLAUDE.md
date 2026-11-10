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
