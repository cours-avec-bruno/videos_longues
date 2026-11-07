# S13 · L'aveu

| | |
|---|---|
| **Durée** | ≈ 0:50 |
| **Fabrication** | Remotion + Blender |
| **Fonction** | RÉVÉLER |
| **Procédé principal** | N02 : le comportement du spectateur pendant la vidéo (jouer, croire choisir) devient la réponse |
| **Procédés secondaires** | M03 (la rafale des écrans de décision), H02 |
| **Statut** | à valider (ajoutée le 06/11/2026, après la décision de Bruno sur la règle secrète) |
| **Production** | à faire |

## Intention

Le twist de la vidéo. Depuis S02, le spectateur croit jouer. L'opérateur avoue : **il a toujours pris l'option la plus fréquente, et même la naissance était la plus probable.** La vie qu'on vient de suivre n'a jamais été choisie : c'est celle qu'il « aurait dû » vivre.

Trois idées, dans cet ordre, sans en rajouter :
1. **Rien n'était choisi** : « Pas même son pays : l'Inde, là où naissent le plus de bébés. Un village, comme la plupart. À chaque carrefour, le chemin le plus fréquenté. » La rafale des écrans le prouve. Le paradoxe, gardé pour S14 : même cette naissance, la plus probable, ne concerne qu'environ 1 bébé sur 200.
2. **Le bon choix ne suffit pas toujours** : « À onze ans, je crois que j'ai choisi ce que vous auriez choisi : l'école. Il n'y avait pas l'argent. » Puis, à l'écran : « ingénieur ».
3. **La nuance, honnête** : ses choix ont compté (la même naissance, jouée une fois « pour réussir », donne un professeur, avec une part de chance). Et : « Personne ne lui a interdit l'université. En soixante-quinze ans, la question ne lui a pas été posée une seule fois. »

On est sorti de la simulation (le noir de S12) : la scène est en **serif**, sauf la rafale (archives de la simulation, en monospace). Ton : une confidence, sans effet de surprise appuyé.

## Script / son

- **Voix off** : voir `../../script.md`, section S13 (version 1 du 07/11/2026). L'ancienne formule « ce n'est pas une interdiction, c'est une pente » est abandonnée : c'est le tic n° 1 relevé par humanizer, et elle laissait entendre que presque personne ne prend les chemins ambitieux, ce que les données ne montrent pas.
- **Règle d'écriture** : rester exact. On ne dit pas « la vie la plus probable qui soit » (voir « Règle du jeu » dans le storyboard), et on ne prétend pas savoir ce que le spectateur a choisi.
- **Sons / musique** : après le noir, ambiance du bureau seule. La rafale est rythmée par des clics de souris. Une note tenue sur la dernière phrase.

## Découpage en plans

Matières : **3D** Blender · **UI** interface du simulateur recréée (Remotion, monospace) · **MD** motion design / animation Remotion · **IMG** vraie photo (banque libre ou archive, voir `../../references/photos.md`), animée dans Remotion · **NOIR**.

| Plan | Durée | Matière | Contenu | Animation / mouvement | Procédé | Son |
|---|---|---|---|---|---|---|
| S13-P01 | 4 s | MD | « Je vous dois un aveu. » en serif, sur noir | Apparition lente | H02 | Voix |
| S13-P02 | 8 s | 3D | Le bureau la nuit, l'acte de décès encore à l'écran. Voix : « Je n'ai rien choisi pour lui. Pas même son pays. » | Fixe | N02 | Voix, ambiance |
| S13-P03 | 12 s | UI | La rafale : la carte des naissances (S04), puis toutes les décisions de sa vie, de plus en plus vite ; sur chacune, l'option prise s'allume. **Aucun pourcentage à l'écran** (décision de Bruno, 07/11/2026) : c'est la voix qui dit la règle | Coupes de plus en plus rapides | M03, N02 | Un clic par décision, qui s'accélère |
| S13-P04 | 6 s | MD | « L'Inde, un village, un garçon : chaque fois, ce qui arrive le plus souvent. » | Apparition | N02 | Voix |
| S13-P05 | 7 s | MD | « La seule fois où j'ai choisi comme vous, à 11 ans, ça n'a pas suffi. » L'encart des 11 ans réapparaît (97 %), puis la ligne « … vous avez dû renoncer » | Fondu de l'encart | N02 | Voix, note tenue |
| S13-P06 | 5 s | UI | « … vous répondiez toujours : ingénieur. » (la ligne de S07) | Texte tapé | | Silence |
| S13-P07 | 8 s | UI | Les 75 ans de questions défilent en colonne, sans le mot « université » ; puis, tout en bas, la seule ligne où il apparaît (74 ans, le petit-fils) | Défilement lent, la dernière ligne reste | | Voix : « Personne ne lui a interdit l'université… » |

## Cadrage et mise en scène

- **Plan(s)** : le bureau en plan fixe et large, pour que l'aveu soit dit « à distance », sans gros plan sur l'opérateur.
- **Angle** : le même que S12, pour que l'aveu sorte de la respiration sans rupture.
- **Mouvement** : quasi aucun ; seule la rafale (P03) est rapide.
- **Rythme / transitions** : entrée depuis le noir de S12 ; sortie vers « Et nous ? » (S14) en serif sur noir.

## Références

- Procédé N02 : réf. 03, à 12:41 (voir le catalogue des procédés).

## Fabrication

- La rafale (P03) se fabrique à partir des **vraies données de la partie** : chaque décision avec ses options et leurs parts observées (`../../prompts/partie/7-vie-la-plus-probable.json`, parts dans `6-parts-decisions.json`). L'interface de décision de S07-S09 et la rafale doivent utiliser **le même composant** : c'est ce qui rend l'indice vérifiable au second visionnage.
- **Option testée** : la même naissance jouée « pour réussir » (politique `ambitious`) réussit beaucoup mieux (professeur, 89 ans). Elle montre que d'autres chemins existaient. La chance y joue aussi : dans cette partie, l'école n'a pas été refusée faute d'argent. Si on la montre, il faut d'abord la confirmer sur beaucoup de vies (`/simulate`).

## Points à revoir

- La formule exacte de l'aveu (script).
- Montrer ou non la variante « pour réussir » (un plan de plus, ≈ 8 s, MD), après vérification sur beaucoup de vies.
