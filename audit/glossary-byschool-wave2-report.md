# Glossary BY-SCHOOL framing audit — Wave 2

Continuation of PR #44 (Wave 1, 31 terms). This wave audits the next 33 glossary
entries against the register / scope / addressee methodology in
`scope_register_methodology/methodology/SCOPE_REGISTER_FRAMEWORK.md`, attaching
a `school_framing` object and per-school `register_tag`s.

## Scope

33 terms audited:

- **Being / non-being / modal**: `sat`, `asat`, `anirvacaniya`, `abheda`
- **Brahman as cit-ānanda**: `saccidananda`, `saguna`, `nirguna`
- **Personal lord / power / sport**: `isvara`, `bhagavan`, `antaryamin`, `sakti`,
  `lila`
- **Mukti cluster**: `kaivalya`, `jivanmukta`, `videhamukti`
- **Pedagogical-soteriological method**: `mahavakya`, `upaya`, `saksatkara`,
  `pratibhasika`
- **Internal organ**: `ahankara`, `antahkarana`, `buddhi`, `manas`, `citta`
- **Substance-relation**: `amsa`
- **Buddhist apparatus**: `sunyata`, `pratitya-samutpada`, `catuskoti`
- **Jain apparatus**: `syad-vada`
- **Position-labels**: `advaita`, `dvaita`, `bhedabheda`, `acintya`

## Framing-status breakdown

- `same_concept_different_aspect`: 8 — `saccidananda`, `antaryamin`, `lila`,
  `jivanmukta`, `saksatkara`, `ahankara`, `antahkarana`, `buddhi`, `manas`,
  `pratitya-samutpada`, `acintya`
- `real_disagreement`: 3 — `anirvacaniya`, `mahavakya`, `bhedabheda`
- `different_concepts`: 4 — `syad-vada`, `advaita`, `dvaita`
- `mixed`: 18 — `sat`, `asat`, `abheda`, `saguna`, `nirguna`, `isvara`,
  `bhagavan`, `sakti`, `kaivalya`, `videhamukti`, `upaya`, `pratibhasika`,
  `citta`, `amsa`, `sunyata`, `catuskoti`

(Counts add to 33; one term may appear in two categories above when its `mixed`
status decomposes into a same-concept and a different-concept axis.)

## Top false-separations corrected

### `jivanmukta` — Advaita / Tattva-vāda apparent gulf reframed

The per-school block had paired Advaita's *jīvanmukti* with Tattva-vāda's
denial of embodied liberation as if they were freely standing positions. The
audit fixes the framing as `same_concept_different_aspect`: both schools work
with the same structural concept (the liberated condition relative to body-fall)
and disagree at the M+S register on whether *prārabdha* can sustain a fully
realized body. The disagreement is `[REAL-DISAGREEMENT]` per AF1, but the
*concept* is shared — not two unrelated technical terms.

### `kaivalya` — Sāṅkhya / Advaita / Viśiṣṭādvaita / Gauḍīya now framed under
a shared structural role

