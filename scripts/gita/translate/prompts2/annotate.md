You are marking English candidate words for Sanskrit words of the Bhagavad-Gītā. Everything is below;
do not run commands or read files. You do NOT choose the word — code chooses it from your marks by
the owner's rule. Mark honestly; a reviewer checks every mark against the dictionary definitions.

The CARD holds one Sanskrit root family: for each lemma, its senses (the meaning in plain words, the
root's IMAGE, and whether the image is active in the Gītā), and for each sense a TABLE of real English
words found in seven dictionaries, with definitions and the first MODERN sense.

STANDING decisions: some lemmas carry `standing` rows — the owner's earlier, reviewed decisions (an
English rendering with its reasons, or a Sanskrit term kept). For each sense of such a lemma set
"standing_sense" to the id of the standing row that applies to it (the verb vs the noun, the system
term vs the person), or null if none applies. Code then uses the standing decision; still mark the
other candidates, so a better one can be shown to the owner as a challenger. Never propose a word in
its `forbidden` list. When the standing row lists several English words, set "standing_english" to
the one that renders THIS lemma (a row "light, dark" gives "dark" to the negative lemma; a plural form for a plural use).

OPPOSITES: a lemma with `opposite_of` is the negative of another lemma of the family (ajñāna of
jñāna, adharma of dharma). Its English keeps the same English base as that lemma's English where
English has the pair (knowing / unknowing, order / disorder): propose that pair.

WORD CLASS: the English must render the Sanskrit word's class — a noun by a noun, an agent noun by an
agent noun, an adjective by an adjective, a verb by a verb. Mark "pos_fits": false otherwise
("again and again" cannot render the noun abhyāsa).

CANDIDATES. Mark every table word worth considering, AND add your own candidates. The table is found
by code and can miss the obvious word: ALWAYS add the real English words a good translator would
consider (sakhi "friend"; ripu "foe"; mārga "way", "path"), each as "kind": "word" — code
checks it is in the dictionaries. Where no word carries both the sense and the image, also add:
(a) an English construction of up to 3 real words
("attend upon", "sit near", "steady of thought"); (b) a new compound of whole real English words, head
last ("upbearer", "houseless", "everywhere-going"), legible at first hearing, saying one thing. Mark
a construction "kind": "construction" and a compound "kind": "new" with its parts and two attested
English words of the same pattern. Every part must be a real English word; code checks each one.

For every candidate give:
- "sense": 2 if a reader of the line would take the CORE sense from it (the `sense` field; the
  `range` is context, not a requirement), 1 if only part of it, 0 if not;
- "image": 1 if its MODERN meaning itself carries the root's image (not its etymology: "pervade"
  does not mean "go through" in English), else 0;
- "misleads": true if a modern reader would first hear something wrong (a cult for "worship", the
  body for "incontinently", "dear in passing" for "passing dear");
- "register": "ok" for plain, grave English fit for scripture read aloud, or "pedantic" | "slang" |
  "technical" | "comic";
- "idiomatic": false if it is not English a good writer would use — a literal paraphrase of the
  Sanskrit parts ("lifter out", "stretching on unbroken", "disliker of none") is not idiomatic; an
  existing word, a natural construction ("attend upon", "steady of thought") or a well-formed new
  compound ("upbearer", "houseless") is;
- "rank": your order among this sense's candidates by Sri Aurobindo's test — the word that makes the
  reader SEE, exact, with the right sound; 1 is best. Rank only candidates with sense 2.


Across the family, prefer English words that share one English root where the Sanskrit lemmas share
a root (udvij "shrink" / udvega "shrinking"): set "family_root" to the English root you would use.

Return only this JSON:
{"family": "...", "family_root": "..." | null,
 "lemmas": [{"lemma": "...", "senses": [{"sense_id": "...", "standing_sense": "<term id>" | null, "standing_english": "..." | null,
   "marks": [{"word": "...", "kind": "table|word|construction|new", "parts": null | ["...", "..."], "models": null | ["...", "..."],
              "pos_fits": true, "idiomatic": true, "sense": 2, "image": 1, "misleads": false, "register": "ok", "rank": 1}]}]}]}

ROOT WORDS. Some table rows carry `etym` and `link`: English words that share the Sanskrit root through
Proto-Indo-European ("cognate", "pie": √yuj ~ yoke, √sthā ~ stand) or whose Latin/Greek/Old English
source pictures the same image ("etymon-gloss": "sit near" ~ assiduous). Such a word carries the image
only if its MODERN sense still does ("yoke" yes; "zygote" no — Sri Aurobindo: "derivations are
depravations … what matters is what the word means"). `root_search_empty` true means no English word
shares the root or the picture; move on to a construction or a new compound.
