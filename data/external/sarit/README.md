# SARIT — Search and Retrieval of Indic Texts (TEI sample)

**Homepage:** https://sarit.indology.info/ — at the time of fetch the
public sarit-pm interface returned `502 Bad Gateway`, so all retrieval
was performed against the upstream GitHub mirror.
**Bulk source:** https://github.com/sarit/SARIT-corpus (default branch `master`).
**License:** SARIT's GitHub mirror does not carry a top-level LICENSE
file. The README declares an open-collaboration policy ("any changes you
make to your files can, if you choose so, be shared with other people").
The SARIT project's public webpage historically lists CC-BY for the
corpus; treat as CC-BY-attributed pending direct confirmation from the
SARIT editors. Attribute to "SARIT corpus / sarit.indology.info" in any
downstream work.

## Fetch record

- Fetched: 2026-05-19 23:36 UTC by corpus-chat-lane2.
- Method: per-file `curl` from `https://raw.githubusercontent.com/sarit/SARIT-corpus/master/<file>.xml` at 1 req/sec.
- 10 TEI XML files, total **20 MB on disk**, sha256 in `SHA256SUMS`.

## Sample contents

| File                                          | Size (B) | Tradition / role                                                  |
|-----------------------------------------------|---------:|-------------------------------------------------------------------|
| `bhartrhari-vakyapadiya.xml`                  |   370227 | Vyākaraṇa — Bhartṛhari Vākyapadīya (full)                         |
| `patanjalayogasastra.xml`                     |   207531 | Yoga — Patañjali-Yogaśāstra (sūtra + bhāṣya)                      |
| `vatsyayana-nyayabhasya.xml`                  |   579227 | Nyāya — Vātsyāyana Nyāya-Bhāṣya                                   |
| `bhattojidiksita-siddhantakaumudi.xml`        |  3233651 | Vyākaraṇa — Bhaṭṭoji Siddhānta-Kaumudī                            |
| `kumarila-tantravarttika.xml`                 |  4588745 | Mīmāṃsā — Kumārila Tantra-Vārttika                                |
| `nyayamanjari.xml`                            |  6943279 | Nyāya — Jayanta Bhaṭṭa Nyāya-Mañjarī                              |
| `prasastapada-padarthadharmasangraha.xml`     |   293273 | Vaiśeṣika — Praśastapāda Padārtha-Dharma-Saṃgraha                 |
| `sarvadarsanasangraha.xml`                    |   468798 | Doxography — Mādhava Sarva-Darśana-Saṃgraha                       |
| `vacaspati-tattvavaisaradi.xml`               |   412471 | Yoga — Vācaspati Tattva-Vaiśāradī (on Yoga-Sūtra)                 |
| `pramanavarttikavrtti.xml`                    |  3025284 | Buddhist epistemology — Manorathanandin's vṛtti on Dharmakīrti PV |

All files are TEI P5 in the SARIT customisation
(`schemas/odd/sarit-guidelines.xml` in the upstream repo). The remaining
~85 SARIT files are catalogued in the manifest under `texts` with
`fetch_status: "pending"`; pull them per-file as the corresponding
prakriya cluster comes online.

## What the prakriya pipeline should consume next

1. `bhartrhari-vakyapadiya.xml` and `bhattojidiksita-siddhantakaumudi.xml`
   are the immediate prakriya commentary expansions beyond Mahābhāṣya
   and Kāśikā; they extend witness layer C in the three-witness stack.
2. `kumarila-tantravarttika.xml` and `vacaspati-tattvavaisaradi.xml`
   give the prakriya semantic-feature layer two extra commentarial
   anchors that DCS does not annotate.
3. `pramanavarttikavrtti.xml` is the Buddhist-side counter-witness for
   the comparative-claims engine in `vedanta-timeline`.
