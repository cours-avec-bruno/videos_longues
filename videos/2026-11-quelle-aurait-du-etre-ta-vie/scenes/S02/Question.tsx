import React from 'react';
import {AbsoluteFill, Easing, interpolate, Sequence, useCurrentFrame} from 'remotion';
import {sec} from '../../../../shared/remotion/specs';
import {TexteRevele} from '../../../../shared/remotion/components/TexteRevele';

/**
 * S02-P06 et P07 · La question au spectateur, sur fond noir.
 * Pas de chiffre à l'écran (règle de la vidéo) : un curseur de « rien » à « tout » hésite, puis s'efface
 * et laisse la ligne vide. Puis « Notez-le. » en coupe sèche.
 */
const SERIF = 'Georgia, "Times New Roman", serif';
const CLAIR = '#d9dde3';
const DISCRET = '#7d8590';

const Curseur: React.FC = () => {
  const f = useCurrentFrame();
  const apparition = interpolate(f, [0, sec(0.8)], [0, 1], {extrapolateRight: 'clamp'});
  // le curseur cherche sa place : il avance, recule, hésite, puis disparaît sans s'être posé
  const cles = [0, sec(1.2), sec(2.4), sec(3.3), sec(4.1), sec(4.8)];
  const pos = interpolate(f, cles, [0.5, 0.68, 0.36, 0.55, 0.47, 0.5], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.sin),
  });
  const curseur = interpolate(f, [sec(0.4), sec(1), sec(5.2), sec(6)], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const L = 900;
  return (
    <div style={{position: 'absolute', top: 640, left: (1920 - L) / 2, width: L, opacity: apparition}}>
      <div style={{position: 'absolute', top: 0, left: 0, width: L, height: 1, background: DISCRET, opacity: 0.6}} />
      <div style={{position: 'absolute', top: -7, left: 0, width: 1, height: 15, background: DISCRET}} />
      <div style={{position: 'absolute', top: -7, left: L - 1, width: 1, height: 15, background: DISCRET}} />
      <div
        style={{
          position: 'absolute',
          top: -9,
          left: pos * L - 9,
          width: 18,
          height: 18,
          borderRadius: 9,
          border: `1.5px solid ${CLAIR}`,
          opacity: curseur,
        }}
      />
      <div style={{position: 'absolute', top: 26, left: -40, width: 80, textAlign: 'center', fontFamily: SERIF, fontSize: 30, color: DISCRET, fontStyle: 'italic'}}>rien</div>
      <div style={{position: 'absolute', top: 26, left: L - 40, width: 80, textAlign: 'center', fontFamily: SERIF, fontSize: 30, color: DISCRET, fontStyle: 'italic'}}>tout</div>
    </div>
  );
};

export const S02Question: React.FC = () => {
  const f = useCurrentFrame();
  const sortie = interpolate(f, [sec(10.6), sec(12)], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <Sequence durationInFrames={sec(12)}>
        <AbsoluteFill style={{opacity: sortie}}>
          <div style={{position: 'absolute', top: 400, width: '100%'}}>
            <TexteRevele
              texte="Quelle part de votre vie avez-vous choisie ?"
              debut={sec(0.6)}
              intervalle={5}
              dureeMot={18}
              style={{fontFamily: SERIF, fontSize: 64, color: CLAIR, letterSpacing: '0.01em'}}
            />
          </div>
          <Sequence from={sec(3.6)}>
            <Curseur />
          </Sequence>
        </AbsoluteFill>
      </Sequence>
      <Sequence from={sec(12)} durationInFrames={sec(4)}>
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
          <div style={{fontFamily: SERIF, fontSize: 72, color: CLAIR}}>Notez-le.</div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
