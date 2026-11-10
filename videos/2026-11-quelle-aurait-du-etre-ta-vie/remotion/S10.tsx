import React from 'react';
import {AbsoluteFill, Audio, Easing, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {S10_T as T, S10_VOIX, S10_DUREE} from './S10_temps';

/**
 * S10 · les autres (10/11/2026, 3e version : de VRAIES photos, pas d'images générées ; voir references/photos.md).
 * - Un POLYPTYQUE : cinq panneaux verticaux, une vie par panneau. Il ouvre la scène et la referme (avec l'âge de la mort).
 * - Chaque vie s'ouvre depuis son panneau (une fente qui s'élargit jusqu'au plein cadre), photo en lente poussée,
 *   et sa ligne de vie se dessine en bas de l'image (la même forme qu'en S09).
 * - Raj et Manoj : l'écran se partage en deux ; leurs deux lignes, alignées, s'arrêtent au même endroit.
 * Données : prompts/partie/4-autres-bebes.json. Pas de musique de fond (Bruno).
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
// un même étalonnage pour des photos d'origines diverses
const GRADE = 'saturate(0.88) contrast(1.06) brightness(0.92)';

type Segment = {de: number; a: number; quoi: string; ecole?: boolean};
type Vie = {id: string; nom: string; pays: string; img: string; video?: string; mort: number; segs: Segment[]; t0: number; t1: number; rouge?: boolean; fx?: number};

const VIES: Vie[] = [
  {id: 'manoj', nom: 'MANOJ', pays: 'INDE', img: 'manoj.jpg', mort: 75, rouge: true, t0: T.regard, t1: T.regard + 3.2, fx: 0.5,
    segs: [{de: 5, a: 11, quoi: 'école', ecole: true}, {de: 11, a: 15, quoi: 'les chèvres'}, {de: 15, a: 66, quoi: 'la mer'}]},
  {id: 'purity', nom: 'PURITY', pays: 'KENYA', img: 'purity.jpg', mort: 66, t0: T.purity + 0.6, t1: T.purity_fin, fx: 0.5,
    segs: [{de: 6, a: 18, quoi: 'jusqu\'au lycée', ecole: true}, {de: 18, a: 31, quoi: 'la pêche'}, {de: 31, a: 66, quoi: 'la terre'}]},
  {id: 'fama', nom: 'FAMA', pays: 'GUINÉE', img: 'fama.jpg', mort: 64, t0: T.fama + 0.6, t1: T.fama_fin, fx: 0.6,
    segs: [{de: 13, a: 14, quoi: 'cuisine'}, {de: 17, a: 28, quoi: 'la terre'}, {de: 28, a: 47, quoi: 'les bêtes'}, {de: 47, a: 64, quoi: 'la pêche'}]},
  {id: 'andrew', nom: 'ANDREW', pays: 'KENYA', img: 'andrew.jpg', mort: 51, t0: T.andrew + 0.6, t1: T.andrew_fin, fx: 0.62,
    segs: [{de: 6, a: 15, quoi: 'collège', ecole: true}, {de: 15, a: 51, quoi: 'les troupeaux'}]},
  {id: 'raj', nom: 'RAJ', pays: 'INDE · DALIT', img: 'raj.jpg', video: 'raj.mp4', mort: 81, t0: T.raj + 0.6, t1: T.raj_fin, fx: 0.55,
    segs: [{de: 5, a: 11, quoi: 'primaire', ecole: true}, {de: 15, a: 19, quoi: 'champs'}, {de: 19, a: 43, quoi: 'électricien'},
      {de: 44, a: 55, quoi: 'champs'}, {de: 55, a: 59, quoi: 'usine'}, {de: 59, a: 63, quoi: 'livreur'}]},
];
const vie = (id: string) => VIES.find((v) => v.id === id)!;

const useT = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return f / fps;
};

/** Une photo (ou un plan vidéo) qui respire : lente poussée, point de fuite choisi. */
const Image: React.FC<{v: Vie; t: number; t0: number; z?: [number, number]; d?: number; filtre?: string; video?: boolean}> =
  ({v, t, t0, z = [1.06, 1.16], d = 10, filtre = GRADE, video = false}) => {
    const {fps} = useVideoConfig();
    const q = Math.min(1, Math.max(0, (t - t0) / d));
    const s = z[0] + (z[1] - z[0]) * IO(q);
    const fx = v.fx ?? 0.5;
    const style: React.CSSProperties = {position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
      objectPosition: `${fx * 100}% 50%`, transform: `scale(${s})`, transformOrigin: `${fx * 100}% 55%`, filter: filtre};
    if (video && v.video) {
      return (
        <Sequence from={Math.round(t0 * fps)} layout="none">
          <OffthreadVideo src={staticFile(`s10/${v.video}`)} muted playbackRate={0.8} style={style} />
        </Sequence>
      );
    }
    return <Img src={staticFile(`s10/${v.img}`)} style={style} />;
  };

/** L'ombre froide de la DA sur les photos : ombres bleu-pétrole, vignette. */
const Teinte: React.FC = () => (
  <>
    <AbsoluteFill style={{mixBlendMode: 'soft-light', opacity: 0.35, background: 'linear-gradient(180deg, #0c3a44 0%, #14283a 60%, #3a1e14 100%)'}} />
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.45) 100%)'}} />
  </>
);

