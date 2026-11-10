import React from 'react';
import {Composition, Folder} from 'remotion';
import {SPECS} from '../../../shared/remotion/specs';
import {Dialogue} from './Dialogue';
import {Repasse} from './Repasse';
import {S09} from './S09';
import {S10} from './S10';

/**
 * Compositions Remotion de cette vidéo.
 * Le nom du Folder doit être unique (le slug de la vidéo, sans tirets en tête).
 */
export const Compositions: React.FC = () => {
  return (
    <Folder name="quelle-aurait-du-etre-ta-vie">
      {/* durées = nombre d'images de public/dialogue/<scene>.json (scenes/S07/dialogue.py) */}
      <Composition id="Dialogue-S07" component={Dialogue} durationInFrames={864} defaultProps={{scene: 's07'}} {...SPECS} />
      {/* repasse de montage de l'aperçu S01→S08, 0 → 4:22 (Bruno, 10/11/2026) */}
      <Composition id="Repasse-01" component={Repasse} durationInFrames={6288} {...SPECS} />
      <Composition id="S10" component={S10} durationInFrames={44 * 24} {...SPECS} />
      <Composition id="S09" component={S09} durationInFrames={134 * 24} {...SPECS} />
      <Composition id="Dialogue-S08" component={Dialogue} durationInFrames={1219} defaultProps={{scene: 's08'}} {...SPECS} />
    </Folder>
  );
};
