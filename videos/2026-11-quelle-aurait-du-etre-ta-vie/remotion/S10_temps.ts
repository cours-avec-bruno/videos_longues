/**
 * S10 : temps calés sur la voix (voix/S10_prise1.mp3), mesurés par Whisper (faster-whisper, mots horodatés).
 * Version courte (Bruno, 10/11 : « trop longue ») : une ou deux phrases par vie ; Raj et Manoj gardent leur place.
 */
// [début, fin] dans la prise, position dans la scène
export const S10_VOIX: [number, number, number][] = [
  [3.86, 10.72, 1.0],     // Manoj n'est pas le seul. La même année… quatre autres naissances, parmi toutes celles du monde.
  [14.74, 15.92, 8.36],   // Purity est née au Kenya.
  [16.82, 18.10, 9.84],   // Elle va jusqu'au bout du lycée.
  [23.72, 25.36, 11.42],  // Son cœur s'arrête à soixante-six ans.
  [26.68, 29.54, 13.66],  // Fama est née en Guinée. Elle ne va jamais à l'école.
  [38.94, 40.18, 16.82],  // Elle meurt à soixante-quatre ans.
  [41.60, 45.18, 18.66],  // Andrew, au Kenya lui aussi, garde des troupeaux toute sa vie,
  [47.78, 49.14, 22.54],  // Il meurt à cinquante et un ans.
  [50.60, 61.14, 24.6],   // Et puis il y a Raj… dalit… parmi les plus pauvres… Lui aussi s'arrête après le primaire.
  [67.88, 69.50, 35.44],  // Il vivra jusqu'à quatre-vingt-un ans.
  [75.50, 77.68, 37.9],   // Aucun d'eux n'a choisi l'endroit où il allait naître.
];
export const S10_T = {
  manoj: 1.0, purity: 8.36, purity_fin: 12.9, fama: 13.66, fama_fin: 17.9, andrew: 18.66, andrew_fin: 23.7,
  raj: 24.6, raj_fin: 36.9, regard: 33.16, final: 37.9,
};
export const S10_DUREE = 44;
