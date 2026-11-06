# S13 · L'aveu

| | |
|---|---|
| **Durée** | ≈ 0:45 |
| **Fabrication** | Remotion + Blender |
| **Fonction** | RÉVÉLER |
| **Procédé principal** | N02 : le comportement du spectateur pendant la vidéo (jouer, croire choisir) devient la réponse |
| **Procédés secondaires** | M03 (la rafale des écrans de décision), H02 |
| **Statut** | à valider (ajoutée le 06/11/2026, après la décision de Bruno sur la règle secrète) |

## Intention

Le twist de la vidéo. Depuis S02, le spectateur croit jouer : à chaque grande décision, il a choisi dans sa tête, et l'opérateur a cliqué. Ici, l'opérateur avoue qu'il a **toujours pris l'option la plus probable**. La vie qu'on vient de suivre n'a jamais été choisie : c'est celle qu'elle « aurait dû » vivre. Et personne n'a vu la différence.

On est sorti de la simulation (le noir de S12) : la scène est en **serif**, sauf la rafale des écrans, qui sont des archives de la simulation (monospace).

Ton : un aveu calme, presque une confidence, sans effet de surprise appuyé. Pas de musique dramatique. L'aveu doit tenir en deux ou trois phrases (N02 : « éviter s'il faut l'expliquer longuement »).

Il prépare la bascule vers le réel : si les choix de cette vie pesaient si peu, qu'en est-il des nôtres ? → S14 (naître en France), S15 (le déterminisme social).

## Script / son

- **Voix off** (piste, formule à fixer au script) : « Je vous dois un aveu. Je n'ai rien choisi pour elle. À chaque carrefour, j'ai pris le chemin le plus fréquenté. Vous, vous avez essayé de bien choisir. Et vous n'avez pas vu la différence. »
- **Règle d'écriture** : rester exact. On ne dit pas « la vie la plus probable qui soit » (voir « Règle du jeu » dans le storyboard), et on ne prétend pas savoir ce que le spectateur a choisi.
- **Sons / musique** : après le noir, ambiance du bureau seule. La rafale est rythmée par des clics de souris. Une note tenue sur la dernière phrase.

## Découpage en plans

Matières : **3D** Blender · **UI** interface du simulateur recréée (Remotion, monospace) · **MD** motion design / animation Remotion · **IMG** vraie photo (banque libre ou archive, voir `../../references/photos.md`), animée dans Remotion · **NOIR**.

| Plan | Durée | Matière | Contenu | Animation / mouvement | Procédé | Son |
|---|---|---|---|---|---|---|
| S13-P01 | 4 s | MD | « Je vous dois un aveu. » en serif, sur noir | Apparition lente | H02 | Voix |
| S13-P02 | 8 s | 3D | Le bureau la nuit, l'acte de décès encore à l'écran. L'opérateur ne bouge pas. Voix : « Je n'ai rien choisi pour elle. » | Fixe | N02 | Voix, ambiance |
| S13-P03 | 12 s | UI | La rafale : tous les écrans de décision de la partie défilent, de plus en plus vite. Sur chacun, l'option cliquée s'allume, et c'est toujours le pourcentage le plus haut | Coupes de plus en plus rapides, la colonne des pourcentages reste à la même place d'un écran à l'autre | M03, N02 | Un clic par écran, qui s'accélère |
| S13-P04 | 6 s | MD | « À chaque carrefour, le chemin le plus fréquenté. » en serif | Apparition | N02 | Voix |
| S13-P05 | 8 s | MD | « Vous, vous avez essayé de bien choisir. » Le dernier encart « À VOUS » de la partie réapparaît, vide, puis s'éteint | Fondu de l'encart | N02 | Voix, note tenue |
| S13-P06 | 7 s | 3D | Plan large du bureau, la nuit. Voix : « Et vous n'avez pas vu la différence. » | Très lent travelling arrière |  | Voix, puis silence |

## Cadrage et mise en scène

- **Plan(s)** : le bureau en plan fixe et large, pour que l'aveu soit dit « à distance », sans gros plan sur l'opérateur.
- **Angle** : le même que S12, pour que l'aveu sorte de la respiration sans rupture.
- **Mouvement** : quasi aucun ; seule la rafale (P03) est rapide.
- **Rythme / transitions** : entrée depuis le noir de S12 ; sortie vers « Et nous ? » (S14) en serif sur noir.

## Références

- Procédé N02 : réf. 03, à 12:41 (voir le catalogue des procédés).

## Fabrication

- La rafale (P03) se fabrique à partir des **vraies données de la partie** : chaque décision avec ses options et leurs probabilités (API `/api/v1/live`, archivée dans `../../prompts/`). L'interface de décision de S07-S09 et la rafale doivent utiliser **le même composant** : c'est ce qui rend l'indice vérifiable au second visionnage.
- **Option à tester** : rejouer la même seed avec les options « pour réussir » et montrer en une image l'écart entre les deux vies. À n'utiliser que si les données montrent vraiment un écart faible (hypothèse non vérifiée).

## Points à revoir

- La formule exacte de l'aveu (script).
- Si l'option « rejouer pour réussir » est retenue, il faudra un plan de plus (≈ 8 s, MD).
