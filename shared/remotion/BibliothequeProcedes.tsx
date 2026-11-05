import React from 'react';
import {AbsoluteFill, interpolate, Sequence, useCurrentFrame} from 'remotion';
import {FondPoussiere} from './components/FondPoussiere';
import {TexteBrouille} from './components/TexteBrouille';
import {TerminalChargement} from './components/TerminalChargement';
import {FiltreArchive} from './components/FiltreArchive';
import {Mosaique} from './components/Mosaique';
import {sec} from './specs';

/**
 * Planche de démonstration des procédés extraits des réf. 03 et 04
 * (voir docs/direction-artistique/procedes/catalogue.md).
 * Visuels volontairement neutres : ce sont des briques, pas une DA.
 */

const SANS = '"Montserrat", "Segoe UI", "Helvetica Neue", Arial, sans-serif';

/** Scène procédurale servant de « faux extrait de film » pour le filtre archive. */
const FauxExtrait: React.FC = () => {
  const frame = useCurrentFrame();
  const derive = interpolate(frame, [0, sec(5)], [0, -40]);
  return (
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #6f8fd8 0%, #b7c7ee 55%, #e8d9c2 56%, #d9c3a2 100%)'}}>
      <div style={{position: 'absolute', left: 1350 + derive, top: 240, width: 160, height: 160, borderRadius: '50%', background: '#fff5d6', boxShadow: '0 0 80px 30px rgba(255,240,200,0.6)'}} />
      {/* Silhouette assise, de profil. */}
      <div style={{position: 'absolute', left: 620, top: 470, width: 150, height: 150, borderRadius: '50%', background: '#1c1a22'}} />
      <div style={{position: 'absolute', left: 560, top: 590, width: 330, height: 300, borderRadius: '45% 55% 10% 10%', background: '#1c1a22', transform: 'rotate(-8deg)'}} />
      <div style={{position: 'absolute', left: 820, top: 800, width: 420, height: 90, borderRadius: 45, background: '#24212b'}} />
    </AbsoluteFill>
  );
};

/** Portrait abstrait en SVG (data URI) pour la mosaïque. */
const PORTRAIT =
  'data:image/svg+xml;utf8,' +
  encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">
      <rect width="400" height="300" fill="#2b3a2f"/>
      <rect x="0" y="0" width="400" height="120" fill="#4a5d3a"/>
      <ellipse cx="200" cy="140" rx="70" ry="85" fill="#e3a07a"/>
      <ellipse cx="200" cy="80" rx="78" ry="45" fill="#3b2a1e"/>
      <rect x="110" y="215" width="180" height="85" rx="30" fill="#f2efe9"/>
      <rect x="185" y="215" width="30" height="85" fill="#b0262f"/>
      <circle cx="175" cy="140" r="7" fill="#222"/><circle cx="225" cy="140" r="7" fill="#222"/>
    </svg>`,
  );

export const BibliothequeProcedes: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      {/* 1. Fond poussière + texte qui émerge du bruit (réf. 03 + réf. 04). */}
      <Sequence durationInFrames={sec(5)} name="Fond poussière + texte brouillé">
        <FondPoussiere>
          <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 40}}>
            <TexteBrouille
              texte="tout est deja ecrit"
              debut={sec(0.4)}
              vitesse={3}
              recherche={14}
              style={{fontFamily: 'Georgia, "Times New Roman", serif', fontSize: 84, color: '#f2efe9', letterSpacing: 6}}
            />
            <TexteBrouille
              texte="LE RAISONNEMENT MOTIVÉ"
              debut={sec(2)}
              vitesse={2}
              recherche={10}
              alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ#%&"
              graine="titre"
              style={{fontFamily: SANS, fontWeight: 800, fontSize: 64, color: '#f5b8e6', textShadow: '0 0 18px rgba(245,184,230,0.55)'}}
            />
          </AbsoluteFill>
        </FondPoussiere>
      </Sequence>

      {/* 2. Carton de transition « terminal » (réf. 04). */}
      <Sequence from={sec(5)} durationInFrames={sec(4)} name="Terminal de chargement">
        <TerminalChargement
          entete="HEX-3F2A · M4 · E5 · V32 · P410"
          libelle="OUVERTURE_GALERIE_∞"
          statut={['[ATTENTION]', 'RECHERCHE_1 ABANDONNÉE : AUCUN INDEX TROUVÉ. GÉNÉRATION_2 EN COURS. AUCUNE VÉRIFICATION POSSIBLE']}
          vertical="BIBLIOTHÉCAIRE EN LIGNE"
          cible={0.94}
        />
      </Sequence>

      {/* 3. Filtre archive / cathodique sur un faux extrait (réf. 03). */}
      <Sequence from={sec(9)} durationInFrames={sec(5)} name="Filtre archive">
        <FiltreArchive source="Extrait · titre de l'œuvre">
          <FauxExtrait />
        </FiltreArchive>
      </Sequence>

      {/* 4. Mosaïque qui se résout par crans (réf. 03). */}
      <Sequence from={sec(14)} durationInFrames={sec(5)} name="Mosaïque">
        <FondPoussiere>
          <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
            <Mosaique src={PORTRAIT} largeur={640} hauteur={480} blocsDepart={8} blocsFin={320} debut={sec(1)} fin={sec(4)} crans={6} style={{boxShadow: '0 0 40px rgba(0,0,0,0.6)'}} />
          </AbsoluteFill>
        </FondPoussiere>
      </Sequence>
    </AbsoluteFill>
  );
};
