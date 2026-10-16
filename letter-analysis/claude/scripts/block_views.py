"""Independent look under a dark deletion: per-channel views, CLAHE, extreme dark-end gamma,
blue-minus-red difference and a local-contrast (top-hat) view, tiled into one sheet.
Usage: python3 block_views.py <page.jpg> <out.jpg> x0 y0 x1 y1"""
import sys, cv2, numpy as np
p, o = sys.argv[1], sys.argv[2]; x0, y0, x1, y1 = map(int, sys.argv[3:7])
im = cv2.imread(p)[y0:y1, x0:x1]
b, g, r = cv2.split(im)
cl = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(8, 8))
def norm(c, lo=1, hi=99):
    a, z = np.percentile(c, lo), np.percentile(c, hi); return np.clip((c.astype(np.float32) - a) / (z - a + 1e-6) * 255, 0, 255).astype(np.uint8)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
dark = gray.astype(np.float32); m = dark < np.percentile(dark, 35)
dg = np.zeros_like(gray); vals = dark[m]; lo, hi = np.percentile(vals, 1), np.percentile(vals, 99)
dg[m] = np.clip(((dark[m] - lo) / (hi - lo + 1e-6)) ** 0.5 * 255, 0, 255).astype(np.uint8)
bmr = norm(b.astype(np.int16) - r.astype(np.int16) + 255)
th = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
views = [('original', im), ('R', cv2.cvtColor(norm(r), cv2.COLOR_GRAY2BGR)), ('G', cv2.cvtColor(norm(g), cv2.COLOR_GRAY2BGR)), ('B', cv2.cvtColor(norm(b), cv2.COLOR_GRAY2BGR)),
         ('CLAHE gray', cv2.cvtColor(cl.apply(gray), cv2.COLOR_GRAY2BGR)), ('dark-end stretch', cv2.cvtColor(dg, cv2.COLOR_GRAY2BGR)),
         ('blue-minus-red', cv2.cvtColor(bmr, cv2.COLOR_GRAY2BGR)), ('black-hat 9px', cv2.cvtColor(norm(th), cv2.COLOR_GRAY2BGR))]
tiles = []
for t, v in views:
    v = v.copy(); cv2.putText(v, t, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2); tiles.append(v)
rows = [np.hstack(tiles[i:i + 2]) for i in range(0, 8, 2)]
out = np.vstack(rows); s = min(1.0, 1600 / out.shape[1])
cv2.imwrite(o, cv2.resize(out, None, fx=s, fy=s), [cv2.IMWRITE_JPEG_QUALITY, 85])
