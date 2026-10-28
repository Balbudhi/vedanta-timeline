# UI style audit and migration — 2026-10-28

## Delivered scope

The user requested a strict, cohesive, digital-first visual standard, especially for
citations, typography and contextual reading. The maintained specification is
[`docs/UI_DESIGN_STANDARD.md`](../../docs/UI_DESIGN_STANDARD.md). This audit owns
migration status; it does not repeat the specification or certify runtime compliance.
Only that standard and this audit were changed for this design slice. Public prose,
source data, CSS and renderers are untouched by this slice. Other agents are changing
runtime files concurrently; observations below describe inspected code, not a frozen
release or a claim that their work has been visually verified. The release-checkout
reconciliation below records later upstream additions separately from the initial
findings; the standard remains a migration target.

Read: project AGENTS, existing UI standard, Bhakti `docs/DESIGN_STANDARD.md`, global
CSS and theme tokens, article/thinker citation renderers, citation panel/mobile
popover, Gītā word/glossary cards and Sahasranāma evidence/footnote styles. Primary
accessibility and browser references are linked beside the rules they support.
No screenshot or phone-input evidence was collected for this document-only slice.

## Decisions and evidence

- Retain neutral Vedānta surfaces, the established serif/sans roles and circular
  controls. Bhakti's restraint/control discipline transfers; its red/cream palette,
  playlist semantics and installed fixed-scale policy do not define Vedānta.
- Give all reference actions one neutral, underlined role. Reserve school/voice color
  for identity. Current `.cite-link` uses neutral ink, `.wc-gl` uses independent
  gold, `.cite-fn-link` falls back to brown, and article grammar/source links request
  `--accent`, which is not defined in the inspected stylesheet/app/shell.
- Source metadata must be readable text. Static sRGB calculations from current
  opaque tokens: `#9a9a9a` on white = **2.81:1**; `#595959` on `#1a1a1a` = **2.48:1**.
  These are the light/dark `--muted-soft` pairs used by `.voice-src`, `.wc-analysis`,
  `.vsn-detail-source` and others. Even dark `--muted` (`#888`) on `--bg-warmer`
  (`#2d2d2d`) is **3.89:1**. Proposed metadata alias uses dark `--ink-soft`, which is
  **6.50:1** on that surface; light `--muted` on `--bg-warmer` is **4.80:1**.
  Calculations establish token-pair risk, not a full computed-style contrast audit.
- Adopt named baseline source references and contextual previews, with a separate
  full-reference destination. Existing `numberCitations()` discards visible labels
  and emits 9.5px superscripts; its CSS comment incorrectly says labels remain
  inline. This is a presentation migration, not permission to alter source wording.
- Give prose a consistent readable role and measure. `.dp-article-body > article`
  explicitly uses 14px/1.55 and `max-width: none`; `.voice-en` is 14.5px;
  `.vsn-source-translation` is 14.5px. Wider panel resizing currently also widens
  article lines. The target uses 17px default reading text and a 72ch maximum.
  The release checkout additionally has a category-theory course override at
  20px/1.65 and 70ch, with 28/24/20px headings, 18px tables, 16px source lists and
  14px attribution. Preserve this larger reading preset; it is not evidence that
  the generic article typography has been migrated.
- Keep short word analysis separate from sustained evidence reading. Current
  `.wcard` uses radius 10px and z-index 600, citation preview radius 4px and shared
  popover level; `.cp-close` is a 28px text × with focus outline removed. These are
  concrete deviations from the stable control/stacking contract.

A separate evidence-integrity defect was independently confirmed during review:
`openCitationPopover()` renders quotation fields for `verified: false` entries,
while desktop `renderCitationTab()` suppresses them. The reviewer found 49 indexed
entries with that flag and quotation fields. This requires renderer parity and
real-entry regression coverage before claiming source-view equivalence; it is
tracked with the active [runtime review](2026-10-28_web_review.md), not deferred as
a cosmetic preference. Release reconciliation now finds an `isUnverified` guard
withholding mobile quotation fields. The runtime slice owns regression results and
release verification; this document-only slice does not claim to have tested it.

