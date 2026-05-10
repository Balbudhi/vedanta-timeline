# Design Rewrite Plan — Vedānta Interactive Timeline

This plan is concrete and execution-ready. No frameworks, no build step, no graph-layout libraries. The cladogram is fully deterministic from `school_color_token` (lane), `sub_school_shade` (sub-lane offset), and `dates_low/high` (x-position).

---

## §0 — Inspirations and what each contributes

- **AMNH / Hillis–Bull cladograms** — rectilinear lineage edges (vertical stems + horizontal twigs); never bowed beziers across whitespace.
- **OneZoom** — color-by-clade saturation gradient maps cleanly onto our `sub_school_shade` 1–5 palette per school.
- **Open Tree of Life** — sticky clade labels in a left rail, persistent across deep zoom.
- **The Pudding, "How Music Taste Evolved"** — era-band tinting and genre-as-lane reading rhythm.
- **NYT, "How Trump's First Year Compared…"** — swim-lane layout with clean horizontal rules and tight type.
- **Tufte small-multiples** — schools-as-lanes is exactly a small-multiples decomposition of the same x-axis (time).

---

## §1 — Timeline visualization redesign (cladogram swim-lanes)

### 1.1 Lane model

Lanes are ordered top-to-bottom (chosen to minimize lineage-edge crossings between schools that historically dialogued):

| order | lane key | school registry token | display label |
|---|---|---|---|
| 1 | `proto` | `proto` | Proto-Vedānta |
| 2 | `advaita` | `advaita` | Advaita |
| 3 | `bhedabheda` | `bhedabheda` | Bhedābheda |
| 4 | `vishishtadvaita` | `vishishtadvaita` | Viśiṣṭādvaita |
| 5 | `dvaita` | `dvaita` | Dvaita (Tattvavāda) |
| 6 | `acintya` | `acintya` | Acintya-Bhedābheda |
| 7 | `shuddha` | `shuddha` | Śuddhādvaita |
| 8 | `avibhaga` | `avibhaga` | Avibhāgādvaita |
| 9 | `trika-comparator` | `trika-comparator` | Pratyabhijñā / Trika (comparator) |
| 10 | `cross-tradition` | `cross-tradition` | Cross-tradition |

**Lane height: 96px.** Inter-lane gap: 0 (use a 1px `--rule` divider). Sub-lanes within a lane are produced by mapping `sub_school_shade ∈ {1..5}` to a vertical offset:

```
sub_y_offset = round( (shade - 3) * 11 )   // -22, -11, 0, +11, +22 px from lane center
```

Greedy collision resolution **only** kicks in if two thinkers in the same lane × same shade overlap horizontally within 18px; in that case, a tertiary nudge of ±6px is applied to the lower-tier thinker.

Each thinker dot's y-position:
```
y_lane_top + 48 (lane center) + sub_y_offset + collision_nudge
```

### 1.2 Sticky left rail (lane labels)

A 168px-wide left rail (`.lane-rail`) is `position: sticky; left: 0` inside `.timeline-scroller`, painted on top of the scrolling content with `background: var(--bg)` and a `box-shadow: 2px 0 6px rgba(0,0,0,.04)` on its right edge. Each lane label:

- school **display name** (Inter 600, 13px, ink color)
- sub-label: count of thinkers in lane (Inter 400, 11px, muted)
- a 4px-tall × 24px-wide color bar in the school's mid-shade (`color_palette[2]`)
- on hover: short_description tooltip (`<title>` element + `aria-describedby`)

### 1.3 Era backgrounds

Vertical bands behind everything (in SVG, drawn first as `<rect>`s in the era layer, opacity 0.04–0.07):

| era | x-range (year) | tint |
|---|---|---|
| Pre-Śaṅkara | low → 700 | warm gray `#a8a29e` @ 0.05 |
| Classical | 700 → 1100 | blue gray `#94a3b8` @ 0.06 |
| Late-Medieval | 1100 → 1500 | amber `#d97706` @ 0.05 |
| Early-Modern | 1500 → 1800 | violet `#9333ea` @ 0.04 |
| Modern | 1800 → high | teal `#0891b2` @ 0.05 |

