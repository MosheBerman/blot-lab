#!/usr/bin/env python3
"""
virtual_raking.py — mimic raking-light photography from a single camera photo.

The letter "scans" are camera photos with real directional shading, so
shape-from-shading is viable. Pipeline:

1. Estimate the dominant light azimuth from the slow illumination field on
   paper-only pixels (plane fit; light comes from the bright side).
2. Mask ink (local background subtraction + Otsu, dilated). Fill ink pixels
   with the local paper value so they don't inject false relief.
3. Relief estimate: high-pass the paper image; treat the residual as the
   surface-gradient component along the light azimuth, integrate along that
   azimuth to get a height proxy.
4. Virtual relight: render the height field under a grazing light (elevation
   ~12 deg) at 4 azimuths (0/90/180/270). The azimuth perpendicular to the
   original light is the classic raking view.

Usage:
    python3 virtual_raking.py --targets all --out img/passes/virtual-raking
"""

import argparse
import json
import math
import os

import cv2
import numpy as np

TARGETS = {
    "blot39":   ("img/blot39.jpg", (88, 389, 474, 726)),
    "scan17":   ("img/passes/postcards/scan17/source-crop.png", (0, 0, 0, 0)),
    "scan51b":  ("img/passes/postcards/scan51/source-crop-blob.png", (0, 0, 0, 0)),
    "scan51l":  ("img/passes/postcards/scan51/source-crop-left.png", (0, 0, 0, 0)),
    "berliner": ("img/passes/berliner-baseline/berliner_roi.png", (0, 0, 0, 0)),
}


def ink_mask(gray):
    bg = cv2.GaussianBlur(gray, (0, 0), 25)
    diff = cv2.subtract(bg, gray)
    _, m = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    return m > 0


def estimate_light_azimuth(gray, paper):
    """Plane fit to log-image on paper pixels; light from the bright side."""
    logf = np.log1p(gray.astype(np.float64))
    slow = cv2.GaussianBlur(logf, (0, 0), 60)
    ys, xs = np.nonzero(paper)
    if len(xs) < 1000:
        return None, None
    A = np.column_stack([xs, ys, np.ones_like(xs)])
    b = slow[ys, xs]
    coef, *_ = np.linalg.lstsq(A, b, rcond=None)
    gx, gy = coef[0], coef[1]  # brightness gradient
    # brightness increases toward the light: light azimuth = gradient direction
    az = math.degrees(math.atan2(gy, gx))  # deg, x-right, y-down, 0=east
    return az, slow


def fill_paper(gray, mask):
    """Replace ink pixels with local paper estimate (large-blur inpaint)."""
    f = gray.astype(np.float64)
    bg = cv2.GaussianBlur(f, (0, 0), 25)
    out = f.copy()
    out[mask] = bg[mask]
    return out


def relief_shading(paper_img, hp_sigma=3.0):
    """Micro-relief shading = high-pass of the illumination-flattened paper.

    Under the Lambertian + uniform-albedo model this is the surface-gradient
    component along the original light azimuth, up to a scale factor.
    The perpendicular gradient component is unobservable from one photo.
    """
    low = cv2.GaussianBlur(paper_img, (0, 0), 40)
    flat = paper_img - low
    hp = flat - cv2.GaussianBlur(flat, (0, 0), hp_sigma)
    return hp


def virtual_rake(hp, light_az_deg, view_az_deg, gain=5.0):
    """Render micro-relief under a virtual grazing light at view_az_deg.

    Only the gradient component along the original light azimuth is observed,
    so the visible signal scales with cos(view - light). gain models the
    contrast boost of grazing incidence: 1/tan(12deg) / 1/tan(45deg) ~ 4.7,
    assuming the photo was taken under roughly 45-degree lighting.
    At view = light +/- 90 the render is honestly flat: no signal there.
    """
    w = math.cos(math.radians(view_az_deg - light_az_deg))
    img = 128.0 + gain * w * hp
    return np.clip(img, 0, 255).astype(np.uint8)


def to8(img):
    p1, p99 = np.percentile(img, (1, 99.5))
    return np.clip((img - p1) / (p99 - p1 + 1e-9) * 255, 0, 255).astype(np.uint8)


def process(name, path, roi, outdir):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    x0, y0, x1, y1 = roi
    roi_img = img if (x0, y0, x1, y1) == (0, 0, 0, 0) else img[y0:y1, x0:x1]
    d = os.path.join(outdir, name)
    os.makedirs(d, exist_ok=True)
    cv2.imwrite(os.path.join(d, "roi.png"), roi_img)

    mask = ink_mask(roi_img)
    paper = ~mask
    cv2.imwrite(os.path.join(d, "inkmask.png"), (mask * 255).astype(np.uint8))

    az, slow = estimate_light_azimuth(roi_img, paper)
    info = {"target": name, "light_azimuth_deg": az,
            "paper_fraction": float(paper.mean())}
    if az is None:
        info["error"] = "insufficient paper pixels for light estimate"
        return info

    paper_img = fill_paper(roi_img, mask)
    hp = relief_shading(paper_img)
    cv2.imwrite(os.path.join(d, "relief_shading.png"), to8(hp))

    # relief strength diagnostic: rms of hp on paper, in gray levels
    info["relief_rms"] = float(np.sqrt(np.mean(hp[paper] ** 2)))

    # virtual lamp sweep: 8 azimuths relative to the original light.
    # 0 = same direction (amplified), 180 = lamp swung to the other side
    # (relief inverts: grooves flip dark/bright), +/-90 = honest null.
    renders = []
    for k in range(8):
        raz = (az + k * 45) % 360
        r = virtual_rake(hp, az, raz)
        fn = f"rake_rel{k*45:03d}.png"
        cv2.imwrite(os.path.join(d, fn), r)
        renders.append(fn)
    info["renders"] = renders
    info["note"] = ("renders are relative to estimated light azimuth; "
                    "rel090/rel270 are the honest null (no cross-light signal "
                    "in a single photo)")
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", nargs="+", default=["all"])
    ap.add_argument("--out", default="img/passes/virtual-raking")
    args = ap.parse_args()
    names = list(TARGETS) if args.targets == ["all"] else args.targets
    os.makedirs(args.out, exist_ok=True)
    results = {}
    for n in names:
        path, roi = TARGETS[n]
        print("processing", n, flush=True)
        results[n] = process(n, path, roi, args.out)
        print("   azimuth:", results[n].get("light_azimuth_deg"),
              "relief_rms:", round(results[n].get("relief_rms", -1), 3), flush=True)
    with open(os.path.join(args.out, "results.json"), "w") as f:
        json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
