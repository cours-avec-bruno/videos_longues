---
name: motion-design-premium
description: Direction artistique et craft de motion design haut de gamme (niveau studio de titres / FUI / génératif) appliqués à Remotion. À utiliser dès qu'on conçoit, code, critique ou améliore une séquence animée « premium », cinématique, scientifique ou générative (particules, visage de particules, tunnel, réseau neuronal, scanner/HUD, morphing, typographie cinétique, caméra virtuelle 3D, glow/bloom, grain, transitions sans fondu), en particulier en vertical 9:16 pour TikTok/Reels/Shorts à 60 fps. Donne des règles chiffrées (easing, durées en frames, springs, caméra, profondeur, lumière, zones sûres, pièges d'encodage), des recettes de code Remotion/canvas et une liste d'anti-patterns. Ne concerne PAS les règles de la chaîne DRAFT MODE.
---

# Motion design premium (Remotion)

Objectif : que chaque image ait l'air dirigée image par image par un motion designer senior
(références : Imaginary Forces — *Foundation*, Elastic — *Westworld*, GMUNK — *Oblivion*,
Territory Studio, Ryoji Ikeda, Refik Anadol, onformative, Robert Hodgin). Voir
`references/sources.md` pour les liens et `references/recettes-remotion.md` pour le code.

## 0. Les 12 lois (à relire avant chaque scène)

