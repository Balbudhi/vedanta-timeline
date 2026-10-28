# Vedānta UI design standard

This is the visual and interaction contract for the timeline, network, thinker
panel, articles, glossary, citations and Sanskrit readers. It retains the shared
Bhakti control language, with Vedānta's neutral palette and information hierarchy.
New and changed components must follow it. Existing deviations are tracked in
[the style migration audit](../internal/mobile_audit/2026-10-28_style_audit.md);
this document is a design specification, not a claim that migration is complete.

## Authority and intent

The text and relationships lead; controls support reading, comparison and listening.
Use space and type before boxes. Use one recognizable action for one purpose.
Do not add permanent chrome simply because a feature has multiple operations.

This document owns presentation and interaction. `SANSKRIT_TRANSLATION_STANDARD.md`
owns script/IAST/translation order and word analysis; the editorial/source standards
own evidence and attribution. Presentation changes must preserve that information,
existing citation keys, deep links, source distinctions and reading position.
No visual redesign authorizes rewriting public scholarly content.

## Color and tokens

`assets/style.css` owns global tokens and both theme definitions. Reader styles
consume them; they must not establish independent palettes. The table gives the
required semantic mapping. Names marked **new** are migration targets, not tokens
already shipped. Add aliases centrally before using them in components.

| Role | Token / mapping | Use |
| --- | --- | --- |
| Canvas | `--bg` | Main reading surface, white / neutral charcoal |
| Secondary surface | `--bg-warm`, `--bg-warmer`, `--pane-bg` | Small contextual regions; dark variants stay neutral |
| Main text | `--ink` | Titles, prose, interactive reference text |
| Supporting text | `--ink-soft` | Secondary prose, explanations |
| Metadata | `--text-meta`: light `--muted`, dark `--ink-soft` | Author, locus, source, grammar, dates; never faded decoration |
| Reference action | `--reference-ink`: `--ink` | Citation, glossary and source actions in every reader |
| Focus | `--focus-ring`: `--ink` | 2px outline, 2px offset; clear of clipping |
| Decoration | `--rule`, `--rule-warm`, `--hairline`, `--muted-soft` | Separators and nonessential marks, not readable metadata |
| Identity | `--c-*`, `--vc`, registered school colors | Graph/school/voice identity, paired with names or shapes |
| Selection | **new** `--selection-bg`: `--bg-warmer`; `--ink` text | Active source/word plus underline or border; never color alone |

Reference actions use the same neutral ink in both themes; do not inherit a school
color or use independent brown/gold/blue values. Identity colors can mark a voice
border, dot or graph edge. They do not recolor its entire quotation or citation.
Preserve existing commentary-move tints only with textual move labels and measured
foreground contrast. Error and pending states name the condition in readable text;
any additional tint needs paired light/dark tokens and cannot imply verification.

