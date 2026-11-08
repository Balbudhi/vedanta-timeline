# The whole Bhagavad-Gītā, word by word, with audio: goal, decisions, task list

Owner instructions (2026-11-07 and 2026-11-08): translate all 700 verses to
[`SANSKRIT_TRANSLATION_STANDARD.md`](SANSKRIT_TRANSLATION_STANDARD.md) by agents
now; **no commentary layer**; **audio for every verse, synced and timed**, with the
existing tap-a-word and tap-a-verse functionality; **one consistent term rule** with
its logic stated; **full use of English** through the dictionary-discovery design
from the Bhakti engine plan (uncommon attested senses, the Joycean step). The owner's
aesthetic judgement is the final gate. This plan amends the standard's §5 for the
Gītā. Measured starting state and evidence: prakriya
`docs/research/DEEP_AUDIT_20261107.md` and `research/audit-20261107/`.

## 1. Goal

A public reader `gita/chN/` for N = 1..18: for each verse the BORI mūla in
Devanāgarī, the IAST pada-pāṭha with a card on every word (root with gaṇa and
pada, pratyaya, morphology, compound with vigraha, kāraka, complete morpheme parts,
attested senses, glossary link), the literal slotted English, and a recitation
synced at verse level (tap a verse to hear it; the playing verse is highlighted).
Every grammatical claim is cited to a locus in the prakriya source library or
flagged. Every English word choice is made from dictionary definitions and recorded.
Every significant deviation from six respected translations is defended in writing.
Nothing is published that failed a validator or the owner's review.

## 2. Decisions

### 2.1 Decided by the lead (override at any time)

| # | Decision | Logic |
| --- | --- | --- |
| L1 | **No commentary rendering.** Commentaries stay in the pipeline as evidence for pada division, sense selection and deviation defence; they are not rendered word by word and the reader shows mūla only. | Owner instruction. Removes the Śaṅkara ch. 18 and Madhva witness blockers from the critical path and about 90% of the card volume. |
| L2 | **Term rule is sense-constant, not string-constant** (§4). A lemma is kept in Sanskrit for a recorded *sense*; the same string in a recorded plain sense is translated; each (lemma, sense) is decided once in `data/glossary/term_policy.json` and machine-checked on every occurrence. | We translate meanings, not strings; a string-constant rule would force a distortion somewhere (2.47 *karmaṇi* "in karma" imports the law-of-action load into a plain "in action"). Consistency is still total: same sense, same rendering, everywhere, enforced by the checker. |
| L3 | **Devanāgarī mūla** is a deterministic transliteration of the BORI IAST witness, labelled as such in the data, collated against a second Devanāgarī witness (per-verse `gita/gita` text or sanskritdocuments) with every difference recorded; BORI remains the text. | The standard forbids *silent* script generation; a labelled lossless transliteration plus collation satisfies it. The only Devanāgarī on disk today sits inside a scraped commentary. |
| L4 | **Audio: one lawful complete recitation, per-chapter files, verse-level manifest, two-method corroboration, owner spot-listening** (§5). Word timestamps are stored provisionally and not shown until verified. | The audio standard allows verse-level only and forbids inferred word highlighting; the alignment stack is already installed locally. |
| L5 | **English discovery is mandatory per content word** (§6): the producer writes a sense description from the Sanskrit evidence, retrieves English candidates from definitions across the full dictionary stack, records the candidates considered, chooses with connotation and register stated, and may form a Joycean compound only under the recorded rules. | Owner instruction: English is rich and the plan exists; the Bhakti design is sound even though its song coordinator never delivered. |
| L6 | **Producers and reviewers are Claude Code agents**; no DeepSeek, TypeSafe or Gemini in the default route; no paid API spend required. | Owner asked for agents now; the prakriya rule against invoking client subscriptions concerns the autobuild product. |
| L7 | **krodha → anger**, and every other emotion word translates (§4). | The preserve test (§4.1) fails: English carries it without adding or dropping; the standard's own §8 example. Existing data preserving *krodha* will be swept. |
| L8 | **Pilot is chapter 12** (20 verses) through the whole loop including audio; then chapter 2 verses 1–53; then all chapters in parallel. | Short, well-commented, complete in every layer; measures throughput before scaling. |
| L9 | Review loop reuses the Yogavāsiṣṭha-Dāma producer-packet → independent-review → fail-closed-builder files and schema under `internal/sanskrit_reviews/gita/chN/`. | Already built and proven in this repository; the Gītā never got it. |

