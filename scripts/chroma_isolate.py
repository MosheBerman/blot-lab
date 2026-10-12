#!/usr/bin/env python3
"""
chroma_isolate.py — chroma-based separation for same-hue ink dabs.

When a dab and the writing underneath share a hue (e.g. postcard scan 51:
blue dabs over blue writing), lightness alone may not separate them.
This script slices:
  - Hue angle bands (in case the dab shifted hue while drying)
  - Saturation bands (blobs are typically more saturated than thin strokes)
  - Blue-channel intensity bands (B in BGR carries most of the signal)
Each slice is saved as a mask plus a composite. Designed to complement
shade_isolate.py, not replace it.
"""

import argparse
import os

import cv2
import numpy as np


def slice_channel(ch, mask, name, n_bands, outdir, lo_pct=2, hi_pct=98):
    vals = ch[mask]
    lo, hi = float(np.percentile(vals, lo_pct)), float(np.percentile(vals, hi_pct))
    edges = np.linspace(lo, hi, n_bands + 1)
    idx = np.zeros_like(ch, dtype=np.uint8)
    for i in range(n_bands):
        m = mask & (ch >= edges[i]) & (ch < edges[i + 1])
        idx[m] = i + 1
        cv2.imwrite(os.path.join(outdir, f"{name}_band_{i:02d}.png"),
                    m.astype(np.uint8) * 255)
    comp = cv2.applyColorMap((idx * (255 // max(n_bands, 1))).astype(np.uint8),
                             cv2.COLORMAP_TURBO)
    comp[~mask] = (240, 240, 240)
    cv2.imwrite(os.path.join(outdir, f"{name}_composite.png"), comp)
    print(f"{name}: range [{lo:.1f},{hi:.1f}] over {mask.sum()} px")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--out", required=True)
    ap.add_argument("--bands", type=int, default=10)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    img = cv2.imread(args.image)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    B = img[:, :, 0].astype(np.float32)

    # ink mask: saturated blue pixels (dabs + writing, not paper)
    ink = cv2.inRange(hsv, np.array([85, 60, 30]),
                      np.array([130, 255, 255])) > 0
    print(f"ink px: {ink.sum()}")

    slice_channel(H.astype(np.float32), ink, "hue", args.bands, args.out)
    slice_channel(S.astype(np.float32), ink, "sat", args.bands, args.out)
    slice_channel(B, ink, "bluech", args.bands, args.out)
    print("done ->", args.out)


if __name__ == "__main__":
    main()
