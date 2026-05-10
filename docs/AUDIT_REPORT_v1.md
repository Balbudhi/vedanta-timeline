# Adversarial Factual Audit — `data/thinkers/` JSON corpus

**Auditor:** main agent (Claude Opus 4.7), adversarial register.
**Scope:** all 74 thinker JSON files in `/orcd/home/002/eeshan/philosophy/site/data/thinkers/`.
**Method:** dating cross-check against Hacker / Nakamura / Mesquita / Carman / Sanderson / Slaje / Sharma / Stanford-tier sources; lineage cross-reference programmatic check; doctrinal-prohibition grep; banned-phrase grep; spot-checks of locus citations and Sanskrit fragments.
**Date:** 2026-05-09.
**Constraint:** no files modified. Findings only.

---

## Executive snapshot

The corpus is, on the whole, in unusually good shape. Doctrinal prohibitions are respected (no mithyā=asat collapse, no Madhva-as-Cartesian, no gods-as-symbols, no Advaita-as-world-denial, no banned-phrase hits). The Sanskrit citations sampled are accurate. The dating tiers (`oral-tradition-only`, `consensus-textual`, `confirmed-from-records`, `contested`) are mostly used honestly. The defects fall into three concentrated buckets: (1) **chronological / lineage inconsistencies** arising from the Hacker-late dating of Prakāśātman colliding with school-lineage edges that presuppose his early dating; (2) **`language: "sanskrit"` mis-tagging of all Aurobindo works** (they are in English); (3) **systematic asymmetry of `lineage_in` / `lineage_out` reciprocity** across roughly forty edges, almost all of which are recoverable because one side records the edge.

No fabricated quotations were detected on the spot-check. No mis-attributed canonical works were detected.

---

## Section A — Confirmed defects

Severity tags: `factual-error`, `hallucination`, `mis-citation`, `register-fail`, `inconsistency`.

### A.1 Chronological / lineage inversions

```
[factual-error] anandabodha.json:lineage_in — currently ["prakasatman"] → recommend ["vimuktatman"]; reason: Hindupedia, advaita-vedanta.org, and Surendranath Dasgupta all record Anandabodha as a disciple of Vimuktātman. The corpus's own prakasatman.json places Prakāśātman at 1200–1300 (Hacker/Potter late date) while anandabodha.json places Anandabodha at 1100–1200 — so Prakāśātman cannot be Anandabodha's teacher in either direction.
[factual-error] vimuktatman.json:lineage_in — currently includes "prakasatman" → recommend remove (or replace with the doctrinal predecessor in the Iṣṭa-siddhi tradition); same chronological reason: Vimuktātman 1050–1100 cannot have a 1200–1300 teacher.
[factual-error] yadava-prakasa.json:lineage_out — includes "ramanuja" with Yādava 1050–1100 vs Rāmānuja 1017–1137; the file says Yādava is Rāmānuja's teacher. For the lineage to hold, Yādava's dates_low must be ≤ Rāmānuja's. Recommend re-dating Yādava to c. 990–1070 (the standard Rāmānuja-as-pupil dating) or marking the lineage as doctrinal-only and adjusting dates_tier to "contested".
[factual-error] aksapada.json:lineage_out and vatsyayana.json:lineage_out reference "uddyotakara" but no uddyotakara.json file exists in the corpus.
```

### A.2 Aurobindo-corpus language mistagging

```
[factual-error] aurobindo.json:engaged_works[*].language — every work is tagged language: "sanskrit". All of them (The Life Divine, Essays on the Gita, The Synthesis of Yoga, The Secret of the Veda, Isha Upanishad, Kena Upanishad, Eight Upanishads, Savitri) are composed in English. Recommend: language: "english"; if a "sanskrit" tag is needed because the genre slot expects it, introduce a separate field language_of_composition vs scriptural_language.
```

### A.3 Dating tier honesty

