#!/usr/bin/env python3
"""
emboss_sweep.py — stylus-press lifting with full permutation sweep.

Reimplements the Oct-7 paper-texture embossing attempt (Experiment 2) and
runs it across a parameter grid instead of a single setting:

Pipeline (per TECHNIQUES.md):
  1. Mask ink via local background subtraction; dilate the mask.
  2. Paper pixels only — ink regions filled with the local flattened
     background value (no structure invented).
  3. Flatten slow illumination variation in the log domain.
  4. High-pass at cutoff px.
  5. Directional Sobel at angle.

Permutations: high-pass cutoffs (4, 8, 16 px) x Sobel angles
(0, 45, 90, 135 deg) x resolutions (full, 1/2, 1/4) = 48 outputs.

Usage:
    python3 emboss_sweep.py img/blot39.jpg --out img/passes/emboss
"""

import argparse
import os

import cv2
import numpy as np

ROI = (88, 389, 474, 726)  # same blot region as shade_isolate.py


def ink_mask(gray):
    """Ink via local background subtraction (paper estimate - pixel)."""
    bg = cv2.GaussianBlur(gray, (0, 0), 25)
    diff = cv2.subtract(bg, gray)
    _, m = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    return m > 0


def directional_sobel(img, angle_deg):
    """Sobel response along angle_deg (0 = horizontal gradients)."""
    if angle_deg % 90 == 0 and angle_deg % 180 != 0:
        return cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    if angle_deg % 180 == 0:
        return cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    # rotate, Sobel_x, rotate back
    h, w = img.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -angle_deg, 1.0)
    rot = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_REPLICATE)
    sx = cv2.Sobel(rot, cv2.CV_64F, 1, 0, ksize=3)
    Mi = cv2.getRotationMatrix2D((w / 2, h / 2), angle_deg, 1.0)
    return cv2.warpAffine(sx, Mi, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REPLICATE)


def emboss_pass(roi_gray, hp_cutoff, sobel_angle):
    f = roi_gray.astype(np.float64)
    # 1-2. ink mask; fill ink pixels with local paper value later
    mask = ink_mask(roi_gray)
    # 3. flatten illumination in log domain
    logf = np.log1p(np.maximum(f, 0))
    bg = cv2.GaussianBlur(logf, (0, 0), 40)
    flat = logf - bg
    # hard paper-only: zero out ink regions in flattened domain
    flat[mask] = 0.0
    # 4. high-pass
    low = cv2.GaussianBlur(flat, (0, 0), hp_cutoff / 2.0)
    hp = flat - low
    hp[mask] = 0.0
    # 5. directional Sobel
    resp = directional_sobel(hp.astype(np.float32), sobel_angle)
    out = np.abs(resp)
    out[mask] = 0.0
    # normalize to 8-bit for viewing
    p99 = np.percentile(out, 99.5) + 1e-9
    return np.clip(out / p99 * 255, 0, 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cutoffs", type=int, nargs="+", default=[4, 8, 16])
    ap.add_argument("--angles", type=int, nargs="+", default=[0, 45, 90, 135])
    ap.add_argument("--scales", type=float, nargs="+", default=[1.0, 0.5, 0.25])
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    img = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    x0, y0, x1, y1 = ROI
    roi = img[y0:y1, x0:x1]
    cv2.imwrite(os.path.join(args.out, "roi.png"), roi)

    n = 0
    for s in args.scales:
        if s == 1.0:
            r = roi
        else:
            r = cv2.resize(roi, None, fx=s, fy=s,
                           interpolation=cv2.INTER_AREA)
        stag = f"s{int(1/s)}" if s != 1.0 else "s1"
        for c in args.cutoffs:
            for a in args.angles:
                out = emboss_pass(r, c, a)
                name = f"emboss_hp{c}_sob{a}_{stag}.png"
                cv2.imwrite(os.path.join(args.out, name), out)
                n += 1
    print(f"wrote {n} outputs -> {args.out}")


if __name__ == "__main__":
    main()
