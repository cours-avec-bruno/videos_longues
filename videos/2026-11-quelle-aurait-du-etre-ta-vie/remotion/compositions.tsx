import React from 'react';
import {Folder} from 'remotion';

/**
 * Compositions Remotion de cette vidéo.
 * Le nom du Folder doit être unique (le slug de la vidéo, sans tirets en tête).
 */
export const Compositions: React.FC = () => {
  return (
    <Folder name="quelle-aurait-du-etre-ta-vie">{null}</Folder>
  );
};
