# Architecture

This document describes the repository as it is served now. It is a static
site: [`index.html`](../index.html) loads the vanilla ES module
[`assets/app.js`](../assets/app.js), which fetches committed files at runtime.
There is no application build, generated schema bundle, or server-side data
API.

## Runtime surface

- `index.html` loads `assets/style.css`, `assets/gita.css`, and `assets/app.js`.
  `app.js` renders the timeline, network view, filters, and the unified detail
  panel.
- `gita/` contains separately served reading pages; their page-specific data
  and scripts are not loaded by the timeline module. `bhakti/` similarly
  contains independently served song pages.
- The main module starts with `data/manifest.json`. It loads the listed thinker
  records from `data/thinkers/`, then loads school registries, the primitive
  graph, full-translation index, glossary, perspectives, and citation index.
  Missing optional JSON is treated as unavailable rather than generated.

## Public data layout

`data/` is the public runtime corpus. Its path names are part of the static
site contract.

| Path | Runtime role |
| --- | --- |
| `manifest.json` | Lists thinker records, comparative-claim records, and polemic-chain metadata for the corpus. |
| `thinkers/<id>.json` | A thinker profile: identity, legacy dates and optional chronology variants, school/lineage links, works, passages, and display metadata. |
| `registries/` | School and sub-school presentation data plus the primitive graph; `schools.json`, `sub_schools.json`, and `primitive_graph.json` are fetched by the main module. |
| `full_translations/index.json` and `full_translations/<thinker>__<work>.md` | The index advertises available extended translations; the reader fetches the matching Markdown file on demand. |
| `glossary/manifest.json` and `glossary/<term>.json` | The manifest enumerates glossary records. The app maps `term_key` and aliases to an entry, then creates its IAST-aware inline lookup matcher. |
| `citation_index.json` | Canonical passage records keyed by the part after `cite://`; aliases resolve to a canonical record. |
| `primary_text_manifest.json` and `sources/` | The source-browser manifest and the public source witnesses it may fetch under `data/sources/`. |
| `articles/` and `perspectives/` | Manifest-driven Markdown material for article and explicitly interpretive-perspective views. |
| `polemic_chains/` | Stored polemic-chain records; the current main module does not fetch them. |

`data/comparative_claims/` is supported by the loader when entries appear in
`manifest.json`; the current manifest contains no such entries. Do not assume a
directory, record count, or a complete schema-defined corpus beyond files that
are committed and manifest-referenced.

## Timeline and chronology

The timeline lays out visible (`display !== false`) thinker records by the
active chronology and uses school tokens and lineage data for lanes/network
relationships. The active chronology is selected by `?chronology=academic` or
`?chronology=traditional`, then local storage, then a record's default; the
choice is persisted by the UI.

Newer records may contain:

```json
{
  "chronology": {
    "default_variant": "academic",
    "variants": {
      "academic": { "low": 700, "high": 750, "tier": "consensus-textual" },
      "traditional": { "low": 788, "high": 820, "tier": "lineage-internal" }
    }
  }
}
```

`low` is required for a usable variant; `high` may be `null` for a living
thinker. If the requested variant is absent, the resolver uses another stored
variant when available, otherwise the legacy top-level `dates_low`,
`dates_high`, `dates_tier`, and `dates_notes` fields. The UI explicitly marks a
requested-mode fallback. It never invents a traditional date. Legacy dates
therefore remain a supported compatibility contract, not an error condition.

## Readers, glossary, and citations

The detail panel has Thinker, Translation, Article, Citation, and Source tabs.
Tabs are revealed as their content is opened and retain their rendered content
within the panel.

- A work reader fetches its `full_translations/<thinker>__<work>.md` file when
  present. Otherwise it renders the work summary and any engaged passages with
  an explicit availability/status explanation; it does not fabricate a full
  translation.
- The source tab reads only files declared in `primary_text_manifest.json` and
  fetches them at `data/sources/<manifest path>`.
- Prose may link a citation as `[label](cite://thinker/work/locus)`. The
  citation index provides the displayed passage, aliases, verification state,
  and any public source URL. Missing, unverified, and pending-acquisition
  citations are surfaced as such rather than silently treated as quotations.
- Glossary entries are independent JSON records. Their `term_key` and aliases
  make terms clickable in rendered site prose; a glossary entry may itself use
  `cite://` links. The matcher is deliberately not a Sanskrit sandhi or
  compound segmenter.

## Source boundary

`data/primary_text_manifest.json` inventories only source witnesses actually
committed below `data/sources/`; its paths must be relative to the manifest
root. The source browser is a viewer for that public mirror, not proof that a
witness is complete, verified, or citation-safe.

The binding policy is [Source inventory policy](SOURCE_INVENTORY_POLICY.md) and
[Content and source standard](CONTENT_AND_SOURCE_STANDARD.md). In brief:

- keep private or rights-unresolved acquisitions outside the public repository;
- treat `data/sources/_unverified_ocr/` as a public search-aid quarantine, not
  a citation corpus; and
- publish a quotation only with its provenance, locus, eligible witness, and
  canonical citation-index route as required by the standard.

## Validation and CI

The supported repository-wide command is:

```sh
sh scripts/run_checks.sh
```

It runs the committed chronology, Gītā, coverage, and source-inventory checks
when Node is available, and the Gītā witness check when Python plus
`indic_transliteration` are available. Local environments may report skipped
optional-runtime checks. GitHub Actions runs the same command in
`.github/workflows/validate.yml` after provisioning Node 22, Python 3.12, and
`indic-transliteration` for pull requests and pushes to `main`.

For a targeted JSON edit, also use `python3 -m json.tool <file> >/dev/null` and
the surface-specific checks required by the content standard.

## Non-guarantees

- The repository has no committed universal JSON Schema contract or build-time
  schema validation for every data file.
- A manifest entry, on-disk text, translation card, citation record, or
  `reviewed` status is not by itself a scholarly verification or a claim of
  complete coverage.
- Runtime fetch support for a path does not mean that the current deployment
  contains every optional dataset; the manifest and HTTP result are decisive.
- The static source viewer does not expose private reference material or turn
  a quarantined/working witness into a citable edition.
