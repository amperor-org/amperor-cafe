# AMPEROR café — Project Documentation

Everything needed to understand, run, edit, and deploy this site. Written to be
picked up cold months from now.

- **Live:** https://amperor-cafe.vercel.app
- **Repo:** https://github.com/amperor-org/amperor-cafe (public, branch `main`)
- **Repo folder:** `kured-cafe-landing` (legacy name — the brand is AMPEROR)
- **The whole site is one file:** [`site/index.html`](site/index.html) (self‑contained: inline CSS + JS)

> **Naming:** the brand is **AMPEROR**. The local folder is still `kured-cafe-landing`
> and the repo domain owner is `amperor-org` — see *Brand history* below. Don't let
> the folder name confuse you; the product is AMPEROR café.

---

## 1. What it is

A marketing landing site for a **QR‑code table‑ordering** experience: a guest scans
the QR on their café table, orders on their phone (no app, no queue, card payment in
the chat), and the order lands on the café's bar dashboard — already paid.

Context: built by **AMPEROR** (agency, Dubai). Originally branded for a client café
("KURE'D"); the current build is AMPEROR‑branded and used as the product showcase.
The copy is intentionally generic/product‑led so it reads as AMPEROR's own demo.

---

## 2. The experience (one cinematic scroll)

The entire page is a single **sticky‑pinned scroll journey** — you scroll vertically
and a timeline scrubs. In order:

1. **Hero** — warm café walk‑in behind "The café that comes to you." Text sits on a
   clean dark spotlight so it never fights the photo (see *Gotcha: hero text*).
2. **Glide to the table** — the walk‑in footage plays forward, settling on a table
   with the branded QR card.
3. **The lights dim** — a dark overlay fades in; the scene shifts from warm café to a
   focused, AWA‑style dark ordering stage.
4. **Phone rises & scans** — a CSS phone mockup rises into center and "scans" the QR
   (the QR is shown *on the phone screen*), lands a **Connected ✓ / Table 3** state.
5. **Phone travels the deck** — as you keep scrolling, four full‑screen panels scroll
   vertically (Scan → Build order → Pay → Order placed) while the phone weaves
   **center → left → right → center** and its screen cross‑fades scan → menu → cart →
   order‑placed.
6. **Order placed → confetti** — a compositor‑driven CSS confetti burst.
7. **Warm turntable close** — the overlay lifts, a finished‑drink turntable rotates
   ("It comes to you."), resolving back to warmth.
8. **Owner dashboard** — a separate section reveals a bar dashboard with animated
   live‑order stats (Covers / Revenue / Avg time).
9. **Footer** — 3‑column, "Book a demo" → `mailto:jawad@amperortech.com`.

---

## 3. How it works (architecture)

No build step, no framework, no dependencies. One HTML file with three inline
`<script>` blocks. Google Fonts (Playfair Display + Inter) is the only external
request.

### 3.1 Scroll‑scrubbed canvas frame sequences
Two cinematic shots are **WebP frame sequences** drawn to `<canvas>` and scrubbed by
scroll — not `<video>` (gives frame‑exact control + no codec/pause jank):

- `walkin/  wi_001..128.webp` → hero walk‑in glide (`walkCanvas`)
- `turntable/ t_001..120.webp` → finished‑drink turntable (`ttCanvas`)

`loadSeq(canvasId, prefix, count, onload)` (index.html ~L331) preloads all frames and
exposes `draw(frac)`:
- `draw` maps `frac`→ frame index `round(frac*(count-1))` and **only repaints when the
  index changes** (`last` cache) — the key perf lever.
- Canvas is sized at **DPR capped to 1.25** (retina without the 3× fill cost).
- `pick(i)` falls back to the nearest already‑loaded frame, so scrubbing never blanks
  while images stream in.
- Images use object‑fit **cover** math (fills the pin, center‑cropped).

### 3.2 The master timeline — `render(p)` (index.html ~L356)
`p` is scroll progress 0→1 over the pinned `#journey` section (`prog()` at ~L329, from
`getBoundingClientRect().top` vs scrollable height). Phase map (from the code):

