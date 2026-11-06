# Panel de skills : script, Remotion, production vidéo

Recherche du 06/11/2026. **Le Tier 1 est installé** dans le projet depuis le 06/11/2026 (voir « Installation » en bas). Le reste du document sert à choisir plus tard.

## Méthode

- **Sources** : l'annuaire skills.sh (`npx skills find`, 25 requêtes), GitHub, et des comparatifs en ligne (Tella, aiskill.market, skillselion). Ces comparatifs sont commerciaux : je ne m'en suis servi que pour repérer des noms.
- **Critères** :
  - le nombre d'installations ;
  - les étoiles et l'activité du dépôt GitHub ;
  - la licence ;
  - les scripts exécutables inclus ;
  - **la lecture réelle du contenu** de chaque skill retenue (44 fichiers `SKILL.md` lus ou parcourus).
- **Filtre de la chaîne** :
  - on écarte tout ce qui pousse vers une voix de synthèse, des avatars, de la musique générée ou des images générées visibles (règle anti-« look IA ») ;
  - on écarte les formats courts (TikTok, Reels) ;
  - on écarte les moteurs concurrents de Remotion.

Légende : ✅ recommandé · 🟡 utile selon le besoin · ⛔ à éviter.

## Déjà installé

| Skill | Où | Remarque |
|---|---|---|
| `remotion-best-practices` | global | ⚠️ **Version ancienne.** L'officielle est devenue un « routeur » vers 12 skills spécialisées (voir plus bas) |
| `motion-design-premium`, `critique-rendu-motion` | global | Les nôtres |
| `retro-ingenierie-video`, `storyboard-procedes` | projet | Les nôtres |
| `find-skills` | global | Recherche dans l'annuaire |

## Tier 1 : à installer

### 1. Remotion officiel : `remotion-dev/skills` ✅

- **Source** : l'équipe Remotion. 6 400 ★, mis à jour le 05/11/2026, ≈ 760 000 installations.
- **Contenu** : `remotion-best-practices` (le routeur) et 12 skills :
  - `create` : démarrer une vidéo ;
  - `markup` : contenu, animation, effets, transitions, flou de mouvement, correction colorimétrique, 3D, voix off, effets sonores ;
  - `render` : l'export ;
  - `captions` : les sous-titres ;
  - `multimedia` : les durées et dimensions des médias ;
  - `maps` : des cartes animées, utiles pour la **carte du monde de S04** ;
  - `studio`, `docs`, `upgrade`, `interactivity`, `license`, `saas`.
- **Pourquoi** : c'est la mise à jour de ce qu'on a déjà, par les auteurs de l'outil.
- **Attention** : la skill `maps` contient de petits scripts JavaScript de préparation de données, du code officiel. Le dépôt n'affiche pas de licence.

### 2. YouTube, côté écriture et rétention : `jakeschincariol/youtube-agent-skill` ✅

- **Source** : 4 750 ★, licence MIT, mis à jour en 09/2026. C'est le dépôt YouTube le plus solide trouvé.
- **Contenu** :
  - `yt-script` : écrit cinq accroches d'après 21 formules, les note avec un script, garde les deux meilleures, puis écrit le script temps par temps avec `[ON SCREEN: …]` sur chaque temps ;
  - `yt-retention` : lit l'export « rétention de l'audience » de YouTube Studio et distingue la fuite de l'accroche, les falaises et la pente lente ;
  - `yt-edit` : produit une liste de coupes à partir d'une transcription ;
  - et aussi `yt-package` (titres), `yt-chapters` et `yt-viral`.
- **Pourquoi** :
  - des règles courtes et justes : « les 15 premières secondes font tout le travail », « une idée par temps », « ne jamais inventer un chiffre » ;
  - le marquage de ce qui est **à l'écran** sur chaque temps, ce qui colle à nos fiches scène ;
  - après publication, `yt-retention` est le seul vrai retour qu'on aura.
- **Limites** :
  - c'est pensé pour des créateurs face caméra et des tutos, au ton anglo-saxon ;
  - on s'en sert pour **l'accroche et la rétention**, pas pour la voix de la chaîne ;
  - 6 scripts Python sont inclus : je les lis avant de les lancer.

