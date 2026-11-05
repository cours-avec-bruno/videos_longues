/**
 * Fonctions communes de l'outil analyser-reference (image et son).
 */
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

export const ICI = path.dirname(fileURLToPath(import.meta.url));
export const RACINE = path.resolve(ICI, '../../..');
export const POLICE = path.join(ICI, 'police', 'JetBrainsMono-Bold.ttf');


export function arreter(message) {
  console.error(`\n✖ ${message}\n`);
  process.exit(1);
}

export const etape = (m) => console.log(`\n▸ ${m}`);
export const info = (m) => console.log(`  ${m}`);

/** Lance une commande sans shell (pas de problème d'échappement, Windows compris). */
export function lancer(cmd, args, {cwd, onStderr, binaire = false} = {}) {
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

export async function verifierOutil(cmd, args, conseil) {
  try {
    await lancer(cmd, args);
  } catch (e) {
    if (e.code === 'ENOENT') arreter(`« ${cmd} » est introuvable.\n  ${conseil}`);
    throw e;
  }
}

/** Secondes → "mm:ss.d" (ou "h:mm:ss.d"). */
export function tc(s, decimales = 1) {
  const neg = s < 0;
  const f = 10 ** decimales;
  s = Math.round(Math.abs(s) * f) / f; // arrondi d'abord : évite « 00:60 »
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = (s % 60).toFixed(decimales).padStart(decimales ? 3 + decimales : 2, '0');
  const mm = String(m).padStart(2, '0');
  return (neg ? '-' : '') + (h ? `${h}:${mm}:${sec}` : `${mm}:${sec}`);
}

export const hex = ([r, g, b]) => '#' + [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('');
export const luma = ([r, g, b]) => (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
export function saturation([r, g, b]) {
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
  return mx === 0 ? 0 : (mx - mn) / mx;
}

export function quantile(tri, q) {
  if (!tri.length) return 0;
  const pos = (tri.length - 1) * q;
  const b = Math.floor(pos);
  return tri[b] + (tri[Math.min(b + 1, tri.length - 1)] - tri[b]) * (pos - b);
}

/** Exécute des tâches asynchrones avec un nombre limité en parallèle. */
export async function enParallele(taches, n, surProgression) {
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

export function slug(s) {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60) || 'reference';
}

export function idYouTube(url) {
  const m = url.match(/(?:youtu\.be\/|[?&]v=|\/shorts\/|\/embed\/|\/live\/)([A-Za-z0-9_-]{11})/);
  return m ? m[1] : null;
}

/** Écrit une image PPM (P6) puis la convertit en PNG avec FFmpeg. */
export async function ecrireImage(fichierPng, largeur, hauteur, pixel) {
  const entete = Buffer.from(`P6\n${largeur} ${hauteur}\n255\n`);
  const corps = Buffer.alloc(largeur * hauteur * 3);
  for (let y = 0; y < hauteur; y++) for (let x = 0; x < largeur; x++) {
    const [r, g, b] = pixel(x, y);
    const i = (y * largeur + x) * 3; corps[i] = r; corps[i + 1] = g; corps[i + 2] = b;
  }
  const ppm = `${fichierPng}.ppm`;
  fs.writeFileSync(ppm, Buffer.concat([entete, corps]));
  await lancer('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-i', ppm, '-y', fichierPng]);
  fs.rmSync(ppm, {force: true});
}

export function barre(valeur, max, largeur = 30) {
  const n = max ? Math.max(0, Math.min(largeur, Math.round(valeur / max * largeur))) : 0;
  return '█'.repeat(n) + '·'.repeat(Math.max(0, largeur - n));
}

