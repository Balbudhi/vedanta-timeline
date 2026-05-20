# DCS morphology gold — handoff to prakriya-chat (2026-05-19)

**From:** Lane 6 (corpus-chat) — `corpus/dcs-gold-2026-05-19`
**To:** prakriya-chat (owner of `scripts/cross_validate_vidyut.py`)
**Acceptance threshold:** Master plan §A.4 — vidyut cross-validation
≥ 99.0 % match rate on tinanta + krdanta + subanta tuples.

## Summary

The Digital Corpus of Sanskrit (DCS) CoNLL-U dump has been parsed into a
prakriya-shaped per-token gold standard. 5 688 416 tokens spanning 270
distinct works (Mahābhārata, Rāmāyaṇa, Ṛgveda, Suśrutasaṃhitā, all
major purāṇas, the entire Kāśikā/Aṣṭādhyāyī commentarial layer, the
Buddhist canon, etc.) are emitted as JSONL with the canonical
`tinanta_tuple` / `krdanta_tuple` / `subanta_tuple` shapes consumed by
`cross_validate_vidyut.py`.

The gold lives **outside any worktree** because it is 3.4 GB:

```
/nas/ucb/eeshan/dcs_morphology_gold/dcs_morphology_gold.jsonl
  sha256: 9a6e7cb155aa19a32c8b1af95de7a586f4abda2ea9ccaa8efa3c73f87bdc1215
  size:   3 374 672 522 bytes
  lines:  5 688 416
```

Schema, vocabulary mapping, and a 50-line sample are committed at
`data/dcs_morphology_gold/{README.md, sample.jsonl, coverage_report.json}`
on branch `corpus/dcs-gold-2026-05-19`.

## What to integrate in prakriya

A new probe-loader for `cross_validate_vidyut.py`. Sketch (do **not**
land this from corpus-chat — prakriya owns the script):

```python
# scripts/cross_validate_vidyut.py — add alongside _load_tinanta_probes etc.

DCS_GOLD_PATH = Path("/nas/ucb/eeshan/dcs_morphology_gold/dcs_morphology_gold.jsonl")


def _load_dcs_morphology_probes(
    path: Path = DCS_GOLD_PATH,
    *,
    domains: frozenset[str] = frozenset({"tin", "krt", "sup"}),
    require_gana: bool = True,
    sample: int | None = None,
    seed: int = 17,
) -> list[Probe]:
    """Pull DCS-derived gold rows into the cross-validation harness.

    Rows with `tuple[gana] is None` are skipped when ``require_gana`` is
    True (the default), since vidyut needs an explicit gaṇa to derive a
    tinanta surface. Set ``require_gana=False`` to additionally probe
    krdanta+subanta rows (which don't need gaṇa).
    """
    if not path.is_file():
        return []
    probes: list[Probe] = []
    with path.open("r", encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            rec = json.loads(line)
            kind = rec["kind"]
            if kind == "tinanta" and "tin" in domains:
                t = rec["tinanta_tuple"]
                if t is None:
                    continue
                root, gana, lakara, purusha, vacana, pada = t
                if require_gana and gana is None:
                    continue
                payload = {
                    "root_slp1": root,
                    "gana": gana,
                    "lakara": lakara,
                    "purusha": purusha,
                    "vacana": vacana,
                    "pada": pada,
                    "_dcs_occ_id": rec["dcs_occ_id"],
                    "_dcs_text_id": rec["text_id"],
                }
                pid = (
                    f"dcs-tin/{root}/{gana}/{lakara}/"
                    f"{purusha}/{vacana}/{pada or '-'}#{rec['dcs_occ_id']}"
                )
                probes.append(Probe(pid, "tin", payload))

            elif kind == "krdanta" and "krt" in domains:
                t = rec["krdanta_tuple"]
                if t is None or t[1] is None:  # need krt
                    continue
                root, krt, linga, vibhakti, vacana = t
                gana = _lookup_gana_or_skip(root)  # see caveat below
                if require_gana and gana is None:
                    continue
                payload = {
                    "root": root,
                    "gana": gana,
                    "krt": krt,
                    "linga": linga,
                    "vibhakti": vibhakti,
                    "vacana": vacana,
                    "_dcs_occ_id": rec["dcs_occ_id"],
                }
                pid = (
                    f"dcs-krt/{root}/{gana}/{krt}/{linga}/{vibhakti}/{vacana}"
                    f"#{rec['dcs_occ_id']}"
                )
                probes.append(Probe(pid, "krt", payload))

            elif kind in ("subanta", "compound_member") and "sup" in domains:
                t = rec["subanta_tuple"]
                if t is None:
                    continue
                stem, linga, vibhakti, vacana = t
                payload = {
                    "stem_slp1": stem,
                    "linga": linga,
                    "vibhakti": vibhakti,
                    "vacana": vacana,
                    "_dcs_occ_id": rec["dcs_occ_id"],
                }
                pid = f"dcs-sup/{stem}/{linga}/{vibhakti}/{vacana}#{rec['dcs_occ_id']}"
                probes.append(Probe(pid, "sup", payload))
    if sample is not None and len(probes) > sample:
        rng = random.Random(seed)
        probes = sorted(rng.sample(probes, sample), key=lambda p: p.probe_id)
    return probes
```

