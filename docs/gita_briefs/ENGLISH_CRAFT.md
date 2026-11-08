# English craft: exact and beautiful English for the word-by-word Gītā

Status: 2026-11-08. A brief for lexicon, verse and review agents, and a proposal to the
owner. It does not override `docs/SANSKRIT_TRANSLATION_STANDARD.md`; where it asks for a
change, §4 gives the exact amendment, and until the owner adopts it the standard governs.

The owner's complaint: the pipeline under-uses English, which has rare and exact words,
rhythm, compounds and registers to spare. This brief takes the owner's own word-choice
procedure (recovered in `bhakti/.transcription/library-review/engine-rebuild-20261027/history.md`,
dated owner quotations; `bhakti/scripts/bhakti_translation_policy.py` RULES, lines 18–134)
and adds, at each step, the criteria Sri Aurobindo gives in his writings on poetry,
language and translation (§1). §2 is the agents' procedure. §3 applies it to ten
chapter-12 lines. §4 lists what in the current briefs works against good English.

**What was read.** Sri Aurobindo, CWSA (plain text) under
`/Users/eeshan/Dev/deep-research/works/sri_aurobindo_and_the_mother/curated_corpus/docs/en/sri_aurobindo/`:

| Abbr. | File |
|---|---|
| FP | `cwsa26__the-future-poetry.txt` |
| LPA | `cwsa27__letters-on-poetry-and-art.txt` |
| TR | `cwsa05__translations.txt` |
| HMF | `cwsa16__hymns-to-the-mystic-fire.txt` |
| ISHA | `cwsa17__isha-upanishad.txt` |
| KENA | `cwsa18__kena-and-other-upanishads.txt` |
| VPS | `cwsa14__vedic-and-philological-studies.txt` |
| L35 | `cwsa35__cwsa35.txt` |

`cwsa08` mentions a "Joyce" twice (lines 10491, 10509), but that is a Company agent,
not James Joyce. `cwsa19` (*Essays on the Gita*) and the Gītā chapters of TR were read for
this derivation. As the briefs forbid, **none of his Gītā renderings are reproduced here,
and none were used to make the lines in §3.** Those lines come from the Sanskrit, the
commentators, the term table and the English dictionaries. One overlap is disclosed in
§3 (12.7, "sea of death"). Quotations are at most about 25 words, with the ligatures
normalised. Line numbers are the file's own.

Dictionary loci are the tail of what `python3 /Users/eeshan/Dev/prakriya/scripts/lookup/lookup.py define WORD`
prints. `W1913:n` is `sources/raw/upstream_data/english/webster1913_pg29765.txt:n`, and
`KAIKKI:n#sk` is `sources/raw/upstream_data/english/kaikki-english/kaikki.org-dictionary-English.jsonl.gz:n#sk`.
Agents rerun `define` and copy what it prints. They never copy a locus from this page.

---

## 1. What Sri Aurobindo says makes language and translation good

### 1.1 The word's inner sense, not its surface

- In the highest speech, a word carries more than its surface sense. The mantra is "a
  language that conveys infinitely more than the mere surface sense of the words seems
  to indicate" (LPA 786–787). What gives speech its life is "a subtle conscious force
  which informs and is the soul of the body of sound" (FP 10414).
- Old words carry a living image that modern words have lost. "In modern language the
  word is a fixed conventional symbol" (VPS 21002). In the old tongues, by contrast,
  "the Sanscrit word for wolf means radically 'tearing'" (VPS 21011–21012). This is the
  ground of our rule to keep the root's image (standard §7.4).
- The image has to live in the English word as it is used now, not in the English
  word's etymology. When a correspondent defended "loft" by its German source, he
  answered: "Derivations are depravations — even when they are right they are useless, —
  what matters is what the word means" (LPA 23731–23732). So the Sanskrit root image is
  evidence about the Sanskrit. An English word carries that image only if its *current*
  sense carries it ("pervade" means to go through only in Latin).
- A deeper reading of a word must stay inside its grammar. "Abide within its clear
  grammatical connotation as in a hedge of defence against one's own intellectual
  self-will" (ISHA 11405–11407).

### 1.2 The exact word, not the ornamental one; and not the merely plain one

- Words that make us see. "The essential power of the poetic word is to make us see,
  not to make us think or feel" (FP 951–952). The poet "finds the revealing word, not
  merely the adequate and effective, but the illumined and illuminating, the inspired
  and inevitable word" (FP 962–970). He gives the scale explicitly: "its adequate, its
  effective, its illuminative, its inspired or its inevitable utterance" (FP 10399–10400).
- Exactness, not ornament. The austere method is "to use just the necessary words and no
  others … the one expressive or revealing image, the precise colour and nothing more"
  (LPA 6207–6209). Praising a poem, he wrote: "There is no word in excess … every word
  just the right revelatory one — no colour, no ornamentation" (LPA 6961–6967).
- Plainness is not exactness either. "Simplicity is not the test. There can be a supreme
  beauty of simplicity and there can be the opposite" (LPA 5804–5805). An inadequate
  plain line falsifies: Pope's couplet "actually falsifies by its poetical inadequacy
  that great truth of the Gita's teaching, the truth of the divine equality" (FP
  1057–1058).
- Common words lifted by turn and rhythm. Milton's epithets are "the right word in the
  right place, exact in statement, but all lies in the turn … and the rhythm"
  (LPA 12158–12161). Richness is mostly made by placing exact words, not by finding rare
  ones.
- Do not suppress the original's figures. "The figures are there in the original and
  one cannot suppress them in a translation" (LPA 23742–23743). He defended a
  translator's vivid English against a corrector who would have had it "chastened, made
  correct, common and unnoticeable" (LPA 23907, ironic), and who seemed "to damn
  everything vividly descriptive, everything new in turn, phrase or image" (LPA
  23796–23797).

### 1.3 Rhythm and sound

- Rhythm comes first. It is "the premier necessity of poetical expression", "the
  sound-movement which carries on its wave the thought-movement in the word" (FP
  902–905).
- Our medium is cadenced prose. For "a poetic translation of poetry reproductive of the
  exact thought and spiritual intention of the original", cadenced prose is "perhaps the
  only method" (FP 5824–5826). Metre would give the original "almost another soul" (FP
  5828–5829). Prose rhythm "aims characteristically at a general harmony in which the
  parts are subdued to get the tone of a total effect" (FP 850–852).
- The sound of each line is a working concern:
  - Sibilants: "not that one cannot have a sibilant line, but the sounds must be
    otherwise dispersed" (LPA 1984–1985).
  - Colliding consonants: "'Dispersed life-blood' brings three d's so near together that
    they collide a little" (LPA 23689).
  - Function words that bury the key word: "'With' makes the line rather weak; the
    loneliness must be brought out in its full effect" (LPA 1980–1981).
  - Echoes: "Purposeful repetitions … as echoes or key notes in the theme" are a resource
    (LPA 10068–10070).
- Sense rules sound. "Swinburne's defect is his preference of sound to sense" (LPA 3917).

