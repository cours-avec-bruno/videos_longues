# Outillage : propositions (skills, connecteurs, outils)

État au 05/11/2026, établi pendant l'analyse des réf. 03 et 04. **Tri de Bruno** : tout est retenu (« intéressant »). L'ordre de réalisation suit les priorités ci-dessous. Chaque ligne indique ce qui est **vérifié** et ce qui est **à vérifier**. Priorités : 🔴 haute · 🟠 moyenne · ⚪ plus tard.

## 1. Skills

| Skill | État | Pourquoi |
|---|---|---|
| `retro-ingenierie-video` (projet, `.claude/skills/`) | ✅ **créée** | Méthode complète d'analyse d'une référence → catalogue de procédés → reconstruction vérifiée |
| `storyboard-procedes` (projet, `.claude/skills/`) | ✅ **créée** | Lier chaque scène du storyboard à un procédé choisi par fonction, avec les règles d'usage (cohérence avant abondance) |
| `remotion-best-practices` | ✅ déjà disponible | À charger avant d'écrire une scène Remotion complexe |
| `critique-rendu-motion` | ✅ déjà disponible, ⚠️ pensée pour le 9:16 | 🟠 L'**adapter au 16:9 long format** : zones sûres YouTube, durée, rythme mesuré par l'outil d'analyse au lieu de règles TikTok |
| `motion-design-premium` | ✅ disponible, ⚠️ orientée 9:16 et 60 i/s | ⚪ Utile pour le craft (easing, glow, caméra), en ignorant les règles verticales |
| `ecriture-storytelling` (à créer) | 🧪 | 🔴 Transformer les procédés N01 à N15 en checklist d'écriture : hook, promesse différée, plants et payoffs, refrain, fin en miroir, silences écrits. À appliquer à chaque script |
| `mixage-chaine` (à créer) | 🧪 | 🟠 Chaîne de mixage reproductible (FFmpeg) : ducking, silences d'une seconde, −14 LUFS, LRA 5-8, crête ≤ −1 dBTP, avec vérification par l'outil d'analyse |
| `blender-plateau` (à créer) | 🧪 | 🟠 Scènes types Blender scriptées : plateau à figurines sans visage (I07), objet-concept lumineux (N07), architecture monumentale + brouillard (I08, I17) |

## 2. Connecteurs (MCP)

Vérifiés dans le registre MCP et dans cette session :

| Connecteur | État | Usage pour nous |
|---|---|---|
| **ElevenLabs** | ✅ **déjà connecté** (outils `creative_*`) | 🔴 Voix off (test de voix, conception de voix), **transcription** d'un audio (pour le timing mot à mot, M02 et I03). À vérifier : les effets sonores et la musique, peut-être via `creative_generate_in_flow` |
| **Higgsfield** (génération) | ✅ connecté | Plans fixes, inserts, décors (I08, I17), avec validation des crédits |
| **Higgsfield plugin** (`bl_*`, `ae_*`, `pr_*`) | ✅ disponible | Pilotage de **Blender** (After Effects et Premiere ne sont pas installés sur le PC) |
| **Blender MCP** (`mcp__Blender__*`) | ✅ disponible | Blender ouvert avec l'add-on : inspection de scène, captures, exécution de code |
| **vidIQ** | ✅ connecté | Transcriptions et analyse d'une vidéo entière (payant). À réserver à « écouter le style » d'une référence clé |
| Adobe (Creative Cloud) | Existe dans le registre, non connecté | ⚪ Inutile sans After Effects ni Premiere installés |
| Freesound, Epidemic Sound, banques d'images | ❌ **absents du registre** | Passer par leurs sites ou leurs API (voir plus bas) |

## 3. Sources de matière (hors MCP)

| Source | Pour quoi | Licence |
|---|---|---|
| **Gallica (BnF)**, Wikimedia Commons, Internet Archive | Gravures et architectures de papier (I08, I09 : Boullée, Ledoux, Piranèse), archives | Domaine public le plus souvent ; vérifier pièce par pièce |
| **Freesound** (API) | Effets sonores (S04) | CC0 ou CC-BY : noter l'auteur |
| **Poly Haven** | HDRI, textures, modèles 3D pour Blender | CC0 |
| **Mixamo** | Animations de figurines (I07) | Gratuit avec un compte Adobe |
| **Google Earth Studio** | Zooms Terre → lieu (vus dans le sponsor de la réf. 04) | Attribution obligatoire |
| **Manim** | Animations mathématiques (matrices, courbes, réf. 04) | MIT |

⚠️ **Extraits de films et d'animés** (réf. 03) : à éviter comme matière principale (Content ID, droit d'auteur). On garde le procédé d'unification (`FiltreArchive`), avec une autre matière.

## 4. Améliorations de `analyser-reference`

Les limites observées sur les réf. 03 et 04, et les ajouts proposés, par priorité :

| # | Ajout | Ce que ça débloque | Outil | Coût |
|---|---|---|---|---|
| 1 🔴 | **Transcription mot à mot** (horodatage par mot) | Débit par tranche, position exacte des phrases-clés, part des coupes sur un **mot** (M02), silences avant les phrases-clés (S01) | `faster-whisper` sur le GPU (modèle *small* ou *medium*, en int8 : tient dans 4 Go), ou ElevenLabs (connecté) | `pip install faster-whisper` |
| 2 🔴 | **Bandes de transition** : 8 images autour de chaque coupe | Micro-détails invisibles sur les planches : flashs, glitchs, *whip pans*, fondus de 2 images | FFmpeg seul | Aucun |
| 3 🔴 | **Détection d'animation à 2 ou 3 images par dessin** | Supprime les fausses rafales (*Look Back*, réf. 03 à 14:56) | FFmpeg (`mpdecimate`) ou comparaison d'images | Aucun |
| 4 🟠 | **Mouvement de caméra** par plan (fixe, panoramique, travelling, zoom) | Grammaire de caméra mesurée, et non plus devinée | OpenCV (flux optique) | `pip install opencv-python` |
| 5 🟠 | **Textes à l'écran** (OCR) | Relever les cartons, les typos, les sources, les messages cachés (T01, I14) | EasyOCR (GPU) ou Tesseract | ~1 Go |
| 6 🟠 | **Nature des sons** (impact, souffle, vent, porte, chœur…) | Répondre au « quoi », pas seulement au « où » | PANNs ou CLAP (GPU) | ~500 Mo |
| 7 ⚪ | **Mode comparaison** : deux extractions côte à côte (référence contre notre rendu) | Reconstruction vérifiée automatisée | Node | — |

## 5. Composants déjà faits (`shared/remotion/components/`)

| Composant | Procédé |
|---|---|
| `FondPoussiere` | I01 |
| `TexteBrouille` | H04, I11 |
| `TerminalChargement` | T01 |
| `FiltreArchive` | I04, H01 |
| `Mosaique` | I13, N03 |
| `TexteRevele` (existant) | I15 |

Démo : composition `Outils/Bibliotheque-Procedes` (`npm run studio`).

Prochains composants proposés : graphique construit pas à pas (I03, N09), pictos pixel art avec halo (I02, N08), schéma isométrique en style gravure (I10), glitch de transition (T02), barre de sponsor (H03).
