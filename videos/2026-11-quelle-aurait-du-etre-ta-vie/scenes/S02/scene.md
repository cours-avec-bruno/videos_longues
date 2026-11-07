# S02 · On s'assoit

| | |
|---|---|
| **Durée** | ≈ 0:50 |
| **Fabrication** | Blender (plans 3D, l'écran texturé avec l'interface de S01) + Higgsfield (mouvement) + Remotion (la question) |
| **Fonction** | ACCROCHER |
| **Procédé principal** | N01 : le spectateur note la part de sa vie qu'il pense avoir choisie ; toute la vidéo y répond |
| **Procédés secondaires** | I18, I16 |
| **Statut** | repensée le 07/11/2026 pour le nouveau décor, à valider par Bruno |
| **Production** | images V1 faites (aperçu muet `S02_apercu_v1.mp4`, 49 s) ; reste la voix (Guillaume) et le son |

## Intention

**Repensée le 07/11/2026** : le décor n'a plus de fenêtre (bureau seul dans le noir), donc plus d'aube. S02 enchaîne directement sur la fin de S01 : on est derrière la chaise, on s'assoit. On reste en vue subjective : le spectateur est à la place de l'opérateur. L'écran est celui de S01 (les vies simulées, les deux portraits robots, le compteur), ce qui relie la voix (« il en naît à peu près quatre par seconde ») à ce qu'on voit. À la place de l'aube qui monte : la lampe de bureau qu'on allume, un clic, le travail commence.

La question au spectateur s'affiche **sans chiffre** (règle : pas de pourcentage à l'écran) : « Quelle part de votre vie avez-vous choisie ? », avec un curseur qui va de « rien » à « tout », hésite, puis reste vide.

Ancienne intention (storyboard) :

L'opérateur sans visage, de dos, face à l'écran ; lumière d'aube froide par la fenêtre. Mission annoncée (« faire vivre quelqu'un, du premier jour au dernier »), puis l'invitation au spectateur : « Vous allez jouer avec moi. À chaque grand choix, choisissez pour lui. » Puis la consigne (chiffre sur 100), affichée en serif.

⚠️ **La règle secrète** (l'opérateur prend toujours l'option la plus probable) n'est **jamais** annoncée ici : elle n'est révélée qu'en S13. L'opérateur ne ment pas pour autant : il ne dit jamais qu'il choisira selon ses préférences.

## Script / son

- **Voix off** : voir `../../script.md`, section S02 (version 1 du 07/11/2026, relue avec humanizer)
- **Sons / musique** :

## Découpage en plans

Matières : **3D** Blender · **UI** interface du simulateur recréée (Remotion, monospace) · **MD** motion design / animation Remotion · **IMG** vraie photo (banque libre ou archive, voir `../../references/photos.md`), animée dans Remotion · **NOIR**.

| Plan | Durée | Matière | Contenu | Animation / mouvement | Son |
|---|---|---|---|---|---|
| S02-P01 | 6 s | 3D | Vue subjective : on tire la chaise et on s'assoit. L'écran grandit et se stabilise devant nous | La caméra descend et avance, puis se pose | Roulettes, assise, tissu |
| S02-P02 | 8 s | 3D | Face à l'écran : les vies simulées, la ligne en cours qui avance. Voix : « On m'a confié quelqu'un… » | Très lent travelling avant | Ronflement de l'ordinateur, voix |
| S02-P03 | 7 s | 3D | Gros plan sur le compteur des vies simulées qui défile. Voix : « …quatre par seconde. Il sera l'un d'eux. » | Fixe, mise au point sur le compteur | Un tic discret par naissance |
| S02-P04 | 4 s | 3D | Notre main allume la lampe de bureau : la lumière chaude s'ajoute à la lumière froide | Fixe | Clic de l'interrupteur |
| S02-P05 | 8 s | 3D | Plan large, du noir : l'îlot de lumière, la chaise désormais occupée par une silhouette de dos. Voix : « Vous allez m'aider… » | Fixe, très lent recul | Voix, la pièce |
| S02-P06 | 12 s | MD | Sur fond noir, en serif : « Quelle part de votre vie avez-vous choisie ? » Un curseur de « rien » à « tout » hésite, puis reste vide | Curseur animé | La pièce seulement |
| S02-P07 | 4 s | MD | « Notez-le. » | Coupe sèche | Silence bref |

## Cadrage et mise en scène

- **Plan(s)** : large, moyen, serré, insert…
- **Angle** : face, plongée, contre-plongée, subjectif…
- **Mouvement** : fixe, travelling, panoramique, zoom…
- **Rythme / transitions** : entrée et sortie de la scène.

## Références

Images, liens, timecodes (déposer les fichiers dans `../../references/`).

## Fabrication

- Images clés : `plans.py` (Blender, ouvre la scène de S01 ; ajoute la lampe qui s'allume, la silhouette assise de dos, une caméra par plan). Silhouette : choix de Bruno (07/11/2026).
- L'écran : même interface que S01 (`../S01/ecran.py`, réutilisable avec `--t0` pour la continuité du compteur, `--image` pour exporter l'image posée sur la dalle dans Blender).
- P03 : `compteur.py`. P06-P07 : `Question.tsx` (Remotion, composition `S02-Question`).
- P01 et P05 : Higgsfield (prompts et devis dans `../../prompts/S02.md`).
- La voix dit encore « sur cent » ; l'écran n'affiche aucun chiffre (curseur de « rien » à « tout »).

## Points à revoir
