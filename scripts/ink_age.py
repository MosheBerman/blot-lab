#!/usr/bin/env python3
"""ink_age.py — relative ink-signature comparison: were marks added after the fact?

Question: for each bold/retraced word, partial spill, blackout stroke, or
suspicious dot, does its ink match the surrounding legible writing
(same pen, same session) or not (different pen — possibly a later addition)?

Method (all comparisons INTRA-photo, i.e. target vs. reference regions from
the SAME image):
  1. Estimate the local paper color from a blank patch in the same figure.
  2. Ink mask per region: L < paper_L - 28 (adaptive; falls back to -18).
  3. Ink signature: median LAB of ink pixels, expressed PAPER-RELATIVE:
       dL = paper_L - ink_L   (darkness depth; larger = darker)
       da = ink_a - paper_a,  db = ink_b - paper_b   (chromaticity vs paper)
     Paper-relative signatures cancel per-photo lighting, exposure, and
     white-balance differences. EXIF on all working images is stripped
     (verified: 0 tags), so there is no exposure/WB metadata to correct
     with anyway; the intra-photo normalization is strictly stronger.
  4. Distance dP = euclidean distance between paper-relative signatures.
  5. Stroke width via distance transform on the ink mask (flags retracing:
     same hue + much darker + wider strokes = double application).

Decision rule (stated before running; thresholds come from the calibration
set, not asserted):
  - Calibration: umlaut dots / i-dots vs their own word bodies, and
    neighboring ordinary words vs each other  -> "same ink" dP distribution.
  - Negative control: penciled "1463" (different hand, graphite) vs ink
    -> "different ink" anchor.
  - Verdict per target: dP within the same-ink band  -> same ink/session;
    dP at/above the different-ink anchor             -> different ink;
    between                                         -> inconclusive.
  - Retracing flag: same hue as ref (chroma dP small) AND dL >= 1.5x ref dL
    AND stroke width >= 1.4x ref -> retraced (written over twice).

Honest limits (also stated up front):
  - This detects same-vs-different INK, not dates. "Different ink" is
    consistent with a later addition but also with a pen change mid-letter.
  - "Same ink" does not prove same minute; it rules out a different pen.
  - Water damage / foxing inside a bbox can pollute a sample; bboxes avoid
    damage contours and low-ink samples are flagged.

Outputs: img/passes/ink-age/fig-<case>.png (annotated) and
         img/passes/ink-age/ink-age-measurements.json
"""
import cv2
import json
import numpy as np
import os

BASE = os.path.expanduser('~/workspace/blot-lab')
SRC = os.path.join(BASE, 'img/passes/ink-age')
OUT = os.path.join(BASE, 'img/passes/ink-age')
os.makedirs(OUT, exist_ok=True)

