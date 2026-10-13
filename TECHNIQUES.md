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

## 2026-10-12 — Color-separation pass (`scripts/color_pass.py`)

External review suggested the shade bands throw away chroma: a different ink
under blue dye ink can separate in the red vs blue channels. Ran on the
letter-39 blot ROI (x[88:474] y[389:726]):

1. R/G/B channel views (grayscale, 1–99% normalized).
2. Decorrelation stretch (PCA whitening, contrast matched) on the ROI.
3. PC1/2/3 false-color composite.
4. B-minus-R asymmetry map (blue dye ink absorbs red strongly).

Outcome: negative. R and B channels are near-identical — one uniform ink.
The decorrelation stretch and false-color show mottled wash texture only, no
letterforms, numbers, or script. The B−R map is smooth (saturated blue core
vs gray text), with no structures shaped like writing. The core is a single
saturated ink: nothing under it differs in chroma on this photo. Outputs in
`img/passes/color39/`.

## 2026-10-12 — UI: pinch zoom out to 50%, floating minimap

- Pinch zoom minimum lowered from 1.0 to 0.5 (sidebar-less; zoom is
  gesture-only). Double-tap still resets to 100%.
- The expanded minimap is no longer a fullscreen modal: it floats in the
  top-right corner (top, left of the tools panel in landscape), tappable to
  dismiss; the toolbar thumbnail button reopens it. Live viewport rectangle
  redraws while expanded, unchanged.

## 2026-10-12 — UI: trackpad support

- Pinch-to-zoom on the trackpad (ctrl+wheel): zooms around the cursor, same
  0.5–8× range as touch pinch.
- Two-finger scroll (wheel): pans, content follows the fingers, scaled by zoom.
- preventDefault stops the browser's page-zoom gesture over the canvas.

## 2026-10-12 — UI: 3D stack advanced layer picker

- 3D stack tab: new "Layer pick" control (Window / Advanced). Advanced hides
  the sliding-window sliders (Window end, Window width) and shows a column of
  per-layer toggle chips (one per layer, 0..n-1), so any non-contiguous set of
  layers can be shown by hand. Works for every algorithm source, not just Bands.
- Chips row has All / None quick buttons; chip count follows the Layers slider
  (growing preserves the existing pattern, shrinking keeps the prefix).
- Tint gradient and sheet spacing follow the visible order, not the raw index.
- Selection lives in tab state, so it survives Reset sliders (resets to all on),
  session auto-restore, and snapshot links.

## 2026-10-12 — Source-resolution audit (prompted by Moshe)

Question: did the analyses run on downscaled copies? Provenance chain,
verified by blot-blob matching:
- Best local source: `goals/the-coded-letters/hidden_files/drive/39-hi-1.png`
  (2550x3300).
- `39-blot.png` (765x726) is a native-resolution crop of it: the blot's
  saturated mask is 306x297 px there vs 306x333 px on the full page (same
  ink, threshold noise). No downscaling of the blot region.
- `img/blot39.jpg` is a JPEG recompress of that PNG crop.
- The PDF (`39.pdf`) embeds a SMALLER 1940x2013 copy — worse, not better.

So the analyses ran at native resolution; only JPEG recompression was lost.
Re-ran the color pass on the PNG crop (`img/source/39-blot.png`): same
negative (uniform ink, mottled wash, no letterforms). `color_pass.py` now
reads the PNG by default. Remaining untapped source: the original iPhone
photo itself (39-hi-1.png is not a native 12MP size), if it still exists.
