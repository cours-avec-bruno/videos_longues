# La partie

Parties jouées le 06/11/2026 avec le **1in8b Engine** (l'API officielle de 1 sur 8 milliards). C'est **la matière de la vidéo**.

Légende : **[MOTEUR]** = donné par le moteur (récit, chiffres, citations) · **[CALCUL]** = calculé par nous à partir des sorties du moteur · **[IDÉE]** = proposition de mise en scène · **[À COMPLÉTER]** = attend le script `shared/outils/1in8b/partie.py`.

## Ce qu'on entend par « la vie la plus probable » (décision de Bruno, 06/11/2026)

| Niveau | Règle | Comment |
|---|---|---|
| **La naissance** | Les conditions les plus probables | Pays : **l'Inde** (17,6 % des naissances, 1 sur 6) **[MOTEUR, page du site]**. Lieu : **la campagne** (68 % des bébés indiens simulés, 41 sur 60) **[MOTEUR]**. Sexe : **garçon** (en Inde, il naît environ 107 à 110 garçons pour 100 filles ; **[À VÉRIFIER]**, ONU WPP 2024). Cinquième de revenus : chacun fait 20 % par définition, donc aucun n'est « le plus probable » ; on prend **celui du milieu** (le 3e). Religion et caste : **les plus fréquentes, mesurées par le moteur** (script, option `--mesurer faith,caste`) |
| **Les décisions** | L'option que prend la majorité dans la même situation | **Décidée par nous, pas à pas** : à chaque décision, l'option la plus fréquente parmi 200 vies nées dans les mêmes conditions. La politique `auto` du moteur ne convient pas, parce qu'elle tire au sort selon les parts (voir plus bas) |
| **Les événements** | Impossible à choisir | Les maladies, les rencontres et la mort sont tirées au sort par le moteur. On situe chacun d'eux par rapport aux médianes de vies simulées |

**[CALCUL]** Inde × campagne × garçon × 3e cinquième ≈ 17,6 % × 68 % × 52 % × 20 % ≈ **1,2 % des naissances**, soit environ 1 sur 80. C'est peu, mais aucune autre combinaison n'est plus fréquente. C'est le paradoxe à dire dans la vidéo : même la vie la plus probable est rare.

## Comment la vie définitive a été jouée

1. **Les conditions de naissance les plus fréquentes, mesurées par le moteur** (`0-mesures-naissance.json`, 60 bébés indiens simulés, garçons, campagne, 3e cinquième) **[MOTEUR]** :
   - religion **hindoue** pour 47 sur 60 (devant musulmane 8, chrétienne 2, aucune 2, autre 1) ;
   - caste **OBC, les « autres classes défavorisées »**, pour 28 sur 60 (devant la catégorie générale 16, les castes répertoriées, ou dalits, 11, et sans catégorie 5).
2. **Découverte qui change la méthode** : la politique `auto` du moteur ne prend **pas** toujours l'option majoritaire. Elle **tire au sort selon les parts réelles**. Par exemple, au carrefour après le lycée, 71 % des vies tentent l'université et 25 % prennent un emploi (`6-parts-decisions.json`). Yash, la version provisoire, avait pris l'emploi : l'option minoritaire. Bruno avait raison de le soupçonner, et « ce que la plupart des gens choisissent » n'était pas « toujours le plus probable ».
3. **On a donc décidé nous-mêmes, pas à pas** (`/live`, script `shared/outils/1in8b/jouer_plus_probable.py`) :
   - à chaque décision, on prend **l'option la plus fréquente**, estimée sur **200 vies nées dans les mêmes conditions** ;
   - on la mesure, quand c'est possible, sur les rencontres où **exactement les mêmes options** étaient proposées ;
   - sur 37 décisions, toutes ont pu être estimées.
4. **Ce que valent ces pourcentages** : ce sont des **parts observées sur des vies simulées** (un échantillon), et non des probabilités publiées par le moteur, qui n'en publie aucune. Ils serviront pour les encarts « À VOUS », avec la mention « part des vies simulées nées dans les mêmes conditions ».
   - Quelques décisions sont des **quasi-égalités** : 7 ans (34 % contre 33 %), 12 ans (51 % contre 49 %), 16 ans (51 % contre 49 %), 40 ans (44 % contre 43 %), 57 et 73 ans (38 % contre 37 %). Avec ces échantillons, ce sont des égalités statistiques. On a pris la plus haute observée et on le dira.
   - Deux décisions reposent sur très peu de cas : 25 ans (l'étranger, 7 cas) et 61 ans (l'argent de poche des petits-enfants, 5 cas).

Les étapes intermédiaires sont gardées dans l'archive : Khadija (tirée au sort), Yash (naissance la plus probable, caste tirée par le moteur), et `1-vie-auto.json` (même naissance que la vie définitive, mais choix laissés à la politique `auto`, qui tire au sort).

## La vie définitive : Manoj Mohanty

`7-vie-la-plus-probable.json` · seed 20261106 · moteur 0.9.52 · **[MOTEUR]** sauf mention.

**Né en 2026 dans un village indien**, garçon, hindou, OBC, 3e cinquième. Il est le petit dernier, après deux grandes sœurs et deux grands frères. Mort à **75 ans**, d'une pneumonie, en Inde. Pour comparer : l'âge médian au décès des hommes indiens simulés est de 72 ans.

| Âge | Ce qui arrive | Décision : l'option la plus fréquente (part estimée) |
|---|---|---|
| 0-4 | Les vaccins ; le premier mot, « Maman » ; l'eau qu'on va chercher toujours plus loin les mois sans pluie ; la cuisine au feu de bois, la fumée qui pique les yeux | 2 ans : courir partout devant le visiteur (30 %, contre 25, 23 et 22 %) |
| 5 | Ses parents l'inscrivent dans une école privée, « les frais étaient loin d'être négligeables » | Une pause : le garder pour soi (100 %) |
| 6-10 | L'école ; le bidon d'eau avant l'aube ; la case « caste : OBC » sur le dossier ; **à 8 ans, il veut être « ingénieur »** ; à 9 ans, les coups de baguette (« vous n'avez plus levé la main en classe »), et la famille s'endette ; à 10 ans, la viande seulement aux fêtes | 7 ans : les rencontres religieuses (34 %, quasi-égalité avec la danse et le cricket) |
| **11** | **Il finit le primaire. Décision : continuer à étudier. Puis : « Votre famille n'a pas pu payer les frais de scolarité ; vous avez dû renoncer à poursuivre vos études. » Il passe ses journées à s'occuper des bêtes.** | **Continuer à étudier : 97 %** (contre 3 % pour travailler) |
| 12-14 | Les champs, l'eau. Un cyclone. **« Vous enviiez vos amis qui allaient à l'école. »** | 12 ans : faire le premier pas vers une amitié (51 %) |
| **15** | **Premier emploi : pêcheur.** | Pêcheur 33 %, éleveur 32 %, paysan 30 %, attendre 5 % |
| 16-23 | Le premier salaire, un cadeau à sa mère, « seulement un long regard silencieux ». La nuit en mer, bredouille. Preeti, une grande amitié à 17 ans. À 21 ans, il confie à une sœur « ce que vous n'aviez pu dire à personne » | 16 ans : emmener à l'hôpital quelqu'un qui s'effondre (51 %) |
| 24 | Une toux qui ne s'arrête pas : **la tuberculose**, guérie, mais endetté | Se faire soigner à l'hôpital (70 %) |
| 25 | Une occasion de partir aux États-Unis | Rester (71 %, sur 7 cas seulement) |
| **26** | **Il épouse Preeti.** La famille de la mariée verse une dot. Ils vivent chez ses parents | Se marier (61 %, contre 29 % pour prendre le temps et 10 % pour refuser) |
| 27 | Le théâtre devient sa passion | Théâtre (28 %, quasi-égalité) |
| 28, 31 | Pradeep naît, puis **Usha** (le prénom de son amie d'enfance) | Avoir un enfant (74 %), deux fois |
| 29 | Preeti s'arrête de travailler pour s'occuper du bébé. **Son deuxième frère meurt de la tuberculose, à 32 ans** | Confier le bébé à sa partenaire (66 %) |
| 30 | Avec Preeti, il construit une maison sur la terre de la famille | — |
| 33 | La mort de son père (maladie diarrhéique) | L'école publique pour Pradeep (61 %) |
| 35 | La dengue : « votre corps n'est plus ce qu'il était » | L'hôpital (70 %) |
| 37 | **Son frère aîné meurt de la tuberculose, à 49 ans** | Dire oui à Pradeep, qui veut apprendre un instrument (59 %) |
| 39-41 | Usha, la typhoïde, guérie. **Une liaison** : « Les mensonges se sont accumulés », puis « Preeti a tout découvert ». Il demande pardon, et elle lui fait confiance « une fois encore » | 39 ans : le grand hôpital, quitte à emprunter (75 %) · 40 ans : demander de l'aide à la famille pour la dette (44 %, contre 43 % pour l'usurier) · 41 ans : se reparler à cœur ouvert (92 %, sur 12 cas) |
| 46-49 | L'alcool, qu'il réduit, puis qui revient, puis qu'il réduit encore. Une moto à crédit. Sa mère vit avec lui | 46 ans : boire moins (58 %) · 48 ans : la moto à crédit (52 %) · 49 ans : s'occuper lui-même de sa mère (41 %) |
| 50 | La mort de sa mère (septicémie) | Le football (28 %) |
| 52-58 | Les mariages de Pradeep et d'Usha, et la dot qu'il verse à son tour. Six petits-enfants. **À 53 ans, au théâtre, le premier rôle, « les applaudissements n'en finissaient plus »**. À 57 ans, il saute des repas, avec 18 300 € de dette | Donner un peu, selon ses moyens (42 %), deux fois · 57 ans : l'aide de la famille (38 %) |
| 60 | — | Continuer à travailler (55 %) |
| 65 | Pradeep devient responsable de l'hébergement dans un hôtel | — |
| 66-73 | Les 40 ans de mariage, une lettre de Preeti. La jeune recrue qu'il a écoutée l'invite à son mariage, « c'était grâce à vous ». L'hypertension. La dette : encore 9 682 € à 73 ans | Écouter la recrue (57 %) · suivre le traitement (51 %) · l'aide de la famille (38 %) |
| 74 | **Son petit-fils entre à l'université.** | — |
| **75** | Usha achète un logement. Puis : « À 75 ans, votre vie a pris fin (pneumonie ou autre infection respiratoire basse). » | — |

