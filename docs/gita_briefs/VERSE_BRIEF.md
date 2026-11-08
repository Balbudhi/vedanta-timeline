# Verse brief: one shard of the Gītā, word by word

Serves queue jobs of type `verse` (main part) and `fix` (last section). Output shape:
`docs/gita_briefs/SCHEMAS.md` (verse job). Rules: `docs/SANSKRIT_TRANSLATION_STANDARD.md`
(the standard), which governs where this brief is silent or seems to differ; §7 is the
line style you apply on every verse. Repository root: `/Users/eeshan/Dev/vedanta-timeline`.

## The owner's direction

Our English comes from the Sanskrit tradition and the dictionaries, through the
lexicon. It is richer, freer and more exact than the published translations, and a
reader understands every line on first hearing. Code has generated every analysis,
derivation and gloss; you choose among them and write the line. Miss nothing the
evidence shows; type nothing code can look up.

## Forbidden

- Reading any published translation (English or word-for-word editions, Sri
  Aurobindo, `prakriya/sources/raw/upstream_data/secondaries/`, the English fields of
  the `gita/gita` index, `lookup.py gita`, web search).
- Writing anywhere except your job's `output` path. Never edit the lexicon
  (`data/glossary/term_policy.json`), packets, scripts, readers, the queue or other
  shards.
- Typing grammar the oracle gives: use its analysis `id`. A manual analysis only where
  the packet has no analysis that fits, then stated in full.
- Improvising a rendering: every content word takes a lexicon sense, an inline decision
  made by step 5a, or a lexicon request (below).
- Supplying content words; changing mood, voice or form; pipeline words ("row",
  "lexicon", "policy", "job", "shard", "owner", "reviewer", "fallback", section numbers)
  in `english`, `line`, `note`, `sense`, `display`, commentator line text.

## Inputs

- `internal/gita_pipeline/packets/commentary/<CH.V>.json` per verse: the full Sanskrit commentary passages (step 0).

`python3 scripts/gita/queue.py next --type verse` printed your job record: `id`,
`inputs` (the verse packets of the shard and the lexicon entries for its lemmas, from
the frozen lexicon), `output`, `validate`. If `output` already exists, this is a
resumed or retried job: read `queue.py show <id>`'s log and repair the file.

Each packet gives, per verse: the BORI saṃhitā and Devanāgarī; split candidates that
recompose to it; per pada every `Analysis` (id, stem, root with gaṇa/pada, affixes,
case, tense, person, number) with its derivation (sūtra by sūtra, each sūtra located);
the commentators' glosses on the pada. To look further:

```
# KIT = python3 -I /Users/eeshan/Dev/prakriya/scripts/gita_kit/gita_kit.py   (type it in full each time)
KIT grammar split 12.2            # split candidates
KIT grammar analyze yuktatamāḥ    # every analysis of a form (e.g. a compound member)
KIT verse packet 12.2             # the packet again
KIT meaning page LEMMA            # only to write a lexicon request
```

## Steps, per verse

