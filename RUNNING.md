# AMPEROR café — landing site: how to run

No build step. It's a single self-contained `index.html` (inline CSS/JS) plus
scroll-scrubbed image-frame sequences. Google Fonts is the only external request.

## Quick start

```bash
cd kured-cafe-landing
python3 serve.py
```

Then open **http://localhost:5501/** — that's the finalized site.

`serve.py` just adds no-cache headers so the frame sequences never show a stale
frame. Any static server works (e.g. `python3 -m http.server 5501` from inside
`site/`). The in-editor preview serves the same `site/` folder on port **5510**.

Ctrl+C to stop.

## What's here

```
site/
  index.html                 the whole site (self-contained)
  assets/
    walkin/     wi_001..128   café walk-in glide (hero → QR table)
    turntable/  t_001..120    finished-drink turntable (warm close)
    promo-latte.webp
    promo-matcha.webp
    promo-strawberry.webp
    qr-brand.png              branded QR composited onto the table card
serve.py                     no-cache static server
```

The scroll journey: hero (café walk-in, "The café that comes to you.") → QR
table → phone rises and runs the scan → menu → cart → order flow → order-placed
confetti → drink turntable → owner dashboard reveal → footer.

## Notes
- The folder is still named `kured-cafe-landing` for path stability
  (`serve.py` and the editor launch config reference it by absolute path).
  The site brand itself is **AMPEROR**.
- Previous page versions, the `versions/` archive, source clips, and frame
  backups were removed when this version was finalized.
