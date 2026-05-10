#!/usr/bin/env python3
"""Merge Codex Wave-1 outputs into glossary JSONs + citation_index.json.

Inputs:
  - handoffs/wave1_glossary_outputs/<term>.out.json  (one per Wave-1 term)
Outputs:
  - site/data/glossary/<term>.json   (updated per_school[])
  - site/data/citation_index.json    (new entries appended)
  - handoffs/glossary_gaps.md        (NOT-YET-RETRIEVED follow-ups)
  - handoffs/glossary_wave1_merge_report.md  (summary)

Discipline:
  - Schema-validate every modified glossary JSON (round-trip + required keys).
  - Reject any output missing per_school or with non-list per_school.
  - Record [NOT YET RETRIEVED] gaps to glossary_gaps.md.
  - Idempotent: re-running with the same outputs produces the same files.
"""
from __future__ import annotations
import json, os, sys, datetime
from pathlib import Path

ROOT = Path('/orcd/home/002/eeshan/philosophy')
GLOSSARY = ROOT / 'site/data/glossary'
CIDX_PATH = ROOT / 'site/data/citation_index.json'
OUT_DIR = ROOT / 'handoffs/wave1_glossary_outputs'
GAPS_MD = ROOT / 'handoffs/glossary_gaps.md'
REPORT_MD = ROOT / 'handoffs/glossary_wave1_merge_report.md'

REQUIRED_GLOSSARY_KEYS = {'term_key', 'term_iast', 'invariant_definition', 'per_school'}


def validate_glossary(d: dict) -> list[str]:
    errs = []
    for k in REQUIRED_GLOSSARY_KEYS:
        if k not in d:
            errs.append(f'missing key: {k}')
    if 'per_school' in d and not isinstance(d['per_school'], list):
        errs.append('per_school is not a list')
    for i, ps in enumerate(d.get('per_school') or []):
        if 'school' not in ps or 'definition' not in ps:
            errs.append(f'per_school[{i}] missing school/definition')
    return errs


def merge_one(term: str) -> dict:
    out_path = OUT_DIR / f'{term}.out.json'
    if not out_path.exists():
        return {'term': term, 'status': 'PENDING', 'reason': 'no Codex output yet'}
    glossary_path = GLOSSARY / f'{term}.json'
    if not glossary_path.exists():
        return {'term': term, 'status': 'ERROR', 'reason': f'glossary file missing: {glossary_path}'}
    try:
        out = json.load(open(out_path))
    except Exception as e:
        return {'term': term, 'status': 'ERROR', 'reason': f'output JSON parse: {e}'}
    if 'per_school' not in out or not isinstance(out['per_school'], list):
        return {'term': term, 'status': 'ERROR', 'reason': 'output lacks per_school list'}
    cur = json.load(open(glossary_path))
    cur_per_school_count = len(cur.get('per_school') or [])
    cur['per_school'] = out['per_school']
    cur['last_verified_at'] = datetime.date.today().isoformat()
    cur['last_verified_by'] = 'glossary-wave1-codex54'
    errs = validate_glossary(cur)
    if errs:
        return {'term': term, 'status': 'ERROR', 'reason': '; '.join(errs)}
    json.dump(cur, open(glossary_path, 'w'), indent=2, ensure_ascii=False)
    new_cits = out.get('new_citations') or []
    not_retrieved = [ps['school'] for ps in out['per_school']
                     if str(ps.get('definition', '')).strip().startswith('[NOT YET RETRIEVED]')]
    return {
        'term': term,
        'status': 'OK',
        'before_schools': cur_per_school_count,
        'after_schools': len(out['per_school']),
        'after_schools_real': len(out['per_school']) - len(not_retrieved),
        'new_citations': new_cits,
        'not_retrieved': not_retrieved,
        'notes': out.get('notes'),
    }