## Migration order and closing checks

The rows below remain **open migration acceptance work**; individual runtime fixes
can land without completing the whole row. Priority means sequencing within
style migration, not a declaration that a security or content defect was confirmed.
Do not adopt unrelated concurrent diffs into these changes.

| Priority / slice | Actual owners and callers | Required change | Closing evidence |
| --- | --- | --- | --- |
| 1 — semantic tokens and contrast | `assets/style.css` root/dark blocks; `assets/gita.css` `.voice-src`, `.voice-school`, `.wc-analysis`, `.wc-gl`; `assets/sahasranama.css` `.vsn-detail-source`, `.vsn-attribution-*`, `.vsn-translation-pending`; article `.grammar-ref` / `.article-passage-source a` | Add central metadata/reference/focus/selection aliases; migrate human-readable metadata off `--muted-soft`; replace independent reference colors and undefined accent dependency | Computed foreground/background contrast on white, charcoal, warm and active surfaces in both themes; no claim/status/translation content differences |
| 1 — control and focus parity | `.topbar-btn--circle`, `.dp-reader-action`, `.cp-close`, `.gp-close`, `.gp-x`, `.rb-progress`, `.vsn-footnote-call` and their markup | Normalize circular Close/glyphs, visible focus, nonoverlapping 44px standalone hit targets; keep inline targets in text flow | Keyboard traversal and coarse-pointer target bounds at 390px/tablet/desktop; check small close controls and seeking focus on actual backgrounds |
| 2 — reading typography/measure | `.dp-article-body`, `.dp-translation-body`, `.voice-en`, `.voice-sa`, `.cp-sk`, `.cp-en`, `.vsn-source-passage`, `.vsn-source-translation`, `.vsn-footnote-citation`; course `[data-article-slug="vedanta-category-theory"]`, `.article-math--display`, `.cite-fn-list` | Preserve the large course preset while migrating generic readers to defined type roles and 72ch prose cap; preserve script-specific marks and source order; wide tables remain local | Article, root text, commentary and source preview at default/200% text size and expanded reader; inspect longest compounds/titles and table scroll |
| 2 — common source action renderer | `assets/app.js` `md`, `numberCitations`, `renderFootnoteList`, full Markdown citation rendering; `.cite-link`, `.cite-fn-*`; `assets/sahasranama.js` evidence/footnote calls | Preserve work/locus labels; named baseline triggers or grouped source disclosure; authored numbering stays intact; internal keys remain lookup IDs, browser links get real destinations | Fixtures compare all original citation identities and meaningful labels; keyboard activation; long/multiple/repeated references; real URL direct load; no regex removes grammatical prose |
| 2 — contextual reference flow | `openCitationPanel`, `openCitationPopover`, `renderCitationTab`, `popoverManager`; `.citation-popover`, `.cite-scrim`, `.glossary-popover`, `.wcard` | Share preview content/state across desktop/mobile while full Citation/Source view remains available; remove preview dragging; make bottom-sheet modality/focus explicit; standardize shape/stacking | Open/close/replace, Escape, internal versus surrounding scroll, outside click, resize, focus return, load failure, repeated source selection; Back restores article position; pending/absent evidence stays truthful |
| 2 — source-note and language parity | `renderCitationSourceNotes`, `citationOriginal`; `.cpa-en`, `.cpa-translation-label`, `.cp-english`, `.cp-label`, `.profile-source-note`, `.gp-source-scope` | Reuse readable note-body/label roles and keyboard-native disclosures; retain original-language versus translation labels, witness scope and verified-only interpretive notes; resolve source-scope border token `--rule-dark` in the shared token system | Verified English and non-English originals, Sanskrit, pending/unverified entries, escaped note text, safe source links and matching desktop/mobile labels; light/dark scope-note contrast and keyboard expansion |
| 3 — state/motion parity | CSS transition/animation declarations in `style.css` and `gita.css`, reader/glossary selection handlers | Shared reduced-motion policy; limit hover to actual hover input; clear transient highlights with surface dismissal | Reduced-motion changes reach same final state; repeated tap/reopen leaves no orphan highlights; profile changed scrolling/graph behavior in Firefox and Chromium |
| 3 — print reading | Article/reader markup and CSS print rules | Flow-based reading/attribution with complete references; hide interactive chrome, reveal notes needed for understanding | Print preview of article and Sanskrit reader: no clipped text, missing evidence or overlay-only content; this is not currently implemented |