Era labels: rendered once at the top of the canvas, Inter 500, 11px, uppercase, letter-spacing 0.08em, muted, `position: sticky; top: 0` inside the scroller, on a translucent off-white strip 24px tall.

### 1.4 Lineage edges (rectilinear cladogram)

Replace the current bowed bezier in `app.js` with a **manhattan-routed** path:

```
M x1 y1
L x1 y1+vertical_stub
L midX y1+vertical_stub      // (skip if same lane)
L midX y2-vertical_stub      // vertical stem
L x2 y2-vertical_stub
L x2 y2
```
Where `midX = x1 + 0.55 * (x2 - x1)` (slight asymmetry reads as parent→child) and `vertical_stub = 8px`. Corners get a 6px rounded join via `stroke-linejoin: round`.

**Same-lane** edges (parent and child in same school): straight horizontal line at the child's y, with an 8px L-shaped stem only if `sub_y_offset` differs.

**Edge styling:**
- `lineage_out` (descent): 1.25px solid, `stroke: var(--dot-color, school mid-shade)`, opacity 0.55.
- `lineage_polemical`: 1.25px **dashed** `4 3`, `stroke: #94a3b8`, opacity 0.65, plus a tiny perpendicular tick at the midpoint indicating direction (`refutes` →, `responded-to-by` ←).
- Hovering a thinker dot raises connected edges to opacity 1.0 and stroke-width 2px (CSS class `.edge--lit`).

### 1.5 Date-range bars

Replace single dot with `(bar + dot)`:
- Bar: horizontal rectangle from `yearToX(dates_low)` to `yearToX(dates_high)`, height 3px, fill = school mid-shade, opacity 0.45, border-radius 1.5px.
- Dot: at midpoint, sized by tier (see §1.6), z-index above bar.
- If `dates_low === dates_high` (single attested year): dot only, no bar.
- If `dates_tier === "oral-tradition-only"`: bar dashed (use SVG `stroke-dasharray` on a `<line>` instead of a filled rect), opacity 0.35.

### 1.6 Tier-based dot sizing

Add a new field consumed but not required: `tier` (1/2/3) defaulting to 2. For now, hardcode tier-1 list in `app.js`:

```
TIER_1 = new Set([
  "shankara","ramanuja","madhva","caitanya","vallabha",
  "madhusudana","vyasatirtha","jiva-goswami","nimbarka",
  "bhaskara","yamuna","sureshvara","mandana-mishra",
  "vijnanabhikshu","appayya-dikshita"
]);
```

Sizes (diameter):
- Tier 1: **18px**, 2.5px white border, 1px outer color ring.
- Tier 2: **12px**, 2px white border.
- Tier 3 / reconstructed / oral-only: **8px**, 1.5px white border, opacity 0.85.

### 1.7 Labels

Default placement: **above** the dot, 8px gap. If a label collides with another already-placed label within ±(labelW/2 + 4px) at the dot's y-band, it flips to **below**. If it still collides, drop the date-meta line (keep only the name) and shrink to 10px.

- Name: Inter 500, 12px, ink (`#1a1a1a`), `background: rgba(255,255,255,.92)`, padding `1px 5px`, border-radius 2px.
- Date-meta: directly under name, EB Garamond italic 11px, muted; format `c. 788–820` or `fl. c. 700`.
- Tier-1 names: Inter 600, 13px, no background tint (drawn above bands so legible).
- Hovered/active thinker label gets a 1px solid border in school color and zIndex 5.

### 1.8 Pixel spec (canonical)

```
--lane-h: 96px;
--lane-rail-w: 168px;
--era-strip-h: 24px;
--axis-h: 28px;
--dot-tier1: 18px;
--dot-tier2: 12px;
--dot-tier3: 8px;
--edge-w: 1.25px;
--edge-w-lit: 2px;
--label-fs: 12px;
--label-fs-tier1: 13px;
--datemeta-fs: 11px;
--year-tick-fs: 11px;
--px-per-year: 1.9;   // up from 1.6 — relieves crowding
```

