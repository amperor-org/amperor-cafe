# amperor-cafe

Marketing landing site for **AMPEROR café** — a QR‑code table‑ordering experience.
Scan the code on your table, order in seconds, no app and no queue.

The page is a single cinematic scroll journey: a warm café walk‑in → the QR table →
a phone‑driven **scan → menu → cart → order** flow → an order‑placed moment →
a finished‑drink turntable → an owner dashboard reveal.

**Live:** https://amperor-cafe.vercel.app · **Full docs:** [DOCS.md](DOCS.md)
(architecture, every design decision, video‑pipeline constraints, deploy/redeploy playbook, roadmap).

## Tech

Static, no build step. One self‑contained [`site/index.html`](site/index.html)
(inline CSS/JS) driving scroll‑scrubbed WebP frame sequences on `<canvas>`.
Google Fonts is the only external request.

## Run locally

```bash
python3 serve.py
```

Then open **http://localhost:5501/**. `serve.py` adds no‑cache headers so the
frame sequences never show a stale frame. Any static server works. See
[RUNNING.md](RUNNING.md) for details.

## Structure

```
site/
  index.html                the whole site (self‑contained)
  assets/
    walkin/    wi_001..128   café walk‑in glide (hero → QR table)
    turntable/ t_001..120    finished‑drink turntable (warm close)
    promo-*.webp             menu imagery
    qr-brand.png             branded QR composited on the table card
serve.py                    no‑cache static server
```
