# Glossary Expansion Plan (Phase 1)

_Generated 2026-05-10. Audits the 144 glossary entries in `site/data/glossary/` for school coverage and citation backing, ranks terms by appearance frequency in the on-disk corpus (thinker JSONs + `full_translations/`), and stages a Wave-1 batch._

## Headline numbers

- Total terms surveyed: **144** (after dropping `manifest.json`).
- Mean per-school entry count, current state: **3.86 schools/term**.
- Distribution: 4 terms with 1 school; 11 with 2; 36 with 3; 59 with 4; 21 with 5; 10 with 6; 3 with 7. **Zero terms** carry cite:// links anywhere in `per_school` prose.
- On-disk citation index: **783 entries** drawing from 29 thinker JSONs, with strong concentration in Madhva (208), Nāgārjuna (71), Madhusūdana (67), Vasubandhu (41), Gauḍapāda (37), Yāmunācārya (37), Śaṅkara (29).
- Full-translation corpus: **70 work-level files** in `site/data/full_translations/` covering all major Vedānta and Buddhist primaries, plus extensive Sanskrit primaries on disk under `materials/primary_texts/sanskrit/`.

## Canonical school axis

The Wave-1 expansion targets these 14 doctrinal schools, plus auxiliary positions (Pāṇinian-Vaiyākaraṇa, Jainism) where the term has standing literature:

Advaita · Viśiṣṭādvaita · Tattva-vāda (Madhva) · Bhedābheda (Bhāskara, Yādava-Prakāśa) · Acintya-Bhedābheda (Caitanya / Jīva Gosvāmī) · Dvaitādvaita (Nimbārka) · Śuddhādvaita (Vallabha) · Sāṅkhya · Yoga · Nyāya-Vaiśeṣika · Pūrva-Mīmāṃsā · Mādhyamaka · Yogācāra · Pratyabhijñā / Trika.

"Substantive" means the school's extant literature treats the term explicitly (not incidental use). `Tattva-vāda` is the project's mandated label for Madhva's school per `CLAUDE.md`; the rename agent is sweeping the rest.

## Wave 1 — top 30 doctrinal terms

Ranked by alias-count across the on-disk corpus (thinker JSONs + full translations), filtered to drop bibliographic-genre terms (`sūtra`, `bhāṣya`, `ṭīkā`, `prakaraṇa`, `vārttika`, `śloka`, `smṛti`).

| # | Term | Hits | Cur | Cite-evidence schools | Missing canonical schools | Diff |
|---|------|-----:|----:|-----------------------|---------------------------|:----:|
| 1 | `brahman` (brahman) | 3441 | 7 | Advaita-pre, Advaita, Dvaitādvaita, Tattva-vāda, Śuddhādvaita, Viśiṣṭādvaita, Sāṅkhya-Yoga (synthetic) | visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika … | L |
| 2 | `atman` (ātman) | 1569 | 5 | Advaita-pre, Advaita, Tattva-vāda, Dvaitādvaita, Śuddhādvaita, Viśiṣṭādvaita, Mādhyamaka, Acintya-Bhedābheda, Yogācāra | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga … | L |
| 3 | `purusa` (puruṣa) | 1432 | 5 | Dvaitādvaita, Śuddhādvaita, Sāṅkhya-Yoga (synthetic), Viśiṣṭādvaita, Advaita, Tattva-vāda, Mādhyamaka, Yogācāra | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, yoga, nyaya-vaisesika … | L |
| 4 | `karma` (karma) | 1386 | 7 | Acintya-Bhedābheda, Tattva-vāda, Advaita, Sāṅkhya-Yoga (synthetic), Viśiṣṭādvaita, Mādhyamaka, Yogācāra | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | L |
| 5 | `sat` (sat) | 1340 | 4 | Advaita, Tattva-vāda, Śuddhādvaita, Mādhyamaka, Yogācāra, Viśiṣṭādvaita, Acintya-Bhedābheda | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga … | L |
| 6 | `karana` (karaṇa) | 1156 | 5 | Advaita, Tattva-vāda, Mādhyamaka | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga … | L |
| 7 | `jnana` (jñāna) | 1149 | 5 | Advaita, Tattva-vāda, Dvaitādvaita, Mādhyamaka, Viśiṣṭādvaita, Acintya-Bhedābheda, Yogācāra | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga … | L |
| 8 | `jiva` (jīva) | 1138 | 7 | Advaita, Tattva-vāda, Dvaitādvaita, Śuddhādvaita, Sāṅkhya-Yoga (synthetic), Acintya-Bhedābheda, Viśiṣṭādvaita | visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika … | L |
| 9 | `anu` (aṇu) | 1071 | 4 | Acintya-Bhedābheda, Tattva-vāda, Dvaitādvaita, Śuddhādvaita, Advaita, Viśiṣṭādvaita, Mādhyamaka, Yogācāra | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | L |
| 10 | `dvaita` (dvaita) | 1025 | 3 | Advaita, Tattva-vāda, Viśiṣṭādvaita | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | L |
| 11 | `vidya` (vidyā) | 978 | 4 | Advaita, Tattva-vāda, Śuddhādvaita, Viśiṣṭādvaita, Sāṅkhya-Yoga (synthetic), Acintya-Bhedābheda, Mādhyamaka, Yogācāra | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | M |
| 12 | `maya` (māyā) | 854 | 6 | Advaita, Dvaitādvaita, Tattva-vāda, Śuddhādvaita, Sāṅkhya-Yoga (synthetic), Mādhyamaka, Acintya-Bhedābheda, Viśiṣṭādvaita, Yogācāra | visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika … | M |
| 13 | `bheda` (bheda) | 782 | 4 | Advaita, Tattva-vāda, Dvaitādvaita, Viśiṣṭādvaita, Acintya-Bhedābheda | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga … | M |
| 14 | `bhakti` (bhakti) | 755 | 5 | Acintya-Bhedābheda, Advaita, Tattva-vāda, Dvaitādvaita, Śuddhādvaita, Viśiṣṭādvaita | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga … | M |
| 15 | `advaita` (advaita) | 696 | 4 | Advaita, Tattva-vāda, Yogācāra | advaita, visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | M |
| 16 | `kartr` (kartṛ) | 662 | 6 | Advaita, Śuddhādvaita, Tattva-vāda, Mādhyamaka, Viśiṣṭādvaita | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga … | M |
| 17 | `avidya` (avidyā) | 628 | 4 | Advaita, Sāṅkhya-Yoga (synthetic), Tattva-vāda, Mādhyamaka, Viśiṣṭādvaita | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | M |
| 18 | `dharma` (dharma) | 543 | 6 | Śuddhādvaita, Viśiṣṭādvaita, Advaita, Tattva-vāda, Mādhyamaka, Yogācāra | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | M |
| 19 | `pramana` (pramāṇa) | 541 | 6 | Advaita, Tattva-vāda, Viśiṣṭādvaita, Yogācāra | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | M |
| 20 | `mithya` (mithyā) | 433 | 5 | Advaita, Tattva-vāda | visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika … | M |
| 21 | `moksa` (mokṣa) | 406 | 5 | Tattva-vāda, Advaita, Yogācāra, Mādhyamaka | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga … | M |
| 22 | `rasa` (rasa) | 385 | 3 | Advaita, Dvaitādvaita, Tattva-vāda, Mādhyamaka, Viśiṣṭādvaita, Acintya-Bhedābheda, Yogācāra | advaita, visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | S |
| 23 | `isvara` (Īśvara) | 338 | 5 | Tattva-vāda, Advaita, Sāṅkhya-Yoga (synthetic), Viśiṣṭādvaita | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, nyaya-vaisesika … | S |
| 24 | `sruti` (śruti) | 336 | 5 | Tattva-vāda, Advaita, Dvaitādvaita, Sāṅkhya-Yoga (synthetic), Viśiṣṭādvaita | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga … | S |
| 25 | `guna` (guṇa) | 332 | 6 | Advaita, Tattva-vāda, Dvaitādvaita, Acintya-Bhedābheda, Viśiṣṭādvaita, Yogācāra | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga … | S |
| 26 | `sakti` (śakti) | 319 | 4 | Acintya-Bhedābheda, Advaita, Dvaitādvaita, Yogācāra, Tattva-vāda | advaita, visistadvaita, tattva-vada, bhedabheda, dvaitadvaita, suddhadvaita … | S |
| 27 | `visnu` (Viṣṇu) | 318 | 4 | Tattva-vāda, Advaita, Viśiṣṭādvaita | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga … | S |
| 28 | `amsa` (aṃśa) | 308 | 5 | Advaita, Dvaitādvaita, Śuddhādvaita, Tattva-vāda, Viśiṣṭādvaita | visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika … | S |
| 29 | `sabda` (śabda) | 304 | 6 | Advaita, Sāṅkhya-Yoga (synthetic), Mādhyamaka, Yogācāra, Tattva-vāda, Viśiṣṭādvaita | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … | S |
| 30 | `buddhi` (buddhi) | 257 | 5 | Advaita, Mādhyamaka, Yogācāra, Tattva-vāda | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga … | S |