Total canvas height ≈ `era-strip + (10 lanes × 96) + axis = 24 + 960 + 28 = 1012px`. The `.timeline-scroller` becomes both x- AND y-scrollable; sticky left rail handles horizontal scroll, sticky era strip handles vertical (top: 0). On desktop, the visible viewport at 1080p shows ~7 lanes at once; user scrolls vertically to see remaining lanes.

### 1.9 Scroll-snap

**Do not** use `scroll-snap-type` on the horizontal axis — it fights free-exploration. Smooth scroll on programmatic centering only (already in code).

---

## §2 — Detail pane redesign

### 2.1 Layout & width

- Open width: **62vw** on desktop (≥1024px). Timeline pane gets 38vw.
- Tablet (720–1023px): 70vw.
- Mobile (<720px): 100vw, full screen overlay (already present, confirm).
- Animate via `grid-template-columns` transition, 320ms cubic-bezier(.4,.0,.2,1).
- Inner content max-width: 760px, centered with `margin: 0 auto`, padding `40px 56px 96px`.

### 2.2 Typography scale (detail pane)

| element | font | size | weight | line-height | notes |
|---|---|---|---|---|---|
| `h2` (thinker name, IAST) | Inter | 36px | 600 | 1.15 | letter-spacing -0.015em |
| name romanization (under h2) | EB Garamond italic | 16px | 400 | 1.3 | muted, optional |
| `.meta` row pills | Inter | 12px | 500 | 1 | school + tier + extra |
| `.dates-line` | EB Garamond italic | 14px | 400 | 1.4 | "c. 788–820 CE · dates by textual consensus" |
| `.thesis` (lead paragraph) | EB Garamond | **22px** | 400 | 1.55 | drop-cap-style left border 3px in school color, `padding-left: 18px` |
| `h3` section heads | Inter | 12px | 600 | 1 | uppercase, letter-spacing 0.1em, muted, top-margin 40px |
| body paragraphs | EB Garamond | 18px | 400 | 1.65 | up from 17 |
| `.work .title` | Inter | 16px | 600 | 1.3 | |
| `.work .ascr` | Inter | 11px | 500 | 1 | uppercase, letter-spacing 0.06em, muted |
| `.work` summary | EB Garamond | 17px | 400 | 1.6 | |
| `.passage .locus` | Inter | 11px | 600 | 1 | uppercase, letter-spacing 0.08em |
| `.passage .sanskrit` | EB Garamond italic | **20px** | 500 | 1.55 | |
| `.passage .english` | EB Garamond | 17px | 400 | 1.6 | |
| `.passage .why` | EB Garamond italic | 14px | 400 | 1.5 | muted |
| `.compclaim .pair` | Inter | 14px | 500 | 1.4 | |
| `.compclaim` body | EB Garamond | 16px | 400 | 1.6 | |
| `.read-full` button | Inter | 13px | 600 | 1 | letter-spacing 0.04em |

### 2.3 Hero thesis

```css
.detail-pane .thesis {
  font-size: 22px;
  line-height: 1.55;
  border-left: 3px solid var(--dot-color);
  padding: 4px 0 4px 18px;
  margin: 18px 0 32px;
  color: var(--ink);
}
```

### 2.4 Engaged-works ↔ key-passages relationship

Restructure so passages are visually nested under their parent work. New rendering:

- One `.work-card` per `engaged_works[]`. Inside it:
  - work title-line (title, IAST, ascription pill)
  - work summary paragraph
  - "Read full work in translation →" inline link (replaces current button styling — see 2.7)
  - **Inline subsection** "Passages from this work" if any `key_passages` have matching `work_id`, listing those passages as `.passage-card`s nested with 16px left padding and a 2px left border in the school's lightest shade (`color_palette[1]`).
