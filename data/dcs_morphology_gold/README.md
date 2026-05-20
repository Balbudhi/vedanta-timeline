# DCS morphology gold for prakriya cross-validation

This directory holds the wire-up artifacts for the DCS → prakriya morphology
gold standard. The large JSONL itself lives **outside any worktree**, on
`/nas`, because it is ~3.4 GB.

## Locations

| Artifact | Path |
|----------|------|
| Primary gold JSONL | `/nas/ucb/eeshan/dcs_morphology_gold/dcs_morphology_gold.jsonl` |
| Build script | `scripts/build_dcs_morphology_gold.py` (this worktree) |
| Schema sample (first 50 lines) | `data/dcs_morphology_gold/sample.jsonl` |
| Coverage report (per-text-id, per-kind counts) | `data/dcs_morphology_gold/coverage_report.json` |
| Handoff brief for prakriya chat | `docs/dcs_morphology_handoff_2026-05-19.md` |

## Provenance

- **Input:** DCS CoNLL-U dump under
  `/nas/ucb/eeshan/corpus_worktrees/external-ingest/data/external/dcs/dump/dcs_repo/dcs/data/conllu/files/`
  (270 work-name directories, 15 900 chapter `.conllu` files, schema in
  the sibling worktree's `data/external/dcs/SCHEMA.md`).
- **Gaṇa lookup source:** prakriya's bundled dhātupāṭha:
  `/nas/ucb/eeshan/prakriya/src/prakriya/panini_prakriya/dhatupatha.py`
  (the `DhatuEntry(...)` literals) + the Vidyut-derived superset at
  `panini_prakriya/data/dhatu_set_flags_baked.json`. Combined yields
  ~1 622 unique SLP1-clean roots with gaṇa annotation.
- **IAST↔SLP1↔Devanāgarī:** `indic_transliteration.sanscript`, invoked via
  the prakriya `.venv` at runtime (no install into our worktree).
- **prakriya repo is read-only.** This worktree never writes into
  `/nas/ucb/eeshan/prakriya/`.

## Output schema (per-line JSON)

```json
{
  "dcs_occ_id": "2588394",
  "dcs_lemma_id": "44133",
  "lemma_iast": "namas",
  "lemma_slp1": "namas",
  "surface_devanagari": "नमो",
  "surface_iast": "namo",
  "unsandhied": "namaḥ",
  "upos": "NOUN",
  "feats": {"Case": "Acc", "Gender": "Neut", "Number": "Sing"},
  "kind": "subanta",                         // tinanta | krdanta | subanta |
                                             //   indeclinable | compound_member | other
  "tinanta_tuple": null,                     // see shape below
  "subanta_tuple": ["namas", "napumsaka", 2, "ekavacana"],
  "krdanta_tuple": null,
  "text_id": "378",
  "text_name": "Abhidharmakośa",
  "chapter_id": "7024",
  "verse_id": "479271",                      // DCS sent_id
  "sent_counter": "1",
  "sent_subcounter": "1",
  "compound_member": false,
  "compound_role": null,                     // purvapada | uttarapada | madhyamapada | null
  "compound_form": null                      // surface compound when compound_member=true
}
```

### Tuple shapes

These match the row shapes consumed by
`/nas/ucb/eeshan/prakriya/scripts/cross_validate_vidyut.py` (see
`panini_prakriya/data/cross_validate_tinanta_fixture.json` and
`krdanta_vidyut_gold.json`):

```
tinanta_tuple = [root_slp1, gana_or_null, lakara, purusha, vacana, pada]
krdanta_tuple = [root_slp1, krt_or_null, linga, vibhakti, vacana]
subanta_tuple = [stem_slp1, linga, vibhakti, vacana]
```

### UD → prakriya vocabulary mapping (canonical)

`Tense` / `Mood` → **lakāra** (`panini_prakriya/tin_pratyaya.py` keys):

| UD                    | prakriya  | gloss      |
|-----------------------|-----------|------------|
| `Tense=Pres`          | `law`     | laṭ        |
| `Tense=Imp`           | `laN`     | laṅ        |
| `Tense=Aor`           | `luN`     | luṅ        |
| `Tense=Perf`          | `liw`     | liṭ        |
| `Tense=Fut`           | `lfw`     | lṛṭ        |
| `Tense=Pqp`           | `lfN`     | lṛṅ (approx) |
| `Mood=Imp`            | `low`     | loṭ        |
| `Mood=Opt`/`Sub`/`Ben`| `liN`     | liṅ        |
| `Mood=Cnd`            | `lfN`     | lṛṅ        |
| `Mood=Jus`            | `luN`     | luṅ (Vedic injunctive → best fit) |

`Voice` → **pada / prayoga**:

| UD          | pada           | prayoga    |
|-------------|----------------|------------|
| `Voice=Act` | `parasmaipada` | `kartari`  |
| `Voice=Mid` | `atmanepada`   | `kartari`  |
| `Voice=Pass`| `atmanepada`   | `karmani`  |

`Person` → puruṣa: `1→uttama`, `2→madhyama`, `3→prathama`.
`Number` → vacana: `Sing→ekavacana`, `Dual→dvivacana`, `Plur→bahuvacana`.
`Case` → vibhakti integer: Nom→1 … Loc→7, Voc→8, Cpd→(omit; mark `compound_member`).
`Gender` → liṅga: `Masc→pum`, `Fem→stri`, `Neut→napumsaka`.

### Kṛt inference (heuristic; DCS does not tag kṛt directly)

The build script back-fills `krt` from `(VerbForm, Tense, Voice)`:

| (VerbForm, Tense, Voice) | kṛt        |
|--------------------------|------------|
| `Part, Past, Pass`       | `kta`      |
| `Part, Past, Act`        | `ktavatu`  |
| `Part, Pres, Act`        | `Satf`     |
| `Part, Pres, Mid`        | `SAnac`    |
| `Part, Fut, Act`         | `syatf`    |
| `Part, Fut, Mid`         | `syamAna`  |
| `Part, Perf, *`          | `kvasu`    |
| `Inf, *, *`              | `tumun`    |
| `Conv, *, *`             | `ktvA`     |
| `Gdv, *, *`              | `tavya`    |
| other                    | `null`     |

Rows with `krt=null` in the krdanta tuple are flagged for the prakriya
chat to refine.

## Smoke test

Read the first 50 lines from `sample.jsonl` — these are the leading
tokens of the build (deterministic file-iteration order), suitable for
diff-review.

The full JSONL has the following hash and size (recorded at build time
in `coverage_report.json` and reproduced here):

- **sha256:** `9a6e7cb155aa19a32c8b1af95de7a586f4abda2ea9ccaa8efa3c73f87bdc1215`
- **size:** 3 374 672 522 bytes (3.4 GB)
- **lines:** 5 688 416

## Re-run

```
cd /nas/ucb/eeshan/corpus_worktrees/dcs-gold
TMPDIR=/nas/ucb/eeshan/tmp \
  /nas/ucb/eeshan/prakriya/.venv/bin/python3 \
  scripts/build_dcs_morphology_gold.py
```

The script reads the DCS CoNLL-U tree once, line-buffers the JSONL,
recomputes the sha256 + coverage report, and refreshes `sample.jsonl`.
Wall clock at last run: **338 seconds** on rnn.ist.berkeley.edu.

## How to consume from prakriya

See `docs/dcs_morphology_handoff_2026-05-19.md` for the integration
sketch and known caveats.
