# Editorial and data standard

This is the controlling template for public intellectual content. It applies to
thinkers, works, dates, sources, claims, Sanskrit readers, glossary entries,
comparative encyclopedia entries, and lineage links. It is intentionally
general: no entry is published merely because an agent can produce prose.

## 1. Core rules

1. **Evidence before prose.** A public claim is written only after its source
   record and locus exist. Primary text is preferred; a secondary witness is
   allowed only when it is identified as secondary and genuinely supports the
   claim.
2. **No invented completion.** Unknown, disputed, unavailable, and
   traditionally attributed material stays labelled as such. Do not fill a gap
   with plausible prose, a guessed date, or generated Sanskrit.
3. **Separate layers.** Preserve the difference between source statement,
   scholarly reconstruction, traditional attribution, and site synthesis.
4. **Quiet citations, inspectable evidence.** Public prose uses compact links;
   clicking opens the supporting locus, short verified excerpt/translation when
   available, status, source witness, and surrounding context.
5. **Audit is not mutation.** An audit may create a queue, report, or source
   packet. It may not rewrite content, add an entry, or promote a status.

## 2. Claim record template

Every new factual, interpretive, comparative, or attribution claim must be
recordable as:

```json
{
  "claim": "One falsifiable or source-testable statement.",
  "claim_kind": "textual | historical | interpretive | comparative | attribution",
  "source_level": "primary | secondary | traditional | site-synthesis",
  "citations": ["cite://thinker/work/locus"],
  "status": "verified | pending-acquisition | disputed | not-published",
  "qualification": "Required when evidence is limited or contested."
}
```

No public claim with `not-published` status may be rendered. A `secondary`
claim must identify its author/work in the citation detail; it may not be
presented as a primary-text conclusion.

## 3. Thinker entry template

Required public sections, in order:

1. **Identity and entry kind** — stable ID; name/IAST; `entity_kind`.
2. **Chronology** — academic and traditional records separately, each with its
   own evidence/status; no traditional claim is inferred from a lineage.
3. **Philosophical introduction and development** — normally a 180–320-word
   orientation in five connected moves (identity/context; text and problem;
   argument or method; philosophical consequence; reception or source limit),
   followed by two or more short, sourced argument sections. It is an
   introduction to a thinker, not a one-line blurb and not an undifferentiated
   research memo. The orientation does not replace earlier substantive material:
   every public legacy paragraph is mapped into a section, retained below it,
   or explicitly omitted with a source-based reason.
4. **Works** — a structured list; no generic “major works” blob.
5. **Lineage and controversy** — only evidence-backed relations, typed as
   teacher/student, textual influence, institutional succession, or polemic.
6. **Reception/source limitations** — concise and explicit.

Admission: a public thinker is an author of serious philosophical/interpretive
text, or the named subject of a serious philosophical text traditionally
attributed to them. Existing canonical-teacher exceptions must remain labelled
as transmitted corpora, not autograph authors.

## 4. Work template

```json
{
  "work_id": "stable-kebab-id",
  "title_iast": "...",
  "language": "...",
  "genre": "...",
  "ascription_tier": "securely-authored | traditionally-ascribed | school-ascribed | disputed",
  "ascription_evidence": [{"kind": "...", "description": "..."}],
  "source_status": "clean-on-disk | working-witness | primary-text-not-in-corpus | private-rights-unresolved | quarantined-ocr",
  "editorial_summary": "50–160 reviewed words: question, method, position, scope; required before a v2 card can use substantive prose.",
  "summary": "Legacy migration text; it does not render for a v2 entry until migrated to editorial_summary.",
  "key_passage_ids": []
}
```

Traditional devotional works are included where relevant but must show their
attribution tier in the reader-facing card. Academic doubt does not erase a
living tradition's attribution; traditional attribution does not become secure
authorship.

## 5. Source and citation template

