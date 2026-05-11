# Mobile Audit Worker Notes

Date: 2026-05-11
Target: local static server at `http://127.0.0.1:8765/`
Runner: [baseline_audit.py](/home/eeshan/philosophy/site/mobile_audit/baseline_audit.py)
Screenshots: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/<viewport>/<flow>.png`

Baseline coverage was captured for:
- `iphone-14-pro` (`393×852`)
- `iphone-se` (`375×667`)
- `pixel-7` (`412×915`)
- `galaxy-s22` (`390×844`)

Notes:
- The screenshot root already contained older `before-*` files from prior work. I did not delete them. The current audit pass produced the `timeline_*`, `topbar_*`, `thinker_sankara`, `glossary_popover`, `citation_popover`, `article_*`, `source_tab`, and `network_view` files for each viewport.
- No app code was edited. This was audit-only work in `mobile_audit/` plus screenshot output to the shared pool path.

Concise findings:
- Top bar jump did not reproduce in Chromium mobile emulation. The header stayed at `top: 0px` before and after the filter and network-toggle taps on all four viewports. The row is still visually crowded at `375px`, but I did not capture a vertical offset shift in this local-browser pass.
- The requested top-bar search flow fails because the local build does not have a search control inside `.topbar`. See `topbar_search.png` in each viewport directory.
- Thinker-panel open worked on all four viewports. The Śaṅkara panel is readable and the mobile tab strip stays reachable.
- Citation popovers do render as mobile bottom sheets and stay on-screen. See `citation_popover.png`.
- Glossary taps do create a mobile bottom sheet in the DOM and keep it on-screen in this Chromium pass. The visual capture is less obvious than the citation sheet, but the interaction did resolve and stayed inside the viewport.
- `ramanuja.md` table rendering is poor on the smallest screen. The `375px` capture shows cells collapsing into narrow stacked syllables and an over-tall block. Best repro: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/article_ramanuja_table.png`.
- Long-list rendering is broken in article view. `primitive-graph.md` does not become semantic `ul/ol` markup; numbered content remains paragraph text like `1. It gives ... 2. It separates ...`. Best repro: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/article_long_lists.png`. The same issue appears on the other three viewports.
- The requested “article footnotes / superscript citations” flow fails because article view is currently rendering inline `cite://` links, not superscript footnotes. In the Hegel article I found inline citations but no `sup.cite-fn` nodes in article view.
- Source-tab mobile behavior is rough. The tree is collapsed by default, the first reachable `Djvu` entry is garbled, and the selected file resolves to `[failed to load — file not present in site/data/sources/]` in the captured state. Best repro: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/iphone-se/source_tab.png`.
- Network view renders on all four viewports, but the legend overlay consumes a large part of the right side on narrow screens. See `network_view.png`.

Flows that failed because of current app behavior:
- Top-bar search: no search control exists in the local build.
- Article long lists: markdown lists in `primitive-graph.md` are not rendered as mobile list elements.
- Article superscript citations: article renderer exposes inline citation links instead of superscript footnotes.
- Source tab: the captured `Djvu` source path produces a load failure state on mobile.
