# Letter Forensics Lab

Microsite for two image-analysis experiments on the Bermann family letters (1940–42):

1. **Blot detector** — custom OpenCV detector (ink-density + saturation gating) swept over 53 PDFs / ~100 pages to find ink blots that may hide words. Found the two known blots plus new accidental drips/stains; no hidden words.
2. **Stylus-press lifting** — attempt to recover paper embossing from flat scans by ignoring ink and enhancing paper texture. Honest negative: the scanner lighting destroys the signal.

Open `index.html` in a browser. Mobile-friendly, images lazy-loaded.

Detector code lives with the research notes (not published here).
