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

## Questions ouvertes

- [ ] Sauvegarde des médias lourds du PC (rushes, générations, rendus) : disque externe, Google Drive, NAS ?
- [ ] Voix off : la voix de Bruno ou une voix générée (ElevenLabs) ?
- [ ] Specs définitives (4K ?) une fois la DA définie.
