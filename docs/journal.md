# Journal des décisions

Trace courte des décisions qui concernent tout le projet. Les décisions propres à une vidéo vont dans son dossier.

## 2026-11-04 · Mise en place du studio

- **Ligne éditoriale** : chaîne généraliste de réflexion, au format storytelling.
- **Direction artistique** : à construire plus tard, à partir des références que Bruno fournira. Rien n'est figé d'ici là.
- **Skills et outillage avancé** : plus tard, une fois la DA posée.
- **Specs provisoires** : 1080p, 24 i/s, H.264 CRF 16, -14 LUFS (détails dans `specs-techniques.md`).
- **Remotion** : un seul projet à la racine (point d'entrée `remotion/`). Les compositions vivent dans le dossier de chaque vidéo et les composants communs dans `shared/remotion/`.
- **Médias lourds** : exclus de Git.

## 2026-11-04 · Répartition cloud / PC fixe

- **Cloud** : écriture et code (recherches, storyboard, script, fiches scène, prompts, code Remotion, scripts Blender), plus les tests de rendu rapides.
- **PC fixe (Windows)** : production lourde (rendus finaux, Blender, montage) et stockage des médias. Claude Code y tourne aussi, sur le même repo.
- **Le repo GitHub fait le lien** : `git pull` en début de session, commit et push après chaque étape. Fins de ligne normalisées en LF par `.gitattributes`. Node 22 fixé par `.nvmrc`.
- Guide d'installation : `installation-pc.md`.

## Questions ouvertes

- [ ] Sauvegarde des médias lourds du PC (rushes, générations, rendus) : disque externe, Google Drive, NAS ?
- [ ] Voix off : la voix de Bruno ou une voix générée (ElevenLabs) ?
- [ ] Specs définitives (4K ?) une fois la DA définie.
