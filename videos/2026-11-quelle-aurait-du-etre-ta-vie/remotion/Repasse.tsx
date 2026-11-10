import React from 'react';
import {Annonce, Choix, Ingenieur, Probas} from './Explications';
import {AbsoluteFill, Audio, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';

/**
 * Repasse 01 (Bruno, 10/11/2026) : un passage de montage sur l'aperçu S01→S08 (0 → 4:22), par-dessus le montage existant.
 * - un étalonnage commun (le film comme un seul objet : ombres froides, rouges gardés, vignette, grain) ;
 * - grammaire : la typo serif italique = une question posée AU SPECTATEUR (le titre en ouverture, la question de S08) ;
 *   les cartouches en capitales = nommer les acteurs (DA de la réf. « Le diable s'habille en Yoda ») ;
 * - une transition (éclair + poussée + souffle) sur la seule coupe sèche entre deux mondes (S06 → S07).
 * Tous les temps sont en secondes dans l'aperçu (S07 commence à 134,43 ; S08 à 212,83).
 */

const CREME = '#EEE6D8';
const ROUGE = '#D6482E';
const SERIF = 'Georgia, "Times New Roman", serif';
const SANS = '"Bahnschrift", "Arial Narrow", Arial, sans-serif';
const QUINT_OUT = Easing.out(Easing.poly(5));

const T_S07 = 134.43;
const T_S08 = 212.83;

const useT = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return f / fps;
};

const rampe = (t: number, a: number, b: number, e = 0.4, s = 0.6) =>
  interpolate(t, [a, a + e, b - s, b], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

/** Le grade, sur tout le film : discret (on ne doit pas « voir le filtre »). */
const Etalonnage: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {/* ombres froides, hautes lumières chaudes, en lumière douce */}
      <AbsoluteFill style={{mixBlendMode: 'soft-light', opacity: 0.32,
        background: 'linear-gradient(180deg, rgba(12,58,68,1) 0%, rgba(20,40,52,1) 55%, rgba(92,44,26,1) 100%)'}} />
      {/* vignette */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 52%, rgba(0,0,0,0.42) 100%)'}} />
      {/* grain fin, qui change à chaque image */}
      <AbsoluteFill style={{opacity: 0.07, mixBlendMode: 'overlay'}}>
        <svg width="100%" height="100%">
          <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={f % 12} /></filter>
          <rect width="100%" height="100%" filter="url(#grain)" />
        </svg>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Un mot qui arrive : fondu + montée + netteté, longue queue ; il se pose et ne bouge plus. */
const Mot: React.FC<{t: number; t0: number; children: React.ReactNode; style?: React.CSSProperties}> = ({t, t0, children, style}) => {
  const q = interpolate(t, [t0, t0 + 0.9], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: QUINT_OUT});
  return (
    <span style={{display: 'inline-block', opacity: q, transform: `translateY(${(1 - q) * 22}px) scale(${0.97 + 0.03 * q})`,
      filter: `blur(${(1 - q) * 8}px)`, ...style}}>{children}</span>
  );
};

