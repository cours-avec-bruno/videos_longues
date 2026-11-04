/**
 * Specs techniques communes à toutes les vidéos.
 * Source de vérité unique : toute composition Remotion doit s'appuyer dessus.
 * Voir docs/specs-techniques.md pour la justification des choix.
 */
export const SPECS = {
  width: 1920,
  height: 1080,
  fps: 24,
} as const;

/** Convertit des secondes en nombre d'images à la cadence du projet. */
export const sec = (secondes: number): number => Math.round(secondes * SPECS.fps);
