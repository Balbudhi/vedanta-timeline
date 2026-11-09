# Lexicon brief: decide a lemma's meaning and English once, for the whole Gītā

> **Retired (2026-11-09).** A brief for the stages A–E job queue, which is no longer used; kept here only because retired code names this path. Current documents: [`docs/history/gita/README.md`](../history/gita/README.md).

Serves queue jobs of type `lexicon` and `lexicon-fix` (Part A) and `lexicon-review`
and `lexicon-rereview` (Part B). Scope (lead, 2026-11-08): lemmas with three or more
Gītā occurrences, every lemma matching a table row or a preserved/system term of the
standard, and any lemma a verse job requests; every other content lemma is decided
inline in its verse job by the same register pass (VERSE_BRIEF step 5a). Output shape: `docs/gita_briefs/SCHEMAS.md`. Rules:
`docs/SANSKRIT_TRANSLATION_STANDARD.md` (the standard), which governs where this brief
is silent or seems to differ. Repository root: `/Users/eeshan/Dev/vedanta-timeline`.

## The owner's direction

Our English comes from the Sanskrit tradition and the dictionaries. It is richer,
freer and more exact than the published translations. Archaic or rare words and
fused (Joycean) formations are used when they carry the meaning more exactly, never
for their own sake. Nobody is followed blindly: not the commentators, not an earlier
draft of ours. Code has gathered every fact; you judge. Miss nothing the evidence
shows; type nothing code can look up.

## Forbidden

- Reading any published translation: English or word-for-word editions, Sri
  Aurobindo's renderings or *Essays on the Gita*, anything under
  `prakriya/sources/raw/upstream_data/secondaries/`, the English fields of the
  `gita/gita` index, `lookup.py gita`, web search. Other translations enter only in
  the verse reviewer's last, blind check.
- Writing anywhere except your job's `output` path. Never edit
  `data/glossary/term_policy.json`, scripts, readers, the queue, or other jobs' files.
- Citing a locus you did not see in your inputs or in a tool's output. Copy ids and
  loci; never type them from memory.
- Pipeline words in any reader-facing field (`gloss`, `image`, `why`, `forms`,
  `meaning_lines[].text`): no "row", "policy", "lexicon", "job", "batch", "owner",
  "reviewer", "pipeline", "fallback", no section numbers (standard §3.4).

## Your job record

`python3 scripts/gita/queue.py next --type lexicon` printed it: `id`, `inputs`, `output`,
`validate`. The first input (`….input.json`) lists per lemma its roots, Gītā forms,
occurrences (`C.V:i`), `existing_rows` (what the current table already decides),
`glossary_key`, `prior_renderings` and its `meaning_page`; then `reserved_english`.
The other inputs are the meaning pages and the current table. If `output` already
exists when you claim the job, this is a resumed or retried job: read
`queue.py show <id>`'s log, keep the file and repair it.

Each entry's `lemma` is the input's lemma (if you spell it differently, add
`"inventory": "<the input's lemma>"`). A sense the table already holds keeps its id
(`row.sense`, e.g. `upasana.attend-upon`) and its decision unless your evidence shows a
defect, which `why` then states; restate it fully with the new evidence (it is
migrated, not re-decided). New senses get new ids, lower-case ASCII `row.sense`.

## The kit (code; it locates, you decide)

```
# KIT = python3 -I /Users/eeshan/Dev/prakriya/scripts/gita_kit/gita_kit.py   (type it in full each time)
# LOOK = python3 /Users/eeshan/Dev/prakriya/scripts/lookup/lookup.py       (type it in full each time)
KIT meaning page LEMMA [--root ROOT]   # kośa groups (Amara+Amaraviveka, Halāyudha, Vaijayantī, Yādava),
                                        # Dhātuvṛtti/Kṣīrataraṅgiṇī/Dhātupradīpa, Nirukta/Nighaṇṭu,
                                        # MW/Apte/SKD/VCP/PW, Gītā concordance, prior site renderings
KIT verse packet LOCUS                 # one occurrence in full, incl. the commentators' glosses per pada
LOOK english "SENSE DESCRIPTION" --rich --limit 25   # English candidates; rare/archaic listed first
LOOK define WORD                       # the headword's own entries: cite only these
```

