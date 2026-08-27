#!/usr/bin/env sh
# Run the repository's committed, read-only validation scripts.
#
# This intentionally does not build the site or infer checks from tooling that
# is not present in the repository.  A missing optional runtime is reported as
# a skip so contributors can still run the checks their environment supports;
# CI provisions all declared runtimes and therefore runs every check.

set -u

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root" || exit 1

failures=0
skips=0

run_check() {
    label=$1
    shift

    printf '\n== %s ==\n' "$label"
    if "$@"; then
        printf 'PASS: %s\n' "$label"
    else
        printf 'FAIL: %s\n' "$label" >&2
        failures=$((failures + 1))
    fi
}

skip_check() {
    printf '\n== %s ==\nSKIP: %s\n' "$1" "$2"
    skips=$((skips + 1))
}

if command -v node >/dev/null 2>&1; then
    run_check "Chronology resolver" node scripts/check_chronology.js
    run_check "Chronology coverage report" node scripts/report_chronology_coverage.js
    run_check "Thinker references" node scripts/check_thinker_references.js
    run_check "Citation-link integrity" node scripts/check_citation_links.js
    run_check "Sanskrit reader completeness report" node scripts/report_reader_completeness.js
    run_check "Gita slot integrity" node scripts/validate_gita_slots.js
    run_check "Gita term consistency" node scripts/check_gita_terms.js
    run_check "Corpus coverage report" node scripts/check_coverage.js
    run_check "Source inventory integrity" node scripts/check_source_inventory.js
    run_check "Source candidate integrity" node scripts/check_source_candidates.js
    run_check "Intake witness integrity" node scripts/check_intake_witnesses.js
    run_check "TEI intake metadata" node scripts/check_tei_intake_metadata.js
    run_check "E-Bharatisampat Unicode intake" node scripts/check_ebharati_unicode_intake.js
    run_check "Scan intake integrity" node scripts/check_scan_intake.js
    run_check "Work witness-link report" node scripts/report_work_witness_links.js
    run_check "School source-coverage report" node scripts/report_school_source_coverage.js
    run_check "E-Bharatisampat sweep coverage" node scripts/check_ebharatisampat_sweep.js
    run_check "Partition sweep coverage" node scripts/report_partition_coverage.js
    run_check "Editorial contract integrity" node scripts/check_editorial_contracts.js
    run_check "Editorial readiness report" node scripts/report_editorial_readiness.js
    run_check "Unmanifested public-source report" node scripts/report_unmanifested_sources.js
    run_check "Glossary completeness report" node scripts/report_glossary_completeness.js
    run_check "Thinker content-shape report" node scripts/report_thinker_content.js
else
    skip_check "Gita term consistency" "node is not installed"
    skip_check "Corpus coverage report" "node is not installed"
fi

if ! command -v python3 >/dev/null 2>&1; then
    skip_check "Gita witness verification" "python3 is not installed"
else
    run_check "Chinmayananda transcription normalization" python3 scripts/normalize_chinmayananda_transcription.py --check
    if ! python3 -c 'import indic_transliteration' >/dev/null 2>&1; then
        skip_check "Gita witness verification" "Python package indic_transliteration is not installed"
    else
        run_check "Gita witness verification" python3 scripts/check_gita_witness.py
    fi
fi

printf '\nValidation complete: %s failure(s), %s skipped.\n' "$failures" "$skips"
test "$failures" -eq 0