### Per-term Wave-1 specs

#### 1. `brahman.json` — brahman

- Aliases: `brahman, ब्रह्मन्, brahmano, Brahma, brahmaṇ, Brahman, brahmaṇi, brahma…`.
- Current schools (7): Advaita, Viśiṣṭādvaita, Dvaita, Bhedābheda (Bhāskara, Yādava-Prakāśa), Acintya-Bhedābheda (Caitanya / Jīva Gosvāmī), Śuddhādvaita (Vallabha), Dvaitādvaita (Nimbārka).
- Missing canonical schools to attempt: **visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=3441).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://bhartrprapanca/brhadaranyaka-commentary-fragments/2.3` — bhartrprapanca / BṛU 2.3.1, 2.3.6 _(school: Advaita-pre)_
  - `cite://bhartrprapanca/brhadaranyaka-commentary-fragments/1.4.10` — bhartrprapanca / BṛU 1.4.10 _(school: Advaita-pre)_
  - `cite://madhusudana/bhakti-rasayana/1.ṭīkā.1` — madhusudana / BR 1.1 ṭīkā _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-discussion-of-nanda` — mandana / BS 1.1 (opening ānanda discussion) _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-ekatva-and-m-y` — mandana / BS 1.1 (plurality as māyā-bound) _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-avidy` — mandana / BS 1.1 (avidyā neither sat nor asat; in the jīvas) _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.4--tarka-k-a-opening-verse` — mandana / BS 1.4 _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.35-36--discussion-of-tattvadar-an-bhy-sa` — mandana / BS 1.35-36 _(school: Advaita)_

#### 2. `atman.json` — ātman

- Aliases: `atma, Ātman, ātmanā, ātman, आत्मन्, ātmanaḥ, ātmā, atman…`.
- Current schools (5): Advaita, Viśiṣṭādvaita, Dvaita, Acintya-Bhedābheda, Buddhist (opponent position).
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=1569).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://bhartrprapanca/brhadaranyaka-commentary-fragments/2.4.5, 1.4.15` — bhartrprapanca / BṛU 2.4.5, 1.4.15 _(school: Advaita-pre)_
  - `cite://gaudapada/mandukya-karika/3.Advaita-prakaraṇa.3-7` — gaudapada / MK 3.3-7 _(school: Advaita)_
  - `cite://madhusudana/siddhanta-bindu/1.prathamo vibhāgaḥ.1` — madhusudana / SB 1 _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-discussion-of-nanda` — mandana / BS 1.1 (opening ānanda discussion) _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/jīvasya brahma-pratibimbatvāpādanam` — prakasatman / PV p. 65 _(school: Advaita)_
  - `cite://raghavendra/tantra-dipika/1.3` — raghavendra / TD 1.3, suṣuptyutkrāntyor bhedena _(school: Tattva-vāda)_
  - `cite://raghavendra/tantra-dipika/1.4` — raghavendra / TD 1.4, jñeyatvavacanāc ca _(school: Tattva-vāda)_
  - `cite://sankara/upadesa-sahasri/I.17.7-9` — sankara / UpS I.17.7-9 _(school: Advaita)_

#### 3. `purusa.json` — puruṣa

- Aliases: `पुरुष, puruṣaḥ, purusa, Puruṣa, puruṣottama, puruṣe, puruṣasya, puruṣa…`.
- Current schools (5): Sāṅkhya / Yoga, Advaita, Viśiṣṭādvaita, Dvaita, Acintya-Bhedābheda.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=1432).
- Citation candidates already in `citation_index.json` (23 top hits):
  - `cite://srinivasa/vedanta-kaustubha/2.3.42` — srinivasa / BS 2.3.42 _(school: Dvaitādvaita)_
  - `cite://vallabha/anu-bhasya/1.1.12-19` — vallabha / BSB 1.1.12-19 _(school: Śuddhādvaita)_
  - `cite://vijnanabhiksu/yoga-varttika/1.24` — vijnanabhiksu / YV 1.24 _(school: Sāṅkhya-Yoga (synthetic))_
  - `cite://yamuna/siddhi-trayam/16-18` — yamuna / ĪS 16-18 _(school: Viśiṣṭādvaita)_
  - `cite://madhusudana/siddhanta-bindu/10` — madhusudana /  _(school: Advaita)_
  - `cite://madhva/brahma-sutra-bhasya/1.1.1.7` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/brahma-sutra-bhasya/1.1.1.18` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/mayavada-khandana/15.16` — madhva /  _(school: Tattva-vāda)_

#### 4. `karma.json` — karma

- Aliases: `Karma, karma, karmaṇaḥ, karman, कर्म, karmān, karmaṇi, karmaṇā…`.
- Current schools (7): Pūrva-Mīmāṃsā, Yoga, Advaita, Viśiṣṭādvaita, Dvaita, Buddhism, Jainism.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya, nyaya-vaisesika, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=1386).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://kesava-kasmiri/krama-dipika/8.96` — kesava-kasmiri / KD 8.96 _(school: Acintya-Bhedābheda)_
  - `cite://madhva/anuvyakhyana/1.1.13-15` — madhva / Anuvy. 1.1.13-15 _(school: Tattva-vāda)_
  - `cite://prakasatman/pancapadika-vivarana/brahma-vicāre kim-ānantaryam atha-śabdāvagamyam` — prakasatman / PV p. 164 _(school: Advaita)_
  - `cite://sankara/upadesa-sahasri/I.11.15` — sankara / UpS I.11.15 _(school: Advaita)_
  - `cite://sankara/upadesa-sahasri/I.17.7-9` — sankara / UpS I.17.7-9 _(school: Advaita)_
  - `cite://sarvajnatman/samksepa-sariraka/1.327` — sarvajnatman / SS I.327 _(school: Advaita)_
  - `cite://sureshvara/naishkarmya-siddhi/1.98-99` — sureshvara / NS 1.98-99 _(school: Advaita)_
  - `cite://vijnanabhiksu/yoga-varttika/1.24` — vijnanabhiksu / YV 1.24 _(school: Sāṅkhya-Yoga (synthetic))_

#### 5. `sat.json` — sat

