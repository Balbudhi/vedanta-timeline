# DCS — Digital Corpus of Sanskrit (bulk dump)

**Source:** Oliver Hellwig, *The Digital Corpus of Sanskrit (DCS)*.
**Homepage:** http://www.sanskrit-linguistics.org/dcs/
**Bulk source:** https://github.com/OliverHellwig/sanskrit (default branch `master`, commit `04e0778d3dc971030229179e25eea043d06ff397` resolved 2026-05-19).
**License:** Creative Commons Attribution 3.0 Unported (CC BY 3.0) — verbatim
from `http://www.sanskrit-linguistics.org/dcs/index.php?contents=impressum`
(fetched 2026-05-19):

> Copyright © 2010-2021 by Oliver Hellwig. The Digital Corpus of Sanskrit by
> Oliver Hellwig is licensed under a Creative Commons Attribution 3.0
> Unported License.

The GitHub repository itself does not carry a top-level LICENSE file; the
license statement above governs the underlying dataset. Attribution is
required (Oliver Hellwig, *DCS*) in any downstream artefact.

## Fetch record

- Fetched: 2026-05-19 23:35 UTC by corpus-chat-lane2 on `rnn.ist.berkeley.edu`.
- Method: `git clone --depth 1 https://github.com/OliverHellwig/sanskrit.git dcs_repo`.
- Total on-disk size (after stripping `.git`): **720 MB** in
  `dcs_repo/` — `dcs/data/conllu/files/` is the morphology dump
  proper (300 MB, 14 780 CoNLL-U files), `corpus/GRETIL` (75 MB) and
  `corpus/VPC` (32 MB) are raw text alignments, `texts/` (4.1 MB) holds
  the Vedic Atharva/Sadviṃśa/Lāṭyāyana sources, `translations/` (3.8 MB)
  carries Olivelle/Griffith/etc., `papers/` (111 MB) carries PDFs of the
  published DCS papers (Hellwig et al.).

The cloned tree is **not** committed to git — it lives only on `/nas`. The
`.gitignore` at the worktree root excludes `dcs_repo/`. Consumers should
re-clone or rsync from this checkout; the canonical pointer is `dump.url`.

## Integrity

`sha256sum` of the cloned commit's `dcs/data/conllu` tarball is recorded
in `dcs_data_conllu.sha256` (computed at staging time).

## Schema (CoNLL-U dialect, DCS-augmented)

DCS dump is delivered as one CoNLL-U file per chapter, organised as
`dcs/data/conllu/files/<TextName>/<TextName>-NNNN-<short>, <chapter>-<chapterID>.conllu`.
There are 14 780 such files across the full DCS corpus. Each file
starts with a four-line header (`## text`, `## text_id`, `## chapter`,
`## chapter_id`) followed by CoNLL-U sentence blocks
(`# text`, `# sent_id`, `# sent_counter`, `# sent_subcounter`).

Each token line carries the standard CoNLL-U columns
(`ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC`); the DCS-specific
augmentation is in the `MISC` column as `|`-separated key=value pairs:

| MISC key                       | Meaning                                                                 |
|--------------------------------|-------------------------------------------------------------------------|
| `LemmaId`                      | Stable integer ID of the lemma in the DCS dictionary (cross-corpus).    |
| `OccId`                        | Stable integer ID of this token occurrence (cross-corpus unique).       |
| `Unsandhied`                   | Unsandhi'd surface form (post-sandhi-split).                            |
| `UnsandhiedReconstructed`      | `True` if the unsandhi form was reconstructed by Hellwig's parser.      |

Compound segmentation uses CoNLL-U range tokens (`2-5 virājitamadhyasadabjaṃ`)
followed by member-token lines whose `FEATS` carry `Case=Cpd` (compound
member marker), e.g.:

```
2-5     virājitamadhyasadabjaṃ  _       _       _       _       _       _       _       _
2       virājita                virāj   VERB    _       Case=Cpd|VerbForm=Part  ... LemmaId=163548|OccId=1845767|Unsandhied=virājita|UnsandhiedReconstructed=True
3       madhya                  madhya  NOUN    _       Case=Cpd                ... LemmaId=35810|OccId=1845768|...
4       sat                     as      VERB    _       Case=Cpd|Tense=Pres|VerbForm=Part ... LemmaId=156122|...
5       abjam                   abja    NOUN    _       Case=Nom|Gender=Neut|Number=Sing  ... LemmaId=21958|...
```

The `LemmaId` index is the join key for downstream tasks. The full lemma
inventory has ~88k unique IDs (per Hellwig 2018 EMNLP / 2020 LREC papers
shipped in `papers/`).

The corpus covers >600k morphologically tagged tokens spanning ~600
distinct works ranging from Vedic (Atharvaveda, Aitareya-Brāhmaṇa) to
classical and late śāstra. See `dcs/data/conllu/files/` for the full
text inventory.

## What the prakriya cross-validation should consume next

1. For each surface form proposed by the prakriya compiler, look up the
   `LemmaId` candidates from the DCS lemma table and compare the FEATS
   (Case/Number/Gender/Tense/VerbForm) against the prakriya derivation.
2. Use `OccId` to back-reference the exact source line in DCS, so any
   morphologically impossible OCR candidate gets a concrete witness
   counterexample.
3. The `Case=Cpd` marker is the immediate consumer for the compounding
   layer (`samāsa`) inside the prakriya pipeline.

## Files in this dump

- `dcs_repo/dcs/data/conllu/files/` — the gold morphology corpus.
- `dcs_repo/dcs/data/atharvaveda-shaunaka/translations/` — Whitney /
  Griffith / Bloomfield Atharvaveda translations.
- `dcs_repo/corpus/GRETIL/` and `dcs_repo/corpus/VPC/` — DCS's own
  re-aligned raw-text corpora.
- `dcs_repo/texts/` — Vedic primaries (Sadviṃśa-Brāhmaṇa,
  Lāṭyāyana-Śrauta-Sūtra) with annotation.
- `dcs_repo/translations/` — modern translations DCS aligns against
  (Olivelle, Griffith, etc.).
- `dcs_repo/papers/` — published DCS papers (PDFs).

## Pointer

The exact upstream commit is captured in `dump.url` next to this README.
To restore the dump on a fresh machine: `git clone https://github.com/OliverHellwig/sanskrit.git dcs_repo && cd dcs_repo && git checkout 04e0778d3dc971030229179e25eea043d06ff397`.
