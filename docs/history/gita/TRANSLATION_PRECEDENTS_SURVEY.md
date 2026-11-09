# Translation precedents survey and chapter 12 check (2026-11-08)

Scope: everything this repository already says about how Sanskrit is translated
and presented, checked against the new chapter-12 reader (`gita/ch12/verses.js`,
20 verses, 244 cards) and `data/glossary/term_policy.json` (version
`1-ch12-pilot`, 53 lemmas, 57 sense rows). This is a survey. It translates
nothing. It records amendments as proposals to the **existing** standard, plan,
checkers and queue (§5), not as a new plan. All counts below come from scripts
run over the working tree on 2026-11-08. Line numbers refer to the working-tree
files as of that date.

Abbreviations: **STD** = `docs/SANSKRIT_TRANSLATION_STANDARD.md`; **PLAN** =
`docs/GITA_FULL_TRANSLATION_PLAN.md`; **POL** = `data/glossary/term_policy.json`;
**CHK** = `scripts/check_gita_terms.js`; **SLOT** = `scripts/validate_gita_slots.js`;
**BLD** = `scripts/build_gita_chapter_reader.py`; **GJS** = `assets/gita.js`;
**UI** = `docs/UI_DESIGN_STANDARD.md`; readers **sp** = `gita/sthitaprajna`
(2.54–72), **kama** = `gita/kama` (3.36–43), **ch5**, **ch12**, **Dāma** =
`gita/yogavasistha-dama`, **VSN** = `gita/vishnu-sahasranama`.

---

## 1. Principles the repository already states

### 1.1 Literalness and faithful rendering

| # | Principle | Where |
|---|---|---|
| L1 | "The truest reading is the literal one"; translate the grammar present, do not paraphrase | STD §1, lines 8–11 |
| L2 | No inserted nouns or subjects; implied 3rd-sg. subject is "he", not "a man"; keep gender, number, person, voice; supplied copulas allowed | STD §1, 13–16 |
| L3 | Epithets and proper names translated with their etymology (Keśava, Pārtha, Kaunteya, Mahābāhu) | STD §1, 17–18 |
| L4 | Explicit ambiguity on the card; never a faked single parse | STD §1, 21–22 |
| L5 | English literal and complete; rules apply to the mūla, every commentary voice, the one-line `sense` and `ourRendering` | STD §7, 289–296 |
| L6 | Do not collapse meaning (scope words, connectives, negations, number, case force) | STD §7.1, 298–303 |
| L7 | Render the word, not an interpretation; *yukta* is "yoked", not "absorbed" | STD §7.2, 305–309 |
| L8 | Insert nothing; elliptical complements stay implied; no `[bracket]` inserts; clarifiers go in the card | STD §7.3, 311–316 |
| L9 | Choose the sense the usage has and **keep the root's image** (*saṃ-√yam* "rein in"; *√car* + object "engaging") | STD §7.4, 318–327 |
| L10 | Match connotation (*vidheya* "governable / self-governed", *sneha* "affection") | STD §7.5, 329–334 |
| L11 | Never print a different Sanskrit word; distinct near-synonyms get distinct English | STD §7.6, 336–340 |
| L12 | Same word, same rendering across mūla and commentary unless the sense shifts | STD §7.7, 342–345 |
| L13 | "Literal, grammar-first, school-neutral word-by-word translation with an inspectable apparatus"; not a paraphrase, devotional rendering, school's reading or poem; where literal and natural conflict, literal wins in the line and natural lives in the card | PLAN §11, 285–305 |
| L14 | Every English word choice made from dictionary definitions and recorded; rarity is not a rejection criterion; Joycean compound only when no attested word fits, never labelled attested | PLAN §1, 21; §6, 203–227; L5, 35 |
| L15 | Owner, 2026-11-08: both as accurate and as poetic as possible; nobody followed blindly | PLAN §17, 495–500; PRODUCER_BRIEF 24–31 |
| L16 | Owner feedback round: richer, more accurate, more literal and more embodied English; meaning before beauty but the line must not be hard to read | `internal/sanskrit_reviews/gita/ch12/MEANING_REVIEW_BRIEF.md` 3–13 |
| L17 | Literal translation is a research target; "lossless translation" | `docs/PROJECT_PURPOSE.md` 112–113, 194 |

### 1.2 Preserve or translate

| # | Principle | Where |
|---|---|---|
| P1 | Untranslatables stay Sanskrit, glossary-linked; `translatable: false` suppresses a forced gloss | STD §1, 19–20 |
| P2 | Keep Sanskrit only when English cannot carry it; current preserve list *rāga, dveṣa, guṇa, dharma, kāma, prajñā, buddhi, manas, indriya, karma, yoga, rasa, ahaṅkāra, tṛṣṇā, samādhi, saṃsāra*; *ātman* → "the self", *brahman* → "Brahman" | STD §8, 349–359 |
| P3 | Translate list: *krodha* anger, *bhaya* fear, *moha* delusion, *duḥkha* sorrow, *sukha* pleasure, *spṛhā* longing, *sneha* affection, *prīti* fondness, *vidheya* governable / disciplined, *jñāna* knowledge, *mokṣa* liberation, *saṅga* clinging | STD §8, 360–368 |
| P4 | Several English words beat one lossy word; don't bloat, don't flatten; four-step decision procedure | STD §8, 369–383 |
| P5 | **Sense-constant** rule: a (lemma, sense) is preserved only if all three tests pass (system term; no English without adding/dropping; nothing lost because card+glossary carry it); otherwise one fixed rendering per sense | PLAN L2, 32; §4.1–4.2, 88–123 |
| P6 | Seed decisions: preserve yoga, dharma, karma (law and fruit-bearing act), guṇa … bhakti and bhakta, **dhyāna**; translate phala, hetu, śaraṇa, śraddhā, siddhi, deva, jīva, śoka | PLAN §4.3, 125–135 |
| P7 | krodha → anger; every emotion word translates; existing *krodha* data "will be swept" | PLAN L7, 37 |
| P8 | Every matching card MUST carry `term:{lemma,sense}`; a new lemma or sense is added deliberately, never ad hoc | POL `rule`; PRODUCER_BRIEF 11–14 |

### 1.3 Nirvacana and depth-reading

| # | Principle | Where |
|---|---|---|
| N1 | Do not silently choose one valid derivation; show every supported formation and every attested traditional *nirvacana* in parallel, each with segmentation, roots, affixes, meaning, locus, qualification | STD §6.2, 226–232 |
| N2 | Keep categories apart: grammatical formation ≠ *nirvacana* ≠ an author's theological reading; unbacked readings withheld or marked unresolved | STD §6.2, 234–241 |
| N3 | Governing hermeneutic is Aurobindonian: preserve outer sense and read the same language for its inward work; presumption of intentional semantic activation; later readings are reception history, not backdated; surface referent remains true | STD §6.3, 243–268 |
| N4 | A public card must separate six categories: formation; lexical senses; pre-existing nirvacanas; activation by the passage; later reception; the site's labelled synthesis | STD §6.3, 273–285 |
| N5 | Depth kept in the card, not smuggled into the line; Aurobindonian reading is labelled category-6 synthesis on the card and never decides the line | PLAN §11 item 4, 296–305 |
| N6 | Meaning dossier per content word: root image, traditional nirvacana with locus, meaning here, Gītā usage, others' renderings, preserve test, verdict | MEANING_REVIEW_BRIEF §A, 51–86 |
| N7 | Do not flatten real disagreement; do not reduce schools to "lower Advaita" | `docs/INTEGRAL_REALISM_GRAMMAR.md` 24–31 |

### 1.4 Glossary

| # | Principle | Where |
|---|---|---|
| G1 | Use the site glossary (`data/glossary/*.json`); readers delegate to the app popover | STD §4, 132–135 |
| G2 | Entries encyclopedic, neutral; give `literal` (traditional grammatical meaning/derivation), `invariant_definition`, `per_school`, genuine `translator_note`; add terms so every technical term is covered | STD §4, 137–143 |
| G3 | Template: plain opening, literal derivation, invariant function, school readings, primary loci, translator note, related terms, completeness | `docs/EDITORIAL_DATA_STANDARD.md` §8, 141–145 |
| G4 | For v2 entries, inherited literal glosses, cognates, school rows, textual history and translator notes are public claims; the renderer must not show an unreviewed legacy field | EDITORIAL §8, 171–175 |
| G5 | Every displayed school reading has a concrete locus; incomplete school slots stay internal | `docs/IMPLEMENTATION_QUEUE.md` P4, 71–84 |
| G6 | Every `glossaryKey` resolves to a file | STD §3, 127–128; PLAN readiness 4, 67–68; PRODUCER_BRIEF 135–137 |

Shape on disk: 253 entries + `manifest.json` (`{version, terms[]}`, 253 names;
`term_policy.json` is on disk but correctly not in the manifest). Field counts:
`term_key/term_iast/term_devanagari/literal/aliases/invariant_definition/see_also`
253; `translator_note` 237; `per_school` 235 (`{school, definition,
primary_loci, citations[{cite,locus_short}], register_tag}`); `last_verified_at`
227; `school_framing` 123; `textual_history` 44; `cognates` 14;
`editorial_contract: v2` 7; `derivations[]` 4 (pratibha, pratibhasa,
bodhakasha, samvedana).

