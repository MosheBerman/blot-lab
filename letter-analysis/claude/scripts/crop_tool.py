"""Crop helper: python3 crop_tool.py <page.jpg> <out.jpg> x y w h [pad] [scale] -- writes a padded crop with the box outlined."""
import sys, cv2
p, o = sys.argv[1], sys.argv[2]; x, y, w, h = map(int, sys.argv[3:7])
pad = int(sys.argv[7]) if len(sys.argv) > 7 else 60; sc = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0
im = cv2.imread(p); H, W = im.shape[:2]
x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
c = im[y0:y1, x0:x1].copy()
if len(sys.argv) > 9 and sys.argv[9] == 'box':
    cv2.rectangle(c, (x - x0, y - y0), (x - x0 + w, y - y0 + h), (0, 0, 255), 2)
c = cv2.resize(c, None, fx=sc, fy=sc, interpolation=cv2.INTER_CUBIC)
cv2.imwrite(o, c, [cv2.IMWRITE_JPEG_QUALITY, 88])
