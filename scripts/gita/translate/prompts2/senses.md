You are deciding what one Sanskrit word means in the Bhagavad-Gītā. Everything you need is in the
CARD below; do not run commands or read files.

The CARD gives the word's root and its meaning in the Dhātupāṭha (artha) and the Dhātuvṛtti, its
Amarakośa synonym group, the Sanskrit dictionaries (Śabdakalpadruma, Vācaspatya), Nirukta, every
place it occurs in the passage with each commentator's gloss there, and every other line of the
Gītā where it occurs. Items have ids.

Do this:
1. Decide the word's sense or senses as used in the Gītā. A sense is a meaning the dhātu, the kośas
   or the Gītā's own usage attest. A commentator's interpretation is evidence FOR a sense; it is
   never a sense by itself. Different commentators reading the same word differently is usually one
   sense with a debated application — keep it one sense. Most words have 1 sense here; give 2 only
   if the Gītā really uses the word in two meanings. The root's picture is never a sense by itself
   (a word from √hṛṣ "bristle" that means gladness has the sense "gladness"; the bristling is its image); a sense must be the meaning at some place of the
   Gītā, and every place belongs to exactly one sense.
   A derived word means its base plus its suffix: -vat/-mat/-in "having X" (śarīrin "one having a
   body", not "the transmigrating self"), -tṛ the agent (kartṛ "one who does"), -tva/-tā the state,
   -ya "to be done". What a commentator says the word IMPLIES at a place is application, not the sense.
2. For each sense write its CORE meaning in at most 6 plain English words — one meaning, no "or",
   no list (`sense`) — and, separately, any wider range it has in at most 12 words (`range`). Write
   them as the SANSKRIT sources give it
   (the dhātu's artha, the kośa's synonyms, the commentators' paraphrase), not as translators render
   it: √bhaj सेवायाम् → "one who shares in and serves someone"; not "devotee", "worship", "meditate".
   This text is used to search English dictionaries. In `range`, list the plain English words a
   Sanskrit–English dictionary gives for the word, comma-separated (sakhi: "friend, companion";
   ripu: "foe, enemy"); they are searched too.
3. The image: the concrete picture in the root, in at most 6 words (√bhaj "share out, partake";
   upa-√ās "sit near"; √śuc "burn, glow"; kūṭa "anvil, peak"), or null if the word has none. The
   image must come from the Dhātupāṭha artha or a kośa (cite the item id), never be invented. The
   owner's rule: what a word signifies, including its root's picture, is part of its meaning and
   must be carried. So the image counts as ACTIVE unless the word has wholly lost it in usage; only
   then set `image_dead` to the reason, with the item ids that show it.
4. List the occurrences (loci) that belong to each sense and the item ids that support it.

Return only this JSON:
{"lemma": "...", "senses": [{"sense_id": "<lemma>.<one word>", "sense": "<core, ≤6 words>", "range": "..." | null,
  "image": "..." | null, "image_dead": null | "<reason>", "occurrences": ["12.14"], "evidence": ["D1", "A1", "O2.g1"]}]}
