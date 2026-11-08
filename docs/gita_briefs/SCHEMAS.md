# Gītā kit: job input/output schemas (lead-owned interface, 2026-11-08)

Governing decision: prakriya `docs/TRANSLATION_PIPELINE_SPEC.md` §0.6. Agents write
only the judgement fields below; code builds everything else.

## Oracles (prakriya `scripts/gita_kit/`, run with `python3 -I`)

```
gita_kit.py grammar analyze FORM_IAST          -> [Analysis]
gita_kit.py grammar derive ANALYSIS_JSON        -> Derivation
gita_kit.py grammar split VERSE_LOCUS           -> [SplitCandidate]
gita_kit.py meaning page LEMMA [--root ROOT]    -> MeaningPage
gita_kit.py verse packet LOCUS                  -> VersePacket (everything above, per pada, + gloss)
```

`Analysis` = `{id, form, kind: tinanta|subanta|krdanta|taddhitanta|avyaya|samasa,
stem, dhatu: {aupadeshika, root, gana, gana_name, pada, artha, upasargas, dp_locus} |
null, lakara, prayoga, purusha, vacana, linga, vibhakti, krt, taddhita, source:
"vidyut-kosha" | "manual"}`. `id` is a stable hash of the normalised analysis.

`Derivation` = `{analysis_id, form_expected, form_derived, matches: bool, steps: [{sutra,
sutra_text, result, ashtadhyayi: "path:line", kashika: "path:a-b"}], engine:
"vidyut-prakriya 0.4.0 (non-authoritative)"}`.

`MeaningPage` = `{lemma, root, kosha: [{work, locus, text}], dhatuvrtti: [{work, locus,
text}], nirukta: [{work, locus, text}], dictionaries: {mw|ap90|skd|vcp|pw: [{locus,
text}]}, concord: [{locus, line}], site_renderings: [{reader, locus, english}]}`.

## Lexicon job (stage B) — agent output, one file per job

```jsonc
{ "schema": "gita-lexicon-v1", "job": "lexicon-0007",
  "entries": [
    { "lemma": "upāsanā", "match": "(^|-)(upās|paryupās)",      // regex for the term checker
      "senses": [
        { "id": "upasana.attend", "gloss": "to sit near in attention and service; the steady turning of thought toward an object",
          "image": "√ās 'sit' + upa 'near'",
          "preserve": false,
          "forms": { "verb": "attend upon", "verb+pari": "attend wholly upon", "noun": "attendance upon" },
          "plain": {"word": "attend upon", "locus": "…"},
          "rich":  {"word": "…", "locus": "…", "tags": ["archaic"]},
          "chosen": "plain", "why": "…",
          "joycean": null,
          "forbidden": ["worship", "meditate"],
          "meaning_lines": [ {"cat": "nirvacana", "text": "…", "who": "Śaṅkara on 12.3", "locus": "…"} ],
          "occurrences": ["12.1", "12.2", "12.3", "12.6", "12.20", "4.25", "9.14"] } ] } ] }
```

## Verse job (stage C) — agent output, one file per shard

```jsonc
{ "schema": "gita-verse-v1", "job": "verse-12-01",
  "verses": [
    { "locus": "12.1",
      "padas": ["evam", "satata-yuktāḥ", "ye", "bhaktāḥ", "tvām", "paryupāsate", "…"],   // must recompose to the saṃhitā
      "words": [
        { "i": 0, "analysis": "<Analysis.id>" | {"manual": Analysis},
          "compound": null | {"type": "…", "vigraha": "…", "members": [{"form": "…", "analysis": "<id>"|{"manual": …}}]},
          "karaka": "…", "sense": "upasana.attend" | null,
          "english": "attend wholly upon", "note": "reader-facing, optional",
          "commentator_lines": [ {"who": "Śaṅkara", "locus": "…", "text": "…"} ] }   // chosen from the packet's gloss hits, 0–3
      ],
      "line": "{0:Thus} {1:ever yoked}, …",
      "sense": "one plain paragraph",
      "forks": [ {"at": "…", "words": [9, 10], "construals": [...], "followed": 0,
                  "reason_class": 1, "reason": "…", "open": false, "display": "…"} ] } ] }
```

