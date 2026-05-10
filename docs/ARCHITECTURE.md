# ARCHITECTURE

Data schema for the per-thinker JSON entries the Vedānta interactive timeline site loads at runtime. Field-by-field. Authoritative; the dispatched sub-agents must conform exactly.

## File layout

```
/orcd/home/002/eeshan/philosophy/site/data/
  thinkers/
    badarayana.json
    gaudapada.json
    sankara.json
    ...
    (one file per id from CORPUS_PLAN.md, kebab-case id matches filename stem)
  comparative_claims/
    advaita-dvaita__ontology__svatantra-vs-paramarthika.json
    ...
    (one file per claim, see §4)
  registries/
    schools.json          # school_color_token → display config
    sub_schools.json      # sub_school → parent + shade
    works_index.json      # work title → ascription_tier across thinkers
    pramanas.json         # canonical list of pramāṇa-types referenced
  schema/
    thinker.schema.json
    comparative_claim.schema.json
    key_passage.schema.json
```

All schemas are JSON Schema draft 2020-12. The site loads schemas at build time and validates every data file; CI fails on any non-conforming file.

## Conventions

- All ids are kebab-case ASCII, stable, never reused. Once published, an id is immutable.
- All Sanskrit fields use IAST throughout, with Devanāgarī only in dedicated `*_devanagari` siblings. The site's typography handles IAST diacritics first-class.
- All dates are stored as integer years CE (negative for BCE). Date *ranges* use `_low` / `_high` pairs.
- All `_tier` enums use the controlled vocabularies defined in CORPUS_PLAN.md. New values require a schema bump.
- Every `claim_*` and `passage_*` object carries a `last_verified_at` ISO date and a `last_verified_by` agent-id, for provenance audit.

---

## §1 — `thinker.schema.json` (TypeScript-style for readability; canonical schema is JSON Schema)

```typescript
interface Thinker {
  // Identity
  id: string;                         // kebab-case, matches filename stem
  name: string;                       // primary display name (no diacritics ok if ambiguous)
  name_iast: string;                  // IAST (e.g., "Śaṅkara")
  name_devanagari?: string;           // optional; rendered as a sibling
  alternate_names?: string[];         // e.g., ["Ādi Śaṅkara", "Ādi-Śaṅkarācārya", "Bhagavatpāda"]

  // Dating
  dates_low: number;                  // year CE; negative for BCE
  dates_high: number;
  dates_tier:
    | "confirmed-from-records"
    | "consensus-textual"
    | "contested"
    | "oral-tradition-only";
  dates_notes: string;                // 1 sentence: what records exist or why range is wide
  dates_evidence?: Array<{
    kind: "inscription" | "court-record" | "sectarian-chronicle" | "internal-citation"
        | "manuscript-colophon" | "pilgrim-account" | "guru-parampara";
    description: string;
    source_citation?: string;         // bibliographic
  }>;

  // Affiliation
  school:
    | "Advaita"
    | "Viśiṣṭādvaita"
    | "Dvaita"
    | "Bhedābheda"
    | "Acintya-Bhedābheda"
    | "Śuddhādvaita"
    | "Avibhāgādvaita"
    | "proto-Vedānta"
    | "Pratyabhijñā/Trika"
    | "Cross-tradition";
  school_color_token:
    | "advaita"
    | "vishishtadvaita"
    | "dvaita"
    | "bhedabheda"
    | "acintya"
    | "shuddha"
    | "avibhaga"
    | "proto"
    | "trika-comparator"
    | "cross-tradition";
  sub_school?: string;                // e.g., "Vivaraṇa-Advaita", "Bhāmatī-Advaita",
                                      // "Vaḍakalai", "Tenkalai", "Tattvavāda",
                                      // "Svābhāvika-Bhedābheda", "Aupādhika-Bhedābheda"
  sub_school_shade: 1 | 2 | 3 | 4 | 5;  // 1=lightest, 5=darkest within school color;
                                        // used to visually distinguish sub-lineages

  // Lineage (graph edges)
  lineage_in: string[];               // thinker ids: teachers / direct influences
  lineage_out: string[];              // thinker ids: students / direct successors
  lineage_polemical?: Array<{         // polemical interlocutors (not teacher/student)
    thinker_id: string;
    direction: "refutes" | "is-refuted-by" | "mutual";
    note?: string;
  }>;

  // Position (the brief)
  core_thesis: string;                // ~150 words, plain prose, no diacritic-free
                                      // colloquialisms; this is the "what does this
                                      // thinker uniquely commit to" paragraph

  // Engaged works
  engaged_works: Array<EngagedWork>;  // see §2

  // Key passages (selected for the site, with linguistic unpacking)
  key_passages: Array<KeyPassage>;    // see §3

  // Comparative claims this thinker participates in
  // (denormalized pointer; canonical claims live in comparative_claims/)
  comparative_claim_ids: string[];

  // Reception and downstream influence
  reception_notes?: string;           // brief: who read this thinker, where they appear
                                      // in the modern reception of Vedānta

  // Provenance
  entry_status: "draft" | "reviewed" | "audited";
  entry_owner_agent: string;          // which dispatch-wave agent populated this
  last_verified_at: string;           // ISO 8601 date
  last_verified_by: string;
}
```

