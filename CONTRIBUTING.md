# Contributing

This is a public research and reading project. Contributions must make their
evidence, uncertainty, and editorial intervention visible. `AGENTS.md` governs
shared-worktree and commit practice; this guide governs content.

Before making a public content change, read
[`docs/EDITORIAL_DATA_STANDARD.md`](docs/EDITORIAL_DATA_STANDARD.md). It is the
controlling template for claims, thinker prose, work summaries, chronology,
sources, Sanskrit readers, glossary entries, and comparative material.

## Before editing

- Declare a narrow file scope and inspect `git status --short` and
  `git diff --name-only`. Do not alter, stage, stash, or commit another
  contributor's work.
- Stage explicit paths only. Never use `git add -A`, `git add .`, `git add -u`,
  or `git commit -a`; inspect `git diff --cached` immediately before committing.
- Keep one coherent change per commit. Pull with rebase before pushing; never
  force-push `main`.

## Content commitments

- Cite factual, textual, and comparative claims with canonical
  `[locus](cite://thinker_id/work_id/locus)` links that resolve in
  `data/citation_index.json`. A source on disk is not automatically a
  citation-safe witness.
- Separate three voices: what a source says, a scholarly disagreement or
  reconstruction, and this site's synthesis. State uncertainty rather than
  smoothing it away.
- Give a date range, `dates_tier`, and `dates_notes` appropriate to the
  evidence. Do not turn tradition, a reconstruction, or a contested range into
  a precise historical fact.
- Identify work authorship with its actual `ascription_tier`; do not silently
  promote `traditionally-ascribed`, `school-ascribed`, or `disputed` material
  to securely authored.
- For Sanskrit, follow
  [`docs/SANSKRIT_TRANSLATION_STANDARD.md`](docs/SANSKRIT_TRANSLATION_STANDARD.md):
  source-script first, source-faithful IAST, literal grammar-led translation,
  complete word analysis, explicit ambiguity, glossary links, and the same
  standard for commentary.

## Source and roster honesty

Follow [`docs/CONTENT_AND_SOURCE_STANDARD.md`](docs/CONTENT_AND_SOURCE_STANDARD.md)
for source handling, roster roles, and readiness labels. In particular, raw
OCR in `data/sources/_unverified_ocr/` is quarantine material: it is never a
witness or citation. Material with unresolved scan rights stays outside this
public repository.

## Checks before handoff

Run the checks that cover the files changed, then report their commands and
results. For additions involving readings, run:

```sh
node scripts/validate_gita_slots.js
node scripts/check_gita_terms.js
python3 scripts/check_gita_witness.py
```

For citation, source, or roster work, run the relevant repository check (at
minimum `node scripts/check_coverage.js` for coverage changes) and validate
every changed JSON file with `python3 -m json.tool <file> >/dev/null`. Checks
that are explicitly informational remain backlog signals; do not describe them
as passing correctness gates.
