# Web reliability and performance review — 2026-10-28

## Outcome and scope

Improve Vedanta and Bhakti installed-app launch/audio behavior, add ten-second
seeking, preserve Bhakti playlist navigation, remove accidental double-tap zoom,
and fix measured graph and article responsiveness/reliability defects.
Content, translations and unrelated work in both checkouts are outside this change.

Actual callers: Vedanta `index.html` → `assets/app.js` → timeline layouts and
shared article panel → Gita/Sahasranama readers; `assets/pwa.js` → `sw.js`.
Bhakti's persistent player owns audio and the queue across song navigation.

## Design and verification requirements

- Keep each app's existing distinct manifest identity/start URL. Do not invent
  new identities that would create duplicate installations.
- Media controls seek by ten seconds, clamp to recording bounds, retain play
  state and publish metadata/position. Vedanta does not advertise playlist actions.
  Reader replacement/close releases old audio ownership. Updates must not reload
  an actively playing recording; the worker must not cache partial media responses.
- Network layout optimization preserves every original node/label placement,
  including fallback/tie behavior, across chronologies, zoom, widths and filters.
  Compare repeated timings on identical input; host CPU is not phone performance.
- Timeline startup does not acquire unused primitive-graph data or calculate
  the same layout twice. Summary-index and individual-file fallback still work.
- Article navigation owns asynchronous work: old manifests, text, scripts,
  passages and reader mounts cannot replace a newer view or undo a close.
  Failed loads remain recoverable. Preserve complete prose/citations and renderer
  semantics; coordinate separately with the category-article worktree.
- Use `touch-action: manipulation` to suppress double-tap zoom while retaining
  reading selection/pinch zoom. Preserve timeline-specific drag/pinch handling.

Dependency order: regression cases and baseline → independent graph/audio/article
slices → integration review → real browser viewport/input/performance checks →
scoped release and deployed verification. Shared-file edits use disjoint functions;
foreign reader changes must be excluded from staging.

## Current evidence and unresolved checks

- Startup regression failed on optional graph acquisition before the fix; both
  summary and individual-file paths pass after it. Removed a 481,672-byte raw
  optional request (26,241 bytes gzipped), not a claimed equivalent latency saving.
- Baseline host profiling of 252 rendered thinkers: network placement ~12 ms,
  labels ~46–48 ms warm, excluding DOM/layout/paint. Lane computation is small;
  a graph-engine rewrite is not justified by this measurement.
- Concurrent course changes were integrated from upstream before release. The
  larger course adds substantial KaTeX/DOM work and citation metadata gating;
  preserve its content, aliases, math and source-note renderers during integration.
- In-app Browser discovery was restored by a separately reviewed account-control
  fix: repeated full socket scans and native executable hashing delayed discovery
  beyond its five-second deadline. Exact identity/provenance checks remain. Genuine
  discovery completed in 1.3 seconds and existing tabs survived the relay refresh.
- IAB local comparison at 390 px, academic network, identical corpus, no-store
  responses and service workers disabled in both variants: three alternating
  runs gave `renderAll` medians 10.9 ms before / 6.0 ms after (DOM writes included),
  timeline-ready 59.1 / 51.4 ms. No observed >50 ms task in these samples. These
  are localhost Chromium measurements, not Internet/phone or Firefox claims.
- An ordinary prose deep-link reached readable text in 86.5 ms and the following
  paint opportunity at 89.7 ms in one local run. The separately measured course
  at upstream 7f1f95f rendered 42,697 nodes and 468 source rows. Three alternating
  baseline/containment runs gave median post-timeline time to the article paint
  opportunity of about 739 / 334 ms. Full node and text counts matched. This
  isolates screen-only offscreen block layout; it is not an Internet latency
  claim. Subsequent upstream changes adopted the same bounded containment.
  Headings/footer remain uncontained, print normal, and all content stays in DOM.
- Combined candidate inspection reached the final source row with End, rendered
  the first display equation and list markers without clipping, and added no
  observed long task on the footer jump. The IAB does not expose a native Find
  dialog through the attempted shortcut: native find remains a browser-specific
  verification item, not a claimed observation. The CSS auto behavior retains
  searchable/selectable content by specification; no hidden/display:none body
  virtualization is introduced.
- Real-browser article checks at 390/768/1440/2560 px found no page overflow;
  widths were 354/716/864/864 px. Bhakti player also fits at 320 px. Native buttons
  in both apps changed paused audio from 0 to 10 seconds and back to 0. Local
  media test serving requires HTTP Range support, as the deployed media host has.
- Actual phone home-screen installation/lock-screen layout and Firefox/Zen
  scroll/paint behavior remain unverified. Isolated Firefox testing was requested
  because project browser rules otherwise restrict testing to IAB; no exception
  has been received. Known gesture math/event-order defects are separately fixed
  and covered by production-handler regressions.
- Bhakti's focused audio/PWA regressions pass. Existing content audits report
  unrelated legacy/migration and trim evidence failures; those are not repaired
  by this UI task and must not be misreported as a clean whole-repo release gate.

Independent review closed graph equivalence, gesture ordering, reader/media
ownership, PWA cache/update, and article/citation lifecycle findings. The article/citation regression
cases include all 49 explicitly unverified quotation entries:
mobile now withholds their text like desktop, retaining locus and evidence notes.
No verification status or source text was changed.

The strict UI standard and selector-level migration backlog are in
`docs/UI_DESIGN_STANDARD.md` and `internal/mobile_audit/2026-10-28_style_audit.md`.
They are a design contract, not a claim that every existing component was migrated.

Release integration: `4e3426dc` is committed and pushed. Publish the strict design
contract, then check the resulting Pages build. Final
combined `scripts/run_checks.sh` completes with zero failures; all nine UI workflow
commands pass. The last perspective-manifest race was reproduced before its fix
and both lifecycle suites pass after it (39 focused cases plus upstream reader
ownership sequences). Native CacheStorage verifies
Bhakti first-install shell keys. Bhakti deployment 60885bf9 succeeded; live buttons
seek paused media 0 → 10 → 0 seconds. No remotely controllable XSS was demonstrated
in inspected public inputs; this review is not a blanket security certification.
Vedanta deployment through fbf1bb5 succeeds; live Gita buttons also seek paused
media 0 → 10 → 0. Final integration deployment is checked after publishing.
Firefox/phone evidence remains outstanding.

Final browser candidate: upstream fbf1bb5 course has 43,190 nodes; measured prose
appeared at 437.5 ms and next paint opportunity at 518.4 ms on one local 390 px
load. The first focused inline reference outline is intact, its source-note
popover opens/closes, the first display equation fits the 354 px reading column,
and the document does not horizontally overflow. A 12-second citation-index delay
leaves prose readable. At the source footer, metadata expands the existing source
rows while browser anchoring retains the first visible source region; later rows
move down as their text grows. Focused/selected footer enrichment is deferred by
the implementation and regression-tested. Native Find remains unverified in IAB.
