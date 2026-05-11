# Mobile Rendering Issue Catalog

Audit target: `http://127.0.0.1:8765/`

## MOB-001 — Top bar stability and tap targets
Viewport: `iphone-se` (`375×667`)
Flow: `topbar_filter`, `topbar_network_toggle`
Before screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/before-topbar-filter.png`
After screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/after-topbar-filter.png`
What was wrong: the mobile top bar was cramped, used smaller-than-comfortable button targets, and relied on viewport-height behavior that risks iOS toolbar jump. The Chromium audit did not reproduce a vertical shift, but the layout was fragile and matched the user report.
Root cause guess: `.topbar` was `position: relative`; `.stage` used `100vh`; buttons had no minimum touch height.
Proposed fix: make the bar sticky, switch the stage to `100svh/100dvh`, and enforce `44px` minimum button height.
Status: fixed

## MOB-002 — Mobile panel interactions leaked through to the timeline
Viewport: `iphone-se` (`375×667`)
Flow: `thinker_sankara`, `source_tab`
Before screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/before-thinker-portal.png`
After screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/after-thinker-portal.png`
What was wrong: the full-screen detail pane sat over the timeline, but pointer activity could still be interpreted as timeline-dismiss input. This made mobile interactions feel unstable.
Root cause guess: the mobile pane overlay did not isolate underlying timeline interactions, and the timeline dismiss handler only filtered a narrow set of targets.
Proposed fix: make the detail pane a true fixed overlay on mobile, disable timeline pointer events while it is open, and hard-stop pointer/touch propagation from the pane before the timeline dismiss handler sees it.
Status: fixed

## MOB-003 — Glossary popover mobile presentation was unreliable
Viewport: `iphone-se` (`375×667`)
Flow: `glossary_popover`
Before screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/before-glossary-popover.png`
After screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/after-glossary-popover.png`
What was wrong: glossary interactions on mobile were not presenting as a strong on-screen surface. The user report described the dictionary popover as not showing up well.
Root cause guess: the mobile sheet treatment existed, but the stack order and mobile pane layering were too weak, and the term sheet typography was not explicitly hardened for IAST-heavy content.
Proposed fix: raise glossary z-index above the pane overlay, keep the mobile bottom-sheet treatment, and add a stronger serif fallback chain for diacritics.
Status: fixed

## MOB-004 — Citation popover needed a true mobile bottom sheet
Viewport: `iphone-se` (`375×667`)
Flow: `citation_popover`
Before screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/before-citation-popover.png`
After screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/after-citation-popover.png`
What was wrong: citation detail on mobile needed to stay fully on-screen and clearly layered over the article/thinker reader.
Root cause guess: the citation popover had a bottom-sheet style but lower stacking than the mobile panel overlay, so it could be visually weak or partially occluded.
Proposed fix: raise the citation sheet and scrim above the mobile reader, preserve the fixed bottom-sheet layout, and keep the close affordance within reach.
Status: fixed

## MOB-005 — Markdown lists were flattened into paragraphs
Viewport: `iphone-se` (`375×667`)
Flow: `article_long_lists`
Before screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/before-article-primitive-graph.png`
After screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/after-article-long-lists.png`
What was wrong: long numbered and bulleted sequences in `primitive-graph.md` rendered as ordinary paragraph text instead of semantic `ul/ol` lists, making dense mobile reading materially worse.
Root cause guess: `renderMarkdownFull()` only split paragraphs and never promoted markdown list blocks to semantic list markup.
Proposed fix: parse contiguous ordered/unordered list blocks in `assets/app.js`, emit real `ul/ol/li`, and tighten mobile list spacing in `assets/style.css`.
Status: fixed

## MOB-006 — Tables collapsed into unusable narrow columns
Viewport: `iphone-se` (`375×667`)
Flow: `article_ramanuja_table`
Before screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/before-article-ramanuja-table.png`
After screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/after-article-ramanuja-table.png`
What was wrong: article tables compressed into the screen width, forcing awkward line breaks and over-tall cells.
Root cause guess: raw `<table>` output had no scroll wrapper and inherited aggressive cell wrapping on narrow screens.
Proposed fix: wrap rendered markdown tables in a horizontal scroll container, give them a minimum readable width, and disable forced word-breaking inside cells.
Status: fixed

## MOB-007 — Article and source markdown blocks needed mobile-safe spacing
Viewport: `iphone-se` (`375×667`)
Flow: `article_hegel_blockquote`, `source_tab`
Before screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/before-source-view.png`
After screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/after-source-tab.png`
What was wrong: markdown surfaces lacked consistent mobile handling for blockquotes, horizontal rules, lists, and source-tab table overflow.
Root cause guess: the shared markdown renderer emitted minimal block structure, and the mobile typography layer did not provide dedicated list/hr/table-wrapper rules for source/article bodies.
Proposed fix: add blockquote overflow guards, `hr` styling, list indentation, and shared `.md-table-wrap` rules to article, translation, and source markdown surfaces.
Status: fixed

## MOB-008 — Network legend consumed too much width on small screens
Viewport: `iphone-se` (`375×667`)
Flow: `network_view`
Before screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/before-network-view.png`
After screenshot: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/after-network-view.png`
What was wrong: the network legend took too much horizontal room on narrow mobile screens.
Root cause guess: the mobile legend width and row sizing were still close to desktop proportions.
Proposed fix: reduce mobile legend max-width and text sizing.
Status: fixed

## Observed But Not Converted Into Rendering Fixes
Viewport: all four presets
Flow: `topbar_search`, `article_footnotes`, `source_tab`
Screenshot paths: current audit outputs under `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/<viewport>/`
What was observed: the local build has no top-bar search control; article view does not currently emit superscript citations; the first reachable `Djvu` source entry in the audit path points to a missing on-disk source file.
Root cause guess: these are product/data gaps rather than mobile CSS regressions.
Proposed fix: separate follow-up work if the site wants a mobile search affordance, article-level superscript citation conversion, or source-manifest cleanup.
Status: not changed in this sweep