1. **Tout mouvement est motivé** : il accompagne une transformation, révèle, ou relie deux idées. Sinon, on l'enlève.
2. **Contraste de tempo** : le spectaculaire vient du *contraste* presque-immobile ↔ extrêmement rapide, pas de la vitesse constante. Un « silence » visuel de 0,3–0,8 s avant chaque impact.
3. **Rien de linéaire** sauf les dérives constantes (et encore : modulées par du bruit). Entrées = décélération, sorties = accélération, caméra = ease-in-out à longues traînes.
4. **Continuité entre scènes** : une transition transporte au moins une chose (forme, position à l'écran, direction du mouvement, couleur, échelle). Jamais de fondu enchaîné ni de fondu au noir.
5. **Profondeur toujours** : ≥ 3 plans visibles, parallaxe proportionnelle à 1/z, perspective atmosphérique (loin = plus sombre, moins contrasté, plus froid, plus flou).
6. **Économie de lumière** : un seul point le plus lumineux à la fois ; l'accent (cyan) est rare (< ~5–8 % des pixels) et signifie quelque chose (détection, énergie, attention).
7. **Hiérarchie** : à chaque instant, l'œil sait où regarder (1 sujet héros, le reste en retrait de ≥ 40 % de luminance).
8. **Vivant mais pas agité** : micro-mouvements (respiration 0,1–0,3 Hz, scintillement lent, dérive) d'amplitude faible ; jamais de tremblement aléatoire.
9. **Organique ≠ aléatoire** : distributions structurées (blue noise, loi de puissance des tailles, délais spatialement cohérents) plutôt que du bruit blanc.
10. **Fonction avant décoration** (J. Hansen, FUI) : chaque trait de HUD a l'air de mesurer quelque chose.
11. **Le mobile d'abord** : lisible sur 6 pouces, dans la zone sûre, survit à la recompression TikTok.
12. **Itérer** : V1 fonctionnelle → critique chiffrée (skill `critique-rendu-motion`) → V2, V3… jusqu'au seuil.

## 1. Timing & courbes (60 fps)

Durées de référence (frames @60) :

| Action | Frames | Courbe |
|---|---|---|
| Micro-réaction (lueur de détection, tick HUD) | 6–12 | attaque 1–2 fr + décroissance exp (`expImpulse`) |
| Flash de transition | 2 fr montée, 10–22 fr décroissance | exp, pic ≤ 0,9 ; ≤ 1 flash plein cadre / 10 s |
| Entrée d'un élément | 18–36 | `bezier(0.16,1,0.3,1)` (expo-out) ou M3 emphasized `bezier(0.05,0.7,0.1,1)` |
| Sortie | 12–24 (plus court que l'entrée) | `bezier(0.7,0,0.84,0)` (expo-in) |
| Lettre (stagger) | décalage 2–4 fr, 24–40 fr chacune | expo-out + overshoot 3–6 % |
| Mouvement caméra lent | 120–600 | inOutSine / inOutCubic, traînes longues |
| Rush / zoom rapide | 20–45 | inExpo → outExpo (vitesse max au milieu) |
| Morphing de nuage de points | 60–120 | smoothstep **par particule** avec délai spatial |
| Maintien lisible d'un mot | ≥ 50 + 4/caractère | — |

Springs Remotion (`spring({frame, fps, config})`, indépendant du fps) :
- sans rebond, doux : `{damping: 200}` ;
- arrivée premium avec léger dépassement (~4 %) : `{damping: 18, stiffness: 140, mass: 0.9}` ;
- « lock-on » HUD nerveux : `{damping: 12, stiffness: 220, mass: 0.6}` ;
- vérifier la durée réelle avec `measureSpring()`. Overshoot > 10 % = cartoon, à proscrire ici.

Principes Disney utiles ici : **anticipation** (contraction 2–4 % / recul de caméra 6–12 fr avant une explosion ou un rush), **follow-through & overlap** (les satellites, traînées, lignes HUD s'arrêtent 4–10 fr après le corps principal), **secondary motion** (halo qui pulse, poussière déplacée par le passage d'un objet), **slow in / slow out**, **arcs** (trajectoires courbes, jamais en ligne droite pour les particules organiques).

**Speed ramp** (time remapping) : ralentir 0,2–0,4× *juste avant* l'impact (pas pendant), puis relâcher d'un coup. Implémentation : temps local = intégrale d'une courbe de vitesse (table pré-calculée), cf. recettes §9.

## 2. Caméra virtuelle (2,5D)

- Projection : `s = focal / (z - camZ)`, `x' = cx + (x - camX)·s`. Focale 1000–1400 pour 1080 px de large. Centre optique à ~0,45–0,47 H (UI TikTok en bas).
- Un mouvement = une intention : **push-in lent** (tension, compréhension), **crash zoom** (révélation), **pull-back** (révéler l'échelle, fin), **roll 0,5–3°** (malaise, énergie), **crane vertical** (naturel en 9:16), **traversée** (transition).
- **Dolly-zoom (Vertigo)** pour le moment « le cerveau comprend » : la caméra avance pendant que la focale diminue, le sujet garde sa taille, le fond s'étire. 40–70 fr.
- Toujours composer 2 axes (ex. push-in + roll + légère dérive latérale) avec des tempos décalés (overlap) ; jamais 3 axes qui démarrent et s'arrêtent sur la même frame.
- Respiration de caméra : bruit lisse 0,05–0,2 Hz, ±6–15 px, roll ±0,3°. Coupée pendant les moments de précision (lecture d'un mot) et remplacée par la vitesse pendant les rushs.
- Chaque vitesse caméra est **continue** (définir une courbe de vitesse intégrée, pas des positions clés qui cassent la dérivée).

## 3. Profondeur & composition

- Plans : P1 avant-plan (grosses particules bokeh, rapides, floues, alpha faible), P2 héros (net), P3 environnement/réseau (−30 % luminance), P4 fond (dégradé + brume + poussière lointaine, mouvement très lent).
- Profondeur de champ : cercle de confusion `coc = k·|d − focus| / d` → sprite pré-flouté (bokeh) + taille ↑ + alpha ↓ (conservation d'énergie : alpha ∝ r²/R²). Mise au point qui glisse (rack focus) = transition douce entre deux sujets.
- Occulteurs d'avant-plan qui traversent le cadre = « wipe naturel » (à placer sur les changements de sujet).
- 9:16 : sujet héros entre 0,30 et 0,55 H, largeur 60–85 % ; tiers verticaux ; lignes de fuite verticales. Rien d'important hors de la **zone sûre stricte** x 120→900, y 288→1248 (1080×1920) ; rien du tout d'utile hors x 60→960, y 150→1600.

## 4. Lumière & finition

- Mode additif (`globalCompositeOperation = "lighter"`) pour tout ce qui émet ; fond en `source-over`.
- **Bloom multi-échelle** (3 rayons, ex. 6/18/48 px sur des copies ¼ et ⅛ de résolution) plutôt qu'un seul halo : c'est ce qui sépare « néon cheap » de « lumière optique ». Seuil : seuls les éléments importants débordent.
- Hiérarchie : noyau quasi blanc (légèrement teinté) → couleur → halo large à 5–15 %. Le cyan est une *lumière*, pas un *remplissage*.
- Flash = impulsion (`expImpulse`), 2 fr d'attaque, jamais un plateau. Option : traînée anamorphique horizontale très fine sur les pics (sci-fi), subtile.
- Aberration chromatique : radiale (croît vers les bords), ≤ 1–2 px, **seulement** pendant les mouvements rapides / flashs. Uniforme et permanente = amateur.
- Grain : fin, animé (seedé par frame), 3–6 % ; il sert aussi de **dither** contre le banding des dégradés sombres après recompression. Vignette douce (−25 à −45 % aux coins).
- Halation (halo chaud autour des hautes lumières) : optionnelle, jamais sur une palette froide stricte.

## 5. Particules (systèmes génératifs)

- Tout est **fonction pure de la frame** (rendu parallèle, frames dans le désordre) : pas de simulation cumulée ; si une simulation est indispensable, la pré-calculer une fois (module-level) en table.
- Échantillonnage des cibles : **Poisson-disk / blue noise** (Bridson) — densité plus forte sur les traits signifiants (yeux, bouche) ; tailles en loi de puissance (beaucoup de petites, quelques grosses).
- Attribution départ → cible **cohérente** (tri par angle/rayon ou par projection) : évite le « chaos de croisements » bon marché ; le désordre doit être *voulu*.
- Morphing : délai **spatialement cohérent** (bruit basse fréquence ou distance à un point d'origine) + jitter faible → une vague organique traverse la forme. Trajectoire courbe (arc/spirale), arrivée ressort.
- Dérive : **curl noise** (champ sans divergence : pas d'amas ni de trous), 2–3 octaves, basse fréquence.
- Vitesse → traînée : *motion blur analytique* (segment entre p(f − shutter) et p(f)), shutter 0,5–1,5 frame ; au-delà d'un seuil de vitesse la particule devient une ligne (tunnel / hyperespace).
- Scintillement : sinusoïde à phase/fréquence propres, amplitude ≤ 25 %. Jamais de clignotement on/off.
- Performances canvas : sprites pré-rendus (cache), `drawImage` en additif, aucun `shadowBlur` ni `ctx.filter` par particule, culling hors cadre, un seul canvas par plan.

## 6. Typographie cinétique

- Mot-titre : 110–180 px (1080 de large), capitales, **tracking +0,08 à +0,25 em** (respire, sci-fi), graisse légère à moyenne ; animer le tracking qui se resserre lentement (0,45 → 0,18 em sur 2–3 s) = signature cinéma. **Calculer la largeur** (somme des avances ≈ 0,55–0,65 em/lettre en grotesque + tracking × (n−1)) au pic du tracking : ≤ 900 px ; un mot de 10 lettres plafonne vers 125–130 px. Au-dessus de y ≈ 840, la colonne de boutons TikTok n'est pas un problème (marges latérales 60 px).
- Entrée : masque (clip-path) + translation 20–40 % de la hauteur de lettre + scale 1,04 → 1 (overshoot) + flou 6 → 0 px, stagger 2–4 fr. Sortie : fragmentation en particules (échantillonner les pixels du texte → points) ou déplacement + aspiration.
- Micro-texte HUD (mono, 18–26 px) = décor : jamais porteur de sens indispensable. Texte porteur ≥ 44 px.
- Échantillonner un texte dans un canvas **après** chargement de la police (`delayRender` + `document.fonts.load`), sinon on échantillonne la police de repli.

## 7. Langages spécifiques

- **Scanner / HUD** : anneaux concentriques contre-rotatifs (vitesses non multiples), graduations (petite tous les 2°, grande tous les 10°), arcs pointillés, micro-labels mono, faisceau = gradient angulaire (bord d'attaque vif, traîne exp ~30–60°). Détection : quand l'angle du faisceau passe sur la cible → `expImpulse`, crochets de verrouillage qui « claquent » (spring), score qui s'incrémente. Lignes 1,5–2 px (1 px scintille à 60 fps et bave en 4:2:0).
- **Réseau neuronal** : nœuds Poisson-disk, arêtes k-plus-proches-voisins (k = 3–5) avec alpha ∝ 1/longueur ; impulsions qui **accélèrent** le long de l'arête (inQuad/inExpo), flash au nœud, période réfractaire, cascade pré-calculée (BFS avec délais ∝ longueur). « Calculer » = vagues successives, pas du bruit.
- **Paréidolie** : zone « Boucle d'or » (MIT, *Faces in Things*) : ni trop simple ni trop complexe ; deux points + une ligne suffisent ; révéler par la *lumière* (les yeux s'allument), jamais en dessinant un visage par-dessus.

## 8. Transitions autorisées (et comment)

Zoom à travers un trou (œil, fenêtre, pupille : scale ×15–40 en expo-in, zoom-blur radial, la texture du nouveau monde est déjà visible dans le trou) · explosion → particules → nouvelle forme · morphing de nuage de points · ligne lumineuse plein écran (qui *laisse* la nouvelle scène derrière elle) · occulteur d'avant-plan · rotation de caméra (roll 90–180° pendant un rush) · flash 2–4 fr qui masque une coupe · tunnel de particules. Interdits : fondu enchaîné, fondu au noir, slide, wipe PowerPoint.

## 9. Pièges d'encodage & plateformes

- Recompression TikTok/Reels : les détails < ~6 % de luminance sur fond quasi noir disparaissent ; les dégradés sombres bandent → grain/dither, fond ≠ noir pur uniforme.
- 4:2:0 : les traits fins saturés (cyan 1 px) deviennent flous/baveux → traits clairs + halo coloré.
- 60 fps : les mouvements rapides sans flou de bouger ont l'air « jeu vidéo » → motion blur analytique ; le grain peut être rafraîchi à 30 Hz pour un rendu plus « film ».
- Première frame = miniature + accroche : jamais noire ; une forme intrigante dès 0,0 s ; « question visuelle » posée avant 1,5 s (ex. deux points lumineux qui ressemblent à des yeux).
- Changement visuel significatif toutes les ~2–4 s (pattern interrupt) sans casser la continuité ; fin qui boucle bien (le noir final → la poussière initiale).
- Master : H.264 CRF ≤ 16, yuv420p, bt709 ; vérifier `ffprobe` (1080×1920, 60/1).

## 10. Remotion — règles techniques

- `useCurrentFrame()` + fonctions pures ; aléatoire seedé (mulberry32 / hash) ; `interpolate` avec `extrapolateLeft/Right: "clamp"` ; **aucune** transition/animation CSS.
- Canvas : dessiner dans `useLayoutEffect` à chaque frame, `clearRect` complet (pas d'accumulation de traînées) ; données statiques au niveau module ou `useMemo`.
- Coûts : `filter: blur()`, `box-shadow`, `backdrop-filter` sur de grands calques à chaque frame = lent ; préférer sprites pré-floutés ou un canvas réduit + `ctx.filter` une fois par frame.
- `@remotion/motion-blur` : `<CameraMotionBlur shutterAngle samples>` multiplie le coût par `samples` et dégrade les couleurs ; `useCurrentFrame()` doit être appelé *dans* les enfants. Réserver aux segments courts ; sinon motion blur analytique.
- `@remotion/effects` (≥ 4.0.464 : `glow`, `chromaticAberration`, `zoomBlur`, `vignette`, `noise`, `lightTrail`…) s'appliquent via la prop `effects` de `<HtmlInCanvas>`, `<Solid>`, `<CanvasImage>`… ; WebGL2 → rendre avec `--gl=angle` ; `<HtmlInCanvas>` rendu OK depuis 4.0.455 (aperçu Studio : Chrome 149+ avec flag) ; expérimental → tester sur un segment court avant d'adopter.
- Rendus longs : segments ≤ 1000 frames (`--frames=a-b`), `--concurrency` réglé via `npx remotion benchmark`, puis concaténation `-c copy`.

## 11. Anti-patterns (refuser)

Fondu au noir / cross-dissolve · tout apparaît en même temps · easing identique partout · linéaire · rebonds cartoon · glow partout (plus rien ne brille) · cyan en aplat · aberration chromatique permanente · particules en bruit blanc uniforme · croisements chaotiques non voulus · texte centré qui fade in/out · HUD décoratif illisible et saturé · caméra fixe > 1 s · caméra qui bouge « pour bouger » · trois axes caméra synchronisés · tremblement aléatoire · texte hors zone sûre · première frame noire · effets qui masquent l'absence d'idée.

## 11 bis. Pièges constatés en production (projet Paréidolie, V1 → V2)

- **Profondeur de champ sans plage de netteté** : le relief du héros (±300 u) partait en bokeh → visage en « bulles de savon ». Toujours une *bande* nette : `coc = k·max(0, |d−focus| − band)/d`.
- **Flash = voile gris plein cadre sur 10–20 fr** → c'est un fondu déguisé. Un flash est une impulsion *centrée* (cœur blanc, halo qui se contracte), 12–14 fr maximum.
- **Caméra qui démarre à ×26 d'un objet vectoriel** → une forme plate géante (capsule cyan) pendant 1,5 s. Borner l'échelle de départ (le détail doit rester lisible) ; un raccord se fait sur la *position et la taille* de l'élément lumineux, pas sur un agrandissement extrême.
- **Décor qui s'épuise avant la fin du mouvement** (tunnel plus court que la course de la caméra) → 0,5 s de vide. Calculer la course intégrée et dimensionner le décor au-delà ; motiver la sortie (anneau-portail que l'on franchit au flash).
- **Visage « dessiné » sur un objet** (sourire, zigzag, yeux carrés) → émoji. La paréidolie vient de traits *natifs* (trous, fentes, fissures) révélés par la lumière intérieure (dégradé blanc → cyan → sombre), jamais par un aplat cyan.
- **Fin qui retombe** : la dernière seconde doit être le maximum d'énergie (poussée qui accélère, impulsions qui s'accélèrent) — le CUT coupe un élan, pas un plan fixe.

## 12. Check-list avant rendu

- [ ] Chaque scène : 1 intention, 1 héros, ≥ 3 plans, caméra motivée, transition d'entrée ET de sortie qui transportent une continuité.
- [ ] Courbe de rythme (mouvement dans le temps) conforme au plan (lent / rapide / hypnotique / montée / cut).
- [ ] Palette : accent ≤ ~8 % des pixels, aucun blanc pur saturé sur de grandes surfaces.
- [ ] Textes ≥ 44 px dans la zone sûre stricte, maintenus assez longtemps.
- [ ] `tsc` sans erreur, aucun `Math.random`/`Date`, stills de contrôle aux frames clés.
- [ ] Après rendu : lancer le skill `critique-rendu-motion`.
