# Bhakti translation pipeline: post-mortem for the Gītā pipeline

Written 2026-11-08 from a read-only examination of `/Users/eeshan/Dev/bhakti`. Nothing
in that repository was changed and no paid or model call was made. Sources: README,
AGENTS, `docs/` (chiefly `TRANSLATION_ENGINE_PLAN.md`, `TRANSLATION_COMPONENT_AUDIT.md`,
`TRANSLATION_WORKFLOW.md`, `LIBRARY_REPAIR_TASKS.md`, `GEMINI_MODEL_QUALIFICATION.md`,
`SONG_PROCESSING_STANDARD.md`), the engine scripts, the private run records, git history (353 commits), the earlier audit
`prakriya/research/audit-20261107/bhakti-engine.md`, and a fresh run of the test
suite. Compared against prakriya `docs/TRANSLATION_PIPELINE_SPEC.md` §0–§0.6,
`docs/GITA_FULL_TRANSLATION_PLAN.md`, this directory's RUNBOOK, LEXICON_BRIEF,
VERSE_BRIEF and REVIEW_BRIEF, and the in-progress chapter-12 acceptance run
(`internal/gita_pipeline/acceptance/ch12/WORKER_FEEDBACK.md`).

**Verdict.** Bhakti built a good retrieval substrate and a good written translation
policy, then spent three weeks failing to get one song through them. It asked one-shot,
low-cost API models (Gemini Flash, then Pro) to make every judgement, including the
review, on a whole song at once. Each call was wrapped in fail-closed validators the
model could not see or fix. When a run stopped, an engineer fixed that one stop and
paid for a fresh run. The model review never learned to catch defects. After about 22
bounded trials on one nine-line song, the October engine produced **0 accepted songs**.

---

## 1. What the Bhakti pipeline tried to do

There were three generations. Each one replaced the previous one instead of extending
it.

### 1.1 Generation 1: Gemini song pipeline (20 Aug – 3 Sep 2026; 192 commits on 20–23 Aug)

`scripts/process_song_gemini.py`, `docs/SONG_PROCESSING_STANDARD.md` "Translation contract":

| Stage | What | Who |
|---|---|---|
| 1 Transcription | language, script, every audible lyric instance | Gemini 3.7 Flash (audio), OpenRouter |
| 2 Alignment | lyric-aware timing | Gemini + local tools |
| 3 Gloss-first translation | word gloss map + semantic frame (agent, action, patient, negation, image) → English | Gemini 3.7 Flash, high reasoning, one call per song |
| 4 Adversarial review | separate call, cannot rewrite, blocks publication | Gemini (same family) |
| 5 Publish | `songs/<slug>/data.js` popups + English segments | code |

Output: the catalogue of about 265 readers and 6,741 popup definitions
(`LIBRARY_REPAIR_TASKS.md`, inventory at `77634641`).

### 1.2 Generation 2: source-first library repair (22–25 Oct; 105 commits on 22–23 Oct)

`b1bfa665` "Add bounded source-first library repair engine and lexical retrieval"
(+24,361 lines in 52 files). This generation added:

- dictionary evidence: Platts, Singh and the Madras Tamil Lexicon via DSAL
  (`dictionary_corpus.py`), plus VCP/SKD from prakriya;
- embedding ranking of candidate senses;
- typed review with scoped repair (`bhakti_semantic_repair.py`);
- word accountability (`bhakti_word_accountability.py`);
- explained retention (`46ab0a8c`, `82b7326d`).

Shared policy went from v1 (`b1c90598`, 22 Oct) to v8 (`82b7326d`, 23 Oct) in seven
commits. The paid work was a sequence of bounded "qualification" runs on single lines,
mainly the Rehnā *ṭhikānā* line and the Har Jīu agency line.

### 1.3 Generation 3: the meaning-first engine rebuild (27–29 Oct; never committed)

`docs/TRANSLATION_ENGINE_PLAN.md` §0–§9 and the audit §1:

