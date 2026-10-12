# Techniques Log

Every image experiment in this repo gets: algorithm, parameters, measured
outcome. Append as you go; never repeat a dead end blind.

---

## 2026-10-07 — Blot detector (density + saturation gating)

- Otsu-threshold page to ink mask; keep saturated pixels (HSV S > 40).
- Local ink density via 25 px box filter; flag regions > 50% density.
- Connected components; keep compact blobs 900–60,000 px.
- Swept 53 PDFs (~100 pages, 150 dpi): 173 candidates, all visually reviewed.
- Outcome: the two known blots (letters 39, 45) plus accidental drips/stains
  in scans 40, 33, 6, 18. No hidden words anywhere.
- Dead end to avoid: plain connected components without the density gate —
  morphological closing merges blots with adjacent text into one giant
  low-solidity component.

## 2026-10-07 — Stylus-press lifting (paper-texture enhancement)

- Mask ink via local background subtraction; dilate mask; work on paper
  pixels only (hard exclusion, no inpainting).
- Flatten illumination in log domain; high-pass at ~8 px; directional
  Sobel for horizontal groove structures.
- Outcome: honest negative. Flatbed diffuse on-axis light suppresses the
  micro-shading embossing produces; signal below the noise floor of
  wrinkles, fiber, JPEG artifacts. No single-image algorithm recovers it.
- What would work: raking-light photos of the originals (desk lamp, any
  camera, one low light position per side), ESDA, or RTI.

## 2026-10-12 — Multi-pass shade-band isolation (`scripts/shade_isolate.py`)

Motivation: a blot has finite transparency, layers, colors, and shades.
Slice the shade range into bands and isolate each band separately, in
multiple passes and directions — "frames of a movie" that should reveal
writing hidden at different depths/sizes.

Algorithm:
1. Auto-detect blot ROI: saturated blue ink mask (HSV H 85–130, S > 60),
   largest connected component + 40 px margin for shade calibration.
   Source images must carry no annotation boxes.
2. Shade range: 2nd/98th percentile of LAB L inside the blot mask.
3. Family A (global bands): split range into N bands (ran N=6 and N=12);
   per-band binary masks + color-coded composite stitch + depthmap
   (band index as height) + animated GIF sweeping dark→light.
4. Families B/C/D (directional): per-line z-score of blot pixels against
   the line's own median/std; |z| > k marks strokes differing from the
   local wash. Directions: rows, columns, both diagonals (via 45° rotation).
   Ran k=1.5 and k=2.5.
5. Family E (multi-scale): row-wise pass at 2× upscale for wider strokes.

Parameters (letter-39 blot, `img/blot39.jpg` 765×726):
- ROI x[88:474] y[389:726], 45,337 blot px; shade range L 128.0–201.0.
- 37 outputs in `img/passes/blot39/`.

Outcome: honest negative. Across 12 shade bands, 4 directions, 2 z
thresholds, and 2 scales, no band or pass resolves into letterforms,
numbers, or Yiddish script. Darkest bands show only fragmented blot-edge
pixels; directional deviation maps show mottled wash texture only. Matches
the 2026-10-07 ink-maximizing enhancement verdict: the core is fully
saturated, nothing recoverable. The sentence reads complete without the
1–3 lost words.

Note for future runs: the method itself is sound (clean shade separation,
verified on the composite/depthmap); it is the right tool if a new blot
candidate ever appears with a non-saturated core.