- Aliases: `satyam, satya, sad-rupa, सत्, satsya, sat, Sat`.
- Current schools (4): Advaita, Sāṅkhya, Viśiṣṭādvaita, Dvaita.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=1340).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://madhusudana/bhakti-rasayana/1.1` — madhusudana / BR 1.1 _(school: Advaita)_
  - `cite://madhva/anuvyakhyana/1.4.111-112` — madhva / Anuvy. 1.4.111-112 _(school: Tattva-vāda)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-avidy` — mandana / BS 1.1 (avidyā neither sat nor asat; in the jīvas) _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.35-36--discussion-of-tattvadar-an-bhy-sa` — mandana / BS 1.35-36 _(school: Advaita)_
  - `cite://padmapada/pancapadika/V–VI.15–16` — padmapada / PañcP V.15–VI.16 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/mahāvākyasyāparokṣa-prayojakatvam` — prakasatman / PV p. 103 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/brahma-vicāre kim-ānantaryam atha-śabdāvagamyam` — prakasatman / PV p. 164 _(school: Advaita)_
  - `cite://sankara/mandukya-bhasya/upaniṣad.7` — sankara / MāṇḍU 7 _(school: Advaita)_

#### 6. `karana.json` — karaṇa

- Aliases: `karaṇa, Karaṇa, karaṇaiḥ, करण, karana, karaṇāni, karaṇena`.
- Current schools (5): Pāṇinian grammar, Sāṅkhya / Yoga, Vaiśeṣika / Nyāya, Advaita, Viśiṣṭādvaita.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=1156).
- Citation candidates already in `citation_index.json` (13 top hits):
  - `cite://gaudapada/mandukya-karika/1.Āgama-prakaraṇa.16-18` — gaudapada / MK 1.16-18 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/2.Vaitathya-prakaraṇa.5-6` — gaudapada / MK 2.5-6 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/3.Advaita-prakaraṇa.3-7` — gaudapada / MK 3.3-7 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/3.Advaita-prakaraṇa.19-21` — gaudapada / MK 3.19-21 _(school: Advaita)_
  - `cite://raghavendra/tantra-dipika/1.1` — raghavendra / TD 1.1, bhedavyapadeśāc ca _(school: Tattva-vāda)_
  - `cite://sankara/upadesa-sahasri/I.11.15` — sankara / UpS I.11.15 _(school: Advaita)_
  - `cite://sankara/upadesa-sahasri/I.17.7-9` — sankara / UpS I.17.7-9 _(school: Advaita)_
  - `cite://sarvajnatman/samksepa-sariraka/3.278` — sarvajnatman / SS III.278 _(school: Advaita)_

#### 7. `jnana.json` — jñāna

- Aliases: `jnana, jñāna, jñānasya, jnani, ज्ञान, Jñāna, jñānin, jñānaṃ…`.
- Current schools (5): Advaita, Viśiṣṭādvaita, Dvaita, Buddhist, Acintya-Bhedābheda.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=1149).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://madhusudana/siddhanta-bindu/upodghāta` — madhusudana / SB Upodghāta _(school: Advaita)_
  - `cite://madhusudana/siddhanta-bindu/1.prathamo vibhāgaḥ.1` — madhusudana / SB 1 _(school: Advaita)_
  - `cite://madhva/anuvyakhyana/1.1.13-15` — madhva / Anuvy. 1.1.13-15 _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/1.4.111-112` — madhva / Anuvy. 1.4.111-112 _(school: Tattva-vāda)_
  - `cite://nimbarka/dasa-shloki/1` — nimbarka / DaŚ 1 _(school: Dvaitādvaita)_
  - `cite://padmapada/pancapadika/V–VI.15–16` — padmapada / PañcP V.15–VI.16 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/jīvasya brahma-pratibimbatvāpādanam` — prakasatman / PV p. 65 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/brahma-vicāre kim-ānantaryam atha-śabdāvagamyam` — prakasatman / PV p. 164 _(school: Advaita)_

#### 8. `jiva.json` — jīva

- Aliases: `jīvātmā, jīvāḥ, jiva, jīvātman, जीव, Jīva, jīvānām, jīvasya…`.
- Current schools (7): Advaita, Viśiṣṭādvaita, Dvaita, Bhedābheda (Bhāskara), Acintya-Bhedābheda, Śuddhādvaita (Vallabha), Jainism.
- Missing canonical schools to attempt: **visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=1138).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://gaudapada/mandukya-karika/1.Āgama-prakaraṇa.16-18` — gaudapada / MK 1.16-18 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/3.Advaita-prakaraṇa.3-7` — gaudapada / MK 3.3-7 _(school: Advaita)_
  - `cite://madhva/anuvyakhyana/1.1.13-15` — madhva / Anuvy. 1.1.13-15 _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/1.4.111-112` — madhva / Anuvy. 1.4.111-112 _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/2.3.66-69` — madhva / Anuvy. 2.3.66-69 _(school: Tattva-vāda)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-avidy` — mandana / BS 1.1 (avidyā neither sat nor asat; in the jīvas) _(school: Advaita)_
  - `cite://nimbarka/dasa-shloki/1` — nimbarka / DaŚ 1 _(school: Dvaitādvaita)_
  - `cite://nimbarka/dasa-shloki/2` — nimbarka / DaŚ 2 _(school: Dvaitādvaita)_

#### 9. `anu.json` — aṇu

- Aliases: `aṇu-jīva, aṇuḥ, Aṇu, aṇu, aṇu-parimāṇa, अणु, anu`.
- Current schools (4): Viśiṣṭādvaita, Dvaita, Advaita, Vaiśeṣika.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=1071).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://kesava-kasmiri/krama-dipika/8.96` — kesava-kasmiri / KD 8.96 _(school: Acintya-Bhedābheda)_
  - `cite://madhva/anuvyakhyana/1.1.13-15` — madhva / Anuvy. 1.1.13-15 _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/1.4.111-112` — madhva / Anuvy. 1.4.111-112 _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/2.3.66-69` — madhva / Anuvy. 2.3.66-69 _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/3.3.1` — madhva / Anuvy. 3.3.1 _(school: Tattva-vāda)_
  - `cite://nimbarka/dasa-shloki/1` — nimbarka / DaŚ 1 _(school: Dvaitādvaita)_
  - `cite://nimbarka/dasa-shloki/5` — nimbarka / DaŚ 5 _(school: Dvaitādvaita)_
  - `cite://srinivasa/vedanta-kaustubha/Upodghāta` — srinivasa / Upodghāta _(school: Dvaitādvaita)_

#### 10. `dvaita.json` — dvaita

- Aliases: `dvaitam, द्वैत, dvaita, tattva-vada, Dvaita, tattvavāda`.
- Current schools (3): Dvaita (Madhva), Advaita, Viśiṣṭādvaita.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **L** (hits=1025).
- Citation candidates already in `citation_index.json` (19 top hits):
  - `cite://gaudapada/mandukya-karika/1.Āgama-prakaraṇa.16-18` — gaudapada / MK 1.16-18 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/3.Advaita-prakaraṇa.3-7` — gaudapada / MK 3.3-7 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/3.Advaita-prakaraṇa.19-21` — gaudapada / MK 3.19-21 _(school: Advaita)_
  - `cite://madhva/anuvyakhyana/1.4.111-112` — madhva / Anuvy. 1.4.111-112 _(school: Tattva-vāda)_
  - `cite://sankara/mandukya-bhasya/upaniṣad.7` — sankara / MāṇḍU 7 _(school: Advaita)_
  - `cite://yamuna/siddhi-trayam/31-35` — yamuna / Svs 31-35 _(school: Viśiṣṭādvaita)_
  - `cite://gaudapada/mandukya-karika/1.13` — gaudapada /  _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/1.16` — gaudapada /  _(school: Advaita)_

#### 11. `vidya.json` — vidyā

- Aliases: `vidyāyām, vidyā, Vidyā, brahmavidya, विद्या, vidya, vidyayā, vidyāyāḥ…`.
- Current schools (4): Advaita, Viśiṣṭādvaita, Dvaita, Mīmāṃsā.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **M** (hits=978).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://gaudapada/mandukya-karika/1.Āgama-prakaraṇa.16-18` — gaudapada / MK 1.16-18 _(school: Advaita)_
  - `cite://madhusudana/bhakti-rasayana/1.ṭīkā.1` — madhusudana / BR 1.1 ṭīkā _(school: Advaita)_
  - `cite://madhva/anuvyakhyana/1.4.111-112` — madhva / Anuvy. 1.4.111-112 _(school: Tattva-vāda)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-avidy` — mandana / BS 1.1 (avidyā neither sat nor asat; in the jīvas) _(school: Advaita)_
  - `cite://padmapada/pancapadika/V–VI.15–16` — padmapada / PañcP V.15–VI.16 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/brahmaṇo lakṣaṇopalakṣaṇe` — prakasatman / PV p. 212 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/brahma-vicāre kim-ānantaryam atha-śabdāvagamyam` — prakasatman / PV p. 164 _(school: Advaita)_
  - `cite://sankara/upadesa-sahasri/I.17.7-9` — sankara / UpS I.17.7-9 _(school: Advaita)_

