# La partie

Parties jouées le 06/11/2026 avec le **1in8b Engine** (l'API officielle de 1 sur 8 milliards). C'est **la matière de la vidéo**.

Légende : **[MOTEUR]** = donné par le moteur (récit, chiffres, citations) · **[CALCUL]** = calculé par nous à partir des sorties du moteur · **[IDÉE]** = proposition de mise en scène · **[À COMPLÉTER]** = attend le script `shared/outils/1in8b/partie.py`.

## Ce qu'on entend par « la vie la plus probable » (décision de Bruno, 06/11/2026)

| Niveau | Règle | Comment |
|---|---|---|
| **La naissance** | Les conditions les plus probables | Pays : **l'Inde** (17,6 % des naissances, 1 sur 6) **[MOTEUR, page du site]**. Lieu : **la campagne** (68 % des bébés indiens simulés, 41 sur 60) **[MOTEUR]**. Sexe : **garçon** (en Inde, il naît environ 107 à 110 garçons pour 100 filles ; **[À VÉRIFIER]**, ONU WPP 2024). Cinquième de revenus : chacun fait 20 % par définition, donc aucun n'est « le plus probable » ; on prend **celui du milieu** (le 3e). Religion et caste : **les plus fréquentes, mesurées par le moteur** (script, option `--mesurer faith,caste`) |
| **Les décisions** | L'option que prend la majorité dans la même situation | La politique `auto` du moteur, « ce que la plupart des gens choisissent ». Statistiquement, c'est l'option qui avait le plus de chances d'être prise |
| **Les événements** | Impossible à choisir | Les maladies, les rencontres et la mort sont tirées au sort par le moteur. On situe chacun d'eux par rapport aux médianes de vies simulées |

**[CALCUL]** Inde × campagne × garçon × 3e cinquième ≈ 17,6 % × 68 % × 52 % × 20 % ≈ **1,2 % des naissances**, soit environ 1 sur 80. C'est peu, mais aucune autre combinaison n'est plus fréquente. C'est le paradoxe à dire dans la vidéo : même la vie la plus probable est rare.

## Où on en est

1. **Khadija Ibrahim**, jouée en premier : naissance **tirée au sort** (Algérie), décisions `auto`. Elle **n'est plus la vie principale**. Elle devient une vie de comparaison : « la vie tirée au sort ».
2. **Yash Gupta**, jouée ensuite par le connecteur : Inde, campagne, garçon, 3e cinquième, décisions `auto`. Mais la religion (hindou) et la caste (« catégorie générale ») ont été **tirées par le moteur**, parce que le connecteur ne permet pas de les fixer. Or la catégorie la plus nombreuse en Inde est sans doute celle des « autres classes défavorisées » (OBC), et pas la catégorie générale **[À VÉRIFIER]**. **Yash est donc une version provisoire.**
3. **La vie définitive** viendra du script : conditions ci-dessus, religion et caste mesurées par le moteur, puis la même vie en politique `ambitious`, et chaque décision avec ses options. Si la caste mesurée est bien la catégorie générale, la vie définitive sera Yash, puisque la seed et les conditions sont les mêmes.

## Yash Gupta (version provisoire)

Seed 20261106, moteur 0.9.52. **[MOTEUR]** Né en 2026 dans un village indien, hindou, catégorie générale, 3e cinquième. Ses parents ont 28 et 32 ans ; il a 1 frère aîné, et 3 petits frères naîtront ensuite. Mort à **74 ans**, de bronchopneumopathie chronique obstructive (BPCO).

- **L'enfance (0 à 10 ans)** :
  - pas de vaccins, parce que le centre de santé était trop loin ; une pneumonie à 1 an ;
  - la queue au puits pour remplir la cruche ;
  - à 6 ans, pas d'acte de naissance : il faut régler les papiers avant l'école ;
  - **à 6 ans, quand on lui demande ce qu'il veut faire plus tard : « chef d'entreprise »** ;
  - des coups de baguette sur la paume, « après cela, vous n'avez plus levé la main en classe » ;
  - le cricket, qui sera la passion de sa vie ;
  - **à 10 ans, une image très forte : les enfants dont la famille a donné une enveloppe à l'enseignant sont assis sous le ventilateur ; lui, au fond, s'essuie le front** (le moteur cite Transparency International : 22 % des usagers disent avoir versé un pot-de-vin à l'école publique).
- **L'école** : à 11 ans, décision « Continuer à étudier » (le collège) ; à 14 ans, « Aller au lycée » ; à 17 ans, « Rester à l'école ». Il finit le lycée à 18 ans. Le moteur cite les 2 276 069 inscrits au concours de médecine NEET-UG 2025.
- **18 ans · le carrefour** : décision **« Prendre un emploi tout de suite » plutôt que l'université**. Il devient éleveur. Décision : « Boire moins et trouver d'autres façons de tenir ».
- **23 ans** : décision **« Partir à Kanpur »**, où il devient électricien. 1 h 30 d'embouteillages par jour. À 25 ans, le chantier s'arrête et il n'a plus de travail ; il reprend comme électricien à 26 ans.
- **27 à 34 ans · l'amour qui n'aboutit pas** : à 27, 29 et 32 ans, la même décision, **« Prendre le temps de mieux se connaître »** avec Rashmi. À 34 ans : « Le projet de mariage avec Rashmi n'a finalement pas abouti. » **Il ne se mariera pas et n'aura pas d'enfant.** Pourtant, environ 93 % des hommes indiens simulés vivent en couple avant 50 ans **[MOTEUR]**. Le choix le plus fréquent, répété trois fois, a mené à une issue rare.
- **28 ans** : une moto à crédit. **31 ans** : la mort de son père, à 64 ans. **37 ans** : décision **« Appeler maintenant pour le dire »** : « Au bout du fil, vos mots ont laissé votre mère sans voix un long moment. »
- **43 ans** : décision « Acheter avec un prêt immobilier » : avec l'aide de sa mère, il achète son logement, et il a 18 900 € de dette.
- **55 ans** : un chat, Max. **56 ans** : licencié après 30 ans de travail, avec une indemnité de 18 900 € ; il devient ouvrier d'usine et rembourse toutes ses dettes.
- **60 ans** : la retraite. **61 ans** : la première télévision et le premier réfrigérateur.
- **62 ans** : la mort de sa mère, à 91 ans. **63 ans** : « Après des années sans rien gagner, vous avez cessé d'acheter des billets de loterie. »
- **64 ans** : « Quand vous rentriez dans la maison où vous viviez seul, le premier bonjour venait de Max. »
- **71 ans** : Max meurt ; ses poumons sont très affaiblis (le moteur cite la pollution, 56 µg/m³ de particules fines, soit 11 fois la valeur guide de l'OMS). **72 ans** : il vend sa maison et rembourse tout. **73 ans** : décision « Rester chez vous ».
- **74 ans** : « Vous avez confié à un frère ce que vous n'aviez pu dire à personne. Pour toute réponse, une présence silencieuse à vos côtés. » Le bénévolat à la soupe populaire. La mort.

**[CALCUL] Une vie très proche de la médiane** : il meurt à 74 ans, quand l'âge médian au décès des hommes indiens simulés est de 72 ans. À 40 ans, il travaille, comme 93 % d'entre eux. Il sort de la statistique sur deux points. Ses études d'abord : il finit le lycée, alors qu'à 40 ans seuls 21 % des hommes indiens simulés ont ce niveau (le plus fréquent est le collège, 45 %), sans doute grâce au 3e cinquième et à la catégorie générale, à vérifier avec la caste mesurée. Et le célibat.

> **[IDÉE]**
> - « Chef d'entreprise » à 6 ans, électricien toute sa vie : c'est l'écho du rêve d'enfant, à reprendre dans l'aveu.
> - Le ventilateur est une image parfaite pour la vidéo, et faisable en motion design : une salle de classe en plan, des pupitres, un ventilateur, des points qui s'écartent.
> - Le grand « À VOUS » devient celui de **18 ans : l'université ou un emploi tout de suite**. Le spectateur choisira l'université, et l'opérateur cliquera « emploi ».

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
