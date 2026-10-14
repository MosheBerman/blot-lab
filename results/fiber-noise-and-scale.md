# Fiber noise + pixel scale audit (2026-10-14)

## Pixel scale: corrected

The earlier 281ppi / 90um-per-px figure was never anchored to a reference object.
Two independent rulers on 17pdf-000.jpg (2138x1494, address side):

- Card width: card spans ~2120px; A6 Normalformat = 148mm -> 367ppi -> 69.3um/px
- Postmark ring: Hough circle r=211px (dia 421px); DR Tagesstempel ~28mm -> ~380ppi -> 66.6um/px

Working scale: 65-75um/px (~350-390ppi). The old 90um figure was ~25% too coarse.
Stamp-based rulers failed (brown stamp half-covered by airmail label; green stamp mask
caught only the printed design, not the stamp rect).

## Fiber resolvability: still no

Paper cellulose fibers: 10-30um wide (textbook: softwood tracheids 20-40um,
hardwood 15-25um). At 65-75um/px that is 0.13-0.46px per fiber width.
Individual fibers are sub-pixel at this resolution; resolving them would need
~2500ppi. The earlier conclusion stands, margin thinner than the old numbers implied.

## Conservative fiber-noise pass

Method: blank paper patches found by low-variance scan, illumination detrended
(gaussian sigma 25 subtracted), then lag autocorrelation + FFT band power.

Postcard blank patches (n=3): detrend_std 6.3-10.6, ac(1,0) 0.71-0.81,
ac(0,1) 0.76-0.89, ac(8,0) ~0 (no JPEG block signature), fine 2-8px power 0.13-0.22.
Onion skin blanks (n=3): detrend_std 4.0-11.9, ac(1,0) 0.66-0.89,
ac(0,1) 0.72-0.89, fine power 0.12-0.25.

Verdict: correlated 1-2px mottle exists on BOTH substrates at similar amplitude
(not white noise), isotropic, no directional fiber signature. Consistent with
sub-pixel fiber mottle aliased through the camera pipeline, but NOT resolvable
as fibers and NOT separable into a fiber channel. There is no fiber-specific
signal to isolate.

## Smoothing experiment (exact lab Bands replication)

Replicated the lab Bands tab exactly: LAB L*, 2nd-98th percentile range,
12 bands, Window mode width 3.

scan5-message (Bands P1): raw stroke_frac 0.948, speckle 0.014;
  gauss0.8 -> 0.972/0.005; gauss1.5 -> 0.982/0.002.
onion p1 (Bands P2): raw 0.946/0.013; gauss0.8 -> 0.963/0.007; gauss1.5 -> 0.964/0.004.

Smoothing is redundant: the lab's Window-3 already consolidates strokes to
0.95 on both substrates. The postcard/onion-skin gap seen in the viewer sweep
is competing printed elements (stamps, postmarks, address rules) on the card,
which no smoothing removes. Smoothing cannot bring the postcard to parity
because grain was never the gap.

## Grain reversal: binary opening works (2026-10-14)

User pushback: there has to be a way to reverse grain. Tested three routes,
metric = stroke edge raggedness p^2/a (circle = 12.6, lower = smoother):

- Grayscale inpaint-flatten (estimate paper field under ink, subtract):
  postcard 78.4 -> 80.0, onion 71.1 -> 71.8. NO effect. The raggedness is not
  in the background field; it is baked into the ink/paper boundary.
- Grayscale white top-hat r=4: postcard 78.4 -> 88.2 AND shattered strokes
  (419 -> 1236 components); onion collapsed (strokes wiped, n=2). Destructive.
- Binary morphological opening r=1 (3x3 ellipse) on the Bands mask:
  postcard 78.4 -> 48.5 (38% smoother), onion 71.1 -> 39.2.
  Opened postcard (48.5) is smoother than RAW onion skin (71.1). Parity achieved.
  Cost: strokes thin ~1px, ink retention 89.5%, some thin strokes fragment
  (components 419 -> 510).

Conclusion: grain reversal is morphological, on the mask, not smoothing of the
image. The grain's footprint is 1-2px boundary protrusions where ink feathered
into board fibers; opening r=1 removes exactly that. Candidate lab feature:
despeckle toggle on the Bands tab (not yet implemented).
