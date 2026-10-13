#!/usr/bin/env python3
"""color_pass.py — color-separation pass on the Letter-39 blot ROI.

1. R/G/B channel views (grayscale) — shade bands ignore chroma; a different
   ink under blue dye ink can separate in R vs B channels.
2. Decorrelation stretch (PCA whitening) on the ROI — pushes nearly identical
   colors apart, the archaeology trick for faded paint.
3. B-minus-R difference map: blue dye ink absorbs red; foreign inks/pencil
   show up as B/R asymmetry.

ROI is the shade_isolate.py Letter-39 blot ROI: x[88:474], y[389:726].
"""
import os
import numpy as np
from PIL import Image

SRC = os.path.join(os.path.dirname(__file__), "..", "img", "source", "39-blot.png")
OUT = os.path.join(os.path.dirname(__file__), "..", "img", "passes", "color39")
ROI = (88, 389, 474, 726)  # x0, y0, x1, y1

def main():
    os.makedirs(OUT, exist_ok=True)
    img = np.array(Image.open(SRC).convert("RGB"))
    x0, y0, x1, y1 = 88, 389, 474, 726
    roi = img[y0:y1, x0:x1].astype(np.float32)
    print("roi", roi.shape)

    # 1. per-channel views, normalized for visibility
    for name, ch in (("R", roi[:, :, 0]), ("G", roi[:, :, 1]), ("B", roi[:, :, 2])):
        lo, hi = np.percentile(ch, 1), np.percentile(ch, 99)
        norm = np.clip((ch - lo) / max(hi - lo, 1e-6), 0, 1)
        Image.fromarray((norm * 255).astype(np.uint8)).save(
            os.path.join(OUT, f"chan_{name}.png"))

    # 3. B-minus-R asymmetry (also saved as diverging map)
    d = roi[:, :, 2] - roi[:, :, 0]
    dl, dh = np.percentile(d, 1), np.percentile(d, 99)
    Image.fromarray((np.clip((d - dl) / max(dh - dl, 1e-6), 0, 1) * 255).astype(
        np.uint8)).save(os.path.join(OUT, "b_minus_r.png"))

    # 2. decorrelation stretch on the ROI
    X = roi.reshape(-1, 3)
    mu = X.mean(axis=0)
    C = np.cov((X - mu).T)
    vals, vecs = np.linalg.eigh(C)
    vals = np.maximum(vals, 1e-9)
    Y = (X - mu) @ vecs @ np.diag(1.0 / np.sqrt(vals))
    target = 55.0  # contrast matched across bands
    Z = Y * target + mu
    stretch = np.clip(Z, 0, 255).reshape(roi.shape).astype(np.uint8)
    Image.fromarray(stretch).save(os.path.join(OUT, "decorrelation.png"))

    # Also stretch the 3-PC false color (PC1,PC2,PC3 -> RGB) to exaggerate
    pc = (Y.reshape(roi.shape) * 60 + 128)
    pc = np.clip(pc, 0, 255).astype(np.uint8)
    Image.fromarray(pc).save(os.path.join(OUT, "pc_falsecolor.png"))

    print("done ->", OUT)

if __name__ == "__main__":
    main()