#### 12. `maya.json` — māyā

- Aliases: `māyāvāda, maya, māyāyāḥ, māyāyām, māyāvādin, māyā, Māyā, माया…`.
- Current schools (6): Advaita, Viśiṣṭādvaita, Dvaita, Acintya-Bhedābheda, Bhedābheda (Bhāskara), Trika / Kashmir Śaivism.
- Missing canonical schools to attempt: **visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara**.
- Difficulty: **M** (hits=854).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://gaudapada/mandukya-karika/1.Āgama-prakaraṇa.16-18` — gaudapada / MK 1.16-18 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/3.Advaita-prakaraṇa.19-21` — gaudapada / MK 3.19-21 _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-ekatva-and-m-y` — mandana / BS 1.1 (plurality as māyā-bound) _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-avidy` — mandana / BS 1.1 (avidyā neither sat nor asat; in the jīvas) _(school: Advaita)_
  - `cite://nimbarka/dasa-shloki/2` — nimbarka / DaŚ 2 _(school: Dvaitādvaita)_
  - `cite://prakasatman/pancapadika-vivarana/brahmaṇo lakṣaṇopalakṣaṇe` — prakasatman / PV p. 212 _(school: Advaita)_
  - `cite://raghavendra/tantra-dipika/1.1` — raghavendra / TD 1.1, bhedavyapadeśāc ca _(school: Tattva-vāda)_
  - `cite://vallabha/anu-bhasya/1.1.12-19` — vallabha / BSB 1.1.12-19 _(school: Śuddhādvaita)_

#### 13. `bheda.json` — bheda

- Aliases: `bhedān, bhede, bhedasya, bhedaḥ, Bheda, bheda, भेद`.
- Current schools (4): Advaita, Viśiṣṭādvaita, Dvaita, Bhedābheda / Acintya-Bhedābheda.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **M** (hits=782).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://gaudapada/mandukya-karika/2.Vaitathya-prakaraṇa.5-6` — gaudapada / MK 2.5-6 _(school: Advaita)_
  - `cite://madhva/anuvyakhyana/1.4.111-112` — madhva / Anuvy. 1.4.111-112 _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/2.3.66-69` — madhva / Anuvy. 2.3.66-69 _(school: Tattva-vāda)_
  - `cite://nimbarka/dasa-shloki/2` — nimbarka / DaŚ 2 _(school: Dvaitādvaita)_
  - `cite://raghavendra/tantra-dipika/1.1` — raghavendra / TD 1.1, bhedavyapadeśāc ca _(school: Tattva-vāda)_
  - `cite://raghavendra/tantra-dipika/1.3` — raghavendra / TD 1.3, suṣuptyutkrāntyor bhedena _(school: Tattva-vāda)_
  - `cite://vedanta-desika/pancaratra-raksha/1.catvāraḥ siddhāntāḥ` — vedanta-desika / PR 1, Catvāraḥ Siddhāntāḥ _(school: Viśiṣṭādvaita)_
  - `cite://gaudapada/mandukya-karika/2.4` — gaudapada /  _(school: Advaita)_

#### 14. `bhakti.json` — bhakti

- Aliases: `bhakta, bhaktaḥ, bhakter, Bhakti, bhaktiḥ, bhakti, bhaktyā, भक्ति…`.
- Current schools (5): Advaita, Viśiṣṭādvaita, Dvaita, Acintya-Bhedābheda, Śuddhādvaita (Vallabha).
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **M** (hits=755).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://kesava-kasmiri/krama-dipika/1.5` — kesava-kasmiri / KD 1.5 _(school: Acintya-Bhedābheda)_
  - `cite://kesava-kasmiri/krama-dipika/8.96` — kesava-kasmiri / KD 8.96 _(school: Acintya-Bhedābheda)_
  - `cite://madhusudana/bhakti-rasayana/1.1` — madhusudana / BR 1.1 _(school: Advaita)_
  - `cite://madhusudana/bhakti-rasayana/1.ṭīkā.1` — madhusudana / BR 1.1 ṭīkā _(school: Advaita)_
  - `cite://madhva/anuvyakhyana/3.3.1` — madhva / Anuvy. 3.3.1 _(school: Tattva-vāda)_
  - `cite://nimbarka/dasa-shloki/2` — nimbarka / DaŚ 2 _(school: Dvaitādvaita)_
  - `cite://vallabha/anu-bhasya/1.1.12-19` — vallabha / BSB 1.1.12-19 _(school: Śuddhādvaita)_
  - `cite://yamuna/stotra-ratna/22-24` — yamuna / YStr 22-24 _(school: Viśiṣṭādvaita)_

#### 15. `advaita.json` — advaita

- Aliases: `advaita, advaya, Advaita, अद्वैत, advayatva, advaitam`.
- Current schools (4): Advaita (Śaṅkara), Viśiṣṭādvaita, Śuddhādvaita (Vallabha), Acintya-Bhedābheda.
- Missing canonical schools to attempt: **advaita, visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **M** (hits=696).
- Citation candidates already in `citation_index.json` (12 top hits):
  - `cite://gaudapada/mandukya-karika/1.Āgama-prakaraṇa.16-18` — gaudapada / MK 1.16-18 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/3.Advaita-prakaraṇa.3-7` — gaudapada / MK 3.3-7 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/3.Advaita-prakaraṇa.19-21` — gaudapada / MK 3.19-21 _(school: Advaita)_
  - `cite://sankara/mandukya-bhasya/upaniṣad.7` — sankara / MāṇḍU 7 _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/1.16` — gaudapada /  _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/1.17` — gaudapada /  _(school: Advaita)_
  - `cite://gaudapada/mandukya-karika/3.18` — gaudapada /  _(school: Advaita)_
  - `cite://madhusudana/advaita-siddhi/4` — madhusudana /  _(school: Advaita)_

#### 16. `kartr.json` — kartṛ