Normal text, including metadata, must meet 4.5:1 against its actual surface.
Meaningful control boundaries/focus indicators must remain distinguishable; use
3:1 against adjacent colors as the project review floor. Do not assume a token
passing on `--bg` passes on every tinted surface. `--muted-soft` currently fails
normal-text contrast in both themes and must not be used for new text. Disabled
controls may be quieter, but an explanation of unavailability is ordinary text.
See [WCAG contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

## Typography and rhythm

Keep the established `--serif` (EB Garamond with existing fallbacks) for prose,
IAST, quotations and work titles; `--sans` (Inter/system fallbacks) for interface,
metadata and navigation. Preserve suitable source-script fallback coverage. No
third decorative family. Sanskrit script stays upright; do not italicize an entire
quotation or English translation to signal that it is a source.

These are target roles at the default scale; implement in `rem` and support text
enlargement. They replace per-component arbitrary sizes as components migrate.

| Role | Default size / line height | Treatment |
| --- | --- | --- |
| Reading prose and English translation | 17px / 1.65 | Serif, `--ink` or `--ink-soft` |
| IAST reading line | 17px / 1.7 | Serif; italics only for the established language convention |
| Source-script reading line | 21px / 1.65 | Upright, no clipped marks |
| Reader title / section / subsection | 24 / 20 / 17px; 1.25–1.4 | Sans, 600; sentence case |
| Controls and metadata | 13px / 1.45 | Sans; metadata uses `--text-meta` |
| Word-card explanation | 15px / 1.55 | Sans; headword 18px serif |
| Compact graph ticks / nonessential counts | 11–12px / 1.3 | Sans; explicit density exception, not a reader default |

The existing category-theory course is a retained **large reading preset**:
20px/1.65 prose, 70ch measure, 28/24/20px headings, 18px tables and 16px source
lists with 14px attribution. It serves extended lesson reading. Its current
`[data-article-slug="vedanta-category-theory"]` selector is a migration seam, not
permission to invent different type scales per article. Preserve this larger scale
when consolidating roles; do not shrink it to 17px in a consistency cleanup. Verify
its equations, tables, source footer and enlarged text alongside ordinary articles.

A source label is metadata; its passage is reading text. Do not shrink the passage
because it appears in a citation preview, commentary, footnote or glossary. Inline
reference actions inherit the surrounding text size and baseline. Keep uppercase
and letter spacing for exceptional short categorical labels, not work names/loci.

Use a 4px spacing base: 4/8px within a group, 12/16px between related groups,
24/32px between sections. Prefer whitespace and a hairline over nested cards.
Reading measures target 60–72 characters; cap long prose at 72ch in the panel and
full screen. Wide tables/parallel passages may use the wider reader region in a
locally scrollable wrapper. They must not widen the document or force all prose wide.

## Controls and state

Universal actions (Share, full screen, Close, Search, Theme, Articles, Filters)
use the circular icon family. SVGs use a 24×24 coordinate system, `currentColor`,
1.6px stroke, round caps and joins. Filled Play/Pause glyphs are the routine exception.
Visible circles are 34px desktop / 36px mobile. Standalone touch targets must be
at least 44×44px; invisible extensions must neither overlap nor be clipped. If the
row cannot fit, reduce optional labels or disclose secondary actions, not targets.
Inline prose links/word tokens retain text flow; do not add overlapping invisible
44px boxes to them. The inline exception is distinct from standalone controls
([WCAG target-size guidance](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)).

Text pills are for choices/disclosures, never duplicates of universal header actions.
A control keeps one position and outer shape across states. Matched glyphs and
accessible action/state labels (and matching `title` when present) change in place.
Buttons perform commands; links
navigate to real URLs. A local source preview uses a button; its full reference
has a link. Do not expose `cite://` as a browser navigation destination after migration.

| State | Required behavior |
| --- | --- |
| Rest | Quiet icon/text and stable geometry |
| Hover | Feedback only for hover-capable fine input; not a persistent touch state |
| Press | Brief feedback without layout shift; no artificial selected state |
| Keyboard focus | Visible `:focus-visible` outline independent of hover/selection |
| Selected / expanded | Matches actual state and corresponding ARIA state |
| Loading | Truthful status; repeated input cannot install stale content |
| Disabled | No activation or hover/press decoration; native `disabled` where applicable |

Tab, Shift+Tab, Enter/Space and Escape must work without hover. Never blur controls
to hide focus styling. Route changes and removals must leave focus at a meaningful
visible target. A noninteractive tooltip must not contain action buttons.

## Reader composition

Thinker/reference panels use `clamp(440px, 36vw, 560px)` on desktop. Long-form and
Sanskrit readers use `clamp(680px, 58vw, 920px)` while the timeline remains visible.
A persisted drag width is clamped for the active content type. Full screen fills
the stage but retains the reading measure. Share, full-screen and close stay in
stable right-aligned header slots; full-screen glyphs encode the current action.

At narrow widths the reader can occupy the stage. Keep top-level controls on one
row; hide optional labels before creating another toolbar. Compact segments may
use initials only with complete accessible names. Preserve titles, safe-area
clearance and scroll position when rotating or changing reader mode.

## Citations and evidence: one digital reading flow

A reader should see what supports a claim, inspect it in context, and return to the
same sentence. Citation identity comes from work/locus/source data, never from a
visual number alone. Use these patterns across thinker text, articles and readers:

1. **Inline reference:** retain a meaningful short work/locus label when it belongs
   to the sentence. Render at the text baseline with a dotted underline and
   `--reference-ink`; hover/focus makes the underline solid. Accessible name:
   `View source: {work}, {locus}`. Full names remain available in the preview.
2. **Dense supporting references:** use one baseline `Sources (3)` disclosure after
   the claim, opening a list of its three named references. The count describes
   actual sources, not verification strength. Do not silently shorten/remove source
   wording through a blanket regex or convert every link into an anonymous numeral.
3. **Source preview:** show work + locus, author/commentator, available passage in
   the standard script → IAST → English order for Sanskrit, and a concise
   source/translator line. Other languages retain their actual original-language,
   romanization and translation labels; an English original is not a translation.
   Offer `Open full reference` only when a destination exists. Missing, contextual,
   pending or disputed evidence keeps its truthful existing status beside the passage;
   visual polish must never promote it to verified quotation.
4. **Sustained reference view:** use the existing Citation/Source panel for context,
   witness details and longer reading. Opening it preserves the originating article's
   scroll/state; Back restores that location. A direct reference URL opens this view.

Inline glossary definitions and references share color/type rules but differ in
content and labels. Source provenance is not a glossary definition. Distinguish the
quoted author, commentator and translator with names/roles; do not collapse them
into one generic “Source” label or duplicate provenance above every word gloss.
A word-card action opening commentary names its author, for example
`Read {commentator} on this word`.
Interpretive source notes, witness/scope notes and quotations remain distinct.
Use sentence-case labels such as `Interpretive source note` and `Witness and scope`;
the note body uses readable prose, not small metadata. Preserve verification gates
and source-language distinctions in shared preview/panel rendering. A compact
`details` disclosure is appropriate for longer profile/glossary scope notes; the
summary is a native keyboard-operable control, not an unlabeled colored badge.
Navigation links remain visibly underlined; preview/disclosure text uses the dotted
reference treatment. Underlining supplies an affordance independent of color,
following the principle illustrated by [GOV.UK links](https://design-system.service.gov.uk/styles/links/);
its blue palette and page layout are not adopted here.

**Permitted exceptions:** an original author's numbered notes and existing imported
scholarly numbering may be retained as source content, with readable named actions
and accessible labels. Print can use numbered endnotes. Existing generated website
references retain their numbers during migration,
but render at the text baseline in neutral reference ink, with a dotted underline
and visible keyboard focus. Their size is 0.8em with a .8125rem minimum; no negative
margins or overlapping expanded hit boxes. Named references remain the target.
Do not apply this generated-marker treatment to an original author’s superscripts.
Never renumber authored source notes to match generated website references.

## Contextual surfaces

| Need | Surface | Lifetime and focus |
| --- | --- | --- |
| Word/gloss analysis | One anchored non-modal word card, max 300px, viewport-clamped | Same-token toggle, outside interaction, Escape or surrounding scroll dismisses; no drag or persistent close control |
| Brief source inspection | One anchored non-modal preview on desktop; bottom sheet on narrow screens | Explicit close, Escape/outside dismissal; keeps origin reading state; no dragging |
| Long glossary/reference reading | Existing persistent panel/tab | Stable header controls; remains while reading/scrolling |
| Blocking decision | Modal only if the task truly requires it | Background inert, focus contained, Escape/close and return focus |

Transient surfaces share an 8px radius, `--bg`, `--rule`, `--shadow-md`, 16px padding
and viewport margins of at least 12px. Mobile sheets may use 16px top corners and
safe-area padding. No nested card shadows. Shared stacking tokens must keep word
cards/preview content above their reader and below a true modal; no local `z-index:
600` escalation over unrelated dialogs.

Opening a transient surface replaces the previous one and clears linked highlights.
Scrolling inside its content keeps it open; scrolling its owning page dismisses it.
Navigation dismisses it; resize repositions or dismisses it. For keyboard activation,
move focus to the named preview/card heading when it contains structured content or
actions, allow Tab to leave a non-modal surface, and dismiss on focus leaving its
trigger/surface region. Escape/explicit close returns focus to a still-present
trigger. Outside-pointer dismissal respects the newly clicked target's focus.
A word card without actions can keep focus on the trigger with its explanation
programmatically associated; keyboard users must still be able to read its content.

A dimmed sheet that blocks the background is a modal dialog: implement its accessible
name, initial focus, inert background, focus containment and restoration together.
Do not paint a scrim over an otherwise keyboard-active background. This follows
[APG's modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).
Optional hover previews must be dismissible, pointer-reachable and persistent long
enough to read ([WCAG hover/focus guidance](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html));
tap/click is always sufficient.

## Listening, sharing and feedback

Reader transport provides Play/Pause, Back 10 seconds, Forward 10 seconds and a
keyboard-operable seek slider with elapsed/total time. Single recordings do not
pretend to have Previous/Next tracks. Seeking preserves paused/playing state and
clamps to boundaries; unavailable duration disables seeking. Show buffering/failure
truthfully and allow explicit retry. System media actions follow the same controller;
the OS decides which buttons it displays. Do not promise a lock-screen layout.
Keep transport slots stable and clear of the viewport safe area and reading text.

On phones, tablets and installed PWAs, Share uses the native sheet when available.
Desktop Share copies the canonical current view URL and gives adjacent `Link copied`
status without changing the icon's geometry. Cancellation is not failure and must
not silently copy. Announce completed/error feedback accessibly without moving focus.
Loading, empty and failed reader states preserve the shell and provide a useful next
action; they must not hide an error behind a permanent spinner.

## Touch, motion and performance

Apply `touch-action: manipulation` at the shared document root to prevent accidental
double-tap zoom while preserving scrolling, selection and pinch zoom. Do not use
`user-scalable=no`, global `touch-action: none`, or global touch cancellation to fix
repeated taps. Custom graph pan/zoom policy is confined to the graph; provide buttons
and keyboard equivalents. See [MDN touch-action](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/touch-action).

Feedback is immediate; optional surface transitions take 120–200ms and never delay
activation. Prefer transform/opacity; do not animate layout during graph pan/zoom or
reader scrolling. Reduced motion removes nonessential movement and smooth scrolling
while reaching the same final state ([MDN reduced motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)).
No backdrop blur, large moving shadows, or repeated label measurement on the graph's
interaction path without a measured browser budget. Chromium smoothness is not
Firefox/Zen evidence. Record equivalent cold/warm loading and continuous pan/zoom
workloads before calling a performance change successful. Lazy loading must keep the
selected view responsive and must not replace a newer view with a late response.

## Print and enforcement

Print reading content with its title, attribution and complete references in document
flow. Remove graph chrome, media controls and transient overlays. Expand referenced
notes or provide endnotes with stable labels; no essential information may exist only
in a popup. Preserve source/translation distinctions without relying on background
colors. Print requirements are a migration target, not evidence of an existing mode.

Before releasing a changed component, check it in the Codex in-app Browser at 390px,
tablet, desktop and large desktop/TV widths, in light and dark themes. Exercise the
changed input paths: repeated tap; mouse enter/leave; Tab/Shift+Tab; Enter/Space;
Escape; surrounding/internal scroll; resize; Back/Forward. Confirm reading measure,
no document overflow, nonoverlapping targets, visible focus, semantic labels, stable
controls and no duplicated actions. Check 200% text enlargement, reduced motion and
safe areas when supported; name unavailable real-device checks rather than claiming
them from a narrow desktop window. Performance work also needs Firefox-family and
Chromium comparison; responsive screenshots alone cannot establish it.

For citation migration specifically, review a thinker passage, article, Sanskrit
commentary and glossary source in both themes, including a long title, multiple
references, missing evidence and return to the original scroll position. Compare
source identities/content before and after. Add behavior tests when renderer or
navigation behavior changes; documentation alone needs review, not synthetic tests.

Exceptions must name the component, user need, affected rule and verification in
this document before adding a new pattern. Temporary deviations belong in the
migration audit with a closing check. Neither an old selector nor a screenshot of
existing behavior grants an exception. Reuse and migrate the shared roles instead
of adding a final override block to each reader stylesheet.
