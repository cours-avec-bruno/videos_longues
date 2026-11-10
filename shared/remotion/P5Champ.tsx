import React, {useLayoutEffect, useRef, useState} from 'react';
import {continueRender, delayRender, useCurrentFrame, useVideoConfig} from 'remotion';
import p5 from 'p5';

/**
 * Un fond génératif p5.js : un champ de courants (bruit de Perlin) dessiné en lignes fines qui ondulent.
 * Déterministe : chaque image ne dépend que de son numéro (Remotion rend les images dans le désordre, en parallèle).
 */
export const P5Champ: React.FC<{couleur?: [number, number, number]; opacite?: number; lignes?: number; graine?: number}> =
  ({couleur = [95, 211, 230], opacite = 0.22, lignes = 260, graine = 7}) => {
    const frame = useCurrentFrame();
    const {width, height, fps} = useVideoConfig();
    const hote = useRef<HTMLDivElement>(null);
    const inst = useRef<p5 | null>(null);
    const [attente] = useState(() => delayRender('p5 : premier dessin'));

    const dessiner = (p: p5, f: number) => {
      const t = f / fps;
      p.clear();
      p.noFill();
      p.randomSeed(graine);
      const w = p.width, h = p.height;
      for (let i = 0; i < lignes; i++) {
        let x = p.random(w);
        let y = p.random(h);
        p.stroke(couleur[0], couleur[1], couleur[2], 255 * opacite * (0.4 + 0.6 * p.random()));
        p.strokeWeight(0.8);
        p.beginShape();
        for (let s = 0; s < 34; s++) {
          p.vertex(x, y);
          const ang = p.noise(x * 0.004, y * 0.004, t * 0.08) * p.TWO_PI * 2;
          x += Math.cos(ang) * 4;
          y += Math.sin(ang) * 4;
        }
        p.endShape();
      }
    };

    useLayoutEffect(() => {
      if (!hote.current) return;
      inst.current = new p5((p: p5) => {
        p.setup = () => {
          const c = p.createCanvas(width / 2, height / 2);     // demi-résolution : plus doux, et quatre fois moins cher
          c.style('width', '100%');
          c.style('height', '100%');
          p.pixelDensity(1);
          p.noLoop();
          p.noiseSeed(graine);
          dessiner(p, frame);
          continueRender(attente);
        };
        p.draw = () => {};
      }, hote.current);
      return () => inst.current?.remove();
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    useLayoutEffect(() => {
      if (inst.current && inst.current.width) dessiner(inst.current, frame);
    }, [frame]); // eslint-disable-line react-hooks/exhaustive-deps

    return <div ref={hote} style={{position: 'absolute', inset: 0}} />;
  };
