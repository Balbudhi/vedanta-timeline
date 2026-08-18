# Source-grounded implementation queue

This queue follows the initial content-surface audit. A batch is not started
until its prerequisite evidence exists; a report is not permission to invent
missing text, dates, or citations.

## P0 — Citation and source intake foundation

**Evidence:** 1,301 unresolved public `cite://` keys; 131 public source files
unmanifested; 0 manifest records presently declared citation-grade.

1. Group unresolved citations by thinker/work and classify each as existing
   witness, index-only gap, acquisition gap, private/restricted witness, or
   malformed key.
2. For one author/work batch at a time, create citation-index records from a
   verified public witness and repair only the claims that rely on it.
3. Add source metadata for unmanifested files only after edition/rights/format
   review; file presence is not citation status.
4. Promote citation-link checking to `--strict` only for completed batches,
   then for the whole corpus when all public references resolve.

**Gate:** no citation text/excerpt is shown without a verified witness and
locus; pending/private citations show status and metadata only.

## P1 — Thinker bio/work normalization

**Evidence:** 17 short and 89 overlong visible core theses; placeholder work
cards in public entries.

1. Fix public placeholder/garbled work cards first: identify source, title,
   authorship, and status, or suppress the card as unavailable.
2. Rewrite source-ready entries in source batches, not by prose length alone.
3. Split research-memo theses into core claim, works, reception, and explicit
   reconstruction/source-limit statements.
4. Add citations only when the P0 batch supplies a resolving target.

**Gate:** each changed entry answers who, text, claim, and source posture in
under twenty seconds; source review is independent of the writer.

## P2 — Chronology migration

**Evidence:** 257 visible records; 3 source-structured variants; 254 require
traditional evidence or explicit status.

1. Prioritize traditions/figures whose current notes already name both date
   traditions.
2. Create separate academic and traditional source packets. Traditional dates
   require an identified chronicle, paramparā, colophon, inscription, or
   equivalent witness.
3. Add `not-attested`, `not-applicable`, or `insufficiently-identified` where
   a traditional record is not actually available.
4. Review the resulting mode switch visually and in the chronology validator.

**Gate:** never infer a traditional range from an academic range or lineage.

## P3 — Sanskrit reader completion

**Evidence:** mūla Gita is reference-quality; commentary is source-incomplete
in many fields; source script now renders where supplied.

1. For each commentary witness, acquire/verify source script before adding it.
2. Backfill word-level morphology, structured compounds, grammar summaries,
   and glossary keys only from the verified text.
3. Add direct validators for glossary-key existence and complete-versus-
   fallback commentary records.
4. Add Śrīdhara Svāmī only after a separate source-grounded thinker record
   exists; do not link him to a different Śrīdhara.

**Gate:** source script is never generated and presented as a witness.

## P4 — Glossary and encyclopedia

**Evidence:** 18 terms lack a sourced school reading/locus; rich and thin
glossary schemas are mixed; the primitive model is pedagogically risky.

1. Upgrade glossary terms in source/tradition batches, starting with entries
   that already have public primary witnesses.
2. Keep incomplete school slots internal; do not render “not yet retrieved” as
   finished encyclopedia prose.
3. Freeze primitive-axis expansion. Preserve its citations while migrating to
   a claim/locus/register/rival/verdict model after the owner supplies the new
   abstraction.

**Gate:** every displayed school reading has a concrete locus and citation.

## P5 — Governance and release verification

1. Keep `AGENTS.md`, contributor guidance, and editorial/source standards in
   sync; delete or demote stale path/build claims rather than preserving them.
2. Run the shared check suite for every batch and record report-only debt
   separately from passing invariants.
3. Independently inspect the deployed site with the in-app Browser after each
   UI/data release: citation path, chronology mode, source status, reader order,
   and new roster entry.

**Gate:** no release claims completion because a report ran; use the report's
actual unresolved count and a visual verification record.
