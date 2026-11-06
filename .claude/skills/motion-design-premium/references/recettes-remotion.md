# Recettes de code — motion design premium dans Remotion

Tout est **fonction pure de la frame** et **seedé**. Les snippets sont en TypeScript,
pensés pour un canvas 2D plein cadre redessiné dans `useLayoutEffect`.

---

## 1. Fonctions de mise en forme (Inigo Quilez) — enveloppes et courbes

```ts
export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
export const remap = (v: number, a: number, b: number) => clamp01((v - a) / (b - a));

/** Impulsion : montée rapide, décroissance lente. Max = 1 atteint en x = 1/k. */
export const expImpulse = (x: number, k: number) => {
  if (x <= 0) return 0;
  const h = k * x;
  return h * Math.exp(1 - h);
};
/** Impulsion à attaque (f) et relâche (k) indépendantes. */
export const sustainedImpulse = (x: number, f: number, k: number) => {
  if (x <= 0) return 0;
  const s = Math.max(x - f, 0);
  return Math.min((x * x) / (f * f), 1 + (2 / f) * s * Math.exp(-k * s));
};
/** Cloche centrée en c, largeur w (alternative à une gaussienne, support fini). */
export const cubicPulse = (c: number, w: number, x: number) => {
  let d = Math.abs(x - c);
  if (d > w) return 0;
  d /= w;
  return 1 - d * d * (3 - 2 * d);
};
/** 0 aux bords, 1 au centre ; k règle la forme. */
export const parabola = (x: number, k: number) => Math.pow(4 * x * (1 - x), k);
/** Contraste d'une progression 0..1 (k > 1 : S plus marqué). */
export const gain = (x: number, k: number) => {
  const a = 0.5 * Math.pow(2 * (x < 0.5 ? x : 1 - x), k);
  return x < 0.5 ? a : 1 - a;
};
/** Amortissement exponentiel en forme close (a → b), demi-vie en frames. */
export const damp = (a: number, b: number, framesElapsed: number, halfLife: number) =>
  b + (a - b) * Math.pow(0.5, framesElapsed / halfLife);
```

Usages : lueur de détection = `expImpulse((f - tHit) / 60, 6)` (pic à ~10 fr) ;
flash = `sustainedImpulse(fLocal, 2, 0.25)` ; respiration = `0.5 + 0.5 * Math.sin(...)` modulée par `gain`.

Courbes de Bézier utiles (`Easing.bezier` de Remotion) :
- expo-out premium `(0.16, 1, 0.3, 1)` · M3 emphasized-decelerate `(0.05, 0.7, 0.1, 1)`
- expo-in (sorties, aspiration) `(0.7, 0, 0.84, 0)` · standard M3 `(0.2, 0, 0, 1)`

---

## 2. Aléatoire seedé

```ts
export const mulberry32 = (seed: number) => () => {
  let t = (seed += 0x6d2b79f5);
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
/** Hash déterministe (i, salt) → [0, 1) : pour des valeurs par frame (grain, scintillement). */
export const hash1 = (i: number, salt = 0) => {
  let h = Math.imul(i ^ 0x9e3779b9, 0x85ebca6b) ^ Math.imul(salt + 0x27d4eb2f, 0xc2b2ae35);
  h = Math.imul(h ^ (h >>> 16), 0x7feb352d);
  h = Math.imul(h ^ (h >>> 15), 0x846ca68b);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
};
/** Taille en loi de puissance : beaucoup de petites, quelques grosses. */
export const powerSize = (u: number, min: number, max: number, alpha = 2.2) =>
  min * Math.pow(1 - u * (1 - Math.pow(min / max, alpha - 1)), -1 / (alpha - 1));
```

---

## 3. Échantillonnage Poisson-disk (Bridson) dans une forme — blue noise

