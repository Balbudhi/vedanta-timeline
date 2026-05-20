# Indica et Buddhica — Lane 5 status report

**Date:** 2026-05-19
**Branch:** corpus/external-unblock-2026-05-19

## Lane 2 finding

Lane 2 hit `ECONNREFUSED` against indica-et-buddhica.org and deferred.

## Lane 5 attempted retries

| Attempt | Timestamp (UTC) | URL probed | Result |
|---|---|---|---|
| 1 | 2026-05-19 ~00:03 | https://indica-et-buddhica.org/ | 301 redirect to https://indica-et-buddhica.com/ (host moved) |
| 2 | 2026-05-19 ~00:05 | https://indica-et-buddhica.com/ | HTTP 200 — site is reachable |
| 3 | 2026-05-19 ~00:09 | https://indica-et-buddhica.com/repositorium | HTTP 404 — the TEI repositorium path is gone |

Three attempts at 10-minute cadence were **not** needed for connectivity — the site responded immediately. The blocker is *content*, not network.

## Diagnosis

The host has changed (`.org` → `.com`) and the operator (Indica et Buddhica Publishers Limited NZ, NZBN 9429041761809) has restructured the site as a **publisher catalogue only**. The former `/repositorium/sources` and `/repositorium/textus` TEI critical-edition tree that Lane 2 expected is no longer published at this host.

Current top-level nav:

- /authors
- /publications
- /about/indica-et-buddhica-publishers
- /about/contact-us

No primary-source TEI index, no XML/TEI file links, no `/repositorium` path.

## Recommendation for Lane 6 / Lane 8

The Indica-et-Buddhica TEI tree must be considered **archived / withdrawn from the open web** as of 2026-05-19. Three remediation paths:

1. **Wayback Machine** — query `web.archive.org/web/*/indica-et-buddhica.org/repositorium/*` to recover the TEI files Lane 2 had earmarked.
2. **GitHub mirrors** — search for forks; the project's earlier TEI corpus was on GitHub (`indica-et-buddhica`/`textus`) some years ago.
3. **Contact the publisher** — `/about/contact-us` to request the legacy TEI archive.

No fetches were performed in Lane 5 for this source. No manifest entries beyond this STATUS note. Source-id `indica_et_buddhica` in `data/external_ingest_manifest.json` should be marked `fetch_status: archived_unavailable` until Wayback / mirror recovery succeeds.
