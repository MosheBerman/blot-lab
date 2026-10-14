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

## 2026-10-12 — Ridge isolation (`scripts/ridge_isolate.py`)

Moshe's hypothesis: the blot is not uniform — ink pools unevenly along each
underlying stroke, so letter strokes should survive as LOCAL maxima/minima
(ridges) inside the blot even though global shade bands see only wash.

Three 2D-local, orientation-free methods on the clean PNG crop:
1. Frangi vesselness (Hessian ridges), sigmas 2–6 px (stroke scale).
2. Black/white top-hat with a 15-px disk (structures on uneven background).
3. Local z-score vs a 31-px median (per-pixel deviation from neighborhood).

Control: the same pipeline on adjacent visible handwriting ("die sollst").
The control validates the method — Frangi and local-z extract the visible
strokes as clean, bright, elongated ridges.

Outcome: negative on structure. The blot interior does vary locally, but the
variation is fine isotropic grain, not elongated stroke-shaped ridges. All
three methods agree; none resolves anything with the character of the
control text. Combined with the morning's synthetic calibration (known text
recoverable at half the real blot's opacity, invisible at full), the
negative is well characterized: no stroke-shaped signal exists in the blot
interior at this scan's resolution. Outputs in `img/passes/ridge39/`.

## 2026-10-12 — Join tab (cross-layer connected components)

Moshe's idea: between the 3D stack's layers, find adjacent strokes and join
them — e.g. layer 0 pixel (2,3) meets the criteria and layer 1 pixel (2,4)
does too, so they join — then project the joined layers onto a flat surface.
The automated version of the stack's manual Advanced layer-pick; conceptually
like tilting a letter to the light, where each layer is a tilt and only
strokes persisting across tilts survive.

Implementation (lab.html, Join tab): renders the same sweep layers as the 3D
stack (Bands, A2 gate, Chroma, Directional, Ridge) at 512px width, reads each
back to a binary mask, runs a CPU 3D flood fill with 26-connectivity over the
layer volume, drops components spanning fewer than Min span layers, and
projects the survivors flat. Two views: binary Projection and a Span map
colored by how many layers each pixel's structure persisted through. Ridge
borrows its scale sweep from the Ridge tab. Flood-fill logic unit-tested in
node (Moshe's example joins; lone pixels drop).

## 2026-10-13 — Scan-17 black block: strict interior test + chain + template match

Moshe's "shapes that look like letters" in the Bands view of the scan-17
redaction block, and his yellow-traced candidates. Four analyses, all on
`the-coded-letters/hidden_files/drive/sweep/pages/17-1.png`:

1. **Strict inside-ink test** (`scripts/block17_strict_test.py`): block =
   union of the two largest low-V components in the lower-left quadrant
   (the two redaction strokes), eroded 9px so no surrounding text leaks in.
   High-pass (L minus 15px median) inside vs a uniform dark control (the
   MIT LUFTPOST label). 254 significant deviations, largest 47px, zero
   elongated (aspect>2.5, length>15px). Outputs:
   `17-block-roi.png` (red = analyzed bbox, blue = interior mask),
   `17-block-inside-hp8x.png` (interior high-pass, 8x amplified).
2. **Sharpen + FFT** (`scripts/block17_chain.py`): flat-field (divide by
   101px median), CLAHE, unsharp mask → `17-block-sharp.png`. 2D FFT power
   spectrum of the windowed interior: energy at JPEG-block frequencies
   (1/8 cyc/px) ≈ background (ratios 0.97–1.07), so the mottling is
   physical ink layering, not compression aliasing → `17-block-fft.png`.
3. **Chained pipeline** (same script): flat-field → PCA on RGB inside the
   ink mask → project onto first PC (ink-density axis) → 8-orientation
   Gabor bank (λ8, σ2.5), max response → threshold top 3% → components.
   Block ink: 62 components, largest 38px, 0 elongated; dark control: 67
   components, largest 27px, 0 elongated. → `17-block-chain-gabor.png`.
4. **Template match** (`scripts/block17_template_match.py`): the 12 most
   stroke-like interior features (ranked by Gabor-component size×aspect)
   as 56px normalized patches, matched with normalized cross-correlation
   against 40 real handwriting-stroke patches from the page and 50 null
   patches (dark-control texture + blank paper), at scales 0.5–2.0.
   Every candidate matched null better than handwriting (mean margin
   −0.253, max −0.134; calibration ref-vs-ref 0.496, null-vs-ref 0.475).
   → `17-block-template-match.png` (candidate | best page-stroke match |
   red/green overlay), `17-block-candidates-on-original.png` (c00–c11
   locations on the original).

Verdict: no letterforms inside the ink; the "stroke-like" shapes are
amplified pen-stroke layering texture (plus the overlapping WIEN postmark
in band views). The redaction destroyed the text.

## 2026-10-13 — Gabor tab + 3D-stack source (lab.html)

The chain's Gabor stage as a live shader: `FS_GABOR` (procedural 15x15
Gabor kernel, orientation = detected stroke direction, wavelength,
sigma, gain, Response/Overlay views). New **Gabor tab** with an Input
toggle: luminance, or the **ink axis** — the first principal component of
the image's RGB, computed by power iteration in `analyzeImage` and passed
as a `u_axis` vec3 uniform (added vec3 support to `draw()`). Added
**Gabor** to the 3D stack's Algorithm picker (index 6, sweep = orientation
0–180°, retarget via the SWEEPS table). Heavier than the other tabs;
layers render at ≤512px. Template matching stays a Python script: it needs
a stroke library and candidate picking, which doesn't fit the sweep
paradigm.