**Bilan [MOTEUR]** :
- l'école primaire seulement ;
- pêcheur toute sa vie ;
- marié à Preeti pendant 49 ans ;
- 2 enfants et 6 petits-enfants ;
- une dette jamais soldée ;
- deux frères emportés par la tuberculose ;
- un patrimoine d'environ 8 600 € (en parité de pouvoir d'achat) à sa mort.

### Pourquoi c'est la vie idéale pour la vidéo

- **11 ans, c'est le cœur de la thèse.** L'option la plus probable, choisie par 97 % des vies, était de continuer l'école. Il la choisit, et le monde lui dit non : la famille ne peut pas payer. C'est la phrase du site, *« les choix changent les probabilités mais ne décident jamais du résultat »*, rendue visible. **C'est le grand « À VOUS » de la vidéo** : le spectateur choisit l'école, l'opérateur aussi, et c'est raté quand même.
- **Le rêve d'enfant** : « ingénieur » à 8 ans, pêcheur à 15 ans. À reprendre dans l'aveu.
- **Une vie ordinaire et pleine** : la mer, Preeti, le théâtre, les enfants, la faute pardonnée, les applaudissements à 53 ans. Elle n'est ni misérable ni enviable, et c'est exactement le registre du « plus probable ».
- **Un écho entre générations** : lui quitte l'école à 11 ans, et **son petit-fils entre à l'université** l'année avant sa mort ; sa fille achète un logement. La pente sociale existe aussi vers le haut, lentement, sur trois générations. C'est la nuance anti-fatalisme (N11), trouvée dans la vie elle-même.
- **La tuberculose** : elle le touche et tue deux de ses frères. Le moteur la rend banale, et c'est un vrai sujet (l'Inde est le pays qui compte le plus de cas au monde, **[À VÉRIFIER]**, OMS).

