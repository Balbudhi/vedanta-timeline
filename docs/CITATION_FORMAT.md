# Citation Format

Canonical form for in-text citations across the corpus (glossary, thinker JSONs,
articles, perspectives, comparative claims, polemic chains).

## Source form

Authors write citations as standard markdown inline links with a `cite://` URL:

    [VISIBLE LOCUS](cite://thinker_id/work_id/locus)

Examples:

    [MMK 24.8](cite://nagarjuna/mula-madhyamaka-karika/24.8)
    [BS 2.1.14](cite://shankara/brahma-sutra-bhasya/2.1.14)

The URL key matches a record in `data/citation_index.json` (or one of its
aliases). The visible text is the short locus the author wants the reader to
see if the citation is ever displayed inline; in normal rendering it is hidden
behind a superscript footnote number.

## Tolerated source variants

The renderer additionally accepts two informal idioms that appear in older or
hand-authored JSONs. Both are normalized to the canonical form before any other
processing (`normalizeCitationSyntax` in `assets/app.js`):

1. Angle-bracketed URL (markdown autolink form), used when the URL contains
   whitespace, commas, or other punctuation:

       [BhR 1.1 ṭīkā 12](<cite://madhusudana/bhakti-rasayana/1.1 ṭīkā.12>)

   Normalized to `[BhR 1.1 ṭīkā 12](cite://madhusudana/bhakti-rasayana/1.1 ṭīkā.12)`.

2. Footnote-bracket idiom (`[[X](cite://Y)]` and chained variants such as
   `[[X](cite://Y); [W](cite://Z)]`), where authors wrap one or more citations
   in an extra pair of brackets to mark them as footnotes:

       *dharma* is real-relational [[MUK 239.15](<cite://madhva/mithyatvanumana-khandana/239>)].

   The outer `[ ]` are stripped because the inline visible text is dropped
   downstream and replaced by a numbered superscript.

These idioms remain accepted by the renderer but are not recommended in new
content — write the canonical form.

## Rendered form

Each prose surface that displays primary-source citations runs the same
two-stage pipeline:

1. `md()` (or `renderMarkdownFull()` for full-article bodies) converts the
   source form into HTML, including `<a class="cite-link" href="cite://…">…</a>`
   anchors for each citation.
2. `numberCitations(html, counter)` rewrites every `<a class="cite-link">`
   into `<sup class="cite-fn"><a … data-fn-idx="N">[N]</a></sup>`, dropping
   the inline visible text. Repeated cite keys reuse the same N (scholarly
   convention).
3. `renderFootnoteList(footnotes)` renders an ordered list of `[N] —
   *Work-Title* locus — Thinker` rows at the bottom of the surface, with each
   row linking back into the Citation tab popover.

Each of the following surfaces applies this pipeline with its own counter
(so [1] [2] … restart per surface or per logical block):

| Surface                              | File / function                       | Counter scope          |
| ------------------------------------ | ------------------------------------- | ---------------------- |
| Thinker hero "core thesis"           | `renderHero`                          | hero block             |
| Engaged-work summary / ascription    | `renderWorkCard`                      | per work card          |
| Glossary popover                     | `openGlossary`                        | whole popover          |
| Article popover (article reader)     | `openArticle`                         | whole article          |
| Citation popover (`english_close`)   | `openCitationPopover` (no footnotes)  | none — translation-only |

Click-target: every `<sup class="cite-fn">` is itself an `<a href="cite://…">`
so the global delegation handler opens the Citation tab popover with the full
locus, Sanskrit IAST, English close, and "Open thinker" CTA.

## Non-canonical forms that the renderer does NOT auto-fix

The following appear in stale data and are slated for normalization by Agent F
in task #176. The renderer leaves them as plain text:

- `(Mayeda 1992, p. 31)` style parentheticals
- `^1` superscript footnote markers
- `[citation needed]` placeholders
- `[Ref, 1.2.3]` bracket placeholders
- bare page numbers in body text

Audit pass (2026-05-12) found **no** instances of any of the above in
`data/glossary/`, `data/thinkers/`, `data/articles/`, or `data/perspectives/` —
all current citations use the canonical or one of the two tolerated variants.

## Sanitization

`md()` and `renderMarkdownFull()` both HTML-escape every text field before
running inline markdown regexes, so no raw HTML from JSON ever reaches the
DOM. Anchor `href` values are constrained to the `cite://…` scheme by the
regex; URLs in user prose go through a separate "plain link" stash that
adds `target="_blank" rel="noopener"`.