/** La ligne de vie d'une personne, en bas de l'image (x0..x1), avec ses étapes et l'âge de la mort. */
const LigneVie: React.FC<{v: Vie; t: number; x0: number; x1: number; y: number; etiquettes?: boolean}> = ({v, t, x0, x1, y, etiquettes = true}) => {
  const xA = (a: number) => x0 + (a / 85) * (x1 - x0);
  const age = v.mort * k(t, v.t0, v.t1 - v.t0, Easing.inOut(Easing.quad));
  const coul = v.rouge ? ROUGE : CREME;
  const mortQ = k(t, v.t1 - 0.1, 0.5);
  return (
    <>
      <div style={{position: 'absolute', left: x0, width: x1 - x0, top: y, height: 1, background: 'rgba(238,230,216,0.3)'}} />
      <div style={{position: 'absolute', left: x0, top: y - 1, height: 3, width: xA(age) - x0, background: coul}} />
      {v.segs.map((s, j) => {
        if (age <= s.de) return null;
        const q = k(t, v.t0 + (s.de / v.mort) * (v.t1 - v.t0), 0.5);
        return (
          <React.Fragment key={j}>
            {s.ecole ? <div style={{position: 'absolute', left: xA(s.de), top: y - 7, height: 14, width: xA(Math.min(age, s.a)) - xA(s.de),
              background: v.rouge ? ROUGE : CYAN, borderRadius: 3}} /> : null}
            {etiquettes ? <div style={{position: 'absolute', left: xA(s.de), top: y + (j % 2 ? -66 : -42), opacity: q, fontFamily: SANS, fontSize: 24,
              color: s.ecole ? (v.rouge ? '#F6C2B8' : CYAN) : 'rgba(238,230,216,0.9)', whiteSpace: 'nowrap', textShadow: '0 2px 10px rgba(0,0,0,0.95)'}}>{s.quoi}</div> : null}
          </React.Fragment>
        );
      })}
      {age < v.mort - 0.01 ? <div style={{position: 'absolute', left: xA(age) - 8, top: y - 8, width: 16, height: 16, borderRadius: '50%', background: coul,
        boxShadow: `0 0 16px ${coul}`}} /> : null}
      <div style={{position: 'absolute', left: xA(v.mort) - 1, top: y - 18, width: 2, height: 36, background: coul, opacity: mortQ}} />
      <div style={{position: 'absolute', left: xA(v.mort) + 14, top: y - 30, opacity: mortQ, fontFamily: SERIF, fontSize: 46, color: coul,
        textShadow: '0 2px 14px rgba(0,0,0,0.95)'}}>{v.mort} ans</div>
    </>
  );
};

/** Le nom, en grand, dans un cartouche. */
const Nom: React.FC<{v: Vie; q: number; x: number; y: number}> = ({v, q, x, y}) => (
  <div style={{position: 'absolute', left: x, top: y, display: 'flex', gap: 14, opacity: q, transform: `translateY(${(1 - q) * 16}px)`}}>
    <div style={{width: 5, background: v.rouge ? ROUGE : CYAN}} />
    <div>
      <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 64, letterSpacing: '0.12em', color: CREME, textShadow: '0 3px 20px rgba(0,0,0,0.85)'}}>{v.nom}</div>
      <div style={{fontFamily: SANS, fontSize: 24, letterSpacing: '0.3em', color: 'rgba(238,230,216,0.8)', textShadow: '0 2px 10px rgba(0,0,0,0.85)'}}>{v.pays}</div>
    </div>
  </div>
);

