#!/usr/bin/env python3
"""Scan-17 block on the HI-RES PDF source (2138x1494, ~1.9x the sweep PNG).
1. Strict interior test (same methodology, rescaled).
2. NEW: ink-mixture chromaticity analysis — is the obliterating ink's RGB
   signature different from the letter ink's? Look for interior pixels whose
   chromaticity pulls toward the letter ink (under-text ghosts would be
   spatially coherent/elongated).
3. Gabor chain at rescaled wavelengths.
4. "Synthetic coloring" isolated views: exterior blocked out, interior
   depth-colored / amplified.
"""
import cv2
import numpy as np
import os

SRC = "/home/hatch/workspace/blot-lab/img/source/17pdf-000.jpg"
OUT = "/home/hatch/workspace/goals/blot-lab-letter-forensics/files"
os.makedirs(OUT, exist_ok=True)

img = cv2.imread(SRC)
H, W = img.shape[:2]
print(f"hi-res {W}x{H}")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
S, V = hsv[:, :, 1].astype(np.float32), hsv[:, :, 2].astype(np.float32)
L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)
RGB = img[:, :, ::-1].astype(np.float32)

# ---- block detection ----
black = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 95]))
quad = np.zeros_like(black)
quad[int(H * 0.55):, :int(W * 0.45)] = 255
cand = cv2.bitwise_and(black, quad)
n, labm, stats, _ = cv2.connectedComponentsWithStats(cand, 8)
order = np.argsort(-stats[1:, cv2.CC_STAT_AREA])
print("top dark components in lower-left quad:")
for i in order[:5]:
    j = int(i) + 1
    print(f"  area={stats[j, 4]:7d} x={stats[j, 0]} y={stats[j, 1]} "
          f"w={stats[j, 2]} h={stats[j, 3]}")
tops = [int(o) + 1 for o in order[:2]]
comp = np.isin(labm, tops)
ys, xs = np.where(comp)
x, y = int(xs.min()), int(ys.min())
w, h = int(xs.max() - x + 1), int(ys.max() - y + 1)
inside = cv2.erode(comp.astype(np.uint8), np.ones((15, 15), np.uint8)
                   ).astype(bool)
print(f"block bbox x[{x}:{x+w}] y[{y}:{y+h}]  interior px: {inside.sum()}")

# ---- 1. strict interior test ----
hp = L - cv2.medianBlur(L.astype(np.uint8), 25).astype(np.float32)
sig_in = hp[inside]
# dark control: MIT LUFTPOST label top area
top = np.zeros_like(black)
top[0:int(H * 0.3), int(W * 0.4):int(W * 0.75)] = 255
darkctl = cv2.erode(cv2.bitwise_and(black, top),
                    np.ones((15, 15), np.uint8)).astype(bool)
sig_dc = hp[darkctl]
print(f"[strict] interior hp std {sig_in.std():.2f} vs dark-control "
      f"{sig_dc.std():.2f}")
thr = 3.0 * sig_dc.std()
sigmap = (np.abs(hp) > thr).astype(np.uint8)
sigmap[~inside] = 0
n3, l3, s3, _ = cv2.connectedComponentsWithStats(sigmap, 8)
elong = sum(1 for j in range(1, n3)
            if s3[j, cv2.CC_STAT_AREA] >= 30
            and max(s3[j, cv2.CC_STAT_WIDTH], s3[j, cv2.CC_STAT_HEIGHT])
            / max(1, min(s3[j, cv2.CC_STAT_WIDTH], s3[j, cv2.CC_STAT_HEIGHT])) > 2.5
            and max(s3[j, cv2.CC_STAT_WIDTH], s3[j, cv2.CC_STAT_HEIGHT]) > 28)
big = max([s3[j, cv2.CC_STAT_AREA] for j in range(1, n3)], default=0)
print(f"[strict] {n3-1} significant components, largest {big}px, "
      f"elongated: {elong}")

# ---- 2. ink-mixture chromaticity ----
# letter ink: dark saturated strokes in message area, away from block
msg = np.zeros_like(black)
msg[int(H * 0.05):int(H * 0.6), 0:int(W * 0.5)] = 255
letter_ink = cv2.inRange(hsv, np.array([0, 30, 0]),
                          np.array([180, 255, 150])) > 0
letter_ink = letter_ink & (msg > 0)
letter_ink = cv2.erode(letter_ink.astype(np.uint8),
                       np.ones((3, 3), np.uint8)).astype(bool)
print(f"letter-ink ref px: {letter_ink.sum()}")


def chroma_centroid(mask):
    px = RGB[mask]
    ch = px / (px.sum(axis=1, keepdims=True) + 1e-9)
    return ch.mean(axis=0), np.cov(ch.T)


c_let, _ = chroma_centroid(letter_ink)
c_top, _ = chroma_centroid(inside)
print(f"chromaticity letter ink: {c_let.round(3)}")
print(f"chromaticity top ink:    {c_top.round(3)}")
print(f"chromaticity distance: {np.linalg.norm(c_let - c_top):.4f}")
# per-pixel affinity: distance to letter ink minus distance to top ink
ch = RGB / (RGB.sum(axis=2, keepdims=True) + 1e-9)
d_let = np.linalg.norm(ch - c_let, axis=2)
d_top = np.linalg.norm(ch - c_top, axis=2)
affin = d_top - d_let  # positive => closer to letter ink
ai = affin[inside]
print(f"[mixture] interior affinity mean {ai.mean():+.4f} std {ai.std():.4f} "
      f"(>0 means letter-ink-like)")
