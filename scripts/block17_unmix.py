#!/usr/bin/env python3
"""Exercise the ink difference properly (hi-res source):
1. PCA of interior pixel colors: is the variation 1-D (paper<->top-ink
   thickness) or is there a second axis pointing at the letter ink?
2. Two/three-endmember linear unmixing (paper, top ink, letter ink) in
   linear RGB -> per-pixel letter-ink fraction map -> elongation test.
3. Repeat restricted to the thinnest-ink decile (highest L), where
   show-through is physically most plausible.
"""
import cv2
import numpy as np
import os

SRC = "/home/hatch/workspace/blot-lab/img/source/17pdf-000.jpg"
OUT = "/home/hatch/workspace/goals/blot-lab-letter-forensics/files"

img = cv2.imread(SRC)
H, W = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
S, V = hsv[:, :, 1].astype(np.float32), hsv[:, :, 2].astype(np.float32)
L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)
srgb = img[:, :, ::-1].astype(np.float32) / 255.0
lin = np.where(srgb <= 0.04045, srgb / 12.92,
               ((srgb + 0.055) / 1.055) ** 2.4)  # linear RGB for mixing

black = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 95]))
quad = np.zeros_like(black)
quad[int(H * 0.55):, :int(W * 0.45)] = 255
cand = cv2.bitwise_and(black, quad)
n, labm, stats, _ = cv2.connectedComponentsWithStats(cand, 8)
order = np.argsort(-stats[1:, cv2.CC_STAT_AREA])
comp = np.isin(labm, [int(o) + 1 for o in order[:2]])
inside = cv2.erode(comp.astype(np.uint8),
                    np.ones((15, 15), np.uint8)).astype(bool)
inside = inside.astype(bool)

msg = np.zeros_like(black)
msg[int(H * 0.05):int(H * 0.6), 0:int(W * 0.5)] = 255
letter_ink = (cv2.inRange(hsv, np.array([0, 30, 0]),
                          np.array([180, 255, 150])) > 0) & (msg > 0)
letter_ink = cv2.erode(letter_ink.astype(np.uint8),
                       np.ones((3, 3), np.uint8)).astype(bool)
paper = (V > 200) & (S < 40)

e_paper = lin[paper].mean(axis=0)
e_top = lin[inside].mean(axis=0)
e_let = lin[letter_ink].mean(axis=0)
print("endmembers (linear RGB):")
print(f"  paper      {e_paper.round(4)}")
print(f"  top ink    {e_top.round(4)}")
print(f"  letter ink {e_let.round(4)}")

X = lin[inside].reshape(-1, 3)
Xc = X - X.mean(axis=0)
U, sv, Vt = np.linalg.svd(Xc, full_matrices=False)
var_exp = sv ** 2 / (sv ** 2).sum()
print(f"\n[PCA interior] variance explained: {var_exp.round(4)}")
d_let = e_let - e_top
d_let /= np.linalg.norm(d_let) + 1e-12
for k in range(3):
    cosang = abs(float(Vt[k] @ d_let))
    print(f"  PC{k+1}: |cos| with letter-ink direction = {cosang:.3f} "
          f"(var {var_exp[k]:.4f})")


def unmix(pixels, E):
    A = np.linalg.pinv(E.T)  # 3x3
    F = (A @ pixels.T).T
    F = np.clip(F, 0, None)
    F /= F.sum(axis=1, keepdims=True) + 1e-12
    return F


E = np.stack([e_paper, e_top, e_let], axis=1)  # 3x3 endmember matrix
F = unmix(X, E)
f_let = F[:, 2]
print(f"\n[unmix] letter-ink fraction: mean {f_let.mean():.4f} "
      f"std {f_let.std():.4f} max {f_let.max():.4f}")
print(f"  fraction of interior px with letter-frac > 0.15: "
      f"{(f_let > 0.15).mean():.4f}")
print(f"  fraction of interior px with letter-frac > 0.30: "
      f"{(f_let > 0.30).mean():.4f}")


def elong_test(fullmap, thresh, tag):
    m = (fullmap > thresh).astype(np.uint8)
    m[~inside] = 0
    nn, ll, ss, _ = cv2.connectedComponentsWithStats(m, 8)
    el = sum(1 for j in range(1, nn)
             if ss[j, cv2.CC_STAT_AREA] >= 40
             and max(ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT])
             / max(1, min(ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT])) > 2.5
             and max(ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT]) > 34)
    big = max([ss[j, cv2.CC_STAT_AREA] for j in range(1, nn)], default=0)
    print(f"  [{tag}] thr {thresh}: {nn-1} components, largest {big}px, "
          f"elongated: {el}")
    return m


print("[unmix] letter-fraction structure:")
full_frac = np.zeros(inside.shape, np.float32)
full_frac[inside] = f_let
m1 = elong_test(full_frac, 0.15, "frac>0.15")
m2 = elong_test(full_frac, 0.30, "frac>0.30")

# thinnest-ink decile
Li = L[inside]
cut = np.percentile(Li, 90)
thin = inside & (L >= cut)
print(f"\nthinnest decile: {thin.sum()} px (L >= {cut:.1f})")
Xt = lin[thin].reshape(-1, 3)
Ft = unmix(Xt, E)
print(f"[thin] letter-ink fraction: mean {Ft[:, 2].mean():.4f} "
      f"std {Ft[:, 2].std():.4f} max {Ft[:, 2].max():.4f}")
full = np.zeros(inside.shape, np.float32)
full[thin] = Ft[:, 2]
mt = (full > 0.15).astype(np.uint8)
mt[~thin] = 0
nn, ll, ss, _ = cv2.connectedComponentsWithStats(mt, 8)
el = sum(1 for j in range(1, nn)
         if ss[j, cv2.CC_STAT_AREA] >= 40
         and max(ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT])
         / max(1, min(ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT])) > 2.5
         and max(ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT]) > 34)
big = max([ss[j, cv2.CC_STAT_AREA] for j in range(1, nn)], default=0)
print(f"[thin] frac>0.15: {nn-1} components, largest {big}px, elongated: {el}")

# viz: letter-fraction map, interior only, exterior blocked out
ys, xs = np.where(comp)
x0, y0 = max(0, xs.min() - 80), max(0, ys.min() - 80)
x1, y1 = min(W, xs.max() + 80), min(H, ys.max() + 80)
fmap = full_frac[y0:y1, x0:x1]
viz = np.full((y1 - y0, x1 - x0, 3), 90, np.uint8)
cm = cv2.applyColorMap(
    np.clip(fmap / (fmap.max() + 1e-9) * 255, 0, 255).astype(np.uint8),
    cv2.COLORMAP_INFERNO)
viz[inside[y0:y1, x0:x1]] = cm[inside[y0:y1, x0:x1]]
cv2.imwrite(f"{OUT}/17-hires-unmix-frac.png", viz)
print("wrote 17-hires-unmix-frac.png")
print("done")
