# Extraction · sintel_trailer-480p

> Généré automatiquement par `shared/outils/analyser-reference`. Données **mesurées** sur la vidéo.
> L'interprétation (DA, intentions) se fait dans `../../analyses/`.

## Source

| | |
|---|---|
| Lien | https://download.blender.org/durian/trailer/sintel_trailer-480p.mp4 |
| Publiée le | 12/05/2010 |
| Durée | 00:52 |
| Résolution analysée | 854×480 @ 24.00 i/s |
| Seuils de détection | 0.3 (franche) / 0.08 (adaptative) |
| Extrait le | 2026-11-05 |

## Rythme du montage

| Mesure | Valeur |
|---|---|
| Plans détectés | 18 |
| Durée moyenne d'un plan | 2.9 s |
| Médiane | 2.5 s |
| 10 % des plans durent moins de | 1.0 s |
| 10 % des plans durent plus de | 5.2 s |
| Coupes par minute (moyenne) | 20.7 |
| Transitions progressives (fondus, enchaînés…) | 8 sur 17 (47 %) |

> Les transitions progressives sont placées au milieu du fondu : la durée des plans qui les entourent est approximative (± 0,5 s).

### Coupes par minute, par tranche de 1 min

```
   00:00  ██████████████████████████████  20.7
```

### Les 10 plans les plus longs (moments contemplatifs)

| Plan | Début | Durée |
|---|---|---|
| P016 | 00:41.5 | 7.0 s |
| P015 | 00:34.8 | 6.8 s |
| P013 | 00:28.0 | 4.5 s |
| P003 | 00:04.5 | 4.3 s |
| P008 | 00:17.5 | 3.5 s |
| P004 | 00:08.8 | 3.5 s |
| P002 | 00:01.0 | 3.5 s |
| P009 | 00:21.0 | 2.8 s |
| P006 | 00:13.9 | 2.6 s |
| P017 | 00:48.5 | 2.4 s |

## Couleur

![Palette](palette.png)

Palette dominante de la vidéo entière (k-means sur les vignettes, pondéré par la durée des plans) :

| Couleur | Part | Luminance | Saturation |
|---|---|---|---|
| `#020202` | 49.2 % | 1 % | 30 % |
| `#271e17` | 14.5 % | 12 % | 41 % |
| `#4d4137` | 10.2 % | 26 % | 28 % |
| `#90613c` | 6.9 % | 41 % | 58 % |
| `#7c7c7a` | 5.6 % | 49 % | 2 % |
| `#9fa19f` | 5.5 % | 63 % | 1 % |
| `#c2885b` | 5.2 % | 57 % | 53 % |
| `#e9bf89` | 3.0 % | 77 % | 41 % |

- Luminance moyenne : **19 %**
- Temps passé sur des plans très sombres (luminance < 15 %) : **49 %**
- Saturation moyenne : **25 %**

Évolution de la couleur dans le temps (chaque plan = sa couleur moyenne, largeur ∝ durée) :

![Barcode](barcode.png)

## Planches contact

20 vignettes pour 18 plans : une par plan, plus une toutes les ~5 s dans les plans longs (notées `2/3`…), pour voir le mouvement.
Étiquette de chaque vignette : `numéro de plan · timecode de l'image · (durée du plan)`.

| Planche | Vignettes |
|---|---|
| [planche-001.jpg](planches/planche-001.jpg) | 00:01 → 00:52 |

Détail plan par plan : [`plans.csv`](plans.csv).

## Fichiers hors Git (sur la machine qui a lancé l'extraction)

- Vidéo et métadonnées : `.cache/references/exemple-sintel-bande-annonce/`
