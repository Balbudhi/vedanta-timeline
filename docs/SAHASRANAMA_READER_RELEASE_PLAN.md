# Sahasranama reader release plan

Status: in progress. Existing review labels and passing schema checks are not
evidence that the published linguistic content has been independently reviewed.

## Product contract

The reader must preserve Chinmayananda's argument and make every Sanskrit use
understandable without turning ordinary prose into a succession of large cards.

- Terms, titles, and isolated words remain inline. Their cards give the actual
  Devanagari, IAST, contextual meaning, and supported analysis.
- Quoted passages use one compact source-script, IAST, and literal-English
  presentation. English and Sanskrit share word mappings. The site translation
  is identified once; Chinmayananda's wording remains separately attributed.
- Derivational formulas receive the same linguistic completeness in a compact
  formula block. They are not certified as scripture quotations.
- Lists remain lists. A Roman duplicate of a quoted Sanskrit passage is recorded
  as an alternate surface, not displayed as a second passage.
- Notes attach to their exact claims. A note cannot interrupt a quotation's
  introduction. Several citations remain distinct and follow the author's order.
- Printed readings, normalized readings, primary-source corrections, and site
  translations remain separate data. No silent OCR correction or text deletion.

## Execution order and ownership

1. Release infrastructure: reconcile the nine existing Simplified summaries with
   the normalizer, include the real reader checks, and require validation before
   deployment. This does not certify the remaining content.
2. Source inventory: pin available witnesses, freeze hashes and all 1,000 name
   packets, and account for every source paragraph, note, quotation, inline
   occurrence, and public word payload. Recover the old received-text snapshot
   or collate its replacement; never simply change the expected hash.
3. Representative end-to-end batch: names 1, 2, 5, 11, 23, 39, 101, 160, 303,
   403, 436, 500, 501, 673, 742, 750, 895, and 997. This set exercises all known
   failures, including wrong script, untranslated English, interrupted quotes,
   formulas classified as citations, merged English/Sanskrit, and duplicate
   surfaces. A successful sample unlocks batching, not release.
4. Linguistic batches: Terra producers own disjoint stable unit IDs and output
   only review artifacts. Each receives prejoined source/context and the fixed
   schema. Start with at most two producers and at most five passage units per
   batch. Record actual elapsed time, output size, acceptance, and tool-reported
   usage when available. Stop and diagnose a failed mechanism before scaling.
5. Integrate only independently accepted records into one canonical builder.
   Reuse only an exact supported form in the same grammatical context; spelling
   similarity and shared headings are insufficient.
6. Complete the three reviews below, then publish the same verified artifact.

The primary agent owns schema, integration, release decisions, and the defect
ledger. Workers do not commit, push, rewrite unrelated files, mark the global
goal complete, or continue producing repetitive status messages after handoff.

## Producer and reviewer contract

Each accepted passage records stable source identity and ranges; exact printed
text; any normalized reading with its evidence; complete pada division;
per-word script, IAST, gloss, morphemes, morphology, roots/affixes/compound
analysis where supported; one coherent literal translation with complete slots;
and exact evidence loci. A non-verbal word does not acquire an invented root.

Review classifications are not generated from field presence. Generic labels
such as "inline Sanskrit token" and joins of gloss strings do not count as
completed morphology or a translated sentence. A known unresolved record stays
open in the ledger and blocks the requested complete release.

## Three independent acceptance passes

1. **Source preservation:** 100% of names, paragraphs, notes and Sanskrit
   occurrences accounted for against the witnesses. Verify source boundaries,
   quotation ownership, citation loci, normalization, and actual rendered-text
   preservation. Comparing a retained source string with itself is insufficient.
2. **Linguistic correctness:** independently inspect every public word record
   and passage translation against the textual and grammatical witnesses.
   Recheck segmentation, inflection, derivation, script, contextual meaning,
   literal English, and English/Sanskrit alignment. Zero open concrete defects.
3. **Reader behavior:** render the full population and compare it to the accepted
   records; test bidirectional interactions and exact anchors. Visually inspect
   every presentation category and all flagged cases in the in-app browser at
   phone, tablet and desktop widths. Verify source/translation order, citations,
   popup clipping, keyboard/touch access, sticky ranges, typography and overflow.

After a correction, invalidate and rerun the affected passes. Record the hashes
reviewed, reviewer identity, findings, corrections and final verdicts. No pass
may be satisfied by relabelling the same producer output as reviewed.

## Release requirements

- The complete review ledger has no pending or failed entries.
- A clean build uses immutable inputs and reproduces the accepted artifacts.
- CI runs the same integrity and review-manifest checks and prevents deployment
  on failure. There are no skipped dependencies disguised as a success.
- Live in-app-browser verification confirms the deployed artifact and key flows.
- The handoff distinguishes evidence from limitations and never promises that
  three schema runs constitute three independent content reviews.

## Current evidence and unresolved work

- The nine-summary validator mismatch is repaired by registering the existing
  published paraphrases in the normalizer; the published source text is unchanged.
- The original received-text bytes were recovered from the Internet Archive
  capture at `20250611100109id_` and independently hash-checked against the
  existing `b53e64398d0a340dd01d2a83979c13346d6b27ec29f50a46a41b9d14080bb19b`
  pin. The builder now uses that archive URL by default and continues to accept
  `--received-source` for an exact local copy. The raw archive was not added to
  the public repository; its redistribution terms still apply.
- A fresh normal build now succeeds into temporary output. It differs from the
  current published reader in 34 fields, so clean-build equality remains an open
  gate. The generated reader has not been overwritten to conceal that difference.
- `scripts/build_sahasranama_review_queue.py` creates the frozen audit queue from
  source hashes. Its flags identify review work; absence of a flag never marks
  a unit accepted. Source, linguistic, and rendered reviews start pending.
- Do not use the current generic morphology labels, automatic gloss joins, or
  existing "reviewed" strings as proof that the linguistic pass is finished.