Your input file is the meaning page for each lemma, including `glosses`: every
commentator's gloss at every occurrence. Prior site renderings show what readers have
already seen; they are not authority.

## Part A: one lemma at a time (job type `lexicon`)

For each lemma in the batch. If the inventory lists a lemma that exists only because
of a wrong analysis (no occurrence really has that lemma), write
`{"lemma": "…", "skip": "the reason, naming the occurrences and the right analysis"}`
instead of an entry, and go on.

1. **Senses by occurrence.** Read every occurrence in the concordance with its
   commentators' glosses. A sense is what the word does in its sentence (its object,
   case frame, pairing), not its string. Group occurrences into senses; distinguish
   the senses the commentators distinguish.
2. **Root image.** From the Dhātupāṭha artha and the Dhātuvṛttis: what the body or
   the hand does in the root, and each upasarga's force (standard §7.4). One line.
3. **Nirvacana and tradition.** Nirukta/Nighaṇṭu, a commentator's semantic etymology
   (category `nirvacana`); the kośa synonym group (which words it is listed with, and
   where) and the dictionaries (`lexical`); what the Gītā's own usage settles
   (`usage`). A reading first attested in a modern author is never `nirvacana`.
4. **The three preserve tests** per sense (standard §8.1): (1) a term of the Gītā's own
   system in this sense; (2) no English word or short phrase carries it without adding,
   dropping or shading; (3) keeping it loses nothing, because card and glossary carry
   it. All three hold → preserve. A disputed referent (the commentators divide on
   *what* it names, §8.2) is evidence that test 2 fails; synonyms for one agreed
   sense are not.
5. **Plain and rich English** per translated sense (standard §7.17). Write a sense
   description from the Sanskrit evidence; search with it and with the root image
   (`english --rich`); run `define` on every candidate you cite. **Plain** = the
   plainest exact English. **Rich** = the richest exact English: a rare, archaic or
   literary attested word (obsolete/archaic tags do not disqualify). Choose rich when
   it carries the meaning more exactly *and* a reader understands the line on first
   hearing; else plain. Rarity is never a reason, either way. If plain is also the
   richest, say so. `chosen` is `plain`, `rich`, `joycean` (step 6) or `preserve`; a
   preserved sense also gives `iast`, the form printed in the line.
6. **Joycean formation** only when no attested word or short phrase is adequate after
   the whole stack has been searched: record it (below), never call it attested, and
   drop it if it adds an image, agency or claim the Sanskrit lacks. Short,
   transparent, reads as English.
7. **Forms** per grammatical category the Gītā actually uses. Keys, and only these:
   `verb`, `verb+<upasarga>` (e.g. `verb+pari`), `noun`, `plural`, `predicate`,
   `adjective`, `adverb`, `participle_past`, `participle_present`, `absolutive`
   ("having …"), `infinitive`, `agent`, `any`. Values are a string or a list. Regular
   English inflections (-s, -ed, -ing) are added by code; list only irregular ones
   ("bear, bore, borne"). A preserved noun stays a noun; a verb of the same root is
   translated (§7.12). Avoid the devices
   of §7.16 (agent-noun calques, adjectives forced to head a noun phrase, bare
   "whatsoever", Sanskrit nouns in English verb frames, hybrid compounds).
8. **Forbidden and reserved English.** `forbidden`: renderings that add, drop or shade
   this sense, each refuted in `why` or by the evidence. Distinctness (§7.6): two
   Sanskrit words never share one English word; the validator reports collisions with
   the table and other batches. Fix a collision by a better word, never a worse one.
