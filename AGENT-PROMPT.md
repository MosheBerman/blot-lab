# Blot-lab: shade-isolation extension — agent prompt

Copy everything below the line into a new agent session. Work on your own
branch; open a PR when you have results.

---

You are working on the **blot-lab** repo (`MosheBerman/blot-lab`, private).
It contains image-forensics experiments on the Bermann family letters
(1940–42): a custom blot detector, a stylus-press lifting attempt, and a
multi-pass shade-band isolation script. Everything so far is an honest
negative — no hidden writing found under any blot. Your job is to extend
the work, not to relitigate it.

**Setup**

1. Clone the repo and create your own branch: `git checkout -b <your-name>/<experiment>`.
2. Read `README.md`, `TECHNIQUES.md`, and `index.html` first. `TECHNIQUES.md`
   is the lab notebook: every experiment gets algorithm, parameters, and
   measured outcome. Append yours; never repeat a dead end blind.
3. Python 3 with OpenCV (`cv2`) and NumPy. PIL only needed for the GIF.

**The current state**

- `scripts/shade_isolate.py` isolates blot shade bands in multiple passes:
  global shade bands (6/12), row/column/diagonal z-score deviation from the
  local wash (k=1.5/2.5), 2× multiscale, plus composite/depthmap/GIF
  outputs. Run: `python3 scripts/shade_isolate.py img/blot39.jpg --out img/passes/blot39`.
- Letter-39 blot verdict: nothing recoverable — darkest bands show only
  blot-edge fragments; directional maps show wash texture only.
- `img/` holds the original samples — do not modify them. Page images live
  in `img/page/` (tight experiment-region crops).

**What to try next (pick one)**

1. **Chroma separation.** The current script works in lightness (LAB L)
   only. The blot is blue/teal; hidden writing might differ in hue, not
   lightness. Try per-channel and hue-angle banding.
2. **A different blot.** Letter 45's scribble (`img/blot45.jpg`) was read by
   grammar ("Berliner"), never by isolation. Run the script on it and on
   any `img/find*.jpg` candidate with a non-saturated core.
3. **Texture/orientation filters.** Gabor banks tuned to handwriting stroke
   widths (3–8 px at this scale), applied per shade band.
4. **Bleed-through.** Check the reverse side of the letter-39 scan for
   show-through that the blot might be covering from behind.

**Rules**

- Every script goes in `scripts/` and gets committed. No throwaway code
  left only in /tmp.
- Every experiment gets a `TECHNIQUES.md` entry: algorithm, parameters,
  measured outcome — including negatives.
- The repo is private because it contains family-letter images. Do NOT
  enable GitHub Pages, make anything public, or publish images elsewhere
  without asking Moshe first.
- Report honest negatives as clearly as positives. "No letterforms
  survive" is a result.
