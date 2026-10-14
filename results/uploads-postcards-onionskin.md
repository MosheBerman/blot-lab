# Task D results: postcards + onion skin isolation test (5 built-in samples)

Procedure per image: Tune defaults; Bands n=12 Window sweep P0–P11; Chroma 105/8 then 20/8 Mask; Gabor Luminance λ8 gain 6, O0/45/90; Directional Rows k1.5 win31. Keyboard-only sliders.

## Scan 5 postcard (address)
- Bands: P0 good; P1 very good bolder; P2 CLEANEST (solid white-on-black, paper suppressed); P3–P5 thinner, more speckle; P6 polarity flip, heavy noise; P7–P11 noisy fragmented.
- Chroma 105/8: specks only, poor. 20/8: stamp + postmark strong; handwriting fragmented/dotted.
- Gabor O0/O45/O90: readable embossed. Directional Rows: edge-sketch with horizontal streak noise, poor.
- Cleanest: Bands P2.

## Scan 5 postcard (message)
- Bands: P0 excellent bold; P1 CLEANEST (boldest, full message crisp); P2 excellent; P3+ thinning + speckle; P6 polarity flip noisy; P11 decent black-on-white.
- Chroma 105/8: poor. 20/8: good, message readable though thin/dotted, left-edge speckle.
- Gabor all orientations: excellent, full message crisp. Directional Rows: very noisy, poor.
- Cleanest: Bands P1.

## Scan 17 postcard (full)
- Bands: P0–P4 good building solidity; P5 CLEANEST (full message + address solid white-on-black); P6 ≈P5; P7–P10 degrading; P11 good black-on-white.
- Chroma 105/8: only stamp label area. 20/8: stamps/postmark strong; handwriting fragmented.
- Gabor all: excellent, full card readable. Directional Rows: very noisy, poor.
- Cleanest: Bands P5.

## Letter 8 onion skin (p1)
- Bands: P1 very good; P2 CLEANEST (bold solid white-on-black, minimal background); P3+ thinning; P11 good black-on-white.
- Chroma 105/8: fragmented/dotted, poor. 20/8: poor to moderate.
- Gabor O0 very good; O45 excellent crisp; O90 very good. Directional Rows: extremely noisy, very poor.
- Cleanest: Bands P2.

## Letter 8 onion skin (p2)
- Bands: P1 very good; P2 CLEANEST (same bold solid pattern as p1); P11 good black-on-white.
- Chroma 105/8: scattered dotted specks, poor. 20/8: fragmented/dotted, moderate/poor.
- Gabor O0 very good; O45 excellent very crisp; O90 very good. Directional Rows: extremely noisy, text barely distinguishable, very poor.
- Cleanest: Bands P2 (Gabor O45 close second).

## Postcard board vs onion skin

Onion skin isolates handwriting better. Its thin, uniform, low-texture substrate lets Bands Window P1–P2 render ink as bold solid strokes with almost no paper interference, and Gabor 45° yields near-print clarity on both pages. Postcard board also isolates well with Bands, but heavier texture and competing printed elements (stamps, postmarks, address rules) intrude more, needing tighter band selection (P5 for dense Scan 17). Chroma masks contribute nothing for black handwriting on either substrate; only colored postal markings. Directional Rows too noisy on all five. Recommended: Bands n=12 Window P1–P2 (P5 dense cards); Gabor Luminance λ8 gain 6 O45.

## Screenshots

Attached (verified): scan17 P5, onion p1 P2, onion p2 P2.
- sandbox://workspace/user/media_library/browser_screenshots/54/54e65dae1a7594458a95a0c25fb9cf39bde30747ec2ec1c4a1b06921acbf712f.png
- sandbox://workspace/user/media_library/browser_screenshots/e0/e014c8deb0c4f10a1e69532189c7dbc359418210e0a2c34b489ac5336bec52cb.png
- sandbox://workspace/user/media_library/browser_screenshots/03/03d387dedd7deafee475be12f7f20523216c0df10ae972313c527c3b53d04fb4.png
Best views for scan5-address (P2) and scan5-message (P1) were captured and verified in-session but their files were cleaned up before handoff; findings stand on direct observation.
