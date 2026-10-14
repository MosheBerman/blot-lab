#!/usr/bin/env python3
"""Scan-17 block follow-ups: (1) expanded selection (erode 4px not 9px),
(2) sharpened visualization, (3) FFT check for JPEG/aliasing vs physical
texture, (4) chained pipeline: flat-field -> PCA on RGB -> PC1 -> Gabor
bank (8 orientations) -> elongation stats, with dark-control comparison.
"""
import cv2
import numpy as np
import os

BASE = os.path.expanduser(
    "~/workspace/goals/the-coded-letters/hidden_files/drive/sweep/pages")
OUT = os.path.expanduser("~/workspace/goals/blot-lab-letter-forensics/files")
os.makedirs(OUT, exist_ok=True)

img = cv2.imread(os.path.join(BASE, "17-1.png"))
H, W = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
V = hsv[:, :, 2].astype(np.float32)
L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)

# ---- block detection (same as strict test) ----
black = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 95]))
quad = np.zeros_like(black)
quad[int(H * 0.55):, :int(W * 0.45)] = 255
cand = cv2.bitwise_and(black, quad)
n, labm, stats, _ = cv2.connectedComponentsWithStats(cand, 8)
order = np.argsort(-stats[1:, cv2.CC_STAT_AREA])
tops = [int(o) + 1 for o in order[:2]]
comp = np.isin(labm, tops)
ys, xs = np.where(comp)
x, y = int(xs.min()), int(ys.min())
w, h = int(xs.max() - x + 1), int(ys.max() - y + 1)
inside = cv2.erode(comp.astype(np.uint8), np.ones((4, 4), np.uint8)
                   ).astype(bool)   # EXPANDED selection: 4px not 9px
print(f"block bbox x[{x}:{x+w}] y[{y}:{y+h}]  expanded-inside px: "
      f"{inside.sum()}")

# dark uniform control: MIT LUFTPOST label
top = np.zeros_like(black)
top[0:int(H * 0.35), int(W * 0.35):int(W * 0.75)] = 255
darkctl = (cv2.bitwise_and(black, top) > 0)
n2, l2, s2, _ = cv2.connectedComponentsWithStats(darkctl.astype(np.uint8), 8)
darkctl = (l2 == 1 + int(np.argmax(s2[1:, cv2.CC_STAT_AREA])))
darkctl = cv2.erode(darkctl.astype(np.uint8),
                    np.ones((4, 4), np.uint8)).astype(bool)

# ---- (2) sharpened viz: flat-field + CLAHE + unsharp ----
x0, y0 = max(0, x - 60), max(0, y - 60)
x1, y1 = min(W, x + w + 60), min(H, y + h + 60)
cropL = L[y0:y1, x0:x1]
flat = cropL / (cv2.medianBlur(cropL.astype(np.uint8), 101)
                .astype(np.float32) + 1) * 128.0
flat = np.clip(flat, 0, 255).astype(np.uint8)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(flat)
blur = cv2.GaussianBlur(clahe, (0, 0), 2.0)
sharp = np.clip(clahe.astype(np.float32) * 1.6
                - blur.astype(np.float32) * 0.6, 0, 255).astype(np.uint8)
cv2.imwrite(os.path.join(OUT, "17-block-sharp.png"), sharp)
print("wrote 17-block-sharp.png")

