#!/usr/bin/env python3
"""Do the traced shapes inside the scan-17 block match other strokes on the
page? Template matching: interior candidate patches vs a library of real
handwriting-stroke patches vs a null library (dark-control ink texture +
blank paper), at multiple scales. Reports best-match scores, margins, and
a calibration (ref-vs-ref, null-vs-ref). Saves an overlay figure.
"""
import cv2
import numpy as np
import os

BASE = os.path.expanduser(
    "~/workspace/goals/the-coded-letters/hidden_files/drive/sweep/pages")
OUT = os.path.expanduser("~/workspace/goals/blot-lab-letter-forensics/files")
os.makedirs(OUT, exist_ok=True)
P = 56  # patch size
SCALES = [0.5, 0.7, 1.0, 1.4, 2.0]

img = cv2.imread(os.path.join(BASE, "17-1.png"))
H, W = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
S, V = hsv[:, :, 1].astype(np.float32), hsv[:, :, 2].astype(np.float32)
L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)
flat = L / (cv2.medianBlur(L.astype(np.uint8), 101).astype(np.float32) + 1)
flat = np.clip(flat * 128.0, 0, 255).astype(np.float32)


def norm_patch(im, cx, cy, size=P):
    x0, y0 = int(cx - size // 2), int(cy - size // 2)
    if x0 < 0 or y0 < 0 or x0 + size > W or y0 + size > H:
        return None
    p = im[y0:y0 + size, x0:x0 + size].astype(np.float32)
    p -= p.mean()
    s = p.std()
    return p / (s + 1e-9)


# ---- block mask (expanded selection) ----
black = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 95]))
quad = np.zeros_like(black)
quad[int(H * 0.55):, :int(W * 0.45)] = 255
cand = cv2.bitwise_and(black, quad)
n, labm, stats, _ = cv2.connectedComponentsWithStats(cand, 8)
order = np.argsort(-stats[1:, cv2.CC_STAT_AREA])
comp = np.isin(labm, [int(o) + 1 for o in order[:2]])
inside = cv2.erode(comp.astype(np.uint8), np.ones((4, 4), np.uint8)
                   ).astype(bool)
ys, xs = np.where(comp)
bx = (int(xs.min()), int(xs.max()) + 1)
by = (int(ys.min()), int(ys.max()) + 1)

# ---- candidates: most stroke-like interior features ----
sub = flat[by[0]:by[1], bx[0]:bx[1]]
gmax = np.zeros_like(sub)
for ti in range(8):
    kern = cv2.getGaborKernel((21, 21), 2.5, ti * np.pi / 8, 8.0, 0.5, 0,
                              ktype=cv2.CV_32F)
    gmax = np.maximum(gmax, np.abs(cv2.filter2D(sub, cv2.CV_32F, kern)))
msub = inside[by[0]:by[1], bx[0]:bx[1]]
thr = np.percentile(gmax[msub], 97)
sig = (gmax > thr).astype(np.uint8)
sig[~msub] = 0
nn, ll, ss, cc = cv2.connectedComponentsWithStats(sig, 8)
feats = []
for j in range(1, nn):
    a = ss[j, cv2.CC_STAT_AREA]
    ww, hh = ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT]
    if a < 8:
        continue
    score = max(ww, hh) * (max(ww, hh) / max(1, min(ww, hh)))
    feats.append((score, cc[j][0] + bx[0], cc[j][1] + by[0], a, ww, hh))
feats.sort(reverse=True)
cands = []
for score, cx, cy, a, ww, hh in feats[:12]:
    p = norm_patch(flat, cx, cy)
    if p is not None:
        cands.append({"p": p, "cx": cx, "cy": cy, "area": a,
                      "score": score})
print(f"{len(cands)} candidate interior patches")

# ---- reference library: real handwriting strokes elsewhere ----
msg = np.zeros_like(black)
msg[int(H * 0.08):int(H * 0.92), 0:int(W * 0.55)] = 255
msg[by[0] - 40:by[1] + 40, bx[0] - 40:bx[1] + 40] = 0  # not the block
ink = cv2.inRange(hsv, np.array([0, 25, 0]), np.array([180, 255, 150]))
ink = cv2.bitwise_and(ink, msg)
nr, lr, sr, cr = cv2.connectedComponentsWithStats(ink, 8)
refs = []
for j in range(1, nr):
    a = sr[j, cv2.CC_STAT_AREA]
    ww, hh = sr[j, cv2.CC_STAT_WIDTH], sr[j, cv2.CC_STAT_HEIGHT]
    if 60 <= a <= 4000 and (max(ww, hh) / max(1, min(ww, hh)) > 1.8
                            or a > 300):
        p = norm_patch(flat, cr[j][0], cr[j][1])
        if p is not None:
            refs.append(p)
    if len(refs) >= 40:
        break