## 2026-10-13 — Ink-difference unmixing (block17_unmix.py)

Moshe's challenge: the block ink and letter ink are chromatically distinct,
so digital separation should have options. Exercised three, on the hi-res
source, in linear RGB with paper/top-ink/letter-ink endmembers:

1. **PCA of interior pixel colors**: 98.2% of variance is one-dimensional
   (the paper↔top-ink thickness axis; it aligns with the letter-ink
   direction at |cos| 0.917 only because both point away from near-black).
   PC2 carries 1.16% variance and aligns poorly (0.382) with the
   letter-ink direction. No letter-ink-directed second axis exists.
2. **Fully-constrained linear unmixing** → per-pixel letter-ink fraction:
   mean 0.001, 32 components above 0.15 fraction, largest 4px, zero
   elongated.
3. **Thinnest-ink decile** (L≥36, where show-through is physically most
   plausible): letter-ink fraction exactly 0.000.

Verdict: the ink difference is real but buys nothing digitally — the top
ink is too opaque for under-ink to contribute measurably to reflected
RGB. The difference is what makes the physical methods (IR/VSC, where the
top ink may go transparent at other wavelengths) the live route.
→ `17-hires-unmix-frac.png` (black = zero letter-ink fraction).

## 2026-10-14 — Band-sensitivity extremes + two-sided coincidence filter (`scripts/twosided_filter.py`)

Moshe's questions: (1) does changing band sensitivity (band count N) help?
(2) what about a filter on BOTH front and back layers instead of the
one-direction dark->light sweep?

1. Band count N=3 and N=24 on the blot-39 crop, blot-mask shade range
   L 128.0-201.0 (N=6/12 ran 2026-10-12). N=24: the blot fragments into
   fine mottled bands - isotropic grain, nothing elongated. N=3: three
   coarse blotchy regions, no structure. Verdict: no. Narrower bands dice
   the wash noise finer; wider bands merge it. No letterforms at any of
   N=3/6/12/24. Outputs: `img/passes/bands-extreme/n{3,24}-blotmask/`.

