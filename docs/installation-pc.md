# Installation du PC fixe (Windows)

Le PC fixe (avec sa **carte NVIDIA**) sert à la **production lourde** : rendus Remotion en qualité finale, Blender, analyse des références avec séparation du son, montage et stockage des médias. Ce guide ne concerne que lui : l'autre machine, sans carte graphique, n'a besoin de rien de tout ça pour discuter avec Claude. L'écriture (recherches, storyboard, scripts, code des scènes) peut se faire dans le cloud. Les deux travaillent sur le même repo GitHub (voir la section « Répartition cloud / PC » du `CLAUDE.md`).

Toutes les commandes ci-dessous se lancent dans **PowerShell**.

> **Installation automatique** : le script [`scripts/installer-pc-fixe.ps1`](../scripts/installer-pc-fixe.ps1) fait tout ce guide d'un coup (logiciels, projet, PyTorch GPU, Demucs, autotest, rendu de test). À coller dans PowerShell. Il est relançable sans risque. Les sections ci-dessous détaillent ce qu'il fait, utile en cas de problème.

## 1. Logiciels

```powershell
winget install --id Git.Git -e
```

```powershell
winget install --id OpenJS.NodeJS.LTS -e
```

```powershell
winget install --id Gyan.FFmpeg -e
```

```powershell
winget install --id BlenderFoundation.Blender -e
```

```powershell
winget install --id yt-dlp.yt-dlp -e
```

`yt-dlp` sert à l'outil d'analyse des vidéos de référence (`npm run analyser-reference`). YouTube change souvent : mets-le à jour de temps en temps avec `yt-dlp -U`.

Fermer puis rouvrir PowerShell, puis vérifier :

```powershell
git --version; node --version; ffmpeg -version; blender --version; yt-dlp --version
```

`node --version` doit afficher une **v22 ou plus récente** (le cloud est en v22).

## 2. Réglages Git (une seule fois)

```powershell
git config --global core.longpaths true
```

```powershell
git config --global core.autocrlf false
```

```powershell
git config --global pull.rebase true
```

- `core.longpaths` : évite les erreurs de chemins trop longs (fréquentes avec `node_modules` sous Windows).
- `core.autocrlf false` : c'est le fichier `.gitattributes` du repo qui gère les fins de ligne. Sinon, Git verrait de faux changements sur tous les fichiers.
- `pull.rebase` : un historique propre quand le cloud et le PC ont tous les deux commité.

## 3. Récupérer le repo

**Important : ne pas mettre le repo dans un dossier OneDrive** (Documents, Bureau, Images sont souvent synchronisés). OneDrive et Git se marchent dessus : fichiers verrouillés, doublons « -PC », `node_modules` synchronisé inutilement. Un chemin court hors OneDrive est idéal.

