# Vedānta UI design standard

This is the maintained interaction and control contract for the timeline,
unified reading panel, and full-screen readers. It adapts the approved Bhakti
control language to Vedānta's neutral palette and reading-first layout.

## First principle: the text leads

The timeline and readings are the product. Controls should be quiet, stable,
and immediately recognizable. Do not add a permanent toolbar, pill, label, or
duplicate action merely because there is room for it.

## Control family

- Universal actions such as Share, Enter full screen, Exit full screen, Close,
  Search, Theme, Articles, and Filters use the established circular icon family.
- Use a 24×24 SVG coordinate system, `currentColor`, 1.6px stroke, round caps,
  and round joins. Filled transport icons are the only routine exception.
- Circular controls are 34px on desktop and 36px on mobile, with an effective
  44px touch target where space permits.
- A stateful control keeps one position and one outer shape. Swap matched
  glyphs and update `aria-label`, `title`, and state attributes in place.
- Text pills are for content choices or disclosures, not universal actions.
  “Read full screen” and “Share link” pills are prohibited when the reader
  header already has full-screen and share controls.

## Reader panel

- Thinker/reference panels use `clamp(440px, 36vw, 560px)` on desktop.
- Long-form article and Sanskrit readers use
  `clamp(680px, 58vw, 920px)` while the timeline remains visible.
- A persisted drag width is clamped to the active content type; an old narrow
  thinker width must not make a long-form reader unusable.
- Full-screen mode occupies the full stage. Reading text remains centered at a
  comfortable measure rather than stretching edge to edge.
- Share, full-screen, and close remain in stable right-aligned header slots.
  Enter and exit full-screen use matched corner glyphs that visibly encode the
  current action.

## Sharing and feedback

- On phones, tablets, and installed PWAs, Share uses the native share sheet
  when available.
- On desktop, Share copies the canonical current view URL and shows a short,
  adjacent `Link copied` status. Do not mutate the icon into text or show a
  modal confirmation.
- A cancelled native share is not an error and must not silently copy.

## Responsive behavior

- Mobile top-level controls stay on one row. Compact segmented choices may use
  initials when their accessible labels remain complete.
- Do not solve overflow by creating a second row of large controls or clipping
  actions off-screen.
- Text selection remains available in reading content. Timeline chrome and
  draggable/zoomable surfaces may suppress selection and accidental browser
  zoom where the interaction requires it.

## Acceptance gate

Before release, verify in the Codex in-app Browser at 390px mobile, tablet,
desktop, and a very large desktop/TV viewport:

1. no horizontal overflow;
2. stable control positions and correct enter/exit glyphs;
3. readable default and full-screen measures;
4. native-share behavior on coarse pointers and copy feedback on desktop;
5. complete accessible names, focus visibility, and keyboard activation; and
6. no duplicate text-pill and icon versions of the same action.
