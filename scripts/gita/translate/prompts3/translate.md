You are doing STEPS 3–6 and THE LINE PASS of the owner's English-craft procedure for one sentence of
the Bhagavad-Gītā. Everything is in the CARD below; do not run commands or read files.

The CARD gives each verse and, per word: its grammar and compound structure; its LITERAL meaning
(step 1, from Sanskrit sources only: what the word itself says — render THIS, never what a commentator
says it refers to or implies); its English CANDIDATES (step 2: found in English dictionaries by
the sense and the image, words sharing its root, and words remembered), each with its own entries from
the English dictionaries (Webster 1913, GCIDE, Wiktionary, Open English WordNet …), modern senses
included; the standing decision if one applies (rows of one word are its different senses: use the row whose
sense this is; never a word in its forbidden list). An owner row binds. A row marked "seed" is the
plan's default (not yet owner-reviewed): follow it, or depart from it only with a reason in
"challenge" (it goes to the owner); and, on a rerun, the chapter's
FIXED renderings. Every content word of a rendering must come from that word's candidates, its literal meaning or a
standing decision — code checks this; to use another English word, it must be a real word that
renders the literal meaning (code checks the dictionaries), and you say why in "why".

THE OWNER'S STANDARD: lossless in the line itself — what each word means and signifies is carried by
the English; translate what English can carry, form a new word when needed, keep the Sanskrit only
when nothing in English can carry it; keep the rhythm and the grammar in Sri Aurobindo's sense.
Where the grammar holds two readings (a listed fork) and one line cannot hold both, give a second full
line. Below are the owner's procedure (ENGLISH_CRAFT.md) and the translation standard's rules (§7),
verbatim. Follow them exactly. Where they mention tools or records, the CARD already holds what the
tools found; record your reasons in "why".

==== ENGLISH_CRAFT.md — principles ====
{{CRAFT_PRINCIPLES}}

==== ENGLISH_CRAFT.md §2 — steps 3 to 6 and the line pass ====
{{CRAFT_STEPS}}

==== SANSKRIT_TRANSLATION_STANDARD.md §7.1–§7.16 ====
{{STANDARD_7}}

==== OUTPUT ====
Return only this JSON:
{"lines": {"<locus>": "<line>"},
 "alternative": null | {"fork": "<which fork>", "lines": {"<locus>": "<line>"}},
 "words": [{"locus": "<locus>", "i": <index>, "english": "<the exact text in the line for this word>",
            "parts": null | [{"stem": "<member>", "english": "<its English inside the word's English>"}],
            "kind": "a" | "b" | "c" | "d" | "e",
            "found_by": "retrieved" | "remembered" | "standing" | "grammar",
            "carried": true | false, "lost": null | "<what is not carried>",
            "why": "<one sentence: why this beats the best rejected candidate, naming it>",
            "challenge": null | "<only to depart from a seed row: the reason>"}]}
kind: a exact current word; b uncommon real word; c two words / phrase / English construction;
d formation (also give "models": two attested English words of the same pattern); e Sanskrit kept.
Give "parts" for every compound and for two words joined by sandhi. Give an entry for every word,
particles and pronouns included (found_by "grammar" for function renderings).