9. **meaning_lines**: 2–6 lines selected from the evidence, ordered `formation`,
   `lexical`, `nirvacana`, `usage`, each with `who` and `locus` copied from the page.
   Per-verse commentator glosses are chosen later by the verse producer; put here only
   what holds for the lemma across the Gītā. Choose the lines that show the reader
   the root image, the operative sense and every distinct traditional reading.
10. **Read it aloud.** Put the chosen English into two real occurrences in your head;
    if a form cannot stand in an English sentence, choose again.

`why` is the reader's answer to "why this English": what it keeps, what the
alternatives drop, and, for a preserved sense, the three tests in plain words.

Joycean record (SCHEMAS `joycean`, else `null`):
`{"expression": "upbearer", "parts": [{"form": "upbear", "sense": "to bear up, raise
aloft", "source": "webster1913_pg29765.txt:919846"}, {"form": "-er", "sense": "agent",
"source": "English agent suffix"}], "relation": "agent of the attested verb",
"paraphrase": "one who lifts up and out", "line_context": "12.7 …I am the upbearer…",
"attested": false}`.

Write the output incrementally, one lemma at a time, as valid JSON:
`{"schema": "gita-lexicon-v1", "job": "<id>", "entries": [...]}`. Then run the job's
`validate` command verbatim; fix until it passes (at most three runs, then stop and
report); then `python3 scripts/gita/queue.py submit <id>`.
If the validator rejects something this brief requires, stop and report its message.

### Worked example 1: upāsanā (translated)

Evidence used: Dhātupāṭha √ās adādi 2Ā *upaveśane*; MW `mw.json#42231`, Apte
`ap90.json#9131`; Śaṅkara on 12.3 (`shankara_gita_bhasya.txt:8411`) defines
*upāsana* from the root image; glosses: *dhyāyanti* (Śaṅkara, Śrīdhara on 12.1),
*sadā cintayanti* (Madhusūdana), *smṛtiṃ kurvanti* (Ānandagiri), *ārādhayanti*
(Śrīdhara on 12.2), *tvat-samīpa āsate* (Vallabha). Usage: 12.6 *dhyāyanta upāsate*
keeps meditating and attending apart; objects include a sacrifice (4.25) and a
teaching (12.20). Tests: not a system category in a sense English cannot carry →
translate. `english --rich` offered *atsit* (obsolete, "to remain sitting").

```json
{ "lemma": "upāsanā", "match": "(^|-)(upās|paryupās|upāsan)",
  "senses": [ {
    "id": "upasana.attend-upon",
    "gloss": "to come near and stay at hand in attention and service",
    "image": "√ās 'sit' with upa 'near': to come close and sit there, at hand",
    "preserve": false,
    "forms": { "verb": "attend upon", "verb+pari": "attend wholly upon", "noun": "attendance upon" },
    "plain": { "word": "attend upon", "locus": "sources/raw/upstream_data/english/webster1913_pg29765.txt:57966" },
    "rich":  { "word": "atsit", "locus": "sources/raw/upstream_data/english/kaikki-english/kaikki.org-dictionary-English.jsonl.gz:525701#s0", "tags": ["obsolete"] },
    "chosen": "plain",
    "why": "'Attend' has in its own dictionary entry all three senses of the Sanskrit: to be near at hand in waiting, to direct the mind upon, to be present at a rite. 'Meditate' is a commentator's explanation and would merge two verbs the Gītā keeps apart (12.6); 'worship' cannot take a teaching as its object (12.20). The old 'atsit' keeps the sitting but loses the nearness and the attention, and would stop a reader. With pari, 'wholly': entirely, to the exclusion of other things.",
    "joycean": null,
    "forbidden": ["worship", "meditate", "wait upon", "serve", "seek after"],
    "meaning_lines": [
      { "cat": "lexical", "text": "to sit near at hand, wait upon; to be intent upon; to be present at a rite", "who": "Monier-Williams; Apte", "locus": "sources/raw/upstream_data/kosha/mw.json#42231; sources/raw/upstream_data/kosha/ap90.json#9131" },
      { "cat": "nirvacana", "text": "going near the object and sitting with it a long time, one thought flowing on like a stream of oil", "who": "Śaṅkara on 12.3", "locus": "data/sources/sanskrit/vedanta/shankara_gita_bhasya.txt:8411" },
      { "cat": "usage", "text": "The Gītā sets it beside meditating as a different act ('meditating, they attend upon me', 12.6), and gives it a sacrifice (4.25) and a teaching (12.20) as objects.", "who": "Gītā", "locus": "data/sources/sanskrit/vedanta/bhagavadgita_mula_bori.txt:2592" } ],
    "occurrences": ["4.25", "9.14", "9.15", "9.22", "12.1", "12.2", "12.3", "12.6", "12.20", "13.7", "13.25"] } ] }
```