### 2.2 Still the owner's

| # | Decision | Needed by |
| --- | --- | --- |
| O1 | Confirm the sense-constant term rule (L2) or demand string-constant. | Phase 0 term table |
| O2 | Choose the recitation source from the lawful shortlist (§5.1), or record it yourself, or commission a reciter with a written release. | Audio pilot |
| O3 | Accept or revise the chapter 12 pilot's English and term table (the aesthetic gate). | Before scaling |
| O4 | Repository hygiene go/no-go (prakriya audit §11) and the stale prompt hook; not blocking. | Any time |

## 3. Readiness: what must be true before "translate all of them"

1. **Lookup layer** in prakriya built and tested offline (prakriya
   `TRANSLATION_PIPELINE_SPEC.md` §0.4 items 1–8): sūtra, dhātu, kośa, uṇādi, liṅga
   indices; Cologne dictionary lookup; English sense engine; Gītā verse and
   commentary locator; pada candidates with sandhi loci; card validator; chapter
   packet builder. Acceptance: the audit's probe loci reproduce; chapter 12 packet
   builds with every pada evidence block.
2. **English engine** returns definitions and tagged senses for a sense query across
   Webster 1913, GCIDE, Wiktionary (kaikki), Open English WordNet 2025, Century OCR,
   Roget and Moby, plus the Bhakti WordNet FTS reverse lookup; a wording-decision
   record validates.
3. **Term policy v1**: the rule of §4 applied to every lemma occurring three or more
   times in the BORI text (about 150 lemmas; 8,584 tokens, 4,510 distinct surface
   forms, 3,514 hapax), with a glossary file for every preserved sense (missing today:
   `adhikara, phala, hetu, papa, soka` and whatever the inventory adds); checker reads
   the table; the standard's §8 quotes it; owner confirmed O1.
4. **Validators**: slot and term checkers discover `gita/*/verses.js` and fail on an
   unresolved glossary key; the witness check verifies the mūla of every reader; the
   builder requires gaṇa and pada on every root and an ending piece in `parts[]`; the
   markup test is green; `run_checks.sh` passes.
5. **Mūla witnesses**: BORI registered in the source ledger; Devanāgarī transliteration
   script with its collation report against a second witness (L3).
6. **Audio**: source acquired for all 18 chapters with licence text (O2); alignment
   runs on chapter 12; corroboration tolerance met; manifest validates; owner has
   spot-listened and the reader plays verse by verse.
7. **Secondaries and dictionaries acquired** into the private store and prakriya
   staging (free items now; purchases listed in prakriya
   `research/audit-20261107/external-resources.md`).
8. **Pilot accepted** (O3): chapter 12 merged through the full gate (§8); producer and
   reviewer briefs frozen; measured verses per agent-hour and defect rate used to set
   shard size and parallelism.

When 1–8 hold, the instruction "translate all of them" runs §7 across chapters
1–18 in parallel with no further design decisions.

## 4. The term rule and its logic

### 4.1 The rule

We translate meanings, not strings. A Sanskrit word is kept in Sanskrit (IAST,
glossary-linked) for a given sense only if **all three** hold:

1. **It is a term of the Gītā's own system in that sense**: the text defines,
   enumerates or argues about it as a category (yoga, dharma, karma-as-law, guṇa,
   prakṛti, puruṣa, buddhi, manas, indriya, ahaṅkāra, prajñā, yajña, tapas, bhakti).
2. **No English word or short phrase carries that sense without adding or dropping**
   (standard §7.1–7.5): "duty" drops most of dharma; "mind" collapses manas, buddhi
   and citta; "action" drops the fruit-and-law load of karma in its technical use.