# (name, image, fig_crop, paper_bbox, targets{label:bbox}, refs{label:bbox})
# bboxes are (x0, y0, x1, y1) in source-image pixels; fig_crop crops the figure.
CASES = [
    dict(name='33-cheder', img='33-p0.png', fig=(240, 1050, 1010, 1220),
         paper=(940, 950, 1100, 1010),
         targets={'cheder (bold)': (468, 1108, 648, 1182)},
         refs={'Schule': (688, 1078, 878, 1142),
               'wie auch': (288, 1112, 468, 1178),
               'konnen die Kinder': (660, 1108, 1005, 1180)}),
    dict(name='33-umlaut', img='33-p0.png', fig=(280, 830, 800, 970),
         paper=(720, 830, 800, 880),
         targets={'u-diaeresis dots': (625, 862, 680, 892)},
         refs={'durchfuhren body': (518, 872, 742, 938),
               'du es': (295, 872, 425, 938)}),
    dict(name='33-fuer', img='33-p0.png', fig=(60, 760, 420, 890),
         paper=(300, 760, 390, 800),
         targets={'u-diaeresis dots': (150, 795, 205, 830)},
         refs={'fur': (125, 810, 265, 880),
               'Mali': (270, 810, 380, 880)}),
    dict(name='33-idot', img='33-p0.png', fig=(680, 1040, 800, 1180),
         paper=(680, 1040, 720, 1075),
         targets={'i dot (die)': (740, 1080, 760, 1100)},
         refs={'die body': (712, 1102, 768, 1138)}),
    dict(name='33-smudge', img='33-p0.png', fig=(60, 850, 750, 1020),
         paper=(660, 850, 750, 900),
         targets={'gray smudge': (530, 875, 640, 985)},
         refs={'durchfuhren': (518, 872, 742, 938),
               'Wie geht': (330, 940, 480, 1000)}),
    dict(name='33-joblot', img='33-p1.png', fig=(440, 940, 870, 1170),
         paper=(760, 880, 900, 940),
         targets={'Jo- blot': (605, 980, 695, 1135)},
         refs={'Ist Jo': (465, 995, 605, 1075),
               'schon in': (700, 995, 860, 1070)}),
    dict(name='33-speck', img='33-p1.png', fig=(750, 1150, 1050, 1330),
         paper=(760, 880, 900, 940),
         targets={'small dark blot': (815, 1215, 875, 1295)},
         refs={'demnaechst': (890, 1190, 1020, 1260)}),
    dict(name='42-du', img='42-p0.png', fig=(100, 920, 500, 1060),
         paper=(400, 920, 500, 970),
         targets={'Du (darker)': (160, 955, 230, 1010)},
         refs={'mir': (240, 955, 320, 1010),
               'regelmaessig': (330, 955, 500, 1010)}),
    dict(name='42-der', img='42-p0.png', fig=(150, 1200, 550, 1340),
         paper=(450, 1200, 550, 1250),
         targets={'Der (darker)': (270, 1245, 350, 1300)},
         refs={'ich': (150, 1245, 265, 1300),
               'geschrieben': (355, 1245, 540, 1300)}),
    dict(name='53-blackout', img='53-p0.png', fig=(150, 1090, 1130, 1310),
         paper=(1055, 1090, 1125, 1150),
         targets={'blackout strokes': (688, 1175, 1052, 1268)},
         refs={'bekommen der Jossel': (375, 1090, 700, 1160),
               'mecht so gern': (175, 1185, 480, 1255)}),
    dict(name='53-dankend', img='53-p0.png', fig=(540, 180, 920, 340),
         paper=(800, 180, 900, 230),
         targets={'Dankend overtext': (600, 245, 750, 295)},
         refs={'von Euch': (180, 175, 330, 245),
               'Freude': (180, 260, 330, 325)}),
    dict(name='54-blackout', img='54-p0.png', fig=(110, 1150, 720, 1400),
         paper=(600, 1150, 700, 1180),
         targets={'blackout strokes': (180, 1240, 560, 1300)},
         refs={'Gruesse Kusse vielmals': (195, 1170, 700, 1235),
               'auch Deine Kinder': (195, 1310, 660, 1370)}),
    dict(name='aerogramme-dab', img='aerogramme-blot-dabs.jpg', fig=None,
         paper=(180, 380, 280, 440),
         targets={'blue dab': (275, 55, 385, 225)},
         refs={'handwriting man': (0, 125, 210, 200),
               'handwriting Hers': (55, 195, 300, 300),
               'printed microtext': (390, 30, 500, 110)}),
    dict(name='33-bluemargin', img='33-p0.png', fig=(100, 0, 1100, 200),
         paper=(950, 20, 1100, 90),
         targets={'3rd-author blue marginalia': (720, 40, 900, 120)},
         refs={'Wien 11/II 1940 dateline': (430, 60, 700, 120),
               'Liebe Frau greeting': (380, 120, 700, 190)}),
    dict(name='44-ausgeloest', img='l44-deletion2.png', fig=None,
         paper=(350, 5, 550, 45),
         targets={'Ausgeloest overwrite': (400, 90, 625, 170)},
         refs={'Alle': (300, 100, 395, 160),
               'werden mit': (625, 95, 800, 165)}),
]


def sample(region_lab, paper_lab, min_margin=28):
    """Paper-relative ink signature for a bbox region (LAB image)."""
    pL, pa, pb = paper_lab
    L = region_lab[:, :, 0].astype(np.float32)
    ink = L < (pL - min_margin)
    if ink.sum() < 25 and min_margin > 18:
        ink = L < (pL - 18)
    n = int(ink.sum())
    if n < 10:
        return None
    mL = float(np.median(region_lab[:, :, 0][ink]))
    ma = float(np.median(region_lab[:, :, 1][ink]))
    mb = float(np.median(region_lab[:, :, 2][ink]))
    # stroke width: distance transform on ink mask
    dt = cv2.distanceTransform(ink.astype(np.uint8), cv2.DIST_L2, 3)
    sw = float(np.median(dt[ink]) * 2.0)
    return dict(n=n, dL=round(pL - mL, 2),
                da=round(ma - pa, 2), db=round(mb - pb, 2),
                rawL=round(mL, 1), stroke_w=round(sw, 2))


