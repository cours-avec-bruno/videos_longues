#!/usr/bin/env node
/**
 * analyser-reference : extrait d'une vidéo de référence de quoi l'analyser image par image.
 *
 *   npm run analyser-reference -- <lien YouTube | fichier vidéo> [options]
 *
 * Étapes : téléchargement (yt-dlp) → détection des changements de plan (FFmpeg)
 * → vignettes horodatées → planches contact → palette et rythme mesurés → resume.md.
 *
 * Sorties :
 *   .cache/references/<id>/                       vidéo, sous-titres, métadonnées (hors Git)
 *   docs/direction-artistique/extractions/<id>/   planches, plans.csv, palette, barcode, resume.md
 *
 * Aucune dépendance npm : uniquement Node ≥ 22, FFmpeg/FFprobe et (pour YouTube) yt-dlp.
 */
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const ICI = path.dirname(fileURLToPath(import.meta.url));
const RACINE = path.resolve(ICI, '../../..');
const POLICE = path.join(ICI, 'police', 'JetBrainsMono-Bold.ttf');

// ───────────────────────── Options ─────────────────────────

const AIDE = `
Usage : npm run analyser-reference -- <lien YouTube | fichier vidéo> [options]

Options :
  --id <nom>                 Nom du dossier de sortie (défaut : id YouTube ou nom du fichier)
  --seuil <0-1>              Score au-delà duquel un changement d'image est toujours une coupe (défaut 0.30)
  --seuil-bas <0-1>          Score minimal d'une coupe peu contrastée, retenue si elle tranche
                             nettement avec les images voisines (défaut 0.08)
  --colonnes <n>             Vignettes par ligne dans une planche (défaut 4)
  --lignes <n>               Lignes par planche (défaut 5)
  --largeur <px>             Largeur d'une vignette (défaut 400)
  --hauteur-max <px>         Résolution max téléchargée (défaut 720)
  --cookies-navigateur <nom> Passe les cookies d'un navigateur à yt-dlp si YouTube demande
                             une connexion (firefox recommandé ; ex. --cookies-navigateur firefox)
  --paralleles <n>           Extractions simultanées (défaut 4)
  --aide                     Affiche cette aide
`;

function lireOptions(argv) {
  const o = {
    source: null, id: null, seuil: 0.3, seuilBas: 0.08, colonnes: 4, lignes: 5, largeur: 400,
    hauteurMax: 720, cookies: null, paralleles: 4,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const val = () => {
      if (i + 1 >= argv.length) arreter(`L'option ${a} attend une valeur.`);
      return argv[++i];
    };
    switch (a) {
      case '--aide': case '--help': case '-h': console.log(AIDE); process.exit(0); break;
      case '--id': o.id = val(); break;
      case '--seuil': o.seuil = Number(val()); break;
      case '--seuil-bas': o.seuilBas = Number(val()); break;
      case '--colonnes': o.colonnes = parseInt(val(), 10); break;
      case '--lignes': o.lignes = parseInt(val(), 10); break;
      case '--largeur': o.largeur = parseInt(val(), 10); break;
      case '--hauteur-max': o.hauteurMax = parseInt(val(), 10); break;
      case '--cookies-navigateur': o.cookies = val(); break;
      case '--paralleles': o.paralleles = parseInt(val(), 10); break;
      default:
        if (a.startsWith('--')) arreter(`Option inconnue : ${a}\n${AIDE}`);
        if (o.source) arreter(`Une seule source à la fois (reçu « ${o.source} » et « ${a} »).`);
        o.source = a;
    }
  }
  if (!o.source) arreter(`Il manque le lien ou le fichier à analyser.\n${AIDE}`);
  if (!(o.seuil > 0 && o.seuil < 1)) arreter('--seuil doit être compris entre 0 et 1.');
  if (!(o.seuilBas > 0 && o.seuilBas <= o.seuil)) arreter('--seuil-bas doit être compris entre 0 et --seuil.');
  for (const k of ['colonnes', 'lignes', 'largeur', 'hauteurMax', 'paralleles']) {
    if (!(o[k] > 0)) arreter(`--${k} doit être un entier positif.`);
  }
  return o;
}

// ───────────────────────── Utilitaires ─────────────────────────

function arreter(message) {
  console.error(`\n✖ ${message}\n`);
  process.exit(1);
}

const etape = (m) => console.log(`\n▸ ${m}`);
const info = (m) => console.log(`  ${m}`);

/** Lance une commande sans shell (pas de problème d'échappement, Windows compris). */
function lancer(cmd, args, {cwd, onStderr, binaire = false} = {}) {
  return new Promise((resolve, reject) => {
    let p;
    try {
      p = spawn(cmd, args, {cwd, windowsHide: true});
    } catch (e) {
      reject(e);
      return;
    }
    const out = [];
    let err = '';
    p.stdout.on('data', (d) => out.push(d));
    p.stderr.on('data', (d) => {
      const s = d.toString();
      err += s;
      if (err.length > 200_000) err = err.slice(-100_000);
      if (onStderr) onStderr(s);
    });
    p.on('error', reject);
    p.on('close', (code) => {
      const stdout = binaire ? Buffer.concat(out) : Buffer.concat(out).toString();
      if (code === 0) resolve({stdout, stderr: err});
      else reject(Object.assign(new Error(`${cmd} a échoué (code ${code})\n${err.slice(-2000)}`), {code, stderr: err}));
    });
  });
}

