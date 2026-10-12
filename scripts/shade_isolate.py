#!/usr/bin/env python3
"""
shade_isolate.py — multi-pass shade-band isolation for ink blots.

Goal: reveal writing (numbers, Yiddish, etc.) hidden under an ink blot by
slicing the blot's finite shade range into bands and isolating each band
separately, in multiple passes and multiple directions.

Pipeline
--------
1. Load image; detect the blot ROI automatically (saturated blue ink mask,
   largest connected component + margin for shade calibration). The margin
   supplies paper/ink reference shades; annotation boxes are NOT expected
   in the source image and are excluded by the margin rule.
2. Within the blot mask, find the darkest and lightest shades (2nd / 98th
   percentile of LAB L) — the finite shade range of this blot.
3. Pass family A (global shade bands): split the range into N bands;
   save each band mask plus a color-coded composite stitch.
4. Pass family B (row-wise): per row, z-score blot pixels against the
   row's own median/std; |z| > k marks strokes that differ from the local
   wash. Same for columns (family C) and both diagonals (family D, via
   45-degree rotation).
5. Pass family E (multi-scale): repeat B at 2x upscale for wider strokes.
6. "Movie" output: animated GIF sweeping bands dark -> light, plus a
   depthmap (band index as height).

Outputs go to <outdir>/; every file name records pass + parameters.

Usage:
    python3 shade_isolate.py img/blot39.jpg --out img/passes/blot39
"""

import argparse
import os
import sys

import cv2
import numpy as np