### 1.5 Card fields

| # | Principle | Where |
|---|---|---|
| C1 | Card: word; whole-word gloss; morpheme pieces each translated; grammar in plain English with case force; samāsa-vigraha; glossary link | STD §2, 35–39 |
| C2 | Click only; contextual, non-modal; closes on same-token tap, outside click, Escape, scroll | STD §2, 40–45; UI 200 |
| C3 | Word schema: `i, iast, deva, gloss, parts[], stem, root, affix, morph, karaka, compound{type,vigraha,members}, glossaryKey, translatable` | STD §3, 96–116 |
| C4 | Pāṇinian strictness: root with gaṇa and pada; pratyaya named; morph in traditional terms; sandhi noted with rule "so the split in `parts[]` is honest"; strict compound class; kāraka per sūtras; complete parts | STD §6, 160–189 |
| C5 | Card per word: root with gaṇa and pada, pratyaya, morphology, compound with vigraha, kāraka, complete parts, **attested senses**, glossary link | PLAN §1, 15–19 |
| C6 | `sandhi`, `term`, `evidence[]`, `fallback[]`, `wording{}`, `note` added to the card; forks per verse | PRODUCER_BRIEF 101–127; PLAN §13.1, 338–346 |
| C7 | FALLBACK "shown on the card"; FALLBACK on a root, pratyaya or compound type blocks completion | PLAN §8, 257–258; §13.4.2, 387–390 |
| C8 | Where English forces a choice, "render the alternative in the card as a parallel construal with its traditions named" | PLAN §13.2 reason 5, 359–362 |
| C9 | Card gloss fields are synonym lists; no cross-language etymology/cognates in card fields (those "live behind 'Explain'") | CHK 206–213; commit 1f98f0d3 |
| C10 | VSN: every inflected word declares `word_class` and an `inflection` record pointing at the ending's `parts[]` index | `docs/SAHASRANAMA_READER_RELEASE_PLAN.md` 61–68 |

### 1.6 UI of readers

| # | Principle | Where |
|---|---|---|
| U1 | Source script, then IAST pada-pāṭha, then literal English; never substitute generated script for a witness | STD §2, 29–34; EDITORIAL §7, 133–139; CONTENT_AND_SOURCE 47–50 |
| U2 | Bidirectional highlight | STD §2, 46–47 |
| U3 | Commentary word-by-word, voice by voice, colour-coded, unranked, chronological, linked to Thinker | STD §2, 48–52 |
| U4 | Word card: one anchored non-modal card, **max 300px**; long reading goes to the persistent panel | UI 196–203 |
| U5 | No local `z-index: 600` escalation | UI 207–209 |
| U6 | Word-card action opening commentary names its author ("Read {commentator} on this word"); dense references as "Sources (n)" | UI 153–156, 172–173 |
| U7 | No essential information only in a popup (print) | UI 266–270 |
| U8 | Exceptions must be named in UI before adding a pattern | UI 288–292 |
| U9 | Owner design (2026-06-15): a plain title with no summary or explanations; no static grammar block, the interactive word cards carry the grammar; grammar disclosure removed again 2026-08-27 | commits a8547c3, e53a1d50 |
| U10 | Audio verse-level only; no inferred word highlighting | AUDIO_ALIGNMENT_STANDARD 19–20, 35–40; PLAN L4, 34 |

### 1.7 Sources and rights

| # | Principle | Where |
|---|---|---|
| R1 | Sanskrit verbatim from cited sources on disk; never invent | STD §1, 23–25; EDITORIAL 10–16 |
| R2 | Authority chain: witness → pada division → Aṣṭādhyāyī → Mahābhāṣya/vṛtti/Dhātupāṭha/Gaṇapāṭha → reviewed English; parsers, dictionaries, LLMs non-authoritative | STD §6.1, 191–215; GRAMMAR_ENGINE_INTEGRATION_PLAN §1, 18–38 |
| R3 | Data whose provenance names Monier-Williams (or a tool/model) as the basis of a public analysis is provisional and must not appear in published payloads | GRAMMAR_ENGINE §6, 136–141 |
| R4 | Use `/Users/eeshan/Dev/prakriya/sources/`; do not run the prakriya interpreter or rely on its tables | STD §6.1, 217–224; AGENTS.md 42–47 |
| R5 | BORI is the Gītā text; Devanāgarī is a labelled deterministic transliteration collated against a second witness | PLAN L3, 33 |
| R6 | Secondaries are never a source of meaning; private store; quotation only; **never republished, never shown in the reader** | PLAN §12, 309–330 |
| R7 | Public repo ships only licensed material; raw OCR quarantined | README 125–129; CONTENT_AND_SOURCE §1 |
| R8 | Audio rights basis, performer, edition in manifest | AUDIO 8–17, 24–25; PLAN §5.1 |

### 1.8 Review process

| # | Principle | Where |
|---|---|---|
| V1 | Produce per-unit data, audit independently (grammar, literalness, fidelity, glossary) | STD §5, 147–153 |
| V2 | Closed readers: every public token reviewed; fail closed | STD §6.1, 210–215; GRAMMAR_ENGINE §4, 95–113 |
| V3 | Producer → independent reviewer (fresh context, recompute, chase citations, try the wrong alternative) → fail-closed builder → owner gate | PLAN §7, 229–249; §13.4, 382–401; REVIEWER_BRIEF |
| V4 | Fork resolution only by grammar, Gītā usage, kośa, English-stays-open, or English-forces (then open fork); never "school X reads it so" | PLAN §13.2, 348–369 |
| V5 | Three independent acceptance passes (source preservation, linguistic, rendered behaviour); relabelling is not review | SAHASRANAMA plan 75–93 |
| V6 | Semantic-field records hash-bound to an independent zero-error review | `scripts/validate_yogavasistha_dama_reader.py` 56–72 |

### 1.9 Voice and register

| # | Principle | Where |
|---|---|---|
| W1 | Three voices kept separate: what the source says, what scholarship disputes, what the site synthesizes | README 120–123; EDITORIAL 17–18 |
| W2 | Glossary register neutral, encyclopedic | STD §4, 137–139 |
| W3 | `sense`: one plain paragraph, no interpretation beyond the words | PRODUCER_BRIEF 86 |
| W4 | Quoted English keeps its source boundary; site English marked as site's | STD §2, 53–66 |
| W5 | Article readers keep "readable IAST and literal English"; do not reintroduce a heavy reader merely to satisfy an obsolete plan | PROJECT_PURPOSE 186–190 |

### 1.10 Contradictions found

Between documents, between documents and checkers, and between documents and data.

