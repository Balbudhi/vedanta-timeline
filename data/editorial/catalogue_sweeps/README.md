# Catalogue sweep records

Each record here is an auditable answer to a source-catalogue question. A
catalogue hit is not a public source promotion. It may be a clean candidate,
an account-gated e-book, a title collision, a scan, or a no-match.

`ebharatisampat_title_sweep_2026-08-19.json` records all 368 Sanskrit
missing/degraded thinker works queried against E-Bharatisampat's public title
search. `ebharatisampat_strict_details_2026-08-19.json` preserves the 90
strict-title candidate records and their public metadata-page headings. The
results distinguish public Unicode readers from account-gated e-books only
after inspecting the individual record.

`ebharatisampat_author_confirmed_2026-08-19.json` is the conservative subset:
26 existing thinker works (42 editions) where the public catalogue's named
author matches the thinker record. It excludes title collisions, blank-author
records, and commentary-only matches. It is the authoritative eBhāratī
retrieval queue; an `ebook-reader` entry still needs an authenticated download
and a `public-unicode-reader` entry still needs witness-quality review.

Run `node scripts/check_ebharatisampat_sweep.js` to ensure the sweep still
covers every current Sanskrit gap. When the worklist changes, create a new
dated sweep rather than silently modifying the historical result.

The seven `*-queue-acquisition-audit.json` files are disjoint work-partition
audits. They preserve positive sources, title collisions, access restrictions,
lost/fragmentary cases, and verified no-match outcomes. Run
`node scripts/report_partition_coverage.js` to compare their union against the
live Sanskrit gap queue; duplicate boundary figures are informational, while a
missing row is a failure.