- Aliases: `kartr, kartāram, kartā, kartṛtva, kartrtva, kartṛ, कर्तृ, Kartṛ…`.
- Current schools (6): Pāṇinian grammar, Sāṅkhya / Yoga, Advaita, Viśiṣṭādvaita, Dvaita, Trika / Kashmir Śaivism.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara**.
- Difficulty: **M** (hits=662).
- Citation candidates already in `citation_index.json` (7 top hits):
  - `cite://sarvajnatman/samksepa-sariraka/1.327` — sarvajnatman / SS I.327 _(school: Advaita)_
  - `cite://vallabha/anu-bhasya/1.4.26` — vallabha / BSB 1.4.26 _(school: Śuddhādvaita)_
  - `cite://madhva/upadhi-khandana/13` — madhva /  _(school: Tattva-vāda)_
  - `cite://nagarjuna/mula-madhyamaka-karika/24.17` — nagarjuna /  _(school: Mādhyamaka)_
  - `cite://ramanuja/shri-bhasya/5` — ramanuja /  _(school: Viśiṣṭādvaita)_
  - `cite://sarvajnatman/samkshepa-sariraka/I.327` — sarvajnatman /  _(school: Advaita)_
  - `cite://vallabha/anubhasya/1.4.26a` — vallabha /  _(school: Śuddhādvaita)_

#### 17. `avidya.json` — avidyā

- Aliases: `avidyayā, avidyā, ajnana, अविद्या, Avidyā, avidyāyāḥ, ajñāna, avidyāyām…`.
- Current schools (4): Advaita, Viśiṣṭādvaita, Dvaita, Buddhist.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **M** (hits=628).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://madhusudana/siddhanta-bindu/upodghāta` — madhusudana / SB Upodghāta _(school: Advaita)_
  - `cite://madhusudana/siddhanta-bindu/1.prathamo vibhāgaḥ.1` — madhusudana / SB 1 _(school: Advaita)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-avidy` — mandana / BS 1.1 (avidyā neither sat nor asat; in the jīvas) _(school: Advaita)_
  - `cite://padmapada/pancapadika/V–VI.15–16` — padmapada / PañcP V.15–VI.16 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/brahmaṇo lakṣaṇopalakṣaṇe` — prakasatman / PV p. 212 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/brahma-vicāre kim-ānantaryam atha-śabdāvagamyam` — prakasatman / PV p. 164 _(school: Advaita)_
  - `cite://sankara/upadesa-sahasri/I.17.7-9` — sankara / UpS I.17.7-9 _(school: Advaita)_
  - `cite://sankara/mandukya-bhasya/upaniṣad.7` — sankara / MāṇḍU 7 _(school: Advaita)_

#### 18. `dharma.json` — dharma

- Aliases: `dharmaḥ, Dharma, dharmāḥ, dharmasya, dharmān, धर्म, dharma, dharmaṃ`.
- Current schools (6): Pūrva-Mīmāṃsā, Advaita, Viśiṣṭādvaita, Dvaita, Yoga, Buddhism.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya, nyaya-vaisesika, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **M** (hits=543).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://vallabha/anu-bhasya/1.1.4` — vallabha / BSB 1.1.4 _(school: Śuddhādvaita)_
  - `cite://vedanta-desika/pancaratra-raksha/1.vaikhānasa-pāñcarātra-avirodha` — vedanta-desika / PR 1, Avirodhopayogābhyām _(school: Viśiṣṭādvaita)_
  - `cite://yamuna/stotra-ratna/22-24` — yamuna / YStr 22-24 _(school: Viśiṣṭādvaita)_
  - `cite://madhusudana/bhakti-rasayana/1.1 ṭīkā.12` — madhusudana /  _(school: Advaita)_
  - `cite://madhva/mithyatvanumana-khandana/239, clause 15` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/mithyatvanumana-khandana/239, clause 16` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/mithyatvanumana-khandana/239, clause 17` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/visnu-tattva-vinirnaya/3.21` — madhva /  _(school: Tattva-vāda)_

#### 19. `pramana.json` — pramāṇa

- Aliases: `Pramāṇa, प्रमाण, pramāṇasya, pramāṇāni, pramāṇa, pramāṇāt, pramane, pramana`.
- Current schools (6): Nyāya, Mīmāṃsā, Advaita, Viśiṣṭādvaita, Dvaita, Buddhist Pramāṇa.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **M** (hits=541).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://madhusudana/siddhanta-bindu/upodghāta` — madhusudana / SB Upodghāta _(school: Advaita)_
  - `cite://madhva/anuvyakhyana/2.3.66-69` — madhva / Anuvy. 2.3.66-69 _(school: Tattva-vāda)_
  - `cite://prakasatman/pancapadika-vivarana/mahāvākyasyāparokṣa-prayojakatvam` — prakasatman / PV p. 103 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/brahma-vicāre kim-ānantaryam atha-śabdāvagamyam` — prakasatman / PV p. 164 _(school: Advaita)_
  - `cite://sankara/upadesa-sahasri/I.17.7-9` — sankara / UpS I.17.7-9 _(school: Advaita)_
  - `cite://sureshvara/naishkarmya-siddhi/4.3` — sureshvara / NS 4.3 _(school: Advaita)_
  - `cite://vimuktatman/ista-siddhi/1.Anirvacanīya-khyāti-vādopasaṃhāraḥ` — vimuktatman / IṢ 1.9 _(school: Advaita)_
  - `cite://vyasatirtha/tarka-tandava/1.5` — vyasatirtha / TT 1.5 _(school: Tattva-vāda)_

#### 20. `mithya.json` — mithyā

- Aliases: `mithyātva, मिथ्या, mithyātvam, mithya, mithyā, Mithyā`.
- Current schools (5): Advaita, Viśiṣṭādvaita, Dvaita, Bhedābheda (Bhāskara), Acintya-Bhedābheda.
- Missing canonical schools to attempt: **visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **M** (hits=433).
- Citation candidates already in `citation_index.json` (18 top hits):
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-avidy` — mandana / BS 1.1 (avidyā neither sat nor asat; in the jīvas) _(school: Advaita)_
  - `cite://padmapada/pancapadika/V–VI.15–16` — padmapada / PañcP V.15–VI.16 _(school: Advaita)_
  - `cite://prakasatman/pancapadika-vivarana/brahma-vicāre kim-ānantaryam atha-śabdāvagamyam` — prakasatman / PV p. 164 _(school: Advaita)_
  - `cite://madhusudana/advaita-siddhi/1` — madhusudana /  _(school: Advaita)_
  - `cite://madhusudana/advaita-siddhi/Prathama-pariccheda, Section 1a` — madhusudana /  _(school: Advaita)_
  - `cite://madhusudana/advaita-siddhi/Prathama-pariccheda, Section 1k` — madhusudana /  _(school: Advaita)_
  - `cite://madhva/mayavada-khandana/would fail to disclose reality` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/mithyatvanumana-khandana/239, clause 1` — madhva /  _(school: Tattva-vāda)_

#### 21. `moksa.json` — mokṣa

- Aliases: `mokṣaṃ, mokṣasya, mokṣa, moksa, Mokṣa, apavarga, muktiḥ, मोक्ष…`.
- Current schools (5): Advaita, Viśiṣṭādvaita, Dvaita, Acintya-Bhedābheda, Trika / Kashmir Śaivism.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara**.
- Difficulty: **M** (hits=406).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://madhva/anuvyakhyana/1.1.13-15` — madhva / Anuvy. 1.1.13-15 _(school: Tattva-vāda)_
  - `cite://sankara/upadesa-sahasri/I.11.15` — sankara / UpS I.11.15 _(school: Advaita)_
  - `cite://sankara/upadesa-sahasri/I.17.7-9` — sankara / UpS I.17.7-9 _(school: Advaita)_
  - `cite://sureshvara/naishkarmya-siddhi/1.98-99` — sureshvara / NS 1.98-99 _(school: Advaita)_
  - `cite://vimuktatman/ista-siddhi/1.Jīvanmuktiḥ` — vimuktatman / IṢ 1.9 _(school: Advaita)_
  - `cite://dharmakirti/pramana-varttika/2.1` — dharmakirti /  _(school: Yogācāra)_
  - `cite://madhusudana/advaita-siddhi/1` — madhusudana /  _(school: Advaita)_
  - `cite://madhva/anuvyakhyana-bhasya-passages/1.1.14` — madhva /  _(school: Tattva-vāda)_

