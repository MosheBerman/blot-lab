#!/usr/bin/env python3
"""
blackblock_isolate.py — shade-band isolation for BLACK redaction blocks.

Same pass families as shade_isolate.py, but the ROI detector gates on
dark ink (low V) instead of saturated blue. For deliberate black
scribble-obliteration over handwriting (e.g. postcard scan 17).
"""

import argparse
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shade_isolate import (pass_global_bands, pass_directional,
                           shade_range)


def detect_black_roi(img, margin=30, v_thresh=110):
    """Bounding box of the largest dark-ink blob, expanded by margin."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 0, 0]),
                       np.array([179, 255, v_thresh]))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                            np.ones((11, 11), np.uint8))
    n, _, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n < 2:
        raise RuntimeError("no black block found")
    biggest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    x, y, w, h = (stats[biggest, cv2.CC_STAT_LEFT],
                  stats[biggest, cv2.CC_STAT_TOP],
                  stats[biggest, cv2.CC_STAT_WIDTH],
                  stats[biggest, cv2.CC_STAT_HEIGHT])
    H, W = img.shape[:2]
    x0, y0 = max(0, x - margin), max(0, y - margin)
    x1, y1 = min(W, x + w + margin), min(H, y + h + margin)
    return (x0, y0, x1, y1), mask[y0:y1, x0:x1] > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--out", required=True)
    ap.add_argument("--margin", type=int, default=30)
    ap.add_argument("--bands", type=int, nargs="+", default=[8, 16])
    ap.add_argument("--k", type=float, nargs="+", default=[1.5, 2.5])
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    img = cv2.imread(args.image)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L = lab[:, :, 0]

    (x0, y0, x1, y1), blk = detect_black_roi(img, margin=args.margin)
    print(f"ROI x[{x0}:{x1}] y[{y0}:{y1}]  black px: {blk.sum()}")
    cv2.imwrite(os.path.join(args.out, "roi.png"), img[y0:y1, x0:x1])

    Lc = L[y0:y1, x0:x1]
    dark, light = shade_range(Lc, blk)
    print(f"shade range in block: darkest L={dark:.1f} lightest L={light:.1f}")

    for n in args.bands:
        pass_global_bands(Lc, blk, dark, light, n, args.out,
                           tag=f"K_bands{n}")
    for k in args.k:
        for d in ("rows", "cols"):
            pass_directional(Lc, blk, k, args.out, tag="KCD",
                             direction=d)
    print("done ->", args.out)


if __name__ == "__main__":
    main()
