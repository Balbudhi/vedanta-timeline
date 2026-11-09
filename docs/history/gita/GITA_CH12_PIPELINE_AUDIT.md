# Gītā chapter 12 pilot: audit of the process

Date 2026-11-08. Auditor role only: nothing here is a translation, and no producer,
review, policy, tool or reader file was changed. The audit covers the run that built
`gita/ch12/` (09:32–11:27 local time, UTC−8), the owner's verdict on it (some words poorly translated, the run far too
slow, the process itself at fault), and what must change before the other 680 verses are translated.

Section 5 is written as **amendments to the existing documents** (the plan, the
standard, the briefs, the tools). It is not a competing plan. The lead applies or
rejects them, and the owner decides the items marked for the owner. The meaning-review
round started at 11:35 (`MEANING_REVIEW_BRIEF.md`; four agents were still running
while this audit was written) is out of scope. No `meaning-review-*` file existed
during the audit.

## 0. Evidence and method

Files read in full or in their decision-bearing fields:

- the plan `docs/GITA_FULL_TRANSLATION_PLAN.md`, all of it
- the standard `docs/SANSKRIT_TRANSLATION_STANDARD.md`
- the four briefs, the four producer shards, the four reviews, `packet.json` (structure only),
  `devanagari-collation.json`, `owner-review-queue.json` and `deviations.json`, all in
  `internal/sanskrit_reviews/gita/ch12/`
- the tools `prakriya/scripts/lookup/lookup.py`, `scripts/build_gita_chapter_packet.py`,
  `scripts/build_gita_chapter_reader.py`, `scripts/repair_kashika_loci.py`,
  `scripts/check_gita_terms.js`, `data/glossary/term_policy.json` and `scripts/audio/*`
