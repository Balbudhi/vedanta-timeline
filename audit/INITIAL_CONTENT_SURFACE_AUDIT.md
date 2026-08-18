# Initial content-surface audit

Date: 2026-08-18. This is a baseline audit, not a mass-rewrite authorization.

## 1. Thinker bios and work summaries

### Strong models

- `data/thinkers/gaudapada-sankhya.json` separates the Sāṅkhya commentator
  from the Vedānta Gauḍapāda, gives an evidence-aware thesis, and states the
  rejected identity claim instead of silently merging persons.
- `data/thinkers/hegel.json` has an unusually compressed, reader-facing core
  thesis, although its work cards still include placeholder material.
- `data/thinkers/jnanesvar.json` honestly limits its claims where OCR quality
  prevents passage-level control.
- `data/thinkers/krsnadasa-kaviraja.json` distinguishes a traditional
  attribution from secure authorship instead of building certainty on it.

### Repair classes

1. **Research memo disguised as a thesis.** Long entries such as
   `ramanuja.json`, `madhva.json`, `vedanta-desika.json`, and `caitanya.json`
   bury the central claim under work-by-work detail. Split core thesis, works,
   reception, and reconstruction status.
2. **Placeholder work cards.** `kc-bhattacharyya.json`, `hegel.json`, and
   `husserl.json` expose ingestion/file-label prose as public work summaries.
   Replace only after source identification; otherwise label as unavailable.
3. **Reconstruction presented as authorial voice.** Caitanya and Nathamuni
   need an explicit prose distinction between direct text, later systematizer,
   and site reconstruction.
4. **Biography before philosophy.** Modern entries such as Chaudhuri and K. C.
   Bhattacharyya lead with institutional biography instead of the text and
   claim that justify inclusion.

The automated report currently identifies 17 thin and 89 overlong visible
profiles. Rewrite batches require a source packet and independent review.

## 2. Glossary and encyclopedia

### Strong models

- `data/glossary/prakrti.json` distinguishes a shared causal problem from
  school-specific answers and warns against the lazy “nature” gloss.
- `data/glossary/maya.json` makes its thin shared core explicit rather than
  pretending that schools agree.
- `data/glossary/atman.json` maps genuine divergence while retaining a clear
  conceptual question.
- `data/glossary/agni.json` is a good textual-history pattern because it marks
  Aurobindo as a hermeneutic lens rather than a philological authority.

### Repair classes

1. Dense terms such as `brahman.json` lead with technical compression before a
   reader receives a plain-language orientation.
2. Rich and thin glossary schemas are silently mixed: `buddhi.json` is a
   source-rich multi-school entry while `nyaya.json` and `visistadvaita.json`
   are short stubs.
3. Reader-facing placeholders such as `[NOT YET RETRIEVED]` must remain
   internal queue state, not article prose.
4. The primitive model is retained as legacy analytical material but is not a
   reader-facing primary explanation; replacement is claim/locus centered.

## 3. Sanskrit reader

### Verified strengths

- Mūla Gita display is source script → IAST → literal English.
- Word/English interaction is click-first and bidirectional.
- Gita 3.42 appropriately leaves the mūla pronoun unresolved and displays
  divergent commentator readings instead of choosing one without warrant.
- Existing Gita slot, terminology, and witness checks pass.

### Gaps

1. Only commentary records that already contain `devanagari` can now render
   source script. Many commentary units lack it and must not be auto-generated.
2. Commentary completeness remains uneven: 71 units lack one or more of
   source script, per-word source script, grammar summary, or explicit glossary
   keys.
3. Śrīdhara Svāmī cannot link to a thinker entry because the present Śrīdhara
   record is a different author; do not create a false link.
4. Reader invariants need a direct glossary-key existence validator and a
   complete-versus-fallback commentary declaration.

## 4. Sources and citations

- `data/primary_text_manifest.json` has 93 valid in-repository records, but
  131 public `data/sources/` files remain unmanifested.
- No manifest record is currently declared citation-grade; two mention a future
  citation-safe condition.
- The citation-link audit found 1,301 unresolved public `cite://` keys. This
  must be repaired in source-backed batches before citation integrity becomes a
  blocking CI gate.
- Legacy private/machine-path references remain in older material and must be
  migrated to explicit public/private witness metadata rather than silently
  treated as site sources.

## 5. Required sequencing

1. Source intake and citation-index batch for each author/work.
2. Rewrite only that author/work's thesis and work summaries from the verified
   packet.
3. Upgrade reader/glossary content only where source text supports it.
4. Promote checks from report to strict gate only after its repair batch is
   complete.
