# Glossary Wave-1 — per-term primary-source extraction (Codex 5.4)

You are extracting primary-source-grounded by-school content for a single Sanskrit philosophical term in the project's glossary at `site/data/glossary/<TERM>.json`. The current entry is incomplete: only **<CUR_N>** schools have prose, none of the prose carries citations, and several substantive school-positions are missing.

Your job is to produce an updated `per_school[]` array (and only that) for this term.

## Term

- File: `site/data/glossary/<TERM>.json`
- Term IAST: `<TERM_IAST>`
- Aliases (for grep): `<ALIASES>`
- Currently present schools: `<CURRENT_SCHOOLS>`
- Schools with citation-evidence already in `site/data/citation_index.json`: `<EVIDENCE_SCHOOLS>`
- Canonical schools to attempt (where the school has substantive treatment of this term): Advaita, Viśiṣṭādvaita, Tattva-vāda, Bhedābheda, Acintya-Bhedābheda, Dvaitādvaita, Śuddhādvaita, Sāṅkhya, Yoga, Nyāya-Vaiśeṣika, Pūrva-Mīmāṃsā, Mādhyamaka, Yogācāra, Pratyabhijñā / Trika. (Add Jainism, Pāṇinian-Vaiyākaraṇa where the term is technical there.)

## What to do

1. Read the current `<TERM>.json`.
2. Read `site/data/citation_index.json` and grep its entries for the aliases listed above to find the existing citation passages. Use these first.
3. Where citation_index lacks evidence for a school that does have substantive treatment, search:
   - `site/data/thinkers/*.json` (each `key_passages[]` carries IAST + locus + on-disk pointer);
   - `site/data/full_translations/*.md` (work-level translations);
   - `materials/primary_texts/sanskrit/` directly for Sanskrit primaries.
4. For each school with substantive treatment AND on-disk citation evidence, write a per-school object:
   ```json
   {
     "school": "<canonical school label>",
     "definition": "<2–5 sentences of project-register prose, engaging the school on its own ground; no comparator-framing; Pāṇinian-rich Sanskrit terminology where natural>",
     "primary_loci": ["<locus 1>", "<locus 2>", ...],
     "citations": [
       {"cite": "cite://<thinker>/<work>/<locus_key>", "locus_short": "<short locus>"},
       ...
     ]
   }
   ```
5. For each canonical school where the on-disk corpus does not yield evidence, emit:
   ```json
   {"school": "<school>", "definition": "[NOT YET RETRIEVED]", "primary_loci": [], "citations": []}
   ```
6. Where you cite a passage that is referenced in a thinker JSON's `key_passages[]` but does NOT yet appear as an entry in `citation_index.json`, list it under the term's `new_citations[]` array (separate from `per_school`) with full record:
   ```json
   {
     "cite_key": "<thinker>/<work>/<locus_key>",
     "thinker_id": "<thinker>",
     "work_id": "<work>",
     "locus": "<long locus>",
     "locus_short": "<short>",
     "sanskrit_iast": "<verse IAST>",
     "english_close": "<close translation>",
     "source": "thinker_jsons/<thinker>.json#key_passages[<idx>]"
   }
   ```
   The merge step will splice these into `citation_index.json`.
7. Preserve the existing top-level fields (`term_key`, `term_iast`, `term_devanagari`, `literal`, `aliases`, `invariant_definition`, `see_also`, `translator_note`).

## Output format

Write a single JSON file to `handoffs/wave1_glossary_outputs/<TERM>.out.json` with this structure:

```json
{
  "term_key": "<TERM>",
  "per_school": [...],
  "new_citations": [...],
  "notes": "<optional 1–3 sentence note re sources used or gaps>"
}
```

## Discipline (HARD)

- **Never fabricate.** If a school has no on-disk evidence, write `[NOT YET RETRIEVED]`. Do not invent a Sanskrit verse or attribute a position the school did not hold.
- **Use Tattva-vāda** for Madhva's school (not "Dvaita"). Other school labels: use the canonical forms above.
- **Cite-format**: every prose claim that is school-specific should carry at least one `cite://...` reference at the end of its sentence, e.g. "*ātman* is here a real, atomic, dependent knower [[VTV §30](cite://madhva/visnu-tattva-vinirnaya/30)]."
- **Russell–Chakrabarti register**: graduate-level professional, no editorializing, no AI-tells, no comparator-framing. Engage each school on its own ground.
- **Pāṇinian-rich Sanskrit**: where a śāstric term explains the doctrinal move (`sāmānādhikaraṇya`, `viśeṣaṇa-viśeṣya`, `aprṭhak-siddhi`, etc.), use it.
- **Do NOT modify** any file other than your output JSON. (No edits to `drafts/`, no edits to glossary or citation_index — the merge step does that.)
- Write to `handoffs/wave1_glossary_outputs/<TERM>.out.json` only.

## Existing-citation candidates (use these first)

<CITATION_CANDIDATES>

Begin extraction now.
