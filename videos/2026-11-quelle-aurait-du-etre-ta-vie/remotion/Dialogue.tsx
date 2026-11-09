import React, {useEffect, useState} from 'react';
import {AbsoluteFill, continueRender, delayRender, Easing, interpolate, staticFile, useCurrentFrame} from 'remotion';

/**
 * Le dialogue des simulateurs (S07, S08) : qui parle.
 * Bruno (09/11/2026) : un motion design qui montre que les gens parlent, sobre, qui ne fasse pas « IA ».
 * Donc pas d'étiquette ni de HUD : une petite onde de quelques barres crème, accrochée à la tête de celui qui parle,
 * qui vit avec sa voix. Hors champ, l'onde reste discrètement du côté où la personne est assise.
 * Données : public/dialogue/<scene>.json (scenes/S07/dialogue.py). Rendu en PNG transparents, posé au montage.
 */
type Tete = [number, number, number] | null;
type Image = {lui: Tete; elle: Tete; parle: 'lui' | 'elle' | null; niveau: number};
type Donnees = {fps: number; debut: number; images: Image[]};

const CREME = '238, 230, 216';
const BARRES = 7;

const presence = (images: Image[], f: number, qui: 'lui' | 'elle') => {
  // une présence lissée : l'onde apparaît et disparaît en quelques images, sans clignoter entre deux mots
  let s = 0;
  let n = 0;
  for (let k = f - 5; k <= f + 5; k++) {
    if (k >= 0 && k < images.length) {
      s += images[k].parle === qui ? 1 : 0;
      n++;
    }
  }
  return n ? s / n : 0;
};

const Onde: React.FC<{images: Image[]; f: number; qui: 'lui' | 'elle'}> = ({images, f, qui}) => {
  const im = images[Math.min(f, images.length - 1)];
  const p = presence(images, f, qui);
  if (p <= 0.01) return null;
  const tete = im[qui];
  // où poser l'onde : à côté de la tête (côté extérieur), ou au bord du cadre si la tête n'est pas à l'image
  const horsChamp = !tete || tete[0] < 60 || tete[0] > 1860 || tete[1] < 40 || tete[1] > 1040;
  const r = tete && !horsChamp ? Math.max(40, Math.min(130, tete[2])) : 60;
  const echelle = r / 70;
  const x = horsChamp ? (qui === 'lui' ? 150 : 1770) : tete![0] + (qui === 'lui' ? -1 : 1) * r * 1.35;
  const y = horsChamp ? 930 : tete![1];
  const opacite = interpolate(p, [0, 1], [0, 0.9], {easing: Easing.bezier(0.16, 1, 0.3, 1)});
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        translate: '-50% -50%',
        scale: String(echelle),
        display: 'flex',
        alignItems: 'center',
        gap: 4,
        opacity: opacite,
      }}
    >
      {Array.from({length: BARRES}).map((_, i) => {
        // chaque barre lit le niveau de la voix un peu plus tôt : l'onde se propage du centre vers les bords
        const retard = Math.abs(i - (BARRES - 1) / 2);
        const src = images[Math.max(0, f - Math.round(retard))];
        const niv = src && src.parle === qui ? src.niveau : 0;
        const h = 4 + niv * (26 - retard * 4.5);
        return (
          <div
            key={i}
            style={{
              width: 3,
              height: Math.max(4, h),
              borderRadius: 2,
              background: `rgba(${CREME}, ${1 - retard * 0.12})`,
              boxShadow: `0 0 6px rgba(${CREME}, 0.35)`,
            }}
          />
        );
      })}
    </div>
  );
};

export const Dialogue: React.FC<{scene: string}> = ({scene}) => {
  const frame = useCurrentFrame();
  const [donnees, setDonnees] = useState<Donnees | null>(null);
  const [handle] = useState(() => delayRender('dialogue'));
  useEffect(() => {
    fetch(staticFile(`dialogue/${scene}.json`))
      .then((r) => r.json())
      .then((d: Donnees) => {
        setDonnees(d);
        continueRender(handle);
      });
  }, [handle, scene]);
  if (!donnees) return null;
  return (
    <AbsoluteFill>
      <Onde images={donnees.images} f={frame} qui="lui" />
      <Onde images={donnees.images} f={frame} qui="elle" />
    </AbsoluteFill>
  );
};
