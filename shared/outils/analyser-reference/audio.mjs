/**
 * Module SON de analyser-reference : mesures objectives de la bande sonore.
 *
 *  - Sonie EBU R128 (intégrée, plage dynamique, crête vraie) et courbe court terme.
 *  - Attaques sonores (flux spectral) → tempo estimé, synchronisation des coupes avec le son.
 *  - Événements marquants (impacts, whooshes, chocs) : saut d'énergie soudain d'un son « bruité »
 *    (forte planéité spectrale), non périodique (donc pas la batterie d'une musique).
 *  - Voix : séparation IA optionnelle (Demucs) → présence de la voix, respirations, ducking ;
 *    sinon, sous-titres YouTube comme repère approximatif.
 *  - Silences, et « frises » : images alignées sur le temps (sonie, voix, spectrogramme, coupes, impacts).
 *
 * Claude ne peut pas écouter : ces mesures et ces images sont ce qu'il lit à la place.
 */
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {POLICE, etape, info, lancer, tc, quantile, ecrireImage, barre} from './commun.mjs';

const SR = 22050;          // fréquence d'analyse (Hz)
const HOP = 441;           // pas d'analyse : 20 ms
const NFFT = 1024;         // fenêtre FFT : ~46 ms
const FPS = SR / HOP;      // 50 mesures par seconde

// ───────────────────────── Récupération de l'audio ─────────────────────────

async function aUnFluxAudio(fichier) {
  try {
    const {stdout} = await lancer('ffprobe', ['-v', 'error', '-select_streams', 'a:0',
      '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', fichier]);
    return stdout.trim().length > 0;
  } catch {
    return false;
  }
}

async function obtenirAudio({o, estUrl, video, dossierCache}) {
  if (await aUnFluxAudio(video)) return video;
  if (!estUrl) return null;
  const deja = fs.readdirSync(dossierCache).find((f) => /^audio\.\w+$/.test(f) && !f.endsWith('.part'));
  if (deja) { info(`Audio déjà téléchargé, réutilisé (${deja}).`); return path.join(dossierCache, deja); }
  info('Téléchargement de la piste audio (yt-dlp)…');
  const args = ['--no-playlist', '--js-runtimes', 'node', '--no-warnings', '-f', 'ba/b',
    '-o', path.join(dossierCache, 'audio.%(ext)s')];
  if (o.cookies) args.push('--cookies-from-browser', o.cookies);
  args.push(o.source);
  try {
    await lancer('yt-dlp', args);
  } catch (e) {
    info(`Audio non récupéré : ${String(e.message).split('\n').slice(-3).join(' ')}`);
    return null;
  }
  const f = fs.readdirSync(dossierCache).find((x) => /^audio\.\w+$/.test(x));
  return f ? path.join(dossierCache, f) : null;
}

// ───────────────────────── Sonie EBU R128 ─────────────────────────

async function mesurerSonie(fichier, duree) {
  const t = [], M = [], S = [];
  let resume = '', reste = '', dernierPct = -20;
  const {stderr} = await lancer('ffmpeg', ['-hide_banner', '-nostdin', '-i', fichier, '-vn', '-sn',
    '-af', 'ebur128=peak=true:framelog=info', '-f', 'null', '-'], {
    onStderr: (s) => {
      const lignes = (reste + s).split(/\r?\n|\r/);
      reste = lignes.pop();
      for (const l of lignes) {
        const m = l.match(/t:\s*([\d.]+)\s.*?M:\s*(-?[\d.]+)\s+S:\s*(-?[\d.]+)/);
        if (m) {
          t.push(+m[1]); M.push(+m[2]); S.push(+m[3]);
          const pct = Math.floor(+m[1] / duree * 100);
          if (pct - dernierPct >= 20) { dernierPct = pct; info(`sonie : ${pct} %`); }
        }
      }
    },
  });
  resume = stderr.slice(stderr.lastIndexOf('Summary:'));
  const lire = (re) => { const m = resume.match(re); return m ? Number(m[1]) : null; };
  return {
    t, M, S,
    I: lire(/I:\s*(-?[\d.]+) LUFS/),
    LRA: lire(/LRA:\s*(-?[\d.]+) LU/),
    TP: lire(/True peak:\s*Peak:\s*(-?[\d.]+) dBFS/),
  };
}

// ───────────────────────── Analyse spectrale (flux) ─────────────────────────

function preparerFFT(n) {
  const bits = Math.log2(n);
  const rev = new Uint32Array(n);
  for (let i = 0; i < n; i++) { let r = 0; for (let b = 0; b < bits; b++) r |= ((i >> b) & 1) << (bits - 1 - b); rev[i] = r; }
  const cos = new Float64Array(n / 2), sin = new Float64Array(n / 2);
  for (let i = 0; i < n / 2; i++) { cos[i] = Math.cos(-2 * Math.PI * i / n); sin[i] = Math.sin(-2 * Math.PI * i / n); }
  const hann = new Float64Array(n);
  for (let i = 0; i < n; i++) hann[i] = 0.5 - 0.5 * Math.cos(2 * Math.PI * i / n);
  return {n, rev, cos, sin, hann};
}

