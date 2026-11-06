# Faits et sources

Vérifié le 05/11/2026. **[VÉRIFIÉ]** = lu sur la source ; **[À VÉRIFIER]** = piste à confirmer au moment du script.

## Le simulateur : 1 sur 8 milliards

- **Site officiel** : https://1in8b.life (version française : https://1in8b.life/fr/). D'autres domaines (1in8billion.app, 1in8b.app, in8b.com) et une application Android **ne sont pas officiels**. [VÉRIFIÉ]
- **Droit de l'utiliser en vidéo** : « Oui. Vous pouvez la diffuser en direct, ou en faire des vidéos et les publier, sans nous demander, y compris sur des chaînes monétisées (…). Nous vous serions reconnaissants de citer la source (1 sur 8 milliards, 1in8b.life). » (page À propos) [VÉRIFIÉ] → **citer la source à l'écran et en description.**
- Créé par Jin's Earth, avec une IA (Claude, d'Anthropic). Ouvert le 5 octobre 2026. Version vue : v0.9.47 bêta, 172 pays et territoires, dès 15 ans. [VÉRIFIÉ]

### Les règles (page À propos)

| Règle | Détail | Usage dans la vidéo |
|---|---|---|
| Tirage du lieu | Selon le nombre de naissances par an (par défaut), ou selon la population. Impossible de choisir. **Le sexe et les moyens de la famille sont aussi tirés au sort** selon les proportions réelles | S04, S05 |
| Choix | Chaque année, on choisit la priorité de l'année. Sur les études, le travail, l'amour, l'émigration et les soins, c'est le joueur qui décide. « **Les choix changent les probabilités mais ne décident jamais du résultat** » | S08, S10 (citation possible) |
| Questions | « À 5, 15, 30, 50 et 70 ans, le temps s'arrête et vous pose une question » | Structure des cartons d'âge (T01) |
| Autres vies | « À côté de la vôtre, les vies de **quatre autres bébés nés à la même seconde** suivent les mêmes statistiques » | S10 (comparaison) · [À VÉRIFIER] même pays ou pays différents ? |
| Fin de vie | Âge du décès tiré chaque année selon les tables de mortalité du lieu et du sexe ; causes selon l'OMS (GHE). Un **acte de décès** clôt la vie | S11 |
| Vrai lieu de naissance | Facultatif, « pour comparer, côte à côte, la vie vécue avec la vôtre » | S03 (plant) → S14 (payoff) |
| Époques | Le passé (1950-2025), le monde d'aujourd'hui, l'avenir (projections), au hasard | Non utilisé (option) |
| Durée | Environ 30 min, 1 h ou 1 h 30 pour une vie entière ; pause, accélération jusqu'à 16 fois ; mode automatique | Production : partie à jouer et à noter |
| Mise en garde du site | « Les vies (…) ne disent rien d'une vraie vie passée, d'un destin (…). Deux bébés nés au même endroit la même année vivent pourtant des vies différentes » | S10, S15 (nuance N11) |

### L'API officielle : 1in8b Engine (https://1in8b.life/fr/api/, lue le 06/11/2026)

Indispensable pour la règle secrète (toujours l'option la plus probable, révélée en S13) :

- **Politique de décision `auto`** : « *what most people choose* » (ce que la plupart des gens choisissent). C'est le défaut quand on ne décide pas soi-même. Il existe aussi `ambitious`. **[VÉRIFIÉ, doc anglaise de l'API, 06/11/2026]** C'est la définition officielle de notre règle secrète.
- **Le connecteur Claude** (`live_a_life`, `compare_lives`…) ne donne que l'option retenue (« Décision : … ») : ni les autres options, ni leurs probabilités, ni le choix de la politique. Pour cela, il faut l'API HTTP : `/life?decisions=1` (« chaque décision rencontrée, ses options et celle qui a été prise ») et `/live`. **[VÉRIFIÉ]**

