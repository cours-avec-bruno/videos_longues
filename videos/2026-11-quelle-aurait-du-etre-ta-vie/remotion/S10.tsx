import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {P5Champ} from '../../../shared/remotion/P5Champ';
import {S10_T as T, S10_VOIX, S10_DUREE} from './S10_temps';

/**
 * S10 · les autres (10/11/2026). Quatre autres bébés, tirés au sort la même année, vivent aussi (données : prompts/partie/4-autres-bebes.json).
 * Une seule frise d'âge, cinq lignes de vie : la même forme que la ligne de vie de S09 (un point qui avance avec l'âge).
 * Manoj en rouge ; chaque vie se dessine pendant que la voix la raconte ; l'école en trait épais, le travail en trait fin, les
 * repères (couple, premier enfant) en petits points ; la mort : la ligne s'arrête, l'âge s'inscrit. À la fin, les cinq âges se rangent.
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

type Segment = {de: number; a: number; quoi: string; ecole?: boolean};
type Vie = {nom: string; pays: string; mort: number; segs: Segment[]; reperes: [number, string][]; t0: number; t1: number; rouge?: boolean};

// les vies (âges réels de la partie) ; t0/t1 : quand la ligne se dessine, calé sur la voix
const VIES: Vie[] = [
  {nom: 'MANOJ', pays: 'INDE', mort: 75, rouge: true, t0: T.manoj, t1: T.manoj + 3.0,
    segs: [{de: 5, a: 11, quoi: 'école', ecole: true}, {de: 11, a: 15, quoi: 'les chèvres'}, {de: 15, a: 66, quoi: 'la mer'}], reperes: [[26, 'Preeti']]},
  {nom: 'PURITY', pays: 'KENYA', mort: 66, t0: T.purity, t1: T.purity_fin,
    segs: [{de: 6, a: 18, quoi: 'jusqu\'au lycée', ecole: true}, {de: 18, a: 31, quoi: 'la pêche'}, {de: 31, a: 66, quoi: 'la terre'}], reperes: [[20, '5 enfants']]},
  {nom: 'FAMA', pays: 'GUINÉE', mort: 64, t0: T.fama, t1: T.fama_fin,
    segs: [{de: 13, a: 14, quoi: 'cuisine'}, {de: 17, a: 28, quoi: 'la terre'}, {de: 28, a: 47, quoi: 'les bêtes'}, {de: 47, a: 64, quoi: 'la pêche'}],
    reperes: [[14, 'en couple'], [16, '1er enfant']]},
  {nom: 'ANDREW', pays: 'KENYA', mort: 51, t0: T.andrew, t1: T.andrew_fin,
    segs: [{de: 6, a: 15, quoi: 'collège', ecole: true}, {de: 15, a: 51, quoi: 'les troupeaux'}], reperes: []},
  {nom: 'RAJ', pays: 'INDE · DALIT', mort: 81, t0: T.raj, t1: T.raj_fin,
    segs: [{de: 5, a: 11, quoi: 'primaire', ecole: true}, {de: 15, a: 19, quoi: 'champs'}, {de: 19, a: 43, quoi: 'électricien'},
      {de: 44, a: 55, quoi: 'champs'}, {de: 55, a: 59, quoi: 'usine'}, {de: 59, a: 63, quoi: 'livreur'}], reperes: []},
];

const X0 = 430, X1 = 1760, A_MAX = 85;
const xA = (a: number) => X0 + (a / A_MAX) * (X1 - X0);
const Y0 = 250, PAS = 150;

const useT = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return f / fps;
};

const Ligne: React.FC<{v: Vie; i: number}> = ({v, i}) => {
  const t = useT();
  const y = Y0 + i * PAS;
  // l'âge atteint par le tracé
  const age = v.mort * k(t, v.t0, v.t1 - v.t0, Easing.inOut(Easing.quad));
  const app = k(t, v.t0 - 0.6, 0.6);
  // Raj et Manoj : mis en regard ; les autres s'effacent un peu
  const regard = k(t, T.regard, 0.8, IO) * (1 - k(t, T.final, 0.8, IO));
  const att = v.nom === 'RAJ' || v.nom === 'MANOJ' ? 1 : 1 - 0.65 * regard;
  const coul = v.rouge ? ROUGE : CREME;
  const mortQ = k(t, v.t1 - 0.1, 0.5);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, opacity: app * att}}>
      {/* le nom */}
      <div style={{position: 'absolute', left: 120, top: y - 30, width: 270, display: 'flex', gap: 12}}>
        <div style={{width: 4, background: v.rouge ? ROUGE : CYAN}} />
        <div>
          <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 32, letterSpacing: '0.12em', color: CREME}}>{v.nom}</div>
          <div style={{fontFamily: SANS, fontSize: 19, letterSpacing: '0.2em', color: 'rgba(238,230,216,0.6)'}}>{v.pays}</div>
        </div>
      </div>
      {/* la ligne de fond (toute la vie possible), à peine visible */}
      <div style={{position: 'absolute', left: X0, width: X1 - X0, top: y, height: 1, background: 'rgba(238,230,216,0.12)'}} />
      {/* la vie vécue */}
      <div style={{position: 'absolute', left: X0, top: y - 1, height: 3, width: xA(age) - X0, background: coul, opacity: v.rouge ? 1 : 0.75}} />
      {v.segs.map((s, j) => {
        if (age <= s.de) return null;
        const a1 = Math.min(age, s.a);
        const q = k(t, v.t0 + ((s.de / v.mort) * (v.t1 - v.t0)), 0.5);
        return (
          <React.Fragment key={j}>
            {s.ecole ? <div style={{position: 'absolute', left: xA(s.de), top: y - 7, height: 14, width: xA(a1) - xA(s.de), background: v.rouge ? ROUGE : CYAN, borderRadius: 3}} /> : null}
            <div style={{position: 'absolute', left: xA(s.de), top: y + (j % 2 ? -66 : -42), opacity: q, fontFamily: SANS, fontSize: 23,
              letterSpacing: '0.04em', color: s.ecole ? (v.rouge ? '#F1B9AE' : CYAN) : 'rgba(238,230,216,0.72)', whiteSpace: 'nowrap'}}>{s.quoi}</div>
          </React.Fragment>
        );
      })}
      {v.reperes.map(([a, txt], j) => (age >= a ? (
        <React.Fragment key={j}>
          <div style={{position: 'absolute', left: xA(a) - 6, top: y - 6, width: 12, height: 12, borderRadius: '50%', background: CREME}} />
          <div style={{position: 'absolute', left: xA(a) - 10, top: y + 16 + j * 26, fontFamily: SERIF, fontStyle: 'italic', fontSize: 23, color: CREME, whiteSpace: 'nowrap',
            opacity: k(t, v.t0 + (a / v.mort) * (v.t1 - v.t0), 0.5)}}>{txt}</div>
        </React.Fragment>
      ) : null))}
      {/* la tête du tracé, puis la fin */}
      {age < v.mort - 0.01 ? (
        <div style={{position: 'absolute', left: xA(age) - 8, top: y - 8, width: 16, height: 16, borderRadius: '50%', background: coul, boxShadow: `0 0 16px ${coul}`}} />
      ) : null}
      <div style={{position: 'absolute', left: xA(v.mort) - 1, top: y - 18, width: 2, height: 36, background: coul, opacity: mortQ}} />
      <div style={{position: 'absolute', left: xA(v.mort) + 14, top: y - 26, opacity: mortQ, fontFamily: SERIF, fontSize: 40, color: coul}}>{v.mort}</div>
    </div>
  );
};