function fft(F, re, im) {
  const {n, rev, cos, sin} = F;
  for (let i = 0; i < n; i++) { const j = rev[i]; if (j > i) { let t = re[i]; re[i] = re[j]; re[j] = t; t = im[i]; im[i] = im[j]; im[j] = t; } }
  for (let taille = 2; taille <= n; taille <<= 1) {
    const demi = taille >> 1, pas = n / taille;
    for (let i = 0; i < n; i += taille) {
      for (let k = 0; k < demi; k++) {
        const c = cos[k * pas], s = sin[k * pas];
        const a = i + k, b = a + demi;
        const tr = re[b] * c - im[b] * s, ti = re[b] * s + im[b] * c;
        re[b] = re[a] - tr; im[b] = im[a] - ti; re[a] += tr; im[a] += ti;
      }
    }
  }
}

/**
 * Décode un fichier en mono 22 050 Hz et calcule, toutes les 20 ms :
 *  - niveau RMS (dBFS), flux spectral (attaques), planéité spectrale (son bruité vs tonal).
 * Traitement en flux : la mémoire reste faible même pour une vidéo de plusieurs heures.
 */
async function analyserSignal(fichier) {
  const F = preparerFFT(NFFT);
  const re = new Float64Array(NFFT), im = new Float64Array(NFFT);
  const nb = NFFT / 2;
  let precedent = new Float64Array(nb), courant = new Float64Array(nb);
  const rms = [], flux = [], plat = [];
  let tampon = new Float32Array(0);
  let resteOctets = Buffer.alloc(0);

  const traiter = (fin) => {
    let pos = 0;
    while (tampon.length - pos >= NFFT || (fin && tampon.length - pos >= HOP)) {
      // Niveau sur le pas (20 ms)
      let e = 0;
      for (let i = 0; i < HOP; i++) { const v = tampon[pos + i] || 0; e += v * v; }
      rms.push(10 * Math.log10(e / HOP + 1e-12));
      // Spectre sur la fenêtre
      for (let i = 0; i < NFFT; i++) { re[i] = (tampon[pos + i] || 0) * F.hann[i]; im[i] = 0; }
      fft(F, re, im);
      let fl = 0, sLog = 0, sLin = 0;
      for (let k = 1; k < nb; k++) {
        const p = re[k] * re[k] + im[k] * im[k];
        const m = Math.log1p(100 * Math.sqrt(p));
        courant[k] = m;
        const d = m - precedent[k];
        if (d > 0) fl += d;
        if (k >= 7 && k < 400) { sLog += Math.log(p + 1e-12); sLin += p; } // 150 Hz-8,6 kHz : ignore basses et grosse caisse
      }
      flux.push(fl);
      plat.push(sLin > 0 ? Math.exp(sLog / 393) / (sLin / 393) : 0);
      const t = precedent; precedent = courant; courant = t;
      pos += HOP;
      if (fin && tampon.length - pos < HOP) break;
    }
    tampon = tampon.slice(pos);
  };

  await new Promise((resolve, reject) => {
    const p = spawn('ffmpeg', ['-hide_banner', '-nostdin', '-loglevel', 'error', '-i', fichier, '-vn', '-sn',
      '-ac', '1', '-ar', String(SR), '-af', 'highpass=f=20', '-f', 'f32le', 'pipe:1'], {windowsHide: true});
    let err = '';
    p.stdout.on('data', (d) => {
      const octets = resteOctets.length ? Buffer.concat([resteOctets, d]) : d;
      const n = Math.floor(octets.length / 4);
      const flt = new Float32Array(n);
      for (let i = 0; i < n; i++) flt[i] = octets.readFloatLE(i * 4);
      resteOctets = octets.subarray(n * 4);
      const nouveau = new Float32Array(tampon.length + n);
      nouveau.set(tampon); nouveau.set(flt, tampon.length);
      tampon = nouveau;
      traiter(false);
    });
    p.stderr.on('data', (d) => { err += d.toString(); });
    p.on('error', reject);
    p.on('close', (c) => { if (c === 0) { traiter(true); resolve(); } else reject(new Error(`ffmpeg (audio) : ${err.slice(-1500)}`)); });
  });
  return {rms: Float32Array.from(rms), flux: Float32Array.from(flux), plat: Float32Array.from(plat)};
}

// ───────────────────────── Outils de séries ─────────────────────────

function moyenneGlissante(x, demi) {
  const n = x.length, cum = new Float64Array(n + 1), out = new Float32Array(n);
  for (let i = 0; i < n; i++) cum[i + 1] = cum[i] + x[i];
  for (let i = 0; i < n; i++) { const a = Math.max(0, i - demi), b = Math.min(n, i + demi + 1); out[i] = (cum[b] - cum[a]) / (b - a); }
  return out;
}

/** Niveau lissé en dB (moyenne en puissance sur ±demi pas). */
function niveauLisse(rmsDb, demi) {
  const p = Float32Array.from(rmsDb, (v) => 10 ** (v / 10));
  return Float32Array.from(moyenneGlissante(p, demi), (v) => 10 * Math.log10(v + 1e-12));
}

function trier(x) { return Float32Array.from(x).sort(); }

/** Segments où cond(i) est vrai, en secondes, en comblant les trous < combler et en retirant ceux < min. */
function segments(n, cond, combler, min) {
  const seg = [];
  let debut = -1;
  for (let i = 0; i <= n; i++) {
    const v = i < n && cond(i);
    if (v && debut < 0) debut = i;
    if (!v && debut >= 0) { seg.push([debut / FPS, i / FPS]); debut = -1; }
  }
  const fusion = [];
  for (const s of seg) {
    if (fusion.length && s[0] - fusion[fusion.length - 1][1] < combler) fusion[fusion.length - 1][1] = s[1];
    else fusion.push([...s]);
  }
  return fusion.filter(([a, b]) => b - a >= min);
}