### Field notes

- **`sub_school_shade`** lets the timeline render Bhāmatī and Vivaraṇa as visually distinct shades of the Advaita color (light vs. mid blue, say). Five tiers gives room for, e.g., distinguishing "Sureśvara-line proto-Vivaraṇa" (shade 2) from "Prakāśātman-line classical Vivaraṇa" (shade 3) from "Madhusūdana-line late Vivaraṇa" (shade 4). The registry in `sub_schools.json` defines the canonical mapping.
- **`lineage_polemical`** captures the Madhva ↔ Madhusūdana, Vyāsatīrtha ↔ Madhusūdana, Vedānta-Deśika ↔ (post-hoc Advaita), Bhāskara ↔ Śaṅkara edges that are NOT teacher-student but ARE structural to understanding the thinker. Renders as a different edge style in the graph.
- **`core_thesis`** is rendered prominently on the thinker's page; it is the one paragraph the user reads first.

---

## §2 — `EngagedWork` sub-schema

```typescript
interface EngagedWork {
  work_id: string;                    // kebab-case; unique within the thinker
                                      // (e.g., "brahma-sutra-bhasya", "advaita-siddhi")
  title: string;                      // primary title
  title_iast: string;                 // IAST form
  title_devanagari?: string;
  alternate_titles?: string[];

  // Dating of the work itself (often distinct from thinker dates)
  composition_dates_low?: number;
  composition_dates_high?: number;
  composition_dates_notes?: string;

  // Ascription
  ascription_tier:
    | "securely-authored"
    | "traditionally-ascribed"
    | "school-ascribed"
    | "disputed";
  ascription_notes: string;           // 1-3 sentences on the state of scholarly opinion
  ascription_evidence?: Array<{
    kind: "manuscript-tradition" | "internal-style" | "internal-references"
        | "school-acceptance" | "scholarly-consensus" | "scholarly-dispute";
    description: string;
    source_citation?: string;
  }>;

  // Content
  genre:
    | "sutra-bhashya"
    | "upanisad-bhashya"
    | "gita-bhashya"
    | "prakarana"        // independent treatise
    | "varttika"         // verse-commentary
    | "tika"             // sub-commentary
    | "stotra"           // hymn
    | "polemical-tract"
    | "rahasya"          // esoteric / sectarian
    | "dialogue"
    | "verse-summary";

  language: "sanskrit" | "tamil" | "tamil-manipravala" | "bengali" | "vrajabhasha"
          | "kannada" | "telugu" | "marathi" | "hindi";

  summary: string;                    // 100-200 words: what this work does, why it matters

  // Pointers into the corpus we have
  primary_corpus_paths?: string[];    // absolute paths under
                                      // /orcd/home/002/eeshan/philosophy/materials/...
  reader_doc_anchor?: string;         // anchor into reader/NN_*.md if relevant

  // Selected passages from this work (subset of thinker.key_passages by work_id)
  key_passage_ids: string[];

  // Provenance
  entry_status: "draft" | "reviewed" | "audited";
}
```

