# Virtual raking light via shape-from-shading

2026-10-12. `scripts/virtual_raking.py`.

## Correction that enables this

The letter "scans" are **camera photos**, not flatbed scans. They contain real
directional shading (visible in paper wrinkles and creases), so the earlier
"flatbed diffuse lighting kills the signal" reasoning is superseded. No EXIF
survives on any source image, so light direction is estimated per photo.

## Method

1. **Light azimuth estimate.** Fit a plane to the log-image on paper-only
   pixels after heavy blur (sigma 60). The brightness gradient points toward
   the lamp. (Vignetting can bias this; treat as approximate.)
2. **Ink masking.** Local background subtraction + Otsu + dilation (same as
   `emboss_sweep.py`). Ink pixels are filled with the local paper value so
   they inject no false relief — covered regions render flat, never invented.
3. **Relief shading.** High-pass of the illumination-flattened paper image.
   Under Lambertian + uniform-albedo assumptions this is the surface-gradient
   component *along the original light azimuth*. The perpendicular component
   is unobservable from a single photo — a hard, honest limit.
4. **Virtual lamp sweep.** 8 renders at azimuths relative to the estimated
   light: 0 (same side, amplified), 180 (lamp swung to the other side —
   relief inverts, grooves flip dark/bright), and the rest of the circle.
   Gain ~5x models the contrast boost of 12-degree grazing incidence versus
   an assumed 45-degree photo light. The +/-90 renders are honestly flat:
   there is no cross-light signal in one photo.

An early integration-based height field produced rotation stripe artifacts
and was dropped; the direct relief-shading render is both cleaner and more
defensible.

## Estimated light azimuths (x-right, y-down, 0 = east)

| target   | azimuth | reading          |
|----------|---------|------------------|
| blot39   | -59.8°  | upper right      |
| scan17   | -122.7° | upper left       |
| scan51b  | +50.0°  | lower right      |
| scan51l  | +97.2°  | below            |
| berliner | +50.3°  | lower right      |

scan51b and berliner share ~50°: likely photographed in the same session.

## Validation

- **Berliner control (positive):** the overwrite scribble and the underlying
  writing both show clear raised-ink relief. The method detects real relief.
- **blot39 wrinkles:** the big diagonal crease and paper grain render
  strongly and invert correctly when the virtual lamp swings 180°.
- **scan17 visible writing:** surrounding ink strokes show raised relief;
  the pipeline is not blind.

## Verdict per target

- **blot39:** micro-relief emerges crisply on paper, none at the blot
  margins suggests hidden grooves or letterforms. Blot interior is masked
  flat by design. **Negative for embossed writing.**
- **scan17 block:** margins show normal paper + raised surrounding writing,
  nothing anomalous; block interior masked. **Negative.**
- **scan51 dabs:** dab margins show proud-ink edges, nothing underneath
  (masked). **Negative.**
- **berliner:** control positive; not a redaction target.

## Bottom line

Virtual raking works as a technique — the renders show genuine micro-relief
that flips correctly with lamp position, which the flatbed assumption had
ruled out. But on every redaction target it finds only paper texture,
wrinkles, and the raised edges of visible ink. No hidden writing via
embossing at any margin. Combined with the band-slicing and GrabCut
negatives, the covered text is unrecoverable from these photos; the
physical originals under real raking light remain the only route.

## Limits (stated plainly)

- Single photo: no perpendicular-gradient signal; +/-90 renders are null.
- Masked ink regions are filled, never reconstructed: relief *under* opaque
  ink is invisible, only margins are testable.
- JPEG blocking, unknown original light elevation (gain ~5x assumes 45°),
  vignetting bias in the azimuth fit.
