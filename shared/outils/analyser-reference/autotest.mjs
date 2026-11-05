#!/usr/bin/env node
/**
 * Autotest de analyser-reference : fabrique des vidéos dont on connaît le contenu exact,
 * lance l'outil dessus et vérifie qu'il retrouve les bonnes valeurs.
 *
 *   npm run tester-analyse            (ajouter -- --separer pour tester aussi Demucs)
 *
 * Ne télécharge rien, n'écrit rien dans le repo (tout est supprimé à la fin).
 */
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {ICI, RACINE, lancer} from './commun.mjs';

const separer = process.argv.includes('--separer');
const demucsIdx = process.argv.indexOf('--demucs');
const demucs = demucsIdx > 0 ? process.argv[demucsIdx + 1] : null;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'autotest-ref-'));
const resultats = [];
const verifier = (nom, ok, detail) => { resultats.push({nom, ok, detail}); console.log(`  ${ok ? '✔' : '✖'} ${nom} — ${detail}`); };

function outil(args) {
  return new Promise((resolve, reject) => {
    const p = spawn(process.execPath, [path.join(ICI, 'index.mjs'), ...args], {windowsHide: true});
    let out = '';
    p.stdout.on('data', (d) => { out += d; });
    p.stderr.on('data', (d) => { out += d; });
    p.on('close', (c) => (c === 0 ? resolve(out) : reject(new Error(out.slice(-1500)))));
  });
}

const sortie = (id) => path.join(RACINE, 'docs', 'direction-artistique', 'extractions', id);
const lireCsv = (f) => fs.readFileSync(f, 'utf8').trim().split('\n').slice(1).map((l) => l.split(';'));

async function testImage() {
  console.log('\n▸ Image : 9 plans connus (coupes franches, raccords sombres, mouvement continu)');
  const v = path.join(tmp, 'coupes.mp4');
  const S = 's=1280x720:r=24';
  await lancer('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y',
    '-f', 'lavfi', '-i', `testsrc2=${S}:d=3`, '-f', 'lavfi', '-i', `smptebars=${S}:d=1`, '-f', 'lavfi', '-i', `color=c=0xc40303:${S}:d=0.5`,
    '-f', 'lavfi', '-i', `mandelbrot=${S}`, '-f', 'lavfi', '-i', `rgbtestsrc=${S}:d=2`, '-f', 'lavfi', '-i', `color=c=0x12222a:${S}:d=12`,
    '-f', 'lavfi', '-i', `life=${S}:mold=10:ratio=0.1:death_color=#000000:life_color=#00ff00`, '-f', 'lavfi', '-i', `testsrc=${S}:d=1`, '-f', 'lavfi', '-i', `cellauto=${S}:rule=110`,
    '-filter_complex', '[3:v]trim=duration=6,setpts=PTS-STARTPTS[m];[6:v]trim=duration=4,setpts=PTS-STARTPTS[l];[8:v]trim=duration=3,setpts=PTS-STARTPTS[c];' +
    '[0:v][1:v][2:v][m][4:v][5:v][l][7:v][c]concat=n=9:v=1:a=0,format=yuv420p[v]',
    '-map', '[v]', '-c:v', 'libx264', '-crf', '20', v]);
  await outil([v, '--id', 'autotest-image', '--sans-son']);
  const plans = lireCsv(path.join(sortie('autotest-image'), 'plans.csv'));
  const attendus = [0, 3, 4, 4.5, 10.5, 12.5, 24.5, 28.5, 29.5];
  const debuts = plans.map((p) => Number(p[4]));
  const justes = attendus.filter((a) => debuts.some((d) => Math.abs(d - a) <= 0.05)).length;
  verifier('Nombre de plans', plans.length === 9, `${plans.length} trouvés (attendu 9)`);
  verifier('Position des coupes', justes === 9, `${justes}/9 à ± 0,05 s`);
}

async function testSon() {
  console.log('\n▸ Son : pulsation à 120 BPM, impacts à 10 s et 25 s, silence de 20 à 30 s');
  const a = path.join(tmp, 'son.mp4');
  await lancer('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y',
    '-f', 'lavfi', '-i', 'color=c=0x202020:s=640x360:r=24:d=40',
    '-f', 'lavfi', '-i', "aevalsrc='0.5*sin(2*PI*60*t)*exp(-20*mod(t,0.5))*(lt(t,20)+gte(t,30))':s=44100:d=40",
    '-f', 'lavfi', '-i', 'anoisesrc=d=40:c=pink:r=44100:a=1',
    '-filter_complex', "[1]highpass=f=30[k];[2]highpass=f=150,volume='0.8*(exp(-12*(t-10))*between(t,10,10.5)+exp(-12*(t-25))*between(t,25,25.5))':eval=frame[i];[k][i]amix=inputs=2:normalize=0[a]",
    '-map', '0:v', '-map', '[a]', '-shortest', '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '192k', a]);
  const args = [a, '--id', 'autotest-son'];
  if (separer) args.push('--separer');
  if (demucs) args.push('--demucs', demucs);
  await outil(args);
  const md = fs.readFileSync(path.join(sortie('autotest-son'), 'resume.md'), 'utf8');
  const bpm = Number((md.match(/Tempo dominant estimé \| \*\*(\d+) BPM/) || [])[1]);
  verifier('Tempo', Math.abs(bpm - 120) <= 2, `${bpm || 'non trouvé'} BPM (attendu 120)`);
  const son = lireCsv(path.join(sortie('autotest-son'), 'son.csv'));
  const ev = son.filter((l) => l[7] === '1').map((l) => Number(l[0]));
  const imp = [10, 25].filter((t) => ev.includes(t) || ev.includes(t - 1)).length;
  verifier('Impacts', imp === 2, `${imp}/2 trouvés (secondes avec événement : ${ev.join(', ') || 'aucune'})`);
  const sil = (md.match(/\| (00:[12]\d\.\d) \| ([\d.]+) s \|/g) || []).filter((l) => {
    const m = l.match(/00:(\d+\.\d) \| ([\d.]+)/); const a = +m[1]; return a >= 19.5 && a < 30;
  });
  verifier('Silence 20-30 s', sil.length >= 1, sil.length ? sil.join(' ') : 'non trouvé');
  if (separer) verifier('Séparation Demucs', /Source : séparation IA/.test(md), /Source : séparation IA/.test(md) ? 'effectuée' : 'non effectuée (voir le message de l\'outil)');
}

try {
  await testImage();
  await testSon();
} catch (e) {
  verifier('Exécution', false, String(e.message).split('\n').slice(-6).join('\n'));
} finally {
  for (const id of ['autotest-image', 'autotest-son']) {
    fs.rmSync(sortie(id), {recursive: true, force: true});
    fs.rmSync(path.join(RACINE, '.cache', 'references', id), {recursive: true, force: true});
  }
  fs.rmSync(tmp, {recursive: true, force: true});
}
const ko = resultats.filter((r) => !r.ok).length;
console.log(ko ? `\n✖ ${ko} vérification(s) en échec.\n` : '\n✔ Tout est bon : l\'outil fonctionne sur cette machine.\n');
process.exit(ko ? 1 : 0);
