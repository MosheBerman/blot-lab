#!/usr/bin/env python3
"""Annotate scan 17: top = full original with red bbox (region analyzed by
every method); bottom = 2x zoom of that region with numbered yellow markers
for the 12 interior candidate locations tested by block17_template_match.py
(coords from its 2026-10-13 run)."""
import cv2
import numpy as np

BASE = "/home/hatch/workspace/goals/the-coded-letters/hidden_files/drive/sweep/pages"
OUT = "/home/hatch/workspace/goals/blot-lab-letter-forensics/files"

CANDS = [(203.5, 1136.1), (215.4, 1144.9), (501.9, 1137.2), (423.5, 1109.0),
         (519.8, 1138.8), (506.9, 1145.3), (540.1, 1127.1), (540.1, 1117.1),
         (486.4, 1114.5), (534.5, 1135.9), (552.2, 1111.4), (527.7, 1122.0)]
X0, Y0, X1, Y1 = 108, 987, 558, 1200  # analyzed block bbox

img = cv2.imread(f"{BASE}/17-1.png")
top = img.copy()
cv2.rectangle(top, (X0, Y0), (X1, Y1), (0, 0, 255), 4)

zx0, zy0, zx1, zy1 = X0 - 30, Y0 - 40, X1 + 30, Y1 + 30
zoom = cv2.resize(img[zy0:zy1, zx0:zx1], None, fx=2, fy=2,
                   interpolation=cv2.INTER_CUBIC)
cv2.rectangle(zoom, ((X0 - zx0) * 2, (Y0 - zy0) * 2),
              ((X1 - zx0) * 2, (Y1 - zy0) * 2), (0, 0, 255), 3)
W = 1275
ZH, ZW = zoom.shape[:2]
strip = np.full((ZH, W - ZW, 3), 20, np.uint8)
zpanel = np.hstack([zoom, strip])
order = sorted(range(len(CANDS)), key=lambda i: CANDS[i][1])
slot = {orig: rank for rank, orig in enumerate(order)}
for i, (cx, cy) in enumerate(CANDS):
    px, py = int(round((cx - zx0) * 2)), int(round((cy - zy0) * 2))
    cv2.circle(zpanel, (px, py), 26, (0, 255, 255), 4)
    cv2.circle(zpanel, (px, py), 26, (0, 0, 0), 1)
    ly = 40 + slot[i] * 42
    lx = ZW + 60
    cv2.line(zpanel, (px + 26, py), (lx - 44, ly), (0, 255, 255), 2)
    t = f"c{i:02d}"
    cv2.putText(zpanel, t, (lx - 40, ly + 12),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 5)
    cv2.putText(zpanel, t, (lx - 40, ly + 12),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

canvas = np.full((top.shape[0] + zpanel.shape[0] + 12, W, 3), 20, np.uint8)
canvas[:top.shape[0], :top.shape[1]] = top
canvas[top.shape[0] + 12:, :] = zpanel
cv2.imwrite(f"{OUT}/17-block-candidates-on-original.png", canvas)
print("wrote 17-block-candidates-on-original.png")
