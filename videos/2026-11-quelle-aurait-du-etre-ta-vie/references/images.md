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
| `s06/16270511.mp4` | Un bébé tenu dans des mains (vertical) | 16270511 | non (S06 refaite en 3D) |
| `s06/5451849.mp4` | Trois garçons qui jouent avec la terre (noir et blanc, Bangladesh) | 5451849 | non (S06 refaite en 3D) |
| `s06/40379978.mp4` | Une grand-mère et un garçon | 40379978 | non (S06 refaite en 3D) |
| `s06/36100216.mp4` | Des rotis sur un feu de bois | 36100216 | non (S06 refaite en 3D) |
| `s06/3978429.mp4` | Des enfants qui jouent dans un champ, soleil bas | 3978429 | non (S06 refaite en 3D) |
| `s07/35724453.mp4` | Écoliers en uniforme qui arrivent à l'école | 35724453 | S07, 5 ans |
| `s07/15957335.mp4` | Rassemblement d'élèves en uniforme (Assam) | 15957335 | S07 |
| `s07/4112783.mp4` | Billets de roupies sur une table | 4112783 | S07, « ça leur coûte cher » |
| `s07/28887495.mp4` | Une foule qui chante et frappe des mains (dévotion) | 28887495 | S07, la prière |
| `s07/16868495.mp4` | Un garçon en chemise rouge à son pupitre | 16868495 | S07, 9 ans |
| `s07/18070270.mp4` | Gros plan d'un billet de 500 roupies | 18070270 | S07, la dette |
| `s07/20143634.mp4` | Des fleurs de souci au bord du fleuve (ghât) | 20143634 | S07, 10 ans |
| `s07/34630320.mp4` | Une lampe à huile (diya) près de l'eau | 34630320 | S07, la fin |
| `s07/36088025.mp4`, `s07/35622767.mp4` | Cricket de rue ; barque au crépuscule | 36088025, 35622767 | non utilisées |

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