### 3. Production documentaire et post-production : `calesthio/generative-media-skills` (une sélection) ✅

- **Source** : 235 ★, licence MIT, mis à jour en 07/2026. Il y a peu d'installations par skill (170 à 500), mais **le contenu est le plus dense et le mieux sourcé** de tout ce que j'ai lu : chaque fait est daté et lié à sa source.
- **À prendre** :

| Skill | Ce qu'elle apporte à la chaîne |
|---|---|
| `documentary-montage-production` | La posture documentaire : séparer le fait documenté, l'interprétation, le témoignage, l'illustration et la thèse. Avec un journal des sources et des affirmations. C'est **exactement** notre règle « observé / rapporté / hypothèse » et notre `sources.md` |
| `editing-montage` | Le montage : chaque plan a une fonction (orienter, révéler, prouver, comparer…), on coupe quand l'information est passée, plans de coupe J et L, raccords, « un montage doit avoir un argument » |
| `sound-design-foley` | Les familles de sons, les ambiances, les transitions, le son émotionnel, la perspective |
| `audio-mixing-mastering` | La hiérarchie voix, musique, ambiance, les cibles de sonie et de crête (true peak). Un script de mesure de sonie est inclus |
| `music-supervision-scoring` | Où placer la musique (spotting), éviter de s'attacher à la musique témoin (temp love), licences, feuilles de montage musical (cue sheets) |
| `color-grading-finishing` | Raccorder des sources mixtes (3D, photos, interface) : utile pour unifier nos 3 matières |
| `title-kinetic-typography` | Lisibilité du texte en mouvement, durée de tenue, coupures de ligne éditoriales |
| `motion-graphics-direction` | La hiérarchie dans le temps, l'intégrité des données à l'écran |

- **À laisser de côté** dans ce dépôt :
  - les skills « providers » (avatars, musique et voix générées), contraires à nos règles ;
  - `storyboard-previsualization`, qui fait doublon avec notre `storyboard-procedes`.
- **Limite** : ces skills sont écrites pour des médias générés. On garde la méthode, pas les recettes de génération.

### 4. Design vidéo : `digitalsamba/claude-code-video-toolkit`, uniquement `video-design` ✅

- **Source** : 2 450 ★, licence MIT, mis à jour le 06/11/2026.
- **Contenu** :
  - « la couleur suit le récit » : 2 ou 3 fonds au maximum, qui ne changent qu'à un tournant du récit, avec des écarts de luminosité et pas seulement de teinte ;
  - un seul accent pour les données ;
  - 5 tailles de texte par vidéo ;
  - un même bord gauche pour tous les titres ;
  - une critique du rendu sur planche-contact.
- **Pourquoi** : c'est très proche de notre grammaire (la lumière par chapitre, l'ambre réservé à l'humain). Ça donne des règles chiffrées pour les cartons et les graphiques (S10, S14, S15).
- **Pas le kit complet** : il impose sa propre structure de projet.

## Tier 2 : utile selon le besoin