# coherent letter-ink-like regions?
pos = (affin > ai.mean() + 2 * ai.std()).astype(np.uint8)
pos[~inside] = 0
n4, l4, s4, _ = cv2.connectedComponentsWithStats(pos, 8)
elong2 = sum(1 for j in range(1, n4)
             if s4[j, cv2.CC_STAT_AREA] >= 40
             and max(s4[j, cv2.CC_STAT_WIDTH], s4[j, cv2.CC_STAT_HEIGHT])
             / max(1, min(s4[j, cv2.CC_STAT_WIDTH], s4[j, cv2.CC_STAT_HEIGHT])) > 2.5
             and max(s4[j, cv2.CC_STAT_WIDTH], s4[j, cv2.CC_STAT_HEIGHT]) > 34)
big2 = max([s4[j, cv2.CC_STAT_AREA] for j in range(1, n4)], default=0)
print(f"[mixture] {n4-1} letter-ink-like components, largest {big2}px, "
      f"elongated: {elong2}")

# ---- 3. Gabor chain (rescaled) ----
flat = L / (cv2.medianBlur(L.astype(np.uint8), 101).astype(np.float32) + 1)
px = RGB[inside].reshape(-1, 3)
px -= px.mean(axis=0)
_, _, vt = np.linalg.svd(px, full_matrices=False)
pc1 = ((RGB - RGB.mean(axis=(0, 1))) @ vt[0])
pc1n = cv2.normalize(pc1, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
pc1n = np.clip(pc1n.astype(np.float32)
               - cv2.medianBlur(pc1n, 61).astype(np.float32) + 128,
               0, 255).astype(np.uint8)
gmax = np.zeros_like(pc1n, dtype=np.float32)
for ti in range(8):
    kern = cv2.getGaborKernel((41, 41), 4.5, ti * np.pi / 8, 14.0, 0.5, 0,
                              ktype=cv2.CV_32F)
    gmax = np.maximum(gmax, np.abs(cv2.filter2D(pc1n, cv2.CV_32F, kern)))
vals = gmax[inside]
thr = np.percentile(vals, 97)
sig = (gmax > thr).astype(np.uint8)
sig[~inside] = 0
n5, l5, s5, _ = cv2.connectedComponentsWithStats(sig, 8)
elong3 = sum(1 for j in range(1, n5)
             if s5[j, cv2.CC_STAT_AREA] >= 60
             and max(s5[j, cv2.CC_STAT_WIDTH], s5[j, cv2.CC_STAT_HEIGHT])
             / max(1, min(s5[j, cv2.CC_STAT_WIDTH], s5[j, cv2.CC_STAT_HEIGHT])) > 2.5
             and max(s5[j, cv2.CC_STAT_WIDTH], s5[j, cv2.CC_STAT_HEIGHT]) > 55)
big3 = max([s5[j, cv2.CC_STAT_AREA] for j in range(1, n5)], default=0)
print(f"[gabor-hi] {n5-1} components, largest {big3}px, elongated: {elong3}")

# ---- 4. synthetic-coloring isolated views ----
x0, y0 = max(0, x - 80), max(0, y - 80)
x1, y1 = min(W, x + w + 80), min(H, y + h + 80)
crop = img[y0:y1, x0:x1].copy()
blk = comp[y0:y1, x0:x1]
# A: exterior blocked out (flat), interior original
isoA = np.full_like(crop, 90)
isoA[blk] = crop[blk]
cv2.imwrite(f"{OUT}/17-hires-isolated.png", isoA)
# B: interior depth-colored (inferno on L), exterior blocked out
Lc = L[y0:y1, x0:x1]
depth = np.zeros_like(Lc)
dmin, dmax = Lc[blk].min(), Lc[blk].max()
depth[blk] = (Lc[blk] - dmin) / max(dmax - dmin, 1e-9) * 255
isoB = np.full_like(crop, 90)
isoB[blk] = cv2.applyColorMap(depth.astype(np.uint8),
                              cv2.COLORMAP_INFERNO)[blk]
cv2.imwrite(f"{OUT}/17-hires-depth.png", isoB)
# C: interior-only amplified high-pass, exterior blocked out
amp = np.full((*Lc.shape, 3), 90, np.uint8)
hh = np.clip((hp[y0:y1, x0:x1] * 6 + 128), 0, 255).astype(np.uint8)
amp[blk] = cv2.cvtColor(hh, cv2.COLOR_GRAY2BGR)[blk]
cv2.imwrite(f"{OUT}/17-hires-interior-amp.png", amp)
# D: letter-ink affinity map, interior only
am = np.full((*Lc.shape, 3), 90, np.uint8)
an = np.clip((affin[y0:y1, x0:x1] - ai.mean()) / (3 * ai.std() + 1e-9)
             * 127 + 128, 0, 255).astype(np.uint8)
am[blk] = cv2.applyColorMap(an, cv2.COLORMAP_JET)[blk]
cv2.imwrite(f"{OUT}/17-hires-affinity.png", am)
print("wrote 17-hires-isolated.png, 17-hires-depth.png, "
      "17-hires-interior-amp.png, 17-hires-affinity.png")
print("done")