Dependencies: central roles precede selector migrations. Source-action renderer and
preview state design must be reviewed together before switching desktop/mobile
callers. Typography can proceed independently of citation routing. Preserve existing
reference URLs/keys and saved reader navigation during rollout; do not delete legacy
renderers until all affected callers and authored numbering cases have migrated.

## Release-checkout reconciliation

The release checkout adds profile/glossary source-scope disclosures (`details`),
shared citation source-note rendering, multilingual original-language handling,
typeset course math and a larger course reading scale. The standard now names these
roles and retains their semantic distinctions. Source-note labels currently use
9.5–11px uppercase styles while note bodies reuse 13–14px citation styles; these
belong in the shared typography migration. `.profile-source-note` and
`.gp-source-scope` request `--rule-dark`; no definition was found in the release
CSS, so the border token belongs in the central-token closing check.

The course has screen-only `content-visibility: auto` on selected direct blocks,
while headings/source footer stay outside that containment. Preserve this structure
and searchable/selectable content during style migration; typography changes need
new visual/scroll checks rather than an assumption that previous timing remains valid.
No public file was edited for this reconciliation.

## Design verification

The distinction that matters: a source reference should be readable and operable in
all readers, with the same visual meaning, while preserving exactly what evidence
it identifies. A plausible wrong implementation would paint every link one color
but retain unreadable metadata, anonymous numbers, lost source labels or an
inaccessible mobile scrim. The standard explicitly rejects that outcome.

Independent `web_review` review on 2026-10-28 found no blocking design contradiction:
semantic tokens, source-label preservation, numbered-source exceptions, modal versus
non-modal focus and browser-evidence limits are coherent. It independently confirmed
and escalated the mobile evidence-integrity defect above. `git diff --check` passed
for these document changes. The same independent reviewer approved the release
reconciliation: the retained course preset matches CSS, source-note/language rules
preserve verification gates, and landed fixes remain distinct from migration work.
Runtime browser acceptance belongs to each migration
slice; documentation review cannot pass those checks on its behalf.

## CSS reference migration — follow-up

Implemented the central `--reference-ink`, `--text-meta` and `--focus-ring`
roles in `assets/style.css`. Generated `.cite-fn` markers now use baseline
numbering, theme-aware neutral ink, dotted underlining and visible focus; their
size is 0.8em with a .8125rem minimum. Removed the fixed brown fallback and
negative-margin expanded hit boxes. Source-list links/attribution and citation
preview/panel labels use the same roles. Grammar/source links no longer request
the undefined accent token. Numbering, source identity, prose and renderers did
not change. Named-reference rendering and other reader styles remain open.

Self-reviewed CSS-only change, checked in IAB at 390/768/1440/2560 px in both themes:
markers resolve to #1a1a1a in light and #e9e9e9 in dark, baseline alignment is
retained, and there is no document horizontal overflow. Course markers are 16 px;
ordinary thinker markers are 13.8125 px at the current 17 px root size. Source-list
metadata resolves to #6a6a6a / #b2b2b2. Keyboard focus and Enter activation of the
first course citation preserve the correct source preview; footer layout and
smaller thinker prose were inspected. PWA shell/version regression passes.