**Sur le PC fixe actuel**, le projet est dans `D:\Studio\videos_longues`, le disque qui a de la place pour les médias. `C:\Studio\videos_longues` est une jonction vers D, si bien que les anciens chemins (script d'installation, sessions Claude) continuent de fonctionner. Sur une installation neuve, clone de préférence sur D, puis recrée la jonction :

```powershell
New-Item -ItemType Junction -Path C:\Studio\videos_longues -Target D:\Studio\videos_longues
```

Les commandes ci-dessous montrent l'installation d'origine, sur C :

```powershell
mkdir C:\Studio; cd C:\Studio
```

```powershell
git clone https://github.com/cours-avec-bruno/videos_longues.git
```

```powershell
cd videos_longues; npm install
```

Le premier rendu Remotion télécharge automatiquement son navigateur de rendu (Chrome Headless Shell), puis le garde pour les fois suivantes. Pour tester :

```powershell
npm run render -- Test-Pipeline out/test.mp4
```

Pour tester l'outil d'analyse des références :

```powershell
npm run analyser-reference -- https://www.youtube.com/watch?v=K8Ugw48gnNk
```

Les planches et l'analyse du son apparaissent dans `docs/direction-artistique/extractions/`. Si YouTube demande une vérification, relance en ajoutant `--cookies-navigateur firefox`.

Pour vérifier que l'outil fonctionne sur le PC, sans rien télécharger :

```powershell
npm run tester-analyse
```

### Séparation voix / musique (Demucs, sur la carte NVIDIA)

Pour une analyse fine du son. Avec la carte graphique, la séparation d'une vidéo de 70 min prend quelques minutes, contre environ 25 min sur processeur seul.

1. Vérifier que la carte est reconnue. La commande affiche son nom et la version CUDA en haut à droite :

```powershell
nvidia-smi
```

2. Installer Python :

```powershell
winget install --id Python.Python.3.12 -e
```

3. Fermer et rouvrir PowerShell, puis installer PyTorch **version GPU**. Cela fait environ 2,5 Go à télécharger. La version CUDA 12.8 couvre les cartes RTX 20 à 50 et demande un pilote NVIDIA récent (≥ 572) :

```powershell
py -3.12 -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
```

4. Installer Demucs :

```powershell
py -3.12 -m pip install demucs soundfile
```

5. Vérifier que PyTorch voit la carte. La commande doit afficher `True` :

```powershell
py -3.12 -c "import torch; print(torch.cuda.is_available())"
```

6. Tester toute la chaîne :

```powershell
npm run tester-analyse -- --separer --demucs "py -3.12 -m demucs"
```

Ensuite, pour analyser une référence avec la séparation, ajoute `--separer --demucs "py -3.12 -m demucs"` à la commande. Demucs utilise la carte NVIDIA automatiquement.

Si l'étape 5 affiche `False`, mets à jour le pilote NVIDIA (application NVIDIA ou nvidia.com), puis recommence à partir de l'étape 3.

## 4. Claude Code sur le PC

Pour que Claude puisse lancer lui-même les rendus et Blender, et voir les résultats :

- **Application de bureau Claude** (claude.ai/download), onglet Claude Code, en ouvrant le dossier `C:\Studio\videos_longues` ;
- ou la **CLI** :

```powershell
irm https://claude.ai/install.ps1 | iex
```

Le `CLAUDE.md` du repo est chargé automatiquement : Claude local et Claude cloud suivent les mêmes règles.

**Option** : dans l'application de bureau, Réglages → Claude Code → Remote Control permet de partager ce dossier avec une session cloud, qui peut alors exécuter des commandes sur le PC. Cette fonction n'est pas encore disponible pour tous les comptes.

## 5. Blender

- **GPU** : Édition → Préférences → Système → Cycles Render Devices → **OptiX** (carte NVIDIA RTX) ou **HIP** (AMD), en cochant la carte graphique.
- **Plugin Higgsfield** : installer le plugin, ouvrir son panneau dans Blender et cliquer sur **Connect**. Claude peut alors piloter Blender directement (outils `bl_*`).

## 6. Polices

Les polices du projet sont dans `shared/assets/polices/`. Pour que Remotion et Blender les trouvent, les installer avec clic droit → **Installer pour tous les utilisateurs**.

Côté Remotion, les polices seront chargées directement depuis le repo, pour que le rendu soit identique dans le cloud et sur le PC. Ce sera mis en place quand la DA aura choisi ses polices.

## 7. Médias lourds

Les vidéos, rendus et sons volumineux ne passent pas par Git. Sur le PC, ils vont **au même emplacement relatif que dans le repo** (`videos/<slug>/medias/`, `videos/<slug>/exports/`) : le code fonctionne ainsi sans modification. Le `.gitignore` exclut déjà les fichiers lourds (vidéo, audio non compressé, EXR, PSD) et tout le contenu des dossiers `exports/`.

La sauvegarde de ces médias (disque externe, Drive, NAS…) reste à décider : voir `docs/journal.md`.