### 1.4 Saxon and Latinate: no rule by stock

He gives no Saxon-first doctrine, and agents must not invent one. He judges each word
by sense and sound:

- He corrected "wideness" back to "vastness": "vastness is the right word and wideness
  is much inferior" (LPA 10365). That is a Latinate word chosen over a Saxon one.
- He rejected "disperse" as an adjective as a "Latin-English neologism" (LPA 23662–23664),
  and Latin participles used as adjectives ("consecrate") because "it sounds to me too
  scholastic" (LPA 23667–23668).
- He calls English, a Teutonic tongue reshaped by French and Latin, "a fine though
  difficult linguistic material" (FP 1914–1916): the double stock is a resource, not a
  hierarchy.

### 1.5 When an uncommon word is right

- **The gloam rule.** A correspondent defended the word "gloam". His answer: "if it is in
  the big dictionary, that is sufficient. Even if it had been an archaism, it would have
  been worth reviving" (LPA 23593–23595). He defended "reboant" as "a recognised (though
  rare and poetic) English word" (LPA 23510–23511). Of a dated form: "I am entitled to
  revive even a past or archaic form if I choose to do so" (LPA 23350–23351).
- **But the dictionary is not a licence.** "The dictionary admits many words which poetry
  refuses to admit" (LPA 23453–23454). "Wherethrough" is "rhetorically pedantic" (LPA
  23451–23452). An archaic connective shoved in to glue clauses is "altogether
  reprehensible" (LPA 23449–23451).
- **Do not fake simplicity.** Copying a plain style yields "ostensible artificial
  artlessness" instead of the original's "bare sincerity" (LPA 6992–6993).
- **The English Bible is the precedent.** "The English Bible is a translation, but it
  ranks among the finest pieces of literature in the world" (LPA 7055–7057). Its stock
  of plain, grave and slightly archaic words ("straightway", "travail") is the register
  nearest to scripture spoken aloud.

### 1.6 Compounds, coined words, and what he says of Joyce

- **Compounds of real words are welcome.** He wished for "a compound adjective like
  'god-holy'" to save a line (LPA 8094–8096). He defended "halo-moon" because it makes
  "moon and halo being one ecstatic splendour" (LPA 8588–8589). That is the test: a
  compound says *one thing* where a phrase would say two. He did not count an
  alliterative compound ("flesh-fret") as Hopkins' mannerism (LPA 17373–17382).
- **He claimed the right to coin.** "I take upon myself the right to coin new words. It
  is not any more fantastic than 'infinitudes' to pair 'infinity'" (LPA 10635–10637).
  That coinage follows an existing English pattern. He refused "eternitudes" for its
  sound: "I would think of the French éternuer and sneeze" (LPA 10640–10641). His rule:
  "If the word is properly formed and not ugly or unintelligible, it seems to me all
  right to venture" (LPA 23944–23945). A word that occurs only once is no blot (the
  hapax legomenon, LPA 23947–23952).
- **But not Joyce's liberty.** Invention is the doubtful case: "one could invent hundreds
  of beautiful words but the liberty to do so would end in a language like Joyce's which
  is not desirable" (LPA 23595–23597). Of a startling phrase he wrote: "the Joyce cut by
  the way of Bedlam does not recommend itself to me" (LPA 23621–23622). And: "If I were
  to use a supramental language like Joyce, you would not even have the illusion of
  understanding it" (L35 7855–7857).
- **Prose is held to a stricter standard than verse.** "Poetry is permitted to be
  insane … though even there there are limits", but "put it in prose and it sounds
  insane" (LPA 23624–23634). The test of a phrase is whether it is English: "I can't
  stomach the two expressions because they are not English" (LPA 23641–23642). Liberty
  belongs to mastery: "before one can take these liberties, one must be a master of the
  language" (LPA 23504–23506).
- **Condensation must earn its place.** Condensations "are justified when they say
  something with more power and depth", but made constant they become "a mannerism or
  artifice" (LPA 5822–5828).

### 1.7 The mantra and "overhead" speech

- The mantra needs "three highest intensities of poetic speech" to "meet and become
  indissolubly one": rhythm, style and the soul's vision of truth (FP 697–700). It is "a
  word of power and light that comes from the Overmind inspiration" (LPA 781–783). Of
  passages from the Upaniṣad and the Gītā he says they "have certainly the Overmind
  accent" (LPA 793–794).
- In this kind of speech, "it must be the right word and no other, in the right place,
  and in no other, the right sounds and no others" (LPA 717–718). Its height is often
  "bare and direct expression where language seems to be used as a scarcely felt
  vaulting-board for a leap into the infinite" (FP 1096–1098).
- What this means for us: a word-by-word translation cannot manufacture the mantra. What
  it can do is not block it, by avoiding padding, flat filler, decoration, pedantry and
  stumbling rhythm, and aim each word at the illumined grade rather than the merely
  adequate. Inevitability is the direction revision moves in. It is not a reviewer's
  pass/fail criterion.

### 1.8 His own practice with Sanskrit scripture

- **First a bare, exact rendering.** In translating the Veda, "the method has been to
  start with a bare and scrupulously exact rendering of the actual language and adhere to
  that as the basis of the interpretation" (HMF 761–763). That is our slot layer.
- **Then literary English, which he admits loosens the text.** "This is a literary and
  not a strictly literal translation" (HMF 759). He had "to turn the concentrated speech
  of the Veda into a looser, more diluted English form" (HMF 772–774).
- **Two words for one, or a phrase.** "I have used two words instead of one or a phrase
  or resorted to some other device to give the exact and complete meaning" (HMF
  795–797).
- **Keep a double sense.** "The Rishis sometimes seem to combine two different meanings
  in the same word; I have occasionally tried to render this double sense" (HMF 806–808).
  For one Vedic symbol he invented phrases: "the 'herds of the light' or 'the shining
  herds'" (HMF 784–785).
- **Give alternatives in notes.** His Kena gives the main construal in the line and the
  other in a note: "Or, 'that which one thinks not with the mind'" (KENA 111). This is
  our fork.
- **Keep terms consistent.** "It is misleading to translate Prâna sometimes by life,
  sometimes by breath, sometimes by life breath or breath of life" (KENA 5744–5745).
  Against that stands his later Veda practice: "I have not always used the same phrase
  though always keeping the same sense" (HMF 790–791).
- **Bold literal English from Upaniṣads.** "One unmoving that is swifter than Mind"
  (ISHA 70); "shrinks not thereafter from aught" (ISHA 119); "the One who becomes
  everywhere … from years sempiternal" (ISHA 132–134); "the eye's seeings" (KENA 85).
  His mature Kena keeps "the Brahman" in Sanskrit (KENA 64).

### 1.9 Where his practice and our product part, and why our rules stand