0. **Read what the verse leaves unsaid, first.** Open
   `internal/gita_pipeline/packets/commentary/<CH.V>.json` for each verse of the shard
   (every Sanskrit commentary passage the library holds on the verse, with the previous
   and next verse; no published translation is in it). Read every passage for: (a)
   **anvaya**, the order in which each commentator construes the words; (b)
   **adhyāhāra**, the words he supplies (an elided verb, subject or object; "iti
   śeṣaḥ", "ity arthaḥ"); (c) **referents** of ye, te, tat, evam, yathoktam, atha; (d)
   **sentences across verses**, a relative here with its correlative in the next verse
   (12.3 → 12.4, 12.13 → 12.14, 12.18 → 12.19); (e) **tātparya**, what the verse does
   in the argument (why this follows that). Where the commentators construe or supply
   differently and grammar admits both, open a fork. Supplied words never enter the
   line (standard §7.3, §7.14): the sense paragraph or a note carries them, attributed
   ("Śaṅkara supplies …"). The per-word glosses in the verse packet do not replace this
   reading; they are the same commentators cut down to one word.
1. **Split.** Choose the pada split from the candidates. Compound members are joined by
   `-` in `padas`. Speaker lines (`arjuna uvāca`) are not padas. The split must
   recompose to the saṃhitā; the validator checks it.
2. **Analysis per pada.** Choose the analysis `id` that this sentence requires, among
   all the packet offers (homonymous roots, other gaṇas, other cases with the same
   ending). If none fits, write `{"manual": Analysis}` with every field of the
   Analysis shape filled, `source: "manual"` and no `id`; code tries to derive it and
   flags what it cannot.
3. **Compounds**: type (tatpuruṣa with its case, karmadhāraya, dvigu, bahuvrīhi,
   dvandva, avyayībhāva), vigraha in Sanskrit, members each with an analysis id
   (`grammar analyze MEMBER`) or a manual analysis.
4. **Kāraka**: the Pāṇinian role tied to the actual verb ("karman of upāsate"); for
   non-kāraka relations name them (viśeṣaṇa of …, ṣaṣṭhī of …, sambodhana).
5. **Sense**: the lexicon sense id for every content word (noun, verb, adjective,
   adverb, participle, compound, meaningful name); `null` for particles, pronouns and
   copulas. The lexicon covers lemmas with three or more Gītā occurrences, every lemma
   with a table row or a system term, and any lemma requested. If the lemma has an
   entry but no sense fits here, file a **lexicon request** (below). If the lemma has
   no entry at all, decide it inline (5a).
   5a. **Inline decision** (the lexicon's register pass, for one or two occurrences).
   Open the lemma's meaning page (`KIT meaning page LEMMA`). Write a sense description
   from the Sanskrit evidence; search with it and with the root image
   (`LOOK english "…" --rich`); run `LOOK define` on every candidate you cite. The word
   then carries `sense: null` and: `image` (the root's bodily image, one line);
   `plain` and `rich` (`{word, locus}` from the headword's own entry, `rich` may be
   `null` if nothing richer is exact); `chosen` (`plain`, `rich` or `joycean`; a
   Joycean formation only when no attested word or short phrase is adequate, recorded
   as in LEXICON_BRIEF, standard §7.17); `why` (reader-facing: what the English keeps,
   what the alternatives drop); `meaning_lines` (1–4, categories `formation`,
   `lexical`, `nirvacana`, `usage`, `who` and `locus` copied from the page). Choose rich
   when it is more exact *and* reads on first hearing. If the word seems to need
   keeping in Sanskrit, do not decide it inline: file a lexicon request. If the lemma
   also occurs outside your shard (the page's concordance), decide for both
   occurrences and say so in `why`. After review these become lexicon entries.
   (`LOOK` = `python3 /Users/eeshan/Dev/prakriya/scripts/lookup/lookup.py`.)
6. **English** per word: the lexicon's form for the word's grammatical category. A
   preserved term is an English noun (plural -s, articles as English needs). `english`
   is exactly the text of the slot carrying the word.
7. **The line** (`line`), slotted `{i:text}`, every word index slotted once; one
   English word for two Sanskrit words is one slot `{i,j:text}`. Apply standard §7:
   - every word and feature surfaces (§7.1); nothing added (§7.3); the root's image
     kept where the Sanskrit carries it (§7.4); distinct words stay distinct (§7.6);
   - mood as present: statements stay statements; optative "should"; imperative a
     command; no question mark without *kim*, *katham*, *kva*…; *atha*/*cet*/*yadi*
     with an indicative protasis may be "If …, then …" (§7.8);
   - ktvā/lyap "having …"; kta past participle (stative English for posture verbs:
     "leaning on", "seated"); śatṛ/śānac "-ing"; tumun "to …"; kṛtya "to be …" (§7.9);
   - epithets by etymology, "O son of Kuntī" (§7.10); sentences may run across
     verses: em dash, next verse lower case (§7.13); elided objects stay elided (§7.14);
     function words may be supplied unslotted, content words never (§7.15);
   - none of the devices of §7.16 unless the lexicon entry approves it.
8. **Read the slotted line aloud** with the braces stripped, as a listener who opens
   no card. If it does not parse on first hearing, rewrite it (word order, a richer
   exact word from the lexicon forms); never by adding or dropping meaning.
9. **Forks** (standard §6.5) wherever more than one construal is grammatically
   admissible: split, sandhi, case force, compound type, referent, sense, negation
   scope, sentence boundary. Each with `words`, `construals` (`reading`,
   `grammar_basis`, `evidence` loci, `traditions` = commentators who take it),
   `followed`, `reason_class` (1 grammar excludes, 2 the Gītā's usage settles, 3 kośa
   lacks the sense, 4 English stays open, 5 English forces a choice), `reason` (never
   "X reads it so"), `open` (true exactly for class 5), `display` (one or two sentences
   for a reader). Every fairness locus your job record lists must carry a fork.
10. **commentator_lines**: per content word, every distinct gloss the packet found for
    this word in this verse (standard §6.4), most telling first (the card shows the
    first three; the reader's panel shows all). Keep only hits that actually gloss
    this word; commentators who give the same gloss share one line (all names in
    `who`). Copy `locus` and the Sanskrit; give its English after it in `text`
    ("*dhyāyanti* — they meditate").
11. **sense**: one plain paragraph per verse, nothing beyond the words. `note`: only
    a reader-facing ambiguity or clarification.
12. **Optional per word**: `word_class` (`content`, `particle`, `pronoun`, `name`,
    `copula`) only when the oracle's class is wrong for this use; `form_note`, one
    reader-facing sentence when English cannot render the form exactly and the line
    departs from it (e.g. a kta of a posture verb rendered "leaning on", §7.9).

**Lexicon request** (SCHEMAS top level, exactly this shape):
`"lexicon_requests": [{"lemma": "…", "sense": "<existing sense id>" | null, "locus":
"12.2:5", "proposal": <a gita-lexicon-v1 entry made by LEXICON_BRIEF Part A from the
meaning page>, "why": "…"}]`. One request per lemma; `locus` names its first
occurrence in the shard. `sense: null` for a lemma or sense the lexicon lacks: every
occurrence then takes the proposal's sense id and English. `sense` set to an existing
id when that sense misfits here: render per the existing entry, and `proposal` gives
the amended entry. `why` is the evidence for the request. The verse reviewer reviews
it with the shard; accepted requests are merged after review.

Top level of the output: `{"schema": "gita-verse-v1", "job": "<id>", "verses": [...],
"lexicon_requests": [...]}`, verses in order. When the shard is written, run the job's
`validate` command verbatim (recomposition, ids, sense ids, slots, public text); fix
until it passes (at most three runs, then stop and report); then
`python3 scripts/gita/queue.py submit <id>`. If the validator rejects something this
brief requires, stop and report its message.

## Worked example: 12.2

*mayy āveśya mano ye māṃ nityayuktā upāsate | śraddhayā parayopetās te me yuktatamā
matāḥ ||* `<…>` marks ids and loci copied from the packet, never typed; the sense
ids are illustrative (use the lexicon's).

```json
{ "locus": "12.2",
  "padas": ["mayi", "āveśya", "manaḥ", "ye", "mām", "nitya-yuktāḥ", "upāsate", "śraddhayā", "parayā", "upetāḥ", "te", "me", "yukta-tamāḥ", "matāḥ"],
  "words": [
    { "i": 0, "analysis": "<asmad, saptamī ekavacana>", "compound": null, "karaka": "adhikaraṇa of āveśya", "sense": null, "english": "in me", "commentator_lines": [] },
    { "i": 1, "analysis": "<ā-√viś ṇic + lyap>", "compound": null, "karaka": "prior action, same agent as upāsate", "sense": "avesa.lodge", "english": "having lodged",
      "commentator_lines": [ { "who": "Madhusūdana", "locus": "<…>", "text": "as lac takes the colour of the vermilion it is steeped in" } ] },
    { "i": 2, "analysis": "<manas, dvitīyā ekavacana>", "compound": null, "karaka": "karman of āveśya", "sense": "manas.faculty", "english": "the manas", "commentator_lines": [] },
    { "i": 5, "analysis": "<nitya-yukta, prathamā bahuvacana puṃliṅga>", "compound": { "type": "dvitīyā-tatpuruṣa", "vigraha": "nityaṃ yuktāḥ",
        "members": [ { "form": "nitya", "analysis": "<nitya avyaya>" }, { "form": "yuktāḥ", "analysis": "<√yuj kta, prathamā bahuvacana>" } ] },
      "karaka": "viśeṣaṇa of ye", "sense": "yukta.yoked", "english": "constantly yoked", "commentator_lines": [] },
    { "i": 6, "analysis": "<upa-√ās laṭ prathama-puruṣa bahuvacana ātmanepada>", "compound": null, "karaka": "kriyā: kartṛ ye, karman mām", "sense": "upasana.attend-upon", "english": "attend upon",
      "commentator_lines": [
        { "who": "Madhusūdana; Nīlakaṇṭha", "locus": "<…>", "text": "*sadā cintayanti* — they think of continually" },
        { "who": "Ānandagiri", "locus": "<…>", "text": "*mayi smṛtiṃ sadā kurvanti* — they keep me always in remembrance" },
        { "who": "Śrīdhara", "locus": "<…>", "text": "*ārādhayanti* — they propitiate" } ] },
    { "i": 9, "analysis": "<upa-√i kta, prathamā bahuvacana puṃliṅga>", "compound": null, "karaka": "viśeṣaṇa of ye; governs śraddhayā (instrumental)",
      "sense": null, "english": "endowed with",
      "image": "√i 'go' with upa 'near': one who has come near, arrived",
      "plain": { "word": "endowed with", "locus": "sources/raw/upstream_data/english/webster1913_pg29765.txt:283983" },
      "rich": null, "chosen": "plain",
      "why": "With the instrumental, the participle of 'come near' means furnished with what one has come to; 'endowed' says this of a quality given, as faith here is. The obsolete 'qualitied' (furnished with qualities) is no more exact and would stop a reader.",
      "meaning_lines": [
        { "cat": "lexical", "text": "one who has come near, arrived at; accompanied by, endowed with, furnished with", "who": "Monier-Williams", "locus": "sources/raw/upstream_data/kosha/mw.json#42326; sources/raw/upstream_data/kosha/mw.json#42330" },
        { "cat": "usage", "text": "Both times the Gītā uses it, it is of faith: 'endowed with faith' (6.37, 12.2).", "who": "Gītā", "locus": "data/sources/sanskrit/vedanta/bhagavadgita_mula_bori.txt:1524" } ],
      "commentator_lines": [] },
    { "i": 11, "analysis": "<asmad, ṣaṣṭhī ekavacana, enclitic me>", "compound": null, "karaka": "ṣaṣṭhī of the agent with a present-sense kta (matāḥ)", "sense": null, "english": "by me", "commentator_lines": [] }
  ],
  "line": "{3:Those who}, {1:having lodged} {2:the manas} {0:in me}, {5:constantly yoked}, {6:attend upon} {4:me}, {9:endowed with} {8:the highest} {7:faith} — {10:they} are {13:deemed} {11:by me} {12:the most yoked}.",
  "sense": "Those who have settled the manas in Kṛṣṇa and, constantly yoked and endowed with the highest faith, attend upon him, are deemed by him the most yoked.",
  "forks": [ { "at": "nityayuktāḥ", "words": [5],
    "construals": [
      { "reading": "constantly yoked, as 'ever yoked' in 12.1", "grammar_basis": "nitya adverbial in a tatpuruṣa with the kta", "evidence": ["<Śaṅkara on 12.2>"], "traditions": ["Śaṅkara", "Śrīdhara", "Madhusūdana"] },
      { "reading": "longing to be yoked for ever", "grammar_basis": "yukta as 'joined to' a goal, with a desire supplied", "evidence": ["<Rāmānuja on 12.2>"], "traditions": ["Rāmānuja"] } ],
    "followed": 0, "reason_class": 4, "reason": "'constantly yoked' leaves the object of the yoking unsaid, as the Sanskrit does; the second reading supplies a desire the words lack.", "open": false,
    "display": "Rāmānuja reads 'constantly yoked' as 'longing for perpetual union'; the other commentators take it as in 12.1." } ] }
```

(Words 3, 4, 7, 8, 10, 12, 13 are omitted here for length; a real shard has every word.
Word 9, *upetāḥ*, has two Gītā occurrences and no lexicon entry, so it is decided
inline by step 5a.)
Read aloud: "Those who, having lodged the manas in me, constantly yoked, attend upon
me, endowed with the highest faith — they are deemed by me the most yoked." It parses;
the lyap is "having …" (§7.9); *me* with the present-sense kta is "by me", not "in my
view"; "Those" and "are" are unslotted function words; *yuktatamāḥ* keeps the
superlative and the yoke rather than inserting "yogis".

Had the packet offered no analysis of *yuktatamāḥ*, word 12 would read:
`"analysis": {"manual": {"form": "yuktatamāḥ", "kind": "taddhitanta", "stem":
"yuktatama", "dhatu": {"aupadeshika": "yujir", "root": "yuj", "gana": 7, "gana_name":
"rudhādi", "pada": "ubhayapada", "artha": "yoge", "upasargas": [], "dp_locus": "<from
grammar analyze yuktāḥ>"}, "krt": "kta", "taddhita": "tamap", "vibhakti": "prathamā",
"vacana": "bahuvacana", "linga": "puṃliṅga", "lakara": null, "prayoga": null,
"purusha": null, "source": "manual"}}`: every field stated, the root record copied
from the oracle's analysis of the base.

## Fix (job type `fix`)

Inputs: your shard and its review (`gita-review-v1`). If your runtime resumes the
session that wrote the shard, you are that session; otherwise read the shard, the
review and the packets first. Fix every S1 and S2 finding in your own file; S3 at your
judgement. A finding that asks for a different sense of a lexicon lemma is answered
with a lexicon request, not a silent change; an inline decision is revised in place. Change nothing a finding does not name. Re-run
`validate`; submit. The reviewer checks only the diff.