print(f"{len(refs)} reference stroke patches")

# ---- null library: dark-control texture + blank paper ----
top = np.zeros_like(black)
top[0:int(H * 0.35), int(W * 0.35):int(W * 0.75)] = 255
darkctl = cv2.erode(cv2.bitwise_and(black, top),
                    np.ones((4, 4), np.uint8)).astype(bool)
paper = (V > 200) & (S < 40)
nulls = []
rng = np.random.default_rng(7)
for m, cnt in ((darkctl, 25), (paper, 25)):
    yy, xx = np.where(m)
    idx = rng.choice(len(xx), size=min(cnt * 4, len(xx)), replace=False)
    for i in idx:
        p = norm_patch(flat, xx[i], yy[i])
        if p is not None:
            nulls.append(p)
        if len(nulls) >= cnt * 2:
            break
    if len(nulls) >= 50:
        break
nulls = nulls[:50]
print(f"{len(nulls)} null patches")


def best_match(cand_patch, library):
    best, best_scale, best_lib = -1, None, None
    for s in SCALES:
        sz = max(8, int(round(P * s)))
        c = cv2.resize(cand_patch, (sz, sz), interpolation=cv2.INTER_AREA)
        for lib in library:
            if s <= 1.0:
                r = cv2.matchTemplate(lib, c, cv2.TM_CCOEFF_NORMED)
            else:
                r = cv2.matchTemplate(c, lib, cv2.TM_CCOEFF_NORMED)
            v = float(r.max())
            if v > best:
                best, best_scale, best_lib = v, s, lib
    return best, best_scale, best_lib


print("\n candidate | best_ref @scale | best_null @scale | margin")
rows = []
for i, c in enumerate(cands):
    br, sr_, blib = best_match(c["p"], refs)
    bn, sn_, _ = best_match(c["p"], nulls)
    rows.append((i, br, sr_, bn, sn_, br - bn, blib, c))
    print(f"  c{i:02d} ({c['cx']},{c['cy']}) | {br:.3f} @{sr_} | "
          f"{bn:.3f} @{sn_} | {br - bn:+.3f}")

# calibration: ref-vs-ref and null-vs-ref typical scores
rr = [best_match(refs[k], refs[:k] + refs[k + 1:])[0] for k in range(0, 10)]
nr_ = [best_match(nulls[k], refs)[0] for k in range(0, 10)]
print(f"\ncalibration: ref-vs-ref mean {np.mean(rr):.3f} | "
      f"null-vs-ref mean {np.mean(nr_):.3f}")
margins = [r[5] for r in rows]
print(f"candidates: mean margin {np.mean(margins):+.3f}, "
      f"max margin {np.max(margins):+.3f}")

# ---- overlay figure for top-3 by margin ----
def panel(g, hf=112):
    u8 = cv2.normalize(g, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return cv2.resize(cv2.cvtColor(u8, cv2.COLOR_GRAY2BGR), (hf, hf),
                      interpolation=cv2.INTER_NEAREST)


rows.sort(key=lambda r: r[5], reverse=True)
fig_rows = []
for i, br, sr_, bn, sn_, mg, blib, c in rows[:3]:
    sz = max(8, int(round(P * sr_)))
    cc = cv2.resize(c["p"], (sz, sz), interpolation=cv2.INTER_AREA)
    ref = cv2.resize(blib, (sz, sz),
                     interpolation=cv2.INTER_AREA) if sr_ <= 1.0 else blib
    a = cv2.normalize(cc, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    b = cv2.normalize(ref, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    ov = np.zeros((a.shape[0], a.shape[1], 3), np.uint8)
    ov[:, :, 2], ov[:, :, 1] = a, b
    sep = np.full((112, 16, 3), 255, np.uint8)
    fig_rows.append(np.hstack([panel(c["p"]), sep, panel(b),
                               sep, cv2.resize(ov, (112, 112),
                                               interpolation=cv2.INTER_NEAREST)]))
fig = np.vstack(fig_rows)
cv2.imwrite(os.path.join(OUT, "17-block-template-match.png"), fig)
print("wrote 17-block-template-match.png")
