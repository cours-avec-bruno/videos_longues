# Storyboard · Quelle aurait dû être ta vie ?

Vue d'ensemble : une ligne par scène, le détail dans chaque fiche scène.
Procédés choisis avec le [mode d'emploi](../../docs/direction-artistique/procedes/README.md) et le [catalogue](../../docs/direction-artistique/procedes/catalogue.md). Faits : [`references/sources.md`](references/sources.md).

**Statut** : proposition de Claude (05/11/2026), à arbitrer par Bruno. Pour chaque scène : le procédé recommandé, et une alternative.

## Décisions déjà prises par Bruno

- **Rien n'est filmé** : Blender pour le bureau et l'opérateur, Remotion pour l'interface, le motion design et le montage.
- **Voix off** : l'opérateur, à la première personne.
- **Images de la vie** : de **vraies photos** d'illustration (banques libres de droits, archives), retravaillées dans Remotion.
- **La vidéo ne doit jamais être reconnaissable comme faite à l'IA** : aucune mention d'IA à l'écran, et les règles anti-« look IA » ci-dessous s'appliquent à toute la fabrication.
- **Priorité à l'animation** : on privilégie les moments d'animation, de motion design et de 3D. Les photos restent un **complément**, pas la matière principale. À appliquer en affinant le découpage : quand un plan peut être raconté en motion design ou en 3D plutôt qu'en photo, on choisit l'animation.

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

Contraintes du concept : pas de twist « simulation dans la simulation », pas d'effets futuristes ni de glitchs démonstratifs (donc **pas de T02**), l'opérateur reste au service du récit.

## Grammaire de la vidéo

| Élément | Choix | Procédés |
|---|---|---|
| Lieu principal | **Le bureau** : huis clos sobre, froid, presque administratif. C'est le seul lieu de la vidéo ; pas d'objet-concept concurrent | (pas de N04 ni de N07) |
| Matières d'image (3) | **3D Blender** = le cadre (le bureau, l'opérateur) · **Remotion** = la machine et les données (interface, cartons, graphiques) · **vraies photos** = la vie humaine simulée | I04 |
| Couleur d'accent | **Ambre chaud**, réservé à **l'humain** : la vie simulée, l'âge, le portrait. Tout le reste est froid (gris-bleu, blanc d'écran). C'est le contraste voulu par le concept : un cadre froid face à une vie humaine | — |
| Palette par chapitre | Huis clos, donc **une lumière qui évolue** : la lumière du bureau suit l'âge de la vie simulée. Aube à la naissance, plein jour à l'âge adulte, crépuscule dans la vieillesse, nuit à la mort, puis **aube de nouveau** au bouclage | I16, I18 |
| Registres typographiques (2) | **Monospace = dans la simulation** (interface, cartons d'âge, données du simulateur) · **Serif = hors de la simulation** (le monde réel, la France, la narration à l'écran, le titre) | H02 |
| Transition signature | **Le carton d'âge** (T01, version sobre : sans glitch, une barre et un âge). Il signifie toujours « la vie simulée avance d'une étape ». Une seule autre transition : le **noir** (T03), qui signifie toujours « on sort de la simulation » | T01, T03 |
| Plants → payoffs | (1) Le spectateur note un chiffre (S02) → on le lui redemande (S15) · (2) L'opérateur saisit son vrai lieu de naissance, la France (S03) → la comparaison avec lui-même (S13) · (3) Le portrait en mosaïque (S05) → net à la mort (S11) : **une seule vraie photo**, pixelisée dès le départ ; on ne découvre qui était cette personne qu'à la fin · (4) Le bureau à l'aube (S02) → l'aube de nouveau (S15) | N01, N05, I13, M07 |
| Son | Clavier et ambiance du bureau au début · musique discrète pendant la simulation · **3 silences d'une seconde** (le pays, la mort, « 1 sur 207 ») · une respiration après la mort · fin musicale | S01, M05, S05, S02 |
| **Signatures (5)** | **T01** cartons d'âge · **I13** le visage qui se précise · **I16 + I18** la lumière du bureau qui suit la vie · **M04** les années qui défilent · **N05** le vrai lieu de naissance | |

## Scènes

