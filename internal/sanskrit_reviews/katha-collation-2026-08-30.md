# Kaṭha quotation collation — source decisions and open repairs

This is a source audit, not publication approval. No public reading is changed
by this report. The printed scan was consulted visually; existing normalized
JSON and automatic OCR were not treated as substitutes for it.

## Closed named-reference population

The current `chinmayananda.json` contains explicit Kaṭha references in names
8, 11, 107, 109, 152, 169, 387, 388, 403, 419, 421, 452, 545, 555, 619,
633, 760, 776, 778, 824, 836, and 895: 22 names. A broad `kath` search also
matches `prakathanam` in name 82; that is not a Kaṭha reference.

Sixteen of those names contain Sanskrit presented as a Kaṭha quotation,
including two fragments under 388: 17 quotation occurrences. The other six
(11, 109, 169, 545, 760, 824) contain English quotation, paraphrase, or a work
reference, not an additional printed Sanskrit Kaṭha passage. This is the
explicitly named population, not a claim that all unattributed allusions in
the book have been identified.

## Evidence

- Chinmayananda, *Thousand Ways to the Transcendental*, CCMT, February 2011
  reprint, ISBN 9788175972452; local scan
  `/Users/eeshan/Downloads/Vishnu Sahasranama.pdf`, SHA-256
  `99084a346d68e5673309e4aca81b9787fe618d8414191f8ec697df4bf2534219`.
  Permission basis is retained in `chinmayananda.json.work`. Page numbers in
  the table are PDF / printed. Only relevant short readings are quoted here.
- Local GRETIL text with Śaṅkara's bhāṣya:
  `data/sources/sanskrit/vedic/katha_upanisad_sankara_bhasya_gretil.txt`, SHA-256
  `3054f718c80eca0f3a1df050e0564e42ef6c04af0b5f891c82b51639721cadcc`.
  Its header names *Ten Principal Upaniṣads with Śaṅkarabhāṣya*, Motilal
  Banarsidass 1964 / reprint 2007; electronic entry Ivan Andrijanić,
  version 2020-07-31. The electronic text, not that physical edition, was
  consulted. CC BY-NC-SA 4.0 terms apply to that transport.
- Sringeri Advaita Sharada:
  <https://advaitasharada.sringeri.net/read/kathaka-bhashya/1/> and
  <https://advaitasharada.sringeri.net/read/kathaka-bhashya/2/>, consulted
  2026-08-30. Chapter/section/locus must follow the text, not an assumed
  equivalence between two-part and three-part verse numbers.

## Sanskrit occurrences

