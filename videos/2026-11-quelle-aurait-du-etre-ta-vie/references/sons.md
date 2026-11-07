# Sons · registre des sources et licences

Tous les fichiers sont hors Git, dans `medias/sons/<source>/`. Pour retélécharger un son Epidemic Sound : outil `DownloadSoundEffect` avec l'identifiant ci-dessous.

Licence Epidemic Sound : abonnement de Bruno (usage sur YouTube couvert par l'abonnement actif au moment de la publication ; vérifier que la chaîne est bien déclarée sur le compte Epidemic avant publication).

| Fichier local | Titre Epidemic Sound | Identifiant | Scène | Usage |
|---|---|---|---|---|
| `epidemic/pas_beton_lent.wav` | Footsteps, Human, Concrete, Shoes, Slow Tempo, Steady 06 | `c18e4e7b-9269-48c2-9864-27daf989154a` | S01 | nos pas (impacts découpés et recalés) |
| `epidemic/pas_grand_hall.wav` | Footsteps, Human, Moderate Tempo, Large Hall, Walk, Scuff, Boots | `d572a75b-a86f-4f02-91b4-276a5d48a8cd` | — | téléchargé, non utilisé (le tempo « slow » colle mieux à la marche) |
| `epidemic/bourdonnement_ordinateur.wav` | Electricity, Buzz & Hum, Computer Case | `e58665e3-34f6-497b-ada2-075c2d77cf94` | S01 | ronflement de l'ordinateur, monte à l'approche |
| `epidemic/bourdonnement_lumiere.wav` | Electricity, Buzz & Hum, Lights, Electrical Hum | `db72319a-e0ff-4582-a0fb-e4b6c5fc4cb5` | S01 | bourdonnement de la lampe au plafond |
| `epidemic/ambiance_grand_hall.wav` | Ambience, Room Tone, Empty Hall, Deep 01 | `cf056827-47df-4465-816d-dbc6d766b714` | S01 | air d'un grand espace vide |
| `epidemic/chaise_assis.wav` | Objects, Furniture, Office Chair, Padded, Person Sit Down | `898f8779-8bc5-4efe-9802-4489aeb33a2f` | S02 | on s'assoit |
| `epidemic/interrupteur_lampe.wav` | Mechanical, Switch, Lamp, On, Off 01 | `e1a8159b-c679-48f9-a24e-00c390560b88` | S02 | le clic de la lampe (premier clic seulement) |
| `epidemic/tic_doux.wav` | Clocks, Tick, Simple, Clicky, Soft, Loop 02 | `0bfb4ddb-4807-4059-a3e9-3383d383c015` | S02 | un tic par naissance, sur le compteur |
| `epidemic/souris_clics.wav` | Computers, Keyboard & Mouse, Mouse, Logitech M90, Left Click, Various Single | `a74993f6-b48c-4d7f-9929-9c516dbaf25a` | S02 | le clic sur « nouvelle vie » |
| `epidemic/souris_tapis.wav` | Computers, Keyboard & Mouse, Mouse, Macbook Pro, Mouse Pad, Movement | `23551ef8-34d7-40a5-94ac-08dcc1ac54d3` | S02 | la souris qui glisse quand le pointeur bouge |
| `epidemic/clavier_lent.wav` | Computers, Keyboard & Mouse, Keyboard, Dell, Typing, Slow | `687247da-0746-4243-a9ec-508f74dcda04` | S03 | les touches de « France » |
| `epidemic/whoosh_zoom.wav` | Swooshes, Whoosh, Fast, Close, Airy, Zoom 01 | `ef3da4c3-b32a-4d99-a58a-8c167e50c4f9` | S04 | plongée dans l'écran, traversées |
| `epidemic/whoosh_air.wav` | Swooshes, Whoosh, Classic, Airy, Cinematic | `5ee53a73-e569-4517-8f13-7e36a47b15e6` | S04 | traversées |
| `epidemic/whoosh_fusee.wav` | Swooshes, Whoosh, Noise, Rockety Texture, Cinematic 02 | `ef48d50d-47fe-491f-a853-7c1cb24af800` | S04 | la plongée sur l'Inde |
| `epidemic/espace_drone.wav` | Designed, Drone, Dark Space, Sub Rumble | `454a607b-ba1d-4cc9-8242-846271b8f035` | S04 | le grondement qui monte jusqu'à l'espace |
| `epidemic/village_amethi.wav` | Ambience, Town, Village, Morning, Washing Utensils, Birds Crows Walla, Bicycle Passing, Amethi, Uttar Pradesh, India 02 | `28a00d2f-20fd-4e42-9350-c8cbfeca2ac1` | S04 | l'arrivée au village |

## Voix (ElevenLabs, voix « Guillaume - Documentary and Storytelling », `3HZyQcLKlT0a3RDeXVsP`)

| Fichier local | Scène | Modèle | Génération | Retenue |
|---|---|---|---|---|
| `voix/S02_prise1.mp3` | S02 | eleven_v3 | `LjXYiNQti90bGIWgWhZL` (flux `U7OowaqbCt44sRCdzHlG`) | **oui** (choix de Bruno) |
| `voix/S02_prise2.mp3` | S02 | eleven_v3 | `AJYrlHKo6A5MqkjFnKZw` | non |
| `voix/S02_aventure_prise1.mp3` | S02 (dernière phrase) | eleven_v3 | `4BD3sDzImlooElDfaLpB` | **oui** : « Vous allez m'accompagner dans cette aventure. », générée avec la phrase précédente pour garder l'intonation |
| `voix/S02_aventure_prise2.mp3` | S02 (dernière phrase) | eleven_v3 | `pqn9DxmUP9pbR0GSYiTX` | non |

| `voix/S03_prise1.mp3` | S03 (réglages) | eleven_v3 | `dIxgGPpYRJi2AoEbTmTn` | non (l'écran des réglages est retiré) |
| `voix/S04_prise2.mp3` | S03-S04 | eleven_v3 | `iq4iwSrsMNJTCGRN9CpH` | non (voix trop aiguë par rapport à S02, remarqué par Bruno) |
| `voix/S04b_prise1.mp3` | S03-S04 (« Commençons… », l'arrivée), générée dans la continuité du texte de S02 | eleven_v3 | `zjedtRiTbwo6WtG2YC0O` | **oui, verrouillée par Bruno (07/11/2026)** |

Toutes les prises sont ramenées au même niveau de voix au montage.

Coût : 646 crédits ElevenLabs pour les deux prises, puis 238 pour la nouvelle dernière phrase. Licence : voix de la bibliothèque ElevenLabs, usage commercial couvert par l'abonnement.

## Niveaux

Toutes les scènes partagent le même gain général (`medias/S01/gain_mix.txt`, écrit par `scenes/S01/son.py`) : le décor sonore garde son niveau d'une scène à l'autre, et seule la voix fait monter la sonie. S01 : -26 LUFS (aucune voix). S02 : -15 LUFS. La sonie finale (-14 LUFS) se règle au mastering.

La réverbération de S01 est synthétique (calculée dans `scenes/S01/son.py`) : pas de source externe.