| # | Contradiction | Evidence |
|---|---|---|
| X1 | **krodha.** STD §8 and PLAN L7 translate it as "anger"; CHK hard-codes it as PRESERVE with "anger", "wrath" forbidden, and lists it among loaded concepts for check F. All seven earlier occurrences print "krodha" (sp 2.56, 2.62, 2.63; kama 3.37; ch5 5.23, 5.26, 5.28). The "sweep" in L7 has not run | STD 360; PLAN 37; CHK 34, 218 |
| X2 | **karma.** STD §8 preserves *karma* everywhere; PLAN L2/§4.2 and POL split plain-act ("action", "karma" forbidden) from law-of-action. CHK's legacy table forbids "action" (line 27) while its policy mode requires it. A word's check therefore depends on whether it carries `term`. ch5 renders plain-act *karmāṇi* "karmas" (5.10, 5.13, 5.14) and passes | STD 355–358; PLAN 32, 112–123; POL karma; CHK 27, 105–137 |
| X3 | **karma-phala.** PLAN §4.3 preserves *karma* as "law and fruit-bearing act"; the POL plain-act note assigns 12.11–12 *karma-phala-tyāga* to plain act ("the fruit of action"). ch5 5.12 and 5.14 print "the fruit of karma" | PLAN 127–128; POL karma.plain-act.note |
| X4 | **dhyāna.** PLAN §4.3 preserves it; POL translates "meditation" (`review: pilot`). The override is recorded only in `owner-review-queue.json` | PLAN 130; POL dhyana |
| X5 | **sukha adverb.** PLAN §4.1: "pleasure or, in the adverb, at ease". POL has no adverb sense and forbids "ease". ch5 prints "at ease" (5.13) and "easily" (5.3) | PLAN 103–104; POL sukha |
| X6 | **vidheya.** STD §7.5 says "governable / self-governed"; STD §8 says "governable / disciplined". sp 2.64 slot prints "disciplined" with the card gloss "governable" | STD 331–332 vs 362 |
| X7 | **Orthography.** STD §8 and CHK spell "ahaṅkāra"; POL and BORI spell "ahaṃkāra" (BORI: 10 × ahaṃkār, 0 × ahaṅkār; 14 × saṃnyās, 0 × sannyās). sp 2.71 prints "ahaṅkāra", ch12 12.13 prints "ahaṃkāra". No spelling rule exists | STD 355; CHK 32; POL ahamkara |
| X8 | **Slot invariants.** STD §3 requires `i` contiguous from 0 and every `glossaryKey` resolving. SLOT explicitly permits non-contiguous `i` (lines 29–31) and checks no glossary key. Only BLD checks glossary keys (151–153), and only for new chapters. PLAN readiness 4 asks the slot and term checkers to fail on an unresolved key; they do not. All keys resolve today (0 unresolved across 924 Gītā words) | STD 125–128; SLOT 29–31; PLAN 67–68 |
| X9 | **Schema drift.** STD §3 lists none of `term, sandhi, note, forks, evidence, fallback, wording, rootGloss, analysis_mode, surface_iast, parallelDerivations, semanticFieldKeys`. PLAN G0.2 and §16 promise "`forks[]` added to the standard's schema §3"; STD is unchanged in the working tree | STD 96–116; PLAN 268, 484 |
| X10 | **Devanāgarī.** STD §2 puts the source script first. STD §3's own comment says `deva` is "kept; not displayed". ch5's header says "Site renders IAST only". `gita/sthitaprajna/_build/DESIGN.md` 20–22 says "IAST only". GJS shows the verse Devanāgarī, and makes it tappable only when every word has `surface_iast`; no Gītā reader has that field | STD 29–34 vs 102; `gita/ch5/verses.js` 6; GJS 103–107 |
| X11 | **Commentary.** STD §2 and AGENTS.md require word-by-word commentary for all Sanskrit. PLAN L1 removes it for the Gītā and says it amends STD §5, but the rule it overrides is in §2 | STD 48–52; AGENTS.md 34–38; PLAN 9, 31 |
| X12 | **Reference implementation.** STD, AGENTS.md and README name `gita/sthitaprajna` as the reference. PLAN §17 and PRODUCER_BRIEF call the earlier readers "known to contain mistakes … not models to copy". IMPLEMENTATION_QUEUE P3 still calls the mūla Gītā "reference-quality". sp itself breaks STD §1: Keśava (2.54), Pārtha (2.55, 2.72) and Kaunteya (2.60) are left untranslated, though §1 names exactly these epithets | STD 5–6; AGENTS.md 39–40; README 76; PLAN 501–504; QUEUE 58 |
| X13 | **Modern dictionaries as basis.** GRAMMAR_ENGINE §6 makes MW-based public analysis provisional and unpublishable. Five ch12 fallbacks rest the formation on Apte or MW: dakṣaḥ 12.16, naraḥ 12.19, parama in 12.10/12.20, and sāgara in 12.7. Those cards are published in `verses.js` | GRAMMAR_ENGINE 136–141; `gita/ch12/apparatus.json` fallbacks |
| X14 | **Pilot-result counts.** PLAN §17.1 says "16 fallback claims (none on a root, a pratyaya or a compound type)" and "65 fork records (10 open, class 5)". Measured: 16 fallbacks, of which at least six concern the affix or formation and so fall under the §13.4.2 completion block: dhruvam 12.3, dakṣaḥ and gatavyathaḥ 12.16, naraḥ 12.19, parama 12.10 and 12.20. Forks: 65, of which **12** are open and 12 are reason-class 5 | PLAN 527–530, 387–390; `gita/ch12/apparatus.json`; `verses.js` forks |
| X15 | **Visibility of forks and fallbacks.** PLAN §8 says each fallback is "visible on its card"; §13.2 puts parallel construals on the card. GJS renders neither. `apparatus.json` is never loaded (app.js 5621–5630 loads only `verses.js`, `audio.js`). 29 card notes say "see forks", pointing at a structure the reader never renders | PLAN 257–258, 359–362; GJS 659–700 |
| X16 | **Sense not visible.** `owner-review-queue.json` tells the owner to "read each verse's english and sense". The site renders no `sense` (owner decision U9). sp DESIGN.md 24–26 still lists a visible "sense caption" | `internal/sanskrit_reviews/gita/ch12/owner-review-queue.json`; GJS 224–246 |
| X17 | **§6.3 vs Dāma UI.** STD §6.3, added in commit 766e843 on 2026-09-01, requires the public card to separate all six categories. Later the same day, commits 7ca9656 and 55a324b removed the methodology block and "narrative-activation" readings from the public popup. Dāma `enhancer.js` line 8 hides the categories `grammatical head` and `narrative activation`. Category 4 is therefore never shown | STD 273–280; `gita/yogavasistha-dama/enhancer.js` 8, 175 |
| X18 | **Nirvacana labelling.** STD §6.2–6.3 treat a later author's resegmentation as reception, not *nirvacana*. VSN stores Chinmayananda's *sa* + *Mā* reading of name 109 *samaḥ* as `kind: "traditional-nirvacana"`, though its own qualification says "Attested here only in Chinmayananda's commentary". Category vocabularies are open-ended: Dāma uses 28 semantic-reading categories and 30 parallel-derivation categories, with 4 records carrying none. VSN reviews use five classes | STD 234–239, 264–265; `gita/vishnu-sahasranama/reader-details.json` name 109 |
| X19 | **Secondaries republished.** PLAN §12 says secondary renderings are never republished. BLD `public_wording` keeps the secondary's word and locus string (docstring line 193–195). The published `gita/ch12/apparatus.json` has 167 secondary-sourced candidates, 57 of which quote the rendering in the `locus` field (e.g. "Sivananda 'steadfastly worship'"). `gita/` is in the deploy allow-list | PLAN 326–328; BLD 192–207; AGENTS.md 126 |
| X20 | **Audio standard stale.** It says there is "no … forced-alignment … pipeline". PLAN §5.2 and §17 report `scripts/audio/` built and run on chapter 12 | AUDIO 42–48; PLAN 199–201, 515–516 |
| X21 | **README stale.** It lists sp, kama and ch5 with "voice-by-voice commentary, recitation audio"; ch5 has neither. It omits ch12, Dāma and VSN | README 40 |
| X22 | **Card width and stacking.** UI requires cards of max 300px and forbids `z-index: 600`. `assets/gita.css` 363 sets `z-index: 600`. Dāma `reader.css` 31–35 widens evidence cards to `clamp(540px, 56vw, 760px)`. Neither is recorded as a UI exception | UI 200, 207–209, 288–290 |
| X23 | **Card design rule outside the standard.** "The small pop-up is gloss-LISTS only … etymology stay[s] behind 'Explain'" exists only in a CHK comment and a commit. It conflicts with STD §6.2/§6.3 and PLAN §11, which put derivations and nirvacanas on the card | CHK 206–210; GJS 670–671 |
| X24 | **Checker morphology.** POL renderings are matched as whole words (`\bsorrow\b`), so plurals fail. Applied to the earlier readers, "amid sorrows" (sp 2.56) and "amid pleasures" would fail. The `para` regex also matches *parāyaṇa* and comparative *para* ("higher"), so 10 of 10 earlier occurrences fail | CHK 121–127; scratch run, §3 below |
| X25 | **nirvāṇa.** PLAN §4.3 says "one occurrence, 2.72 already rendered". BORI has five (2.72, 5.24, 5.25, 5.26, 6.15). The readers give three renderings: "is extinguished into Brahman" (sp 2.72), "extinction in Brahman" (ch5 5.24), and "brahma-nirvāṇa" (ch5 5.25–26) | PLAN 134–135; BORI lines 745, 1308, 1311, 1318, 1410 |
| X26 | **Coverage.** CHK and SLOT cover only the four Gītā readers plus the VSN preface. The Dāma validator is not in `scripts/run_checks.sh`, and BLD `--check-only` is not run there | CHK 187–192; SLOT 65–70; run_checks.sh 49–86 |
| X27 | **Glossary `literal` carries unlabelled nirvacanas.** `duhkha.json` and `sukha.json` give "duḥ-/su- + kha 'axle-hole'" without a locus or a category label. EDITORIAL §8 makes literal glosses public claims (lines 171–175). Their first glosses are also POL-forbidden renderings ("ease, pleasure, happiness"; dvesa "aversion"; tyaga "abandonment"; yoga "union") with no note that the reader uses a fixed rendering | `data/glossary/duhkha.json`, `sukha.json`, `dvesa.json`, `tyaga.json`, `yoga.json` `literal` |

---

## 2. Richer-meaning machinery not used in chapter 12