| Name | Scan page | Observed issue or result | Decision for integration |
| --- | --- | --- | --- |
| 8 | 23 / 19 | Print has `भूतान्तरात्मा`; stored transcription has `भृतान्तरात्मा`. Printed opening `एको वशी` agrees with 2.2.12; its later `रूपं रूपं प्रतिरूपो बहिश्च` agrees with 2.2.9–10. | Correct the transcription's vowel from the scan. Preserve the printed composite quotation; do not represent it as a verbatim single verse or silently replace its opening. Record the two textual parallels. |
| 107 | 48 / 44 | Print stops after `सुखं` with an ellipsis. Stored text adds `शाश्वतं नेतरेषाम्` and leaves a stray `रूपं` before the following English paragraph. The expansion is explicitly implemented in `ENTRY_REPAIRS[107]`. | Restore the printed quotation boundary. Fix the duplicated/dislocated `रूपं` using the page's continuous quote. A full 2.2.12 may be available separately as source context, never silently attributed to this printed excerpt. |
| 152 | 60 / 56 | `वामन-` ends a printed line; `मासीनं` starts the next. Passage corresponds to second half of 2.2.3, numbered 5.3 in print. | Remove only the line-wrap hyphen; retain the fragment, author's English, and print reference. Word division is `vāmanam āsīnam`, not two unrelated hyphenated words. |
| 387 | 118 / 114 | `यथाकर्म यथाश्रुतम्` is the end of 2.2.7 (5.7); print uses II-V-7. | Retain as a fragment. Record normalized locator alongside the printed numbering. The next note `कर्मफलदाता…` is a separate explanatory formula, not more Kaṭha text. |
| 388a | 118 / 114 | `नित्योऽनित्यानाम्` agrees with the local witness's beginning of 2.2.13. | Retain the negative compound reading in this edition; do not erase its avagraha or replace it from a different tradition's `nityo nityānām`. |
| 388b | 118 / 114 | `चेतनश्चेतनानाम्` follows in 2.2.13 but has a separate printed call. | Keep the two note-to-claim relationships even though the fragments share a verse. |
| 403 | 122 / 118 | `सुविज्ञेयम्` really is printed. Sringeri's mantra 1.1.21 agrees; local GRETIL's mantra has `sujñeyam` and its bhāṣya `suvijñeyam`. | Preserve the attested printed reading; no typo classification is justified. Detailed evidence and limitations are in `verified-pilot/witnesses/katha-1-1-21-collation.md`. Analyze the `vi-` too. |
| 419 | 125 / 121 | `परमे व्योम्नि प्रतिष्ठितः` and its attribution to Kaṭha are genuinely printed. No exact matching Kaṭha verse was found in the consulted GRETIL or Sringeri witnesses. | Retain author's wording and attribution as printed, but withhold a verified Kaṭha locator. Related expressions in other Upaniṣads do not establish this exact quotation's source. This remains an attribution-resolution item, not an OCR fix. |
| 421 | 125 / 121 | The printed Sanskrit agrees lexically with 2.3.3 (6.3). | Retain; distinguish the book's II-VI-3 numbering from 2.3.3. Preserve its separate relationship to the author's English. |
| 452 | 131 / 127 | The printed citation agrees with the verse portion of 2.2.1 (5.1), without the following refrain `etad vai tat`. | Keep this quotation boundary; do not silently append the refrain. |
| 555 | 153 / 149 | Printed Kaṭha fragment agrees with opening 2.3.1 (6.1). The footnote also prints Roman text and an English translation; both the Kaṭha and adjacent Gītā English translations are absent from `chinmayananda.json`. | Restore missing authored English from the scan before generating site English. Roman duplicate surfaces may be consolidated for display only with explicit source accounting. Preserve the Kaṭha fragment boundary. |
| 619 | 164 / 160 | Print has `भान्तमनुभाति`; transcription has `भान्तमनभाति`. Printed Roman independently includes `anubhaati`. Passage is the latter half of 2.2.15 (5.15). | Correct the transcription from the scan. Do not classify the dropped `u` as an attested verse variant. Keep the author's English, already present. |
| 633 | 168 / 164 | The printed Sanskrit and Roman line correspond to 2.2.15. | Retain the complete verse and existing authored English; allow source-context reuse with 619 without merging their distinct occurrences. |
| 776 | 200 / 196 | The scan has `सूर्यः`; transcription has `सुर्यः`. The printed Roman says `sooryah`. Text corresponds to 2.3.3, also quoted under 421. | Correct the vowel from the scan. This is transcription error, not grounds for inventing a variant. Preserve independent call and author's translation. |
| 778 | 201 / 197 | Printed fragment `दुर्गं पथस्तत्कवयो वदन्ति` agrees with the end of 1.3.14. | Retain a fragment; do not add earlier verse material. |
| 836 | 217 / 213 | Print and printed Roman both have `nihitaṃ/nihitam`; GRETIL and Sringeri 1.2.20 have `nihito`, with the bhāṣya explaining nominative `nihitaḥ` of `ātmā`. | Not an OCR error. Treat as a likely erroneous printed form, not an established variant. Proposed corrected reading `nihito` needs a separate textual note, preserving `nihitam` as printed; do not silently rewrite the author's layer. |
| 895 | 228 / 224 | Several transcription spellings differ from legible print (`वहभियों`, `श्रुष्वन्तो`, `बहुवो`, `कुशलानशिष्टः`). The printed Roman corroborates the normal forms of 1.2.7. | Proofread the whole quoted unit against the page and retained source, not independent regex replacements. Preserve the quotation's complete scope and its distinction from the preceding Gītā quote. |

## Additional source-preservation failures exposed by this check

The saved string is not a lossless source witness merely because a builder
copies it unchanged. Name 107 demonstrates an addition; name 555 demonstrates
an omission. The full source pass must therefore reconcile every page's body,
notes, Roman alternatives, and authored translations with a source-coverage
map. Comparing the stored commentary with a second copy of itself cannot
satisfy that gate.

No rule may classify all text mismatches as typos. Use separate decisions:
`scan_transcription_error`, `attested_reading_difference`,
`probable_print_error`, `composite_quote`, `printed_fragment`,
`attribution_unresolved`, and `source_coverage_error`. Record the evidence and
the exact printed/display layers for each. These are editorial decisions, not
new large warning labels to insert throughout the reader.

## Still open

Seven flagged names have a separate scan recheck in `katha-source-review.json`;
their eleven proposed replacements replay unique targets in the frozen source.
The repairs still need integration, and this report does not mark their word
analyses or translations accepted. Unattributed
Kaṭha parallels and the six English-only/general-reference names remain in the
full source review. Name 419 has no verified exact external locus. The
proposed correction under 836 is qualified, not a proven critical-edition
judgment. The public reader has not been certified or republished on the
strength of this audit.
