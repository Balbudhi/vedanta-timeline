# The whole Bhagavad-Gītā, word by word, with audio: goal, decisions, process

Owner instructions (2026-11-07 and 2026-11-08): translate all 700 verses to
[`SANSKRIT_TRANSLATION_STANDARD.md`](SANSKRIT_TRANSLATION_STANDARD.md) by agents
now; **no commentary layer**; **audio for every verse, synced and timed**, with the
existing tap-a-word and tap-a-verse functionality; **one consistent term rule** with
its logic stated; **full use of English** through the dictionary-discovery design
from the Bhakti engine plan (uncommon attested senses, the Joycean step). The owner's
aesthetic judgement is the final word. Measured starting state and evidence: prakriya
`docs/research/DEEP_AUDIT_20261107.md` and `research/audit-20261107/`.

**What this plan is (amended 2026-11-08).** The standard is the single authority for
rules; `data/glossary/term_policy.json` is its §8 table (for the Gītā, the Gītā
lexicon). This plan carries the Gītā project's scope, stages, jobs, gates and
measured numbers, and does not restate rules: where it once did (term rule, English
rules, fork rules, secondaries), those rules now live in the standard and this plan
points to them. The process sections (§3, §6–§8, §10, §13.4, §14) were replaced on
2026-11-08 after the chapter-12 pilot audit (`GITA_CH12_PIPELINE_AUDIT.md`), the
precedents survey (`TRANSLATION_PRECEDENTS_SURVEY.md`) and the owner's direction on
the pipeline architecture (§7). History is kept in §16–§17; lessons in §18.

## 1. Goal

A public reader `gita/chN/` for N = 1..18: for each verse the BORI mūla in
Devanāgarī, the IAST pada-pāṭha with a card on every word (root with gaṇa and
pada, pratyaya, morphology, compound with vigraha, kāraka, complete morpheme parts,
sandhi, the meaning layer of standard §6.4 with traditional voices, other readings,
glossary link), the literal slotted English, and a recitation synced at verse level
(tap a verse to hear it; the playing verse is highlighted). Every grammatical claim is
cited to a locus in the prakriya source library or stated as not located. Every
content lemma-sense is decided once for the whole Gītā in the lexicon, and every
English word choice is made from dictionary definitions with a plain and a rich
candidate recorded (standard §7.17). Our English comes from the Sanskrit and the
dictionaries, not from other translations (standard §9). Nothing is published that
failed a validator; publication is provisional until the owner's taste review.

## 2. Decisions

### 2.1 Decided by the lead (override at any time)

| # | Decision | Logic |
| --- | --- | --- |
| L1 | **No commentary rendering.** Commentaries are evidence for pada division, sense and the meaning layer (their per-word glosses appear as named meaning lines on the cards); they are not rendered word by word and the reader shows mūla only. Recorded in standard §2. | Owner instruction. Removes the Śaṅkara ch. 18 and Madhva witness blockers and about 90% of the card volume. |
| L2 | **Term rule is sense-constant** (standard §7.7, §8). Each (lemma, sense) is decided once in the table and machine-checked on every occurrence. | We translate meanings, not strings; 2.47 *karmaṇi* is the act, not the law of action. |
| L3 | **Devanāgarī mūla** is a deterministic transliteration of the BORI IAST witness, labelled as such, collated against a second Devanāgarī witness with every difference recorded; BORI remains the text. | The standard forbids *silent* script generation; a labelled lossless transliteration plus collation satisfies it. |
| L4 | **Audio: one lawful complete recitation, per-chapter files, verse-level manifest, two-method corroboration, owner spot-listening** (§5). Word timestamps stored provisionally, not shown. | The audio standard allows verse-level only. |
| L5 | **English discovery is mandatory per content word**, with a plain and a rich candidate (standard §7.17; process §6). | Owner instruction: English is rich; the pilot used the plainest word almost everywhere. |
| L6 | **Producers and reviewers are agents** (Claude Code or Codex, §7.9); no DeepSeek, TypeSafe or Gemini in the default route; no paid API spend required. | Owner asked for agents now; the prakriya rule against invoking client subscriptions concerns the autobuild product. |
| L7 | **krodha → anger**, and every other emotion word translates (standard §8.4). The row enters the lexicon in stage B; `check_gita_terms.js`'s hard-coded table that preserves *krodha* is being retired by its owner; earlier readers are migrated (G1.5). | The preserve test fails: English carries it. |
| L8 | **Pilot was chapter 12**; its revised lines (term policy `2-ch12-meaning`) are the calibration set for line style (O5). The remaining chapters run through stages A–E (§7) together. | Lexicon-first makes chapter order irrelevant to consistency. |
| L9 | Review records follow the Yogavāsiṣṭha-Dāma pattern under `internal/sanskrit_reviews/gita/`. Fixes are made by the same producer, resumed with the review; re-reviews by the same reviewer, resumed with the diff. The lead does not edit producer files. | Pilot: fresh fix agents spent 12.5–18.5 min re-reading each (audit P1). |
| L10 | **One authority**: the standard governs; `term_policy.json` is its §8 table; `GITA_CARD_MEANING_SCHEMA.md` is folded into standard §2–§3; this plan carries process only. | Survey §1.10: 27 contradictions between documents, checkers and data. |
| L11 | **Meaning is decided before production, lexicon first** (§7.4): each content lemma-sense once across the Gītā, from a dossier using the whole source library (standard §6.4), with an independent lexicon reviewer per batch. | Pilot: 12 of 53 rows changed mid-run; 59% of findings came from late decisions, tools and hygiene (audit §1.1). |
| L12 | **One review pass** per shard covering grammar, form in the line, meaning against the lexicon, readability, policy fit, forks and the public surface, with the blind check against other translations last (standard §5.1, §9). | The pilot's review never checked meaning or readability (audit §3). |
| L13 | **dhyāna → "meditation"** (translate), replacing the seed table's "preserve". | Noun and participle must pair (12.6 *dhyāyantaḥ*, 12.12 *dhyānam*); survey X4. |
| L14 | **Other translations are out of production** (standard §9): not read in stages A–C; used only in stage D as a blind check. Files that quote them are private and git-ignored. The audit's proposal D-4 to commit review records is not adopted. | Owner direction 2026-11-08: our English must come from the Sanskrit and the dictionaries and be richer and freer than the published translations. The repository is public. |
| L15 | **Deploy by script from a clean worktree of `origin/main`** carrying only the chapter's scope (§7.7). The owner's instruction to run the pipeline authorises provisional publication of each chapter that passes the gate (§8). | The working tree is shared with other agents (AGENTS.md rules 1–2); the pilot was never deployed (audit P7). |
| L16 | **Line-style rules** standard §7.8–§7.17 (mood, non-finite forms, epithets, multi-index slots, preserved terms in English syntax, sentences across verses, elision, function words, readability and disfavoured devices, register). | Audit §1.2 D3–D6, D14 and §5.1. |
| L17 | **Public-text rule** (standard §3.4): no pipeline vocabulary in any public field; the builder refuses. | Pilot: 23 public fields carried process jargon (audit T21). |
| L18 | **Orchestrator-neutral pipeline** (§7.9): a disk job queue plus the runbook (§7.10), so Claude Code and Codex execute it identically from one instruction. | Owner direction 2026-11-08. |
| L19 | **Chapter-12 decisions from the meaning reviews** (term policy `2-ch12-meaning`, `internal/sanskrit_reviews/gita/ch12/APPLY_DECISIONS.md`): upa-√ās "attend upon", pari-upa-√ās "attend wholly upon"; *atha* + indicative protasis "If …, then …" (12.9–12.11); *kūṭastha* preserved; *duḥkha* paired with *sukha* "pain"; saṃ-ni-√as with a locative of the person "laying down … in"; *ananya* "undivided"; ud-√vij + ablative "shrink from". Decided; the owner may revise at the taste review. | Four meaning reviews, consolidated by the lead. |

