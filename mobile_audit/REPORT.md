# Mobile Rendering Audit Report

Date: `2026-05-11`
Branch: `feature/mobile-rendering-fixes`
Audit target: `http://127.0.0.1:8765/`
Runner: [baseline_audit.py](/orcd/home/002/eeshan/philosophy/site/mobile_audit/baseline_audit.py)

## Scope
Viewports audited:
- `iphone-14-pro` (`393×852`)
- `iphone-se` (`375×667`)
- `pixel-7` (`412×915`)
- `galaxy-s22` (`390×844`)

Flows audited:
- landing / timeline
- top bar filter and network toggle
- thinker panel open
- glossary popover
- citation popover
- article rendering
- source tab
- network view

## Fixed Rendering Defects
- `MOB-001`: sticky mobile top bar, dynamic viewport units, larger touch targets
- `MOB-002`: mobile detail pane now isolates pointer activity from the underlying timeline
- `MOB-003`: glossary popover now presents reliably as a high-z mobile bottom sheet
- `MOB-004`: citation popover now presents reliably as a high-z mobile bottom sheet
- `MOB-005`: markdown ordered and unordered lists now render as semantic lists
- `MOB-006`: markdown tables now render inside a horizontal scroll wrapper with a minimum readable width
- `MOB-007`: article/source markdown spacing improved for blockquotes, rules, lists, and wrapped tables
- `MOB-008`: network legend narrowed for small screens

## Verification
- Top bar stayed pinned at `top: 0` before and after filter / network-toggle interaction on all four audit viewports.
- `article_long_lists` now reports `listCount = 55` on all four viewports instead of the prior paragraph flattening.
- `article_ramanuja_table` now renders inside a scrollable wrapper whose inner table width is `620px` on all four viewports, avoiding syllable-stacked cells.
- `glossary_popover`, `citation_popover`, `source_tab`, and `network_view` now complete successfully in the Playwright pass for all four viewport presets.

Primary evidence:
- Before issue references: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/<viewport>/before-*`
- After issue references: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/<viewport>/after-*`
- Full latest pass: `/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots/<viewport>/{timeline_*,topbar_*,thinker_sankara,glossary_popover,citation_popover,article_*,source_tab,network_view}.png`

## Files Changed
- [assets/style.css](/orcd/home/002/eeshan/philosophy/site/assets/style.css)
- [assets/app.js](/orcd/home/002/eeshan/philosophy/site/assets/app.js)
- [mobile_audit/ISSUES.md](/orcd/home/002/eeshan/philosophy/site/mobile_audit/ISSUES.md)
- [mobile_audit/REPORT.md](/orcd/home/002/eeshan/philosophy/site/mobile_audit/REPORT.md)

## Not Changed In This Sweep
- `topbar_search`: the local build has no search control inside `.topbar`.
- `article_footnotes`: article view still does not render superscript citation footnotes; the audit finds no article-side `sup.cite-fn` nodes to validate.
- `source_tab`: the first reachable `Djvu` entry used by the audit still points to a missing source file on disk. The mobile rendering around that state is improved, but the missing-file condition itself is a data/manifest issue rather than a CSS/layout defect.
