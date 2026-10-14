#!/usr/bin/env python3
"""Strict inside-the-black-block structure test (scan 17) + green/graphite/paper
signature comparison (letter 40 p2, same photo = same illumination).

Read-only on source scans. Writes viz PNGs to the blot-lab goal files/ dir.
"""
import cv2
import numpy as np
import os

BASE = os.path.expanduser(
    "~/workspace/goals/the-coded-letters/hidden_files/drive/sweep/pages")
OUT = os.path.expanduser("~/workspace/goals/blot-lab-letter-forensics/files")
os.makedirs(OUT, exist_ok=True)


def load(name):
    p = os.path.join(BASE, name)
    img = cv2.imread(p)
    assert img is not None, p
    return img


def hp_dev(L, ksize=15):
    med = cv2.medianBlur(L.astype(np.uint8), ksize).astype(np.float32)
    return L.astype(np.float32) - med


print("=" * 60)
print("PART A — scan 17 black block: structure strictly INSIDE the ink?")
print("=" * 60)
img = load("17-1.png")
H, W = img.shape[:2]
print(f"17-1.png {W}x{H}")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
V = hsv[:, :, 2].astype(np.float32)
S = hsv[:, :, 1].astype(np.float32)
L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)

black = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 95]))
quad = np.zeros_like(black)
quad[int(H * 0.55):, :int(W * 0.45)] = 255
cand = cv2.bitwise_and(black, quad)
n, labm, stats, _ = cv2.connectedComponentsWithStats(cand, 8)
order = np.argsort(-stats[1:, cv2.CC_STAT_AREA])
print("largest dark components in lower-left quad (area, bbox):")
for i in order[:6]:
    j = i + 1
    print(f"  area={stats[j, 4]:7d}  x={stats[j, 0]} y={stats[j, 1]} "
          f"w={stats[j, 2]} h={stats[j, 3]}")
# union of the two largest components (the block is two redaction strokes)
tops = [int(o) + 1 for o in order[:2]]
comp = np.isin(labm, tops)
ys, xs = np.where(comp)
x, y = int(xs.min()), int(ys.min())
w, h = int(xs.max() - x + 1), int(ys.max() - y + 1)
print(f"block = union of comps {tops}, bbox x[{x}:{x + w}] y[{y}:{y + h}]")
inside = cv2.erode(comp.astype(np.uint8),
                   np.ones((9, 9), np.uint8)).astype(bool)
print(f"block bbox x[{x}:{x + w}] y[{y}:{y + h}]  strictly-inside px: "
      f"{inside.sum()}")

# dark uniform control: the MIT LUFTPOST airmail label (top area, dark blue)
top = np.zeros_like(black)
top[0:int(H * 0.35), int(W * 0.35):int(W * 0.75)] = 255
darkctl = (cv2.bitwise_and(black, top) > 0)
# keep only the biggest dark blob up there (the label)
n2, l2, s2, _ = cv2.connectedComponentsWithStats(darkctl.astype(np.uint8), 8)
if n2 > 1:
    j2 = 1 + int(np.argmax(s2[1:, cv2.CC_STAT_AREA]))
    darkctl = (l2 == j2)
darkctl = cv2.erode(darkctl.astype(np.uint8),
                    np.ones((9, 9), np.uint8)).astype(bool)
print(f"dark control (airmail label) px: {darkctl.sum()}  mean L: "
      f"{L[darkctl].mean():.1f}  block mean L: {L[inside].mean():.1f}")

hp = hp_dev(L)
sig_in = hp[inside]
sig_dark = hp[darkctl]
print(f"inside-block hp std: {sig_in.std():.2f}   "
      f"dark-control hp std: {sig_dark.std():.2f}")
thr = 3.0 * sig_dark.std()
sigmap = (np.abs(hp) > thr).astype(np.uint8)
sigmap[~inside] = 0
n3, l3, s3, _ = cv2.connectedComponentsWithStats(sigmap, 8)
print(f"significant deviations inside block (>3 sigma of dark control): "
      f"{n3 - 1} components")