function trous(segs, debut, fin) {
  const t = [];
  let cur = debut;
  for (const [a, b] of segs) { if (a > cur) t.push([cur, a]); cur = Math.max(cur, b); }
  if (fin > cur) t.push([cur, fin]);
  return t;
}

// ───────────────────────── Attaques, tempo, événements ─────────────────────────

function detecterAttaques(sig) {
  const {flux} = sig;
  const fond = moyenneGlissante(flux, Math.round(0.5 * FPS));
  const med = quantile(trier(flux), 0.5);
  const att = [];
  for (let i = 3; i < flux.length - 3; i++) {
    const f = flux[i];
    if (f < 1.5 * fond[i] + 0.2 * med) continue;
    let max = true;
    for (let k = i - 3; k <= i + 3; k++) if (flux[k] > f || (flux[k] === f && k < i)) { max = false; break; }
    if (max) att.push({i, t: i / FPS, force: f / (fond[i] + 1e-9)});
  }
  return att;
}

/** Tempo par fenêtres de 12 s (autocorrélation de l'enveloppe d'attaques), 60-180 BPM. */
function estimerTempo(sig, duree) {
  const env = Float32Array.from(sig.flux);
  const fond = moyenneGlissante(env, Math.round(0.25 * FPS));
  for (let i = 0; i < env.length; i++) env[i] = Math.max(0, env[i] - fond[i]);
  const W = 12 * FPS, P = 6 * FPS;
  const lagMin = Math.floor(60 * FPS / 180), lagMax = Math.ceil(60 * FPS / 60);
  const fenetres = [];
  for (let d = 0; d + W <= env.length; d += P) {
    let moy = 0;
    for (let i = d; i < d + W; i++) moy += env[i];
    moy /= W;
    const x = new Float64Array(W);
    let e0 = 0;
    for (let i = 0; i < W; i++) { x[i] = env[d + i] - moy; e0 += x[i] * x[i]; }
    if (e0 <= 0) continue;
    const ac = new Float64Array(2 * lagMax + 2);
    for (let L = lagMin; L <= 2 * lagMax + 1 && L < W; L++) {
      let s = 0;
      for (let i = 0; i + L < W; i++) s += x[i] * x[i + L];
      ac[L] = s / e0;
    }
    let best = -1, bestScore = -Infinity;
    for (let L = lagMin; L <= lagMax; L++) {
      const score = ac[L] + 0.5 * (ac[2 * L] || 0);
      if (score > bestScore) { bestScore = score; best = L; }
    }
    // Affinage parabolique
    const y0 = ac[best - 1] || 0, y1 = ac[best], y2 = ac[best + 1] || 0;
    const den = y0 - 2 * y1 + y2;
    const Lf = best + (den !== 0 ? 0.5 * (y0 - y2) / den : 0);
    fenetres.push({t: (d + W / 2) / FPS, bpm: 60 * FPS / Lf, nettete: y1});
  }
  const nettes = fenetres.filter((f) => f.nettete >= 0.3);
  const bpms = trier(nettes.map((f) => f.bpm));
  return {
    fenetres,
    bpm: nettes.length ? quantile(bpms, 0.5) : null,
    partRythmee: fenetres.length ? nettes.length / fenetres.length : 0,
  };
}

/**
 * Événements marquants : saut d'énergie ≥ 10 dB en < 60 ms, son « bruité » (planéité ≥ 0,15 :
 * impact, whoosh, souffle, choc — pas une voyelle ni une note), assez fort, et non périodique.
 */
function detecterEvenements(sig, attaques) {
  const {rms, plat} = sig;
  const actifs = trier(Array.from(rms).filter((v) => v > -60));
  const niveauMedian = actifs.length ? quantile(actifs, 0.5) : -30;
  const candidats = [];
  for (const a of attaques) {
    const i = a.i;
    const avant = Array.from(rms.subarray(Math.max(0, i - 25), Math.max(0, i - 2))).sort((x, y) => x - y);
    if (!avant.length) continue;
    const base = Math.max(-60, avant[Math.floor(avant.length / 2)]); // depuis le silence numérique : borne à −60 dBFS
    let crete = -Infinity, pl = 0;
    for (let k = i; k < Math.min(rms.length, i + 4); k++) { crete = Math.max(crete, rms[k]); pl = Math.max(pl, plat[k]); }
    const saut = crete - base;
    if (saut >= 10 && pl >= 0.15 && crete >= niveauMedian - 6) candidats.push({t: a.t, saut, crete, plat: pl});
  }
  // Exclut les séries régulières (batterie, pulsation musicale).
  const tol = 0.035;
  const proche = (t) => candidats.some((c) => Math.abs(c.t - t) <= tol);
  return candidats.filter((c, k) => {
    const prec = candidats[k - 1];
    if (!prec) return true;
    const d = c.t - prec.t;
    return !(d >= 0.2 && d <= 1.5 && proche(c.t + d) && proche(c.t - 2 * d));
  });
}

// ───────────────────────── Voix ─────────────────────────

