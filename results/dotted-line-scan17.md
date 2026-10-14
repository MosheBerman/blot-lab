# Task A results: Scan-17 block dotted rows — Chroma / Directional / Gabor / Ridge sweep

Image: "Scan 17 block" (1024×388). All sliders keyboard-driven. Judgments: invisible / faint / clear (Chroma); isolated / not isolated (others).

## Part 1 — Chroma tab, View=Mask (27 combos)

Width 4: 85 invisible (specks only); 90 faint; 95 faint (fragmented); 100 clear; 105 clear (best at w4); 110 faint; 115 faint; 120 faint; 125 faint (sparse traces).
Width 8: 85 faint (denser, no clean rows); 90 faint; 95 clear; 100 clear; 105 clear (best overall — densest, cleanest two rows); 110 clear; 115 clear; 120 clear; 125 clear (traceable, weaker).
Width 16: 85 faint (dense blobby, muddled); 90 faint (blobby); 95 faint (dense blob); 100 clear (blobby); 105 clear (tied best — dense clear rows); 110 clear; 115 clear; 120 clear; 125 clear.

## Part 2 — Chroma at best center (105/8)

View=Saturation: rows NOT visible (rows indistinguishable inside black block). View=Hue: clear (two rough dotted rows as lighter dotted bands).

## Part 3 — Directional tab, Rows, k 1.0/1.5/2.0/2.5 × win 15/31/47/61 (16 combos)

ALL not isolated. Every combination rendered dense speckle/handwriting texture across the whole postcard (handwriting and the 1927 postmark visible); dotted rows never distinguishable. Best threshold/window: none — the filter responds to all horizontal handwriting texture, which overwhelms the faint dotted signal.

## Part 4 — Gabor tab, Ink axis, Orientation=0, Gain=6, λ 4/6/8/12

ALL not isolated. Horizontal ink texture everywhere; λ12 showed the block as a dark blob with handwriting strokes; rows not separated.

## Part 5 — Ridge tab, Dark, Sensitivity 0.01/0.02/0.05

ALL not isolated. Dense white ridge outlines across the whole postcard at every sensitivity; rows not separated.

## Observations

The feature is a hue-specific ink signal: the Chroma mask isolates the two rough dotted horizontal rows only near hue center 95–125, peaking at 105, width 8–16. Width 4 thins the rows; width 16 densifies but adds blob noise; below ~95 only specks remain; above 125 the rows fade. Saturation view hides the rows; Hue view renders them as brighter bands. Edge/texture methods (Directional rows, horizontal Gabor, Ridge) all fail because they respond to the postcard's overall handwriting, which overwhelms the faint dotted signal.

## Screenshots (task-attached)

1. Chroma Mask 105/8 — best isolation: sandbox://workspace/user/media_library/browser_screenshots/7d/7d2296dfa2a149a0082c9dff2674f47775545756dc170a6b1c9d9d0b43ab160a.png
2. Chroma Hue view 105/8: sandbox://workspace/user/media_library/browser_screenshots/02/02f1f0cab6e75da4ee86ddc3c353e61848f5ef029d177ad9620ce2d121cac448.png
3. Chroma Mask 105/16 (third best, nearly identical rows, slightly denser/blobbier) — captured in-session but the path was not exposed; not attached.

## Re-run on cropped image (1308x446, margins removed)

Same settings, whole set repeated: centers 100/105/110 w8, 105 w16, union 95-125 step5 w8, plus edge-distance test. Result: 126 dots at 105/8, ALL within 3px of the block edge (median 0.0), zero in the interior, zero on open paper. Row-fit residuals still ~28-30px (edge-tracing, not clean rows). Verdict unchanged: the dotted rows are edge pixels of the covering ink, not under-text. Annotated outputs in ~/workspace/your_files/dot-trace/crop2/.
