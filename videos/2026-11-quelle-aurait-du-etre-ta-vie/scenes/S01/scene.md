# S01 · Ouverture · on marche vers le bureau

| | |
|---|---|
| **Durée** | 0:10 |
| **Fabrication** | Blender (la scène, `bureau.py`) puis Higgsfield (la marche) |
| **Fonction** | ACCROCHER |
| **Procédé principal** | Plan subjectif d'ouverture : le spectateur est l'opérateur, il marche vers sa chaise |
| **Procédés secondaires** | — |
| **Statut** | en construction (07/11/2026) |
| **Production** | validée en V1 (07/11/2026) ; V5 : bouton « nouvelle vie » à l'écran (raccord S02), son à gain fixe (`S01_v5.mp4`) |

## Intention

Décisions de Bruno (07/11/2026) : pas de carton de référence (le crédit « 1 sur 8 milliards · 1in8b.life » ira en description). On ouvre **en vue subjective** : on est quelqu'un qui marche vers sa chaise.

**Le bureau est seul au milieu d'un immense espace noir.** Pas de murs, pas de fenêtre : on a l'impression qu'il est perdu dans l'obscurité. Une seule lumière froide tombe d'en haut et dessine un îlot ; l'écran allumé est la seconde source. Le sol, un peu brillant, étire le reflet de l'écran jusqu'à nous. Un câble part du bureau et s'enfonce dans le noir.

On part de loin, environ sept mètres, dans le noir, à pas lents, avec un léger balancement de marche. On arrive juste derrière la chaise vide, une veste posée sur le dossier, face à l'écran.

## Script / son

- **Voix off** : aucune. Voir `../../script.md`, section S01.
- **Son** : nos pas sur le sol, lents, qui résonnent dans un grand volume vide ; le bourdonnement de l'ordinateur et de la lumière qui grandit à mesure qu'on approche ; aucune musique. À chercher dans Epidemic Sound (pas sur linoléum, grand espace, ronflement électrique).

## Découpage en plans

| Plan | Durée | Matière | Contenu | Animation / mouvement | Procédé | Son |
|---|---|---|---|---|---|---|
| S01-P01 | 10 s | 3D | Vue subjective : on marche dans le noir vers le bureau éclairé, jusqu'à la chaise vide | Marche lente, léger balancement (Blender : images de départ et d'arrivée ; Higgsfield : l'animation) | | Pas, bourdonnement, pas de musique |

## Fabrication

- Scène : `bureau.py` (Blender 5.2, lancé en arrière-plan sur le PC ; tout est construit par le script, matières procédurales, aucun asset téléchargé).
- Rendus (hors Git) : `../../medias/S01/S01_depart.png`, `S01_milieu.png`, `S01_arrivee.png` ; scène : `../../medias/blender/S01_bureau.blend`.
- Animation : Higgsfield, Wan 3.0 (`../../prompts/S01.md`).
  - V1 : 6 s, 21 crédits, `../../medias/S01/S01_marche_v1.mp4`. La caméra ne démarrait qu'après 1,5 s.
  - V2 (demande de Bruno : marche plus lente) : 10 s, 35 crédits. Le modèle ne donne aucun balancement de tête, donc on l'ajoute en post (FFmpeg) : un pas toutes les 0,95 s à partir de 0,45 s, 6 px en vertical, 4 px en latéral, éteint sur la dernière seconde :
    `ffmpeg -i S01_marche_v2.mp4 -vf "scale=1960:1102:flags=lanczos,crop=1920:1080:'20+4*sin(PI*(t-0.45)/0.95)*min(1\,(9.6-t)/1.2)*gte(9.6\,t)':'11+6*cos(2*PI*(t-0.45)/0.95)*min(1\,(9.6-t)/1.2)*gte(9.6\,t)',fps=24" -c:v libx264 -crf 16 -pix_fmt yuv420p -an S01_marche_v2_balancement.mp4`
- Son : `son.py` (sons Epidemic Sound, registre `../../references/sons.md`) : `python son.py --video ../../medias/S01/S01_marche_v2_balancement.mp4 --sortie ../../medias/S01/S01_son_v2.wav --pas 0.45,1.40,2.35,3.30,4.25,5.20,6.15,7.10,8.05,9.00`. Dix pas posés sur les points bas du balancement, l'air d'un grand hall vide, le ronflement de l'ordinateur et de la lampe qui montent et s'éclaircissent à l'approche, une réverbération de grand volume. Pas de musique. Mesures : -26 LUFS intégré (début de vidéo volontairement calme), crête -1,5 dBTP, chaque pas environ 8 dB au-dessus du fond.
- Écran (V3, V4) : `ecran.py` remplace ce qu'affiche l'ordinateur, sans regénérer la marche. L'écran d'origine est suivi image par image (par sa fenêtre claire, que la chaise ne cache jamais) et on y incruste une interface : une ligne par vie simulée (pays, naissance, école, travail, mariage, enfants, âge de la mort), la vie en cours qui se dessine pendant le plan, un compteur de vies simulées au rythme des naissances dans le monde (≈ 4,3 par seconde), et deux fiches avec un portrait robot (un homme, Inde, vie terminée ; une jeune femme, Nigeria, la vie en cours). La chaise passe devant l'écran comme avant. Aucun pourcentage. Ensuite : même balancement et même son que la V2.
- **Plan livré : `../../medias/S01/S01_v4.mp4`** (V2 sans l'écran : `S01_v2.mp4`) (10 s, 1920 × 1080, 24 i/s, H.264 + AAC 48 kHz).

## Points à revoir

- Le son n'a été vérifié que par mesures (je n'entends pas) : à écouter au casque. Les pas sont réguliers (0,95 s) ; au montage, on pourra varier légèrement leur cadence.

- La géométrie est faite de formes simples : correcte de loin, plus sommaire de près (chaise, clavier). À enrichir si l'animation Higgsfield le révèle.
- S02 (« le bureau à l'aube », l'opérateur vu de dos) est à repenser pour suivre ce nouveau décor : plus de fenêtre, donc plus d'aube par la fenêtre.
