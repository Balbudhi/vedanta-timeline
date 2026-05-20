# GRETIL per-file mirror (Lane 5 additions)

**Policy:** per-file fetches only — NO bulk mirror. See parent `../README.md`.

**Date:** 2026-05-19
**Branch:** corpus/external-unblock-2026-05-19

## Files (31 fetched)

All slugs and SHA-256 hashes recorded in `data/external_ingest_manifest_lane5.json` under `lane5_additions`.

### Pāṇinian three-witness stack (layer A/B + partial layer C)

| File | Bytes | Witness |
|---|---|---|
| `panini_astadhyayi.htm` | 173 KB | A — Aṣṭādhyāyī sūtra (legacy HTML) |
| `panini_astadhyayi_corpustei.txt` | 168 KB | A — Aṣṭādhyāyī (corpustei TEI plaintext) |
| `patanjali_mahabhasya.htm` | 6.3 MB | B — Mahābhāṣya (legacy HTML) |
| `patanjali_mahabhasya_corpustei.txt` | 4.6 MB | B — Mahābhāṣya (corpustei plaintext) |
| `jayaditya_vamana_kasika.htm` | 2.7 MB | C — Kāśikā |
| `varadaraja_laghusiddhantakaumudi.txt` | 225 KB | C — Laghu-Siddhānta-Kaumudī (Varadarāja) |

Pradīpa (Kaiyaṭa), Uddyota (Nāgeśa), Bālamanoramā, Tattvabodhinī, and Bhaṭṭoji's full Siddhānta-Kaumudī are **not** on GRETIL — manifest-only entries point to archive.org / Sanskrit Library candidates.

### Engaged works — Buddhist / Yogācāra

| File | Bytes | Engaged thinker |
|---|---|---|
| `vasubandhu_abhidharmakosa.txt` | 79 KB | vasubandhu |
| `vasubandhu_abhidharmakosabhasya.txt` | 1.1 MB | vasubandhu |
| `vasubandhu_trimsika.txt` | 5.5 KB | vasubandhu |
| `vasubandhu_vimsatika.txt` | 20 KB | vasubandhu |
| `nagarjuna_mulamadhyamakakarika.txt` | 56 KB | nagarjuna |
| `candrakirti_prasannapada.txt` | 582 KB | candrakirti |
| `dharmakirti_pramanavarttika_karika.txt` | 139 KB | dharmakirti |
| `dharmakirti_nyayabindu.txt` | 24 KB | dharmakirti |
| `dharmakirti_hetubindu.txt` | 50 KB | dharmakirti |
| `dignaga_prajnaparamita_pindartha.txt` | 9 KB | dignaga |
| `asanga_abhidharmasamuccaya.txt` | 220 KB | asanga |
| `asanga_mahayanasutralamkara.txt` | 365 KB | asanga |

### Engaged works — Kashmir Śaivism

| File | Bytes | Engaged thinker |
|---|---|---|
| `abhinavagupta_tantraloka.txt` | 736 KB | abhinavagupta |
| `abhinavagupta_tantrasara.txt` | 125 KB | abhinavagupta |
| `abhinavagupta_ipv.txt` | 341 KB | abhinavagupta |
| `abhinavagupta_paramarthasara.txt` | 15 KB | abhinavagupta |
| `ksemaraja_pratyabhijnahrdaya.txt` | 41 KB | ksemaraja |
| `utpaladeva_isvarapratyabhijna_karika_with_vrtti.txt` | 65 KB | utpaladeva |
| `vasugupta_spandakarika.txt` | 8 KB | vasugupta / bhatta-kallata |
| `vasugupta_spandakarika_comm.txt` | 100 KB | vasugupta + comm. |

### Engaged works — Vedānta / Mīmāṃsā / Nyāya

| File | Bytes | Engaged thinker |
|---|---|---|
| `bhartrhari_vakyapadiya.txt` | 245 KB | bhartrhari |
| `jaimini_mimamsasutra.txt` | 159 KB | jaimini |
| `mandanamizra_brahmasiddhi.txt` | 299 KB | mandana-misra |
| `vacaspatimisra_bhamati.txt` | 1.1 MB | vacaspati-misra |
| `udayana_nyayakusumanjali.txt` | 259 KB | udayana |

## Two confirmed-404 entries (manifest-only, deferred to next session)

- `sa_bhartRhari-vAkyapadIya1-3.txt` — superseded by merged `sa_bhartRhari-vAkyapadIya.txt` (already fetched)
- `sa_kumArila-tantravArttika-2.txt` — re-probe next session

## Encoding

- `.htm` files: GRETIL legacy mark-up, Devanāgarī / IAST mixed, Latin-1 / UTF-8.
- `.txt` files: GRETIL `corpustei` plaintext transformations — UTF-8, IAST/SLP1 mix per encoder header at top of file.

## Total bytes

~20.3 MB across 31 GRETIL files. Compare to the 1.14 GB bulk Sanskrit zip that Lane 2 had originally pulled and that we deleted under the no-bulk-mirror rule.