// ---------------------------------------------------------------- le polyptyque
const PW = 300, PG = 26, PY = 120, PH = 760;
const ORDRE = ['manoj', 'purity', 'fama', 'andrew', 'raj'];
const PX = (i: number) => (1920 - (5 * PW + 4 * PG)) / 2 + i * (PW + PG);

/** Une vie en plein cadre : elle s'ouvre comme une fente (le panneau du polyptyque qui s'élargit), puis se referme en fondu. */
const Plein: React.FC<{v: Vie; a: number; b: number; panneau: number}> = ({v, a, b, panneau}) => {
  const t = useT();
  if (t < a - 0.05 || t > b + 0.05) return null;
  const o = k(t, a, 0.9, IO);
  const cx = PX(panneau) + PW / 2;
  const gauche = interpolate(o, [0, 1], [cx - PW / 2, 0]);
  const droite = interpolate(o, [0, 1], [1920 - (cx + PW / 2), 0]);
  const haut = interpolate(o, [0, 1], [PY, 0]);
  const sortie = 1 - k(t, b - 0.5, 0.5, Easing.linear);
  return (
    <AbsoluteFill style={{clipPath: `inset(${haut}px ${droite}px ${haut}px ${gauche}px)`, opacity: sortie}}>
      <Image v={v} t={t} t0={a} video />
      <Teinte />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 55%, rgba(4,6,9,0.88) 100%)'}} />
      <Nom v={v} q={k(t, a + 0.5, 0.7)} x={120} y={90} />
      <LigneVie v={v} t={t} x0={120} x1={1800} y={960} />
    </AbsoluteFill>
  );
};

