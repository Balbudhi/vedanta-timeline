# Vedānta — a realist tradition

**Live site: [vedanta.eeshan.xyz](https://vedanta.eeshan.xyz/)**

An interactive timeline of Vedāntic thinkers and the schools they argue with, plus
word-by-word Sanskrit reading pages and a cross-linked glossary. Each thinker entry
carries a core thesis, an `engaged_works` list with ascription tiers, key passages with
Pāṇinian breakdown (pada-analysis · samāsa-vigraha · kāraka structure · lakāra), and
lineage edges (teacher / student / polemical) to the rest of the corpus.

Two things to know before reading anything here:

- **The site's prose is AI-generated.** Thinker entries, work summaries, passage
  selections, Sanskrit transcription and morphology, and the comparative analyses were
  composed by large language models working from primary texts on disk and from the
  editions cited in each entry. Every claim is meant to be checkable against the cited
  locus. A misreading is a defect of the synthesis, not of the tradition — please report
  it.
- **The site is unlisted, not private.** `robots.txt` and a `noindex` meta keep it out of
  search engines and out of the crawlers that honour them, but they restrict nothing:
  anyone with the URL sees everything, and a scraper that ignores `robots.txt` can read
  the whole site. Share by direct link, and do not put anything here that would be a
  problem to find in public.

---

## What is on the site

| | |
|---|---|
| **Timeline** | 281 thinker entries — 252 plotted on the timeline, the rest cross-tradition entries that exist for article cross-reference — across Vedāntic schools (Advaita, Viśiṣṭādvaita, Dvaita, Bhedābheda, Acintya-Bhedābheda, Śuddhādvaita, Avibhāgādvaita, proto-Vedānta) and the traditions they engage — Sāṅkhya, Yoga, Nyāya, Navya-Nyāya, Vaiśeṣika, Pūrva-Mīmāṃsā, Jaina, Cārvāka, Mādhyamaka, Yogācāra, Buddhist-Pramāṇa, Pratyabhijñā/Trika, Śaiva-Siddhānta, Śākta, Pāśupata, Pāñcarātra, Vīraśaiva — plus Western interlocutors. Lane and network views; academic and traditional chronologies side by side. |
| **Glossary** | 246 Sanskrit philosophical terms, each with an invariant definition plus per-school definitions where schools genuinely diverge. Clickable from any term occurrence. |
| **Sanskrit readers** | Gītā reading pages at [`gita/sthitaprajna/`](gita/sthitaprajna/) (2.54–72), [`gita/kama/`](gita/kama/) (3.36–43), and [`gita/ch5/`](gita/ch5/) — source script, IAST, literal translation, tap-a-word morphology, voice-by-voice commentary, recitation audio. |
| **Articles** | Long-form essays and engagements, opened from the **Articles** button. Currently live: [Sin, punishment, forgiveness](data/articles/source/sin-avidya-primary-sources.md), [Madhva and Advaita](data/articles/source/madhva.md), and [Ramakrishna, Vijñāna Vedānta, and Śaṅkara](data/articles/source/engagement-medhananda__vijnana-vedanta-and-sankara.md). |

Drafts that are not live stay in the repository with `"status": "unpublished"` in
[`data/articles/manifest.json`](data/articles/manifest.json); the site filters them out.
The presence of a draft in `data/articles/source/` is not a claim that it has been
reviewed.

---

## Corpus

| Path | Contents |
|---|---|
| [`data/thinkers/`](data/thinkers/) | One JSON per thinker — thesis, works, key passages, lineage edges, chronology tiers. |
| [`data/glossary/`](data/glossary/) | Term entries with invariant and per-school definitions. |
| [`data/full_translations/`](data/full_translations/) | 70 markdown files, one per `<thinker>__<work>`: line-by-line English with Pāṇinian breakdown. |
| [`data/polemic_chains/`](data/polemic_chains/) | 12 major refutations (saptavidhānupapatti, Nyāyāmṛta, Māyāvāda-khaṇḍana, Śatadūṣaṇī, …) reproduced premise → inference → conclusion, with what each argument actually touches and what it leaves intact. |
| [`data/articles/`](data/articles/) | Article manifest, source markdown, and the passage packets readers cite. |
| [`data/perspectives/`](data/perspectives/) | Explicitly framed interpretive re-readings, kept separate from the on-its-own-terms presentation. |
| [`data/sources/`](data/sources/) | The primary-text mirror the citation index resolves against, by language. Public-domain material only. |
| [`data/registries/`](data/registries/) | `schools.json` (color tokens), `sub_schools.json`, `pramanas.json`, `sub_axes.json`, `primitive_graph.json`. |
| [`data/citation_index.json`](data/citation_index.json) | Resolves every `cite://thinker_id/work_id/locus` link to a witness and excerpt. |

---

## Site code

Vanilla HTML / CSS / ES-module JavaScript. No build step, no framework, no dependencies.

- [`index.html`](index.html) — app shell.
- [`assets/app.js`](assets/app.js) — timeline, detail pane, glossary, articles.
- [`assets/gita.js`](assets/gita.js), [`assets/gita.css`](assets/gita.css) — the Sanskrit reader (`window.GitaReader`), reference implementation for [`docs/SANSKRIT_TRANSLATION_STANDARD.md`](docs/SANSKRIT_TRANSLATION_STANDARD.md).

Cladogram layout is deterministic from `school_color_token` (lane), `sub_school_shade`
(sub-lane), and `dates_low`/`dates_high` (x-position).

Run it locally from the repository root — the pages fetch JSON, so `file://` will not
work:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/>.

---

## Repository layout

| Path | |
|---|---|
| `index.html`, `assets/`, `gita/` | The site itself. |
| `data/` | The corpus (above). |
| `docs/` | Standards, schemas, and dated audit reports. |
| `scripts/` | Maintained validators and reports; `run_checks.sh` runs them all. |
| `audit/` | Dated audit outputs referenced by editorial decisions. |
| `to-do/` | Open acquisition and digitisation gaps. |
| `internal/` | Working material from the project's own construction — see [`internal/README.md`](internal/README.md). Not published. |

Absolute paths in provenance notes that read `materials/primary_texts/...` refer to
the local working corpus, which is larger than the mirror in `data/sources/` and is not
in this repository.

## Editorial standard

Content changes are governed by evidence rules, not by style preference. Before adding or
rewriting a thinker, work, citation, glossary entry, reader, or comparative claim, read:

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — the short version.
- [`docs/EDITORIAL_DATA_STANDARD.md`](docs/EDITORIAL_DATA_STANDARD.md) — controlling template for claims, prose, chronology, and sources.
- [`docs/CONTENT_AND_SOURCE_STANDARD.md`](docs/CONTENT_AND_SOURCE_STANDARD.md) — source handling, roster roles, readiness labels.
- [`docs/SANSKRIT_TRANSLATION_STANDARD.md`](docs/SANSKRIT_TRANSLATION_STANDARD.md) — how Sanskrit is presented and translated.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — schemas for thinker / engaged_work / key_passage and the validation rules.
- [`AGENTS.md`](AGENTS.md) — working rules for the shared worktree (path-scoped staging, one logical change per commit).

Three commitments do most of the work: cite claims to a locus that resolves in the
citation index; keep the three voices separate (what the source says, what scholarship
disputes, what this site synthesizes); and state uncertainty — dates, ascriptions, and
reconstructions carry their tier rather than being smoothed into fact.

Rights: this repository is public and ships only material whose licence we can show.
Modern scholarship under copyright, and scans with unresolved rights, live outside it —
secondary-source holdings are in the private `parishishta` repository. Raw OCR in
`data/sources/_unverified_ocr/` is quarantine material: never a witness, never a
citation, never published.

## Validation

```bash
sh scripts/run_checks.sh
```

Runs the committed read-only validators — chronology resolution, thinker references,
citation-link integrity, Gītā slot and term consistency, source-inventory and intake
integrity, plus coverage reports. Missing optional runtimes are reported as skips.
[`.github/workflows/validate.yml`](.github/workflows/validate.yml) provisions Node 22 and
Python 3.12 and runs the full set on every push and pull request.

Reports labelled *report* are backlog signals, not correctness gates; do not describe a
green report as a passing check.

---

## Hosting

GitHub Pages, deployed from `main` by
[`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) on every push.
The custom domain in [`CNAME`](CNAME) is canonical:
`balbudhi.github.io/vedanta-timeline/` 301-redirects to `vedanta.eeshan.xyz`.

**The repository and the site are not the same surface.** The build publishes an
allow-list — `index.html`, `CNAME`, `robots.txt`, `assets/`, `gita/`, and `data/` minus
`sources/` and `editorial/`. Working material stays in the repository, where it is
readable by anyone who wants it, and is not served from the site's origin. Adding a
directory the site must serve means adding it to that allow-list; the build is
deliberately not an exclude-list, because an exclude-list publishes every new directory
by default.

A build step then copies in exactly the text sources listed in
`data/primary_text_manifest.json` (66 files, ~27 MB) and republishes the manifest
describing only what it copied, so the Source tab is served from the site's own origin
and never offers a file that 404s. The 1.17 GB of page-image PDF scans and the
`_intake/` and `_unverified_ocr/` trees are never published.

---

## Provenance

Synthesis, comparative analysis, and audit were done primarily with **Claude Opus**;
primary-source extraction, Sanskrit transcription, and morphological analysis primarily
with **OpenAI Codex (GPT-5.4, reasoning=high)**. The aim is to let an English-only reader
meet each thinker on that thinker's own ground and verify the reading against a specific
locus. Where a figure survives only in later citation (Auḍulomi, Āśmarathya, Kāśakṛtsna,
Bodhāyana, Upavarṣa, Sundara-Pāṇḍya, Brahmadatta), the entry says so and explains how the
dating estimate is derived.

---

## License

[MIT](LICENSE). The primary texts under `data/sources/` carry their own upstream terms —
GRETIL, SARIT, Wikisource, and Project Madurai each state theirs — and the MIT grant
here covers this project's own code, data files, and prose, not those upstream sources.