def detect_blot_roi(img, margin=40, sat_thresh=60):
    """Bounding box of the largest saturated-blue blob, expanded by margin."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # blue/teal ink: hue ~85-130 in OpenCV's 0-179 range
    mask = cv2.inRange(hsv, np.array([85, sat_thresh, 30]),
                       np.array([130, 255, 255]))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                            np.ones((9, 9), np.uint8))
    n, _, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n < 2:
        raise RuntimeError("no blot found: saturation gate found nothing")
    biggest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    x, y, w, h = (stats[biggest, cv2.CC_STAT_LEFT],
                  stats[biggest, cv2.CC_STAT_TOP],
                  stats[biggest, cv2.CC_STAT_WIDTH],
                  stats[biggest, cv2.CC_STAT_HEIGHT])
    H, W = img.shape[:2]
    x0, y0 = max(0, x - margin), max(0, y - margin)
    x1, y1 = min(W, x + w + margin), min(H, y + h + margin)
    return (x0, y0, x1, y1), mask[y0:y1, x0:x1] > 0


def shade_range(L, blot_mask, lo_pct=2, hi_pct=98):
    """Darkest/lightest shades inside the blot (percentiles of L)."""
    vals = L[blot_mask]
    return float(np.percentile(vals, lo_pct)), float(np.percentile(vals, hi_pct))


def pass_global_bands(L, blot_mask, dark, light, n_bands, outdir, tag):
    """Family A: stepwise shade-band masks over the blot's finite range."""
    edges = np.linspace(dark, light, n_bands + 1)
    band_idx = np.zeros_like(L, dtype=np.uint8)
    for i in range(n_bands):
        m = blot_mask & (L >= edges[i]) & (L < edges[i + 1])
        band_idx[m] = i + 1
        cv2.imwrite(os.path.join(outdir, f"{tag}_band_{i:02d}.png"),
                    (m.astype(np.uint8)) * 255)
    # composite stitch: color-coded bands
    cmap = cv2.applyColorMap((band_idx * (255 // max(n_bands, 1))).astype(np.uint8),
                             cv2.COLORMAP_TURBO)
    cmap[~blot_mask] = (240, 240, 240)
    cv2.imwrite(os.path.join(outdir, f"{tag}_composite.png"), cmap)
    # depthmap: band index as height (grayscale)
    depth = (band_idx.astype(np.float32) / n_bands * 255).astype(np.uint8)
    depth[~blot_mask] = 0
    cv2.imwrite(os.path.join(outdir, f"{tag}_depthmap.png"), depth)
    # movie: dark -> light sweep
    frames = []
    for i in range(n_bands):
        m = (band_idx == i + 1)
        frame = np.full_like(L, 255)
        frame[m] = 0
        frames.append(frame)
    gif_path = os.path.join(outdir, f"{tag}_sweep.gif")
    try:
        from PIL import Image
        ims = [Image.fromarray(f) for f in frames]
        ims[0].save(gif_path, save_all=True, append_images=ims[1:],
                     duration=350, loop=0)
    except ImportError:
        print("PIL missing: skipping GIF", file=sys.stderr)
    return band_idx


def pass_directional(L, blot_mask, k, outdir, tag, direction):
    """Families B/C/D: per-line z-score deviation from the local wash.

    direction: 'rows', 'cols', 'diag1', 'diag2'.
    """
    work = L.astype(np.float32).copy()
    ang = {'rows': 0, 'cols': 90, 'diag1': 45, 'diag2': -45}[direction]
    H, W = work.shape
    if ang != 0:
        M = cv2.getRotationMatrix2D((W / 2, H / 2), ang, 1.0)
        work = cv2.warpAffine(work, M, (W, H), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_REPLICATE)
        bmask = cv2.warpAffine(blot_mask.astype(np.uint8), M, (W, H),
                               flags=cv2.INTER_NEAREST).astype(bool)
    else:
        bmask = blot_mask
    dev = np.zeros_like(work, dtype=np.uint8)
    for r in range(H):
        row_m = bmask[r]
        if row_m.sum() < 8:
            continue
        vals = work[r][row_m]
        med, sd = float(np.median(vals)), float(vals.std()) + 1e-6
        z = np.abs((work[r] - med) / sd)
        dev[r][row_m & (z > k)] = 255
    if ang != 0:
        Mi = cv2.getRotationMatrix2D((W / 2, H / 2), -ang, 1.0)
        dev = cv2.warpAffine(dev, Mi, (W, H), flags=cv2.INTER_NEAREST)
    cv2.imwrite(os.path.join(outdir, f"{tag}_{direction}_k{k}.png"), dev)
    return dev


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("image", help="source image (no annotation boxes)")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--margin", type=int, default=40,
                    help="calibration margin around blot (px)")
    ap.add_argument("--bands", type=int, nargs="+", default=[6, 12],
                    help="band counts for family A passes")
    ap.add_argument("--k", type=float, nargs="+", default=[1.5, 2.5],
                    help="z thresholds for directional passes")
    ap.add_argument("--upscale", type=int, default=2,
                    help="upscale factor for family E")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    img = cv2.imread(args.image)
    if img is None:
        raise RuntimeError(f"cannot read {args.image}")
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L = lab[:, :, 0]

    (x0, y0, x1, y1), blot = detect_blot_roi(img, margin=args.margin)
    print(f"ROI x[{x0}:{x1}] y[{y0}:{y1}]  blot px: {blot.sum()}")
    crop = img[y0:y1, x0:x1]
    cv2.imwrite(os.path.join(args.out, "roi.png"), crop)

    Lc = L[y0:y1, x0:x1]
    dark, light = shade_range(Lc, blot)
    print(f"shade range in blot: darkest L={dark:.1f} lightest L={light:.1f}")

    # Family A: global shade bands, several band counts = several passes
    for n in args.bands:
        pass_global_bands(Lc, blot, dark, light, n, args.out,
                           tag=f"A_bands{n}")

    # Families B/C/D: directional deviation passes
    for k in args.k:
        for d in ("rows", "cols", "diag1", "diag2"):
            pass_directional(Lc, blot, k, args.out, tag="BCD", direction=d)

    # Family E: multi-scale (2x) row-wise pass for wider strokes
    big = cv2.resize(Lc, None, fx=args.upscale, fy=args.upscale,
                     interpolation=cv2.INTER_CUBIC)
    big_blot = cv2.resize(blot.astype(np.uint8), None, fx=args.upscale,
                          fy=args.upscale,
                          interpolation=cv2.INTER_NEAREST).astype(bool)
    for k in args.k:
        d = pass_directional(big, big_blot, k, args.out, tag="E_2x",
                             direction="rows")
        small = cv2.resize(d, (Lc.shape[1], Lc.shape[0]),
                           interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(os.path.join(args.out, f"E_2x_rows_k{k}_small.png"),
                    small)

    # summary stats per band (12-band pass) for the techniques log
    edges = np.linspace(dark, light, 13)
    print("band occupancy (12-band pass):")
    for i in range(12):
        m = blot & (Lc >= edges[i]) & (Lc < edges[i + 1])
        print(f"  band {i:02d}  L[{edges[i]:5.1f},{edges[i+1]:5.1f})  "
              f"px={m.sum():6d}")
    print("done ->", args.out)


if __name__ == "__main__":
    main()