| # | Stage | Code / model |
|---|---|---|
| 1 | Reviewed source and performed order | code (`bhakti_native_meaning.source_context`) |
| 2 | Source evidence: DSAL bilingual dictionaries, VCP/SKD, 209-passage Hindi usage index | code, HTTP, cached |
| 3 | Source gloss and native-language meaning (`native_meaning`, per-token popups, name references) | **Gemini 3.7 Flash**, scoped **Gemini 3.1 Pro** retry |
| 4 | Native meaning → English concept retrieval over WordNet 3.1 (117,791 synsets): dense (E5-small ONNX, LaBSE, Google `gemini-embedding-001`) plus FTS5/BM25 | code + encoders (`bhakti_reverse_dictionary.py`) |
| 5 | Writer: word / compositional phrase / transparent compound (Joycean) / retained term / proper name, with paraphrase and evidence IDs | **Flash**; optional DeepSeek Node tool-loop (`bhakti_dsh.py`) |
| 6 | Independent typed review → scoped repair | **Flash or Pro**, then **Codex CLI `gpt-6-astra`** (`bhakti_codex_review.py`) |
| 7 | Acceptance → SQLite term memory → private preview → zero-call replay | code (`bhakti_term_memory.py`) |

Coordinator: `bhakti_pipeline.complete_semantics` → `bhakti_semantic_repair.complete`.
The engine modules total about 32.8k lines of code; `bhakti_pipeline.py` alone has
8,073.

### 1.4 What was tried, in order, and what was abandoned

| When | Tried | Outcome |
|---|---|---|
| 20 Aug | "Polish English across all readers": 134 of 462 lines rewritten (`715caeba`, 17:28) | reverted 16 minutes later (`2fb5cdc1`, 17:44): the rewrite flattened owner-approved images |
| Aug | Together audio route | abandoned (`TOGETHER_AUDIO_QUALIFICATION.md`) |
| 22 Oct | Gemini 3.7 vs 3.8 on four lines | kept 3.7. Both models reported "full fidelity" while making the purified mind the sin-cutting agent, and both gave bare "Nanak"/"Govinda" popups (`GEMINI_MODEL_QUALIFICATION.md`) |
| 22 Oct | cheaper medium-reasoning reviewer | failed: missed the known extra "true", truncated at 7,032 of 8,174 tokens, $0.1255 (`ee2714a6`) |
| 23 Oct | dictionary-grounded writer runs | the writer still produced "true resting place" (`5c553b0e`), and the Hindi glossary still added an unsupported qualifier. Hindi, Punjabi and Tamil runs stopped at validators before review (`4dfb22f8`). Task spending reached $3.92 (`e399011d`) |
| 27–28 Oct | E5 and LaBSE dense indexes | E5 kept 0/7 of the expected narrower concepts in its initial shortlist and LaBSE 1/7, so neither was qualified. Google embedding-001 was chosen for V9 |
| 28 Oct | `gemini-song-v1…v4`, `next-song-trial-v1…v6` | V6 passed the machine pipeline and zero-call replay, but its reviewer approved a lost "O brother" and amplified frames |
| 28–29 Oct | reviewer diagnostics (Flash, Pro, free critique, two-scope) | 0 of 3 planted defects detected. The Flash/Pro reviewer was abandoned for Codex |
| 28–29 Oct | `dictionary-repair-song-v1…v11`, DeepSeek pilot | each run held on a new defect. V11: Flash spent 31,454 of 32,753 completion tokens on reasoning, and Pro wrote its "native" summaries in English |
| 29 Oct → now | nothing | the plan names five contradictory next steps. The rebuild is uncommitted |

---

## 2. What failed and why

### 2.1 Outcome, measured

- **Generation 3:** 0 accepted songs after about 22 bounded trials. Deduplicated
  ledgers: $6.84 generative + $0.28 embeddings for the rebuild, $18.20 across all 78
  Bhakti ledgers, plus at least 8 Codex subscription runs of unknown cost (audit §3.1).
  The term memory was never populated, because promotion into it requires an accepted
  song (audit §5).
- **Generation 2:** no reader qualified. The 23 Oct bounded runs ended in validator
  holds or reviewer misses (commits above).
