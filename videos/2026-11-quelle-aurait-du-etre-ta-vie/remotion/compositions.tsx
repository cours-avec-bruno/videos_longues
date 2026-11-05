import React from 'react';
import {Folder} from 'remotion';

/**
 * Compositions Remotion de cette vidéo.
 * Exemple :
 *   import {Composition} from 'remotion';
 *   import {SPECS, sec} from '../../../shared/remotion/specs';
 *   import {S01} from '../scenes/S01/S01';
 *   <Composition id="S01" component={S01} durationInFrames={sec(8)} {...SPECS} />
 * Le nom du Folder doit être unique (le slug de la vidéo, sans tirets en tête).
 */
export const Compositions: React.FC = () => {
  return <Folder name="quelle-aurait-du-etre-ta-vie">{null}</Folder>;
};
