# Catalogue des procédés

Les mécanismes de fabrication (narratifs, visuels, sonores, de montage) extraits des références, avec leur recette dans nos outils. **Ce ne sont pas des choses à copier** : chaque fiche dit à quoi sert le procédé, pour pouvoir le réinventer ailleurs.

**Avant de s'en servir, lire le [mode d'emploi](README.md)** : couches, fonctions, règles d'usage, grammaire de vidéo.

- **Sources** : réf. 01 (true crime en figurines), 02 (Panoptique), 03 (Paradoxe de l'intelligence, CroustiJu), 04 (Bibliothèque de Babel, ASTRE). Analyses dans `../analyses/`.
- **Format de chaque fiche** :
  - **Définition** : ce qu'est le procédé ;
  - **Fonction** : à quoi il sert (voir le mode d'emploi) ;
  - **Quand l'utiliser** et **Éviter si** ;
  - **Recette** : comment le fabriquer chez nous ;
  - **Exemple** : une scène type ;
  - **Va avec** et **Évite avec** : les compatibilités ;
  - **Fiche** : source dans les références, effort, état.
- **Effort** : ● faible · ●● moyen · ●●● fort. **État** : ✅ composant prêt dans `shared/` · 🧪 à prototyper · 📝 de l'écriture ou du mixage (aucun outil nécessaire).
- **Tri de Bruno (05/11/2026)** : 55 procédés en couche 1, 3 en couche 2, 1 écarté.

---

# Couche 1 · proposés d'office

## N · Écriture et narration

### N01 · Jeu-expérience fait sur le spectateur
- **Définition** : le spectateur vit le phénomène dont parle la vidéo avant qu'on le lui explique. Une consigne simple, une manipulation faite à l'image, et la résolution révélée bien plus tard.
- **Fonction** : ACCROCHER, et préparer RÉVÉLER.
- **Quand l'utiliser** : un sujet sur la perception, les biais, la mémoire, l'attention, la décision. Tout ce qu'on peut faire éprouver plutôt que décrire.
- **Éviter si** : la manipulation serait gratuite ou trompeuse sans payoff, ou le sujet n'a rien d'expérimentable.
- **Recette** : une consigne d'une phrase (choisir, fermer les yeux, compter, retenir) ; la manipulation à l'image (souvent par M01) ; la résolution au moins 8 min plus tard, en rappelant mot pour mot la consigne (N05).
- **Exemple** : « Choisissez une équipe. Les rouges, fermez les yeux » ; chaque équipe voit une image différente ; à 11 min, on révèle que personne n'a vu la même chose.
- **Va avec** : M01, N05, N02 · **Évite avec** : un autre hook concurrent dans la même minute.
- **Fiche** : réf. 03 (0:00-1:15, résolu à 11:41) · ●● · 📝. Une fois par vidéo.

### N02 · Troisième groupe / twist méta
- **Définition** : la chute révèle que le comportement du spectateur pendant la vidéo était lui-même la réponse.
- **Fonction** : RÉVÉLER.
- **Quand l'utiliser** : quand la vidéo contient un jeu (N01) ou une consigne qu'un spectateur a pu ne pas suivre.
- **Éviter si** : le twist contredirait la thèse, ou s'il faut l'expliquer longuement.
- **Recette** : prévoir dès l'écriture un comportement « hors consigne » (ceux qui n'ont pas obéi, qui ont mis pause, qui ont douté) ; le nommer à la fin et en faire la solution.
- **Exemple** : « Il y avait un troisième groupe : ceux qui n'ont jamais fermé les yeux. Les curieux. »
- **Va avec** : N01, N14 · **Évite avec** : N12 juste avant (deux retournements à la suite).
- **Fiche** : réf. 03 (12:41) · ● · 📝. Une fois par vidéo.

### N03 · Promesse différée visible
- **Définition** : on montre, masqué, l'élément qui sera révélé plus tard, en disant qu'on le cache.
- **Fonction** : PROMETTRE.
- **Quand l'utiliser** : la vidéo a une « image-clé » (graphique, objet, document) qui résume la thèse.
- **Éviter si** : la révélation ne tient pas la promesse : la frustration se retourne contre la vidéo.
- **Recette** : montrer l'élément flou, pixelisé (`Mosaique`), de dos ou en silhouette ; une phrase du type « je vous le cache, pour l'instant » ; le révéler au même cadrage pour que le spectateur le reconnaisse.
- **Exemple** : le graphique flouté apparaît à 1:57 ; « l'explication tient en une image » ; il est révélé à 5:47.
- **Va avec** : I13, N05, I15 · **Évite avec** : plus de deux promesses ouvertes en même temps.
- **Fiche** : réf. 03 · ● · ✅ `Mosaique`.

### N04 · Narrateur-guide d'une visite
- **Définition** : l'exposé devient un déplacement. Le narrateur emmène le spectateur dans un lieu-concept, et chaque salle correspond à une étape de l'argument.
- **Fonction** : INCARNER, RELIER.
- **Quand l'utiliser** : une idée qui se « spatialise » (un système, une architecture, une progression par étapes).
- **Éviter si** : le sujet est une suite d'exemples sans progression, ou si les décors ne sont pas produisibles à un niveau suffisant.
- **Recette** : écrire le **lieu-concept avant le script** (plan du lieu, une salle par idée, le trajet). Verbes de mouvement et consignes (« suivez-moi, ne touchez à rien »). Seuils (T04) entre les salles, une palette par salle (I16).
- **Exemple** : la Bibliothèque de Babel visitée du hall au centre ; le panoptique parcouru de la cellule à la tour.
- **Va avec** : T04, I16, I08, M05 · **Évite avec** : un deuxième lieu-concept concurrent.
- **Fiche** : réf. 02, 04 · ●●● (décors) · 📝. Signature possible de la chaîne.

### N05 · Consigne de mémoire
- **Définition** : on demande explicitement au spectateur de retenir une image ou une phrase, puis on la rappelle mot pour mot au moment du payoff.
- **Fonction** : PROMETTRE, RELIER.
- **Quand l'utiliser** : tout plant important dont le payoff est éloigné (plus de 5 min).
- **Éviter si** : le payoff est proche, ou s'il y a déjà deux consignes en cours.
- **Recette** : « Gardez cette image, elle va revenir. » Au payoff : « Vous vous souvenez de cette image ? » + la même image au même cadrage.
- **Exemple** : la machine dans la pièce du début, revue à la fin comme l'IA.
- **Va avec** : N03, M07, T05 · **Évite avec** : plus de 2 consignes par vidéo.
- **Fiche** : réf. 04 (1:11, 7:26, 20:33) · ● · 📝.

### N07 · Objet-concept à face cachée
- **Définition** : l'idée abstraite devient un objet unique, lumineux et en lente rotation. Une de ses propriétés reste cachée jusqu'à la fin.
- **Fonction** : RELIER, RÉVÉLER.
- **Quand l'utiliser** : un concept à plusieurs facettes (l'intelligence, la vérité, la mémoire) ou un « Graal » que l'on cherche.
- **Éviter si** : la vidéo a déjà un lieu-concept fort (N04) qui porte le même rôle. Ne pas faire deux symboles centraux.
- **Recette** : un solide simple (cube, sphère, monolithe) ; matière reconnaissable (verre dépoli à fluide intérieur, or mat) ; même éclairage à chaque apparition ; la face cachée n'est jamais tournée vers la caméra avant le dernier plan. Blender (script réutilisable à faire dans `shared/blender/`).
- **Exemple** : le cube de l'intelligence aux faces « fluide, cristallisée, sociale, verbale, méta », dont la sixième, CURIOSITÉ, n'apparaît qu'à la fin.
- **Va avec** : T05, N14, I18 · **Évite avec** : N04 en concurrence.
- **Fiche** : réf. 03 (cube), 04 (cube doré) · ●● · 🧪.

