import React from 'react';
import {random, useCurrentFrame} from 'remotion';

/**
 * Alphabet de libraryofbabel.info : minuscules sans accents, virgule, point, espace.
 * (Borges parle de 25 signes ; le site en utilise 29. Le point commun : ni majuscules ni accents.)
 */
export const ALPHABET_BABEL = 'abcdefghijklmnopqrstuvwxyz,. ';

type Props = {
  texte: string;
  /** Image où commence la résolution du premier caractère. */
  debut?: number;
  /** Images entre la résolution de deux caractères successifs. */
  vitesse?: number;
  /** Images pendant lesquelles un caractère « cherche » avant de se fixer. */
  recherche?: number;
  /** Les caractères tirés au hasard pendant la recherche. */
  alphabet?: string;
  /** Le bruit change toutes les N images (2 = nerveux, 4 = lisible). */
  cadenceBruit?: number;
  /** Sens : 'resoudre' (bruit → texte) ou 'dissoudre' (texte → bruit). */
  sens?: 'resoudre' | 'dissoudre';
  graine?: string;
  style?: React.CSSProperties;
};

/**
 * Texte qui émerge du bruit, caractère par caractère (ou s'y dissout).
 * Procédé observé dans la réf. 04 : « support technique français » se forme à partir de lettres
 * aléatoires (le motif de Babel appliqué jusque dans le sponsor), pages de charabia, adresses.
 * Déterministe (random de Remotion) : le rendu est identique à chaque export.
 */
export const TexteBrouille: React.FC<Props> = ({
  texte,
  debut = 0,
  vitesse = 2,
  recherche = 10,
  alphabet = ALPHABET_BABEL,
  cadenceBruit = 2,
  sens = 'resoudre',
  graine = 'brouille',
  style,
}) => {
  const frame = useCurrentFrame();
  const pas = Math.floor(frame / cadenceBruit);

  const caracteres = texte.split('').map((c, i) => {
    const fixe = debut + i * vitesse + recherche;
    const apparu = frame >= debut + i * vitesse;
    const resolu = sens === 'resoudre' ? frame >= fixe : frame < debut + i * vitesse;
    if (resolu) return c;
    if (sens === 'resoudre' && !apparu) return ' ';
    const k = Math.floor(random(`${graine}-${i}-${pas}`) * alphabet.length);
    const tire = alphabet[k];
    return tire === ' ' ? ' ' : tire;
  });

  return <span style={{whiteSpace: 'pre', ...style}}>{caracteres.join('')}</span>;
};
