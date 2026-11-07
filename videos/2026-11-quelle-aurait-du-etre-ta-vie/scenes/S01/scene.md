# S01 · Ouverture · on marche vers le bureau

| | |
|---|---|
| **Durée** | ≈ 0:05 à 0:08 |
| **Fabrication** | Blender (la scène, `bureau.py`) puis Higgsfield (la marche) |
| **Fonction** | ACCROCHER |
| **Procédé principal** | Plan subjectif d'ouverture : le spectateur est l'opérateur, il marche vers sa chaise |
| **Procédés secondaires** | — |
| **Statut** | en construction (07/11/2026) |
| **Production** | en cours |

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
| S01-P01 | 6 s | 3D | Vue subjective : on marche dans le noir vers le bureau éclairé, jusqu'à la chaise vide | Marche lente, léger balancement (Blender : images de départ et d'arrivée ; Higgsfield : l'animation) | | Pas, bourdonnement, pas de musique |

## Fabrication

- Scène : `bureau.py` (Blender 5.2, lancé en arrière-plan sur le PC ; tout est construit par le script, matières procédurales, aucun asset téléchargé).
- Rendus (hors Git) : `../../medias/S01/S01_depart.png`, `S01_milieu.png`, `S01_arrivee.png` ; scène : `../../medias/blender/S01_bureau.blend`.
- Prochaine étape : Higgsfield anime la marche à partir des images de départ et d'arrivée (devis de crédits à valider par Bruno).

## Points à revoir

- La géométrie est faite de formes simples : correcte de loin, plus sommaire de près (chaise, clavier). À enrichir si l'animation Higgsfield le révèle.
- S02 (« le bureau à l'aube », l'opérateur vu de dos) est à repenser pour suivre ce nouveau décor : plus de fenêtre, donc plus d'aube par la fenêtre.
