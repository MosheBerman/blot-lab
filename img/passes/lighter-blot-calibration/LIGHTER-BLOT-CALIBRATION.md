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