function lireSRT(fichier) {
  const txt = fs.readFileSync(fichier, 'utf8');
  const seg = [];
  for (const m of txt.matchAll(/(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)/g)) {
    const a = +m[1] * 3600 + +m[2] * 60 + +m[3] + +m[4] / 1000;
    const b = +m[5] * 3600 + +m[6] * 60 + +m[7] + +m[8] / 1000;
    if (b - a > 0.05) seg.push([a, b]);
  }
  seg.sort((x, y) => x[0] - y[0]);
  const u = [];
  for (const s of seg) { if (u.length && s[0] <= u[u.length - 1][1] + 0.05) u[u.length - 1][1] = Math.max(u[u.length - 1][1], s[1]); else u.push([...s]); }
  return u;
}

function choisirSousTitres(liste) {
  if (!liste?.length) return null;
  const score = (f) => (/\.fr[.-]/.test(f) ? 0 : 1) + (/orig/.test(f) ? 0 : 0.5);
  return [...liste].sort((a, b) => score(a) - score(b))[0];
}

async function separerVoix({o, audio, dossierCache}) {
  const sortie = path.join(dossierCache, 'separation');
  const nom = path.parse(audio).name;
  const dossier = path.join(sortie, 'htdemucs', nom);
  const voix = ['vocals.mp3', 'vocals.wav'].map((f) => path.join(dossier, f)).find((f) => fs.existsSync(f));
  const reste = ['no_vocals.mp3', 'no_vocals.wav'].map((f) => path.join(dossier, f)).find((f) => fs.existsSync(f));
  if (voix && reste) { info('Séparation voix/accompagnement déjà faite, réutilisée.'); return {voix, accompagnement: reste}; }

  const [cmd, ...pre] = o.demucs.split(' ').filter(Boolean);
  info('Séparation voix / accompagnement (Demucs) — peut prendre du temps sans carte graphique…');
  let dernier = -20;
  try {
    await lancer(cmd, [...pre, '--two-stems', 'vocals', '-n', 'htdemucs', '--mp3', '--mp3-bitrate', '192', '-o', sortie, audio], {
      onStderr: (s) => {
        const m = [...s.matchAll(/(\d+)%\|/g)].pop();
        if (m && +m[1] - dernier >= 20) { dernier = +m[1]; info(`séparation : ${m[1]} %`); }
      },
    });
  } catch (e) {
    if (e.code === 'ENOENT') {
      info(`Demucs introuvable (« ${cmd} »). Voir shared/outils/analyser-reference/README.md, section Son. Analyse sans séparation.`);
    } else {
      info(`La séparation a échoué, analyse sans séparation : ${String(e.message).split('\n').slice(-2).join(' ')}`);
    }
    return null;
  }
  const v = path.join(dossier, 'vocals.mp3'), r = path.join(dossier, 'no_vocals.mp3');
  return fs.existsSync(v) && fs.existsSync(r) ? {voix: v, accompagnement: r} : null;
}

// ───────────────────────── Frises (images alignées sur le temps) ─────────────────────────

const C = {
  fond: [17, 17, 17], grille: [45, 45, 45], sonie: [210, 210, 210], sonieFond: [70, 70, 70],
  voix: [80, 150, 255], accomp: [255, 160, 60], coupe: [255, 255, 255], fondu: [140, 140, 140],
  impact: [255, 60, 60], ref: [255, 220, 0],
};

function toile(l, h, coul = C.fond) {
  const px = new Uint8Array(l * h * 3);
  for (let i = 0; i < l * h; i++) { px[i * 3] = coul[0]; px[i * 3 + 1] = coul[1]; px[i * 3 + 2] = coul[2]; }
  const set = (x, y, c) => { if (x < 0 || y < 0 || x >= l || y >= h) return; const i = (y * l + x) * 3; px[i] = c[0]; px[i + 1] = c[1]; px[i + 2] = c[2]; };
  return {
    l, h, px, set,
    rect: (x0, y0, x1, y1, c) => { for (let y = Math.max(0, y0); y < Math.min(h, y1); y++) for (let x = Math.max(0, x0); x < Math.min(l, x1); x++) set(x, y, c); },
  };
}

async function ecrireToile(t, fichier) {
  await ecrireImage(fichier, t.l, t.h, (x, y) => { const i = (y * t.l + x) * 3; return [t.px[i], t.px[i + 1], t.px[i + 2]]; });
}

/**
 * Une frise = une tranche de temps, de haut en bas :
 *   sonie court terme (avec ligne de sonie intégrée) · voix (bleu) et accompagnement (orange)
 *   · spectrogramme · coupes image (blanc = franche, gris = fondu) et événements (rouge) · temps.
 */
