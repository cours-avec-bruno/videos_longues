# Méthode de rétro-ingénierie d'une vidéo de référence

## D'où vient cette méthode : REA

[REA](https://github.com/morluto/rea) (« Reverse Engineer Anything ») est un outil de rétro-ingénierie de **logiciels** : binaires, applications, Android, sites web. Il **ne sait pas lire une vidéo**, et il n'est pas utile de l'installer pour ce projet.

Sa **méthode**, en revanche, se transpose très bien à la vidéo. Voici ce qu'on lui emprunte (d'après sa skill `reverse-engineer-anything` et son guide `evidence-workflows`) :

| Principe REA | Ce que ça devient pour une vidéo |
|---|---|
| **Choisir l'outil selon la cible** (*route the target first*) | Chaque question a son instrument : le rythme passe par la mesure des plans, le son par Demucs et les frises, la typographie par une image en pleine résolution, le sens par la transcription. On ne demande pas à une IA de « décrire la vidéo » |
| **Résumé d'abord, détail ensuite** (*summary-first*) | `resume.md`, puis les planches, puis les frises, puis des images ou des segments ciblés. On ne descend dans le détail que là où une question le demande |
| **Chaque conclusion porte sa preuve, son autorité et ses limites** | Étiquettes [MES] mesuré, [OBS] vu, [TRANS] transcription, [DESC] description de l'auteur, [HYP] hypothèse. Une fiche d'analyse sans étiquettes n'est pas recevable |
| **Distinguer observation, inférence et inconnue** | Chaque fiche finit par un **registre des inconnues** : la question, et ce qu'il faudrait pour trancher |
| **L'absence de preuve n'est pas une preuve d'absence** | Un événement sonore non détecté peut être masqué par la voix ; une « rafale » de coupes peut être une animation à deux images par dessin. On le note |
| **Vérifier la reconstruction** (*verify_reconstruction* : une spécification finie, comparée point par point) | Quand on reproduit un procédé, on **analyse notre propre rendu avec le même outil** et on compare les mesures déclarées : durée des plans, part de coupes sur le son, sonie, palette. Le test ne porte que sur les critères qu'on a déclarés, pas sur une ressemblance globale |

## Le pipeline

1. **Acquérir** (sur le PC) :
   `npm run analyser-reference -- <lien> --separer --demucs "py -3.12 -m demucs"`
   On obtient planches, plans, couleurs, son, frises, sous-titres et métadonnées.
2. **Lire le résumé** : rythme, palette, sonie, voix, respirations, silences, événements.
3. **Regarder vraiment** toutes les planches. Les **frises** servent pour le lien entre son et montage.
4. **Plonger de façon ciblée** :
   - images en pleine résolution là où un micro-détail se joue (`ffmpeg -ss <t> -i .cache/references/<id>/video.mp4 -frames:v 1 x.png`) : typographies, grain, aberrations, textes à l'écran ;
   - transcription horodatée (les sous-titres `.vtt` sont dans `.cache/references/<id>/`) : structure, plants, refrains, phrases-clés ;
   - description de la vidéo : crédits, outils, musiques, équipe.
5. **Écrire la fiche d'analyse** dans `analyses/refNN-<nom>.md` : identité, structure en timecodes, écriture, image, montage, transitions, son, « ce qu'on retient », inconnues.
6. **Extraire les procédés** dans `procedes/catalogue.md` : un identifiant, la source avec ses timecodes, l'effet recherché, la recette dans nos outils, l'effort et l'état.
7. **Reconstruire** les procédés les plus utiles (composant Remotion, script Blender, prompt Higgsfield), dans `shared/`.
8. **Vérifier la reconstruction** : rendu, puis `npm run analyser-reference -- <notre-rendu.mp4> --id test-<procede>`, puis comparaison des mesures visées avec celles de la référence.

## Règles

- **Le son ne s'invente pas** : je n'entends pas. Je décris ce que disent les mesures et les frises, et je marque [HYP] tout ce qui touche au timbre, au genre ou à l'émotion.
- **Les descriptions par IA** (vidIQ, Higgsfield) sont des témoignages, pas des observations. Elles ne remplacent jamais les planches.
- **On ne copie pas une vidéo** : on extrait des mécanismes. Le catalogue décrit *pourquoi* un procédé marche, pour pouvoir le réinventer ailleurs.
- **Droits** : les vidéos téléchargées restent dans `.cache/`, hors Git. Seules les planches réduites et les mesures sont versionnées.

La skill `.claude/skills/retro-ingenierie-video/` applique cette méthode pas à pas.