| ID | Partie | Ce qui se passe | Fonction | Procédé principal | Secondaires | Alternative au principal | Durée ≈ | Fabrication |
|---|---|---|---|---|---|---|---|---|
| S01 | Ouverture | Carton : « Cette vie est simulée par *1 sur 8 milliards* (1in8b.life) à partir de statistiques réelles. » | ACCROCHER | **H06** : contrat de confiance. Il pose d'emblée que la **vie** est simulée (ce que demande le concept), sans parler des outils de fabrication | — | (aucune : c'est une mention honnête nécessaire) | 0:06 | Remotion |
| S02 | Le bureau, à l'aube | L'opérateur de dos, l'écran allumé, la lumière d'aube. « On m'a confié une mission. » Puis, au spectateur : « Avant que je commence, notez un chiffre : sur 100, quelle part de votre vie avez-vous choisie ? » | ACCROCHER | **N01** : le spectateur s'engage avec une estimation, et toute la vidéo y répond | I18, I16 | N03 (montrer l'acte de décès flouté : « voilà comment cette vie finira ») | 0:50 | Blender + Remotion |
| S03 | La mission | L'interface : le monde d'aujourd'hui, le tirage selon les naissances. L'opérateur saisit son vrai lieu de naissance, la France. « Gardez ça en tête, on y reviendra. » | PROMETTRE | **N05** : le plant le plus utile de la vidéo, car le site permet vraiment la comparaison avec sa propre vie | H02 | N03 | 0:35 | Remotion (interface) + Blender |
| S04 | Naître | Le bouton « Naître », le premier carton **0 AN**, une seconde de silence, puis le pays et la ville seuls à l'écran | RÉVÉLER | **T01** : sa première apparition fixe son sens (une étape d'âge) | S01, I15 | I15 en principal (le pays seul, en grand) | 0:20 | Remotion |
| S05 | Les conditions de départ | La famille, ses moyens, le lieu. « Je n'ai rien choisi de tout ça. Elle non plus. » Le portrait apparaît en très gros pixels | INCARNER | **I13** : la personne n'existe encore presque pas. Chaque étape ajoutera un cran de netteté | I04 | I04 en principal (les photos du lieu) | 0:40 | Photos + Remotion |
| S06 | Les années qui passent | Une année ≈ une seconde ; le compteur d'âge ; la lumière du bureau qui monte. Revient en interlude entre chaque étape | TRANSITIONNER | **M04** : le temps qui passe devient un rythme, et le site fonctionne vraiment ainsi (environ une année par minute, accélérée) | I16 | T03 (noir entre les étapes : non, ce noir est réservé à la sortie) | 0:15 (×4) | Remotion + Blender |
| S07 | 5 ans · l'enfance | Carton 5 ANS, la question du site. L'enfance en vraies photos du pays (des enfants de dos ou de loin, jamais un visage identifiable) | INCARNER | **I04** : les photos, d'origines variées, sont unifiées en une seule matière chaude, distincte du bureau froid | T01 | M03 (une grappe d'images courtes) | 0:50 | Photos + Remotion |
| S08 | 15 ans · le premier choix | L'opérateur choisit (les études). Le site prévient que le choix change des probabilités, pas le résultat. Il réagit, doute | INCARNER | **N15** : la réaction spontanée de l'opérateur rend le choix humain | T01, I13 (un cran de netteté) | N11 (la nuance du site, citée à l'écran) | 0:50 | Blender + Remotion |
| S09 | 30 et 50 ans · la vie adulte | Travail, relations, ce qui arrive sans qu'on l'ait choisi. Trois ou quatre événements seulement | RESSENTIR | **M03** : de courtes grappes d'images sur les événements, entre deux temps d'interface | T01, I13 | I04 (des plans plus longs, plus contemplatifs) | 1:00 | Photos + Remotion |
| S10 | Les autres trajectoires | Les 4 autres bébés nés à la même seconde. Leurs vies se dessinent sur la même frise d'âge. « Une trajectoire probable n'est pas un destin » | EXPLIQUER | **I03** : un seul plan où les 5 trajectoires se construisent ensemble, et où l'on voit à la fois les écarts et les ressemblances | N11 | I05 (la vraie phrase du site, en source primaire) | 1:15 | Remotion |
| S11 | La fin de la vie | Le dernier carton (l'âge du décès), une seconde de silence, l'acte de décès. Le portrait (la même vraie photo, pixelisée depuis S05) est enfin net | RÉVÉLER | **I13** (payoff) : on ne connaît vraiment quelqu'un qu'à la fin | T01, S01 | N03 en amont (acte de décès flouté dès S02) | 0:40 | Remotion + photo |
| S12 | Respiration | La nuit dans le bureau. L'écran affiche l'acte de décès, l'opérateur ne bouge plus. 15 s sans voix, puis une coupe au noir | RESPIRER | **M05** : laisser décanter, comme le demande le concept | T03 | S05 (musique seule, sans image nouvelle) | 0:20 | Blender |
| S13 | Et nous ? Naître en France | On ressort de la simulation (serif). Le payoff du lieu saisi au début : un mur de 207 noms de pays tirés au sort, où la France n'apparaît qu'une fois. Silence. « 1 sur 207. » Puis la distinction entre naître en France et être Français, et la source | RÉVÉLER | **I11** : 1 chance sur 207 devient visible et physique | S01, I15 | I15 seul (le chiffre en grand, sans le mur) | 1:00 | Remotion |
| S14 | Le déterminisme social en France | Même en France, les départs diffèrent : le diplôme selon l'origine sociale (Insee), un graphique qui se construit, la page source. « Une tendance n'est pas un destin » | PROUVER | **I03** : même forme, même sens qu'en S10 (comparer des trajectoires) | I05, N11 | I05 en principal (la page Insee seule) | 1:10 | Remotion |
| S15 | Conclusion | Retour au bureau, à l'aube. L'écran propose de nouveau « Naître ». « Et votre chiffre du début, il a bougé ? » Puis : « Quelle aurait dû être ta vie ? » Musique seule | RÉVÉLER | **N14** : la question rendue au spectateur | M07, S05 | N12 (couche 2 : l'opérateur avoue qu'il croyait avoir tout choisi). À ne prendre que si la confession est sincère | 0:40 | Blender + Remotion |

**Durée totale estimée** : ≈ 10 min 30 (à resserrer au script).

## Arc narratif

1. **Contrôle** (S01-S04) : l'opérateur croit maîtriser la simulation ; on installe le jeu et les deux plants.
2. **Glissement** (S05-S09) : la vie avance, les choix existent mais pèsent peu face au point de départ. La lumière monte, puis décline.
3. **Recul** (S10) : les autres trajectoires montrent la part du hasard et celle des statistiques, sans fatalisme.
4. **Fin et silence** (S11-S12) : la mort, le portrait net, la respiration, le noir.
5. **Retournement** (S13-S14) : on sort de la simulation ; la question devient la nôtre, en France.
6. **Ouverture** (S15) : le bouclage à l'aube, le chiffre du spectateur, la question finale.

## Bilan des procédés

| Procédé | Scènes | Rôle dans cette vidéo (sens constant) |
|---|---|---|
| T01 | S04, S07, S08, S09, S11 | Carton d'âge : la vie simulée avance d'une étape (calé sur les arrêts du site à 5, 15, 30, 50, 70 ans) |
| I13 | S05, S08, S09, S11 | Le visage de la personne se précise à mesure qu'on la connaît |
| I16 + I18 | S02, S06, S12, S15 | La lumière du bureau suit l'âge de la vie simulée |
| M04 | S06 | Le temps qui passe (une année ≈ une seconde) |
| N05 | S03 → S13 | Le vrai lieu de naissance, saisi puis comparé |
| N01 | S02 → S15 | Le chiffre du spectateur |
| I04 | S05, S07, S09, S11, S14 | La vie en vraies photos, unifiées par un même traitement photo |
| H01 | S13 | La source des données à l'écran |
| I03 | S10, S14 | Comparer des trajectoires (dans la simulation, puis en France) |
| S01 | S04, S11, S13 | Silence avant le pays, la mort, « 1 sur 207 » |
| I15 | S04, S13 | Le lieu ou le chiffre seul à l'écran |
| N11 | S10, S14 | Probabilité ≠ destin |
| H02 | partout | Mono = dans la simulation · serif = hors de la simulation |
| H06, N15, M03, M05, T03, I11, I05, N14, M07, S05 | une fois chacun | Voir les scènes |
| M02, S02, S07 | partout | Standards |

- **Nombre de procédés différents** : 24, hors standards (cible : 15 à 25) ✅
- **Procédés « une fois par vidéo »** : N01, H06, N14, M07, chacun utilisé une seule fois ✅
- **Couche 2** : aucune. N12 est proposée seulement comme alternative en S15.
- **Écartés ou exclus par le concept** : N13 (écarté), T02 (pas de glitch), N02 (pas de twist : le concept l'exclut).

## Découpage en plans : vue d'ensemble

**Une scène n'est pas un plan.** Chaque fiche scène contient son découpage plan par plan (identifiants `S05-P03`…) : durée, matière, contenu, animation, procédé, son.

Les quatre matières de plan, toutes fabriquées. Elles restent dans les 3 matières de la grammaire, car UI et MD sont deux usages de Remotion :
- **3D** : Blender (le bureau, l'opérateur) ;
- **UI** : l'interface du simulateur recréée (Remotion, monospace) ;
- **MD** : le motion design et les animations Remotion (cartes, jauges, frises, graphiques, textes) : en monospace dans la simulation, en serif hors de la simulation ;
- **IMG** : de vraies photos d'illustration (banques libres, archives), animées dans Remotion par de lents mouvements, avec un même traitement photo (grain, ton chaud). Aucune mention à l'écran.

| | Plans | Temps | Part |
|---|---|---|---|
| 3D | 23 | 150 s | 24 % |
| UI | 28 | 162 s | 26 % |
| MD | 24 | 232 s | 37 % |
| IMG | 12 + 6 vignettes par interlude | 74 s + 18 s d'interludes | ≈ 14 % |
| Noir | 5 | 13 s | 2 % |

- **92 plans**, plus 3 retours de l'interlude S06 et les grappes d'images : **environ 125 coupes** pour ≈ 11 min. La médiane visée est de 3 à 5 s par plan : entre la réf. 03 (3,3 s) et une vidéo plus contemplative. Les plans longs sont réservés aux graphiques (I03) et à la respiration (M05).
- **Équilibre des matières validé par Bruno (05/11/2026)** : on garde la répartition ci-dessus (3D 24 %, UI 26 %, MD 37 %, IMG ≈ 14 %).

### Motion design à créer (Remotion)

| Élément | Scènes | Base existante |
|---|---|---|
| Interface du simulateur (réglages, fiche, choix, événements, acte de décès, comparaison) | S02-S13 | 🧪 nouveau, le plus gros chantier Remotion |
| Carton d'âge sobre | S04, S07-S09, S11 | ✅ `TerminalChargement`, à décliner |
| Compteur de naissances | S02 | 🧪 simple |
| Curseur 0-100 (la consigne au spectateur) | S02, S15 | 🧪 simple |
| Carte du monde : tirage pondéré des naissances | S04 | 🧪 moyen (données ONU du site) |
| Jauges des conditions de départ | S05 | 🧪 simple |
| Frise d'âge (curseur, événements, icônes) | S06, S09 | 🧪 moyen |
| Barres de probabilité avant et après un choix | S08 | 🧪 simple |
| Graphique de trajectoires (I03), réutilisé en S14 | S10, S14 | 🧪 moyen |
| Mur de 207 pays (I11) | S13 | 🧪 simple (`TexteBrouille` en base) |
| Schéma territoire / nationalité | S13 | 🧪 simple |
| 100 points : tendance contre parcours individuels | S14 | 🧪 moyen |
| Portrait en mosaïque par crans (I13) | S05, S08, S09, S11 | ✅ `Mosaique` |
| Unification des photos (I04) : préréglage « photo » (grain fin, ton chaud, vignettage, sans balayage ni aberration) | partout | ✅ `FiltreArchive`, préréglage à créer |
| Animation des photos (Ken Burns lent, recadrage) | partout | 🧪 composant simple à créer |

### Photos à sourcer

Environ **15 photos d'illustration de la vie** (S05, S07, S08, S09, S11, S14), plus **24 vignettes** pour les interludes, plus **1 portrait** (le même du début à la fin, pixelisé puis net) : **≈ 40 photos**. Elles ne peuvent être choisies qu'**après la partie jouée**, puisqu'il faut connaître le pays tiré.

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

- **Jouer une vraie vie sur 1in8b.life** (mode 1 h, avec la France comme vrai lieu de naissance) et noter : le pays tiré, la famille, les questions à 5, 15, 30, 50 et 70 ans, les choix proposés, l'acte de décès, l'écran de comparaison, les 4 autres bébés (même pays ou pas ?). C'est la matière de l'interface et du récit.
- Sourcer précisément les chiffres de S13 et S14 (`references/sources.md`).
