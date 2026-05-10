#!/usr/bin/env bash
# Wave-1 glossary expansion: dispatch one Codex 5.4 (reasoning=high) job per top-30 term.
# Each job reads the existing glossary entry, the citation_index, the thinker JSONs,
# and the full_translations corpus, and writes an enriched per_school[] + new_citations[]
# to handoffs/wave1_glossary_outputs/<TERM>.out.json.

set -u
ROOT=/home/eeshan/philosophy
mkdir -p "$ROOT/handoffs/wave1_glossary_outputs"
mkdir -p "$ROOT/handoffs/wave1_glossary_logs"

PROMPT_TEMPLATE="$(cat "$ROOT/prompts/glossary_wave1_per_term.md")"
SPEC_JSON="$ROOT/handoffs/glossary_top30_gaps.json"

dispatch_codex() {
  local term="$1"; shift
  local prompt="$1"; shift
  local label="glossary_wave1_${term}"
  local out="$ROOT/handoffs/wave1_glossary_outputs/${term}.out.json"
  if [ -f "$out" ]; then
    echo "SKIP $term — output exists"
    return 0
  fi
  cd "$ROOT" && nohup codex exec \
    --skip-git-repo-check --json \
    -c 'model="gpt-5.4"' \
    -c 'model_reasoning_effort="high"' \
    -c 'service_tier="fast"' \
    --add-dir "$ROOT" \
    --dangerously-bypass-approvals-and-sandbox \
    --output-last-message "$ROOT/handoffs/wave1_glossary_logs/${label}_lastmsg.txt" \
    "$prompt" \
    > "$ROOT/handoffs/wave1_glossary_logs/${label}.log" 2>&1 &
  echo "$(date -Iseconds)	dispatch	${label}	pid=$!" >> "$ROOT/handoffs/cron_log.tsv"
  echo "[${label}] pid=$!"
}

# Build per-term prompts using Python (cleaner string interpolation)
python3 - <<PYEOF
import json, os, subprocess, shlex
ROOT="$ROOT"
spec=json.load(open(f"{ROOT}/handoffs/glossary_top30_gaps.json"))['top30_gap_analysis']
template=open(f"{ROOT}/prompts/glossary_wave1_per_term.md").read()
os.makedirs(f"{ROOT}/handoffs/wave1_glossary_prompts", exist_ok=True)
for r in spec:
    term=r['file'].replace('.json','')
    cands=[]
    for c in r['top_citations'][:20]:
        cands.append(f"- cite://{c['cid']}  ({c['thinker']} / {c['locus_short']})  [school: {c['school']}]")
    p = (template
         .replace('<TERM>', term)
         .replace('<TERM_IAST>', r['term_iast'])
         .replace('<CUR_N>', str(len(r['current_schools'])))
         .replace('<ALIASES>', ', '.join(r['aliases']))
         .replace('<CURRENT_SCHOOLS>', ', '.join(r['current_schools']) or '(none)')
         .replace('<EVIDENCE_SCHOOLS>', ', '.join(r['schools_with_citation_evidence']) or '(none)')
         .replace('<CITATION_CANDIDATES>', '\n'.join(cands) or '(none — search the on-disk corpus)'))
    open(f"{ROOT}/handoffs/wave1_glossary_prompts/{term}.prompt.md",'w').write(p)
print("prompts written:", len(spec))
PYEOF

# Concurrency cap: dispatch in batches; check active codex count and back off if too many.
MAX_CONCURRENT="${MAX_CONCURRENT:-6}"
TERMS=$(python3 -c "import json; d=json.load(open('$SPEC_JSON'))['top30_gap_analysis']; print(' '.join(r['file'].replace('.json','') for r in d))")

for term in $TERMS; do
  while [ "$(pgrep -fc 'codex exec.*glossary_wave1' || true)" -ge "$MAX_CONCURRENT" ]; do
    sleep 5
  done
  prompt_file="$ROOT/handoffs/wave1_glossary_prompts/${term}.prompt.md"
  prompt="$(cat "$prompt_file")"
  dispatch_codex "$term" "$prompt"
done

echo "wave1 glossary dispatch initiated."
ps -ef | grep "codex exec.*glossary_wave1" | grep -v grep | wc -l
