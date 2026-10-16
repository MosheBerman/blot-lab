"""Deletion / blot ink comparison (Claude version).
Finds dense ink masses (scribble-outs, blots) on each page and compares their ink colour with the
surrounding handwriting within 6 x-heights. A deletion made with the writer's own pen should match the
writing (after allowing for the darker, re-loaded pen); a different hue suggests another pen or hand
(e.g. a censor's blacking). Usage: python3 deletion_ink.py <sweep_json_dir> <pages_dir> <out.json> <crops_dir>"""
import sys, os, json, glob, cv2, numpy as np
sj, pd, outp, cd = sys.argv[1:5]; os.makedirs(cd, exist_ok=True)
res = []
for jf in sorted(glob.glob(f'{sj}/*.json')):
    meta = json.load(open(jf)); name = meta['page']; xh = meta['xheight']
    bgr = cv2.imread(f'{pd}/{name}.jpg'); H, W = bgr.shape[:2]
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    k = int(max(31, (min(H, W) // 25) | 1))
    bg = cv2.medianBlur(lab[..., 0].astype(np.uint8), k).astype(np.float32) + 1
    ratio = lab[..., 0] / bg
    ink = (ratio < 0.80).astype(np.uint8)
    win = int(xh * 1.2) | 1
    dens = cv2.blur(ink.astype(np.float32), (win, win))
    core = ((dens > 0.62) & (ink > 0)).astype(np.uint8)
    core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lb, st, _ = cv2.connectedComponentsWithStats(core, 8)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < (xh * 1.3) ** 2 or a > (xh * 30) ** 2: continue
        if x < 5 or y < 5 or x + w > W - 5 or y + h > H - 5: continue
        m = lb[y:y+h, x:x+w] == i
        Lb = lab[y:y+h, x:x+w]
        blot = dict(L=float(np.median(Lb[..., 0][m])), a=float(np.median(Lb[..., 1][m]) - 128), b=float(np.median(Lb[..., 2][m]) - 128))
        r = int(xh * 6)
        X0, Y0, X1, Y1 = max(0, x - r), max(0, y - r), min(W, x + w + r), min(H, y + h + r)
        ring = (ink[Y0:Y1, X0:X1] > 0).copy()
        ring[y - Y0:y - Y0 + h, x - X0:x - X0 + w] = False
        if ring.sum() < 200: continue
        Lr = lab[Y0:Y1, X0:X1]
        wr = dict(L=float(np.median(Lr[..., 0][ring])), a=float(np.median(Lr[..., 1][ring]) - 128), b=float(np.median(Lr[..., 2][ring]) - 128))
        # darkest decile of the writing = freshly loaded pen; compare the blot against that
        dk = Lr[..., 0][ring] <= np.percentile(Lr[..., 0][ring], 10)
        wd = dict(L=float(np.median(Lr[..., 0][ring][dk])), a=float(np.median(Lr[..., 1][ring][dk]) - 128), b=float(np.median(Lr[..., 2][ring][dk]) - 128))
        dE = float(np.sqrt((blot['a'] - wd['a']) ** 2 + (blot['b'] - wd['b']) ** 2))
        hue_b = float(np.degrees(np.arctan2(blot['b'], blot['a']))); hue_w = float(np.degrees(np.arctan2(wd['b'], wd['a'])))
        crop = bgr[max(0, y - r // 2):min(H, y + h + r // 2), max(0, x - r):min(W, x + w + r)]
        cn = f'{name}_blot{i}.jpg'
        cv2.imwrite(f'{cd}/{cn}', cv2.resize(crop, None, fx=min(1.0, 500 / max(crop.shape[:2])), fy=min(1.0, 500 / max(crop.shape[:2]))), [cv2.IMWRITE_JPEG_QUALITY, 85])
        res.append(dict(page=name, box=[int(x), int(y), int(w), int(h)], area=int(a), blot=blot, writing=wr, writing_dark=wd,
                        chroma_dE_vs_dark_writing=round(dE, 1), crop=cn))
json.dump(res, open(outp, 'w'), indent=1)
print(len(res))
