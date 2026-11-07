# S02 · On s'assoit

| | |
|---|---|
| **Durée** | ≈ 0:50 |
| **Fabrication** | Blender (plans 3D, l'écran texturé avec l'interface de S01) + Higgsfield (mouvement) + Remotion (la question) |
| **Fonction** | ACCROCHER |
| **Procédé principal** | N01 : le spectateur note la part de sa vie qu'il pense avoir choisie ; toute la vidéo y répond |
| **Procédés secondaires** | I18, I16 |
| **Statut** | repensée le 07/11/2026 pour le nouveau décor, à valider par Bruno |
| **Production** | V1 avec voix et son (`S02_v1.mp4`, 34 s), à valider par Bruno |

## Intention

**Repensée le 07/11/2026** : le décor n'a plus de fenêtre (bureau seul dans le noir), donc plus d'aube. S02 enchaîne directement sur la fin de S01 : on est derrière la chaise, on s'assoit. On reste en vue subjective : le spectateur est à la place de l'opérateur. L'écran est celui de S01 (les vies simulées, les deux portraits robots, le compteur), ce qui relie la voix (« il en naît à peu près quatre par seconde ») à ce qu'on voit. À la place de l'aube qui monte : la lampe de bureau qu'on allume, un clic, le travail commence.

**La question au spectateur est retirée** (décision de Bruno, 07/11/2026), à l'écran comme dans la voix : la scène se termine sur la silhouette seule dans le noir.

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
- P03 : `compteur.py`.
- P01 et P05 : Higgsfield (prompts et devis dans `../../prompts/S02.md`).
- Montage et son : `montage.py` (voix prise 1 de Guillaume, découpée phrase par phrase et posée sur les plans ; la chaise, un tic par naissance sur le compteur, le clic de la lampe, la pièce qui s'éloigne dans le plan large). Plans : P01 6 s, P02 9 s, P03 7 s, P04 4 s, P05 8 s. Même gain général qu'en S01 : le raccord S01 → S02 est au même niveau.

## Points à revoir
