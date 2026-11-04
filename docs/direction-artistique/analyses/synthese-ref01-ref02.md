# Synthèse · Réf. 01 (Mareko Scarla) × Réf. 02 (Panoptique)

Ce document **extrait des pistes**, il ne fige pas encore la DA de la chaîne : on la construira quand il y aura plus de références. Analyses détaillées : `ref01-mareko-scarla.md`, `ref02-panoptique.md`.

## Ce que les deux vidéos ont en commun

| Catégorie | Point commun | Importance pour nous |
|---|---|---|
| **Langage visuel** | De la **3D stylisée et symbolique**, pas réaliste : des figurines ou un décor-concept plutôt que des acteurs. Le visuel *représente* au lieu de *montrer*. | ★★★ |
| Personnages | **Sans visage** : mannequins laqués (01), silhouette ou POV (02). Anonymisation, universalité, et pas d'animation faciale à produire. | ★★★ |
| Lumière | **Clair-obscur dur** : fonds sombres ou aplats, une source principale, des ombres nettes, du volumétrique | ★★★ |
| Couleur | **Une couleur-signal** : le rouge = danger ou regard, sur un monde par ailleurs neutre ou froid | ★★★ |
| Surréalisme symbolique | Tableaux classiques géants, crâne doré, champ de fleurs (01) ; œil géant face à une figurine (02) | ★★ |
| Habillage | Overlays de type HUD et surveillance, glitchs, grain | ★★ |
| Voix | Grave, posée, proche du micro | ★★ |
| Sponsor | **Intégré à la DA et au récit**, sans rupture | ★★ |

## Ce qui les oppose, et ce que ça nous apprend

| | Réf. 01 · true crime | Réf. 02 · essai |
|---|---|---|
| Narrateur | Externe, 3e personne, ton journalistique | **Personnage, 1re personne**, ton intime |
| Rapport image/texte | L'image **illustre** le récit | L'image **est** le raisonnement (le trajet = l'argument) |
| Débit | ≈ 178 mots/min, quasi sans silence | Plus lent, **cinq grandes plages sans voix** (jusqu'à 69 s) |
| Moteur de tension | Enquête : qui ? comment ? cliffhangers | Une seule question (« y a-t-il quelqu'un ? ») et des révélations en chaîne |
| Fin | Morale explicite | **Miroir** : le spectateur est concerné |

**Pour une chaîne qui veut « faire réfléchir » en storytelling, la réf. 02 est la plus proche de notre intention** : narrateur impliqué, idée mise en espace, silences, chute en miroir. La réf. 01 apporte la **boîte à outils de production** : figurines codées par couleur, cartes et HUD, voix jouées, datation des scènes, hook monté en rafale.

## Signature, techniques récurrentes, effets ponctuels

1. **Signature visuelle (ce qui se reconnaît immédiatement)** : figurines ou humain minuscule face à un système géant, aplat ou fond sombre, lumière dure, une couleur-signal.
2. **Techniques récurrentes** : POV et travellings lents dans des décors-concepts, cartes et HUD néon, overlays de surveillance, voix grave et intime, sound design illustratif, silence avant les révélations.
3. **Effets ponctuels** : tableau classique géant dans un décor, objet surréaliste (crâne doré, œil géant), rappel d'un motif visuel (serpent, lumière rouge).

## Les 10 techniques les plus intéressantes à retenir

1. **Mettre l'idée en espace** : un lieu parcourable dont chaque étape correspond à une étape de l'argument (02).
2. **Narrateur-personnage** qui vit ce qu'il raconte et finit par se confesser (02).
3. **Personnages sans visage, codés par la couleur du matériau** (01).
4. **Contraste d'échelle** : humain minuscule face à un objet ou un système monumental (02, miniature).
5. **Silence de 20 à 70 s** juste avant une révélation (02).
6. **Plant et payoff visuel** : un détail montré dans le hook, expliqué plus tard (02 : la lumière rouge ; 01 : le serpent).
7. **Hook en rafale** : un mot répété et des cuts d'1 à 2 s, jusqu'au carton titre (01).
8. **Datation et localisation** des scènes (« Mercredi 18 novembre 2020, Marseille ») avec un zoom sur carte (01).
9. **Énumération en compte à rebours** (« cellule par cellule… la dernière ») (02).
10. **Sponsor accroché au récit**, avec un retour par la quête (02).

## Les 5 éléments qui portent le plus l'identité

1. La 3D symbolique et non réaliste.
2. Les personnages sans visage.
3. La lumière dure sur fond sombre ou aplat.
4. La couleur-signal rouge.
5. La voix intime et grave.

## Les 5 techniques les plus faciles à reproduire (avec nos outils)

| Technique | Outil | Effort |
|---|---|---|
| Titres, étiquettes et bulles HUD | Remotion | Faible : composants réutilisables |
| Cartes avec zoom et tracé néon | Remotion | Faible à moyen |
| Overlays de surveillance (REC, CAM, boîtes) | Remotion | Faible |
| Silences et drops de basse | Écriture + mixage | Nul : c'est de l'écriture |
| Plans « humain minuscule face à un objet géant » | Higgsfield (image) ou Blender simple | Faible |

## Les 5 techniques les plus impressionnantes

1. 70 min de figurines animées et jouées (01) : très coûteux à produire.
2. La prison circulaire parcourue en continu (02).
3. L'extérieur monumental : piliers, brume, faisceaux (02).
4. Les décors oniriques avec tableaux classiques (01).
5. La chute en miroir sur le spectateur (02) : impressionnante, et pourtant gratuite.

## Limites observées

- Réf. 01 : saturation verbale ; la question ouverte devient un tic ; violence textuelle éprouvante.
- Réf. 02 : un tunnel de preuves après le climax ; l'esthétique béton et cyan est assez courante.

## Proposition de workflow pour une DA de ce type

1. **Écrire d'abord le lieu-concept** de la vidéo : quel espace incarne l'idée, et quel trajet le traverse ?
2. **Storyboard du trajet** : une fiche scène par étape de l'argument, en notant les silences prévus.
3. **Bibliothèque de figurines** : un ou deux personnages sans visage, déclinés par matériau et couleur (Blender, réutilisables d'une vidéo à l'autre dans `shared/blender/`).
4. **Décors** : Blender pour les espaces parcourus en continu ; Higgsfield pour les plans fixes symboliques et les inserts (avec une image de référence pour garder la cohérence).
5. **Habillage** dans Remotion : composants communs (titre, étiquette, carte, overlay surveillance, visualiseur audio) dans `shared/remotion/`.
6. **Son** : voix intime, nappes, sound design illustratif, silences écrits dans le script.
7. **Étalonnage commun** : grain, vignettage, une couleur-signal. Ce sera à définir dans la DA finale.

## Ce qu'il faudrait pour aller plus loin

- **Des images réelles** : extraction des plans sur le PC, pour mesurer les palettes, la durée des plans et les mouvements. C'est la limite principale des analyses actuelles.
- **D'autres références**, pour distinguer ce qui relève du goût de Bruno de ce qui relève de ces deux vidéos.
