# Thinker-first acquisition coverage — 2026-08-19

## Completion boundary for the audit phase

The live Sanskrit missing/degraded queue had **367** work records when the
audit was closed. `node scripts/report_partition_coverage.js` verifies that
every one appears in a work-partition result. This is a coverage check, not a
claim that every work is available or ready for publication.

The full matrix is machine-readable in `data/editorial/catalogue_sweeps/`:

| Partition | Records | File |
|---|---:|---|
| Advaita / Avibhāgādvaita | 50 | `advaita-queue-acquisition-audit.json` |
| Vaiṣṇava schools and Pāñcarātra | 95 | `vaishnava-queue-acquisition-audit.json` |
| Tattvavāda / Dvaita | 31 | `dvaita-queue-acquisition-audit.json` |
| Buddhist and Jaina | 95 | `buddhist-jain-queue-acquisition-audit.json` |
| Nyāya, Mīmāṃsā, Sāṅkhya, Yoga, grammar, poetics | 41 | `darsanas-queue-acquisition-audit.json` |
| Śaiva, Śākta, Pāśupata, Nāth, regional | 49 | `saiva-regional-queue-acquisition-audit.json` |
| Cross-tradition residual | 41 | `cross-residual-queue-acquisition-audit.json` |

Boundary figures may occur in two files; this is reported but not treated as
a coverage failure. Historical rows no longer in the live queue remain in
some audit files for provenance.

## Catalogue evidence

- E-Bharatisampat: all 368 then-current title queries are recorded, alongside
  the 26 author-confirmed work subset. Public Unicode HTML and account-gated
  e-books are distinguished.
- SARIT: every corpus XML was checked; named-edition TEI candidates are in the
  candidate registry and relevant files have entered quarantine.
- Muktabodha, GRETIL, Sanskrit Wikisource, Sanskrit Documents, DSBC, JainQQ,
  Project Madurai, Marathi Wikisource, Vachana Sanchaya, and school-specific
  archives are recorded in [the source database registry](SOURCE_DATABASE_REGISTRY.md).

## Unresolved categories

The audit records individual outcomes rather than substituting a similar title
for a missing work. A work may remain unresolved because it is:

- `no-exact-sanskrit-witness-found` after the listed catalogue checks;
- `lost/fragmentary/citation-only`, where no full original can exist;
- `scan-only` or `reader-or-collation-only`, retained as a source/edition lead;
- `account-gated`, queued for authenticated retrieval;
- `attribution-conflict` or `wrong-author-or-work`, which requires editorial
  correction before acquisition; or
- a clean/public or structured candidate, already in raw quarantine awaiting
  header review and collation.

The next work is therefore mechanical and bounded: fetch the public clean and
public Unicode candidates, keep scan material in the scan lane, then promote
only witnesses that meet the explicit source and provenance gates.