# ---- (3) FFT: JPEG-block / aliasing signature? ----
bboxL = L[y:y + h, x:x + w]
m = inside[y:y + h, x:x + w]
filled = bboxL.copy()
filled[~m] = bboxL[m].mean()
wy, wx = np.hanning(h), np.hanning(w)
win = np.outer(wy, wx)
f = np.fft.fftshift(np.fft.fft2((filled - filled.mean()) * win))
P = np.log1p(np.abs(f) ** 2)
cy, cx = h // 2, w // 2
N = min(h, w)
ratios = {}
for name, (du, dv) in {"h": (N // 8, 0), "v": (0, N // 8),
                       "d": (N // 8, N // 8)}.items():
    disc = np.zeros_like(P, bool)
    yy, xx = np.ogrid[:h, :w]
    disc[((yy - (cy + dv)) ** 2 + (xx - (cx + du)) ** 2 <= 9)
         | ((yy - (cy - dv)) ** 2 + (xx - (cx - du)) ** 2 <= 9)] = True
    ring = np.zeros_like(P, bool)
    d2 = (yy - cy) ** 2 + (xx - cx) ** 2
    r = np.sqrt(du ** 2 + dv ** 2)
    ring[(d2 >= (r - 8) ** 2) & (d2 <= (r + 8) ** 2) & ~disc] = True
    ratios[name] = float(P[disc].mean() / (P[ring].mean() + 1e-9))
print("JPEG-block-frequency energy ratios (1.0 = no blocking signature):",
      {k: round(v, 2) for k, v in ratios.items()})
cv2.imwrite(os.path.join(OUT, "17-block-fft.png"),
            (255 * (P - P.min()) / (P.max() - P.min())).astype(np.uint8))


# ---- (4) chained pipeline ----
def chain(mask, tag):
    yy, xx = np.where(mask)
    by = (int(yy.min()), int(yy.max()) + 1)
    bx = (int(xx.min()), int(xx.max()) + 1)
    sub = img[by[0]:by[1], bx[0]:bx[1]].astype(np.float32)
    subL = L[by[0]:by[1], bx[0]:bx[1]]
    # flat-field
    med = cv2.medianBlur(subL.astype(np.uint8), 51).astype(np.float32) + 1
    fL = subL / med * 128.0
    # PCA on RGB inside mask -> PC1 (ink-density axis)
    px = sub[mask[by[0]:by[1], bx[0]:bx[1]]].reshape(-1, 3)
    px -= px.mean(axis=0)
    _, _, vt = np.linalg.svd(px, full_matrices=False)
    pc1 = ((sub - sub.mean(axis=(0, 1))) @ vt[0])
    pc1n = cv2.normalize(pc1, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    pc1n = (pc1n.astype(np.float32)
            - cv2.medianBlur(pc1n, 31).astype(np.float32) + 128)
    pc1n = np.clip(pc1n, 0, 255).astype(np.uint8)
    # Gabor bank, 8 orientations
    gmax = np.zeros_like(pc1n, dtype=np.float32)
    for ti in range(8):
        th = ti * np.pi / 8
        kern = cv2.getGaborKernel((21, 21), 2.5, th, 8.0, 0.5, 0,
                                 ktype=cv2.CV_32F)
        r = cv2.filter2D(pc1n, cv2.CV_32F, kern)
        gmax = np.maximum(gmax, np.abs(r))
    msub = mask[by[0]:by[1], bx[0]:bx[1]]
    vals = gmax[msub]
    thr = np.percentile(vals, 97)
    sig = (gmax > thr).astype(np.uint8)
    sig[~msub] = 0
    nn, ll, ss, _ = cv2.connectedComponentsWithStats(sig, 8)
    elong = 0
    big = 0
    for j in range(1, nn):
        a = ss[j, cv2.CC_STAT_AREA]
        ww, hh = ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT]
        big = max(big, a)
        if a >= 12 and max(ww, hh) / max(1, min(ww, hh)) > 2.5 \
                and max(ww, hh) > 15:
            elong += 1
    print(f"[{tag}] gabor-chain: {nn - 1} components, largest {big}px, "
          f"elongated: {elong}")
    return gmax, (by, bx)


g_block, (by_b, bx_b) = chain(inside, "block-ink")
g_dark, (by_d, bx_d) = chain(darkctl, "dark-control")
# viz: gabor max-response on block, masked
viz = np.zeros_like(g_block)
viz[inside[by_b[0]:by_b[1], bx_b[0]:bx_b[1]]] = \
    g_block[inside[by_b[0]:by_b[1], bx_b[0]:bx_b[1]]]
viz = cv2.normalize(viz, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
cv2.imwrite(os.path.join(OUT, "17-block-chain-gabor.png"),
            cv2.applyColorMap(viz, cv2.COLORMAP_INFERNO))
print("wrote 17-block-chain-gabor.png, 17-block-fft.png")
print("done")