```
[factual-error] anandabodha.json:dates_low/dates_high — currently 1100–1200 [consensus-textual]. Standard placement (Hindupedia, Dasgupta, advaita-vedanta.org, Hiriyanna) is 11th c.: c. 1050–1100, immediately following Vimuktātman. Recommend 1050–1150 with tier "consensus-textual" or 1050–1200 with tier "contested".
[factual-error] sarvajnatman.json:dates_low/dates_high — currently 900–1100 [contested]. The 200-year window is excessive. The standard placement is 10th c. (he salutes his guru Deveśvara, conventionally identified with Sureśvara's lineage). Recommend 900–1000 [consensus-textual] or 950–1050 [contested].
[factual-error] ramanuja.json:dates_tier — currently "consensus-textual" with 1017–1137. The 120-year lifespan is the traditional Sri Vaishnava sectarian dating. Modern academic consensus (Carman 1974; Mesquita 1980; Lester) is c. 1077–1157 (80-year lifespan). Recommend tier "contested" with dates_notes flagging the Carman/Lester alternative.
[factual-error] yamuna.json:dates_low/dates_high — currently 916–1041 [oral-tradition-only]. The 125-year span is the long traditional dating. Mesquita 1973 argued for c. 967–1042. The "oral-tradition-only" tier is honest but the date range itself should be flagged as the long-tradition variant; recommend dates_notes to record the Mesquita alternative.
[factual-error] sankara.json:dates_low/dates_high — currently 700–750 [consensus-textual]. This is the modern (Hacker / Nakamura) consensus shift; the older 788–820 dating is still in many secondary sources. The choice 700–750 is defensible; recommend dates_notes to record the older 788–820 alternative for transparency.
[suspicious] gaudapada.json:dates_low/dates_high — currently 500–600. Modern consensus (Bhattacharya, King) tends late-6th to mid-7th century, since Gauḍapāda is Śaṅkara's parama-guru and Śaṅkara is now placed 700–750. Recommend 600–700 or 575–675 to align with the down-dated Śaṅkara.
[suspicious] bhaskara.json:dates_low/dates_high — currently 750–800 [consensus-textual]. Some scholarship (Nakamura) places him later, c. 800–850, making him post-Śaṅkara as the polemical relation requires. Acceptable as is, but worth widening the upper bound.
```

### A.4 Lineage reciprocity asymmetries (37 edges)

Each of the following edges is recorded on one side but not the other. None is necessarily wrong; the inconsistency itself is the defect. (Listed compactly; each is a one-line fix on the receiving file.)

```
[inconsistency] anandabodha.in=prakasatman ↔ prakasatman.out lacks anandabodha
[inconsistency] anantakrishna-sastri.in=madhusudana ↔ madhusudana.out lacks anantakrishna-sastri
[inconsistency] anantakrishna-sastri.in=brahmananda ↔ brahmananda.out lacks anantakrishna-sastri
[inconsistency] asmarathya.out=badarayana ↔ badarayana.in lacks asmarathya
[inconsistency] audulomi.out=badarayana ↔ badarayana.in lacks audulomi
[inconsistency] kasakrtsna.out=badarayana ↔ badarayana.in lacks kasakrtsna
[inconsistency] badarayana.out=sankara,ramanuja,madhva,bhaskara,nimbarka,vallabha,baladeva ↔ none of those records Bādarāyaṇa as lineage_in (defensible: Bādarāyaṇa is a śāstra-author, not a personal teacher, but the edge should be symmetric on the convention the corpus has chosen)
[inconsistency] baladeva.in=madhva ↔ madhva.out lacks baladeva
[inconsistency] bannanje.in=madhva,raghavendra,jayatirtha ↔ none of those records bannanje
[inconsistency] bhaktisiddhanta.in=bhaktivinoda,jiva-gosvami,baladeva ↔ none records bhaktisiddhanta
[inconsistency] caitanya.out=jiva-gosvami ↔ jiva-gosvami.in lacks caitanya
[inconsistency] caitanya.in=madhva,kesava-kasmiri ↔ neither madhva.out nor kesava-kasmiri.out records caitanya
[inconsistency] citsukha.out=madhusudana ↔ madhusudana.in lacks citsukha
[inconsistency] dharmaraja.in=madhusudana ↔ madhusudana.out lacks dharmaraja
[inconsistency] jiva-gosvami.out=baladeva ↔ baladeva.in lacks jiva-gosvami
[inconsistency] karpatri.in=sankara,vidyaranya,madhusudana ↔ none records karpatri
[inconsistency] nimbarka.out=kesava-kasmiri ↔ kesava-kasmiri.in lacks nimbarka
[inconsistency] ramabhadracarya.in=ramanuja ↔ ramanuja.out lacks ramabhadracarya
[inconsistency] rangaramanuja-muni.out=uttamur-viraraghavacharya ↔ uttamur-viraraghavacharya.in lacks rangaramanuja-muni
[inconsistency] rangaramanuja-muni.in=vedanta-desika,sudarsana,ramanuja ↔ none of those records rangaramanuja-muni
[inconsistency] satchidanandendra.in=sankara ↔ sankara.out lacks satchidanandendra
[inconsistency] sundara-pandya.out=mandana ↔ mandana.in lacks sundara-pandya
[inconsistency] upavarsa.out=ramanuja ↔ ramanuja.in lacks upavarsa
[inconsistency] uttamur-viraraghavacharya.in=vedanta-desika,ramanuja,sudarsana ↔ none records uttamur-viraraghavacharya
[inconsistency] vimuktatman.in=prakasatman ↔ prakasatman.out lacks vimuktatman (also a chronological inversion — see A.1)
[inconsistency] yadava-prakasa.out=ramanuja ↔ ramanuja.in lacks yadava-prakasa
```

