# TITUS — Thesaurus Indogermanischer Text- und Sprachmaterialien (registry only)

**Homepage:** https://titus.uni-frankfurt.de/indexe.htm (HTTP 200, served
Apache, content unchanged since 2017-07-10 per `Last-Modified`).
**License:** TITUS does not publish a redistributable-bulk-download
licence; the project's public terms permit research browsing and
attribution-bearing reuse of individual files. Treat as
"academic-use-with-attribution"; contact `titus@em.uni-frankfurt.de`
for redistribution rights.

## Status

Registry-only. The TITUS Sanskrit catalogue is browsed via HTML index
pages under `texte/etcs/ind/aind/`; there is no public single-zip dump.
The high-value targets are recorded in the manifest:

- Rigveda Saṃhitāpāṭha + Padapāṭha (Frankfurt encoding, full 10 maṇḍalas).
- Atharvaveda Śaunaka.
- Yajurveda Taittirīya.
- Sāmaveda.
- Classical Sanskrit kāvya + drama (per-author index).

Per-file URLs follow the pattern
`http://titus.uni-frankfurt.de/texte/etcs/ind/aind/ved/<branch>/<file>.htm`
and are HTML with embedded TITUS-XML metadata. Fetch route on a future
run: per-URL scrape at 1 req/sec; expect ~50-80 MB total for the full
Vedic Rigveda Padapāṭha set.

GRETIL already ships the Vedic Saṃhitā + Padapāṭha as plain text
(`1_veda/1_sam/`), so the unique TITUS value is the Frankfurt-school
philological apparatus + non-Sanskrit Indo-European comparators. Lane 1
does not need TITUS for the Sanskrit-only side.