2. Two-sided filter, two operationalizations, calibrated on the synthetic
   wash ladder (known text at s=0.5/0.75/1.0/1.25; wash-restricted
   mask+scoring via --washref so un-obscured text can't inflate recall):
   - dev-mode: |z|>1.5 deviation within the 2 darkest bands AND within
     the 2 lightest bands, spatial coincidence (3px dilate). Too strict:
     a pixel lives in exactly one band, so it only fires at
     thick-to-thin transitions. Recall 2% even at s=0.5 - weak positive
     control.
   - anom-mode: band-index anomaly (>=2 bands from the local 31px median)
     required in BOTH the dark half and the light half of the stack.
     Too loose: the wash's own mottling is a depth anomaly everywhere -
     coincidence covers 33-57% of the wash at every opacity and 55% of
     blot39. Cannot distinguish text-bearing s=0.5 wash from text-free
     s=1.0 wash. Fails the calibration signature.
   - Verdict: the idea is physically sound (a pooling stroke should
     perturb multiple depths), but this blot's wash texture varies with
     depth at every scale, so "present at both ends" does not
     discriminate. The measured opacity floor stands: lightness-based
     methods cannot reach the core. Script kept; do not rerun blind.

3. UI: the Bands tab gained a "Both ends" mode (darkest + lightest
   windows shown together, Window-width slider visible) so
   depth-persistent structure can be eyeballed in one view - built for
   Moshe's 2026-10-14 note that human eyes beat the algorithms on
   curvature.

## 2026-10-14 — 3D-stack thickness readout (per-layer µm + layer–thickness correlation)

Moshe: referencing the forensics report's thickness section, add a
thickness↔layer correlation and show the per-layer µm.

- Model: dye glaze R = Rg·exp(−2K·X) (report §5) → K·X = −0.5·ln(Y/Yg),
  Y from CIE L*, Yg at the image 98th percentile. µm scale: K·X=1 ↔ 30µm,
  the midpoint of the report's 10–50µm single-pass penetration bracket
  (§§2–4); labeled on the UI as an estimate, not a measurement.
- 3D stack, Bands source only: each Advanced layer-pick chip shows its
  layer's µm under the index; a Thickness row reports r(layer index, K·X)
  and the layer-0 → layer-(n−1) µm span. On the blot-39 crop (12 bands):
  r = −0.997, layer 0 (darkest) ≈ 24µm → layer 11 ≈ 1µm. Other sources
  show no thickness UI — their layers are parameter sweeps, not depth.
- Verified: node --check on the page script; µm math cross-checked in
  Python against the real crop numbers before shipping.

## 2026-10-14 — Postcard sizes re-researched + manufacturer-marking hunt

Moshe: research German postcard sizes again; look for manufacturer
markings on the edges of our postcards.

- Standards: UPU 1878 max 14×9cm → UPU 1924 max 10.5×15cm; DIN A6
  "Normalformat" (148×105mm) introduced in Germany 1 Oct 1927, standard
  through the 1930s–40s; official DR Ganzsachen postcards 148:105mm
  (Hindenburg-Medaillon article: 29 templates P216–P244). Reichspost 1875
  norm was 140×90mm.
- Our cards (scans 1, 5, 17, 18, 19, 23 — all Chaja/Ch. Willner or Salomon
  Willner): measured ~190×136mm against the PDF letter pages — BUT the
  10pf Hindenburg stamp on card 1 (true size 21.5×26mm) measures ~28.8mm
  in the same render, so the Apple Notes scan-to-PDF pipeline enlarged
  the photos ~1.3×. Corrected size ≈ 146×105mm = A6 Normalformat, ratio
  1.40 ≈ √2. The forensics report's A6 assumption was correct. Card/aspect
  check: card:stamp width ratio 6.58 vs 6.88 expected for A6 (4% off);
  the 190mm reading would need 8.84 — ruled out.
- ⚠ Standing caution: do NOT measure absolute mm from the coded-letters
  PDFs without a reference object — the scans are ~1.3× enlarged.
- Scan 51 is not a postcard (small handwritten note, blue dabs).
- Markings: none found. Examined at 300dpi: bottom/top/left edges and
  center-bottom of cards 1, 5, 17, plus both message sides (fully
  handwritten). Post-1905 publisher imprints usually sit on the address
  side (Ansichtskarte article) — ours are clean. Either unmarked stock or
  the imprint hides under handwriting / the airmail label. 300dpi edge
  crops kept in img/pc-edges-hires/.