### La variante « pour réussir » (même naissance, même seed, politique `ambitious`)

`1-vie-auto.json` (choix tirés au sort selon les parts) et `2-vie-ambitieuse.json` (choix ambitieux) : **[MOTEUR]**

| | Choix tirés au sort (`auto`) | Choix ambitieux |
|---|---|---|
| Études | lycée | **master ou doctorat** |
| Travail | éleveur, électricien, mécanicien | **professeur** |
| Rang de revenu dans le pays, à 40 ans | 78e centile | **97e centile** |
| Enfants | 2 | 4 |
| Mort | 80 ans, AVC | **89 ans**, AVC |

⚠️ **L'hypothèse qu'on voulait tester est infirmée.** Dans le moteur, des choix ambitieux, dès l'enfance, **changent beaucoup** la vie. L'aveu (S13) ne doit donc **pas** dire « vos choix n'auraient rien changé ». Proposition :
- **ce qu'on peut dire honnêtement** : « Les choix comptent. Mais à chaque carrefour, la plupart des gens prennent le même chemin, celui que leur point de départ rend le plus probable. Le déterminisme, ce n'est pas une interdiction. C'est une pente. » Et le cas des 11 ans montre l'autre face : même le bon choix peut être refusé par le monde ;
- **ce qu'il faut vérifier avant de montrer la variante** : la vie ambitieuse vient d'un autre chemin aléatoire (ses événements divergent après le premier choix différent). Pour la montrer à l'écran, il faudrait comparer sur beaucoup de vies (`/simulate` en politique `ambitious` contre `auto`), et non sur une seule. **[À FAIRE]**