### A.5 Polemical asymmetry

```
[inconsistency] satchidanandendra marks anantakrishna-sastri as "mutual" polemic ↔ anantakrishna-sastri.lineage_polemical contains no entry for satchidanandendra. Either both should record the mutual relation, or "mutual" should be downgraded to "refutes" / "is-refuted-by".
```

The other "REFUTES-NO-BACK" cases (Madhva refutes Śaṅkara; Rāmānuja refutes Śaṅkara; Aurobindo refutes Śaṅkara; Madhva refuted by Madhusūdana, etc.) are defensible because the earlier figure cannot polemically reference a later one; recommend, for those cases, retain the asymmetry but document it as the corpus's policy (earlier figures do not back-reference later refuters).

### A.6 Doctrinal-school vs personal-teacher conflation

```
[suspicious] caitanya.json:lineage_in includes ["madhva", "kesava-kasmiri"]. Caitanya's actual personal sannyāsa-guru was Īśvarapurī (a Mādhva sannyāsin), not Madhva himself. Keśava-Kāśmīrī was a Nimbarka-line scholar Caitanya is reported to have defeated in debate (Caitanya-Caritāmṛta), not a teacher. Either:
  (a) the lineage_in convention is doctrinal-school descent, in which case keep madhva and remove kesava-kasmiri (Caitanya does not align doctrinally with Nimbarka), or
  (b) the convention is personal-teacher, in which case both should be removed and "isvara-puri" added.
The Caitanya-as-Madhva-sampradāya identification is itself contested (S. K. De; Wright 1977; Halbfass) and is largely a Baladeva-Vidyābhūṣaṇa 18th-c. construction. Recommend dates_notes to flag this.
[suspicious] vidyaranya.json:lineage_in = ["prakasatman", "vimuktatman"]. These are doctrinal-school sources, not personal teachers (Vidyāraṇya was personally taught by Bhāratī Tīrtha and Vidyātīrtha at Sringeri). The corpus needs to choose one convention.
```

### A.7 Asmarathya / Audulomi / Kāśakṛtsna sūtra-locus check

The Asmarathya entry cites Brahma-Sūtra **1.2.29** and **1.4.20** for Āśmarathya (the formula *abhivyakter ity āśmarathyaḥ*). Both are correct in the standard Śaṅkara-numbering. Auḍulomi is at 1.4.21; Kāśakṛtsna at 1.4.22. These are accurate. **No defect.**

