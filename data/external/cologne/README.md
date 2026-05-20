# Cologne Digital Sanskrit Dictionaries — Lane 5 mirror

**Source:** Cologne Digital Sanskrit Dictionaries, Institut für Indologie und Tamilistik, Universität zu Köln
**Homepage:** https://www.sanskrit-lexicon.uni-koeln.de/
**Date fetched:** 2026-05-19
**Branch:** corpus/external-unblock-2026-05-19

## Files in this directory

| File | Size | Description |
|---|---|---|
| `mwxml.zip` | 11.41 MB | Monier-Williams 1899 Sanskrit-English Dictionary — XML, by headword |
| `mwtxt.zip` | 10.59 MB | Monier-Williams 1899 — text version (SLP1 transliteration) |
| `apxml.zip` | 6.14 MB | Apte 1957 Practical Sanskrit-English Dictionary — XML |
| `aptxt.zip` | 5.74 MB | Apte 1957 — text version |

SHA-256 fingerprints, exact byte sizes, and upstream URLs are in `data/external_ingest_manifest_lane5.json` under the `lane5_additions` array (slugs: `cologne_mw_xml`, `cologne_mw_txt`, `cologne_apte_xml`, `cologne_apte_txt`).

## Schema notes

- **Encoding:** SLP1 (`mw.xml`, `ap.xml` use SLP1 transliteration for the headwords). DTD bundled in `mw.dtd` / `ap.dtd` inside each zip.
- **Header:** `mwheader.xml` / `apheader.xml` carry the per-dictionary license statement.
- **Structure:** XML files have one `<H>` (headword) element per entry, with `<h>` (head) and `<body>` children. The `mw.xml` also exposes `<key1>` (SLP1 form) and `<key2>` (display form).

## License

Cologne Digital Sanskrit Dictionaries are released under an attribution-required license; precise terms are in each zip's `*header.xml`. Default policy: **academic re-use with citation to the Cologne project and the source dictionary**. The Cologne site explicitly grants download access for these dictionaries via the public `/scans/.../downloads/*.zip` URLs. No CAPTCHA, no registration.

If we redistribute extracts, the per-entry `<H>` records must carry attribution to "Cologne Digital Sanskrit Dictionaries, www.sanskrit-lexicon.uni-koeln.de".

## Relationship to prakriya lexicon

`prakriya` already bundles MW + Apte indexes at `/nas/ucb/eeshan/prakriya/src/prakriya/data/lexicon/` derived from these same Cologne XML files. The zip files in this directory are the **upstream canonical witness**: keep them here, parse them on demand, and do not re-fetch what prakriya already exposes through its API.

## Direct download URLs (re-verified 2026-05-19)

- https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/downloads/mwxml.zip
- https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/downloads/mwtxt.zip
- https://www.sanskrit-lexicon.uni-koeln.de/scans/APScan/2020/downloads/apxml.zip
- https://www.sanskrit-lexicon.uni-koeln.de/scans/APScan/2020/downloads/aptxt.zip

## DSAL substitution rationale

The Digital South Asia Library (DSAL) hosts the same dictionaries (MW, Apte) but as **publisher-restricted bulk-XML** — no anonymous download. Cologne is the upstream and the canonical free source. This satisfies sub-task (c) of Lane 5: DSAL → Cologne substitute.