1. **Literal against literary.** He held that "literal translations more completely
   betray than those that are reasonably free — turning life into death and poetic power
   into poverty and flatness" (LPA 6808–6810). He held that "any attempt at close verbal
   rendering would be disastrous" (TR 11201–11202). His ideal was to "keep as close as
   possible to the original provided … the translation does not read like a translation"
   (LPA 6817–6819), varying "the turn of the language" (LPA 6859) but never saying
   "something quite different in substance" (LPA 6879–6880).

   Our product is the word-by-word layer he himself started from (HMF 762). His freedoms
   of *addition* and *dilution* are closed to us. They go to the card and the sense
   paragraph. His freedoms of *word choice, order, turn and rhythm* are open to us, and
   are the subject of this brief.
2. **Preserved terms.** His early essay calls unfamiliar Sanskrit terms "a high & thick
   hedge of brambles" (KENA 5722–5723), and mocks "This truly is That" as "a juggling
   with demonstrative pronouns" (KENA 5738–5739). His later translations keep "Brahman"
   and "That".

   Our standard (§8) keeps a term only when three tests pass. The owner's procedure
   (§2, step 3e) adds that keeping a term is the last resort. Every kept term is
   therefore a standing question: does an English word now pass?
3. **Consistency.** His own Prāṇa criticism supports our sense-constant table (§7.7). The
   only variation we allow is a register variant of the *same* English word ("does not
   shrink" or "shrinks not"), chosen for cadence (§4, amendment F).
4. **Joyce.** The owner asks for "Joyceian words". Aurobindo opposes free invention. The
   two agree on the line that matters: real words, joined transparently, yes; invented
   words ("made-up words from comic books", the owner; Joyce's "language", Aurobindo),
   no. §2 step 3d makes that line operational.

---

## 2. The procedure: one ordered decision per word, then one pass per line

The six steps are the owner's. The criteria at each step are from §1. Run the steps in
order. A step that fails sends you back to the step named; it never sends you forward
by default.

### Step 1. Establish the Sanskrit meaning from Sanskrit sources

**Do:**
- Read the Dhātupāṭha *artha* of the root and the upasargas, the kośa group, the
  commentators' glosses and anvaya at *this* occurrence, and the Gītā's own usage
  (`KIT meaning page`, `KIT verse packet`, the commentary packet).
- Monier-Williams and Apte may locate a sense. They do not decide it (owner: "the easy
  thing ... use that Sanskrit-English dictionary thing ... I don't think it's the right
  way to do it").
- Write a **sense description** in plain English. It names the operative meaning, the
  root's bodily image if the occurrence activates it, the grammatical form (case, voice,
  agent suffix, negation scope) and the relation inside a compound.
- If the tradition gives more than one admissible meaning, write one description per
  reading and open a fork (owner: "if there are multiple interpretations, then again you
  want multiple translations").
- If you cannot establish the meaning, stop and report it as unresolved. Never hide it
  by keeping the Sanskrit word.

**Aurobindo's criterion:** the inner sense held within the "hedge" of grammar (§1.1).
The root image is evidence about the Sanskrit, not a licence to add images (standard
§7.17: "summit-standing" is rejected).

### Step 2. Find English words by that meaning, then judge them in English dictionaries

**Do:**
- Search with the sense description, not with a word you remember. Run
  `LOOK english "<sense description>" --rich --limit 25`, once with the plain sense and
  once with the root image (owner: "We're literally finding a word.").
- **Tool limitation:** the index matches definitions. Agent nouns, whose definitions
  read "One who …", and many idioms are found poorly. "One who knows" returned only
  interjections. Search the verb's sense, then `define` its agent form (-er) and any
  phrase you need.
- A word you remember may enter the list. Record it as *remembered*, not *retrieved*,
  and judge it by the same `define` test.
- Run `LOOK define` on every candidate. Read the headword's own entries in all seven
  sources, including the modern ones (OEWN, Wiktionary).

**Aurobindo's criterion:** the big dictionary decides whether a word exists. It does not
decide whether the word belongs in the line (§1.5).

### Step 3. Choose the kind of expression, in this order

Take the first kind that carries the whole meaning of the sense description without
adding anything.

**a. An exact current English word.**

**b. An uncommon but real word.** Archaic, rare, literary or dated tags do not
disqualify (owner: "Good words that people don't know are still fair game."). It is
right only if all of these hold:
- (i) it is in the stack *in this sense*, not only as a related form;
- (ii) no current word is equally exact;
- (iii) its current senses do not take it over on first hearing (step 4);
- (iv) it is a content word in the grave, plain register of scripture spoken aloud, not
  a pedantic connective ("wherethrough", "whenas", "whereas", LPA 23436–23452) and not a
  scholastic Latin form (LPA 23668).

It is affectation if any of these hold:
- it was chosen because it is rare;
- the line needs the card to parse;
- a common word is equally exact and sounds as well (LPA 23454).

**c. Two real words, a short phrase, or a hyphenated pair.** This is Aurobindo's "two
words instead of one or a phrase" (HMF 795) and the owner's "putting two real words
together or using a hyphen". English has constructions that hold Sanskrit compounds
without new words, and these come before any formation:
- adjective + "of" + noun for a bahuvrīhi: "steady of thought", "pure of heart";
- the absolute construction: "his trembling gone";
- the Saxon genitive: "action's fruit";
- *-less* or *un-* on an attested base: "houseless".

**d. A formation (the "Joycean" compound).** Use one only when no word or short phrase
holds the two or three concepts at once. It must pass all of the following:
1. **Not already attested.** Search the stack, including Wiktionary, for the compound
   and for the agent noun of the verb. "Upbearer" was called a formation in standard
   §7.17, but it is attested (KAIKKI:756277#s0).
2. **Properly formed** (LPA 23944). It follows a productive English pattern, and two
   attested models of the pattern are named. Examples: X-going like "seagoing";
   agent -er on an attested verb; noun–noun with the head last; *-less* or *un-*. It is
   built of **whole real English words**: no blends of word-fragments, no Sanskrit–English
   hybrids (standard §7.16).
3. **Not ugly** (LPA 10640, "eternitudes" → sneeze). Say it aloud. It must not collide
   with an existing sense: "mineless" already means "Without mines", KAIKKI:698283#s0.
4. **Intelligible on first hearing**, without the card (LPA 23944; owner's
   "intelligibility in the actual sentence").
5. **One thing, not two.** It fuses what the Sanskrit compound fuses ("halo-moon", LPA
   8588). If a phrase says the same, use the phrase.
6. **Adds nothing.** No image, agency or relation the Sanskrit lacks. Attested parts do
   not make the whole attested (bhakti RULES).
7. **Compared in a record.** Record it next to its ordinary English paraphrase and its
   rejected near-alternatives, each with the distortion it causes. This follows the
   bhakti walkthrough format (`joycean-walkthrough-v1/lotus-source-walkthrough.json`:
   `candidate`, `ordinary_paraphrase`, `source_role`, `witnesses`,
   `negative_comparisons`, `limits`).
8. **Budget.** At most one formation per verse line. Condensation made constant becomes
   mannerism (LPA 5827).

**e. Keep the Sanskrit.** Only when no word, phrase or formation carries the sense
without adding, dropping or shading anything (standard §8.1). Give the stated reason,
the best English candidate that was beaten, and what it loses. Keeping a term is never
cover for an unresolved meaning (step 1).

### Step 4. Check meaning and connotation separately

**Meaning.** Does the headword's entry carry the sense description: all of it, and
nothing more? Does the word keep the Sanskrit's form (agent noun, participle, passive,
negation scope)?

**Connotation.** Read the word's modern senses (OEWN and Wiktionary first), then read it
in the actual line. Reject a word whose current associations take over on first hearing,
even when an old sense is exact (owner: "taint" is not forbidden, but the reader's
associations are). Examples:
- "incontinently" means "immediately" (gcide), but readers hear bodily incontinence;
- "passing dear" means "exceedingly" (W1913:608925), but is heard as "dear in passing";
- "hardly won" means "with difficulty" (W1913:386058), but is heard as "barely won";
- "uplifter" carries the modern moral sense of "uplift".

Connotation is contextual, not a fixed list (owner: "earth" against "clay" depends on
the song).

### Step 5. Decide once, keep the plural senses, reuse by context

The decision becomes a (lemma, sense) row in the table (standard §7.7). Separate senses
stay separate rows.

When a lemma has a decided English, reuse it when sense and role match, and make its
other parts of speech from the same English root where English allows. Aurobindo keeps
the double value and the echo (HMF 806–808; LPA 10068). Example: in 12.15 the verb
*udvijate* and the noun *udvega* share a root, so they share "shrink" and "shrinking".

A row's `forms` may list register variants of the same word ("does not shrink",
"shrinks not"). The line chooses among them by cadence (§4, amendment F).

Reuse never proves a sense (history.md §3). Each occurrence is still checked at step 1.

### Step 6. The card gives meaning; it never repeats the headword

A word's primary gloss says what the word means, in English. "Without ahaṃkāra" or "my
bhakta" as the gloss of a kept term only repeats it. The gloss is instead something like
"without ahaṃkāra, the making of 'I'". The etymological `parts` do not replace this (§3
lists the cases found).

### The line pass: after every word is decided

Strip the braces, say the line aloud at speaking pace, and check each of the following.
Each check is derived from §1.3 unless marked otherwise.

- **L1. Parses on first hearing** (standard §7.16). Put the grammatical head where a
  listener needs it. For example, put "Who is my bhakta" before a litany of six
  epithets, not after it.
- **L2. End-weight.** Each clause ends on a stressed content word that carries its news
  ("… with hardship", "… straightway"). It does not end on two stacked prepositional
  phrases or a buried key word (LPA 1980).
- **L3. No "of"-chains.** At most two "of" phrases in sequence. Use the Saxon genitive
  where the relation is possession or source ("action's fruit").
- **L4. Keep the Sanskrit's figures of sound and order where English allows** (LPA
  23743, 10068): anaphora (12.12), chiasmus (12.15), the litany of epithets (12.3), and
  a repeated root (12.15).
- **L5. Disperse sound.** No sibilant clusters and no colliding consonants (LPA 1984,
  23689).
- **L6. Of two exact versions, the shorter**, unless the longer keeps a feature the
  shorter drops. Compactness comes from English constructions (step 3c), never from
  dropping function words English needs.
- **L7. Punctuation serves the ear.** One dash for the main break. No mid-line dash in a
  line that ends with a dash running into the next verse.
- **L8. One register per line** (derived from LPA 6993 and 23454). A biblical archaism
  and a modern idiom do not share a line.
- **L9. Sense rules sound** (LPA 3917). A cadence bought by changing a form, mood or
  word is a §7.2 violation. Rewrite instead.

### Keeping the literal mapping while doing all this

Every craft change has to be one of the following:
- a different word in the same slot that passes steps 1–4;
- a change of English word order;
- a change of supplied function words;
- an English construction that renders the same form (step 3c).

Nothing is added or dropped. Mood, voice and non-finite forms are unchanged (§7.8–§7.9).
Quantifiers surface: under negation, English renders a universal as "any" (12.13,
"toward any being"). A slot may hold a phrase (§7.11). The validator's slot check and
the reviewer's form check (REVIEW_BRIEF checks 2 and 4) apply unchanged.

---

## 3. Calibration: ten chapter-12 lines

"Current" is the published line in `gita/ch12/verses.js`. Its own word count, computed
exactly from the stripped line, is given.

Some changes are not craft but **table conformance**: the published lines predate
current rows of `data/glossary/term_policy.json`. These are marked "table". Changes made
under this brief are marked "craft". Changes that need a decision before they can ship
are marked "**needs**".

A script check confirmed that every revised line covers every word index of its verse.
The ten lines go from **270 words to 253**.

### 12.1

*evaṃ satatayuktā ye bhaktās tvāṃ paryupāsate | ye cāpy akṣaram avyaktaṃ teṣāṃ ke yogavittamāḥ ||*

- **Current (31 words):** Thus ever yoked, those bhaktas who wait upon you on every
  side, and those too who wait upon the imperishable, the unmanifest — of these, which
  are the most knowing in yoga?
- **Revised (29 words):** `{0:Thus} {1:ever yoked}, {2:those} {3:bhaktas} who {5:attend wholly upon} {4:you}, {7:and} {6:those} {8:too} who {5:attend upon} {9:the imperishable}, {10:the unmanifest} — {11:of these}, {12:which} are {13:the best knowers of yoga}?`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| 5 | wait upon … on every side | attend wholly upon | table row `upasana.attend-upon` (pari → "wholly") | table |
| 13 | the most knowing in yoga | the best knowers of yoga | knower: W1913:472952 "One who knows. Shak." | craft. *-vid* is an agent noun (kvip) and *-tama* a superlative. "Knowing in yoga" is not English (LPA 23641). "Knower" keeps the agent noun, where "know best" would change form (§7.2). |

- **Already right:** "ever yoked" (monosyllable, keeps √yuj).
- **Second clause:** its verb is elided in the Sanskrit. The repeated slot 5 is the
  same word, given in its plain form, because *pari* is already printed once.
- **Procedure check:**
  - Step 1: vid + tamap, from the grammar.
  - Step 2: retrieval failed for "one who knows" (tool limit). "Knower" is *remembered*
    and confirmed by `define`.
  - Step 3: kind a.
  - Step 4: no adverse connotation.
  - Step 6: the card gloss already gives the meaning.

### 12.3

*ye tv akṣaram anirdeśyam avyaktaṃ paryupāsate | sarvatragam acintyaṃ ca kūṭastham acalaṃ dhruvam ||*

- **Current (25):** But those who wait upon on every side the imperishable, the
  indefinable, the unmanifest — and the everywhere-going, the unthinkable, the
  unchanging, the unmoving, the steadfast —
- **Revised (23):** `{1:But} {0:those who} {5:attend wholly upon} {2:the imperishable}, {3:the indefinable}, {4:the unmanifest}, {8:and} {6:the everywhere-going}, {7:the unthinkable}, {9:the kūṭastha}, {10:the unmoving}, {11:the steadfast} —`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| 5 | wait upon on every side | attend wholly upon | table | table |
| 9 | the unchanging | the kūṭastha | table row `kutastha.system` (preserve; five readings on the card) | table |
| (punctuation) | mid-line dash | comma | — | craft: L7. The line already ends in a dash that runs into 12.4. |

- **Already right: the litany.** "The imperishable, the indefinable, the unmanifest" is
  three chiming *im-/in-/un-* substantives. That is a purposeful repetition (LPA 10068)
  and the most mantra-like run in the chapter. Leave it.
- **Already right: "steadfast".** W1913:818035 "Firmly fixed or established".
- **Already right: "the everywhere-going".** It passes the formation test:
  - it follows the productive "seagoing" pattern;
  - it keeps *√gam*, which "all-pervading" keeps only in etymology (LPA 23731);
  - it reads on first hearing.

  It stays the owner's choice; Monier-Williams's "all-pervading" goes on the card.

### 12.5

*kleśo 'dhikataras teṣām avyaktāsaktacetasām | avyaktā hi gatir duḥkhaṃ dehavadbhir avāpyate ||*

- **Current (24):** Greater is the travail of those whose awareness is fastened to the
  unmanifest; for the unmanifest way is attained with hardship by the embodied.
- **Revised (24):** `{1:Greater} is {0:the travail} {2:of those} {3:whose awareness is fastened on the unmanifest}; {5:for} {4:the unmanifest} {6:way} {9:is attained} {8:by the embodied} {7:with hardship}.`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| 3 | fastened to | fastened on | fasten: W1913:314399, "to fasten anything in our thoughts … To fasten one's eyes upon" | craft. "Fasten on" is the English idiom for fixing attention. "Fasten to" is the idiom for tying objects. The table word "fastened" is kept. |
| 7/8 | with hardship by the embodied | by the embodied with hardship | — | craft: L2 end-weight. The clause now ends on its news, not on a second prepositional phrase. |

- **Already right: "travail".** W1913:889585, "Labor with pain; severe toil". It is the
  exact old word for *kleśa* (toil that hurts), and the line's best word.
- **Already right: "Greater is …".** The inversion gives end-weight.
- **Already right: the repeated "unmanifest".** It mirrors *avyakta … avyaktā*.
- **Considered and kept: "the embodied".** "The bodied" (W1913:95449) is exact for
  *-vat*, but is used "usually in composition", so "embodied" stays.

### 12.7

*teṣām ahaṃ samuddhartā mṛtyusaṃsārasāgarāt | bhavāmi nacirāt pārtha mayy āveśitacetasām ||*

- **Current (29):** Of these I become, before long, the one who lifts up out of the
  ocean of death-saṃsāra, O son of Pṛthā — of those whose awareness is lodged in me.
- **Revised (28):** `{1:I} {4:become}, {5:before long}, {6:O son of Pṛthā}, {2:the upbearer} {0:of these} {3:out of the sea of death, of saṃsāra} — {8:of those whose awareness is lodged} {7:in me}.`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| 2 | the one who lifts up | the upbearer | upbearer: KAIKKI:756277#s0 "One who upbears or upholds"; upbear: W1913:919846 "To bear up; to raise aloft … A monstrous wave upbore the chief" (Pope) | craft (owner's taste, now attested). The old phrase is an agent-noun calque (§7.16). *Sam-ud-√hṛ* with *√hṛ* "haraṇe", carrying (`dhatupatha.json#1011046`); "up-bear" keeps both "up/out" and "carry". |
| 3 | out of the ocean of death-saṃsāra | out of the sea of death, of saṃsāra | sea: W1913:753591 | craft. "Death-saṃsāra" is a hybrid compound (§7.16). The apposition keeps both nouns in Sanskrit order and leaves their relation to the card. "Sea" is a monosyllable and carries the rhythm. |
| 0 | Of these … (fronted) | the upbearer of these | — | craft: L1. "Of these I become" is first heard as "I become one of these". |

- **Candidates for slot 2:**

  | Candidate | Locus | Kind | Verdict |
  |---|---|---|---|
  | upbearer | KAIKKI:756277#s0 | attested | chosen |
  | uplifter | KAIKKI:445547#s0 | attested | rejected: modern "uplift" carries moral and social improvement (step 4) |
  | upraiser | KAIKKI:713042#s0 | attested | rejected: raising only, no carrying |
  | deliverer | W1913:223610 | attested | rejected: drops the image |

  Retrieval returned the verbs (uplift, upraise). The agent nouns were found by `define`.
- **Sanskrit evidence for slot 3:** Śaṅkara reads *mṛtyu-yuktaḥ saṃsāraḥ*, saṃsāra joined
  with death (`shankara_gita_bhasya.txt:8474`). Rāmānuja reads *mṛtyubhūtāt
  saṃsārākhyāt sāgarāt*, the sea called saṃsāra, which is death
  (`ramanuja_gita_bhasya.txt:2617`). The apposition leans to Rāmānuja. The card must
  carry a fork.
- **Disclosed overlap:** "sea of death" also occurs in Sri Aurobindo's prose on this
  chapter. It was reached here independently, from *sāgara* and *mṛtyu*.
- **Already right:** "before long", and "lodged" for the causative *āveśita*.
- **Card:** the gloss "out of the ocean of death-saṃsāra" repeats the line. It should
  state the two readings (step 6).

### 12.12

*śreyo hi jñānam abhyāsāj jñānād dhyānaṃ viśiṣyate | dhyānāt karmaphalatyāgas tyāgāc chāntir anantaram ||*

- **Current (24):** For knowledge is better than practice; above knowledge meditation is
  distinguished; above meditation, the relinquishment of the fruit of action; from
  relinquishment, peace immediately.
- **Revised (22):** `{1:For} {2:knowledge} is {0:better} {3:than practice}; {4:above knowledge}, {5:meditation} {6:is distinguished}; {7:above meditation}, {8:the relinquishment of action's fruit}; {9:from relinquishment}, {10:peace} {11:straightway}.`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| 8 | the relinquishment of the fruit of action | the relinquishment of action's fruit | — | craft: L3, no "of"-chain. The clause ends on a stressed monosyllable. |
| 11 | immediately | straightway | W1913:825930 "Immediately; without loss of time; without delay … And straightway the damsel arose" (Mark) | craft: sound and register. Retrieved: gcide `CIDE.S#5156560`. |
| (comma) | above knowledge meditation | above knowledge, meditation | — | craft: L7 and L4. The anaphora "above …, above …, from …" now falls the same way three times. |

- **Sanskrit meaning of *anantaram*:** *an-antara*, "with no interval". Śaṅkara has
  *śāntir … anantaram eva syāt* (`shankara_gita_bhasya.txt:8549–8556`); Rāmānuja has
  *karmaṇo 'nantaram eva* (`ramanuja_gita_bhasya.txt:2642`).
- **Candidates for slot 11** (all exact):

  | Candidate | Locus | Verdict |
  |---|---|---|
  | straightway | W1913:825930 | chosen |
  | instantly | gcide `CIDE.I#1688313` "Without the least delay or interval" | equally exact; loses to straightway on sound |
  | forthwith | W1913:339711 | rejected: legal and formal connotation ("Law", Wiktionary "formal") |
  | incontinently | — | rejected: misleads on first hearing (step 4) |
  | presently | — | rejected: misleads on first hearing (step 4) |

  The tie between "straightway" and "instantly" is decided by sound: a Saxon spondee
  ending the verse, against a Latinate dactyl.
- **Already right:** "is distinguished" (the table keeps the passive and *vi-√śiṣ*), and
  "better".

### 12.13

*adveṣṭā sarvabhūtānāṃ maitraḥ karuṇa eva ca | nirmamo nirahaṃkāraḥ samaduḥkhasukhaḥ kṣamī ||*

- **Current (23):** Bearing no dveṣa toward all beings, friendly and compassionate
  indeed, without 'mine', without ahaṃkāra, to whom sorrow and pleasure are the same,
  forbearing —
- **Revised (23):** `{0:Bearing no dveṣa} {1:toward any being}, {2:friendly} {5:and} {3:compassionate} {4:indeed}, {6:without 'mine'}, {7:without ahaṃkāra}, {8:to whom pain and pleasure are the same}, {9:forbearing} —`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| 1 | toward all beings | toward any being | — | craft (**needs** standard §7.1 note, §4 amendment D). Under the negation in *a-dveṣṭṛ*, *sarva* is universal: no being is the object. In English a universal under negation is "any"; "no dveṣa toward all beings" can be heard as "not toward all". |
| 8 | sorrow and pleasure | pain and pleasure | table row `duhkha.pain` (the pair with sukha) | table |

- **Slot 0 (needs owner):** "Bearing no dveṣa" is the device §7.12 names, a Sanskrit noun
  in an English verb frame, and it stays an owner item. Under the owner's step 3e,
  keeping a term is the last resort. Retrieval with "dislike, have aversion to" found
  **mislike**: W1913:537202 (verb) "To dislike; to disapprove of; to have aversion to";
  W1913:537210 (noun) "Dislike; disapprobation; aversion"; Wiktionary noun tagged
  archaic. That is a real word for exactly the sense the row records ("aversion"). If
  the owner finds it exact, *dveṣa* fails §8.1 test 2, and 12.13 could read "{0:No
  misliker} {1:of any being}" (agent noun kept). Not adopted here, because the row
  pairs *rāga–dveṣa* as a system term.