Every citation target records author/work, exact locus, source witness,
verification state, and public-safe excerpt fields. A citation can be:

- **verified:** source text/excerpt is shown;
- **pending acquisition:** locus is visible but the claim is not displayed as a
  verified quotation;
- **unverified:** no source text or close translation is shown; or
- **private/right-restricted:** only non-infringing metadata and a concise
  evidence note are public.

Scraping or ingestion records must include URL/edition, rights basis, language,
script, checksum where possible, acquisition date, and transcription status.
Raw OCR is never a citation witness.

## 6. Chronology template

```json
{
  "chronology": {
    "default_variant": "academic",
    "traditional_status": "pending-evidence | not-attested | not-applicable | insufficiently-identified",
    "variants": {
      "academic": {"low": 0, "high": 0, "tier": "...", "source_kind": "academic", "evidence": []},
      "traditional": {"low": 0, "high": 0, "tier": "...", "source_kind": "sectarian-traditional", "evidence": []}
    }
  }
}
```

All visible figures eventually receive an academic record and either a
traditional record or an explicit status. A range is preferable to false
precision. `high: null` means living; UI supplies “present.”

## 7. Sanskrit reader template

For verified Sanskrit text: source script → IAST → slotted literal English.
Every unit carries witness/locus, `words[]`, grammar, and glossary references.
Commentary follows the same standard. If a field is absent, the reader must
show an honest availability state, not a generated substitute. Audio is
optional and separate from text verification.

## 8. Glossary and encyclopedia template

A glossary entry has: plain-language opening, literal derivation, invariant
function, school readings, primary loci, translator note, related terms, and
internal completeness status.

A comparative encyclopedia entry is a **claim card**, not an axis tuple:
claim; source/work/locus; register/scope; compared claim; verdict; evidence;
and uncertainty. Preserve legacy primitive records only as migration evidence.

### Layered-entry migration gate

`editorial_contract: "v2"` is the public depth contract. It requires:

- a verified witness for every rendered verified/disputed claim;
- `argument_sections` (thinkers) or `exposition_sections` (terms), with source
  citations on each claim;
- `legacy_coverage`, which makes any omission visible to review rather than
  silently shortening an article; and
- `editorial_dependencies`, a small set of review areas and update events.

For v2 work cards, legacy `summary` and `ascription_notes` are migration
material only. Substantive reader-facing prose must move to
`editorial_summary` or `editorial_ascription_note` and carry verified loci;
otherwise the UI shows only the work's attribution and source-status limit.

`pending-acquisition` and `private-rights-restricted` source-limit records may
state the scope of a gap without pretending that the missing source proves a
claim. They do not render as verified doctrine.

## 9. Agent protocol and hooks

Before any content mutation an agent must:

1. read this standard and the source policy;
2. declare file scope and mutation type (`audit`, `source intake`, `data`,
   `reader`, `UI`);
3. run the relevant validators before and after editing;
4. stage by path and inspect the staged diff; and
5. obtain independent review for source, Sanskrit, chronology, or claim work.

Automated hooks/checks may reject malformed data, unresolved citations, missing
source status, invalid lineage, or UI regression evidence. They cannot prove a
philosophical interpretation; that still requires source review.

## 10. Executable workflow

The machine-readable contract is `data/editorial/authoring_contract.json`; the
source ledger is `data/editorial/source_ledger.json`. The following commands
are part of the editorial process:

```sh
node scripts/report_editorial_readiness.js --json
node scripts/report_content_impacts.js --changed <changed-source-path>
scripts/preflight_content_change.sh <changed-content-path>
```

The readiness report produces the acquisition and migration worklist. The
impact report names every current public record that cites a changed witness
and every v2 entry whose declared dependency areas match the newly changed or
ingested source. This produces review notices; it never silently rewrites an
article.
The preflight validates the ledger and any opted-in v1 content record. Existing
legacy data is deliberately reported for planned migration rather than silently
rewritten or falsely certified.
