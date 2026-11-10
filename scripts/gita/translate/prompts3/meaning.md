You are doing STEP 1 of the owner's English-craft procedure for one sentence of the Bhagavad-Gītā:
establish what each word means, from SANSKRIT sources only, in the owner's order. Everything is in the
CARD below; do not run commands or read files.

The CARD gives each verse and, per word, its grammar (case, number, person, voice; what it depends on
and how) and its compound structure, and under "sanskrit" the evidence in the order you must use it:

  M1_decode            the analysis chosen by the parse, its prakṛti and affixes, and the derivation
                       with the sūtras that introduce each affix (prakṛti + pratyaya).
  M2_morphemes         the meaning of each morpheme: the root's Dhātupāṭha entries and the Dhātuvṛttis
                       (Mādhavīya, Kṣīrataraṅgiṇī, Dhātupradīpa, Daiva), and for every affix, lakāra,
                       prayoga and case the sūtras of the Aṣṭādhyāyī that state its meaning.
  M3_lexical_texts     the kośas (Amarakośa, Amaraviveka, Halāyudha, Vaijayantī, Yādavakośa,
                       Ākhyātacandrikā), the Nirukta and Nighaṇṭu, the Śabdakalpadruma and Vācaspatya.
  M4_usage             how many places the Gītā uses the word, and other Gītā lines with it.
  M5_commentaries_last what each commentator says the word means in this verse.
  sources              every source with its status (shown, no entry, partial matches only, not in the
                       library). A source marked "no entry" has nothing to say; do not invent it.

Compound members have their own M2 and M3 under "member_sanskrit".

Work in that order. Build the meaning from M1 and M2 (what the root and each affix mean), find the senses
the word admits in M3, choose the sense used here with M4 and the context of the sentence, and only
then read M5. The commentaries are witnesses: they help choose AMONG the senses M1–M4 allow and may
show a second admissible construal (a fork). A sense that only a commentator gives, and no text
supports, is the commentator's reading: it goes in HERE, never in LITERAL, unless no text has any
entry for the word (then say so in "grounds").

For every word (particles and pronouns included) write, kept apart:
- LITERAL: what the word itself says, in plain English: the meaning of its root and affixes in the
  sense used here, the root's bodily image if this occurrence activates it (√ās sit, √yuj yoke, √viś
  enter, √sthā stand, √dhā place), the grammatical form that must surface (case force, voice, agent
  suffix, participle, mood, negation scope, quantifier), and for a compound the relation of its
  members. Nothing the word does not say: not what it refers to (hṛṣīkeśa is "lord of the senses",
  not "Kṛṣṇa"), not what it implies (sthitaprajña is "one whose wisdom stands firm", not "the
  liberated sage"). The line is made from this.
- GROUNDS: the sources that establish LITERAL, by name and place as the card gives them (e.g.
  "DP 01.1077 gatinivṛttau", "kta 3.2.102", "Amarakośa 1.10.35", "Vācaspatya", "Gītā 2.47"). Name
  a commentator only if no text has an entry.
- HERE: what the commentators say the word refers to or implies at this place, with who says it.
  Evidence for choosing the sense; it never goes into the line.
If the texts and the grammar admit two LITERAL meanings here (a real fork), give one per reading in
"readings", each with who reads it so. If you cannot establish the meaning, say "unresolved".

Also list English words or short English constructions you REMEMBER that might render the word (they
will be checked in English dictionaries; write none rather than guess). Do not write a line.

Return only this JSON:
{"words": [{"locus": "<locus>", "i": <index>,
            "literal": "<what the word itself says, one or two sentences>",
            "grounds": ["<source and place>", ...],
            "here": "<what the commentators say it refers to or implies here, with who>" | null,
            "image": null | "<the root image this occurrence activates, ≤5 words>",
            "search": "<the core meaning in ≤6 plain English words, to search English dictionaries>",
            "readings": null | [{"sense": "...", "who": "<texts or commentators>"}],
            "remembered": ["<English candidate>", ...]}]}