---

## §3 — `KeyPassage` sub-schema

This is the schema that makes the site philosophically serious. Each passage carries linguistic unpacking sufficient for an Indologist-grade reader.

```typescript
interface KeyPassage {
  passage_id: string;                 // kebab-case, unique within the thinker
  work_id: string;                    // pointer to engaged_works[].work_id

  // Locus
  locus_short: string;                // e.g., "BSB 1.1.1", "Advaita-Siddhi pratham-paricheda 1"
  locus_long: string;                 // human-readable full locus
  locus_structured: {
    chapter?: number | string;
    section?: number | string;
    verse?: number | string;
    line?: number | string;
    other?: Record<string, string | number>;
  };

  // Original
  sanskrit_iast: string;              // IAST text of the passage (faithfully transcribed)
  sanskrit_devanagari?: string;
  text_critical_note?: string;        // any variant-readings of philosophical relevance

  // Linguistic unpacking — the rich Pāṇinian breakdown
  panini_breakdown: {
    // Word-by-word morphological / syntactic analysis
    pada_analysis: Array<{
      pada: string;                   // surface form (IAST)
      stem: string;                   // root / nominal stem
      pratyaya?: string;              // suffix(es)
      morphology: string;             // case+number for nouns; tense+person+number+
                                      // pada (P/Ā) for verbs; sandhi-resolution noted
      gloss: string;                  // English gloss of just this word
    }>;
    // Compound resolution (samāsa-vigraha)
    samasa_vigrahas?: Array<{
      compound: string;
      type: "tatpurusha" | "karmadharaya" | "dvandva" | "bahuvrihi"
          | "avyayibhava" | "dvigu" | "upapada" | "luk-tatpurusha"
          | "negative-tatpurusha" | "other";
      resolution: string;             // the vigraha sentence
      note?: string;
    }>;
    // Kāraka relations (the syntactic semantic-roles)
    karaka_structure?: Array<{
      role: "kartṛ" | "karman" | "karaṇa" | "sampradāna" | "apādāna"
          | "adhikaraṇa" | "sambandha" | "sambodhana";
      pada: string;
      note?: string;
    }>;
    // Verbal modality
    verb_modality?: Array<{
      pada: string;
      lakara: "laṭ" | "liṅ" | "liṭ" | "luṅ" | "lṛṅ" | "lṛṭ" | "loṭ"
            | "let" | "lāṅ" | "vidhi-liṅ" | "āśīr-liṅ";
      pada_PA: "parasmaipada" | "atmanepada";
      voice: "active" | "middle" | "passive" | "causative" | "denominative" | "desiderative" | "intensive";
      note?: string;
    }>;
  };

  english_close: string;              // faithful but readable English (NOT a paraphrase)
  english_paraphrase?: string;        // optional: a more accessible second translation

  // Untranslatable terms preserved with first-use gloss
  preserved_terms?: Array<{
    term_iast: string;
    first_use_gloss: string;          // "(roughly: ...)" — the parenthetical the reader sees
  }>;

  // Why we picked this
  why_this_passage: string;           // 1-2 sentences justifying that this passage fairly
                                      // represents the thinker's position on a topic
                                      // (NOT cherry-picking; explicit defense)

  // What topic-tags this passage bears (links to claim categories)
  topic_tags: Array<
    | "ontology" | "causation" | "epistemology" | "soteriology" | "ethics-devotion"
  >;
  sub_axes?: string[];                // e.g., "two-tier-hierarchy", "locus-of-avidya"

  // Cross-references
  cited_in_comparative_claims: string[];   // claim_ids
  parallel_passages?: Array<{               // structurally parallel passages elsewhere
    thinker_id: string;
    passage_id: string;
    note: string;
  }>;

  // Provenance
  source_edition: string;             // bibliographic: which edition we transcribed from
  transcription_verified_by: string;  // agent-id
  entry_status: "draft" | "reviewed" | "audited";
}
```

