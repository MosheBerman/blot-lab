#!/usr/bin/env python3
"""
postcard_sweeps.py — full sweep permutations on the postcard redaction targets.

Reuses the three sweep families from sweep_windows.py (sliding windows,
multi-resolution, checkerboard) with target-appropriate gating:

- scan17 (black redaction block): dark-ink gate (V<110) from
  blackblock_isolate.py; lightness channel only.
- scan51 (blue dabs, same hue as writing): saturated-blue gate from
  shade_isolate.py to catch the dab cores; sweeps run on lightness,
  saturation, AND hue channels (worker 4 found saturation separates dab
  cores from writing while hue does not — the sweep confirms per band).

Outputs under img/passes/postcards/scan17/sweeps/ and
img/passes/postcards/scan51/sweeps/<crop>/.

Usage:
    python3 scripts/postcard_sweeps.py
"""

import json
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sweep_windows import (family_sliding, family_multires,
                           family_checkerboard)
from blackblock_isolate import detect_black_roi
from shade_isolate import detect_blot_roi


def chan_range(ch, mask, lo=2, hi=98):
    vals = ch[mask]
    if vals.size == 0:
        raise RuntimeError("empty mask for channel range")
    return float(np.percentile(vals, lo)), float(np.percentile(vals, hi))


def run_all(channel, mask, dark, light, outdir, label):
    os.makedirs(outdir, exist_ok=True)
    print(f"--- {label}: shape {channel.shape}, mask px {mask.sum()}, "
          f"range {dark:.1f}-{light:.1f}")
    r1 = family_sliding(channel, mask, dark, light, outdir)
    r2 = family_multires(channel, mask, dark, light, outdir)
    r3 = family_checkerboard(channel, mask, dark, light, outdir)
    with open(os.path.join(outdir, "sweep_summary.json"), "w") as f:
        json.dump({"sliding": r1, "multires": r2,
                   "checkerboard": r3}, f, indent=1)


def scan17():
    src = "img/passes/postcards/scan17/source-crop.png"
    img = cv2.imread(src)
    if img is None:
        raise RuntimeError(f"cannot read {src}")
    (x0, y0, x1, y1), mask = detect_black_roi(img, margin=30)
    L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0][y0:y1, x0:x1]
    dark, light = chan_range(L, mask)
    run_all(L, mask, dark, light,
            "img/passes/postcards/scan17/sweeps", "scan17/L")


def scan51():
    crops = {
        "blob": "img/passes/postcards/scan51/source-crop-blob.png",
        "left": "img/passes/postcards/scan51/source-crop-left.png",
        "right": "img/passes/postcards/scan51/source-crop-right.png",
    }
    for name, src in crops.items():
        img = cv2.imread(src)
        if img is None:
            raise RuntimeError(f"cannot read {src}")
        (x0, y0, x1, y1), mask = detect_blot_roi(img, margin=30)
        crop = img[y0:y1, x0:x1]
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(crop, cv2.COLOR_BGR2LAB)
        channels = {
            "L": lab[:, :, 0].astype(np.float32),
            "S": hsv[:, :, 1].astype(np.float32),
            # OpenCV hue 0-179; dabs live ~51-54 (102-108 deg)
            "H": hsv[:, :, 0].astype(np.float32),
        }
        for chname, ch in channels.items():
            dark, light = chan_range(ch, mask)
            run_all(ch, mask, dark, light,
                    f"img/passes/postcards/scan51/sweeps/{name}/{chname}",
                    f"scan51/{name}/{chname}")


if __name__ == "__main__":
    scan17()
    scan51()
    print("done")
