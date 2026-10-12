#!/usr/bin/env python3
"""
sweep_windows.py — extended permutation sweeps for the letter-39 blot.

Three families, all on the blot ROI detected by shade_isolate.py:

1. Sliding windows: N shade levels across the blot's finite lightness
   range; every overlapping window [i, i+w) for several widths w,
   sliding by 1. Catches writing that sits in a narrow shade band the
   non-overlapping slices miss.
2. Multi-resolution: pixel-bin the ROI to 1/1, 1/2, 1/4, 1/8, 1/12, 1/16
   and run band slicing at each scale. Coarser scales may reveal larger
   structures the fine pass misses.
3. Checkerboard: tile the ROI on a grid; from each seed expand outward N
   px and run band isolation inside each patch. Catches local structure
   that global banding washes out.

Each window/patch gets a simple structure score (connected components in
a stroke-plausible size/elongation range) so the top candidates can be
reviewed by a human eye instead of eyeballing ~1000 masks.

Usage:
    python3 sweep_windows.py --out img/passes/blot39
"""

import argparse
import json
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shade_isolate import detect_blot_roi, shade_range  # noqa: E402


def structure_score(mask):
    """Score a binary mask for stroke-like structure.

    Counts pixels in connected components that are plausibly strokes:
    area 40..3000 px and elongated (bbox aspect >= 1.8 either way).
    Returns (score, n_components).
    """
    n, _, stats, _ = cv2.connectedComponentsWithStats(
        mask.astype(np.uint8), 8)
    score, cnt = 0, 0
    for i in range(1, n):
        area = stats[i, cv2.CC_STAT_AREA]
        if not (40 <= area <= 3000):
            continue
        w, h = stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        if w < 3 or h < 3:
            continue
        aspect = max(w / h, h / w)
        if aspect >= 1.8:
            score += area
            cnt += 1
    return score, cnt


def montage(tiles, labels, tile_w=120, cols=12):
    """Contact sheet of (mask, label) tiles, downscaled for review."""
    rows = []
    for t, lab in zip(tiles, labels):
        h, w = t.shape[:2]
        s = tile_w / w
        small = cv2.resize(t, (tile_w, max(1, int(h * s))),
                           interpolation=cv2.INTER_NEAREST)
        if small.ndim == 2:
            small = cv2.cvtColor(small, cv2.COLOR_GRAY2BGR)
        cv2.putText(small, lab, (3, 12), cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (0, 0, 255), 1, cv2.LINE_AA)
        rows.append(small)
    th = max(r.shape[0] for r in rows)
    padded = []
    for r in rows:
        pad = np.full((th - r.shape[0], r.shape[1], 3), 255, np.uint8)
        padded.append(np.vstack([r, pad]))
    grid = []
    for i in range(0, len(padded), cols):
        row = padded[i:i + cols]
        while len(row) < cols:
            row.append(np.full_like(padded[0], 255))
        grid.append(np.hstack(row))
    return np.vstack(grid)


def family_sliding(Lc, blot, dark, light, outdir):
    """Family 1: overlapping shade windows. Returns list of run records."""
    cfgs = [(25, (2, 3, 5, 8)), (255, (5, 10, 25, 50))]
    records = []
    for N, widths in cfgs:
        edges = np.linspace(dark, light, N + 1)
        sdir = os.path.join(outdir, f"sweep_N{N}")
        os.makedirs(sdir, exist_ok=True)
        for w in widths:
            tiles, labels, scores = [], [], []
            nwin = N - w + 1
            for i in range(nwin):
                m = blot & (Lc >= edges[i]) & (Lc < edges[i + w])
                sc, nc = structure_score(m)
                scores.append({"i": int(i), "w": int(w),
                               "score": int(sc), "ncomp": int(nc)})
                fn = f"win_{i:03d}_w{w}.png"
                cv2.imwrite(os.path.join(sdir, fn),
                            m.astype(np.uint8) * 255)
                tiles.append(m.astype(np.uint8) * 255)
                labels.append(f"{i}-{i + w}")
            scores.sort(key=lambda r: -r["score"])
            with open(os.path.join(
                    sdir, f"scores_w{w}.json"), "w") as f:
                json.dump(scores, f)
            mon = montage(tiles, labels)
            cv2.imwrite(os.path.join(sdir, f"montage_w{w}.png"), mon)
            top = scores[0]
            print(f"N={N} w={w}: {nwin} windows, "
                  f"top win {top['i']}-{top['i'] + w} "
                  f"score={top['score']} ncomp={top['ncomp']}")
            records.append({"N": N, "w": w, "nwin": nwin,
                            "top": top, "dir": sdir})
    return records


