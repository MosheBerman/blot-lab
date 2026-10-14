#!/usr/bin/env python3
"""Trace the dotted rows inside the scan-17 block.

Replicates the lab's Chroma mask exactly (pure hue gate: |H-center| < width,
H in 0-179), extracts dot centroids, fits the two rows, measures spacing,
and unions nearby hue centers to test whether the dots connect.
"""
import cv2
import numpy as np

import sys
SRC = sys.argv[1] if len(sys.argv) > 1 else "/home/hatch/workspace/blot-lab/img/passes/postcards/scan17/block-closeup.png"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/hatch/workspace/your_files/dot-trace/"

img = cv2.imread(SRC)
h, w = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
H = hsv[:, :, 0].astype(np.float32)

def hue_mask(center, width):
    dh = np.abs(H - center)
    dh = np.minimum(dh, 180.0 - dh)
    return dh < width

def dots_of(mask, min_area=3):
    n, lab, stats, cent = cv2.connectedComponentsWithStats(mask.astype(np.uint8) * 255, 8)
    keep = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= min_area]
    return np.array([cent[i] for i in keep]), np.array([stats[i, cv2.CC_STAT_AREA] for i in keep])

def fit_rows(cent):
    """Two rows: split by y at the largest gap, fit x->y line per row."""
    ys = np.sort(cent[:, 1])
    gaps = np.diff(ys)
    split = ys[np.argmax(gaps)]
    rows = [cent[cent[:, 1] <= split], cent[cent[:, 1] > split]]
    out = []
    for r in rows:
        if len(r) < 3:
            out.append(None); continue
        A = np.vstack([r[:, 0], np.ones(len(r))]).T
        m, b = np.linalg.lstsq(A, r[:, 1], rcond=None)[0]
        resid = r[:, 1] - (m * r[:, 0] + b)
        xs = np.sort(r[:, 0])
        gapsx = np.diff(xs)
        out.append(dict(n=len(r), slope=m, icept=b, resid_std=float(np.std(resid)),
                        y_mean=float(r[:, 1].mean()),
                        gap_med=float(np.median(gapsx)) if len(gapsx) else 0,
                        gap_std=float(np.std(gapsx)) if len(gapsx) else 0))
    return out, split

print(f"image {w}x{h}")
for center, width in [(105, 8), (100, 8), (110, 8), (105, 16)]:
    m = hue_mask(center, width)
    cent, areas = dots_of(m)
    print(f"\ncenter={center} width={width}: mask px={m.sum()} dots(n>=3px)={len(cent)}")
    if len(cent) >= 6:
        rows, split = fit_rows(cent)
        print(f"  y-split={split:.1f}")
        for i, r in enumerate(rows):
            if r is None:
                print(f"  row{i}: too few"); continue
            print(f"  row{i}: n={r['n']} y~{r['y_mean']:.0f} slope={r['slope']:.4f} "
                  f"resid_std={r['resid_std']:.1f}px xgap_med={r['gap_med']:.1f} xgap_std={r['gap_std']:.1f}")

# union of nearby hue centers ("append nearby bands")
um = np.zeros_like(H, dtype=bool)
for c in range(95, 126, 5):
    um |= hue_mask(c, 8)
cent, areas = dots_of(um)
print(f"\nUNION centers 95..125 step5 width8: mask px={um.sum()} dots={len(cent)}")
if len(cent) >= 6:
    rows, split = fit_rows(cent)
    print(f"  y-split={split:.1f}")
    for i, r in enumerate(rows):
        if r is None: continue
        print(f"  row{i}: n={r['n']} y~{r['y_mean']:.0f} slope={r['slope']:.4f} "
              f"resid_std={r['resid_std']:.1f}px xgap_med={r['gap_med']:.1f} xgap_std={r['gap_std']:.1f}")

# annotation: dots + fitted rows on the 105/8 mask
m = hue_mask(105, 8)
cent, _ = dots_of(m)
vis = img.copy()
for x, y in cent:
    cv2.circle(vis, (int(x), int(y)), 4, (0, 0, 255), 2)
if len(cent) >= 6:
    rows, _ = fit_rows(cent)
    for r in rows:
        if r is None: continue
        x0, x1 = 0, w - 1
        cv2.line(vis, (x0, int(r['slope'] * x0 + r['icept'])),
                 (x1, int(r['slope'] * x1 + r['icept'])), (0, 0, 255), 2)
import os
os.makedirs(OUT, exist_ok=True)
cv2.imwrite(OUT + "dots-traced-105-8.png", vis)
# union version
cent_u, _ = dots_of(um)
vis2 = img.copy()
for x, y in cent_u:
    cv2.circle(vis2, (int(x), int(y)), 4, (0, 0, 255), 2)
cv2.imwrite(OUT + "dots-union-95-125.png", vis2)
print("\nwrote", OUT)