3. **Keeping it loses nothing a reader needs**, because the card and glossary carry
   the full meaning.

If any test fails, the word is translated, with one fixed rendering per sense
(krodha → anger, bhaya → fear, moha → delusion, duḥkha → sorrow, sukha → pleasure
or, in the adverb, at ease, saṅga → clinging, jñāna → knowledge, mokṣa →
liberation, śānti → peace, pāpa → sin, puṇya → merit, saṃnyāsa → renunciation,
tyāga → relinquishment, kṣetra → field, avyakta → the unmanifest, akṣara → the
imperishable, īśvara → the Lord). Two distinct Sanskrit words never share one
English word (§7.6), so saṃnyāsa and tyāga, contrasted by the text itself in 18.1–2,
get distinct renderings. Established English forms count as "kept": brahman →
Brahman, ātman → the self (as the standard already rules).

### 4.2 Why this is consistent

The unit of consistency is the (lemma, sense) pair, not the spelling. Each pair is
decided once, written in `term_policy.json` with its glossary key, renderings,
forbidden renderings and the test results, and the checker verifies every
occurrence in every chapter against that one row. The same sense is therefore
rendered the same way in all 700 verses. A string-constant rule looks simpler but
is less consistent in the sense that matters: it would render *karmaṇi* in 2.47 as
"karma" while every commentator glosses it as the act, importing a meaning the verse
does not have, which is exactly the distortion §7 forbids. Where the text uses one
string in two senses, the card shows the Sanskrit, the gloss, and the glossary link
either way; only the line's English differs, and the row records why.

### 4.3 Seed decisions for the pilot (complete table built in Phase 0)

- Preserve: yoga, dharma (incl. svadharma "one's own dharma"), karma (law and
  fruit-bearing act), guṇa, sattva, rajas, tamas, prakṛti, puruṣa, buddhi, manas,
  indriya, ahaṅkāra, prajñā, kāma, rāga, dveṣa, tṛṣṇā, rasa, samādhi, saṃsāra, māyā,
  yajña, tapas, bhakti and bhakta, dhyāna. Established: Brahman, the self.
- Translate: the list in §4.1 plus phala → fruit, hetu → cause, śaraṇa → refuge,
  śraddhā → faith, siddhi → perfection, deva → god, jīva → living being, śoka → grief.
- Decide in the pilot with the commentators open: vijñāna, kṣetrajña, sama/samatva,
  karma in plain-act contexts (2.47 pattern), yoga in the plain "joining" sense if
  it occurs, nirvāṇa (one occurrence, 2.72 already rendered).

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
   repeated verses are corrected by hand.
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
manifest.

## 6. English discovery and wording (the Bhakti design, applied)

For every content word the producer records a wording decision:

1. **Sense**: a one-line English description of the operative sense derived from
   the Sanskrit evidence (root image, commentators' lemma, kośa synonym group).
2. **Discovery**: run the English engine with that description and with the Sanskrit
   root image; retrieve candidate words and phrases from definitions across the
   stack (Webster 1913, GCIDE, Wiktionary with obsolete/archaic/dated tags, OEWN,
   Century, Roget, Moby, WordNet FTS). Rarity is not a rejection criterion; a
   WordNet miss means consult another dictionary, not coin a word.
3. **Choice**: pick the candidate whose definition carries the sense without adding
   or dropping (§7.1–7.5), state connotation and register, keep the root image where
   the Sanskrit carries it, and keep distinct Sanskrit words distinct (§7.6).
4. **Joycean step**, only when no attested word or short phrase is adequate: form a
   compact compound or blend; record parts, their senses and sources, the relation,
   a plain paraphrase and the line it must read in; never label it attested; reject
   it if it adds an image, agency or claim the Sanskrit lacks. The reviewer judges
   the whole formation, not its parts.
5. **Memory**: accepted decisions enter the term-decision memory; later shards reuse
   them (§7.7) or record a justified context exception.

The deterministic parts (retrieval, definition expansion, record validation) are
code in prakriya's lookup layer and the Bhakti reverse-dictionary modules; the
judgement is the producer's and is checked by the reviewer against the definitions.

## 7. Production loop per chapter

```text
packet builder (code) → ChapterPacket (per verse, per pada evidence; commentators'
   Sanskrit as evidence; six secondary renderings, private)
producer agent (shard ≈10 verses) → cards + slotted english + sense + grammar{} +
   evidence per claim or FALLBACK + wording decisions + forks (§13) + deviation defences
independent reviewer agent (fresh context) → recomputes every card from sources,
   checks §6 completeness and §7.1–7.7, term policy, wording against definitions,
   challenges every deviation defence; tests every fork's wrong alternative and
   that no fork was resolved by a school (§13.2); findings → producer; accept at frozen hash
builder (fail-closed) → gita/chN/verses.js, index.html, registrations; refuses on
   any validator failure
audio (§5) → gita/chN/audio.js + mp3, corroborated then verified
owner review page → accept / revise per verse; decisions into term_policy.json
```

Producer and reviewer briefs are as in the previous revision of this plan
(cite or flag every claim; §6 formality; §7 rules; secondaries compared, deviations
defended; adversarial self-reread before handoff; reviewer recomputes and tries
the plausible wrong alternative), now with the §6 wording record added.

## 8. Gate per chapter

`validate_gita_slots.js` OK; `check_gita_terms.js` OK against `term_policy.json`;
`check_gita_witness.py` 0 undocumented divergences for the mūla; markup test green;
independent review `complete: true` for every shard at the frozen producer hash;
every `glossaryKey` resolves; every root carries gaṇa and pada; FALLBACK count
reported and each one visible on its card; wording records complete; fork records
complete for every §13.3 locus in the chapter and every reviewer-raised fork; deviation
file complete (every secondary, every verse); audio manifest `verified` with all
boundaries corroborated or hand-corrected; owner review accepted; `run_checks.sh`
0 failures; standalone and embedded page checked at 390 and 1440 px.

## 9. Task list (mirrored in prakriya `.codex/tasklist-autobuild.json`, tasks G0–G3)

| Id | Task | Done when |
| --- | --- | --- |
| G0.1 | prakriya lookup layer incl. the English engine (spec §0.4) | readiness 1–2 |
| G0.2 | vedanta Phase 0: validators, markup test, term table v1 from the §4 rule, glossary files, BORI ledger record, Devanāgarī transliteration + collation, free acquisitions, `gita/gita` clone as evidence index, `forks[]` added to the standard's schema §3 and to the slot validator | readiness 3–5, 7 |
| G0.3 | audio pipeline: quality measurement of every candidate on ch. 12 (§15), licence-request drafts, source decision (O2), `scripts/audio/` alignment + aligner calibration + corroboration + mastering + manifest, run on chapter 12 | readiness 6 |
| G1 | pilot chapter 12 end to end incl. audio and owner review; freeze briefs; measure throughput; then chapter 2.1–53 | readiness 8 |
| G2 | chapters 1, 3, 4, 6–11, 13–18 in parallel shards; cross-chapter term memory | 700/700 merged through §8 |
| G3 | audio for all chapters corroborated and verified; word-timestamp layer kept provisional | every chapter `verified` |

## 10. Effort (estimates from the two-verse test; no commentary)

About 9,500 mūla cards. With the lookup layer, 12–20 min per verse for a
knowledgeable agent, 45–90 cold: producers about 250–525 agent-hours total,
reviewers similar, run in parallel across chapters. Owner review: flagged cards only
(10–25%) plus the aesthetic pass, about 50–80 hours over the project. Audio:
alignment runs in minutes per chapter; owner listening about 3 hours total for the
samples and disagreements. No paid API spend in the default route.

## 11. What kind of translation this is (owner question, 2026-11-08)

A **literal, grammar-first, school-neutral word-by-word translation with an
inspectable apparatus**, in the sense of `SANSKRIT_TRANSLATION_STANDARD.md` §1 and
§7. Concretely, for every verse the reader gets:

1. the BORI critical-edition text (the only text; variants recorded, not chosen);
2. one card per word proving its grammar from Pāṇini and the kośas (root, gaṇa,
   pada, pratyaya, morphology, kāraka, compound with vigraha), each claim cited to
   a locus in the prakriya library or marked FALLBACK;
3. a literal English line whose every English word maps to a Sanskrit word by slot,
   with nothing added and nothing dropped, rendering the form that is actually there
   (participle as participle, passive as passive, case in its own force);
4. the depth kept in the card, not smuggled into the line: attested senses, root
   image, traditional nirvacanas, and the site's labelled synthesis (standard §6.3
   categories 1–6 kept separate).