/** Une question au spectateur, en serif : la ligne posée, le mot-clé en rouge italique, souligné et auréolé. */
const Question: React.FC<{t0: number; t1: number; kicker?: string; avant: string[]; cle: string; apres?: string[]; y: number; taille: number}> =
  ({t0, t1, kicker, avant, cle, apres = [], y, taille}) => {
    const t = useT();
    if (t < t0 - 0.1 || t > t1 + 0.1) return null;
    const atmo = rampe(t, t0, t1, 0.4, 0.6);
    const sortie = interpolate(t, [t1 - 0.5, t1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const tCle = t0 + 0.35 + 0.12 * avant.length;
    const trait = interpolate(t, [tCle + 0.3, tCle + 1.0], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: QUINT_OUT});
    return (
      <AbsoluteFill style={{pointerEvents: 'none'}}>
        <AbsoluteFill style={{opacity: atmo * 0.8,
          background: `linear-gradient(180deg, rgba(0,0,0,0) ${y * 100 - 30}%, rgba(4,6,9,0.55) ${y * 100}%, rgba(0,0,0,0) ${y * 100 + 30}%)`}} />
        <div style={{position: 'absolute', left: '10%', right: '10%', top: `${y * 100}%`, transform: 'translateY(-50%)',
          textAlign: 'center', opacity: sortie, color: CREME}}>
          {kicker ? (
            <div style={{fontFamily: SANS, fontSize: 26, letterSpacing: '0.42em', marginBottom: 18, color: 'rgba(238,230,216,0.72)'}}>
              <Mot t={t} t0={t0}>{kicker}</Mot>
            </div>
          ) : null}
          <div style={{fontFamily: SERIF, fontSize: taille, lineHeight: 1.12, textShadow: '0 4px 30px rgba(0,0,0,0.75)'}}>
            {avant.map((m, i) => <Mot key={i} t={t} t0={t0 + 0.2 + 0.12 * i} style={{marginRight: '0.26em'}}>{m}</Mot>)}
            <span style={{position: 'relative', display: 'inline-block'}}>
              {/* auréole : un dégradé radial derrière le mot (jamais un text-shadow, qui ferait un rectangle) */}
              <span style={{position: 'absolute', left: '-30%', right: '-30%', top: '-60%', bottom: '-60%', opacity: 0.55 * trait,
                background: 'radial-gradient(ellipse at center, rgba(214,72,46,0.45) 0%, rgba(214,72,46,0) 65%)'}} />
              <Mot t={t} t0={tCle} style={{fontStyle: 'italic', color: ROUGE, position: 'relative'}}>{cle}</Mot>
              <span style={{position: 'absolute', left: 0, bottom: '0.02em', height: Math.max(3, taille / 26), width: `${trait * 100}%`,
                background: ROUGE, borderRadius: 2}} />
            </span>
            {apres.map((m, i) => m === '|' ? <br key={i} /> : <Mot key={i} t={t} t0={tCle + 0.25 + 0.1 * i} style={{marginLeft: '0.26em'}}>{m}</Mot>)}
          </div>
        </div>
      </AbsoluteFill>
    );
  };

/** Un cartouche qui nomme un acteur (capitales, filet rouge à gauche), qui glisse et se pose. */
const Cartouche: React.FC<{t0: number; t1: number; titre: string; sous?: string; x: number; y: number}> = ({t0, t1, titre, sous, x, y}) => {
  const t = useT();
  if (t < t0 || t > t1) return null;
  const q = interpolate(t, [t0, t0 + 0.6], [0, 1], {extrapolateRight: 'clamp', easing: QUINT_OUT});
  const s = interpolate(t, [t1 - 0.35, t1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: `${x * 100}%`, top: `${y * 100}%`, opacity: q * s, transform: `translateX(${(1 - q) * -24}px)`,
      display: 'flex', alignItems: 'stretch', gap: 14}}>
      <div style={{width: 5, background: ROUGE, transform: `scaleY(${q})`, transformOrigin: 'top'}} />
      <div style={{background: 'rgba(6,9,12,0.62)', padding: '10px 18px 12px'}}>
        <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 34, letterSpacing: '0.14em', color: CREME}}>{titre}</div>
        {sous ? <div style={{fontFamily: SANS, fontSize: 21, letterSpacing: '0.2em', color: 'rgba(238,230,216,0.62)', marginTop: 2}}>{sous}</div> : null}
      </div>
    </div>
  );
};

