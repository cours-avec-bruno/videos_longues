import React, {useEffect, useLayoutEffect, useRef, useState} from 'react';
import {cancelRender, continueRender, delayRender, Easing, interpolate, useCurrentFrame} from 'remotion';

type Props = {
  /** Image à pixeliser (staticFile, URL ou data URI ; raster ou SVG). */
  src: string;
  largeur: number;
  hauteur: number;
  /** Nombre de blocs en largeur au départ (très gros pixels = identité masquée). */
  blocsDepart?: number;
  /** Nombre de blocs en largeur à la fin (= largeur pour une image nette). */
  blocsFin?: number;
  /** Fenêtre de l'animation, en images. */
  debut?: number;
  fin?: number;
  /** Paliers : la résolution monte par crans (plus « numérique » qu'un fondu continu). */
  crans?: number;
  style?: React.CSSProperties;
};

/**
 * Image en mosaïque dont la résolution monte (ou descend) par crans.
 * Procédé observé dans la réf. 03 : un personnage « quelconque » (un participant, un électeur)
 * est montré en gros pixels : il est présent mais anonyme, et on évite d'avoir à le dessiner.
 * Inversé, c'est une révélation progressive.
 * Technique : l'image est dessinée dans un canvas minuscule (blocs × blocsH pixels réels), puis
 * affichée agrandie avec image-rendering: pixelated. Un simple <img> réduit ne suffit pas : le
 * navigateur la redessine nette à la taille finale (surtout pour un SVG).
 */
export const Mosaique: React.FC<Props> = ({
  src,
  largeur,
  hauteur,
  blocsDepart = 10,
  blocsFin = 10,
  debut = 0,
  fin = 1,
  crans = 6,
  style,
}) => {
  const frame = useCurrentFrame();
  const canvas = useRef<HTMLCanvasElement>(null);
  const [image, setImage] = useState<HTMLImageElement | null>(null);
  const [attente] = useState(() => delayRender(`Mosaique : chargement de l'image`));

  useEffect(() => {
    const img = new Image();
    img.onload = () => {
      setImage(img);
      continueRender(attente);
    };
    img.onerror = () => cancelRender(new Error(`Mosaique : image illisible (${src.slice(0, 80)})`));
    img.src = src;
  }, [src, attente]);

  const t = interpolate(frame, [debut, fin], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.in(Easing.quad),
  });
  const tCran = Math.round(t * crans) / crans;
  // Interpolation géométrique : chaque cran multiplie la finesse par un même facteur.
  const blocs = Math.max(1, Math.round(blocsDepart * Math.pow(blocsFin / blocsDepart, tCran)));
  const blocsH = Math.max(1, Math.round((blocs * hauteur) / largeur));

  useLayoutEffect(() => {
    const c = canvas.current;
    if (!c || !image) return;
    const ctx = c.getContext('2d');
    if (!ctx) return;
    ctx.imageSmoothingEnabled = true;
    ctx.clearRect(0, 0, blocs, blocsH);
    ctx.drawImage(image, 0, 0, blocs, blocsH);
  }, [image, blocs, blocsH]);

  return (
    <canvas
      ref={canvas}
      width={blocs}
      height={blocsH}
      style={{width: largeur, height: hauteur, imageRendering: 'pixelated', display: 'block', ...style}}
    />
  );
};
