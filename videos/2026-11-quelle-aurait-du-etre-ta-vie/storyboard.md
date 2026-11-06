# Storyboard · Quelle aurait dû être ta vie ?

Vue d'ensemble : une ligne par scène, le détail dans chaque fiche scène.
Procédés choisis avec le [mode d'emploi](../../docs/direction-artistique/procedes/README.md) et le [catalogue](../../docs/direction-artistique/procedes/catalogue.md). Faits : [`references/sources.md`](references/sources.md).

**Statut** : proposition de Claude (05/11/2026), à arbitrer par Bruno. Pour chaque scène : le procédé recommandé, et une alternative.

## Décisions déjà prises par Bruno

- **La règle du jeu (06/11/2026)** : le spectateur croit jouer, mais l'opérateur prend en secret **toujours le choix le plus probable**. On ne le révèle qu'à la fin (S13), avant la réflexion sur la France et le déterminisme social. Voir la section « Règle du jeu » ci-dessous.
- **Rien n'est filmé** : Blender pour le bureau et l'opérateur, Remotion pour l'interface, le motion design et le montage.
- **Voix off** : l'opérateur, à la première personne.
- **Images de la vie** : de **vraies photos** d'illustration (banques libres de droits, archives), retravaillées dans Remotion.
- **La vidéo ne doit jamais être reconnaissable comme faite à l'IA** : aucune mention d'IA à l'écran, et les règles anti-« look IA » ci-dessous s'appliquent à toute la fabrication.
- **Priorité à l'animation** : on privilégie les moments d'animation, de motion design et de 3D. Les photos restent un **complément**, pas la matière principale. À appliquer en affinant le découpage : quand un plan peut être raconté en motion design ou en 3D plutôt qu'en photo, on choisit l'animation.

## La partie jouée (06/11/2026)

**Décision de Bruno : la vie de la vidéo est la vie la plus probable, à la naissance comme aux décisions.** On ne prend pas seulement les choix les plus probables : on impose aussi la naissance la plus probable. Elle est donc **en Inde, à la campagne, d'un garçon, dans le cinquième du milieu**, avec la religion et la caste les plus fréquentes, mesurées par le moteur. Le détail est dans [`references/partie.md`](references/partie.md).

- **La vie définitive : Manoj Mohanty**, hindou, OBC. À chaque décision, l'option la plus fréquente, mesurée sur 200 vies nées dans les mêmes conditions :
  - à 8 ans, il veut être « ingénieur » ;
  - **à 11 ans, il choisit de continuer l'école, comme 97 % des vies, mais sa famille ne peut pas payer**, et il garde les bêtes ;
  - à 15 ans, il devient pêcheur ;
  - il guérit de la tuberculose, qui emporte deux de ses frères ;
  - il épouse Preeti à 26 ans, et ils ont 2 enfants ;
  - il découvre le théâtre, puis il y a une liaison, et le pardon ;
  - à 53 ans, il est applaudi pour un premier rôle ;
  - il ne solde jamais sa dette ;
  - son petit-fils entre à l'université ;
  - il meurt à 75 ans.
- **Découverte de méthode** : la politique `auto` du moteur tire au sort selon les parts. Elle ne prend pas toujours l'option majoritaire, d'où la partie jouée pas à pas. Les pourcentages des encarts « À VOUS » sont les parts observées.
- **La variante ambitieuse** (même naissance) donne un professeur, dans le top 3 % des revenus, mort à 89 ans. **Les choix comptent donc, dans le moteur.** L'aveu dira « une pente, pas une interdiction », et non « vos choix n'auraient rien changé ».
- **Khadija Ibrahim** (Algérie, tirée au sort) devient une vie de comparaison : « la vie tirée au sort ».
- **L'aveu (S13) gagne une phrase** : « Je n'ai rien choisi. Pas même son pays. » Le paradoxe à dire : même la vie la plus probable ne concerne qu'environ 1 bébé sur 80.

**À arbitrer par Bruno avant de reprendre les fiches S04 à S13** : le recalage des âges sur la vie définitive, et le traitement des passages sensibles.

## Règle du jeu : le spectateur croit jouer, mais il ne joue pas

**L'enjeu de la vidéo** (décisions de Bruno, 06/11/2026) :
1. **Le spectateur est invité à jouer.** À chaque grande étape, les options s'affichent avec leurs pourcentages : « Vous, vous prendriez quoi ? » Il anticipe, il essaie de bien choisir, de « réussir » cette vie. L'opérateur clique.
2. **En réalité, l'opérateur prend toujours l'option la plus probable**, sans le dire. La vie montrée est donc celle que cette personne « aurait dû » vivre, au sens statistique : le chemin le plus fréquenté à chaque carrefour.
3. **L'aveu arrive à la fin (S13)**, après la mort et le silence : « Je n'ai rien choisi pour elle. » Le spectateur découvre qu'une vie qui avait l'air faite de choix n'a jamais été choisie, et qu'il n'a pas vu la différence. C'est **N02** (le twist méta) : son propre comportement pendant la vidéo devient la réponse. On surestime la part qu'on choisit.
4. **Puis on bascule vers le réel** : naître en France (S14), le déterminisme social (S15), la question finale (S16).

Pourquoi ce n'est pas le twist que le concept exclut : il ne s'agit pas d'une « simulation dans la simulation » qui détournerait du sujet. L'aveu **porte sur le sujet lui-même** (la part de choix dans une vie) et se résume en une phrase, sans explication longue.

### Les indices laissés en route (pour que l'aveu soit loyal)

Au second visionnage, tout doit être visible :
- **Les pourcentages sont toujours à l'écran**, et l'option cliquée est toujours la plus haute. Personne n'y prête attention, parce que tout le monde regarde le contenu des options.
- **S05** : « Je n'ai rien choisi de tout ça. Elle non plus. » La phrase a un double sens, qu'on ne comprend qu'à la fin.
- **S08** : la main de l'opérateur hésite au-dessus d'une option, puis clique sur une autre, sans commentaire.
- L'opérateur **ne ment jamais** : il ne dit jamais « je choisis ceci parce que je préfère ». Il dit « je prends celle-là », « on continue ».
- **S10** : les 4 autres bébés suivent **la même règle** que Khadija (politique `auto`), et pourtant leurs vies n'ont rien à voir. Même règle, cinq départs, cinq vies (voir `references/partie.md`).

### La mécanique de jeu à l'écran

Un élément d'interface récurrent, **« À VOUS »** : à chaque décision, les options et leurs pourcentages restent figés 3 à 4 secondes, avec un compte à rebours discret, le temps que le spectateur choisisse dans sa tête. Puis le clic de l'opérateur. Même forme, même sens à chaque fois : « c'est votre tour ». Il apparaît aux grandes décisions seulement (S07, S08, S09), pas à chaque année, pour ne pas lasser.

### Points de méthode (à trancher avant de jouer)

- **Le point de départ reste tiré au sort** (le pays, le sexe, les moyens de la famille). C'est la loterie de la naissance, le sujet même, et le site ne permet pas de le choisir. La règle ne porte que sur les décisions.
- **« Le plus probable » est défini par le moteur lui-même** : sa politique `auto`, « ce que la plupart des gens choisissent » (le défaut). C'est elle qui a joué la partie du 06/11/2026. Les options et leurs probabilités, décision par décision, viennent du script `shared/outils/1in8b/partie.py`, qui passe par l'API (`/life` avec `decisions=1`, et `/live`).
- **Le choix le plus probable à chaque étape** ne garantit pas, mathématiquement, la trajectoire la plus probable dans son ensemble. L'aveu dira donc « à chaque carrefour, j'ai pris le chemin le plus fréquenté », et non « la vie la plus probable qui soit ». La formule exacte sera fixée au script.
- **Les événements subis** (maladies, rencontres, décès) restent tirés au sort par le simulateur.
- **Reproductibilité** : l'API accepte une `seed` (la même seed et la même version du moteur redonnent la même vie). On archive la seed, la version du moteur et la partie complète dans `prompts/`.
- **Option à tester (preuve renforcée)** : rejouer la même seed en prenant cette fois les options « pour réussir » (celles que le spectateur aurait sans doute choisies), et comparer les deux vies dans l'aveu. Si l'écart est faible, c'est une démonstration très forte de « les choix changent les probabilités, pas le résultat ». **Hypothèse non vérifiée** : on ne l'utilise que si les données le montrent vraiment.

## Règles anti-« look IA »

| Domaine | Règle |
|---|---|
| Images de la vie | Uniquement de **vraies photos**. Pas de visage ni de personnage généré. Chaque photo est inscrite dans `references/photos.md` (lien, auteur, licence) |
| Animation des photos | Mouvements **lents et sobres** (Ken Burns, léger recadrage). Pas de parallaxe 2.5D exagérée ni d'animation de photo par IA : les déformations trahissent tout de suite |
| Traitement | Un même traitement « photo » pour toutes les sources (I04) : grain argentique fin, ton chaud, léger vignettage. **Pas** de lignes de balayage ni d'aberration chromatique sur ces images |
| 3D Blender | Textures réelles (Poly Haven, CC0), imperfections (poussière, usure, câbles), optique crédible (focale 35-50 mm, profondeur de champ, flou de mouvement), grain identique aux photos. Rien de « trop parfait » ni de trop symétrique |
| Higgsfield | Jamais d'image générée à l'écran telle quelle. Usage réservé, si besoin, à des références de travail ou à des éléments invisibles (texture de fond, recherche de lumière) |
| Voix | Une **voix humaine** (Bruno ou un comédien), pas de voix de synthèse. Recommandation : à confirmer (voir la question ouverte du journal) |
| Musique | Composée par un humain : bibliothèque sous licence ou compositeur. Pas de musique générée |
| Design | Typographies et mises en page choisies, pas de gabarits génériques. Les données et le texte à l'écran sont toujours exacts et sourcés |

Contraintes du concept : pas de twist « simulation dans la simulation » (l'aveu de S13 porte sur le sujet lui-même, voir « Règle du jeu »), pas d'effets futuristes ni de glitchs démonstratifs (donc **pas de T02**), l'opérateur reste au service du récit.

## Grammaire de la vidéo

| Élément | Choix | Procédés |
|---|---|---|
| Lieu principal | **Le bureau** : huis clos sobre, froid, presque administratif. C'est le seul lieu de la vidéo ; pas d'objet-concept concurrent | (pas de N04 ni de N07) |
| Matières d'image (3) | **3D Blender** = le cadre (le bureau, l'opérateur) · **Remotion** = la machine et les données (interface, cartons, graphiques) · **vraies photos** = la vie humaine simulée | I04 |
| Couleur d'accent | **Ambre chaud**, réservé à **l'humain** : la vie simulée, l'âge, le portrait. Tout le reste est froid (gris-bleu, blanc d'écran). C'est le contraste voulu par le concept : un cadre froid face à une vie humaine | — |
| Palette par chapitre | Huis clos, donc **une lumière qui évolue** : la lumière du bureau suit l'âge de la vie simulée. Aube à la naissance, plein jour à l'âge adulte, crépuscule dans la vieillesse, nuit à la mort, puis **aube de nouveau** au bouclage | I16, I18 |
| Registres typographiques (2) | **Monospace = dans la simulation** (interface, cartons d'âge, données du simulateur) · **Serif = hors de la simulation** (le monde réel, la France, la narration à l'écran, le titre) | H02 |
| Transition signature | **Le carton d'âge** (T01, version sobre : sans glitch, une barre et un âge). Il signifie toujours « la vie simulée avance d'une étape ». Une seule autre transition : le **noir** (T03), qui signifie toujours « on sort de la simulation » | T01, T03 |
| Plants → payoffs | (1) Le spectateur note un chiffre (S02) → on le lui redemande (S16) · (2) L'opérateur saisit son vrai lieu de naissance, la France (S03) → la comparaison avec lui-même (S14) · (3) Le portrait en mosaïque (S05) → net à la mort (S11) : **une seule vraie photo**, pixelisée dès le départ ; on ne découvre qui était cette personne qu'à la fin · (4) Le bureau à l'aube (S02) → l'aube de nouveau (S16) · (5) **Les pourcentages et l'encart « À VOUS »** à chaque grande décision (S07-S09) → l'aveu : l'option cliquée était toujours la plus haute (S13), puis « À VOUS » revient une dernière fois sur la question finale (S16) | N01, N05, I13, M07, N02 |
| Son | Clavier et ambiance du bureau au début · musique discrète pendant la simulation · **3 silences d'une seconde** (le pays, la mort, « 1 sur 207 ») · une respiration après la mort · fin musicale | S01, M05, S05, S02 |
| **Signatures (5)** | **T01** cartons d'âge · **I13** le visage qui se précise · **I16 + I18** la lumière du bureau qui suit la vie · **M04** les années qui défilent · **N05** le vrai lieu de naissance | |

