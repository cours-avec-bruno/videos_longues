# Images et vidéos externes · registre des sources et licences

Fichiers hors Git, dans `medias/pexels/` et `medias/nasa/`.

## Pexels (licence Pexels : usage gratuit, y compris commercial, modification permise, attribution non obligatoire)

Le crédit en description reste une bonne pratique (« Vidéos : Pexels » et les auteurs si on les liste). Page de chaque vidéo : `https://www.pexels.com/video/<identifiant>/`.

| Fichier | Lieu | Identifiant Pexels | Utilisé |
|---|---|---|---|
| `tokyo_6574285.mp4` | Tokyo, carrefour de Shibuya | 6574285 | S03-S04, le monde |
| `paris_34558256.mp4` | Paris, tour Eiffel (drone) | 34558256 | S03-S04 |
| `rio_16023860.mp4` | Rio, Christ rédempteur (drone) | 16023860 | S03-S04 |
| `newyork_5565202.mp4` | New York, Manhattan depuis l'eau | 5565202 | S03-S04 |
| `caire_10717893.mp4` | Gizeh, pyramides (drone) | 10717893 | S03-S04 |
| `venise_36328559.mp4` | Venise, Grand Canal | 36328559 | S03-S04 |
| `kenya_7499056.mp4` | Savane, éléphants | 7499056 | S03-S04 |
| `shanghai_33009782.mp4` | Shanghai, le Bund la nuit | 33009782 | S03-S04 |
| `sydney_36924503.mp4` | Sydney, l'Opéra | 36924503 | S03-S04 |
| `sahara_37523973.mp4` | Sahara, caravane | 37523973 | S03-S04 |
| `islande_29477448.mp4` | Islande, icebergs (drone) | 29477448 | S03-S04 |
| `amazonie_35969886.mp4` | Amazonie, fleuve (drone) | 35969886 | S03-S04 |
| `inde/inde_31372348.mp4` | (remplacé) | 31372348 | non : le village de Manoj est passé au bord de la mer |
| `inde/inde_34732091.mp4` | (remplacé) | 34732091 | non |
| `s05/35356378.mp4` | Village de pêcheurs au bord de la mer, vu du ciel (Inde du Sud) | 35356378 | S04, l'arrivée |
| `s05/19598363.mp4` | Pêcheurs qui poussent une barque sur la plage | 19598363 | S04 |
| `s05/4440945.mp4` | Pêcheurs et filets sur la plage, contre-jour | 4440945 | S05 |
| `s05/31700496.mp4` | Des enfants qui jouent devant une maison du village | 31700496 | S05 |
| `s05/856779.mp4` | Les marmites sur le feu de bois | 856779 | S05 |
| `s05/4113114.mp4` | Le feu de bois de près, la fumée | 4113114 | S05 |
| `s05/38994414.mp4` | Une femme puise l'eau au fond d'un trou | 38994414 | S05 |
| `portraits/manoj_16067431.jpg` | Portrait (Pexels, photo 16067431), affiché en très gros pixels : jamais reconnaissable | 16067431 | S05, le visage de Manoj |

Autres candidats téléchargés, non utilisés pour l'instant (dans les mêmes dossiers) : d'autres vues de ces lieux, et des villages indiens (champs, femmes portant l'eau, cour avec vaches), utiles pour S05.

## NASA (domaine public)

| Fichier | Source | Utilisé |
|---|---|---|
| `nasa/terre_24000.jpg` | NASA Blue Marble, « Whole world - land and oceans » 24000 x 12000, via Wikimedia Commons (`File:Whole_world_-_land_and_oceans_12000.jpg`) | S04, la Terre (`scenes/S04/terre.py`) |

## Données

| Fichier | Source | Licence | Utilisé |
|---|---|---|---|
| `donnees/kontur_r4.gpkg` | Kontur Population, 1er novembre 2023, hexagones H3 ~22 km (HDX : kontur-population-dataset-22km) | **CC BY 4.0 : crédit obligatoire** (à l'écran en bas à gauche, et en description : « Population : Kontur Population 2023, CC BY 4.0 ») | S04, la carte des densités (`scenes/S04/carte.py`) |
| `donnees/ne_pays_50m.geojson` | Natural Earth, pays 1:50m | domaine public | S04, contours des pays et de l'Inde |

Vérification faite avec ces données : l'Inde compte 1,43 milliard d'habitants sur 8,03, soit 17,8 % (« plus de dix-sept pour cent » est juste).
