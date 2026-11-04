# Vidéos longues

Studio de production des vidéos longues YouTube : storyboard, script, scènes (Remotion, Blender, outils génératifs) et assemblage.

- **Fonctionnement et principes** : [`CLAUDE.md`](CLAUDE.md)
- **Installer le PC fixe (Windows)** : [`docs/installation-pc.md`](docs/installation-pc.md)
- **Specs techniques** : [`docs/specs-techniques.md`](docs/specs-techniques.md)
- **Décisions et questions ouvertes** : [`docs/journal.md`](docs/journal.md)
- **Direction artistique** : [`docs/direction-artistique/`](docs/direction-artistique/)
- **Démarrer une vidéo** : copier [`videos/_modele/`](videos/_modele/)

## Remotion

```bash
npm install
npm run studio                                   # prévisualisation interactive
npm run render -- Test-Pipeline out/test.mp4     # rendu d'une composition
npm run typecheck
```