### Field notes

- **`panini_breakdown`** is the load-bearing field. The user wants the Pāṇinian apparatus visible and usable. The fields decompose as: (1) `pada_analysis` — every word, root/stem, suffix, morphological category, gloss; (2) `samasa_vigrahas` — every compound, classified by type, with vigraha; (3) `karaka_structure` — the syntactic semantic-roles, which are exactly what the rasa-of-the-passage hinges on; (4) `verb_modality` — *lakāra* (tense/mood), pada (P/Ā with its diathetic implications), voice. This is enough for an MIT-level reader to *re-derive* the translation rather than trust it.
- **`why_this_passage`** is not optional. Without it, sub-agents will tend to pick the most-anthologized verse rather than the most-positionally-representative one.
- **`topic_tags`** + **`sub_axes`** drive the comparative-claims engine: when a user is reading Madhva on ontology, the site can surface every Advaita passage tagged ontology+two-tier-hierarchy and offer the comparison.

---

## §4 — `comparative_claim.schema.json`

```typescript
interface ComparativeClaim {
  claim_id: string;                   // schema:
                                      // "<schoolA>-<schoolB>__<category>__<short-axis>"
                                      // or for intra-school:
                                      // "<sub_schoolA>-<sub_schoolB>__<category>__<axis>"
                                      // or for individual-thinker:
                                      // "<thinkerA>-<thinkerB>__<category>__<axis>"

  // The pair (always two thinkers; if comparing schools, pick canonical representatives)
  thinker_a: string;                  // thinker id
  thinker_b: string;
  comparison_grain: "thinker-pair" | "school-pair" | "sub-school-pair" | "stotra-vs-bhashya";

  // Category
  category: "ontology" | "causation" | "epistemology" | "soteriology" | "ethics-devotion";
  sub_axis: string;                   // human-readable axis name; controlled vocab in
                                      // registries/sub_axes.json

  // Surface formulations
  surface_disagreement: string;       // 100-200 words: how the disagreement looks before
                                      // unpacking. Quote both sides in their own idiom.

  // World-model unpacking
  world_model_unpacking: {
    thinker_a_referents: string;      // what does A actually mean by the contested terms?
    thinker_b_referents: string;
    shared_presuppositions: string[]; // background commitments both share
    structural_mapping: string;       // explicit mapping between the two frameworks
  };

  // Verdict
  verdict:
    | "shared-presupposition"         // (a)
    | "parallel-structure"            // (b) — terminologically different, structurally same
    | "terminological-equivalence"    // (b') — same word, different referent
    | "genuine-disagreement"          // (c)
    | "contested";                    // (d)
  verdict_confidence: "low" | "medium" | "high";
  verdict_notes: string;              // why this verdict; what evidence pushed it here

  // Filter axis for stotra-vs-bhashya disambiguation (Śaṅkara case)
  ascription_filter?: {
    thinker_a_ascription_tier: "securely-authored" | "traditionally-ascribed"
                              | "school-ascribed" | "disputed";
    thinker_b_ascription_tier: "securely-authored" | "traditionally-ascribed"
                              | "school-ascribed" | "disputed";
    note: string;                     // e.g., "verdict changes if Śaṅkara's school-
                                      // ascribed stotra corpus is included"
  };

  // Primary sources
  primary_sources: Array<{
    thinker_id: string;
    work_id: string;
    passage_id?: string;              // optional pointer into the thinker's key_passages
    locus: string;                    // human-readable
    quote_iast?: string;              // optional short quote
  }>;

  // Scholarly debate
  scholarly_debate?: {
    summary: string;                  // 50-150 words
    key_scholars?: Array<{
      name: string;
      position: string;
      citation: string;
    }>;
  };

  // Commentary by the site (the "philosophical" voice)
  commentary: string;                 // 200-400 words: the site's own carefully-hedged
                                      // synthesis. Must NOT impose the user's position;
                                      // must NOT collapse genuine disagreement.

  // Anti-pattern flags (explicit guards)
  anti_pattern_flags: {
    avoids_mithya_as_asat_equation: true;       // hard-required
    avoids_dvaita_as_crude_dualism: true;       // hard-required
    avoids_gods_as_mere_symbols: true;          // hard-required
    avoids_non_duality_as_world_denial: true;   // hard-required
    avoids_all_paths_same_sentimentalism: true; // hard-required
  };

  // Provenance
  entry_status: "draft" | "reviewed" | "audited";
  entry_owner_agent: string;
  last_verified_at: string;
  last_verified_by: string;
}
```

