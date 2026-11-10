# Fabriquer des vidéos courtes par le code — la stack

Guide générique pour monter une chaîne de vidéos verticales (TikTok, Reels, Shorts) entièrement fabriquées par le code :
animations, voix de synthèse, sous-titres, bruitages et rendu. Aucun logiciel de montage.

---

## 1. Vue d'ensemble

```
texte du script ──► voix de synthèse ──► transcription mot à mot ──► repères de mots (image où tombe chaque mot)
                                                                         │
données (cartes, chiffres, images) ──► précalcul ──────────────────────► │
                                                                         ▼
                                              composants React (Remotion) : chaque image = une page web
                                                                         │
                                         rendu (Chrome sans écran) ──► MP4 ──► export
```

L'idée centrale : **le visuel suit la voix**. On génère d'abord la voix, on mesure quand chaque mot est prononcé, puis
chaque animation se cale sur un mot (« le tampon tombe sur le mot 1789 »).

---

## 2. Les briques

| Rôle | Outil | Pourquoi |
|---|---|---|
| Moteur vidéo | **Remotion** (React + TypeScript) | une vidéo = des composants React ; chaque image est calculée à partir de son numéro |
| Langage | **TypeScript / TSX** pour les scènes, **JavaScript Node.js (`.mjs`)** pour les scripts | typage des scènes, scripts simples à lancer |
| Dessin | **SVG + HTML/CSS** | formes vectorielles nettes, transformations CSS pour la fausse 3D (perspective, rotateX) |
| Voix | une **API de synthèse vocale** (text-to-speech) | voix naturelle ; la clé API dans une variable d'environnement |
| Repères de mots | **transcription avec horodatage** (par exemple Whisper) | donne l'instant exact de chaque mot → calage des animations et des sous-titres |
| Encodage | **ffmpeg** (fourni avec Remotion) | recoller les segments, poser l'audio, compresser, extraire des images de contrôle |
| Données | sources ouvertes (OpenStreetMap, Natural Earth, relief IGN…) | cartes et chiffres réels, précalculés une fois |
| Musique / bruitages | banques libres de droits (Mixkit, Freesound CC0…) | licence vérifiée et notée |
| Versionnement | git | un commit par version de vidéo |

Installation de base :

```bash
npm init -y
npm i remotion @remotion/cli @remotion/bundler @remotion/renderer react react-dom
npm i -D typescript @types/react
```

---

## 3. Le principe de Remotion en 30 secondes

```tsx
import { useCurrentFrame, interpolate, Composition, registerRoot } from "remotion";

const MaScene: React.FC = () => {
  const f = useCurrentFrame();                                      // numéro de l'image en cours
  const x = interpolate(f, [0, 30], [-200, 540], { extrapolateRight: "clamp" });
  return <div style={{ position: "absolute", left: x, top: 900, fontSize: 120 }}>BONJOUR</div>;
};

registerRoot(() => (
  <Composition id="MaVideo" component={MaScene} durationInFrames={300} fps={30} width={1080} height={1920} />
));
```

