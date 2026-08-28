# Sanskrit grammar tooling boundary

> **Status: this document supersedes the May 2026 grammar-engine integration
> plan.** That plan incorrectly treated a computational parser, generated
> derivation trace, confidence score, or agreement with another parser as a
> sufficient basis for public Sanskrit analysis. It must not be used to design,
> generate, approve, or publish site content.

This repository may use software to make an audit faster. Software does not
become the authority for a Sanskrit reading, segmentation, derivation, grammar,
or translation merely because it is deterministic or cites sūtra numbers.
If a parser, dictionary, or model suggestion conflicts with a witnessed source
text or the shared source library, the witness wins until the reading is
independently re-derived from the sources.

## 1. Authority order

For every public Sanskrit unit, work in this order:

1. **Exact textual witness.** Establish the reading, locus, recension, and
   immediate context from the cited edition on disk. Preserve meaningful
   variants instead of silently harmonizing them.
2. **Pada division and syntactic context.** Establish how the witnessed
   saṃhitā is divided and how each form functions in the sentence or name.
3. **Primary grammatical authority.** Derive the form from Pāṇini's
   *Aṣṭādhyāyī*, citing the operative rules in their required order.
4. **Traditional adjudication.** Where the sūtras alone do not settle the
   intended analysis, consult the *Mahābhāṣya*, the relevant traditional
   vṛtti/commentary, the Dhātupāṭha or Gaṇapāṭha, and text-specific traditional
   commentary. Record the authority actually used.
5. **Reviewed English explanation.** Write the gloss and plain-language
   grammar from that analysis and the passage context. For quoted commentary,
   keep the quoted author's translation distinct from the site's grammatical
   explanation.

A modern dictionary can help locate possibilities, but it cannot establish the
reading or substitute for derivation and context. A parser or language model can
suggest a question to check, but it cannot supply the final answer.

### Shared Sanskrit source library

The maintained cross-project textual library is
`/Users/eeshan/Dev/prakriya/sources/`. **Read that library directly for Sanskrit
work in this repository.** In particular:

- `sources/primary/panini/ashtadhyayi/ashtadhyayi_upstream.txt`
- `sources/primary/panini/dhatupatha/dhatupatha_upstream.txt`
- `sources/primary/panini/ganapatha/ganapatha_upstream.txt`
- `sources/primary/panini/kashika/kashika_upstream.txt`
- `sources/primary/panini/mahabhashya/mahabhashya_gretil.txt`
- `sources/primary/panini/siddhantakaumudi/siddhantakaumudi_sutrapatha_upstream.txt`
- `sources/primary/panini/unadi/unadi_pancapadi_upstream.txt`
- `sources/primary/etymology/nirukta/nirukta_wikisource_13_chapters.txt`

Read `/Users/eeshan/Dev/prakriya/sources/README.md` and
`sources/manifest/clean_witnesses.json` for witness status and provenance. The
`primary/` readings are usable Sanskrit-only research witnesses, not universally
critical editions; consult their corresponding `raw/` witness and apparatus
when a textual correction or disputed reading matters.

## 2. Permitted use of computational tools

Parsers, morphology libraries, OCR, dictionaries, and language models may be
used only as **non-authoritative audit aids**:

- compare two independently established readings;
- find possible omissions, duplicates, or inconsistent spellings;
- enumerate candidate analyses for a human to test against the sources;
- detect disagreement with an already source-derived analysis;
- run mechanical schema, population, replay, and slot checks.

Their output must be labelled provisional and kept out of the public payload
until the source review is complete. Tool agreement is not evidence of truth;
tool disagreement is only a prompt to reopen the sources.

## 3. Forbidden publication paths

Do not:

- auto-fill public word cards from Vidyut, Sūtrakṛt, Monier-Williams, Apte,
  Heritage, a local grammar engine, an API, or a language model;
- publish a top-ranked or confidence-scored parse as though probability settled
  grammar;
- call a corpus "Pāṇinian" because a program emitted Aṣṭādhyāyī numbers;
- use parser-to-parser agreement, sampled spot checks, or aggregate accuracy as
  acceptance for a closed finite corpus;
- silently replace an author's wording, a received reading, or a printed verse
  number with a normalized one;
- expose unresolved generated analysis behind a tooltip, hover, laboratory, or
  other apparently authoritative UI.

The earlier proposals for engine-authored breakdowns, automatic correction,
arbitrary-text grammar labs, and confidence-ranked alternatives are withdrawn.

## 4. Publication gate

Each public word analysis must carry enough internal evidence to replay the
decision:

- exact witness ID and locus;
- witnessed source-script text and faithful IAST;
- reviewed pada division;
- lemma/root and inflection or derivation;
- operative Aṣṭādhyāyī rule sequence;
- any traditional grammatical or text-commentary authority needed to
  adjudicate the reading;
- literal contextual gloss and an explicit uncertainty note where necessary;
- reviewer status distinct from any tool-generated status.

For a closed finite corpus, acceptance is 100%: every unit accounted for, every
public analysis source-reviewed, every citation replayable, and every unresolved
item withheld or explicitly shown as unavailable. Random samples and parser
coverage percentages cannot authorize publication.

## 5. Relationship to `~/Dev/prakriya`

The separate `prakriya` repository has two different roles that must not be
conflated:

1. Its `sources/` tree is the shared, read-only Sanskrit textual evidence base
   and should be consulted directly as specified above.
2. Its interpreter, APIs, generated projections, form tables, tests, and traces
   are unfinished research software and are **not** an editorial authority for
   this site. Do not invoke them to create or certify public analysis.

This repository may cite stable source files in that checkout during review,
but public artifacts must record the witness identity/locus rather than depend
on the checkout's executable code.

If a grammar engine is evaluated later, the evaluation begins only after a
frozen, independently source-reviewed oracle exists. The engine may then serve
as a validator or disagreement detector. Shipping engine-authored Sanskrit
analysis would require a new editorial decision and a revised standard; this
document does not authorize it.

## 6. Current corrective action

Any existing data whose provenance names Sūtrakṛt, Vidyut, Monier-Williams, or a
model as the basis of a public analysis is provisional until re-derived under
§1. Builders must fail closed: provisional analysis may be audited locally but
must not appear in published reader payloads.