### A.8 Banned-phrase scan

Zero hits across all 74 files for the explicit banned-phrase list (navigates the tension, weaves together, draws on, underscores, sheds light on, rich tapestry, delves into, represents a synthesis, marks a turning point, stands as a testament, intricate interplay, robust framework, nuanced understanding). **No defects in this category.**

The wider AI-tell scan (seamlessly, holistic, pivotal, crucial, paramount, navigate, robust, weaving, harmonize, synergy, paradigm shift) returned a small number of hits, but each is in genuinely substantive context (e.g. "doctrinally pivotal", "the standard reference", "robust *bhedābheda*"). These do not rise to register-fail.

---

## Section B — Suspicious-but-unconfirmed (needs human verification)

```
[suspicious] anandabodha.json:engaged_works does not list Pramāṇamālā's section structure or the relation to Citsukha cited in the corpus's standard secondary literature (Warrier, *The Contribution of Anandabodha to Advaita*); could not confirm without inspecting the file in full.
[suspicious] vacaspati.json:dates_low/dates_high — 900–980. Vāchaspati's *Nyāyasūcīnibandha* gives a date corresponding to either 841 CE (Vikrama era) or 976 CE (Śaka era); the modern consensus (Stcherbatsky, Karl Potter) splits. The 900–980 window is defensible but should record the dual-era ambiguity in dates_notes.
[suspicious] purusottama.json:dates_low/dates_high — 1668–1781 (113-year span tagged "contested"). Standard biographical scholarship on the Puṣṭimārga (Bennett 1990s) gives 1668/9–1781 from the Vārtā literature. Acceptable but the span itself is unusual; verify whether the corpus intends this as a lifespan claim or as a floruit window.
[suspicious] baladeva.json:dates_low/dates_high — 1700–1793 (93-year span). Modern Gauḍīya scholarship (De; Brzezinski) typically gives 1701–1793. Acceptable but check whether dates_high is the precise death year or a window upper bound.
[suspicious] brahmananda-saraswati.json — Śaṅkarācārya of Jyotirmaṭh 1871–1953. The 1953 death is verifiable; the 1871 birth is sometimes given as 1869 in Jyotirmaṭha records. Worth a check.
[suspicious] gaudapada-samkhya.json (Sāṃkhya commentator) and gaudapada.json (Advaita) — must verify the corpus distinguishes these two figures cleanly. The Sāṃkhya Gauḍapāda (the *Bhāṣya* on the *Sāṃkhya-Kārikā*) is a different person from the Advaita Gauḍapāda (the *Māṇḍūkya-Kārikā*); some 19th-c. scholarship conflated them. Did not have time to inspect both files in full.
[suspicious] vimuktatman.json — full date range 1050–1100 against the Hindupedia / advaita-vedanta.org placement of c. 850–1050. The range as given is the late-dating consensus; the very-early dating (~9th c.) is also defended in some secondary literature.
[suspicious] hastamalaka.json:dates_tier "oral-tradition-only" with "lineage_in: sankara". The historicity of Hastāmalaka as a distinct disciple of Śaṅkara (versus a stylised name in the four-disciple śiṣya-mythology) is not settled. Standard dates_tier "legend-only" might be more honest than "oral-tradition-only".
[suspicious] totaka.json:dates_tier "oral-tradition-only" — same caveat as Hastāmalaka. The Toṭakāṣṭaka is widely transmitted but the historical existence of a distinct disciple named Toṭaka is contested in modern scholarship (Bader, Hacker).
```

---

## Section C — Doctrinal-prohibition violations

Grep across all files for the four canonical prohibitions:

1. **mithyā = asat collapse.** Zero violations. Every occurrence of "mithyā" / "asat" co-located is in a context that *explicitly distinguishes* them (sankara.json, madhva.json, madhusudana.json, mandana.json, padmapada.json, prakasatman.json, vimuktatman.json all use sub_axes:`mithya-vs-asat` to mark the distinction). The Madhva file's treatment in *Māyāvāda-Khaṇḍana* is exemplary in this regard ("*Mithyā* is not equivalent to *asat*: he denies the equation").