## Partie 1 · Khadija Ibrahim (la vie tirée au sort, pour comparaison)

### Fiche technique

| | |
|---|---|
| Seed | **20261106** (la date du jour, choisie avant le tirage ; **un seul tirage**, pas de sélection) |
| Moteur | 1in8b Engine **0.9.52** (bêta), API v1, offre gratuite |
| Monde | Aujourd'hui (né en 2026), lieu tiré au sort selon les naissances |
| Règle des choix | **Politique `auto`** du moteur : « *what most people choose* » (ce que la plupart des gens choisissent), le défaut. **[MOTEUR, doc officielle]** C'est exactement notre règle secrète, appliquée par le moteur lui-même |
| Unités consommées | 95 sur 2 000 ce mois-ci (1 vie, 4 bébés, 3 comparaisons) |
| Crédit obligatoire | « 1in8b Engine (1in8b.life) » ; vies simulées, pas des personnes réelles |
| Reproduire | Même seed + même version du moteur = même vie. **Si le moteur change de version, la vie peut changer** : d'où l'archive JSON (`../prompts/partie/`) |

### Qui est-elle

**Khadija Ibrahim**, née en **2026 en Algérie, à la campagne**, fille. **[MOTEUR]**

- **Famille** : sa mère a 38 ans et son père 44 ans ; le père est présent ; elle a 2 grands frères. Musulmane.
- **Les moyens** : sa famille appartient au **premier cinquième de revenus, c'est-à-dire les 20 % les plus pauvres du pays**.
- **Sa vie** :
  - école primaire seulement ;
  - mariée à 24 ans à Amr ;
  - 3 enfants, dont un mort avant un an ;
  - jamais d'emploi déclaré à l'âge adulte.
- **Sa mort** : à **94 ans**, des complications d'une fracture après une chute, en Algérie.

