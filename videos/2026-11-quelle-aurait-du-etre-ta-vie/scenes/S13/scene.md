# S13 · L'aveu

| | |
|---|---|
| **Durée** | ≈ 0:50 |
| **Fabrication** | Remotion + Blender |
| **Fonction** | RÉVÉLER |
| **Procédé principal** | N02 : le comportement du spectateur pendant la vidéo (jouer, croire choisir) devient la réponse |
| **Procédés secondaires** | M03 (la rafale des écrans de décision), H02 |
| **Statut** | à valider (ajoutée le 06/11/2026, après la décision de Bruno sur la règle secrète) |

## Intention

Le twist de la vidéo. Depuis S02, le spectateur croit jouer. L'opérateur avoue : **il a toujours pris l'option la plus fréquente, et même la naissance était la plus probable.** La vie qu'on vient de suivre n'a jamais été choisie : c'est celle qu'il « aurait dû » vivre.

Trois idées, dans cet ordre, sans en rajouter :
1. **Rien n'était choisi** : « Pas même son pays : l'Inde, là où naissent le plus de bébés. Un village, comme la plupart. À chaque carrefour, le chemin le plus fréquenté. » La rafale des écrans le prouve. Le paradoxe : même cette vie, la plus probable, ne concerne qu'environ 1 bébé sur 80.
2. **Le bon choix ne suffit pas toujours** : « La seule fois où j'ai choisi comme vous, à 11 ans, ça n'a pas suffi. » Et : « À huit ans, il voulait être ingénieur. »
3. **La nuance, honnête** : les choix comptent (la même naissance, jouée « pour réussir », mène bien plus loin dans le moteur). « Mais presque tout le monde prend le même chemin. Ce n'est pas une interdiction : c'est une pente. »

On est sorti de la simulation (le noir de S12) : la scène est en **serif**, sauf la rafale (archives de la simulation, en monospace). Ton : une confidence, sans effet de surprise appuyé.

## Script / son

- **Voix off** (piste, formule à fixer au script) : « Je vous dois un aveu. Je n'ai rien choisi pour lui. Pas même son pays. À chaque carrefour, j'ai pris le chemin le plus fréquenté. Vous, vous avez essayé de bien choisir. Et vous n'avez pas vu la différence. La seule fois où j'ai choisi comme vous, à onze ans, ça n'a pas suffi. Les choix comptent. Mais presque tout le monde prend le même chemin : ce n'est pas une interdiction, c'est une pente. »
- **Règle d'écriture** : rester exact. On ne dit pas « la vie la plus probable qui soit » (voir « Règle du jeu » dans le storyboard), et on ne prétend pas savoir ce que le spectateur a choisi.
- **Sons / musique** : après le noir, ambiance du bureau seule. La rafale est rythmée par des clics de souris. Une note tenue sur la dernière phrase.

## Découpage en plans

Matières : **3D** Blender · **UI** interface du simulateur recréée (Remotion, monospace) · **MD** motion design / animation Remotion · **IMG** vraie photo (banque libre ou archive, voir `../../references/photos.md`), animée dans Remotion · **NOIR**.

| Plan | Durée | Matière | Contenu | Animation / mouvement | Procédé | Son |
|---|---|---|---|---|---|---|
| S13-P01 | 4 s | MD | « Je vous dois un aveu. » en serif, sur noir | Apparition lente | H02 | Voix |
| S13-P02 | 8 s | 3D | Le bureau la nuit, l'acte de décès encore à l'écran. Voix : « Je n'ai rien choisi pour lui. Pas même son pays. » | Fixe | N02 | Voix, ambiance |
| S13-P03 | 12 s | UI | La rafale : la carte des naissances (S04), puis tous les encarts « À VOUS » de la partie, de plus en plus vite ; sur chacun, l'option cliquée s'allume, et c'est toujours le pourcentage le plus haut | Coupes de plus en plus rapides, la colonne des pourcentages reste à la même place | M03, N02 | Un clic par écran, qui s'accélère |
| S13-P04 | 6 s | MD | « À chaque carrefour, le chemin le plus fréquenté. » En petit, dessous : « même la vie la plus probable ne concerne qu'environ 1 bébé sur 80 » | Apparition | N02 | Voix |
| S13-P05 | 7 s | MD | « La seule fois où j'ai choisi comme vous, à 11 ans, ça n'a pas suffi. » L'encart des 11 ans réapparaît (97 %), puis la ligne « … vous avez dû renoncer » | Fondu de l'encart | N02 | Voix, note tenue |
| S13-P06 | 5 s | UI | « … vous répondiez toujours : ingénieur. » (la ligne de S07) | Texte tapé | | Silence |
| S13-P07 | 8 s | MD | « Les choix comptent. Mais presque tout le monde prend le même chemin. Ce n'est pas une interdiction : c'est une pente. » | Une ligne qui s'incline doucement | | Voix |

## Cadrage et mise en scène

- **Plan(s)** : le bureau en plan fixe et large, pour que l'aveu soit dit « à distance », sans gros plan sur l'opérateur.
- **Angle** : le même que S12, pour que l'aveu sorte de la respiration sans rupture.
- **Mouvement** : quasi aucun ; seule la rafale (P03) est rapide.
- **Rythme / transitions** : entrée depuis le noir de S12 ; sortie vers « Et nous ? » (S14) en serif sur noir.

## Références

- Procédé N02 : réf. 03, à 12:41 (voir le catalogue des procédés).

## Fabrication

- La rafale (P03) se fabrique à partir des **vraies données de la partie** : chaque décision avec ses options et leurs parts observées (`../../prompts/partie/7-vie-la-plus-probable.json`, parts dans `6-parts-decisions.json`). L'interface de décision de S07-S09 et la rafale doivent utiliser **le même composant** : c'est ce qui rend l'indice vérifiable au second visionnage.
- **Option testée** : la même naissance jouée « pour réussir » (politique `ambitious`) réussit beaucoup mieux (professeur, 89 ans). Elle **ne prouve donc pas** que les choix ne servent à rien : elle justifie la phrase « une pente, pas une interdiction ». Si on la montre, il faut d'abord la confirmer sur beaucoup de vies (`/simulate`).

## Points à revoir

- La formule exacte de l'aveu (script).
- Montrer ou non la variante « pour réussir » (un plan de plus, ≈ 8 s, MD), après vérification sur beaucoup de vies.
