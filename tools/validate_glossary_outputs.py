#!/usr/bin/env python3
"""Validate Codex Wave-1 glossary outputs.

Per-output checks:
  - JSON parses.
  - Has term_key, per_school[].
  - Each per_school[] entry has school + definition + (citations | NOT YET RETRIEVED).
  - All cite:// keys in `citations[].cite` resolve to citation_index.json.
  - new_citations[] entries have all required fields.
  - Inline markdown cite:// links (in definition prose) parse and resolve.
"""
import json, re, sys
from pathlib import Path

ROOT = Path('/orcd/home/002/eeshan/philosophy')
OUT_DIR = ROOT / 'handoffs/wave1_glossary_outputs'
CIDX = json.load(open(ROOT / 'site/data/citation_index.json'))['entries']

# Match either [label](cite://KEY) or [label](<cite://KEY>)
INLINE_CITE_RE = re.compile(r'cite://([^\)>\]]+?(?: [^\)>\]]+)*?)(?:[>\)])')


def validate(path: Path) -> dict:
    name = path.stem.replace('.out', '')
    try:
        d = json.load(open(path))
    except Exception as e:
        return {'term': name, 'ok': False, 'errors': [f'parse: {e}']}
    errs = []
    if 'per_school' not in d or not isinstance(d['per_school'], list):
        errs.append('missing per_school[]')
    real = 0
    placeholder = 0
    bad_cites = []
    inline_bad = []
    for i, ps in enumerate(d.get('per_school') or []):
        if 'school' not in ps or 'definition' not in ps:
            errs.append(f'per_school[{i}] missing school/definition')
            continue
        defn = ps['definition'].strip()
        if defn.startswith('[NOT YET RETRIEVED]'):
            placeholder += 1
            continue
        real += 1
        # structured citations
        for c in ps.get('citations') or []:
            ck = c.get('cite', '').replace('cite://', '')
            if ck and ck not in CIDX:
                bad_cites.append((ps['school'], ck))
        # inline markdown
        for m in INLINE_CITE_RE.findall(defn):
            ck = m.strip()
            if ck not in CIDX:
                inline_bad.append((ps['school'], ck))
    new_cits = d.get('new_citations') or []
    nc_errs = []
    for nc in new_cits:
        for k in ('cite_key', 'thinker_id', 'work_id', 'sanskrit_iast', 'english_close'):
            if k not in nc:
                nc_errs.append(f'new_citations missing key: {k}')
                break
    return {
        'term': name,
        'ok': not (errs or bad_cites or nc_errs),
        'errors': errs,
        'real_schools': real,
        'placeholders': placeholder,
        'bad_structured_cites': bad_cites,
        'inline_unresolved_cites': inline_bad,
        'new_citations': len(new_cits),
        'nc_errs': nc_errs,
    }


def main():
    outs = sorted(OUT_DIR.glob('*.out.json'))
    if not outs:
        print('no outputs yet')
        return
    print(f'{"term":15s} {"ok":3s} {"real":>4s} {"plh":>4s} {"new":>4s}  bad_struct  inline_unres')
    total_real = 0
    total_plh = 0
    for p in outs:
        r = validate(p)
        print(f'{r["term"]:15s} {"Y" if r["ok"] else "N":3s} {r.get("real_schools", 0):4d} {r.get("placeholders", 0):4d} {r.get("new_citations", 0):4d}  {len(r.get("bad_structured_cites", [])):>5d}       {len(r.get("inline_unresolved_cites", [])):>5d}')
        total_real += r.get('real_schools', 0)
        total_plh += r.get('placeholders', 0)
        if r.get('bad_structured_cites'):
            for s, c in r['bad_structured_cites'][:3]:
                print(f'    bad-struct ({s}): {c}')
        if r.get('inline_unresolved_cites'):
            for s, c in r['inline_unresolved_cites'][:3]:
                print(f'    inline-unres ({s}): {c}')
    print(f'\nTotals: outputs={len(outs)} real_schools_sum={total_real} placeholders_sum={total_plh}')


if __name__ == '__main__':
    main()