- Passages **without** a matching `work_id` (or with `work_id` pointing to nothing in `engaged_works`) get rendered in a tail "Other key passages" section.

CSS sketch:
```css
.work-card {
  background: #ffffff;
  border: 1px solid var(--rule);
  border-left: 4px solid var(--dot-color);
  border-radius: 4px;
  padding: 20px 24px;
  margin: 14px 0;
}
.work-card + .work-card { margin-top: 20px; }
.work-card .passages-nested {
  margin-top: 16px;
  padding-left: 16px;
  border-left: 2px solid var(--school-light, #eee);
}
```

### 2.5 Passage card

```css
.passage-card {
  background: #fbfaf7;          /* warm off-white, contrasts with #ffffff work card */
  border: 1px solid #ece8df;
  border-radius: 3px;
  padding: 18px 20px;
  margin: 10px 0;
}
.passage-card .locus { margin-bottom: 10px; }
.passage-card .sanskrit { margin: 8px 0 10px; }
.passage-card .english { margin: 0 0 12px; }
.passage-card details[open] { background: #fffdf6; padding: 14px 16px; border-radius: 3px; margin-top: 10px; }
.passage-card summary {
  cursor: pointer;
  font-family: var(--sans);
  font-size: 12px; font-weight: 600;
  color: var(--muted);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  list-style: none;
}
.passage-card summary::before { content: "▸ "; transition: transform 160ms ease; display: inline-block; }
.passage-card details[open] summary::before { transform: rotate(90deg); }
```

### 2.6 Pāṇinian breakdown — table form

Replace the current `white-space: pre-wrap` dump. Render an HTML table per category:

```html
<div class="panini-section">
  <h4>Pada-analysis</h4>
  <table class="panini-table">
    <thead><tr><th>Pada</th><th>Stem</th><th>Pratyaya</th><th>Morphology</th><th>Gloss</th></tr></thead>
    <tbody>...</tbody>
  </table>
</div>
```

CSS:
```css
.panini-table { width: 100%; border-collapse: collapse; font-family: var(--sans); font-size: 13px; }
.panini-table th { text-align: left; font-weight: 600; color: var(--muted); font-size: 11px;
                   text-transform: uppercase; letter-spacing: 0.06em; padding: 6px 10px; border-bottom: 1px solid var(--rule); }
.panini-table td { padding: 8px 10px; border-bottom: 1px solid #f0ede5; vertical-align: top; }
.panini-table td:first-child { font-family: var(--serif); font-style: italic; font-weight: 500; }
.panini-section h4 { font-family: var(--sans); font-size: 11px; font-weight: 600;
                     text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted);
                     margin: 14px 0 4px; }
```

Render four such tables: Pada-analysis, Samāsa-vigraha, Kāraka structure, Verbal modality. Skip empty ones.

### 2.7 "Read full work in translation" link

Convert from button to a typographic CTA:

```css
.read-full-link {
  display: inline-flex; align-items: center; gap: 6px;
  font-family: var(--sans); font-size: 13px; font-weight: 600;
  color: var(--dot-color);
  text-decoration: none;
  border-bottom: 1.5px solid currentColor;
  padding-bottom: 1px;
  transition: gap 180ms ease, opacity 180ms ease;
}
.read-full-link::after { content: "→"; transition: transform 180ms ease; }
.read-full-link:hover { gap: 10px; opacity: .85; }
.read-full-link:hover::after { transform: translateX(2px); }
```

Behavior: opens the existing `.reader-modal` with the markdown from `data/full_translations/<thinker>__<work>.md`. The modal already exists; restyle its content per §7.

### 2.8 Comparative-claims

Verdict color-coding becomes the structural anchor: a thick **left border** in verdict color, plus a verdict pill in the upper-right.