Ce qu'aucun choix n'a décidé : le pays (l'Algérie représente environ 0,7 % des naissances mondiales, **[À VÉRIFIER]** sur la page statistiques du site), le sexe, la campagne, le cinquième le plus pauvre, l'âge des parents.

## La vie, étape par étape

Chaque **décision** est celle que la politique `auto` a prise. **[MOTEUR]** Les autres options proposées et leurs probabilités viendront du script **[À COMPLÉTER]**.

### 0 à 10 ans · l'enfance

**[MOTEUR]**
- 0 an : les vaccins de base.
- 1 an : une pneumonie (« vous aviez du mal à respirer »), puis les premiers pas.
- 2 ans : le premier mot (« Maman »).
- 4 ans : l'école maternelle. On dit d'elle qu'elle est « une enfant affectueuse » : elle tend son jouet à l'enfant qui pleure, et s'assoit près d'un parent malade pour lui « tâter le front ».
- **6 ans : quand on lui demande ce qu'elle veut faire plus tard, elle répond toujours : « youtubeuse ».**
- 6 ans, encore : l'instituteur la gifle devant la classe pour des devoirs non faits.
- 7 ans : l'école coranique chaque matin. Décision : les rencontres religieuses, qui deviendront « sa passion » toute sa vie.
- 8 ans : après l'école, elle aide aux champs.
- 9 ans : grâce à un bon professeur, elle prend goût aux mathématiques.
- 10 ans : des notes moyennes. Les vêtements neufs n'arrivent qu'une fois par an. Son premier smartphone.

> **[IDÉE]** « Youtubeuse » est un cadeau pour une vidéo YouTube : une petite fille, à la campagne en Algérie, qui rêve de faire exactement ce que fait la personne qui regarde. On le garde pour S07, sans appuyer. Et on le reprend à l'aveu (S13) : « À six ans, elle voulait faire des vidéos. Elle n'en a jamais fait. »

### 11 ans · la décision qui décide de tout

**[MOTEUR]**
- Elle termine l'école primaire.
- **Décision : « Commencer à travailler pour aider votre famille ».** Elle quitte l'école.
- Le moteur cite : *« Dans le monde, environ 160 millions d'enfants sont astreints au travail (OIT et UNICEF 2020) »*.
- La même année, le travail des parents se stabilise et la famille vit « bien plus à l'aise ». Trop tard pour l'école.

**Contexte [MOTEUR, simulation de 30 Algériennes du cinquième le plus pauvre] :**
- **à 15 ans, 43 % n'ont que le primaire**, contre 7 % des filles du cinquième le plus riche ;
- **à 40 ans, 26 % ont fait des études supérieures**, contre 52 % du cinquième le plus riche (petits échantillons : ordres de grandeur seulement).

> **[IDÉE]** C'est **le grand « À VOUS » de la vidéo** (S08 : on passe de « 15 ans » à **11 ans**). Le spectateur, qui veut « réussir », choisira presque sûrement « continuer l'école ». L'opérateur clique « travailler ». C'est le moment où l'hésitation de sa main est l'indice le plus fort.

### 12 à 23 ans · la jeunesse

**[MOTEUR]**
- 12 à 14 ans : elle porte des charges au marché, s'occupe des bêtes, aide aux champs.
- 14 ans : la mort de sa grand-mère.
- 15 ans : la mort de son grand-père. **Décision : aider aux tâches ménagères.**
- **16 ans : décision « Partir à Alger ».** Elle déménage. Puis : « Attendre un meilleur emploi ».
- 17 ans :
  - elle cherche du travail, « ce n'était pas facile » ; aide aux tâches ménagères ;
  - **une récession mondiale** (le moteur cite le FMI, Laeven et Valencia 2018) ;
  - elle participe à la reconstruction d'une région frappée par une catastrophe.
- 18 ans : pendant des années, elle saute souvent des repas ; le moteur cite la FAO (733 millions de personnes souffrant de la faim en 2023).
- 19 et 22 ans : **décision « Refinancer vos emprunts »**, deux fois. À 20 ans, elle ne dort plus à cause d'une dette de 6 010 € (aux prix français). Sa famille en éponge une partie.
- 23 ans : la mort de son père, à 68 ans (cancer du poumon).

### 24 à 49 ans · la vie adulte

**[MOTEUR]**
- **24 ans : décision « Se marier »** avec Amr. **Décision : « Essayer l'école du soir »**. Elle échoue à l'examen d'équivalence de fin de collège : « Vous pourrez le repasser l'an prochain. » Elle ne le repassera pas.
- **25 ans : décisions « Chercher du travail », puis « Se consacrer au foyer et aux enfants ».** À partir de là, ce sont les revenus d'Amr qui font vivre le foyer.
- **27 ans : décision « Accueillir un chat » : Luna.** Les premiers jours, elle se cache sous le canapé, puis un soir elle grimpe sur ses genoux.
- 29 ans : une crise de change ; la naissance de **Khaled**.
- **31 ans : « Il y a encore eu des violences à la maison. Vous n'avez pu en parler à personne. »** La même phrase revient à 36, 41, 42, 44, 47 et 50 ans.
- **33 ans :**
  - la naissance de **Hussein**, qui meurt avant son premier anniversaire (le moteur cite UN IGME : 22 décès pour 1 000 naissances avant 5 ans en Algérie) ;
  - **décision « Proposer de se lancer ensemble »** : la boutique d'Amr ouvre, pour 7 773 €. Elle ferme en moins de deux ans.
- 34 ans : Luna, chaque nuit, ronronne sur sa poitrine pendant cette « année difficile ».
- 35 ans : une crise financière ; la naissance de **Tarek**.
- **37 ans : décision « L'accueillir chez vous »** : sa mère vient vivre chez eux. Elle meurt à 83 ans, quand Khadija en a 44 (« Vous auriez voulu lui dire merci, à l'époque »).
- 42 ans : Luna meurt, à 15 ans.
- 43 ans : Tarek a du mal à lire ; chaque soir, elle lit avec lui, ligne par ligne.
- 44 ans : sans lunettes, elle lit les petits caractères en plein soleil, à bout de bras (le moteur cite l'OMS).
- **46 ans : décision « Essayer de tenir le coup par vous-même »** (« votre cœur restait lourd »). À 47 ans, « cette période pesante était passée ». Le moteur cite l'OMS : un tiers seulement des personnes dépressives sont soignées, même dans les pays riches.
- 49 ans : **décision « S'asseoir et écouter »** Tarek.

### 50 à 79 ans · le second souffle

**[MOTEUR]**
- 50 ans : Amr perd son emploi, et le foyer n'a plus de revenu. Avec sa première paie, Khaled lui offre un cadeau.
- 51 ans : Tarek est pris à voler dans un magasin ; elle l'emmène s'excuser chez le commerçant.
- 55 ans : Tarek devient militaire de carrière ; Khaled est vendeur de rue.
- **58 ans : décision « Participer généreusement aux frais du mariage »** de Khaled. Son premier petit-enfant naît.
- 65 ans : elle a « l'esprit clair et le cœur serein » ; elle fait du bénévolat à la soupe populaire. Amr prend sa retraite.
- 66 ans : **pour la première fois, des économies** : 16 300 € (aux prix français).
- **68 ans : décision « Se faire soigner à l'hôpital »** : une fracture, guérie.
- 70 ans : **la première télévision et le premier réfrigérateur à la maison.**
- 73 ans : son premier ordinateur.
- 74 et 75 ans : angine de poitrine, puis hypertension, « traitement pris avec régularité ».
- **77 ans : décision « Donner une partie, selon vos moyens »**.

### 80 à 94 ans · la fin

**[MOTEUR]**
- **80 ans : décision « Partir en pèlerinage »** : La Mecque. On l'appelle désormais « Hajja ». C'est la plus grosse dépense de sa vie (11 400 €).
- 85 ans : elle assiste au mariage de sa petite-fille. 86 ans : son premier arrière-petit-enfant, quatre générations réunies.
- 90 ans : un AVC, pris en charge à temps : elle réapprend à marcher et à parler.
- 91 ans : la mort d'Amr, à 96 ans.
- 94 ans : « Votre mémoire n'est plus ce qu'elle était. » Puis « À 94 ans, vous avez perdu la vie (complications d'une fracture). »

**Bilan [MOTEUR]** :
- 3 enfants, dont 2 vivants ;
- 6 petits-enfants et 5 arrière-petits-enfants ;
- le dernier emploi déclaré à 14 ans ;
- elle n'a jamais quitté l'Algérie.

## Les décisions de la vie de Khadija

| Âge | Décision retenue (politique `auto`) **[MOTEUR]** | Autres options et probabilités | Pour la vidéo |
|---|---|---|---|
| 2 | Courir dans la maison, le jouet à la main | [À COMPLÉTER] | — |
| 7 | Rencontres religieuses (passion) | [À COMPLÉTER] | Possible « À VOUS » de S07 (léger, pour apprendre le jeu) |
| 8 | Grignoter avec ses amis | [À COMPLÉTER] | — |
| **11** | **Commencer à travailler pour aider la famille** | [À COMPLÉTER] | **« À VOUS » n° 1 (S08)**, le pivot |
| 15, 17 | Aider aux tâches ménagères | [À COMPLÉTER] | — |
| **16** | **Partir à Alger** · attendre un meilleur emploi | [À COMPLÉTER] | « À VOUS » n° 2 (S09) |
| 19, 22, 34 | Refinancer ses emprunts | [À COMPLÉTER] | Une ligne, pour la dette |
| **24** | **Se marier** · essayer l'école du soir | [À COMPLÉTER] | « À VOUS » n° 3 (S09) |
| 25 | Chercher du travail, puis se consacrer au foyer | [À COMPLÉTER] | — |
| 27 | Accueillir un chat | [À COMPLÉTER] | Respiration tendre (Luna) |
| **33** | **Se lancer avec son partenaire (la boutique)** | [À COMPLÉTER] | « À VOUS » n° 4 (S09) : le seul vrai « pari » de la vie, perdu en deux ans |
| 36 | « Bien sûr, essaie tout ce que tu as envie de faire » (à Khaled) | [À COMPLÉTER] | Écho possible à « youtubeuse » |
| 37 | Accueillir sa mère | [À COMPLÉTER] | — |
| **46** | **Tenir le coup seule** | [À COMPLÉTER] | « À VOUS » n° 5 (S09), à traiter avec pudeur |
| 47, 49 | Emmener quelqu'un à l'hôpital · écouter Tarek | [À COMPLÉTER] | — |
| 58 | Participer aux frais du mariage | [À COMPLÉTER] | — |
| 68 | Se faire soigner | [À COMPLÉTER] | — |
| 77 | Donner selon ses moyens | [À COMPLÉTER] | — |
| **80** | **Partir en pèlerinage** | [À COMPLÉTER] | « À VOUS » final, avant la mort : le seul choix « pour elle » |

**[IDÉE] Le rythme des « À VOUS »** : 6 au total (7, 11, 16, 24, 33, 46 ou 80 ans). Pour chacun, la vidéo montre :
- la question ;
- les options, avec leurs pourcentages réels ;
- **une ligne de contexte** (un chiffre du moteur ou une source réelle) ;
- **une prévision** posée au spectateur, du type « à votre avis, si elle reste à l'école, elle gagne combien d'années d'études ? ».

Puis le clic, et la conséquence.

## Les 4 autres bébés

Tirés avec les seeds suivantes (20261107 à 20261110), avec la même politique `auto`. **[MOTEUR]**

| Seed | Nom | Pays | Né(e) | Études | Travail | Famille | Mort |
|---|---|---|---|---|---|---|---|
| 07 | Purity Ochieng | Kenya, campagne, 3e cinquième | F | fin du lycée | pêcheuse (18-31 ans), puis agricultrice (31-66 ans) | en couple à 19 ans, 5 enfants (le 1er à 20 ans), père absent | 66 ans, cardiopathie |
| 08 | Fama Drammeh | Guinée, campagne, 3e cinquième | F | **aucune** | cuisinière dès 13 ans, agricultrice, éleveuse, pêcheuse | **en couple à 14 ans**, premier enfant à 16 ans, 5 enfants | 64 ans, infection respiratoire |
| 09 | Andrew Kweka | Kenya, campagne, 3e cinquième | M | collège | éleveur de 15 à 51 ans | 2 enfants | **51 ans**, infection respiratoire |
| 10 | Raj Valmiki | Inde, ville, **cinquième le plus pauvre**, **dalit** | M | primaire | ouvrier agricole, électricien, ouvrier d'usine, livreur | 1 enfant | 81 ans, cancer |

⚠️ **Correction du storyboard** : on supposait que les autres bébés faisaient leurs choix « au hasard ». Dans l'API, **ils suivent la même politique `auto` que Khadija**. C'est encore plus fort pour S10 : **même règle, cinq départs, cinq vies**. La seule chose qui change, c'est le point de départ. (Sur le site web, à vérifier.)

**[CALCUL]** Les 5 sont nés en Afrique ou en Inde, aucun en Europe ni dans les Amériques. C'est cohérent avec la répartition des naissances (l'Inde en fait 17,6 % à elle seule, et l'Afrique subsaharienne environ 30 % ; ce second chiffre est à vérifier), mais 5 tirages ne prouvent rien : on le dit comme une coïncidence parlante, pas comme une preuve.

## Comparaisons (contexte)

**Simulations du moteur, femmes nées aujourd'hui, 15 vies par pays (ordres de grandeur seulement). [MOTEUR]**

| | Algérie | France |
|---|---|---|
| Âge médian au décès | 87 ans | 88 ans |
| À 40 ans : travaille | 13 % | 53 % |
| À 40 ans : propriétaire de son logement | 20 % | 53 % |
| À 40 ans : patrimoine médian (en revenus médians) | −0,19 (endettée) | 3,3 |
| Enfants à 46 ans | 2,8 | 1,7 |
| Premier enfant (âge médian) | 26 ans | 32 ans |

**Algériennes, 30 vies : le cinquième le plus pauvre (le sien) et le plus riche. [MOTEUR]**

| | 20 % les plus pauvres | 20 % les plus riches |
|---|---|---|
| À 15 ans : primaire seulement | 43 % | 7 % |
| À 40 ans : université ou plus | 26 % | 52 % |
| À 40 ans : propriétaire | 4 % | 48 % |
| À 40 ans : rang de revenu médian dans le pays | 24e centile | 96e centile |
| Âge moyen au décès | 74 ans | 76 ans |

> **[IDÉE] Nuance anti-fatalisme (N11)** : Khadija a vécu jusqu'à **94 ans**. C'est plus que l'âge médian des Algériennes simulées (87 ans), et même que celui des Françaises (88 ans). La statistique pèse sur la vie, mais elle ne la dicte pas.

## Ce que la partie change pour la vidéo (propositions)

⚠️ Écrit pour Khadija, avant la décision du 06/11/2026 sur la naissance la plus probable. Le pays de la vie principale est désormais l'**Inde**, et Khadija devient une vie de comparaison. Les points 3 à 6 restent valables en les transposant (le rêve d'enfant, l'animal, le portrait, la preuve de l'aveu).

1. **Le pays : l'Algérie.** Cela rapproche la vidéo du spectateur français : les liens entre la France et l'Algérie sont forts, et c'est un vrai sujet. Il faudra le traiter **sans cliché**. Les photos (S05, S07, S09) seront des photos de l'Algérie rurale et d'Alger.
2. **Les étapes d'âge se recalent sur la vraie vie** : 0-10 ans (S07), **11 ans** (S08, l'école ou le travail), 16-49 ans (S09 : Alger, le mariage, la boutique, les années lourdes), puis 80 ans (le pèlerinage) et 94 ans (S11).
3. **« Youtubeuse »** (6 ans) : le détail le plus fort de la partie pour notre public. À placer en S07 et à reprendre dans l'aveu (S13).
4. **Luna**, la chatte : la respiration tendre du milieu de vie (27 à 42 ans).
5. **Le portrait (I13)** : une vraie photo d'une femme algérienne âgée, libre de droits et dont la licence autorise ce récit. ⚠️ Pexels interdit de montrer une personne identifiable sous un jour négatif : une vie avec des violences et un enfant perdu peut tomber sous cette clause. **À vérifier licence par licence.**
6. **L'aveu (S13) a sa preuve** : le moteur lui-même définit la politique `auto` comme « ce que la plupart des gens choisissent ». Et si le script le confirme, **la même vie jouée « pour réussir »** (politique `ambitious`) donnera la comparaison promise. **[À COMPLÉTER]**