- **`POST /api/v1/live`** : « une vie vécue de l'extérieur, un pas à la fois : vous prenez chaque décision ». Et pour les applis : « /live envoie chaque décision avec les probabilités que le monde lui donne ». → On peut donc prendre, à chaque décision, l'option la plus probable, de façon **mesurée et prouvable**. [VÉRIFIÉ sur la page ; format exact des réponses à lire dans la doc anglaise et dans `/api/v1/openapi.json`]
- **`seed`** : « la même seed et la même version du moteur donnent les mêmes vies ». Pour reproduire une partie, il faut conserver la version du moteur (`meta.engine`) et la date. [VÉRIFIÉ]
- Sans `country`, le lieu est tiré selon la part des naissances, comme sur le site. Le paramètre `lang` donne le récit et les choix en français. [VÉRIFIÉ]
- **Clé gratuite** : envoyer un e-mail à api@1in8b.life (la clé, qui commence par `k8b_`, arrive en réponse). 2 000 unités de vie par mois, une vie du monde d'aujourd'hui = 1 unité, 30 appels par minute. Largement suffisant. **C'est Bruno qui la demande et la garde** : elle ne va ni dans Git ni dans une conversation. [VÉRIFIÉ]
- Il existe aussi un connecteur MCP officiel (`https://1in8b.life/mcp`), à ajouter dans les réglages de Claude. Il permettrait de jouer la partie directement en discutant, sans que la clé me soit transmise. [VÉRIFIÉ sur la page, non testé]
- **Citer la source** : « 1in8b Engine (1in8b.life) ». [VÉRIFIÉ]
- **À vérifier** : est-ce que le **site web** affiche aussi les probabilités des options pendant une partie ? Si oui, l'encart « À VOUS » peut reprendre l'interface réelle ; sinon, on l'affiche à partir des données de l'API, en le disant honnêtement à l'écran ou en description.

### Sources des chiffres du site

ONU *Perspectives de la population mondiale 2024* (naissances, population, espérance de vie, fécondité), UN IGME (mortalité des enfants), OMS et UN MMEIG, PNUD et UNESCO, Banque mondiale (revenus, inégalités), OIT, ONU-Habitat, ONUSIDA, ONUDC, UNICEF, *World Happiness Report* 2024. Revenu tiré de la distribution du lieu (indice de Gini). [VÉRIFIÉ, page À propos]

## Naître en France

Page « Statistiques de 172 pays » du site (https://1in8b.life/fr/c/), d'après l'ONU WPP 2024, **environ 132 millions de naissances dans le monde en 2023** [VÉRIFIÉ] :

| Pays | Part des naissances | Probabilité | Espérance de vie | Décès avant 5 ans | Revenu par habitant (PPA, $) |
|---|---|---|---|---|---|
| **France** | **0,48 %** | **1 sur 207** | 83,3 | 0,4 % | 54 297 |
| Inde | 17,60 % | 1 sur 6 | 72,0 | 2,8 % | 8 871 |
| Chine | 6,75 % | 1 sur 15 | 77,9 | 0,6 % | 22 687 |
| Nigeria | 5,69 % | 1 sur 18 | 54,5 | 11,7 % | 7 843 |
| RD Congo | 3,31 % | 1 sur 30 | 61,9 | 9,1 % | 1 559 |
| États-Unis | 2,77 % | 1 sur 36 | 79,3 | 0,7 % | 74 352 |

- ⚠️ « 1 sur 207 » est la probabilité de **naître sur le territoire français** (naissances en France / naissances dans le monde). Ce n'est **pas** la probabilité d'avoir la nationalité française : le concept demande de bien faire la différence. [À VÉRIFIER] : le périmètre exact (la France entière, avec ou sans Mayotte) dans les données de l'ONU.
- Naissances en France en **2024** : **660 800** (Insee Focus, juillet 2025, données définitives ; −2,8 % par rapport à 2023 ; le plus bas depuis 1945). [Résumé d'une recherche web, page à relire avant le script : https://www.insee.fr/fr/statistiques/8614311] → Pour un calcul sur la même année que l'ONU (2023), prendre les naissances 2023 de l'Insee. [À VÉRIFIER]

## Le déterminisme social en France

Pistes (une ou deux suffiront, avec l'année et la population à l'écran) :
- **Diplôme du supérieur selon l'origine sociale** : enfants de cadres contre enfants d'ouvriers, environ 77 % contre 25 % pour la génération née au milieu des années 1970 (Insee) ; 76 % contre 20 % (enfants de cadres ou d'enseignants contre enfants d'ouvriers non qualifiés) pour le panel d'élèves entrés en 6e en 1995 (Depp/SIES). [À VÉRIFIER sur les publications]
- **Source de référence la plus à jour** : Insee Références, édition 2025, « Niveau de diplôme de la population » (https://www.insee.fr/fr/statistiques/8612520). [À VÉRIFIER]
- Rappel obligatoire à l'écran : **une tendance collective ne détermine pas un parcours individuel.**
