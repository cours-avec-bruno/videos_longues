import React from 'react';
import {Composition, Folder} from 'remotion';
import {SPECS, sec} from '../shared/remotion/specs';
import {TestPipeline} from '../shared/remotion/TestPipeline';
import {BibliothequeProcedes} from '../shared/remotion/BibliothequeProcedes';
import {Compositions as QuelleAuraitDuEtreTaVie} from '../videos/2026-11-quelle-aurait-du-etre-ta-vie/remotion/compositions';

/**
 * Point d'entrée Remotion du studio.
 * Chaque vidéo enregistre ses compositions dans un <Folder> à son nom :
 *   import {Compositions as MaVideo} from '../videos/<slug>/remotion/compositions';
 *   puis <MaVideo /> ci-dessous.
 */
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Folder name="Outils">
        <Composition
          id="Test-Pipeline"
          component={TestPipeline}
          durationInFrames={sec(6)}
          {...SPECS}
        />
        <Composition
          id="Bibliotheque-Procedes"
          component={BibliothequeProcedes}
          durationInFrames={sec(19)}
          {...SPECS}
        />
      </Folder>
      <QuelleAuraitDuEtreTaVie />
    </>
  );
};