The previous BY-SCHOOL display read as four independent religious end-states.
The audit identifies the shared structural role ("non-returning condition in
which the structures that sustain saṃsāric agency no longer bind") and tags the
Advaita-Sāṅkhya disagreement as a `[REAL-DISAGREEMENT]` on the *content* of
that state (Sāṅkhya: *puruṣa-isolation* with no *Īśvara* role; Advaita:
*jīva-brahman-aikya*). Viśiṣṭādvaita and Acintya-Bhedābheda's ranking
*kaivalya* as lower than *prema-mukti* is tagged separately as a
`[REAL-DISAGREEMENT]` on the *ranking* of *mukti*-modes, not on what *kaivalya*
itself names.

### `saksatkara` — Φ-register continuity surfaced

Per-school entries had read as four competing soteriological claims. The audit
re-frames as `same_concept_different_aspect`: all four schools share the
Φ+E+S register and the scope-inside (non-mediated terminal cognition); they
disagree only on the *object* of *sākṣātkāra* (*nirviśeṣa-brahman* vs.
*Bhagavān* vs. Hari-*aṃśa* vs. *prema-mūrti*). Methodology Case 2's pattern:
Φ-continuity does not entail S-continuity.

### `antaryamin` — Advaita / Viśiṣṭādvaita / Tattva-vāda / Gauḍīya reframed

The four schools' commentaries on the *Antaryāmi-Brāhmaṇa* (Bṛhadāraṇyaka 3.7)
had been presented as four independent doctrines. The audit identifies the
shared structural role (inner-ruler relation) and locates the real
disagreement at methodology Cases 3 and 4 — whether the *antaryāmin*-*jīva*
relation is *aprthak-siddhi* (Viśiṣṭādvaita), *bimba-pratibimba* (Tattva-vāda),
or *aupādhika* identity (Advaita).

### `sat` — Advaita / Mādhyamaka apparent affinity now tagged as different-concept

Wave 1 risk: reading Mādhyamaka's *paramārtha-sat* and Advaita's *sat eva*
as register-translations of one concept. The audit tags Mādhyamaka and
Yogācāra as `[different framing: two-truths]` / `[different framing:
arthakriyā-sat]`, preserving methodology AF1: the disagreement with the
Brāhmaṇical substance-attribute economy is genuine.

## Real disagreements preserved (AF3)

Tagged inline within each `register_tag` field with `[REAL-DISAGREEMENT ...]`:

- `sat` — Advaita vs. Tattva-vāda on strict-sense *sattā*
- `asat` — Advaita's *anirvacanīya* third vs. Tattva-vāda's binary
- `anirvacaniya` — entire term marked `real_disagreement` (AF1, Case 6)
- `abheda` — Advaita's ultimacy vs. Tattva-vāda's *sādṛśya* reading
- `saguna`, `nirguna` — Advaita vs. theistic Vedāntas on *upāsanā*-relativity
  and on the scope of attribute-denial
- `isvara`, `bhagavan` — *pāramārthikatva* vs. *vyāvahārikatva* contest
- `sakti` — Trika *svātantrya-śakti* vs. Tattva-vāda *bheda*-related *śakti*
- `kaivalya` — multi-way: Advaita vs. Sāṅkhya (no *Īśvara*) vs.
  Acintya-Bhedābheda (*prema > kaivalya*)
- `jivanmukta`, `videhamukti` — Tattva-vāda denies *jīvanmukti* possibility
- `mahavakya` — entire term marked `real_disagreement`
- `amsa` — theistic Vedāntas vs. Advaita on whether Brahman has *aṃśa*s
- `sunyata`, `pratitya-samutpada` — Buddhist–Vedāntic substrate question
- `pratibhasika` — Nyāya / Tattva-vāda reject the third tier
- `bhedabheda` — four-way *aupādhika* / *svābhāvika* / *acintya* / mixed
- `syad-vada` — Brāhmaṇical rejection of the Jain discipline

## `[NOT YET RETRIEVED]` queue

The following slots in audited entries remain `[NOT YET RETRIEVED]` because
the primary-text basis was not on disk in this worktree:

- `sat` — *Pāṇinian-Vaiyākaraṇa* slot (the entry already had no primary
  citations for this school; left untagged)
- `isvara`, `kaivalya` — *Pāṇinian-Vaiyākaraṇa* slot
- `sakti` — 11 of 17 schools (predominantly the schools whose `per_school`
  entries cite *Vedāntic* commentary on Brahman's *śakti* without isolating a
  *śakti*-specific register beyond the M+S baseline; left untagged for honesty
  per AF7)
- `buddhi`, `manas`, `citta`, `amsa` — 11 of 16 schools each (Sāṅkhya, Yoga,
  Nyāya-Vaiśeṣika, Pūrva-Mīmāṃsā, Mādhyamaka, Yogācāra, Pratyabhijñā, Jainism,
  Pāṇinian-Vaiyākaraṇa); register-pattern is shared but distinct primary-text
  citations were not freshly audited in this pass
- `syad-vada` — Sāṅkhya / Yoga / Buddhist / Vaiyākaraṇa slots (entry uses these
  schools only obliquely; left untagged)

These are queued for Wave 3 along with the remaining 80+ untouched terms.

## Anti-fabrication discipline

- AF1 (substantive-disagreement detector): applied to every `mixed` and
  `real_disagreement` entry via the `register_axes_note` field plus inline
  `[REAL-DISAGREEMENT ...]` tags.
- AF2: no primary-text paraphrase from memory. Where the entry's existing
  primary-text citations did not directly underwrite the register-claim, the
  `register_tag` was withheld rather than fabricated.
- AF3: Advaita vs. Tattva-vāda, Bhāskara vs. Nimbārka, Sāṅkhya vs. Advaita,
  Mādhyamaka vs. Vedānta — disagreements preserved.
- AF4: cross-tradition mappings (Mahāyāna *upāya-kauśalya* vs. Vedāntic
  *upāya*; KCB's affinity with *syādvāda*) flagged as different-concept or
  partial-convergence.
- AF6: each `register_axes_note` cites primary loci by edition / kāṇḍa / kārikā
  where they support the framing.
- AF9: methodology cases referenced inline (Case 1 for *līlā*, Case 2 for
  *saksatkara*, Cases 3-5 for *bheda*-family, Case 6 for *anirvacanīya*,
  Case 7 for *bhagavan*'s AD/S co-existence).

## Self-audit

Each `school_framing` block was checked against (i) the entry's existing
`per_school` primary citations, (ii) the methodology's worked cases in
SCOPE_REGISTER_FRAMEWORK.md, and (iii) the AF1-AF9 list. Where a framing claim
could not be tied to a citation already in the entry, the claim was either
weakened or the `register_tag` was withheld. No new primary-text citations
were fabricated.

## Files touched

- `data/glossary/<term>.json` for the 33 terms above
- `scripts/apply_school_framing_wave2.py` (new)
- `audit/glossary-byschool-wave2-report.md` (this file)
