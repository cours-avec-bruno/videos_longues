# Installation du PC fixe (Windows)

Le PC fixe sert à la **production lourde** : rendus Remotion en qualité finale, Blender, montage et stockage des médias. L'écriture (recherches, storyboard, scripts, code des scènes) peut se faire dans le cloud. Les deux travaillent sur le même repo GitHub (voir la section « Répartition cloud / PC » du `CLAUDE.md`).

Toutes les commandes ci-dessous se lancent dans **PowerShell**.

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

`node --version` doit afficher une **v22**. C'est la même version que dans le cloud, fixée par `.nvmrc`.

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

**Important : ne pas mettre le repo dans un dossier OneDrive** (Documents, Bureau, Images sont souvent synchronisés). OneDrive et Git se marchent dessus : fichiers verrouillés, doublons « -PC », `node_modules` synchronisé inutilement. Un chemin court hors OneDrive est idéal :

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

**Optionnel : séparation voix / musique (Demucs)**, pour une analyse plus fine du son. Voir `shared/outils/analyser-reference/README.md`, section « Installer Demucs ». Il faut Python, puis `py -m pip install demucs soundfile`.

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