It is **not** a paraphrase, a devotional rendering, a school's reading, or a poem.
Readability comes from rich and exact English (§6), not from loosening the mapping.
Where English cannot be literal and natural at once, literal wins in the line and
natural lives in the card paraphrase. The site's Aurobindonian depth-reading
(standard §6.3) is the labelled category-6 synthesis on the card; it never decides
the line.

## 12. Secondary translations: whose, why, how used

Secondaries are **never a source of meaning**. They are used for three things only:
(a) **deviation detection**, every verse compared, every significant difference
defended in writing from grammar and kośa; (b) the **tradition-spread check** of
§13, which shows where the schools actually diverge so that the line stays open
there; (c) **pada-division cross-check** against the two word-by-word editions.
Full details, legal status and acquisition in prakriya
`research/audit-20261107/external-resources.md`.

| Role | Translator and edition | Why this one |
| --- | --- | --- |
| Aurobindo tradition | Anilbaran Roy, *The Message of the Gita* (1938; Ashram reprint *The Bhagavad Gita*, free auro-ebooks PDF/EPUB), supplemented by *The Gita in the Vision and the Words of Sri Aurobindo* (Ashram 2025, buy) for verses Roy lacks; CWSA 19 *Essays on the Gita* for context | The verse-ordered compilation Aurobindo himself approved; the one the Aurobindo community uses. He did not call it his translation, so it is read as his exegesis. |
| Advaita | Swami Gambhirananda, Śaṅkara's bhāṣya with translation (Advaita Ashrama, buy e-book); PD check: Swami Swarupananda 1909 (word-for-word) | The standard English of the Śaṅkara line; Swarupananda gives an independent pada gloss. |
| Viśiṣṭādvaita | Swami Adidevananda, Rāmānuja's Gītābhāṣya (Sri Ramakrishna Math, buy); free: Rama Ramanuja Achari 2013 PDF | The Rāmānuja reading at verse level. |
| Dvaita | S. Subba Rau 1906 (PD, NEHU DSpace PDF); modern: Nagesh Sonde (buy) | The Madhva reading; Madhva's and Jayatīrtha's Sanskrit from the `gita/gita` index for checking. |
| Kashmir Śaiva | S. Sankaranarayan 1985 (SVU; in `gita/gita`), Boris Marjanovic 2002 (buy) | Abhinavagupta's Gītārthasaṅgraha; also the Kashmirian recension for witness awareness. |
| Philological word-by-word | Winthrop Sargeant, ed. Chapple (SUNY 2009, buy): per-word grammatical tags; PD checks: Besant & Das 1905, Telang 1882 (SBE 8); Edgerton 1944 only via Indian PD copies (US copyright to 2039) | The only published translation with a full grammatical tag on every word; the direct comparator for our cards. |

Rules: all secondaries live in the private store (`internal/`), quotation only,
never republished, never shown in the reader; the ISKCON synonyms, Mukundananda
meanings and the modern `gita/gita` translations are index material only. The
deviation file for a chapter lists, per verse, each secondary's rendering of the
disputed words and the defence of ours.

## 13. Accuracy and fairness: how the line stays open to every valid reading