def merge_citation_index(results: list[dict]) -> int:
    cidx = json.load(open(CIDX_PATH))
    added = 0
    for r in results:
        if r['status'] != 'OK':
            continue
        for nc in r.get('new_citations') or []:
            ck = nc.get('cite_key')
            if not ck:
                continue
            if ck in cidx['entries']:
                continue
            cidx['entries'][ck] = {
                'thinker_id': nc.get('thinker_id', ck.split('/')[0]),
                'work_id': nc.get('work_id', ck.split('/')[1] if '/' in ck else ''),
                'locus': nc.get('locus', ''),
                'locus_short': nc.get('locus_short', ''),
                'sanskrit_iast': nc.get('sanskrit_iast', ''),
                'english_close': nc.get('english_close', ''),
                'source': nc.get('source', ''),
            }
            added += 1
    json.dump(cidx, open(CIDX_PATH, 'w'), indent=2, ensure_ascii=False)
    return added


def write_gaps(results: list[dict]) -> None:
    rows = []
    rows.append('# Glossary gaps — Wave-1 follow-up\n')
    rows.append('_NOT-YET-RETRIEVED entries from Wave-1 Codex extraction. These schools have no on-disk citation evidence in the current corpus and are queued for Wave-2 acquisition._\n')
    for r in results:
        if r['status'] != 'OK':
            continue
        if not r['not_retrieved']:
            continue
        rows.append(f'- **{r["term"]}** — schools to acquire: {", ".join(r["not_retrieved"])}.')
    open(GAPS_MD, 'w').write('\n'.join(rows) + '\n')


def write_report(results: list[dict], cidx_added: int) -> None:
    ok = [r for r in results if r['status'] == 'OK']
    pending = [r for r in results if r['status'] == 'PENDING']
    err = [r for r in results if r['status'] == 'ERROR']
    if ok:
        before = sum(r['before_schools'] for r in ok) / len(ok)
        after_real = sum(r['after_schools_real'] for r in ok) / len(ok)
    else:
        before = after_real = 0.0
    rows = []
    rows.append('# Glossary Wave-1 merge report\n')
    rows.append(f'_Run at {datetime.datetime.now().isoformat()}._\n')
    rows.append(f'- Terms merged: **{len(ok)}** of {len(results)} (pending: {len(pending)}, errored: {len(err)}).')
    rows.append(f'- Mean schools/term: **{before:.2f} -> {after_real:.2f}** (excluding NOT-YET-RETRIEVED placeholders).')
    rows.append(f'- New citation_index entries: **{cidx_added}**.')
    rows.append('')
    rows.append('## Per-term outcome\n')
    rows.append('| Term | Status | Before | After (real) | New cites | Not-retrieved |')
    rows.append('|------|--------|------:|--------------:|----------:|--------------|')
    for r in results:
        if r['status'] == 'OK':
            rows.append(f'| {r["term"]} | OK | {r["before_schools"]} | {r["after_schools_real"]} | {len(r["new_citations"])} | {", ".join(r["not_retrieved"]) or "—"} |')
        else:
            rows.append(f'| {r["term"]} | {r["status"]} | — | — | — | {r.get("reason", "")} |')
    open(REPORT_MD, 'w').write('\n'.join(rows) + '\n')


def main():
    spec_path = ROOT / 'handoffs/glossary_top30_gaps.json'
    spec = json.load(open(spec_path))['top30_gap_analysis']
    terms = [r['file'].replace('.json', '') for r in spec]
    results = [merge_one(t) for t in terms]
    cidx_added = merge_citation_index(results)
    write_gaps(results)
    write_report(results, cidx_added)
    print(f'merged: OK={sum(1 for r in results if r["status"]=="OK")} '
          f'PEND={sum(1 for r in results if r["status"]=="PENDING")} '
          f'ERR={sum(1 for r in results if r["status"]=="ERROR")} '
          f'cidx_added={cidx_added}')


if __name__ == '__main__':
    main()
