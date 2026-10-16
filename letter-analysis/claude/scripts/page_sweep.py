"""Per-page image sweep for the letter analysis (Claude version).

For each page image:
  - word segmentation (ink mask -> horizontal closing -> components)
  - (ii) lighter-word test: each word's ink darkness vs. its line/neighbours (robust z)
  - (ii-b) different-ink test: each word's ink hue/chroma vs. the page's dominant ink
  - (iii) subtle marks: small isolated ink specks not part of any word, classified
          by position (below baseline / above word / in gap / margin) + bright pinhole-like specks
Writes flags JSON, an annotated overview and a contact sheet of the strongest flags.
Usage: python3 page_sweep.py <page.jpg> <outdir>
"""
import sys, json, os
import cv2, numpy as np

def robust_z(v, ref):
    med = np.median(ref); mad = np.median(np.abs(ref - med)) * 1.4826 + 1e-6
    return (v - med) / mad

def sweep(path, out):
    name = os.path.splitext(os.path.basename(path))[0]
    bgr = cv2.imread(path); H, W = bgr.shape[:2]
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    L = lab[..., 0].astype(np.float32); A = lab[..., 1].astype(np.float32) - 128; B = lab[..., 2].astype(np.float32) - 128
    k = int(max(31, (min(H, W) // 25) | 1))
    bg = cv2.medianBlur(lab[..., 0], k).astype(np.float32) + 1
    ratio = L / bg
    ink = None
    # edges of the photo (dark surround) excluded: keep only area where bg is paper-bright
    # paper mask: background colour close to the page's dominant paper colour (excludes scanner bed, stamps, labels)
    bga = cv2.medianBlur(lab[..., 1], k).astype(np.float32); bgb = cv2.medianBlur(lab[..., 2], k).astype(np.float32)
    samp = (bg > np.percentile(bg, 30)) & (bg < np.percentile(bg, 90))
    pL, pa0, pb0 = np.median(bg[samp]), np.median(bga[samp]), np.median(bgb[samp])
    paper = ((np.abs(bg - pL) < 28) & (np.hypot(bga - pa0, bgb - pb0) < 9)).astype(np.uint8)
    np_, pl_, ps_, _ = cv2.connectedComponentsWithStats(paper, 4)
    if np_ > 1: paper = (pl_ == 1 + np.argmax(ps_[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    paper = cv2.morphologyEx(paper, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))
    paper = cv2.erode(paper, np.ones((45, 45), np.uint8))
    if paper.mean() < 0.30:  # colour-based mask failed (e.g. strongly lit or white sheet): fall back to brightness
        paper = (bg > np.percentile(bg, 15) * 0.92).astype(np.uint8)
        paper = cv2.erode(paper, np.ones((45, 45), np.uint8))
    chrom = np.hypot(A - (pa0 - 128), B - (pb0 - 128))
    ink = ((ratio < 0.86) | ((chrom > 16) & (ratio < 0.97))).astype(np.uint8)
    ink = cv2.morphologyEx(ink, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    ink = ink & paper
    # stroke scale estimate from ink run lengths
    n, lab_cc, st, cen = cv2.connectedComponentsWithStats(ink, 8)
    hs = st[1:, cv2.CC_STAT_HEIGHT]; areas = st[1:, cv2.CC_STAT_AREA]
    xh = float(np.median(hs[(areas > 30)])) if np.any(areas > 30) else 20.0  # ~x-height
    # words
    kw = max(3, int(xh * 0.8))
    closed = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (kw, max(1, int(xh * 0.3)))))
    nw, wl, ws, wc = cv2.connectedComponentsWithStats(closed, 8)
    words = []
    for i in range(1, nw):
        x, y, w, h, a = ws[i]
        if a < xh * xh * 0.6 or w < xh * 0.8: continue
        m = (wl[y:y+h, x:x+w] == i) & (ink[y:y+h, x:x+w] > 0)
        if m.sum() < 15: continue
        dark = float((1 - ratio[y:y+h, x:x+w][m]).mean())
        core = float(np.percentile(1 - ratio[y:y+h, x:x+w][m], 90))
        ca = float(np.median(A[y:y+h, x:x+w][m])); cb = float(np.median(B[y:y+h, x:x+w][m]))
        words.append(dict(id=i, x=int(x), y=int(y), w=int(w), h=int(h), cy=float(y + h / 2), dark=dark, core=core, a=ca, b=cb, npx=int(m.sum())))
    flags = []
    # (ii) lighter / different-ink test on a grid of text cells (robust to word merging in dense cursive)
    cw, ch = int(xh * 3), int(xh * 1.2)
    cells = []
    for y0 in range(0, H - ch, ch):
        for x0 in range(0, W - cw, cw):
            m = ink[y0:y0+ch, x0:x0+cw] > 0
            if m.sum() < xh * 4: continue
            # skip cells touching the paper boundary (scanner bed / torn edge shading)
            if paper[y0:y0+ch, x0:x0+cw].mean() < 0.98: continue
            r = 1 - ratio[y0:y0+ch, x0:x0+cw][m]
            cells.append((x0, y0, float(np.percentile(r, 75)), float(np.median(A[y0:y0+ch, x0:x0+cw][m])), float(np.median(B[y0:y0+ch, x0:x0+cw][m])), int(m.sum())))
    if len(cells) >= 12:
        C = np.array(cells, dtype=np.float32)
        gx, gy = C[:, 0] / cw, C[:, 1] / ch
        pa_, pb_ = np.median(C[:, 3]), np.median(C[:, 4])
        cd = np.hypot(C[:, 3] - pa_, C[:, 4] - pb_)
        light = np.zeros(len(C), bool); diff = np.zeros(len(C), bool); zl = np.zeros(len(C)); zc = robust_z(cd, cd)
        for j in range(len(C)):
            nb = (np.abs(gx - gx[j]) <= 4) & (np.abs(gy - gy[j]) <= 2); nb[j] = False
            if nb.sum() < 6: continue
            zl[j] = robust_z(C[j, 2], C[nb, 2])
            # a genuinely lighter word: low darkness AND normal amount of ink (not a sparse fragment)
            light[j] = zl[j] < -3.0 and C[j, 5] >= 0.6 * np.median(C[nb, 5])
            diff[j] = (zc[j] > 4.0) and cd[j] > 6
        for kind, sel, sc in (('lighter_word', light, -zl), ('different_ink', diff, zc)):
            mk = np.zeros((H // ch + 1, W // cw + 1), np.uint8)
            for j in np.where(sel)[0]: mk[int(gy[j]), int(gx[j])] = 1
            nr, rl, rs, _ = cv2.connectedComponentsWithStats(mk, 8)
            for r_ in range(1, nr):
                ids = [j for j in np.where(sel)[0] if rl[int(gy[j]), int(gx[j])] == r_]
                xs = [int(C[j, 0]) for j in ids]; ys = [int(C[j, 1]) for j in ids]
                box = [min(xs), min(ys), max(xs) + cw - min(xs), max(ys) + ch - min(ys)]
                flags.append(dict(kind=kind, box=box, score=round(float(max(sc[j] for j in ids)), 2), cells=len(ids),
                                  detail=(f"ink darkness z={min(zl[j] for j in ids):.1f} vs neighbouring cells" if kind == 'lighter_word' else f"ink a*/b* {C[ids[0],3]:.0f}/{C[ids[0],4]:.0f} vs page {pa_:.0f}/{pb_:.0f}")))
    # subtle marks: small components not inside/adjacent any word box
    wb = np.zeros((H, W), np.uint8)
    for w in words:
        cv2.rectangle(wb, (w['x'], w['y']), (w['x'] + w['w'], w['y'] + w['h']), 1, -1)
    lo, hi = max(3, int(xh * xh * 0.01)), int(xh * xh * 0.35)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if not (lo <= a <= hi) or w > xh * 0.8 or h > xh * 0.8: continue
        cxm, cym = x + w // 2, y + h // 2
        if wb[cym, cxm]: continue
        # nearest word
        best, bd = None, 1e9
        for ww in words:
            dx = max(ww['x'] - cxm, 0, cxm - (ww['x'] + ww['w'])); dy = max(ww['y'] - cym, 0, cym - (ww['y'] + ww['h']))
            d = np.hypot(dx, dy)
            if d < bd: bd, best = d, ww
        if best is None: continue
        if bd > xh * 4: pos = 'isolated'
        elif cym > best['y'] + best['h'] and abs(cxm - (best['x'] + best['w'] / 2)) < best['w'] / 2: pos = 'below_word'
        elif cym < best['y'] and abs(cxm - (best['x'] + best['w'] / 2)) < best['w'] / 2: pos = 'above_word'
        else: pos = 'beside_word'
        dk = float((1 - ratio[y:y+h, x:x+w][ink[y:y+h, x:x+w] > 0]).mean())
        if pos in ('below_word', 'isolated') and dk > 0.25:
            flags.append(dict(kind='mark_' + pos, box=[int(x), int(y), int(w), int(h)], score=round(dk * 10, 2), detail=f"area {a}px, {bd:.0f}px from word"))
    # bright specks (pinhole-like): much brighter than local paper
    near_ink = cv2.dilate(ink, np.ones((int(xh * 0.6) | 1, int(xh * 0.6) | 1), np.uint8))
    bright = ((ratio > 1.16) & (paper > 0) & (near_ink == 0)).astype(np.uint8)
    nb2, bl, bs, bc = cv2.connectedComponentsWithStats(bright, 8)
    for i in range(1, nb2):
        x, y, w, h, a = bs[i]
        if 4 <= a <= xh * xh * 0.15 and w < xh * 0.5 and h < xh * 0.5:
            flags.append(dict(kind='bright_speck', box=[int(x), int(y), int(w), int(h)], score=round(float(ratio[y:y+h, x:x+w].max()), 2), detail=f"area {a}px"))
    bs_ = [f for f in flags if f['kind'] == 'bright_speck']
    n_bright_total = len(bs_)
    if len(bs_) > 15:
        keep = set(id(f) for f in sorted(bs_, key=lambda f: -f['score'])[:15])
        flags = [f for f in flags if f['kind'] != 'bright_speck' or id(f) in keep]
    res = dict(page=name, n_bright_total=n_bright_total, paper_frac=round(float(paper.mean()), 3), size=[W, H], xheight=xh, n_words=len(words), flags=flags,
               n_cells=len(cells))
    os.makedirs(out, exist_ok=True)
    json.dump(res, open(f"{out}/{name}.json", 'w'))
    # overview
    ov = bgr.copy()
    col = dict(lighter_word=(0, 200, 255), different_ink=(255, 0, 255), mark_below_word=(0, 0, 255), mark_isolated=(0, 120, 255), bright_speck=(255, 200, 0))
    for f in flags:
        x, y, w, h = f['box']; pad = 6
        cv2.rectangle(ov, (x - pad, y - pad), (x + w + pad, y + h + pad), col.get(f['kind'], (0, 255, 0)), 3)
    s = 1400 / max(H, W)
    cv2.imwrite(f"{out}/{name}_overview.jpg", cv2.resize(ov, None, fx=s, fy=s, interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 80])
    # contact sheet: top 24 flags by kind priority
    pri = dict(lighter_word=0, different_ink=1, mark_below_word=2, mark_isolated=3, bright_speck=4)
    top = sorted(flags, key=lambda f: (pri.get(f['kind'], 9), -f['score']))[:24]
    tiles = []
    for f in top:
        x, y, w, h = f['box']; m = int(xh * 2.5)
        x0, y0, x1, y1 = max(0, x - m), max(0, y - m), min(W, x + w + m), min(H, y + h + m)
        t = bgr[y0:y1, x0:x1].copy()
        cv2.rectangle(t, (x - x0 - 3, y - y0 - 3), (x - x0 + w + 3, y - y0 + h + 3), col.get(f['kind'], (0, 255, 0)), 2)
        t = cv2.resize(t, (260, 140), interpolation=cv2.INTER_AREA)
        cv2.putText(t, f"{f['kind'][:14]} {f['score']}", (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 3)
        cv2.putText(t, f"{f['kind'][:14]} {f['score']}", (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
        tiles.append(t)
    if tiles:
        while len(tiles) % 4: tiles.append(np.full((140, 260, 3), 40, np.uint8))
        rows = [np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]
        cv2.imwrite(f"{out}/{name}_flags.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 82])
    mk = [f for f in flags if f['kind'].startswith('mark_')]
    tiles = []
    for f in sorted(mk, key=lambda f: -f['score'])[:32]:
        x, y, w, h = f['box']; m = int(xh * 1.8)
        x0, y0, x1, y1 = max(0, x - m * 2), max(0, y - m), min(W, x + w + m * 2), min(H, y + h + m)
        t = bgr[y0:y1, x0:x1].copy()
        cv2.circle(t, (x - x0 + w // 2, y - y0 + h // 2), int(max(w, h) * 1.6) + 4, (0, 0, 255), 1)
        tiles.append(cv2.resize(t, (300, 150), interpolation=cv2.INTER_CUBIC))
    if tiles:
        while len(tiles) % 4: tiles.append(np.full((150, 300, 3), 40, np.uint8))
        cv2.imwrite(f"{out}/{name}_marks.jpg", np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
    return res

if __name__ == '__main__':
    r = sweep(sys.argv[1], sys.argv[2])
    from collections import Counter
    print(r['page'], 'xh', round(r['xheight'], 1), 'words', r['n_words'], dict(Counter(f['kind'] for f in r['flags'])))
