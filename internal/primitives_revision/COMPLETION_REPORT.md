# Completion Report

## What changed

1. Wrote `primitives_revision/audit.md`.
   The audit checks the two old framework files against the on-disk thinker articles and JSON files, with special attention to Śaṅkara, Madhva, the later Advaita sub-schools, and the missing Western coverage.

2. Wrote `primitives_revision/ai_tell_catalog.md`.
   The catalog records exact-string hits for the named stock phrases, gives grouped line lists for the two large heuristic classes, and names the first thirty line edits as a bounded cleanup pass.

3. Wrote `data/articles/source/primitive-graph.md`.
   This is the new framework document.
   It replaces the old split between primitive table and verdict schema with a single graph apparatus built out of:
   - primitive nodes
   - dependency edges
   - thinker commitment edges
   - critique and subsumption edges

4. Updated `data/articles/manifest.json`.
   - added `primitive-graph`
   - marked `primitive-model` as superseded by `primitive-graph`
   - marked `comparative-claims-framework` as superseded by `primitive-graph`

5. Applied the thirty first-pass style rewrites named in the catalog.
   Files edited in that pass:
   - `whitehead.md`
   - `heidegger.md`
   - `leibniz.md`
   - `prigogine.md`
   - `vivekananda-ramakrishna.md`
   - `caitanya.md`
   - `husserl.md`
   - `ramanuja.md`
   - `madhva.md`
   - `aurobindo.md`
   - `deleuze.md`
   - `derrida.md`
   - `bergson.md`
   - `chaudhuri-banerji.md`
   - `gebser.md`
   - `kc-bhattacharyya.md`
   - `kala-cakra-clock-structures.md`

## What the new framework does

1. It stops treating a thinker row as the whole framework.
   The old files mixed three layers:
   - primitive definition
   - thinker assignment
   - pairwise comparative verdict
   The new graph keeps those layers separate.

2. It adds missing primitives.
   The largest additions are:
   - `temporal_mode`
   - `register_of_evolution`
   - `scope_of_grammar`
   - `modal_structure_of_truth`
   - `relation_to_perspectivism`
   - `individuation_status`

3. It rebuilds the Madhva case on stronger footing.
   The new framework does not reduce Madhva to a thin "hierarchical-dependent" label and does not treat his relation to Advaita as a near-identity in different words.

4. It gives the verdict schema a proper place.
   The four verdicts now classify critique and subsumption edges rather than floating as a free method note.

5. It introduces register discipline as a hard rule.
   A claim now has to be tagged by register before it gets a primitive-value.

## What should change on the live site

1. The framework section should now present one core article, not two half-overlapping ones.

2. Readers should see a tighter comparison grammar for:
   - Madhva vs Advaita
   - Deleuze vs Hegel
   - Western process and perspectivism cases that the old files could not even state cleanly

3. The manifest should now surface `primitive-graph` as the live framework entry and show the earlier two documents as superseded.

4. The worst stock phrasing should be less visible in the edited articles, especially the adverb-heavy throat-clearing sentences.

## What was deferred

1. I did not rewrite every thinker article into graph format.
   Section 7 of `primitive-graph.md` gives the format for that rollout.

2. I did not do a full corpus-wide style rewrite.
   The catalog shows that the problem is larger than the first thirty edits.

3. I did not delete `primitive-model.md` or `comparative-claims-framework.md`.
   They remain on disk and in the manifest history, but they are marked as superseded.

4. I did not resolve every old article that still overuses "the user" as a speaking subject.
   The audit records where that remains.
   The new framework itself keeps that to the minimum required by the explicit failure-mode note.

5. I did not add new thinker rows or sub-blocks to every Western article.
   The new framework is ready for that pass, but the pass itself remains to be done.