### Field notes

- **`anti_pattern_flags`** are required-true booleans that force the populating agent to affirmatively confirm none of the user's prohibited reductions has crept in. CI fails if any is missing or false.
- **`ascription_filter`** is the mechanism that makes the Śaṅkara stotra-vs-*bhāṣya* disambiguation a first-class site control. The same comparative claim can be filtered to either layer of corpus, and the verdict can legitimately differ between layers.
- **`comparison_grain`** keeps three different kinds of comparison cleanly separated: thinker-pair (the highest resolution), school-pair (canonical representatives), sub-school-pair (Bhāmatī vs. Vivaraṇa, Vaḍakalai vs. Tenkalai), and the special **stotra-vs-bhashya** grain (intra-Śaṅkara, intra-Madhva, intra-any-thinker disambiguation across ascription tiers).
- **`commentary`** must be carefully hedged. The user's position must NOT be the site's voice. The site's voice is the disciplined comparative method (per COMPARATIVE_CLAIMS_FRAMEWORK.md). The user's position is one *reader* of the site, not its author.

---

## §5 — Registries

### `schools.json`

```typescript
interface SchoolRegistry {
  [school_color_token: string]: {
    display_name: string;
    color_hex: string;                // base color
    color_palette: [string, string, string, string, string]; // shades 1–5
    short_description: string;
  };
}
```

### `sub_schools.json`

```typescript
interface SubSchoolRegistry {
  [sub_school_id: string]: {
    display_name: string;
    parent_school_color_token: string;
    shade: 1 | 2 | 3 | 4 | 5;
    short_description: string;
    representative_thinker_ids: string[];
  };
}
```

### `works_index.json`

A reverse-index from work title → list of `{thinker_id, ascription_tier, ascription_notes}`. Lets the site detect cases where the same work is ascribed to multiple thinkers (rare but real — e.g., disputed Gauḍapāda *prakaraṇa*-s, contested Maṇḍana = Sureśvara identification).

### `pramanas.json`

Canonical list of *pramāṇa* labels with IAST + English + brief gloss; referenced by `KeyPassage.topic_tags` and by the epistemology-category comparative claims.

### `sub_axes.json`

Controlled vocabulary of `sub_axis` strings used in `ComparativeClaim.sub_axis`. Forces consistency across the corpus. Each sub-axis carries a 1-2 sentence definition.

---

## §6 — Validation rules (CI)

The build fails if any of:

1. A `lineage_in` / `lineage_out` references a non-existent thinker id.
2. A `key_passage.work_id` does not exist in the thinker's `engaged_works`.
3. A `comparative_claim.primary_sources[].passage_id` does not exist in the referenced thinker's `key_passages`.
4. A `comparative_claim` with `comparison_grain == "school-pair"` has thinkers from the same school.
5. Any `anti_pattern_flag` is missing or set to `false`.
6. Any `panini_breakdown.pada_analysis[].morphology` cannot be parsed by the morphological-tag regex.
7. A `dates_tier` is `"confirmed-from-records"` but no `dates_evidence[]` is present.
8. An `ascription_tier` is `"securely-authored"` but no `ascription_evidence[]` is present.
9. The `core_thesis` is over 200 words or under 100 words.
10. A `key_passage.why_this_passage` is missing or under 30 words.