| Skill | Source | Pour quoi | Réserve |
|---|---|---|---|
| `sound-design-film` | `guia-matthieu/clawfu-skills` (150 ★, MIT) | La méthode de Walter Murch : hiérarchie du son, loi des « deux et demi », worldizing, arc émotionnel | Tournée vers le marketing |
| `voiceover-direction` | idem | Brief d'un comédien voix, script facile à dire, notes de séance | Utile si on choisit un comédien (question ouverte du journal) |
| `storytelling` | `ghaida/intent` (246 ★, CC0) | Bibliothèque de structures narratives, avec ses garde-fous | Généraliste |
| `story-sense` | `jwynia/agent-skills` (182 ★, sans licence) | Diagnostic d'un récit qui ne marche pas (rythme, fin qui ne porte pas) | Pensé pour la fiction |
| `blender-cameras`, `blender-lighting` | `roble3/cc-blender-skill` (144 ★, MIT) | Focales, profondeur de champ, travelling avant, éclairage pratique (l'écran comme seule source) : le bureau | En partie couvert par le plugin Higgsfield (`bl_*`) |
| `ffmpeg-audio-processing` | `josiahsiegel/claude-plugin-marketplace` (59 ★, MIT) | Normalisation `loudnorm`, filtres audio, règles pour les chemins Windows | Peu d'étoiles, contenu solide |
| `youtube-scriptwriting` | `cdeistopened/skill-stack` (29 ★, MIT) | Un déroulé par étapes et un « score de surprise » des faits | Fait doublon avec `yt-script`, auteur moins établi |

## ⛔ À éviter

| Skill | Pourquoi |
|---|---|
| `elevenlabs/skills@text-to-speech`, `ai-voiceover`, avatars (HeyGen, Synthesia…) | Voix et visages de synthèse : contraire à la règle anti-« look IA » |
| Musique générée (Suno, Lyria, MiniMax…) | Règle : musique composée par un humain |
| `heygen-com/hyperframes` (1,3 M d'installations) | Un autre moteur de rendu vidéo (HTML), concurrent de Remotion : on ne mélange pas |
| `calesthio/openmontage` (77 000 ★) | Un cadre complet qui impose sa structure, sous licence AGPL-3.0 (contaminante) |
| `affaan-m/ecc` (un pack de 1 068 skills) | `video-editing` est correct, mais le pack entier apporte surtout du bruit |
| `higgsfield-ai/skills@higgsfield-youtube-thumbnail` | Miniatures générées : à arbitrer plus tard avec la règle anti-IA |
| Skills TikTok, Reels, Shorts | Format court, hors sujet |

## Ce qui manque (rien de bon trouvé)

- **L'écriture de voix off en français**, façon essai vidéo narratif (réflexion, storytelling, première personne). Tout ce qui existe est anglophone et orienté « créateur de contenu ».
- **Proposition** : créer notre propre skill `script-voix-off`, nourrie de nos analyses de références (`docs/direction-artistique/`) et de nos règles (sources, nuance, pas de chiffre inventé). On la créera au moment d'écrire le script de la première vidéo, à partir de ce qui marche vraiment.

## Installation (faite le 06/11/2026)

Installées : les 13 skills Remotion, `yt-script`, `yt-retention`, `yt-edit`, `yt-package`, `video-design` et les 8 skills calesthio. Elles sont toutes dans `.claude/skills/`, avec les sources et les empreintes dans `skills-lock.json`.

Ce qui a été fait :
- les scripts inclus ont été relus : ils lisent des fichiers locaux, et le script de sonie appelle seulement ffmpeg ;
- l'ancienne `remotion-best-practices` globale a été déplacée dans `~/.claude/skills-archive/`, pas supprimée ;
- mise à jour : `npx skills update -p`.

Dans le **projet** et non en global : le cloud ne voit que les skills versionnées dans le repo. `--copy` évite les liens symboliques, qui passent mal dans Git sous Windows.

```bash
npx skills add remotion-dev/skills -s '*' -a claude-code --copy -y
npx skills add jakeschincariol/youtube-agent-skill -s yt-script -s yt-retention -s yt-edit -s yt-package -a claude-code --copy -y
npx skills add calesthio/generative-media-skills -s documentary-montage-production -s editing-montage -s sound-design-foley -s audio-mixing-mastering -s music-supervision-scoring -s color-grading-finishing -s title-kinetic-typography -s motion-graphics-direction -a claude-code --copy -y
npx skills add digitalsamba/claude-code-video-toolkit -s video-design -a claude-code --copy -y
```


## Sources

- Annuaire : https://skills.sh/ (recherches `npx skills find`, 06/11/2026)
- https://github.com/remotion-dev/skills
- https://github.com/jakeschincariol/youtube-agent-skill
- https://github.com/calesthio/generative-media-skills
- https://github.com/digitalsamba/claude-code-video-toolkit
- https://github.com/guia-matthieu/clawfu-skills · https://github.com/ghaida/intent · https://github.com/jwynia/agent-skills · https://github.com/roble3/cc-blender-skill · https://github.com/josiahsiegel/claude-plugin-marketplace · https://github.com/cdeistopened/skill-stack
- Comparatifs consultés (repérage seulement) : https://www.tella.com/blog/best-claude-code-skills · https://aiskill.market/blog/best-claude-skills-for-video-production-2026 · https://skillselion.com/guides/best-remotion-skills-for-claude-code