#### 22. `rasa.json` — rasa

- Aliases: `rasaḥ, Rasa, rasānubhava, rasasya, rase, rasa`.
- Current schools (3): Alaṅkāra / Abhinavagupta, Advaita (Madhusūdana), Acintya-Bhedābheda.
- Missing canonical schools to attempt: **advaita, visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **S** (hits=385).
- Citation candidates already in `citation_index.json` (18 top hits):
  - `cite://madhusudana/bhakti-rasayana/1.1` — madhusudana / BR 1.1 _(school: Advaita)_
  - `cite://nimbarka/dasa-shloki/1` — nimbarka / DaŚ 1 _(school: Dvaitādvaita)_
  - `cite://madhusudana/advaita-siddhi/Prathama-pariccheda, Section 1e` — madhusudana /  _(school: Advaita)_
  - `cite://madhusudana/bhakti-rasayana/1.1ab` — madhusudana /  _(school: Advaita)_
  - `cite://madhusudana/bhakti-rasayana/1.1 ṭīkā.10` — madhusudana /  _(school: Advaita)_
  - `cite://madhusudana/bhakti-rasayana/1.1 ṭīkā.14` — madhusudana /  _(school: Advaita)_
  - `cite://madhusudana/bhakti-rasayana/1.1 ṭīkā.16` — madhusudana /  _(school: Advaita)_
  - `cite://madhva/bhagavata-tatparya-nirnaya/1.1.4` — madhva /  _(school: Tattva-vāda)_

#### 23. `isvara.json` — Īśvara

- Aliases: `Iśvara, īśvarasya, ईश्वर, īśvaraḥ, isvara, Īśvara, īśvara, ishvara…`.
- Current schools (5): Yoga, Advaita Vedānta, Viśiṣṭādvaita, Dvaita Vedānta, Acintya-Bhedābheda.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **S** (hits=338).
- Citation candidates already in `citation_index.json` (14 top hits):
  - `cite://madhva/anuvyakhyana/1.4.111-112` — madhva / Anuvy. 1.4.111-112 _(school: Tattva-vāda)_
  - `cite://sarvajnatman/samksepa-sariraka/1.327` — sarvajnatman / SS I.327 _(school: Advaita)_
  - `cite://vidyaranya/panchadashi/1.15-16` — vidyaranya / Pañcadaśī 1.15-16 _(school: Advaita)_
  - `cite://vijnanabhiksu/yoga-varttika/1.23` — vijnanabhiksu / YV 1.23 _(school: Sāṅkhya-Yoga (synthetic))_
  - `cite://vijnanabhiksu/yoga-varttika/1.24` — vijnanabhiksu / YV 1.24 _(school: Sāṅkhya-Yoga (synthetic))_
  - `cite://yamuna/siddhi-trayam/16-18` — yamuna / ĪS 16-18 _(school: Viśiṣṭādvaita)_
  - `cite://madhva/anuvyakhyana-bhasya-passages/1.4.111` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/1.4.111` — madhva /  _(school: Tattva-vāda)_

#### 24. `sruti.json` — śruti

- Aliases: `Śruti, shruti, śruty, sruti, śrutau, śruteḥ, śruti, श्रुति`.
- Current schools (5): Pūrva-Mīmāṃsā, Advaita, Viśiṣṭādvaita, Dvaita, Acintya-Bhedābheda.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **S** (hits=336).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://madhva/anuvyakhyana/2.3.66-69` — madhva / Anuvy. 2.3.66-69 _(school: Tattva-vāda)_
  - `cite://mandana/brahma-siddhi/1.1.1--opening-prose-on-ekatva-and-m-y` — mandana / BS 1.1 (plurality as māyā-bound) _(school: Advaita)_
  - `cite://raghavendra/tantra-dipika/1.3` — raghavendra / TD 1.3, suṣuptyutkrāntyor bhedena _(school: Tattva-vāda)_
  - `cite://srinivasa/vedanta-kaustubha/1` — srinivasa / Maṅgalācaraṇa 1 _(school: Dvaitādvaita)_
  - `cite://srinivasa/vedanta-kaustubha/2.3.42` — srinivasa / BS 2.3.42 _(school: Dvaitādvaita)_
  - `cite://vijnanabhiksu/vijnanamrta-bhasya/1.1.5` — vijnanabhiksu / VĀB 1.1.5 _(school: Sāṅkhya-Yoga (synthetic))_
  - `cite://yamuna/siddhi-trayam/31-35` — yamuna / Svs 31-35 _(school: Viśiṣṭādvaita)_
  - `cite://madhusudana/advaita-siddhi/1` — madhusudana /  _(school: Advaita)_

#### 25. `guna.json` — guṇa

- Aliases: `guṇāḥ, traiguṇya, guna, गुण, guṇatraya, guṇa-atīta, guṇātīta, guṇa-traya…`.
- Current schools (6): Sāṅkhya / Yoga, Advaita, Viśiṣṭādvaita, Dvaita, Nyāya-Vaiśeṣika, Trika / Kashmir Śaivism.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga, purva-mimamsa, madhyamaka, yogacara**.
- Difficulty: **S** (hits=332).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://madhusudana/bhakti-rasayana/1.ṭīkā.1` — madhusudana / BR 1.1 ṭīkā _(school: Advaita)_
  - `cite://madhva/anuvyakhyana/2.3.66-69` — madhva / Anuvy. 2.3.66-69 _(school: Tattva-vāda)_
  - `cite://nimbarka/dasa-shloki/4` — nimbarka / DaŚ 4 _(school: Dvaitādvaita)_
  - `cite://raghavendra/tantra-dipika/1` — raghavendra / TD 1.1, adhyāya summary _(school: Tattva-vāda)_
  - `cite://vidyaranya/panchadashi/1.15-16` — vidyaranya / Pañcadaśī 1.15-16 _(school: Advaita)_
  - `cite://vyasatirtha/tarka-tandava/1.5` — vyasatirtha / TT 1.5 _(school: Tattva-vāda)_
  - `cite://jiva-gosvami/sat-sandarbha/§43` — jiva-gosvami /  _(school: Acintya-Bhedābheda)_
  - `cite://jiva-gosvami/sat-sandarbha/§45` — jiva-gosvami /  _(school: Acintya-Bhedābheda)_

#### 26. `sakti.json` — śakti

- Aliases: `śaktyā, शक्ति, Śakti, śaktiḥ, sakti, shakti, śakti, śakteḥ…`.
- Current schools (4): Mīmāṃsā and Vyākaraṇa, Trika / Kashmir Śaivism, Śākta, Acintya-Bhedābheda.
- Missing canonical schools to attempt: **advaita, visistadvaita, tattva-vada, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, madhyamaka, yogacara**.
- Difficulty: **S** (hits=319).
- Citation candidates already in `citation_index.json` (16 top hits):
  - `cite://kesava-kasmiri/krama-dipika/2.18` — kesava-kasmiri / KD 2.18 _(school: Acintya-Bhedābheda)_
  - `cite://padmapada/pancapadika/V–VI.15–16` — padmapada / PañcP V.15–VI.16 _(school: Advaita)_
  - `cite://srinivasa/vedanta-kaustubha/2.3.42` — srinivasa / BS 2.3.42 _(school: Dvaitādvaita)_
  - `cite://caitanya/shikshashtakam/2` — caitanya /  _(school: Acintya-Bhedābheda)_
  - `cite://dharmakirti/pramana-varttika/2.1` — dharmakirti /  _(school: Yogācāra)_
  - `cite://dharmakirti/pramana-varttika/2.4` — dharmakirti /  _(school: Yogācāra)_
  - `cite://jiva-gosvami/sat-sandarbha/§43` — jiva-gosvami /  _(school: Acintya-Bhedābheda)_
  - `cite://madhusudana/siddhanta-bindu/22` — madhusudana /  _(school: Advaita)_

