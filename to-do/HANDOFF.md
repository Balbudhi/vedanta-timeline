# HANDOFF — corpus primary-source grounding + UI cleanup

State as of 2026-06-15. Read this first after a context reset.

## The grounding standard (apply to every thinker entry)
Reader-facing prose — `core_thesis` and `engaged_works[].summary` — must rest on
**primary sources**: the thinker's own works (cite by title + chapter/page) and the
primary texts they engage. NOT on modern scholars' characterizations, and with **no
editorializing** ("most important", "unmatched", "magnum opus", "included here for
completeness", meta-commentary about the entry, "(Lutgendorf 1991)"-style authority).
Secondary scholars belong only in `ascription_notes` / `dates_evidence` (the sanctioned
"state of scholarly opinion" fields). Critical-edition citations (Thibaut, Kuppuswami
Sastri, Mayeda) are legitimate provenance — keep them.
Reference example: **`data/thinkers/karpatri.json`** (commit `03e84b1`).
Living-thinker date convention: `dates_high: 2050` (sentinel — see `assets/app.js:143`), never the current year.

## Done this session (pushed to main)
- UI: audio player slim redesign (gita) · dark-theme rebuilt (neutral charcoal) · lanes-view
  label de-collision + clickable hit targets + zoom-declutter.
- Header reduced to "Vedānta" + quiet "a realist tradition" tagline; About notice rewritten
  (whole site AI-generated; unbiased/literal framing; per-model Opus/Codex attribution dropped).
- Karpātrī regrounded on primary sources (the template).
- Merged duplicate Ayon Maharaj + Swami Medhananda → canonical `medhananda` (living; both OUP books).
- Fixed false 2026 death-dates: Melamed, Butler, Rambhadracharya, Macherey → 2050; Spinoza → 1632–1677.
- Added Debashish Banerji + Arindam Chakrabarti (draft; birth years marked contested/unverified).

## Task #4 — secondary-source audit fix-wave (PENDING)
Findings: **`docs/SECONDARY_SOURCE_AUDIT.md`**. Severity counts: HIGH 4, MED 9, LOW 11,
~170 prose-clean; **78 entries have zero primary `cite://` grounding** (collection backlog).
Fix worst-first: clooney, sankara, appayya, vedanta-desika, ramanuja, srinivasa, nimbarka,
vijnanabhiksu, rangaramanuja-muni, yadava-prakasa, bodhayana, kasakrtsna, bhartrprapanca, vidyaranya.
Recurring fixes: (a) delete "X is the standard secondary reading (Clooney/Dasgupta/Carman)"
parentheticals → cite the primary text instead; (b) move authorship/dating debates
(Hacker/King/van Buitenen/Pollock/Hiriyanna) out of prose into `ascription_notes`/`dates_evidence`;
(c) strip "single most important / most ambitious / magnum opus" value-judgments.

## Task #5 — primary-source collection (IN PROGRESS, background agent)
Output will be **`docs/PRIMARY_SOURCE_INVENTORY.md`** + new `.txt` under `data/sources/`.
Collect primary texts in original languages as committed plain text (NOT gitignored); skip
huge files (>~2 MB). Sources: GRETIL (Sanskrit/Prakrit), SuttaCentral (Pali), Gutenberg/Zeno (German).

## Deferred (user said: note, don't burn tokens now)
- **Wire already-present English texts into the Source tab** — e.g. K.C. Bhattacharyya: text is in
  the corpus but not wired. Check `data/sources/english/` and the detail-pane Source-tab wiring.
- **Richer bios** for thinkers whose primary text we hold (K.C. Bhattacharyya, etc.).
- **`assets/app.js` placeholder strings (~lines 2248, 2252)** still say "Codex 5.4 pass" / "queued
  for Codex extraction" — update to the new "AI-generated" framing once app.js is safe to edit.
- **Sanskrit word-by-word translation is NOT being done for every text** — only where it already
  exists. Do not over-claim coverage in prose or UI.

## Glossary content gaps (see `to-do/GLOSSARY_GAPS.md`)
Glossary popover now hides placeholder per-school rows (NOT-APPLICABLE / [NOT YET
RETRIEVED]); data keeps them as honest internal state. **117 missing school-views**
across 43 entries — sourcing split: **21 FILL** (primary text already on disk →
writable now), 31 PARTIAL (thin: Jaina-prakrit / grammar only), 65 NO-CORPUS (minor
Vedānta sub-schools — needs external sourcing, do NOT fabricate). Plus 302 unsourced
`primary_loci` markers. Full per-entry list + FILL/PARTIAL/NO-CORPUS tags in the doc.

## Concurrency
A separate agent is adding a glossary "cognate pills" feature (touches `data/glossary/*`,
`assets/app.js` `openGlossary`, `assets/style.css` `gp-cog`, `assets/gita.*`). Leave its uncommitted
edits alone; stage only your own hunks by path/content (`git diff --cached` before every commit).
