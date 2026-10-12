#!/usr/bin/env python3
"""Berliner baseline: overwrite-separation algorithms on letter 45.

Ground truth: the overwritten word is "Berliner" (read 2026-10-07).
Goal: isolate underlying letterforms from the overwriting scribble/strike.
Four approaches, scored against color-based reference masks.
"""
import numpy as np, cv2, json
from PIL import Image
import os

OUT = os.path.expanduser('~/workspace/blot-lab/img/passes/berliner-baseline')
os.makedirs(OUT, exist_ok=True)

im = np.array(Image.open(os.path.expanduser('~/workspace/blot-lab/img/blot45.jpg')).convert('RGB'))
hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV).astype(np.float32)
lab = cv2.cvtColor(im, cv2.COLOR_RGB2LAB).astype(np.float32)
H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
L = lab[:, :, 0]

# ROI around "Berliner"
ry, rx = slice(140, 250), slice(30, 330)
roi_rgb = im[ry, rx]
rh, rw = roi_rgb.shape[:2]

ink = ((H[ry, rx] > 85) & (H[ry, rx] < 135) & (S[ry, rx] > 40) & (V[ry, rx] < 200))
Lr, Sr = L[ry, rx], S[ry, rx]

# ---- reference masks (independent parametric gates) ----
blob_ref = ink & (Lr < 90)            # unambiguous overwrite core
write_ref = ink & (Lr >= 105) & (Lr <= 165)  # unambiguous underlying writing
print(f'ink px={ink.sum()} blob_ref={blob_ref.sum()} write_ref={write_ref.sum()}')

results = {}

def score(name, kept):
    kept = kept.astype(bool)
    removed = ink & ~kept
    blob_recall = (removed & blob_ref).sum() / max(blob_ref.sum(), 1)
    write_keep = (kept & write_ref).sum() / max(write_ref.sum(), 1)
    # fragmentation: components of kept ink in word band
    n, _ = cv2.connectedComponents(kept.astype(np.uint8), 8)
    results[name] = dict(blob_recall=float(blob_recall), write_keep=float(write_keep),
                         kept_components=int(n - 1))
    print(f'{name:28s} blob_removed={blob_recall:.3f} writing_kept={write_keep:.3f} comps={n-1}')
    return kept

def save_viz(name, kept):
    kept = kept.astype(bool)
    viz = roi_rgb.copy()
    viz[ink & ~kept] = [255, 255, 255]          # removed -> paper white
    viz[~ink] = roi_rgb[~ink]
    Image.fromarray(viz).save(f'{OUT}/{name}.png')
    # removed-mask view
    rm = np.zeros((rh, rw, 3), np.uint8) + 255
    rm[kept] = roi_rgb[kept]
    rm[ink & ~kept] = [255, 0, 0]
    Image.fromarray(rm).save(f'{OUT}/{name}_removedred.png')

# ============ A1: k-means on (L, S) ============
feat = np.stack([Lr[ink] / 255.0, Sr[ink] / 255.0], axis=1).astype(np.float32)
crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1e-4)
_, labels, centers = cv2.kmeans(feat, 2, None, crit, 8, cv2.KMEANS_PP_CENTERS)
dark_cluster = int(np.argmin(centers[:, 0]))   # lower L = overwrite
print('kmeans centers (L,S):', (centers * 255).round(1).tolist(), 'dark cluster =', dark_cluster)
lab_full = np.zeros((rh, rw), np.int32) - 1
lab_full[ink] = labels.flatten()
kept_a1 = ink & (lab_full != dark_cluster)
score('A1_kmeans_LS', kept_a1); save_viz('A1_kmeans_kept', kept_a1)

# ============ A2: parametric gate ============
overwrite_a2 = ink & (Lr < 100) & (Sr > 150)
kept_a2 = ink & ~overwrite_a2
score('A2_parametric_L100_S150', kept_a2); save_viz('A2_parametric_kept', kept_a2)

# ============ B: stroke-continuity seeded growth ============
dist = cv2.distanceTransform(ink.astype(np.uint8), cv2.DIST_L2, 3)
seeds = write_ref.copy()
allowed = ink & (Lr >= 100) & (dist <= 6.0)
# BFS flood from seeds through allowed
grown = seeds.copy()
frontier = list(zip(*np.nonzero(seeds)))
from collections import deque
q = deque(frontier)
seen = seeds.copy()
while q:
    y, x = q.popleft()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny, nx = y + dy, x + dx
            if 0 <= ny < rh and 0 <= nx < rw and not seen[ny, nx] and allowed[ny, nx]:
                seen[ny, nx] = True
                grown[ny, nx] = True
                q.append((ny, nx))
score('B_seeded_growth', grown); save_viz('B_seeded_growth_kept', grown)

# ============ C: GrabCut ============
mask = np.full((rh, rw), cv2.GC_PR_BGD, np.uint8)
mask[ink] = cv2.GC_PR_FGD
mask[write_ref] = cv2.GC_FGD
mask[ink & (Lr < 85)] = cv2.GC_BGD
bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
cv2.grabCut(roi_rgb, mask, None, bgd, fgd, 5, cv2.GC_INIT_WITH_MASK)
kept_c = ink & np.isin(mask, [cv2.GC_FGD, cv2.GC_PR_FGD])
score('C_grabcut', kept_c); save_viz('C_grabcut_kept', kept_c)

# ============ D1: white top-hat (thin structures survive) ============
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))  # r=6
opened = cv2.morphologyEx(ink.astype(np.uint8), cv2.MORPH_OPEN, kernel)
kept_d1 = (ink.astype(np.uint8) - opened).astype(bool)
score('D1_tophat_r6', kept_d1); save_viz('D1_tophat_kept', kept_d1)

# ============ D2: opening-based blob mask subtraction ============
blob_est = opened.astype(bool)
kept_d2 = ink & ~blob_est
score('D2_opening_subtract', kept_d2); save_viz('D2_opening_kept', kept_d2)

with open(f'{OUT}/scores.json', 'w') as f:
    json.dump(results, f, indent=1)

# ---- comparison panel ----
names = ['A1_kmeans_kept', 'A2_parametric_kept', 'B_seeded_growth_kept',
         'C_grabcut_kept', 'D1_tophat_kept', 'D2_opening_kept']
tiles = [np.array(Image.open(f'{OUT}/{n}.png').resize((rw * 2, rh * 2), Image.NEAREST)) for n in names]
labels_row = ['A1 kmeans', 'A2 parametric', 'B seeded growth', 'C grabcut', 'D1 tophat', 'D2 opening-sub']
panel = np.vstack(tiles)
Image.fromarray(panel).save(f'{OUT}/comparison_panel.png')
print('wrote', f'{OUT}/comparison_panel.png')
print(json.dumps(results, indent=1))