#### 27. `visnu.json` — Viṣṇu

- Aliases: `viṣṇave, Vishnu, viṣṇoḥ, viṣṇunā, viṣṇau, विष्णु, visnu, Viṣṇu…`.
- Current schools (4): Advaita Vedānta, Viśiṣṭādvaita, Dvaita, Acintya-Bhedābheda.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **S** (hits=318).
- Citation candidates already in `citation_index.json` (25 top hits):
  - `cite://madhva/anuvyakhyana/1.1.13-15` — madhva / Anuvy. 1.1.13-15 _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/3.3.1` — madhva / Anuvy. 3.3.1 _(school: Tattva-vāda)_
  - `cite://raghavendra/tantra-dipika/1` — raghavendra / TD 1.1, adhyāya summary _(school: Tattva-vāda)_
  - `cite://madhusudana/advaita-siddhi/1` — madhusudana /  _(school: Advaita)_
  - `cite://madhva/anuvyakhyana-bhasya-passages/1.1.15` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana-bhasya-passages/3.3.1` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/anuvyakhyana/1.1.15` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/mayavada-khandana/purport: Viṣṇu's supremacy` — madhva /  _(school: Tattva-vāda)_

#### 28. `amsa.json` — aṃśa

- Aliases: `Aṃśa, aṃśa, aṃśaḥ, amśa, amsa, vibhinnamsa, अंश, aṃśasya…`.
- Current schools (5): Advaita, Viśiṣṭādvaita, Bhedābheda (Bhāskara), Dvaita, Acintya-Bhedābheda.
- Missing canonical schools to attempt: **visistadvaita, dvaitadvaita, suddhadvaita, sankhya, yoga, nyaya-vaisesika, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **S** (hits=308).
- Citation candidates already in `citation_index.json` (16 top hits):
  - `cite://gaudapada/mandukya-karika/1.Āgama-prakaraṇa.16-18` — gaudapada / MK 1.16-18 _(school: Advaita)_
  - `cite://srinivasa/vedanta-kaustubha/2.3.42` — srinivasa / BS 2.3.42 _(school: Dvaitādvaita)_
  - `cite://vallabha/anu-bhasya/2.3.43-45` — vallabha / BSB 2.3.43-45 _(school: Śuddhādvaita)_
  - `cite://gaudapada/mandukya-karika/1.17` — gaudapada /  _(school: Advaita)_
  - `cite://madhusudana/advaita-siddhi/Prathama-pariccheda, Section 1c` — madhusudana /  _(school: Advaita)_
  - `cite://madhusudana/advaita-siddhi/Prathama-pariccheda, Section 1d` — madhusudana /  _(school: Advaita)_
  - `cite://madhusudana/advaita-siddhi/Prathama-pariccheda, Section 1e` — madhusudana /  _(school: Advaita)_
  - `cite://madhusudana/advaita-siddhi/Prathama-pariccheda, Section 1g` — madhusudana /  _(school: Advaita)_

#### 29. `sabda.json` — śabda

- Aliases: `shabda, śabde, शब्द, sabda, sabda-pramana, Śabda, śabdasya, śabda-pramāṇa…`.
- Current schools (6): Nyāya, Mīmāṃsā, Advaita, Viśiṣṭādvaita, Dvaita, Buddhist Pramāṇa.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya, yoga, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **S** (hits=304).
- Citation candidates already in `citation_index.json` (13 top hits):
  - `cite://prakasatman/pancapadika-vivarana/mahāvākyasyāparokṣa-prayojakatvam` — prakasatman / PV p. 103 _(school: Advaita)_
  - `cite://vijnanabhiksu/vijnanamrta-bhasya/1.1.5` — vijnanabhiksu / VĀB 1.1.5 _(school: Sāṅkhya-Yoga (synthetic))_
  - `cite://candrakirti/madhyamakavatara/1.14` — candrakirti /  _(school: Mādhyamaka)_
  - `cite://dharmakirti/pramana-varttika/2.2` — dharmakirti /  _(school: Yogācāra)_
  - `cite://madhva/brahma-sutra-bhasya/1.1.1.13` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/brahma-sutra-bhasya/1.1.1.15` — madhva /  _(school: Tattva-vāda)_
  - `cite://nagarjuna/vigraha-vyavartani/25` — nagarjuna /  _(school: Mādhyamaka)_
  - `cite://prakasatman/pancapadika-vivarana/p. 103b` — prakasatman /  _(school: Advaita)_

#### 30. `buddhi.json` — buddhi

- Aliases: `Buddhi, buddheḥ, बुद्धि, buddhi, buddher, buddhyā, buddhau`.
- Current schools (5): Sāṅkhya / Yoga, Advaita, Viśiṣṭādvaita, Dvaita, Nyāya-Vaiśeṣika.
- Missing canonical schools to attempt: **visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga, purva-mimamsa, madhyamaka, yogacara, pratyabhijna**.
- Difficulty: **S** (hits=257).
- Citation candidates already in `citation_index.json` (9 top hits):
  - `cite://sarvajnatman/samksepa-sariraka/1.327` — sarvajnatman / SS I.327 _(school: Advaita)_
  - `cite://candrakirti/madhyamakavatara/1.1` — candrakirti /  _(school: Mādhyamaka)_
  - `cite://dharmakirti/pramana-varttika/2.5` — dharmakirti /  _(school: Yogācāra)_
  - `cite://madhva/mayavada-khandana/15.20` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/mayavada-khandana/Upaniṣad 1.3.10` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/tattva-sankhyana/9` — madhva /  _(school: Tattva-vāda)_
  - `cite://madhva/upadhi-khandana/5` — madhva /  _(school: Tattva-vāda)_
  - `cite://sankara/vivekacudamani/26` — sankara /  _(school: Advaita)_

## Wave 2+ — remaining 107 terms (deferred)

