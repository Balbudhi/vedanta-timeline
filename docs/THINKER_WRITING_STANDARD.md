# Thinker writing standard

## Purpose

Each public thinker record must help a reader answer: who is this author, what
serious text or attributed text places them here, what claim do they make, and
how secure is that account? It is not a hagiography, a generic biography, or a
mini-encyclopedia of every doctrine nearby.

## Core thesis

Target: 180–320 words for the orientation, normally three to five short
paragraphs, followed by two or more short argument sections where the source
packet can support them.

1. Name the author and historical/intellectual location.
2. State the distinctive philosophical or exegetical contribution.
3. Name the work or corpus that bears the claim.
4. State the real interlocutor, disagreement, or limitation when relevant.
5. State a traditional succession separately from the philosophical argument;
   do not draw a direct teacher edge when an intermediate teacher is known.
6. Use `cite://` links for claims supported by public engaged sources.

The orientation is a map, not a substitute for the argument. Preserve the
philosophical development of a well-sourced existing entry by migrating it
into titled, readable sections. If a former claim cannot survive source review,
record it in `legacy_coverage.omitted_claims` with the reason; do not quietly
make the profile thinner.

Do not use ranking language (“greatest,” “unmatched,” “most important”), turn a
school affiliation into a philosophical claim, or merge a modern scholar's
reconstruction with an author's own assertion. State the source's claim first;
label reconstruction and this site's synthesis separately.

## Work summary

Target: 50–160 words per work.

- Say what the work is, its genre/language, its internal movement or structure,
  the question it addresses, and the position or method it develops.
- Identify ascription status in the card, never bury it in prose.
- Do not make a settled authorship question the work summary's subject. A
  necessary unresolved qualification belongs in a compact editorial note, not
  in the account of what the work argues.
- Do not claim a full translation, exact source wording, or local text witness
  when `source_status` says otherwise.
- For a traditional devotional work, state both the traditional attribution and
  the academic uncertainty where relevant; devotional genre does not erase
  philosophical or exegetical significance.

## Dating and lineage

- Keep academic and traditional dates in separate chronology variants.
- Explain the witness type in the relevant variant, not through vague phrases
  such as “tradition says.”
- Use `lineage_in`/`lineage_out` only for actual documented teacher, student,
  succession, or specified textual influence. Use `lineage_polemical` for
  argument, never an invented teacher relation.

## Source posture labels

Every source-dependent statement must be legible as one of:

- direct public witness;
- public working witness requiring further comparison;
- traditionally attributed work;
- scholarly reconstruction from named witnesses; or
- not yet in the public corpus.

## Rewrite workflow

1. Read the source record and cited locus before editing prose.
2. Draft core thesis and each work summary against the target shape.
3. Run the thinker-content report and relevant citation/source checks.
4. Run `node scripts/report_content_impacts.js --changed <source-path>` for
   each new or changed witness; inspect both direct citation and dependency
   review queues.
5. Send the changed entry to an independent source/grammar reviewer.
6. Mark `reviewed` only after the evidence and labels match the rendered text.

## Citation interaction

A public citation opens a compact verified-passage view: locus, witness text
(source script where the verified record supplies it, otherwise IAST), and a
literal English rendering. It may offer an annotated translation dossier for
the relevant text. Do not expose a raw repository file as if it were a finished
reader or a complete critical edition; raw mirrors are maintenance material,
not a public scholarly interface.