The standard's rule is "explicit ambiguity, never a faked single parse" (§1) and
"show every independently supported formation in parallel" (§6.2). For a text that
five schools read differently, that rule needs a mechanism, which is this:

### 13.1 The fork record

A verse record gains `forks[]`. A fork is any place where more than one construal
is **grammatically admissible**: a pada division, a sandhi resolution, a case
force, a compound type, a referent of a pronoun, an attested sense of a lemma, or
the scope of a negation. Each fork records: the locus; each construal with its
grammar basis (sūtra, kośa, parallel usage inside the Gītā) and its evidence
loci; which of the six secondaries take which construal; the construal the line
follows; and the reason, which must be one of the admissible reasons below.

### 13.2 Admissible reasons to resolve a fork

In this order, and only these:

1. **Grammar excludes it**: a construal breaks Pāṇini (cite the sūtra) or sandhi.
2. **The Gītā's own usage**: the same word or construction elsewhere in the text
   settles the sense (cite the verses).
3. **Kośa**: the sense is not attested for the lemma in the kośas and dictionaries.
4. **English can stay open**: choose the English that admits the same readings the
   Sanskrit admits (often possible; the literal line is already underdetermined the
   way the Sanskrit is).
5. **English forces a choice**: when no English keeps both readings, follow the
   reading with the strongest grammar-only support, render the alternative in the
   card as a parallel construal with its traditions named, and mark the fork
   `open: true`. The reviewer confirms that no reason of the form "school X reads
   it so" was used.

A school's reading is **evidence that a construal is attested**, never a reason to
prefer it. Where grammar underdetermines and English forces a choice, the reader
sees both; this is the sense in which the translation facilitates multiple valid
streams rather than adjudicating them. Readings attested only in later reception
are kept as reception (standard §6.3), not promoted into the fork.

### 13.3 Fairness test set

Loci where the schools are known to diverge; each must carry a fork record and
pass review before its chapter merges. Pilot (ch. 12): 12.3–4 *akṣaram avyaktam*,
12.5 *avyaktāsaktacetasām*, 12.12 the *jñāna → dhyāna → karmaphalatyāga* ordering,
12.20 *dharmyāmṛtam*. Chapter 2: 2.12, 2.16 *nāsato vidyate bhāvaḥ*, 2.39 *sāṅkhye
buddhiḥ*, 2.47 *karmaṇi … akarmaṇi*, 2.48 *samatvaṃ yoga ucyate*, 2.49–50
*buddhiyoga*, *yogaḥ karmasu kauśalam*, 2.72 *brahmanirvāṇam*. Whole text:
3.42–43, 4.18, 7.4–5 *parā prakṛti*, 9.32, 13.1–2 *kṣetrajña*, 15.7 *mamaivāṃśaḥ*,
18.61, 18.66 *sarvadharmān parityajya*. The list grows from the deviation files.

### 13.4 Quality assurance stack (how we know it is done properly)

1. **Deterministic validators** (cannot be argued with): slot mapping, term policy,
   witness check of the mūla, glossary resolution, card completeness (gaṇa, pada,
   ending piece), wording-record completeness, fork completeness on the test set.
2. **Citation discipline**: every grammatical claim cites `file:line` in the
   prakriya library or is FALLBACK; FALLBACK is counted per chapter, shown on the
   card, and the chapter cannot be marked complete while any FALLBACK concerns a
   root, a pratyaya or a compound type.
3. **Independent review in a fresh context**: the reviewer recomputes every card
   from sources without seeing the producer's reasoning first, checks every
   wording against the dictionary definition it cites, tries the plausible wrong
   alternative on every fork, and challenges every deviation defence.
4. **Secondary comparison**: six traditions per verse; deviation defended or
   corrected.
5. **Owner gate**: aesthetic acceptance of the English and the term table on the
   pilot; flagged cards and a sample afterwards.
6. **Post-scale audit**: after each merged chapter a third agent re-derives a 5%
   random sample of accepted cards; a defect rate above the pilot's measured rate
   halts the chapter's merge and reopens the brief.

## 14. Layers and build order