- Tout est **fonction du numéro d'image** : pas d'état, pas de minuterie. Une image peut être rendue seule, dans n'importe
  quel ordre (c'est ce qui permet le rendu en parallèle et les images de contrôle).
- `interpolate`, `spring` et `Easing` donnent les mouvements ; `<Audio>` pose la voix, la musique et les bruitages.
- Format vertical : **1080 × 1920**, 30 ou 60 images/s.

Commandes utiles :

```bash
npx remotion studio                                   # aperçu interactif dans le navigateur
npx remotion still MaVideo out.png --frame=120        # une image de contrôle
npx remotion render MaVideo out.mp4                   # le rendu complet
```

---

## 4. Organisation des dossiers

```
projet/
├── CLAUDE.md / README.md        règles de la chaîne (ton, format, durée, licences)
├── docs/                        charte, format, pipeline, sources et licences
│   └── episodes/<slug>/         script.md · sources.md
├── remotion/
│   ├── src/
│   │   ├── Root.tsx             la liste des compositions (une par épisode)
│   │   ├── commun/              briques partagées : thème, sous-titres, voix, sons, transitions
│   │   └── episodes/<slug>/     les scènes d'un épisode + timing.ts + mots.ts (généré)
│   ├── scripts/                 voix · render · stills · exporter · nouveau (Node.js)
│   └── modele-episode/          squelette copié pour chaque nouvel épisode
└── (disque de données)          médias, rendus, exports, temporaires — séparés du code
```

Garder le **code** (léger, versionné) séparé des **médias** (lourds, hors git).

---

## 5. Le pipeline, étape par étape

1. **Nouvel épisode** — un script copie le squelette, crée les docs et ajoute la composition à `Root.tsx`.
2. **Script** — le texte découpé en *unités* (une respiration = une prise de voix). Nombres écrits en lettres pour la
   voix, réaffichés en chiffres dans les sous-titres ; graphies phonétiques si un nom est mal prononcé.
3. **Voix** — un script envoie chaque unité à l'API de synthèse, met en cache (on ne paie que les unités modifiées),
   normalise le volume, puis **transcrit** l'audio pour obtenir l'horodatage de chaque mot → génère `mots.ts` :
   ```ts
   export const w = (unite: number, mot: string, n = 0): number => /* image où commence ce mot */;
   ```
   Un mot introuvable doit faire **planter** le rendu (une faute de frappe se voit tout de suite).
4. **Données** — un script `prep-*.mjs` télécharge une fois les données brutes, puis les précalcule (projection fixe,
   simplification des tracés) dans un fichier `.ts`. Aucun calcul lourd par image.
5. **Scènes** — chaque scène lit `w(unité, "mot")` pour déclencher ses animations. Le `timing.ts` déduit tout de la voix.
6. **Sons** — une liste de repères `{ image, fichier, volume }` posée sur les mêmes mots ; la musique en fond.
7. **Images de contrôle** — on rend quelques images fixes (début de chaque scène, transitions) et on les **regarde**
   avant le rendu complet : chevauchements, zones sûres de l'appli, lisibilité.
8. **Rendu** — l'audio en une seule passe (wav), la vidéo **par segments** de ~1000 images (Chrome plante sur les longs
   rendus), recollés par ffmpeg, puis contrôles automatiques : nombre d'images, durée vidéo = durée audio, sonie.
9. **Export** — copie de la version finale + un aperçu léger (540 × 960) pour validation.

---

## 6. Les recettes qui marchent

- **Caméra unique** : une seule trajectoire de caméra pour toute la vidéo (clés `[image, position, durée]`, interpolation
  du zoom en logarithme) → la vidéo ne « coupe » jamais, elle vole d'un sujet à l'autre.
- **Calage au mot** : tout élément qui illustre une phrase apparaît sur le mot qui le nomme.
- **Sous-titres mot à mot** : le mot prononcé surligné, générés depuis la transcription.
- **Boucle parfaite** : la vidéo commence en pleine phrase et la dernière phrase se termine par la première ; la dernière
  image = la première → envie de revoir.
- **Fluidité** : rendu à 60 images/s ; flou de mouvement seulement sur les mouvements rapides (il coûte cher).
- **Un squelette d'épisode** prêt à copier : un nouvel épisode compile et se rend dès sa création.

---

## 7. Pièges connus

- **Chrome plante sur les longs rendus** → rendre par segments, avec reprise des segments déjà complets.
- **Pointillés et traits complexes** très coûteux au rendu → simplifier, découper en tuiles.
- **Plusieurs épisodes dans le même `Root.tsx`** : si un épisode en cours ne compile pas, tous les rendus échouent → un
  point d'entrée séparé par épisode en dépannage.
- **Disque plein** : rendus et temporaires sur un autre disque que le code.
- **Quota de la voix** : écrire le vrai texte avant de générer ; tester une graphie douteuse sur un fragment court.
- **Licences** : vérifier et noter chaque source (musique, images, données) avant usage ; mention à l'écran si exigée
  (ex. « © les contributeurs d'OpenStreetMap »).
- **Secrets** : clés d'API dans des variables d'environnement, jamais dans le code ni dans git.

---

## 8. Pour démarrer une nouvelle chaîne

1. Créer le projet Remotion (section 2) et l'arborescence (section 4).
2. Écrire la **charte** : couleurs, polices, format, durée cible, ton, règles de sources.
3. Écrire les briques communes : thème, sous-titres, lecteur de voix, piste de sons.
4. Écrire les scripts : `voix`, `stills`, `render`, `exporter`, `nouveau` (en reprenant la logique de la section 5).
5. Faire un **épisode pilote** court de bout en bout, puis en tirer le squelette d'épisode.