| Phase | `p` range | What happens |
|---|---|---|
| Glide | 0 – ~0.11 | Walk‑in plays to ~72% of frames (`gp=min(1,p/0.09)`); hero cap fades out by ~0.03 |
| Dim | ~0.15 – 0.20 | Dark overlay fades in (`dim` → 0.94), out again at 0.72 |
| Deck | **static until 0.31**, then 0.31 – 0.72 | 4 panels translateY by `(i-si)*100%`, `si = clamp((p-0.31)/0.41)*3` |
| Phone | rises 0.19 – 0.26, exits 0.72 – 0.78 | `PX=[0,-26,22,0]%` x‑travel, `PS=[1,1.05,1.1,1.12]` scale, per section index `si` |
| Scan lands | `p≥0.265 && si<0.45` | `.scanned` class → "Connected ✓" before the phone moves |
| Screens | by `si` | scan→menu (~0.55), menu→cart (~1.6), cart→ok (~2.5) crossfade |
| Placed | `si>2.6` | `.placed` + confetti `.go` fire |
| Turntable | 0.73 – 0.92 | `ttCanvas` fades in (0.73), rotates (`draw` over 0.78–0.92) |
| Resolve | 0.92 – 1 | endveil + endline fade in, "Ordered with a scan." |

**Smooth‑scrub loop** (~L399): `cur` lerps toward `target=prog(sec)` at `0.12`/frame
and only calls `render` when `cur` changes. A `resize` listener **snaps** `cur=target`
and re‑renders (also how you force a static frame for testing — see *Gotchas*).

### 3.3 Performance techniques (these fixed real scroll lag)
- **Frame‑index cache** — redraw canvas only when the frame changes.
- **DPR cap 1.25**.
- **Cover‑hiding** — when opaque deck panels fully cover the screen
  (`covered = deckShow>0.98 && p<0.715`), `cwrap` + `dim` are set `visibility:hidden`
  so the browser stops compositing the café canvases behind them.
- **Panel culling** — off‑screen panels (`|i-si|>1.35`) set `visibility:hidden`.
- **CSS confetti on the compositor** — 28 `<i>` particles animated via CSS custom
  props + keyframes (generated once at ~L353). This **replaced** a JS‑canvas confetti
  that fought the main thread and caused the order‑confirmation jank.
- **No `filter:blur` / `backdrop-filter` on animating elements** — they kill scroll FPS.

### 3.4 The other two scripts
- **Owner dashboard** (~L408) — `IntersectionObserver` (threshold .3) runs a one‑shot
  `countUp()` easing the stat numbers (Covers 42, Revenue AED 3180, Avg 11 min).
- **Nav + reveals** (~L422) — nav gets `.scrolled` past 30px; `.reveal` elements fade
  in via `IntersectionObserver`.

### 3.5 Palette (CSS `:root`)
`--cream:#F5EEE2 · --espresso:#2A2320 · --accent:#C0872E (caramel) · --accent2:#E6B667
(gold) · --bg:#14100C`. Hero headline = cream `#F8F2E7`; "comes to you." = gold
gradient `linear-gradient(100deg,#F1C87E,#D89A3C,#C0872E)`. **Keep this palette** (see
gotcha below).

---

## 4. Project structure

```
kured-cafe-landing/                (folder name is legacy; brand = AMPEROR)
├── site/                          ← what Vercel serves (Root Directory = site)
│   ├── index.html                 the entire site (self-contained)
│   ├── assets/
│   │   ├── walkin/    wi_001..128.webp
│   │   ├── turntable/ t_001..120.webp
│   │   ├── promo-latte.webp / promo-matcha.webp / promo-strawberry.webp
│   │   └── qr-brand.png           branded QR composited onto the table card
│   ├── .vercel/                   project link (gitignored)
│   ├── .env.local                 Vercel OIDC token (gitignored — never commit)
│   └── .gitignore                 (.vercel, .env*) — auto-created by Vercel CLI
├── .github/workflows/deploy.yml   CI — auto-deploy to Vercel on push to main
├── serve.py                       no-cache static dev server
├── README.md                      short intro
├── RUNNING.md                     quick run card
└── DOCS.md                        this file
```

Total repo ≈ 13 MB (mostly the 248 WebP frames), ~260 files tracked in git.

---

## 5. Assets & the video pipeline (important constraints)

The cinematic shots came from **Veo 3** generations, then post‑processed to WebP frame
sequences. Two hard constraints learned the hard way:

1. **Veo cannot render legible text or a scannable QR.** So **all text and the QR are
   composited in code / post**, never baked by the model. The table‑card QR is a real
   QR **warm‑tinted** (dark modules recolored espresso→mocha, proportionally, so the
   video blur blends) with the brand text baked on; the phone‑screen QR is
   `assets/qr-brand.png` shown in the mockup.
