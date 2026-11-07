#!/usr/bin/env python3
"""Outils pour caler des bruits de pas sur une vidéo en vue subjective.

1. detecter_pas(wav)     : repère les impacts dans un enregistrement de pas (enveloppe + pics).
2. temps_des_pas(video)  : estime l'instant de chaque pas à partir du balancement vertical de la caméra
                           (corrélation de phase image par image ; un pas = le point bas du balancement).
3. Le mixage lui-même se fait dans scenes/<id>/son.py, qui appelle ces fonctions.

Dépend de numpy et de ffmpeg (dans le PATH).
"""
import subprocess

import numpy as np

SR = 48000


def lire_audio(chemin, sr=SR, mono=True):
    cmd = ["ffmpeg", "-v", "error", "-i", chemin, "-f", "f32le", "-acodec", "pcm_f32le", "-ar", str(sr)]
    cmd += ["-ac", "1"] if mono else ["-ac", "2"]
    cmd += ["-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32)
    return a if mono else a.reshape(-1, 2)


def detecter_pas(chemin, seuil_db=-28.0, ecart_min=0.35, sr=SR):
    """Renvoie les instants (s) des impacts de pas : montées rapides de l'enveloppe au-dessus du seuil."""
    a = lire_audio(chemin, sr)
    fen = int(0.01 * sr)
    env = np.sqrt(np.convolve(a ** 2, np.ones(fen) / fen, mode="same") + 1e-12)
    db = 20 * np.log10(env / (env.max() + 1e-12))
    pas, dernier = [], -1e9
    pente = np.diff(db, prepend=db[0])
    for i in range(1, len(db)):
        t = i / sr
        if db[i] > seuil_db and pente[i] > 0.02 and t - dernier > ecart_min:
            # recule au début de la montée
            j = i
            while j > 0 and db[j - 1] < db[j] and i - j < int(0.02 * sr):
                j -= 1
            pas.append(j / sr)
            dernier = t
    return pas


def temps_des_pas(video, largeur=320, hauteur=180):
    """Estime les instants des pas à partir du mouvement vertical de l'image (vue subjective)."""
    cmd = ["ffmpeg", "-v", "error", "-i", video, "-vf", f"scale={largeur}:{hauteur},format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                            "-of", "csv=p=0", video], capture_output=True, text=True, check=True).stdout.strip()
    num, den = probe.split("/")
    fps = float(num) / float(den)
    imgs = np.frombuffer(raw, dtype=np.uint8).reshape(-1, hauteur, largeur).astype(np.float32)
    # éclaircit le noir pour que la corrélation porte sur les zones lisibles
    imgs = np.sqrt(imgs / 255.0)
    fenetre = np.outer(np.hanning(hauteur), np.hanning(largeur))
    dy = [0.0]
    for k in range(1, len(imgs)):
        A = np.fft.fft2((imgs[k - 1] - imgs[k - 1].mean()) * fenetre)
        B = np.fft.fft2((imgs[k] - imgs[k].mean()) * fenetre)
        R = A * np.conj(B)
        R /= np.abs(R) + 1e-9
        c = np.fft.ifft2(R).real
        y, x = np.unravel_index(np.argmax(c), c.shape)
        if y > hauteur // 2:
            y -= hauteur
        dy.append(float(y))
    pos = np.cumsum(dy)
    # retire la dérive lente (le travelling avant) pour ne garder que le balancement
    n = max(3, int(fps * 1.2) | 1)
    tendance = np.convolve(pos, np.ones(n) / n, mode="same")
    bal = pos - tendance
    bal = np.convolve(bal, np.ones(3) / 3, mode="same")
    # un pas = un minimum local marqué du balancement (la tête descend quand le pied touche le sol)
    instants = []
    for k in range(2, len(bal) - 2):
        if bal[k] < bal[k - 1] and bal[k] <= bal[k + 1] and bal[k] < -0.15:
            if not instants or (k / fps - instants[-1]) > 0.45:
                instants.append(k / fps)
    return instants, fps, bal.tolist()


def ecrire_normalise(mix, chemin, lufs=None, tp=-1.5, sr=SR, gain_db=None):
    """Écrit un mixage stéréo (float, N x 2) en WAV 24 bits, normalisé à `lufs` par un gain FIXE.

    (Le filtre loudnorm de ffmpeg, en une passe, agit comme un gain automatique : il remonte les passages calmes et
    écrase les nuances. Ici on mesure, on applique un seul gain, puis un limiteur ne touche que les crêtes.)
    """
    import json
    import re
    brut = mix.astype(np.float32).tobytes()
    mesure = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-",
                             "-af", "ebur128=peak=true", "-f", "null", "-"], input=brut, capture_output=True).stderr.decode("utf-8", "ignore")
    i_mesure = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", mesure)[-1])
    gain = gain_db if gain_db is not None else lufs - i_mesure   # gain imposé : même échelle d'une scène à l'autre
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-",
                    "-af", f"volume={gain:.2f}dB,alimiter=limit={10 ** (tp / 20):.4f}:attack=2:release=60:level=disabled",
                    "-ar", str(sr), "-c:a", "pcm_s24le", chemin], input=brut, check=True)
    return i_mesure, gain


def boucle(a, n, fondu_s=0.5, sr=SR):
    """Allonge un son d'ambiance (N x 2) à n échantillons en le bouclant avec un fondu enchaîné."""
    if len(a) >= n:
        return a[:n]
    f = int(fondu_s * sr)
    out = a.copy()
    while len(out) < n:
        g = np.linspace(0, 1, f)[:, None]
        jonction = out[-f:] * (1 - g) + a[:f] * g
        out = np.concatenate([out[:-f], jonction, a[f:]])
    return out[:n]