---

## §7 — Recommended dispatch waves

The corpus (58 thinker entries + ~25 high-priority comparative claims at minimum) is too large for one dispatch. Sub-agents must be selected per the project's HARD model-selection rule (Codex 5.4 reasoning=high, OR Claude Opus — never Sonnet/Haiku). Codex is the default for primary-source extraction; Opus is used for synthesis, planning, audit, and comparative-claims composition.

Dependencies are strict: each wave assumes the previous wave's outputs are on disk, audited, and committed.

### Wave 0 — registries and skeletons (Opus, 1 agent)

**Goal.** Populate `registries/schools.json`, `registries/sub_schools.json`, `registries/sub_axes.json`, `registries/pramanas.json`. Generate empty thinker-skeleton JSON files (one per id from CORPUS_PLAN.md), pre-filled with `id`, `name`, `name_iast`, `dates_*`, `school`, `school_color_token`, `sub_school`, `sub_school_shade`, `lineage_in`, `lineage_out`, `engaged_works[].title` and `ascription_tier` from CORPUS_PLAN.md. Set `entry_status: "draft"` everywhere.

**Output.** 58 skeleton JSON files + 4 registry files. Plus a `wave0_audit.md` listing every thinker and confirming the skeleton is consistent with CORPUS_PLAN.md.

**Why Opus.** This is structural / cross-referential work, not primary-source extraction. Opus is correct for the lineage-graph wiring and the cross-ref discipline.

**Dependencies.** None. Reads CORPUS_PLAN.md and ARCHITECTURE.md.

### Wave 1 — per-thinker `core_thesis` and `engaged_works[].summary` (Opus, parallel — 1 agent per ~10 thinkers, 6 agents)

**Goal.** For each thinker, write the `core_thesis` (150 words) and each `engaged_works[].summary` (100-200 words). These are *secondary-source synthesis*, not primary-source extraction — Opus is the right model.

**Output.** All 58 thinker files have `core_thesis` and `engaged_works[].summary` populated. `entry_status: "draft"` becomes `entry_status: "reviewed"` after a second-pass audit.

**Why Opus.** Synthesis of secondary scholarship; each summary requires Opus-tier judgment about what to foreground per thinker.

**Dependencies.** Wave 0 complete (skeletons exist).

### Wave 2 — primary-source `key_passages[]` extraction (Codex 5.4 reasoning=high, parallel — 1 agent per thinker for tier-1 thinkers, batched for minor thinkers; ~25 agents)

**Goal.** For each thinker, extract 3-8 key passages from the engaged works, using the primary corpus at `/orcd/home/002/eeshan/philosophy/materials/primary_texts/sanskrit/vedanta/full_corpus/`. Each passage gets: locus, sanskrit_iast, full `panini_breakdown`, `english_close`, `why_this_passage`, `topic_tags`, `sub_axes`. Reconstruction-only thinkers (Bhartṛprapañca, Auḍulomi, Āśmarathya, Kāśakṛtsna, Brahmadatta, Bodhāyana, Upavarṣa, Sundara-Pāṇḍya) get passages reconstructed from the citation-evidence in later authors, explicitly flagged.

**Output.** All 58 thinker files have `key_passages[]` populated.

**Why Codex.** This is the project's canonical primary-source-extraction pipeline (`handoffs/dispatch_wave*.sh`). Codex 5.4 reasoning=high handles Sanskrit IAST + Pāṇinian morphological analysis at the required depth.

**Dependencies.** Wave 0 (skeletons + work-list) complete. Wave 1 is *helpful but not strictly blocking* — passages can be selected before the summaries are written, but selection is better when the thesis is articulated. Recommend: Wave 1 finishes first.

