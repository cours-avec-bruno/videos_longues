import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {TexteRevele} from './components/TexteRevele';
import {sec} from './specs';

/**
 * Composition de test : vérifie que la chaîne Remotion → rendu fonctionne
 * aux specs du projet. Visuel volontairement neutre (la DA n'est pas encore définie).
 */
export const TestPipeline: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();

  // Lent travelling avant (zoom très léger) + fondu au noir final.
  const zoom = interpolate(frame, [0, durationInFrames], [1, 1.06]);
  const sortie = interpolate(frame, [durationInFrames - sec(1), durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#0b0b0d', opacity: sortie}}>
      <AbsoluteFill
        style={{
          transform: `scale(${zoom})`,
          background: 'radial-gradient(ellipse at 50% 45%, #2a2a33 0%, #0b0b0d 70%)',
        }}
      />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: '0 240px'}}>
        <TexteRevele
          texte="Et si la question était plus importante que la réponse ?"
          debut={sec(0.5)}
          style={{
            color: '#f2efe9',
            fontFamily: 'Georgia, serif',
            fontSize: 84,
            lineHeight: 1.25,
            textAlign: 'center',
            transform: `scale(${zoom})`,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
