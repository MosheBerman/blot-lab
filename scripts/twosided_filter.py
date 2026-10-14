#!/usr/bin/env python3
"""
twosided_filter.py — two-sided coincidence filter over the shade stack.

Moshe's idea (2026-10-14): the Bands sweep looks at one band at a time,
dark -> light (one direction). If a hidden stroke pools ink unevenly along
its length (the ridge hypothesis from 2026-10-12), it modulates the ink at
EVERY depth — so stroke structure should appear in the DARK end (front)
AND the LIGHT end (back) of the stack at the same (x, y). Requiring
coincidence in both ends keeps depth-persistent structure and cancels wash
noise that is uncorrelated across depths.

Method:
1. Shade-slice the blot mask into N bands (family A machinery from
   shade_isolate.py).
2. dark_dev: pixels inside the darkest E bands whose lightness deviates
   |z| > k from the dark-end median/std.
   light_dev: pixels inside the lightest E bands whose lightness deviates
   |z| > k from the light-end median/std.
3. coincidence = dilate(dark_dev, tol) & dilate(light_dev, tol).

Calibration protocol: run on the synthetic washes with KNOWN text first
(s=0.5 is the positive control — the method must recover glyph fragments;
s=1.0 is the negative control), then on the real blot-39 crop.

Usage:
    python3 twosided_filter.py IMG --out DIR [--bands N] [--ends E]
        [--k K] [--tol T] [--fullmask] [--textmask PATH]
"""

import argparse
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from shade_isolate import detect_blot_roi, shade_range


def lab_L(bgr):
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)


def band_index_map(L, mask, dark, light, n_bands):
    """Per-pixel band index 1..n_bands (0 = outside mask)."""
    edges = np.linspace(dark, light, n_bands + 1)
    idx = np.zeros_like(L, dtype=np.int32)
    for i in range(n_bands):
        m = mask & (L >= edges[i]) & (L < edges[i + 1])
        idx[m] = i + 1
    return idx


