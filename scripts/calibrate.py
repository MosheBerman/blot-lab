#!/usr/bin/env python3
"""
calibrate.py — ground-truth calibration for shade-band isolation.

1. Baseline: run band + directional passes on CLEAN readable text, so we
   know what known letterforms look like in the pass outputs.
2. Synthetic blot: model the real letter-39 blot as a variable-opacity
   wash (opacity map estimated from the real blot), overlay it on clean
   text at several overall opacity scales, run the passes, and measure at
   which opacity the text stops being recoverable. This sets the
   detection floor for the real blot-39 negative.

Outputs -> img/passes/calibration/ (nothing committed by this script).
"""

import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from shade_isolate import (detect_blot_roi, pass_directional,
                           pass_global_bands, shade_range)

IMG = "img/blot39.jpg"
OUT = "img/passes/calibration"
# clean text region (top of blot39, away from blot) and blot ROI geometry
# blot ROI from the earlier run: x[88:474] y[389:726]  -> 386 x 337
TX0, TY0, TX1, TY1 = 88, 20, 474, 357
BX0, BY0, BX1, BY1 = 88, 389, 474, 726


def lab_L(bgr):
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)


def main():
    os.makedirs(OUT, exist_ok=True)
    img = cv2.imread(IMG)

    # ---- real blot: mask + opacity map ---------------------------------
    (x0, y0, x1, y1), blot_m = detect_blot_roi(img, margin=40)
    assert (x0, y0, x1, y1) == (BX0, BY0, BX1, BY1), "ROI drift!"
    B = img[y0:y1, x0:x1].astype(np.float32)
    Lb = lab_L(img[y0:y1, x0:x1])

    # paper reference: median L of non-blot pixels inside ROI
    paper_L = float(np.median(Lb[~blot_m]))
    ink_L = float(np.percentile(Lb[blot_m], 2))  # darkest core
    # opacity map: 0 = paper, 1 = fully saturated core
    op = np.clip((paper_L - Lb) / max(paper_L - ink_L, 1e-6), 0, 1)
    op[~blot_m] = 0.0
    # ink color: median BGR of the darkest 10% of blot pixels
    core = blot_m & (Lb <= np.percentile(Lb[blot_m], 10))
    ink_col = np.median(B[core], axis=0)
    print(f"paper_L={paper_L:.1f} ink_L={ink_L:.1f} "
          f"ink_col={ink_col.round(1)} mean_op={op[blot_m].mean():.2f}")

    # ---- clean text ------------------------------------------------------
    T = img[TY0:TY1, TX0:TX1].astype(np.float32)
    assert T.shape[:2] == B.shape[:2], f"{T.shape} vs {B.shape}"
    cv2.imwrite(f"{OUT}/00_clean_text.png", T.astype(np.uint8))

    # baseline: bands on clean text (mask = everything: paper+ink separate)
    full = np.ones(T.shape[:2], bool)
    Lt = lab_L(T.astype(np.uint8))
    d0, l0 = shade_range(Lt, full)
    print(f"clean text shade range L {d0:.1f}..{l0:.1f}")
    pass_global_bands(Lt, full, d0, l0, 12, OUT, tag="baseA_clean")
    for k in (1.5, 2.5):
        pass_directional(Lt, full, k, OUT, tag="baseBCD_clean",
                         direction="rows")

    # ---- synthetic blots --------------------------------------------------
    Tu = T.astype(np.uint8)
    for s in (0.5, 0.75, 1.0, 1.25):
        o = np.clip(s * op, 0, 1)[..., None]
        synth = (o * ink_col + (1 - o) * T)
        synth_u8 = np.clip(synth, 0, 255).astype(np.uint8)
        cv2.imwrite(f"{OUT}/10_synth_s{s}.png", synth_u8)
        Ls = lab_L(synth_u8)
        # run passes restricted to the blot mask (as with the real blot)
        ds, ls_ = shade_range(Ls, blot_m)
        pass_global_bands(Ls, blot_m, ds, ls_, 12, OUT,
                           tag=f"S_s{s}_A12")
        for k in (1.5, 2.5):
            pass_directional(Ls, blot_m, k, OUT, tag=f"S_s{s}",
                             direction="rows")
        # occupancy of the darkest band: proxy for "how much text-like
        # dark structure survives"
        edges = np.linspace(ds, ls_, 13)
        dark_px = int((blot_m & (Ls >= edges[0]) & (Ls < edges[2])).sum())
        print(f"s={s}: shade L {ds:.1f}..{ls_:.1f} "
              f"darkest-2-bands px={dark_px}")

    # ---- size floor: smaller glyphs at real-blot opacity ------------------
    small = cv2.resize(Tu, None, fx=0.5, fy=0.5,
                       interpolation=cv2.INTER_AREA)
    small = cv2.resize(small, (Tu.shape[1], Tu.shape[0]),
                       interpolation=cv2.INTER_CUBIC).astype(np.float32)
    o = np.clip(op, 0, 1)[..., None]
    synth_small = np.clip(o * ink_col + (1 - o) * small, 0, 255
                          ).astype(np.uint8)
    cv2.imwrite(f"{OUT}/20_synth_small_s1.0.png", synth_small)
    Ls2 = lab_L(synth_small)
    ds2, ls2 = shade_range(Ls2, blot_m)
    pass_global_bands(Ls2, blot_m, ds2, ls2, 12, OUT, tag="S_small_A12")
    print("done ->", OUT)


if __name__ == "__main__":
    main()