## Points sensibles (à arbitrer avec Bruno)

La partie contient :
- **des violences conjugales répétées** (de 31 à 50 ans) ;
- la **mort d'un nourrisson** ;
- le **travail des enfants** ;
- une **gifle à l'école** ;
- la **faim** ;
- une **dépression** non soignée.

Ces choses arrivent « aussi souvent que dans les statistiques réelles » (c'est ce que dit le site).

Proposition, suivant la skill `documentary-montage-production` :
- ne jamais **illustrer** les violences : une phrase de l'interface, un silence, et c'est tout ;
- afficher **le 3919** (le numéro des violences conjugales en France) en surimpression discrète, comme le fait le moteur ;
- les mentionner en description ;
- ne pas en faire le cœur du récit, mais **ne pas les effacer** : ce serait trahir la statistique, et donc le sujet.

## Fidélité à l'interface du site

Le site arrête le temps à 5, 15, 30, 50 et 70 ans. L'API, elle, présente des décisions année par année. Notre interface recréée reprend **le style** du site, mais **le contenu** vient de l'API (le même moteur). On le dira honnêtement en description : « vie simulée avec le 1in8b Engine (1in8b.life) ».

## Archive

- `../prompts/partie/` : les JSON bruts du script (vie `auto`, vie `ambitious`, pas à pas `/live`, 4 bébés), produits par `shared/outils/1in8b/partie.py`. **[À COMPLÉTER]**, à lancer par Bruno avec sa clé.
- Les sorties du connecteur utilisées ici (vie, bébés, comparaisons) : seed et version du moteur ci-dessus ; le script les régénère à l'identique tant que le moteur reste en 0.9.52.