def end_deviation(L, mask, idx, n_bands, ends, which, k):
    """Deviation mask within the dark/light end of the stack.

    which='dark': bands 1..ends; which='light': bands n-ends+1..n.
    |z| > k against that end's own median/std.
    """
    if which == 'dark':
        end = mask & (idx >= 1) & (idx <= ends)
    else:
        end = mask & (idx >= n_bands - ends + 1) & (idx <= n_bands)
    vals = L[end]
    if vals.size < 8:
        return np.zeros_like(mask), 0.0, 0.0
    med, sd = float(np.median(vals)), float(vals.std()) + 1e-6
    z = np.abs((L - med) / sd)
    dev = end & (z > k)
    return dev, med, sd


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("image")
    ap.add_argument("--out", required=True)
    ap.add_argument("--bands", type=int, default=12)
    ap.add_argument("--ends", type=int, default=2,
                    help="bands at each end of the stack")
    ap.add_argument("--k", type=float, default=1.5)
    ap.add_argument("--tol", type=int, default=3,
                    help="dilation px for spatial coincidence")
    ap.add_argument("--fullmask", action="store_true",
                    help="use the whole image as the blot mask")
    ap.add_argument("--textmask", default=None,
                    help="known-text image for recall/precision scoring")
    ap.add_argument("--washref", default=None,
                    help="clean reference image: restricts mask+scoring to "
                         "the actual wash region (|B diff| > 25 or |L diff| > 20)")
    ap.add_argument("--mode", default="dev", choices=["dev", "anom"],
                    help="dev: deviation-within-each-end coincidence; "
                         "anom: band-index anomaly present at both depths")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    img = cv2.imread(args.image)
    if img is None:
        sys.exit(f"cannot read {args.image}")
    L = lab_L(img)
    H, W = L.shape

    if args.fullmask:
        mask = np.ones((H, W), bool)
    else:
        try:
            (_, _, _, _), m = detect_blot_roi(img)
            # detect returns roi-sized mask; rebuild full-size
            mask = np.zeros((H, W), bool)
            (x0, y0, x1, y1), _ = detect_blot_roi(img)  # noqa
            mask[y0:y1, x0:x1] = m
        except RuntimeError:
            mask = np.ones((H, W), bool)

    if args.washref:
        ref = cv2.imread(args.washref)
        if ref is not None and ref.shape == img.shape:
            dB = (img[:, :, 0].astype(np.float32)
                  - ref[:, :, 0].astype(np.float32))
            dL = np.abs(L - lab_L(ref))
            wash = (dB > 25) | (dL > 20)
            wash = cv2.morphologyEx(
                wash.astype(np.uint8), cv2.MORPH_CLOSE,
                np.ones((7, 7), np.uint8)) > 0
            mask = mask & wash

    dark, light = shade_range(L, mask)
    idx = band_index_map(L, mask, dark, light, args.bands)

    tag = (f"{args.mode}_b{args.bands}_e{args.ends}_k{args.k:g}_t{args.tol}")

    if args.mode == "anom":
        # Band-index anomaly: pixel sits >=2 bands away from its local
        # depth. A hidden stroke pooling ink shows up as a depth anomaly
        # at EVERY wash thickness it crosses, so require the anomaly in
        # both the dark half (front) and the light half (back).
        med_idx = cv2.medianBlur(idx.astype(np.uint8), 31).astype(np.int32)
        anom = mask & (np.abs(idx - med_idx) >= 2)
        front = anom & (idx <= args.bands // 2)
        back = anom & (idx > args.bands // 2)
        ddev, ldev = front, back
    else:
        ddev, dmed, dsd = end_deviation(L, mask, idx, args.bands, args.ends,
                                       'dark', args.k)
        ldev, lmed, lsd = end_deviation(L, mask, idx, args.bands, args.ends,
                                       'light', args.k)
        rep_extra = {
            "dark_end": (round(dmed, 1), round(dsd, 2), int(ddev.sum())),
            "light_end": (round(lmed, 1), round(lsd, 2), int(ldev.sum())),
        }

    kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                     (2 * args.tol + 1, 2 * args.tol + 1))
    dd = cv2.dilate(ddev.astype(np.uint8), kern) > 0
    ld = cv2.dilate(ldev.astype(np.uint8), kern) > 0
    coinc = dd & ld & mask

    cv2.imwrite(os.path.join(args.out, f"{tag}_dark_dev.png"),
                ddev.astype(np.uint8) * 255)
    cv2.imwrite(os.path.join(args.out, f"{tag}_light_dev.png"),
                ldev.astype(np.uint8) * 255)
    cv2.imwrite(os.path.join(args.out, f"{tag}_coincidence.png"),
                coinc.astype(np.uint8) * 255)
    # overlay on original for eyeballing
    ov = img.copy()
    ov[coinc] = (0, 0, 255)
    cv2.imwrite(os.path.join(args.out, f"{tag}_overlay.png"), ov)

    n_mask = int(mask.sum())
    rep = {
        "shade_range": (round(dark, 1), round(light, 1)),
        "dark_px": int(ddev.sum()),
        "light_px": int(ldev.sum()),
        "coincidence_px": int(coinc.sum()),
        "coincidence_frac_of_mask": round(float(coinc.sum()) / n_mask, 4),
    }
    if args.mode == "dev":
        rep.update(rep_extra)
    if args.textmask:
        timg = cv2.imread(args.textmask)
        if timg is not None and timg.shape[:2] == (H, W):
            tL = lab_L(timg)
            text = (tL < 200) & mask  # text under the wash only
            tp = int((coinc & text).sum())
            rep["text_px"] = int(text.sum())
            rep["recall"] = round(tp / max(text.sum(), 1), 4)
            rep["precision"] = round(tp / max(coinc.sum(), 1), 4)
    print(tag, rep)


if __name__ == "__main__":
    main()
