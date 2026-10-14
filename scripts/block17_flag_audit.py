#!/usr/bin/env python3
"""Audit Moshe's flags on the scan-17 block (hi-res source 17pdf-000.jpg).
1. Mask audit: strict interior vs generous mask; letter-ink fraction and
   elongation on the excluded ring (did the mask hide block pixels?).
2. Bottom-left boundary zone: letter-ink fraction profile across the edge
   where the block meets visible strokes (overlap vs under-text).
3. Mid-left-band zone: fine-grained scan for small surviving letterforms.
4. Full interior fine scan: lower size floors + loop detection, with a
   printed-ink (postmark) control for the false-positive rate.
5. Texture (fiber idea): paper texture correlation length vs physical fiber
   size; high-pass residual structure inside block vs blank paper.
"""
import cv2
import numpy as np
import os

SRC = "/home/hatch/workspace/blot-lab/img/source/17pdf-000.jpg"
OUT = "/home/hatch/workspace/goals/blot-lab-letter-forensics/files"
PX_UM = 25400 / 281.0  # ~90.4 um/px at 281 ppi

img = cv2.imread(SRC)
H, W = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
S, V = hsv[:, :, 1].astype(np.float32), hsv[:, :, 2].astype(np.float32)
L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)
srgb = img[:, :, ::-1].astype(np.float32) / 255.0
lin = np.where(srgb <= 0.04045, srgb / 12.92,
               ((srgb + 0.055) / 1.055) ** 2.4)

black = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 95]))
quad = np.zeros_like(black)
quad[int(H * 0.55):, :int(W * 0.45)] = 255
cand = cv2.bitwise_and(black, quad)
n, labm, stats, _ = cv2.connectedComponentsWithStats(cand, 8)
order = np.argsort(-stats[1:, cv2.CC_STAT_AREA])
comp = np.isin(labm, [int(o) + 1 for o in order[:2]])
strict = cv2.erode(comp.astype(np.uint8),
                   np.ones((15, 15), np.uint8)).astype(bool)
generous = cv2.dilate(comp.astype(np.uint8),
                      np.ones((21, 21), np.uint8)).astype(bool)
ring = generous & ~strict
print(f"[mask] strict {strict.sum()} px, generous {generous.sum()} px, "
      f"ring {ring.sum()} px ({ring.sum()/generous.sum():.1%} excluded)")

msg = np.zeros_like(black)
msg[int(H * 0.05):int(H * 0.6), 0:int(W * 0.5)] = 255
letter_ink = (cv2.inRange(hsv, np.array([0, 30, 0]),
                          np.array([180, 255, 150])) > 0) & (msg > 0)
letter_ink = cv2.erode(letter_ink.astype(np.uint8),
                       np.ones((3, 3), np.uint8)).astype(bool)
paper = (V > 200) & (S < 40)
e_paper = lin[paper].mean(axis=0)
e_top = lin[comp].mean(axis=0)
e_let = lin[letter_ink].mean(axis=0)
E = np.stack([e_paper, e_top, e_let], axis=1)
A = np.linalg.pinv(E.T)


def letter_frac(mask):
    X = lin[mask].reshape(-1, 3)
    F = (A @ X.T).T
    F = np.clip(F, 0, None)
    F /= F.sum(axis=1, keepdims=True) + 1e-12
    return F[:, 2]


fr = letter_frac(ring)
fi = letter_frac(strict)
print(f"[ring] letter-frac mean {fr.mean():.4f} std {fr.std():.4f} "
      f"max {fr.max():.4f} | interior mean {fi.mean():.4f}")


def struct_report(frac_full, mask, tag, area_min=12, len_min=15,
                  aspect_min=2.0):
    m = ((frac_full > 0.12) & mask).astype(np.uint8)
    nn, ll, ss, _ = cv2.connectedComponentsWithStats(m, 8)
    elong, loops, items = 0, 0, []
    for j in range(1, nn):
        area = ss[j, cv2.CC_STAT_AREA]
        if area < area_min:
            continue
        wpx, hpx = ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT]
        big, sml = max(wpx, hpx), max(1, min(wpx, hpx))
        # holes via fill-minus-original
        cj = (ll == j).astype(np.uint8) * 255
        ff = cj.copy()
        ffm = np.zeros((cj.shape[0] + 2, cj.shape[1] + 2), np.uint8)
        cv2.floodFill(ff, ffm, (0, 0), 128)
        holes = int((ff == 0).sum())
        is_el = (big / sml > aspect_min and big > len_min)
        is_loop = holes >= 8 and area <= 900
        elong += is_el
        loops += is_loop
        if is_el or is_loop:
            items.append((ss[j, cv2.CC_STAT_LEFT], ss[j, cv2.CC_STAT_TOP],
                          wpx, hpx, area, holes))
    print(f"[{tag}] comps>=12px: "
          f"{sum(1 for j in range(1, nn) if ss[j, cv2.CC_STAT_AREA] >= area_min)}, "
          f"elongated: {elong}, loops: {loops}")
    for it in items[:12]:
        print(f"    x={it[0]} y={it[1]} {it[2]}x{it[3]} area={it[4]} "
              f"holes={it[5]}")
    return m


