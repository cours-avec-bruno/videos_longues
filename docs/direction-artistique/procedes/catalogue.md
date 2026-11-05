# Catalogue des procédés

Les procédés de fabrication extraits des références, rendus **réutilisables**. Ce ne sont pas des choses à copier : ce sont des mécanismes (narratifs, visuels, sonores, de montage) avec leur recette dans nos outils.

- **Sources** : réf. 01 (true crime en figurines), réf. 02 (Panoptique), réf. 03 (Paradoxe de l'intelligence, CroustiJu), réf. 04 (Bibliothèque de Babel, ASTRE). Analyses dans `../analyses/`.
- **Utilisation** : dans chaque fiche scène, la ligne **Procédés** cite les identifiants utilisés (ex. `N05, I12, T01`). On voit ainsi ce qui marche, ce qui revient trop, et ce qui manque.
- **Effort** : ● faible (moins d'une heure, composant prêt) · ●● moyen (une demi-journée) · ●●● fort (plusieurs jours ou de la 3D lourde).
- **État** : ✅ composant prêt dans `shared/` · 🧪 à prototyper · 📝 de l'écriture (aucun outil nécessaire).

Ce catalogue est vivant : chaque nouvelle référence l'enrichit, et chaque procédé testé dans une vidéo reçoit ses réglages réels.

---

## N · Écriture et narration

| ID | Procédé | Vu dans | Effet recherché | Recette | Effort | État |
|---|---|---|---|---|---|---|
| N01 | **Jeu-expérience fait sur le spectateur** | 03 (0:00-1:15, résolu à 11:41) | Le spectateur vit le phénomène avant qu'on le lui explique | Une consigne simple (choisir, fermer les yeux, compter, retenir) ; la manipulation est faite à l'image (amorçage par alternance rapide, voir M01) ; la résolution arrive ≥ 8 min plus tard | ●● | 📝 + M01 |
| N02 | **Troisième groupe / twist méta** | 03 (12:41) | Retourner la conclusion sur le spectateur : son comportement pendant la vidéo était la réponse | Prévoir dès l'écriture un comportement « hors consigne » (ceux qui n'ont pas obéi, qui ont mis pause, qui ont douté) et en faire la chute | ● | 📝 |
| N03 | **Promesse différée visible** | 03 (graphe flouté à 1:57, révélé à 5:47) | Suspense explicite : on montre qu'on cache quelque chose | Montrer l'objet de la révélation flouté, pixelisé ou de dos, et dire « je vous le cache » | ● | ✅ `Mosaique` |
| N04 | **Narrateur-guide d'une visite** | 02, 04 (« vous me suivez, ne touchez à rien ») | L'exposé devient un déplacement : chaque idée a son lieu | Écrire le **lieu-concept** avant le script : une salle = une étape de l'argument. Consignes au spectateur, verbes de mouvement | ●●● (décors) | 📝 + I08 |
| N05 | **Consigne de mémoire** | 04 (« gardez cette image », « gardez ça pour la fin ») | Le spectateur guette le payoff, l'attention remonte | Dire explicitement ce qu'il faut retenir, puis le rappeler mot pour mot au moment du payoff | ● | 📝 |
| N06 | **Refrain retourné** | 04 (« tout est déjà écrit » ×4, puis « c'est à nous de le dire ») | Une phrase-marteau qui change de sens à la fin | 3 à 5 occurrences espacées ; la dernière est complétée ou inversée | ● | 📝 |
| N07 | **Objet-concept à face cachée** | 03 (cube aux faces nommées, la 6e révélée au dernier plan), 04 (cube doré = « livre parfait ») | L'idée abstraite devient un objet unique, lumineux, mémorable | Un solide simple (cube, sphère, monolithe), toujours en lente rotation et toujours éclairé de la même façon. Une propriété reste cachée jusqu'à la fin | ●● (Blender) | 🧪 |
| N08 | **Pictogramme-personnage** | 03 (explorateur 🪖 contre avocat ⚖️, 6 retours) | Une métaphore qui revient sans réexplication | 2 pictos opposés, mêmes couleurs à chaque retour, avec un attribut visuel qui change selon la situation (la flèche preuves → conclusion) | ● | 🧪 |
| N09 | **Fausses pistes dessinées** | 03 (lignes parallèles, puis convergence, puis la vraie courbe) | Le spectateur parie, se trompe, retient | Animer les hypothèses naïves *avant* la réponse, puis les effacer | ●● | 🧪 (graphique animé) |
| N10 | **Interdiction qui donne envie** | 04 (« ne calculez pas… tant pis, on calcule ») | Humour, et transition vers une partie technique | Annoncer qu'on ne fera pas X, puis le faire | ● | 📝 |
| N11 | **Nuance assumée** | 03 (OSI contestable), 04 (« c'est un débat… ») | Crédibilité : on n'enjolive pas la science | Une phrase « ce n'est pas tranché », puis montrer que la thèse tient dans les deux cas | ● | 📝 |
| N12 | **Confession / revirement du narrateur** | 03 (« je me suis trompé »), 02 (le gardien, c'était moi) | Le narrateur change devant nous : la thèse est incarnée | Avant la fin, le narrateur applique la thèse à lui-même | ● | 📝 |
| N13 | **Sponsor tissé dans la métaphore** | 02, 04 (adresse ↔ hébergeur) | Pas de rupture : le sponsor prolonge l'image du récit | Trouver le mot-pivot commun (adresse, surveillance, organisation…). Habillage dans la DA de la vidéo | ●● | 📝 + H03 |
| N14 | **Fin en miroir** | 02, 03, 04 | Le spectateur est le dernier sujet de la vidéo | La dernière phrase lui rend la question (« vous êtes la tour », « c'est à nous de le dire ») | ● | 📝 |
| N15 | **Apartés humains** | 04 (« ouais, j'avais besoin d'air ») | Casser la solennité, donner de la présence | Garder 2 ou 3 réactions spontanées à l'enregistrement, ne pas tout lisser | ● | 📝 |

## I · Image

| ID | Procédé | Vu dans | Effet | Recette | Effort | État |
|---|---|---|---|---|---|---|
| I01 | **Tableau noir vivant** | 03 | Le fond explicatif n'est jamais figé | Aplat sombre + poussière de pixels qui dérive et scintille | ● | ✅ `FondPoussiere` |
| I02 | **Pictos pixel art + accent unique** | 03 (rose / magenta sur gris) | Une identité graphique simple, économique et cohérente | Bibliothèque d'icônes pixel art (Remotion SVG ou sprites), **une** couleur d'accent, titres sans-serif grasse avec halo | ●● | 🧪 |
| I03 | **Graphique construit en un seul plan** | 03 (84 s, P053) | L'explication dure sans couper : c'est l'animation qui relance | Axes, puis hypothèses, puis vraie courbe, puis mise en évidence, au rythme de la voix (timings depuis la transcription mot à mot) | ●● | 🧪 |
| I04 | **Unifier des sources hétérogènes** | 03 (40 extraits) | Toutes les sources se lisent comme une seule matière, et le crédit est réglé | Lignes de balayage, aberration chromatique, coins bombés, teinte commune, source en bas à gauche. ⚠️ **Matière** : plans générés, domaine public, nos rendus plutôt que des films sous droits | ● | ✅ `FiltreArchive` |
| I05 | **La source primaire à l'écran** | 03 (pages d'études), 04 (texte de Borges) | Preuve, sérieux, « on n'invente pas » | Page en perspective sur fond noir, faible profondeur de champ (on lit seulement le passage utile), léger travelling | ●● | 🧪 |
| I06 | **Archive brute = registre preuve** | 03 (JT 2004), 04 (Borges RTS) | Rupture de texture qui dit « ceci est réel » | Format d'origine (4:3, noir et blanc), logo conservé, pas de filtre « joli » | ● | 📝 (sourcing) |
| I07 | **Figurines sans visage sur un plateau** | 01, 03 | Personnages universels, codés par couleur, sans animation faciale | Blender : figurines basse définition (ou voxel), plateau, **un seul spot**, fond noir, sol texturé | ●●● (première fois), puis ● | 🧪 `shared/blender/` |
| I08 | **Architecture de papier construite** | 04 (Cénotaphe de Newton de Boullée [HYP]) | Un lieu réel et vertigineux, jamais bâti : légitime et inédit | Choisir une architecture utopique documentée (Boullée, Ledoux, Piranèse, Lequeu…), la modéliser, intercaler ses gravures d'origine 1 s chacune (I09) | ●●● | 🧪 |
| I09 | **Dessin ↔ modèle** | 04 (gravures entre les plans 3D) | Authentifie le décor et crée un vertige « ça existe vraiment » | Plans d'archive de 0,9 à 1 s en coupe franche au milieu d'un mouvement de caméra 3D | ● | 📝 (sourcing : Gallica, Wikimedia) |
| I10 | **Schéma isométrique en style gravure** | 04 (hexagones sur papier) | L'explication reste dans l'univers de la vidéo | Fond papier vignetté, trait noir isométrique, pavage par répétition, typo serif espacée | ●● | 🧪 |
| I11 | **Texture de texte plein cadre** | 04 (charabia, « 25x », « sens ») | Rendre une quantité ou un concept palpable | Mur de texte répété, faible profondeur de champ, page courbe, lent travelling | ● | 🧪 (+ `TexteBrouille`) |
| I12 | **Le « faux parfait »** | 04 (Curie : « mourut » devient « naquit ») | Montrer qu'un détail change tout, sans le dire | Deux plans identiques ; un seul mot diffère ; coupe franche ; ne pas le souligner | ● | 📝 |
| I13 | **Mosaïque d'anonymat / de révélation** | 03 | Un humain présent mais anonyme, ou une révélation par crans | Pixelisation par crans | ● | ✅ `Mosaique` |
| I14 | **Easter egg chiffré** | 03 (César +3 : « Merci d'être curieux ») | Récompense ceux qui mettent pause, et prolonge la thèse | Texte chiffré lisible seulement en pause ; ne jamais le résoudre dans la vidéo | ● | 📝 |
| I15 | **Mot seul à l'écran** | 04 (« vraisemblable », « tout est déjà écrit ») | Graver le mot-clé | Un mot, petit, au centre, sur noir ou blanc, 3 s, avec un fondu de sortie lent | ● | ✅ (`TexteRevele`) |
| I16 | **Une palette par lieu / chapitre** | 04 (cyan, or, bougie, marbre) | Le spectateur sait où il est sans titre | Définir 4 ou 5 ambiances avant la production ; les contrôler au barcode de l'outil d'analyse | ●● | 📝 + mesure |
| I17 | **Échelle « fourmi »** | 02, 04 | Écrasement, vertige | Humain minuscule ou caméra au ras du sol face à un objet monumental ; contre-plongée ; brouillard | ●● | 🧪 |
| I18 | **Lumière unique et motivée** | 01, 02, 03, 04 | Lisibilité et dramaturgie | Une source par plan (spot, oculus, bougies, éclairs), du volumétrique, des fonds qui tombent au noir | ●● | 📝 (Blender) |

## M · Montage et rythme

| ID | Procédé | Vu dans | Effet | Recette | Effort | État |
|---|---|---|---|---|---|---|
| M01 | **Alternance A/B rapide (amorçage)** | 03 (0,3 s, 10 coupes en 10 s) | Faire voir sans montrer | Alterner 2 images toutes les 7 images (24 i/s), pendant 3 à 5 s | ● | 🧪 |
| M02 | **Couper sur le mot** | 03 (94 % des coupes sur une attaque) | Fluidité « parlée », énergie | Placer les coupes sur les attaques de syllabes. Calcul automatique possible depuis la transcription mot à mot | ●● | 🧪 (outil) |
| M03 | **Deux régimes** | 03 | Le long explicatif (20-80 s) alterne avec des grappes d'images de 2-4 s | Écrire la vidéo en « blocs explicatifs » et « respirations d'images » | 📝 | 📝 |
| M04 | **Coupes métronomiques** | 04 (séries de plans de 1,0 s pile) | Mouvement, compte à rebours, déplacement | Plans de durée identique calés sur le tempo de la musique (ex. 60 BPM = 24 images) | ● | 🧪 |
| M05 | **Longue respiration sur une révélation de lieu** | 02 (jusqu'à 69 s), 04 (30 s, 18 s, 15 s) | Laisser regarder ; la musique raconte | 15 à 30 s sans voix, sur un mouvement de caméra lent et un lieu nouveau | ● (écriture) / ●●● (plan) | 📝 |
| M06 | **Climax d'accélération puis noir** | 04 (0,2-1 s, puis 28 s de noir) | Le pic de rythme de toute la vidéo, gardé pour la fin | Accélération progressive sur la musique, puis coupe au noir sèche, musique qui décroît | ●● | 🧪 |
| M07 | **Bouclage** | 04 (retour à la pièce et au titre) | Sentiment d'œuvre close, et le payoff du plant N05 | Le dernier lieu est le premier, vu autrement | ● | 📝 |

## T · Transitions

| ID | Procédé | Vu dans | Effet | Recette | Effort | État |
|---|---|---|---|---|---|---|
| T01 | **Carton terminal / machine** | 04 | Chapitre, et un **sous-texte** qui annonce la thèse | Noir, barre de chargement à à-coups, statuts système en monospace dont le texte prépare la chute | ● | ✅ `TerminalChargement` |
| T02 | **Glitch avant un saut de monde** | 04 (datamosh 2,4 s) | Rupture, passage | Datamosh FFmpeg (suppression des images clés) ou glitch Remotion (bandes décalées) | ●● | 🧪 |
| T03 | **Noir ponctuant** | 01-04 | Respiration, fin de chapitre | 1 à 4 s de noir, souvent sur une queue de musique | ● | 📝 |
| T04 | **Seuil physique** | 02, 04 (portes, arches) | Le passage d'une porte = un changement de chapitre | Travelling avant à travers une ouverture ; la lumière change de l'autre côté (I16) | ●● | 📝 (Blender) |
| T05 | **Retour d'objet-symbole** | 03 (cube), 04 (cube) | Continuité thématique entre les chapitres | Le même objet, autre cadrage, autre lumière | ● | 📝 + N07 |
| T06 | **Papier ↔ monde** | 04 | Passer de l'explication au vécu | Coupe franche du blanc schéma vers la 3D sombre (contraste de luminance maximal) | ● | 📝 |

## H · Habillage et typographie

| ID | Procédé | Vu dans | Effet | Recette | Effort | État |
|---|---|---|---|---|---|---|
| H01 | **Source en bas à gauche** | 03 | Crédit sans casser l'image | Petit, gras, blanc à 70 % | ● | ✅ (dans `FiltreArchive`) |
| H02 | **Deux registres typographiques = deux voix** | 04 (serif livre contre mono machine), 03 (sans grasse + halo) | Le spectateur sait « qui parle » (l'humain, la machine, la preuve) | Choisir 2 ou 3 familles maximum, chacune attachée à un rôle | ● | 📝 (DA) |
| H03 | **Sponsor balisé** | 04 (« COLLABORATION COMMERCIALE » + barre de progression + QR code) | Transparence légale et UX : on sait combien de temps ça dure | Mention en haut à gauche, barre de durée du segment, QR code en haut à droite | ● | 🧪 |
| H04 | **Texte qui émerge du bruit** | 04 | Le sens qui sort du hasard | Résolution caractère par caractère | ● | ✅ `TexteBrouille` |
| H05 | **Mot accentué en couleur** | 03 (« explicable », « justifiable » en rose) | Hiérarchie de lecture | Phrase blanche, 1 ou 2 mots dans la couleur d'accent | ● | 🧪 |
| H06 | **Carton d'authenticité** | 04 (« 100 % fait sur Blender », « aucune IA ») | Contrat de confiance avec le public | 2 à 4 s en ouverture. ⚠️ Si on utilise des outils génératifs, on dit **ce qu'on a fait avec**, on ne le cache pas | ● | 📝 (décision éditoriale) |

## S · Son

| ID | Procédé | Vu dans | Effet | Recette | Effort | État |
|---|---|---|---|---|---|---|
| S01 | **Silence d'une seconde avant la phrase-clé** | 03 (9:51, 16:01), 04 (4:34) | La phrase suivante prend tout le poids | 0,6 à 1,2 s, voix et musique coupées (pas seulement baissées) | ● | 📝 |
| S02 | **Lit musical continu sous la voix** | 03 (ducking de 8 dB) | Confort, continuité « podcast » | Musique à −30 dBFS sous la voix, remontée de 8 dB dans les respirations | ● | 📝 (mixage) |
| S03 | **Musique par chapitre** | 04 (tempo de 60 à 187 BPM) | Chaque lieu a son ambiance sonore | Un thème par lieu (cohérent avec I16) ; transitions sur les noirs | ●●● (composition) | 📝 |
| S04 | **Grappe sonore de changement de monde** | 04 (6 événements en 8 s à 23:24) | Le spectateur « sort » physiquement | Vent, ouverture, réverbération qui change, oiseaux | ●● | 🧪 (SFX) |
| S05 | **Fin musicale de 25-35 s, puis silence** | 03 (35 s), 04 (27 s + 17 s de silence) | Laisser décanter | Pas de voix après la dernière phrase ; la musique s'éteint naturellement | ● | 📝 |
| S06 | **Silence « numérique » sur le message machine** | 04 (4:34) | Inquiétude, bug | Coupure franche du son pendant le carton terminal [ERREUR] | ● | 📝 |
| S07 | **Dynamique maîtrisée** | Contre-exemples : 03 (LRA 2,9, trop compressé), 04 (crête +0,7 dBTP) | Ni écrasé ni saturé | Cible : −14 LUFS, LRA 5 à 8, crête ≤ −1 dBTP (`docs/specs-techniques.md`) | ● | 📝 + mesure |

---

## Convergences des 4 références (ce qui ressemble à une signature possible pour nous)

1. Un **lieu ou un objet-concept** porte l'idée (02, 04 : lieux ; 03, 04 : cube).
2. Un **narrateur impliqué**, qui guide, joue avec le spectateur et se remet en question (02, 03, 04).
3. **Fonds sombres, lumière unique, une couleur d'accent** (01 : rouge, 02 : rouge et cyan, 03 : rose, 04 : une palette par lieu).
4. **Personnages sans visage** (01, 03) ou absence d'humain (04).
5. **Silences et respirations écrits** dans le script (02, 03, 04).
6. **Fin en miroir** sur le spectateur (02, 03, 04).

Ces points restent des pistes : la DA se décide avec Bruno (voir `../README.md`).