### N09 · Fausses pistes dessinées
- **Définition** : avant la vraie réponse, on anime les hypothèses naïves, puis on les efface. Le spectateur parie, se trompe et retient.
- **Fonction** : EXPLIQUER.
- **Quand l'utiliser** : un résultat contre-intuitif (graphique, chiffre, expérience).
- **Éviter si** : le résultat est intuitif. L'effet de surprise tombe à plat.
- **Recette** : « À première vue, on pourrait penser à ça » (hypothèse 1), « ou à ça » (hypothèse 2), on efface, « sauf que… » et la vraie courbe. Dans un même plan (I03).
- **Exemple** : deux lignes parallèles, puis une convergence, puis la divergence réelle.
- **Va avec** : I03, S01 · **Évite avec** : plus d'une fois par vidéo sur le même type de graphique.
- **Fiche** : réf. 03 (5:24-5:47) · ●● · 🧪.

### N10 · Interdiction qui donne envie
- **Définition** : on annonce qu'on ne fera pas quelque chose, puis on le fait, avec humour.
- **Fonction** : PROMETTRE, et une transition vers une partie technique.
- **Quand l'utiliser** : avant un passage de chiffres ou de technique que le public pourrait redouter.
- **Éviter si** : le ton de la vidéo est grave à ce moment-là.
- **Recette** : plant (« surtout, n'essayez pas de calculer ») ; payoff (« je vous avais dit de ne pas calculer. Tant pis, on calcule »).
- **Exemple** : le nombre de livres de Babel.
- **Va avec** : N15 · **Évite avec** : utilisation répétée (devient un tic).
- **Fiche** : réf. 04 (1:49, 6:26) · ● · 📝.

### N11 · Nuance assumée
- **Définition** : le narrateur signale ce qui est débattu, puis montre que sa thèse tient malgré tout.
- **Fonction** : PROUVER.
- **Quand l'utiliser** : sur tout point scientifique contesté ou fragile.
- **Éviter si** : la nuance détruit la thèse. Dans ce cas, c'est la thèse qu'il faut revoir.
- **Recette** : « Ce n'est pas tranché, des chercheurs sérieux trouvent ces preuves fragiles… » ; puis « dans les deux cas, le problème reste le même ».
- **Exemple** : la planification interne des IA (débat), puis le problème est identique.
- **Va avec** : I05 · **Évite avec** : —.
- **Fiche** : réf. 03, 04 (19:50) · ● · 📝.

### N14 · Fin en miroir
- **Définition** : la dernière phrase rend la question au spectateur. Le sujet de la vidéo, c'était lui.
- **Fonction** : RÉVÉLER.
- **Quand l'utiliser** : quasiment toujours sur une chaîne qui veut « faire réfléchir ».
- **Éviter si** : la phrase devient moralisatrice. Elle doit ouvrir, pas conclure à la place du spectateur.
- **Recette** : une phrase courte, à la 2e personne ou en « nous », souvent un retournement du refrain ou du titre ; suivie de S05.
- **Exemple** : « Vous êtes le prisonnier. Vous êtes le gardien. Et vous êtes la tour. » ; « Tout est déjà écrit. C'est à nous de le dire. »
- **Va avec** : S05, M06, N02 · **Évite avec** : un résumé explicatif après.
- **Fiche** : réf. 02, 03, 04 · ● · 📝. Une fois par vidéo. Signature possible de la chaîne.

### N15 · Apartés humains
- **Définition** : on garde 2 ou 3 réactions spontanées du narrateur (soupir, « ouais, j'avais besoin d'air »).
- **Fonction** : INCARNER.
- **Quand l'utiliser** : après un passage dense ou sombre ; à la sortie d'un lieu.
- **Éviter si** : elles sont jouées ou trop nombreuses.
- **Recette** : à l'enregistrement, laisser venir ; au montage, en garder peu ; mixer plus proche et plus sec que la voix principale.
- **Exemple** : sortie de la bibliothèque, « Bon, on remonte… Ouais, j'avais besoin d'air ».
- **Va avec** : S04, N10 · **Évite avec** : un moment solennel en cours.
- **Fiche** : réf. 04 (23:20) · ● · 📝.

## I · Image

### I01 · Tableau noir vivant
- **Définition** : un aplat sombre animé par une poussière de pixels qui dérive et scintille. Le fond des explications n'est jamais figé.
- **Fonction** : EXPLIQUER (support de toutes les séquences 2D).
- **Quand l'utiliser** : comme fond par défaut des séquences de motion design.
- **Éviter si** : la scène est en 3D ou sur fond papier (I10). Ne pas mélanger deux fonds explicatifs dans la même vidéo.
- **Recette** : `FondPoussiere` (fond `#2f2f31`, 60 à 120 particules, taille ≤ 4 px, vitesse 0,2-0,3 px par image). Couleurs des particules = couleur d'accent + blanc.
- **Exemple** : tout le bloc explicatif sur le raisonnement motivé.
- **Va avec** : I02, I03, H05 · **Évite avec** : I10 dans la même vidéo, comme fond concurrent.
- **Fiche** : réf. 03 · ● · ✅ `FondPoussiere`.

### I02 · Pictos et accent unique
- **Définition** : une famille d'icônes au même style (pixel art dans la réf. 03) et une seule couleur d'accent, avec des titres en sans-serif grasse et un léger halo.
- **Fonction** : EXPLIQUER.
- **Quand l'utiliser** : pour représenter des groupes, des rôles ou des notions sans illustration coûteuse.
- **Éviter si** : la DA de la vidéo est entièrement en 3D réaliste. Un style d'icône étranger casse l'univers.
- **Recette** : une bibliothèque d'icônes vectorielles d'un seul style (pixel art ou trait) ; l'accent est réservé aux concepts (règle 3 du mode d'emploi) ; titres en grasse avec un halo de 10 à 20 px.
- **Exemple** : les groupes « démo » et « répu » en pictos roses, une échelle de 1 à 4 entre eux.
- **Va avec** : I01, I03, H05 · **Évite avec** : plusieurs styles d'icônes.
- **Fiche** : réf. 03 · ●● · 🧪 (bibliothèque d'icônes à constituer).

### I03 · Graphique construit en un seul plan
- **Définition** : un graphique qui se construit sous les yeux, élément par élément, au rythme de la voix et sans coupe.
- **Fonction** : EXPLIQUER, PROUVER.
- **Quand l'utiliser** : la preuve centrale de la vidéo repose sur des données.
- **Éviter si** : les données sont secondaires. Un chiffre suffit alors (I15).
- **Recette** : axes, puis légendes, puis hypothèses (N09), puis vraie courbe, puis mise en évidence ; chaque étape calée sur un mot de la voix (timings issus de la transcription mot à mot) ; 30 à 90 s.
- **Exemple** : « % d'accord » en fonction de l'intelligence, démocrates contre républicains, sur 84 s.
- **Va avec** : N09, I01, I05 · **Évite avec** : de couper le plan pour des extraits.
- **Fiche** : réf. 03 (P053) · ●● · 🧪 (composant graphique à faire).

### I04 · Unifier des sources hétérogènes
- **Définition** : toutes les images extérieures (archives, captures, plans générés, extraits) reçoivent le même traitement, pour se lire comme une seule matière.
- **Fonction** : HABILLER.
- **Quand l'utiliser** : dès qu'une vidéo mélange plus de 3 sources visuelles d'origines différentes.
- **Éviter si** : la source doit garder son aspect brut pour faire « preuve » (I06).
- **Recette** : `FiltreArchive` (lignes de balayage 0,1-0,15, aberration 2-4 px, bombé 0,6, teinte = couleur d'accent, source en bas à gauche). ⚠️ **Matière** : plans générés, domaine public, nos propres rendus plutôt que des films sous droits.
- **Exemple** : une série d'images d'illustration émotionnelle sur « toute ma vie, j'ai cru que… ».
- **Va avec** : H01, M03 · **Évite avec** : I06 sur la même source.
- **Fiche** : réf. 03 · ● · ✅ `FiltreArchive`.

### I05 · La source primaire à l'écran
- **Définition** : on montre le vrai document (étude, livre, article), en perspective, avec seulement le passage utile net.
- **Fonction** : PROUVER.
- **Quand l'utiliser** : à chaque affirmation qui s'appuie sur une étude ou un texte précis.
- **Éviter si** : la source n'est pas lisible ou n'apporte rien de visible.
- **Recette** : page sur fond noir, inclinaison de 10 à 20°, profondeur de champ faible (le flou autour du passage) ; lent travelling avant ; surlignage éventuel dans la couleur d'accent.
- **Exemple** : la figure de l'étude de Kahan, puis le passage de Borges en traduction.
- **Va avec** : N11, I03 · **Évite avec** : I04 (la preuve ne se maquille pas).
- **Fiche** : réf. 03, 04 · ●● · 🧪.

### I06 · Archive brute = registre preuve
- **Définition** : une archive authentique (journal télévisé, entretien, document d'époque) montrée dans son format d'origine.
- **Fonction** : PROUVER.
- **Quand l'utiliser** : pour montrer qu'une personne, un événement ou une parole est réel.
- **Éviter si** : les droits ne sont pas clairs. On peut alors se rabattre sur une photo du domaine public, ou sur un plan reconstitué et annoncé comme tel.
- **Recette** : format d'origine (4:3, noir et blanc), logo ou mention conservés, aucun filtre embellissant ; courte (2 à 5 s).
- **Exemple** : Borges en entretien à la télévision suisse.
- **Va avec** : H01 · **Évite avec** : I04.
- **Fiche** : réf. 03, 04 · ● · 📝 (sourcing).

### I07 · Figurines sans visage sur un plateau
- **Définition** : des personnages universels, sans visage, codés par couleur ou par matière, posés sur un plateau éclairé par un seul spot dans le noir.
- **Fonction** : INCARNER, RESSENTIR.
- **Quand l'utiliser** : pour représenter des groupes, des camps, des rôles sociaux, sans désigner personne.
- **Éviter si** : la scène demande une émotion de visage.
- **Recette** : Blender. Figurines basse définition (ou voxel) ; matière unie par groupe ; plateau texturé ; un spot conique ; fond noir ; caméra au ras du plateau ou en plongée. Script réutilisable à faire dans `shared/blender/`.
- **Exemple** : équipe bleue et équipe rouge face à face autour d'une image au sol ; les « curieux » en rose apparaissent derrière.
- **Va avec** : I18, I17 · **Évite avec** : des visages photoréalistes dans la même séquence.
- **Fiche** : réf. 01, 03 · ●●● (la première fois), puis ● · 🧪.

### I08 · Architecture de papier construite
- **Définition** : on construit en 3D une architecture réelle mais jamais bâtie (utopie, projet abandonné), et on y place la vidéo.
- **Fonction** : RESSENTIR.
- **Quand l'utiliser** : un lieu-concept (N04) doit être grandiose et légitime.
- **Éviter si** : le lien entre l'architecture et le sujet est artificiel.
- **Recette** : choisir dans Boullée, Ledoux, Piranèse, Lequeu, Sant'Elia… (sources : Gallica, Wikimedia) ; modéliser dans Blender (ou générer les plans fixes avec Higgsfield, gravure en référence) ; montrer les gravures d'origine (I09).
- **Exemple** : la sphère du Cénotaphe de Newton [hypothèse] devient l'extérieur de la bibliothèque.
- **Va avec** : N04, I09, I17, M05 · **Évite avec** : un décor générique sans histoire.
- **Fiche** : réf. 04 · ●●● · 🧪.

### I09 · Dessin ↔ modèle
- **Définition** : des documents d'origine (gravures, plans, photos) intercalés une seconde chacun au milieu des plans 3D du même objet.
- **Fonction** : PROUVER.
- **Quand l'utiliser** : avec I08, ou dès qu'on reconstitue quelque chose qui a existé.
- **Éviter si** : il n'y a pas de document d'origine.
- **Recette** : 3 à 5 documents, 0,9 à 1 s chacun, en coupe franche pendant un mouvement de caméra 3D ; une photo des tirages sur une table pour finir.
- **Exemple** : la coupe de la sphère de Boullée qui s'intercale entre deux plans de la sphère en 3D.
- **Va avec** : I08, M04 · **Évite avec** : I04 (les documents restent bruts).
- **Fiche** : réf. 04 (3:20-3:33) · ● · 📝 (sourcing).

### I10 · Schéma en style gravure
- **Définition** : les explications sont dessinées dans le style de l'univers de la vidéo (trait isométrique, papier, typo serif), au lieu d'un motion design générique.
- **Fonction** : EXPLIQUER.
- **Quand l'utiliser** : quand la vidéo a un univers « livre, archive, savoir ancien ».
- **Éviter si** : le fond explicatif de la vidéo est I01. Choisir l'un ou l'autre.
- **Recette** : fond papier blanc cassé vignetté ; trait noir isométrique ; pavage par répétition ; typo serif espacée ; coupes franches entre les étapes. Remotion (SVG).
- **Exemple** : l'hexagone de Babel, puis son pavage infini, puis une étagère de 32 livres, puis « 410 pages ».
- **Va avec** : T06, I11 · **Évite avec** : I01 dans la même vidéo.
- **Fiche** : réf. 04 (5:31-6:30) · ●● · 🧪.

### I11 · Texture de texte plein cadre
- **Définition** : un mur de texte qui remplit l'image, pour rendre une quantité ou un concept palpable.
- **Fonction** : EXPLIQUER, RESSENTIR.
- **Quand l'utiliser** : pour figurer une immensité, du bruit, une répétition ou une obsession.
- **Éviter si** : le texte doit être lu. Ce n'est qu'une texture.
- **Recette** : texte répété ou aléatoire (`TexteBrouille`), faible profondeur de champ, page légèrement courbe, lent travelling ; un mot peut émerger (I15).
- **Exemple** : « 25x 25x 25x… » pour une exponentielle ; « sens sens senssens » pour le sens qui se perd.
- **Va avec** : H04, I12 · **Évite avec** : plus de 3 occurrences par vidéo.
- **Fiche** : réf. 04 · ● · 🧪 (avec ✅ `TexteBrouille`).

### I12 · Le « faux parfait »
- **Définition** : deux plans identiques, à un détail près, en coupe franche. Le spectateur attentif voit que tout a changé.
- **Fonction** : RÉVÉLER.
- **Quand l'utiliser** : pour illustrer qu'un détail suffit à rendre faux un tout (désinformation, mémoire, hallucination).
- **Éviter si** : il faut souligner le détail. Le procédé meurt si on l'explique.
- **Recette** : même cadrage, même lumière, un seul mot (ou objet) différent ; 4 à 6 s par plan ; ne jamais le commenter.
- **Exemple** : la biographie de Marie Curie, où « mourut » devient « naquit ».
- **Va avec** : I11, I14 · **Évite avec** : un commentaire en voix off.
- **Fiche** : réf. 04 (12:57) · ● · 📝.

### I13 · Mosaïque d'anonymat ou de révélation
- **Définition** : une image en gros pixels dont la résolution monte (révélation) ou reste basse (anonymat), par crans.
- **Fonction** : PROMETTRE, INCARNER.
- **Quand l'utiliser** : pour un humain « quelconque », un visage qu'on ne doit pas montrer, ou une image cachée (N03).
- **Éviter si** : l'image doit être lisible tout de suite.
- **Recette** : `Mosaique` (8 à 12 blocs au départ, 5 à 7 crans, accélération à la fin).
- **Exemple** : un électeur type entre deux groupes ; le graphique caché qui se dévoile.
- **Va avec** : N03, I02 · **Évite avec** : —.
- **Fiche** : réf. 03 · ● · ✅ `Mosaique`.

### I14 · Easter egg chiffré
- **Définition** : un message caché, lisible seulement si l'on met pause et qu'on le déchiffre, qui prolonge la thèse.
- **Fonction** : HABILLER (récompense de la communauté).
- **Quand l'utiliser** : une fois par vidéo au plus, quand le sujet touche à la curiosité, au secret, au code.
- **Éviter si** : le message est nécessaire à la compréhension.
- **Recette** : chiffre simple (César, inversion, première lettre de chaque ligne) ; affiché 3 à 5 s ; jamais résolu dans la vidéo ; on peut l'évoquer dans le commentaire épinglé.
- **Exemple** : « Phufl g'hwuh fxulhxa » se déchiffre en « Merci d'être curieux ».
- **Va avec** : I11 · **Évite avec** : une scène émotionnelle.
- **Fiche** : réf. 03 (14:38) · ● · 📝.

### I15 · Mot seul à l'écran
- **Définition** : un seul mot, ou une phrase très courte, centré sur un fond uni.
- **Fonction** : RÉVÉLER.
- **Quand l'utiliser** : pour graver le mot-clé de la thèse, 1 à 3 fois par vidéo.
- **Éviter si** : on l'emploie pour chaque idée. Il perd alors sa force.
- **Recette** : `TexteRevele` ou une apparition sèche ; petit corps ; 2 à 4 s ; fondu de sortie lent ; souvent précédé de S01.
- **Exemple** : « vraisemblable » ; « tout est déjà écrit ».
- **Va avec** : S01, H05 · **Évite avec** : I11 dans la même seconde.
- **Fiche** : réf. 04 · ● · ✅ `TexteRevele`.

### I16 · Une palette par lieu ou par chapitre
- **Définition** : chaque partie de la vidéo a sa dominante colorée. Le spectateur sait où il est sans titre.
- **Fonction** : RELIER.
- **Quand l'utiliser** : toute vidéo à chapitres ou à lieux (presque toutes).
- **Éviter si** : la vidéo est un seul huis clos. On garde alors une palette unique avec une évolution lente.
- **Recette** : définir 3 à 5 ambiances dans la grammaire ; les tenir en 3D comme en 2D ; vérifier au `barcode.png` de l'outil d'analyse sur notre rendu.
- **Exemple** : cyan pour la machine, or pour l'extérieur, bougie pour la galerie, marbre blanc pour le centre.
- **Va avec** : N04, T04 · **Évite avec** : un étalonnage uniforme qui écrase les différences.
- **Fiche** : réf. 04 · ●● · 📝 + mesure.

### I17 · Échelle « fourmi »
- **Définition** : un humain minuscule, ou une caméra au ras du sol, face à un objet ou un lieu monumental.
- **Fonction** : RESSENTIR, ACCROCHER.
- **Quand l'utiliser** : pour la révélation d'un lieu, d'un système ou d'une grandeur qui écrase.
- **Éviter si** : la scène est intime.
- **Recette** : contre-plongée, focale longue, brouillard (perspective atmosphérique), figure de 1 à 3 % de la hauteur de l'image ; mouvement très lent (M05).
- **Exemple** : la sphère géante au bout d'un lac ; « dans une minute, vous ferez la taille d'une fourmi ».
- **Va avec** : I08, M05, I18 · **Évite avec** : un montage rapide.
- **Fiche** : réf. 02, 04 · ●● · 🧪.

### I18 · Lumière unique et motivée
- **Définition** : chaque plan a une seule source de lumière identifiable, et le reste tombe au noir.
- **Fonction** : RESSENTIR.
- **Quand l'utiliser** : par défaut dans toute la 3D.
- **Éviter si** : la scène doit être neutre et informative (schéma sur papier).
- **Recette** : spot, oculus, bougies, éclairs ou soleil rasant ; volumétrique léger ; fonds sombres ; Blender (Cycles).
- **Exemple** : un spot conique sur le plateau ; un puits de lumière sur la tombe.
- **Va avec** : I07, I08, N07 · **Évite avec** : un éclairage plat de studio.
- **Fiche** : réf. 01, 02, 03, 04 · ●● · 📝 (Blender). Signature possible de la chaîne.

## M · Montage et rythme

### M01 · Alternance A/B rapide
- **Définition** : deux images alternent très vite (environ 0,3 s chacune) pendant quelques secondes.
- **Fonction** : ACCROCHER (faire voir sans montrer).
- **Quand l'utiliser** : pour un amorçage (N01), une hésitation ou une dualité.
- **Éviter si** : les images sont très contrastées en luminosité (flash désagréable, risque pour les personnes photosensibles).
- **Recette** : alternance toutes les 7 images à 24 i/s, pendant 3 à 5 s ; luminosités proches.
- **Exemple** : l'image en taches et la coccinelle colorée en alternance pendant que « les bleus regardent ».
- **Va avec** : N01 · **Évite avec** : M06 dans la même minute.
- **Fiche** : réf. 03 (0:42-1:03) · ● · 🧪.

### M02 · Couper sur le mot · STANDARD
- **Définition** : les coupes tombent sur les attaques de la voix.
- **Fonction** : STANDARD (toute la vidéo).
- **Recette** : au montage, placer chaque coupe sur une syllabe accentuée ; automatisable avec la transcription mot à mot. On contrôle avec l'outil d'analyse sur notre rendu (part des coupes sur une attaque).
- **Fiche** : réf. 03 (94 % contre 57 % au hasard) · ●● · 🧪 (outil).

### M03 · Deux régimes de montage
- **Définition** : de longs blocs explicatifs animés alternent avec des grappes d'images courtes sur les phrases émotionnelles.
- **Fonction** : EXPLIQUER, RESSENTIR.
- **Quand l'utiliser** : dans toute vidéo qui mêle explication et émotion.
- **Éviter si** : la vidéo est entièrement contemplative.
- **Recette** : blocs de 20 à 80 s (I03, I01), puis 3 à 6 images de 2 à 4 s (I04), puis retour au bloc.
- **Exemple** : un graphique de 84 s, puis 4 images sur « toute ma vie j'ai cru… ».
- **Va avec** : I03, I04 · **Évite avec** : —.
- **Fiche** : réf. 03 · 📝.

### M04 · Coupes métronomiques
- **Définition** : une série de plans de durée strictement identique, calée sur le tempo de la musique.
- **Fonction** : TRANSITIONNER (déplacement, progression).
- **Quand l'utiliser** : pendant un déplacement, une avancée vers un lieu, un décompte.
- **Éviter si** : la scène est émotionnelle ou explicative.
- **Recette** : durée d'un plan = un temps (ou deux) de la musique, par exemple 24 images à 60 BPM ; 6 à 15 plans.
- **Exemple** : 13 plans d'une seconde dans la pièce au début ; les grilles qu'on franchit.
- **Va avec** : T04, I09 · **Évite avec** : M05 juste après sans transition.
- **Fiche** : réf. 04 · ● · 🧪.

### M05 · Longue respiration sur une révélation de lieu
- **Définition** : 15 à 30 s sans voix, sur un mouvement de caméra lent, quand on découvre un lieu.
- **Fonction** : RESPIRER, RESSENTIR.
- **Quand l'utiliser** : à chaque entrée dans un lieu majeur (2 à 4 fois par vidéo).
- **Éviter si** : le plan n'est pas assez riche pour tenir 15 s.
- **Recette** : écrire la respiration dans le script (« [RESPIRATION 20 s] ») ; musique en avant (S03) ; caméra lente (travelling, grue).
- **Exemple** : 30 s sur la sphère avant le premier mot.
- **Va avec** : I08, I17, S03 · **Évite avec** : M04 juste avant sans transition.
- **Fiche** : réf. 02, 04 · ● (écriture), ●●● (plan) · 📝.

### M06 · Climax d'accélération, puis noir
- **Définition** : le rythme le plus rapide de toute la vidéo est gardé pour la fin, puis une coupe sèche au noir.
- **Fonction** : RÉVÉLER.
- **Quand l'utiliser** : au payoff final.
- **Éviter si** : la fin est intime et apaisée. On préfère alors S05 seul.
- **Recette** : plans de 1 s qui descendent à 0,2 s sur la montée musicale ; coupe au noir sur le dernier temps ; la musique décroît (S05).
- **Exemple** : la machine filmée sous tous les angles, de plus en plus vite.
- **Va avec** : M07, S05, N14 · **Évite avec** : une autre rafale ailleurs dans la vidéo, plus forte.
- **Fiche** : réf. 04 (24:20-25:16) · ●● · 🧪. Une fois par vidéo.

### M07 · Bouclage
- **Définition** : le dernier lieu est le premier, vu autrement. Le carton-titre peut revenir.
- **Fonction** : RELIER, RÉVÉLER.
- **Quand l'utiliser** : quand l'ouverture contient un plant (N05).
- **Éviter si** : le premier lieu n'a rien à « dire » de plus à la fin.
- **Recette** : même décor, même cadrage d'entrée, lumière ou sens changés ; reprise du titre.
- **Exemple** : la pièce du début ; la machine est maintenant comprise comme l'IA.
- **Va avec** : N05, M06 · **Évite avec** : —.
- **Fiche** : réf. 04 · ● · 📝. Une fois par vidéo.

## T · Transitions

### T01 · Carton terminal
- **Définition** : un écran noir avec une barre de chargement à à-coups et des messages système. Les messages annoncent la thèse en sous-texte.
- **Fonction** : TRANSITIONNER.
- **Quand l'utiliser** : une vidéo où une machine, un système ou une IA joue un rôle ; changement de lieu ou de chapitre.
- **Éviter si** : le sujet n'a aucune dimension « système ». L'effet paraît plaqué.
- **Recette** : `TerminalChargement` ; 2 à 4 s ; messages écrits comme des **plants** (lus vraiment au second visionnage) ; silence numérique possible (S06).
- **Exemple** : « [ATTENTION] RECHERCHE_1 ABANDONNÉE : AUCUN INDEX TROUVÉ. GÉNÉRATION_2 EN COURS ».
- **Va avec** : S06, H02 (registre machine) · **Évite avec** : T02 et T03 enchaînés.
- **Fiche** : réf. 04 · ● · ✅ `TerminalChargement`.

### T02 · Glitch avant un saut de monde
- **Définition** : l'image se décompose (pixels qui coulent, bandes décalées) avant de basculer dans un autre univers.
- **Fonction** : TRANSITIONNER.
- **Quand l'utiliser** : pour passer du réel à l'imaginaire ou du monde à la machine, une ou deux fois par vidéo.
- **Éviter si** : la vidéo n'a pas de « monde » technologique.
- **Recette** : datamosh FFmpeg (suppression des images clés entre deux plans) ou glitch Remotion (bandes décalées, séparation des couleurs) ; 1 à 2,5 s.
- **Exemple** : la machine qui se décompose avant le premier terminal.
- **Va avec** : T01 · **Évite avec** : un usage décoratif.
- **Fiche** : réf. 04 (1:57) · ●● · 🧪.

### T03 · Noir ponctuant
- **Définition** : 1 à 4 s d'écran noir.
- **Fonction** : RESPIRER, TRANSITIONNER.
- **Quand l'utiliser** : fin de chapitre, après une phrase forte.
- **Éviter si** : il y en a déjà un dans les 2 minutes précédentes.
- **Recette** : coupe franche au noir, souvent sur une queue de musique ou un silence ; jamais de fondu au noir mou.
- **Exemple** : 1,5 s de noir avant « toute ma vie, j'ai cru… ».
- **Va avec** : S05, S01 · **Évite avec** : T01 ou T02 collés.
- **Fiche** : réf. 01-04 · ● · 📝.

### T04 · Seuil physique
- **Définition** : on passe une porte, une arche, une grille : un changement de chapitre matérialisé.
- **Fonction** : TRANSITIONNER, RELIER.
- **Quand l'utiliser** : dans toute vidéo à lieu-concept (N04).
- **Éviter si** : il n'y a pas d'espace en 3D ou en plans générés.
- **Recette** : travelling avant à travers l'ouverture ; la lumière et la palette changent de l'autre côté (I16) ; le son aussi (S04).
- **Exemple** : la caméra franchit l'entrée sombre de la sphère et arrive dans le hall doré.
- **Va avec** : N04, I16, S04 · **Évite avec** : T01 pour la même transition.
- **Fiche** : réf. 02, 04 · ●● · 📝 (Blender, Higgsfield).

### T05 · Retour d'objet-symbole
- **Définition** : l'objet-concept revient entre les chapitres, avec un autre cadrage et une autre lumière.
- **Fonction** : RELIER.
- **Quand l'utiliser** : quand la vidéo a un N07.
- **Éviter si** : l'objet n'a pas évolué. Chaque retour doit montrer quelque chose de neuf.
- **Recette** : 3 à 5 retours, de plus en plus proches et lumineux jusqu'à la révélation finale.
- **Exemple** : le cube minuscule dans le noir, puis plein cadre, puis la face cachée.
- **Va avec** : N07 · **Évite avec** : —.
- **Fiche** : réf. 03, 04 · ● · 📝.

### T06 · Papier ↔ monde
- **Définition** : une coupe franche entre un schéma sur fond papier clair et une scène 3D sombre.
- **Fonction** : TRANSITIONNER.
- **Quand l'utiliser** : pour revenir de l'explication au vécu, ou l'inverse.
- **Éviter si** : le fond explicatif est sombre (I01). Le contraste disparaît.
- **Recette** : coupe franche, contraste de luminosité maximal, souvent sur un son marqué.
- **Exemple** : le pavage d'hexagones sur papier, puis l'escalier en 3D.
- **Va avec** : I10 · **Évite avec** : I01.
- **Fiche** : réf. 04 · ● · 📝.

## H · Habillage et typographie

### H01 · Source en bas à gauche
- **Définition** : la mention de l'origine d'une image (œuvre, archive, étude) en petit, en bas à gauche.
- **Fonction** : HABILLER.
- **Recette** : sans-serif grasse, blanc à 70 %, corps 24-26 (en 1080p), marge 20 px ; intégrée à `FiltreArchive`.
- **Éviter si** : l'image est à nous.
- **Fiche** : réf. 03 · ● · ✅.

### H02 · Un registre typographique par voix
- **Définition** : chaque « voix » de la vidéo (l'humain, la machine, la preuve, le concept) a sa famille de police.
- **Fonction** : HABILLER.
- **Quand l'utiliser** : à fixer dans la grammaire de chaque vidéo ; 2 ou 3 registres au maximum.
- **Recette** : par exemple serif = narration et livres, monospace = machine et système, sans grasse = concepts. Ne jamais mélanger les rôles.
- **Exemple** : serif pour « LA BIBLIOTHÈQUE DE BABEL », monospace pour les terminaux.
- **Va avec** : T01, H05 · **Évite avec** : plus de 3 familles.
- **Fiche** : réf. 03, 04 · ● · 📝 (DA).

### H03 · Sponsor balisé
- **Définition** : le segment sponsorisé est signalé de façon transparente : mention légale, barre de durée et QR code.
- **Fonction** : HABILLER.
- **Recette** : « COLLABORATION COMMERCIALE » en haut à gauche, une barre qui avance sur la durée du segment, un QR code en haut à droite ; dans les couleurs de la vidéo.
- **Fiche** : réf. 04 · ● · 🧪 (composant à faire).

### H04 · Texte qui émerge du bruit
- **Définition** : les lettres défilent au hasard puis se fixent une à une pour former le texte (ou l'inverse).
- **Fonction** : EXPLIQUER, RÉVÉLER.
- **Quand l'utiliser** : quand le sujet touche au hasard, au code, à l'information, au sens.
- **Éviter si** : on l'utilise pour tous les titres. Il faut le réserver au registre « machine » ou « hasard ».
- **Recette** : `TexteBrouille` (vitesse 1 à 3 images par caractère, recherche de 8 à 14 images, alphabet adapté au sujet).
- **Exemple** : « support technique français » qui sort de lettres aléatoires ; une adresse de Babel.
- **Va avec** : I11, T01 · **Évite avec** : le registre « humain » (H02).
- **Fiche** : réf. 04 · ● · ✅ `TexteBrouille`.

### H05 · Mot accentué en couleur
- **Définition** : dans une phrase en blanc, un ou deux mots sont dans la couleur d'accent.
- **Fonction** : HABILLER, EXPLIQUER.
- **Recette** : 1 ou 2 mots maximum ; ceux qui portent l'opposition ou la thèse.
- **Exemple** : « Tout est **explicable** mais pas **justifiable** ».
- **Va avec** : I02, I15 · **Évite avec** : plus de 2 mots colorés.
- **Fiche** : réf. 03 · ● · 🧪 (composant simple à faire).

### H06 · Carton d'authenticité
- **Définition** : 2 à 4 s en ouverture pour dire au public comment la vidéo a été faite.
- **Fonction** : ACCROCHER (contrat de confiance).
- **Quand l'utiliser** : quand la méthode de fabrication compte pour le sujet (vidéo sur l'IA, sur les images, sur la manipulation).
- **Recette** : une phrase vraie et précise. Si on utilise des outils génératifs, on dit **ce qu'on a fait avec**, on ne le cache pas.
- **Fiche** : réf. 04 (« 100 % fait sur Blender ») · ● · 📝. Une fois par vidéo.

## S · Son

### S01 · Silence d'une seconde avant la phrase-clé
- **Définition** : voix et musique coupées pendant 0,6 à 1,2 s, juste avant la phrase la plus importante.
- **Fonction** : RÉVÉLER.
- **Quand l'utiliser** : 2 à 4 fois par vidéo, sur les phrases qu'on veut graver.
- **Éviter si** : plus de 4 fois. Le procédé devient alors prévisible.
- **Recette** : écrire « [SILENCE] » dans le script ; au mixage, couper vraiment (pas seulement baisser) ; reprendre sur la phrase, souvent avec I15.
- **Exemple** : silence de 1,2 s, puis « c'est pour ça que les deux courbes s'éloignent ».
- **Va avec** : I15, N14 · **Évite avec** : T03 au même endroit (doublon).
- **Fiche** : réf. 03 (9:51, 16:01), 04 · ● · 📝.

### S02 · Lit musical sous la voix · STANDARD
- **Définition** : une musique continue sous la voix, qui s'efface quand la voix parle et remonte dans les respirations.
- **Fonction** : STANDARD.
- **Recette** : musique vers −30 dBFS sous la voix ; ducking de 6 à 8 dB ; remontée dans les respirations ; à régler avec `docs/specs-techniques.md`.
- **Fiche** : réf. 03 · ● · 📝 (mixage).

### S03 · Musique par chapitre
- **Définition** : chaque lieu ou chapitre a son thème musical.
- **Fonction** : RESSENTIR, RELIER.
- **Quand l'utiliser** : avec I16 et N04.
- **Recette** : un thème par lieu (tempo et texture cohérents avec la palette) ; les changements se font sur les noirs (T03) ou les seuils (T04). Source : composition, bibliothèque libre de droits, ou génération (à évaluer).
- **Fiche** : réf. 04 (tempo de 60 à 187 BPM) · ●●● · 📝.

### S04 · Grappe sonore de changement de monde
- **Définition** : plusieurs sons rapprochés (vent, porte, réverbération qui change, oiseaux) font « sortir » ou « entrer » physiquement le spectateur.
- **Fonction** : RESSENTIR, TRANSITIONNER.
- **Recette** : 4 à 6 événements en moins de 10 s au franchissement d'un seuil (T04) ; changement de réverbération ; effets sonores Freesound ou générés.
- **Exemple** : la sortie à l'air libre au coucher du soleil.
- **Va avec** : T04, N15 · **Évite avec** : une voix continue par-dessus.
- **Fiche** : réf. 04 (23:24) · ●● · 🧪.

### S05 · Fin musicale, puis silence
- **Définition** : après la dernière phrase, 25 à 35 s de musique seule qui s'éteint, parfois suivies de silence.
- **Fonction** : RESPIRER.
- **Recette** : pas de voix après N14 ; la musique décroît naturellement ; générique sobre ou noir.
- **Va avec** : N14, M06 · **Évite avec** : un appel à s'abonner qui casse le moment.
- **Fiche** : réf. 03 (35 s), 04 (27 s + 17 s de silence) · ● · 📝.

### S06 · Silence « numérique » sur un message machine
- **Définition** : une coupure franche du son pendant un message système inquiétant.
- **Fonction** : RÉVÉLER.
- **Recette** : 0,5 à 1 s de silence total sur un carton T01 [ERREUR].
- **Va avec** : T01 · **Évite avec** : S01 dans la même minute.
- **Fiche** : réf. 04 (4:34) · ● · 📝.

### S07 · Dynamique maîtrisée · STANDARD
- **Définition** : un son ni écrasé ni saturé.
- **Fonction** : STANDARD.
- **Recette** : −14 LUFS intégré, plage dynamique (LRA) de 5 à 8 LU, crête ≤ −1 dBTP ; vérifié avec l'outil d'analyse sur notre rendu.
- **Contre-exemples** : réf. 03 (LRA 2,9, trop compressé), réf. 04 (crête à +0,7 dBTP).
- **Fiche** : ● · 📝 + mesure.

---

# Couche 2 · disponibles, pas proposés d'office

À proposer seulement si une scène en a précisément besoin et qu'aucun procédé de couche 1 ne fait mieux.

### N06 · Refrain retourné
- **Définition** : une phrase-marteau répétée 3 à 5 fois, dont la dernière occurrence change de sens.
- **Fonction** : RELIER, RÉVÉLER.
- **Proposer seulement si** : la thèse tient en une formule courte et retournable, et que N05 ne suffit pas.
- **Recette** : occurrences espacées ; la dernière complétée ou inversée (« Tout est déjà écrit. C'est à nous de le dire »).
- **Fiche** : réf. 04 · ● · 📝.

### N08 · Pictogramme-personnage
- **Définition** : deux pictos opposés incarnent une métaphore et reviennent tout au long de la vidéo sans réexplication.
- **Fonction** : EXPLIQUER, RELIER.
- **Proposer seulement si** : une opposition (deux attitudes, deux camps) structure toute la vidéo et que la DA est en 2D.
- **Recette** : 2 pictos, mêmes couleurs à chaque retour, un attribut qui change selon la situation (une flèche « preuves → conclusion » dans un sens ou dans l'autre).
- **Fiche** : réf. 03 · ● · 🧪.

### N12 · Confession du narrateur
- **Définition** : avant la fin, le narrateur s'applique la thèse et change d'avis devant nous.
- **Fonction** : INCARNER, RÉVÉLER.
- **Proposer seulement si** : la thèse touche une croyance que le narrateur partageait vraiment. Jamais une confession inventée.
- **Recette** : 2 ou 3 phrases simples, sans pathos, juste avant N14.
- **Fiche** : réf. 02, 03 · ● · 📝.

---

# Écartés

Ne pas les reproposer, même si une nouvelle référence les utilise.

| ID | Procédé | Écarté le | Par |
|---|---|---|---|
| N13 | Sponsor tissé dans la métaphore (mot-pivot entre le récit et la marque) | 05/11/2026 | Bruno |