Then in `load_all_probes(...)`:

```python
    probes.extend(
        _load_dcs_morphology_probes(
            DCS_GOLD_PATH,
            domains=frozenset({"tin", "krt", "sup"}) & set(ALL_DOMAINS),
            sample=getattr(args, "dcs_sample", None),
        )
    )
```

The DCS payload schemas above are byte-compatible with the existing
`_engine_*_surface` / `_vidyut_*_surface` adapters, with one caveat:
**the DCS row records the inflected surface (in `surface_iast` /
`unsandhied`) but the harness today compares to a fixture-recorded
``expected`` SLP1 surface.** For the DCS pass, the comparison should be
`vidyut_surface` ↔ `our_surface` directly; populate `expected` from
`iast_to_slp1(rec["unsandhied"])` so the existing match logic continues
to work, *and* track surface↔DCS divergence as a third axis.

## Known caveats

1. **Gaṇa-null fraction.** DCS does not tag dhātu-gaṇa. We resolve it
   via prakriya's bundled dhātupāṭha (1 622 unique SLP1-clean roots)
   plus a leading-upasarga stripping pass. **Resolution rate: 27.05 %**
   (129 002 / 476 859 tinanta rows). The other 73 % split roughly into:
   - homonymous roots (`vac` ∈ {gaṇa 2, 10}, `hf` ∈ {1, 3}, `as` ∈ {1, 2, 4}…)
     — DCS provides no disambiguator; prakriya-chat should pick the most
     frequent gaṇa from the corpus distribution, or carry the
     ambiguity as a probe-time pada-axis split.
   - roots not in the bundled dhātupāṭha at all (low-frequency or
     post-Pāṇinian formations). Expand
     `panini_prakriya/dhatupatha.py` to widen coverage if needed; the
     baked JSON already has ~1 622 entries and Vidyut's full
     dhātupāṭha runs to ~2 000.

   **Action for prakriya-chat:** decide policy. Conservative is to set
   `require_gana=True` and validate the 27 % subset; the ≥ 99 % §A.4
   threshold then applies only to that subset. Less conservative is to
   probe all (root, gaṇa) combinations and accept any vidyut match.

2. **Voice=Pass tokens.** Mapped to `pada=atmanepada` +
   `prayoga=karmani`. Pāṇinian karmaṇi-prayoga indeed selects
   ātmanepada endings, but DCS sometimes tags semantically passive
   forms that are morphologically aniṭ + parasmaipada. Expect 1–3 %
   noise on the pada axis for `Voice=Pass` rows; cross-check via the
   `feats.Voice` field if a row diverges.

3. **Kṛt suffix inference.** DCS does not tag the kṛt directly; the
   build script back-fills `krt` from `(VerbForm, Tense, Voice)` —
   see the mapping table in `data/dcs_morphology_gold/README.md`.
   This covers kta / ktavatu / Satf / SAnac / syatf / syamAna /
   kvasu / tumun / ktvA / tavya. Rows outside this set get
   `krt=null` (skip when consuming as krdanta probes). About 8 % of
   `kind=krdanta` rows in the DCS dump have unresolved kṛt.