/** L'éclair de transition : une montée de lumière froide, la coupe au pic, puis l'extinction. */
const Eclair: React.FC<{tc: number}> = ({tc}) => {
  const t = useT();
  const a = interpolate(t, [tc - 0.18, tc, tc + 0.32], [0, 0.85, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (a <= 0) return null;
  return <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, rgba(235,246,250,1) 0%, rgba(120,210,230,0.9) 60%, rgba(20,60,70,0.8) 100%)', opacity: a}} />;
};

/** Un passage refait en Remotion, en plein écran par-dessus le montage, avec un fondu d'entrée et de sortie. */
const Plein: React.FC<{a: number; b: number; e?: number; s?: number; children: React.ReactNode}> = ({a, b, e = 0.25, s = 0.2, children}) => {
  const t = useT();
  const {fps} = useVideoConfig();
  if (t < a || t > b) return null;
  const o = interpolate(t, [a, a + e, b - s, b], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

export const Repasse: React.FC = () => {
  const t = useT();
  const {fps} = useVideoConfig();
  // la poussée : le film « avance » de quelques pour cent autour de la coupe S06 → S07
  const pousse = 1 + 0.05 * interpolate(t, [T_S07 - 0.35, T_S07, T_S07 + 0.6], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <AbsoluteFill style={{transform: `scale(${pousse})`, filter: 'contrast(1.06) saturate(1.04) brightness(0.99)'}}>
        <OffthreadVideo src={staticFile('repasse/apercu.mp4')} />
      </AbsoluteFill>
      {/* les passages d'explication refaits en Remotion (Bruno, 10/11/2026) */}
      <Plein a={T_S07 + 12.8} b={T_S07 + 21.6} e={0.15} s={0.1}><Ingenieur t0={T_S07 + 12.8} /></Plein>
      <Plein a={T_S07 + 60.5} b={T_S07 + 68.4} e={0.35}><Choix tC1={T_S07 + 61.3} tC2={T_S07 + 65.0} tDecompte={[T_S07 + 70.6, T_S07 + 73.6]} /></Plein>
      <Plein a={T_S07 + 70.2} b={T_S07 + 73.8} e={0.2}><Choix tC1={T_S07 + 61.3} tC2={T_S07 + 65.0} tDecompte={[T_S07 + 70.6, T_S07 + 73.6]} /></Plein>
      <Plein a={T_S08 + 4.1} b={T_S08 + 13.3} e={0.3} s={0.4}><Annonce tTape={[T_S08 + 4.85, T_S08 + 8.4]} tPourquoi={T_S08 + 9.0} tFin={T_S08 + 13.3} /></Plein>
      <Plein a={T_S08 + 28.9} b={262} e={0.5} s={0.01}>
        <Probas tGrille={T_S08 + 29.6} tChoix={T_S08 + 32.1} tEchec={T_S08 + 34.6} tLui={T_S08 + 36.6} tSara1={T_S08 + 38.4} tSara2={T_S08 + 41.3} tVous={T_S08 + 44.3} />
      </Plein>
      <Etalonnage />
      <Eclair tc={T_S07} />

      {/* ouverture : le titre, posé comme une question au spectateur, pendant la marche dans le noir */}
      <Question t0={1.6} t1={8.9} kicker="UNE VIE, TIRÉE AU SORT" avant={['Quelle', 'aurait', 'dû', 'être']} cle="ta vie" apres={['?']}
        y={0.7} taille={96} />

      {/* la salle des simulateurs : on nomme les deux acteurs à leur première réplique */}
      <Cartouche t0={T_S07 + 45.0} t1={T_S07 + 49.4} titre="LE SIMULATEUR" sous="IL A FAIT VIVRE MANOJ" x={0.05} y={0.76} />
      <Cartouche t0={T_S07 + 52.8} t1={T_S07 + 56.8} titre="LA SIMULATRICE" sous="ELLE VEUT REPRENDRE LA MAIN" x={0.05} y={0.76} />

      {/* S08 : la question au spectateur, au-dessus des deux silhouettes */}
      <Question t0={T_S08 + 45.8} t1={T_S08 + 49.9} avant={['Et']} cle="vous," apres={['à', 'onze', 'ans…', '|', 'qui', 'payait', 'pour', 'que', 'vous', 'restiez', 'à', "l'école ?"]}
        y={0.22} taille={64} />

      {/* le son des nouvelles couches : un souffle sur l'éclair, un coup grave sous le titre */}
      <Sequence from={Math.round((T_S07 - 0.55) * fps)}>
        <Audio src={staticFile('repasse/souffle.wav')} volume={0.45} />
      </Sequence>
      <Sequence from={Math.round(2.6 * fps)}>
        <Audio src={staticFile('repasse/coup.wav')} volume={0.5} />
      </Sequence>
    </AbsoluteFill>
  );
};
