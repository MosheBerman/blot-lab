#!/usr/bin/env python3
"""ridge_isolate.py — test Moshe's local-maxima hypothesis on the Letter-39 blot.

Hypothesis: the blot is not uniform; ink pools unevenly, so underlying letter
strokes should survive as LOCAL maxima/minima (ridges) inside the blot, even
though global shade bands see only mottled wash.

Methods (all 2D-local, orientation-free):
  1. Frangi vesselness (Hessian ridge detector) at stroke scales — finds
     elongated dark ridges, the shape of pen strokes.
  2. Black top-hat (disk larger than a stroke) — dark structures on uneven bg.
  3. Local z-score vs a wide median — per-pixel deviation from its neighborhood.

Control: the same pipeline runs on adjacent VISIBLE handwriting ("die sollst"
region). If the method cannot find ridges there, it is broken; if it finds
them there but only isotropic blobs inside the blot, the blot interior carries
no stroke-shaped signal.
"""
import os
import numpy as np
import cv2
from PIL import Image
from skimage.filters import frangi, median
from skimage.morphology import disk, black_tophat, white_tophat

SRC = os.path.join(os.path.dirname(__file__), "..", "img", "source", "39-blot.png")
OUT = os.path.join(os.path.dirname(__file__), "..", "img", "passes", "ridge39")
BLOT_ROI = (88, 389, 474, 726)      # shade_isolate.py blot ROI
CTRL_ROI = (474, 400, 765, 560)     # visible "die sollst" handwriting


def analyze(gray, name):
    g = gray.astype(np.float32) / 255.0
    inv = 1.0 - g  # strokes are dark -> bright ridges for frangi
    fr = frangi(inv, sigmas=range(2, 7), black_ridges=False)
    fr_n = (fr / max(fr.max(), 1e-9) * 255).astype(np.uint8)
    Image.fromarray(fr_n).save(os.path.join(OUT, f"{name}_frangi.png"))

    bg = median(gray, disk(15))
    bth = black_tophat(gray, disk(15))
    Image.fromarray(bth).save(os.path.join(OUT, f"{name}_blacktophat.png"))
    wth = white_tophat(gray, disk(15))
    Image.fromarray(wth).save(os.path.join(OUT, f"{name}_whitetophat.png"))

    loc_med = cv2.medianBlur(gray, 31)
    loc_std = cv2.blur((gray.astype(np.float32) - loc_med) ** 2, (31, 31)) ** 0.5
    z = (loc_med.astype(np.float32) - gray.astype(np.float32)) / np.maximum(loc_std, 3.0)
    z_n = np.clip((z / 6.0 + 0.5), 0, 1)
    Image.fromarray((z_n * 255).astype(np.uint8)).save(
        os.path.join(OUT, f"{name}_localz.png"))
    print(name, "frangi max %.3f  bth max %d  z range [%.1f, %.1f]" %
          (fr.max(), bth.max(), z.min(), z.max()))


def main():
    os.makedirs(OUT, exist_ok=True)
    img = np.array(Image.open(SRC).convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    for name, (x0, y0, x1, y1) in (("blot", BLOT_ROI), ("control", CTRL_ROI)):
        roi = gray[y0:y1, x0:x1]
        Image.fromarray(roi).save(os.path.join(OUT, f"{name}_gray.png"))
        analyze(roi, name)
    print("done ->", OUT)


if __name__ == "__main__":
    main()