def dist(s1, s2):
    return round(float(np.sqrt((s1['dL'] - s2['dL']) ** 2 +
                               (s1['da'] - s2['da']) ** 2 +
                               (s1['db'] - s2['db']) ** 2)), 2)


def main():
    results = []
    for c in CASES:
        img_path = os.path.join(SRC, c['img'])
        # l44 crop lives in letter-analysis crops dir; aerogramme in img/source
        if not os.path.exists(img_path):
            img_path = os.path.join(BASE, 'letter-analysis/muse/crops', c['img'])
        if not os.path.exists(img_path):
            img_path = os.path.join(BASE, 'img/source', c['img'])
        bgr = cv2.imread(img_path)
        if bgr is None:
            print('MISSING', c['img'])
            continue
        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
        x0, y0, x1, y1 = c['paper']
        paper = lab[y0:y1, x0:x1]
        paper_lab = (float(np.median(paper[:, :, 0])),
                     float(np.median(paper[:, :, 1])),
                     float(np.median(paper[:, :, 2])))
        entry = dict(case=c['name'], img=c['img'], paper_L=round(paper_lab[0], 1),
                     targets={}, refs={})
        for label, (bx0, by0, bx1, by1) in c['targets'].items():
            s = sample(lab[by0:by1, bx0:bx1], paper_lab)
            entry['targets'][label] = s
        for label, (bx0, by0, bx1, by1) in c['refs'].items():
            s = sample(lab[by0:by1, bx0:bx1], paper_lab)
            entry['refs'][label] = s
        # pairwise target-vs-ref distances
        entry['distances'] = {}
        for tl, ts in entry['targets'].items():
            if ts is None:
                continue
            for rl, rs in entry['refs'].items():
                if rs is None:
                    continue
                entry['distances'][f'{tl} vs {rl}'] = {
                    'dP': dist(ts, rs),
                    'dL_ratio': round(ts['dL'] / rs['dL'], 2) if rs['dL'] else None,
                    'stroke_ratio': round(ts['stroke_w'] / rs['stroke_w'], 2)
                    if rs['stroke_w'] else None,
                }
        # ref-vs-ref distances (calibration: how much ordinary words vary)
        rlabels = [rl for rl, rs in entry['refs'].items() if rs is not None]
        entry['ref_spread'] = {}
        for i in range(len(rlabels)):
            for j in range(i + 1, len(rlabels)):
                a, b = rlabels[i], rlabels[j]
                entry['ref_spread'][f'{a} vs {b}'] = dist(entry['refs'][a],
                                                          entry['refs'][b])
        results.append(entry)

        # annotated figure
        fx0, fy0, fx1, fy1 = c['fig'] if c['fig'] else (0, 0, bgr.shape[1], bgr.shape[0])
        fig = bgr[fy0:fy1, fx0:fx1].copy()
        for label, (bx0, by0, bx1, by1) in c['targets'].items():
            cv2.rectangle(fig, (bx0 - fx0, by0 - fy0), (bx1 - fx0, by1 - fy0),
                          (0, 0, 255), 3)
            cv2.putText(fig, 'TARGET', (bx0 - fx0, by0 - fy0 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        for label, (bx0, by0, bx1, by1) in c['refs'].items():
            cv2.rectangle(fig, (bx0 - fx0, by0 - fy0), (bx1 - fx0, by1 - fy0),
                          (0, 150, 0), 2)
        cv2.rectangle(fig, (x0 - fx0, y0 - fy0), (x1 - fx0, y1 - fy0),
                      (255, 0, 0), 2)
        cv2.imwrite(os.path.join(OUT, f"fig-{c['name']}.png"), fig)
        print(c['name'], 'ok')

    with open(os.path.join(OUT, 'ink-age-measurements.json'), 'w') as f:
        json.dump(results, f, indent=1)
    print('wrote', os.path.join(OUT, 'ink-age-measurements.json'))


if __name__ == '__main__':
    main()
