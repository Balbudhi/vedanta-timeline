# Clean Sanskrit acquisition standard

This is the acquisition guide for source work. Its purpose is to gather usable
Sanskrit witnesses without quietly converting PDFs, scans, or OCR into public
text.

## The rule

Seek a clean digital Sanskrit transcription first. A PDF or image scan can
identify an edition and later serve collation, but it is never the intake
source. OCR is a search aid only and stays quarantined until independently
checked.

Every missing work belongs to one of four states:

1. **clean candidate found** — a Unicode or TEI transcription exists and is
   entered in `data/editorial/source_candidates.json`;
2. **downloaded quarantine** — the source has been retrieved under
   `data/sources/_intake/`, with its header and source URL retained;
3. **accepted witness** — provenance, mechanical normalization, and a sample
   collation have been recorded; only then may it enter the public manifest;
4. **no clean digital witness found** — the work remains a documented gap;
   do not substitute a PDF, bad OCR, translation, or nearby work.

Before downloading, run `node scripts/report_unmanifested_sources.js --json`.
The current repository has 131 non-quarantine witnesses that are already on
disk but absent from the manifest. Review those first: a newly found URL may
duplicate a local GRETIL or institutional witness whose provenance simply has
not been registered yet.

## Where to look

| Priority | Provider | Appropriate use | Boundary |
|---|---|---|---|
| 1 | GRETIL TEI/plaintext | Classical Sanskrit with named editions/inputters | Preserve header; inspect source-specific rights and coverage. |
| 2 | SARIT / DSBC | Scholarly digital Sanskrit editions | Confirm exact work, language, edition, and completeness. |
| 3 | Muktabodha / IFP | Kashmir Śaiva, Śaiva Siddhānta, Tantra discovery | Catalogue and rights are source-specific; scans are not intake. |
| 4 | Sanskrit Wikisource | Revisioned Unicode candidate | Retain revision ID and collate a sample against print. |
| 5 | Tradition-specific HTML | Madhva.in, Anandamakaranda, maṭha/publisher sites | Candidate/collation only until reuse terms and edition identity are clear. |
| 6 | Sanskrit Documents | Short clean Unicode texts | Personal-study terms are not blanket permission to mirror. |
| 7 | Archive/DLI/Hathi | Print collation only | Never use scan or automatic OCR as the public witness. |

## Mechanical intake rules

Allowed normalization: UTF-8/NFC, LF line endings, accidental repeated blank
lines, and clearly separable navigation/template material. Record every such
change in provenance. Never silently alter spelling, sandhi, punctuation,
avagraha, variants, headings, colophons, commentary labels, or script.

Each accepted witness needs a provenance sidecar with source URL, retrieval
date, provider, named edition/inputter, rights/reuse posture, coverage,
normalization log, and sample-collation result. A citation-safe passage also
needs its own verified locus in the citation index.

## Commands

```sh
node scripts/report_acquisition_queue.js --language sanskrit --status missing
node scripts/report_acquisition_queue.js --language sanskrit --status degraded
node scripts/check_source_candidates.js
node scripts/fetch_source_candidate.js <candidate-id>
node scripts/check_source_inventory.js
node scripts/discover_gretil_candidates.js /path/to/gretil-path-index.txt --json
```

The queue reports every current missing or degraded work from thinker JSON.
Candidate records are research evidence; they do not authorize publication or
content rewrites.

## Research matrix: August 2026

The first survey found clean digital candidates in the following lanes:

- **Buddhist/Jaina:** GRETIL witnesses for Nāgārjuna’s *Ratnāvalī*,
  *Śūnyatāsaptati*, and Sanskrit-reconstruction *Yuktiṣaṣṭikā*; Candrakīrti’s
  *Prasannapadā*; Asaṅga’s *Bodhisattvabhūmi*; Dharmakīrti’s *Vādanyāya*;
  Haribhadra’s *Śāstravārttāsamuccaya*; and Samantabhadra’s *Āptamīmāṃsā*.
  These are candidates, not complete verification. The Ratnāvalī witness is
  explicitly partial and the Yuktiṣaṣṭikā is a reconstruction.
- **Vaiṣṇava:** GRETIL has clean candidates for Rūpa Gosvāmin’s
  *Laghubhāgavatāmṛta* and *Ujjvalanīlamaṇi*. No clean complete source was
  located for Nimbārka’s *Vedāntapārijātasaurabha*, Vallabha’s *Aṇubhāṣya*,
  or Baladeva’s *Govindabhāṣya*.
- **Classical Vedānta:** Much more is already local than older inventories
  report. Sanskrit Wikisource supplies a clean Unicode candidate for Rāmānuja’s
  *Śaraṇāgatigadya*, but no clean complete *Śrībhāṣya*, *Vedānta-Dīpa*, or
  *Vedānta-Sāra* was found. Do not substitute partial *Śrībhāṣya* 1.1.3 for
  the whole work.
- **Śaiva/Śākta:** GRETIL TEI has high-value candidates including
  Abhinavagupta’s *Tantrāloka*, *Tantrasāra*, and
  *Īśvarapratyabhijñāvimarśinī*; Utpaladeva’s
  *Īśvarapratyabhijñākārikā*; Kṣemarāja’s *Pratyabhijñāhṛdaya*; and multiple
  Śaiva-Siddhānta/Āgama witnesses. *Śivadṛṣṭi* and Sadyojyotis’ principal
  works remain true no-clean-digital-witness gaps.
- **Nyāya, Mīmāṃsā, Yoga, Sāṅkhya, poetics:** current local coverage already
  includes the basic Nyāya, Mīmāṃsā, Yoga, grammar, and poetics corpus.
  Good candidate additions include Sāṅkhya commentarial corpora,
  *Yuktidīpikā*, Haṭhayogapradīpikā, Bhāmaha, Daṇḍin, and Vāmana. Do not
  accept partial, unproofread, or legacy-GRETIL records as complete witnesses.

Important true gaps include *Nyāyamañjarī*, complete *Tantravārttika*,
*Yoga-Vārttika*, *Sāṅkhya-Pravacana-Bhāṣya*, *Tattvavaiśāradī*, and several
lost or fragmentary early Vedānta works. A nearby text is never a substitute.

### Muktabodha correction

The tantric database requested in the acquisition brief is the **Muktabodha
Digital Library**, not a speculative lead. Dr. **Mark S. G. Dyczkowski**, who
studied with Swami Lakshman Joo, served as its Academic Advisor and trained the
team that transcribed many of its searchable e-texts. Muktabodha reports more
than 570 searchable Sanskrit e-texts and a much larger image/transcript
collection across Kashmir Śaiva, Śaiva Siddhānta, Pāñcarātra, Śrīvidyā,
Śākta, Nātha, and Vīraśaiva traditions.

Use <https://muktabodha-digital-library.org/welcome> for its current e-text
interface and the legacy catalogue for IFP/Vedic holdings. Each title must be
checked individually for searchable-text availability, completeness, export
permission, and edition metadata. Muktabodha scans or access-only records are
discovery/collation aids, not automatic public-witness candidates.
