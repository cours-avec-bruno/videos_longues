import React from 'react';
import {Composition, Folder} from 'remotion';
import {SPECS, sec} from '../../../shared/remotion/specs';
import {S02Question} from '../scenes/S02/Question';

/**
 * Compositions Remotion de cette vidéo.
 * Le nom du Folder doit être unique (le slug de la vidéo, sans tirets en tête).
 */
export const Compositions: React.FC = () => {
  return (
    <Folder name="quelle-aurait-du-etre-ta-vie">
      <Composition id="S02-Question" component={S02Question} durationInFrames={sec(16)} {...SPECS} />
    </Folder>
  );
};
