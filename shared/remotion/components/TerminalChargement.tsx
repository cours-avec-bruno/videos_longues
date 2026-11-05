import React from 'react';
import {AbsoluteFill, interpolate, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {TexteBrouille} from './TexteBrouille';

const MONO = 'Consolas, "JetBrains Mono", "DejaVu Sans Mono", "Courier New", monospace';

type Props = {
  /** Libellé de la barre (ex. « INDEXATION_VOLUME_INFINI »), affiché dans la barre. */
  libelle?: string;
  /** Ligne d'en-tête au-dessus (ex. une adresse « HEX-3F2A · M4 · E5 · V32 · P410 »). */
  entete?: string;
  /** Lignes de statut en bas à gauche, en petit (ex. « [ATTENTION] »). */
  statut?: string[];
  /** Texte vertical sur le bord droit (ex. « BIBLIOTHÉCAIRE EN LIGNE »). */
  vertical?: string;
  /** Progression finale atteinte (0-1). */
  cible?: number;
  /** Nombre d'à-coups dans la progression (chargement « humain » plutôt que linéaire). */
  acoups?: number;
  couleur?: string;
  graine?: string;
};

/**
 * Carton de transition « machine » : écran noir, barre de chargement à à-coups, statuts système.
 * Procédé observé dans la réf. 04 : chaque changement de lieu passe par un faux terminal
 * (INDEXATION_VOLUME_INFINI, OUVERTURE_GALERIE_∞, // RETOUR DÉBUT //). Les messages
 * (« AUCUNE VÉRIFICATION POSSIBLE », « LA PAGE AFFICHÉE PEUT ÊTRE VRAIE… ») préparent
 * en sous-main la révélation finale (la machine = l'IA) : c'est un plant/payoff typographique.
 */
export const TerminalChargement: React.FC<Props> = ({
  libelle = 'INDEXATION_VOLUME_INFINI',
  entete,
  statut = [],
  vertical,
  cible = 1,
  acoups = 5,
  couleur = '#d8d8d8',
  graine = 'terminal',
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();

  // Progression en marches d'escalier : paliers tirés au hasard, puis petit rattrapage.
  const paliers = new Array(acoups).fill(0).map((_, i) => ({
    t: Math.round(((i + 1) / (acoups + 1)) * durationInFrames * (0.7 + 0.3 * random(`${graine}-t${i}`))),
    v: ((i + 1) / acoups) * cible * (0.8 + 0.2 * random(`${graine}-v${i}`)),
  }));
  let progression = 0;
  for (const p of paliers) {
    if (frame >= p.t) progression = p.v;
  }
  progression = Math.min(cible, progression);

  // Apparition sèche (pas de fondu) : 2 images de clignotement, comme un écran qui s'allume.
  const allume = frame < 2 ? (frame % 2 === 0 ? 0 : 1) : 1;
  const curseur = Math.floor(frame / 12) % 2 === 0;

  return (
    <AbsoluteFill style={{backgroundColor: '#000', fontFamily: MONO, color: couleur, opacity: allume}}>
      {entete ? (
        <div style={{position: 'absolute', top: 130, width: '100%', textAlign: 'center', fontSize: 52, letterSpacing: 2}}>
          <TexteBrouille texte={entete} vitesse={1} recherche={8} alphabet="0123456789ABCDEF·" graine={`${graine}-e`} />
        </div>
      ) : null}

      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          width: 1200,
          height: 56,
          transform: 'translate(-50%, -50%)',
          border: `3px solid ${couleur}`,
          opacity: 0.85,
        }}
      >
        <div style={{position: 'absolute', inset: 0, width: `${progression * 100}%`, backgroundColor: couleur, opacity: 0.55}} />
        <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 26, letterSpacing: 3}}>
          {libelle}
          <span style={{opacity: curseur ? 1 : 0}}>&nbsp;_</span>
        </div>
      </div>

      {statut.length ? (
        <div style={{position: 'absolute', left: 6, bottom: 8, fontSize: 24, lineHeight: 1.25, opacity: 0.9}}>
          {statut.map((l, i) => (
            <div key={i}>{l}</div>
          ))}
        </div>
      ) : null}

      {vertical ? (
        <div
          style={{
            position: 'absolute',
            right: 18,
            top: '50%',
            transform: 'translateY(-50%) rotate(90deg)',
            transformOrigin: 'center',
            fontSize: 20,
            letterSpacing: 3,
            whiteSpace: 'nowrap',
            opacity: interpolate(frame, [6, 14], [0, 0.85], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
          }}
        >
          {vertical}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