2. **Madhva as crude Cartesian dualism.** Zero violations. The only occurrences of "crude dualist" are *negations* (madhusudana.json: "Madhusūdana treats Madhva not as a 'crude dualist' but as a serious dialectical opponent"). The madhva.json core_thesis explicitly says "*Svatantra-bhāva* is not a Cartesian-substance claim about non-interaction; it is a claim about ontological asymmetry of dependence". Exemplary handling.

3. **Gods as mere symbols.** Zero violations. No occurrence of "symbol of", "symbolic of", "stand in for", "merely symbolic" in reference to Viṣṇu / Śiva / Devī.

4. **Non-duality as world-denial.** Zero violations. No occurrence of "world-denial", "world-denying", "nihilism", "negate the world" in reference to Advaita.

The aurobindo.json's polemic against Śaṅkara is doctrinally framed ("Aurobindo treats Śaṅkara as articulating a partial truth: the *nirguṇa* pole is real, but the *māyā*-doctrine, read as the unreality of manifestation, is rejected"), not as a generic anti-Advaita slur.

---

## Section D — Pattern findings

1. **Late-dating Prakāśātman cascades.** Adopting Hacker's 13th-c. dating of Prakāśātman creates a chronological knot: Anandabodha (11th c.) and Vimuktātman (10th–11th c.) cannot have him as teacher, yet the lineage edges record this. Either (a) re-date Prakāśātman to 10th c. (the older Vidyasankar / Stanford-tier consensus) and the inversions disappear, or (b) keep the 13th-c. dating and remove the inverted edges. The current state is incoherent.

2. **`lineage_in` / `lineage_out` reciprocity is intermittently maintained.** ~40 edges out of the corpus are recorded on only one side. This is not necessarily wrong substantively (the receiving side may simply not have been updated), but the asymmetry must be resolved if downstream code (graph rendering, lineage queries) relies on either side being canonical. Recommend a one-shot reciprocity-pass that mirrors every edge.

3. **Doctrinal-school vs personal-teacher conflation.** Several `lineage_in` arrays mix the two: Caitanya in=[madhva, kesava-kasmiri] (school + debate-opponent, neither a personal teacher), Vidyāraṇya in=[prakasatman, vimuktatman] (school predecessors, not personal teachers). The corpus needs to commit to one convention; if both are wanted, introduce `lineage_doctrinal` separately from `lineage_personal`.

4. **Aurobindo language tagging.** All eight Aurobindo works carry `language: "sanskrit"`. This is a clear schema mis-population — likely a copy-paste default that was never corrected for the English-composing modern figure. Worth checking whether `bhaktivinoda.json`, `aurobindo.json`'s peers in the modern Bengali / English / Tamil register, and `uttamur-viraraghavacharya.json` (some works in Tamil, some in Sanskrit) have the same problem.

5. **Sectarian-traditional vs modern-academic dating.** The corpus mixes Sri Vaishnava sectarian dates (Rāmānuja 1017–1137, Yamuna 916–1041), Mādhva sectarian-with-inscription dates (Madhva 1238–1317), and modern-academic dates (Śaṅkara 700–750) without flagging the mixture. A `dates_source` field (sectarian / academic / hybrid) would help downstream readers calibrate.

6. **The `dates_tier: "confirmed-from-records"` standard.** Inspection of madhva.json's `dates_evidence` — inscription, sectarian-chronicle, manuscript-colophon — does pass the threshold. Inspection of ramanuja.json's tier — "consensus-textual" with the 120-year traditional span — is misleading; the consensus, if any, is that the dates are sectarian-traditional with modern-academic alternatives. The tier system is honest where applied honestly, but is not consistently applied.

7. **Sanskrit citation accuracy.** Spot-checks of Maṇḍana key passages, Madhva key passages, Asmarathya/Audulomi/Kāśakṛtsna sūtra-loci, all return correct Sanskrit and accurate locus citations. No fabricated quotations detected. Translations on the spot-check are close and accurate.

