/**
 * S10 : temps calés sur la voix (voix/S10_prise1.mp3), mesurés par Whisper (faster-whisper, mots horodatés).
 * Position dans la scène = temps dans la prise + décalage du morceau (des silences après chaque mort).
 */
// [début, fin] dans la prise, position dans la scène
export const S10_VOIX: [number, number, number][] = [
  [3.6, 25.6, 1.0], [25.6, 40.4, 24.0], [40.4, 49.4, 39.8], [49.4, 70.5, 49.8], [70.5, 77.76, 72.1],
];
export const S10_T = {
  manoj: 1.3, purity: 12.1, purity_fin: 22.8, fama: 25.1, fama_fin: 38.6, andrew: 41.0, andrew_fin: 48.5,
  raj: 51.0, raj_fin: 69.9, regard: 59.6, final: 72.6,
};
export const S10_DUREE = 83;
