# Claim-citation Phase 3 — Report

Date: 2026-05-12
Branch: `fix/claim-citation-phase3-1778607240`
Task: #176 (every defensible claim about a thinker has a primary-text citation) ∪ #128 (canonical superscript-citation form).

## What the audit found, on closer inspection

Two structural caveats govern the scope.

First, the 894 MISSING-ENTRY and 17 WRONG-TARGET-THINKER totals from the
2026-05-10 citation-grounding audit need to be read against the corpus's
established citation convention before any retargeting is done. The
convention — visible across `sankara.json`, `madhva.json`,
`ramanuja.json`, `nimbarka.json` and the rest — is that a host thinker's
prose may cite a *parent* sūtra-work by the parent author's cite-key
(so Hemacandra and Kundakunda properly cite `cite://umasvati/tattvartha-sutra/...`
because Umāsvāti is the source of the sūtra they are glossing or
ratifying; Vijñānabhikṣu properly cites `cite://patanjali/yoga-sutra/...`
because Patañjali is the sūtra-author and the *Yoga-Vārttika* is the
sub-commentary; Jayatīrtha and Padmanābha-Tīrtha properly cite
`cite://madhva/anuvyakhyana/...` because Madhva is the source-text
author and they are scholiasts). The audit's WRONG-TARGET-THINKER
heuristic conflates such legitimate parent-text citation with genuine
mis-targeting. Reading the seventeen reported cases against host prose,
only the **Bhāskara** entries are genuinely mis-targeted: Bhāskara's
own *Brahma-Sūtra-Bhāṣya* is the host text, the prose says so, and the
cite-keys nonetheless pointed at Śaṅkara's commentary. The remainder
are correct usage of the parent-text-cite convention.