2. **Don't regenerate the walk‑in ("Scene 1").** The turntable ("Scene 3") was
   generated as a continuation and is **framing‑aligned** to Scene 1's last frame.
   Regenerating Scene 1 breaks that alignment. If you must change footage, plan to
   redo both and re‑extract frames.

The original Veo `.mp4` clips, older frame backups, and prior page versions were
**removed when this version was finalized** (repo went 236 MB → 13 MB). They are not
recoverable from git (this history starts at "first commit"). If you need to
regenerate frames, you'll re‑generate from Veo, not restore from here.

---

## 6. Key decisions & gotchas

- **Hero text "merging" was a z‑index bug, not a color problem.** `.heroCap::before`
  (the dark overlay) is `position:absolute` and, per CSS paint order, painted *on top
  of* the in‑flow headline — so darkening the overlay to hide the café also dimmed the
  text. Fix: `.heroCap>div{position:relative;z-index:2}` lifts the text above the
  overlay. Now the overlay mutes only the café. **Keep the caramel/gold‑on‑warm
  palette** — switching schemes was explicitly rejected; the goal was only "text not
  merging."
- **Phone is centered** because the QR is centered on the table. It rises to scan
  *before* it starts weaving (scan lands at `p≥0.265`), so the user understands "we
  scanned, now it moves" rather than everything happening at once.
- **The deck stays static until `p=0.31`** — the phone rises and scans on a still
  stage first; only then do the panels start scrolling. This sequencing fixed the
  "everything all at sudden" feedback.
- **Confetti must be CSS/compositor**, not JS canvas — the JS version caused the
  order‑confirmation lag.
- **Browser‑pane screenshots are flaky here** (compositing times out). Verify via
  `getComputedStyle`, `curl`, or network requests instead. To inspect a specific
  scroll state statically: set `window.scrollTo(...)` then dispatch a `resize` event —
  the loop snaps `cur=target` and renders that frame synchronously.

---

## 7. Run locally

```bash
cd kured-cafe-landing
python3 serve.py            # serves site/ at http://localhost:5501 (no-cache headers)
```

Any static server works (`python3 -m http.server 5501` from inside `site/`). The
in‑editor preview serves the same folder on port **5510**.

---

## 8. Deploy & auto-deploy (Vercel)

Hosted on **Vercel**, project **`amperor-cafe`**. Because `index.html` lives in
`site/`, the project's **Root Directory is set to `site`** (Vercel serves `site/` as
the web root).

**Auto-deploy: every push to `main` ships.** The GitHub Actions workflow
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) runs `vercel pull` +
`vercel deploy --prod`, authenticated by the repo secret **`VERCEL_TOKEN`** (a Vercel
access token; the non‑secret Org/Project IDs live in the workflow). So the loop is
just **edit → commit → push → it's live**. No CLI needed.

> It runs through GitHub Actions rather than Vercel's native Git integration, for
> account/permission reasons specific to this repo. The effect is identical
> (push‑to‑deploy); the mechanism is the workflow above.

**Manual deploy** (rarely needed) — trigger the same workflow without a code change:

```bash
gh workflow run "Deploy to Vercel" --repo amperor-org/amperor-cafe
```

Notes:
- The `*.vercel.app` URL is public — good for sharing the demo.
- `site/.env.local` (Vercel OIDC token) and `site/.vercel/` are gitignored — never
  commit them.
- Rotate `VERCEL_TOKEN` anytime at vercel.com/account/tokens, then update the repo
  secret (`gh secret set VERCEL_TOKEN --repo amperor-org/amperor-cafe`).

---

## 9. Roadmap / not yet done

- **PR preview deploys** — extend the workflow to build a preview URL per pull request.
- **Custom domain** (e.g. `cafe.amperortech.com`).
- **Cache headers** for the 248 WebP frames (`Cache-Control: public, max-age=31536000,
  immutable`) via a `site/vercel.json` — faster repeat visits.
- **Responsive / mobile pass** — the journey is tuned for desktop; verify the phone
  mockup, deck captions, and hero clamp on small screens.
- **Rename the folder** `kured-cafe-landing` → `amperor-cafe` (would require updating
  the absolute paths in `serve.py` invocation and `.claude/launch.json`).

---

## 10. History (brief)

Iterated through ~12 versions (walk‑in scan → phone order flow → dark AWA deck →
perf pass → aesthetic pass). On finalize, all previous page versions, the `versions/`
archive, source clips, and frame backups were deleted, `merge4.html` was promoted to
`site/index.html`, and the brand was renamed **KURE'D → AMPEROR**. This repo's git
history begins at that finalized state.