Why this is good: one sense, because every occurrence does the same thing; the image
is the body's; the rich candidate was searched, defined and declined for a stated
reason; the forbidden words are each refuted by the Gītā's own usage, not by taste.

### Worked example 2: kūṭastha (preserved)

Evidence: Amarakośa 3.1.148–149 defines the lexeme *ekarūpatayā tu yaḥ kālavyāpī sa
kūṭasthaḥ* (`amarakosha_gretil_clean.txt:1796`); MW `mw.json#60703`, `#60705`.
The commentators divide five ways on what it names: standing over māyā (the false
thing, *kūṭa*) as its ground (Śaṅkara's first reading `shankara_gita_bhasya.txt:8411-8412`,
with Madhusūdana, Nīlakaṇṭha, Śrīdhara); standing like a heap, unmoving (Śaṅkara's
second); common to all (Rāmānuja `ramanuja_gita_bhasya.txt:2607`, Deśika); standing in
space (Madhva `madhva_gita_bhasya.txt:5414-5416`); one in form through time (Amara).
The Gītā defines *akṣara* by it (15.16) and says it of the yogin (6.8). A formation
"summit-standing" was considered and rejected: it rests on one member-sense of *kūṭa*
that no commentator reads here, so it adds an image (standard §7.17).

```json
{ "lemma": "kūṭastha", "match": "kūṭasth",
  "senses": [ {
    "id": "kutastha.system",
    "gloss": "standing on the kūṭa: what stands unmoved amid change, read by the tradition as its ground and witness, as fixed like a heap, as common to all, or as one in form through all time",
    "image": "√sthā 'stand' on a kūṭa: a heap, a peak, an anvil, and also a false thing, a counterfeit",
    "preserve": true, "iast": "kūṭastha",
    "forms": { "noun": "the kūṭastha", "predicate": "kūṭastha" },
    "plain": { "word": "unchanging", "locus": "sources/raw/upstream_data/english/kaikki-english/kaikki.org-dictionary-English.jsonl.gz:55244#s0" },
    "rich":  { "word": "immoved", "locus": "sources/raw/upstream_data/english/kaikki-english/kaikki.org-dictionary-English.jsonl.gz:410853#s0", "tags": ["archaic"] },
    "chosen": "preserve",
    "why": "Kept in Sanskrit. The Gītā uses the word to define the imperishable (15.16) and to describe the yogin (6.8). The commentators read five different things in it, and every English word picks one: 'unchanging' takes the kośa's reading, 'immoved' the heap, 'common to all' Rāmānuja's; 'unchanging' would also blur it with 'unmoving' (acala) in the same verse. The card and the glossary give all five readings.",
    "joycean": null,
    "forbidden": ["unchanging", "immutable", "immovable", "immoved", "common to all", "summit-standing", "peak-like"],
    "meaning_lines": [
      { "cat": "lexical", "text": "what pervades time in one form", "who": "Amarakośa 3.1.148–149", "locus": "sources/primary/lexica/amarakosha/amarakosha_gretil_clean.txt:1796" },
      { "cat": "nirvacana", "text": "kūṭa is the false thing that looks good outside, māyā; the kūṭastha stands over it as its overseer; or: standing like a heap, unmoving", "who": "Śaṅkara on 12.3", "locus": "data/sources/sanskrit/vedanta/shankara_gita_bhasya.txt:8411-8412" },
      { "cat": "nirvacana", "text": "common to all", "who": "Rāmānuja on 12.3", "locus": "data/sources/sanskrit/vedanta/ramanuja_gita_bhasya.txt:2607" },
      { "cat": "nirvacana", "text": "kūṭa is space; what stands in space", "who": "Madhva on 12.3", "locus": "data/sources/sanskrit/vedanta/madhva_gita_bhasya.txt:5414-5416" },
      { "cat": "usage", "text": "The Gītā defines the imperishable by it (15.16) and says it of the yogin (6.8).", "who": "Gītā", "locus": "data/sources/sanskrit/vedanta/bhagavadgita_mula_bori.txt:3056" } ],
    "occurrences": ["6.8", "12.3", "15.16"] } ] }
```

