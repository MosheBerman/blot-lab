# Calibration — ground-truth validation of shade-band isolation

Date: 2026-10-12. Script: `scripts/calibrate.py` (uncommitted).
All outputs in this directory (106 files).

## Method

The real letter-39 blot was modeled as a variable-opacity wash:
- Opacity map estimated per-pixel from the real blot
  (paper L=249 reference, core L=128; mean blot opacity 0.67).
- Ink color sampled from the darkest 10% of blot pixels: BGR (154, 138, 87).
- The wash was overlaid on clean readable text
  (`img/blot39.jpg` top region: "zugeschrieben / was unser / hoffen daß")
  at opacity scales s = 0.5, 0.75, 1.0, 1.25
  (s=1.0 reproduces the real blot's opacity).
- Each synthetic was run through the 12-band + row-directional passes
  with the real blot mask. A half-size-glyph variant was tested at s=1.0.

## What working detection looks like

- **s=0.5:** band composites show color-separated letterforms; the
  row-directional pass (k=1.5) shows recognizable glyph fragments.
  The method is validated — it genuinely recovers text through a
  translucent wash. See `S_s0.5_A12_composite.png`, `S_s0.5_rows_k1.5.png`.
- **s=0.75:** marginal. Faint stroke structures in the composite, not
  readable. See `S_s0.75_A12_composite.png`.
- **s=1.0 (real-blot opacity):** nothing. The composite is mottled wash
  texture, visually indistinguishable from the real blot-39 negative.
  The directional passes show texture only.
- **s=1.25:** fully opaque; darkest two bands hold 16,738 px vs 4,603 at
  s=1.0 — the wash saturates the dark bands completely.
- **Size:** half-size glyphs at s=1.0 fare worse than full-size, as
  expected; no separate size floor was established beyond this.

## The measured floor

Text remains recoverable at wash opacity ≤ ~0.5× the real blot
(mean opacity ≈ 0.33), marginal at ~0.75×, unrecoverable at 1.0×.
The most sensitive pass family is the directional (row-wise) z-score
deviation, which shows glyph fragments where the band composite only
shows color smears.

## What this implies for the letter-39 negative

The earlier verdict ("honest negative — nothing recoverable under the
blot") must be restated with the calibration caveat:

**The method cannot see through the real blot's opacity even when text
is definitely present.** The s=1.0 synthetic negative looks exactly like
the real blot-39 negative. Therefore the real negative is
*uninformative about the blot's opaque core*: it establishes the method's
limit, not the absence of writing.

What the negative *does* establish: within the method's demonstrated
sensitivity (wash opacity ≤ ~0.5× real), no text was found — i.e., the
blot's translucent fringes yielded nothing. The saturated core
(L≈128, opacity ≈1) is beyond this method's reach, by measurement.

## Consequences for next steps

- Do not cite the blot-39 isolation passes as evidence that no writing
  hides there. Cite them as evidence the blot is too opaque for
  lightness-based separation.
- Methods that could reach the core must exploit something other than
  lightness: chroma/hue separation (the ink is blue-teal, the writing ink
  is gray-blue — a hue difference may survive where lightness does not),
  or the physical original (raking light).
- Any future "negative" claim on a new target must be accompanied by a
  calibration at that target's opacity, per this procedure.