async function dessinerFrise({fichier, audio, t0, dureeTranche, dureeTotale, sonie, voixSeg, accompDb, evenements, plans, travail, num}) {
  const L = 1600, MARGE = 96;
  const dureeReelle = Math.min(dureeTranche, dureeTotale - t0);
  const X = (t) => Math.round((t - t0) / dureeTranche * L);

  // Bandeau haut : sonie (70 px) + voix/accompagnement (36 px)
  const haut = toile(L, 106);
  for (const db of [-10, -20, -30, -40, -50]) { const y = Math.round((-db / 60) * 70); haut.rect(0, y, L, y + 1, C.grille); }
  for (let x = 0; x < X(t0 + dureeReelle); x++) {
    const t = t0 + (x + 0.5) / L * dureeTranche;
    const k = Math.min(sonie.S.length - 1, Math.max(0, Math.round(t * 10) - 1));
    const v = Math.max(-60, Math.min(0, sonie.S[k] ?? -60));
    const y = Math.round((-v / 60) * 70);
    haut.rect(x, y, x + 1, 70, C.sonieFond);
    haut.rect(x, y, x + 1, y + 2, C.sonie);
  }
  if (sonie.I != null) { const y = Math.round((-sonie.I / 60) * 70); for (let x = 0; x < L; x += 6) haut.rect(x, y, x + 3, y + 1, C.ref); }
  haut.rect(0, 70, L, 72, C.grille);
  if (voixSeg) for (const [a, b] of voixSeg) if (b > t0 && a < t0 + dureeTranche) haut.rect(Math.max(0, X(a)), 74, Math.min(L, X(b)), 88, C.voix);
  if (accompDb) {
    for (let x = 0; x < X(t0 + dureeReelle); x++) {
      const t = t0 + (x + 0.5) / L * dureeTranche;
      const v = accompDb[Math.min(accompDb.length - 1, Math.round(t * FPS))] ?? -90;
      const h = Math.max(0, Math.min(16, Math.round((v + 60) / 60 * 16)));
      haut.rect(x, 106 - h, x + 1, 106, C.accomp);
    }
  }

  // Spectrogramme (FFmpeg)
  const spec = path.join(travail, `spec-${num}.png`);
  const lSpec = Math.max(16, Math.round(dureeReelle / dureeTranche * L));
  await lancer('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-ss', t0.toFixed(3), '-t', dureeReelle.toFixed(3), '-i', audio, '-vn',
    '-lavfi', `showspectrumpic=s=${lSpec}x200:legend=0:fscale=log:scale=log:color=intensity,pad=${L}:200:0:0:color=0x111111`,
    '-y', spec]);

  // Bandeau bas : événements (34 px) + graduations (12 px)
  const bas = toile(L, 46);
  for (const p of plans) {
    if (p.n === 1 || p.debut < t0 || p.debut > t0 + dureeTranche) continue;
    const x = X(p.debut);
    bas.rect(x, 0, x + 2, p.entree === 'progressive' ? 14 : 34, p.entree === 'progressive' ? C.fondu : C.coupe);
  }
  for (const e of evenements) {
    if (e.t < t0 || e.t > t0 + dureeTranche) continue;
    const x = X(e.t);
    bas.rect(x - 2, 16, x + 3, 34, C.impact);
  }
  const pasGrad = dureeTranche > 90 ? 10 : 5;
  for (let t = Math.ceil(t0 / pasGrad) * pasGrad; t <= t0 + dureeTranche; t += pasGrad) {
    const x = X(t);
    bas.rect(x, 34, x + 1, 46, C.sonie);
  }

  const fHaut = path.join(travail, `haut-${num}.png`), fBas = path.join(travail, `bas-${num}.png`);
  await ecrireToile(haut, fHaut);
  await ecrireToile(bas, fBas);

  // Assemblage + textes (via fichiers texte : aucun échappement nécessaire)
  const textes = [];
  const ajouter = (txt, x, y, taille = 13, coul = 'white') => {
    const f = `txt-${num}-${textes.length}.txt`;
    fs.writeFileSync(path.join(travail, f), txt);
    textes.push(`drawtext=fontfile=police.ttf:textfile=${f}:fontcolor=${coul}:fontsize=${taille}:x=${x}:y=${y}`);
  };
  const H = 106 + 200 + 46 + 18;
  ajouter('SONIE', 6, 28); ajouter('LUFS', 6, 44, 11, 'gray');
  ajouter('VOIX', 6, 74, 12, '0x5096ff'); ajouter('ACCOMP.', 6, 90, 11, '0xffa03c');
  ajouter('SPECTRE', 6, 106 + 90); ajouter('grave↓', 6, 106 + 180, 11, 'gray');
  ajouter('COUPES', 6, 306 + 4, 12); ajouter('IMPACTS', 6, 306 + 20, 12, '0xff3c3c');
  for (let t = Math.ceil(t0 / pasGrad) * pasGrad; t <= t0 + dureeTranche; t += pasGrad * 2) {
    ajouter(tc(t, 0), MARGE + Math.min(L - 50, Math.max(0, X(t) - 22)), H - 16, 12, '0xbbbbbb');
  }
  await lancer('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-i', fHaut, '-i', spec, '-i', fBas,
    '-filter_complex', `[0][1][2]vstack=inputs=3,pad=${L + MARGE}:${H}:${MARGE}:0:color=0x111111,${textes.join(',')}`,
    '-q:v', '3', '-y', fichier], {cwd: travail});
}

// ───────────────────────── Programme du module ─────────────────────────

/**
 * Analyse le son et renvoie la section Markdown du rapport (ou null si pas d'audio).
 * Écrit dans dossierSortie : son.csv, son-global.png, frises/frise-XXX.jpg.
 */
export const _interne = () => ({analyserSignal, detecterAttaques, detecterEvenements, estimerTempo, FPS});