| Machinery | What it does | Data shape | How the UI shows it | What ch12 would need |
|---|---|---|---|---|
| **Dāma `semantic_fields`** | Carries a word's inherited semantic field (lexical senses, Nirukta nirvacanas, Uṇādi formations, patronymic fields, narrative activation) apart from its contextual gloss, under the §6.3 method. 15 fields; 72 of 599 words linked | `gita/yogavasistha-dama/apparatus.js` → `semantic_fields{schema_version, methodology{title,summary,principles[≥4]}, witness_history[4], fields[{key, lemma_iast, lemma_devanagari, match_forms[], opening, chronology_note, readings[≥2]{category, formation?, meaning, source_label?, source_path?, source_locus?, qualification?}]}`. Source: `internal/sanskrit_reviews/yogavasistha-dama/semantic-fields.json`. Builder validates the shape and that source_path exists (`build_yogavasistha_dama_reader.py` 405–452), attaches `semanticFieldKeys` by matching `match_forms` against iast/stem/parts/members (455–480, 745) | `enhancer.js` `prepare` resolves keys (18–33). After GitaReader's card opens, `appendWordEvidence` appends "Attested meanings" (261–285): the lemma heading, then each reading's category, formation, meaning, source and qualification. It hides `grammatical head`/`narrative activation` (8, 175) and duplicate formations. `opening` and `chronology_note` are never shown. Names in the English line become their own triggers (217–247) | `internal/sanskrit_reviews/gita/ch12/semantic-fields.json` in the same schema, with the categories closed (§5 S6). BLD attaches keys and emits them (a `CH12_SEMANTIC` global or `meanings.js`). The `gita-ch12` entry in app.js loads it. The enhancer becomes generic in GJS, not Dāma-only. Add an independent review file hash-bound as in `validate_yogavasistha_dama_reader.py` 56–72, and a check in `run_checks.sh`. Ready inputs: MEANING_REVIEW_BRIEF dossiers (`root_image`, `nirvacana[{source,locus,gloss}]`, `gita_usage`), which map one to one onto `readings[]` |
| **Dāma root record** | Root as an object with gaṇa, pada and Dhātupāṭha locus, upadeśa form and artha | word `root{form,gana,pada,gloss,dhatupatha{locus,aupadeshika_devanagari,artha_sanskrit}}`, `rootEvidence`, `root_ref`, `rule_refs` | "Root evidence" row: Root · gaṇa · pada; Dhātupāṭha locus · upadeśa · artha | ch12 roots are strings that already include gaṇa, pada and artha (e.g. "√kliś (divādi, 4A, 'upatāpe')"). The Dhātupāṭha locus sits in `apparatus.json` `evidence[]` (`dhatupatha.json#…`). BLD can lift the matching evidence item into a structured `root` object; GJS needs a renderer for it |
| **Dāma `parallelDerivations` / `derivations` / `alternatives`** | Parallel supported analyses: textual variants, uṇādi vs regular formation, compound and syntax construals. `alternatives` holds grammatically expected readings that were not adopted | `parallelDerivations[{category, form|formation|analysis, meaning, evidence, qualification, roots[]}]` (45 words non-empty); `alternatives[{reading,status,meaning,reason}]` (320 words) | "Parallel supported analyses" block (enhancer 145–159, 272–276). `alternatives` is not displayed | ch12 holds the equivalent at verse level in `forks[].construals[{reading, grammar_basis, evidence, traditions}]` (65 forks, 173 construals). BLD can project each fork onto the cards of the words it names (`at`), and GJS renders it as "Other construals" |
| **VSN name analyses** | A full per-name card: Dhātupāṭha-bound root, sandhi, uncertainty, evidence, and parallel derivations split into grammatical vs nirvacana | `analysis.json` (1000 names): `{citation_iast, citation_devanagari, whole_gloss, parts[{form_iast,gloss,kind}], stem, root{form,gana,pada,gloss,dhatupatha{…}}, affix, morph, compound, sandhi, derivation, grammar, uncertainty[], evidence{…}}`. `reader-details.json` `word_analysis.parallel_derivations[{id,label,kind: grammatical|traditional-nirvacana, meaning, parts, roots, formation, morphology, qualification, evidence[{source,locus,detail}]}]`: 92 records on 81 names (56 nirvacana, 36 grammatical). `traditional_derivation` (printed commentary text) on 270 names | `assets/sahasranama.js` 543–577 and 850–885. The card shows Devanāgarī under the headword, the definition, then a "Primary grammatical formation" section and one section per alternative headed "Traditional nirvacana" or "Alternative grammatical derivation" (title, meaning, parts, roots with Dhātupāṭha locus and artha, formation, qualification, short evidence labels). Sandhi is shown as a note (864–866). A button opens "Read Chinmayananda's explanation" | This is the best existing public display of STD §6.2. ch12 needs a `parallel_derivations` array per word (same shape) and the same renderer moved into GJS. VSN already holds relevant data: name 109 *samaḥ* (sa + Mā, which is reception per X18); name 813 *amṛtāśaḥ* (*amṛta* as both "nectar" and "immortality"); names 17/481 *akṣara*, 722 *avyakta*, 832 *acintya* (√cint), 123 *sarvaga*, 584 *śānti*. These are cross-reader precedents for 12.3 *acintya*, *sarvaga* and 12.20 *amṛta*, but they are Chinmayananda's glosses, not site literal renderings |
| **VSN derivation reviews** | A claim-level classification that turns §6.2 into a procedure | `internal/sanskrit_reviews/chinmayananda-derivation-review-*.json` `rows{id:{primary_relation, dispositions[{claim_text, classification, reason, evidence[], public_derivation}], review_notes}}`. Classifications measured: established-grammar 115, interpretive-not-etymology 115, attested-traditional-nirvacana 52, unsupported-withheld 52, source-backed-alternative 32 | Not displayed. It decides which claims become `parallel_derivations` | Apply the same five classes to every etymological statement the ch12 commentators make (packet.json), the Nirukta, Amarakośa and Uṇādi. Only `established-grammar`, `attested-traditional-nirvacana` and `source-backed-alternative` become public. Add a date field so reception is separated (X18) |
| **Glossary v2 `derivations[]`** | Sourced derivation on the glossary term | `{category, formation, meaning, root{form,gana,pada,dhatupatha{…}}, affix, evidence[], qualification}`, in 4 entries | Glossary popover via "Explain" | None of the 31 glossary keys ch12 links has `derivations`. ch12 preserved terms (yoga, bhakti, buddhi, manas, citta, indriya, ahaṃkāra, dveṣa, dharma, karma) would gain sourced derivations |
| **Glossary `per_school` / `school_framing`** | School readings with loci; whether schools share a concept or diverge | `per_school[{school, definition, primary_loci, citations, register_tag}]` (2–16 schools on the ch12 keys); `school_framing{framing_status, shared_core, register_axes_note}` | Glossary popover, reached only through "Explain" | ch12 reaches them for 65 cards. The verse-specific school spread (which ācārya reads 12.5 *avyakta* as Brahman, prakṛti or Kṛṣṇa's body) lives in forks and is unrendered. Link each fork construal's `traditions` to the glossary's school rows |
| **sp/kama voices** (`commentaries.js`, `aurobindo.js`, `parallels.js`) | Each commentator's Sanskrit word by word, Aurobindo's English, cross-tradition parallels | `{author, school, work, locus, sanskrit, words[], english, ourRendering, segments[{from,to,kind}]}` | Voice bar with colour chips, segments tagged by rhetorical move (GJS 83–94, 170–258) | PLAN L1 excludes this layer for the Gītā. UI 172–173 offers a lighter form: a card action "Read {commentator} on this word", which can quote the commentator's one-line gloss of the word (already in packet.json and in fork evidence) as reception (category 5) |
| **ch12 `apparatus.json` wording records** | 155 wording records: sense description, dictionary candidates with definitions, chosen word, connotation | `verses[].words[]{i, iast, evidence[{claim,locus,quote}], fallback[], wording{sense_description, candidates[], chosen, connotation, joycean}, term}` | Not loaded or rendered anywhere | Publishable as a "Why this English" disclosure once X19 is fixed. `sense_description` is the natural "meaning here" line |
| **GJS grammar notes** | Reader-local explanations of grammar labels and forms in passage notes | `GRAMMAR_HELP` (GJS 407–424); `grammar_annotations[]` | Buttons inside article passage grammar notes | Could explain `sandhi` and the sūtras cited in `sandhi`/`affix` if those are rendered |

Plan promise not met: PLAN §11 item 4 (296–298) says the card carries "attested
senses, root image, traditional nirvacanas, and the site's labelled synthesis".
In ch12 `verses.js` the word "nirvacana" occurs 7 times, "Nirukta" 0 times and
"Aurobindo" once. No card has a meaning section, so the six §6.3 categories are
not separable on any ch12 card.

---

## 3. Cross-reader consistency

Method: every word in the four Gītā readers (924 cards) was extracted with its
slotted English. Lemmas were matched on stem, compound members and part forms,
and each match was read by hand. "Agree" means the slot English is the same for
the same lemma and sense. "Better" is judged against STD §7 and §1 and POL.

| Lemma | ch12 | sp | kama | ch5 | Agree? | Better per the standard |
|---|---|---|---|---|---|---|
| *yukta* (√yuj kta) | 12.1 satata-yuktāḥ "ever yoked"; 12.2 nitya-yuktāḥ "constantly yoked", yuktatamāḥ "the most yoked" [yukta/yoked] | 2.61 "yoked" | — | 5.8, 5.12 "The yoked one"; 5.23 "is yoked"; 5.6 yoga-yuktaḥ "yoked with yoga"; 5.7 "Yoked in yoga"; **5.12 ayuktaḥ "the undisciplined one"** | No: ch5 5.12 | ch12/sp. *a-yukta* is "unyoked" (§7.2, §7.7). Also ch5 has "yoked with" vs "yoked in" for the same compound (5.6/5.7) |
| *nitya* | 12.2 "constantly" | — | 3.39 "perpetual" | 5.3 nitya-saṃnyāsī "the eternal renunciant" | No | No policy row. ch12's "constantly" fits the adverbial *nitya-* of a practice. "eternal" (5.3) imports metaphysical permanence (§7.5). Needs a POL row |
| √ās / upa-√ās | (pari-)upāsate "wait upon (on every side)" ×5 [upasana]; udāsīnaḥ "sitting apart" | 2.54, 2.61 āsīta "sit / should sit" | — | 5.13 āste "dwells" | No | §7.4 keep the root's image: sp's "sit" is best for the bare root; ch5 "dwells" drops it. ch12's "wait upon" drops "sit" while udāsīna keeps it (MEANING_REVIEW_BRIEF already lists this) |
| *buddhi* | 12.4, 12.8, 12.14 "buddhi" | 2.63–2.66 "buddhi" | 3.40–3.43 "buddhi" | 5.11, 5.17, 5.20, 5.28 "buddhi" | Yes (slots) | Agree. But sp card **glosses** say "intellect" (2.63, 2.65, 2.66), the POL-forbidden English, and CHK does not check glosses |
| *manas* | 12.2, 12.8, 12.14 "manas" | 2.56, 2.60, 2.67 "manas" | 3.40, 3.42 "manas" | 5.11, 5.13, 5.19, 5.28 "manas" | Yes (slots) | Agree. sp card glosses "the mind" (2.55, 2.56, 2.60, 2.67) contradict the slot |
| *indriya* | 12.4 indriya-grāmam "the host of indriyas" | "indriyas" ×6; indriyārtha "the objects of indriya" (2.58) / "the indriya-objects" (2.68) | "indriyas" | "indriyas"; 5.9 "the objects of the indriyas" | Partly | Term agrees. *indriyārtha* has three renderings (§7.7); ch5 5.9 is best. sp glosses say "the senses". **Defect:** ch5 5.11 slots are swapped (`{3:with the indriyas} {4:alone}`: i=3 is *kevalaiḥ*, i=4 is *indriyaiḥ*) |
| *sama* | 12.4, 12.13, 12.18 ×2 "the same" [sama/same, pilot] | — | — | 5.18 sama-darśinaḥ "see with an equal eye"; 5.19 samam "the same", sāmye "in sameness"; 5.27 samau "equal" | No | ch12 and ch5 5.19 agree. 5.18 uses "equal", which POL forbids. 5.27 (*prāṇāpānau samau kṛtvā*, "making even") is a separate sense and needs its own row. The owner's pilot decision governs |
| *saṅga* / √sañj | 12.18 saṅga-vivarjitaḥ "rid of clinging"; 12.5 āsakta "fastened" | 2.62 "clinging" ×2 | — | 5.10, 5.11 saṅgam "clinging"; **5.12 saktaḥ "clinging"**; **5.21 asaktātmā "unattached"** | No (participles) | ch12. *sakta* is a kta participle ("stuck, fastened"), not the action-noun (§7.2), and printing "clinging" for it merges it with *saṅga* (§7.6). "unattached" uses POL-forbidden "attached". Should be "fastened" / "unfastened" (add an *a-sakta* row) |
| *dveṣa* / √dviṣ | 12.13 adveṣṭā "Bearing no dveṣa"; 12.17 "bears no dveṣa" [pilot] | 2.57 "feels dveṣa"; 2.64 "rāga and dveṣa" | — | 5.3 "feels dveṣa" | Noun yes, verb no | No rule decides between "bears" and "feels"; §7.7 requires one. "feels" has two precedents and avoids the "bear a grudge" overtone of "bears" (§7.5). Owner pilot row. sp/ch5 glosses say "hates … feels aversion", both forbidden renderings |
| *harṣa* / √hṛṣ | 12.15 "elation"; 12.17 "is not elated" | — | — | 5.20 na prahṛṣyet "should he rejoice" | No | ch12: one rendering for one root (§7.7). "rejoice" sits beside "joy", which POL forbids |
| *bhaya* | 12.15 "fear" | 2.56 "fear" | — | 5.28 "fear" | Yes | — |
| √vij / *udvega* | 12.15 "is not agitated" ×2, "agitation" | 2.56 anudvigna-manāḥ "unagitated" | — | 5.20 na udvijet "should he be distressed" | No: ch5 | ch12 and sp. "distressed" shades toward grief (*śoka*) (§7.5, §7.6) |
| *krodha* | — | "krodha" ×3 | "krodha" | "krodha" ×3 | Yes among themselves | None meets STD §8 / PLAN L7 ("anger"). They pass only because of X1 |
| *śānti* | 12.12 "peace" | 2.66, 2.70, 2.71 "peace" | — | 5.12, 5.29 "peace" | Yes | — |
| *tyāga* / √tyaj | "relinquishment" ×3; "relinquisher" ×2 | — | — | 5.10 tyaktvā "having abandoned"; 5.11, 5.12 "having given up" | No | ch12. ch5 is inconsistent within itself and uses two POL-forbidden renderings |
| *jñāna* | 12.12 "knowledge" ×2 | — | 3.39, 3.40 "knowledge"; 3.39 jñānin "the knower" | 5.15–5.17 "knowledge"; ajñāna "ignorance" | Yes | Agree. *ajñāna* and *jñānin* need POL rows |
| *dhyāna* / √dhyai | 12.6 "meditating on"; 12.12 "meditation" ×2 [pilot] | 2.62 dhyāyataḥ (viṣayān) "dwelling on" | — | — | No (sense shift) | Both are defensible: with the sense-objects as object the sense is "dwell on" (§7.4, §7.7). POL has a single row, so a second sense row is needed |
| *karma* | plain act "action(s)" (12.6, 12.10 ×2); karma-phala "fruit of action" | — | — | "karmas" (5.1, 5.10, 5.13, 5.14), "karma" (5.11), "the fruit of karma" (5.12), "karma-yoga" (5.2) | No | ch12 for plain acts (PLAN L2). The *karma-phala* sense is unsettled (X3); the owner decides. *karma-yoga* needs a row |
| *yoga* / *yogin* | "yoga"; 12.14 "a yogī" | — | — | "yoga"; 5.24 "yogī"; **5.11 "Yogins"**; 5.5 yogaiḥ "by the followers of yoga" | Partly | The plural form is unsettled ("yogins" vs POL `iast_forms` "yogīs"). 5.5 "followers" is an inserted noun (§7.3) |
| *bhakta* / *bhakti* | "bhaktas", "my bhakta", "possessed of bhakti" | — | — | — | n/a | Not attested in the earlier readers |
| *priya* | "dear" ×6 | — | — | 5.20 priyam / apriyam "what is pleasant / unpleasant" | Sense shift | Both fit their context (masc. "dear to me" vs neut. substantive). Needs a second POL sense row |
| *mukta* / √muc | 12.15 "freed" (from …) | 2.64 viyukta "freed from" | — | 5.28 "liberated"; 5.3 pramucyate "is released"; 5.26 viyukta "released from" | No | Two senses (freed-from-X vs absolute liberation) need POL rows. Also sp *viyukta* "freed" collides with ch12 *mukta* "freed" (§7.6), and ch5 renders *viyukta* "released" |
| *saṃtuṣṭa* / *tuṣṭa* | "content" ×2 | 2.55 "content" | — | — | Yes | — |
| *ātman* | — | "the self" | "the self" | "the self"; 5.17 tad-ātmānaḥ slot "self", gloss "mind" | Yes (slots) | ch5 5.17's gloss contradicts its slot |
| *yatātman* / √yam | 12.14 "whose self is restrained"; 12.11 yatātmavān "self-restrained"; 12.4 saṃniyamya "having fully reined in" | 2.61 saṃyamya "Having reined in"; 2.69 saṃyamī "the self-controlled one"; 2.64 vidheyātmā "whose self is disciplined" | 3.41 niyamya "having reined in" | 5.25 yatātmānaḥ "whose selves are controlled"; 5.26 yata-cetasām "whose minds are controlled"; 5.28 "controlled" | No | ch12. One English for *yata* (§7.7); POL forbids "self-controlled". The "rein in" image agrees across ch12, sp and kama (§7.4) |
| *prajñā* / *dhī* / *mati* / *sthira* / *sthita* | 12.19 sthira-matiḥ "whose thought is steady"; 12.9 sthiram "steady" | sthita-prajña "whose prajñā stands firm" (2.54) / "of settled prajñā" (2.55); sthita-dhīḥ **"the steady-minded one" (2.54) / "of steady wisdom" (2.56)** | — | 5.20 sthira-buddhiḥ "steadfast in buddhi" | No | sp breaks §7.7 (two renderings each for *sthitaprajña* and *sthitadhī*). It also breaks §7.6: "minded" is *manas*' forbidden English, and "wisdom" is the forbidden English of the preserved *prajñā*. *sthira* is "steady" (ch12) vs "steadfast" (ch5). *dhī* needs a POL row distinct from buddhi, prajñā and mati |
| *cetas* | 12.5, 12.7 "awareness" [pilot] | 2.65 prasanna-cetasaḥ "whose mind is serene" | — | 5.26 "whose minds are controlled" | No | ch12, whatever word the owner settles on. STD §7.6 forbids printing *manas* for *cetas*, and "mind" is *manas*' forbidden English |
| *duḥkha* | 12.13, 12.18 "sorrow"; 12.5 adverb "with hardship" | 2.56 "amid sorrows"; 2.65 "of all sorrows" | — | 5.22 "sources of sorrow"; 5.6 adverb "hard" | Mostly | Noun agrees. For the adverb ch12 has "with hardship" and ch5 "hard": same POL row, different English |
| *sukha* | 12.13, 12.18 "pleasure" [pilot] | 2.56 "amid pleasures"; **2.66 "happiness"** | — | 5.21 "pleasure"; 5.24 "has pleasure within"; **5.3 "easily"; 5.13 "at ease"; 5.23 sukhī "is happy"** | No | ch12 for the noun. "happiness" and "happy" are POL-forbidden. The adverb needs the row PLAN §4.1 promises (X5) |
| *śubha* / *aśubha* | 12.17 "the fair and the foul" [pilot] | 2.57 "good and evil" | — | — | No | ch12 (§7.5): "good and evil" imports a moral dualism that *śubha* (bright, auspicious) does not state. Owner pilot row |
| *para* | 12.2 parayā "the highest"; 12.6 mat-parāḥ "having me as highest" | 2.61 mat-paraḥ "holding me as the supreme"; **2.59 slot swap** | 3.42–43 "higher", "beyond" (comparative) | 5.16 param "supreme" | No | ch12. It keeps *para* "highest" distinct from *parama* "supreme" (§7.6); sp 2.61 is the same compound rendered differently. kama's comparative is a separate sense needing a row. **Defect:** sp 2.59 `{8:on seeing} {9:the Supreme}` maps i=8 *param* to "on seeing" and i=9 *dṛṣṭvā* to "the Supreme" |
| *śatru* | 12.18 "a foe" | — | 3.43 "the enemy"; 3.37 / 3.39 *vairin* also "the enemy" | — | No | ch12. kama renders two distinct words (*śatru*, *vairin*) with one English (§7.6) |
| *ahaṃkāra* | 12.13 "without ahaṃkāra" | 2.71 "without ahaṅkāra" | — | — | Spelling | BORI spelling *ahaṃkāra* (X7) |
| *nirmama* | 12.13 "without 'mine'" | 2.71 "without 'mine'" | — | — | Yes | — |
| *sarva-bhūta(-hita)* | "all beings"; "in the welfare of all beings" | "all beings" | — | identical (5.25) | Yes | — |
| *phala* | "fruit" | — | — | "the fruit" | Yes | — |
| *rata*, *śreyas*, *nara*, *śānti*, *bhaya* | "delighting", "better", "the man", "peace", "fear" | same where present | — | same | Yes | — |
| Vocative epithets | 12.7 pārtha "O son of Pṛthā"; 12.9 "O winner of wealth" | **2.54 "Keśava", 2.55/2.72 "Pārtha", 2.60 "Kaunteya"** | 3.39 "O son of Kuntī" | "O son of Kuntī", "O mighty-armed one" | No: sp | ch12, kama and ch5 meet STD §1 (17–18); sp does not |

Earlier readers checked against the ch12 policy (scratch script applying each POL
row to sp/kama/ch5 slots). These would fail: *cetas* 2 of 2, *para* 10 of 10
(partly regex over-reach, X24), *sukha* 5 of 8, *duḥkha* 3 of 4 (partly
plurals), *sama* 3 of 4, *prāp* 3 of 6 ("on meeting", "having gotten" vs
"attain"), and one each for *yatātman*, *dhyāna*, *śubha*, *udvega*, *yukta*,
*saṃnyāsa* ("Having renounced" for *saṃnyasya* is policy-compliant on a stem
but fails the row's form list), *ahaṃkāra* (spelling) and *loka* (plural).
*buddhi*, *manas*, *kāma*, *saṅga*, *śānti*, *bhaya*, *dveṣa* and *karma* pass.
*karma* passes only because its preserve sense accepts "karma" without a
`term` field to fix the sense.

---

## 4. Card display: what chapter 12 shows

GJS `wordCardHtml` (659–700) and `renderVerse` (224–246) decide what is visible.

| ch12 field (count of 244 cards) | Rendered? | How |
|---|---|---|
| `iast` (244) | Yes | headword |
| `gloss` (244) | Yes | `.wc-mean` |
| `parts[]` (244; 677 pieces) | Yes | form + gloss chips |
| `root` + `rootGloss` (132) | Yes | full root string including gaṇa/pada; hidden only if equal to a part form (672) |
| `stem` (244) | Yes, if it differs from iast | "stem:" |
| `affix` (244) | Yes, unless "none (avyaya)" | "formation:" |
| `morph` (244) | Yes | through `plainMorph` |
| `karaka` (244) | Yes | "syntax:" |
| `compound` (57) | type + vigraha yes; `members` no | `.wc-gram-cmp` |
| `glossaryKey` (65) | Yes | "Explain ‘…’ →" button(s), also for parts in the embedded app |
| `note` (94) | **Yes** | `.wc-note` |
| `translatable` (244) | Only as a CSS class | `w-name` |
| `deva` (244) | **No** on the card. The verse Devanāgarī is plain text and not tappable, because ch12 words lack `surface_iast` (GJS 106) | — |
| `sandhi` (136) | **No** | invisible |
| `term` (92) | **No** | invisible; the reader cannot tell that a word is under a fixed policy rendering or kept in Sanskrit by rule |
| `evidence[]`, `fallback[]`, `wording{}` | **No**. They are not in `verses.js`; they sit in `gita/ch12/apparatus.json`, which is never loaded | invisible |
| verse `forks[]` (65; 12 open) | **No** | invisible; 29 notes refer to them |
| verse `sense` (20) | **No** (owner decision U9) | invisible |
| verse `grammar` (20) | **No** (removed in e53a1d50) | invisible |
| verse `iast` saṃhitā, `meter` | **No** | invisible |

So the reader sees grammar but not meaning. It cannot see why a word is kept in
Sanskrit or fixed in English, the sandhi that justifies the split, the
traditional meanings, the open alternatives, or which claims are unsourced.

**What the card should show** (proposed order; sections collapse when empty;
card text uses the 15px/1.55 role from UI 75):

1. Headword: IAST, with `deva` beneath it (as VSN does, `sahasranama.js` 885).
2. Contextual gloss (`gloss`).
3. **Term line** from `term`, when present, in plain words, e.g. "Kept in
   Sanskrit throughout the Gītā in this sense: *bhakta*. Explain →" or
   "Rendered ‘clinging’ wherever *saṅga* has this sense." The wording comes from
   the POL row, so the reader learns that consistency is deliberate.
4. Parts; root with gaṇa, pada and Dhātupāṭha artha; formation; morphology;
   syntax; compound type and vigraha (as now).
5. **Sandhi** row: "Printed *kleśo 'dhikataraḥ* ← *kleśaḥ* + *adhikataraḥ*
   (8.2.66; 6.1.113; 6.1.87; 6.1.109)".
6. **Meanings**, a disclosure labelled by count, e.g. "Meanings (4)",
   grouped under the closed §6.3 categories: Formation, Attested senses (kośa),
   Traditional nirvacana (with locus), In this verse, Reception (named
   commentators' glosses), Site reading (labelled synthesis). Categories 4 and 6
   need the owner decision in S6.
7. **Other construals**, from the forks that name this word: each reading with
   its traditions named, the construal followed, and "open" where English forced
   the choice (PLAN §13.2 reason 5).
8. **Sources (n)** disclosure (UI pattern 2, 153–156): the `evidence[]` loci.
   Unlocated claims are listed under "Not located in the grammatical sources"
   (PLAN §8).
9. Verse level, on the locus row: a fork marker "Readings (n)" for multi-word
   forks (e.g. 12.12 ordering) that opens the same construal list.

Because of UI 200 (max 300px) and U7 (print), sections 6–8 should open in the
existing persistent glossary/reference panel (UI 202), or the UI must record
the Dāma-style wider-card exception (X22). The card itself stays compact.

---

## 5. Recommended consolidated standard: amendments

Principle: **STD governs**. PLAN is the Gītā project plan and stops restating
rules. POL is STD §8's table. CHK, SLOT and BLD enforce STD and nothing else.
Each amendment below names its file and section. Items marked **owner** need a
decision that the record does not settle.

### S0. STD header (replace lines 3–6)

> How Sanskrit is translated and presented on this site. This document is the
> **single governing standard** for every Sanskrit reader (mūla and commentary).
> Its preserve/translate table is `data/glossary/term_policy.json` (§8). Project
> plans (e.g. `GITA_FULL_TRANSLATION_PLAN.md`) set scope, order and gates and may
> record a deliberate deviation only by naming the section they amend; they do
> not restate rules. Checkers (`check_gita_terms.js`, `validate_gita_slots.js`,
> chapter builders) enforce this document and the table, and nothing else. The
> reference implementation for word cards is `gita/ch12/` once the owner accepts
> the pilot. The meaning layer follows `gita/yogavasistha-dama/` (semantic fields)
> and `gita/vishnu-sahasranama/` (parallel derivations). Earlier readers are
> migrated under §9.

### S1. STD §2, card bullet (replace lines 35–39)

> - **Tap a word → a card** with, in this order: the word in IAST with its
>   Devanāgarī; its contextual gloss; the **term line** when a `term_policy` row
>   applies (kept in Sanskrit, or the fixed English, stated in plain words); the
>   morpheme pieces, each translated; the root with gaṇa, pada and Dhātupāṭha
>   artha; the formation (pratyaya); the grammar in plain English with the case's
>   force; the syntax (kāraka); the samāsa-vigraha; the **sandhi** that produced
>   the printed form; a **Meanings** section in the §6.4 categories; **Other
>   construals** from every fork naming the word, with traditions named and
>   open forks marked; **Sources** (evidence loci), with any unlocated claim
>   listed as such; and glossary links. Empty sections are omitted. Long
>   sections open in the persistent reference panel (`UI_DESIGN_STANDARD.md`,
>   Contextual surfaces) so the card stays compact.

### S2. STD §2, commentary bullet (append to line 52)

> A reading's plan may record a mūla-only decision (the Gītā: plan L1). Then
> commentators appear only as reception (§6.4 category 5) inside word cards and
> fork construals, named and located, never as a voice layer.

### S3. STD §2 and §3, Devanāgarī (replace line 102's comment)

> `"deva": "स्थितप्रज्ञस्य",  // Devanāgarī citation form; shown under the card headword`

Add to §2 after line 34: "Readers declare `surface_iast` per word when the printed
Devanāgarī line should be tappable." Correct the stale comments in
`gita/ch5/verses.js` line 6 and `gita/sthitaprajna/_build/DESIGN.md` 20–22.

### S4. STD §3, schema and invariants (replace lines 96–128)

> Per word, public file (`verses.js`): `i, iast, deva, gloss, parts[], stem,
> root` (string with gaṇa and pada, or object `{form,gana,pada,gloss,
> dhatupatha{locus,aupadeshika_devanagari,artha_sanskrit}}`), `rootGloss, affix,
> morph, karaka, compound{type,vigraha,members}, sandhi, glossaryKey,
> translatable, term{lemma,sense}, note, meaningKeys[]` (keys into the reader's
> semantic-field file), and `parallel_derivations[]` (shape as in the
> Sahasranāma reader: `{id,label,kind,meaning,parts,roots,formation,morphology,
> qualification,evidence[]}`).
> Per word, apparatus file (`apparatus.json`, loaded by the reader for the
> Sources section): `evidence[{claim,locus,quote}], fallback[{claim,kind}]`
> (where `kind` ∈ `root|pratyaya|compound|sense|syntax|other`), and
> `wording{sense_description,candidates[],chosen,connotation,joycean}`.
> Per unit: `locus, speaker, meter, iast, devanagari, english, sense,
> grammar{karakaSummary,verbalModality}, forks[{at, words[], construals[{reading,
> grammar_basis, evidence[], traditions[]}], followed, reason_class, reason,
> open}]`.
> Invariants (CI-checked for every reader on the site): `i` contiguous from 0;
> every `{i:…}` slot resolves; pada-pāṭha reproduces the witness saṃhitā (sandhi
> only); every `glossaryKey` resolves; every word matching a `term_policy` row
> carries `term`, and every `term` resolves to a row; every root names gaṇa and
> pada; every fork's `words[]` resolves; no `fallback` of kind `root`, `pratyaya`
> or `compound` in a reader marked complete.

(`forks[].words[]` is new: it is what lets the builder attach a fork to its
cards. Today forks carry only the free-text `at`.)

### S5. STD §5, procedure (replace lines 147–156)

> 1. Acquire witnesses (§1, §6.1). 2. Build the packet (code). 3. Producer: cards,
> slotted line, forks, wording records, **meaning dossier per content word**
> (root image; formation; kośa senses; nirvacanas with locus; use in this text;
> reception), classified by §6.4. 4. Independent reviewer in a fresh context:
> recompute every card, chase every locus, try the wrong alternative, verify
> every §6.4 category label and date. 5. Fail-closed builder emitting the public
> file, the apparatus file and the semantic-field file. 6. Owner review on the
> rendered page. 7. Audio per `AUDIO_ALIGNMENT_STANDARD.md`. The Gītā's files,
> briefs and gates are in `GITA_FULL_TRANSLATION_PLAN.md` §7–§8.

### S6. STD new §6.4 "Meaning record and public display" (insert after line 285)

> Each meaning claim carries exactly one category from this closed list:
> `formation` (regular Pāṇinian or Uṇādi formation); `lexical` (attested kośa
> sense); `nirvacana` (transmitted traditional semantic derivation attested
> **before or in the text's tradition**: Nirukta, Uṇādi vṛtti, kośa, or a
> commentator who presents it as received); `activation` (how this passage uses
> the field); `reception` (a named later author's gloss, application or
> resegmentation, with date); `synthesis` (the site's labelled reading).
> Vocabularies already in use map onto it: Sahasranāma review classes
> `established-grammar` → `formation`, `attested-traditional-nirvacana` →
> `nirvacana`, `source-backed-alternative` → `formation` (parallel),
> `interpretive-not-etymology` → `reception`, `unsupported-withheld` → not
> published. Dāma categories ("Nirukta segmentation", "Uṇādi formation",
> "lexical sense", "narrative activation", …) map by name. A reading first
> attested in a modern author (e.g. a twentieth-century commentator's
> resegmentation) is `reception`, never `nirvacana`. Records of every category
> stay in data. **Public display (owner):** either (a) all six categories are
> shown, labelled, as §6.3 requires; or (b) `activation` and `synthesis` are
> held in data and not shown, as the Dāma reader has done since 2026-09-01
> (commits 55a324b and 7ca9656). In case (b), §6.3's sentence "A public card must
> accordingly separate" is amended to "A meaning record must separate", and
> §6.3's six-item list governs data rather than display.

### S7. STD §7 lead paragraph (replace lines 293–296)

> Three scripts enforce the mechanical part on every reader listed in their
> shared registry: `validate_gita_slots.js` (§3 invariants),
> `check_gita_terms.js` (§7.6 and §8, reading only `term_policy.json`), and each
> reader's builder in check mode. `scripts/run_checks.sh` runs all of them.

### S8. STD §7.7 (replace lines 342–345)

> ### 7.7 Render the same sense the same way
> The unit of consistency is the (lemma, sense) pair. Each pair is decided once
> in `term_policy.json`, with its rendering(s), the inflected English forms it
> may take (plural, adverb, verb), its forbidden renderings and its test
> results. Every reader on the site is checked against that row. When one
> string is used in two senses, both senses are rows; the card states the sense.
> Inconsistency within a word's own card (gloss vs slot) is also a distortion:
> card glosses may give the range but must not contradict the row (no "the mind"
> in the gloss of a word whose slot prints *manas*).

### S9. STD §8 (replace lines 349–368; keep 369–383)

> Keep a term in Sanskrit for a sense only if all three tests hold: (1) it is a
> category of the text's own system in that sense; (2) no English word or short
> phrase carries the sense without adding, dropping or shading (§7.1–7.5);
> (3) the card and glossary carry what keeping it withholds. Otherwise translate
> it with one fixed rendering for that sense. **The current decisions are the
> rows of `data/glossary/term_policy.json`**; examples in this document are
> illustrative and the table governs. Two distinct Sanskrit words never share an
> English rendering. Established English forms count as kept: *brahman* →
> "Brahman", *ātman* → "the self". Printed IAST follows the witness's
> orthography (BORI: *ahaṃkāra*, *saṃnyāsa*, *saṃtuṣṭa*). Emotion words
> translate (*krodha* → anger). *vidheya* → "governable" (one rendering; strike
> "disciplined").

### S10. STD new §9 "Cross-reader consistency and migration" (append)

> All readers on the site share one table. A reader built before the table
> (sthitaprajña, kāma, chapter 5) is migrated in one pass: add `term` to every
> matching word; apply the row's rendering; fix card glosses that contradict
> slots; record a context exception as a new sense row, never a one-off. Until
> migrated, such a reader is listed in the checker registry as `legacy`. Its
> violations are reported, not hidden. When migration completes, the legacy
> tables in the checker are deleted.

### Plan amendments (`GITA_FULL_TRANSLATION_PLAN.md`)

- **P1 §4.3, line 130:** move *dhyāna* from Preserve to Translate: "dhyāna →
  meditation (pilot, owner O3); √dhyai with sense-objects as object →
  'dwell on' (row `dhyana/dwell-on`)".
- **P2 §4.3, lines 127–128:** state the *karma-phala* decision (**owner**):
  either "karma-phala → the fruit of action (plain-act)", which matches POL and
  ch12, or "the fruit of karma (fruit-bearing act)", which matches ch5 5.12 and
  5.14. Then align POL's note.
- **P3 §4.1, lines 103–104:** "sukha → pleasure; adverbial *sukham* → at ease
  (row `sukha/at-ease`)". Add the row to POL and drop "ease" from the pleasure
  row's forbidden list.
- **P4 §4.3, lines 134–135:** "nirvāṇa: five occurrences (2.72, 5.24–26, 6.15).
  Earlier readers give three renderings; decide one row."
- **P5 §12, line 326–328:** add "This includes the published apparatus: a
  candidate offered by a secondary is recorded there only as `source_note` with
  the translator's name; its word and locus quotation stay in the private
  deviation file." BLD `public_wording` must then drop `word` and `locus` for
  non-dictionary candidates (X19).
- **P6 §17.1, lines 527–530:** correct to the measured "16 fallbacks, at least
  six on an affix or formation (dhruvam, dakṣaḥ, gatavyathaḥ, naraḥ, parama
  ×2): §13.4.2 not met" and "65 forks, 12 open". Add task G1.6: resolve or
  withdraw those fallbacks, and re-derive the five cards resting on Apte or MW
  (GRAMMAR_ENGINE §6).
- **P7 §8 gate, line 257:** append "fork construals, sandhi, the term line and
  each fallback are visible on the rendered card (STD §2); a semantic-field
  file exists for every content lemma with a recorded nirvacana or lexical
  field, with an independent review at its hash".
- **P8 L1, line 31:** "This amends STD §2 (commentary layer) for the Gītā, as
  recorded in STD §2 (S2)."

### Other documents

- **UI_DESIGN_STANDARD.md, Contextual surfaces (after line 203):** "Word cards
  in Sanskrit readers may hold a compact meaning summary. The full Meanings,
  Other construals and Sources sections open in the persistent reference panel.
  The wider Dāma evidence card (`reader.css` 31–35) is recorded here as a
  temporary exception until it migrates to that panel." Record the `z-index:
  600` in `gita.css` 363 in the migration audit.
- **AGENTS.md lines 32–40:** replace "Reference implementation:
  `gita/sthitaprajna/`" with "Reference implementation: `gita/ch12/` (after owner
  acceptance); meaning layer: Dāma semantic fields and Sahasranāma parallel
  derivations. Earlier Gītā readers are being migrated (standard §9)." Also
  change "voice-by-voice commentary" to "voice-by-voice commentary where the
  reader's plan includes it".
- **README.md line 40:** list `gita/ch12/` (mūla, recitation), `gita/ch5/` (mūla
  only, no audio), `gita/yogavasistha-dama/` and the Sahasranāma reader. Remove
  "recitation audio" from ch5.
- **AUDIO_ALIGNMENT_STANDARD.md lines 42–48:** "The repository has a local
  forced-alignment pipeline in `scripts/audio/` (models and licences recorded in
  each manifest; see the Gītā plan §5.2). Its output is `provisional` until
  owner listening."
- **IMPLEMENTATION_QUEUE.md P3 line 58:** "mūla Gītā readers predate the term
  policy and are queued for migration (STD §9, plan G1.5)". Under P-G add
  "G1.6 meaning layer for ch12 (semantic-field file, card sections), then
  migration of sp/kama/ch5."

### Checker and data amendments

- **CHK:** delete the `PRESERVE`/`TRANSLATE`/`PRES_FORMS` tables (19–44, 218).
  Instead, derive detectors from POL, with a per-reader `legacy` flag in a
  shared registry (also used by SLOT). Until migration, at least remove the
  `krodha` PRESERVE row and add `krodha → anger` to POL. Extend the card-field
  check: a gloss must not contain a row's forbidden rendering when the slot
  prints the preserved IAST. Add the Dāma reader and the Sahasranāma preface to
  the registry. Match POL English forms from an explicit `forms[]` list
  (plurals, verb forms) instead of `\b…\b` on the base word.
- **SLOT:** enforce `i` contiguity (STD §3) or amend §3 explicitly. Fail on an
  unresolved `glossaryKey` and an unresolved fork `words[]` index. Report slot
  maps whose slot text matches another word's gloss better than its own: that
  heuristic would have caught sp 2.59 and ch5 5.11 (fix those two now).
- **BLD:** emit `sandhi`, `term` and fork-to-word attachment into a renderable
  form. Write `meanings.js` from a reviewed semantic-field file. Type
  `fallback[].kind` and fail on root/pratyaya/compound fallbacks unless
  `--allow-unreviewed`. Strip secondary `word` and `locus` from the public
  apparatus (P5).
- **GJS:** render the term line, sandhi, `deva` under the headword, Meanings,
  Other construals and Sources (S1). Load `apparatus.json` and the semantic-field
  file in the `gita-ch12` registration (`assets/app.js` 5621–5630). Generalize
  Dāma's `appendWordEvidence` and VSN's `renderParallelDerivation` into one
  shared renderer.
- **`scripts/run_checks.sh`:** add `python3 scripts/validate_yogavasistha_dama_reader.py`
  and `python3 scripts/build_gita_chapter_reader.py 12 --check-only`.
- **POL new rows (owner-visible, each listing occurrences):** `sukha/at-ease`;
  `dhyana/dwell-on`; `para/higher` (comparative) and a separate `parayana` row;
  `asakta/unfastened` (a-sakta) and `sakta/fastened`; `jnana/ignorance`
  (*ajñāna*) and `jnanin/knower`; `mukta/freed-from` and `mukta/liberated`;
  `priya/pleasant` (neuter substantive); `nitya/constant`; `dhi` (distinct from
  buddhi, prajñā and mati); `sthira/steady` and `sthita` (one rendering);
  `vairin/enemy` with `satru/foe`; `viyukta` (distinct from *mukta*);
  `karma-yoga`; `krodha/anger`; `nirvana` (one rendering for 2.72, 5.24–26,
  6.15). Pilot rows awaiting the owner: cetas, dhyāna, duḥkha/sukha, dveṣa
  verb form ("bears" vs "feels", which needs one choice across readers),
  sama, śubha/aśubha, amṛta.
- **Glossary:** label the *kha* "axle-hole" analyses in `duhkha.json` and
  `sukha.json` as `nirvacana` with a locus, or withdraw them (EDITORIAL §8).
  Add a `translator_note` sentence to each POL-linked entry giving the reader's
  fixed rendering, so the glossary and the line agree openly.
- **VSN data:** recategorize name 109's *sa* + *Mā* derivation as reception
  (X18). Validators should reject a `traditional-nirvacana` whose only evidence
  is a modern author.

---

## Summary

1. The repository states its translation rules in about 60 places. STD §1–§8, PLAN §4, §6, §11–§13 and POL carry the core (§1 of this file).
2. There are 27 contradictions. Main ones: STD §8 says *krodha* → anger, but `check_gita_terms.js` line 34 still forces "krodha". *karma* is handled differently by STD, PLAN and the checker's two modes. On *dhyāna* and adverbial *sukha*, PLAN and POL disagree. The two spell *ahaṃkāra* differently. STD §3 lacks the fields the Gītā pipeline uses.
3. PLAN §17.1 under-reports: of the 16 fallbacks, at least six are on an affix. Five published cards rest on Apte or MW, which GRAMMAR_ENGINE §6 forbids. 12 forks are open, not 10.
4. The published `gita/ch12/apparatus.json` quotes secondary renderings in 57 candidate loci, against PLAN §12.
5. Chapter 12 uses none of the richer-meaning machinery: no semantic fields (Dāma), no parallel derivations or nirvacanas (Sahasranāma), no glossary `derivations`.
6. The ch12 card shows grammar but not meaning. `sandhi` (136 cards), `term` (92), `forks` (65), evidence and fallbacks are invisible; `note` is visible; `sense` and `grammar` are hidden by the owner's design.
7. Across readers ch12 agrees on buddhi, manas, indriya, śānti, bhaya, jñāna, yoga, saṃtuṣṭa and nirmama. It disagrees with ch5 on sama, sakta/asakta, tyāga, karma, harṣa, udvij, yatātman and sukha, and with sp on cetas, śubha, para and the sthita-/sthira- compounds. ch12 better meets §7 in almost every case.
8. sp breaks STD §1 (Keśava, Pārtha and Kaunteya are untranslated) and STD §7.6/§7.7 (two renderings each for *sthitaprajña* and *sthitadhī*). Two earlier slot maps are swapped (sp 2.59, ch5 5.11).
9. §5 gives exact amendment text that makes STD the one governing document with POL as its §8 table. It adds a closed §6.4 meaning-category list (with an owner choice on showing activation and synthesis), a full card contract and a §9 migration rule.
10. The checkers would then read POL only, cover every reader including Dāma, and fail on root/pratyaya/compound fallbacks and unresolved keys. The owner still decides the pilot rows, *karma-phala*, and the §6.4 display option.
