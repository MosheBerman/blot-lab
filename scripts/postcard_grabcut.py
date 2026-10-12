#!/usr/bin/env python3
"""Overwrite-separation (A2 parametric gate + GrabCut) on the intentional
postcard redactions, with sensitivity sweeps over gate thresholds and
GrabCut seed strictness.

Targets:
  scan17  - black ink block (allpdfs/17.pdf p1)
  scan51  - blue ink dabs, same hue as writing (allpdfs/51.pdf), 3 crops

Nothing is committed; all output lands under img/passes/postcards/*/grabcut/.
"""
import numpy as np, cv2, json
from PIL import Image
import os

WS = os.path.expanduser('~/workspace/blot-lab')

TARGETS = {
    'scan17': {
        'crop': 'img/passes/postcards/scan17/source-crop.png',
        'out':  'img/passes/postcards/scan17/grabcut',
        'kind': 'black',
    },
    'scan51-blob': {
        'crop': 'img/passes/postcards/scan51/source-crop-blob.png',
        'out':  'img/passes/postcards/scan51/grabcut/blob',
        'kind': 'blue',
    },
    'scan51-left': {
        'crop': 'img/passes/postcards/scan51/source-crop-left.png',
        'out':  'img/passes/postcards/scan51/grabcut/left',
        'kind': 'blue',
    },
    'scan51-right': {
        'crop': 'img/passes/postcards/scan51/source-crop-right.png',
        'out':  'img/passes/postcards/scan51/grabcut/right',
        'kind': 'blue',
    },
}

# A2 sweep grids. Blue dabs: overwrite = (L < Lt) & (S > St), exactly the
# Berliner form. Black block: covering ink is dark AND desaturated, so the
# adapted form is overwrite = (V < Vt) & (S < St).
A2_BLUE_L = [80, 100, 120, 140]
A2_BLUE_S = [100, 150, 200]
A2_BLACK_V = [80, 100, 120, 140]
A2_BLACK_S = [60, 100, 140]


def load(path):
    return np.array(Image.open(os.path.join(WS, path)).convert('RGB'))


def viz_kept(rgb, ink, kept, outpath):
    kept = kept.astype(bool)
    viz = rgb.copy()
    viz[ink & ~kept] = [255, 255, 255]   # removed -> paper white
    Image.fromarray(viz).save(outpath)


def viz_removed(rgb, ink, kept, outpath):
    kept = kept.astype(bool)
    rm = np.zeros(rgb.shape[:2] + (3,), np.uint8) + 255
    rm[kept] = rgb[kept]
    rm[ink & ~kept] = [255, 0, 0]
    Image.fromarray(rm).save(outpath)


