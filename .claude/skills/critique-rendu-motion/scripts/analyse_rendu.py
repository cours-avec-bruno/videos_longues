#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANALYSE OBJECTIVE D'UN RENDU VIDÉO (motion design, Remotion ou autre).

Décode la vidéo via le ffmpeg embarqué de Remotion (`npx remotion ffmpeg`,
aucun ffmpeg système requis), puis mesure image par image :
  - énergie de mouvement  = moyenne |Y(t) - Y(t-1)|  (0-255, sur une image réduite)
  - luminance moyenne / p99 / part de pixels « noir pur »
  - part d'accent cyan/bleu (discipline de palette)
  - barycentre lumineux (où est l'œil attiré ? dans la zone sûre ?)
Et détecte : passages quasi statiques, segments noirs, coupes/pops, flashs.

Produit dans --out :
  metrics.csv        une ligne par frame
  rapport.md         résumé chiffré + rythme par tranche de 0,5 s (barres ASCII)
  courbes.png        mouvement + luminance dans le temps (+ version précédente si --compare)
  planche_XX.png     planches-contact (une image toutes les --every s, horodatées,
                     zones sûres TikTok/Reels superposées si --safe)
  strip_<t>.png      N frames CONSÉCUTIVES autour d'un instant (--strips), pour juger
                     la continuité d'une transition sans pouvoir « regarder » la vidéo
  still_<t>.jpg      images demi-résolution aux instants demandés (--stills)

Usage (Git Bash, depuis n'importe où) :
  python ~/.claude/skills/critique-rendu-motion/scripts/analyse_rendu.py \
      D:/pareidolie/out/pareidolie-v1.mp4 --project D:/pareidolie --label v1 \
      --every 1.5 --safe --strips 9.3,14.6 --stills 2,5.5 \
      --marks "0:Intro,6.5:Visage,9.3:Explosion,14.6:Objets" \
      --compare D:/pareidolie/out/review/v0/metrics.csv

Dépendances : Python 3.9+, numpy, Pillow. Rien n'est écrit en dehors de --out.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ utilitaires


def env_for_npx() -> dict:
    """Cache npm et fichiers temporaires sur D: (le disque C: est plein)."""
    e = dict(os.environ)
    if os.path.isdir("D:/"):
        os.makedirs("D:/npm-cache", exist_ok=True)
        os.makedirs("D:/tmp", exist_ok=True)
        e.setdefault("npm_config_cache", "D:/npm-cache")
        e["TEMP"] = "D:/tmp"
        e["TMP"] = "D:/tmp"
    return e


def run_npx(args: str, project: str, stdout=subprocess.PIPE) -> subprocess.Popen:
    cmd = f"npx remotion {args}"
    return subprocess.Popen(cmd, shell=True, cwd=project, stdout=stdout, stderr=subprocess.PIPE, env=env_for_npx())


def probe(video: str, project: str) -> dict:
    p = run_npx(
        f'ffprobe -v error -select_streams v:0 -show_entries '
        f'stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,duration,codec_name,pix_fmt '
        f'-show_entries format=duration,bit_rate -of json "{video}"',
        project,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        sys.exit(f"ffprobe a échoué : {err.decode(errors='ignore')}")
    j = json.loads(out.decode())
    s = j["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    fps = float(num) / float(den)
    dur = float(s.get("duration") or j["format"]["duration"])
    nb = int(s.get("nb_frames") or round(dur * fps))
    return {
        "width": int(s["width"]),
        "height": int(s["height"]),
        "fps": fps,
        "avg_fps": s.get("avg_frame_rate"),
        "duration": dur,
        "frames": nb,
        "codec": s.get("codec_name"),
        "pix_fmt": s.get("pix_fmt"),
        "bitrate_kbps": round(int(j["format"].get("bit_rate", 0)) / 1000),
    }


_FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def font(size: int):
    """Police avec accents (la police par défaut de PIL n'a pas é, è…)."""
    for p in _FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow ancien
        return ImageFont.load_default()


def fmt_t(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:05.2f}"


# --------------------------------------------------------------- zones sûres
# Coordonnées pour 1080x1920 (mises à l'échelle sinon).
# « stricte » = intersection TikTok / Reels / Shorts (texte, visages, éléments clés)
# « large »   = marges minimales de toutes les interfaces (rien d'important au-delà)
SAFE_STRICT = (120, 288, 900, 1248)  # x0, y0, x1, y1
SAFE_WIDE = (60, 150, 960, 1600)


def draw_safe(d: ImageDraw.ImageDraw, w: int, h: int, x0: int = 0, y0: int = 0):
    sx, sy = w / 1080, h / 1920
    for (a, b, c, e), col in ((SAFE_WIDE, (255, 170, 60)), (SAFE_STRICT, (80, 255, 140))):
        d.rectangle([x0 + a * sx, y0 + b * sy, x0 + c * sx, y0 + e * sy], outline=col, width=1)


# ------------------------------------------------------------------ analyse


def analyse(video: str, project: str, info: dict, aw: int, keep_every: float, strips: list[float],
            strip_len: int):
    W, H, fps = info["width"], info["height"], info["fps"]
    ah = int(round(aw * H / W / 2) * 2)
    fsize = aw * ah * 3
    keep_idx = set()
    if keep_every > 0:
        k = 0.0
        while k < info["duration"]:
            keep_idx.add(int(round(k * fps)))
            k += keep_every
    strip_idx = {}
    for t in strips:
        c = int(round(t * fps))
        for i in range(c - strip_len // 2, c - strip_len // 2 + strip_len):
            strip_idx.setdefault(i, []).append(t)

    p = run_npx(
        f'ffmpeg -hide_banner -loglevel error -i "{video}" -vf scale={aw}:{ah}:flags=area,format=rgb24 '
        f'-c:v rawvideo -f image2pipe -',
        project,
    )
    rows, kept, strip_frames = [], {}, {}
    prev = None
    prev_hist = None
    i = 0
    ys, xs = np.mgrid[0:ah, 0:aw]
    while True:
        buf = p.stdout.read(fsize)
        if not buf or len(buf) < fsize:
            break
        rgb = np.frombuffer(buf, np.uint8).reshape(ah, aw, 3)
        f32 = rgb.astype(np.float32)
        Y = 0.2126 * f32[..., 0] + 0.7152 * f32[..., 1] + 0.0722 * f32[..., 2]
        mean = float(Y.mean())
        p99 = float(np.percentile(Y, 99))
        black = float((Y < 3).mean())
        # accent cyan/bleu : B et G nettement au-dessus de R, pixel assez lumineux
        r_, g_, b_ = f32[..., 0], f32[..., 1], f32[..., 2]
        cyan = float((((b_ - r_) > 40) & ((g_ - r_) > 15) & (Y > 40)).mean())
        wsum = Y.sum()
        cx = float((Y * xs).sum() / wsum / aw) if wsum > 0 else 0.5
        cy = float((Y * ys).sum() / wsum / ah) if wsum > 0 else 0.5
        hist = np.histogram(Y, bins=16, range=(0, 256))[0].astype(np.float32) / Y.size
        motion = float(np.abs(Y - prev).mean()) if prev is not None else 0.0
        hdiff = float(np.abs(hist - prev_hist).sum()) if prev_hist is not None else 0.0
        rows.append({
            "frame": i, "t": i / fps, "motion": motion, "luma": mean, "p99": p99,
            "black": black, "cyan": cyan, "cx": cx, "cy": cy, "hdiff": hdiff,
        })
        if i in keep_idx:
            kept[i] = rgb.copy()
        if i in strip_idx:
            strip_frames[i] = rgb.copy()
        prev, prev_hist = Y, hist
        i += 1
    p.wait()
    if not rows:
        sys.exit("Aucune frame décodée : " + p.stderr.read().decode(errors="ignore"))
    return rows, kept, strip_frames


def runs(mask: np.ndarray, min_len: int):
    out, start = [], None
    for k, v in enumerate(list(mask) + [False]):
        if v and start is None:
            start = k
        elif not v and start is not None:
            if k - start >= min_len:
                out.append((start, k - 1))
            start = None
    return out


def detect(rows, fps, freeze_thr, freeze_min_s):
    m = np.array([r["motion"] for r in rows])
    lum = np.array([r["luma"] for r in rows])
    p99 = np.array([r["p99"] for r in rows])
    hd = np.array([r["hdiff"] for r in rows])
    med = float(np.median(m[1:])) if len(m) > 1 else 0.0
    blacks = runs((lum < 3) & (p99 < 14), 1)
    still = runs(m < freeze_thr, int(round(freeze_min_s * fps)))
    cut_thr = max(10.0, 6 * med)
    cuts = [k for k in range(1, len(m)) if m[k] > cut_thr and hd[k] > 0.25]
    flashes = []
    for k in range(3, len(lum)):
        if lum[k] - lum[k - 3] > 22:
            if not flashes or k - flashes[-1] > int(fps * 0.25):
                flashes.append(k)
    # surexposition prolongée (aplat clair géant, flash qui s'éternise) : luminance moyenne > 70 pendant ≥ 0,4 s
    overexp = runs(lum > 70, int(round(0.4 * fps)))
    # énergie de fin : dernière seconde avant le premier noir final vs médiane globale
    end_idx = blacks[-1][0] if blacks and blacks[-1][1] >= len(lum) - 2 else len(lum)
    s0 = max(1, end_idx - int(fps))
    end_energy = float(m[s0:end_idx].mean()) if end_idx > s0 else 0.0
    prev_energy = float(m[max(1, s0 - int(fps)):s0].mean()) if s0 > 1 else 0.0
    return {"median_motion": med, "blacks": blacks, "still": still, "cuts": cuts, "flashes": flashes,
            "cut_thr": cut_thr, "overexp": overexp, "end_energy": end_energy, "prev_energy": prev_energy}


# ------------------------------------------------------------------- sorties


def write_csv(rows, path: Path):
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})


def read_csv(path: str):
    with open(path, encoding="utf-8") as fh:
        return [{k: float(v) for k, v in r.items()} for r in csv.DictReader(fh)]


def parse_marks(s: str):
    out = []
    for part in [p for p in (s or "").split(",") if p.strip()]:
        t, _, name = part.partition(":")
        out.append((float(t), name.strip()))
    return out


def plot(rows, fps, det, marks, out: Path, compare=None, label="", cmp_label="précédente"):
    Wp, Hp, pad = 1600, 760, 60
    img = Image.new("RGB", (Wp, Hp), (12, 13, 16))
    d = ImageDraw.Draw(img)
    fnt, fsm = font(18), font(14)
    T = rows[-1]["t"]
    if compare:
        T = max(T, compare[-1]["t"])
    x_of = lambda t: pad + (Wp - 2 * pad) * t / max(T, 1e-6)
    top, mid, bot = 50, 400, Hp - 50  # panneau mouvement [top, mid-30], luminance [mid, bot]

    def series(vals_t, vals_v, y0, y1, vmax, col, width=2):
        pts = [(x_of(t), y1 - (y1 - y0) * min(v / vmax, 1.0)) for t, v in zip(vals_t, vals_v)]
        if len(pts) > 1:
            d.line(pts, fill=col, width=width)

    def smooth(v, n):
        if n <= 1:
            return np.array(v)
        k = np.ones(n) / n
        return np.convolve(v, k, mode="same")

    n = max(1, int(fps / 6))
    t = [r["t"] for r in rows]
    mo = smooth([r["motion"] for r in rows], n)
    lu = [r["luma"] for r in rows]
    mmax = max(float(np.percentile(mo, 99.5)) * 1.1, 1.0)
    if compare:
        ct = [r["t"] for r in compare]
        series(ct, smooth([r["motion"] for r in compare], n), top, mid - 30, mmax, (90, 90, 100), 2)
        series(ct, [r["luma"] for r in compare], mid, bot, 100, (90, 90, 100), 1)
    # zones : statique (gris), noir (rouge sombre)
    for a, b in det["still"]:
        d.rectangle([x_of(a / fps), top, x_of(b / fps), mid - 30], fill=(45, 40, 25))
    for a, b in det["blacks"]:
        d.rectangle([x_of(a / fps), mid, x_of(b / fps), bot], fill=(60, 18, 18))
    series(t, mo, top, mid - 30, mmax, (80, 220, 255), 2)
    series(t, lu, mid, bot, 100, (236, 232, 225), 2)
    for k in det["cuts"]:
        d.line([x_of(k / fps), top, x_of(k / fps), bot], fill=(255, 80, 80), width=1)
    for k in det["flashes"]:
        d.line([x_of(k / fps), mid, x_of(k / fps), bot], fill=(255, 220, 90), width=1)
    for tm, name in marks:
        x = x_of(tm)
        d.line([x, top - 10, x, bot], fill=(140, 120, 255), width=1)
        d.text((x + 3, top - 28), name, fill=(170, 155, 255), font=fsm)
    s = 0
    while s <= T:
        x = x_of(s)
        d.line([x, bot, x, bot + 6], fill=(120, 120, 120))
        d.text((x - 8, bot + 8), f"{s:g}s", fill=(150, 150, 150), font=fsm)
        s += 5
    d.text((pad, 12), f"{label}  énergie de mouvement (cyan, lissée {n} fr)"
           + ("  | gris = " + cmp_label if compare else "")
           + f"  | bandes brunes = quasi statique", fill=(200, 200, 200), font=fnt)
    d.text((pad, mid - 24), "luminance moyenne (blanc, 0-100)  | jaune = flash  | rouge = coupe/pop  | fond rouge = noir",
           fill=(200, 200, 200), font=fnt)
    img.save(out)


def contact_sheets(kept: dict, fps: float, out_dir: Path, cols: int, safe: bool, per_sheet: int, label: str):
    idx = sorted(kept)
    if not idx:
        return []
    h0, w0 = kept[idx[0]].shape[:2]
    lab_h = 22
    paths = []
    fnt = font(15)
    for s in range(0, len(idx), per_sheet):
        chunk = idx[s:s + per_sheet]
        rows_n = math.ceil(len(chunk) / cols)
        sheet = Image.new("RGB", (cols * (w0 + 6) + 6, rows_n * (h0 + lab_h + 6) + 6), (28, 28, 32))
        d = ImageDraw.Draw(sheet)
        for j, fi in enumerate(chunk):
            x = 6 + (j % cols) * (w0 + 6)
            y = 6 + (j // cols) * (h0 + lab_h + 6)
            sheet.paste(Image.fromarray(kept[fi]), (x, y + lab_h))
            d.text((x + 2, y + 3), f"{fmt_t(fi / fps)}  f{fi}", fill=(230, 230, 230), font=fnt)
            if safe:
                draw_safe(d, w0, h0, x, y + lab_h)
        p = out_dir / f"planche_{s // per_sheet + 1:02d}.png"
        sheet.save(p)
        paths.append(p)
    return paths


def strip_images(strip_frames: dict, strips: list[float], strip_len: int, fps: float, out_dir: Path):
    paths = []
    fnt = font(14)
    for t in strips:
        c = int(round(t * fps))
        ids = [i for i in range(c - strip_len // 2, c - strip_len // 2 + strip_len) if i in strip_frames]
        if not ids:
            continue
        h0, w0 = strip_frames[ids[0]].shape[:2]
        cols = min(len(ids), 8)
        rows_n = math.ceil(len(ids) / cols)
        img = Image.new("RGB", (cols * (w0 + 4) + 4, rows_n * (h0 + 22) + 4), (28, 28, 32))
        d = ImageDraw.Draw(img)
        for j, fi in enumerate(ids):
            x = 4 + (j % cols) * (w0 + 4)
            y = 4 + (j // cols) * (h0 + 22)
            img.paste(Image.fromarray(strip_frames[fi]), (x, y + 20))
            d.text((x + 2, y + 2), f"f{fi} {fi / fps:.3f}s", fill=(230, 230, 230), font=fnt)
        p = out_dir / f"strip_{t:06.2f}s.png"
        img.save(p)
        paths.append(p)
    return paths


def stills(video: str, project: str, times: list[float], scale: float, out_dir: Path, W: int, H: int):
    paths = []
    w, h = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    for t in times:
        p = out_dir / f"still_{t:06.2f}s.jpg"
        pr = run_npx(
            f'ffmpeg -hide_banner -loglevel error -y -ss {t:.3f} -i "{video}" -frames:v 1 '
            f'-vf scale={w}:{h}:flags=lanczos -q:v 2 "{p.as_posix()}"', project, stdout=subprocess.DEVNULL)
        pr.communicate()
        if p.exists():
            paths.append(p)
    return paths


def bar(v, vmax, width=40):
    n = int(round(width * min(v / vmax, 1.0))) if vmax > 0 else 0
    return "█" * n + "·" * (width - n)


def report(info, rows, det, marks, fps, out: Path, label: str, extra: list[str], expect: dict):
    m = np.array([r["motion"] for r in rows])
    lu = np.array([r["luma"] for r in rows])
    cy = np.array([r["cy"] for r in rows])
    cx = np.array([r["cx"] for r in rows])
    cyan = np.array([r["cyan"] for r in rows])
    blk = np.array([r["black"] for r in rows])
    L = []
    L.append(f"# Analyse objective — {label}\n")
    L.append("## Technique")
    ok = lambda c: "OK" if c else "**À CORRIGER**"
    L.append(f"- Fichier : `{info['path']}`")
    L.append(f"- {info['width']}×{info['height']} · {info['fps']:.3f} fps (moy. {info['avg_fps']}) · "
             f"{info['duration']:.3f} s · {info['frames']} frames · {info['codec']} {info['pix_fmt']} · "
             f"{info['bitrate_kbps']} kb/s")
    if expect:
        if "w" in expect:
            L.append(f"- Dimensions attendues {expect['w']}×{expect['h']} : "
                     f"{ok(info['width'] == expect['w'] and info['height'] == expect['h'])}")
        if "fps" in expect:
            L.append(f"- Fréquence attendue {expect['fps']} fps : {ok(abs(info['fps'] - expect['fps']) < 0.01)}")
        if "dmin" in expect:
            L.append(f"- Durée dans [{expect['dmin']} ; {expect['dmax']}] s : "
                     f"{ok(expect['dmin'] <= info['duration'] <= expect['dmax'])}")
    L.append(f"- Frames analysées : {len(rows)}\n")

    L.append("## Détections")
    L.append(f"- Mouvement médian : {det['median_motion']:.2f} (0-255/px/frame)")
    st = det["still"]
    L.append(f"- Passages quasi statiques (mouvement < seuil pendant ≥ durée min) : {len(st)}"
             + ("".join(f"\n  - {fmt_t(a / fps)} → {fmt_t(b / fps)} ({(b - a + 1) / fps:.2f} s)" for a, b in st)))
    bl = det["blacks"]
    L.append(f"- Segments noirs : {len(bl)}"
             + ("".join(f"\n  - {fmt_t(a / fps)} → {fmt_t(b / fps)} ({b - a + 1} frames)" for a, b in bl)))
    L.append(f"- Coupes / pops (saut d'image > {det['cut_thr']:.1f}) : {len(det['cuts'])}"
             + ("".join(f"\n  - f{k} ({fmt_t(k / fps)})" for k in det["cuts"])))
    L.append(f"- Flashs (luminance +22 en 3 frames) : {len(det['flashes'])}"
             + ("".join(f"\n  - f{k} ({fmt_t(k / fps)})" for k in det["flashes"])))
    ov = det["overexp"]
    L.append(f"- Surexpositions prolongées (luminance moyenne > 70 pendant ≥ 0,4 s) : {len(ov)}"
             + ("".join(f"\n  - {fmt_t(a / fps)} → {fmt_t(b / fps)} ({(b - a + 1) / fps:.2f} s)" for a, b in ov)))
    ee, pe = det["end_energy"], det["prev_energy"]
    trend = "monte" if ee > pe * 1.05 else ("retombe" if ee < pe * 0.9 else "stable")
    L.append(f"- Énergie de la dernière seconde avant le noir final : {ee:.2f} (seconde précédente {pe:.2f}) → **{trend}**")
    L.append("")
    L.append("## Composition & palette")
    live = lu > 3
    out_c = ((cy[live] < 288 / 1920) | (cy[live] > 1248 / 1920) | (cx[live] < 120 / 1080) | (cx[live] > 900 / 1080))
    L.append(f"- Barycentre lumineux hors zone sûre stricte : {100 * out_c.mean():.1f} % des frames (hors noir)")
    L.append(f"- Barycentre vertical moyen : {cy[live].mean():.3f} H (cible 0,40-0,50 : au-dessus de l'UI basse)")
    L.append(f"- Accent cyan/bleu : médiane {100 * np.median(cyan):.2f} % des pixels, p95 {100 * np.percentile(cyan, 95):.2f} %"
             " (accent = rare ; au-delà de ~8 % en continu, ce n'est plus un accent)")
    L.append(f"- Pixels noir pur (<3/255) : médiane {100 * np.median(blk):.1f} % (fond « jamais vide » : "
             "viser < 60 % hors cut final)")
    L.append(f"- Luminance moyenne : médiane {np.median(lu):.1f}, p95 {np.percentile(lu, 95):.1f}, max {lu.max():.1f}\n")

    L.append("## Rythme (tranches de 0,5 s) — mouvement | luminance")
    step = max(1, int(round(fps * 0.5)))
    vmax = max(float(np.percentile(m, 99)), 1e-3)
    mk = {int(round(t * 2)) / 2: n for t, n in marks}
    L.append("```")
    for s in range(0, len(rows), step):
        seg_m = m[s:s + step].mean()
        seg_l = lu[s:s + step].mean()
        t = s / fps
        tag = mk.get(round(t * 2) / 2, "")
        L.append(f"{t:6.1f}s {bar(seg_m, vmax, 34)} {seg_m:6.2f} | {seg_l:5.1f} {tag}")
    L.append("```")
    if extra:
        L.append("\n## Fichiers produits")
        L += [f"- `{p}`" for p in extra]
    out.write_text("\n".join(L), encoding="utf-8")


# ---------------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--project", default=".", help="dossier d'un projet Remotion (pour npx remotion ffmpeg)")
    ap.add_argument("--out", default=None, help="dossier de sortie (défaut : <project>/out/review/<label>)")
    ap.add_argument("--label", default="vX")
    ap.add_argument("--width", type=int, default=180, help="largeur d'analyse (px)")
    ap.add_argument("--every", type=float, default=1.5, help="pas des planches-contact (s) ; 0 = aucune")
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--per-sheet", type=int, default=24)
    ap.add_argument("--safe", action="store_true", help="superposer les zones sûres sur les planches")
    ap.add_argument("--strips", default="", help="instants (s) séparés par des virgules")
    ap.add_argument("--strip-len", type=int, default=16)
    ap.add_argument("--stills", default="", help="instants (s) pour des images demi-résolution")
    ap.add_argument("--still-scale", type=float, default=0.5)
    ap.add_argument("--marks", default="", help='"0:Intro,6.5:Visage,..." (repères de scènes)')
    ap.add_argument("--compare", default=None, help="metrics.csv d'une version précédente")
    ap.add_argument("--freeze-thr", type=float, default=0.12, help="seuil de mouvement « quasi statique »")
    ap.add_argument("--freeze-min", type=float, default=0.5, help="durée min (s) d'un passage statique")
    ap.add_argument("--expect", default="1080x1920@60:45-60", help="WxH@fps:dmin-dmax (contrôles techniques)")
    a = ap.parse_args()

    video = Path(a.video).resolve().as_posix()
    project = str(Path(a.project).resolve())
    out = Path(a.out) if a.out else Path(project) / "out" / "review" / a.label
    out.mkdir(parents=True, exist_ok=True)

    expect = {}
    if a.expect:
        try:
            dims, _, rest = a.expect.partition("@")
            w, h = dims.split("x")
            fps_s, _, dur_s = rest.partition(":")
            expect = {"w": int(w), "h": int(h), "fps": float(fps_s)}
            if dur_s:
                dmin, dmax = dur_s.split("-")
                expect.update(dmin=float(dmin), dmax=float(dmax))
        except ValueError:
            expect = {}

    info = probe(video, project)
    info["path"] = video
    print(f"[info] {info['width']}x{info['height']} {info['fps']:.3f} fps {info['duration']:.2f}s {info['frames']} frames")
    strips = [float(x) for x in a.strips.split(",") if x.strip()]
    rows, kept, strip_frames = analyse(video, project, info, a.width, a.every, strips, a.strip_len)
    fps = info["fps"]
    det = detect(rows, fps, a.freeze_thr, a.freeze_min)
    marks = parse_marks(a.marks)
    write_csv(rows, out / "metrics.csv")
    compare = read_csv(a.compare) if a.compare else None
    plot(rows, fps, det, marks, out / "courbes.png", compare, a.label)
    files = [out / "metrics.csv", out / "courbes.png"]
    files += contact_sheets(kept, fps, out, a.cols, a.safe, a.per_sheet, a.label)
    files += strip_images(strip_frames, strips, a.strip_len, fps, out)
    st = [float(x) for x in a.stills.split(",") if x.strip()]
    if st:
        files += stills(video, project, st, a.still_scale, out, info["width"], info["height"])
    report(info, rows, det, marks, fps, out / "rapport.md", a.label, [p.as_posix() for p in files], expect)
    print(f"[ok] rapport : {(out / 'rapport.md').as_posix()}")
    for p in files:
        print("   ", p.as_posix())


if __name__ == "__main__":
    main()