| Term | Cur | Citations available | First-pass schools to add |
|------|----:|--------------------:|---------------------------|
| `abhasa` (ābhāsa) | 2 | 5 | visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `abheda` (abheda) | 4 | 7 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `abhipraya` (abhiprāya) | 4 | 2 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `acintya` (acintya) | 2 | 4 | advaita, visistadvaita, tattva-vada, bhedabheda, dvaitadvaita … |
| `adhyasa` (adhyāsa) | 5 | 2 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `adrsta` (adṛṣṭa) | 6 | 3 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `ahankara` (ahaṅkāra) | 4 | 1 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `akhandakara-vrtti` (akhaṇḍākāra-vṛtti) | 3 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `akhyati` (akhyāti) | 3 | 0 | visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `alaya-vijnana` (ālaya-vijñāna) | 4 | 2 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `anatta` (anattā) | 4 | 4 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `anekanta-vada` (anekānta-vāda) | 4 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `anirvacaniya` (anirvacanīya) | 2 | 10 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `antahkarana` (antaḥkaraṇa) | 4 | 2 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `antaryamin` (antaryāmin) | 4 | 0 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `anubhava` (anubhava) | 4 | 2 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `anumana` (anumāna) | 5 | 4 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `anyatha-khyati` (anyathā-khyāti) | 4 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `aparoksa-jnana` (aparokṣa-jñāna) | 4 | 0 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `apoha` (apoha) | 3 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `aprthak-siddhi` (apṛthak-siddhi) | 3 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `asat` (asat) | 3 | 17 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `avibhaga` (avibhāga) | 4 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `avikrta-parinama` (avikṛta-pariṇāma) | 3 | 0 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `bhagavan` (Bhagavān) | 4 | 27 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `bhedabheda` (bhedābheda) | 4 | 0 | advaita, visistadvaita, dvaitadvaita, suddhadvaita, sankhya … |
| `catuskoti` (catuṣkoṭi) | 3 | 0 | visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `citta` (citta) | 4 | 13 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `dharmabhuta-jnana` (dharmabhūta-jñāna) | 1 | 0 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `ekayana` (eka-yāna) | 4 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `ishta-devata` (iṣṭa-devatā) | 5 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `ishta-linga` (iṣṭa-liṅga) | 2 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `jivanmukta` (jīvan-mukta) | 4 | 7 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `kaivalya` (kaivalya) | 4 | 0 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, yoga … |
| `karya` (kārya) | 6 | 15 | visistadvaita, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga … |
| `kriya` (kriyā) | 5 | 19 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `kutastha` (kūṭastha) | 3 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `laksana` (lakṣaṇā) | 4 | 2 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `lila` (līlā) | 4 | 2 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `mahavakya` (mahāvākya) | 4 | 6 | visistadvaita, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `manana` (manana) | 3 | 3 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `manas` (manas) | 5 | 25 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `mukti-yogya` (mukti-yogya) | 1 | 0 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `nididhyasana` (nididhyāsana) | 3 | 2 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `nirguna` (nirguṇa) | 4 | 0 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `nirupadhika` (nirupādhika) | 3 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `niskama-karma` (niṣkāma-karma) | 4 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `nitya-samsari` (nitya-saṃsārī) | 1 | 0 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `panca-bheda` (pañca-bheda) | 3 | 0 | visistadvaita, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `paramartha-satya` (paramārtha-satya) | 4 | 3 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `paramarthika` (pāramārthika) | 4 | 8 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `paramattha-sacca` (paramattha-sacca) | 2 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `paratantra` (paratantra) | 2 | 2 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `parinama` (pariṇāma) | 6 | 5 | visistadvaita, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga … |
| `pati-pasu-pasa` (pati-paśu-pāśa) | 4 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `paticca-samuppada` (paṭicca-samuppāda) | 4 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `prakrti-prabhasvara-citta` (prakṛti-prabhāsvara-citta) | 4 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `prakrti` (prakṛti) | 5 | 7 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, yoga … |
| `pramana-dvaya` (pramāṇa-dvaya) | 4 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `prapatti` (prapatti) | 4 | 2 | advaita, visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita … |
| `prarabdha` (prārabdha) | 4 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `pratibhasika` (prātibhāsika) | 3 | 3 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `pratitya-samutpada` (pratītya-samutpāda) | 3 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `pratyabhijna` (pratyabhijñā) | 2 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `pratyaksa` (pratyakṣa) | 5 | 6 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `prema` (prema) | 3 | 6 | advaita, visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita … |
| `rajas` (rajas) | 4 | 3 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `saccidananda` (saccidānanda) | 4 | 3 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `sadhana` (sādhana) | 4 | 17 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `saguna` (saguṇa) | 4 | 0 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `saksatkara` (sākṣātkāra) | 4 | 1 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `saksin` (sākṣin) | 4 | 4 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `samanyalaksana` (sāmānya-lakṣaṇa) | 3 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `sammuti-sacca` (sammuti-sacca) | 2 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `samsara` (saṃsāra) | 5 | 9 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `samvrti-satya` (saṃvṛti-satya) | 4 | 2 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `sarira-saririn-bhava` (śarīra-śarīrī-bhāva) | 3 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `sarvam-asti` (sarvam asti) | 3 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `satkarya-vada` (satkārya-vāda) | 6 | 0 | visistadvaita, acintya-bhedabheda, dvaitadvaita, suddhadvaita, yoga … |
| `sattva` (sattva) | 4 | 14 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `shuddha-sattva` (śuddha-sattva) | 3 | 0 | advaita, visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita … |
| `siva` (Śiva) | 4 | 3 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `sopadhika` (sopādhika) | 3 | 0 | visistadvaita, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `spanda` (spanda) | 2 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `sraddha` (śraddhā) | 4 | 4 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `sravana` (śravaṇa) | 4 | 5 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `stotra` (stotra) | 4 | 1 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `sunyata` (śūnyatā) | 4 | 13 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `svalaksana` (svalakṣaṇa) | 3 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `svatantra` (svatantra) | 3 | 5 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `svatantrya` (svātantrya) | 2 | 0 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `syad-vada` (syād-vāda) | 4 | 0 | visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `tamas` (tamas) | 4 | 8 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `tamo-yogya` (tamo-yogya) | 1 | 0 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `taratamya` (tāratamya) | 3 | 0 | advaita, visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita … |
| `tathagatagarbha` (tathāgatagarbha) | 3 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `tatparya` (tātparya) | 4 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `trisvabhava` (trisvabhāva) | 3 | 0 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `upadhi` (upādhi) | 4 | 12 | visistadvaita, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `upaya` (upāya) | 5 | 2 | visistadvaita, bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `vibhu` (vibhu) | 3 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `videhamukti` (videha-mukti) | 3 | 0 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `vijnapti-matrata` (vijñapti-mātratā) | 3 | 3 | advaita, visistadvaita, tattva-vada, bhedabheda, acintya-bhedabheda … |
| `visesa` (viśeṣa) | 3 | 18 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |
| `vivarta` (vivarta) | 5 | 0 | visistadvaita, acintya-bhedabheda, dvaitadvaita, suddhadvaita, sankhya … |
| `vyavaharika` (vyāvahārika) | 4 | 5 | visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita, suddhadvaita … |
| `vyuha` (vyūha) | 3 | 4 | advaita, visistadvaita, bhedabheda, acintya-bhedabheda, dvaitadvaita … |

## Execution mechanics

1. **Dispatch one Codex 5.4 (`reasoning=high`, `service_tier=fast`) job per Wave-1 term**, using the canonical pattern in `handoffs/dispatch_wave*.sh`. Each job receives: the term JSON, this plan's per-term spec, and an instruction to consult the citation index and full-translations corpus. It returns an updated `per_school[]` array (each entry carries 1–3 cite:// references). It **never** fabricates and writes `[NOT YET RETRIEVED]` where the on-disk corpus lacks evidence.
2. **Merge.** Main agent collects each Codex output, validates JSON, integrates into `site/data/glossary/<term>.json`. Where Codex names a passage not yet in `citation_index.json`, the corresponding key_passage from the named thinker JSON is added to the index (locus_key, IAST, English, on-disk path).
3. **Schema validation.** Every modified JSON is re-loaded; schema is preserved (`term_key`, `term_iast`, `term_devanagari`, `literal`, `aliases`, `invariant_definition`, `per_school[]`, `see_also`, `translator_note`, `last_verified_at`, `last_verified_by`).
4. **PR.** Branch `glossary/wave1-expansion-citations`; commit modified glossary JSONs + citation_index.json deltas; PR title "Glossary Wave 1 — by-school expansion + primary-source citations on top 30 terms"; do **not** auto-merge.
5. **Gap log.** Any school for which the on-disk corpus does not yield a passage is recorded in `handoffs/glossary_gaps.md` for Wave 2 acquisition.

## Constraints

- No claim without an on-disk citation. `[NOT YET RETRIEVED]` is the escape hatch.
- Tattva-vāda label for Madhva's school throughout (the rename agent is in flight; coordinate by reading the live school registry before merge).
- Citation links use the cite:// scheme; e.g. `[[ŚB 1.1.1](cite://sankara/brahma-sutra-bhasya/1.1.1)]`.
- Tone: project register. No editorializing, no comparator-framing, no AI-tells.
- `Sonnet` and `Haiku` are forbidden for sub-agent dispatch on this project (see project `CLAUDE.md`).