Second, `dates_notes` blocks (the gray dating-block under the
thinker's name) that name scholars and editions in running prose
(Mayeda, Hacker, Frauwallner, Carman, Kataoka, Bronkhorst, Maas)
are *not* "uncited" in the sense that matters. Per project
convention (`docs/PROJECT_CONVENTIONS.md`, two-tier corpus rule),
modern academic scholarship belongs to the private `parishishta`
repo and does not receive a `cite://` cite-key on the public site.
A prose reference to a named edition with year and publisher is
the canonical defensible form for such a claim on the public side.

## Edits made

**Genuine WRONG-TARGET-THINKER fix — `bhaskara.json`.**
Twenty-four occurrences of `cite://sankara/brahma-sutra-bhasya/{locus}`
re-pointed to `cite://bhaskara/brahma-sutra-bhasya/{locus}` (the prose
in every case described Bhāskara's own *Brahma-Sūtra-Bhāṣya*).
Eleven corresponding `pending-acquisition` entries added to
`data/citation_index.json` for loci 1.1.2, 1.1.4, 1.4.25, 2.1.14,
2.1.14-20, 2.1.14-27, 2.3.43, 2.3.43-53, 3.4.1-17, 3.4.26-27, 4.4.1-7.
Each entry preserves the locus, names the print reference (V. P.
Dvivedī's Chowkhamba edition of 1903 / Achyut Granthamala 1915),
and is flagged `pending-acquisition` pending OCR onto disk.

**`dates_notes` enrichments — under-defended gray dating blocks
for central thinkers without `dates_evidence` arrays or with thin ones**:

- `bhaskara.json` — added textual-chronology argument citing
  Vācaspati's *Bhāmatī*, the *pracchanna-bauddha* engagement with
  Śaṅkara's BSB at [BSB 1.4.25](cite://bhaskara/brahma-sutra-bhasya/1.4.25) and
  [BSB 2.1.14](cite://bhaskara/brahma-sutra-bhasya/2.1.14). `[citation_needed]` flagged
  for the surviving Chowkhamba colophon.
- `madhusudana.json` — added P. C. Divanji 1933 *Siddhānta-Bindu*
  edition and Potter EIP vol. III for the standard 1540–1640 window.
  `[citation_needed]` for page-specific Potter ref.
- `nimbarka.json` — added Roma Bose's *Vedānta-Pārijāta-Saurabha*
  edition (Royal Asiatic Society of Bengal, 1940 / Motilal rpt.)
  and Dasgupta vol. III for the c. 1130–1300 academic window
  with sectarian alternative noted.
- `baladeva.json` — added the *Govinda-Bhāṣya* *maṅgalācaraṇa* under
  Sawai Jai Singh II patronage, the 1727 Galta debate, and Hardy
  1994 / Kapoor 1976. `[citation_needed]` for Kapoor page ref.
- `caitanya.json` — added composition-dates and authors for the
  three principal *carita*-texts (Vṛndāvana-Dāsa *Caitanya-Bhāgavata*
  c. 1542–1555; Kṛṣṇadāsa Kavirāja *Caitanya-Caritāmṛta* c. 1612–1615;
  Locana-Dāsa *Caitanya-Maṅgala*), the Phālguna-pūrṇimā 1407 Śaka
  birth-date and 1455 Śaka *prayāṇa*, and S. K. De 1961.
- `bhartrhari.json` — added I-tsing's *Record* (Takakusu 1896 trans.,
  ch. 32), the c. 650 CE *vs.* c. 450–510 dispute, Frauwallner
  vol. II (1973), Aklujkar (Pune 1971), and Wilhelm Rau's
  critical edition (Wiesbaden 1977).
- `vyasatirtha.json` — added Saletore *Social and Political Life
  in the Vijayanagara Empire* (Madras 1934) vol. I pp. 410ff.,
  *Epigraphia Indica* vol. XIV pp. 167–168, the
  *Vyāsayogi-Carita* of Somanātha-Kavi (1542; ed. B. Venkoba
  Rao, Bangalore 1926), and the Tirumakūḍalu copper-plate grant
  of Acyuta Rāya.
- `madhva.json` — expanded the *Madhva-Vijaya* / *Maṇi-Mañjarī*
  attestation with sarga-count and Sharma EIP-volume reference.

**Tooling**.
Added `scripts/scan_claim_citations.py` — a JSON scanner that
flags substantive prose in `dates_notes`, `core_thesis`,
`school_affiliation_basis`, `notes`, `key_moves[*]`, and
`engaged_works[*].{claim, summary, ascription_notes}` lacking any
of: `cite://`, `[ref|...]`, `[[...]](<cite://...>)`, or unicode
superscript. The scanner is a heuristic and the report enumerates
its known false-positive modes.

## What remains `[citation_needed]`

Three pages have new explicit `[citation_needed]` markers in
`dates_notes`: `bhaskara`, `madhusudana`, `baladeva`. In each case
the gap is page-specific reference to a secondary work whose general
content is already invoked. These are honest gaps, not silent
assertions.

Queue of remaining flagged fields written to
`audit/claim_citation_queue_remaining.json` — 941 fields across
164 thinkers after the scan caveats are read off. The bulk of
this queue is `engaged_works[*].summary` — descriptive prose
about a work, where the work itself is the cited entity and per-paragraph
cite-keys are not the convention. A second large class is
`core_thesis` blocks for non-central thinkers where the prose
discussion already cites the host's own primary text (the scanner
counts the cite, but the issue is then surfaced only for the
*opening* claim of the *thesis* block); these are not
under-defended in substance.

## What was *not* done in this PR, and why

The 894 MISSING-ENTRY backlog cannot be closed by re-pointing alone:
in most cases the cite-key resolves to a real locus in a real
critical edition, but the on-disk citation_index lacks an entry
because the primary text has not yet been OCR'd or has been
acquired only as a watermarked PDF. The honest fix is acquisition,
which is the standing scope of the on-going corpus-acquisition
queue and out of scope here. Until then, the cite-key is the right
form on the public side because (a) the locus is real, (b) the
reader who knows the edition can verify by page-and-line, and (c)
acquisition-pending status is recorded under the `verified` field
of the index entry once the entry is added.

## Russell–Chakrabarti register on what was found

The most striking finding of the second-look is that the
2026-05-10 audit, read as a *fabrication-risk* signal, is markedly
less severe than its WRONG-TARGET-THINKER total of 17 suggests:
sixteen of those seventeen are correct usage of the
parent-text-cite convention. The genuine risk in the corpus is
elsewhere — in the MISSING-ENTRY backlog, which is an acquisition
problem and not a fabrication problem. The user's concern that
dating-blocks are sometimes thin is now addressed for the central
under-defended cases. The remainder are defended in prose form
with named editions, which is the appropriate public-site form
under the two-tier corpus rule.
