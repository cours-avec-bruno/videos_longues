import React from 'react';
import {P5Champ} from '../../../shared/remotion/P5Champ';
import {AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

/**
 * Les passages d'explication refaits en Remotion (Bruno, 10/11/2026), posés en plein écran sur l'aperçu :
 *   Ingenieur  (2:27 → 2:36)  le rêve « ingénieur », puis 200 vies : deux seulement y arrivent
 *   Choix      (3:15 → 3:28)  le premier choix : chaque option, ce qu'elle apporte, ce qu'elle risque
 *   Annonce    (3:37 → 3:46)  la lettre, puis pourquoi : les frais + la dette dépassent ce que gagne la famille
 *   Probas     (4:01 → 4:22)  200 vies : qui choisit quoi, qui y va, qui n'y va pas ; lui ; puis vous
 * Une même forme garde le même sens : un point = une vie née comme lui ; Manoj est le point rouge.
 * Les temps sont ABSOLUS (secondes dans l'aperçu), calés sur la voix.
 */

const CREME = '#EEE6D8';
const ROUGE = '#D6482E';
const CYAN = '#5FD3E6';
const SANS = '"Bahnschrift", "Arial Narrow", Arial, sans-serif';
const SERIF = 'Georgia, "Times New Roman", serif';
const QO = Easing.out(Easing.poly(5));
const IO = Easing.inOut(Easing.cubic);

const useT = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return f / fps;
};
const k = (t: number, a: number, d = 0.5, ease = QO) =>
  interpolate(t, [a, a + d], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
const mix = (a: number, b: number, q: number) => a + (b - a) * q;

/** Le fond commun : nuit bleu-pétrole, un halo, une grille de plan qui respire à peine. */
const Fond: React.FC<{grille?: boolean; teinte?: string}> = ({grille = false, teinte = 'rgba(16,52,62,0.9)'}) => (
  <AbsoluteFill style={{background: `radial-gradient(ellipse at 35% 30%, ${teinte} 0%, rgba(8,14,20,1) 60%, #05070a 100%), #05070a`}}>
    {/* le champ de courants (p5.js, bruit de Perlin) : le fond bouge toujours un peu */}
    <P5Champ opacite={0.2} />
    {grille ? (
      <AbsoluteFill style={{opacity: 0.18, backgroundImage:
        'linear-gradient(rgba(95,211,230,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(95,211,230,0.5) 1px, transparent 1px)',
        backgroundSize: '64px 64px', maskImage: 'radial-gradient(ellipse at 50% 45%, black 20%, transparent 75%)',
        WebkitMaskImage: 'radial-gradient(ellipse at 50% 45%, black 20%, transparent 75%)'}} />
    ) : null}
  </AbsoluteFill>
);

/** Le cartouche (capitales, filet rouge) : nomme ce qu'on regarde. */
const Cartouche: React.FC<{q: number; titre: string; sous?: string; style?: React.CSSProperties; couleur?: string; taille?: number}> =
  ({q, titre, sous, style, couleur = ROUGE, taille = 30}) => (
    <div style={{position: 'absolute', display: 'flex', gap: 12, opacity: q, transform: `translateY(${(1 - q) * 14}px)`, ...style}}>
      <div style={{width: 5, background: couleur, transform: `scaleY(${q})`, transformOrigin: 'top'}} />
      <div style={{background: 'rgba(5,8,11,0.7)', padding: '8px 16px 10px', whiteSpace: 'nowrap'}}>
        <div style={{fontFamily: SANS, fontWeight: 700, fontSize: taille, letterSpacing: '0.12em', color: CREME}}>{titre}</div>
        {sous ? <div style={{fontFamily: SANS, fontWeight: 700, fontSize: taille * 1.5, letterSpacing: '0.04em', color: couleur, marginTop: 2}}>{sous}</div> : null}
      </div>
    </div>
  );

/** Une ligne d'enjeu : + (crème) ou – (rouge), qui glisse depuis la gauche. */
const Enjeu: React.FC<{q: number; signe: '+' | '-'; texte: string}> = ({q, signe, texte}) => (
  <div style={{display: 'flex', alignItems: 'baseline', gap: 14, opacity: q, transform: `translateX(${(1 - q) * -26}px)`, margin: '10px 0'}}>
    <span style={{fontFamily: SANS, fontWeight: 700, fontSize: 34, width: 26, color: signe === '+' ? CYAN : ROUGE}}>{signe === '+' ? '+' : '–'}</span>
    <span style={{fontFamily: SANS, fontSize: 31, color: signe === '+' ? CREME : '#F1B9AE', letterSpacing: '0.01em'}}>{texte}</span>
  </div>
);

/** Une image d'illustration dans un cadre, avec une poussée lente (jamais immobile). */
const Illustration: React.FC<{src: string; t: number; t0: number; style?: React.CSSProperties}> = ({src, t, t0, style}) => {
  const z = 1.04 + 0.05 * Math.min(1, Math.max(0, (t - t0) / 6));
  return (
    <div style={{overflow: 'hidden', borderRadius: 6, boxShadow: '0 18px 50px rgba(0,0,0,0.6)', ...style}}>
      <Img src={staticFile(`repasse/img/${src}`)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z})`}} />
    </div>
  );
};

// ---------------------------------------------------------------- les 200 vies : un même nuage de points, réutilisé
type Groupe = 'jamais' | 'travail' | 'ecole' | 'echec' | 'manoj';
const VIES: Groupe[] = (() => {
  const g: Groupe[] = [];
  for (let i = 0; i < 19; i++) g.push('jamais');
  for (let i = 0; i < 5; i++) g.push('travail');
  for (let i = 0; i < 156; i++) g.push('ecole');
  for (let i = 0; i < 19; i++) g.push('echec');
  g.push('manoj');
  // mélange déterministe
  let s = 7;
  for (let i = g.length - 1; i > 0; i--) {
    s = (s * 9301 + 49297) % 233280;
    const j = Math.floor((s / 233280) * (i + 1));
    [g[i], g[j]] = [g[j], g[i]];
  }
  return g;
})();
const COLS = 20;
const grilleXY = (i: number, cx: number, cy: number, pas: number) => [cx + ((i % COLS) - (COLS - 1) / 2) * pas, cy + (Math.floor(i / COLS) - 4.5) * pas];
/** La position d'un point quand il est rangé dans un bloc (rang dans son groupe, largeur du bloc en points). */
const blocXY = (rang: number, x0: number, y0: number, cols: number, pas: number) => [x0 + (rang % cols) * pas, y0 + Math.floor(rang / cols) * pas];

const Point: React.FC<{x: number; y: number; r: number; couleur: string; halo?: number; opacite?: number}> = ({x, y, r, couleur, halo = 0, opacite = 1}) => (
  <div style={{position: 'absolute', left: x - r, top: y - r, width: 2 * r, height: 2 * r, borderRadius: '50%', background: couleur, opacity: opacite,
    boxShadow: halo ? `0 0 ${halo}px ${couleur}` : undefined}} />
);

// ---------------------------------------------------------------- 1 · ingénieur
export const Ingenieur: React.FC<{t0: number}> = ({t0}) => {
  const t = useT() + 0;
  const tl = t - t0;
  const pont = k(tl, 0.0, 2.2, IO);
  const mot = k(tl, 0.35, 0.9);
  const haut = k(tl, 3.9, 0.8, IO);           // « Sur deux cents vies » : le rêve remonte, les vies arrivent
  const tri = k(tl, 6.05, 0.9, IO);           // « deux seulement… »
  const L = 1400;
  return (
    <AbsoluteFill>
      <Fond grille />
      <div style={{position: 'absolute', left: 0, right: 0, top: mix(300, 70, haut), transform: `scale(${mix(1, 0.55, haut)})`, transformOrigin: '50% 0%'}}>
        <svg width={1920} height={300} viewBox="0 0 1920 300" style={{display: 'block'}}>
          {/* le pont qui se dessine : tablier, arc, suspentes */}
          <path d="M 260 230 L 1660 230" stroke={CYAN} strokeWidth={4} fill="none" strokeDasharray={L} strokeDashoffset={L * (1 - pont)} />
          <path d="M 360 230 Q 960 -40 1560 230" stroke={CYAN} strokeWidth={3} fill="none" strokeDasharray={1500} strokeDashoffset={1500 * (1 - pont)} opacity={0.85} />
          {Array.from({length: 13}).map((_, i) => {
            const x = 460 + i * 83.3;
            const yArc = 230 - (1 - Math.pow((x - 960) / 600, 2)) * 135;
            const a = k(tl, 0.6 + i * 0.07, 0.4);
            return <line key={i} x1={x} y1={230} x2={x} y2={mix(230, yArc, a)} stroke={CYAN} strokeWidth={2} opacity={0.6} />;
          })}
        </svg>
        <div style={{textAlign: 'center', marginTop: 20, opacity: mot, filter: `blur(${(1 - mot) * 8}px)`,
          fontFamily: SANS, fontWeight: 700, fontSize: 150, letterSpacing: `${mix(0.4, 0.22, mot)}em`, color: CREME, textShadow: '0 6px 40px rgba(0,0,0,0.7)'}}>
          INGÉNIEUR
        </div>
      </div>
      {/* les 200 vies nées comme lui ; deux seulement deviennent ingénieurs */}
      {haut > 0
        ? VIES.map((g, i) => {
            const [x, y] = grilleXY(i, 960, 690, 40);
            const app = k(tl, 3.9 + 0.004 * i, 0.4);
            const elu = i === 47 || i === 152;
            const c = elu ? ROUGE : CREME;
            const op = app * (elu ? 1 : mix(0.85, 0.16, tri));
            return <Point key={i} x={x} y={y} r={elu ? mix(9, 13, tri) : 9} couleur={c} halo={elu ? 24 * tri : 0} opacite={op} />;
          })
        : null}
      <Cartouche q={k(tl, 4.2, 0.5)} titre="200 VIES NÉES COMME LUI" style={{left: 180, top: 470}} couleur={CYAN} taille={26} />
      <Cartouche q={k(tl, 6.5, 0.5)} titre="2 DEVIENNENT INGÉNIEURS" style={{right: 180, top: 940}} taille={30} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 2 · le premier choix
const ECOLE: [('+' | '-'), string][] = [['+', 'apprendre à lire, à compter'], ['+', 'un diplôme, un métier moins dur'],
  ['-', 'des frais à payer chaque année'], ['-', 'la dette de la famille grossit']];
const TRAVAIL: [('+' | '-'), string][] = [['+', 'un salaire, tout de suite'], ['+', 'aider à rembourser la dette'],
  ['-', "l'école, finie pour de bon"], ['-', 'les champs, les bêtes, la mer']];

const Panneau: React.FC<{t: number; t0: number; titre: string; img: string; img2?: string; lignes: [('+' | '-'), string][];
  x: number; actif: number; ouvert: number}> = ({t, t0, titre, img, img2, lignes, x, actif, ouvert}) => {
  const w = 780;
  const h = mix(150, 800, ouvert);
  const swap = img2 ? k(t, t0 + 2.0, 0.8, IO) : 0;
  return (
    <div style={{position: 'absolute', left: x, top: mix(420, 170, ouvert), width: w, height: h, borderRadius: 14, overflow: 'hidden',
      background: 'rgba(8,13,18,0.86)', border: `2px solid rgba(238,230,216,${0.18 + 0.5 * actif})`, opacity: 0.35 + 0.65 * actif,
      boxShadow: actif > 0.5 ? '0 30px 80px rgba(0,0,0,0.6)' : undefined}}>
      <div style={{padding: '30px 38px 0', fontFamily: SANS, fontWeight: 700, fontSize: 46, letterSpacing: '0.08em', color: CREME}}>{titre}</div>
      {ouvert > 0.02 ? (
        <div style={{opacity: ouvert, padding: '22px 38px'}}>
          <div style={{position: 'relative', height: 330}}>
            <Illustration src={img} t={t} t0={t0} style={{position: 'absolute', inset: 0}} />
            {img2 ? <Illustration src={img2} t={t} t0={t0 + 2} style={{position: 'absolute', inset: 0, opacity: swap}} /> : null}
          </div>
          <div style={{marginTop: 18}}>
            {lignes.map(([s, l], i) => <Enjeu key={i} q={k(t, t0 + 0.45 + 0.42 * i, 0.4)} signe={s} texte={l} />)}
          </div>
        </div>
      ) : null}
    </div>
  );
};

export const Choix: React.FC<{tC1: number; tC2: number; tDecompte: [number, number]}> = ({tC1, tC2, tDecompte}) => {
  const t = useT();
  const o1 = k(t, tC1, 0.6, IO);
  const o2 = k(t, tC2, 0.6, IO);
  const final = t >= tDecompte[0] - 0.4;
  const a1 = final ? 1 : t < tC2 ? 1 : 0.45;
  const a2 = final ? 1 : t >= tC2 ? 1 : t >= tC1 ? 0.45 : 1;
  const p = interpolate(t, tDecompte, [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill>
      <Fond />
      <div style={{position: 'absolute', top: 72, width: '100%', textAlign: 'center', fontFamily: SANS, fontSize: 26, letterSpacing: '0.42em',
        color: 'rgba(238,230,216,0.7)'}}>MANOJ · 10 ANS · LE PREMIER CHOIX</div>
      <Panneau t={t} t0={tC1} titre="CONTINUER L'ÉCOLE" img="classe.png" img2="ecole.png" lignes={ECOLE} x={150} actif={a1} ouvert={final ? 1 : o1} />
      <Panneau t={t} t0={tC2} titre="TRAVAILLER POUR SA FAMILLE" img="betes.png" img2="mer.png" lignes={TRAVAIL} x={990} actif={a2} ouvert={final ? 1 : o2} />
      {final ? (
        <>
          <div style={{position: 'absolute', left: 150, right: 150, top: 1012, height: 6, background: 'rgba(238,230,216,0.15)'}} />
          <div style={{position: 'absolute', left: 150, top: 1012, height: 6, width: 1620 * p, background: CREME}} />
        </>
      ) : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 3 · l'annonce, et pourquoi
const LIGNE = "Votre famille n'a pas pu payer les frais de scolarité ; vous avez dû renoncer à poursuivre vos études.";

export const Annonce: React.FC<{tTape: [number, number]; tPourquoi: number; tFin: number}> = ({tTape, tPourquoi, tFin}) => {
  const t = useT();
  const n = Math.floor(LIGNE.length * interpolate(t, tTape, [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const tampon = k(t, tTape[1] + 0.5, 0.18, Easing.in(Easing.quad));
  const gauche = k(t, tPourquoi - 0.2, 0.8, IO);           // la lettre se range à gauche ; le pourquoi arrive à droite
  const dette = k(t, tPourquoi + 0.9, 0.6);
  const frais = k(t, tPourquoi + 1.7, 0.6);
  const deborde = k(t, tPourquoi + 2.6, 0.5);
  const sortie = 1 - k(t, tFin - 0.4, 0.4, Easing.linear);
  const H0 = 760;   // le sol des barres
  const gagne = 330, hDette = 200, hFrais = 220;
  return (
    <AbsoluteFill style={{opacity: sortie}}>
      <Fond teinte="rgba(60,22,20,0.85)" />
      {/* la lettre */}
      <div style={{position: 'absolute', left: mix(460, 120, gauche), top: mix(230, 250, gauche), width: 1000, transform: `scale(${mix(1, 0.72, gauche)}) rotate(${-1.2}deg)`,
        transformOrigin: '0% 0%', background: '#E9E1D2', borderRadius: 4, padding: '60px 70px 80px', boxShadow: '0 30px 80px rgba(0,0,0,0.6)'}}>
        <div style={{fontFamily: SANS, fontSize: 22, letterSpacing: '0.3em', color: '#6a5f55', marginBottom: 30}}>ÉCOLE PRIVÉE · AVIS À LA FAMILLE</div>
        <div style={{fontFamily: SERIF, fontSize: 52, lineHeight: 1.35, color: '#1d1a17', minHeight: 290}}>
          {LIGNE.slice(0, n)}<span style={{opacity: Math.floor(t * 2.2) % 2 === 0 ? 1 : 0, color: ROUGE}}>|</span>
        </div>
        {/* le tampon */}
        <div style={{position: 'absolute', right: 60, bottom: 40, opacity: tampon, transform: `scale(${mix(1.8, 1, tampon)}) rotate(-9deg)`,
          border: `6px solid ${ROUGE}`, color: ROUGE, fontFamily: SANS, fontWeight: 700, fontSize: 54, letterSpacing: '0.16em', padding: '6px 22px'}}>
          FRAIS IMPAYÉS
        </div>
      </div>
      {/* pourquoi : ce que gagne la famille, et ce qu'elle doit */}
      {gauche > 0.01 ? (
        <div style={{position: 'absolute', left: 940, top: 0, width: 900, height: 1080, opacity: gauche}}>
          <Illustration src="dette.png" t={t} t0={tPourquoi} style={{position: 'absolute', left: 520, top: 120, width: 360, height: 240, transform: 'rotate(2deg)'}} />
          {/* la barre de ce que gagne la famille */}
          <div style={{position: 'absolute', left: 60, top: H0 - gagne * k(t, tPourquoi + 0.2, 0.7), width: 170, height: gagne * k(t, tPourquoi + 0.2, 0.7), background: 'rgba(238,230,216,0.85)'}} />
          <div style={{position: 'absolute', left: 30, top: H0 + 18, width: 230, textAlign: 'center', fontFamily: SANS, fontSize: 22, letterSpacing: '0.12em', color: CREME}}>CE QUE GAGNE{'\n'}LA FAMILLE</div>
          {/* le niveau à ne pas dépasser */}
          <div style={{position: 'absolute', left: 30, width: 600, top: H0 - gagne, borderTop: '2px dashed rgba(238,230,216,0.5)', opacity: k(t, tPourquoi + 0.6, 0.4)}} />
          {/* ce qu'elle doit : la dette, puis les frais d'école par-dessus */}
          <div style={{position: 'absolute', left: 320, top: H0 - hDette * dette, width: 170, height: hDette * dette, background: '#8E2A1E'}} />
          <div style={{position: 'absolute', left: 320, top: H0 - hDette - hFrais * frais, width: 170, height: hFrais * frais, background: ROUGE,
            boxShadow: deborde ? `0 0 ${30 * deborde}px rgba(214,72,46,0.8)` : undefined}} />
          <div style={{position: 'absolute', left: 505, top: H0 - hDette / 2 - 16, opacity: dette, fontFamily: SANS, fontSize: 24, letterSpacing: '0.12em', color: '#F1B9AE'}}>LA DETTE</div>
          <div style={{position: 'absolute', left: 505, top: H0 - hDette - hFrais / 2 - 16, opacity: frais, fontFamily: SANS, fontSize: 24, letterSpacing: '0.12em', color: '#F1B9AE'}}>LES FRAIS D'ÉCOLE</div>
          <div style={{position: 'absolute', left: 30, width: 600, top: H0, borderTop: '2px solid rgba(238,230,216,0.35)'}} />
          <Cartouche q={deborde} titre="LA FAMILLE NE PEUT PLUS SUIVRE" style={{left: 30, top: 880}} taille={30} />
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 4 · les probabilités
export const Probas: React.FC<{tGrille: number; tChoix: number; tEchec: number; tLui: number; tSara1: number; tSara2: number; tVous: number}> =
  ({tGrille, tChoix, tEchec, tLui, tSara1, tSara2, tVous}) => {
    const t = useT();
    const qC = k(t, tChoix, 1.1, IO);      // chacun rejoint son choix
    const qE = k(t, tEchec, 1.0, IO);      // ceux qui ont choisi l'école se séparent : y vont / n'y vont pas
    const qL = k(t, tLui, 0.5);            // lui
    const qS1 = k(t, tSara1, 0.5);
    const qS2 = k(t, tSara2, 0.6);
    const qV = k(t, tVous - 1.2, 1.2, IO); // tout s'efface sauf lui
    const rangs: Record<Groupe, number> = {jamais: 0, travail: 0, ecole: 0, echec: 0, manoj: 0};
    const pas = 34;
    const points = VIES.map((g, i) => {
      const r = rangs[g]++;
      const [gx, gy] = grilleXY(i, 960, 540, 44);
      // où va chaque groupe quand il rejoint son choix
      let cx = gx, cy = gy;
      if (g === 'jamais') [cx, cy] = blocXY(r, 150, 760, 5, pas);
      if (g === 'travail') [cx, cy] = blocXY(r, 150, 320, 5, pas);
      if (g === 'ecole' || g === 'echec' || g === 'manoj') {
        const rr = g === 'ecole' ? r : 156 + (g === 'echec' ? r : 19);
        [cx, cy] = blocXY(rr, 720, 300, 16, pas);
      }
      // puis l'école se sépare : 156 y vont (en haut), 20 n'y vont pas (en bas, à part)
      let ex = cx, ey = cy;
      if (g === 'ecole') [ex, ey] = blocXY(r, 720, 230, 16, pas);
      if (g === 'echec' || g === 'manoj') [ex, ey] = blocXY(g === 'echec' ? r : 19, 720, 780, 10, pas);
      const x = mix(mix(gx, cx, qC), ex, qE);
      const y = mix(mix(gy, cy, qC), ey, qE);
      const app = k(t, tGrille + 0.003 * i, 0.4);
      let c = CREME;
      let op = 0.9;
      if (g === 'jamais') op = mix(0.9, 0.25, qC);
      if (g === 'travail') c = '#9FB3BA';
      if (g === 'echec') c = mix(0, 1, qE) > 0.5 ? '#9A4A3E' : CREME;
      if (g === 'manoj') c = qE > 0.5 ? ROUGE : CREME;
      // Sara 2 : « jamais du résultat » : on ne garde que ceux qui n'y vont pas
      if (g !== 'echec' && g !== 'manoj') op *= mix(1, 0.25, qS2);
      if (g !== 'manoj') op *= 1 - qV;
      const rLui = g === 'manoj' ? mix(11, 14, qL) : 11;
      return {x, y, c, op: op * app, r: rLui, halo: g === 'manoj' ? 30 * qL : 0};
    });
    const lui = points[VIES.indexOf('manoj')];
    // à la fin, il devient une silhouette au centre ; vous apparaissez à côté
    const qSil = k(t, tVous - 0.4, 1.0, IO);
    return (
      <AbsoluteFill>
        <Fond grille teinte="rgba(14,40,50,0.9)" />
        {points.map((p, i) => (VIES[i] === 'manoj' && qSil > 0 ? null : <Point key={i} x={p.x} y={p.y} r={p.r} couleur={p.c} opacite={p.op} halo={p.halo} />))}
        <div style={{opacity: 1 - qV}}>
          <Cartouche q={k(t, tGrille + 0.3, 0.5) * (1 - qC)} titre="200 ENFANTS NÉS COMME LUI" style={{left: 760, top: 90}} couleur={CYAN} />
          <Cartouche q={qC} titre="TRAVAILLER" sous="5" style={{left: 150, top: 230}} couleur="#9FB3BA" taille={26} />
          <Cartouche q={qC} titre="PAS LE CHOIX" sous="19" style={{left: 150, top: 670}} couleur="#55606a" taille={26} />
          <Cartouche q={qC * (1 - qE)} titre="CHOISISSENT L'ÉCOLE" sous="176" style={{left: 1290, top: 300}} couleur={CYAN} taille={26} />
          <Cartouche q={qE} titre="Y VONT" sous="156" style={{left: 1290, top: 230}} couleur={CYAN} taille={26} />
          <Cartouche q={qE} titre="N'Y VONT PAS QUAND MÊME" sous="20" style={{left: 1090, top: 800}} taille={26} />
          <Cartouche q={qL} titre="MANOJ" style={{left: lui.x - 40, top: lui.y + 26}} taille={22} />
          {/* Sara : « les choix changent les probabilités » */}
          <div style={{position: 'absolute', width: '100%', top: 965, textAlign: 'center', opacity: qS1 * (1 - qS2),
            fontFamily: SANS, fontSize: 36, letterSpacing: '0.08em', color: CREME}}>
            CHOISIR L'ÉCOLE : LA PLUPART Y VONT. <span style={{color: '#9FB3BA'}}>CHOISIR DE TRAVAILLER : AUCUN.</span>
          </div>
          <div style={{position: 'absolute', width: '100%', top: 965, textAlign: 'center', opacity: qS2,
            fontFamily: SANS, fontSize: 36, letterSpacing: '0.08em', color: '#F1B9AE'}}>
            MAIS LE BON CHOIX NE GARANTIT RIEN.
          </div>
        </div>
        {/* lui, puis vous */}
        {qSil > 0 ? (
          <>
            <Silhouette x={mix(lui.x, 790, qSil)} y={mix(lui.y, 600, qSil)} s={mix(0.12, 1, qSil)} c={ROUGE} />
            <Silhouette x={1130} y={600 + 20 * (1 - k(t, tVous + 1.0, 0.6))} s={1} c={CREME} op={k(t, tVous + 1.0, 0.6)} />
          </>
        ) : null}
      </AbsoluteFill>
    );
  };

const Silhouette: React.FC<{x: number; y: number; s: number; c: string; op?: number}> = ({x, y, s, c, op = 1}) => (
  <div style={{position: 'absolute', left: x - 60 * s, top: y - 150 * s, width: 120 * s, height: 300 * s, opacity: op}}>
    <div style={{position: 'absolute', left: 30 * s, top: 0, width: 60 * s, height: 60 * s, borderRadius: '50%', background: c}} />
    <div style={{position: 'absolute', left: 0, top: 78 * s, width: 120 * s, height: 190 * s, borderRadius: 50 * s, background: c}} />
  </div>
);