**Sub-batching.** Tier-1 (one agent per thinker): Bādarāyaṇa, Gauḍapāda, Maṇḍana, Śaṅkara, Sureśvara, Padmapāda, Vāchaspati, Sarvajñātman, Prakāśātman, Vimuktātman, Vidyāraṇya, Madhusūdana, Yāmuna, Rāmānuja, Vedānta-Deśika, Pillai-Lokācārya, Madhva, Jayatīrtha, Vyāsatīrtha, Bhāskara, Nimbārka, Caitanya, Jīva Gosvāmī, Vallabha, Vijñānabhikṣu (25 agents). Tier-2 (batched ~3 per agent): the remaining 33 thinkers across ~11 agents.

### Wave 3 — comparative-claims composition (Opus, parallel — 1 agent per pair-cluster, ~5 agents)

**Goal.** Populate the `comparative_claims/` directory with the high-priority pairwise comparisons from COMPARATIVE_CLAIMS_FRAMEWORK.md §"Pairwise comparison registry". For each pair, generate ~3-5 comparative-claim entries (one per major sub-axis within each category), referencing `primary_sources` from the thinkers' `key_passages` populated in Wave 2.

**Output.** ~50 comparative-claim JSON files, each conforming to `comparative_claim.schema.json`, each with `anti_pattern_flags` all-true, each citing concrete passage_ids from Wave 2.

**Why Opus.** Comparative-claims composition requires multi-source integration across schools. The verdict (parallel-structure / genuine-disagreement / contested) is exactly the synthesis-judgment Opus is correct for.

**Dependencies.** Wave 2 complete (passages exist to cite). Wave 1 complete (theses exist to summarize from).

**Pair-cluster batching.**
- Cluster A: Advaita-Viśiṣṭādvaita (priority 1) + Vaḍakalai-Tenkalai (priority 6) + Bhāmatī-Vivaraṇa (priority 7)
- Cluster B: Advaita-Dvaita (priority 2) + Acintya-Bhedābheda-Dvaita (priority 9)
- Cluster C: Advaita-Bhedābheda (priority 3) + Śuddhādvaita-Advaita (priority 8)
- Cluster D: Advaita-Acintya-Bhedābheda (priority 4) + Viśiṣṭādvaita-Dvaita (priority 5)
- Cluster E: Vijñānabhikṣu vs. all (priority 10) + Trika-Advaita (priority 11)

### Wave 4 — audit and `entry_status` lift to `audited` (Opus, 1 agent per cluster, 4 agents)

**Goal.** For every thinker file and every comparative-claim file, run a checklist audit:
1. Schema validation passes.
2. All `anti_pattern_flags` are true and the commentary text actually conforms (Opus reads the commentary and confirms the prohibitions are honored — not just box-checked).
3. Primary-source citations actually appear in the cited works (spot-check via the corpus paths).
4. `core_thesis` is faithful to the thinker's actual position (not contaminated by the user's own thesis).
5. The internal project codename (see CLAUDE.md) appears nowhere in any data file or any user-facing string.

Lift `entry_status` from `reviewed` to `audited` only when all five pass.

**Output.** A `wave4_audit_report.md` itemizing every file, its audit status, and any defects. Defects round-trip to a Wave 4b cleanup with Codex (for primary-source defects) or Opus (for synthesis defects).

**Why Opus.** Audit is judgment-heavy; Codex is correct for re-extracting passages, but the *audit decision* about whether the populated entry is faithful is Opus's role.

**Dependencies.** Waves 0-3 complete.

### Cross-wave invariants

- After every wave, commit the data files under `/orcd/home/002/eeshan/philosophy/site/data/` to git with a wave-tagged commit message (`data: wave-N <thinker-id-list>`).
- Every dispatched agent must be given the relevant section of COMPARATIVE_CLAIMS_FRAMEWORK.md and the user's prohibitions (CLAUDE.md's "What sub-agents must NOT do" plus POSITION_BRIEF.md's "What the user has forbidden") in its system prompt.
- The internal project codename (see CLAUDE.md) must never appear in any wave's output. CI grep at the end of each wave against the codename string.

