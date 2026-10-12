#!/usr/bin/env python3
"""
lighter_blot_calibrate.py — natural calibration targets from scans 33/40.

Earlier verdicts called the marks on scan33 p1 and scan40 p1 drips/stains/
foxing. Their opacity is what matters: they are REAL lighter blots, giving
a natural calibration point between the synthetic s=0.5 (works) and s=1.0
(fails) from img/passes/calibration/.

Per mark:
  1. detect the mark (blob filter: large compact dark/saturated component,
     distinguished from thin writing strokes)
  2. measure opacity on the synthetic-calibration scale:
       s_eq = mean over mark px of clip((249 - L) / (249 - 128), 0, 1)
     (249 = blot-39 paper L, 128 = blot-39 core L)
  3. run the standard passes: 12-band slicing + directional z-score
     (rows/cols/diag1/diag2 at k=1.5, 2.5)
  4. report whether the method behaves as the synthetic calibration
     predicts at that opacity, and whether any text resolves under/around
     the mark.

Outputs -> img/passes/lighter-blot-calibration/ (nothing committed).
"""

import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from shade_isolate import pass_directional, pass_global_bands, shade_range

OUT = "img/passes/lighter-blot-calibration"
# blot-39 reference values from the synthetic calibration
PAPER_L39, CORE_L39 = 249.0, 128.0


def lab_L(bgr):
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)


def find_mark_blobs(img, kind):
    """Return list of (bbox, mask) for large compact mark blobs.

    kind='blue': saturated-blue gate (scan40 drips, same ink as writing).
    kind='dark': darkness gate (scan33 grayish drip).
    Writing strokes are filtered out by compactness: blobs must fill a
    decent fraction of their bounding box.
    """
    L = lab_L(img)
    if kind == "blue":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gate = cv2.inRange(hsv, np.array([85, 60, 30]),
                           np.array([130, 255, 255])) > 0
    else:
        paper = float(np.median(L))
        gate = L < (paper - 25)
    gate = cv2.morphologyEx(gate.astype(np.uint8), cv2.MORPH_CLOSE,
                            np.ones((7, 7), np.uint8)) > 0
    n, labels, stats, _ = cv2.connectedComponentsWithStats(
        gate.astype(np.uint8), 8)
    blobs = []
    for i in range(1, n):
        area = stats[i, cv2.CC_STAT_AREA]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        if area < 1500:          # too small: speckle / stroke fragment
            continue
        compact = area / max(w * h, 1)
        if compact < 0.25:       # sprawling: text line, not a blob
            continue
        if max(w, h) > 600:      # whole-page component: writing mass
            continue
        x, y = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP]
        blobs.append(((x, y, x + w, y + h), labels == i))
    # largest first
    blobs.sort(key=lambda b: b[1].sum(), reverse=True)
    return blobs


def run_target(img, tag, bbox, mask):
    x0, y0, x1, y1 = bbox
    m = 40
    H, W = img.shape[:2]
    rx0, ry0 = max(0, x0 - m), max(0, y0 - m)
    rx1, ry1 = min(W, x1 + m), min(H, y1 + m)
    crop = img[ry0:ry1, rx0:rx1]
    cv2.imwrite(f"{OUT}/{tag}_roi.png", crop)
    Lc = lab_L(crop)
    mm = np.zeros(Lc.shape, bool)
    mm[y0 - ry0:y1 - ry0, x0 - rx0:x1 - rx0] = mask[y0:y1, x0:x1]

    # opacity on the synthetic scale
    paper_L = float(np.median(Lc[~mm]))
    core_L = float(np.percentile(Lc[mm], 2))
    s_eq = float(np.clip((PAPER_L39 - Lc[mm]) /
                         (PAPER_L39 - CORE_L39), 0, 1).mean())
    print(f"{tag}: ROI x[{rx0}:{rx1}] y[{ry0}:{ry1}] mark px={mm.sum()} "
          f"paper_L={paper_L:.1f} core_L={core_L:.1f} s_eq={s_eq:.2f}")

    dark, light = shade_range(Lc, mm)
    pass_global_bands(Lc, mm, dark, light, 12, OUT, tag=f"{tag}_A12")
    for k in (1.5, 2.5):
        for d in ("rows", "cols", "diag1", "diag2"):
            pass_directional(Lc, mm, k, OUT, tag=f"{tag}_BCD", direction=d)
    return dict(tag=tag, paper_L=paper_L, core_L=core_L, s_eq=s_eq,
                mark_px=int(mm.sum()), dark=dark, light=light)


def main():
    os.makedirs(OUT, exist_ok=True)
    results = []
    for fname, kind, label in [("scan33-1.png", "dark", "scan33"),
                              ("scan40-1.png", "blue", "scan40")]:
        img = cv2.imread(os.path.join(OUT, fname))
        blobs = find_mark_blobs(img, kind)
        print(f"{label}: {len(blobs)} candidate blobs")
        # take up to 3 largest
        for j, (bbox, mask) in enumerate(blobs[:3]):
            x0, y0, x1, y1 = bbox
            print(f"  blob{j}: bbox x[{x0}:{x1}] y[{y0}:{y1}] "
                  f"px={mask.sum()}")
            results.append(run_target(img, f"{label}_b{j}", bbox, mask))
    # summary
    with open(f"{OUT}/measurements.txt", "w") as f:
        for r in results:
            f.write(f"{r['tag']}: paper_L={r['paper_L']:.1f} "
                    f"core_L={r['core_L']:.1f} s_eq={r['s_eq']:.2f} "
                    f"mark_px={r['mark_px']} shade L {r['dark']:.1f}.."
                    f"{r['light']:.1f}\n")
    print("done ->", OUT)


if __name__ == "__main__":
    main()
