#!/usr/bin/env sh
# Content changes are admitted only after their contract and impact notice run.
# This hook is intentionally deterministic and offline: it checks the evidence
# wiring we can prove locally; human source review remains mandatory.

set -eu
repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

node scripts/check_editorial_contracts.js
if [ "$#" -gt 0 ]; then
  node scripts/report_content_impacts.js --changed "$@"
fi
