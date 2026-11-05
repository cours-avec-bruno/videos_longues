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

## 2026-11-05 · Branche `main`

- Création de **`main`**, la référence du projet. Avant, la branche par défaut était une branche de session cloud (`claude/wizardly-archimedes-sapbhh`), au nom généré automatiquement.
- Le PC fixe travaille directement sur `main`. Chaque session cloud travaille sur sa branche `claude/...` et ouvre une PR vers `main`.
- Le script d'installation du PC bascule maintenant sur `main`.
- Reste à faire par Bruno : définir `main` comme branche par défaut dans les réglages GitHub, puis supprimer les anciennes branches `claude/...`.

## Questions ouvertes

- [ ] Sauvegarde des médias lourds du PC (rushes, générations, rendus) : disque externe, Google Drive, NAS ?
- [ ] Voix off : la voix de Bruno ou une voix générée (ElevenLabs) ?
- [ ] Specs définitives (4K ?) une fois la DA définie.
