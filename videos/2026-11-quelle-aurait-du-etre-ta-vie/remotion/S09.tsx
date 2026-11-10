import React from 'react';
import {AbsoluteFill, Audio, Easing, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {P5Champ} from '../../../shared/remotion/P5Champ';
import {Question} from './Repasse';

/**
 * S09 · la vie adulte, de 15 à 60 ans (refaite le 10/11/2026 : Bruno veut un montage dynamique mais posé, sobre, premium).
 * Script réécrit (plus de contexte, relu avec /humanizer) ; voix de Guillaume en prise 1 (voix/S09b_prise1.mp3).
 * - les images tiennent plusieurs secondes, poussées lentes, fondus longs ;
 * - la LIGNE DE VIE en bas : un point avance avec l'âge ; à partir de 24 ans un fil rouge le suit (la dette, jamais soldée) ;
 * - les choix : les mêmes panneaux qu'en S07 (une même forme garde le même sens) ;
 * - quelques silences ajoutés aux moments-clés.
 */

const CREME = '#EEE6D8';
const ROUGE = '#D6482E';
const CYAN = '#5FD3E6';
const SANS = '"Bahnschrift", "Arial Narrow", Arial, sans-serif';
const SERIF = 'Georgia, "Times New Roman", serif';
const QO = Easing.out(Easing.poly(4));
const IO = Easing.inOut(Easing.cubic);
const cl = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const k = (t: number, a: number, d = 0.6, e = QO) => interpolate(t, [a, a + d], [0, 1], {...cl, easing: e});

const useT = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return f / fps;
};

// ---------------------------------------------------------------- la voix : la prise, coupée en quelques morceaux, avec des silences
// [début, fin] dans la prise -> position dans la scène = début - 3,4 + silence cumulé
const MORCEAUX: [number, number, number][] = [
  [4.6, 14.4, 0], [14.4, 34.5, 1.0], [34.5, 45.8, 2.5], [45.8, 63.5, 3.7],
  [63.5, 100.2, 5.2], [100.2, 112.6, 6.0], [112.6, 119.0, 9.0], [119.0, 122.4, 10.2],
];
export const S09_DUREE = 134;

// ---------------------------------------------------------------- les plans (images fixes et vidéos), avec leur mouvement
type Plan = {src: string; a: number; b: number; z?: [number, number]; c?: [number, number, number, number]; video?: boolean; vit?: number;
  grade?: 'froid' | 'chaud' | 'souvenir' | 'nuit'; graded?: [number, number]};
const PLANS: Plan[] = [
  {src: 'classe.png', a: 2.2, b: 5.6, z: [1.12, 1.04], grade: 'souvenir'},
  {src: 'mer_nuit.png', a: 14.6, b: 16.6, z: [1.25, 1.12]},
  {src: 'mere.png', a: 15.8, b: 23.6, z: [1.04, 1.14], c: [0.5, 0.45, 0.42, 0.42]},
  {src: 'mer_nuit.png', a: 23.0, b: 28.2, z: [1.08, 1.14], c: [0.42, 0.5, 0.56, 0.5], grade: 'nuit'},
  {src: 'bateau_plein.mp4', a: 27.6, b: 33.8, video: true, vit: 0.55},
  {src: 'hopital.png', a: 33.4, b: 38.6, z: [1.18, 1.06], grade: 'froid'},
  {src: 'hopital.png', a: 47.8, b: 55.6, z: [1.0, 1.1], grade: 'froid', graded: [51.0, 52.5]},
  {src: 'freres.png', a: 55.0, b: 60.4, z: [1.04, 1.1]},
  {src: 'freres_2.png', a: 59.6, b: 62.8, z: [1.06, 1.1]},
  {src: 'freres_1.png', a: 62.0, b: 66.8, z: [1.06, 1.12]},
  {src: 'preeti.png', a: 66.0, b: 70.6, z: [1.0, 1.12]},
  {src: 'mariage.png', a: 69.8, b: 76.8, z: [1.12, 1.02], grade: 'chaud'},
  {src: 'naissance.png', a: 76.0, b: 80.8, z: [1.02, 1.12], grade: 'chaud'},
  {src: 'classe.png', a: 80.0, b: 84.6, z: [1.1, 1.16], grade: 'souvenir'},
  {src: 'maison.png', a: 83.8, b: 91.4, z: [1.0, 1.1]},
  {src: 'mensonge.png', a: 90.6, b: 103.6, z: [1.04, 1.16], grade: 'froid', graded: [99.0, 101.5]},
  {src: 'theatre.png', a: 102.8, b: 119.6, z: [1.0, 1.3], c: [0.5, 0.5, 0.5, 0.4], grade: 'chaud'},
  {src: 'vieux.mp4', a: 118.8, b: 131.4, video: true, vit: 0.55},
  {src: 'bureau.png', a: 130.6, b: 134, z: [1.1, 1.04], grade: 'chaud'},
];