const Polyptyque: React.FC<{a: number; b: number; final?: boolean}> = ({a, b, final = false}) => {
  const t = useT();
  if (t < a || t > b) return null;
  const sortie = final ? 1 - k(t, b - 0.8, 0.8, Easing.linear) : 1 - k(t, b - 0.6, 0.6, Easing.linear);
  return (
    <AbsoluteFill style={{opacity: sortie}}>
      {ORDRE.map((id, i) => {
        const v = vie(id);
        // à l'ouverture, Manoj d'abord, puis les quatre autres sur « quatre autres naissances »
        const app = final ? k(t, a + 0.15 * i, 0.9) : id === 'manoj' ? k(t, a, 1.0) : k(t, a + 3.0 + 0.25 * i, 0.9);
        const couleur = final ? 1 : id === 'manoj' ? 1 : 0.4;
        const ageQ = final ? k(t, a + 0.8 + 0.25 * i, 0.7) : 0;
        return (
          <div key={id} style={{position: 'absolute', left: PX(i), top: PY + (1 - app) * 60, width: PW, height: PH, opacity: app}}>
            <div style={{position: 'absolute', inset: 0, overflow: 'hidden', borderRadius: 4,
              outline: v.rouge ? `3px solid ${ROUGE}` : '1px solid rgba(238,230,216,0.25)', outlineOffset: 6}}>
              <Image v={v} t={t} t0={a} z={[1.15, 1.25]} d={14} filtre={`${GRADE} saturate(${couleur}) brightness(${0.62 + 0.38 * couleur})`} />
              <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(4,6,9,0.9) 100%)'}} />
            </div>
            <div style={{position: 'absolute', bottom: 26, width: '100%', textAlign: 'center', fontFamily: SANS, fontWeight: 700, fontSize: 30,
              letterSpacing: '0.16em', color: CREME}}>{v.nom}</div>
            {final ? (
              <div style={{position: 'absolute', top: PH + 26, width: '100%', textAlign: 'center', opacity: ageQ, fontFamily: SERIF, fontSize: 70,
                color: v.rouge ? ROUGE : CREME, transform: `translateY(${(1 - ageQ) * 14}px)`}}>{v.mort}<span style={{fontSize: 28}}> ans</span></div>
            ) : null}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/** Raj et Manoj côte à côte : l'écran se partage ; leurs lignes, alignées, s'arrêtent au même endroit à l'école. */
const Regard: React.FC<{a: number; b: number}> = ({a, b}) => {
  const t = useT();
  if (t < a || t > b) return null;
  const o = k(t, a, 1.0, IO);
  const sortie = 1 - k(t, b - 0.5, 0.5, Easing.linear);
  const raj = vie('raj'), manoj = vie('manoj');
  return (
    <AbsoluteFill style={{opacity: sortie}}>
      <AbsoluteFill style={{clipPath: `inset(0 ${interpolate(o, [0, 1], [100, 50])}% 0 0)`}}>
        <Image v={manoj} t={t} t0={a} />
      </AbsoluteFill>
      <AbsoluteFill style={{clipPath: `inset(0 0 0 ${interpolate(o, [0, 1], [0, 50])}%)`}}>
        <Image v={raj} t={t} t0={a - 9} />
      </AbsoluteFill>
      <Teinte />
      <div style={{position: 'absolute', left: 959, top: 0, width: 2, height: 1080, background: 'rgba(238,230,216,0.6)', opacity: o}} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 45%, rgba(4,6,9,0.9) 100%)'}} />
      <Nom v={manoj} q={k(t, a + 0.4, 0.6)} x={90} y={80} />
      <Nom v={raj} q={k(t, a + 0.4, 0.6)} x={1050} y={80} />
      <div style={{opacity: o}}>
        <LigneVie v={{...manoj, t0: a, t1: a + 2.4}} t={t} x0={120} x1={1800} y={860} etiquettes={false} />
        <LigneVie v={{...raj, t0: a, t1: a + 2.4}} t={t} x0={120} x1={1800} y={960} etiquettes={false} />
        {/* le même arrêt : un trait vertical sur la fin de l'école */}
        <div style={{position: 'absolute', left: 120 + (11 / 85) * 1680 - 1, top: 820, width: 2, height: 180, background: CYAN, opacity: k(t, a + 1.4, 0.5)}} />
        <div style={{position: 'absolute', left: 120 + (11 / 85) * 1680 + 14, top: 790, fontFamily: SANS, fontSize: 24, letterSpacing: '0.12em', color: CYAN,
          opacity: k(t, a + 1.4, 0.5), textShadow: '0 2px 10px rgba(0,0,0,0.95)'}}>FIN DE L'ÉCOLE, À 11 ANS</div>
      </div>
    </AbsoluteFill>
  );
};

export const S10: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: '#05070a'}}>
      <Polyptyque a={0.6} b={T.purity + 0.9} />
      <Plein v={vie('purity')} a={T.purity} b={T.fama + 0.3} panneau={1} />
      <Plein v={vie('fama')} a={T.fama} b={T.andrew + 0.3} panneau={2} />
      <Plein v={vie('andrew')} a={T.andrew} b={T.raj + 0.3} panneau={3} />
      <Plein v={vie('raj')} a={T.raj} b={T.regard + 1.0} panneau={4} />
      <Regard a={T.regard} b={T.final + 0.4} />
      <Polyptyque a={T.final} b={S10_DUREE} final />

      {/* le son : la voix, des souffles sur les ouvertures, un clic à chaque mort, un coup grave sur le partage d'écran */}
      {S10_VOIX.map(([a, b, x], i) => (
        <Sequence key={i} from={Math.round(x * fps)} durationInFrames={Math.round((b - a) * fps) + 2}>
          <Audio src={staticFile('s10/voix.mp3')} startFrom={Math.round(a * fps)} endAt={Math.round(b * fps)} />
        </Sequence>
      ))}
      {[0.2, T.purity - 0.9, T.fama - 0.9, T.andrew - 0.9, T.raj - 0.9, T.final - 0.9].map((s, i) => (
        <Sequence key={`w${i}`} from={Math.max(0, Math.round(s * fps))}>
          <Audio src={staticFile('s09/sfx/whoosh_doux.wav')} volume={0.18} />
        </Sequence>
      ))}
      {[T.purity_fin, T.fama_fin, T.andrew_fin, T.raj_fin].map((s, i) => (
        <Sequence key={`c${i}`} from={Math.round(s * fps)}>
          <Audio src={staticFile('s09/sfx/clic_doux.wav')} volume={0.3} />
        </Sequence>
      ))}
      <Sequence from={Math.round(T.regard * fps)}>
        <Audio src={staticFile('s09/sfx/boom_bas.wav')} volume={0.22} />
      </Sequence>
      {[0, 1, 2, 3, 4].map((i) => (
        <Sequence key={`p${i}`} from={Math.round((T.final + 0.8 + 0.25 * i) * fps)}>
          <Audio src={staticFile('s09/sfx/clic_doux.wav')} volume={0.2} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