```ts
/** Points espacés d'au moins r dans [0,w]x[0,h], acceptés par inside(x,y). */
export const poissonDisk = (w: number, h: number, r: number, inside: (x: number, y: number) => boolean,
  rand: () => number, k = 24) => {
  const cell = r / Math.SQRT2;
  const gw = Math.ceil(w / cell), gh = Math.ceil(h / cell);
  const grid = new Int32Array(gw * gh).fill(-1);
  const pts: [number, number][] = [];
  const active: number[] = [];
  const add = (x: number, y: number) => {
    pts.push([x, y]);
    active.push(pts.length - 1);
    grid[Math.floor(y / cell) * gw + Math.floor(x / cell)] = pts.length - 1;
  };
  // graine : premier point accepté
  for (let t = 0; t < 1000; t++) { const x = rand() * w, y = rand() * h; if (inside(x, y)) { add(x, y); break; } }
  while (active.length) {
    const ai = Math.floor(rand() * active.length);
    const [px, py] = pts[active[ai]];
    let found = false;
    for (let n = 0; n < k; n++) {
      const a = rand() * Math.PI * 2, d = r * (1 + rand());
      const x = px + Math.cos(a) * d, y = py + Math.sin(a) * d;
      if (x < 0 || y < 0 || x >= w || y >= h || !inside(x, y)) continue;
      const gx = Math.floor(x / cell), gy = Math.floor(y / cell);
      let ok = true;
      for (let j = Math.max(0, gy - 2); j <= Math.min(gh - 1, gy + 2) && ok; j++)
        for (let i = Math.max(0, gx - 2); i <= Math.min(gw - 1, gx + 2); i++) {
          const q = grid[j * gw + i];
          if (q >= 0 && (pts[q][0] - x) ** 2 + (pts[q][1] - y) ** 2 < r * r) { ok = false; break; }
        }
      if (ok) { add(x, y); found = true; break; }
    }
    if (!found) active.splice(ai, 1);
  }
  return pts;
};
```
Densité variable (plus dense sur les yeux) : faire deux passes (r petit dans le masque des traits, r grand ailleurs) ou rejeter selon une probabilité `density(x, y)`.

---

## 4. Attribution départ → cible sans chaos

