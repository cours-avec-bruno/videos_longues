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

## Voix (ElevenLabs, voix « Guillaume - Documentary and Storytelling », `3HZyQcLKlT0a3RDeXVsP`)

| Fichier local | Scène | Modèle | Génération | Retenue |
|---|---|---|---|---|
| `voix/S02_prise1.mp3` | S02 | eleven_v3 | `LjXYiNQti90bGIWgWhZL` (flux `U7OowaqbCt44sRCdzHlG`) | **oui** (choix de Bruno) |
| `voix/S02_prise2.mp3` | S02 | eleven_v3 | `AJYrlHKo6A5MqkjFnKZw` | non |

Coût : 646 crédits ElevenLabs pour les deux prises. Licence : voix de la bibliothèque ElevenLabs, usage commercial couvert par l'abonnement.

## Niveaux

Toutes les scènes partagent le même gain général (`medias/S01/gain_mix.txt`, écrit par `scenes/S01/son.py`) : le décor sonore garde son niveau d'une scène à l'autre, et seule la voix fait monter la sonie. S01 : -26 LUFS (aucune voix). S02 : -15 LUFS. La sonie finale (-14 LUFS) se règle au mastering.

La réverbération de S01 est synthétique (calculée dans `scenes/S01/son.py`) : pas de source externe.