### 2.2 The owner's decisions (open)

| # | Decision | Needed by |
| --- | --- | --- |
| O1 | Confirm the sense-constant term rule (L2) or demand string-constant. | Lexicon v3 (stage B) |
| O2 | Choose the recitation source (§5.1), record it, or commission a reciter with a written release. | Audio for publication |
| O3 | Read the revised chapter 12 on the site (the first taste review). | Before the first remaining chapter is published |
| O4 | Repository hygiene go/no-go (prakriya audit §11) and the stale prompt hook; not blocking. | Any time |
| O5 | Line style (standard §7.8–§7.17), once, with chapter 12 as the calibration set. | With O3 |
| O6 | The pilot term rows still marked `review: pilot` in `2-ch12-meaning`: *cetas* "awareness", *dhyāna* "meditation", *duḥkha* "sorrow" / *sukha* "pleasure" (including adverbial *sukham*: plan once said "at ease", the row forbids "ease"; survey X5), the verb of *dveṣa* "bears no dveṣa" (site-wide), *sama* "the same", *śubha/aśubha* "the fair and the foul", *amṛta* "deathless" (state) beside "nectar" (noun). | Taste review; non-blocking |
| O7 | "the everywhere-going" (formation) vs "all-pervading" (attested; MW's gloss) for *sarvatraga* (12.3). | Taste review |
| O8 | Taste items among the rich choices: "upbearer" (12.7, a recorded formation), "infixed" (12.14, plain "fixed"), "loosed" (12.15, plain "freed"), "weigh alike" (12.19). | Taste review |
| O9 | The *karma-phala* rendering across chapter 5 ("the fruit of karma", 5.12, 5.14) and chapter 12 ("the fruit of action", 12.11–12). | Before ch5 migration (G1.5) |
| O10 | Whether cards show the `synthesis` meaning category publicly (standard §2, §6.3). | Before the first card with a synthesis line is published |
| O11 | Adopting any of Sri Aurobindo's register devices (capitalised principles) in lines (standard §7.17). | With O5 |
| O12 | ~~Two chapter-12 lines vs the non-finite rule~~ — resolved by the lead 2026-11-08: 12.6 → "having laid down … in me"; 12.11 "leaning on" kept under the stative-kta clause added to standard §7.9. | closed |

## 3. Readiness: what must be true before stages run (amended 2026-11-08)

1. **Lookup layer** in prakriya (`scripts/lookup/lookup.py`: sūtra, dhātu, kośa,
   amara, uṇādi, liṅga, gita, cheda, english, define) — built in the pilot. To add
   (audit §5.5): `define` with lemmatiser and phrase index; Kāśikā spans with a
   self-test; adhikāras in force; `gloss` (commentators' per-word glosses) and
   `concord` (Gītā occurrences and site renderings); the reviewed chain table.
2. **English stack** of seven sources indexed (Webster 1913, GCIDE, Wiktionary/kaikki,
   OEWN 2025, Century, Roget, Moby; the pilot index has the first two plus WordNet
   3.1); "not attested" is concluded only after all seven.
3. **Meaning-source hits by code** (standard §6.4): Dhātuvṛttis (Mādhavīya,
   Kṣīrataraṅgiṇī, Dhātupradīpa, Daiva-Puruṣakāra), Nirukta and Nighaṇṭu, kośas
   (Amarakośa with Amaraviveka and Kṣīrasvāmin, Halāyudha, Vaijayantī, Yādavakośa),
   Śabdakalpadruma and Vācaspatyam, located per lemma in the packets.
4. **Stage A packets** for all 700 verses and the Gītā-wide lemma inventory built and
   validated (§7.3).
5. **Validators**: slot and term checkers discover `gita/*/verses.js`, read only the
   table and fail on an unresolved key; the builder's fail-closed checks of audit §5.7
   (B1–B18) including the public-text rule and the render contract; markup test green;
   `run_checks.sh` passes.
6. **Reader renders** every public field the gate depends on — `meaning` and fork
   `display` (standard §2) — verified by the markup test on a chapter's first open
   fork. The presentation change belongs to the UI owner under `UI_DESIGN_STANDARD.md`.
7. **Job queue and runbook** (§7.9–§7.10) with a validator per job type.
8. **Briefs** instantiated from `docs/gita_briefs/` (LEXICON, PRODUCER, REVIEW).
9. **Private store**: every path a job writes that quotes another translation is
   git-ignored (`git check-ignore`), standard §9.
10. **Mūla witnesses**: BORI registered; Devanāgarī transliteration with its collation
    report (L3).
11. **Audio**: source acquired with licence text (O2); alignment, corroboration and
    calibration per §5; owner listening sample generated.

## 4. The term rule (moved)

The rule — three tests, sense-constancy, the disputed-referent precedent, the table's
structure — is standard §7.7 and §8. The decisions are rows of `term_policy.json`;
from stage B the table is the Gītā lexicon (v3).

**Seed decisions of the pilot (history, corrected 2026-11-08).** Preserve: yoga,
dharma (incl. svadharma), karma (law of action), guṇa, sattva, rajas, tamas, prakṛti,
puruṣa, buddhi, manas, indriya, ahaṃkāra, prajñā, kāma, rāga, dveṣa, tṛṣṇā, rasa,
samādhi, saṃsāra, māyā, yajña, tapas, bhakti and bhakta; established Brahman, the
self. Translate: krodha → anger, bhaya → fear, moha → delusion, duḥkha → sorrow,
sukha → pleasure, saṅga → clinging, jñāna → knowledge, mokṣa → liberation, śānti →
peace, pāpa → sin, puṇya → merit, saṃnyāsa → renunciation, tyāga → relinquishment,
kṣetra → field, avyakta → the unmanifest, akṣara → the imperishable, īśvara → the
Lord, phala → fruit, hetu → cause, śaraṇa → refuge, śraddhā → faith, siddhi →
perfection, deva → god, jīva → living being, śoka → grief, karma in the plain-act
sense → action, and **dhyāna → meditation** (L13; the seed list had it preserved).
Still to decide in the lexicon: vijñāna, kṣetrajña, the plain "joining" sense of
yoga, *nirvāṇa* (five occurrences — 2.72, 5.24, 5.25, 5.26, 6.15 — with three
renderings in the earlier readers; the seed text's "one occurrence" was wrong), and
the further rows the survey lists (§3 there).

## 5. Audio

### 5.1 Source

One complete Sanskrit recitation of all 700 verses that may lawfully be hosted on
the public site with attribution. The research (prakriya
`research/audit-20261107/audio-resources.md`, about 2,350 archive.org Gītā audio
items scanned) found three lawful candidates and rejected the rest (no licence, or
uploader not the rights holder, e.g. the ISKCON 2006 recording relabelled CC):

| Candidate | What | Rights today | Use |
| --- | --- | --- | --- |
| A. Dr Kisan Maharaj Sakhare, Sadhakashram Alandi (archive.org `bhagavad-gita-complete-1-to-18-by-sakhare-maharaj`) | 18 chapter MP3s, 224 min, one-pass pārāyaṇa, about 19 s per verse; ch. 15 also as per-verse clips | Public Domain Mark set by the ashram's own uploader (a label, not a waiver) | best quality fit; ask the ashram for CC0 or CC BY 4.0 in writing before publishing |
| B. P R Iyer (archive.org `bhagavad-gita_pri`) | 18 chapters, 177 min, self-uploaded | CC BY-NC-ND 4.0 | lawful now for a re-encoded whole-chapter file plus an external timing manifest; no per-verse clipping |
| C. Samskrita Samvadah (archive.org `geeta_parayanam`) | one 168 min file | Public Domain Mark | fallback; quality unverified |

Wikimedia Commons has only chapters 2 and 3 (CC BY-SA 4.0); LibriVox has no Sanskrit
Gītā; Gita Supersite's Swami Brahmananda audio is Chinmaya Mission Trust property
used by permission for that site only; Vedabase audio is BBT all-rights-reserved.
Commissioning a reciter with a CC BY release costs roughly $500–1,500 for the three
to four finished hours; self-recording gives CC0.

Lead decision for the pilot: run chapter 12 on **B** (lawful immediately) while the
ashram is asked for a CC licence on **A**; the owner chooses the final source (O2).
Chanting must be plain pārāyaṇa (no music, no repeats). Rights basis, performer,
edition and URL go in the manifest and the source ledger
(`AUDIO_ALIGNMENT_STANDARD.md`).

### 5.2 Alignment method (local, free, deterministic)

1. Normalise the audio to 16 kHz mono WAV per chapter (ffmpeg).
2. Transcript = the BORI IAST of the chapter in verse order, romanised to the
   aligner's alphabet (uroman or a fixed IAST→ASCII table), one token per pada word,
   with verse and pāda boundaries recorded by token index. Speaker lines (*arjuna
   uvāca*) included only if chanted.
3. Primary aligner: `torchaudio.pipelines.MMS_FA` with `uroman` romanisation
   (installed in `/Users/eeshan/Dev/read-along-video/.venv`, torch 2.8, MPS
   available; model weights CC BY-NC 4.0, acceptable for this non-commercial site),
   giving a timestamp per token. Verse start = first token start; verse end = last
   token end. The whisperx route is unusable here: it has no Sanskrit alignment model.
4. Second aligner sharing no acoustic model: the Sanskrit wav2vec2 CTC model
   `Harveenchadha/vakyansh-wav2vec2-sanskrit-sam-60` (native Devanāgarī vocabulary)
   through `torchaudio.functional.forced_align`, or `ctc-forced-aligner` from GitHub
   (`--language san --romanize`). Both estimates are snapped to the nearest Silero
   VAD speech gap. A verse boundary is *corroborated* when the two aligners land in
   the same gap within 0.25 s, and the verse duration passes a syllable-count sanity
   check. Calibrate on the Sakhare chapter 15 per-verse clips and the Commons
   chapter 2–3 files, which give known boundaries.
5. Verification: the owner listens to every disagreement and a 10% random sample per
   chapter against the displayed text; the manifest is marked `verified` only then,
   otherwise `provisional`. Chant introductions, pauses, elongated finals and
   repeated verses are corrected by hand. *(Added 2026-11-08.)* The aligner writes the
   listening sample (10% of verses, seeded) and every disagreement into the manifest
   as `owner_listening: [{locus, reason}]`, and step 4's calibration result per aligner
   as `calibration: {aligner, boundary_error_s, clips}`. Neither existed for chapter 12
   (audit T20).
6. Output per chapter: `gita/chN/audio.js` as in `gita/sthitaprajna/audio.js`
   (`src, reciter, attribution, licence, timing_status, verses[{locus,start,end}]`),
   the chapter MP3 encoded **CBR 64 kbps mono with a Xing header** (VBR seeks are
   inaccurate in Chrome and Firefox; about 107 MB for the whole Gītā), an optional
   WebVTT copy of the manifest, and a private `timings-raw.json` with the per-token
   timestamps kept for a future verified word layer.
7. Reader: the existing `GitaReader` audio controls (tap verse to seek and play,
   active-verse highlight, global play/pause, keyboard seeking) are reused unchanged;
   no word highlighting until a verified word layer exists.

Scripts live in vedanta-timeline `scripts/audio/` and may import the
read-along-video alignment code; they document model, version and licence in the
manifest. Audio jobs run from stage A in parallel with everything else.

## 6. English discovery: who does it, with what (amended 2026-11-08)

The rules (plain and rich candidate, formations, worked examples, register) are
standard §7.17. The process:

1. **Where.** Lemmas in the lexicon get their candidates in stage B, once for the
   Gītā: the lexicon agent writes the sense description per sense from the Sanskrit
   evidence, retrieves candidates, and records `plain` and `rich` with the choice and
   the English forms per grammatical category. Content words with no lexicon row (the
   lead's scope rule, §7.4) get the same record from the producer in stage C.
2. **Retrieval.** `lookup.py english "<sense description>"` and with the root image;
   then `lookup.py define WORD` for every candidate cited, so the definition and locus
   are the headword's own entry. A miss in the indexed sources means "consult the rest
   of the stack" (§3 item 2), not "coin a word"; until all seven sources are indexed a
   formation record states which sources were searched.
3. **Not from translations.** Candidates come from the dictionaries and the Sanskrit,
   never from other translations (standard §9). Secondaries enter only in stage D.
4. **Memory.** Accepted decisions are lexicon rows; producers reuse them and file a row
   proposal for an occurrence that does not fit.

The deterministic parts (retrieval, definition expansion, record validation) are code;
the judgement is the agent's and is checked by the reviewer against the definitions.

## 7. The pipeline (replaced 2026-11-08: owner direction on the architecture)

### 7.1 Stages

| Stage | Who | Output | Gate to next stage |
| --- | --- | --- | --- |
| **A. Packets and inventory** | code, all 700 verses at once | per-verse packets; Gītā-wide lemma inventory; lexicon jobs; shard plan | packet validator passes for every verse |
| **B. Lexicon first** | lexicon agents in batches; one independent lexicon reviewer per batch; merge by code | the Gītā lexicon = `term_policy.json` v3, frozen by content hash | every batch reviewed with no open S1; merged table validates |
| **C. Verse production** | one producer per chapter shard; expansion by code | analysis records → cited cards, lines, forks, meaning selections | shard passes the builder's check mode with no ERROR |
| **D. Review** | one reviewer per shard (single pass, blind check last); fixes by the same producer resumed; diff re-review by the same reviewer | accepted shard at a recorded hash | `complete: true`, no open S1 |
| **E. Build, validate, deploy** | code, per chapter | `gita/chN/` published, provisional | §8 gate; live files verified |
| **Taste review** | owner, after publication | lexicon edits, line-style amendments | mechanical sweep of affected occurrences → diff re-review → rebuild |

Audio (§5) runs from stage A in parallel. Chapters do not wait for each other after
stage B: each shard moves through C → D → E as soon as it is ready.

### 7.2 Principles

1. Code does everything exact: segmentation candidates, lookups, citation chains,
   loci, citation chases, policy matching, consistency, counts, public-surface checks.
   Agents assert analyses and choose meanings; code expands each assertion into a
   cited card wherever the expansion script exists.
2. Meaning is decided once per lemma-sense, for the whole Gītā, before verse
   production (stage B). Producers then spend their judgement on construal, word
   order, readability and the card's meaning selections.
3. Production depends on no other translation; the secondaries enter only in the
   stage-D blind check (standard §9).
4. One review pass checks grammar, meaning and readability together. Fixes go back to
   the same producer, resumed; nobody else edits a producer's file.
5. The owner's taste review follows provisional publication and flows back as lexicon
   edits plus a mechanical sweep; the owner never meets a decision made silently.

### 7.3 Stage A: packets and inventory (code)

`scripts/gita/build_all_packets.py` builds, for every verse: the BORI IAST and
Devanāgarī (with collation); pada candidates with sandhi loci (Vidyut `cheda` as a
labelled hint); per candidate pada the Dhātupāṭha records of root candidates, the
derivation chains auto-cited from the reviewed chain table, kośa entries (MW, Apte,
Śabdakalpadruma, Vācaspatyam, Amarakośa, Halāyudha, Vaijayantī, Yādavakośa),
Dhātuvṛtti entries for the root (Mādhavīya, Kṣīrataraṅgiṇī, Dhātupradīpa,
Daiva-Puruṣakāra), Nirukta/Nighaṇṭu hits, the commentators' per-word glosses (every
commentary on disk: Śaṅkara, Rāmānuja, Madhva and the `gita_gita_sanskrit` authors),
the concordance of the lemma's Gītā occurrences, and the renderings in published site
readers. The secondaries are kept in a separate private file read only by stage-D jobs.

For the Gītā as a whole: the lemma inventory (lemma, sense candidates, every
occurrence, existing row or none, prior site renderings), the shard plan (sentence
units, balanced to about 60 cards; chapter 2 yields 14–15 shards), and the lexicon job
list (`scripts/gita/build_lexicon_jobs.py`). Validator: every verse has a packet; the
pada candidates rejoin to the BORI saṃhitā exactly; every inventory occurrence
resolves to a packet locus.

### 7.4 Stage B: the lexicon (lexicon first)

This is where richness and consistency are made. A **lexicon job** is a batch of
about eight lemmas; the agent follows `docs/gita_briefs/LEXICON_BRIEF.md` and writes,
per lemma, a dossier across **all** its Gītā occurrences: senses per occurrence; the
root and its image (Dhātupāṭha, Dhātuvṛttis); nirvacanas (Nirukta, commentators);
synonym fields (kośas, Śabdakalpadruma, Vācaspatyam); the commentators' glosses per
occurrence; the Gītā's own usage; the three tests (standard §8.1–§8.2); plain, rich
and, where admissible, formation candidates with `define` evidence; English forms per
grammatical category; distinctness against reserved English; the draft card meaning
lines; and a proposed row. No other translation is read.

A **lexicon-review job** (same brief, reviewer part) checks each batch independently:
the senses against the sources, the tests, the candidates against their definitions,
the formation rule, distinctness, and readability of the forms in a sample line. A
**merge job** (code) folds reviewed rows into `term_policy.json` v3 with status
`lexicon-reviewed`, records the content hash, and rejects reserved-English
collisions.

Scope (proposed default; the lead fixes it when the inventory is measured): every
content lemma with two or more Gītā occurrences, every lemma that already has a row or
a prior site rendering, and every system term regardless of count. Hapax content words
are decided by the producer with a full wording record and enter the lexicon through
the stage-D review. Pilot rows (`2-ch12-meaning`) are migrated, not re-decided, unless
the dossier finds a defect.

### 7.5 Stage C: verse production

A **produce job** is one shard. The producer follows
`docs/gita_briefs/VERSE_BRIEF.md`: it writes a compact analysis record per word
(pada, root id, affixes, compound and vigraha, kāraka, `term` from the lexicon, sense,
the English and why), the slotted line (standard §7), the verse `sense`, the forks
with `words` and `display`, and the card's `meaning` selected from the lexicon and the
packet's glosses for this verse. Code expands the record into cited cards (an
**expand job**); until the expansion script exists, the producer writes full cards
with evidence as in the pilot. The producer runs the builder's check mode for its
shard and hands off only when it prints no ERROR. It never reads other translations.

### 7.6 Stage D: one review pass, fixes, diff re-review

A **review job** freezes the shard (sha256) and follows
`docs/gita_briefs/REVIEW_BRIEF.md`: the eight checks of standard §5.1, starting from the
builder report (no hand-chasing of loci the builder verified), with the blind check
against the secondaries last. Findings carry severities S1–S3 and may include row
proposals, which the lead routes to the lexicon (a lexicon edit plus sweep), never into
the shard silently.

A **fix job** goes to the same producer, resumed with the finding IDs (§7.9 on how a
queue resumes an agent). A **rereview job** goes to the same reviewer with the diff
between the reviewed and revised shard: it checks every changed field against its
finding and spot-recomputes two verses; any regression or new S1 keeps
`complete: false`.

### 7.7 Stage E: build, validate, deploy (code)

The fail-closed builder emits `gita/chN/verses.js`, `index.html` and registrations;
`scripts/run_checks.sh` runs every validator. Deploy (`scripts/deploy_gita_chapter.sh N`,
audit §5.8) never pulls, rebases or stashes in the shared working tree:

1. build and check in the working tree;
2. `git fetch origin main`; `git worktree add --detach <tmp> origin/main`;
3. copy only the chapter's own files (`gita/chN/verses.js`, `index.html`, `audio.js`,
   the MP3), the table `data/glossary/term_policy.json` and any glossary file the
   chapter adds; apply the registration step (`assets/app.js`,
   `data/articles/manifest.json`) to origin/main's copies;
4. run the checks in the worktree;
5. stage by path only; refuse any staged path outside the expected list
   (`git diff --cached --name-only`);
6. commit (`Gītā N: reader from reviewed shards (policy <hash>)`) and
   `git push origin HEAD:main` — never force;
7. verify HTTP 200 on the live files (`https://vedanta.eeshan.xyz/gita/chN/verses.js`,
   the chapter page, `audio.js`, the MP3) and that the live `verses.js` equals the
   built file; remove the worktree.

`apparatus.json` is not published unless the reader loads it and it holds no text from
another translation. The chapter is marked `provisional` in its manifest entry until
the owner's taste review.

### 7.8 The owner's taste review

After a chapter is published (provisional), the owner reads it on the site. A change
to a row becomes a lexicon edit (status `owner-decided`); code lists every affected
occurrence across all chapters, applies the mechanical sweep, and the affected shards
get a diff re-review and rebuild. A line-style change amends the standard (§7.8–§7.17)
and is swept the same way. Chapter 12 is the first taste review (O3, O5).

### 7.9 The job queue (orchestrator-neutral)

The pipeline lives in the repository as a disk job queue, so that Claude Code (through
its Workflow tool) and OpenAI Codex execute it identically from one instruction: "run
the Gītā pipeline". A job record:

```jsonc
{ "id": "lexicon-b017", "type": "lexicon",            // job type, §7.10
  "brief": "docs/gita_briefs/LEXICON_BRIEF.md",       // judgement jobs only; null for scripts
  "command": null,                                     // mechanical jobs: the script to run
  "inputs": ["internal/…/inventory.json#b017", "…"],
  "output": "internal/sanskrit_reviews/gita/lexicon/b017.json",
  "validator": "python3 scripts/gita/validate_lexicon.py internal/…/b017.json",
  "deps": ["packets-all"],
  "status": "pending",                                 // pending | ready | claimed | submitted | done | failed
  "agent_ref": null,                                   // the agent/session that produced it, for resumed fixes
  "attempts": 0, "notes": [] }
```

Rules: every judgement job is self-contained (its brief plus its inputs suffice);
every mechanical step is a script; every job has a validator, and a job becomes `done`
only when its validator passes. A fix or re-review job names its parent's `agent_ref`;
an orchestrator that can resume that agent does so (Claude Code: SendMessage to the
agent; Codex: resume the session). If it cannot, a fresh agent receives the producer's
own output, its `handoff` notes and the findings — the pilot's costlier fallback.
Outputs that quote other translations go to git-ignored paths (standard §9).

### 7.10 RUNBOOK (stub; the lead is building the scripts)

Scripts under `scripts/gita/` (names as the lead has set them; validators to be named
in the queue records):

| Script | Does |
| --- | --- |
| `build_all_packets.py` | stage A: all verse packets, the lemma inventory, the shard plan |
| `build_lexicon_jobs.py` | stage A→B: lexicon and lexicon-review jobs from the inventory |
| `queue.py next` | returns the next `ready` job (deps done) and marks it `claimed` |
| `queue.py submit JOB` | runs the job's validator; `done` on pass, `failed` with the validator's output otherwise |
| `queue.py status` | counts by stage, type and status; failed jobs with reasons |
| validators | one per job type (packet, lexicon batch, merged table, analysis/shard check, review record, build, deploy) |

Job types: `packets` (script) · `lexicon` (LEXICON_BRIEF) · `lexicon-review`
(LEXICON_BRIEF, reviewer part) · `lexicon-merge` (script) · `produce` (VERSE_BRIEF)
· `expand` (script) · `review` (REVIEW_BRIEF) · `fix` (VERSE_BRIEF, fix part) ·
`rereview` (REVIEW_BRIEF, diff part) · `build` (script) · `deploy` (script) · `sweep`
(script, after a lexicon edit) · `audio-align` (script) · `audio-listen` (owner).

The loop, for either orchestrator:

1. `python3 scripts/gita/queue.py next` → a job, or "none ready", or "blocked".
2. Mechanical job: run `command`. Judgement job: start an agent with the instruction
   "Follow `<brief>`; your job record is `<job JSON>`", up to the concurrency limit.
3. `python3 scripts/gita/queue.py submit <id>`. On `failed`, give the same agent the
   validator output once; a second failure goes to the lead.
4. Repeat until `status` shows nothing ready. Stop and report on: a failed job after
   retry; a quality halt (§10 targets missed on a chapter); a missing licence (audio);
   any action outside the queue's paths.

Instantiating briefs: each brief is a template; the job record supplies `{{CH}}`,
`{{RANGE}}`, input and output paths, and the table hash.

## 8. Gate per chapter (amended 2026-11-08)

`validate_gita_slots.js` OK; `check_gita_terms.js` OK against the table only;
`check_gita_witness.py` 0 undocumented divergences; markup test green including the
render contract (meaning and fork display); builder citation chase 0 failures;
builder report 0 errors in schema, table hash, Kāśikā spans, wording headwords,
forbidden words in all public fields, pipeline vocabulary (standard §3.4), fork
consistency, cross-shard consistency and distinctness; every shard's review
`complete: true` at the frozen hash, the review including the meaning, readability
and blind-check passes; every `glossaryKey` resolves; every root carries gaṇa and pada;
no fallback of kind root, pratyaya or compound; every root or compound card carries at
least one traditional or kośa voice; every open fork visible; audio manifest
`verified` (or published `provisional` with the owner-listening list); deployed by the
script and verified at the live URL; `run_checks.sh` 0 failures; standalone and
embedded page checked at 390 and 1440 px.

## 9. Task list (amended 2026-11-08; prakriya `.codex/tasklist-autobuild.json` G0–G3 mirrors the earlier version)

| Id | Task | Done when |
| --- | --- | --- |
| G0.1 | prakriya lookup layer incl. the English engine; additions of §3 item 1–3 | readiness 1–3 |
| G0.2 | vedanta validators, builder checks B1–B18, public-text rule, render contract; Devanāgarī collation; BORI ledger | readiness 5, 10 |
| G0.3 | audio pipeline incl. calibration and listening sample | readiness 11 |
| G0.4 | `scripts/gita/`: packets, inventory, queue, validators, expansion, deploy script; runbook | readiness 4, 7 |
| G0.5 | reader display of `meaning` and fork `display` (UI owner) | readiness 6 |
| G1 | pilot chapter 12 (done 2026-11-08; meaning round applied as `2-ch12-meaning`); owner's first taste review (O3, O5, O12) | owner has read ch12 |
| G1.5 | migrate the earlier readers (sthitaprajña, kāma, ch5) to the table (standard §10) | no reader `legacy` |
| G1.6 | chapter-12 meaning layer on every card; fallbacks on affix or formation resolved; cards resting on Apte/MW re-derived (survey X13–X14) | ch12 passes the §8 gate |
| G2 | stage B lexicon for the whole Gītā; stages C–E for chapters 1–11, 13–18 | 700/700 published |
| G3 | audio for all chapters corroborated and verified | every chapter `verified` |

## 10. Effort and throughput (replaced 2026-11-08 with measured pilot figures)

**Measured on chapter 12** (audit §2, §4.8): 20 verses, 244 cards; loop total ≈426
agent-min (7.1 agent-h) = **21.3 agent-min per verse**; critical path 115 min at 4
concurrent shards (136 min from the owner's go); producers 46.6–62.3 min per 5-verse
shard, round-1 reviews 22–31 min, fresh fix agents 15–27 min (12.5–18.5 of them
re-reading), re-reviews 4.1–9.6 min; 70 findings (8 S1, 31 S2, 31 S3) = 28.7 per 100
cards, 3.3 S1 per 100 cards; about 44% of the agent time was work code should do or
rework that earlier decisions and tools would have prevented.

**Targets** (audit §4.8, projected per 5-verse shard): production ≈25 min, review
≈25, fix ≈8, re-review ≈5 → **≈63 agent-min per shard, ≈12.6 per verse**. The lexicon
was estimated at ≈6 agent-min per lemma for ≈200 lemmas (≈20 agent-h); lexicon-first
over the whole Gītā covers more lemmas, and the stage-A inventory gives the count
(BORI: 8,584 tokens, 4,510 distinct surface forms, 3,514 hapax). Whole Gītā (680
remaining verses): 680 × 12.6 ≈ 143 agent-h, plus the lexicon, plus a 5% post-scale
audit (≈7 agent-h): **≈170 agent-h** before the lexicon's measured size, against
≈241 agent-h under the pilot process with no meaning gate. At 16 concurrent agents
that is ≈11 h of agent wall time; the calendar is set by the lexicon and the owner's
taste reviews, not by the agents.

**Quality targets per chapter:** ≤ 10 findings per 100 cards; 0 findings of the
mechanical classes A–E (they become build errors); S1 ≤ 1 per 100 cards; 0 public
jargon fields; every root or compound card shows at least one traditional or kośa
voice; every open fork visible. A chapter that misses these halts and reopens the
brief (§13.4 item 6).

## 11. What kind of translation this is (owner question, 2026-11-08)

A **literal, grammar-first, school-neutral word-by-word translation with an
inspectable apparatus**, in the sense of `SANSKRIT_TRANSLATION_STANDARD.md` §1 and
§7. Concretely, for every verse the reader gets:

1. the BORI critical-edition text (the only text; variants recorded, not chosen);
2. one card per word proving its grammar from Pāṇini and the kośas (root, gaṇa,
   pada, pratyaya, morphology, kāraka, compound with vigraha), each claim cited to
   a locus in the prakriya library or stated as not located;
3. a literal English line whose every English word maps to a Sanskrit word by slot,
   with nothing added and nothing dropped, rendering the form that is actually there
   (participle as participle, passive as passive, case in its own force);
4. the depth kept in the card, not smuggled into the line: root image, attested
   senses, traditional nirvacanas, commentators' glosses, usage, reception, and the
   site's labelled synthesis (standard §6.3–§6.4).

It is **not** a paraphrase, a devotional rendering, a school's reading, or a poem.
Readability comes from rich and exact English (standard §7.17), not from loosening
the mapping. *(Amended 2026-11-08.)* The line must also parse on first reading
(standard §7.16): where literal and readable seem to conflict, the remedy is richer
exact English, English word order or an allowed construction, never an unreadable
line and never added or dropped meaning. The site's Aurobindonian depth-reading
(standard §6.3) is the labelled synthesis on the card; it never decides the line.

## 12. Secondary translations: whose, and how used (amended 2026-11-08)

The rule is standard §9: secondaries are out of production and of the lexicon; they
enter only in the stage-D blind check, after our line exists, for two questions — did
we miss an admissible construal, and what renderings will readers meet — and are never
authority and never republished. The editions held for that check:

| Role | Translator and edition | Why this one |
| --- | --- | --- |
| Aurobindo tradition | Anilbaran Roy, *The Message of the Gita* (1938; Ashram reprint *The Bhagavad Gita*, free auro-ebooks PDF/EPUB), supplemented by *The Gita in the Vision and the Words of Sri Aurobindo* (Ashram 2025, buy) for verses Roy lacks; CWSA 19 *Essays on the Gita* for context | The verse-ordered compilation Aurobindo himself approved. He did not call it his translation, so it is read as his exegesis (reception). |
| Advaita | Swami Gambhirananda, Śaṅkara's bhāṣya with translation (Advaita Ashrama, buy e-book); PD check: Swami Swarupananda 1909 (word-for-word) | The standard English of the Śaṅkara line. |
| Viśiṣṭādvaita | Swami Adidevananda, Rāmānuja's Gītābhāṣya (Sri Ramakrishna Math, buy); free: Rama Ramanuja Achari 2013 PDF | The Rāmānuja reading at verse level. |
| Dvaita | S. Subba Rau 1906 (PD, NEHU DSpace PDF); modern: Nagesh Sonde (buy) | The Madhva reading. |
| Kashmir Śaiva | S. Sankaranarayan 1985 (SVU; in `gita/gita`), Boris Marjanovic 2002 (buy) | Abhinavagupta's Gītārthasaṅgraha. |
| Philological word-by-word | Winthrop Sargeant, ed. Chapple (SUNY 2009, buy); PD checks: Besant & Das 1905, Telang 1882 (SBE 8); Edgerton 1944 only via Indian PD copies (US copyright to 2039) | Per-word grammatical tags; the comparator for construals. |

The commentators' **Sanskrit** (Śaṅkara, Rāmānuja, Madhva and the other commentaries
on disk) is not a secondary: it is primary evidence for the meaning layer (standard
§6.4) and is used from stage A. A blind-check record lists, per verse, only the
differences that matter (a missed construal, which becomes a fork; or better English
for the same construal, adopted on its dictionary merits or declined with a reason);
it is private and git-ignored.

## 13. Accuracy and fairness: how the line stays open to every valid reading

### 13.1–13.2 The fork record and admissible reasons (moved)

Now standard §6.5 (record, `words`, `display`, the five admissible reasons, "a
school's reading is evidence, never a reason").

### 13.3 Fairness test set

Loci where the schools are known to diverge; each must carry a fork record and
pass review before its chapter is published. Pilot (ch. 12): 12.3–4 *akṣaram avyaktam*,
12.5 *avyaktāsaktacetasām*, 12.12 the *jñāna → dhyāna → karmaphalatyāga* ordering,
12.20 *dharmyāmṛtam*. Chapter 2: 2.12, 2.16 *nāsato vidyate bhāvaḥ*, 2.39 *sāṅkhye
buddhiḥ*, 2.47 *karmaṇi … akarmaṇi*, 2.48 *samatvaṃ yoga ucyate*, 2.49–50
*buddhiyoga*, *yogaḥ karmasu kauśalam*, 2.72 *brahmanirvāṇam*. Whole text:
3.42–43, 4.18, 7.4–5 *parā prakṛti*, 9.32, 13.1–2 *kṣetrajña*, 15.7 *mamaivāṃśaḥ*,
18.61, 18.66 *sarvadharmān parityajya*. The list grows from the commentators' Sanskrit
in the packets and from the blind checks.

### 13.4 Quality assurance stack (amended 2026-11-08)

1. **Deterministic validators** (cannot be argued with): slot mapping, the table,
   witness check of the mūla, glossary resolution, card completeness (gaṇa, pada,
   ending piece), wording-record completeness, fork consistency and fairness loci,
   public-text rule, render contract; one validator per queue job.
2. **Citation discipline**: every grammatical claim cites `file:line` or a record id,
   chased by the builder; an unlocated claim is counted per chapter and stated on the
   card in reader words; no chapter is complete with an unlocated root, pratyaya or
   compound type.
3. **Lexicon review**: every lexicon batch reviewed independently before production
   uses it.
4. **One review pass in a fresh context** per shard (standard §5.1), the blind check
   last.
5. **Owner taste review** after provisional publication, flowing back as lexicon
   edits and sweeps.
6. **Post-scale audit**: after each published chapter a third agent re-derives a 5%
   random sample of accepted cards; a defect rate above the targets of §10 halts the
   chapter and reopens the brief.

## 14. Order of building (replaced 2026-11-08; from audit §5.9)

1. Reader display of `meaning` and fork `display` (UI owner, `UI_DESIGN_STANDARD.md`).
2. The standard's consolidation (done 2026-11-08) and the owner's line-style reading
   on chapter 12 (O5).
3. In parallel: lookup additions (§3 item 1–3) and their tests; `scripts/gita/`
   packets, inventory, queue and validators; the English stack.
4. The chain table and its review.
5. Stage A for all 700 verses; lexicon jobs; migration of the `2-ch12-meaning` rows.
6. Builder checks B1–B18; expansion script; deploy script.
7. Stage B, the whole lexicon.
8. Stages C–E for every chapter, shards in parallel up to the concurrency limit;
   chapter 12 rebuilt through the same route as the check that the route reproduces a
   known chapter.

The lead owns the table, the queue, the tools and integration, and does not edit
producer files. Audio runs in parallel throughout.

## 15. Audio: best achievable quality, and how the source is chosen

Owner instruction: the audio should be as good as the source allows, and a better
source may be taken from elsewhere. Procedure:

1. **Candidate set** = the lawful shortlist (§5.1 A, B, C) plus any source the
   owner adds. Two further high-quality recitations exist but need a licence we
   do not have: Swami Brahmananda (Chinmaya Mission; the Gita Supersite audio;
   licensing contact Central Chinmaya Mission Trust, commercial MP3 sold at $18–20)
   and the BBT recording (ISKCON; all rights reserved). The GitaVani app's 701
   per-verse files were ripped from a stream and are excluded. Commissioning a
   reciter (about $500–1,500 with a CC BY release) or self-recording (CC0) remain
   the only fully unencumbered routes.
2. **Measured quality** on chapter 12 of each candidate, by script
   (`scripts/audio/measure_quality.py`, ffmpeg `astats`/`ebur128`): sample rate and
   true bitrate, integrated loudness and loudness range, noise floor in the
   inter-verse gaps, clipping count, stereo correlation, tempo (seconds per verse,
   variance), presence of music or repeats, whether 13.1 and colophons are chanted.
3. **Heard quality**: the owner listens to the same two verses from each candidate
   and ranks pronunciation, pace and clarity.
4. **Choice**: the best-ranked lawful source; if the best source is not yet lawful
   (A), the pilot ships on the best lawful one (B) and swaps when the licence
   arrives; the manifest format does not change. The lead drafts the licence
   requests (A: Sadhakashram, to re-mark CC0 or CC BY 4.0 and permit per-verse
   clipping; optionally Chinmaya for Brahmananda); the owner sends them.
5. **Mastering** (format shift only, allowed under ND): high-pass at 60 Hz,
   loudness normalised to −18 LUFS integrated, true-peak −1 dBTP, no compression
   beyond that, downmix to mono, CBR 64 kbps MP3 with Xing header (or 96 kbps if
   the measured source warrants it); the raw source is kept untouched in the
   private store.
6. **Aligner choice** is also measured, not assumed: calibrate MMS forced
   alignment, the Sanskrit wav2vec2 model, and the Sanskrit-recitation Conformer
   (`prathoshap/sushrota-sanskrit-asr` through NeMo, if it installs on macOS) on
   the Sakhare chapter 15 per-verse clips and the Commons chapter 2–3 clips, which
   have known boundaries; keep the two with the lowest boundary error as the
   corroborating pair (§5.2). Report boundary error per aligner in the manifest.

## 16. Where everything is saved (as of 2026-11-08)

| What | Where | Committed? |
| --- | --- | --- |
| This plan | `vedanta-timeline/docs/GITA_FULL_TRANSLATION_PLAN.md` | no (untracked) |
| Pointer in the queue | `vedanta-timeline/docs/IMPLEMENTATION_QUEUE.md` §P-G | no (modified) |
| Governing standard (now with the card schema, forks, line style, register, secondaries rule) | `vedanta-timeline/docs/SANSKRIT_TRANSLATION_STANDARD.md`, `AUDIO_ALIGNMENT_STANDARD.md` | standard amended 2026-11-08, not committed |
| The table / Gītā lexicon | `vedanta-timeline/data/glossary/term_policy.json` (version `2-ch12-meaning`) | no (untracked) |
| Brief templates | `vedanta-timeline/docs/gita_briefs/` (LEXICON, PRODUCER, REVIEW) | no (untracked) |
| Pilot audit and precedents survey | `vedanta-timeline/docs/GITA_CH12_PIPELINE_AUDIT.md`, `TRANSLATION_PRECEDENTS_SURVEY.md` | no (untracked) |
| Pilot review store (private, git-ignored where it quotes secondaries) | `vedanta-timeline/internal/sanskrit_reviews/gita/ch12/` | ignored / untracked |
| Tooling spec for the lookup layer and data contracts | `prakriya/docs/TRANSLATION_PIPELINE_SPEC.md` §0 | no (untracked) |
| Task list G0–G3, H1 | `prakriya/.codex/tasklist-autobuild.json` | no (modified) |
| Audit synthesis and the nine agent reports | `prakriya/docs/research/DEEP_AUDIT_20261107.md`, `prakriya/research/audit-20261107/` | no (untracked) |
| Current-task pointers | `prakriya/docs/PICKUP.md`, `prakriya/AGENTS.md` | no (modified) |

Commits: the owner commits documents on request (no `git add -A` in vedanta-timeline).
Chapter publication follows §7.7 (L15), which supersedes the earlier sentence "nothing
is committed; the owner commits on request" for reader releases.

## 17. Owner instruction 2026-11-08 (third message) and the pilot run (history)

"Don't blindly follow any of these guys. They're making mistakes. Everything
should be grounded in the Sanskrit, in the tradition, in your ability to make it
as accurate as possible … as accurate and as poetic as possible." Recorded as:

- Secondaries (§12) are evidence of attested construals and inspiration for how
  exact English can read; none is authority; the producer brief says so.
  *(Superseded later that day by the owner's direction recorded in standard §9 and
  L14: secondaries are out of production and enter only as a blind check.)*
- The existing readers (`gita/sthitaprajna`, `gita/kama`, `gita/ch5`) are known
  to contain mistakes (e.g. roots without gaṇa/pada, the standard's §8 contradicted
  by the hard-coded checker on *krodha*). They are not models to copy. Task: a
  re-review sweep under the policy and the fork rule after the pilot (G1.5).
- The owner authorised the lead to build one chapter now without waiting for the
  readiness items to be complete: chapter 12, end to end, published to the
  Vedanta Timeline, then owner feedback. Readiness items delivered in this run:
  lookup layer (prakriya `scripts/lookup/lookup.py`, nine subcommands, tests in
  `tests/lookup/`), English definition index (Webster 1913 + GCIDE + WordNet 3.1,
  552k definitions, `prakriya/tmp/english/english.db`), term policy v1 for the
  chapter-12 lemmas (`data/glossary/term_policy.json`), policy mode in
  `check_gita_terms.js`, ChapterPacket builder with Devanāgarī collation
  (`scripts/build_gita_chapter_packet.py`), fail-closed reader builder
  (`scripts/build_gita_chapter_reader.py`), producer and reviewer briefs
  (`internal/sanskrit_reviews/gita/ch12/`), audio pipeline on P R Iyer's
  chapter 12 (`scripts/audio/`), markup test repaired (DOM stub).
- Devanāgarī collation result for chapter 12: 30 of 40 witness pairs identical
  after orthographic folding; the differences are edition variants or OCR noise
  in the Madhva file (12.18 *mānāpamānayoḥ* vs BORI *mānāvamānayoḥ* is a real
  variant, recorded; BORI stands).

### 17.1 Pilot result (2026-11-08, same day)

Chapter 12 built and registered: `gita/ch12/` (verses.js, apparatus.json, audio.js,
recitation.mp3, index.html), `assets/app.js` GITA_READINGS `gita-ch12`,
`data/articles/manifest.json`. 20 verses, 244 cards, 65 fork records (10 open,
class 5), 16 fallback claims (none on a root, a pratyaya or a compound type),
every card with a wording record where required, deviations against seven
secondaries per verse. Four independent reviews, 68 findings in round 1 (8 of
severity 1, all grammar or policy), all resolved and re-verified at the frozen
hash (rounds 2–3). Validators: slots OK, policy OK, witness OK, markup test
green, audio manifest OK (20/20 corroborated, `provisional` until the owner
listens). Defects found by the pilot and fixed in the tools: Kāśikā locator
offset base and nearest-line selection; policy detector per-field matching;
three missing policy rows (upāsanā, para, parama); wording records citing a
neighbouring headword (new `define` subcommand, brief rule); builder exemptions
for preserved terms, names and copulas. Measured cost: producers 47–62 min per
five-verse shard, reviewers 22–31 min, fix rounds 15–27 min, re-reviews 4–7 min;
about 3.5 h wall-clock for the chapter with four shards in parallel.
Owner items (O3): the `review: pilot` rows (cetas, dhyāna, duḥkha/sukha, dveṣa
verb forms, sama, śubha/aśubha, amṛta), "the everywhere-going" vs "all-pervading"
(12.3), "the travail" (12.5), "content with whatsoever" (12.19), and the audio
spot-listening list in `gita/ch12/audio.js`. Not committed: the owner commits.

### 17.2 Corrections to §17.1 (2026-11-08, from audit P8 and survey X14)

- Forks: 65 records, of which **12** are open (reason class 5), not 10. They were in
  the data but not rendered by the reader (audit T18).
- Fallbacks: 16, of which at least six concern an affix or formation (12.3 *dhruvam*,
  12.16 *dakṣaḥ* and *gatavyathaḥ*, 12.19 *naraḥ*, *parama* in 12.10 and 12.20); the
  completion rule was not met. Five cards rest their formation on Apte or MW (G1.6).
- Findings: 70 in all (68 in round 1, 2 in round 2); re-reviews took 4.1–9.6 min.
- Wording records are complete only under the builder's exemptions for preserved
  terms, names and copulas.
- The audio spot-listening list did not exist in `audio.js` (§5.2 step 5 now requires
  it).
- The chapter was built but not deployed (audit P7). A meaning round followed (four
  meaning reviews; term policy `2-ch12-meaning`; L19).

## 18. Lessons of the pilot (2026-11-08)

1. **Decide meaning before production.** The table was written in one call five
   minutes before the producers started; 12 of 53 rows changed during the run while
   its version string did not. Classes A–E — late rows, undecided line style, tool
   defects, hand-written derivation chains, citation hygiene — produced 41 of 70
   findings (59%) and 4 of the 8 S1. Hence lexicon first (§7.4) and line style in the
   standard (§7.8–§7.17).
2. **Spend the agents on meaning, not on typing citations.** Producers spent 62% of
   their model time emitting JSON, about half of it citation text code can generate;
   the English line and sense were 0.7% of their output. Reviewers spent ≈42% of
   their time chasing citations by hand (4,112 checks). Code must expand and chase.
3. **Review what the reader reads.** The review never asked whether a line reads as
   English, whether a card carries the tradition's meaning, or whether the root's
   image survives; it could not challenge a row; it exempted the lead's decisions.
   Result: 'wait upon' for the chapter's governing verb, three statements turned into
   questions against Apte's 'if', and 104 of 145 root or compound cards with no
   traditional voice. Hence the single review pass with meaning and readability, row
   proposals, and the lead reviewed like anyone else.
4. **Use the whole library for meaning.** About 1,170–1,190 Aṣṭādhyāyī and 650 Kāśikā
   citations (audit §0: 1,166 and 646; the lead's later count: 1,190 and 656), but none
   from the Nirukta, Nighaṇṭu, Kṣīrataraṅgiṇī, Mādhavīya Dhātuvṛtti, Dhātupradīpa,
   Daiva-Puruṣakāra, Halāyudha, Vaijayantī, Yādavakośa or Amaraviveka, 7 from the
   Śabdakalpadruma, 2 from the Vācaspatyam, and 0 from *Essays on the Gita*. Grammar
   was proved; meaning was thin.
5. **Our English, not theirs.** Comparing every verse with seven secondaries cost
   140 deviation records and pulled the English toward the most common word; of 155
   wording decisions only one chosen word was rare or archaic, and three of four
   "Joycean" records were the ordinary "unmanifest". The register pass (plain and rich
   candidates) found "houseless", "deft", "infixed", "loosed", "weigh alike". Hence
   standard §7.17 and §9.
6. **Resume, do not respawn.** Fresh fix agents spent 12.5–18.5 min each re-acquiring
   context; a shard was changed while under review; lead edits after acceptance
   re-stamped the hash. Fixes go to the same producer; shards freeze at review; the
   builder refuses unreviewed edits.
7. **The reader must show what the gate certifies.** 65 forks and 20 sense paragraphs
   were invisible; 23 public fields carried process jargon. Hence the render contract
   and the public-text rule.
8. **Publish by script.** The pilot was built but not deployed, in a working tree
   shared with other agents. Hence §7.7.
9. **Measure.** 21.3 agent-min per verse measured; 12.6 is the target; a chapter that
   misses the quality targets halts and reopens the brief.