def label_tile(tile, text):
    t = tile.copy()
    cv2.putText(t, text, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    cv2.putText(t, text, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1)
    return t


def montage(tiles, cols):
    rows = (len(tiles) + cols - 1) // cols
    h, w = tiles[0].shape[:2]
    canvas = np.zeros((rows * h, cols * w, 3), np.uint8)
    for i, t in enumerate(tiles):
        r, c = divmod(i, cols)
        canvas[r * h:(r + 1) * h, c * w:(c + 1) * w] = t
    return canvas


def run_grabcut(rgb, ink, sure_bg, sure_fg, iters=5):
    h, w = rgb.shape[:2]
    mask = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
    mask[ink] = cv2.GC_PR_FGD
    mask[sure_fg] = cv2.GC_FGD
    mask[sure_bg] = cv2.GC_BGD
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(rgb, mask, None, bgd, fgd, iters, cv2.GC_INIT_WITH_MASK)
    return ink & np.isin(mask, [cv2.GC_FGD, cv2.GC_PR_FGD])


def blob_bbox(blob):
    n, lab, stats, _ = cv2.connectedComponentsWithStats(blob.astype(np.uint8), 8)
    if n <= 1:
        return None
    big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    x, y, ww, hh, _ = stats[big]
    return (slice(y, y + hh), slice(x, x + ww))


def score(name, rgb, ink, kept, blob_ref, write_ref, bbox, outdir):
    kept = kept.astype(bool)
    removed = ink & ~kept
    blob_recall = float((removed & blob_ref).sum() / max(blob_ref.sum(), 1))
    write_keep = float((kept & write_ref).sum() / max(write_ref.sum(), 1))
    # key diagnostic: writing-like pixels INSIDE the block bbox
    in_bbox_write = 0
    if bbox is not None:
        ry, rx = bbox
        region = np.zeros_like(ink)
        region[ry, rx] = True
        in_bbox_write = int((kept & write_ref & region).sum())
        in_bbox_ink = int((ink & region).sum())
    else:
        in_bbox_ink = 0
    rec = dict(blob_recall=blob_recall, write_keep=write_keep,
               in_bbox_write_px=in_bbox_write, in_bbox_ink_px=in_bbox_ink,
               kept_px=int(kept.sum()))
    print(f'  {name:32s} blob_removed={blob_recall:.3f} writing_kept={write_keep:.3f} '
          f'bbox_write_kept={in_bbox_write}')
    return rec


def process_black(name, cfg):
    outdir = os.path.join(WS, cfg['out'])
    os.makedirs(outdir, exist_ok=True)
    rgb = load(cfg['crop'])
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    L = lab[:, :, 0]

    ink = V < 110                       # dark-ink gate (blackblock_isolate)
    blob_ref = ink & (V < 70)           # unambiguous black block ink
    bbox = blob_bbox(blob_ref)
    region = np.zeros_like(ink)
    if bbox is not None:
        region[bbox[0], bbox[1]] = True
    write_ref = ink & (S > 100) & (V >= 95) & (V <= 200) & ~region  # visible blue writing outside block
    write_like = ink & (S > 100) & (V >= 95) & (V <= 200)           # anywhere, for bbox diagnostic
    print(f'{name}: ink={ink.sum()} blob_ref={blob_ref.sum()} write_ref={write_ref.sum()}')

    scores = {}

    # ---- main A2 (mid): overwrite = (V<100) & (S<100) ----
    ow_main = ink & (V < 100) & (S < 100)
    kept_a2 = ink & ~ow_main
    viz_kept(rgb, ink, kept_a2, f'{outdir}/a2_main_kept.png')
    viz_removed(rgb, ink, kept_a2, f'{outdir}/a2_main_removedred.png')
    scores['a2_main'] = score('a2_main', rgb, ink, kept_a2, blob_ref, write_ref, bbox, outdir)

    # ---- main GrabCut (mid strictness) ----
    sure_bg = ink & (V < 70)
    sure_fg = ink & (S > 100) & (V >= 100)
    kept_gc = run_grabcut(rgb, ink, sure_bg, sure_fg)
    viz_kept(rgb, ink, kept_gc, f'{outdir}/grabcut_main_kept.png')
    viz_removed(rgb, ink, kept_gc, f'{outdir}/grabcut_main_removedred.png')
    scores['grabcut_main'] = score('grabcut_main', rgb, ink, kept_gc, blob_ref, write_ref, bbox, outdir)

    # ---- A2 sensitivity sweep: 4x3 ----
    tiles, sweep_scores = [], {}
    for vt in A2_BLACK_V:
        for st in A2_BLACK_S:
            ow = ink & (V < vt) & (S < st)
            kept = ink & ~ow
            tile = rgb.copy()
            tile[ink & ~kept] = [255, 255, 255]
            tile = cv2.resize(tile, (260, int(260 * rgb.shape[0] / rgb.shape[1])))
            tiles.append(label_tile(tile, f'V<{vt} S<{st}'))
            sweep_scores[f'V{vt}_S{st}'] = score(f'a2_V{vt}_S{st}', rgb, ink, kept,
                                                 blob_ref, write_ref, bbox, outdir)
    Image.fromarray(montage(tiles, 4)).save(f'{outdir}/a2_sweep_montage.png')
    print(f'  wrote a2_sweep_montage.png')

    # ---- GrabCut strictness sweep: 3 levels ----
    strictness = {
        'strict': dict(bg=(V < 50), fg=ink & (S > 120) & (V >= 110)),
        'mid':    dict(bg=(V < 70), fg=ink & (S > 100) & (V >= 100)),
        'loose':  dict(bg=(V < 90), fg=ink & (S > 80) & (V >= 90)),
    }
    gtiles, gsweep = [], {}
    for lvl, s in strictness.items():
        kept = run_grabcut(rgb, ink, ink & s['bg'], s['fg'])
        viz_kept(rgb, ink, kept, f'{outdir}/grabcut_{lvl}_kept.png')
        tile = cv2.resize(rgb.copy(), (260, int(260 * rgb.shape[0] / rgb.shape[1])))
        tmp = rgb.copy(); tmp[ink & ~kept] = [255, 255, 255]
        tile = cv2.resize(tmp, (260, int(260 * rgb.shape[0] / rgb.shape[1])))
        gtiles.append(label_tile(tile, f'grabcut {lvl}'))
        gsweep[lvl] = score(f'grabcut_{lvl}', rgb, ink, kept, blob_ref, write_ref, bbox, outdir)
    Image.fromarray(montage(gtiles, 3)).save(f'{outdir}/grabcut_sweep_montage.png')
    print(f'  wrote grabcut_sweep_montage.png')

    # baseline: writing-like pixels inside bbox with no separation at all
    base = int((write_like & region).sum()) if bbox is not None else 0
    scores['baseline'] = dict(in_bbox_write_like_px=base)
    scores['a2_sweep'] = sweep_scores
    scores['grabcut_sweep'] = gsweep
    with open(f'{outdir}/scores.json', 'w') as f:
        json.dump(scores, f, indent=1)
    return scores


def process_blue(name, cfg):
    outdir = os.path.join(WS, cfg['out'])
    os.makedirs(outdir, exist_ok=True)
    rgb = load(cfg['crop'])
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    L = lab[:, :, 0]

    ink = (H > 85) & (H < 135) & (S > 40) & (V < 200)
    blob_ref = ink & (L < 100) & (S > 150)     # dab cores
    bbox = blob_bbox(blob_ref)
    region = np.zeros_like(ink)
    if bbox is not None:
        region[bbox[0], bbox[1]] = True
    write_ref = ink & (L >= 105) & (L <= 165) & ~region
    write_like = ink & (L >= 105) & (L <= 165)
    print(f'{name}: ink={ink.sum()} blob_ref={blob_ref.sum()} write_ref={write_ref.sum()}')

    scores = {}

    # ---- main A2 (Berliner params): (L<100) & (S>150) ----
    ow_main = ink & (L < 100) & (S > 150)
    kept_a2 = ink & ~ow_main
    viz_kept(rgb, ink, kept_a2, f'{outdir}/a2_main_kept.png')
    viz_removed(rgb, ink, kept_a2, f'{outdir}/a2_main_removedred.png')
    scores['a2_main'] = score('a2_main', rgb, ink, kept_a2, blob_ref, write_ref, bbox, outdir)

    # ---- main GrabCut (mid strictness) ----
    sure_bg = ink & (L < 100) & (S > 150)
    sure_fg = ink & (L >= 105) & (L <= 180)
    kept_gc = run_grabcut(rgb, ink, sure_bg, sure_fg)
    viz_kept(rgb, ink, kept_gc, f'{outdir}/grabcut_main_kept.png')
    viz_removed(rgb, ink, kept_gc, f'{outdir}/grabcut_main_removedred.png')
    scores['grabcut_main'] = score('grabcut_main', rgb, ink, kept_gc, blob_ref, write_ref, bbox, outdir)

    # ---- A2 sensitivity sweep: 4x3, Berliner form ----
    tiles, sweep_scores = [], {}
    for lt in A2_BLUE_L:
        for st in A2_BLUE_S:
            ow = ink & (L < lt) & (S > st)
            kept = ink & ~ow
            tmp = rgb.copy(); tmp[ink & ~kept] = [255, 255, 255]
            tile = cv2.resize(tmp, (260, int(260 * rgb.shape[0] / rgb.shape[1])))
            tiles.append(label_tile(tile, f'L<{lt} S>{st}'))
            sweep_scores[f'L{lt}_S{st}'] = score(f'a2_L{lt}_S{st}', rgb, ink, kept,
                                                blob_ref, write_ref, bbox, outdir)
    Image.fromarray(montage(tiles, 4)).save(f'{outdir}/a2_sweep_montage.png')
    print(f'  wrote a2_sweep_montage.png')

    # ---- GrabCut strictness sweep: 3 levels ----
    strictness = {
        'strict': dict(bg=(L < 85) & (S > 175),  fg=ink & (L >= 120) & (L <= 170)),
        'mid':    dict(bg=(L < 100) & (S > 150), fg=ink & (L >= 105) & (L <= 180)),
        'loose':  dict(bg=(L < 115) & (S > 125), fg=ink & (L >= 90) & (L <= 200)),
    }
    gtiles, gsweep = [], {}
    for lvl, s in strictness.items():
        kept = run_grabcut(rgb, ink, ink & s['bg'], s['fg'])
        viz_kept(rgb, ink, kept, f'{outdir}/grabcut_{lvl}_kept.png')
        tmp = rgb.copy(); tmp[ink & ~kept] = [255, 255, 255]
        tile = cv2.resize(tmp, (260, int(260 * rgb.shape[0] / rgb.shape[1])))
        gtiles.append(label_tile(tile, f'grabcut {lvl}'))
        gsweep[lvl] = score(f'grabcut_{lvl}', rgb, ink, kept, blob_ref, write_ref, bbox, outdir)
    Image.fromarray(montage(gtiles, 3)).save(f'{outdir}/grabcut_sweep_montage.png')
    print(f'  wrote grabcut_sweep_montage.png')

    base = int((write_like & region).sum()) if bbox is not None else 0
    scores['baseline'] = dict(in_bbox_write_like_px=base)
    scores['a2_sweep'] = sweep_scores
    scores['grabcut_sweep'] = gsweep
    with open(f'{outdir}/scores.json', 'w') as f:
        json.dump(scores, f, indent=1)
    return scores


all_scores = {}
for name, cfg in TARGETS.items():
    print('=====', name)
    if cfg['kind'] == 'black':
        all_scores[name] = process_black(name, cfg)
    else:
        all_scores[name] = process_blue(name, cfg)

with open(os.path.join(WS, 'img/passes/postcards/scan51/grabcut/sweep_summary.json'), 'w') as f:
    json.dump(all_scores, f, indent=1)
print('done')
