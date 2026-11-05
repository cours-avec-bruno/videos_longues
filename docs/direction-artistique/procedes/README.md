# Procédés : mode d'emploi

Le [catalogue](catalogue.md) contient des procédés de fabrication extraits des références. Ils ont **tous été validés** par Bruno (tri du 05/11/2026). En avoir beaucoup est une richesse **à condition de s'en servir avec cohérence** : ce document fixe comment on les choisit, combien on en utilise et comment ils s'articulent.

## Les couches

| Couche | Contenu | Usage |
|---|---|---|
| **Couche 1** | Les procédés jugés intéressants (55) | **Proposés d'office** lors du storyboard, quand ils servent la fonction de la scène |
| **Couche 2** | Les procédés jugés moyennement intéressants (3 : N06, N08, N12) | Disponibles, mais **proposés seulement** si une scène en a précisément besoin et qu'aucun procédé de couche 1 ne fait mieux |
| **Écartés** | Les procédés jugés pas intéressants | Supprimés. Listés en fin de catalogue pour ne pas les reproposer après une nouvelle analyse |

## Choisir par fonction, jamais par envie

Chaque procédé sert une ou deux **fonctions narratives**. Au storyboard, on se demande d'abord **ce que la scène doit faire**, puis on cherche les procédés qui servent cette fonction.

| Fonction | La scène doit… | Procédés (couche 1) |
|---|---|---|
| **ACCROCHER** | capter dans les 30 premières secondes | N01, N03, N05, M01, I17, H06 |
| **PROMETTRE** | créer une attente, un manque | N03, N05, N10, I13 |
| **EXPLIQUER** | faire comprendre un mécanisme | N09, I01, I02, I03, I10, I11, M03, H04, H05 |
| **PROUVER** | montrer que c'est vrai | I05, I06, I09, N11 |
| **RESSENTIR** | émouvoir, donner le vertige | I07, I08, I17, I18, M05, S03, S04 |
| **RESPIRER** | laisser décanter | M05, T03, S02, S05 |
| **TRANSITIONNER** | changer de chapitre ou de lieu | T01, T02, T03, T04, T06, M04 |
| **RELIER** | garder la continuité, rappeler | N07, T05, I16, M07, N05 |
| **RÉVÉLER** | faire tomber la vérité, conclure | N02, N14, I12, I15, S01, S06, M06 |
| **HABILLER** | rendre lisible, créditer, informer | H01, H02, H03, H05, I04, I14 |
| **INCARNER** | donner une présence humaine | N04, N15, I07, I13 |
| **STANDARD** | s'applique à toute la vidéo, sans être un choix de scène | M02, S02, S07 |

## Les règles d'usage

1. **Une fonction, puis un procédé.** Chaque scène a une fonction principale. Le procédé est choisi pour elle, et la fiche scène dit **pourquoi** en une phrase.
2. **Un procédé principal par scène**, au plus **deux secondaires**. Au-delà, la scène est surchargée : on la découpe ou on renonce.
3. **Une même forme garde le même sens dans toute la vidéo.** Si le carton terminal (T01) annonce un changement de lieu, il n'annonce jamais autre chose. Si le rose désigne les concepts (I02), il ne sert pas à décorer. C'est ce qui rend l'abondance lisible.
4. **3 à 5 procédés signatures par vidéo.** Ce sont ceux qui reviennent et donnent son identité à la vidéo (un objet-concept, une transition, une palette…). Les autres sont ponctuels.
5. **Les procédés « une fois par vidéo » ne servent qu'une fois** : N01 (jeu-expérience), N02 (twist méta), M06 (climax d'accélération), M07 (bouclage), H06 (carton d'authenticité), N14 (fin en miroir).
6. **Ne pas empiler deux procédés de la même fonction au même endroit.** Exemples : pas de noir (T03), puis un glitch (T02), puis un terminal (T01) à la suite ; pas deux objets-concepts concurrents.
7. **La couche 1 n'est pas une checklist.** Une vidéo utilise en général **15 à 25 procédés**. Ne pas avoir utilisé un procédé n'est pas un manque.
8. **Varier d'une vidéo à l'autre.** Les signatures de la chaîne (voir la grammaire) restent stables, mais les procédés ponctuels tournent, pour éviter les tics. Le bilan de chaque vidéo (fin du storyboard) sert à le vérifier.
9. **Respecter les compatibilités** indiquées dans les fiches (« va avec » et « évite avec »).
10. **Bilan après chaque vidéo** : ce qui a marché, ce qui a gêné, et le catalogue s'ajuste (réglages réels, nouvelles règles).

## La grammaire d'une vidéo

Avant d'écrire les scènes, le storyboard fixe la **grammaire** de la vidéo. Ce sont les choix structurants, à ne décider qu'une fois :

| Élément | Question | Procédés concernés |
|---|---|---|
| Lieu ou objet-concept | Quel espace ou quel objet incarne l'idée ? (un seul principal) | N04, N07, I08 |
| Matières d'image | Quelles matières, et lesquelles pour quel rôle ? (3 au maximum, ex. 3D = vécu, papier = explication, archive = preuve) | I01-I11 |
| Couleur | Une couleur d'accent, et une palette par chapitre | I02, I16, H05 |
| Typographie | Quels registres pour quelles voix ? (2 ou 3 au maximum) | H02 |
| Transition de chapitre | Laquelle est la signature ? (une seule ; les autres restent ponctuelles) | T01, T03, T04 |
| Plants et payoffs | Qu'est-ce qu'on cache ou fait retenir, et où on le révèle | N03, N05, M07, T05 |
| Son | Où sont les silences, les respirations et la fin | S01, M05, S05 |

## Le storyboard

Le processus est détaillé dans la skill `.claude/skills/storyboard-procedes/`. En résumé, Claude :
1. propose la **grammaire** (avec 2 options quand le choix change sensiblement le rendu) ;
2. pour chaque scène, identifie la **fonction**, puis propose **2 ou 3 procédés pertinents** (couche 1 d'abord), en recommande un et justifie le choix ;
3. vérifie les **règles** (budget, procédés uniques, sens constant, pas d'empilement) ;
4. tient le **bilan** des procédés utilisés dans `storyboard.md`.

Bruno arbitre. Les choix finaux sont inscrits dans chaque fiche scène.