export const S10: React.FC = () => {
  const t = useT();
  const {fps} = useVideoConfig();
  const fin = k(t, T.final, 1.2, IO);
  // l'axe des âges
  const axe = k(t, 0.6, 1.2);
  return (
    <AbsoluteFill style={{background: '#05070a'}}>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 40% 30%, rgba(16,52,62,1) 0%, #080e14 60%, #05070a 100%)'}} />
      <P5Champ opacite={0.16} />
      <div style={{position: 'absolute', top: 92, width: '100%', textAlign: 'center', fontFamily: SANS, fontSize: 25, letterSpacing: '0.42em',
        color: 'rgba(238,230,216,0.7)', opacity: k(t, 0.8, 0.8) * (1 - fin)}}>CINQ NAISSANCES, LA MÊME ANNÉE</div>
      {/* l'axe */}
      <div style={{position: 'absolute', inset: 0, opacity: axe * (1 - fin)}}>
        {[0, 10, 20, 30, 40, 50, 60, 70, 80].map((a) => (
          <div key={a} style={{position: 'absolute', left: xA(a) - 40, width: 80, top: 990, textAlign: 'center', fontFamily: SANS, fontSize: 20,
            color: 'rgba(238,230,216,0.45)'}}>{a} ans</div>
        ))}
        {[0, 10, 20, 30, 40, 50, 60, 70, 80].map((a) => (
          <div key={`l${a}`} style={{position: 'absolute', left: xA(a), top: 190, width: 1, height: 790, background: 'rgba(238,230,216,0.06)'}} />
        ))}
      </div>
      <div style={{opacity: 1 - fin}}>
        {VIES.map((v, i) => <Ligne key={v.nom} v={v} i={i} />)}
      </div>
      {/* la fin : les cinq âges se rangent, celui de Manoj en rouge */}
      {fin > 0 ? (
        <div style={{position: 'absolute', top: 420, width: '100%', display: 'flex', justifyContent: 'center', gap: 90}}>
          {[...VIES].sort((a, b) => a.mort - b.mort).map((v, i) => {
            const q = k(t, T.final + 0.4 + 0.25 * i, 0.7);
            return (
              <div key={v.nom} style={{textAlign: 'center', opacity: q, transform: `translateY(${(1 - q) * 20}px)`}}>
                <div style={{fontFamily: SERIF, fontSize: 120, color: v.rouge ? ROUGE : CREME}}>{v.mort}</div>
                <div style={{fontFamily: SANS, fontSize: 24, letterSpacing: '0.2em', color: 'rgba(238,230,216,0.7)', marginTop: 6}}>{v.nom}</div>
              </div>
            );
          })}
        </div>
      ) : null}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.4) 100%)', pointerEvents: 'none'}} />

      {/* le son */}
      {S10_VOIX.map(([a, b, x], i) => (
        <Sequence key={i} from={Math.round(x * fps)} durationInFrames={Math.round((b - a) * fps) + 2}>
          <Audio src={staticFile('s10/voix.mp3')} startFrom={Math.round(a * fps)} endAt={Math.round(b * fps)} />
        </Sequence>
      ))}
      <Audio src={staticFile('s09/musique.wav')} startFrom={Math.round(60 * fps)}
        volume={(f) => interpolate(f / fps, [0, 3, S10_DUREE - 4, S10_DUREE], [0, 0.05, 0.05, 0], cl)} />
      {[0.4, T.purity - 0.9, T.fama - 0.9, T.andrew - 0.9, T.raj - 0.9, T.final - 0.9].map((s, i) => (
        <Sequence key={`w${i}`} from={Math.max(0, Math.round(s * fps))}>
          <Audio src={staticFile('s09/sfx/whoosh_doux.wav')} volume={0.16} />
        </Sequence>
      ))}
      {[T.purity_fin, T.fama_fin, T.andrew_fin, T.raj_fin].map((s, i) => (
        <Sequence key={`c${i}`} from={Math.round(s * fps)}>
          <Audio src={staticFile('s09/sfx/clic_doux.wav')} volume={0.28} />
        </Sequence>
      ))}
      <Sequence from={Math.round(T.regard * fps)}>
        <Audio src={staticFile('s09/sfx/boom_bas.wav')} volume={0.2} />
      </Sequence>
    </AbsoluteFill>
  );
};