const FONDU = 0.8;

const Couche: React.FC<{p: Plan}> = ({p}) => {
  const t = useT();
  const {fps} = useVideoConfig();
  if (t < p.a || t > p.b) return null;
  const q = (t - p.a) / (p.b - p.a);
  const o = interpolate(t, [p.a, p.a + FONDU, p.b - FONDU, p.b], [0, 1, 1, 0], cl);
  const [z0, z1] = p.z ?? [1.02, 1.08];
  const [x0, y0, x1, y1] = p.c ?? [0.5, 0.5, 0.5, 0.5];
  const z = z0 + (z1 - z0) * IO(q);
  const ox = (0.5 - (x0 + (x1 - x0) * q)) * 100 * (z - 1);
  const oy = (0.5 - (y0 + (y1 - y0) * q)) * 100 * (z - 1);
  // l'étalonnage du plan ; « graded » : la lumière change pendant le plan (il guérit ; elle lui refait confiance)
  const g = p.graded ? k(t, p.graded[0], p.graded[1] - p.graded[0], IO) : 0;
  const filtres: Record<string, string> = {
    froid: `saturate(${0.75 + 0.25 * g}) brightness(${0.9 + 0.12 * g}) hue-rotate(${-6 * (1 - g)}deg)`,
    chaud: 'saturate(1.05) brightness(1.02) sepia(0.08)',
    souvenir: 'saturate(0.25) brightness(0.8) contrast(0.95)',
    nuit: 'saturate(0.85) brightness(0.88)',
  };
  const style: React.CSSProperties = {width: '100%', height: '100%', objectFit: 'cover',
    transform: `translate(${ox}%, ${oy}%) scale(${z})`, filter: p.grade ? filtres[p.grade] : undefined};
  return (
    <AbsoluteFill style={{opacity: o}}>
      {p.video ? (
        <Sequence from={Math.round(p.a * fps)} layout="none">
          <OffthreadVideo src={staticFile(`s09/${p.src}`)} playbackRate={p.vit ?? 1} muted style={style} />
        </Sequence>
      ) : (
        <Img src={staticFile(`s09/${p.src}`)} style={style} />
      )}
      {p.grade === 'souvenir' ? <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 40%, rgba(0,0,0,0.6) 100%)'}} /> : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- les choix : les panneaux de S07, en plus posé
type Carte = {titre: string; img?: string; ligne?: string};
const Choix: React.FC<{a: number; b: number; cartes: Carte[]; apparitions: number[]; tSel: number; sel: number; barres?: number[]; tBarres?: number}> =
  ({a, b, cartes, apparitions, tSel, sel, barres, tBarres = 0}) => {
    const t = useT();
    if (t < a || t > b) return null;
    const o = interpolate(t, [a, a + 0.7, b - 0.7, b], [0, 1, 1, 0], cl);
    const n = cartes.length;
    const w = n === 3 ? 500 : 620;
    const gap = 50;
    const x0 = (1920 - (n * w + (n - 1) * gap)) / 2;
    const s = k(t, tSel, 0.6, IO);
    return (
      <AbsoluteFill style={{opacity: o}}>
        <AbsoluteFill style={{background: 'radial-gradient(ellipse at 40% 35%, rgba(16,52,62,1) 0%, #080e14 60%, #05070a 100%)'}} />
        <P5Champ opacite={0.18} />
        {cartes.map((c, i) => {
          const q = k(t, apparitions[i], 0.7);
          const choisie = i === sel;
          const eteinte = !choisie ? s : 0;
          const hImg = c.img ? 300 : 0;
          return (
            <div key={i} style={{position: 'absolute', left: x0 + i * (w + gap), top: 300 + (1 - q) * 30, width: w, opacity: q * (1 - 0.7 * eteinte),
              transform: `scale(${1 + 0.03 * (choisie ? s : 0)})`, borderRadius: 12, overflow: 'hidden', background: 'rgba(8,13,18,0.9)',
              border: `2px solid ${choisie && s > 0.5 ? ROUGE : 'rgba(238,230,216,0.3)'}`, boxShadow: '0 30px 70px rgba(0,0,0,0.55)'}}>
              {c.img ? (
                <div style={{height: hImg, overflow: 'hidden'}}>
                  <Img src={staticFile(`s09/${c.img}`)} style={{width: '100%', height: '100%', objectFit: 'cover',
                    transform: `scale(${1.05 + 0.05 * k(t, apparitions[i], 6, Easing.linear)})`}} />
                </div>
              ) : null}
              <div style={{padding: '24px 30px 28px'}}>
                <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 40, letterSpacing: '0.1em', color: CREME}}>{c.titre}</div>
                {c.ligne ? <div style={{fontFamily: SANS, fontSize: 28, color: 'rgba(238,230,216,0.7)', marginTop: 8}}>{c.ligne}</div> : null}
                {barres ? (
                  <div style={{marginTop: 18, height: 10, background: 'rgba(238,230,216,0.12)', borderRadius: 5}}>
                    <div style={{height: 10, borderRadius: 5, width: `${barres[i] * 100 * k(t, tBarres + 0.15 * i, 1.0, IO)}%`,
                      background: choisie && s > 0.5 ? ROUGE : CYAN}} />
                  </div>
                ) : null}
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
    );
  };

// ---------------------------------------------------------------- la ligne de vie
const AGES: [number, number][] = [[1.5, 15], [34.0, 24], [69.8, 26], [83.8, 30], [90.6, 39], [106.0, 53], [118.8, 60]];
const AGE_MIN = 15, AGE_MAX = 60, X0 = 360, X1 = 1560, Y = 1004;
const ageA = (t: number) => {
  let a = AGES[0][1];
  for (let i = 0; i < AGES.length; i++) {
    const [ti, ai] = AGES[i];
    if (t >= ti) {
      const prec = i > 0 ? AGES[i - 1][1] : ai;
      a = prec + (ai - prec) * k(t, ti, 1.6, IO);
    }
  }
  return a;
};
const xAge = (a: number) => X0 + ((a - AGE_MIN) / (AGE_MAX - AGE_MIN)) * (X1 - X0);
const T_DETTE = 52.3;      // « mais la dette s'alourdit encore »
const T_PULSE = 120.6;     // « La dette est toujours là »

const LigneDeVie: React.FC = () => {
  const t = useT();
  const o = interpolate(t, [0.4, 1.4, 129.5, 130.5], [0, 0.85, 0.85, 0], cl);
  const a = ageA(t);
  const x = xAge(a);
  const dette = k(t, T_DETTE, 1.2);
  const pulse = t > T_PULSE ? 0.5 + 0.5 * Math.sin((t - T_PULSE) * 2 * Math.PI * 0.8) : 0;
  const ageAffiche = AGES.reduce((acc, [ti, ai]) => (t >= ti - 0.3 ? ai : acc), 15);
  return (
    <div style={{position: 'absolute', inset: 0, opacity: o}}>
      <div style={{position: 'absolute', left: X0, width: X1 - X0, top: Y, height: 2, background: 'rgba(238,230,216,0.28)'}} />
      {[15, 20, 30, 40, 50, 60].map((v) => (
        <div key={v} style={{position: 'absolute', left: xAge(v) - 1, top: Y - 5, width: 2, height: 12, background: 'rgba(238,230,216,0.35)'}} />
      ))}
      {/* le fil rouge : la dette, à partir de 24 ans, qui le suit */}
      {dette > 0 ? (
        <div style={{position: 'absolute', left: xAge(24), top: Y - 1 - pulse * 1.5, height: 4 + pulse * 3, width: Math.max(0, (x - xAge(24)) * dette),
          background: ROUGE, boxShadow: `0 0 ${10 + 14 * pulse}px rgba(214,72,46,0.7)`}} />
      ) : null}
      <div style={{position: 'absolute', left: x - 9, top: Y - 8, width: 18, height: 18, borderRadius: '50%', background: CREME,
        boxShadow: '0 0 14px rgba(238,230,216,0.6)'}} />
      <div style={{position: 'absolute', left: x - 100, width: 200, top: Y - 54, textAlign: 'center', fontFamily: SERIF, fontSize: 34, color: CREME,
        textShadow: '0 2px 12px rgba(0,0,0,0.8)'}}>{ageAffiche} ans</div>
    </div>
  );
};

/** Une petite mention en serif (les âges des frères) qui apparaît et s'efface. */
const Mention: React.FC<{a: number; b: number; texte: string; x: number; y: number}> = ({a, b, texte, x, y}) => {
  const t = useT();
  if (t < a || t > b) return null;
  const o = interpolate(t, [a, a + 0.8, b - 0.8, b], [0, 1, 1, 0], cl);
  return <div style={{position: 'absolute', left: x, top: y, opacity: o, fontFamily: SERIF, fontStyle: 'italic', fontSize: 44, color: CREME,
    textShadow: '0 3px 20px rgba(0,0,0,0.85)', transform: `translateY(${(1 - o) * 8}px)`}}>{texte}</div>;
};

/** Le cartouche (comme ailleurs dans la vidéo). */
const Cartouche: React.FC<{a: number; b: number; titre: string; x: number; y: number}> = ({a, b, titre, x, y}) => {
  const t = useT();
  if (t < a || t > b) return null;
  const q = k(t, a, 0.6);
  const s = interpolate(t, [b - 0.5, b], [1, 0], cl);
  return (
    <div style={{position: 'absolute', left: x, top: y, display: 'flex', gap: 12, opacity: q * s, transform: `translateX(${(1 - q) * -20}px)`}}>
      <div style={{width: 5, background: ROUGE}} />
      <div style={{background: 'rgba(5,8,11,0.7)', padding: '10px 18px', fontFamily: SANS, fontWeight: 700, fontSize: 34, letterSpacing: '0.14em', color: CREME}}>{titre}</div>
    </div>
  );
};

// [fichier, début (s), volume] : le souffle culmine ~1,1 s après son début ; la montée d'air culmine à sa fin (9,9 s)
const SFX: [string, number, number][] = [
  ...[4.4, 14.6, 33.0, 55.0, 66.0, 83.6, 102.6, 118.6, 130.4].map((t): [string, number, number] => ['whoosh_doux', t - 1.0, 0.22]),
  ...[7.8, 8.7, 9.6, 38.8, 40.0].map((t): [string, number, number] => ['clic_doux', t, 0.3]),
  ['clic_doux', 14.0, 0.45], ['clic_doux', 46.6, 0.45],
  ['boom_bas', 14.05, 0.18], ['boom_bas', 46.65, 0.18],
  ['boom_bas', 52.2, 0.28], ['boom_bas', 59.7, 0.2], ['boom_bas', 62.0, 0.2], ['boom_bas', 120.6, 0.22], ['boom_bas', 126.0, 0.26],
  ['whoosh_inverse', 90.6 - 3.8, 0.2],
  ['riser_aerien', 69.8 - 9.6, 0.12], ['riser_aerien', 111.6 - 9.6, 0.14],
];

export const S09: React.FC = () => {
  const t = useT();
  const {fps} = useVideoConfig();
  // les applaudissements : la lumière de la scène qui respire
  const scene = k(t, 111.5, 1.5) * (1 - k(t, 118.3, 0.8));
  const souffle = scene * (0.5 + 0.5 * Math.sin(t * 5.2));
  // la musique : basse sous la voix, creusée aux moments graves, qui s'ouvre au mariage et au théâtre
  const vol = (f: number) => {
    const s = f / fps;
    return interpolate(s, [0, 3, 33.0, 34.0, 64.5, 69.0, 71.0, 89.8, 91.0, 99.0, 102.0, 111.0, 114.0, 118.6, 119.4, 128, 134],
      [0, 0.16, 0.16, 0.04, 0.04, 0.12, 0.22, 0.2, 0.0, 0.0, 0.14, 0.18, 0.08, 0.06, 0.03, 0.03, 0], cl) * 0.45;   // Bruno : musique plus basse
  };
  return (
    <AbsoluteFill style={{background: '#05070a'}}>
      {PLANS.map((p, i) => <Couche key={i} p={p} />)}

      {/* 15 ans : trois chemins, presque à égalité ; il choisit la mer */}
      <Choix a={4.4} b={15.4} cartes={[{titre: 'LA MER', img: 'mer_nuit.png'}, {titre: "L'ÉLEVAGE", img: 'elevage.png'}, {titre: 'LES CHAMPS', img: 'terre.png'}]}
        apparitions={[7.8, 8.7, 9.6]} tSel={14.0} sel={0} barres={[0.86, 0.83, 0.78]} tBarres={12.3} />
      {/* 24 ans : l'hôpital ou la pharmacie */}
      <Choix a={38.4} b={48.2} cartes={[{titre: "L'HÔPITAL", ligne: 'soigné, mais cher'}, {titre: 'LA PHARMACIE', ligne: 'beaucoup moins cher'}]}
        apparitions={[38.8, 40.0]} tSel={46.6} sel={0} />
      <Cartouche a={48.6} b={51.8} titre="TUBERCULOSE" x={120} y={140} />

      <Mention a={59.8} b={66.4} texte="32 ans" x={520} y={250} />
      <Mention a={62.1} b={66.4} texte="49 ans" x={900} y={250} />

      {/* le théâtre : la poursuite qui respire sur les applaudissements */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 42%, rgba(255,214,160,0.35) 0%, rgba(255,214,160,0) 45%)', opacity: souffle,
        mixBlendMode: 'screen'}} />

      <LigneDeVie />

      {/* la question au spectateur (même forme qu'au début de la vidéo) */}
      <Question t0={126.0} t1={131.2} avant={['Et', 'vous…', 'à', 'quel', 'âge']} cle="pourrez-vous" apres={['vous', 'arrêter ?']} y={0.42} taille={70} />

      {/* l'étalonnage commun : vignette et grain */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.4) 100%)', pointerEvents: 'none'}} />

      {/* le son */}
      {MORCEAUX.map(([a, b, x], i) => (
        <Sequence key={i} from={Math.round((a - 3.4 + x) * fps)} durationInFrames={Math.round((b - a) * fps) + 2}>
          <Audio src={staticFile('s09/voix.mp3')} startFrom={Math.round(a * fps)} endAt={Math.round(b * fps)} volume={1} />
        </Sequence>
      ))}
      {/* plus de musique de fond (Bruno, 10/11) : la voix, les ambiances et les SFX suffisent */}
      {/* les SFX (Epidemic Sound), discrets : un souffle sur chaque grand changement de lieu, un clic doux par carte,
          un coup grave sur les moments qui pèsent, une montée d'air vers le mariage et vers les applaudissements */}
      {SFX.map(([f, t0, v], i) => (
        <Sequence key={`sfx${i}`} from={Math.max(0, Math.round(t0 * fps))}>
          <Audio src={staticFile(`s09/sfx/${f}.wav`)} volume={v} />
        </Sequence>
      ))}
      <Sequence from={Math.round(14.8 * fps)} durationInFrames={Math.round(19 * fps)}>
        <Audio src={staticFile('s09/vagues_plage.wav')} volume={(f) => interpolate(f / fps, [0, 1.5, 17, 19], [0, 0.22, 0.22, 0], cl)} />
      </Sequence>
      <Sequence from={Math.round(23 * fps)} durationInFrames={Math.round(11 * fps)}>
        <Audio src={staticFile('s09/barque_bois_vagues.wav')} volume={(f) => interpolate(f / fps, [0, 1, 9.5, 11], [0, 0.2, 0.2, 0], cl)} />
      </Sequence>
      <Sequence from={Math.round(33.2 * fps)} durationInFrames={Math.round(2.6 * fps)}>
        <Audio src={staticFile('s09/toux_homme.wav')} volume={0.55} />
      </Sequence>
      <Sequence from={Math.round(111.0 * fps)} durationInFrames={Math.round(8.4 * fps)}>
        <Audio src={staticFile('s09/applaudissements_salle.wav')} volume={(f) => interpolate(f / fps, [0, 1.6, 6.8, 8.4], [0, 0.5, 0.5, 0], cl)} />
      </Sequence>
      <Sequence from={Math.round(112.4 * fps)} durationInFrames={Math.round(6.8 * fps)}>
        <Audio src={staticFile('s09/applaudissements_grands.wav')} volume={(f) => interpolate(f / fps, [0, 1.8, 5.6, 6.8], [0, 0.35, 0.35, 0], cl)} />
      </Sequence>
      <Sequence from={Math.round(119.2 * fps)} durationInFrames={Math.round(12 * fps)}>
        <Audio src={staticFile('s09/vagues_plage.wav')} startFrom={Math.round(8 * fps)} volume={(f) => interpolate(f / fps, [0, 1.5, 10, 12], [0, 0.2, 0.2, 0], cl)} />
      </Sequence>
    </AbsoluteFill>
  );
};
