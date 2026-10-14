# Lighter-blot calibration — natural targets from scans 33 and 40

Date: 2026-10-12. Script: `scripts/lighter_blot_calibrate.py`
(+ one hand-targeted ROI for the scan-33 wash).
All outputs in this directory.

## Why

The synthetic calibration (`img/passes/calibration/`) set the detection
floor on artificial blots: text recoverable at ≤0.5× the letter-39 blot's
opacity, marginal at 0.75×, gone at 1.0×. Scans 33 p1 and 40 p1 carry REAL
lighter marks (earlier called drips/stains/foxing — the opacity is what
matters), giving natural calibration points on the same scale:

    s_eq = mean over mark px of clip((249 − L) / (249 − 128), 0, 1)

(249 = blot-39 paper L, 128 = blot-39 core L.)

## Targets

**scan33_wash** (hand ROI x[640:880] y[770:1160]): diffuse gray-blue wash
running through readable text ("durchführen", "geht es Euch", "wird der").
s_eq = 0.41. A true positive control: text definitely present under a
translucent wash.

**scan40_b0** (auto, blue gate): saturated blue drip over text ("Pakete"
area). s_eq = 0.95.

**scan40_b1 / scan40_b2** (auto, blue gate): smaller drip fragments.
s_eq = 0.77 / 0.79.

(Note: the auto-detector's scan33_b0/b1/b2 hits were faint stain regions,
s_eq 0.43–0.49, not the visual drip — the hand-targeted wash above is the
primary scan-33 data point.)

## Results vs. synthetic prediction

| target | s_eq | synthetic predicts | observed |
|---|---|---|---|
| scan33 wash | 0.41 | works (≤0.5) | **WORKS** — 12-band composite shows color-separated stroke fragments; row-directional k=1.5 shows recognizable glyph fragments |
| scan40 b1/b2 | 0.77/0.79 | marginal (~0.75) | **MARGINAL** — faint internal structures in the composite, scattered fragments in the directional pass, not readable |
| scan40 b0 | 0.95 | fails (1.0) | **FAILS** — composite is a smooth concentric shade gradient; directional pass shows only the drip's edge outline, no strokes inside |

Every natural target lands exactly where the synthetic curve says it
should. The calibration is confirmed on real data.

## What this says about the real-world detection floor

- The method genuinely recovers writing through translucent washes down
  to about half the letter-39 blot's opacity — demonstrated, not assumed.
- The floor is sharp: between s_eq 0.41 (clean recovery) and 0.77
  (unreadable) the signal collapses. The letter-39 blot's core (s≈1.0)
  is far above it.
- Practical rule for future targets: measure s_eq first. If ≤0.5, run
  the passes and trust a negative. If ≥0.75, lightness-based separation
  cannot reach it — go to chroma/hue or the physical original.
- The scan-33 wash doubles as a regression test: any future algorithm
  change must still recover strokes there, or it regressed.

## 2026-10-14 — Pixel-level re-audit of the scan33 "WORKS" verdict

Working backwards from the extraction pixels (not the visual impression):

- The composite's color is dominated by the wash itself: bands 10+11 (lightest)
  hold 54% of all colored pixels. Most of what the eye reads as "fragments"
  is wash texture in different shades, not separated text.
- Dark bands 0-3 (where hidden text would have to appear): 1.3% of ROI,
  173 components, median 5 px, median elongation 1.25 (only 11% exceed 2:1).
  Real strokes are elongated; these are mostly round specks.
- Directional passes weaker still: 281 components, median 3 px, median
  elongation 1.20 — at the noise floor.
- Dense rows are consistent across methods (~88, ~150, ~210, ~311, ~388) but
  irregularly spaced; no clean text-line rhythm.
- Geometry check: the composite is 320x470 but the documented hand ROI
  x[640:880] y[770:1160] is 240x390. Template-matching the dark-band mask
  against scan33-1.png at scales 0.5-1.5 finds no convincing source region
  (best normalized score 0.37). The extraction's true source crop is
  unverified; any published source-vs-extraction pairing must re-derive it.

Revised verdict: the scan33 wash extraction does NOT demonstrate recovered
text at the pixel level. The earlier "WORKS" was a visual read of wash
texture. Do not cite scan33 as a true-positive control without new evidence.