async function verifierOutil(cmd, args, conseil) {
  try {
    await lancer(cmd, args);
  } catch (e) {
    if (e.code === 'ENOENT') arreter(`« ${cmd} » est introuvable.\n  ${conseil}`);
    throw e;
  }
}

/** Secondes → "mm:ss.d" (ou "h:mm:ss.d"). */
function tc(s, decimales = 1) {
  const neg = s < 0;
  const f = 10 ** decimales;
  s = Math.round(Math.abs(s) * f) / f; // arrondi d'abord : évite « 00:60 »
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = (s % 60).toFixed(decimales).padStart(decimales ? 3 + decimales : 2, '0');
  const mm = String(m).padStart(2, '0');
  return (neg ? '-' : '') + (h ? `${h}:${mm}:${sec}` : `${mm}:${sec}`);
}

const hex = ([r, g, b]) => '#' + [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('');
const luma = ([r, g, b]) => (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
function saturation([r, g, b]) {
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
  return mx === 0 ? 0 : (mx - mn) / mx;
}

function quantile(tri, q) {
  if (!tri.length) return 0;
  const pos = (tri.length - 1) * q;
  const b = Math.floor(pos);
  return tri[b] + (tri[Math.min(b + 1, tri.length - 1)] - tri[b]) * (pos - b);
}

/** Exécute des tâches asynchrones avec un nombre limité en parallèle. */
async function enParallele(taches, n, surProgression) {
  const resultats = new Array(taches.length);
  let suivant = 0, faits = 0;
  async function ouvrier() {
    while (suivant < taches.length) {
      const i = suivant++;
      resultats[i] = await taches[i]();
      faits++;
      if (surProgression) surProgression(faits, taches.length);
    }
  }
  await Promise.all(Array.from({length: Math.min(n, taches.length)}, ouvrier));
  return resultats;
}

function slug(s) {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60) || 'reference';
}

function idYouTube(url) {
  const m = url.match(/(?:youtu\.be\/|[?&]v=|\/shorts\/|\/embed\/|\/live\/)([A-Za-z0-9_-]{11})/);
  return m ? m[1] : null;
}

// ───────────────────────── Étape 1 : source ─────────────────────────

async function preparerSource(o, dossierCache) {
  const estUrl = /^https?:\/\//i.test(o.source);
  if (!estUrl) {
    const fichier = path.resolve(o.source);
    if (!fs.existsSync(fichier)) arreter(`Fichier introuvable : ${fichier}`);
    return {video: fichier, meta: {title: path.basename(fichier), webpage_url: null}, sousTitres: []};
  }

  await verifierOutil('yt-dlp', ['--version'],
    'Installe-le sous Windows avec : winget install --id yt-dlp.yt-dlp -e  (puis rouvre PowerShell).');

  const communs = ['--no-playlist', '--js-runtimes', 'node', '--newline', '--no-warnings'];
  if (o.cookies) communs.push('--cookies-from-browser', o.cookies);
  const sortie = path.join(dossierCache, 'video.%(ext)s');

  const dejaLa = fs.readdirSync(dossierCache).find((f) => /^video\.(mp4|mkv|webm)$/.test(f));
  if (dejaLa) {
    info(`Vidéo déjà téléchargée, réutilisée (${dejaLa}).`);
  } else {
    etape('Téléchargement de la vidéo (yt-dlp)…');
    const h = o.hauteurMax;
    // Image seule (pas de son) : plus léger, et suffisant pour l'analyse visuelle.
    const args = [...communs,
      '-f', `bv*[height<=${h}][vcodec^=avc1]/bv*[height<=${h}]/b[height<=${h}]/b`,
      '-o', sortie, '--write-info-json', o.source];
    let dernier = 0;
    try {
      await new Promise((resolve, reject) => {
        const p = spawn('yt-dlp', args, {windowsHide: true});
        let err = '';
        p.stdout.on('data', (d) => {
          const m = d.toString().match(/(\d+(?:\.\d+)?)%/);
          if (m && Number(m[1]) - dernier >= 10) { dernier = Number(m[1]); info(`${m[1]} %`); }
        });
        p.stderr.on('data', (d) => { err += d.toString(); });
        p.on('error', reject);
        p.on('close', (c) => (c === 0 ? resolve() : reject(new Error(err))));
      });
    } catch (e) {
      const msg = String(e.message || e);
      if (/confirm you.re not a bot|Sign in to confirm/i.test(msg)) {
        arreter("YouTube demande de prouver qu'on n'est pas un robot.\n" +
          '  Relance avec les cookies de ton navigateur : --cookies-navigateur firefox\n' +
          '  (sous Windows, Firefox marche mieux que Chrome pour cette option).');
      }
      if (/no such option.*js-runtimes/i.test(msg)) {
        arreter('Ta version de yt-dlp est trop ancienne. Mets-la à jour : yt-dlp -U  (ou winget upgrade yt-dlp.yt-dlp)');
      }
      arreter(`Le téléchargement a échoué :\n${msg.slice(-1500)}`);
    }
  }

  // Sous-titres : étape séparée et facultative (YouTube limite souvent ce téléchargement).
  if (!fs.readdirSync(dossierCache).some((f) => f.endsWith('.srt'))) {
    etape('Sous-titres (facultatif)…');
    try {
      await lancer('yt-dlp', [...communs, '--skip-download', '--write-subs', '--write-auto-subs',
        '--sub-langs', 'fr,fr-orig,fr-FR,en,en-orig', '--convert-subs', 'srt', '-o', sortie, o.source]);
      const n = fs.readdirSync(dossierCache).filter((f) => f.endsWith('.srt')).length;
      info(n ? `${n} fichier(s) de sous-titres.` : 'Aucun sous-titre disponible.');
    } catch {
      info('Sous-titres non récupérés (pas grave : l\'analyse continue sans).');
    }
  }

  const fichiers = fs.readdirSync(dossierCache);
  const video = fichiers.find((f) => /^video\.(mp4|mkv|webm)$/.test(f));
  if (!video) arreter('Téléchargement terminé mais aucune vidéo trouvée dans le cache.');
  const infoJson = fichiers.find((f) => f.endsWith('.info.json'));
  const meta = infoJson ? JSON.parse(fs.readFileSync(path.join(dossierCache, infoJson), 'utf8')) : {};
  const sousTitres = fichiers.filter((f) => f.endsWith('.srt')).map((f) => path.join(dossierCache, f));
  return {video: path.join(dossierCache, video), meta, sousTitres};
}

// ───────────────────────── Étape 2 : détection des plans ─────────────────────────

async function sonder(video) {
  const {stdout} = await lancer('ffprobe', [
    '-v', 'error', '-select_streams', 'v:0',
    '-show_entries', 'stream=width,height,r_frame_rate:format=duration', '-of', 'json', video,
  ]);
  const j = JSON.parse(stdout);
  const s = j.streams?.[0] || {};
  const [n, d] = String(s.r_frame_rate || '0/1').split('/').map(Number);
  return {duree: Number(j.format?.duration) || 0, largeur: s.width, hauteur: s.height, fps: d ? n / d : 0};
}

// Paramètres de la détection des transitions progressives (fondus), calibrés sur des films réels.
const FONDU_FPS = 4;          // images échantillonnées par seconde
const FONDU_FENETRE = 4;      // comparaison avec l'image 1 s plus tôt
const FONDU_NIVEAUX = 6;      // niveaux par canal (racine carrée : plus fin dans les ombres)
const FONDU_SEUIL = 0.7;      // distance d'histogramme (0-2) à partir de laquelle on parle de transition
const FONDU_SUPPRESSION = 4;  // un seul pic retenu par ±1 s

function histogramme(px) {
  const L = FONDU_NIVEAUX, h = new Float64Array(L * L * L);
  const n = px.length / 3;
  const q = (v) => Math.min(L - 1, Math.floor(Math.sqrt(v / 255) * L));
  for (let i = 0; i < px.length; i += 3) h[q(px[i]) * L * L + q(px[i + 1]) * L + q(px[i + 2])] += 1 / n;
  return h;
}

/**
 * Détecte les changements de plan en une seule lecture de la vidéo, par deux méthodes :
 *
 * 1. Coupes franches (précision à l'image) — score de changement FFmpeg entre images successives :
 *    - score ≥ seuil → coupe ;
 *    - score ≥ seuilBas ET ≥ 5 × la moyenne des voisines (±0,5 s) → coupe peu contrastée
 *      (ex. raccord entre deux images sombres), sans réagir aux mouvements continus.
 * 2. Transitions progressives (fondus enchaînés, fondus au noir, transitions floues) :
 *    distance entre histogrammes de couleur à 1 s d'écart ; un pic au-dessus de FONDU_SEUIL
 *    marque une transition, placée au milieu de la fenêtre. Ignorée si une coupe franche est à ±0,75 s.
 */
async function detecterCoupes(video, seuil, seuilBas, duree) {
  const scores = [];
  const histos = [];
  const tailleImage = 64 * 36 * 3;
  let tampon = Buffer.alloc(0);
  let tCourant = null, reste = '', dernierPct = -10;

  await new Promise((resolve, reject) => {
    const p = spawn('ffmpeg', [
      '-hide_banner', '-nostdin', '-i', video, '-an', '-sn', '-dn',
      '-filter_complex',
      '[0:v]scale=320:-2,split[a][b];' +
      '[a]format=rgb24,select=\'gte(scene,0)\',metadata=print:key=lavfi.scene_score[sc];' +
      `[b]fps=${FONDU_FPS},scale=64:36:flags=area,format=rgb24[hi]`,
      '-map', '[sc]', '-f', 'null', '-',
      '-map', '[hi]', '-f', 'rawvideo', 'pipe:1',
    ], {windowsHide: true});
    let err = '';
    p.stdout.on('data', (d) => {
      tampon = tampon.length ? Buffer.concat([tampon, d]) : d;
      let o = 0;
      while (tampon.length - o >= tailleImage) { histos.push(histogramme(tampon.subarray(o, o + tailleImage))); o += tailleImage; }
      tampon = tampon.subarray(o);
    });
    p.stderr.on('data', (d) => {
      const s = d.toString();
      err = (err + s).slice(-20000);
      const lignes = (reste + s).split(/\r?\n|\r/);
      reste = lignes.pop();
      for (const l of lignes) {
        const pt = l.match(/pts_time:\s*([\d.]+)/);
        if (pt) { tCourant = Number(pt[1]); continue; }
        const sc = l.match(/lavfi\.scene_score=([\d.]+)/);
        if (sc && tCourant !== null) { scores.push([tCourant, Number(sc[1])]); tCourant = null; continue; }
        const t = l.match(/time=(\d+):(\d+):([\d.]+)/);
        if (t && duree) {
          const pct = Math.floor((+t[1] * 3600 + +t[2] * 60 + +t[3]) / duree * 100);
          if (pct - dernierPct >= 10) { dernierPct = pct; info(`${pct} % analysé`); }
        }
      }
    });
    p.on('error', reject);
    p.on('close', (c) => (c === 0 ? resolve() : reject(new Error(`ffmpeg a échoué (code ${c})\n${err.slice(-2000)}`))));
  });

  // 1. Coupes franches
  const franches = [];
  let g = 0, d = 0, somme = 0; // fenêtre glissante ±0,5 s
  for (let i = 0; i < scores.length; i++) {
    const [t, s] = scores[i];
    while (d < scores.length && scores[d][0] <= t + 0.5) somme += scores[d++][1];
    while (g < d && scores[g][0] < t - 0.5) somme -= scores[g++][1];
    const voisines = d - g - 1;
    const moyenne = voisines > 0 ? (somme - s) / voisines : 0;
    if (s >= seuil || (s >= seuilBas && s >= 5 * moyenne + 0.01)) franches.push(t);
  }

  // 2. Transitions progressives
  const W = FONDU_FENETRE, dist = new Float64Array(histos.length);
  for (let t = W; t < histos.length; t++) {
    let s = 0; const a = histos[t], b = histos[t - W];
    for (let k = 0; k < a.length; k++) s += Math.abs(a[k] - b[k]);
    dist[t] = s;
  }
  const progressives = [];
  for (let t = W; t < dist.length; t++) {
    if (dist[t] < FONDU_SEUIL) continue;
    let max = true;
    for (let k = Math.max(W, t - FONDU_SUPPRESSION); k <= Math.min(dist.length - 1, t + FONDU_SUPPRESSION); k++) {
      if (dist[k] > dist[t] || (dist[k] === dist[t] && k < t)) { max = false; break; }
    }
    if (!max) continue;
    const centre = (t - W / 2) / FONDU_FPS;
    if (!franches.some((f) => Math.abs(f - centre) <= 0.75)) progressives.push(centre);
  }
  info(`${franches.length} coupes franches, ${progressives.length} transitions progressives (fondus).`);
  return {coupes: [...franches, ...progressives], franches, progressives};
}

/** Transforme une liste de coupes en plans, en fusionnant les « coupes » trop rapprochées (flashs). */
function construirePlans(coupes, duree, minDuree = 0.12) {
  const bornes = [0];
  for (const c of [...new Set(coupes)].sort((a, b) => a - b)) {
    if (c - bornes[bornes.length - 1] >= minDuree && duree - c >= minDuree) bornes.push(c);
  }
  bornes.push(duree);
  const plans = [];
  for (let i = 0; i < bornes.length - 1; i++) {
    plans.push({n: i + 1, debut: bornes[i], fin: bornes[i + 1], duree: bornes[i + 1] - bornes[i]});
  }
  return plans;
}

// ───────────────────────── Étape 3 : vignettes ─────────────────────────

/** Nombre d'images prises dans un plan : 1, plus une toutes les ~5 s pour voir le mouvement (max 4). */
function instantsDuPlan(p) {
  const n = Math.min(4, 1 + Math.floor(p.duree / 5));
  return Array.from({length: n}, (_, i) => p.debut + p.duree * (i + 0.5) / n);
}

async function extraireVignettes(video, plans, o, dossierTravail, dossierVignettes) {
  const L = o.largeur;
  const H = Math.round(L * 9 / 16 / 2) * 2;
  const bandeau = Math.max(20, Math.round(H * 0.11));
  const taillePolice = Math.round(bandeau * 0.62);
  fs.copyFileSync(POLICE, path.join(dossierTravail, 'police.ttf'));

  const travaux = [];
  for (const p of plans) {
    const instants = instantsDuPlan(p);
    instants.forEach((t, k) => travaux.push({p, t, k, total: instants.length}));
  }

  const taches = travaux.map((w, i) => async () => {
    const num = String(i + 1).padStart(5, '0');
    const etiquette = `P${String(w.p.n).padStart(3, '0')}` +
      (w.total > 1 ? ` ${w.k + 1}/${w.total}` : '') +
      `  ${tc(w.t)}  (${w.p.duree.toFixed(1)}s)`;
    const fichierTexte = `lbl-${num}.txt`;
    fs.writeFileSync(path.join(dossierTravail, fichierTexte), etiquette);
    const filtre =
      // L'étiquette est placée SOUS l'image (bandeau ajouté), pour ne masquer ni sous-titres ni textes à l'écran.
      `[0:v]scale=${L}:${H}:force_original_aspect_ratio=decrease,pad=${L}:${H}:(ow-iw)/2:(oh-ih)/2:color=black,split[a][b];` +
      `[a]pad=${L}:${H + bandeau}:0:0:color=0x1c1c1c,` +
      `drawtext=fontfile=police.ttf:textfile=${fichierTexte}:fontcolor=white:fontsize=${taillePolice}:x=8:y=${H}+(${bandeau}-th)/2[v];` +
      `[b]scale=32:18:flags=area,format=rgb24[c]`;
    const {stdout} = await lancer('ffmpeg', [
      '-hide_banner', '-nostdin', '-loglevel', 'error',
      '-ss', w.t.toFixed(3), '-i', video, '-frames:v', '1',
      '-filter_complex', filtre,
      '-map', '[v]', '-q:v', '3', '-y', path.join(dossierVignettes, `${num}.jpg`),
      '-map', '[c]', '-frames:v', '1', '-f', 'rawvideo', 'pipe:1',
    ], {cwd: dossierTravail, binaire: true});
    fs.rmSync(path.join(dossierTravail, fichierTexte), {force: true});
    return {plan: w.p.n, k: w.k, t: w.t, pixels: stdout.length >= 32 * 18 * 3 ? stdout : null};
  });

  let dernier = -10;
  const res = await enParallele(taches, o.paralleles, (f, tot) => {
    const pct = Math.floor(f / tot * 100);
    if (pct - dernier >= 10) { dernier = pct; info(`${f}/${tot} vignettes`); }
  });
  return {vignettes: res, L, H};
}

// ───────────────────────── Étape 4 : planches ─────────────────────────

async function construirePlanches(dossierVignettes, dossierPlanches, o, nb) {
  const parPlanche = o.colonnes * o.lignes;
  await lancer('ffmpeg', [
    '-hide_banner', '-nostdin', '-loglevel', 'error',
    '-framerate', '1', '-i', path.join(dossierVignettes, '%05d.jpg'),
    '-vf', `tile=${o.colonnes}x${o.lignes}:padding=6:margin=6:color=0x111111`,
    '-q:v', '3', '-y', path.join(dossierPlanches, 'planche-%03d.jpg'),
  ]);
  const planches = fs.readdirSync(dossierPlanches).filter((f) => f.endsWith('.jpg')).sort();
  return {planches, parPlanche, attendues: Math.ceil(nb / parPlanche)};
}

// ───────────────────────── Étape 5 : couleurs ─────────────────────────

/** k-means déterministe (initialisation k-means++ avec graine fixe), pondéré. */
function kmeans(points, poids, k, iterations = 25) {
  let graine = 42;
  const alea = () => ((graine = (graine * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const d2 = (a, b) => (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2;
  const centres = [points[Math.floor(alea() * points.length)]];
  while (centres.length < k) {
    const dist = points.map((p, i) => Math.min(...centres.map((c) => d2(p, c))) * poids[i]);
    const tot = dist.reduce((a, b) => a + b, 0);
    if (tot === 0) break;
    let r = alea() * tot, i = 0;
    while (r > dist[i]) r -= dist[i++];
    centres.push(points[Math.min(i, points.length - 1)]);
  }
  const affect = new Array(points.length).fill(0);
  for (let it = 0; it < iterations; it++) {
    for (let i = 0; i < points.length; i++) {
      let best = 0, bd = Infinity;
      for (let c = 0; c < centres.length; c++) { const d = d2(points[i], centres[c]); if (d < bd) { bd = d; best = c; } }
      affect[i] = best;
    }
    const somme = centres.map(() => [0, 0, 0, 0]);
    for (let i = 0; i < points.length; i++) {
      const s = somme[affect[i]], w = poids[i];
      s[0] += points[i][0] * w; s[1] += points[i][1] * w; s[2] += points[i][2] * w; s[3] += w;
    }
    for (let c = 0; c < centres.length; c++) if (somme[c][3] > 0) centres[c] = somme[c].slice(0, 3).map((v) => v / somme[c][3]);
  }
  const masse = centres.map(() => 0);
  affect.forEach((c, i) => { masse[c] += poids[i]; });
  const tot = masse.reduce((a, b) => a + b, 0) || 1;
  return centres.map((c, i) => ({rgb: c, part: masse[i] / tot})).filter((c) => c.part > 0).sort((a, b) => b.part - a.part);
}

function analyserCouleurs(plans, vignettes) {
  const points = [], poids = [];
  for (const p of plans) {
    const vs = vignettes.filter((v) => v.plan === p.n && v.pixels);
    const acc = [0, 0, 0]; let n = 0;
    for (const v of vs) {
      for (let i = 0; i + 2 < v.pixels.length; i += 3) {
        const px = [v.pixels[i], v.pixels[i + 1], v.pixels[i + 2]];
        acc[0] += px[0]; acc[1] += px[1]; acc[2] += px[2]; n++;
        points.push(px); poids.push(p.duree / (vs.length * 576));
      }
    }
    p.couleur = n ? acc.map((x) => x / n) : [0, 0, 0];
    p.luma = luma(p.couleur);
    p.saturation = saturation(p.couleur);
  }
  // Sous-échantillonne pour garder le k-means rapide sur les longues vidéos.
  const pas = Math.max(1, Math.floor(points.length / 60000));
  const P = [], W = [];
  for (let i = 0; i < points.length; i += pas) { P.push(points[i]); W.push(poids[i]); }
  return P.length ? kmeans(P, W, 8) : [];
}

/** Écrit une image PPM (P6) puis la convertit en PNG avec FFmpeg. */
async function ecrireImage(fichierPng, largeur, hauteur, pixel) {
  const entete = Buffer.from(`P6\n${largeur} ${hauteur}\n255\n`);
  const corps = Buffer.alloc(largeur * hauteur * 3);
  for (let y = 0; y < hauteur; y++) for (let x = 0; x < largeur; x++) {
    const [r, g, b] = pixel(x, y);
    const i = (y * largeur + x) * 3; corps[i] = r; corps[i + 1] = g; corps[i + 2] = b;
  }
  const ppm = fichierPng.replace(/\.png$/, '.ppm');
  fs.writeFileSync(ppm, Buffer.concat([entete, corps]));
  await lancer('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-i', ppm, '-y', fichierPng]);
  fs.rmSync(ppm, {force: true});
}

async function imagesCouleurs(plans, palette, duree, dossierSortie) {
  // « Barcode » : chaque plan est une bande de sa couleur moyenne, largeur ∝ durée.
  const W = 1600, Hb = 140;
  const colonnes = new Array(W);
  for (let x = 0; x < W; x++) {
    const t = (x + 0.5) / W * duree;
    const p = plans.find((q) => t >= q.debut && t < q.fin) || plans[plans.length - 1];
    colonnes[x] = p.couleur;
  }
  await ecrireImage(path.join(dossierSortie, 'barcode.png'), W, Hb, (x) => colonnes[x]);

  // Nuancier : bandes proportionnelles à la part de chaque couleur.
  const Wp = 1200, Hp = 120;
  const bandes = []; let cumul = 0;
  for (const c of palette) { bandes.push({fin: cumul + c.part, rgb: c.rgb}); cumul += c.part; }
  await ecrireImage(path.join(dossierSortie, 'palette.png'), Wp, Hp, (x) => {
    const f = (x + 0.5) / Wp;
    return (bandes.find((b) => f <= b.fin) || bandes[bandes.length - 1]).rgb;
  });
}

// ───────────────────────── Étape 6 : rapport ─────────────────────────

function barre(valeur, max, largeur = 30) {
  const n = max ? Math.round(valeur / max * largeur) : 0;
  return '█'.repeat(n) + '·'.repeat(Math.max(0, largeur - n));
}

function rapport({o, meta, sonde, plans, palette, planches, parPlanche, vignettes, idRef, sousTitres}) {
  const durees = plans.map((p) => p.duree).sort((a, b) => a - b);
  const total = sonde.duree;
  const moy = total / plans.length;
  const lignes = [];
  const titre = meta.title || idRef;
  lignes.push(`# Extraction · ${titre}`, '');
  lignes.push('> Généré automatiquement par `shared/outils/analyser-reference`. Données **mesurées** sur la vidéo.');
  lignes.push('> L\'interprétation (DA, intentions) se fait dans `../../analyses/`.', '');

  lignes.push('## Source', '');
  lignes.push('| | |', '|---|---|');
  if (meta.webpage_url) lignes.push(`| Lien | ${meta.webpage_url} |`);
  if (meta.uploader || meta.channel) lignes.push(`| Chaîne | ${meta.channel || meta.uploader} |`);
  if (meta.upload_date) lignes.push(`| Publiée le | ${meta.upload_date.replace(/(\d{4})(\d{2})(\d{2})/, '$3/$2/$1')} |`);
  lignes.push(`| Durée | ${tc(total, 0)} |`);
  lignes.push(`| Résolution analysée | ${sonde.largeur}×${sonde.hauteur} @ ${sonde.fps.toFixed(2)} i/s |`);
  lignes.push(`| Seuils de détection | ${o.seuil} (franche) / ${o.seuilBas} (adaptative) |`);
  lignes.push(`| Extrait le | ${new Date().toISOString().slice(0, 10)} |`, '');

  if (Array.isArray(meta.chapters) && meta.chapters.length) {
    lignes.push('## Chapitres YouTube', '', '| Début | Chapitre |', '|---|---|');
    for (const c of meta.chapters) lignes.push(`| ${tc(c.start_time, 0)} | ${c.title} |`);
    lignes.push('');
  }

  lignes.push('## Rythme du montage', '');
  lignes.push('| Mesure | Valeur |', '|---|---|');
  lignes.push(`| Plans détectés | ${plans.length} |`);
  lignes.push(`| Durée moyenne d'un plan | ${moy.toFixed(1)} s |`);
  lignes.push(`| Médiane | ${quantile(durees, 0.5).toFixed(1)} s |`);
  lignes.push(`| 10 % des plans durent moins de | ${quantile(durees, 0.1).toFixed(1)} s |`);
  lignes.push(`| 10 % des plans durent plus de | ${quantile(durees, 0.9).toFixed(1)} s |`);
  lignes.push(`| Coupes par minute (moyenne) | ${(plans.length / (total / 60)).toFixed(1)} |`);
  const nProg = plans.filter((p) => p.entree === 'progressive').length;
  lignes.push(`| Transitions progressives (fondus, enchaînés…) | ${nProg} sur ${Math.max(0, plans.length - 1)} (${plans.length > 1 ? (nProg / (plans.length - 1) * 100).toFixed(0) : 0} %) |`, '');
  lignes.push('> Les transitions progressives sont placées au milieu du fondu : la durée des plans qui les entourent est approximative (± 0,5 s).', '');

  const tranche = total > 1800 ? 300 : total > 600 ? 120 : 60;
  lignes.push(`### Coupes par minute, par tranche de ${tranche / 60} min`, '', '```');
  const parTranche = [];
  for (let t = 0; t < total; t += tranche) {
    const n = plans.filter((p) => p.debut >= t && p.debut < t + tranche).length;
    parTranche.push({t, cpm: n / (Math.min(tranche, total - t) / 60)});
  }
  const maxCpm = Math.max(...parTranche.map((x) => x.cpm));
  for (const x of parTranche) lignes.push(`${tc(x.t, 0).padStart(8)}  ${barre(x.cpm, maxCpm)}  ${x.cpm.toFixed(1)}`);
  lignes.push('```', '');

  const parDuree = [...plans].sort((a, b) => a.duree - b.duree);
  lignes.push('### Les 10 plans les plus longs (moments contemplatifs)', '', '| Plan | Début | Durée |', '|---|---|---|');
  for (const p of parDuree.slice(-10).reverse()) lignes.push(`| P${String(p.n).padStart(3, '0')} | ${tc(p.debut)} | ${p.duree.toFixed(1)} s |`);
  lignes.push('');
  // Rafales : fenêtres de 10 s contenant le plus de coupes.
  const rafales = [];
  for (const p of plans) {
    const n = plans.filter((q) => q.debut >= p.debut && q.debut < p.debut + 10).length;
    if (n >= 6) rafales.push({debut: p.debut, n});
  }
  const rafalesUniques = [];
  for (const r of rafales.sort((a, b) => b.n - a.n)) {
    if (!rafalesUniques.some((u) => Math.abs(u.debut - r.debut) < 10)) rafalesUniques.push(r);
    if (rafalesUniques.length >= 10) break;
  }
  if (rafalesUniques.length) {
    lignes.push('### Rafales de montage (≥ 6 coupes en 10 s)', '', '| Début | Coupes en 10 s |', '|---|---|');
    for (const r of rafalesUniques.sort((a, b) => a.debut - b.debut)) lignes.push(`| ${tc(r.debut)} | ${r.n} |`);
    lignes.push('');
  }

  lignes.push('## Couleur', '');
  lignes.push('![Palette](palette.png)', '');
  lignes.push('Palette dominante de la vidéo entière (k-means sur les vignettes, pondéré par la durée des plans) :', '');
  lignes.push('| Couleur | Part | Luminance | Saturation |', '|---|---|---|---|');
  for (const c of palette) lignes.push(`| \`${hex(c.rgb)}\` | ${(c.part * 100).toFixed(1)} % | ${(luma(c.rgb) * 100).toFixed(0)} % | ${(saturation(c.rgb) * 100).toFixed(0)} % |`);
  lignes.push('');
  const pond = (f) => plans.reduce((a, p) => a + f(p) * p.duree, 0) / total;
  const sombres = plans.filter((p) => p.luma < 0.15).reduce((a, p) => a + p.duree, 0) / total;
  lignes.push(`- Luminance moyenne : **${(pond((p) => p.luma) * 100).toFixed(0)} %**`);
  lignes.push(`- Temps passé sur des plans très sombres (luminance < 15 %) : **${(sombres * 100).toFixed(0)} %**`);
  lignes.push(`- Saturation moyenne : **${(pond((p) => p.saturation) * 100).toFixed(0)} %**`, '');
  lignes.push('Évolution de la couleur dans le temps (chaque plan = sa couleur moyenne, largeur ∝ durée) :', '');
  lignes.push('![Barcode](barcode.png)', '');

  lignes.push('## Planches contact', '');
  lignes.push(`${vignettes.length} vignettes pour ${plans.length} plans : une par plan, plus une toutes les ~5 s dans les plans longs (notées \`2/3\`…), pour voir le mouvement.`);
  lignes.push('Étiquette de chaque vignette : `numéro de plan · timecode de l\'image · (durée du plan)`.', '');
  lignes.push('| Planche | Vignettes |', '|---|---|');
  planches.forEach((f, i) => {
    const a = vignettes[i * parPlanche], b = vignettes[Math.min((i + 1) * parPlanche, vignettes.length) - 1];
    lignes.push(`| [${f}](planches/${f}) | ${a ? tc(a.t, 0) : ''} → ${b ? tc(b.t, 0) : ''} |`);
  });
  lignes.push('');
  lignes.push('Détail plan par plan : [`plans.csv`](plans.csv).', '');

  lignes.push('## Fichiers hors Git (sur la machine qui a lancé l\'extraction)', '');
  lignes.push(`- Vidéo et métadonnées : \`.cache/references/${idRef}/\``);
  if (sousTitres.length) lignes.push(`- Sous-titres : ${sousTitres.map((s) => `\`${path.relative(RACINE, s).replace(/\\/g, '/')}\``).join(', ')}`);
  lignes.push('');
  return lignes.join('\n');
}

// ───────────────────────── Programme principal ─────────────────────────

async function principal() {
  const o = lireOptions(process.argv.slice(2));
  const debutChrono = Date.now();

  await verifierOutil('ffmpeg', ['-version'], 'Installe-le avec : winget install --id Gyan.FFmpeg -e');
  await verifierOutil('ffprobe', ['-version'], 'Il est fourni avec FFmpeg : winget install --id Gyan.FFmpeg -e');

  const estUrl = /^https?:\/\//i.test(o.source);
  const idRef = slug(o.id || (estUrl ? idYouTube(o.source) || o.source : path.parse(o.source).name));
  const dossierCache = path.join(RACINE, '.cache', 'references', idRef);
  const dossierSortie = path.join(RACINE, 'docs', 'direction-artistique', 'extractions', idRef);
  const dossierVignettes = path.join(dossierCache, 'vignettes');
  const dossierTravail = path.join(dossierCache, 'travail');
  const dossierPlanches = path.join(dossierSortie, 'planches');
  for (const d of [dossierCache, dossierVignettes, dossierTravail, dossierSortie, dossierPlanches]) fs.mkdirSync(d, {recursive: true});
  // Repart de zéro pour les sorties (la vidéo téléchargée, elle, est conservée).
  for (const d of [dossierVignettes, dossierPlanches]) for (const f of fs.readdirSync(d)) fs.rmSync(path.join(d, f), {force: true});

  console.log(`\nAnalyse de référence « ${idRef} »`);
  const {video, meta, sousTitres} = await preparerSource(o, dossierCache);

  etape('Lecture de la vidéo…');
  const sonde = await sonder(video);
  if (!sonde.duree) arreter('Impossible de lire la durée de la vidéo.');
  info(`${tc(sonde.duree, 0)} · ${sonde.largeur}×${sonde.hauteur} · ${sonde.fps.toFixed(2)} i/s`);

  etape(`Détection des changements de plan (seuils ${o.seuil} / ${o.seuilBas})…`);
  const {coupes, progressives} = await detecterCoupes(video, o.seuil, o.seuilBas, sonde.duree);
  const plans = construirePlans(coupes, sonde.duree);
  for (const p of plans) {
    p.entree = p.n === 1 ? 'début' : progressives.some((c) => Math.abs(c - p.debut) < 0.01) ? 'progressive' : 'franche';
  }
  info(`${plans.length} plans détectés.`);

  etape('Extraction des vignettes…');
  const {vignettes} = await extraireVignettes(video, plans, o, dossierTravail, dossierVignettes);

  etape('Assemblage des planches contact…');
  const {planches, parPlanche, attendues} = await construirePlanches(dossierVignettes, dossierPlanches, o, vignettes.length);
  if (planches.length !== attendues) info(`Attention : ${planches.length} planches produites, ${attendues} attendues.`);
  info(`${planches.length} planches.`);

  etape('Analyse des couleurs…');
  const palette = analyserCouleurs(plans, vignettes);
  await imagesCouleurs(plans, palette, sonde.duree, dossierSortie);

  etape('Écriture des résultats…');
  const csv = ['plan;debut;fin;duree_s;debut_s;transition_entree;couleur_moyenne;luminance;saturation'];
  for (const p of plans) {
    csv.push([p.n, tc(p.debut), tc(p.fin), p.duree.toFixed(2), p.debut.toFixed(2), p.entree, hex(p.couleur),
      p.luma.toFixed(3), p.saturation.toFixed(3)].join(';'));
  }
  fs.writeFileSync(path.join(dossierSortie, 'plans.csv'), csv.join('\n') + '\n');
  fs.writeFileSync(path.join(dossierSortie, 'resume.md'),
    rapport({o, meta, sonde, plans, palette, planches, parPlanche, vignettes, idRef, sousTitres}));
  fs.rmSync(dossierTravail, {recursive: true, force: true});

  const rel = path.relative(RACINE, dossierSortie).replace(/\\/g, '/');
  console.log(`\n✔ Terminé en ${((Date.now() - debutChrono) / 1000).toFixed(0)} s → ${rel}/resume.md\n`);
}

principal().catch((e) => arreter(e.stack || String(e)));
