# Berliner baseline: overwrite-separation algorithms

**Date:** 2026-10-12
**Ground truth:** letter 45, the overwritten word is "Berliner" (read 2026-10-07).
The writer scribbled over the "B" and struck through "erlin" with the same pen,
pressed harder. Task: isolate the underlying letterforms from the overwrite,
scored against the known reading.

## Ink analysis

Both inks share one hue (H 103-113, median 107). Separation lives entirely in
lightness/saturation: heavy overwrite application is darker (L < 100) and more
saturated (S > 150); normal writing sits at L 105-165. Light overwrite strokes
(same pen, normal pressure) are color-identical to the underlying writing.

## Approaches and scores

Reference masks: `blob_ref` = ink with L < 90 (unambiguous overwrite core,
1243 px); `write_ref` = ink with L 105-165 (unambiguous writing, 4128 px).
Metric: fraction of blob_ref removed / fraction of write_ref kept.

| Approach | blob removed | writing kept | verdict |
|---|---|---|---|
| A1 k-means (L,S), k=2 | 0.91 | 0.68 | boundary cuts through the writing distribution; eats 32% of writing |
| A2 parametric L<100 & S>150 | 0.84 | 1.00 | simple, nearly best; best effort-to-result ratio |
| A3 k-means k=3 | 0.81 | 0.85 | mid-tone scribble overlaps writing in (L,S); no clean third class |
| **B seeded stroke growth** | **1.00** | **1.00** | removes most overwrite, but fragments letterforms at crossings |
| **C GrabCut** | **0.92** | **1.00** | **winner: B reads cleanly, best letterform coherence** |
| D1/D2 morphological (r=6) | 0.73 | 0.92 | punches holes in the B's own thick downstroke |

**Winner: C, GrabCut.** Init: sure-background = L < 85 pixels, sure-foreground =
light writing pixels, 5 iterations on the ROI. The color-distribution model is
forgiving at stroke crossings: darkened crossing pixels stay classified as
writing because the sure-foreground seeds anchor the distribution.

**Why B loses despite perfect scores:** the seeded growth (BFS from light
writing pixels through thin, writing-colored ink) excludes any pixel the
scribble darkened - including the B's own strokes where the scribble crosses
them. The B comes out fragmented with white gaps at every crossing. It is the
better *background cleaner* (475 residual mid-tone px in the B zone vs C's
837) but the worse *letterform recoverer*. The scores don't capture
coherence; the eye does.

**Why D fails structurally:** thickness does not equal ink identity. The B's
own downstroke is as thick as thin parts of the blob, so opening at r=6
removes blob and letterform alike.

## Fundamental limit

Light overwrite is unrecoverable by any color method: same pen + normal
pressure = identical (L,S) to the underlying writing. Only the heavy, dark
application separates. The residual scribble in every output is light
overwrite, and no tuning removes it without eating writing.

## Generalization

- **Scans 17/51 (opaque redactions): no recovery value.** The technique would
  cleanly *mask* the redactions (uniform dark/saturated ink separates
  perfectly), but there is nothing underneath - the text is destroyed, not
  covered. The isolation passes already confirmed opacity. Useful only for
  presentation cleanup, not for reading what was redacted.
- **Letter-39 core: no.** The calibration (img/passes/calibration/) proved the
  saturated core is beyond the method's sensitivity at full opacity. There is
  no underlying signal to isolate - same reason the shade bands found nothing.
- **Where it does generalize:** partial overwrites with differential ink
  application, i.e. exactly this geometry - crossed-out words elsewhere in the
  corpus where underlying text peeks through lighter scribble. Recommended
  pipeline for such cases: A2 parametric gate as a fast first pass, C GrabCut
  for the final recovery.

## Files

- `scripts/berliner_baseline.py` - all four approaches + scoring
- `berliner_roi.png` / `berliner_roi_3x.png` - working ROI
- `roi_blobref_overlay.png` - blob core (red) over original
- `A1_kmeans_kept.png`, `A2_parametric_kept.png`, `A3_k3_light_mid.png`,
  `B_seeded_growth_kept.png`, `C_grabcut_kept.png`, `D1_tophat_kept.png`,
  `D2_opening_kept.png` (+ `_removedred` variants)
- `comparison_panel.png`, `b_zoom_panel.png`, `final_compare.png`,
  `BC_fullword.png` - visual comparisons
- `scores.json` - numeric scores