```text
L0  witnesses        BORI IAST mūla · second Devanāgarī witness · commentators'
                     Sanskrit (evidence) · six secondaries (private)
L1  lookup (code)    prakriya: sūtra · dhātu · kośa · uṇādi · liṅga · dictionaries ·
                     English engine · verse/commentary locator · sandhi/pada candidates
L2  packet (code)    ChapterPacket: per verse, per pada, every locatable evidence block
L3  pada + grammar   producer: division, sandhi loci, root/gaṇa/pada, pratyaya,
                     morphology, kāraka, compound → cited cards (§6.1 authority)
L4  sense + term     attested sense chosen; term_policy applied (§4); forks opened (§13)
L5  wording          English discovery per content word; Joycean step if needed (§6)
L6  line             slotted literal English; fork resolution recorded
L7  review           independent reviewer; secondaries; deviation file; forks tested
L8  build (code)     fail-closed builder → gita/chN/verses.js; validators; markup test
L9  audio            per-chapter MP3 · two aligners · corroboration · owner listening
L10 owner gate       accept / revise; decisions flow back into term_policy and briefs
```

Order and parallelism:

1. **G0.1 lookup layer** first (L1–L2); nothing semantic starts without it, because
   every card cites it. One agent owns `src/prakriya/lookup/`.
2. **G0.2 vedanta Phase 0** (validators, term table, glossary, witnesses) and
   **G0.3 audio** run in parallel with G0.1; they share no files.
3. **G1 pilot** chapter 12 through L3–L10; briefs frozen from what the pilot
   teaches; throughput and defect rate measured; then 2.1–53 to confirm.
4. **G2** all remaining chapters at once: one producer per shard of about ten
   verses, one fresh reviewer per shard, one builder per chapter, disjoint files
   (`gita/chN/`, `internal/sanskrit_reviews/gita/chN/`); the lead owns
   `term_policy.json`, the glossary and cross-chapter memory, and merges.
5. **G3 audio** for all chapters in parallel with G2 (L9 depends only on the mūla).

When the owner says "go", the lead's procedure is fixed: build the eighteen
ChapterPackets, spawn producers with the frozen brief, then reviewers, then
builders, run the §8 gate per chapter, and report FALLBACK, fork and deviation
counts per chapter with the owner's review queue.

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
| This plan (goal, decisions, readiness, term rule, audio, English, loop, gate, tasks, kind of translation, secondaries, fairness, layers) | `vedanta-timeline/docs/GITA_FULL_TRANSLATION_PLAN.md` | no (untracked) |
| Pointer in the queue | `vedanta-timeline/docs/IMPLEMENTATION_QUEUE.md` §P-G | no (modified) |
| Governing data standard | `vedanta-timeline/docs/SANSKRIT_TRANSLATION_STANDARD.md`, `AUDIO_ALIGNMENT_STANDARD.md` | yes; §3 schema gains `forks[]` in G0.2 |
| Tooling spec for the lookup layer and data contracts | `prakriya/docs/TRANSLATION_PIPELINE_SPEC.md` §0 | no (untracked) |
| Task list G0–G3, H1 | `prakriya/.codex/tasklist-autobuild.json` | no (modified) |
| Audit synthesis and the nine agent reports | `prakriya/docs/research/DEEP_AUDIT_20261107.md`, `prakriya/research/audit-20261107/` | no (untracked) |
| Current-task pointers | `prakriya/docs/PICKUP.md`, `prakriya/AGENTS.md` | no (modified) |

Nothing is committed; the owner commits on request (no `git add -A` in
vedanta-timeline). Until then the files exist only in the working trees.

## 17. Owner instruction 2026-11-08 (third message) and the pilot run

"Don't blindly follow any of these guys. They're making mistakes. Everything
should be grounded in the Sanskrit, in the tradition, in your ability to make it
as accurate as possible … as accurate and as poetic as possible." Recorded as:

- Secondaries (§12) are evidence of attested construals and inspiration for how
  exact English can read; none is authority; the producer brief says so.
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
