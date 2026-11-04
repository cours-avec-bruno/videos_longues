# Specs techniques

Specs **provisoires** : elles peuvent changer une fois la DA définie. Côté code, la source de vérité est `shared/remotion/specs.ts`.

| Élément | Valeur | Pourquoi |
|---|---|---|
| Résolution de travail | 1920 × 1080 (16:9) | Rendus rapides et poids raisonnable. Passer en 4K (3840 × 2160) se fait en changeant une seule ligne dans `specs.ts` si la DA le justifie. |
| Cadence | 24 i/s | C'est la cadence cinéma, adaptée au storytelling. C'est aussi la cadence par défaut de Blender et des principaux modèles vidéo génératifs, ce qui évite les conversions (saccades, images dupliquées) au montage. |
| Master vidéo | H.264, CRF 16, yuv420p, `.mp4` | Excellente qualité, accepté tel quel par YouTube. |
| Plans intermédiaires | ProRes 422 HQ ou séquence PNG si le plan doit être retravaillé (compositing, étalonnage) | Évite de cumuler les pertes de compression. |
| Audio | AAC 320 kb/s, 48 kHz, stéréo | Standard vidéo. |
| Niveau sonore | -14 LUFS intégré, true peak ≤ -1 dBTP | Cible de normalisation de YouTube : ni écrasé, ni baissé. |

## Règle pour les plans externes

Un plan venant de Blender ou d'un outil génératif est converti aux specs avant d'être intégré :

```bash
ffmpeg -i entree.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24" -c:v libx264 -crf 16 -pix_fmt yuv420p -an sortie.mp4
```

Si la source n'est pas en 16:9, mieux vaut recadrer ou outpeindre (outils Higgsfield) qu'ajouter des bandes noires : la décision se prend au cas par cas, dans la fiche scène.

## Vérifier un rendu

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate -of compact rendu.mp4
ffmpeg -i rendu.mp4 -af loudnorm=print_format=summary -f null -
```
