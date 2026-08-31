#!/usr/bin/env sh
# Run the repository's committed, read-only validation scripts.
#
# This intentionally does not build the site or infer checks from tooling that
# is not present in the repository.  The declared Node and Python dependencies
# are required: a missing runtime must fail instead of silently reducing the
# release gate.  CI provisions them before invoking this one entry point.

set -u

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root" || exit 1

failures=0

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

require_command() {
    label=$1
    command_name=$2

    printf '\n== %s ==\n' "$label"
    if command -v "$command_name" >/dev/null 2>&1; then
        printf 'PASS: %s\n' "$label"
        return 0
    fi
    printf 'FAIL: %s (%s is not installed)\n' "$label" "$command_name" >&2
    failures=$((failures + 1))
    return 1
}

if require_command "Node.js runtime" node; then
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
fi

if require_command "Python runtime" python3; then
    run_check "Chinmayananda transcription normalization" python3 scripts/normalize_chinmayananda_transcription.py --check
    if python3 -c 'import indic_transliteration' >/dev/null 2>&1; then
        run_check "Gita witness verification" python3 scripts/check_gita_witness.py
        run_check "Sahasranama name-analysis reviews" python3 scripts/validate_vishnu_name_analysis_review.py
        run_check "Chinmayananda derivation reviews" python3 scripts/validate_chinmayananda_derivation_reviews.py
        run_check "Chinmayananda footnote apparatus" python3 scripts/validate_chinmayananda_footnote_apparatus.py
        run_check "Chinmayananda inline Sanskrit" python3 scripts/validate_chinmayananda_inline_sanskrit.py
        run_check "Chinmayananda Sanskrit commentary" python3 scripts/validate_chinmayananda_sanskrit_analysis.py --require-complete
        run_check "Chinmayananda ASCII Sanskrit" python3 scripts/validate_chinmayananda_ascii_sanskrit.py
        run_check "Sahasranama reader builder" python3 scripts/build_vishnu_sahasranama_reader.py --check gita/vishnu-sahasranama/reader.json --require-commentary
        run_check "Sahasranama presentation" python3 scripts/validate_sahasranama_presentation.py
    else
        printf '\n== Indic transliteration dependency ==\nFAIL: Indic transliteration dependency (Python package indic_transliteration is not installed)\n' >&2
        failures=$((failures + 1))
    fi
fi

printf '\nValidation complete: %s failure(s).\n' "$failures"
test "$failures" -eq 0
