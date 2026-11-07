"""S02-P01 : raccord avec la fin de S01.

La fin de S01 est légèrement agrandie (le balancement de marche est fait par un recadrage : x 1,0208, centré).
On applique le même agrandissement au début de « on s'assoit », puis on revient à 1,0 en 1,5 s (pendant le mouvement,
ça ne se voit pas) : plus de saut de cadre à la coupe.
"""
import subprocess
import sys

import cv2
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
W, H, FPS = 1920, 1080, 24
Z0, DUREE = 1960 / 1920, 1.5
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
ecr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
for k, f in enumerate(F):
    p = min(1.0, k / (DUREE * FPS))
    z = Z0 + (1 - Z0) * (p * p * (3 - 2 * p))
    if z > 1.0001:
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
        f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    ecr.stdin.write(np.ascontiguousarray(f).tobytes())
ecr.stdin.close(); ecr.wait()
print("écrit :", dst)