```css
.compclaim-card {
  background: #ffffff;
  border: 1px solid var(--rule);
  border-left: 4px solid var(--verdict-color);
  border-radius: 4px;
  padding: 18px 22px;
  margin: 12px 0;
  position: relative;
}
.compclaim-card .verdict-pill {
  position: absolute; top: 14px; right: 18px;
  font-family: var(--sans); font-size: 10px; font-weight: 700;
  letter-spacing: 0.08em; text-transform: uppercase;
  padding: 3px 9px; border-radius: 999px;
  background: var(--verdict-bg); color: var(--verdict-fg);
}
```

Verdict palette (extends existing):
```css
[data-verdict="real-disagreement"]    { --verdict-color: #b91c1c; --verdict-bg: #fee2e2; --verdict-fg: #7f1d1d; }
[data-verdict="terminological"]       { --verdict-color: #1d4ed8; --verdict-bg: #dbeafe; --verdict-fg: #1e3a8a; }
[data-verdict="parallel-structure"]   { --verdict-color: #047857; --verdict-bg: #d1fae5; --verdict-fg: #064e3b; }
[data-verdict="contested"]            { --verdict-color: #b45309; --verdict-bg: #fef3c7; --verdict-fg: #78350f; }
```

### 2.9 Spacing canon

- Section spacing (between `h3` blocks): 40px top.
- Card-to-card spacing: 14px.
- Inside-card padding: 20–24px horizontal, 18–20px vertical.
- Pane bottom padding: 96px (so last card breathes).

---

## §3 — Topbar / header

### 3.1 Compact bar (40px tall)

```
+------------------------------------------------------------------+
| Vedānta — A Realist Tradition   ·  60 thinkers, ~2700 yrs        |
|     [Reading mode] [Legend ▾]                              right |
+------------------------------------------------------------------+
```

```css
.topbar { height: 40px; padding: 0 24px; display: flex; align-items: center; gap: 18px; border-bottom: 1px solid var(--rule); }
.topbar h1 { font-family: var(--sans); font-size: 14px; font-weight: 600; letter-spacing: -0.005em; }
.topbar .subtitle { font-family: var(--sans); font-size: 12px; color: var(--muted); }
.topbar .spacer { flex: 1; }
.topbar .topbar-btn { font-family: var(--sans); font-size: 12px; font-weight: 500; color: var(--ink);
                      background: none; border: 1px solid var(--rule); padding: 5px 10px; border-radius: 3px; cursor: pointer; }
.topbar .topbar-btn:hover { border-color: var(--ink); }
```

`calc(100vh - 96px)` becomes `calc(100vh - 40px)` everywhere.

### 3.2 Move legend → left rail

Delete the topbar `.legend`. The lane rail (§1.2) is the legend: lane label + color bar = legend swatch + name. This deduplicates and recovers vertical space.

Optional: a "Legend ▾" topbar dropdown explains era-band tints, edge styles (solid = lineage, dashed = polemical), and dot tier sizing. This is supplementary, not essential — implement later.

### 3.3 Subtitle copy

Current: "A timeline. Click any thinker."

