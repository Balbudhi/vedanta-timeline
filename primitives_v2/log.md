# primitives_v2 execution log

## 2026-05-11 — Phase 1 completed

Scope:

- rewrote `data/articles/source/primitive-graph.md`
- widened the grammar from the earlier Vedānta-heavy frame to a twenty-primitive graph
- added source-article anchor cases for each primitive
- added explicit assignment rules for `withheld`, mixed-register commitments, dependency edges, and cross-engagement passages

What changed in the grammar:

- added missing non-Vedāntic coverage for phenomenology, genealogy, deconstruction, critical theory, process, Mīmāṃsā, and social-formation analysis
- split method, authority, semantic mediation, normativity, social formation, affective motive, practice-path, and soteric end into distinct axes
- kept the older Vedāntic load-bearing axes, but tightened them against the audit's warnings about reading later sub-school positions back into earlier authors

Validation notes:

- pressure-checked the primitive set against the full thinker-school inventory in `data/thinkers/`
- removed remaining anchor references that leaned on non-article support
- retained the global `withheld` token so Phase 2 can avoid forced assignments where the corpus is thin

Artifact-path note:

- the worktree did not contain the expected prior `primitives_v2/PLAN.md` and `primitives_v2/STYLE_GUIDE_AGAINST_AI_TELLS.md`
- the effective phase-0 inputs present on disk were `primitives_revision/audit.md`, `primitives_revision/ai_tell_catalog.md`, and `primitives_revision/COMPLETION_REPORT.md`
- Phase 1 proceeded from those on-disk artifacts

## 2026-05-11 — Phase 2 completed

Scope:

- added `primitive_commitments` to every thinker JSON in `data/thinkers/`
- created `data/registries/primitive_graph.json` from the Phase 1 primitive set
- created minimal article-backed thinker stubs where the corpus had a substantive source article but no corresponding thinker JSON

Implementation notes:

- generated commitments through school defaults, grouped override sets, and thinker-level corrections
- added low-confidence proto and comparator defaults where the corpus is thin, instead of leaving those thinkers blank
- re-ran the generator after the adequacy check exposed three missing value-ranges in the first draft grammar

Validation notes:

- all thinker JSON files parse
- all 165 thinker JSON files now carry non-empty `primitive_commitments`
- `data/registries/primitive_graph.json` parses and reflects the revised twenty-primitive grammar

## 2026-05-11 — Phase 3 completed

Scope:

- inserted inline cross-engagement passages into every markdown file under `data/articles/source/`
- mirrored thinker-linked cross-engagement records into `cross_engagements` arrays in thinker JSON

Implementation notes:

- generated comparison passages from the commitment graph rather than treating each article as an isolated hand-edit
- inserted each passage under a major heading after the first body paragraph, so the comparison sits near a load-bearing claim rather than in a detached appendix
- required every generated comparison target to carry a primary `cite://...` witness before the passage could be emitted

Validation notes:

- all 51 source articles now contain cross-engagement passages
- cross-engagement counts range from 2 to 12 per article, with an average of 8.5
- all thinker JSON files still parse after the `cross_engagements` mirror pass

## 2026-05-11 — Phase 4 completed

Scope:

- applied a corpus-wide anti-tell cleanup across `data/articles/source/`
- wrote per-article before/after metrics to `primitives_v2/style_metrics.json`

Implementation notes:

- used the exact-string tell inventory already present in `primitives_revision/ai_tell_catalog.md` as the measurable baseline
- kept the pass conservative: sentence-openers and stock connective adverbs were removed or tightened first, then a smaller lexical set was normalized

Validation notes:

- tracked tell-count total dropped from 170 to 0 on the measured exact-string set
- the metrics file records before/after counts for each article plus aggregate totals

## 2026-05-11 — Phase 5 completed

Scope:

- loaded `data/registries/primitive_graph.json` into front-end state
- exposed the parsed registry on `window.__primitiveGraph` for future UI work

Validation notes:

- `assets/app.js` passes `node --check`
- the registry JSON parses after the full content pass
