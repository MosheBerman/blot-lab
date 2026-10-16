"""Ink maps for visual review (Claude version).
For each page: (a) ink-darkness heat map -- every ink pixel coloured by how dark it is relative to the
page's own ink range (lighter-than-usual words show as cool/blue islands among warm text); (b) ink-hue map
-- every ink pixel coloured by its chroma angle (a second ink, pencil or a later addition shows as a
different colour). Usage: python3 ink_maps.py <page.jpg> <outdir>"""
import sys, os, cv2, numpy as np
p, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
name = os.path.splitext(os.path.basename(p))[0]
bgr = cv2.imread(p); H, W = bgr.shape[:2]
s = 1100 / max(H, W); bgr = cv2.resize(bgr, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
k = int(max(21, (min(bgr.shape[:2]) // 25) | 1))
bg = cv2.medianBlur(lab[..., 0].astype(np.uint8), k).astype(np.float32) + 1
ratio = lab[..., 0] / bg
ink = ratio < 0.88
dark = np.clip(1 - ratio, 0, 1)
lo, hi = np.percentile(dark[ink], 5), np.percentile(dark[ink], 95)
v = np.clip((dark - lo) / (hi - lo + 1e-6), 0, 1)
heat = cv2.applyColorMap((v * 255).astype(np.uint8), cv2.COLORMAP_TURBO)
heat[~ink] = 255
a, b = lab[..., 1] - 128, lab[..., 2] - 128
ang = (np.degrees(np.arctan2(b, a)) + 360) % 360
chroma = np.hypot(a, b)
hsv = np.zeros_like(bgr); hsv[..., 0] = (ang / 2).astype(np.uint8); hsv[..., 1] = np.clip(chroma * 6, 0, 255).astype(np.uint8); hsv[..., 2] = 230
hue = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR); hue[~ink] = 255
cv2.imwrite(f'{out}/{name}_heat.jpg', heat, [cv2.IMWRITE_JPEG_QUALITY, 80])
cv2.imwrite(f'{out}/{name}_hue.jpg', hue, [cv2.IMWRITE_JPEG_QUALITY, 80])