The expander turns each word into the public card: `deva`, `iast`, `gloss`, `parts`,
`stem`, `root` (with gaṇa/pada), `rootGloss`, `affix` (Pāṇinian names), `morph`,
`karaka`, `compound`, `sandhi`, `term`, `glossaryKey`, `meaning` (lexicon
meaning_lines + this verse's commentator_lines), `derivation` (steps with loci), and
the apparatus.

## Review job (stage D) — agent output

`{ "schema": "gita-review-v1", "job": "review-12-01", "shard_sha256": "…",
"findings": [{"locus","word_i","severity","check","says","should_be","evidence"}],
"blind_secondary_check": [{"locus","construal_missed": "…" | null}],
"verdict": "accept" | "revise" }`

## Amendments (lead, 2026-11-08, from the brief author's gap list)

- **Lexicon review output** `gita-lexicon-review-v1` as defined in LEXICON_BRIEF Part B
  (`{schema, job, lexicon_job, lexicon_sha256, findings[{lemma, sense, severity, check,
  says, should_be, evidence}], verdict}`).
- **Lexicon sense** `chosen` ∈ `"plain" | "rich" | "joycean" | "preserve"`; for `preserve`,
  `why` states the three tests in reader words and `iast` is required.
- **Verse output** may carry top-level `lexicon_requests: [{lemma, sense|null, locus,
  proposal, why}]`; stage D merges accepted requests and re-checks the other occurrences.
- **commentator_lines** carry every distinct gloss the packet found for the word in this
  verse (standard §6.4); the card shows the first three and the reader's panel shows all.
  The former 0–3 cap is withdrawn.
- **MeaningPage** gains `glosses: [{locus, who, text, line}]` per occurrence, so lexicon
  agents never re-run per-verse packets.
- **Review output** gains `readers_will_meet: [{locus, word_i, renderings: [{who, word}]}]`
  — single words or phrases of at most eight words with the translator's name; the
  expander turns them into `reception` meaning lines and the card's `alternatives`.
- **Private translations file** for review jobs: `internal/gita_pipeline/secondaries/CH.json`
  (git-ignored), built by stage A from the gita/gita index, the Roy and Besant–Das texts
  and CWSA 19; never read by lexicon or verse jobs.
- **Expander output location**: `internal/sanskrit_reviews/gita/chN/producer-AA-BB.json`
  (schema gita-producer-v2), which the builder and deploy script already read.
- **Inline sense fields** (lead decision 2026-11-08, to cut cost). The lexicon covers
  lemmas with ≥ 3 Gītā occurrences, every lemma matching a table row or the standard's
  preserved/system list, and any lemma requested; every other content lemma is decided
  inline in the verse job. Such a word carries `sense: null` and `english`, `why`,
  `meaning_lines` (1–4, categories formation | lexical | nirvacana | usage, each
  `{cat, text, who, locus}` from the meaning page), `image`, `plain` `{word, locus}`,
  `rich` `{word, locus, tags}` | null, `chosen` ∈ plain | rich | joycean, and `joycean`
  (a Joycean record) when chosen. Inline senses are always translated (a lemma needing
  preservation goes through a lexicon request). The verse review checks them as lexicon
  entries; after acceptance they become lexicon entries automatically.

## Amendments from the grammar oracle (2026-11-08)

- `Analysis.source` ∈ `vidyut-kosha | vidyut-prakriya | vidyut-kosha-members | manual`
  (`vidyut-prakriya`: a reading code searched for and verified by derivation, e.g.
  bhakti + matup; `vidyut-kosha-members`: a compound read through its members).
- `Analysis` gains `pausal, variant, pada, ending, avyaya, derivable, engine, members,
  final_member`; `SplitCandidate` is defined in prakriya `scripts/gita_kit/grammar.py`.
- Compounds: Vidyut 0.4.0 exposes no samāsa derivation, so compounding sūtras (2.1–2.2,
  2.4.71) are agent claims on the card, flagged for review; taddhitas that change the
  base's first vowel (aṇ, ḍhak, ṭhañ) likewise.
- Packets present analyses ranked and filtered: readings agreeing with a commentator's
  gloss or the split's stem first; root-noun (kvip/vic) readings of short forms shown
  only when nothing else fits; at most 8 shown per pada with the full list on request.
- `SplitCandidate` (`gita_kit.py grammar split LOCUS` returns a ranked list) =
  `{locus, tokens: [IAST pausal; compound members hyphenated only when a source hyphenates],
  hemistichs: [{half: "a"|"c"|"e", bori: "path:line", text, tokens, recomposes: bool,
  recomposed?: "agreeing prefix‖first departing join", boundaries: [{left, right, surface,
  engine_rule: "first+second→result" | null, sutras: [a.p.s], ashtadhyayi: ["path:line"],
  compound_internal: bool}]}], sources: ["gita-gita word_meanings" | "commentator: NAME" |
  "vidyut sandhi splitter + kosha"], agreement: int (number of sources), recomposes: bool (every
  hemistich re-joins to BORI), unanalysed: [tokens], rank: int}`. Rank = recomposes, then
  agreement, then fewest unanalysed. `sutras` is filled only for unambiguous sandhi classes.
- `Analysis.enclitic` = `{substitute, sutra: "8.1.20"|"8.1.21"|"8.1.22"|"8.1.23", condition}` on
  asmad/yuṣmad readings of me, te, naḥ, vaḥ, vām, nau, tvā, mā (source `vidyut-prakriya` when
  the kosha lacks that case). The Derivation is the engine's full form (mama, tava …) plus one
  step `{sutra, applied_by: "kit", condition}`; `engine` then reads `… + kit step 8.1.2x`. The
  context condition (after a pada, not pāda-initial: 8.1.17–18) is reported, not checked.
- Basic-stem readings: when the kosha gives a prātipadika only as a basic stem, `analyze` adds
  (source `vidyut-prakriya`) the same case reading with a kṛdanta stem the engine derives to
  exactly that prātipadika, and for a-/an- stems a `samasa` reading whose `members` are
  `[{stem: "a"|"an", nan: true, sutras: ["6.3.73"(, "6.3.74")]}, {stem, analyses: [ids],
  stem_analyses: [{stem, kind: "krdanta", dhatu, krt, derivation_matches: true, id}]}]`
  (`final_member: null`). Uṇādi formations outside the engine's kṛt list (karman, manas) stay
  basic and are manual on the card.
