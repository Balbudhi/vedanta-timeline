# Sanskrit mathematics and astronomy corpus

Acquired 2026-08-10 for the Bandyopadhyay metaphysics research and the
Vedānta-timeline primary-source library. These are original-language working
witnesses, retained with the upstream GRETIL XML/HTML and its bibliographic
header. They are not translations, modern reconstructions, or evidence that a
mathematical procedure automatically carries a cosmological doctrine.

## Current core

| Work | What it contributes | Source form |
| --- | --- | --- |
| Āryabhaṭa, *Āryabhaṭīya* with Bhāskara I and Someśvara | astronomical cycles, positional number work, and trigonometric procedures | GRETIL TEI XML |
| Brahmagupta, *Brāhmasphuṭasiddhānta* | arithmetic with `śūnya`/`kha`, algebra, geometry, and jya procedures | GRETIL legacy HTML; its scope is mathematical chapters 12, 18–21, not a falsely labeled complete work |
| *Sūryasiddhānta* | cycles, astronomy, `bhujajyā`/`koṭijyā`, and numerical operations | GRETIL TEI XML |
| Bhāskara II, *Līlāvatī* | arithmetic, algorithms, geometry, and `śūnya` in procedure | GRETIL TEI XML |
| Bhāskara II, *Bījagaṇita* | algebraic rules, unknowns, positive/negative values, and zero | GRETIL TEI XML |
| Mahāvīrācārya, *Gaṇitasārasaṅgraha* | early Jain mathematical source: arithmetic, fractions, series, geometry, and combinatorial procedures | 61-page Devanāgarī manuscript scan; **incomplete**, so retained as a witness rather than a complete text |
| Śrīdharācārya, *Pāṭīgaṇita* | procedural arithmetic, mensuration, rules for fractions and numerical operations | 337-page scan with visibly Sanskrit root/commentary; its modern English layer is not used as constructive evidence |
| Nīlakaṇṭha Somayājī, *Tantrasaṅgraha* | Sanskrit astronomical mathematics, including the Kerala-school series and trigonometric material, with Sanskrit commentaries | 494-page source-edition scan |
| Jyeṣṭhadeva, *Yuktibhāṣā* | Kerala mathematical argument and series tradition | 360-page Malayalam original-language scan; comparator, **not Sanskrit** |

## Research use and limits

The immediate task is literal, source-pinned analysis of the technical terms
and operations: what `śūnya`, `kha`, `bindu`, `ananta`, `jya`, `koṭijyā`, and
series-related vocabulary do in their own mathematical contexts. Only then can
they be compared with Bandyopadhyay's point/zero/one/infinity, prime, clock,
or projection vocabulary. The comparison must keep four levels separate:

1. the Sanskrit expression and its grammatical construction;
2. the mathematical operation or astronomical model actually stated;
3. any later philosophical or cosmological use of a cognate term; and
4. Bandyopadhyay's authorial formalization.

The Kerala lane is now source-held and has a first direct reading pass: the
*Tantrasaṅgraha* scan visibly contains the Devanāgarī Sanskrit root and
commentary text. Its chapter 2, printed pp. 88–94, is explicitly headed as
summation material and treats natural-number, square, cube, and a further
summation series; printed pp. 95–120 then opens a sustained `jyā`/arc and
R-sine procedure. These are secure technical anchors, not yet a reconstructed
calculus or an infinity metaphysics. The *Yuktibhāṣā* scan is a readable
Malayalam witness; its language distinction is part of the evidence, rather
than a defect to be hidden. Both still require complete relevant-unit reading
before a calculus or infinity comparison.

## Upstream provenance

- `aryabhata_aryabhatiya_bhaskara_somesvara_gretil.xml` —
  `https://gretil.sub.uni-goettingen.de/gretil/corpustei/sa_AryabhaTa-AryabhaTIya-comm.xml`
- `bhaskara_lilavati_gretil.xml` —
  `https://gretil.sub.uni-goettingen.de/gretil/corpustei/sa_bhAskara-lIlAvatI.xml`
- `bhaskara_bijaganita_gretil.xml` —
  `https://gretil.sub.uni-goettingen.de/gretil/corpustei/sa_bhAskara-bIjagaNita.xml`
- `suryasiddhanta_gretil.xml` —
  `https://gretil.sub.uni-goettingen.de/gretil/corpustei/sa_sUryasiddhAnta.xml`
- `brahmagupta_brahmasphutasiddhanta_gretil.html` —
  `https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/6_sastra/8_jyot/brsphutu.htm`
- `nilakantha_tantrasangraha_yuktidipika_laghuvivrti_1977_scan.pdf` —
  `https://exhibits.cooponscitech.in/files/original/39012/Tantrasan_graha_of_Ni_lakan_t_ha_Somaya_ji_with_Yuktidi_pika_and_Laghuvivr_ti_of_S_an_kara.pdf`
- `jyesthadeva_yuktibhasa_malayalam_scan.pdf` —
  `https://commons.wikimedia.org/wiki/Special:FilePath/Yukthibhasha.pdf`
- `mahavira_ganitasarasangraha_devanagari_manuscript.pdf` —
  `https://archive.org/details/india.history.resource.16342`
- `sridhara_patiganita_shukla_scan.pdf` —
  `https://archive.org/details/patiganita-sridharacharya-kripa-shankar-shukla`

Every file retains its upstream edition and normalization note. SHA-256 and
file metadata are registered in `data/primary_text_manifest.json`.

## Machine-readability note

All four GRETIL XML witnesses parse as XML. GRETIL's *Līlāvatī* source carries
two repeated XML IDs (`Lil_219p1` and `Lil_226p1`), so its supplied verse labels
remain useful human locators but must not be treated as globally unique XML IDs
by a reader or citation tool. This is retained upstream data, not silently
corrected editorially.
