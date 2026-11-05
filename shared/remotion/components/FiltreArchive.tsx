import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';

type Props = {
  children: React.ReactNode;
  /** Mention de la source, en bas à gauche (titre du film, de l'émission…). */
  source?: string;
  /** Couleur d'unification : teinte toutes les sources hétérogènes vers une même dominante. */
  teinte?: string;
  /** Force de la teinte (0-1). */
  forceTeinte?: number;
  /** Décalage des canaux rouge / bleu, en px (aberration chromatique). */
  aberration?: number;
  /** Opacité des lignes de balayage (0 = aucune). */
  balayage?: number;
  /** Force du vignettage « écran bombé » (0-1). */
  bombe?: number;
  /** Opacité du grain (0-1). */
  grain?: number;
  /** Identifiant unique si plusieurs filtres sont à l'écran en même temps. */
  id?: string;
};

/**
 * Traitement « archive / écran cathodique » pour intégrer des extraits hétérogènes (films, JT,
 * animés, captures) dans un même univers. Procédé observé dans la réf. 03 : chaque extrait reçoit
 * lignes de balayage, aberration chromatique, coins assombris et bombés, teinte magenta commune,
 * et sa source en petit en bas à gauche. Résultat : 40 sources différentes se lisent comme une seule
 * matière, et la mention de source règle la question du crédit sans casser l'image.
 */
export const FiltreArchive: React.FC<Props> = ({
  children,
  source,
  teinte = '#b86bd6',
  forceTeinte = 0.18,
  aberration = 3,
  balayage = 0.12,
  bombe = 0.6,
  grain = 0.08,
  id = 'archive',
}) => {
  const frame = useCurrentFrame();
  const idFiltre = `ca-${id}`;
  const idGrain = `grain-${id}`;

  return (
    <AbsoluteFill style={{backgroundColor: '#000', overflow: 'hidden'}}>
      <svg width="0" height="0" style={{position: 'absolute'}}>
        <defs>
          {/* Aberration chromatique : on isole R et B, on les décale en sens opposés, on recompose. */}
          <filter id={idFiltre} x="-5%" y="-5%" width="110%" height="110%" colorInterpolationFilters="sRGB">
            <feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
            <feOffset in="r" dx={-aberration} dy="0" result="r2" />
            <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g" />
            <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b" />
            <feOffset in="b" dx={aberration} dy="0" result="b2" />
            <feBlend in="r2" in2="g" mode="screen" result="rg" />
            <feBlend in="rg" in2="b2" mode="screen" />
          </filter>
          <filter id={idGrain}>
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={frame % 97} />
            <feColorMatrix type="saturate" values="0" />
          </filter>
        </defs>
      </svg>

      {/* L'image, légèrement agrandie pour que le bombé ne laisse pas voir de bord. */}
      <AbsoluteFill style={{filter: `url(#${idFiltre}) contrast(1.06) saturate(0.9)`, transform: 'scale(1.03)'}}>
        {children}
      </AbsoluteFill>

      {/* Teinte d'unification. */}
      <AbsoluteFill style={{backgroundColor: teinte, mixBlendMode: 'soft-light', opacity: forceTeinte * 2}} />
      <AbsoluteFill style={{backgroundColor: teinte, mixBlendMode: 'color', opacity: forceTeinte * 0.5}} />

      {/* Lignes de balayage, qui défilent très lentement. */}
      {balayage > 0 ? (
        <AbsoluteFill
          style={{
            backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.9) 0px, rgba(0,0,0,0.9) 1px, transparent 1px, transparent 4px)',
            backgroundPositionY: `${(frame * 0.5) % 4}px`,
            opacity: balayage,
            mixBlendMode: 'multiply',
          }}
        />
      ) : null}

      {/* Grain. */}
      {grain > 0 ? (
        <AbsoluteFill style={{filter: `url(#${idGrain})`, opacity: grain, mixBlendMode: 'overlay', backgroundColor: '#808080'}} />
      ) : null}

      {/* Écran bombé : coins sombres et arrondis + léger halo sur les bords. */}
      <AbsoluteFill
        style={{
          borderRadius: 28,
          boxShadow: `inset 0 0 ${180 * bombe}px ${60 * bombe}px rgba(0,0,0,${0.75 * bombe}), 0 0 0 40px #000`,
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 75% 70% at 50% 50%, transparent 60%, rgba(0,0,0,${0.55 * bombe}) 100%)`,
        }}
      />

      {source ? (
        <div
          style={{
            position: 'absolute',
            left: 22,
            bottom: 18,
            fontFamily: '"Segoe UI", "Helvetica Neue", Arial, sans-serif',
            fontWeight: 700,
            fontSize: 26,
            color: '#fff',
            opacity: 0.72,
            textShadow: '0 1px 3px rgba(0,0,0,0.6)',
          }}
        >
          {source}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