```ts
/** Associe chaque départ à une cible en préservant l'ordre angulaire autour d'un centre :
 *  les trajectoires ne se croisent presque pas → convergence lisible et élégante. */
export const assignByAngle = <T extends { x: number; y: number }>(from: T[], to: T[], cx: number, cy: number) => {
  const key = (p: T) => Math.atan2(p.y - cy, p.x - cx) * 1000 + Math.hypot(p.x - cx, p.y - cy) * 1e-3;
  const a = from.map((p, i) => ({ i, k: key(p) })).sort((u, v) => u.k - v.k);
  const b = to.map((p, i) => ({ i, k: key(p) })).sort((u, v) => u.k - v.k);
  const map = new Int32Array(from.length);
  a.forEach((u, n) => (map[u.i] = b[Math.floor((n * b.length) / a.length)].i));
  return map; // map[indexDépart] = indexCible
};
```
Variante « tranches » : trier les deux ensembles par projection sur 2–3 directions et moyenner (approximation d'un transport optimal).
Si l'on *veut* du tourbillon : ajouter un angle de spirale proportionnel à la distance restante.

---

## 5. Morphing avec délai spatial (vague organique)

```ts
/** progress global g ∈ [0,1] → progression propre à la particule. spread = part du temps consacrée au décalage. */
export const localProgress = (g: number, px: number, py: number, noise2: (x: number, y: number) => number,
  spread = 0.45, jitter = 0.05, rnd = 0.5) => {
  const n = 0.5 + 0.5 * noise2(px * 0.0022, py * 0.0022); // basse fréquence : cohérent dans l'espace
  const delay = spread * clamp01(n + (rnd - 0.5) * jitter);
  const t = clamp01((g - delay) / (1 - spread));
  return t * t * (3 - 2 * t); // smoothstep (ou un ressort)
};
// Position : arc au lieu d'une ligne droite
// mid = milieu + normale * courbure * (distance) ; p = bezierQuad(start, mid, target, localProgress)
```
Pendant le trajet : taille ×(1 + 0,6·parabola(t,1)), luminosité ↑ puis retour → les particules « en vol » brillent.

---

## 6. Curl noise 2D (dérive fluide sans amas)

```ts
/** Champ de vitesse sans divergence à partir d'un bruit scalaire n(x, y, t). */
export const curl2 = (n: (x: number, y: number, t: number) => number, x: number, y: number, t: number, e = 0.01) => {
  const dx = (n(x + e, y, t) - n(x - e, y, t)) / (2 * e);
  const dy = (n(x, y + e, t) - n(x, y - e, t)) / (2 * e);
  return [dy, -dx] as const; // rotation du gradient de 90°
};
```
Pour rester une **fonction pure de la frame** : déplacement = `base + A * curl2(n, base.x * f0, base.y * f0, frame * speed)`
(on ne l'intègre pas dans le temps), ou pré-calculer une advection sur une table au chargement du module.
Tyler Hobbs : éviter le Perlin « brut » trop reconnaissable → sommer 2–3 octaves, distordre le domaine (domain warping).

---

## 7. Motion blur analytique (traînées, tunnel « hyperespace »)

```ts
// pos(i, f) : position projetée de la particule i à la frame f (fonction pure)
const SHUTTER = 0.5; // 180° ; 1–1,5 pendant les rushs ; tunnel : jusqu'à 3–6
const p1 = pos(i, frame);
const p0 = pos(i, frame - SHUTTER);
const len = Math.hypot(p1.x - p0.x, p1.y - p0.y);
if (len < r * 2) drawDot(p1); else drawStreak(p0, p1); // gradient 0 → alpha, lineCap round
// Conserver l'énergie : alpha_traînée ≈ alpha * min(1, k / len) — une ligne longue est plus diffuse.
```
C'est exactement le principe des « étoiles qui s'étirent » de *Star Wars* (pose longue pendant que la caméra avance).
La caméra aussi : projeter avec `cam(frame - SHUTTER)` pour p0 → le flou suit les mouvements de caméra.

---

## 8. Bloom multi-échelle en canvas 2D (bon marché)

```ts
// Canvases réutilisés (module-level). Coût : 3 petits drawImage + filtres sur ¼ et ⅛ de résolution.
const mk = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; };
const q = mk(270, 480), e = mk(135, 240);

export const bloom = (dst: CanvasRenderingContext2D, src: HTMLCanvasElement, strength = 0.8) => {
  const qc = q.getContext("2d")!, ec = e.getContext("2d")!;
  qc.clearRect(0, 0, 270, 480);
  qc.filter = "blur(3px)";            // ≈ 12 px à pleine résolution
  qc.drawImage(src, 0, 0, 270, 480);
  qc.filter = "none";
  ec.clearRect(0, 0, 135, 240);
  ec.filter = "blur(4px)";            // ≈ 32 px
  ec.drawImage(src, 0, 0, 135, 240);
  ec.filter = "none";
  dst.save();
  dst.globalCompositeOperation = "lighter";
  dst.imageSmoothingQuality = "high";
  dst.globalAlpha = 0.55 * strength; dst.drawImage(q, 0, 0, 1080, 1920);
  dst.globalAlpha = 0.35 * strength; dst.drawImage(e, 0, 0, 1080, 1920);
  dst.restore();
};
```
Seuil : dessiner d'abord seulement les éléments « importants » dans `src` (canvas dédié), pas toute la scène.
Alternative GPU : `<HtmlInCanvas effects={[glow({radius, intensity, threshold})]}>` (`@remotion/effects/glow`, `--gl=angle`).

---

## 9. Speed ramp (time remapping) sans cassure

```ts
// Vitesse du temps local (1 = normal). Pré-intégrée une fois → t(f) continu et dérivable.
const SPEED_KEYS = [ { f: 0, v: 1 }, { f: 540, v: 1 }, { f: 556, v: 0.25 }, { f: 590, v: 0.25 }, { f: 598, v: 2.2 }, { f: 640, v: 1 } ];
const STEP = 0.25;
const T = (() => {
  const n = Math.ceil(4000 / STEP); const out = new Float64Array(n); let t = 0;
  for (let k = 0; k < n; k++) { out[k] = t; t += keyedSmooth(k * STEP, SPEED_KEYS) * STEP; }
  return out;
})();
export const timeAt = (f: number) => { const k = Math.max(0, f / STEP); const i = Math.floor(k); return T[i] + (T[i + 1] - T[i]) * (k - i); };
// Dans la scène : const t = timeAt(useCurrentFrame()); puis toutes les animations lisent t au lieu de frame.
```
Règle : le ralenti commence *juste avant* l'impact, l'accélération qui suit est plus brutale que le ralenti.

---

## 10. Dolly-zoom (effet Vertigo) — « le cerveau comprend »

```ts
// Sujet à z = zs, caméra qui avance de camZ0 à camZ1 ; la focale compense pour garder la taille du sujet.
const camZ = interpolate(f, [a, b], [camZ0, camZ1], { easing: Easing.inOut(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const d0 = zs - camZ0;
const focal = FOCAL * (zs - camZ) / d0; // taille du sujet constante, le décor s'étire
```

---

## 11. Texte → particules (après chargement de la police)

```ts
import { continueRender, delayRender } from "remotion";

const [handle] = useState(() => delayRender("police pour échantillonnage"));
const [pts, setPts] = useState<[number, number][] | null>(null);
useEffect(() => {
  document.fonts.load('600 160px "Space Grotesk"').then(() => {
    const c = document.createElement("canvas"); c.width = 1080; c.height = 400;
    const g = c.getContext("2d")!;
    g.font = '600 160px "Space Grotesk"'; g.textAlign = "center"; g.textBaseline = "middle";
    (g as CanvasRenderingContext2D & { letterSpacing: string }).letterSpacing = "18px";
    g.fillStyle = "#fff"; g.fillText("PARÉIDOLIE", 540, 200);
    const d = g.getImageData(0, 0, 1080, 400).data;
    const out: [number, number][] = [];
    for (let y = 0; y < 400; y += 4) for (let x = 0; x < 1080; x += 4) if (d[(y * 1080 + x) * 4 + 3] > 128) out.push([x, y]);
    setPts(out); continueRender(handle);
  });
}, [handle]);
```
Mieux : faire l'échantillonnage une seule fois hors rendu (script Node) et committer un JSON de points — zéro dépendance au timing de police.
Chaque lettre garde l'index de son glyphe → désassemblage lettre par lettre (stagger), puis chaque point part vers un nœud du réseau (attribution §4).

---

## 12. Scanner : faisceau angulaire + détection

```ts
const ang = baseAngle + speed * f;                           // rad
const g = ctx.createConicGradient(ang - TRAIL, cx, cy);      // Chrome ≥ 99
g.addColorStop(0, "rgba(70,227,255,0)");
g.addColorStop(TRAIL / (2 * Math.PI) * 0.85, "rgba(70,227,255,0.10)");
g.addColorStop(TRAIL / (2 * Math.PI), "rgba(200,245,255,0.55)"); // bord d'attaque vif
g.addColorStop(TRAIL / (2 * Math.PI) + 0.002, "rgba(70,227,255,0)");
ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.fill();

// Détection d'une cible à l'angle a_i : frames écoulées depuis le dernier passage du faisceau
const since = (((ang - a_i) % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI) / speed;
const glow = expImpulse(since / 60, 7);                     // la zone s'illumine immédiatement puis décroît
```
Crochets de verrouillage : 4 coins qui partent de ±60 px et se referment avec `spring({damping: 12, stiffness: 220, mass: 0.6})`, puis une étiquette mono qui tape ses caractères (1 caractère / 2 fr).

---

## 13. Réseau neuronal : graphe, cascade pré-calculée, impulsions

```ts
// Arêtes : k plus proches voisins (k = 3–4), dédupliquées ; longueur max pour éviter les grandes diagonales.
// Cascade : BFS depuis des sources ; chaque activation déclenche ses voisins après un délai ∝ longueur.
type Act = { node: number; at: number };
export const cascade = (adj: number[][], len: (a: number, b: number) => number, sources: number[], t0: number,
  pxPerFrame = 14, refractory = 40, rand: () => number) => {
  const last = new Float64Array(adj.length).fill(-1e9);
  const acts: Act[] = []; const queue: Act[] = sources.map((n) => ({ node: n, at: t0 }));
  while (queue.length) {
    queue.sort((a, b) => a.at - b.at); const a = queue.shift()!;
    if (a.at - last[a.node] < refractory || a.at > t0 + 600) continue;
    last[a.node] = a.at; acts.push(a);
    for (const nb of adj[a.node]) if (rand() < 0.62) queue.push({ node: nb, at: a.at + len(a.node, nb) / pxPerFrame });
  }
  return acts; // pré-calculé au niveau module
};
// Impulsion sur l'arête (a→b) partie à t : u = inQuad(clamp01((f - t) / dur)) → accélère, flash du nœud à l'arrivée (expImpulse).
```

---

## 14. Aberration chromatique radiale (canvas 2D, optionnelle)

```ts
// Sur un calque lumineux (fond noir) : 3 copies teintées, légèrement mises à l'échelle autour du centre.
const split = (dst: CanvasRenderingContext2D, layer: HTMLCanvasElement, tmp: HTMLCanvasElement, px: number) => {
  const t = tmp.getContext("2d")!;
  ([["#ff0000", 1 + px / 540], ["#00ff00", 1], ["#0000ff", 1 - px / 540]] as const).forEach(([col, s]) => {
    t.globalCompositeOperation = "source-over"; t.clearRect(0, 0, tmp.width, tmp.height);
    t.drawImage(layer, 0, 0);
    t.globalCompositeOperation = "multiply"; t.fillStyle = col; t.fillRect(0, 0, tmp.width, tmp.height);
    t.globalCompositeOperation = "destination-in"; t.drawImage(layer, 0, 0); // ré-applique l'alpha du calque
    dst.save(); dst.globalCompositeOperation = "lighter";
    dst.translate(540, 900); dst.scale(s, s); dst.translate(-540, -900);
    dst.drawImage(tmp, 0, 0); dst.restore();
  });
};
// Remplace le calque d'origine (ne pas le dessiner en plus). px ≤ 1,5 ; seulement pendant les rushs/flashs.
```

---

## 15. Grain (dither) à 30 Hz, stable

```ts
const grainFrame = Math.floor(frame / 2);       // rafraîchi toutes les 2 frames à 60 fps → plus « film »
const ox = Math.floor(hash1(grainFrame, 11) * 256), oy = Math.floor(hash1(grainFrame, 29) * 256);
// motif de bruit pré-calculé (tuiles 256², moyenne de 3 uniformes ≈ gaussien), overlay 3–6 % + screen ~1 %
```

---

## 16. Contrôle qualité intégré

- Script de stills : rendre 1 frame toutes les 90 frames + toutes les frames clés de `config.ts` à `--scale=0.5`.
- Après chaque rendu MP4 : `python ~/.claude/skills/critique-rendu-motion/scripts/analyse_rendu.py <mp4> --project <dossier> --label vN --safe --strips <transitions>`.