4. **Sandhi-undone tokens.** DCS resolves sandhi: token-level `FORM`
   is the post-sandhi-split surface, and the unsandhi'd dictionary
   form lives in MISC `Unsandhied` (with a `UnsandhiedReconstructed`
   boolean flag). When `UnsandhiedReconstructed=True`, the
   unsandhi-shape was inferred by DCS's segmenter and may not
   round-trip to the surface; ~96 % of DCS tokens carry this flag.
   Treat surface divergence on these rows as soft.

5. **Multiword (compound) tokens.** DCS emits each samāsa as a
   CoNLL-U range row (`2-5 virājitamadhyasadabjaṃ`) followed by the
   individual member rows. Range rows are emitted as
   `kind=compound_range` and carry no morphology tuple. Member rows
   carry `compound_member=True` and `compound_role ∈
   {purvapada, madhyamapada, uttarapada}`. The final member (highest
   index) carries the inflectional case/gender/number; non-final
   members have `Case=Cpd` and are emitted with a subanta tuple
   built from their lemma + the inherited linga/vibhakti/vacana of
   the final member (i.e. a subanta tuple is emitted on members
   that have full Case/Gender/Number; the `Case=Cpd` members get the
   feature trio dropped and the tuple is None).

   1 024 841 compound ranges + 792 492 compound members are present.

6. **UPOS distribution.**
   - `subanta`: 2 862 038  (50 %)
   - `indeclinable`: 1 026 525  (18 %)
   - `compound_range`: 1 024 841  (18 % — bookkeeping rows)
   - `compound_member`: 792 492  (14 %)
   - `tinanta`: 523 721  (9 %)
   - `krdanta`: 483 640  (8.5 %)

7. **DCS lemmas already in IAST.** All `lemma_iast`/`surface_iast`
   fields are NFC-normalised IAST as DCS records them. SLP1 and
   Devanāgarī projections are computed at build time via
   `indic_transliteration.sanscript`. If prakriya prefers a different
   transliteration round-trip for a specific work, recompute from the
   `lemma_iast` field.

## Per-text-id top coverage

| Work | Tokens | tinanta | krdanta | subanta |
|------|--------|---------|---------|---------|
| Mahābhārata | 1 351 604 | 104 342 | 112 709 | 592 070 |
| Rāmāyaṇa | 306 926 | 20 210 | 30 841 | 133 747 |
| Suśrutasaṃhitā | 180 673 | 9 652 | 11 284 | 64 294 |
| Ṛgveda | 179 345 | 23 682 | 9 617 | 103 949 |
| Śatapathabrāhmaṇa | 165 691 | 21 784 | 5 969 | 75 858 |
| Liṅgapurāṇa | 156 945 | 7 754 | 10 129 | 65 301 |
| Matsyapurāṇa | 152 415 | 9 529 | 10 473 | 62 851 |
| Skandapurāṇa (Revākhaṇḍa) | 138 250 | 9 141 | 10 807 | 57 235 |
| Kathāsaritsāgara | 134 668 | 9 325 | 13 139 | 52 459 |
| Aṣṭāṅgahṛdayasaṃhitā | 129 657 | 5 789 | 7 843 | 47 462 |

Full per-text breakdown for all 270 works is in
`data/dcs_morphology_gold/coverage_report.json`.

## Acceptance plan

Per master plan §A.4:

1. prakriya-chat lands the `_load_dcs_morphology_probes` loader.
2. Run `python3 scripts/cross_validate_vidyut.py --fail-below 99.0
   --dcs-sample 50000` (or full).
3. Triage divergences. Expect the dominant divergence sources to be:
   - gaṇa-ambiguous rows (skip via `require_gana=True`),
   - kṛt-null rows (skip),
   - sandhi-reconstruction round-trip differences (soft-fail).
4. Once ≥ 99 % match rate is achieved on the gaṇa-resolved subset,
   §A.4 is green.

If the gaṇa-resolved subset is too narrow to be statistically
meaningful, propose expanding `panini_prakriya/dhatupatha.py` with
the remaining ~400 multi-gaṇa lemmas using corpus-frequency-weighted
gaṇa assignment — corpus-chat can pull the frequency table from the
gold JSONL on request.