## Scènes

| ID | Partie | Ce qui se passe | Fonction | Procédé principal | Secondaires | Alternative au principal | Durée ≈ | Fabrication |
|---|---|---|---|---|---|---|---|---|
| S01 | Ouverture | Carton : « Cette vie est simulée par *1 sur 8 milliards* (1in8b.life) à partir de statistiques réelles. » | ACCROCHER | **H06** : contrat de confiance. Il pose d'emblée que la **vie** est simulée (ce que demande le concept), sans parler des outils de fabrication | — | (aucune : c'est une mention honnête nécessaire) | 0:06 | Remotion |
| S02 | Le bureau, à l'aube | L'opérateur de dos, l'écran allumé, la lumière d'aube. « On m'a confié une mission : faire vivre quelqu'un, du premier jour au dernier. » Puis, au spectateur : « Vous allez jouer avec moi. À chaque grand choix, choisissez pour elle. Mais avant, notez un chiffre : sur 100, quelle part de votre vie avez-vous choisie ? » (La règle secrète n'est **jamais** annoncée.) | ACCROCHER | **N01** : le spectateur s'engage (un chiffre, puis le jeu), et toute la vidéo y répond | I18, I16 | N03 (montrer l'acte de décès flouté : « voilà comment cette vie finira ») | 0:50 | Blender + Remotion |
| S03 | La mission | L'interface : le monde d'aujourd'hui, le tirage selon les naissances. L'opérateur saisit son vrai lieu de naissance, la France. « Gardez ça en tête, on y reviendra. » | PROMETTRE | **N05** : le plant le plus utile de la vidéo, car le site permet vraiment la comparaison avec sa propre vie | H02 | N03 | 0:35 | Remotion (interface) + Blender |
| S04 | Naître | Le bouton « Naître », le premier carton **0 AN**, une seconde de silence, puis le pays et la ville seuls à l'écran | RÉVÉLER | **T01** : sa première apparition fixe son sens (une étape d'âge) | S01, I15 | I15 en principal (le pays seul, en grand) | 0:20 | Remotion |
| S05 | Les conditions de départ | La famille, ses moyens, le lieu. « Je n'ai rien choisi de tout ça. Elle non plus. » Le portrait apparaît en très gros pixels | INCARNER | **I13** : la personne n'existe encore presque pas. Chaque étape ajoutera un cran de netteté | I04 | I04 en principal (les photos du lieu) | 0:40 | Photos + Remotion |
| S06 | Les années qui passent | Une année ≈ une seconde ; le compteur d'âge ; la lumière du bureau qui monte. Revient en interlude entre chaque étape | TRANSITIONNER | **M04** : le temps qui passe devient un rythme, et le site fonctionne vraiment ainsi (environ une année par minute, accélérée) | I16 | T03 (noir entre les étapes : non, ce noir est réservé à la sortie) | 0:15 (×4) | Remotion + Blender |
| S07 | 5 ans · l'enfance | Carton 5 ANS, la question du site. Premier encart « À VOUS » : les options et leurs pourcentages, 3 s pour choisir, puis le clic. L'enfance en vraies photos du pays (des enfants de dos ou de loin, jamais un visage identifiable) | INCARNER | **I04** : les photos, d'origines variées, sont unifiées en une seule matière chaude, distincte du bureau froid | T01 | M03 (une grappe d'images courtes) | 0:50 | Photos + Remotion |
| S08 | 15 ans · le premier choix | La décision (les études). « À VOUS » : les options et leurs pourcentages. La main de l'opérateur hésite au-dessus d'une option, puis clique sur une autre, sans commentaire (en secret : la plus probable). Le site rappelle que le choix change des probabilités, pas le résultat | INCARNER | **N15** : la réaction spontanée de l'opérateur rend le moment humain, et son hésitation est l'indice le plus visible de la règle secrète | T01, I13 (un cran de netteté) | N11 (la nuance du site, citée à l'écran) | 0:50 | Blender + Remotion |
| S09 | 30 et 50 ans · la vie adulte | Travail, relations, ce qui arrive sans qu'on l'ait choisi. Trois ou quatre événements seulement. « À VOUS » à 30 et à 50 ans | RESSENTIR | **M03** : de courtes grappes d'images sur les événements, entre deux temps d'interface | T01, I13 | I04 (des plans plus longs, plus contemplatifs) | 1:00 | Photos + Remotion |
| S10 | Les autres trajectoires | Les 4 autres bébés nés à la même seconde. Leurs vies se dessinent sur la même frise d'âge. « Une trajectoire probable n'est pas un destin » | EXPLIQUER | **I03** : un seul plan où les 5 trajectoires se construisent ensemble, et où l'on voit à la fois les écarts et les ressemblances | N11 | I05 (la vraie phrase du site, en source primaire) | 1:15 | Remotion |
| S11 | La fin de la vie | Le dernier carton (l'âge du décès), une seconde de silence, l'acte de décès. Le portrait (la même vraie photo, pixelisée depuis S05) est enfin net | RÉVÉLER | **I13** (payoff) : on ne connaît vraiment quelqu'un qu'à la fin | T01, S01 | N03 en amont (acte de décès flouté dès S02) | 0:40 | Remotion + photo |
| S12 | Respiration | La nuit dans le bureau. L'écran affiche l'acte de décès, l'opérateur ne bouge plus. 15 s sans voix, puis une coupe au noir | RESPIRER | **M05** : laisser décanter, comme le demande le concept | T03 | S05 (musique seule, sans image nouvelle) | 0:20 | Blender |
| S13 | L'aveu | Après le noir, en serif. « Je vous dois un aveu. » La rafale de tous les écrans de décision de la partie : à chaque fois, l'option cliquée était la plus haute. « Je n'ai rien choisi pour elle. À chaque carrefour, j'ai pris le chemin le plus fréquenté. » Puis au spectateur : « Vous, vous avez essayé de bien choisir. Et vous n'avez pas vu la différence. » | RÉVÉLER | **N02** : le comportement du spectateur pendant la vidéo (jouer, croire choisir) devient la réponse. On surestime la part qu'on choisit | M03 (la rafale des écrans), H02 | I15 (les pourcentages cliqués seuls, en grand, sans rafale) | 0:45 | Remotion + Blender |
| S14 | Et nous ? Naître en France | On ressort de la simulation (serif). Le payoff du lieu saisi au début : un mur de 207 noms de pays tirés au sort, où la France n'apparaît qu'une fois. Silence. « 1 sur 207. » Puis la distinction entre naître en France et être Français, et la source | RÉVÉLER | **I11** : 1 chance sur 207 devient visible et physique | S01, I15 | I15 seul (le chiffre en grand, sans le mur) | 1:00 | Remotion |
| S15 | Le déterminisme social en France | Même en France, les départs diffèrent : le diplôme selon l'origine sociale (Insee), un graphique qui se construit, la page source. « Une tendance n'est pas un destin » | PROUVER | **I03** : même forme, même sens qu'en S10 (comparer des trajectoires) | I05, N11 | I05 en principal (la page Insee seule) | 1:10 | Remotion |
| S16 | Conclusion | Retour au bureau, à l'aube. L'écran propose de nouveau « Naître ». « Et votre chiffre du début, il a bougé ? » Puis : « Quelle aurait dû être ta vie ? », avec l'encart « À VOUS » une dernière fois : cette fois, c'est vraiment son tour. Musique seule | RÉVÉLER | **N14** : la question rendue au spectateur | M07, S05 | I15 (la question seule à l'écran, sans l'encart) | 0:40 | Blender + Remotion |

**Durée totale estimée** : ≈ 11 min 15 (à resserrer au script ; l'aveu ajoute ≈ 45 s).

## Arc narratif

1. **Le jeu** (S01-S04) : l'opérateur invite le spectateur à jouer ; on installe le chiffre sur 100 et le lieu de naissance.
2. **Glissement** (S05-S09) : la vie avance. À chaque grande décision, le spectateur choisit dans sa tête, l'opérateur clique (en secret, toujours l'option la plus fréquente). Les choix pèsent peu face au point de départ. La lumière monte, puis décline.
3. **Recul** (S10) : les autres trajectoires montrent la part du hasard et celle des statistiques, sans fatalisme.
4. **Fin et silence** (S11-S12) : la mort, le portrait net, la respiration, le noir.
5. **L'aveu** (S13) : personne n'a rien choisi, et personne n'a vu la différence. Le twist renverse tout ce qu'on vient de voir.
6. **Retournement** (S14-S15) : la question devient la nôtre, en France, jusqu'au déterminisme social.
7. **Ouverture** (S16) : le bouclage à l'aube, le chiffre du spectateur, la question finale.

## Bilan des procédés

| Procédé | Scènes | Rôle dans cette vidéo (sens constant) |
|---|---|---|
| T01 | S04, S07, S08, S09, S11 | Carton d'âge : la vie simulée avance d'une étape (calé sur les arrêts du site à 5, 15, 30, 50, 70 ans) |
| I13 | S05, S08, S09, S11 | Le visage de la personne se précise à mesure qu'on la connaît |
| I16 + I18 | S02, S06, S12, S16 | La lumière du bureau suit l'âge de la vie simulée |
| M04 | S06 | Le temps qui passe (une année ≈ une seconde) |
| N05 | S03 → S14 | Le vrai lieu de naissance, saisi puis comparé |
| N01 | S02 → S16 | Le chiffre du spectateur |
| I04 | S05, S07, S09, S11, S15 | La vie en vraies photos, unifiées par un même traitement photo |
| H01 | S14 | La source des données à l'écran |
| I03 | S10, S15 | Comparer des trajectoires (dans la simulation, puis en France) |
| S01 | S04, S11, S14 | Silence avant le pays, la mort, « 1 sur 207 » |
| I15 | S04, S14 | Le lieu ou le chiffre seul à l'écran |
| N11 | S10, S15 | Probabilité ≠ destin |
| H02 | partout | Mono = dans la simulation · serif = hors de la simulation |
| M03 | S09, S13 | Une suite d'instants vus en rafale (les événements de la vie, puis les écrans de décision) |
| N02 | S07-S09 → S13 | Le jeu du spectateur, puis l'aveu : il ne jouait pas |
| H06, N15, M05, T03, I11, I05, N14, M07, S05 | une fois chacun | Voir les scènes |
| M02, S02, S07 | partout | Standards |

- **Nombre de procédés différents** : 25, hors standards (cible : 15 à 25, on est à la limite haute) ✅
- **Procédés « une fois par vidéo »** : N01, N02, H06, N14, M07, chacun utilisé une seule fois ✅
- **Couche 2** : aucune. N12 est écartée : N02 la remplace, et le catalogue déconseille de les enchaîner.
- **Écartés ou exclus par le concept** : N13 (écarté), T02 (pas de glitch). N02 n'est plus exclue : l'aveu porte sur le sujet lui-même, pas sur une « simulation dans la simulation » (décision de Bruno, 06/11/2026).

## Découpage en plans : vue d'ensemble

**Une scène n'est pas un plan.** Chaque fiche scène contient son découpage plan par plan (identifiants `S05-P03`…) : durée, matière, contenu, animation, procédé, son.

Les quatre matières de plan, toutes fabriquées. Elles restent dans les 3 matières de la grammaire, car UI et MD sont deux usages de Remotion :
- **3D** : Blender (le bureau, l'opérateur) ;
- **UI** : l'interface du simulateur recréée (Remotion, monospace) ;
- **MD** : le motion design et les animations Remotion (cartes, jauges, frises, graphiques, textes) : en monospace dans la simulation, en serif hors de la simulation ;
- **IMG** : de vraies photos d'illustration (banques libres, archives), animées dans Remotion par de lents mouvements, avec un même traitement photo (grain, ton chaud). Aucune mention à l'écran.

| | Plans | Temps | Part |
|---|---|---|---|
| 3D | 25 | 165 s | 24 % |
| UI | 29 | 174 s | 25 % |
| MD | 27 | 250 s | 36 % |
| IMG | 12 + 6 vignettes par interlude | 74 s + 18 s d'interludes | ≈ 13 % |
| Noir | 5 | 13 s | 2 % |

- **98 plans** (dont les 6 de l'aveu, S13), plus 3 retours de l'interlude S06 et les grappes d'images : **environ 125 coupes** pour ≈ 11 min. La médiane visée est de 3 à 5 s par plan : entre la réf. 03 (3,3 s) et une vidéo plus contemplative. Les plans longs sont réservés aux graphiques (I03) et à la respiration (M05).
- **Équilibre des matières validé par Bruno (05/11/2026)** : 3D 24 %, UI 26 %, MD 37 %, IMG ≈ 14 %. L'ajout de l'aveu (S13) le modifie à peine (chiffres ci-dessus).

### Motion design à créer (Remotion)

| Élément | Scènes | Base existante |
|---|---|---|
| Interface du simulateur (réglages, fiche, choix, événements, acte de décès, comparaison) | S02-S14 | 🧪 nouveau, le plus gros chantier Remotion |
| Carton d'âge sobre | S04, S07-S09, S11 | ✅ `TerminalChargement`, à décliner |
| Compteur de naissances | S02 | 🧪 simple |
| Curseur 0-100 (la consigne au spectateur) | S02, S16 | 🧪 simple |
| Carte du monde : tirage pondéré des naissances | S04 | 🧪 moyen (données ONU du site) |
| Jauges des conditions de départ | S05 | 🧪 simple |
| Frise d'âge (curseur, événements, icônes) | S06, S09 | 🧪 moyen |
| Barres de probabilité avant et après un choix | S08 | 🧪 simple |
| Graphique de trajectoires (I03), réutilisé en S15 | S10, S15 | 🧪 moyen |
| Mur de 207 pays (I11) | S14 | 🧪 simple (`TexteBrouille` en base) |
| Schéma territoire / nationalité | S14 | 🧪 simple |
| 100 points : tendance contre parcours individuels | S15 | 🧪 moyen |
| Encart « À VOUS » : options + pourcentages figés, compte à rebours de 3 s, puis le clic (S07-S09, S16) ; rafale des écrans de décision pour l'aveu (S13) | S07-S09, S13, S16 | 🧪 simple, à concevoir avec l'interface |
| Portrait en mosaïque par crans (I13) | S05, S08, S09, S11 | ✅ `Mosaique` |
| Unification des photos (I04) : préréglage « photo » (grain fin, ton chaud, vignettage, sans balayage ni aberration) | partout | ✅ `FiltreArchive`, préréglage à créer |
| Animation des photos (Ken Burns lent, recadrage) | partout | 🧪 composant simple à créer |

### Photos à sourcer

Environ **15 photos d'illustration de la vie** (S05, S07, S08, S09, S11, S15), plus **24 vignettes** pour les interludes, plus **1 portrait** (le même du début à la fin, pixelisé puis net) : **≈ 40 photos**. Elles ne peuvent être choisies qu'**après la partie jouée**, puisqu'il faut connaître le pays tiré.

Règles :
- banques libres de droits (Unsplash, Pexels, Pixabay), Wikimedia Commons (attention aux licences CC-BY-SA, qui imposent l'attribution) ou archives ;
- chaque photo est inscrite dans [`references/photos.md`](references/photos.md) (lien, auteur, licence, plan) ;
- crédits en description ;
- personnes de dos ou de loin, sauf le portrait ;
- **le portrait** : vérifier que la licence autorise ce récit (une personne qui « meurt » dans une simulation). Pexels interdit par exemple de montrer une personne identifiable sous un jour négatif ;
- même lumière et même saison autant que possible, pour que la vie paraisse une ; le traitement I04 fait le reste.

## Ce qu'il faut fabriquer

| Élément | État | Coût |
|---|---|---|
| Bureau + opérateur sans visage, lumière qui évolue de l'aube à la nuit | 🧪 Blender | ●●● (le plus gros chantier) |
| Interface du simulateur recréée (réglages, vie, choix, acte de décès, comparaison) | 🧪 Remotion | ●●● |
| Cartons d'âge (T01, version sobre) | ✅ `TerminalChargement`, à décliner | ● |
| Portrait en mosaïque (I13) | ✅ `Mosaique` | ● |
| Unification des photos (I04, préréglage « photo ») | ✅ `FiltreArchive`, préréglage à créer | ● |
| Graphique de trajectoires (I03) | 🧪 Remotion | ●● |
| Mur de 207 pays (I11) | 🧪 Remotion | ● |
| Photos de la vie (lieux, scènes, un portrait) | À sourcer après la partie jouée | Gratuit (banques libres), temps de recherche |

## À faire avant le script

- ✅ **Parties jouées le 06/11/2026** (seed 20261106, moteur 0.9.52) : voir [`references/partie.md`](references/partie.md). Il reste à lancer le script, avec la clé de Bruno, pour obtenir la vie définitive. Il fixe la caste et la religion les plus fréquentes, archive les options et les probabilités de chaque décision, et produit la variante « ambitieuse » :
  `python shared/outils/1in8b/partie.py --seed 20261106 --country IND --sex male --place village --fifth 3 --mesurer faith,caste --sortie videos/2026-11-quelle-aurait-du-etre-ta-vie/prompts/partie`
- Sourcer précisément les chiffres de S14 et S15 (`references/sources.md`).
