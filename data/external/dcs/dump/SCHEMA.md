# DCS dump — schema cheatsheet for the prakriya morphology join

Format: CoNLL-U with DCS-specific MISC keys.

## Per-file headers

```
## text: <work title in IAST with diacritics>
## text_id: <integer, joins to the DCS work table>
## chapter: <chapter label, free-text>
## chapter_id: <integer, joins to the DCS chapter table>
```

## Per-sentence headers

```
# text = <pre-sandhi raw sentence in IAST>
# sent_id = <integer, globally unique across DCS>
# sent_counter = <integer, sentence index inside the work>
# sent_subcounter = <integer, post-segmentation sub-index>
```

## Per-token columns (standard CoNLL-U)

| Col | Name    | DCS use                                                             |
|-----|---------|---------------------------------------------------------------------|
| 1   | ID      | `N` or `N-M` (CoNLL-U multiword token for compounds).               |
| 2   | FORM    | Surface form (post-sandhi-split, sandhi-resolved).                  |
| 3   | LEMMA   | Lemma form (IAST).                                                  |
| 4   | UPOS    | Universal POS (NOUN, VERB, ADJ, ADV, PRON, …).                      |
| 5   | XPOS    | Empty in DCS (`_`).                                                 |
| 6   | FEATS   | UD morphological features (`Case`, `Number`, `Gender`, `Tense`, …). |
| 7   | HEAD    | Empty in DCS (`_`); DCS is not currently dependency-parsed.         |
| 8   | DEPREL  | Empty in DCS (`_`).                                                 |
| 9   | DEPS    | Empty in DCS (`_`).                                                 |
| 10  | MISC    | DCS-specific keys (see below).                                      |

## MISC keys (DCS extension)

| Key                       | Meaning                                                             |
|---------------------------|---------------------------------------------------------------------|
| `LemmaId`                 | Stable integer ID of the lemma in DCS's lemma dictionary.           |
| `OccId`                   | Stable integer ID of this token occurrence (corpus-wide).           |
| `Unsandhied`              | Unsandhi'd surface form (segmentation output).                      |
| `UnsandhiedReconstructed` | `True` if the unsandhi form was reconstructed (vs. directly read).  |

## Compound encoding (samāsa)

A compound surface form is emitted as a CoNLL-U *multiword token*: the
range line (`2-5 virājitamadhyasadabjaṃ`) is the original
surface compound; lines `2`, `3`, `4`, `5` are the morphemic members.
Compound members carry `Case=Cpd` in FEATS, and the final member carries
the inflectional case/gender/number.

## Sandhi encoding

DCS resolves sandhi at the segmentation layer: token-level `FORM` is the
post-sandhi-split surface form, and `Unsandhied` (in MISC) is the
unsandhi'd dictionary-shape token. The original (sandhi-applied)
sentence text lives in the `# text` header.

## File inventory shape

`dcs/data/conllu/files/<WorkName>/<WorkName>-NNNN-<chapter_short>, <chapter>-<chapter_id>.conllu`

- ~600 distinct works ⇒ ~600 subdirectories.
- 14 780 chapter files total.
- 300 MB packed; ~600 k tagged tokens.

## Join recipes for prakriya

- **Lemma identity:** `prakriya.derived_lemma` ↦ DCS `LEMMA` (IAST).
  Use NFC-normalised IAST on both sides. Multiple matches resolved via
  `LemmaId`.
- **Morphology vector:** parse DCS `FEATS` into the UD feature dict;
  compare the matching subset to the prakriya derivation's feature dict.
  Mismatched features = OCR or sandhi error in the surface input.
- **Compound member identification:** every CoNLL-U multiword token in
  DCS is a samāsa pattern; the member chain is a labelled training pair
  for the prakriya compounder.
- **Occurrence back-reference:** the integer `OccId` is the corpus-wide
  primary key. Embed it in any error report so the witness sentence can
  be retrieved verbatim from DCS.