- **Generation 1:** it shipped volume but not trusted quality. The 27 Oct inventory
  marks 243 of 265 readers review-needed and 11 repair-needed; 2 are protected
  (`LIBRARY_REPAIR_TASKS.md`). The owner's August objections were all model output
  that had passed the model review:
  - *pati* → "Lord" everywhere;
  - "adamantium";
  - *Sarasvatī* glossed as "pronoun or untranslatable";
  - *buddhi* glossed by repeating itself;
  - *māyā* → "worldly illusion";
  - "tainted" with unintended associations.

  (The owner's recorded requirements, private.)

### 2.2 Design failures (root causes)

**D1. Wrong unit of work: a whole song per call, with meaning re-decided every time.**
Source meaning, popups, English and review all ran over the whole song in one request.
- Prompts were 150–470 KB. One writer prompt was 294 KB with 73 full Platts entries.
- 47–67% of output bytes were repeated bookkeeping (audit §3.3.2;
  `TRANSLATION_COMPONENT_AUDIT.md`: 10,569 of 22,185 writer-row bytes restated
  unchanged glosses).
- Large requests exhausted the model's reasoning budget: V11 used 31,454 of 32,753
  tokens, and the 22 Oct Gagan run used 15,725 of 16,384.
- There was no per-word or per-sense decision that could be made once and reused. The
  owner had asked for exactly that: a decision made once and reused, not re-made
  every time.
- Memory was gated on whole-song acceptance, so one bad line in nine kept the memory
  empty.

**D2. Cheap one-shot models were asked for judgement, and for the review of that
judgement.**
- Flash did source meaning, writing and review. Pro was the fallback.
- On known-answer tests the model reviewers failed:
  - Flash two-scope: approved the defects.
  - Pro: approved both the defective and the corrected input, 0 of 3 planted defects
    ($0.372).
  - Pro free critique: blanket approval (`TRANSLATION_ENGINE_PLAN.md` l.715–735).
- Self-certification failed the same way. Generation 1's drafting models reported "full
  fidelity" over a wrong agent, and V6's machine acceptance hid a lost address.
- Codex `gpt-6-astra` found real defects but over-objected (7 supported, 2 mixed, 2
  questionable of 11), and 2 of 5 invocations timed out.
- No reviewer was ever qualified on discrimination: catching planted defects while
  passing clean controls.

**D3. Embedding retrieval stood in for meaning and did not deliver it.**
- The owner's requirement was a retrieval trace: the word is found by search, not
  assumed to be known by the model.
- Bhakti answered with dense retrieval from model-written "native meaning" summaries.
- Results:
  - E5 shortlist kept 0/7 expected concepts and LaBSE 1/7 (`TRANSLATION_WORKFLOW.md`).
  - A Sanskrit summary for √yuj returned no yoke or join concept in the top 16.
  - A Hindi summary put "yoke,link" at rank 8.
  - Plain FTS returned `yoke` at rank 1 in 34 ms (audit §2.3).
- The dense channel cost 5.6 GB of experiment indexes and 934 embedding calls without
  becoming the source of a chosen word.
- Separately, exact lemma lookup delivered senses in WordNet ID order: "land" → farming,
  "world" → humanity, "remain" → unchanged state (`TRANSLATION_COMPONENT_AUDIT.md`,
  "What failed").

**D4. Fail-closed gates on one-shot structured output, with no repair loop.**
- Of the 22 stops, about 12 were engineering and 11 were host-contract strictness:
  fenced JSON, missing arrays, echoed IDs, a plural "seekers", span containment, a
  lemma limit of 4 against 6 requested, a byte limit (audit §3.2–3.3).
- There was no self-repair loop. In V9 a scoped Pro retry received all six diagnostics
  and repeated them. Most stops became a human fix, then a new paid run, which hit the
  next edge.
- `bhakti_pipeline.py` has 314 `raise`/`_require` sites and `bhakti_semantic_repair.py`
  has 132.
- The contracts changed faster than they were qualified:
  - policy v1 → v8 in 23 hours (`b1c90598` 22 Oct 14:13 → `82b7326d` 23 Oct 13:17), then v9 uncommitted;
  - source contract 6 → 8;
  - writer input 10 → 13;
  - review input 3 → 6.
- Provider structured-output schemas failed with HTTP 400 three times before inference.
- Result: "no run was stopped by a linguistic judgement alone until V6/V8". The gates
  used up the budget before the translation question was ever asked.

**D5. A qualification loop with no exit, recorded as a growing plan.**
- About 22 trials ran on one nine-line song; the scope never widened.
- `TRANSLATION_ENGINE_PLAN.md` grew from 24,028 B (22 Oct) to 181,871 B (29 Oct), 7.6×.
  Of that, 54% is dated run log, with 8 "current step" declarations, at least five
  mutually contradictory (audit §6).
- `TRANSLATION_COMPONENT_AUDIT.md` (54 KB) and `TRANSLATION_WORKFLOW.md` (36 KB) restate
  the same runs.
- No rule said "after N failed trials, change the design or escalate".

**D6. Thin, borrowed source evidence.**
- Only 51.97% of popup definitions are in a language with any dictionary adapter.
- The adapters are bilingual (Platts, Singh). The owner had asked that Sanskrit-to-English
  dictionaries not be used as sources of meaning.
- Sanskrit witnesses cannot establish Hindi or Punjabi usage, so the model filled the
  gap, which is the D2 problem again.

**D7. Automated rewriting of approved text.** The 20 Aug polish rewrote 29% of lines
(134/462) and had to be reverted the same quarter-hour. The owner-lock
(`data/editorial_baselines.json`) came after this, not before.

### 2.3 Implementation failures

- **I1. Never committed.** Today, `git status` lists 281 entries and `git diff --stat`
  shows 137 files, +13,963/−3,866, all from 27–29 Oct. HEAD's plan is the 22 Oct
  version.
- **I2. Red suite.** This post-mortem ran every test file under the documented pinned
  runtime: Python 3.12, `scripts/requirements-translation.txt`, 8 files in parallel,
  2 min 41 s wall.
  - Results: 2,714 tests: 1,588 pass, 432 fail, 694 error (**41.5% red**); 130 of 265
    test files red.
  - 456 errors come from an uncommitted schema tightening that forbids
    `preserve_in_english` while 50 fixtures still emit it; 270 failures are one UI
    template regex.
  - The documented `.venv-translation` does not exist, and system `python3` (3.14)
    lacks `jsonschema`, so the literal `python3 -m pytest -q` cannot pass in this
    environment.
- **I3. Transport.** `urlopen(timeout=300)` is a per-socket timeout, not a wall deadline
  (`GEMINI_MODEL_QUALIFICATION.md`). Codex CLI timed out three times.
- **I4. Cache identity.** Duplicate witnesses and path-bound receipt identities caused 4
  stops, and one change re-queued 5 lines instead of 1.
- **I5. Tool loop.** The writer made zero tool calls in v4. The worker's undisclosed
  4-lemma limit killed v5.
- **I6. Accounting overhead.** Reservations versus charges, duplicated ledger rows (158
  of 1,462), and unknown subscription cost all took effort to reconcile.

---

## 3. What worked and is worth reusing

| Asset | Path | Why |
|---|---|---|
| WordNet FTS reverse lookup | `bhakti/scripts/bhakti_reverse_dictionary.py` `LexicalSearch.search` (l.599), store `.transcription/reverse-index/wordnet-3.1-multilingual-e5-small/entries.sqlite` | the one retrieval channel that finds the obvious word (yoke, rank 1, 34 ms). Already consumed by prakriya `scripts/lookup/lookup.py` l.45, l.1091 |
| English-register policy v9 | `bhakti/scripts/bhakti_translation_policy.py` `RULES` l.30–134, `SENSE_DECISION_RULES` l.18 | sense before inflection; uncommon attested English is eligible; epithet vs name; the *pati* rule (relation from grammar, not a stock "Lord"); retention needs an explicit loss argument; **unresolved meaning is reported, never disguised as retention**; a dictionary entry gives possible senses only |
| Joycean rules and record shape | `RULES` (formation paragraphs); the Joycean walkthrough records (private run records) | parts + relation + paraphrase; "attested parts do not make the whole attested"; reject a coinage that adds an image. Each walkthrough records rejected neighbours: *fresh-lotus-eyed* against lotus-born (resemblance → origin), lotuseer (adds a seer), lotus-eyed (drops freshness) |
| Popup hygiene | `bhakti/scripts/gloss_policy.py` `PLACEHOLDER_GLOSSES` l.15, `FICTIONAL_COINAGES` l.17, `MEANING_ONLY` l.53 | bans "proper name", self-repeating glosses and comic-book coinages, the owner's August complaints in code |
| Typed review issues | `bhakti/scripts/bhakti_semantic_repair.py` `issue_schema` l.679, `REVIEW_GUIDANCE` l.693 | five kinds (gloss_sense, frame_relation, english_realization, english_mapping, unresolved_evidence); "do not prescribe a rewrite"; an issue authorizes only its scoped repair |
| Term-memory schema | `bhakti/scripts/bhakti_term_memory.py` `record_accepted` l.195, `lookup` l.228, `withdraw` l.277 | keeps language, sense, context and alternatives separate; withdrawal is explicit; reuse is not proof |
| Owner locks | `bhakti/data/editorial_baselines.json`, `data/translation_conventions.json` (42 reviewed occurrences by line and word index) | approved wording cannot be silently rewritten (lesson D7) |
| Recovered owner requirements | a private record in the bhakti project | dated owner instructions on meaning-first search, once-only decisions, Joycean words, connotation and retention |
| Transport lessons | `bhakti/docs/GEMINI_MODEL_QUALIFICATION.md` "Operational decision"; `process_song_gemini.py` `_remaining_timeout` l.190 | subprocess wall deadline; save raw bytes before parsing; unknown outcome ≠ free |

Not reusable for the Gītā:
- the song coordinator and audio/timing code;
- DSAL bilingual adapters;
- Gemini routing and ledgers;
- the dense E5/LaBSE/Google indexes (unqualified; see D3);
- `seal_meaning`/`project_meaning`, which matter only on the later interpreter route of
  spec §§1–2.

---

## 4. Each lesson against the Gītā pipeline

Status key: **No** = the Gītā pipeline does not repeat it; **Partly** or **Yes** = a
concrete change follows. The Gītā evidence comes from the files named, from tests run
today (prakriya `tests/lookup` + `tests/gita_kit`: 114 passed in 10.4 s; vedanta
`scripts/gita/tests`: 18 passed in 7.2 s), and from the chapter-12 acceptance run in
progress (queue: 7 lexicon done, 5 running, 12 lexicon-review pending at the time of
writing).

| # | Bhakti lesson | Gītā status | Change |
|---|---|---|---|
| L1 | Whole-song unit; meaning re-decided per occurrence; memory gated on acceptance (D1) | **No** for the main path: lexicon-first, one decision per lemma-sense, frozen before verses (plan §7.2.2), 5-verse shards. **Partly** for inline decisions: about 790 lemmas are decided inside verse jobs (RUNBOOK §9), and shards running in parallel can decide the same lemma differently. Divergence is detected only after acceptance (`scripts/gita/run_pipeline.py` l.176) | In stage A, give each inline lemma one owning shard (its first occurrence). Other shards use the owner's decision or file a lexicon request. This prevents conflicts instead of reworking accepted shards |
| L2 | Judgement and review by unqualified models; no reviewer ever shown to discriminate (D2) | **Partly.** Capable tool-using agents judge, in separate pools that never review their own work (RUNBOOK §3), and the ch12 pilot's reviewers found 70 findings incl. 8 S1. But nothing measures a reviewer against known answers: there is no planted-defect or clean-control set in the plan, briefs or standard. The 5% post-scale audit (plan §13.4.6) is the same class of agent with no known answer | Add a **reviewer canary**. Seed the review pool with one shard holding known defects and one known-clean control. Take the defects from the ch12 pilot's real S1s ('wait upon' for the governing verb, statements turned into questions, a dropped lyap) and from Bhakti's own (an added qualifier like "true", a lost vocative). Require every planted S1 caught and no S1 on the control before stage C scales; re-seed every ~20 shards. Record the over-objection rate too: Codex's failure was false S1s |
| L3 | Embedding retrieval standing in for meaning; owner wants a real search trace (D3) | **No** on embeddings: the kit's `english` is FTS over seven monolingual English sources plus Bhakti's WordNet store, and `define` returns the headword's own entry (spec §0.4 item 4, §0.6). **Partly** on the trace. Acceptance feedback #25: "`english --rich` weak (off-target rare words); useful rich words came from the agent's own ideas + define". SCHEMAS records the chosen `plain`/`rich` loci but not the queries run or what they returned, so nobody can tell found from remembered | (a) Have `lookup.py english/define` append each call to `internal/gita_pipeline/logs/<job>.lookups.jsonl`, keyed by a `GITA_JOB` environment variable. (b) In `validate_job.py`, require at least one `english` query per decided sense, and require every cited locus to appear in that job's `define` output. (c) Add a `candidate_origin: retrieved \| proposed_then_defined` field. Proposals stay allowed (Bhakti's own finding was that retrieval must be advisory), but labelled honestly. (d) Add the thesaurus-first rich search of feedback #25 (Roget/Moby groups of the plain word, then `define` each) |
| L4 | Fail-closed gates on one-shot output; contracts changing mid-run (D4) | **Mostly no:** workers see the validator message and repair up to 3 times, and files replace provider structured output. **Partly** on drift between tools, briefs and validators, which is already showing in the acceptance run: `define` prints WordNet loci the validator rejects (#24); the brief names a nonexistent `KIT verse packet` (#1); `meaning page` needs an undocumented `--json` (#2); worked-example loci are stale (#5); the `KIT=` shorthand cannot be pasted in zsh (#19). Job records carry no hash of brief, schema or validator (`scripts/gita/queue.py` fields: id, type, brief, inputs, output, validate) | (a) Add a contract test that runs every command quoted in the briefs and passes each worked example through `validate_job.py`; make it part of RUNBOOK §1. (b) Stamp each job with the sha256 of its brief, SCHEMAS and validator when claimed. A changed hash re-validates done jobs before merge. This is the pilot's lesson 1 (12 of 53 rows changed while the version did not) made mechanical |
| L5 | Endless qualification loop; plan bloated with run history and competing "next steps" (D5) | **Partly.** `GITA_FULL_TRANSLATION_PLAN.md` is 56 KB with 11 sections "amended/replaced 2026-11-08" in one day. It carries run history (§17–§18) and a RUNBOOK stub (§7.10) that duplicates `RUNBOOK.md`. Spec §0.4 places code in `src/prakriya/lookup/`, but it lives in `scripts/lookup/`. The quality halt (plan §10: >10 findings or >1 S1 per 100 cards → "reopen the brief") has no exit bound | Move §17–§18 into a dated history file, keep one status line in the plan, and delete §7.10 in favour of `RUNBOOK.md`. Correct the §0.4 path. Bound the halt: at most two brief or tool revisions per halted chapter, each re-measured on the same chapter, then escalate to the owner with the numbers, never a third silent round |
| L6 | 137-file engine never committed (I1) | **Yes, repeating now.** Untracked in vedanta-timeline: `scripts/gita/` (5,135 Python lines), `docs/gita_briefs/`, `docs/GITA_FULL_TRANSLATION_PLAN.md`; the standard is modified (+627/−96). Untracked in prakriya: `scripts/gita_kit/`, `scripts/lookup/`, `tests/gita_kit/`, `tests/lookup/` (6,107 lines) and `docs/TRANSLATION_PIPELINE_SPEC.md` | Commit both toolchains on a branch before the full run, with the owner's authorization. This is a reproducibility problem, not only a backup one: `scripts/deploy_gita_chapter.sh` and `scripts/build_gita_chapter_reader.py` are themselves untracked. The script runs the main checkout's builder against an `origin/main` worktree (l.58, l.103), so a published chapter cannot be rebuilt from git |
| L7 | Red suite under a runtime that does not exist (I2) | **No.** The setup tests are green on the system `python3`, and RUNBOOK §1 makes them a precondition | Keep it so. Add the contract test of L4 |
| L8 | Prompts and outputs dominated by evidence and bookkeeping (D1) | **Partly.** The pilot measured 62% of producer model time spent on JSON. Lean output plus a code expander fixed that (spec §0.6). Acceptance feedback #18: meaning pages up to 40 KB repeat full kośa text, and "most wall time spent reading" | Add a compact per-lemma summary view: one line per kośa group, Dhātupāṭha artha, and the distinct commentator glosses, with loci, linking to the full page on demand |
| L9 | Identity errors (span containment, duplicate witnesses, cache churn: 4 stops) (I4) | **Partly.** The concordance and inventory match substrings: "ās" pulls in chapter-1 words; *dhyāna* ← *madhyāni*; *√hṛṣ* ← *dhṛṣṭaketu*; finite forms paired with roots; dvandvas listed as lemmas (#3, #15, #21, #23) | Build the inventory and concordance from the grammar oracle's lemma and root for each analysed pada, not from string matching, before the full stage B |
| L10 | Decisions made in the wrong order (writer before source settled) | **Partly.** Compounds get decided before their member lemmas (#13, #20) | Treat compositional compounds as non-lemmas whose sense code composes from members. Only lexicalised compounds get entries, and they are scheduled after their members' batches |
| L11 | Automated rewrite of approved text (D7) | **Partly.** The taste review flows through lexicon edits, a sweep and a diff re-review (plan §7.2.5), which is right. But acceptance-run lexicon work is already changing published ch12 wording: *kāṅkṣ* "long for" → "yearn for" changes 12.17, and existing rows contradict ch12 (#16) | Any lexicon change that alters a published or owner-read line must list the affected loci and wait for the owner, the equivalent of Bhakti's `editorial_baselines.json` |
| L12 | Self-certification by the drafting model (Generation 1) | **No.** Producers never certify their own work. Single-worker mode states that its review is not independent (MASTER_PROMPT) | — |
| L13 | Bilingual dictionaries as meaning authority (D6) | **No.** Monolingual Sanskrit evidence (kośa, Dhātupāṭha, Dhātuvṛttis, Nirukta, commentators) is primary; MW and Apte are "staging, locating aid" (spec §0.4). Five ch12 cards still rest on Apte/MW (plan §17.2, task G1.6) | Finish G1.6 before chapter 12 counts as passed |
| L14 | Unresolved meaning disguised as retention (Bhakti RULES) | **Partly.** The three preserve tests (LEXICON_BRIEF step 4) cover a disputed referent. No field records "meaning not established from the evidence"; `skip` covers only wrong analyses | Carry the Bhakti rule into LEXICON_BRIEF step 4: an unresolved sense is reported as such (S1 for the reviewer), never preserved as if decided |
| L15 | Unknown cost (subscription runs uncounted) (I6) | **Partly.** "The lead reports it if the runtime shows it" (RUNBOOK §9) | Write wall time, and tokens where visible, into each job's done record. The runbook's 245 agent-hour estimate then gets checked against what was actually spent |

### What "done properly" means, in priority order

1. Commit both toolchains (L6).
2. Build the inventory and concordance from the oracle (L9) and settle compound order
   (L10), before the full lexicon.
3. Add the brief/validator contract test and hash stamping (L4).
4. Run the reviewer canary before stage C scales (L2).
5. Add the lookup trace and candidate origin, so "we're literally finding a word" can
   be checked (L3).
6. Hold any change to published lines for the owner (L11), and bound the quality halt
   (L5).

Items 1–3 are deterministic engineering that removes the Bhakti failure class, where a
run stops on a clerical issue. Items 4–5 address the failure Bhakti never solved:
trusting the judgement.

---

## Ten-line summary

1. Bhakti tried three times: a Gemini song pipeline (Aug), a source-first repair engine (22–25 Oct) and a meaning-first engine rebuild (27–29 Oct).
2. The rebuild produced 0 accepted songs in about 22 trials on one nine-line song ($6.84 + $0.28 embeddings; $18.20 across all ledgers); August's 265 readers remain 243 review-needed and 11 repair-needed.
3. Root cause 1, unit of work: a whole song per one-shot call, re-deciding meaning each time, with memory gated on whole-song acceptance, so it stayed empty.
4. Root cause 2, judgement: Gemini Flash and Pro wrote and reviewed. Reviewers caught 0 of 3 planted defects; Codex caught real ones but over-objected.
5. Root cause 3, retrieval: dense embeddings were weak (E5 0/7, LaBSE 1/7; nothing for Sanskrit), while plain FTS found "yoke" at rank 1.
6. Root cause 4, gates: about 12 of 22 stops were engineering, mostly host-contract strictness with no self-repair loop. Policy went v1→v9 in a week and the plan grew 7.6× with five contradictory next steps.
7. Implementation: 137 files uncommitted; today's suite has 2,714 tests and is 41.5% red (456 errors from one uncommitted schema change); the documented runtime does not exist.
8. Reuse: WordNet FTS, policy v9 RULES (register, *pati*, retention vs unresolved, Joycean), the Joycean walkthrough records, gloss_policy hygiene, the typed review issues, the term-memory schema, owner locks and the recovered owner requirements.
9. The Gītā pipeline already avoids the core errors: lexicon-first, capable agents with validator feedback, FTS over seven monolingual sources, Sanskrit evidence primary, green tests.
10. It is repeating Bhakti in five places: an uncommitted toolchain, no reviewer canary, no retrieval trace, brief/tool/validator drift, and a plan accreting history. The fixes are in §4, in priority order.