- the built output `gita/ch12/verses.js`, `apparatus.json`, `audio.js` and `index.html`
- the reader `assets/gita.js`
- the source witnesses for spot checks (Śaṅkara's bhāṣya and the Apte/MW kośa records)

The agent transcripts of this session (local, not published) are also evidence: 28
transcripts covering 4 producers, 4 reviewers, 4 fix agents, the audio agent and the
meaning reviewers. They give start and end times, tool calls by kind, output tokens
and the lead's mid-run messages. I counted the producer and review JSON with scripts
in the session scratchpad, so every count below can be reproduced from those files.
Where a number is an estimate rather than a count, it is marked **est.** and its
derivation is given.

Pilot size: 20 verses, 244 cards, 155 wording records with 642 candidates, 92 cards
under a policy row, 65 forks (12 open), 140 deviation records and 16 fallbacks. The
producers cited 2,280 evidence items: 1,166 sūtra lines, 646 Kāśikā references (52 as
separate items, the rest attached to sūtra items), 181 Dhātupāṭha records, 348 Cologne
kośa entries, 411 commentator quotes, 52 BORI lines and 62 others.

## 1. Failure catalogue

Each entry gives **what and where**, **caught by and when**, **root cause**, **cost**,
**systemic?** and **fix** (with a pointer into §5).

### 1.1 The 70 review findings, by class

Round 1 had 68 findings and round 2 added 2 (06-10 F23, F24). Severity: 8 are S1,
31 are S2 and 31 are S3. By shard: 01-05 has 21 (3 S1), 06-10 has 24 (2 S1), 11-15
has 13 (2 S1) and 16-20 has 12 (1 S1).

| Class | n | S1 | Findings | Root cause | Code could have prevented it? |
| --- | --- | --- | --- | --- | --- |
| A. Late term-policy rows or senses | 8 | 3 | 01-05 F2 (duḥkha.hardship), F3 (para), F4 (upasana); 06-10 F1 ('worship' vs new upasana row), F3 (para), F4 (parama/terms[]); 11-15 F12 (viśiṣyate across readers), F13 (eva 'indeed' vs 'alone') | 12 of 53 rows were added or changed after production began (D1, D2, D9) | Yes: lemma inventory and rows decided before production |
| B. Undecided line-style conventions | 5 | 1 | 01-05 F15 (placement of 'and'); 06-10 F2 (`hence}{forth` vs one multi-index slot), F19 (epithet capitals), F20 (articles with preserved nouns); 11-15 F11 (action/actions) | the standard has no line-convention section (D4–D6, D14) | Yes: rules in the standard plus builder checks |
| C. Consequences of tool defects | 6 | 0 | 06-10 F8 (Kāśikā loci), F12 (neighbouring headwords), F23 (vārttika moved by repair); 11-15 F5, F6 (false "term missing" from the lead's checker); 16-20 F5 (118 of 266 Kāśikā loci wrong) | T1–T3, T7 | Yes |
| D. Incomplete or misordered standard derivation chains | 9 | 0 | 01-05 F6 (7.1.3 vs 7.1.5), F7 (8.3.19 vs 8.3.22), F18 (6.1.87 missing), F19 (7.2.97 missing); 06-10 F17 (jas/śas label); 11-15 F7 (7.3.52); 16-20 F10 (6.3.74), F11 (ṇic/iṭ/ṇi-lopa/7.2.117), F12 (8.3.34 vs 8.3.36) | agents hand-writing paradigm and sandhi chains for every card | Yes: reviewed chain tables (§5.5 L-6) |
| E. Locus, quote and lookup hygiene | 13 | 0 | 01-05 F8, F21 (glossaryKey files exist), F13 (wrong BORI line), F14 (line ranges), F16 (kośa locus missing), F17 (4 "unlocatable" fallbacks that were locatable); 06-10 F9 (quote ≠ line), F11 (claim not in MW entry), F13 (Roy deviations missing), F21 ('mind' in a sense paragraph); 11-15 F8 (witness typo normalised), F9 (Madhva variant not on card), F10 (located negative not cited) | no machine chase of citations or completeness in the builder; four reviewers wrote their own chasers | Yes: builder checks B2, B6, B13 |
| F. Grammar judgement | 10 | 3 | 01-05 F12 (3.2.4 vs 3.2.77); 06-10 F5 (two formations of ananyena), F22 (ḍhak untested); 11-15 **F1 (kṣam 1A for divādi 4P)**, **F2 (4.4.98 prescribes yat, not aṇ)**, F4 (yatātmavān formation); 16-20 **F1 (2.1.7 read backwards)**, F2 (śatru split), F3 (bhakta kartari), F4 (māna from √mān) | real Pāṇinian errors or missing parallels (§6.2) | Partly: printing the adhikāra in force would have caught 11-15 F2 (T6) |
| G. Fork records | 7 | 0 | 01-05 F5 (one construal), F9 (wrong attribution); 06-10 F6 (class/open mismatch), F7 (sense closes an open fork), F18 (attribution); 11-15 F3 (mislabelled variable); 16-20 F7 (class 1 misuse) | the fork schema has no machine consistency rules | Partly: builder check B7 |
| H. Wording, meaning, readability | 12 | 1 | 01-05 **F1 ('the summit-standing')**, F10 ('undesignable'), F11 ('everywhere-going'), F20 ('travail'); 06-10 F10 ('steady'), F14 ('uplifter'), F15 ('death-saṃsāra'), F16 ('exclusive … alone'), F24 (ablative slot); 16-20 F6 ('this deathless'), F8 ('longs for nothing'), F9 ('his anguish gone') | no meaning gate; most H findings were judgements the lead asked for, and 7 of the 12 ended "keep" | No: this is the semantic work that should get the time (§3) |

Classes A, B and C (19 findings, 27%) come from decisions and tools that should have
existed before production. Classes D and E (22, 31%) are deterministic and belong in
code. Together that is **41 of 70 findings (59%), including 4 of the 8 S1**. Only
classes F, G and H (29, 41%) are the judgement the agents exist for. Class H was
reviewed only where the lead asked for it.

### 1.2 Decisions taken during the run that belonged before production

**D1. The upāsanā row family (`upasana`, `para`, `parama`).**
- What: the chapter's governing verb upa-√ās / pari-upa-√ās occurs 5 times (12.1,
  12.2, 12.3, 12.6, 12.20). It had no policy row, and the shards rendered it 'wait upon'
  (01-05), 'worship' (06-10) and 'attend upon' (16-20 draft).
- Caught by: the lead at the first `--check-only`, 10:18, and then the reviewers
  (01-05 F4; 06-10 F1, F3, F4).
- Root cause: policy v1 (50 rows) was written in a single call at 09:27, five
  minutes before production (transcript), from the plan's §4.3 seed list. There was no
  lemma inventory of the chapter.
- Cost: 2 S1 and 3 S2 findings. 'worship' had to be purged from the gloss, sense,
  grammar and deviations of 06-10. Shards 11-15 and 16-20 re-edited finished drafts
  after the lead's message at 10:27/10:30 (about 8 agent-minutes). The row was then
  never put to the owner (T16).
- Systemic: yes. Every chapter has governing lemmas that cross shards.
- Fix: a lemma inventory and term dossiers per chapter, decided before production
  (§4.3, §5.4).

**D2. duḥkha as an adverbial accusative (12.5): the 'hardship' sense.**
- What: the row gave 'with sorrow'. The producer objected, and the lead added a sense
  after production.
- Caught by: producer objection; review 01-05 F2 (S1).
- Root cause: senses were enumerated per lemma rather than per occurrence.
- Systemic: yes.
- Fix: the dossier lists every occurrence with its sense (§5.4).

**D3. Conditional protases printed as echo-questions (12.9, 12.10, 12.11).**
- What: "Now, you are not able to compose the citta, steady, in me?" The lead decided
  this mid-run "to avoid inserting 'if'".
- Caught by: no reviewer. It was a lead decision, and there was no meaning gate.
- Root cause: decided without consulting the kośa. Apte `ap90.json#795` s.v. *atha*,
  sense 3, reads "If, supposing, now if, in case, but if (पक्षांतर) … oft. followed by
  ततः … Bg. 12. 9, 11". The kośa cites these very verses for 'if'. Śaṅkara at
  `shankara_gita_bhasya.txt:8506` reads the clause as "… na śaknoṣi cet, tataḥ …".
  The device turns a statement into a question, which is a change of mood (§7.2). The
  card note on 12.11 prints "Lead decision (12.9–12.11)" to the public.
- Cost: three public lines.
- Systemic: yes. Conditional *atha* recurs, e.g. 2.33 and 18.58 *atha cet*, which
  Apte cites in the same entry.
- Fix: standard §7.8 (§5.1).

**D4. Epithets.** Translated etymologically, in lower case ("O son of Pṛthā",
"O winner of wealth"). Caught by 06-10 F19. The standard §1 says to translate epithets
but sets no form. Fix: §5.1 (e).

**D5. One-word English for two Sanskrit words.** The rule is one multi-index slot,
`{10,11:henceforth}`. Caught by 06-10 F2 (S1). This was a slot-syntax rule absent
from the brief and the validator. Fix: §5.1 (e) and builder check B12.

**D6. Preserved terms inside English syntax.** Plural 'bhaktas' (01-05 objection 2),
articles ('the manas', 06-10 F20), the verb forms of a preserved noun ('bears no
dveṣa' for *na dveṣṭi* and *adveṣṭā*, objections in 11-15 and 16-20), and *bhaktimān*
'possessed of bhakti' (16-20 objection). Root cause: a row records one string, not
forms per grammatical category. Fix: `forms{}` in the policy row (§5.4) and the
standard §7.11 (§5.1).

**D7. Compounds matching several rows.** Producers 01-05 and 06-10 independently
invented `terms[]`. The checker reads only `term` (06-10 lead_decisions). Root cause:
schema gap. Fix: §5.4 (`term` becomes a list keyed by member index).

**D8. Distinctness (§7.6).** These were discovered by producers reading each other's
files mid-run:
- 'lodged' was reserved for ā-√viś, so *arpita* became 'placed' by elimination (11-15
  notes_for_lead);
- satata 'ever' versus nitya 'constantly';
- eva 'alone' versus 'indeed' (11-15 F13).

Fix: `reserved_english{}` in the policy (§5.4) and builder check B8.

**D9. Regex detectors repaired mid-run.**
- `sama` hit the upasarga sam-, and `śraddh` missed *śraddadhānāḥ* (16-20 objection).
- `yoga` missed *yogī* (11-15 objection), and √āp missed *āptum*.
- `harṣa` needed 'elated'.
- `udvega` forbids 'fear', yet the slot of *harṣāmarṣabhayodvegaiḥ* must contain
  bhaya's 'fear' (11-15 notes).

Eight rows were modified after 09:32 (yoga, bhakti, śraddhā, harṣa, dveṣa, sama,
prāpti, duḥkha), and three were added. The policy `version` string stayed
`1-ch12-pilot` throughout, so the builder's policy-version check passed while 23% of
the rows changed. Fix: detection by declared lemma, not regex, and a content hash
(§5.4, B1).

**D10. samuddhartā (12.7).**
- What: four renderings in succession: 'uplifter' → 'upraiser' (the lead's fix prompt
  said "'upraiser' is attested"; `define upraiser` prints NO HEADWORD) → 'lifter' →
  'the one who lifts up and out'. Then a round-3 finding (06-10 F24) on the slot split.
- Root cause: attestation judged against a three-dictionary stack (T5), and decided by
  the lead under time pressure.
- Cost: one extra review round on 12.6–12.10.
- Fix: the full English stack (§5.5 L-2) and a dossier decision before production.

**D11. Cross-reader conflicts.** *viśiṣyate* is 'is distinguished' here but 'is
superior' in `gita/ch5` 5.2 (11-15 F12). *eva* is 'indeed' in sthitaprajña/ch5 but
'alone' in ch12 (F13). Root cause: no concordance of the site's existing renderings in
the packet. Fix: `concord` (§5.5 L-5).

**D12. Kāśikā citation density.** Shards 01-05 and 11-15 cite the Kāśikā 25 and 24
times. Shards 06-10 and 16-20 attach a Kāśikā locus to nearly every sūtra (302 and 295
references). The brief never says when the vṛtti is evidence. The two dense shards
absorbed 279 of the 286 Kāśikā repairs (T1). Fix: §5.3 P-4. Cite the vṛtti only when
its example, counter-example or restriction decides the card.

**D13. Evidence schema.** Kāśikā references take four shapes: a separate item, `also`,
`kashika`+`sutra`, and `kashika_quote`. Shards carry 2 to 5 distinct evidence-key
schemas. Each reviewer wrote a chaser to cope. Fix: one evidence schema validated by
the builder (B12).

**D14. Sentences across verses.** 12.3→4, 12.6→7, 12.13→14 and 12.18→19: dash at
the end, lower-case continuation. Negotiated between shards. Fix: standard §7.11.

**D15. Wording records after a row has fixed the word.**
- What: the upāsate record (12.3[5]) has `sense_description` "Śaṅkara 12.3: upāsana
  is sitting long near the object with an unbroken flow of like cognitions". Its chosen
  'wait upon' cites GCIDE "To attend, as a servant; to perform services for".
- Root cause: the chosen word's own definition contradicts the sense the record
  states. The row overrode the discovery step (plan §6), and the brief forbids the
  producer to depart from a row.
- Fix: rows are decided from a dossier (§4.3). The reviewer may raise a "row
  proposal" finding (§5.3 R-3).

### 1.3 Tool defects

**T1. Kāśikā locator offset base** (`lookup.py` `sutra_lookup`, lines 159–189).
- What: the tool applied the projection's offsets on `kashika_upstream.txt` to
  `kashika_collated_clean.txt`. Measured wrong: 118 of 266 loci in 16-20 (44%); 5 of 6
  sampled in 06-10. After the first fix, 4 of 134 were still wrong (06-10 round 2).
- Caught by: reviewers 06-10 (F8) and 16-20 (F5), around 10:40–10:48. Fixed at 10:54,
  then a nearest-line fix, then a repair script. Repair runs at 11:14, 11:21 and 11:22.
- Root cause: shipped without a self-test. The clean file has no sūtra headers, and a
  single line was cited for a multi-line vṛtti.
- Cost: 286 evidence items rewritten (162 in 06-10, 118 in 16-20, 6 elsewhere).
  Reviewer model time on Kāśikā was 6.9 min, fix-agent time 3.0 min, plus round 3 on
  06-10.
- Systemic: yes.
- Fix: L-3 and B3.

**T2. `repair_kashika_loci.py` was lossy.**
- What: the first version chose the sūtra number from the claim before the quote (the
  claim may name a neighbouring rule). When the Kāśikā reference is the `locus`, the
  script overwrites the producer's `quote` with the first 160 characters of the vṛtti.
  That relocated a vārttika cited on line 524 to the vṛtti's opening line 518 (06-10
  F23).
- Root cause: line loci for spans, and quotes rewritten by code.
- Fix: span loci; code never rewrites a quote, and it verifies the quote lies inside
  the span (B2, B3).

**T3. `english` showed neighbouring headwords** (lead's item 2).
- What: the search matches definition text only (`definition:"…"`) and prints the
  headword whose definition matched. Producers cited that definition as the chosen
  word's own.
- Cost:
  - re-anchoring: every chosen word in 01-05, every candidate in 06-10 (F12), 47
    records in 11-15 and 98 candidates in 16-20;
  - 104k fix-agent output tokens (11%) went to `define` calls;
  - residue still in the shard: rejected candidates in 01-05 cite other headwords
    ("constantly" ← *Still*, "joined" ← *Combinate*, "ever" ← *Always*; 25 such
    candidates in 01-05 and 27 in 16-20 by an automated head-mismatch scan, though
    most of those are inflections).
- Fix: L-1 and B4.

**T4. `define` has no lemmatiser and no phrase index.**
- What: `define yoked`, `clinging`, `highest`, `wait upon` and `all-pervading` print
  "NO HEADWORD … not attested in the stack". The brief then requires a Joycean record.
- Effect: 'unmanifest' got Joycean records on three avyakta cards (01-05
  self_review), although it is ordinary English.
- Fix: L-1.

**T5. The English stack is three of the seven planned sources.**
- What: `english.db` holds webster1913 165,271 rows, gcide 179,741 and wordnet3.1
  207,272. Plan §3.2 requires Wiktionary (kaikki), OEWN 2025, Century, Roget and Moby
  as well.
- Effect: attestation judgements went wrong ('upraiser', 'uplifter', 'unmanifest',
  'all-pervading'). GCIDE loci are letter files only (`gcide-0.53/CIDE.W`); the 16-20
  reviewer called them "locatable but weak".
- Fix: L-2.

**T6. `sutra` does not print the adhikāras in force.**
- What: `ashtadhyayi.json` already encodes them. 4.4.75 has
  `type: "AD$यदधिकारः प्राग्घितीयः$51136"`, and 4.1.83 has `AD$…अणधिकारः$43168`.
  `sutra 4.4.98` prints `anuvritti: ''`.
- Effect: 11-15 F2 (S1). The producer cited 4.4.98 for aṇ, though the aṇ adhikāra
  ends at 4.3.168 and 4.4.98 lies under the yat adhikāra.
- Fix: L-4 (code in §5.5).

**T7. Term detector over a joined string** (lead's item 3).
- What: fixed in the builder (per field). The legacy `detectTerms` in
  `check_gita_terms.js:70–75` still joins stem, iast and parts.
- Effect: the lead's checker reported *maitraḥ* and *karuṇaḥ* as lacking `term`. The
  reviewer spent effort disproving it (11-15 F5, F6).
- Fix: B1. Detection by declared lemma.

**T8. Two policy sources of truth.**
- What: `check_gita_terms.js` hard-codes PRESERVE/TRANSLATE tables (lines 19–44). They
  keep *krodha* preserved and forbid 'anger', against plan L7 and `term_policy.json`.
  The standard §8 lists a third version.
- Fix: §5.1 (h). The checker reads only the policy.

**T9. Builder demanded wording records for preserved terms, names and copulas**
(lead's item 5). Fixed with prose regexes: `is_name` matches "epithet|voc.", and
`is_copula` matches a gloss starting "is|are…" (`build_gita_chapter_reader.py:167–171`).
Fragile. Fix: cards declare `word_class` (B12).

**T10. Builder gaṇa regex rejected Ā** (lead's item 6). Fixed with `[PAUĀ]`. Fix: verify
gaṇa and pada against the Dhātupāṭha record id, not a regex (B17).

**T11. Builder "school authority" regex** (line 261) flagged a legitimate grammar reason
(lead's item 7). Root cause: prose regex on a reason. Fix: `reason_class` plus a
structured `basis` field (§5.3), with the reviewer judging.

**T12. Builder published the deviation defences** (lead's item 8). The lead caught this
before deployment, and they now go to private `deviations.json`.
- Residue: the public `apparatus.json` still carries 230 candidates offered by
  secondary translations, 54 of which print the translator's rendering inside `locus`
  (e.g. "Adidevananda 12.1 'ever integrated'"). The `source_note` beside each says
  "quotation not republished".
- Fix: B13.

**T13. Weak pada check.** The builder accepts pada-pāṭha versus saṃhitā at an
edit-distance ratio ≤ 0.16 (line 241). A dropped *ca*, *hi* or *tu* (2–3% of a
90-character verse) passes. Fix: B11.

**T14. Builder fork and sense checks too shallow.**
- The fairness-locus check accepts any fork in the verse (line 265) rather than at
  the named word.
- It does not test class-4-with-`open: true` (16-20 F6).
- It does not scan `sense`, `gloss`, `parts` or `note` for forbidden words (06-10
  F21: 'mind').

Fix: B6 and B7.

**T15. Builder does not chase citations.** The four reviewers did 4,112 citation
checks in round 1 (540, 917, 747 and 1,908). Three wrote their own chasers ("a script
resolved all 504", `chase_0610.py`, `chase2.py`), and 11-15 re-implemented the policy
detector. Fix: B2–B4.

**T16. Owner queue generated from row notes, not occurrences.**
- `owner-review-queue.json` still says under `duhkha.sorrow`: "12.5 duḥkham
  (adverbial accusative) 'with sorrow / sorrowfully'". 12.5 now reads 'with hardship'
  under another sense.
- The mid-run rows `upasana`, `para` and `parama` are absent from the queue, because
  they are not marked `review: pilot`. So the most consequential English choice in the
  chapter, 'wait upon', never reached the owner's queue.

Fix: B14.

**T17. Validators hard-code the reader list** (`validate_gita_slots.js:69`,
`check_gita_terms.js:191`). Plan readiness 4 asks for discovery. Each chapter needs
manual edits. Fix: B16.

**T18. The reader renders neither `forks` nor `sense`.**
- What: `assets/gita.js` `renderVerse` (about lines 224–246) renders only the
  Devanāgarī, the interactive words and the English.
- Effect: 65 forks (12 open) and 20 sense paragraphs are invisible, while 43 public
  cards say "see fork". Plan §13.2 ("the reader sees both") is false for this reader.
- Caught by: this audit. No gate checks it.
- Fix: B10. The presentation change itself belongs to `UI_DESIGN_STANDARD.md`'s owner.

**T19. Unused public apparatus.** `apparatus.json` (1.08 MB) is not loaded by the
reader but sits under `gita/`, which the Pages allow-list publishes. Fix: B13. Either
the reader uses it, or it stays private.

**T20. Audio** (lead's item 10). The aligner needed rule changes for end snapping and
for masking untranscribed speech. The manifest reports 20/20 corroborated and
`provisional`. Missing:
- the per-aligner calibration on known-boundary clips (plan §5.2.4, §15.6);
- the 10% owner listening sample (§5.2.5).

Plan §17.1 says "the audio spot-listening list in `gita/ch12/audio.js`". The file has
none. Fix: §5.2 (f).

**T21. Process language in public cards.** 23 public fields carry pipeline vocabulary,
for example:
- 12.5 *kleśaḥ* note: "Owner's aesthetic gate (F20) …";
- 12.8 *ūrdhvam*: "(lead decision)";
- 12.3 *paryupāsate*: "policy row upasana, term {upasana, wait-upon}";
- 12.9 *cittam*: "Preserved per term_policy";
- 12.7: "`terms` lists both".

Fix: B9.

**T22. Output-token ceiling.** Producer 16-20 hit the output limit at 10:06 and was
resumed. Shards average 300 KB of JSON (1.53 MB for four), most of it citation text.
Fix: §4.2. Code expands citations.

### 1.4 Where the built chapter is weaker than it should be

These are my readings of the built lines, as the owner reads them, with the evidence
the pipeline had and did not use. They say what is wrong and what had to be weighed.
They do not propose renderings.

**W1. upa-√ās / pari-upa-√ās → 'wait upon (on every side)', five times.**
- Register: in current English 'wait upon' is a servant's service. The record's own
  GCIDE citation says so.
- The richest gloss in the evidence is missing from the card. Śaṅkara defines
  *upāsana* at 12.3 (`shankara_gita_bhasya.txt:8411`): *sāmīpyam upagamya
  taila-dhārāvat samāna-pratyaya-pravāheṇa dīrgha-kālaṃ yad āsanam*, that is,
  approaching nearness and sitting long in an unbroken stream of one cognition like
  poured oil. The producer cited it, but it is not on the card.
- The tradition glosses differ by object: at 12.1 Śaṅkara has *dhyāyanti*; at 12.20
  *anutiṣṭhanti*, because the object there is a teaching ("wait upon … this
  deathless").
- 'on every side' renders *pari* spatially where Śaṅkara has *samantāt*.
- One row for a person-object and a teaching-object is a string-constant decision
  dressed as a sense-constant one (plan L2).

**W2. Statements turned into questions** (12.9–12.11; D3).

**W3. Non-finite form drift.**
- 12.6 *saṃnyasya* (lyap) is printed 'renouncing'; the card itself says "having laid
  down completely".
- 12.11 *āśritaḥ* (kta) is printed 'resorting to'. The producer changed it from
  'having resorted to' during re-read.
- 12.4 keeps 'having fully reined in'.
- 'renouncing … in me' is not English. The root image of sam-ni-√as, laying down, is
  on the card, not in the line.
- No reviewer flagged §7.2 here.

**W4. Coinages and calques where attested English exists.**
- 'the everywhere-going' (12.3; the reviewer showed 'all-pervading' is MW's own gloss);
- 'the one who lifts up out of the ocean of death-saṃsāra' (12.7);
- 'relinquisher of all undertakings', 'relinquisher of the fair and the foul' (12.16,
  12.17);
- 'Be one to whom action for me is supreme' (12.10);
- 'make the relinquishment of the fruit of all actions' (12.11; *kuru* plus noun,
  calqued);
- 'this deathless accordant with dharma' (12.20; adjective used as a noun; reviewer
  F6 flagged it and it was kept);
- 'content with whatsoever' (12.19; the unrendered `sense` has to add "comes" to make
  it read).

**W5. Traditional senses flattened or misdirected.**
- 12.16 *dakṣa* 'able'. Śaṅkara at 8618: *pratyutpanneṣu kāryeṣu sadyo yathāvat
  pratipattuṃ samarthaḥ*, able to meet what arises at once and rightly.
- 12.9 *abhyāsa* 'practice'. Śaṅkara at 8506: *punaḥ punaḥ sthāpanam*, placing again
  and again; this is on no public card.
- 12.4 'whose buddhi is the same everywhere'. Śaṅkara at 8426: *sarvatra sarvasmin
  kāle*, *samā tulyā buddhiḥ … iṣṭāniṣṭa-prāptau*, equal in getting the wanted and the
  unwanted. 'the same everywhere' reads as spatial uniformity.
- 12.15 *amarṣa* 'resentment'. Śaṅkara at 8604: *asahiṣṇutā*. The reviewer recorded
  the overtone and kept it "because the row fixes it".
- 12.15 *harṣa*. Śaṅkara's embodied description (*romāñcanāśrupātādi-liṅgaḥ*, hair
  standing on end, tears) is absent from the card.
- 12.1 'the most knowing in yoga' (Śaṅkara *atiśayena yoga-vidaḥ*).
- 12.2 'deemed the most yoked'.
- 12.5 'the travail' (archaic; the card note exposes F20).

**W6. Hybrid Sanskrit–English syntax.** 'bhaktas', 'bears no dveṣa', 'possessed of
bhakti', 'the manas', 'compose the citta, steady, in me', 'a yogī'. For *dveṣa* the
preserve test of plan §4.1 was never run in a dossier. The row came from the
standard's §8 list, and the producers flagged the verb problem twice (11-15, 16-20
objections).

**W7. Depth missing from the cards.**
- Of 145 cards with a root or compound, 104 (72%) show no traditional voice, neither
  commentator nor kośa, in any field the reader displays.
- Examples: *bhaktāḥ*, *upāsate* (12.2, 12.6), *abhyāsayogena*, *dhyānam*,
  *karmaphalatyāgaḥ*, *adveṣṭā*, *nirmamaḥ*, *dakṣaḥ*, *udvijate*, *saṃnyasya*,
  *samuddhartā*.
- The 411 commentator quotes the producers gathered sit in `apparatus.json`, which the
  reader does not load.
- *Essays on the Gita* (`cwsa19_essays_on_the_gita.txt`, on disk, the site's governing
  hermeneutic per standard §6.3) is cited 0 times, and the Nirukta 0 times.
- No card separates the six categories of §6.3.

**W8. The fairness apparatus is invisible** (T18).

**W9. Process jargon in the cards** (T21).

**W10. Words chosen by elimination.** *arpita* 'placed' because 'lodged' was taken
(D8). The record shows the choice was made by the §7.6 constraint, not by the meaning.
Śaṅkara's *sthāpite* happens to support it.

**W11. Measured composition of what producers wrote** (1.195 M characters of JSON):

| Content | Share |
| --- | --- |
| grammar evidence | 26.5% |
| commentary and other evidence | 9.4% |
| forks | 9.0% |
| wording candidates' retrievable text (word, source, locus, definition) | 8.6% |
| grammar strings | 6.3% |
| public card text (gloss, parts, note) | 6.2% |
| deviations | 6.0% |
| kośa evidence | 6.0% |
| wording judgement | 5.3% |
| **English line plus sense paragraph** | **0.7%** |

The text the owner actually reads got less than 1% of the output.

Per-verse reading (A = add or drop, F = form, R = readability, M = meaning lost or
richness):

| Verse | Problems a reader meets |
| --- | --- |
| 12.1 | R 'wait upon … on every side'; R 'the most knowing in yoga'; hybrid 'bhaktas' |
| 12.2 | M 'having lodged the manas' (card: "having caused to enter"); R 'by me deemed the most yoked' |
| 12.3 | R 'the everywhere-going'; R 'wait upon on every side the imperishable' |
| 12.4 | M 'whose buddhi is the same everywhere' (W5) |
| 12.5 | R 'the travail'; M 'the unmanifest way' for *avyaktā gatiḥ* (Śaṅkara: the goal that is the imperishable) |
| 12.6 | F/R 'renouncing all actions in me'; R 'wait upon, meditating on me' (object displaced); R 'with an exclusive yoga alone' |
| 12.7 | R 'the one who lifts up out of the ocean of death-saṃsāra' |
| 12.8 | (reads well) |
| 12.9 | F mood 'you are not able …?'; R 'compose the citta, steady, in me'; M 'practice' (W5) |
| 12.10 | F mood '?'; R 'Be one to whom action for me is supreme' |
| 12.11 | F mood '?'; F 'resorting to'; R 'make the relinquishment …' |
| 12.12 | R 'is distinguished'; 'fruit of action' here vs 'of all actions' in 12.11 |
| 12.13 | R 'bearing no dveṣa'; R "without 'mine'" |
| 12.14 | (reads acceptably) |
| 12.15 | M 'resentment' (W5); R 'on account of whom' |
| 12.16 | M 'able' (W5); R 'looking to nothing' (English 'look to' = rely on); R 'relinquisher of …' |
| 12.17 | R 'bears no dveṣa'; R 'possessed of bhakti' |
| 12.18 | R 'The same both toward a foe and toward a friend' |
| 12.19 | R 'content with whatsoever'; 'the man' for *naraḥ* |
| 12.20 | R/M 'wait upon on every side this deathless accordant with dharma' |

### 1.5 Process and publication failures

**P1. Fix rounds used fresh agents.**
- What: the fix prompts begin "You are the producer applying the independent review".
  These were new agents, not the producers.
- Each spent 12.5–18.5 minutes and 16–36 read-type tool calls before its first edit,
  re-acquiring context the producer already had.
- Cost: est. 40–50 agent-minutes of re-reading across four fix agents.
- Fix: §4.7.

**P2. Lead decisions reached producers after their drafts were finished.** The 10:27
and 10:30 messages arrived as producers 16-20 and 11-15 finished. Six decisions were
applied as rework. Fix: §4.3.

**P3. The shard changed under review.** 11-15 was modified at 10:54 while being
reviewed (`producer_sha256_note`). Fix: §4.6. Shards are frozen when the review
starts.

**P4. Lead edits after acceptance re-stamped the review hash** without re-review
(06-10: one gloss; 11-15: two glosses; `lead_edits_after_acceptance`). Small edits,
but the mechanism lets unreviewed edits pass the gate. Fix: B15. Edits go through
the producer and a diff re-review.

**P5. Hygiene checks ran after acceptance.** `check_gita_terms.js` check F (bare
preserved-term glosses) ran only after acceptance and caused P4. Fix: producers run
the full builder check before handoff (§5.3 P-7).

**P6. The review record is not versioned.**
- Producer shards, reviews, packet, deviations and owner queue are all gitignored
  (`.gitignore` lines 41–50), because they quote copyrighted secondaries.
- The only evidence behind 244 public cards exists in one working tree.
- Fix: §5.8 D-4. Keep the quotations in one private file and commit the rest.

**P7. Not deployed.** The owner asked for the chapter to be published on the site (plan §17:
"published to the Vedanta Timeline"). Plan §16 says "the owner commits". The §8 gate
has no deploy step, and the working tree holds other agents' uncommitted changes
(sahasranama and chinmayananda scripts). Fix: §5.8.

**P8. The plan's §17.1 overstates the pilot.** "the audio spot-listening list in
`gita/ch12/audio.js`" does not exist (T20). "65 fork records" are invisible to the
reader (T18). "every card with a wording record where required" holds only after the
exemptions of T9. Fix: §5.2 (g).

**P9. The meaning gate was absent.** The owner had to supply it (§3).

**P10. No calibration of shard size.** Shards were fixed at 5 verses, and sentence
units happened to fall inside them in ch12. Chapter 2 has longer sentence units, so
shards must follow them (§4.5).

## 2. Why it took so long

### 2.1 Timeline (local time, from the agent transcripts)

| Time | Event |
| --- | --- |
| 09:11 | Owner: build one chapter now (plan §17) |
| 09:22–09:31 | English index built; policy v1 (50 rows) written in one call; packet built; briefs written |
| 09:32 | 4 producers and the audio agent spawned |
| 09:36 | Builder written (during production) |
| 10:06 | Producer 16-20 hits the output-token ceiling and is resumed |
| 10:18–10:34 | Producers finish (46.6, 53.9, 62.3, 58.1 min) |
| 10:18–10:31 | First builder check; policy rows added or changed (upasana, para, parama, duḥkha.hardship …) |
| 10:20–10:35 | Reviewers spawned as each shard lands |
| 10:27 / 10:30 | Lead decisions (6 items) to the two producers just finishing |
| 10:44 | Owner asks why it is not done |
| 10:46–11:06 | Round-1 reviews finish (26, 25, 31, 22 min) |
| 10:47–11:06 | Fix agents spawned (fresh) |
| 10:53–10:55 | `define` added; Kāśikā offset fixed; repair script written |
| 11:11 | Lead re-decides samuddhartā mid-fix |
| 11:12–11:27 | Re-reviews (5.5, 9.6 including round 3, 4.1, 4.5 min); repair runs at 11:14, 11:21, 11:22 |
| 11:27 | Lead edits after acceptance; build |
| 11:32 | Owner: words not well translated; not on the live site |

The production loop's critical path ran 09:32→11:27, **115 minutes**: 62 producing
(the slowest shard), 31 reviewing, 15 fixing, 5 re-reviewing and 2 building. From
the owner's "go" it was 136 minutes. The lead's ≈3.5 h figure also counts ≈1 h of
setup before the go. The meaning round now running adds a full further pass that the
pilot did not budget.

### 2.2 Agent time by phase

| Phase | Agent-minutes | Share |
| --- | --- | --- |
| Producing (4 agents) | 220.9 | 52% |
| Review round 1 (4) | ≈104 | 24% |
| Fix (4 fresh agents) | 77.6 | 18% |
| Re-review (rounds 2–3) | 23.7 | 6% |
| **Loop total** | **≈426 (7.1 agent-h) = 21.3 agent-min per verse** | |
| Audio (parallel, off the critical path) | 32.9 | |
| Lead | ≈1 h setup plus ≈2 h of coordination, policy edits, tool fixes, repair runs and builder fixes | on the critical path |

### 2.3 What the agents' time was spent on

The transcripts give model-generation time attributed to the action that followed it.
This covers about two thirds of producer wall time; the rest is inter-call latency.

| Activity | Producers (141.7 model-min) | Reviewers (91.4) | Fix agents (49.2) |
| --- | --- | --- | --- |
| emitting JSON (Write/Edit, plus scripted edits) | **88.3 (62%)** + 2.9 | 8.6 (python-written review JSON) | 21.9 + 2.2 |
| reasoning text | 29.6 (21%) | 42.6 (47%) | 15.4 |
| grammar and kośa lookups | 5.5 | **22.6 (25%)** | 0.6 |
| English lookups (`english`, `define`) | 2.3 | 0.7 | 1.6 |
| Kāśikā work | 1.4 | 6.9 | 3.0 |
| grep, inspect, read, validators | 11.7 | 10.0 | 4.5 |

Output tokens: producers 2.13 M, reviewers 1.62 M, fix agents 0.93 M.

### 2.4 Deterministic work, semantic judgement, rework

- **Deterministic work done by producers: est. ≈36% of producer time (≈80
  agent-min).** 62% of producer model time was spent emitting JSON. About 49% of that
  JSON is code-derivable: grammar and kośa evidence 32.5%, retrievable wording
  candidate text 8.6%, half of the commentary evidence (locating is code, choosing is
  judgement) and half of the grammar strings (paradigm forms). Lookups add 6%.
  0.62 × 0.49 + 0.06 ≈ 0.36.
- What that deterministic work was:
  - 1,166 sūtra citations, 70% of them standard machinery (sandhi and phonology 26%,
    aṅga operations 16%, saṃjñā 14%, vibhakti 8%, tiṅ 4%, luk 2%). The top 50 sūtras
    account for 58% of all sūtra citations; 8.2.66 is cited 30 times, 8.3.23 27 times
    and 3.2.102 24 times.
  - 646 Kāśikā references, 181 Dhātupāṭha records and 348 kośa entries, all lookups.
  - 642 wording candidates with definitions, all retrievable.
- **Deterministic work done by reviewers: est. ≈42% of reviewer model time (≈44
  agent-min).** Lookups, Kāśikā, grep, inspection and chase scripts. Agents performed
  4,112 round-1 citation checks.
- **Rework caused by tool defects, late policy and hygiene: est. ≈65 agent-min**
  (59% of the ≈110 agent-min of fix, re-review and post-draft rework). It includes
  286 Kāśikā loci rewritten, 145+ wording records re-anchored, the 'worship' purge,
  six late decisions applied to finished drafts and one extra review round.
- **Semantic judgement: the remaining ≈240 agent-min (≈56%).** Most of it went to
  grammar judgement and fork records. As W11 shows, the English line and sense
  received <1% of the output, and no review gate examined meaning, richness or
  readability (§3).

In short, about **44% of the 7.1 agent-hours** was work code should do, or rework
that code and earlier decisions would have prevented. The semantic work that
remained was spent mostly on the half of the problem the owner did not complain
about.

## 3. What the review did not check

`REVIEWER_BRIEF.md` has nine method steps:

| Step | Concern |
| --- | --- |
| 1 | recompute grammar |
| 2 | chase citations |
| 3 | wrong alternatives |
| 4 | policy |
| 5 | slot mapping |
| 6 | wording against the definition |
| 7 | forks |
| 8 | deviations |
| 9 | verbatim text |

None of them asks whether the line reads as English, whether the card carries the
tradition's meaning of the word, or whether the root's image (what the body does)
survives. The verdict rule makes only S1 blocking, and S1 is defined as "wrong or
unsupported claim or distortion". Meaning losses were therefore recorded as S3 or
left out. Concretely:

1. **Readability was never a gate.** The 16-20 reviewer wrote of 'content with
   whatsoever': "archaic … acceptable, owner may find it stiff". Of 'this deathless':
   "does NOT clearly read as a noun phrase … owner decision". Both are severity 3,
   accepted and published. The 06-10 reviewer called 'compose citta steady' "not
   natural English" (F10), and the fix was a pair of commas.
2. **Rows could not be challenged.** The 11-15 reviewer saw that 'resentment' adds an
   overtone Śaṅkara's *asahiṣṇutā* lacks. The finding text reads "fixed by the policy
   row, so no change". The same structure protected 'wait upon' (W1) and 'bears no
   dveṣa' (W6).
3. **Wording was checked against the chosen word's definition, not against the
   tradition's sense.** Step 6 compares the chosen English with the producer's own
   `sense_description`. If that description is thin ('able' for *dakṣa*), the check
   passes. No step asked "what do the commentators on this verse say the word means,
   and does the card show it?" So 104 of 145 root and compound cards ship with no
   traditional voice (W7). Śaṅkara's *upāsana* definition was cited as evidence and
   left off the card.
4. **Form drift in the line was not recomputed.** Recomputation covered the card
   fields (root, affix, morph). It did not cover whether the line renders the form the
   card states: 'renouncing' for lyap, 'resorting to' for kta, a question for a
   statement (W2, W3).
5. **Lead decisions were exempt.** The echo-question device, 'upraiser is attested'
   and 'the one who lifts up and out' arrived as binding instructions. Reviewers
   checked compliance, not correctness (06-10 verdict_note: "Lead decisions … are
   satisfied").
6. **The public surface was not reviewed.** No reviewer looked at what the reader
   renders. So the invisible forks and senses, the 23 jargon fields and the public
   secondary quotations all passed.
7. **Embodiment.** Standard §7.4 says to keep the root's image. The brief's re-read
   checklist asks "does the slot text equal the gloss's sense". It does not ask
   whether the image survived: sam-ni-√as 'lay down', ā-√viś 'make enter', abhyāsa
   'again-placing' and ud-√vij 'start back, tremble' are all on the cards and absent
   from the lines.

The review optimised what it could measure: citations resolve (0 failures after the
fixes), roots carry gaṇa and pada, the policy is obeyed. It produced a chapter that
is grammatically defensible and lexically thin.

## 4. How it should be done for the remaining chapters

### 4.1 Principles

1. Code does everything exact: segmentation candidates, lookups, citation chains,
   loci, chases, policy matching, consistency, counts, public-surface checks.
   Agents assert analyses and choose meanings. Code expands each assertion into a
   cited card. This is the paid-model rule in `/Users/eeshan/Dev/AGENTS.md`, applied
   to agents.
2. Meaning is decided once per lemma-sense, before production, from a dossier. Lines
   are then built from decided senses, so the producer's semantic effort goes to
   construal, word order and readability.
3. The owner decides rows and line style before production and reads the chapter
   after. The owner never meets a decision that was made silently mid-run.
4. One review pass checks grammar, meaning and readability together. Fixes go back to
   the same producer, resumed with its context.

### 4.2 Ordered layers

| Layer | Code | Agent judgement |
| --- | --- | --- |
| L0 witnesses | BORI, Devanāgarī collation, commentaries, secondaries (private) | none |
| L1 lookup | `sutra` with adhikāras and Kāśikā span; `dhatu`; `kosha`; `define` with lemmatiser and phrases over seven sources; `gloss` (commentator glosses per pada); `concord` (Gītā occurrences and site renderings); `chain` (reviewed paradigm and sandhi chains) | none |
| L2 packet | per-pada blocks: pada candidates, root candidates with Dhātupāṭha records, kośa entries, commentator glosses, concordance, prior site renderings, matched policy rows; the chapter lemma inventory; a shard plan aligned to sentence units | none |
| L3 dossiers (before production) | assemble per lemma: occurrences with context, glosses, kośa, Nirukta and CWSA 19 hits, secondaries' renderings, English candidates with definitions | the dossier agent writes the senses per occurrence, the root image, the three-test result, proposed forms per category, and checks distinctness |
| L4 owner gate 1 | builds the decision sheet: new and changed rows, line-style sample | the owner decides; the lead freezes the policy version (hash) |
| L5 production | expands analysis records into cards: evidence, chains, Kāśikā spans, definitions, glossary keys; runs the builder check per shard | the producer writes the analysis record per word (pada, root id, affix ids, compound and vigraha, kāraka, sense id, English choice and why, the card's tradition line), forks, the line and the sense |
| L6 review (one pass) | builder report: chases, schema, policy, consistency, form warnings, public hygiene | the reviewer recomputes grammar on the expanded cards, then meaning and richness against the dossier, readability, forks; may file row proposals |
| L7 fix | diff of the shard before and after | the same producer resumed; the same reviewer resumed for a diff re-review |
| L8 build | fail-closed build: B1–B18 | none |
| L9 audio (parallel from L0) | alignment, corroboration, calibration report, listening sample | owner listening |
| L10 owner gate 2 and deploy | deploy script; owner queue from occurrences | owner reads; row changes flow back through L3–L4 and a mechanical sweep |

### 4.3 What must be decided before production

1. **Lemma inventory per chapter (code).** Every lemma with its occurrences across the
   Gītā, its matching policy row or none, and its prior renderings in published
   readers.
2. **Term dossiers (agents, parallel)** for every lemma without a row, every row
   marked `pilot`, and every content lemma occurring three or more times in the
   chapter. For chapter 12 that set would have included upāsanā, para/parama,
   abhyāsa, dakṣa, udāsīna, kleśa and dveṣa (verb).
3. **Policy rows** with forms per grammatical category, reserved English
   (distinctness) and `status: owner-decided`.
4. **Line-style rules** in the standard (§5.1): mood, non-finite forms, epithets,
   multi-index slots, preserved-term inflection and articles, sentences across
   verses, elided objects, supplied function words, and disfavoured devices
   (agent-noun calques, adjectives used as nouns, archaic absolute pronouns) that need
   an owner-approved row.
5. **Evidence policy.** What must be cited, which is the producer's analysis, and
   what code cites automatically. The Kāśikā is cited only where it decides something.
6. **Shard plan** aligned to sentence units and balanced by card count.

### 4.4 Where the owner sits

- **Gate 0, once, before chapter 2.** Line-style rules plus the revised chapter-12
  lines as the calibration set. This is the decision §3 of the plan already reserves
  for the owner (O3).
- **Gate 1, per chapter or per batch of chapters.** The dossier decision sheet: rows
  proposed, alternatives, what each choice changes across the Gītā. Est. 30–60 min for
  chapter 2, falling sharply once the common lemmas are decided.
- **Gate 2, per chapter.** Reading the built chapter on the site, marked
  `provisional`. A change to a row propagates through the occurrence list and a
  mechanical sweep, then a diff re-review.

### 4.5 Parallelism

- Dossier agents run in parallel, about 8 lemmas each, during packet building.
- Producers run one per shard. Shards are sized to about 60 cards on sentence
  boundaries, so chapter 2 yields 14–15 shards. All run concurrently when the
  concurrency limit allows.
- A reviewer starts on its shard as soon as that shard passes the builder check. This
  pipelining is already in use.
- The lead owns the policy, dossiers, tools and integration. The lead does not edit
  producer files; every change goes through the producer.
- Audio runs from L0 in parallel.

### 4.6 The single review pass

Input: the frozen shard, its sha256, and the builder report. The builder has already
done every mechanical check, so the reviewer does not chase loci by hand. The
reviewer checks, per verse:

1. **Grammar.** Recompute pada, root id, affix ids, compound and vigraha, kāraka.
   Test the plausible wrong alternative (other gaṇa, homonym, compound type,
   adhikāra).
2. **Form in the line.** Every non-finite verb, mood and voice in the line equals the
   card (lyap → 'having …', kta → past participle, indicative stays a statement).
3. **Meaning.** For every content word, the card shows the root image, the operative
   sense with its kośa locus, and every commentator gloss on this word in this verse
   (from `gloss`), labelled by §6.3 category. The line's word carries the dossier
   sense. Flag any traditional sense dropped without a recorded reason.
4. **Readability.** Read the line aloud with no card. Each sentence must parse on
   first reading. A device from the disfavoured list needs an owner-approved row.
5. **Policy.** Compliance is checked by code. The reviewer judges whether the row
   fits this occurrence and may file a `row_proposal` finding with occurrences.
6. **Forks.** Admissible construals, reason class, open state, and visibility in the
   reader.
7. **Public surface.** Read the rendered verse in the reader at 390 px: jargon,
   dangling references, missing fork and sense display.

Severity: S1 covers wrong grammar, a dropped or added meaning, a mood or form change,
or a line that does not parse. S2 covers lost richness that the dossier documents.
S3 covers style.

### 4.7 Fixes: resume, do not respawn

- The lead sends the review to the **same producer agent** (SendMessage) with the
  finding IDs and any row decisions. The producer edits its file and re-runs the
  builder check.
- The **same reviewer agent** is resumed with the diff (`git diff --no-index` of the
  two shard versions) and checks only the changed fields plus two spot-recomputed
  verses.
- Lead edits never touch producer files.

Expected saving against the pilot: the 12.5–18.5 min of re-reading per fix agent, and
the round-3 class of findings. Repair scripts are retired. Loci are spans computed by
code, so no locus needs repair.

### 4.8 Throughput targets, derived from this run

**Measured now:**
- 21.3 agent-min per verse (426 for 20);
- 115 min wall per 20 verses at 4 concurrent shards;
- 70 findings per 244 cards (28.7 per 100 cards), 3.3 S1 per 100 cards.

**Projected per 5-verse shard after the changes** (each step derived from §2):

| Step | Pilot | Projected | Basis |
| --- | --- | --- | --- |
| Production | ≈55 min | ≈25 min | JSON emission falls ≈60% because citations, chains, Kāśikā, kośa and candidate definitions are code-expanded (88→≈35 model-min over four shards); lookups fall from 9 to ≈3 model-min; reasoning stays at ≈30, or more if meaning work grows |
| Review | ≈26 min | ≈25 min | removes the ≈42% mechanical share (−11 min), adds a meaning and readability pass (+10 min) |
| Fix | ≈19 min | ≈8 min | resumed producer, no re-reading; findings fall by the 59% that came from classes A–E |
| Re-review | ≈6 min | ≈5 min | diff-based |
| **Total** | **≈105 agent-min** | **≈63 agent-min (≈12.6 per verse)** | |

**Dossiers:** about 6 agent-min per lemma. The plan counts about 150 lemmas with three
or more occurrences; with chapter-specific needs, est. 200 new dossiers for the whole
Gītā, ≈20 agent-hours, mostly front-loaded and fully parallel.

**Chapter 2 (72 verses, est. 900 cards, 14–15 shards):**
- 72 × 12.6 ≈ 15 agent-h, plus est. 60 dossiers (≈6 agent-h).
- Wall-clock at 15 concurrent agents:

  | Step | Minutes |
  | --- | --- |
  | packet and inventory (code) | 5 |
  | dossiers | ≈45 |
  | owner gate 1 | owner time |
  | produce | ≈25 |
  | review | ≈25 |
  | fix | ≈8 |
  | re-review | ≈5 |
  | build and deploy | ≈10 |

  That is **≈2 h plus the owner's gate**, or ≈3.2 h at 7–8 concurrent agents. Under
  the pilot process, at 4 shards at a time, chapter 2 would need four waves of ≈115
  min (≈7.7 h) and about 25 agent-h, with no meaning gate.

**Whole Gītā (680 remaining verses):**
- 680 × 12.6 ≈ 143 agent-h, plus ≈20 dossier agent-h, plus a 5% post-scale audit
  (≈7 agent-h): **≈170 agent-h**, against ≈241 agent-h under the pilot process plus a
  meaning round it never had.
- At 16 concurrent agents that is ≈11 h of agent wall time. With owner gates, the
  realistic calendar is 3–4 working days. It is gated by the owner's row decisions
  and readings, not by the agents.

**Quality targets:**
- ≤ 10 findings per 100 cards;
- 0 findings in classes A–E, since those become build errors before review;
- S1 ≤ 1 per 100 cards;
- 0 public jargon fields;
- every root or compound card shows at least one traditional or kośa voice;
- every open fork is visible in the reader.

A chapter that misses these halts and reopens the brief (plan §13.4.6).

## 5. Amendments (exact proposed text and code)

### 5.1 `docs/SANSKRIT_TRANSLATION_STANDARD.md`

(a) **§3 schema.** After the per-unit paragraph, insert:

> Per unit also: `forks[]` (plan §13.1) and, per word, `term` as a list
> `[{lemma, sense, member}]` (member = compound member index or null). Per word,
> `meaning`: `{root_image, lexical: [{sense, source, locus}], nirvacana: [{gloss,
> source, locus}], activation, reception: [{reading, source, locus}], synthesis}`,
> one field per §6.3 category. A field that a reader does not render is not public
> content; a builder must refuse data whose required display (forks, `meaning`) the
> target reader cannot render.

(b) **§6.3**, append:

> A closed reader's card shows, for every content word, the root image, the
> operative lexical sense with its kośa locus, and every commentator gloss on that
> word in that verse, labelled by category. A gloss gathered as evidence but kept off
> the card is a defect, not a saving.

(c) **New §7.8 Mood and clause type:**

> Render the mood and clause type that are present. A statement stays a statement;
> never print a protasis as a question. Where a particle carries a conditional sense
> attested in the kośas (e.g. *atha … tataḥ*, Apte s.v. *atha* 3, citing Bg 12.9,
> 12.11), 'if' renders that particle and is not an insertion. Where no particle is
> present (12.10 *asamartho 'si*), keep the indicative and let the following
> imperative carry the sequence.

(d) **New §7.9 Non-finite forms:**

> ktvā/lyap → 'having …'; kta → past participle; śatṛ/śānac → '-ing'; tumun → 'to …';
> tṛc → an agent noun only where English has one in that register, else a relative
> clause. A form change for euphony is a §7.2 violation; record any unavoidable one
> on the card with its reason.

(e) **New §7.10 Readable on first reading, and §7.11 Line conventions:**

> §7.10 Every line must parse as English for a reader who opens no card. Agent-noun
> calques ('relinquisher of'), adjectives used as nouns ('this deathless'), archaic
> absolute pronouns ('whatsoever' without a verb), Sanskrit nouns forced into English
> verb frames ('bears no dveṣa'), and noun–noun hybrids of Sanskrit and English
> ('death-saṃsāra') require an owner-approved policy row; otherwise they are
> findings of severity 1.
>
> §7.11 Conventions: epithets translated, lower case after 'O' ('O son of Pṛthā');
> a one-word English rendering of two words is one multi-index slot `{i,j:…}`; a
> sentence that runs across verses ends the earlier line with an em dash and begins
> the next in lower case; preserved terms take English plural -s and the definite
> article only as the policy row's `forms` list; an elided object stays elided unless
> English grammar requires 'nothing'/'it', which is then unslotted and noted;
> supplied copulas and function words are unslotted. No process vocabulary (policy,
> review, finding IDs, lead, owner, shard) in any public field.

(f) **§8.** Replace the opening of the two lists with:

> The decisions are recorded only in `data/glossary/term_policy.json`; the lists
> below are examples of decided rows, and checkers read the policy file alone. A
> preserved noun used for a verbal form must have a decided verbal rendering in the
> row (`forms.finite`, `forms.agent`), chosen by the owner; otherwise the verb is
> translated.

### 5.2 `docs/GITA_FULL_TRANSLATION_PLAN.md`

(a) **§2.1 L9**, replace the sentence after "Review loop reuses …" with:

> Fixes are made by the same producer agent, resumed with the review; re-reviews by
> the same reviewer, resumed with the diff. The lead does not edit producer files.

(b) **§3 readiness**, add:

> 9. **Chapter lemma inventory and term dossiers** complete; every lemma occurring in
> the chapter is matched to an `owner-decided` row or translated by an ordinary
> wording record; policy content hash frozen before production.
> 10. **Reader renders** every public field the gate depends on (forks, card
> `meaning`); verified by the markup test on the chapter's first open fork.
> 11. **English stack** has all seven sources indexed, `define` lemmatises and
> indexes phrases; "not attested" is concluded only after all seven.

(c) **§7.** Replace the production-loop diagram with the layer table of this audit's
§4.2, and the paragraph "Producer and reviewer briefs are as in …" with:

> Producers write analysis records; code expands them into cited cards (no agent
> types a sūtra chain, Kāśikā line, kośa entry or dictionary definition that code can
> look up). One review pass checks grammar, meaning, readability and the public
> surface (audit §4.6).

(d) **§8 gate**, append:

> builder citation chase 0 failures; builder report 0 errors in schema, policy hash,
> Kāśikā spans, wording headwords, forbidden words in all public fields, process
> vocabulary, fork consistency, cross-shard consistency and distinctness; review
> includes the meaning and readability pass; every root/compound card carries a
> traditional or kośa voice; owner queue generated from occurrences; deployed by
> `scripts/deploy_gita_chapter.sh` and verified at the live URL.

(e) **§10 effort.** Replace with the measured pilot figures and the projection of audit
§4.8: 21.3 agent-min per verse measured; 12.6 target; ≈170 agent-h for the remaining
680 verses; owner gates as in §4.4.

(f) **§5.2.** Append to step 5:

> The aligner writes the listening sample (10% of verses, seeded) and every
> disagreement into the manifest as `owner_listening: [{locus, reason}]`; step 4's
> calibration result per aligner is recorded as `calibration: {aligner,
> boundary_error_s, clips}`.

(g) **§17.1.** Correct three sentences:

> The audio spot-listening list does not yet exist in `audio.js` (to be generated, §5.2).
> The 65 fork records are in the data but not rendered by the reader (to be fixed
> before chapter 2). Wording records are complete under the builder's exemptions for
> preserved terms, names and copulas.

(h) **§16.** Replace "Nothing is committed; the owner commits on request" with:

> When the owner instructs publication, the lead
> runs `scripts/deploy_gita_chapter.sh N`, which commits only the chapter's paths and
> pushes; otherwise nothing is committed.

### 5.3 Briefs (`internal/sanskrit_reviews/gita/chN/`)

**Producer brief.** Replace "What to produce" and "Pacing" with:

> **P-1** Write `analysis-AA-BB.json`, not full cards. Per word: `i`, `iast`,
> `lemma_id` (from the packet), `root_id` (Dhātupāṭha record id), `affixes` (ids from
> the chain table, e.g. `kta`, `lyap`, `sup:a.m.1.3`), `compound {type, vigraha,
> members}`, `karaka`, `sense_id` (dossier), `english` (slot text), `why` (one
> sentence: what this English keeps and what it gives up), `card_line` (the
> tradition's gloss to show, chosen from the packet's `gloss` block), `forks`. Run
> `python3 scripts/expand_gita_analysis.py N AA-BB` to produce the cited cards, then
> `python3 scripts/build_gita_chapter_reader.py N --check-only --shard AA-BB`; hand
> off only when it prints no ERROR.
>
> **P-2** Every line passes standard §7.8–7.11. Read it aloud before handoff; if it
> needs a card to be understood, rewrite it.
>
> **P-3** The dossier for each lemma is binding for sense; if this occurrence differs,
> write a `row_proposal` and render per the row meanwhile.
>
> **P-4** Cite the Kāśikā only where its example, counter-example or restriction
> decides your analysis; standard chains are cited by code.
>
> **P-5** Do not write deviation defences for every secondary; record a deviation
> only where a secondary takes a different construal (it then belongs in a fork) or
> has better English for the same construal (adopt it or say why not).
>
> **P-6** Never print process vocabulary in public fields.
>
> **P-7** Stay available: fixes come back to you.

**Reviewer brief.** Replace the Method with the seven checks of audit §4.6 and add:

> **R-1** Start from the builder report; do not hand-chase loci it has verified.
>
> **R-2** Every line: read aloud without the card; a line that does not parse is S1.
>
> **R-3** You may challenge a policy row: file `{"type": "row_proposal", "row",
> "occurrences", "evidence", "proposed"}`; the lead routes it to the owner gate.
>
> **R-4** Lead decisions are reviewed like any other choice.
>
> **R-5** Open the chapter in the reader at 390 px and check what a reader sees.

**Re-review brief.** Replace with:

> Resumed reviewer. Input: the diff between the reviewed and the revised shard and
> the new builder report. Check every changed field against its finding; spot-recompute
> two verses; any regression or new S1 keeps `complete: false`.

### 5.4 `data/glossary/term_policy.json` structure

Keep one file, versioned by content hash, with this shape:

```jsonc
{
  "version": "2",                       // human label; the builder uses the sha256 of the file
  "rule": "…plan §4…",
  "reserved_english": {                 // §7.6 distinctness, checked across all readers
    "lodged": "āveśa", "ever": "satata", "constantly": "nitya",
    "highest": "para", "supreme": "parama", "fear": "bhaya"
  },
  "lemmas": {
    "upasana": {
      "lemma_iast": "upa-√ās", "root_id": "dhatupatha.json#1020011",
      "detect": { "root_ids": ["dhatupatha.json#1020011"], "upasargas": [["upa"], ["pari", "upa"]] },
      "occurrences": ["12.1[5]", "12.2[6]", "12.3[5]", "12.6[12]", "12.20[5]", "…all Gītā loci from concord"],
      "dossier": "internal/sanskrit_reviews/gita/dossiers/upasana.json",
      "senses": {
        "attend-person": {
          "applies_to": ["12.1[5]", "12.2[6]", "12.6[12]"],
          "policy": "translate",
          "tests": { "system_term": "…", "english_carries": "…", "nothing_lost": "…" },
          "forms": { "finite": ["…"], "participle_present": ["…"], "agent": ["…"], "noun": ["…"] },
          "forbidden_english": ["…"],
          "glossaryKey": "upasana",
          "card_line": "Śaṅkara 12.3: sitting near … in an unbroken stream of one cognition (shankara_gita_bhasya.txt:8411)",
          "status": "owner-decided",
          "decided": { "by": "owner", "date": "YYYY-MM-DD", "policy_sha256": "…" }
        },
        "practise-teaching": { "applies_to": ["12.20[5]"], "…": "…" }
      }
    }
  }
}
```

The rules for this structure:

1. The producer declares `lemma_id` from the packet. The builder matches rows by that
   id. Regexes survive only as a linter ("possible unmarked occurrence", a warning).
2. `forms` are checked per grammatical category, so 'bears no dveṣa' versus 'does not
   hate' is a decision, not an accident.
3. `applies_to` makes senses per occurrence, so the queue can list them.
4. `status` is one of `proposed`, `pilot` or `owner-decided`. Production may use only
   `owner-decided` rows, or `pilot` rows the owner has allowed.
5. A shard records the policy sha256. Any change invalidates the affected shards,
   which the builder lists by occurrence.

### 5.5 `prakriya/scripts/lookup/lookup.py`

**L-1 `define` with lemmatiser and phrases.**

```python
def lemma_candidates(word: str) -> list[str]:
    w = word.strip().lower()
    out = [w]
    for suf, rep in (("ied", "y"), ("ies", "y"), ("ed", ""), ("ed", "e"), ("ing", ""), ("ing", "e"),
                     ("est", ""), ("est", "e"), ("er", ""), ("s", ""), ("es", "")):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            stem = w[: -len(suf)] + rep
            out.append(stem)
            if len(stem) > 3 and stem[-1] == stem[-2]:      # stopped → stop
                out.append(stem[:-1])
    return list(dict.fromkeys(out))

def english_define(word, limit=40):
    con = sqlite3.connect(str(ENGLISH_DB))
    for cand in lemma_candidates(word):
        rows = con.execute("select headword,pos,source,tags,definition,locus from defs where lower(headword)=? "
                           "union all select phrase,pos,source,tags,definition,locus from phrases where lower(phrase)=? "
                           "limit ?", (cand, cand, limit)).fetchall()
        if rows:
            return [{"headword": h, "pos": p, "source": s, "tags": t, "definition": d, "locus": l,
                     "inflected_from": cand if cand != word.lower() else None} for h, p, s, t, d, l in rows]
    return []
```

`english-build` adds a `phrases` table:
- from GCIDE `<col><b>…</b></col>` plus the following `<cd>`;
- from Webster lines of the form `To wait on, or To wait upon. (a) …`;
- from Wiktionary (kaikki) entries, which already list phrasal verbs.

GCIDE loci become `gcide-0.53/CIDE.W#<byte offset of <p><ent>>`, so they resolve to
one entry. The NO HEADWORD message is printed only after all seven sources fail.

**L-2 Full stack.** Index Wiktionary (kaikki JSONL with `tags`), OEWN 2025, Century
(OCR), Roget and Moby into the same `defs` table, with a `source` value each. Refuse
`english`/`define` with an error naming the missing sources until all seven are
present.

**L-3 Kāśikā span and self-test.**

```python
def kashika_span(rec_i: str) -> dict | None:
    ku = kashika_units().get(rec_i)
    if not ku:
        return None
    s = char_offset_to_line(KASHIKA_UPSTREAM, ku["character_start"])
    e = char_offset_to_line(KASHIKA_UPSTREAM, ku["character_end"] - 1)
    cs, ce = map_upstream_line_to_clean(s), map_upstream_line_to_clean(e)   # nearest-line map, as now
    return {"kashika": f"{rel(KASHIKA_CLEAN)}:{cs}-{ce}", "kashika_upstream": f"{rel(KASHIKA_UPSTREAM)}:{s}-{e}"}
```

`lookup.py selftest kashika` checks, for all sūtras with a vṛtti:
- the spans are ordered and non-overlapping;
- the first clean line begins with the vṛtti's first 25 characters;
- the sūtra's pratīka occurs inside the span.

It must pass before any producer runs.

**L-4 Adhikāras in force** (data already on disk).

```python
def adhikaras_in_force(rec_i: str) -> list[dict]:
    sid, out = int(rec_i), []
    for s in sutra_table():
        for part in (s.get("type") or "").split("##"):
            if part.startswith("AD$"):
                _, name, end = (part.split("$") + ["", ""])[:3]
                if end.isdigit() and int(s["i"]) <= sid <= int(end):
                    out.append({"sutra": f"{s['a']}.{s['p']}.{s['n']}", "text": s["s"], "adhikara": name, "until": end})
    return out
```

`sutra_lookup` returns `adhikaras` and `anuvritti` (`s["an"]`). For 4.4.98 it then
prints 4.4.75 *prāg ghitād yat* until 5.1.136. That alone would have caught 11-15 F2.

**L-5 `gloss` and `concord`.**
- `gloss PADA CH.V`: from the packet's commentaries (Śaṅkara, Rāmānuja and Madhva
  blocks, plus every `gita_gita_sanskrit` author), print each clause containing the
  pada's stem, in IAST or Devanāgarī. A clause runs to the next daṇḍa or `|` and
  includes a following `iti` / `ity arthaḥ`. Output author, locus and clause. This is
  the card's tradition line, gathered by code.
- `concord LEMMA`: every BORI occurrence (stem match over the chapter tags) with
  locus, plus every published reader's rendering of the lemma (from `gita/*/verses.js`
  word stems to their slot text).

**L-6 `chain`.** A reviewed table `data/grammar/derivation_chains.json`, keyed for
example `sup:a.m.1.3`, `tin:lat.atm.3.3.non-a`, `krt:kta.anit`, `krt:lyap`,
`sandhi:as+voiced`. Each chain is a list of sūtras with the line loci `sutra`
prints. It is built once from the Siddhāntakaumudī prakaraṇas by an agent and
independently reviewed. `chain KEY` prints the cited chain. The producer asserts the
key (the analysis); code supplies the citations. This is consistent with standard
§6.1: the table is a reviewed source artefact, and the agent still makes every
analytical claim.

External sandhi keys are computed from the two pada boundaries. That removes 299
sandhi and phonology citations and finding class D from agent work.

### 5.6 `scripts/build_gita_chapter_packet.py`

Add to each verse a `padas[]` block:
- the BORI tokens split at spaces;
- the Vidyut `cheda` hint, labelled non-authoritative;
- per candidate pada:
  - the `dhatu` records of the root candidates;
  - the `kosha` entries (mw, ap90) for the stem;
  - the `gloss` block (L-5);
  - the policy rows matched by `lemma_id`;
  - the `concord` summary;
  - the published-reader renderings.

Add to the chapter:
- `lemma_inventory[]` (lemma, occurrences, policy status, dossier path or `needed`);
- `shard_plan[]`, built from sentence units (Rāmānuja's grouped tags such as
  `(BhGR_12.3-4)`, verse-final punctuation) and balanced to about 60 cards;
- `policy_sha256`.

Fail if any lemma occurring three or more times in the chapter lacks a row or a
`translate-by-wording` mark.

### 5.7 `scripts/build_gita_chapter_reader.py`: fail-closed checks

| Check | Catches | Rule |
| --- | --- | --- |
| B1 policy hash | D1, D9, P2 | `shard.policy_sha256 == sha256(term_policy.json)`, else list the rows changed since then and the affected occurrences |
| B2 citation chase | E, T15 | every `file:line[-line]` exists; normalised quote (NFC, no accents, avagraha or spaces) ⊂ span text; `json#id` exists and contains the quote; packet loci resolve |
| B3 Kāśikā span | T1, T2, D12 | every Kāśikā locus ⊂ `kashika_span(item.sutra)`; `sutra` is required on the item |
| B4 wording headwords | T3, T4 | every dictionary candidate: `define(word)` non-empty and the candidate's `locus` ∈ the returned loci; a Joycean record requires `define` empty across all seven sources |
| B5 form agreement | W3, D3 | lyap/ktvā card and a slot not matching `^having\b` → ERROR unless the card carries `form_note`; kta → slot not ending in `-ing`; a `?` in a line whose words carry no interrogative (kim, kva, katham …) → ERROR |
| B6 forbidden words everywhere | 06-10 F21 | scan `english`, `sense`, `gloss`, `parts[].gloss`, `note` and `meaning.*` against every matched row's `forbidden_english` (quotations exempt) |
| B7 fork consistency | G | `open is True` ⇔ `reason_class == 5`; `word_i` required; every required fairness locus matched by `word_i`, not merely by verse; ≥ 2 construals each with `basis` |
| B8 consistency and distinctness | A, D8, D11 | per (lemma, sense), every slot ⊆ `forms`; a `reserved_english` word in a slot of a different lemma → ERROR; across all published readers as well |
| B9 public hygiene | T21 | `\b(policy row\|term_policy\|lead decision\|F\d{1,2}\b\|owner\|shard\|review: pilot\|forks\[\]\|`terms`)` in any public field → ERROR |
| B10 render contract | T18 | if any verse has `forks` or any card has `meaning`, run `scripts/test_gita_word_markup.js` with the chapter's first open fork and assert its construals appear in the rendered DOM; else ERROR "reader cannot show forks" |
| B11 pada check | T13 | re-join padas with the sandhi table of L-6 and compare to the BORI saṃhitā exactly (orthographic folds as in the packet's `fold_deva`); no edit-ratio tolerance |
| B12 schema | D5, D13, T9 | JSON Schema `gita-producer-v2`: one evidence shape `{claim, locus, quote, sutra?, kind}`; `word_class` ∈ {content, particle, pronoun, name, copula}, which replaces the regex exemptions; slot syntax |
| B13 public apparatus | T12, T19 | publish `apparatus.json` only if the reader loads it; strip every candidate whose source is a secondary; scan public files for translator names followed by a quoted string |
| B14 owner queue | T16 | build from occurrences: every row used in the chapter with its rendering per occurrence, `status != owner-decided` first, rows changed since the last owner decision flagged |
| B15 post-acceptance edits | P4 | the review's `producer_sha256` must equal the shard and the review's `rereview.date` ≥ the shard's last change; re-stamping without re-review → ERROR |
| B16 discovery | T17 | validators discover `gita/*/verses.js` |
| B17 root record | T10 | card `root_id` resolves in `dhatupatha.json`, and its gaṇa and pada equal the card's root string |
| B18 fallback kinds | plan §13.4.2 | each fallback has `kind`; `root`, `pratyaya` or `compound` → ERROR for a complete chapter |

### 5.8 Deploy step: new `scripts/deploy_gita_chapter.sh N`

The working tree is shared with other agents. It currently holds their uncommitted
edits, `assets/app.js` among them. So the deploy never pulls, rebases or stashes in
the working tree. It commits from a clean worktree of `origin/main`, into which it
copies only the chapter's own files and re-runs only the registration step. This
follows `AGENTS.md` rules 1, 1a and 2.

```sh
#!/bin/sh
set -eu
N="$1"
REPO="$(git rev-parse --show-toplevel)"; cd "$REPO"
python3 scripts/build_gita_chapter_reader.py "$N"            # fail-closed build in the working tree
sh scripts/run_checks.sh                                     # slots, terms, witness, markup, audio manifest
TMP="$(mktemp -d)"; git fetch origin main; git worktree add --detach "$TMP" origin/main
OWN="gita/ch$N"                                              # the chapter's own directory
mkdir -p "$TMP/$OWN"
for f in verses.js index.html audio.js recitation.mp3; do [ -f "$OWN/$f" ] && cp "$OWN/$f" "$TMP/$OWN/$f"; done
cp data/glossary/term_policy.json "$TMP/data/glossary/term_policy.json"
python3 scripts/build_gita_chapter_reader.py "$N" --register-only --root "$TMP"   # app.js + manifest edits applied to origin/main's copies
cd "$TMP"
EXPECT="$OWN/verses.js $OWN/index.html $OWN/audio.js $OWN/recitation.mp3 assets/app.js data/articles/manifest.json data/glossary/term_policy.json"
for f in $EXPECT; do [ -e "$f" ] && git add "$f"; done          # by path only
git diff --cached --name-only | while read -r f; do
  case " $EXPECT " in *" $f "*) ;; *) echo "unexpected staged path: $f"; exit 1;; esac
done
git diff --cached --stat
git commit -m "Gītā $N: reader from reviewed shards (policy $(shasum -a 256 data/glossary/term_policy.json | cut -c1-12))"
git push origin HEAD:main
cd "$REPO"; git worktree remove "$TMP"
for u in "https://vedanta.eeshan.xyz/gita/ch$N/verses.js" "https://vedanta.eeshan.xyz/"; do
  i=0; until curl -fsI "$u" >/dev/null; do i=$((i+1)); [ $i -gt 20 ] && { echo "not live: $u"; exit 1; }; sleep 6; done
done
curl -fs "https://vedanta.eeshan.xyz/gita/ch$N/verses.js" | cmp -s - "gita/ch$N/verses.js" || { echo "live verses.js differs"; exit 1; }
```

This needs one builder change: `--register-only --root DIR` applies `register()` to
`DIR/assets/app.js` and `DIR/data/articles/manifest.json` and writes nothing else.
The rules around the script:

1. **D-1.** Run the script only on the owner's instruction, recorded in plan §17. It
   commits only the chapter's own paths plus the two registrations and the policy,
   and refuses any other staged path.
2. **D-2.** `apparatus.json` is not copied unless B13 allows it, that is, unless the
   reader loads it.
3. **D-3.** Published as `provisional` until owner gate 2. A status field in the
   `data/articles/manifest.json` entry carries it.
4. **D-4.** Make the review record versionable. Move the secondary quotations into
   `internal/sanskrit_reviews/gita/chN/private/` (gitignored: `deviations.json`, the
   packet's secondaries, the secondary text in wording candidates). Have the producer
   and review files reference them by id, and stop ignoring `producer-*.json`,
   `independent-review-*.json` and `owner-review-queue.json`. Commit them with the
   chapter, through the same worktree route.

### 5.9 Order of applying these amendments

1. Reader display of forks and `meaning`: the UI owner, under `UI_DESIGN_STANDARD.md`.
2. The standard's §7.8–7.11 and the owner's gate 0 on line style.
3. In parallel, the lookup changes L-1 to L-5 and their tests. These are independent.
4. The chain table (L-6) and its review.
5. Policy v2 structure and migration of the 53 rows.
6. Packet v2.
7. Builder B1–B18.
8. The briefs.
9. The deploy script.
10. Chapter 12 re-run through the new route: its lines are revised by the meaning round
    and the dossiers, which validates the route on a known chapter.
11. Chapter 2.

Steps 3–4 and 5–6 can run in parallel. Builder checks B2, B3 and B4 depend on L-1 and
L-3.

## 6. Summary

1. 59% of the 70 review findings, including 4 of the 8 S1, came from tool defects, rows and line rules decided mid-run, or deterministic hygiene, not from translation judgement.
2. The term policy (50 rows) was written in one call five minutes before production; 12 of 53 rows changed during the run, and the version string never changed.
3. Producers spent 62% of their model time emitting JSON, half of it citation text code can generate; the English line and sense were 0.7% of their output.
4. Reviewers spent ≈42% of their time chasing citations by hand (4,112 checks) and never had a gate for meaning, richness, embodiment or readability.
5. Hence the owner's verdict: 72% of root/compound cards show no traditional voice, Śaṅkara's upāsana definition sits unused in evidence, the chapter's governing verb reads 'wait upon', and three statements were turned into questions against Apte's 'if' (Bg 12.9, 11).
6. The reader shows neither the 65 forks nor the sense paragraphs; 23 public fields carry pipeline jargon; the owner queue omitted the chapter's key row.
7. Fix agents were fresh and spent 12.5–18.5 min re-reading; fixes must resume the same producer and reviewer.
8. Before production, per chapter: lemma inventory (code), term dossiers (agents), rows decided by the owner with forms per grammatical category and reserved English; line-style rules live in the standard.
9. Producers assert analyses and choose meanings; code expands citations (chains, Kāśikā spans, adhikāras, `define`, `gloss`, `concord`); the builder fails closed on B1–B18, including what the reader can display; deploy is a script.
10. Target 12.6 agent-min/verse (now 21.3): chapter 2 in ≈2–3 h of wall time plus the owner's gate, the whole Gītā in ≈170 agent-h, with ≤10 findings per 100 cards and none from classes A–E.
