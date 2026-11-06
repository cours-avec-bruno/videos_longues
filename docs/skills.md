# Skills du studio

Treize skills au total, dans `.claude/skills/` (versionnées, donc visibles aussi dans le cloud). Les skills externes ont leur source et leur empreinte dans `skills-lock.json` ; pour les mettre à jour : `npx skills update -p`.

## Règle d'usage

Comme pour les procédés : **une skill se choisit, elle ne s'empile pas.**

1. **C'est Claude qui choisit**, à chaque tâche, sans demander. Il annonce en une ligne la skill retenue et pourquoi (« je m'appuie sur `editing-montage` pour le rythme de S09 »).
2. **Une skill principale par tâche**, deux au maximum. Aucune skill n'est obligatoire : si la tâche est simple, on n'en charge pas.
3. **Les skills du studio passent avant les skills externes** quand elles couvrent le même terrain.
4. **Les règles de la chaîne passent avant toute skill.** `CLAUDE.md`, la règle anti-« look IA », les specs (16:9 long format) et la grammaire de la vidéo l'emportent toujours. Si une skill conseille une voix de synthèse, une image générée ou une zone sûre TikTok, on ne suit pas ce conseil.
5. **Pas de nouvelle skill sans tri.** On cherche, on lit le contenu, on compare avec ce qui existe, et Bruno valide. On en retire une si elle ne sert pas.

## Quelle skill pour quelle tâche

| Tâche | Skill principale | En appui (si utile) | À savoir |
|---|---|---|---|
| Analyser une vidéo de référence | `retro-ingenierie-video` | — | Avec l'outil `analyser-reference` |
| Storyboard, choix des procédés | `storyboard-procedes` | — | Toujours, dès qu'on touche au storyboard |
| Écrire le script, l'accroche | `yt-script` | `documentary-montage-production` (faits, sources, nuance) | Pensée pour des créateurs face caméra et en anglais : on garde la méthode (accroche notée, une idée par temps, `[À L'ÉCRAN]`), on écrit dans la voix de la chaîne |
| Vérifier les faits, les sources, la loyauté d'un plan | `documentary-montage-production` | — | Séparer fait, interprétation, illustration et thèse ; c'est le complément de `references/sources.md` |
| Rythme, découpage, raccords, montage | `editing-montage` | — | Chaque plan a une fonction ; on coupe quand l'information est passée |
| Coder une scène Remotion | `remotion-best-practices` | `motion-design-premium` (séquences premium) | Le routeur officiel charge lui-même la bonne sous-partie (markup, rendu, sous-titres, cartes…) |
| Palette, typographie, mise en page des cartons et graphiques | `video-design` | — | « La couleur suit le récit » : à accorder avec la grammaire de la vidéo |
| Concevoir le son (ambiances, bruitages, silences) | `sound-design-foley` | — | Partir du découpage : où le son raconte quelque chose |
| Mixer, mesurer la sonie, livrer l'audio | `audio-mixing-mastering` | — | Script de mesure de sonie inclus (ffmpeg) ; cibles dans `docs/specs-techniques.md` |
| Critiquer un rendu | `critique-rendu-motion` | — | Après chaque rendu à valider. Ignorer les zones sûres 9:16 |
| Titre et miniature | `yt-package` | — | Au moment de la publication |
| Lire la rétention après publication | `yt-retention` | — | À partir de l'export de YouTube Studio |

⚠️ `motion-design-premium` et `critique-rendu-motion` ont été écrites pour le vertical 9:16 (TikTok, Reels). Leurs zones sûres et leur cadrage ne valent pas pour nos vidéos en 16:9. Le reste vaut (easing, caméra, lumière, grille de critique, script d'analyse).

## Les skills et leur source

| Skill | Source | Pourquoi elle est gardée |
|---|---|---|
| `storyboard-procedes`, `retro-ingenierie-video`, `motion-design-premium`, `critique-rendu-motion` | le studio | Nos méthodes |
| `remotion-best-practices` | [remotion-dev/skills](https://github.com/remotion-dev/skills) (officiel) | Contient les 12 sous-skills Remotion en un seul dossier |
| `yt-script`, `yt-package`, `yt-retention` | [jakeschincariol/youtube-agent-skill](https://github.com/jakeschincariol/youtube-agent-skill) (MIT, 4 750 ★) | Les seules skills YouTube solides trouvées. Petits scripts Python relus |
| `documentary-montage-production`, `editing-montage`, `sound-design-foley`, `audio-mixing-mastering` | [calesthio/generative-media-skills](https://github.com/calesthio/generative-media-skills) (MIT) | Le contenu le plus dense et le mieux sourcé |
| `video-design` | [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) (MIT) | Des règles chiffrées de design vidéo, proches de notre grammaire |

## Historique du tri

- **06/11/2026, recherche** : 25 requêtes sur skills.sh, vérification sur GitHub, 44 skills lues. Ont été écartées d'office :
  - les voix et avatars de synthèse, et la musique générée (règle anti-« look IA ») ;
  - HyperFrames (un moteur concurrent de Remotion) ;
  - OpenMontage (licence AGPL, qui impose sa structure) ;
  - les formats courts.
- **06/11/2026, installation puis tri** : sur 26 installées, on en garde 9 externes.
  - Retirées parce qu'elles faisaient doublon : les 12 sous-skills Remotion (déjà dans le routeur) ; `title-kinetic-typography` et `motion-graphics-direction` (couvertes par `motion-design-premium` et `video-design`).
  - Retirées parce qu'elles étaient secondaires : `yt-edit` (pensée pour des enregistrements face caméra), `music-supervision-scoring` et `color-grading-finishing` (à reprendre si un vrai besoin apparaît).
  - L'ancienne `remotion-best-practices` globale est archivée dans `~/.claude/skills-archive/`.
- **Pistes non retenues, à garder en tête** : `sound-design-film` (méthode de Walter Murch), `voiceover-direction` (si on prend un comédien), dans [guia-matthieu/clawfu-skills](https://github.com/guia-matthieu/clawfu-skills) ; `blender-cameras` et `blender-lighting` dans [roble3/cc-blender-skill](https://github.com/roble3/cc-blender-skill).
- **Manque** : une skill d'écriture de voix off en français, façon essai narratif. On la créera au moment du script de la première vidéo.
