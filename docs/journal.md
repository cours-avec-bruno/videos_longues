# Journal des décisions

Trace courte des décisions qui concernent tout le projet. Les décisions propres à une vidéo vont dans son dossier.

## 2026-11-04 · Mise en place du studio

- **Ligne éditoriale** : chaîne généraliste de réflexion, au format storytelling.
- **Direction artistique** : à construire plus tard, à partir des références que Bruno fournira. Rien n'est figé d'ici là.
- **Skills et outillage avancé** : plus tard, une fois la DA posée.
- **Specs provisoires** : 1080p, 24 i/s, H.264 CRF 16, -14 LUFS (détails dans `specs-techniques.md`).
- **Remotion** : un seul projet à la racine (point d'entrée `remotion/`). Les compositions vivent dans le dossier de chaque vidéo et les composants communs dans `shared/remotion/`.
- **Médias lourds** : exclus de Git.

## 2026-11-04 · Répartition cloud / PC fixe

- **Cloud** : écriture et code (recherches, storyboard, script, fiches scène, prompts, code Remotion, scripts Blender), plus les tests de rendu rapides.
- **PC fixe (Windows)** : production lourde (rendus finaux, Blender, montage) et stockage des médias. Claude Code y tourne aussi, sur le même repo.
- **Le repo GitHub fait le lien** : `git pull` en début de session, commit et push après chaque étape. Fins de ligne normalisées en LF par `.gitattributes`. Node 22 fixé par `.nvmrc`.
- Guide d'installation : `installation-pc.md`.

## 2026-11-04 · Premières références DA analysées

- Réf. 01 (true crime en figurines 3D) et réf. 02 (essai sur le panoptique), analysées dans `direction-artistique/analyses/`.
- Sources : transcriptions complètes (vidIQ, 2 × 5 crédits), analyses vidIQ de la vidéo entière (2 × 25 crédits), analyses plan par plan Higgsfield (gratuites, mais seulement sur le début des vidéos), miniatures vues et mesurées.
- Il reste **50 crédits vidIQ**, rechargés le 27/11.
- Limite : pas d'images de la vidéo elle-même, car YouTube bloque le téléchargement depuis le cloud. Il faut l'outil d'extraction d'images sur le PC pour un plan par plan complet.
- Les transcriptions complètes ne sont pas versionnées (droits d'auteur) : seules des analyses et de courtes citations sont dans le repo.

## 2026-11-05 · Outil d'analyse des références

- `npm run analyser-reference -- <lien>` : téléchargement (yt-dlp), détection des coupes franches et des fondus, planches contact horodatées, rythme et couleurs mesurés. Sorties dans `docs/direction-artistique/extractions/`.
- Testé ici sur des vidéos synthétiques (9/9 et 300/300 coupes, 0 fausse) et sur la bande-annonce de Sintel (18 plans sur ≈ 20). Le téléchargement YouTube reste **à valider sur le PC**, puisque le cloud est bloqué par YouTube.
- Prochaine étape : relancer les réf. 01 et 02 avec l'outil pour compléter leurs analyses (plan par plan sur toute la durée, couleurs mesurées).

## 2026-11-05 · Module son de l'outil d'analyse

- Le son est **très important** pour la chaîne (décision de Bruno).
- Le module mesure : sonie EBU R128 et dynamique, voix (séparation Demucs optionnelle, sinon sous-titres), respirations, silences, tempo, événements sonores (impacts, whooshes), synchronisation des coupes avec le son. Il produit aussi des frises (sonie, voix, spectrogramme, coupes et impacts alignés sur le temps).
- Les 5 crédits vidIQ de transcription ne servent pas au son : les sous-titres YouTube récupérés par l'outil les remplacent. L'analyse vidIQ à 25 crédits reste la seule qui « écoute » le style (genre, instruments, timbre) : à garder pour quelques références clés.
- Autotest : `npm run tester-analyse`, qui valide l'installation sur le PC.

## 2026-11-05 · Machines

- **PC fixe** : carte NVIDIA. C'est la machine de production (Blender en OptiX, rendus finaux, analyses de références avec séparation Demucs sur GPU). Le guide d'installation inclut PyTorch en version GPU (CUDA).
- **Machine de discussion** : sans carte graphique. Bruno y échange avec Claude, mais rien de lourd ne doit y tourner.

## 2026-11-05 · Projet déplacé sur le disque D

- Le disque C du PC fixe n'avait plus que 22 Go libres sur 214, contre 147 Go libres sur D.
- Le projet est maintenant dans `D:\Studio\videos_longues`. `C:\Studio\videos_longues` est une **jonction** vers D : le script d'installation, les sessions Claude et la mémoire de Claude gardent le même chemin.
- Le projet ne pesait que ≈ 760 Mo (surtout `node_modules`) : le déplacement libère peu sur C. L'intérêt est que les médias à venir (rushes, générations, rendus, extractions) iront sur D.
- Le reste de C est occupé par autre chose : Windows, logiciels, PyTorch, caches. C'est à surveiller.

## 2026-11-05 · Réf. 03 et 04, catalogue de procédés

- Analyse complète de la réf. 03 (CroustiJu, *Le paradoxe de l'intelligence*) et de la réf. 04 (ASTRE, *La Bibliothèque de Babel*) avec `analyser-reference --separer` : toutes les planches regardées, frises, transcriptions, images en pleine résolution.
- **REA** (github.com/morluto/rea) est un outil de rétro-ingénierie de logiciels, inutilisable sur une vidéo. On a repris **sa méthode** : preuves étiquetées, registre des inconnues, reconstruction vérifiée. → `docs/direction-artistique/methode-retro-ingenierie.md` et la skill `retro-ingenierie-video`.
- Création du **catalogue de procédés** (`docs/direction-artistique/procedes/catalogue.md`, 59 procédés en 6 familles) et d'un champ « Procédés » dans le modèle de fiche scène.
- 5 composants Remotion reproduisent les procédés les plus transposables (`FondPoussiere`, `TexteBrouille`, `TerminalChargement`, `FiltreArchive`, `Mosaique`). Ils sont vérifiés par des rendus fixes.
- Propositions de skills, de connecteurs et d'améliorations de l'outil d'analyse : `docs/outillage-propositions.md`. ElevenLabs est **déjà connecté**, et n'a pas encore servi.
- Point de vigilance : la réf. 03 repose sur de nombreux extraits de films et d'animés. On garde le procédé d'unification, mais avec une autre matière (droits).
- Aucun crédit dépensé.

## 2026-11-05 · Tri des procédés et storyboard

- Bruno a trié un par un les procédés extraits. **Couche 1** (proposés d'office) : 55, dont **toutes les images**. **Couche 2** (sur besoin précis) : N06 refrain retourné, N08 pictogramme-personnage, N12 confession du narrateur. **Écarté** : N13 sponsor tissé dans la métaphore. Skills, améliorations de l'outil et ressources : tout est retenu.
- Exigence de Bruno : chaque procédé **défini correctement**, et un usage **cohérent et raisonné**. En avoir beaucoup ne doit pas créer de confusion. D'où :
  - le catalogue réécrit en fiches complètes (définition, fonction, quand, éviter si, recette, exemple, compatibilités) ;
  - un mode d'emploi (`procedes/README.md`) : fonctions narratives, 10 règles d'usage, grammaire de vidéo ;
  - les modèles `storyboard.md` et `scene.md` : grammaire, fonction, procédé principal justifié, bilan des procédés ;
  - la skill `storyboard-procedes` : au storyboard, je propose pour chaque scène les 2 ou 3 procédés les plus pertinents, et Bruno arbitre ;
  - `CLAUDE.md` (section 4) mis à jour.

## 2026-11-05 · Première vidéo : « Quelle aurait dû être ta vie ? »

- Concept de Bruno, autour du simulateur *1 sur 8 milliards* (1in8b.life). Dossier `videos/2026-11-quelle-aurait-du-etre-ta-vie/`.
- Le site autorise les vidéos, même monétisées, à condition de citer « 1 sur 8 milliards, 1in8b.life ». Ses règles sont vérifiées et consignées dans `references/sources.md` : choix qui changent des probabilités mais pas le résultat, arrêts à 5, 15, 30, 50 et 70 ans, 4 autres bébés nés à la même seconde, comparaison avec son vrai lieu de naissance. France : 0,48 % des naissances, soit 1 sur 207.
- Décisions de Bruno : **tout est fabriqué** (Blender, Remotion, couche Higgsfield), rien n'est filmé ; voix off = l'opérateur à la 1re personne ; images de la vie générées.
- Premier storyboard construit avec la skill `storyboard-procedes` : grammaire (un bureau en huis clos dont la lumière suit l'âge, ambre = l'humain, mono = dans la simulation, serif = hors de la simulation), 15 scènes, 24 procédés, 5 signatures. À arbitrer par Bruno.

## 2026-11-05 · Règle : jamais de « look IA »

- Décision de Bruno : **une vidéo de la chaîne ne doit jamais être reconnaissable comme faite à l'IA**. Pour « Quelle aurait dû être ta vie ? », les illustrations sont de **vraies photos** (banques libres, archives), sans aucune mention d'IA à l'écran.
- Règles anti-« look IA » posées dans le storyboard :
  - pas de visage ni de personnage généré ;
  - mouvements de photo lents, pas de parallaxe ni d'animation par IA ;
  - un même traitement photo pour toutes les sources ;
  - une 3D crédible et imparfaite ;
  - Higgsfield jamais visible tel quel ;
  - voix humaine, musique composée par un humain.
- Conséquence sur la question ouverte de la voix off : une **voix humaine** est recommandée.
- Précision de Bruno : on **privilégie l'animation, le motion design et la 3D**. Les photos ne sont qu'un complément.
- **Reprise prévue le 06/11/2026** : affiner le storyboard et commencer la création des scènes.

## 2026-11-06 · « Quelle aurait dû être ta vie ? » : le spectateur croit jouer

- Décision de Bruno : **le spectateur croit jouer, mais il ne joue pas.** À chaque grande décision, la vidéo affiche les options et leurs pourcentages (« À VOUS ») et laisse le spectateur choisir. En secret, l'opérateur prend **toujours l'option la plus probable**. Il l'avoue à la fin (nouvelle scène **S13 · L'aveu**, procédé N02), avant la France et le déterminisme social.
- Les scènes S13-S15 deviennent **S14-S16**. Le storyboard compte 16 scènes et 98 plans, pour ≈ 11 min 15.
- Pour que « le plus probable » soit mesuré et non deviné : l'**API officielle** du site (`/api/v1/live`) donne les probabilités de chaque décision, et une `seed` permet de rejouer la même vie (voir `references/sources.md` de la vidéo). La clé gratuite est à demander par Bruno.
- Le storyboard reste à arbitrer scène par scène.

## 2026-11-06 · Skills de production vidéo

- Panel établi d'après l'annuaire skills.sh et GitHub, avec le contenu des skills lu : `docs/skills.md`.
- Le Tier 1 est installé dans le projet (`.claude/skills/`, `skills-lock.json`), donc disponible aussi dans le cloud :
  - les 13 skills Remotion officielles ;
  - `yt-script`, `yt-retention`, `yt-edit`, `yt-package` ;
  - `video-design` ;
  - 8 skills de production documentaire (montage, son, mixage, musique, étalonnage, typographie, motion graphics).
- L'ancienne `remotion-best-practices` globale est archivée dans `~/.claude/skills-archive/`.
- Manque repéré : une skill d'écriture de voix off en français, façon essai narratif. On la créera au moment du script.
- Tri demandé par Bruno (le dossier doit rester court) : **13 skills gardées** sur 30. Les 12 sous-skills Remotion faisaient doublon avec le routeur. Retirées aussi : `yt-edit`, `music-supervision-scoring`, `color-grading-finishing`, `title-kinetic-typography`, `motion-graphics-direction`.
- **Règle** (ajoutée à `CLAUDE.md`) : comme pour les procédés, Claude choisit lui-même la skill adaptée à chaque tâche (une principale, deux au maximum) et l'annonce. La table « tâche → skill » est dans `docs/skills.md`.

## 2026-11-06 · La partie est jouée : Khadija Ibrahim

- Une seule partie, seed 20261106, 1in8b Engine 0.9.52, jouée par le connecteur Claude. Les choix ont été faits par la **politique `auto` du moteur**, que la doc définit comme « ce que la plupart des gens choisissent » : c'est exactement notre règle secrète.
- La vie : Khadija Ibrahim, Algérie rurale, cinquième le plus pauvre. Elle quitte l'école à 11 ans, part à Alger à 16 ans, se marie à 24 ans, a 3 enfants (dont un meurt bébé), traverse des années de dettes et de violences, part en pèlerinage à 80 ans et meurt à 94 ans. À 6 ans, elle voulait être « youtubeuse ». Détail complet : `videos/2026-11-quelle-aurait-du-etre-ta-vie/references/partie.md`.
- Les 4 autres bébés (Kenya, Guinée, Kenya, Inde) suivent la même politique : même règle, cinq vies très différentes.
- Le connecteur ne donne pas les options ni leurs probabilités. Le script `shared/outils/1in8b/partie.py` les récupère par l'API HTTP, avec la variante « ambitieuse ». **À lancer par Bruno avec sa clé.**
- À arbitrer : le recalage des étapes d'âge sur la vraie vie (11 ans au lieu de 15), le traitement des passages sensibles (violences, enfant mort).

## 2026-11-06 · La vie la plus probable, naissance comprise

- Précision de Bruno : « les choix les plus probables » vaut aussi pour la **naissance**. La vie de la vidéo naît donc en Inde (17,6 % des naissances), à la campagne (68 % des bébés indiens simulés), garçon, dans le 3e cinquième (les cinquièmes sont équiprobables). La religion et la caste sont les plus fréquentes, mesurées par le moteur.
- Version provisoire jouée par le connecteur : **Yash Gupta** (caste tirée par le moteur). La vie définitive sortira du script `shared/outils/1in8b/partie.py`, qui a maintenant les options `--country`, `--sex`, `--place`, `--fifth` et `--mesurer faith,caste`.
- Khadija (Algérie, tirée au sort) devient une vie de comparaison.

## 2026-11-06 · Vie définitive : Manoj Mohanty

- Le moteur a mesuré la religion et la caste les plus fréquentes pour un garçon indien de la campagne, 3e cinquième : hindoue (47 sur 60) et OBC (28 sur 60).
- **Découverte** : la politique `auto` tire au sort selon les parts réelles. Elle ne prend pas toujours l'option majoritaire. La vie définitive a donc été jouée pas à pas (`/live`) en prenant à chaque décision l'option la plus fréquente, estimée sur 200 vies nées dans les mêmes conditions. Les scripts sont `parts_decisions.py` et `jouer_plus_probable.py`.
- L'API ne publie aucune probabilité par option : les pourcentages des encarts « À VOUS » seront des **parts observées**, à présenter comme telles.
- La variante ambitieuse de la même naissance réussit beaucoup mieux (professeur, 89 ans). L'aveu doit dire « une pente, pas une interdiction ».
- Environ 800 unités sur 2 000 consommées ce mois-ci.

## 2026-11-06 · Storyboard recalé sur la vie de Manoj

- Les fiches S04, S05 et S07 à S11 suivent maintenant la vie de Manoj. Les cartons d'âge tombent à 0, 5, 11, 15, 24, 26, 60 et 75 ans.
- Les 6 « À VOUS » : 7 ans (loisirs, une quasi-égalité pour apprendre le jeu), **11 ans (l'école, 97 %, refusée faute d'argent : le pivot)**, 15 ans (premier emploi), 24 ans (tuberculose), 26 ans (mariage), 60 ans (retraite).
- Nouveaux plants : « ingénieur » (8 ans) → l'aveu ; la carte des naissances qui s'arrête au plus dense (l'Inde) → « pas même son pays » ; l'école refusée → « la seule fois où j'ai choisi comme vous ».
- L'aveu (S13) est reformulé : « Ce n'est pas une interdiction : c'est une pente. »
- La durée estimée monte à ≈ 12 min 30, à resserrer au script. À arbitrer : la liaison et l'alcool (garder ou couper), la variante « pour réussir » (à confirmer sur beaucoup de vies avant de la montrer).

## 2026-11-05 · Branche `main`

- Création de **`main`**, la référence du projet. Avant, la branche par défaut était une branche de session cloud (`claude/wizardly-archimedes-sapbhh`), au nom généré automatiquement.
- Le PC fixe travaille directement sur `main`. Chaque session cloud travaille sur sa branche `claude/...` et ouvre une PR vers `main`.
- Le script d'installation du PC bascule maintenant sur `main`.
- Reste à faire par Bruno : définir `main` comme branche par défaut dans les réglages GitHub, puis supprimer les anciennes branches `claude/...`.

## 2026-11-07 · Script v1 : « Quelle aurait dû être ta vie ? »

- Le script complet de la voix off est écrit (`videos/2026-11-quelle-aurait-du-etre-ta-vie/script.md`), sur la vraie partie, puis relu avec la skill **humanizer** (installée dans le projet à la demande de Bruno) et vérifié fait par fait.
- Le spectateur prend la place de Manoj : à chaque « À VOUS », la voix passe en « vous avez onze ans ». La question naît d'un fait placé avant le compte à rebours. Deux fois seulement (11 et 60 ans), une vraie question est posée au spectateur sur sa propre vie.
- L'aveu abandonne « ce n'est pas une interdiction, c'est une pente » : c'est le tic n° 1 de l'écriture d'IA, et la phrase sous-entendait un fait faux. À la place, une observation tirée de la partie : en 75 ans, la question de l'université ne lui a jamais été posée, et le mot n'apparaît qu'une fois, pour son petit-fils.
- Nouveau calcul : en comptant la religion et la caste, la naissance la plus probable ne concerne qu'environ 1 bébé sur 200, presque la même chance que de naître en France (1 sur 207). C'est le rapprochement de S14.
- Environ 950 mots dits, soit à peu près 7 min 20 de voix.
- À décider : garder ou non le mensonge des 39 ans ; la variante ambitieuse (à confirmer sur beaucoup de vies) ; les chiffres de l'Insee (à vérifier) ; la voix.

## 2026-11-07 · Méthode de fabrication de la vidéo

- Décision de Bruno : on suit le storyboard pas à pas. **Chaque scène est générée une par une**, puis retravaillée ensemble avant de passer à la suivante.
- Quand toutes les scènes existent, on monte une **V1 globale**, qu'on retouche ensuite dans son ensemble.
- La variante ambitieuse (conclusion, S13) est traitée à la fin.

## 2026-11-07 · Retours de Bruno sur le storyboard

- On n'affiche pas les pourcentages. **Jamais à l'écran, même dans l'aveu** (décision de Bruno) : c'est la voix qui dit la règle.
- Tout ne se passe pas dans le bureau : c'est l'intro, avec quelques plans de retour. La vie de Manoj a ses lieux.
- Blender fait les scènes 3D, Higgsfield leur donne vie (pas Remotion). Règle ajoutée à `CLAUDE.md`, section 5.
- Le jeu est implicite : pas d'« À VOUS » répété, chaque étape est amenée par la précédente.
- Plus de moments en 3D.
- Tout cela s'appliquera au cas par cas, scène par scène, pendant la construction. Le storyboard et le script portent l'avertissement en tête.

## 2026-11-07 · Logiciel de montage : Premiere Pro pour la finition

- Remotion reste la colonne vertébrale jusqu'à la V1 : chaque scène est du code versionné, qu'on retravaille ensemble, et l'assemblage V1 se fait dans Remotion.
- Pour la finition (rythme à l'oreille, mixage, étalonnage), on passe à **Adobe Premiere Pro**, avec l'essai gratuit de 7 jours de Bruno. Claude peut y agir par les outils Premiere du plugin Higgsfield (à tester quand Premiere sera installé).
- **L'essai ne dure que 7 jours** : on ne le démarre qu'une fois la V1 prête, avec les rendus des scènes exportés en haute qualité, pour en tirer le maximum.
- Écartés : DaVinci Resolve (excellent, mais sans connecteur pour Claude), Palmier Pro (macOS uniquement, version 0.6).

## 2026-11-07 · Timeline de suivi

- Demande de Bruno : une timeline horizontale pour voir chaque scène, le script et tout ce qui est prévu, et savoir ce qui est en cours.
- Outil : `shared/outils/timeline/generer.py` (gabarit `gabarit.html`). La page est générée à partir du storyboard, des fiches, du script et de `suivi.json`. Elle montre l'avancement global, la scène en cours, les durées, la répartition des matières, les points à appliquer et à décider, et une timeline à pistes (scènes, plans, voix, son) à l'échelle du temps. Un clic sur une scène affiche ses plans et sa voix off.
- Chaque fiche a maintenant une ligne **Production** : à faire, en cours, à retravailler, validée.
- Page publiée (privée) : https://claude.ai/artifact/EnQAHrMvEwDgaZ6moaq4Hh. Elle est republiée au même lien après chaque étape.

## 2026-11-07 · Voix, son, et liberté de création

- **Le storyboard est une ligne directrice** : pendant la création, Claude peut ne pas le suivre et le changer si quelque chose n'est pas pertinent. C'est désormais la première chose écrite dans `CLAUDE.md`.
- **Voix off : ElevenLabs, voix « Guillaume »**. Cinq voix portent ce nom ; Bruno a retenu « Guillaume - Documentary and Storytelling » (ElevenLabs, identifiant `3HZyQcLKlT0a3RDeXVsP`). Cela remplace la règle « voix humaine » des règles anti-« look IA ».
- **Son** : recherche libre dans Epidemic Sound (connecté, vérifié), ElevenLabs et en ligne, avec la source et la licence notées.

## 2026-11-07 · S01 en construction : le bureau perdu dans le noir

- Décisions de Bruno : pas de carton de référence (crédit en description) ; vue subjective, on marche vers sa chaise ; **le bureau est seul au milieu d'un immense espace noir, sans fenêtre**, perdu dans l'obscurité.
- La scène est construite dans Blender par un script versionné (`videos/2026-11-quelle-aurait-du-etre-ta-vie/scenes/S01/bureau.py`), lancé en arrière-plan sur le PC (Blender 5.2, rendu OptiX sur la GTX 1650 Super). Le plugin Higgsfield pour Blender n'était pas connecté.
- Une lumière froide tombe d'en haut, un peu derrière le bureau : un îlot, avec une brume bornée au cône. L'écran est la seconde source. Le sol brillant étire le reflet de l'écran. Un câble part dans le noir.
- Images de départ, de milieu et d'arrivée rendues (hors Git, dans `medias/S01/`). Prochaine étape : Higgsfield anime la marche entre le départ et l'arrivée, après devis.
- Le `.gitignore` exclut désormais `medias/` et les `.blend`, comme le demande la règle « médias hors Git ».

## 2026-11-07 · S01 animée (V1)

- Bruno a choisi d'animer sans remplacer d'abord la chaise et la lampe.
- Higgsfield, modèle Wan 3.0 (images de début et de fin), 6 s en 1080p, sans audio : 21 crédits (FLUX 3 Video aurait coûté 48). Prompt et identifiants dans `videos/2026-11-quelle-aurait-du-etre-ta-vie/prompts/S01.md`.
- Le résultat reste fidèle au rendu Blender, sans déformation visible. Converti en 24 i/s. La caméra n'avance presque pas pendant la première seconde et demie.
- Note technique : l'envoi d'images vers Higgsfield est refusé (erreur Cloudflare 1010) si le client HTTP s'annonce comme Python ; il passe avec un en-tête de client standard.

## 2026-11-09 · Le storyboard ne se suit plus à la lettre

- Décision de Bruno : à la construction, on ne suit pas le storyboard à la lettre. La vidéo doit être un **habile mélange** de motion design, de 3D Blender, d'emprunts aux références et d'improvisation.
- Fixe : l'intention de chaque scène, la voix off validée, les règles de la chaîne et la grammaire. Libre : plans, ordre, procédé, outil, transitions, ajouts.
- Chaque écart est noté dans une nouvelle section « Écarts au storyboard » de la fiche scène. Un écart qui change sensiblement l'intention, le contenu ou la durée est montré à Bruno avant d'être figé.
- Mis à jour : `CLAUDE.md` (sections 4 et 5), le modèle de fiche scène et la skill `storyboard-procedes`.

## Questions ouvertes

- [ ] Sauvegarde des médias lourds du PC (rushes, générations, rendus) : disque externe, Google Drive, NAS ?
- [x] Voix off : ElevenLabs, voix « Guillaume - Documentary and Storytelling » (ElevenLabs, identifiant `3HZyQcLKlT0a3RDeXVsP`) (07/11/2026).
- [ ] Specs définitives (4K ?) une fois la DA définie.

## 2026-11-07 · S01 V2 : marche plus lente et son

- Demande de Bruno : ajouter le son et ralentir la cadence de la marche.
- Marche régénérée sur 10 s (Wan 3.0, 35 crédits). Le modèle ne produit pas de balancement de tête : ajouté en post-production, calé sur une cadence d'un pas toutes les 0,95 s.
- Son construit par script (`scenes/S01/son.py`, outil partagé `shared/outils/son/pas.py`) à partir de sons Epidemic Sound (registre `references/sons.md`) : nos pas, l'air d'un grand hall, le ronflement de l'ordinateur et de la lampe qui montent à l'approche, une réverbération synthétique. Pas de musique.
- Livré : `medias/S01/S01_v2.mp4` (hors Git). À écouter au casque par Bruno : le son n'est vérifié que par mesures.

## 2026-11-07 · S01 : l'écran montre des vies simulées

- Demande de Bruno : sur l'ordinateur, des timelines de vies simulées, discrètes mais reconnaissables, puis deux portraits robots.
- Incrustation suivie image par image dans la marche existante (`scenes/S01/ecran.py`), sans nouvelle génération vidéo. Portraits robots générés par Higgsfield (GPT Image 2.6, 0,5 crédit en tout).
- Livré : `medias/S01/S01_v4.mp4`. On passe à la S02, à la demande de Bruno.

## 2026-11-07 · S02 en construction : on s'assoit

- S02 repensée pour le décor sans fenêtre : on s'assoit en vue subjective, l'écran de S01 (vies simulées, portraits robots, compteur), la lampe de bureau qu'on allume, un plan large avec une silhouette de dos (choix de Bruno), puis la question sur fond noir, sans chiffre (curseur de « rien » à « tout »).
- Images clés dans Blender (`scenes/S02/plans.py`, à partir de la scène de S01). Plans sans génération : travelling vers l'écran, gros plan du compteur (`compteur.py`), la lampe, la question (Remotion, `S02-Question`).
- `scenes/S01/ecran.py` devient réutilisable (`--t0` pour la continuité du compteur, `--image` pour exporter l'interface).
- Higgsfield (validé par Bruno, 49 crédits) : « on s'assoit » et « la silhouette de dos » (Wan 3.0).
- Bruno retire la question au spectateur (« quelle part de votre vie avez-vous choisie ? ») et valide les images de S02. Conséquence : S16 reprenait « le chiffre du début », à repenser.
- Voix de S02 : ElevenLabs, deux prises ; Bruno retient la prise 1. Son monté par `scenes/S02/montage.py` → `medias/S02/S02_v1.mp4` (34 s).
- Correction du son : le filtre loudnorm (une passe) agissait comme un gain automatique et écrasait les nuances. Remplacé par un gain fixe + limiteur (`shared/outils/son/pas.py`, `ecrire_normalise`) ; toutes les scènes partagent le même gain général, pour que le décor sonore garde son niveau aux raccords. Son de S01 refait (`S01_son_v3.wav`, remis sur `S01_v4.mp4`).
- Retours de Bruno sur S02 : dernière phrase changée (« Vous allez m'accompagner dans cette aventure. ») ; « on s'assoit » traversait la chaise → refait entièrement dans Blender (vrai mouvement de chaise) ; le plan fixe sur l'écran devient une vraie utilisation du logiciel (pointeur, fiches au survol, clic « nouvelle vie », fiche sans visage). Le bouton « nouvelle vie » est aussi ajouté à l'écran de S01 (`S01_v5.mp4`) pour le raccord.
- Tasse blanche retirée (demande de Bruno), sans nouveau rendu : décor Blender corrigé pour la suite (`bureau.py`), et effacement en post sur les plans existants (`scenes/S01/effacer_tasse.py` : suivi + image propre alignée image par image). S01 → `S01_v6.mp4` ; S02 : début de « on s'assoit » effacé, plan de la lampe recadré. Reste le plan large final (S02-P05), où le remplissage laisse des raccords visibles.

## 2026-11-07 · S03 et S04 réécrites par Bruno : le voyage jusqu'en Inde

- S03 : on reste sur l'écran (fenêtre « Nouvelle vie », « France » tapé). S04 réécrite par Bruno : « Commençons. On peut atterrir n'importe où » ; douze lieux du monde traversés ; la Terre vue de l'espace ; plongée sur l'Inde ; un village : « C'est ici que nous sommes arrivés. Pas étonnant : plus de dix-sept pour cent de la population mondiale vit ici. »
- Extraits réels : Pexels (licence libre, usage commercial, attribution non obligatoire ; registre `references/images.md`). La Terre : calculée image par image d'après NASA Blue Marble (domaine public, via Wikimedia Commons ; le serveur de la NASA ne répondait pas), `scenes/S04/terre.py`, sans rendu 3D.
- Son : traversées, grondement jusqu'à l'espace, vrai enregistrement d'un village d'Uttar Pradesh. Toutes les prises de voix ramenées au même niveau.
- Abandonnés : le carton « 0 AN », la carte des naissances, « INDE · UN VILLAGE · UN GARÇON » ; « Il s'appelle Manoj » passe en S05.
- Livré : `medias/S04/S03_S04_v1.mp4` (37 s) ; S01 à S04 à la suite : `medias/S01_a_S04_apercu.mp4` (1 min 21).
- Retours de Bruno sur S03-S04 : l'écran des réglages est retiré (on va directement à « Commençons ») ; la voix de S04 sonnait différente (plus aiguë, mesurée à 112 Hz contre 92 Hz en S02) → phrases regénérées dans la continuité du texte de S02, prise choisie et **verrouillée** par Bruno ; raccord S01 → S02 rendu fluide (même cadrage au début de « on s'assoit », fondu d'un quart de seconde, plus de retombée du son en fin de S01). Livré : `medias/S01_a_S04_apercu_v2.mp4` (1 min 08).
- Passage du monde refait (Bruno) : 6 lieux au lieu de 12, plus rapide, effet « écran de surveillance » bleu cyan (bichromie, trame, lignes, halo) d'après une référence de Bruno, coupes glitchées avec négatif bleu et sons numériques ; la Terre perd le cyan en arrivant (retour au réel). Nouvel outil partagé : `shared/outils/image/effets.py`. Livré : `medias/S01_a_S04_apercu_v3.mp4` (1 min 02).
- S03 devient un carton (Bruno) : coupe nette depuis S02, « commençons » en lettres à empattements pixelisées avec lueur (style donné par Bruno, outil `carton_pixel`), puis coupe glitchée sur les villes. Livré : `medias/S01_a_S04_apercu_v4.mp4` (1 min 01).
- Retouches (Bruno) : souffle coupé après « aventure » (S02) ; mini-flash blanc avec un souffle d'air et un léger impact avant « commençons ». Les raccords entre scènes vivent maintenant dans `videos/2026-11-quelle-aurait-du-etre-ta-vie/assemblage.py` (sortie : `medias/S01_a_S04_apercu.mp4`).
- S04 (Bruno) : sur « plus de dix-sept pour cent », glitch puis carte du monde des densités (Kontur Population 2023, CC BY ; Natural Earth), projection Equal Earth légèrement courbée, l'humain en rouge-ambre, l'Inde qui se dessine et pulse sur « vit ici » ; Inde = 17,8 % dans les données. Procédés des références : T02, I03, I02, H01, I04 (étalonnage documentaire du village, outil `etalonnage_doc`).
- Carte des densités (S04) validée par Bruno.

### 08/11/2026 · S05, le village de Manoj

- S05 construite (`scenes/S05/montage.py`, V1 37 s) : carton « manoj » en pixels lumineux, le village de pêcheurs au bord de la mer (vraies vidéos Pexels, étalonnage documentaire), la fiche de naissance tapée ligne à ligne, la maison, le feu de bois et la fumée, le chemin de l'eau, la case « OBC » qui se coche seule, le visage en très gros blocs chauds, puis l'opérateur seul. Voix : `S05_prise1`, **verrouillée** par Bruno. Musique discrète (Epidemic, Bhimpalasi), à confirmer à l'oreille.
- Les jauges prévues en S05-P04 (espérance de vie, revenu) ne sont pas montées : chiffres à l'écran, et la voix suffit.
- Le village de S04 passe au bord de la mer (vu du ciel, puis des pêcheurs qui poussent une barque), avec les vagues sous le village.
- Raccord S04 → S05 dans `assemblage.py` : coupe nette de la carte au carton « manoj », un bref éclat de glitch. Sortie : `medias/S01_a_S05_apercu.mp4`.
- Fiche de naissance de S05 refaite (Bruno) d'après les références : HUD inspiré des fiches profil de la réf. 01 (étiquettes en capitales, données en monospace, coins de viseur), pictos pixel art et accent unique de la réf. 03 ; le portrait n'est plus un plan à part : il remplit le cadre de la fiche, en cadrage photo d'identité sur fond noir (on lit enfin un visage), avec une jauge de netteté à 7 crans qui annonce qu'il deviendra net.
- Nouvelle fiche de naissance et portrait de S05 validés par Bruno ; S05 validée en V1 (la musique reste à confirmer à l'oreille). Prochaine : S06.

### 08/11/2026 · S06, le journal des années

- Piste choisie par Bruno : « le journal des années ». Écran du simulateur (même interface que la fiche), compteur d'âge en grand qui avance à chaque pulsation, une ligne du vrai journal de la simulation par année, une vraie vidéo à côté (Pexels), et le portrait qui gagne un cran de netteté à chaque passage (7 crans, net à sa mort). Outil : `scenes/S06/journal.py` (les quatre passages y seront décrits) ; le portrait par crans vit dans `scenes/S05/fiche.py`.
- Passage 1 (0 → 5 ans) monté : `medias/S06/S06a_v1.mp4` (12,8 s, -22 LUFS : plus bas qu'une scène parlée). Aperçu : `medias/S01_a_S06a_apercu.mp4`.
- Retours de Bruno : le portrait de S05 se révèle seul, au centre (plus la fiche entière) ; le « journal des années » faisait trop IA (couleurs, interface). S06 refaite en 3D : cinq petits tableaux de théâtre dans le noir, mannequins low poly sans visage (Manoj seul en rouge, les autres en argile grise) d'après les deux références de Bruno, sol sombre qui reflète, une lumière par tableau, la caméra qui file de l'un à l'autre ; âge et phrase en typographie sobre. Nouvel outil partagé : `shared/blender/mannequin.py` (mannequins posables par script, réutilisables pour S07 à S09). Rendu Eevee, sans crédits génératifs.
- S06 reprise (Bruno) : plus de portrait à la fin ; la voix décrit chaque année (prise 3, choisie par mesure) ; transitions lentes ; les tableaux sont regardés sur l'écran de l'opérateur (on part du bureau, on s'approche de l'écran, on ressort à la fin) ; lampe allumée par continuité avec S02 (`S02_p06_bureau.png`). Durée : 36,6 s.
- S06 (Bruno) : plutôt qu'un moniteur en 3D, les tableaux passent dans une fenêtre d'interface de PC (sa capture de référence) : petits bords ronds, marge sombre autour, léger quadrillage de pixels ; la fenêtre s'ouvre et se referme. 34,6 s.
- S06, passage 1 (0 → 5 ans), validé par Bruno. Prochaine : S07.

### 08/11/2026 · S07, l'enfance

- Construite d'après la demande de Bruno (« un mix de motion design, 3D, images d'illustration, montage dynamique qui transmet des émotions ») : tableaux 3D (`scenes/S07/tableaux.py`, avec le nouveau module partagé `shared/blender/plateau.py`), vraies images Pexels, le choix à 7 ans en motion design (trois vignettes, un curseur qui hésite, pas de pourcentages), « ingénieur » sur le dessin d'un pont, l'éclair du coup de baguette, la classe où tous lèvent la main sauf lui, le deuil au piano. La fenêtre d'interface devient un outil partagé (`shared/outils/image/fenetre.py`), avec le passage fluide fenêtre / plein écran. 52,8 s, -14,6 LUFS.
- Voix : prise 2 (choisie par mesure). **Quota ElevenLabs presque épuisé** : la 3e prise a échoué, 250 crédits restants.
- Aperçu : `medias/S01_a_S07_apercu.mp4` (3 min 07).
- S07 (Bruno) : le moment « ingénieur » retravaillé en motion design. Le mot remonte, 200 silhouettes (une par vie simulée née dans les mêmes conditions) apparaissent, 198 s'éteignent : deux seulement font des études d'ingénieur (chiffre de la simulation elle-même). Nouvelle phrase : « Un rêve plutôt ambitieux. Sur deux cents vies nées comme lui, deux seulement font des études d'ingénieur. » Une seule prise possible (crédits ElevenLabs épuisés), un peu aiguë, baissée au rubberband. S07 : 58,5 s.
- S07 v2 (Bruno) : narration en prise 1 (la prise 2 avait une autre couleur de voix) ; plus de choix à 7 ans ni de coups de baguette ; nouvelles phrases : « À l'école, il est plutôt timide. Souvent au fond de la classe, à écouter. » (Manoj au dernier rang) et « À dix ans, le premier gros évènement de sa vie arrive. » Puis, après les funérailles, on recule : c'était un écran, dans une salle de surveillance en 3D (`scenes/S07/salle.py`, d'après l'image de référence de Bruno : bleu nuit, reflets, chrome), un mur d'écrans avec des instants de sa vie, deux « simulateurs » en costume sombre, peau pâle. Ils parlent de lui (« Je lui ai laissé la vie douce, jusqu'à maintenant », « C'est le moment de reprendre les rênes ») et posent le premier choix : continuer l'école ou travailler pour aider sa famille ; elle se tourne vers nous : « À toi de voir. » Ce choix quitte S08, qui devient la conséquence. Les répliques sans voix (crédits épuisés) sont en sous-titres provisoires. S07 : 74,6 s.
- S07 : voix générées après la recharge. Narration : nouvelles phrases dans la continuité de « À huit ans… », **prise 1** (règle de Bruno : pour Guillaume, toujours la prise 1, sans mesurer ni choisir). Dialogue : le simulateur en Nori (prise 1), la simulatrice en Sara (prise 2), avec un peu de pièce autour de leur voix. Plus de sous-titres provisoires. S07 : 75,4 s.
- S07, retours de Bruno : le rêve reprend la version d'hier (sans retouche de hauteur) ; « arrive » n'est plus coupé ; nouvelle phrase « Il perd son grand-père. » ; moins d'écho sur les voix de la salle ; « L'école. » devient « Il faut qu'il continue l'école. Ses frères et sœurs n'ont pas eu cette chance. » S07 : 77,6 s.

### 08/11/2026 · S08, le bon choix ne suffit pas

- Déroulé validé par Bruno, qui demande « un vrai travail de motion design cohérent », des intégrations réfléchies, des transitions et des couleurs travaillées, inspirées des références. Grammaire : la salle = ceux qui regardent ; on entre dans l'écran (ses coins s'envolent jusqu'à la fenêtre d'interface) pour la vie de Manoj, on en ressort par le même chemin ; on plonge en plein écran dans les données (noir chaud, crème et rouge, comme « ingénieur »). Un élément rouge porte la continuité : la carte « Continuer l'école » se replie en curseur et écrit la conséquence ; à la fin, la silhouette rouge reste seule et le spectateur apparaît à côté.
- Les données viennent de la simulation : sur 200 vies nées comme lui, 176 choisissent l'école à 11 ans ; une vingtaine n'iront pourtant pas au collège. La phrase du site devient une réplique de la simulatrice.
- Voix : Guillaume prise 1 (dans la continuité de S07), Nori, Sara. S08 V1 : 46,4 s. Aperçu S01 à S08 : 4 min 18.

### 09/11/2026 · S07 et S08 retravaillées (retours de Bruno)

- Plus d'écran noir entre S07 et S08 : S07 s'arrête sur le clic ; « Bon choix. Reste à savoir s'ils pourront payer » ouvre S08 sur l'écran de la salle.
- L'école de S08 refaite pour qu'on la comprenne (enseigne « ÉCOLE », uniformes, cartables, petit portail vert : plus de « barreaux de prison »).
- Nouvelle méthode 3D (Bruno) : Blender construit la scène, Higgsfield l'embellit (restylage `gpt_image_2_6` dans la DA de ses trois références : laque rouge pour Manoj, laque noire et chrome pour les simulateurs, ambiance cyan, reflets nets), puis l'anime (Kling 3.0 pro). Appliquée à toute la salle (S07 et S08) et à tous les tableaux de S07 et S08. Les écrans de la salle restent incrustés au montage : coins Blender reportés dans la vidéo IA par homographie (ORB + RANSAC) et suivis image par image (`scenes/S08/hf.py`). Règle Kling : ne jamais écrire « latex » ni décrire des enfants (refus « nsfw ») ; « mannequin figures made of shiny lacquered plastic ».
- Dialogue : une onde de quelques barres crème accrochée à la tête de celui qui parle, vivante avec sa voix (composition Remotion `Dialogue`, données `scenes/S07/dialogue.py`, `scenes/S08/dialogue.py`). Volontairement sans texte ni HUD, pour ne pas faire « IA ».
- Perfectionnement d'après les références : silence d'une seconde avant les phrases-clés (réf. 03), cloche de l'école à l'entrée du portail, léger dédoublement du signal au plus fort des traversées d'écran (réf. 02, 04).
- Crédits Higgsfield : environ 200 sur la journée (≈ 970 → ≈ 770).
