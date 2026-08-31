# Kaṭha 1.1.21: the reading quoted under name 403

Date: 2026-08-30. Scope: textual reading only, not approval of the translation
or grammatical analysis and not a critical edition of the Kaṭha Upaniṣad.

## Decision

Preserve Chinmayananda's **सुविज्ञेयम् / suvijñeyam**. It is visible in the
printed source and is also attested in the verse text published by Sringeri's
Advaita Sharada. The evidence does not justify calling it an OCR or printing
error or replacing it with **सुज्ञेयम् / sujñeyam**.

Treat these as differing attested readings of this locus. This collation does
not establish their manuscript ancestry or which reading is earliest. Do not
infer that the verse was altered from the adjacent bhāṣya merely because one
electronic witness differs. Keep the alternative in source details, not as an
extra competing translation in the main reading flow.

## Witnesses consulted directly

1. **Chinmayananda, Thousand Ways to the Transcendental**, CCMT reprint,
   February 2011, ISBN 9788175972452. PDF page 122, printed page 118, footnote
   under name 403. Local scan: `/Users/eeshan/Downloads/Vishnu Sahasranama.pdf`.
   SHA-256:
   `99084a346d68e5673309e4aca81b9787fe618d8414191f8ec697df4bf2534219`.
   The page image was rendered and visually inspected, not inferred from OCR.
   The printed reading is **सुविज्ञेयमणुरेष**. In the retained transcription:

   देवैरत्रापि विचिकित्सितं पुरा नहि सुविज्ञेयमणुरेष धर्मः।

2. **Sringeri Advaita Sharada, Kaṭhopaniṣad-bhāṣya, first chapter**, first
   vallī, mantra 21. Retrieved 2026-08-30:
   <https://advaitasharada.sringeri.net/read/kathaka-bhashya/1/>.
   The mantra itself, not only its commentary, reads:

   देवैरत्रापि विचिकित्सितं पुरा न हि सुविज्ञेयमणुरेष धर्मः ।

   Its adjacent bhāṣya also reads **सुविज्ञेयं सुष्ठु विज्ञेयम्**. This is an
   electronic institutional witness, not a manuscript apparatus. Only the
   short relevant excerpts are retained here; no licence for republishing the
   entire site's edition is asserted.

3. **GRETIL Kaṭha Upaniṣad with Śaṅkara's bhāṣya**, local text:
   `data/sources/sanskrit/vedic/katha_upanisad_sankara_bhasya_gretil.txt`,
   lines 178–181, locus `kau_1.21/1,1.21`. SHA-256:
   `3054f718c80eca0f3a1df050e0564e42ef6c04af0b5f891c82b51639721cadcc`.
   Its verse reads:

   devair atrāpi vicikitsitaṃ purā na hi sujñeyam aṇur eṣa dharmaḥ /

   Its bhāṣya then reads **na hi suvijñeyaṃ suṣṭhu jñeyam**. Keep the verse
   and bhāṣya readings separate; neither is a licence to overwrite the scan.

4. **Swami Krishnananda, Commentary on the Katha Upanishad**, discourse
   including 1.1.21, official site, retrieved 2026-08-30:
   <https://www.swami-krishnananda.org/kathopanishad/katha_03.html>.
   Its quotation of verse 1.1.21 includes **na hi suvijñeyam**. This
   corroborates use of that reading in another modern commentary; it does not
   establish independent manuscript transmission.

## Required consequence for the candidate data

- Keep the printed string unchanged in `source_text`.
- Display the quoted reading with **su-vi-jñeya**, not **su-jñeya**. Spacing
  `नहि` as `न हि` is a separately recorded segmentation change, not a change
  of the lexical reading.
- Analyze **vi-** as part of the printed verbal formation. Recheck the
  gerundive and inflection from the grammatical witnesses; do not merely edit
  the spelling and leave the old analysis.
- Recheck English alignment against the retained reading and all eleven
  grammatical words. Independently review the final candidate hash.
- Apply the same scan-first/collation decision procedure to other Kaṭha
  occurrences. This finding settles this locus only.
