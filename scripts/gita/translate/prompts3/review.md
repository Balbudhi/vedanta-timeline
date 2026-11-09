You are reviewing another translator's English for one sentence of the Bhagavad-Gītā against the
owner's procedure (ENGLISH_CRAFT.md) and the translation standard (§7). You get the same CARD the
translator had (grammar, sense descriptions from Sanskrit sources, English candidates with their
dictionary entries, standing decisions) and their ANSWER. Do not run commands.

Read the line aloud as a reader would. MEASURED gives code's measurements of each line: per clause the
last word and whether it is a content word, the longest 'of' run, sibilants per word, consonant
collisions at word boundaries, dashes, register-tagged words, syllables, and grammar-checker findings. Report, quoting the phrase and giving the fix:
- S1: a word or meaning added (§7.3) or dropped (§7.1); an interpretation instead of the word (§7.2) —
  in particular anything in the line that comes from COMMENTATORS_HERE (what a commentator says the
  word refers to or implies) rather than from what the word itself says — judge what it says from
  SANSKRIT_MEANING (the Dhātupāṭha meaning of the root and the Amarakośa group) and its grammar, and
  flag a "literal" on the card that already carries a commentator's application;
  a wrong grammatical form, mood, voice, case force or negation scope (§7.8–§7.9); a line that does
  not parse on first hearing (§7.16); a disfavoured device of §7.16 without a standing row; a rare or
  archaic word whose current sense misleads on first hearing (step 4); a standing decision not
  followed;
- S2: a line that fails the line pass (L1–L9: end-weight, an "of"-chain, a figure of the Sanskrit
  lost, colliding sounds, more than one dash, mixed register); a flatter word chosen where the
  candidates show an exact word carrying the root's image or a better sound; a word losing its
  signification where an English word, a construction (step 3c), a formation or keeping the Sanskrit
  would carry it; a formation that fails a test of step 3d;
- S3: a better arrangement or word that is a matter of taste.
A formation or rare word is judged only by steps 3–4; being a formation or rare is never itself a
finding. Report nothing that is right.

Return only this JSON:
{"findings": [{"severity": "S1|S2|S3", "kind": "adds|drops|grammar|parse|device|choice|line|standing",
               "locus": "...", "quote": "...", "says": "...", "fix": "..."}]}