Why this is good: the disputed referent is shown by the commentators' divergence,
not by any translation; plain and rich were still searched, so the reader learns why
English fails; every reading is on the card with its locus.

## Part A, fix (job type `lexicon-fix`)

Inputs: your batch file and the lexicon review. If you can be resumed in the session
that wrote the batch, you will be; otherwise read the batch and the review first.
Fix every S1 and S2 finding in your output file; S3 at your judgement. Change nothing
a finding does not name. Re-run `validate`; submit.

## Part B: reviewing a batch (job types `lexicon-review`, `lexicon-rereview`)

You did not write this batch. Record `shasum -a 256 <lexicon output>` as
`lexicon_sha256`; if it changes while you review, stop and report. Recompute from the same meaning pages; do not trust.
Per lemma and sense:

1. **Occurrences** complete (compare the concordance) and grouped by what the word
   does; none given a sense it does not have.
2. **Evidence**: every `meaning_lines` locus exists in the page and says what the line
   says; each line in its right category; no distinct traditional reading left out.
3. **Image**: the root's bodily image, from the Dhātupāṭha and Dhātuvṛttis.
4. **Tests**: each argued from the sources; a preserve decision on a disputed referent
   rests on the commentators' divergence.
5. **Candidates**: run `define` on plain, rich and the chosen word; the definition is
   the headword's own and carries the sense without adding, dropping or shading. Search
   once yourself for a better word. A formation is admissible only per step 6.
6. **Readability**: each form in a real occurrence, read aloud; a §7.16 device is a
   finding.
7. **Distinctness, forms, forbidden**: no collision; forms cover the occurrences;
   forbidden words refuted.
8. **Public text** in every reader-facing field; no translation text anywhere.

Severity: **S1** wrong sense or unsupported claim; a test wrongly passed or failed; a
collision; an inadmissible formation; a form that does not parse; a §7.16 device;
pipeline words in a public field. **S2** richness the evidence documents but the entry
drops (a traditional reading, the root image, a better attested word). **S3** style.
Verdict `accept` only when no S1 is open.

Output (`gita-lexicon-review-v1`, SCHEMAS.md amendments):

```json
{ "schema": "gita-lexicon-review-v1", "job": "lexicon-review-0007", "lexicon_job": "lexicon-0007", "lexicon_sha256": "…",
  "findings": [ { "lemma": "…", "sense": "…", "severity": 1, "check": "occurrences|evidence|image|tests|candidates|readability|distinctness|public",
                  "says": "…", "should_be": "…", "evidence": ["locus", "quote"] } ],
  "verdict": "accept" }
```

**Re-review** (`lexicon-rereview`): inputs are the batch as reviewed, the batch as
fixed, and your review. Check only the changed fields against each finding, plus one
lemma recomputed in full. Write a new review file: the findings still open, carried
over verbatim, plus any new ones; `verdict` as above.
