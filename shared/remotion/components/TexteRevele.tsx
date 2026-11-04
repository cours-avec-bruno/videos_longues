import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';

type Props = {
  texte: string;
  /** Image à laquelle commence l'apparition du premier mot. */
  debut?: number;
  /** Nombre d'images entre deux mots. */
  intervalle?: number;
  /** Durée d'apparition d'un mot, en images. */
  dureeMot?: number;
  style?: React.CSSProperties;
};

/**
 * Révèle un texte mot à mot (fondu + légère montée + flou qui se dissipe).
 * Brique neutre, pensée pour les citations et phrases-clés en storytelling.
 */
export const TexteRevele: React.FC<Props> = ({
  texte,
  debut = 0,
  intervalle = 4,
  dureeMot = 14,
  style,
}) => {
  const frame = useCurrentFrame();
  const mots = texte.split(' ');

  return (
    <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 0.28em', ...style}}>
      {mots.map((mot, i) => {
        const t0 = debut + i * intervalle;
        const p = interpolate(frame, [t0, t0 + dureeMot], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: Easing.out(Easing.cubic),
        });
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              opacity: p,
              transform: `translateY(${(1 - p) * 18}px)`,
              filter: `blur(${(1 - p) * 8}px)`,
            }}
          >
            {mot}
          </span>
        );
      })}
    </div>
  );
};