---

## Final report — top defects (≤400 words)

**Top-10 most severe defects, ranked by how badly they mislead a reader.**

1. **anandabodha.json:lineage_in = ["prakasatman"]** — chronologically impossible under the corpus's own dating (Prakāśātman 1200–1300, Anandabodha 1100–1200) and historically wrong: Anandabodha's teacher was Vimuktātman, not Prakāśātman.
2. **vimuktatman.json:lineage_in includes "prakasatman"** — same chronological inversion.
3. **yadava-prakasa.json:lineage_out = "ramanuja"** with Yādava 1050–1100 vs Rāmānuja 1017–1137 — Yādava cannot be Rāmānuja's teacher unless Yādava's dates_low is brought below 1017; either the dates or the lineage edge is wrong.
4. **All 8 aurobindo.json:engaged_works carry language: "sanskrit"** — they are in English. Schema-data mismatch likely propagated by copy-paste.
5. **anandabodha.json dates 1100–1200** are out of sync with the standard 11th-c. consensus.
6. **sarvajnatman.json dates 900–1100** is a 200-year window that is too wide; standard placement is 10th c.
7. **ramanuja.json:dates_tier = "consensus-textual"** with the 120-year traditional span — the 1017–1137 dates are sectarian-traditional, not academic-consensus; tier should be "contested" with the Carman/Lester c. 1077–1157 alternative noted.
8. **caitanya.json:lineage_in = ["madhva", "kesava-kasmiri"]** — keśava-kāśmīrī was a debate-opponent, not a teacher; Caitanya's actual sannyāsa-guru was Īśvarapurī.
9. **~40 lineage_in / lineage_out reciprocity asymmetries** — none individually grave, collectively a corpus-quality smell.
10. **Polemical "mutual" between satchidanandendra and anantakrishna-sastri** is recorded only on one side.

**Defect density by file:** prakasatman.json (cascade epicentre), anandabodha.json, vimuktatman.json, yadava-prakasa.json, aurobindo.json, sarvajnatman.json, caitanya.json, ramanuja.json. The remaining files are clean to within minor reciprocity asymmetries.

**Estimated total defects:** 4 factual-errors of substance (A.1 inversions + Aurobindo language); 5 dating-tier honesty issues (A.3); ~37 lineage reciprocity asymmetries (A.4, mostly cosmetic); 1 polemical asymmetry (A.5); ~8 suspicious-needs-verification (Section B). Total ≈ 55, of which ~10 are substantive and ~45 are reciprocity / tier-honesty / suspicious-needs-confirmation.

**Recommended dispatch order for fixes (highest-impact first):**

1. Resolve the Prakāśātman dating decision (10th c. vs 13th c.) and adjust anandabodha / vimuktatman / sarvajnatman lineage edges accordingly. *One-pass fix; touches 4 files.*
2. Fix yadava-prakasa.dates_low to predate Rāmānuja, OR mark the lineage as doctrinal-only. *One file.*
3. Fix aurobindo.json:engaged_works[*].language from "sanskrit" to "english". Sweep other modern-figure files for the same schema bug. *One pass over the modern-figures sub-corpus.*
4. Re-tier ramanuja.json:dates_tier to "contested" with Carman/Lester alternative in dates_notes. *One file.*
5. Re-pass caitanya.json:lineage_in to either commit to doctrinal-school convention (drop keśava-kāśmīrī, retain madhva, document the contested Madhva-Gauḍīya identification) or commit to personal-teacher convention (replace both with isvara-puri). *One file.*
6. Sweep all 37 reciprocity asymmetries with a one-shot mirror script that adds the missing back-edge on the receiving file. *One programmatic pass.*
7. Down-tier suspicious entries (sarvajnatman, anandabodha, hastamalaka, totaka) to the appropriate honesty level. *4 files.*
8. Add `dates_source: sectarian | academic | hybrid` field to flag the mixed-source dating. *Schema extension.*

The corpus is high-quality. The defects are concentrated and recoverable.