Replace with: "Sixty thinkers across the Vedāntic schools — Advaita to Acintya-Bhedābheda — read here as constructive variations on a shared realism rather than rival systems." (Note: per project naming rule, do not name the user's thesis.)

---

## §4 — Typography

### 4.1 Confirmed choices

- Body / Sanskrit IAST: **EB Garamond** (already loaded). Excellent diacritic coverage — ā ī ū ṛ ṝ ḷ ṃ ḥ ñ ṅ ṇ ṭ ḍ ś ṣ all render correctly with proper kerning. Confirmed.
- UI / labels / metadata: **Inter** (already loaded). Good x-height, clear at 10–13px.
- Weights to load: EB Garamond 400, 500, 600, 400-italic, 500-italic. Inter 400, 500, 600, 700.

Update the Google Fonts URL:
```html
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 4.2 Fallbacks

```css
--serif: "EB Garamond", "Cormorant Garamond", "Adobe Garamond Pro", Georgia, "Times New Roman", serif;
--sans:  "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
--mono:  ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
```

### 4.3 IAST ligature/diacritic check

EB Garamond handles all required diacritics. **Do not** apply `font-feature-settings: "liga"` to passages — disable common ligatures inside `.passage .sanskrit` to prevent unwanted ct/st/fi ligatures from interfering with transliteration legibility:
```css
.passage-card .sanskrit { font-feature-settings: "liga" 0, "clig" 0; }
```

---

## §5 — Color system

### 5.1 Palette confirmation

The 9-school palette is well-spaced in hue and works at the lane scale. One adjustment: **Bhedābheda (#9333ea violet)** and **Acintya-Bhedābheda (#db2777 magenta)** sit in adjacent lanes (3 and 6) but are visually similar at low saturation. Mitigation: assign Acintya the darker `palette[3]` (#db2777 → #831843 for tier-1 dots in that lane) only if you want stronger separation. Otherwise the era-band tinting and lane separators suffice.

The mid-shade (`color_palette[2]`) is the canonical "school dot color" at tier 1. Use `palette[2]` for all dots and lineage edges; reserve `palette[1]` (light) for nested-passage left borders, `palette[4]` (dark) for hover-lit edges.

### 5.2 Neutral system

```css
:root {
  --bg:           #ffffff;
  --bg-warm:      #fbfaf7;     /* passage cards, reading mode */
  --bg-warmer:    #f5f1e8;     /* lane rail tinted hover */
  --ink:          #1a1a1a;
  --ink-soft:     #3a3a3a;
  --muted:        #6a6a6a;
  --muted-soft:   #9a9a9a;
  --rule:         #e6e6e6;
  --rule-warm:    #ece8df;
  --hairline:     #f0ede5;
  --shadow-sm:    0 1px 3px rgba(0,0,0,.04);
  --shadow-md:    0 4px 12px rgba(0,0,0,.06);
}
```

Off-whites: `--bg-warm` for passage cards (warm cream), `--bg-warmer` for hover/selected rail rows. The detail pane background stays `#fafafa` (cool off-white) so the passage cards' warm cream reads as nested.

---

## §6 — Interactions

### 6.1 Dot states

```css
.thinker-dot .node {
  transition: transform 180ms ease, box-shadow 180ms ease;
}
.thinker-dot:hover .node {
  transform: scale(1.18);
  box-shadow: 0 0 0 1px var(--dot-color), 0 0 0 5px rgba(0,0,0,.05);
}
.thinker-dot.active .node {
  transform: scale(1.3);
  box-shadow: 0 0 0 2px #fff, 0 0 0 4px var(--dot-color), 0 0 0 8px rgba(0,0,0,.06);
}
.thinker-dot:focus-visible .node {
  outline: 2px solid var(--dot-color);
  outline-offset: 4px;
}
```

On hover, also dim every other dot: `.timeline-dots:has(.thinker-dot:hover) .thinker-dot:not(:hover) { opacity: .35; }` — and lift connected lineage edges to opacity 1 (apply `.edge--lit` in JS).

### 6.2 Active state

Open thinker stays "active" until pane is closed. Lineage edges connected to active node also stay lit (slightly more subtle than hover: opacity 0.85, stroke-width 1.75).

### 6.3 Keyboard navigation

- `Esc`: close detail pane (and reading-modal if open).
- `←` / `→`: move to **previous / next thinker in date order** (entire corpus, ignoring lanes — this matches expectation when paging through history).
- `↑` / `↓`: move to previous / next thinker **in the same lane** (within school).
- `r`: toggle reading mode (§7).
- `?`: toggle a small in-page hotkey cheatsheet overlay.
- `Tab`: cycles dots in DOM order (matches date-sort order). Each `.thinker-dot` gets `tabindex="0"` and `role="button"` and `aria-label` matching label text.

### 6.4 Open-pane scroll behavior

Keep current center-the-dot behavior. Refinement: when the detail pane opens, also vertically scroll the lane into view if it's outside the viewport (the canvas is now taller than viewport).

```js
function scrollLaneIntoView(thinker) {
  const laneIdx = LANE_ORDER.indexOf(thinker.school_color_token);
  const yTarget = ERA_STRIP_H + laneIdx * LANE_H + LANE_H/2;
  const sc = scroller;
  if (yTarget < sc.scrollTop + 80 || yTarget > sc.scrollTop + sc.clientHeight - 80) {
    sc.scrollTo({ top: Math.max(0, yTarget - sc.clientHeight/2), behavior: "smooth" });
  }
}
```

### 6.5 Mobile (<720px)

- Detail pane: full-screen overlay (already correct).
- Timeline: lanes become 72px each; lane rail collapses to 110px; sticky.
- Dots: tier 1 = 16px, tier 2 = 11px, tier 3 = 7px.
- Tap target padding: 12px invisible halo on each `.thinker-dot` via `::before`.

---

## §7 — Reading mode

A third mode: hide the timeline entirely; expand detail pane to 100% width with a generous reading column.

### 7.1 Toggle

Topbar button: `[Reading mode]`. Hotkey `r`. When active:
- Body gets class `reading-mode`.
- `.timeline-pane { display: none; }`.
- `.detail-pane { width: 100%; background: var(--bg-warm); }`.
- `#detailContent { max-width: 720px; padding: 56px 32px 120px; }`.
- All body text bumps +1 step (thesis 22→24, body 18→19, sanskrit 20→22).
- Topbar shows a "Back to timeline" button replacing "Reading mode".
- A previous/next arrow control appears at the top of the content (date-order navigation).

### 7.2 Implementation

```css
body.reading-mode .timeline-pane { display: none; }
body.reading-mode .stage { grid-template-columns: 100%; }
body.reading-mode .detail-pane {
  background: var(--bg-warm);
  border-left: none;
}
body.reading-mode #detailContent {
  max-width: 720px; padding: 56px 32px 120px;
}
body.reading-mode .thesis { font-size: 24px; }
body.reading-mode .passage-card .sanskrit { font-size: 22px; }
```

JS:
```js
function setReadingMode(on) {
  document.body.classList.toggle("reading-mode", on);
  topbarReadingBtn.textContent = on ? "Back to timeline" : "Reading mode";
  if (on && !state.activeId && state.thinkers[0]) openThinker(state.thinkers[0].id);
}
```

If user enters reading mode without an active thinker, default to first by date.

The existing `.reader-modal` (full-work translation) is a separate concern and stays as-is. Reading-mode is for the **detail panel content**, not for full work translations.

---

## §8 — Implementation guidance

### 8.1 What to preserve in `app.js`

Keep as-is:
- `loadJSON`, `loadAll`, manifest pattern.
- `colorFor`, `defaultColorFor`, school registry consumption.
- `escape`, `md`, `renderMarkdown` (already-fixed asterisks logic).
- `openReader` / `closeReader` for full-work modal.
- `linkThinker` and the global click delegation for `[data-thinker-link]`.

### 8.2 What to refactor

**Replace `renderTimeline()` entirely.** Decompose into:
- `computeLayout(thinkers)` → returns `Map<id, {x, y, lane, shade, tier, barX1, barX2}>`.
- `renderLaneRail(lanes)` → builds the sticky left rail.
- `renderEraBands(svg, range)` → background era rects.
- `renderEraStrip()` → top sticky era labels.
- `renderAxis(range)` → year ticks.
- `renderEdges(svg, layout)` → manhattan-routed paths; tag with `data-from` / `data-to` for hover-lit toggling.
- `renderDots(layout)` → date-bar + dot + label per thinker.
- `wireHover(layout)` → adds hover handlers that toggle `.edge--lit` on connected edges and `.dot-dim` on others.

**Replace `renderDetail()` body** (keep signature). New helpers:
- `renderHero(t)` — h2, romanization, meta row, dates line, hero thesis.
- `renderLineageBlock(t)`.
- `renderEngagedWorks(t)` — uses the new nested `.work-card` containing `.passage-card`s.
- `renderOrphanPassages(t)` — passages whose `work_id` doesn't match any engaged work.
- `renderPaniniTables(passage)` — replaces the pre-formatted `.panini` block.
- `renderComparativeBlock(t)`.

### 8.3 CSS modularization

Split `assets/style.css` into modules and concatenate via a single `<link>` chain (no build):

```
assets/css/
  tokens.css        // :root vars, color, type scale, spacing
  base.css          // reset, html/body, focus styles
  topbar.css
  timeline.css      // lanes, rail, era bands, dots, edges, axis
  detail.css        // pane, hero, lineage, works, passages, compclaims
  panini.css        // morphology tables
  reader.css        // full-work modal + reading-mode
  responsive.css    // ≤720, 720–1023 overrides
```

Update `index.html` to load each in that order. (Or: merge by hand into one `style.css` with clear `/* === SECTION === */` banners — this is simpler and matches the "no build" constraint. Recommended: stay with one file but use banners.)

### 8.4 CSS variable system

Use the tokens declared in §1.8 and §2.2 throughout. Never hardcode pixel values inside component CSS — always reference vars. Example:
```css
.thinker-dot.tier-1 .node { width: var(--dot-tier1); height: var(--dot-tier1); }
```

This makes future scale tweaks one-line edits.

### 8.5 New `data-` attributes for selection

In the rendered DOM, tag everything for hover/JS hooks:
- `.thinker-dot[data-id][data-school][data-shade][data-tier]`
- `.lineage-edge[data-from][data-to][data-kind="lineage|polemical"]`
- `.work-card[data-work-id]`
- `.passage-card[data-passage-id][data-work-id]`
- `.compclaim-card[data-claim-id][data-verdict]`

### 8.6 Class name conventions

BEM-lite, dash-cased:
- Components: `.timeline`, `.timeline__rail`, `.timeline__lane`, `.timeline__era-strip`.
- Variants: `.thinker-dot--tier-1`, `.lineage-edge--polemical`.
- States: `.is-active`, `.is-lit`, `.is-dim`, `.is-open`.

Migrate existing `.detail-open` to `body.is-detail-open` (clearer that it's a global mode toggle).

### 8.7 Function names (new)

```
// timeline
computeLayout, renderLaneRail, renderEraBands, renderEraStrip, renderAxis,
renderEdges, routeManhattan, renderDots, wireHover, scrollLaneIntoView

// detail
renderHero, renderLineageBlock, renderEngagedWorks, renderWorkCard,
renderOrphanPassages, renderPassageCard, renderPaniniTables,
renderComparativeBlock, renderComparativeCard

// modes / nav
setReadingMode, navigateByDate, navigateByLane, openThinkerById, closePane

// utilities (existing) — keep
md, escape, renderMarkdown, linkThinker, formatDates
```

---

## §9 — Anti-requirements check

- No framework added (vanilla ES module).
- No build step (single CSS file with section banners; or simple `<link>` chain).
- No graph-layout library (cladogram is fully deterministic from `school_color_token` + `sub_school_shade` + dates).
- No data-schema changes (uses existing fields; tier-1 list hardcoded in JS until/unless `tier` is added to the schema later).

---

## §10 — Execution order (priority)

Highest priority first; each row is one focused commit-sized chunk.

1. **Topbar slim to 40px + remove legend** (§3.1, §3.2). Frees vertical space; trivial change.
2. **Cladogram lanes + sticky left rail + manhattan edges** (§1.1–§1.4). The biggest visual lift; eliminates dot crowding and edge chaos.
3. **Detail-pane width 62% + hero thesis + nested work/passage cards** (§2.1, §2.3, §2.4, §2.5). Solves the "cramped detail / unclear engaged-works" complaint.
4. Era bands + date-range bars + tier sizing + always-on labels (§1.3, §1.5, §1.6, §1.7).
5. Pāṇinian breakdown as morphological tables (§2.6).
6. Comparative-claims verdict-anchored cards (§2.8).
7. Reading mode (§7).
8. Keyboard navigation (§6.3).
9. Mobile pass (§6.5).
10. CSS module split / token cleanup (§8.3, §8.4).
