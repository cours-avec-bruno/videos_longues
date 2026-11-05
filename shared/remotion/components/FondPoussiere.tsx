import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';

type Props = {
  /** Couleur du fond (aplat). */
  fond?: string;
  /** Couleurs des particules, tirées au hasard (déterministe). */
  couleurs?: string[];
  /** Nombre de particules. */
  nombre?: number;
  /** Taille max d'une particule, en px (carrées : rendu « pixel »). */
  tailleMax?: number;
  /** Vitesse de dérive, en px par image. */
  vitesse?: number;
  /** Graine : change le tirage sans changer le style. */
  graine?: string;
  children?: React.ReactNode;
};

/**
 * Fond « tableau noir vivant » : aplat sombre + poussière de pixels qui dérive et scintille.
 * Procédé observé dans la réf. 03 (motion design 2D sur gris #343333) : le fond n'est jamais
 * parfaitement figé, ce qui évite l'effet « diapo PowerPoint » pendant les longs plans explicatifs.
 */
export const FondPoussiere: React.FC<Props> = ({
  fond = '#2f2f31',
  couleurs = ['#f5b8e6', '#ffffff', '#c98bd8'],
  nombre = 90,
  tailleMax = 4,
  vitesse = 0.25,
  graine = 'poussiere',
  children,
}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{backgroundColor: fond, overflow: 'hidden'}}>
      {new Array(nombre).fill(0).map((_, i) => {
        const r = (k: string) => random(`${graine}-${i}-${k}`);
        const x0 = r('x') * 1920;
        const y0 = r('y') * 1080;
        const angle = r('a') * Math.PI * 2;
        const v = vitesse * (0.4 + r('v'));
        const x = (((x0 + Math.cos(angle) * v * frame) % 1920) + 1920) % 1920;
        const y = (((y0 + Math.sin(angle) * v * frame) % 1080) + 1080) % 1080;
        const taille = 1 + Math.round(r('t') * (tailleMax - 1));
        // Scintillement lent, déphasé par particule.
        const scint = 0.5 + 0.5 * Math.sin(frame * (0.03 + r('f') * 0.05) + r('p') * 6.28);
        const opacite = (0.08 + r('o') * 0.35) * scint;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: taille,
              height: taille,
              backgroundColor: couleurs[Math.floor(r('c') * couleurs.length)],
              opacity: opacite,
            }}
          />
        );
      })}
      {children}
    </AbsoluteFill>
  );
};