- **Already right:**
  - "friendly", "compassionate", "forbearing";
  - "without 'mine'". The candidate "mineless" collides with "Without mines",
    KAIKKI:698283#s0, the step 3d.3 example.
- **Card (step 6):** the glosses of slot 0 ("bearing no dveṣa") and slot 7 ("without
  ahaṃkāra") only repeat the line. Each needs an English meaning, for example "without
  ahaṃkāra, the making of 'I'".

### 12.15

*yasmān nodvijate loko lokān nodvijate ca yaḥ | harṣāmarṣabhayodvegair mukto yaḥ sa ca me priyaḥ ||*

- **Current (34):** On account of whom the world is not agitated, and who is not
  agitated on account of the world, who is freed from elation, resentment, fear and
  agitation — he too is dear to me.
- **Revised (28):** `{0:From whom} {3:the world} {1,2:shrinks not}, {7:and} {8:who} {5,6:shrinks not} {4:from the world}, {11:who} is {10:loosed} {9:from elation, resentment, fear and shrinking} — {12:he} {13:too} is {15:dear} {14:to me}.`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| 1,2 / 5,6 | is not agitated | shrinks not | table row `udvega.shrink-from` (forms list "shrink", "does not shrink"); shrink: W1913:776082 "To withdraw or retire, as from danger … to recoil, as in fear" | table (verb). The post-verbal negation is craft and **needs** the form "shrinks not" added to the row (§4 amendment F). "From whom the world shrinks not, and who shrinks not from the world" mirrors the Sanskrit chiasmus stress for stress (L4). ISHA 119 uses the same form. |
| 0, 4 | on account of whom / of the world | from whom / from the world | — | follows from the table verb: the ablative of the feared, P. 1.4.25. |
| 10 | freed | loosed | table row `mukta.loosed`; loose (verb): W1913:500851 "To untie or unbind … to set free" | table |
| 9 (last member) | agitation | shrinking | shrinking (noun): KAIKKI:106351#s0 "act of … moving timidly away"; recoil (noun): W1913:697725 "A starting or falling back; a rebound; a shrinking" | craft (**needs** a lexicon request against `udvega.agitation`). See below. |

- **Why "shrinking" for *udvega*:**
  - The root is *ovijī bhaya-calanayoḥ*, to fear and to move or tremble
    (`dhatupatha.json#1060009`).
  - Śaṅkara glosses the verb by the noun (*nodvegaṃ gacchati*) and the noun as
    *udvignatā* (`shankara_gita_bhasya.txt:8604`). So the verse uses one root twice on
    purpose.
  - The same English root keeps that echo (HMF 806–808, LPA 10068; step 5).
- **Risk:** the modern first sense of "shrinking" is "becoming less" (OEWN). In a list of
  emotions it should read as recoil. If the owner judges otherwise, keep "agitation"
  (W1913:18816).
- **Tool note:** `define loosed` falls back to the adjective "loose", because Webster's
  verb entry is mislabelled "v. n." at W1913:500851. Cite the verb by its line.
- **Already right:** "elation", "resentment", "fear", and "he too is dear to me".

### 12.16

*anapekṣaḥ śucir dakṣa udāsīno gatavyathaḥ | sarvārambhaparityāgī yo madbhaktaḥ sa me priyaḥ ||*

- **Current (23):** Who, looking to nothing, pure, able, sitting apart, his anguish gone,
  relinquisher of all undertakings, is my bhakta — he is dear to me.
- **Revised (22):** `{6:Who} is {7:my bhakta}, {0:looking to nothing}, {1:pure}, {2:deft}, {3:sitting apart}, {4:his trembling gone}, {5:relinquishing all undertakings} — {8:he} is {10:dear} {9:to me}.`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| (order) | Who, [six epithets], is my bhakta | Who is my bhakta, [six epithets] | — | craft: L1. The head comes before the litany, so the listener is not kept waiting through six items. |
| 2 | able | deft | table row `daksa.deft`; W1913:221368 [archaic, poetic]; OEWN "skillful … especially of the hands" | table |
| 4 | his anguish gone | his trembling gone | table row `vyatha.trembling` | table |
| 5 | relinquisher of all undertakings | relinquishing all undertakings | relinquish: W1913:706994 | craft (**needs** standard §7.9 amendment E). *-in* (ṇini) is habitual: one in the habit of relinquishing. The English form for a habitual agent in apposition is the present participle. "Relinquisher of …" is the calque §7.16 names. |

- **Already right:**
  - "looking to nothing": keeps *apa-√īkṣ*, is plain, and makes the reader see (FP 951);
  - "sitting apart": keeps the root image of *ud-ā-√ās*;
  - "his trembling gone": an English absolute construction for a bahuvrīhi (step 3c).
- **Card:** the gloss "my bhakta" only repeats the line (step 6).

### 12.19

*tulyanindāstutir maunī saṃtuṣṭo yena kena cit | aniketaḥ sthiramatir bhaktimān me priyo naraḥ ||*

- **Current (26):** to whom blame and praise are alike, silent, content with whatsoever,
  without abode, whose thought is steady, possessed of bhakti — the man is dear to me.
- **Revised (25):** `{0:to whom blame and praise weigh alike}, {1:silent}, {2:content} {3,4,5:with anything whatsoever}, {6:houseless}, {7:steady of thought}, {8:possessed of bhakti} — {11:the man} is {10:dear} {9:to me}.`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| 0 | are alike | weigh alike | table row `tulya` ("weigh alike" for 12.19, keeping *tulā*, the balance); weigh (v.i.): W1913:950722 | table. It is also the "seeing" word: a scale (FP 951). |
| 3,4,5 | with whatsoever | with anything whatsoever | whatsoever: W1913:952968 | craft. A bare "whatsoever" is the §7.16 device. "Anything" renders the indefinite pronouns *yena kena* and is not a content word. |
| 6 | without abode | houseless | table row `aniketa.houseless`; W1913:408273 | table |
| 7 | whose thought is steady | steady of thought | steady: W1913:818083 | craft: step 3c, adjective + "of" + noun for a bahuvrīhi. Shorter, cadenced, with stress on the content words, and it uses the row's word "thought". |

- **Already right:** "silent", "content", and "the man is dear to me".

### 12.20

*ye tu dharmyāmṛtam idaṃ yathoktaṃ paryupāsate | śraddadhānā matparamā bhaktās te 'tīva me priyāḥ ||*

- **Current (31):** But they who wait upon on every side this deathless accordant with
  dharma, as it has been declared, having faith, having me as supreme — those bhaktas
  are exceedingly dear to me.
- **Revised (29):** `{1:But} {0:they who} {5:attend wholly upon} {3:this} {2:nectar true to dharma}, {4:as it has been spoken}, {6:having faith}, {7:having me as supreme} — {9:those} {8:bhaktas} are {10:exceedingly} {12:dear} {11:to me}.`

| Slot | Was | Now | Evidence | Principle |
|---|---|---|---|---|
| 5 | wait upon on every side | attend wholly upon | table | table |
| 2 | deathless accordant with dharma | nectar true to dharma | table rows `amrta.nectar` (cites 12.20) and `dharma` (*dharmya* → "true to dharma"); nectar: W1913:559802 "The drink of the gods" | table. It removes a §7.16 device (an adjective forced to head a noun phrase). The "deathless" reading (Śaṅkara: *amṛtatva-hetutvāt*) stays a fork on the card. |
| 4 | as it has been declared | as it has been spoken | spoken: W1913:808653 "Uttered in speech; delivered by word of mouth"; declare: W1913:217908 | craft. *Ukta* is the kta of *√vac*, "speak". "Declared" shades the word toward proclamation. |

- **Already right: "exceedingly".** W1913:300757 "beyond what is usual; surpassingly"
  carries *ati*.
- **Rejected: "passing dear".** W1913:608925, "passing" = exceedingly, is exact, but is
  the step 4 example of an archaism that misleads on first hearing.
- **Card:** the glosses of slots 2 and 8 should give the meaning, not repeat the line
  (step 6).

---

## 4. What in the current briefs works against good English, with exact amendments

Each item gives the text as it stands now and the text proposed. Nothing here has been
applied; the owner decides.

**A. Plainness is the default.** Standard §7.17 (line 719) and LEXICON_BRIEF step 5
(line 87 ff.) define plain as "the plainest exact English". The choice rule (standard
line 727) then takes rich only when it is more exact, "otherwise the plain one". A tie
therefore always goes to the flatter word, which Aurobindo says can falsify (FP 1057)
and which the owner's complaint names.

Amend standard §7.17, **Choice**, to:

> The line takes the candidate that, in order: carries the sense description whole
> (§7.1–§7.5); reads on first hearing (§7.16); keeps the root's image where the Sanskrit
> carries it (§7.4); sounds best in the line (ENGLISH_CRAFT §2, line pass); fits the
> register of scripture spoken aloud. Neither plain nor rich is the default. Rarity,
> familiarity and brevity are never reasons by themselves. The record states which
> criterion decided.

Make the same change in LEXICON_BRIEF step 5 and VERSE_BRIEF step 5a ("Choose rich when
…").

**B. "Joycean" is undefined, and the worked example is wrong.**
- Standard §7.17 line 724 says "a fused (Joycean) formation". LEXICON_BRIEF step 6 says
  "Joycean formation". Neither says what makes a formation good, beyond "short,
  transparent and read as English".
- Standard line 748 calls "upbearer" a formation, "the agent noun being ours, because no
  attested agent noun carries 'lift up and out'". But "upbearer" (KAIKKI:756277#s0),
  "uplifter" (KAIKKI:445547#s0) and "upraiser" (KAIKKI:713042#s0) are all attested.

Amendments:
- Replace the upbearer example with: "*Good, attested:* 'upbearer' for *samuddhartā*
  (12.7), Wiktionary 'One who upbears or upholds', on the verb 'upbear' (Webster: 'To bear
  up; to raise aloft'). It keeps *ud* 'up, out' and *√hṛ* 'carry'."
- Add after **Formations**: "A formation is built only from whole real English words, by
  a productive English pattern named with two attested models. It passes the eight
  tests of ENGLISH_CRAFT §2 step 3d. It is not a blend of word-fragments, and not a
  Sanskrit–English hybrid. At most one per line."
- Keep the schema value `"joycean"` (SCHEMAS.md lines 87 and 110). Code reads it.

**C. The rule against bad devices has no list of good English resources.** §7.16 lists
only bad devices, so careful agents fall back on relative clauses ("whose thought is
steady"). Add to §7.16:

> *Not devices:* adjective + "of" + noun for a bahuvrīhi ("steady of thought"); the
> absolute construction ("his trembling gone"); the Saxon genitive ("action's fruit");
> *-less* and *un-* on attested bases ("houseless"); inversion for end-weight ("Greater
> is the travail"); post-verbal negation where the row lists it ("shrinks not"); an
> attested agent noun ("upbearer", "knower") is not an agent-noun calque.

**D. Quantifier scope under negation.** §7.1 (line 568) requires quantifiers to surface,
but does not say how English shows a universal under negation. Add:

> Under negation a universal surfaces as English "any" (*adveṣṭā sarvabhūtānām*, "toward
> any being"); "all" there would invert the scope.

**E. The *-in* (ṇini) agent.** §7.9 (line 653) requires that agent forms "(tṛc, ṇvul,
ṇini) take an attested English agent noun". For the habitual *-in* this produced
"relinquisher of all undertakings". Amend:

> ṇini/ini of habit (tācchīlya) in apposition may take the present participle
> ("relinquishing all undertakings"); the card names the suffix.

The `tyaga` row's English list then needs "relinquishing" as the form for 12.16 and
12.17.

**F. One fixed form per category kills cadence.** VERSE_BRIEF step 6 makes `english` "the
lexicon's form for the word's grammatical category". LEXICON_BRIEF step 7 lets `forms`
values be lists, but nothing says how a line chooses among them. Add to LEXICON_BRIEF
step 7:

> A list may hold register variants of the same English word ("does not shrink",
> "shrinks not"); never different words.

Add to VERSE_BRIEF step 7:

> Choose among a row's listed variants by the line pass (ENGLISH_CRAFT §2).

**G. Reading aloud checks only for parsing.** VERSE_BRIEF step 8 (line 121) and standard
§7.16 (line 699) ask only whether the line parses. Add to both:

> … and then the line pass of ENGLISH_CRAFT §2 (end-weight, no "of"-chains, the
> Sanskrit's figures of sound and order kept, sounds dispersed, one dash, one register).

**H. Reviewers can call flatness only "style", which never blocks.**
- REVIEW_BRIEF line 99 and LEXICON_BRIEF line 249 rank style as S3. REVIEW_BRIEF check 4
  (line 81) asks for "better exact English" only when a line is "stiff".
- No severity covers a misleading archaism. And because §7.16 marks devices S1, a
  reviewer can mark any agent noun or formation S1 as a "calque".

Amend REVIEW_BRIEF Severity:
- S1 adds: "a rare or archaic word whose current sense misleads on first hearing (step
  4)".
- S2 adds: "a line that fails the line pass; a flatter word chosen where the evidence
  shows an exact word with the root's image or a better sound".
- Add to check 4: "A formation or rare word is judged only by ENGLISH_CRAFT §2 steps
  3–4; being a formation or rare is never itself a finding."

Make the same S1/S2 change in LEXICON_BRIEF Part B.

**I. The search can be skipped.** Nothing in the briefs requires that an English
candidate came from the sense search rather than from memory. Add to LEXICON_BRIEF
step 5 and VERSE_BRIEF step 5a:

> Each candidate records `found_by`: `retrieved` (the `english` query that found it) or
> `remembered`; every candidate is still `define`d. For agent nouns, search the verb's
> sense and `define` the -er form.

(This can go in `why` until SCHEMAS adds a field.)

**J. The card repeats the headword.** The ch12 cards give kept terms the line text as
their primary gloss: "bearing no dveṣa", "without ahaṃkāra", "my bhakta", "possessed of
bhakti", "bhaktas", "out of the ocean of death-saṃsāra". Add to the standard's card
rules and VERSE_BRIEF step 6:

> A word's gloss states its meaning in English; for a kept term it says what the term
> means ("without ahaṃkāra, the making of 'I'"), never only the term.

**K. Kept terms are not re-examined.** §8.1 test 2 is passed once and not re-asked when
a better English word turns up. Owner item: re-run test 2 for *dveṣa* with "mislike"
(W1913:537202/537210), and record the result either way. The verb frame "bears no
dveṣa" (§7.12, line 676) remains the owner's decision.

**L. Producers do not see these principles.** VERSE_BRIEF, LEXICON_BRIEF and
REVIEW_BRIEF forbid Sri Aurobindo's Gītā renderings, which is right. This brief reproduces
none of them. Add `docs/gita_briefs/ENGLISH_CRAFT.md` to each brief's "Rules:" line as the
English-craft procedure, governed by the standard.

---

## 5. Summary

**The five principles that matter most:**

1. **Meaning first, then a found word.** Establish the Sanskrit sense from Sanskrit
   sources. Search English by that sense. Admit the word the big dictionary has, archaic
   or not (LPA 23593–23595). The dictionary proves the word exists; whether it belongs
   in the line is decided by the line (LPA 23454).
2. **The word that makes the reader see, not the plainest and not the rarest.**
   Adequate is the lowest grade (FP 962–970, 10399–10400). Simplicity is not the test
   (LPA 5804), and inadequacy falsifies (FP 1057). Exact common words become poetry by
   turn and rhythm (LPA 12158–12161).
3. **Rhythm carries the thought.** It is the premier necessity (FP 902–905). Cadenced
   prose is the right medium for exact translation (FP 5824–5826). End-weight, dispersed
   sounds, and the original's figures kept.
4. **Compounds of real words, yes; Joyce's invented language, no.** A formation must be
   properly formed, not ugly, intelligible, and must say one thing a phrase cannot (LPA
   23944, 8588). Prose is held stricter than verse (LPA 23634). Real words joined
   transparently satisfy both the owner and Aurobindo.
5. **A bare exact rendering first, beauty inside it.** Begin from the exact rendering
   (HMF 762). Keep the original's figures and double senses (LPA 23743; HMF 806–808).
   Add nothing; what Aurobindo diluted into the line belongs on our card.

**The ten revised lines** (braces stripped):

- 12.1 Thus ever yoked, those bhaktas who attend wholly upon you, and those too who
  attend upon the imperishable, the unmanifest — of these, which are the best knowers of
  yoga?
- 12.3 But those who attend wholly upon the imperishable, the indefinable, the
  unmanifest, and the everywhere-going, the unthinkable, the kūṭastha, the unmoving, the
  steadfast —
- 12.5 Greater is the travail of those whose awareness is fastened on the unmanifest; for
  the unmanifest way is attained by the embodied with hardship.
- 12.7 I become, before long, O son of Pṛthā, the upbearer of these out of the sea of
  death, of saṃsāra — of those whose awareness is lodged in me.
- 12.12 For knowledge is better than practice; above knowledge, meditation is
  distinguished; above meditation, the relinquishment of action's fruit; from
  relinquishment, peace straightway.
- 12.13 Bearing no dveṣa toward any being, friendly and compassionate indeed, without
  'mine', without ahaṃkāra, to whom pain and pleasure are the same, forbearing —
- 12.15 From whom the world shrinks not, and who shrinks not from the world, who is
  loosed from elation, resentment, fear and shrinking — he too is dear to me.
- 12.16 Who is my bhakta, looking to nothing, pure, deft, sitting apart, his trembling
  gone, relinquishing all undertakings — he is dear to me.
- 12.19 to whom blame and praise weigh alike, silent, content with anything whatsoever,
  houseless, steady of thought, possessed of bhakti — the man is dear to me.
- 12.20 But they who attend wholly upon this nectar true to dharma, as it has been
  spoken, having faith, having me as supreme — those bhaktas are exceedingly dear to me.

**Needing a decision before shipping:**
- 12.13: "any" under negation (D), and *dveṣa* or "mislike" (K).
- 12.15: "shrinks not" as a listed form (F), and "shrinking" for *udvega* (a lexicon
  request).
- 12.16: the ṇini participle (E).
- Everything else either conforms to the current table or is a craft change inside the
  current rules.
