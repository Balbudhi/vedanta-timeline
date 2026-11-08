# Review brief: one pass over one Gītā shard, the blind check last

Serves queue jobs of type `review` (main part) and `rereview` (last section). Output
shape: `docs/gita_briefs/SCHEMAS.md` (review job). Rules:
`docs/SANSKRIT_TRANSLATION_STANDARD.md` §5.1 (this review), §6 and §7 (what is right),
§9 (other translations). What the producer was told: `docs/gita_briefs/VERSE_BRIEF.md`.
Repository root: `/Users/eeshan/Dev/vedanta-timeline`.

## The owner's direction

The review must be something the owner can trust. You did not write this shard: you
recompute, you do not believe. Code has checked everything exact (recomposition, ids,
derivations, loci, slots, the lexicon's renderings and forbidden words, pipeline
words); you judge what code cannot: the choice among analyses, the form in the line,
the meaning, whether the line reads, the forks. Our English must come from the Sanskrit
and the dictionaries; other translations are a last, blind check, never a reason.

## Forbidden

- Opening the secondaries before checks 1–7 are written for every verse of the shard.
- Writing anywhere except your job's `output` path. You never edit the shard, the
  lexicon, packets, scripts or the queue; the producer fixes from your file alone.
- Any finding whose reason is "a translation (or a school) says so".
- Copying more than a few words of a published translation into your output.

## Inputs and setup

`python3 scripts/gita/queue.py next --type review` printed your job record. Its first
input file names: `verse_output` (the shard you review), `frozen_copy`,
`expanded_shard` (the cards as a reader will get them), `expansion_report` (the
validator and builder report), `packets`, `secondaries`
(`internal/gita_pipeline/secondaries/CH.json`, private), `fairness` (loci that must
carry a fork) and, for a re-review, `previous_review` and `shard_as_reviewed`.

1. `shasum -a 256 <verse_output>` → `shard_sha256`. If it changes while you review,
   stop and report.
2. `git check-ignore -q <output> && git check-ignore -q <secondaries file>`; if either
   is not ignored, stop and report: your file will quote translations and the
   repository is public.
3. Read the validator report; do not re-check what it verified.

Tools: `python3 -I /Users/eeshan/Dev/prakriya/scripts/gita_kit/gita_kit.py`
(`grammar analyze|derive|split`, `verse packet`, `meaning page`) and
`python3 /Users/eeshan/Dev/prakriya/scripts/lookup/lookup.py define WORD`.

## The pass: every verse, these seven checks in order

1. **Grammar choice vs alternatives.** Before reading the producer's choices, pick the
   split and the analysis per pada yourself from the packet. Compare. For each word try
   the plausible wrong alternative the packet offers (other root or gaṇa, other case
   with the same ending, other compound type, other kāraka) and confirm the sentence
   excludes it; if it does not, a fork is required. Recompute every manual analysis in
   full, and check the derivation report: a manual analysis that code could not derive
   must be right on Pāṇini's terms.
2. **Form in the line.** Every mood, voice, tense and non-finite form in the line equals
   the analysis (standard §7.8–§7.9): no statement printed as a question; lyap "having
   …"; kta a past participle; śatṛ "-ing"; optative "should"; agent forms not calques.
3a. **What the verse leaves unsaid.** Read the commentary packet
   (`internal/gita_pipeline/packets/commentary/<CH.V>.json`) yourself: check the
   producer's construal against each commentator's anvaya, that every supplied word
   (adhyāhāra) a commentator states is either reflected in the sense paragraph or a note
   (attributed) or rejected with a reason, that pronoun and evam/yathoktam referents are
   right, that a sentence running into the next verse is read as one, and that every
   construal on which commentators differ and grammar admits both has a fork. A missed
   construal or a wrong referent is S1.