full_frac = np.zeros((H, W), np.float32)
full_frac[generous] = letter_frac(generous)
print("[ring] fine structure (area>=12):")
struct_report(full_frac, ring, "ring")

# bottom-left boundary zone
bl = np.zeros((H, W), bool)
bl[1280:1450, 80:320] = True
blz = bl & generous
frz = letter_frac(blz)
print(f"[bottom-left] letter-frac mean {frz.mean():.4f} "
      f"max {frz.max():.4f} (n={blz.sum()})")
# row profile: where does the fraction concentrate?
prof = []
for yy in range(1280, 1450, 10):
    band = np.zeros((H, W), bool)
    band[yy:yy + 10, :] = blz[yy:yy + 10, :]
    if band.sum():
        prof.append((yy, letter_frac(band).mean()))
prof = np.array(prof)
pk = prof[np.argmax(prof[:, 1])]
print(f"[bottom-left] peak mean frac {pk[1]:.4f} at y~{int(pk[0])}")

# mid-left-band zone
mid = np.zeros((H, W), bool)
mid[1080:1360, 280:620] = True
midz = mid & generous
print("[mid-band] fine structure (area>=12):")
struct_report(full_frac, midz, "mid-band")

# full interior fine scan + postmark control
print("[interior] fine structure (area>=12):")
struct_report(full_frac, strict, "interior")
pm = np.zeros((H, W), bool)
pm[1080:1380, 1080:1420] = True  # postmark circle strokes
print("[postmark-control] fine structure (area>=12):")
struct_report(full_frac, pm, "postmark")

# ---- texture / fiber ----
blank = np.zeros((H, W), bool)
blank[150:400, 100:500] = True
Lb = L[150:400, 100:500].astype(np.float32)
Lb -= Lb.mean()
ac = np.fft.ifft2(np.abs(np.fft.fft2(Lb, s=(512, 512))) ** 2).real
ac /= ac[0, 0]
# radial profile
yy, xx = np.mgrid[0:512, 0:512]
r = np.sqrt(((yy - 256)) ** 2 + ((xx - 256)) ** 2).astype(int)
rad = np.bincount(r.ravel(), weights=ac.ravel()) / np.bincount(r.ravel())
cl = np.argmax(rad < 1 / np.e)
print(f"[texture] paper correlation length ~{cl}px "
      f"(~{cl * PX_UM:.0f} um); 1px = {PX_UM:.0f} um; "
      f"fibers 10-30um are sub-pixel")
# high-pass residual structure: block interior vs blank paper
Lhp = L - cv2.medianBlur(L.astype(np.uint8), 51).astype(np.float32)
sig = Lhp[blank].std()
resid = np.zeros((H, W), np.float32)
resid[strict] = np.abs(Lhp[strict])
mm = ((resid > 3 * sig) & strict).astype(np.uint8)
nn, _, ss, _ = cv2.connectedComponentsWithStats(mm, 8)
el = sum(1 for j in range(1, nn)
         if ss[j, cv2.CC_STAT_AREA] >= 12
         and max(ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT])
         / max(1, min(ss[j, cv2.CC_STAT_WIDTH], ss[j, cv2.CC_STAT_HEIGHT])) > 2.0)
print(f"[texture] interior |HP|>3sig: {nn-1} comps>=1px, "
      f"{sum(1 for j in range(1,nn) if ss[j,cv2.CC_STAT_AREA]>=12)} >=12px, "
      f"elongated {el}; paper sig={sig:.2f}L, "
      f"interior HP std={Lhp[strict].std():.2f}")
mm2 = ((np.abs(Lhp) > 3 * sig) & blank).astype(np.uint8)
nn2, _, ss2, _ = cv2.connectedComponentsWithStats(mm2, 8)
print(f"[texture] blank paper |HP|>3sig: {nn2-1} comps "
      f"({blank.sum()} px area) vs interior ({strict.sum()} px)")

# ---- visuals ----
def crop_viz(x0, y0, x1, y1, name):
    rgb = img[y0:y1, x0:x1]
    ov = rgb.copy()
    m = ring[y0:y1, x0:x1]
    ov[m] = (0, 0, 255)
    both = np.hstack([rgb, cv2.addWeighted(rgb, 0.55, ov, 0.45, 0)])
    both = cv2.resize(both, None, fx=2, fy=2,
                      interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(f"{OUT}/{name}", both)

crop_viz(60, 1260, 340, 1470, "17-flag-bottomleft.png")
crop_viz(260, 1060, 640, 1380, "17-flag-midband.png")
print("done")
