import React from 'react';
import {Composition, Folder} from 'remotion';
import {SPECS} from '../../../shared/remotion/specs';
import {Dialogue} from './Dialogue';

/**
 * Compositions Remotion de cette vidéo.
 * Le nom du Folder doit être unique (le slug de la vidéo, sans tirets en tête).
 */
export const Compositions: React.FC = () => {
  return (
    <Folder name="quelle-aurait-du-etre-ta-vie">
      {/* durées = nombre d'images de public/dialogue/<scene>.json (scenes/S07/dialogue.py) */}
      <Composition id="Dialogue-S07" component={Dialogue} durationInFrames={864} defaultProps={{scene: 's07'}} {...SPECS} />
      <Composition id="Dialogue-S08" component={Dialogue} durationInFrames={1219} defaultProps={{scene: 's08'}} {...SPECS} />
    </Folder>
  );
};
