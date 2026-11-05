# Installation complète du PC fixe (Windows + carte NVIDIA) pour le studio videos_longues.
# À coller dans PowerShell (pas besoin du mode administrateur ; Windows peut demander des confirmations).
# Relançable sans risque : ce qui est déjà installé est simplement ignoré.

$ErrorActionPreference = 'Continue'
function Etape($m) { Write-Host "`n=== $m ===" -ForegroundColor Cyan }
function Ok($m) { Write-Host "  OK  $m" -ForegroundColor Green }
function Ko($m) { Write-Host "  !!  $m" -ForegroundColor Yellow }
function RechargerPath { $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') }

Etape '1/7 Logiciels (Git, Node, FFmpeg, yt-dlp, Blender, Python)'
foreach ($id in 'Git.Git', 'OpenJS.NodeJS.LTS', 'Gyan.FFmpeg', 'yt-dlp.yt-dlp', 'BlenderFoundation.Blender', 'Python.Python.3.12') {
  Write-Host "  - $id"
  winget install --id $id -e --silent --accept-source-agreements --accept-package-agreements | Out-Null
}
RechargerPath
foreach ($c in 'git', 'node', 'npm', 'ffmpeg', 'yt-dlp', 'py') {
  if (Get-Command $c -ErrorAction SilentlyContinue) { Ok $c } else { Ko "$c introuvable : ferme PowerShell, rouvre-le et relance ce script" }
}

Etape '2/7 Reglages Git et recuperation du projet'
git config --global core.longpaths true
git config --global core.autocrlf false
git config --global pull.rebase true
New-Item -ItemType Directory -Force C:\Studio | Out-Null
if (-not (Test-Path C:\Studio\videos_longues\.git)) {
  Write-Host '  Une fenetre GitHub peut s''ouvrir pour te connecter.'
  git clone https://github.com/cours-avec-bruno/videos_longues.git C:\Studio\videos_longues
}
Set-Location C:\Studio\videos_longues
git fetch origin
git checkout claude/wizardly-archimedes-sapbhh
git pull
if (Test-Path package.json) { Ok 'projet dans C:\Studio\videos_longues' } else { Ko 'le projet n''a pas ete recupere (connexion GitHub ?)' }

Etape '3/7 Dependances du projet (npm)'
npm install
if ($LASTEXITCODE -eq 0) { Ok 'npm install' } else { Ko 'npm install a echoue' }

Etape '4/7 Carte graphique'
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
if ($LASTEXITCODE -ne 0) { Ko 'nvidia-smi ne repond pas : installe ou mets a jour le pilote NVIDIA, puis relance' }

Etape '5/7 PyTorch (version carte graphique) et Demucs - environ 3 Go a telecharger'
py -3.12 -m pip install --upgrade pip
py -3.12 -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
py -3.12 -m pip install demucs soundfile
py -3.12 -c "import torch; ok = torch.cuda.is_available(); print('  CUDA disponible :', ok); print('  Carte :', torch.cuda.get_device_name(0) if ok else '-')"

Etape '6/7 Autotest de l''outil d''analyse (image + son + separation)'
node shared/outils/analyser-reference/autotest.mjs --separer --demucs "py -3.12 -m demucs"

Etape '7/7 Rendu Remotion de test'
npx remotion render remotion/index.ts Test-Pipeline out/test-pipeline.mp4
if (Test-Path out\test-pipeline.mp4) { Ok 'rendu Remotion : out\test-pipeline.mp4' } else { Ko 'le rendu Remotion a echoue' }

Write-Host "`nTermine. Copie tout ce qui s'est affiche depuis le debut et envoie-le a Claude pour verification." -ForegroundColor Cyan