def family_multires(Lc, blot, dark, light, outdir, n_bands=12):
    """Family 2: band slicing at 6 downsampled resolutions."""
    mdir = os.path.join(outdir, "multires")
    os.makedirs(mdir, exist_ok=True)
    edges = np.linspace(dark, light, n_bands + 1)
    H, W = Lc.shape
    records = []
    for denom in (1, 2, 4, 8, 12, 16):
        h, w = max(1, H // denom), max(1, W // denom)
        small_L = cv2.resize(Lc, (w, h), interpolation=cv2.INTER_AREA)
        small_b = cv2.resize(blot.astype(np.uint8), (w, h),
                             interpolation=cv2.INTER_NEAREST).astype(bool)
        band_idx = np.zeros((h, w), np.uint8)
        for i in range(n_bands):
            m = (small_b & (small_L >= edges[i])
                 & (small_L < edges[i + 1]))
            band_idx[m] = i + 1
        comp = cv2.applyColorMap(
            (band_idx * (255 // n_bands)).astype(np.uint8),
            cv2.COLORMAP_TURBO)
        comp[~small_b] = (240, 240, 240)
        cv2.imwrite(os.path.join(mdir, f"res_1_{denom}.png"), comp)
        # upscale back for side-by-side comparison
        up = cv2.resize(comp, (W, H), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(os.path.join(mdir, f"res_1_{denom}_up.png"), up)
        sc, nc = structure_score(band_idx > 0)
        print(f"1/{denom}: {w}x{h}, blot px={small_b.sum()}, "
              f"score={sc} ncomp={nc}")
        records.append({"denom": denom, "size": (w, h),
                        "score": sc, "ncomp": nc})
    # comparison strip
    strips = [cv2.imread(os.path.join(mdir, f"res_1_{d}_up.png"))
              for d in (1, 2, 4, 8, 12, 16)]
    th = max(s.shape[0] for s in strips)
    normed = []
    for s, d in zip(strips, (1, 2, 4, 8, 12, 16)):
        s = cv2.resize(s, (int(s.shape[1] * th / s.shape[0]), th))
        cv2.putText(s, f"1/{d}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255), 2, cv2.LINE_AA)
        normed.append(s)
    cv2.imwrite(os.path.join(mdir, "compare_strip.png"),
                np.hstack(normed))
    return records


def family_checkerboard(Lc, blot, dark, light, outdir, n_bands=12):
    """Family 3: grid seeds, expand N px outward, band isolation per patch."""
    cdir = os.path.join(outdir, "checkerboard")
    os.makedirs(cdir, exist_ok=True)
    edges = np.linspace(dark, light, n_bands + 1)
    H, W = Lc.shape
    records = []
    for spacing, N in ((32, 16), (64, 32)):
        tiles, labels = [], []
        ny, nx = H // spacing, W // spacing
        for gy in range(ny):
            for gx in range(nx):
                cy, cx = gy * spacing + spacing // 2, \
                    gx * spacing + spacing // 2
                y0, y1 = max(0, cy - N), min(H, cy + N)
                x0, x1 = max(0, cx - N), min(W, cx + N)
                pL, pb = Lc[y0:y1, x0:x1], blot[y0:y1, x0:x1]
                if pb.sum() < 50:
                    continue
                band_idx = np.zeros_like(pL, np.uint8)
                for i in range(n_bands):
                    m = pb & (pL >= edges[i]) & (pL < edges[i + 1])
                    band_idx[m] = i + 1
                comp = cv2.applyColorMap(
                    (band_idx * (255 // n_bands)).astype(np.uint8),
                    cv2.COLORMAP_TURBO)
                comp[~pb] = (240, 240, 240)
                sc, nc = structure_score(band_idx > 0)
                tiles.append(comp)
                labels.append(f"{gx},{gy}")
        mon = montage(tiles, labels, tile_w=96, cols=10)
        cv2.imwrite(os.path.join(
            cdir, f"patches_s{spacing}_N{N}.png"), mon)
        print(f"spacing={spacing} N={N}: {len(tiles)} patches "
              f"-> montage")
        records.append({"spacing": spacing, "N": N,
                        "npatches": len(tiles)})
    return records


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--image", default="img/blot39.jpg")
    ap.add_argument("--out", default="img/passes/blot39")
    ap.add_argument("--margin", type=int, default=40)
    args = ap.parse_args()

    img = cv2.imread(args.image)
    if img is None:
        raise RuntimeError(f"cannot read {args.image}")
    L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0]
    (x0, y0, x1, y1), blot = detect_blot_roi(img, margin=args.margin)
    Lc = L[y0:y1, x0:x1]
    dark, light = shade_range(Lc, blot)
    print(f"ROI {Lc.shape[1]}x{Lc.shape[0]}, "
          f"shade L {dark:.1f}-{light:.1f}, blot px {blot.sum()}")

    r1 = family_sliding(Lc, blot, dark, light, args.out)
    r2 = family_multires(Lc, blot, dark, light, args.out)
    r3 = family_checkerboard(Lc, blot, dark, light, args.out)

    with open(os.path.join(args.out, "sweep_summary.json"), "w") as f:
        json.dump({"sliding": r1, "multires": r2,
                   "checkerboard": r3}, f, indent=1)
    print("done ->", args.out)


if __name__ == "__main__":
    main()