3. **Meaning vs lexicon and evidence.** Each content word carries a lexicon sense that
   fits *this* occurrence and the lexicon's English form for its category. The root's
   image survives in the line where the Sanskrit carries it (§7.4). The commentator
   lines are real glosses of this word; agreeing commentators share a line; no
   distinct gloss in the packet is left out (standard §6.4). Every lexicon request is reviewed by
   `LEXICON_BRIEF.md` Part B. Every inline decision (`sense: null` on a content word,
   VERSE_BRIEF step 5a) gets the same meaning check as a lexicon entry: open its
   meaning page and the `define` entries of `plain`, `rich` and the chosen word; the
   sense fits the evidence and the occurrence; the image is the root's; the chosen word
   adds, drops and shades nothing; a formation only per standard §7.17; search once
   yourself for a better word; `why` and `meaning_lines` are reader English with real
   loci; a word that needs keeping in Sanskrit was not decided inline. These decisions
   become lexicon entries after your review, so an error here is an error everywhere.
4. **Readability aloud.** Strip the braces and read each line aloud as a listener with
   no card. It parses on first hearing (§7.16); none of the §7.16 devices without an
   approving entry. For a line that is exact but stiff, give better exact English with
   its `define` entry, never a looser meaning.
5. **Policy fit.** Whether the lexicon entry is right for this occurrence (code checks
   compliance). If not: a finding with `check: "policy"` whose `should_be` states the
   amendment; the producer answers with a lexicon request. Decisions already in the
   lexicon are reviewed like any other.
6. **Forks.** Every admissible construal recorded; grammar basis real; reason class
   1–5, never a school's authority; `open` true exactly for class 5; `words` right;
   `display` clear to a reader; every fairness locus in the job record carries one.
7. **Public text.** Read `line`, `english`, `note`, `sense`, `display` and commentator
   line text as a reader: no pipeline words, no dangling references ("see above"), no
   Sanskrit left untranslated in a commentator line.

**Severity.** **S1**: a wrong analysis or unsupported claim; a dropped or added meaning;
a mood or form change; a sense that does not fit the occurrence; a line that does not
parse; a §7.16 device without an approving entry; pipeline words in a public field; a
missing fork at a fairness locus. **S2**: richness the lexicon or the evidence documents
but the line or card drops (the root image, a commentator gloss, a better attested
word); a missing fork elsewhere. **S3**: style. Quote exactly: the producer fixes from
your file alone.

## Then, last: the blind secondary check

Only now open the secondaries file. One question per verse: **did a published
translation see a grammatically admissible construal that the shard has not
recorded?** If so, record it in `blind_secondary_check` and add a finding (`check:
"forks"`, S1 at a fairness locus, else S2) whose `should_be` is the fork, decided by
standard §6.5 reasons (grammar, the Gītā's usage, kośa, English). Never "they say X, so
we should". Where a translation shows better English for the same construal, you may
add an S3 finding citing the word's own `define` entry; it is adopted on its dictionary
merits or not at all. `construal_missed: null` for a verse with nothing missed; one
entry per verse.

Second, record the renderings readers will meet elsewhere, for the card's other
readings: `readers_will_meet: [{"locus", "word_i", "renderings": [{"who": "translator",
"word": "at most eight words"}]}]`, only for words where a published rendering differs
from ours in a way a reader would notice. This is the only translation text that
reaches the public card.

## Output and verdict

Write `output` per SCHEMAS (`gita-review-v1`); `findings[].check` is one of `grammar`,
`form`, `meaning`, `readability`, `policy`, `forks`, `public`; `word_i` is `null` for
a whole-line finding; `severity` is 1, 2 or 3; `evidence` holds loci and exact
quotes. `verdict: "accept"` only when no S1 is open, else `"revise"`. Run the job's
`validate` command; fix your file until it passes (at most three runs, then stop and
report); `python3 scripts/gita/queue.py submit <id>`. If the validator rejects something this brief
requires, stop and report its message.

## The fix loop and the diff re-review (job type `rereview`)

A `revise` verdict sends the shard back to its producer (resumed in its own session
when the runtime can), who fixes every S1 and S2 in the shard and nothing else. You
(resumed if the runtime can; otherwise read your review first) receive the shard as
reviewed (`shard_as_reviewed`), the shard as fixed (`verse_output`), your
`previous_review` and the new `expansion_report`. Diff them
(`diff <(python3 -m json.tool A) <(python3 -m json.tool B)`). Check only the changed
fields, each against its finding; flag any change no finding asked for; recompute one
verse in full (checks 1–4). Write a new `gita-review-v1` file: the findings still open,
carried over verbatim, plus any new ones, with the new `shard_sha256`. `accept` only
when no S1 is open.
