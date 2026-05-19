# GRETIL — Göttingen Register of Electronic Texts in Indian Languages

**Source:** https://gretil.sub.uni-goettingen.de/gretil.html
**Per-language bulk zips:** https://gretil.sub.uni-goettingen.de/gretil/1_sanskr.zip (Sanskrit, ~282 MB compressed / 1.14 GB unpacked)
**License:** GRETIL surfaces no front-page LICENSE statement; per-text headers carry encoder attribution. De-facto policy: usage permitted with attribution to GRETIL and the original encoder; redistribution should preserve per-text headers. Contact `gretil@sub.uni-goettingen.de` for explicit licensing.

## Scope policy (revised 2026-05-19)

**Bulk-mirror approach abandoned.** Mirroring the full Sanskrit zip (3 741 files, 1.14 GB) pulled hundreds of texts the project does not engage. The corrected policy:

> Fetch only specific files that appear in `data/thinkers/*.json` `engaged_works[]`, the priority-12 acquisition list (`docs/ACQUISITION_PATHWAYS.md` §A), or the v2 expansion punch-list (`docs/audit_corpus_expansion_v2_punch_list_2026-05-19.md`).

The originally-fetched `1_sanskr.zip` and unpacked tree were deleted from `/nas` on 2026-05-19 after the over-pull was flagged. The SHA-256 fingerprint of that zip is retained in `1_sanskr.zip.sha256` for traceability; the file itself is not on disk.

## Per-file fetch index (in flight via Lane 5)

The project-relevant subset is on the order of **~30 files / ≈30 MB total**, not the full 1.14 GB. Lane 5 fetches per-URL into `data/external/gretil/files/<work_slug>.txt` (or `.htm`). Manifest entries in `data/external_ingest_manifest.json` enumerate the exact URLs.

Initial Lane 5 targets — Aṣṭādhyāyī commentary stack and the engaged-works-cross-referenced Vedānta / Mīmāṃsā / Buddhist subset:

| Slug | GRETIL path | Use |
|---|---|---|
| `patanjali_mahabhasya` | `6_sastra/1_gram/pmbhassu.htm` | Witness B against SanskritDocuments Mahābhāṣya |
| `panini_astadhyayi` | `6_sastra/1_gram/panini_u.htm` | Witness B Aṣṭādhyāyī |
| `jayaditya_vamana_kasika` | `6_sastra/1_gram/kasiku.htm` | Layer-C commentary witness |
| `bhattoji_siddhantakaumudi` | (locate via index) | Layer-C commentary witness |
| `nagesabhatta_uddyota` | (locate via index) | Layer-C commentary witness |
| `kaiyata_pradipa` | (locate via index) | Layer-C commentary witness |
| `vasubandhu_abhidharmakosa` | `4_rellit/buddh/abhkbh_u.htm` | Engaged work — Vasubandhu |
| `nagarjuna_mmk` | `4_rellit/buddh/madhg_pu.htm` | Engaged work — Nāgārjuna |
| `bhartrhari_vakyapadiya` | `6_sastra/1_gram/bhvpadeu.htm` | Engaged work — Bhartṛhari (also on SARIT) |
| `gretil_vidyaranya_anubhutiprakasha` | (locate) | v2 punch-list |

Other GRETIL files outside this slugged subset are intentionally not mirrored. If a text becomes engaged later, add a manifest entry and Lane-2-followup will fetch the specific URL.
