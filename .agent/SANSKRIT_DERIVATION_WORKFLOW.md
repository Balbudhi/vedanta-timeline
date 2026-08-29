# Sanskrit derivation workflow

Use the personal skill
`/Users/eeshan/.codex/skills/sanskrit-source-derivation-review/SKILL.md`
for every public Sanskrit derivation, root claim, or word-analysis certification
in this repository.

The producer must derive from `/Users/eeshan/Dev/prakriya/sources/` directly;
the unfinished interpreter, generated traces/tables, Vidyut, parser output, and
dictionary guesses are not authority. A separate reviewer must recompute the
analysis from the sources. Schema validation is not independent review.

For commentator derivations, independently check the printed claim while
building the popup, but do not add a public comparison verdict unless the user
asks. The commentary stays unchanged and the popup presents the supported
grammar, so any difference remains inspectable without editorial argument.

Never leave a root field empty when the public prose discusses a root and the
grammar sources support one. Never use placeholder morphology such as
“surface token preserved” or “see parts” in a reviewed record.

The completeness inventory must also review undiacritized Roman Sanskrit in
older scans (for example `Tvam` or `Atman`). A deterministic folded-form match
may locate a candidate but is never authority: accept or reject it in context,
restore proper IAST only in the popup, and do not map an ambiguous ASCII form to
a different Sanskrit word. English joined to Sanskrit by an OCR-style hyphen
stays English prose; never invent a Sanskrit compound or morpheme for it.

For the current Sahasranāma pass, run:

```sh
python3 /Users/eeshan/.codex/skills/sanskrit-source-derivation-review/scripts/audit_claims.py \
  --commentary gita/vishnu-sahasranama/chinmayananda.json \
  --analysis gita/vishnu-sahasranama/analysis.json
python3 scripts/audit_chinmayananda_sanskrit_coverage.py --check --summary
python3 scripts/validate_chinmayananda_sanskrit_analysis.py --require-complete
python3 scripts/validate_chinmayananda_inline_sanskrit.py
python3 scripts/validate_chinmayananda_ascii_sanskrit.py
```
