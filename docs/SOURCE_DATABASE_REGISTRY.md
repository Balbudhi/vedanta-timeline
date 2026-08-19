# Source database registry

This is the consolidated discovery map for the thinker-first acquisition
programme. It records what each database is for, whether it has been swept,
and what a hit means. A database is not re-searched without a reason; work
partitions consume its recorded results first.

| Database | Scope / evidence | Current use | Sweep state |
|---|---|---|---|
| E-Bharatisampat | 9,519 uploaded books; 5,576 searchable records; public metadata, Unicode readers, and account-gated e-books | Primary catalogue and authenticated-download queue; do not confuse e-book reader with clean text | Complete title sweep for all 368 current Sanskrit gaps, 2026-08-19 |
| SARIT | Named-edition TEI, per-file editorial headers and licences | First-choice scholarly digital witness; preserve TEI header | Complete 88-file corpus sweep |
| GRETIL | Large Sanskrit corpus with mixed legacy/TEI quality | Candidate discovery; assess each header/edition, never infer proofing from format | Existing full catalogue/filename sweep; use recorded candidates |
| Muktabodha | Śaiva/Śākta/Tantra corpus with IAST/Devanāgarī downloads and catalogue metadata | Direct paired-witness intake for relevant named thinkers; retain both scripts | Full local 569-record catalogue audit |
| Sanskrit Wikisource | Revisioned Unicode community transcription | Candidate source, capture revision/oldid and collate | Full 32,430-title dump compared to current gaps |
| Sanskrit Documents | Volunteer Unicode HTML/ITX with contributor fields | Candidate/discovery source; respect page permission notice and collate | Full 87-page sitemap, 9,823 records compared to current gaps |
| Ambuda | Readable/downloadable Sanskrit texts with proofing indicators | Working witness only when source identity and proofing status are retained | Targeted validated route; expand through work partitions |
| DSBC | Buddhist Digital Sanskrit Canon reader/transcriptions | Read/collate/bibliography only; its policy does not authorise republication | Buddhist gap sweep complete |
| JainQQ / Jain eLibrary | Large Jain scan/OCR and romanized-text catalogue | Edition discovery/collation only; not a clean intake source | Jain gap sweep complete |
| Project Madurai | Headered Unicode Tamil originals | Native-language primary witness candidate; retain header and follow redistribution condition | Relevant Tamil thinker sweep complete |
| Marathi Wikisource | Revisioned Marathi public transcription | Native-language primary witness candidate; capture revision and sample | Relevant Marathi thinker sweep complete |
| Vachana Sanchaya | Research Vachana corpus with author/verse citations | Allama discovery/collation route; text-data licence still unclear | Relevant Kannada thinker sweep complete |
| madhva.in | Structured Madhva Sanskrit/roman reader | Comparison/source-provenance lead; site-wide rights notice prevents automatic copying | Relevant Sarvamūla subset checked |
| Tattvavada E-LIB | Multilingual bibliographic directory | Discover print/Drive links only; current typed links are stubs | Madhva bibliography checked |
| Acharya.org | Śrīvaiṣṇava catalogue | Bibliographic only for the missing primary works | Śrīvaiṣṇava catalogue checked |
| raw_etexts / GitHub aggregators | Broad raw/derived corpora | Discovery metadata only, unless traced to a direct authorised source | GitHub audit complete |

## Result vocabulary

Every work/database check must use one of these results: `clean-public`
(candidate may be downloaded), `account-gated`, `reader-or-collation-only`,
`metadata-only`, `already-held`, `no-title-match`, `wrong-author-or-work`,
`ritual-only-or-anonymous`, or `lost/fragmentary`.

The full E-Bharatisampat matrix is in `data/editorial/catalogue_sweeps/`.
Other partition reports must be added there in a dated, machine-readable form
before their coverage is considered complete.