export async function analyserSon({o, estUrl, video, dossierCache, dossierSortie, duree, plans, sousTitres}) {
  etape('Son : récupération de la piste…');
  const audio = await obtenirAudio({o, estUrl, video, dossierCache});
  if (!audio) { info('Pas de piste audio : analyse du son ignorée.'); return null; }

  const travail = path.join(dossierCache, 'travail-son');
  const dossierFrises = path.join(dossierSortie, 'frises');
  fs.mkdirSync(travail, {recursive: true});
  fs.mkdirSync(dossierFrises, {recursive: true});
  for (const f of fs.readdirSync(dossierFrises)) fs.rmSync(path.join(dossierFrises, f), {force: true});
  fs.copyFileSync(POLICE, path.join(travail, 'police.ttf'));

  etape('Son : sonie EBU R128…');
  const sonie = await mesurerSonie(audio, duree);

  etape('Son : analyse spectrale…');
  const sig = await analyserSignal(audio);

  let separation = null;
  if (o.separer) {
    etape('Son : séparation voix / accompagnement…');
    separation = await separerVoix({o, audio, dossierCache});
  }

  let voixSeg = null, sourceVoix = null, accompDb = null, voixDb = null, sigAccomp = null;
  if (separation) {
    const sv = await analyserSignal(separation.voix);
    sigAccomp = await analyserSignal(separation.accompagnement);
    voixDb = niveauLisse(sv.rms, 10);
    accompDb = niveauLisse(sigAccomp.rms, 10);
    const tri = trier(Array.from(voixDb).filter((v) => v > -80));
    // Calibré sur une piste de vérité (95 % d'exactitude) : voix à moins de 20 dB de son maximum
    // ET pas plus de 6 dB sous l'accompagnement (écarte les « fuites » de musique dans la piste voix).
    const seuil = Math.max(-45, (tri.length ? quantile(tri, 0.95) : -20) - 20);
    voixSeg = segments(voixDb.length, (i) => voixDb[i] > seuil && voixDb[i] - accompDb[i] > -6, 0.4, 0.5);
    sourceVoix = 'séparation IA (Demucs)';
  } else {
    const st = choisirSousTitres(sousTitres);
    if (st) { voixSeg = lireSRT(st); sourceVoix = `sous-titres (${path.basename(st)}) — approximatif`; }
  }

  etape('Son : attaques, tempo, événements…');
  const attaques = detecterAttaques(sig);
  const tempo = estimerTempo(sigAccomp || sig, duree);
  const evenements = detecterEvenements(sigAccomp || sig, detecterAttaques(sigAccomp || sig));

  // Silences (niveau du mixage)
  const niv = niveauLisse(sig.rms, 10);
  const actifs = trier(Array.from(niv).filter((v) => v > -70));
  const seuilSilence = Math.max(-60, (actifs.length ? quantile(actifs, 0.5) : -30) - 35);
  const silences = segments(niv.length, (i) => niv[i] < seuilSilence, 0.15, 0.6);

  // Synchronisation coupes ↔ son
  const coupesFranches = plans.filter((p) => p.n > 1 && p.entree === 'franche').map((p) => p.debut);
  const tAtt = attaques.map((a) => a.t);
  const prochesAtt = (t, tol) => { let lo = 0, hi = tAtt.length - 1; while (lo <= hi) { const m = (lo + hi) >> 1; if (tAtt[m] < t - tol) lo = m + 1; else if (tAtt[m] > t + tol) hi = m - 1; else return true; } return false; };
  const TOL = 0.07;
  const synchro = coupesFranches.length ? coupesFranches.filter((t) => prochesAtt(t, TOL)).length / coupesFranches.length : null;
  let couvert = 0, fin = -1;
  for (const t of tAtt) { const a = Math.max(t - TOL, fin), b = t + TOL; if (b > a) couvert += b - a; fin = Math.max(fin, b); }
  const hasard = Math.min(1, couvert / duree);

  // ── Sorties : son.csv (une ligne par seconde)
  let ptrAtt = 0;
  const csv = ['seconde;sonie_court_terme_lufs;sonie_moment_lufs_max;niveau_dbfs;voix;accompagnement_dbfs;attaques;evenement'];
  for (let s = 0; s < Math.ceil(duree); s++) {
    const kS = Math.min(sonie.S.length - 1, s * 10 + 9);
    let mMax = -Infinity;
    for (let k = s * 10; k < Math.min(sonie.M.length, s * 10 + 10); k++) mMax = Math.max(mMax, sonie.M[k]);
    const nivS = niv[Math.min(niv.length - 1, s * FPS + 25)] ?? -90;
    const v = voixSeg ? voixSeg.reduce((acc, [a, b]) => acc + Math.max(0, Math.min(b, s + 1) - Math.max(a, s)), 0) : '';
    const ac = accompDb ? (accompDb[Math.min(accompDb.length - 1, s * FPS + 25)]).toFixed(1) : '';
    while (ptrAtt < tAtt.length && tAtt[ptrAtt] < s) ptrAtt++;
    let nAtt = 0; while (ptrAtt + nAtt < tAtt.length && tAtt[ptrAtt + nAtt] < s + 1) nAtt++;
    const ev = evenements.some((e) => e.t >= s && e.t < s + 1) ? 1 : 0;
    csv.push([s, (sonie.S[kS] ?? -70).toFixed(1), Number.isFinite(mMax) ? mMax.toFixed(1) : '', nivS.toFixed(1),
      v === '' ? '' : v.toFixed(2), ac, nAtt, ev].join(';'));
  }
  fs.writeFileSync(path.join(dossierSortie, 'son.csv'), csv.join('\n') + '\n');

  // ── Vue globale : sonie + voix sur toute la durée
  {
    const L = 1600, G = toile(L, 110);
    for (const db of [-10, -20, -30, -40, -50]) { const y = Math.round((-db / 60) * 80); G.rect(0, y, L, y + 1, C.grille); }
    for (let x = 0; x < L; x++) {
      const a = Math.floor(x / L * duree * 10), b = Math.max(a + 1, Math.floor((x + 1) / L * duree * 10));
      let m = 0, n = 0;
      for (let k = a; k < Math.min(b, sonie.S.length); k++) { m += sonie.S[k]; n++; }
      const v = Math.max(-60, Math.min(0, n ? m / n : -60));
      const y = Math.round((-v / 60) * 80);
      G.rect(x, y, x + 1, 80, C.sonieFond); G.rect(x, y, x + 1, y + 2, C.sonie);
    }
    if (sonie.I != null) { const y = Math.round((-sonie.I / 60) * 80); for (let x = 0; x < L; x += 6) G.rect(x, y, x + 3, y + 1, C.ref); }
    if (voixSeg) for (const [a, b] of voixSeg) G.rect(Math.round(a / duree * L), 86, Math.max(Math.round(a / duree * L) + 1, Math.round(b / duree * L)), 100, C.voix);
    for (const e of evenements) { const x = Math.round(e.t / duree * L); G.rect(x, 102, x + 1, 110, C.impact); }
    await ecrireToile(G, path.join(dossierSortie, 'son-global.png'));
  }

  // ── Frises détaillées
  etape('Son : frises…');
  const dureeTranche = o.trancheSon || (duree <= 90 ? Math.ceil(duree) : duree <= 900 ? 60 : 120);
  const frises = [];
  for (let t0 = 0, n = 1; t0 < duree - 0.05; t0 += dureeTranche, n++) {
    const nom = `frise-${String(n).padStart(3, '0')}.jpg`;
    await dessinerFrise({fichier: path.join(dossierFrises, nom), audio, t0, dureeTranche, dureeTotale: duree,
      sonie, voixSeg, accompDb, evenements, plans, travail, num: n});
    frises.push({nom, t0, t1: Math.min(duree, t0 + dureeTranche)});
    if (n % 10 === 0) info(`${n} frises`);
  }
  info(`${frises.length} frises.`);
  fs.rmSync(travail, {recursive: true, force: true});

  // ── Section du rapport
  const md = [];
  md.push('## Son', '');
  md.push('> Mesures objectives de la bande sonore. Claude ne peut pas écouter : il lit ces mesures, les frises et la transcription.', '');
  md.push('![Son global](son-global.png)', '');
  md.push('*Sonie court terme sur toute la vidéo (ligne jaune pointillée = sonie intégrée), voix en bleu, événements marquants en rouge.*', '');

  md.push('### Niveau et dynamique', '');
  md.push('| Mesure | Valeur | Repère |', '|---|---|---|');
  if (sonie.I != null) md.push(`| Sonie intégrée | **${sonie.I.toFixed(1)} LUFS** | YouTube normalise à −14 LUFS (${sonie.I > -14 ? 'plus fort : sera baissé' : 'plus faible : ne sera pas monté'}) |`);
  if (sonie.LRA != null) md.push(`| Plage dynamique (LRA) | **${sonie.LRA.toFixed(1)} LU** | < 5 : très compressé · 5-10 : typique YouTube · > 12 : cinéma, très nuancé |`);
  if (sonie.TP != null) md.push(`| Crête vraie | ${sonie.TP.toFixed(1)} dBTP | ≤ −1 dBTP recommandé |`);
  md.push('');
  const tranche = duree > 1800 ? 300 : duree > 600 ? 120 : 60;
  md.push(`Sonie médiane par tranche de ${tranche / 60} min (où ça monte, où ça respire) :`, '', '```');
  const parTranche = [];
  for (let a = 0; a < duree; a += tranche) {
    const vals = trier(sonie.S.filter((_, k) => sonie.t[k] >= a && sonie.t[k] < a + tranche && sonie.S[k] > -70));
    parTranche.push({a, v: vals.length ? quantile(vals, 0.5) : -70});
  }
  for (const x of parTranche) md.push(`${tc(x.a, 0).padStart(8)}  ${barre(x.v + 50, 45)}  ${x.v.toFixed(1)} LUFS`);
  md.push('```', '');

  md.push('### Voix', '');
  if (voixSeg) {
    const dVoix = voixSeg.reduce((s, [a, b]) => s + b - a, 0);
    md.push(`Source : ${sourceVoix}.`, '');
    md.push('| Mesure | Valeur |', '|---|---|');
    md.push(`| Temps de parole | **${(dVoix / duree * 100).toFixed(0)} %** de la vidéo |`);
    if (separation && voixDb && accompDb) {
      const enV = [], horsV = [], ecart = [];
      const dansVoix = new Uint8Array(accompDb.length);
      for (const [a, b] of voixSeg) for (let i = Math.floor(a * FPS); i < Math.min(dansVoix.length, b * FPS); i++) dansVoix[i] = 1;
      for (let i = 0; i < accompDb.length; i += 5) {
        if (accompDb[i] < -70) continue;
        if (dansVoix[i]) { enV.push(accompDb[i]); ecart.push(voixDb[i] - accompDb[i]); } else horsV.push(accompDb[i]);
      }
      const mE = enV.length ? quantile(trier(enV), 0.5) : null, mH = horsV.length ? quantile(trier(horsV), 0.5) : null;
      if (ecart.length) md.push(`| Voix au-dessus de l'accompagnement (médiane) | **${quantile(trier(ecart), 0.5).toFixed(1)} dB** |`);
      if (mE != null && mH != null) md.push(`| Ducking (l'accompagnement baisse quand la voix parle) | **${(mH - mE).toFixed(1)} dB** (${mE.toFixed(1)} dBFS sous la voix, ${mH.toFixed(1)} dBFS sans) |`);
    }
    md.push('');
    const resp = trous(voixSeg, 0, duree).filter(([a, b]) => b - a >= 2.5).sort((x, y) => (y[1] - y[0]) - (x[1] - x[0])).slice(0, 15);
    if (resp.length) {
      md.push('**Respirations** (passages sans voix ≥ 2,5 s), les plus longues :', '');
      md.push('| Début | Durée | Ce que fait le son pendant ce temps |', '|---|---|---|');
      for (const [a, b] of resp.sort((x, y) => x[0] - y[0])) {
        const vals = trier(sonie.S.filter((_, k) => sonie.t[k] >= a && sonie.t[k] < b && sonie.S[k] > -90));
        const med = vals.length ? quantile(vals, 0.5) : -90;
        const nEv = evenements.filter((e) => e.t >= a && e.t < b).length;
        const desc = med < -50 ? 'quasi-silence' : `son à ${med.toFixed(0)} LUFS` + (nEv ? `, ${nEv} événement(s)` : '');
        md.push(`| ${tc(a)} | ${(b - a).toFixed(1)} s | ${desc} |`);
      }
      md.push('');
    }
  } else {
    md.push('Pas de repère de voix (ni séparation, ni sous-titres). Relancer avec `--separer` pour mesurer la voix.', '');
  }

  md.push('### Silences', '');
  if (silences.length) {
    md.push(`${silences.length} silence(s) ≥ 0,6 s (niveau < ${seuilSilence.toFixed(0)} dBFS) :`, '');
    md.push('| Début | Durée |', '|---|---|');
    for (const [a, b] of silences.slice(0, 20)) md.push(`| ${tc(a)} | ${(b - a).toFixed(1)} s |`);
    if (silences.length > 20) md.push(`| … | ${silences.length - 20} autres dans son.csv |`);
  } else {
    md.push('Aucun vrai silence : le son ne s\'arrête jamais complètement.');
  }
  md.push('');

  md.push('### Musique et rythme', '');
  md.push('| Mesure | Valeur |', '|---|---|');
  md.push(`| Tempo dominant estimé | ${tempo.bpm ? `**${Math.round(tempo.bpm)} BPM**` : 'non identifiable'} |`);
  md.push(`| Part du temps avec une pulsation nette | ${(tempo.partRythmee * 100).toFixed(0)} % |`);
  md.push(`| Attaques sonores (tous sons confondus) | ${(attaques.length / (duree / 60)).toFixed(0)} par minute |`);
  if (synchro != null) md.push(`| Coupes franches tombant sur une attaque sonore (± 70 ms) | **${(synchro * 100).toFixed(0)} %** (hasard : ${(hasard * 100).toFixed(0)} %) |`);
  md.push('');
  md.push('> Tempo : estimation automatique (une erreur d\'un facteur 2 est possible). Synchronisation : nettement au-dessus du hasard = montage calé sur le son.', '');
  const parT = [];
  for (let a = 0; a < duree; a += tranche) {
    const f = tempo.fenetres.filter((w) => w.t >= a && w.t < a + tranche && w.nettete >= 0.3);
    parT.push(f.length ? `${tc(a, 0)} : ${Math.round(quantile(trier(f.map((w) => w.bpm)), 0.5))} BPM` : `${tc(a, 0)} : —`);
  }
  if (parT.length > 1) md.push(`Tempo par tranche : ${parT.join(' · ')}`, '');

  md.push('### Événements sonores marquants', '');
  md.push(`${evenements.length} événements (${(evenements.length / (duree / 60)).toFixed(1)} par minute) : sons soudains et « bruités » (impacts, whooshes, chocs, souffles), hors pulsation musicale${separation ? ', détectés sur l\'accompagnement (voix retirée)' : ''}.`, '');
  if (evenements.length) {
    md.push('| Timecode | Saut d\'énergie | Niveau |', '|---|---|---|');
    for (const e of [...evenements].sort((a, b) => b.saut - a.saut).slice(0, 20).sort((a, b) => a.t - b.t)) {
      md.push(`| ${tc(e.t)} | +${e.saut.toFixed(0)} dB | ${e.crete.toFixed(0)} dBFS |`);
    }
    md.push('');
  }

  md.push('### Frises', '');
  md.push('De haut en bas : **sonie** (pointillé jaune = sonie intégrée) · **voix** (bleu) et **accompagnement** (orange, si séparation) · **spectrogramme** (grave en bas, aigu en haut ; la voix forme des bandes horizontales serrées, les impacts des traits verticaux) · **coupes** image (blanc = franche, gris = fondu) et **événements** (rouge) · temps.', '');
  md.push('| Frise | Tranche |', '|---|---|');
  for (const f of frises) md.push(`| [${f.nom}](frises/${f.nom}) | ${tc(f.t0, 0)} → ${tc(f.t1, 0)} |`);
  md.push('');
  md.push('Détail seconde par seconde : [`son.csv`](son.csv).', '');
  return md.join('\n');
}