elong = 0
biggest_sig = 0
for j in range(1, n3):
    area = s3[j, cv2.CC_STAT_AREA]
    ww, hh = s3[j, cv2.CC_STAT_WIDTH], s3[j, cv2.CC_STAT_HEIGHT]
    biggest_sig = max(biggest_sig, area)
    if area >= 12 and max(ww, hh) / max(1, min(ww, hh)) > 2.5 \
            and max(ww, hh) > 15:
        elong += 1
print(f"largest significant component: {biggest_sig}px   "
      f"elongated stroke-like components: {elong}")

# viz 1: crop with bbox + eroded-inside outline
crop = img[max(0, y - 60):y + h + 60, max(0, x - 60):x + w + 60].copy()
oy, ox = max(0, y - 60), max(0, x - 60)
cv2.rectangle(crop, (x - ox, y - oy), (x + w - ox, y + h - oy),
              (0, 0, 255), 3)
contours, _ = cv2.findContours(inside.astype(np.uint8),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(crop, [c - np.array([ox, oy]) for c in contours],
                 -1, (255, 0, 0), 2)
cv2.imwrite(os.path.join(OUT, "17-block-roi.png"), crop)
# viz 2: amplified high-pass of the block interior only
amp = np.zeros_like(L)
amp[inside] = np.clip(hp[inside] * 8 + 128, 0, 255)
viz2 = amp[max(0, y - 40):y + h + 40, max(0, x - 40):x + w + 40]
cv2.imwrite(os.path.join(OUT, "17-block-inside-hp8x.png"),
            viz2.astype(np.uint8))
print("wrote 17-block-roi.png, 17-block-inside-hp8x.png")

print()
print("=" * 60)
print("PART B — letter 40 p2: green note vs graphite note vs paper")
print("=" * 60)
img2 = load("40-2.png")
H2, W2 = img2.shape[:2]
hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
Hh, Ss, Vv = hsv2[:, :, 0], hsv2[:, :, 1], hsv2[:, :, 2]
L2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)
bot = np.zeros_like(Hh)
bot[int(H2 * 0.55):, :] = 1
green = (bot > 0) & (Hh >= 35) & (Hh <= 85) & (Ss > 25) & (Vv > 80) & (Vv < 230)
# graphite: low saturation, mid-dark, bottom-right corner
corner = np.zeros_like(Hh)
corner[int(H2 * 0.62):, int(W2 * 0.45):] = 1
graph = (corner > 0) & (Ss < 70) & (Vv > 70) & (Vv < 175)
paper2 = (Vv > 200) & (Ss < 40)
# local paper near the green note for contrast reference
gx = np.where(green)[1]
gy = np.where(green)[0]
print(f"green-note px: {green.sum()}  x[{gx.min()}-{gx.max()}] "
      f"y[{gy.min()}-{gy.max()}]")
print(f"graphite-note px: {graph.sum()}   paper px: {paper2.sum()}")
for name, m in [("green wax?", green), ("graphite", graph),
                ("paper", paper2)]:
    bgr = img2[m].mean(axis=0)
    print(f"{name:9s} n={m.sum():6d}  meanBGR=({bgr[0]:.0f},{bgr[1]:.0f},"
          f"{bgr[2]:.0f})  meanL={L2[m].mean():.1f}  "
          f"hue~{Hh[m].mean():.0f} sat~{Ss[m].mean():.0f}")
# Weber contrast of each medium against nearby paper
loc = np.zeros_like(Hh)
loc[max(0, gy.min() - 80):gy.max() + 80,
    max(0, gx.min() - 80):gx.max() + 80] = 1
local_paper = (loc > 0) & (Vv > 200) & (Ss < 40)
Lp = L2[local_paper].mean()
for name, m in [("green", green), ("graphite", graph)]:
    c = (Lp - L2[m].mean()) / Lp
    print(f"Weber contrast vs local paper — {name}: {c:.3f}")
print("done")
