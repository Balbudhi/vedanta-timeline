# Content and source standard

This standard keeps a public interpretive project evidentially honest. It
applies to every source, timeline entry, translation, article, glossary entry,
and comparison.

## 1. Source states

| State | May enter the public repository? | May support a quotation or citation? | Required action |
|---|---|---|---|
| **Public, verified witness** | Yes | Yes | Record edition, stable acquisition URL or bibliographic source, file path, work/author identity, and exact locus; retain any licence or reuse condition. |
| **Public working witness** | Yes | Only within its stated limits | Mark its verification status honestly (for example, clean text, scan needing OCR, or searchable capture needing page confirmation); do not represent it as a critical edition. |
| **Private / rights-unresolved acquisition** | No | No | Keep it outside the public repository. Record only a non-infringing acquisition note; obtain permission or a public lawful witness before use. |
| **Quarantined OCR** (`data/sources/_unverified_ocr/`) | Yes, as quarantine only | No | Treat as a search aid. Proofread each proposed reading against its named printed scan, create or update a clean witness with provenance, and then cite that witness. |

Raw OCR can make plausible but false Sanskrit readings and can mix running heads
or apparatus into the text. It cannot become citable merely because a string
search matches. A recension with different numbering must be aligned by text,
not mapped mechanically by verse number.

## 2. Provenance and citation

Every published passage or quotation needs a traceable chain: author/work,
edition or witness, on-disk source path, exact locus, and a canonical
`cite://thinker_id/work_id/locus` entry resolving in `data/citation_index.json`.
For a scan or transcription, also retain the source URL, acquisition context,
and what was checked (including page/folio where available). `source_status`
and manifest `verification_status` must describe the actual witness, not its
ideal future state.

Do not use a citation to decorate an inference. Label the difference between
direct textual report, scholarly reconstruction, and the site's own
interpretation. Comparative claims must name both positions, cite support for
each, classify one specific claim rather than whole traditions, and preserve
genuine disagreement or contestation where it remains.

## 3. Dates, authorship, and translation

- Use `dates_estimate`, `dates_tier`, and `dates_notes` together. Accepted
  tiers include `confirmed-from-records`, `consensus-textual`, `contested`,
  `lineage-internal`, `oral-tradition-only`, and `reconstructed`. Precision may
  not exceed the evidence.
- Use the work's real `ascription_tier`: `securely-authored`,
  `traditionally-ascribed`/`traditionally-attributed`, `school-ascribed`,
  `lineage-attributed`, `compiled-redacted`, `attributed`, or `disputed`.
  Explain the qualification when it affects a reader's conclusion.
- Sanskrit text must be verbatim from an eligible witness and translated under
  `docs/SANSKRIT_TRANSLATION_STANDARD.md`: source script displayed first,
  IAST below it, then literal grammar-faithful English; word-level morphology
  and glossary links, explicit uncertainty, and equal word-by-word treatment
  of commentary are required. An editorial emendation must be documented in
  `textualNote`; never silently repair, supply, or normalize a source reading.

## 4. Roster and completeness

Every roster entry must state why it belongs in one of these roles:

1. **School-defining or lineage-shaping thinker** — central to a tradition's
   doctrine or transmission.
2. **Systematizer, commentator, or polemical interlocutor** — included for a
   specified textual or dialectical contribution, not miscast as a founder.
3. **Reconstruction-only / citation-preserved figure** — no surviving secure
   work; display the evidential limitation prominently.
4. **Comparator** — useful for a stated structural comparison but not counted
   as Vedānta; label it as such in data and presentation.
5. **Modern, scholarly, or contextual figure** — included for a stated
   interpretive, reception, or contextual function, not as primary authority
   for an earlier tradition.

Use existing `entry_status` values (`draft`, `reviewed`, `audited`, or an
existing explicitly named backlog status) honestly. A reviewed entry is not a
warrant for unsupported claims, and `display: false` is an editorial choice,
not proof of incompleteness. Translation coverage must be one of `full`,
`selection`, or `placeholder`; choose the lower claim when unsure. `full` means
the entire work or a complete natural unit, `selection` means identified loci
from a larger work, and `placeholder` means no rendered primary text.

## 5. Required validation

Before publishing a change, validate changed JSON with
`python3 -m json.tool <file> >/dev/null` and run the checks that match its
surface:

| Change | Required check |
|---|---|
| Interactive Sanskrit reading or commentary | `node scripts/validate_gita_slots.js`; `node scripts/check_gita_terms.js`; `python3 scripts/check_gita_witness.py` |
| Witness, quote, or citation-index grounding | `python3 scripts/check_gita_witness.py` when the reading corpus is affected; inspect the cited witness and citation-index resolution. |
| Thinker/source coverage | `node scripts/check_coverage.js` (informational: investigate its report; it is not a correctness pass/fail gate). |
| Translation coverage labels | Verify the stated locus scope against the source; use `python3 scripts/classify_translation_coverage.py` only when intentionally regenerating its frontmatter and audit output. |

`check_gita_witness.py` must have no undocumented divergences. Unresolved
witnesses are not validated evidence; resolve them or keep the related content
out of citation-bearing publication. Report every command run and its outcome
with the handoff.
