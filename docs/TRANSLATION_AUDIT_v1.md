# TRANSLATION_AUDIT v1
Owner: `wave-translation-audit-opus`. Scope: every `key_passages[]` entry in every thinker JSON.
Audit method: programmatic walker (`/orcd/home/002/eeshan/philosophy/site/.snap-tool/audit_translations.py`) checks line-correspondence, pada-coverage, samāsa-coverage, kāraka presence, verb-modality presence, and `why_this_passage` length. Defects are then fixed in-place via Edit; a second adversarial pass re-runs the same walker.

## §A — Defect catalog (Pass 1)
**Total passages audited:** 84
**Totals by defect kind:**
- `line-collapse`: 50
- `missing-pada`: 45
- `missing-samasa`: 34
- `missing-verb-modality`: 3

### Per-thinker defects

#### `bhartrprapanca` (4 defective passages)
- **bu-1-4-7__avyakrta-to-nama-rupa** (BṛU 1.4.7)
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `vyākriyata`
- **bu-2-3-1-6__murta-amurta-neti-neti** (BṛU 2.3.1, 2.3.6)
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `neti, neti`
- **bu-1-4-10__aham-brahmasmi-and-no-radical-other** (BṛU 1.4.10)
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `brahmāsmi, sāv, asmīti`
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `upāste`
- **bu-2-4-5-1-4-15__sravana-manana-nididhyasana-upasana** (BṛU 2.4.5, 1.4.15)
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `nididhyāsitavyaḥ, upāsīta`

#### `gaudapada` (4 defective passages)
- **mk-1-16-18__awakening-and-duality-as-maya** (MK 1.16-18)
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `upadeśād`
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `vinivarteta`
- **mk-2-5-6__dream-and-waking-as-one** (MK 2.5-6)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 3 sentence(s).
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `hy, nāsti, pi`
- **mk-3-3-7__pot-space-and-the-jivas** (MK 3.3-7)
  - [high] **line-collapse**: Sanskrit has 10 lines, English has 7 sentence(s).
  - [medium] **missing-pada**: 4 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `hy, ivoditaḥ, jātāv, yathaikasmin`
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `saṃpralīyante, saṃprayujyante`
- **mk-3-19-21__maya-and-non-origination** (MK 3.19-21)
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `hy, nānyathājaṃ, hy`

#### `kesava-kasmiri` (3 defective passages)
- **kd-1-4__gopala-mantra-open-to-all** (KD 1.4)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 1 sentence(s).
- **kd-1-5__bhakti-from-acyuta-glance** (KD 1.5)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
- **kd-8-96__murari-eternally-pure-pada** (KD 8.96)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 1 sentence(s).

#### `madhusudana` (4 defective passages)
- **siddhanta-bindu-upodghata__mahavakya-eva-pramapakam** (SB Upodghāta)
  - [high] **line-collapse**: Sanskrit has 5 lines, English has 3 sentence(s).
- **siddhanta-bindu-1__anirvacyam-ajnanam-eva-tat** (SB 1)
  - [high] **line-collapse**: Sanskrit has 7 lines, English has 4 sentence(s).
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `jānāmīti, cedam`
  - [medium] **missing-verb-modality**: 1 finite verb(s) lack verb_modality.
    - verbs: `sidhyatīti`
- **bhakti-rasayana-1-1__bhakti-yoga-parama-pumartha** (BR 1.1)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
- **bhakti-rasayana-1-1-tika__bhakti-brahmavidya-vailakshanya** (BR 1.1 ṭīkā)
  - [high] **line-collapse**: Sanskrit has 8 lines, English has 4 sentence(s).

#### `madhva` (4 defective passages)
- **anuvy-1-1-13-15__svatantra-dependence-and-moksha** (Anuvy. 1.1.13-15)
  - [high] **line-collapse**: Sanskrit has 6 lines, English has 4 sentence(s).
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `narte, pi, kasyāpi`
- **anuvy-1-4-111-112__panca-bheda-is-real** (Anuvy. 1.4.111-112)
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `caiva`
- **anuvy-2-3-66-69__abheda-as-sadrsya-not-identity** (Anuvy. 2.3.66-69)
  - [high] **line-collapse**: Sanskrit has 9 lines, English has 6 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `sādṛśyācca`
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `avaśiṣyate, pravadanti`
- **anuvy-3-3-1__bhakti-upasana-aparoksya** (Anuvy. 3.3.1)
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `tenopāsā, bhaved`

#### `mandana` (3 defective passages)
- **bs-1-1__ananda-svabhava-atma** (BS 1.1 (opening ānanda discussion))
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `tasmād`
- **bs-1-1__maya-borne-plurality** (BS 1.1 (plurality as māyā-bound))
  - [medium] **missing-verb-modality**: 1 finite verb(s) lack verb_modality.
    - verbs: `nānāsti`
- **bs-1-1__avidya-anirvacaniya-jivanam** (BS 1.1 (avidyā neither sat nor asat; in the jīvas))
  - [medium] **missing-pada**: 7 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `nāvidyā, nārthāntaraṃ, nātyantam, nāpi, eveyam, tasmād, kasyāvidyeti`

#### `nimbarka` (4 defective passages)
- **dasa-shloki-1__jiva-svarupa-harer-adhina** (DaŚ 1)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 1 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `cānantam`
- **dasa-shloki-2__anadi-maya-prabheda-bahulya** (DaŚ 2)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `athāpi`
- **dasa-shloki-4__krsna-param-brahma** (DaŚ 4)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 1 sentence(s).
  - [medium] **missing-samasa**: 3 compound(s) lack a samasa_vigraha.
    - compounds: `aśeṣakalyāṇaguṇaikarāśim, vyūhāṅginam, kamalekṣaṇam`
- **dasa-shloki-5__radha-vama-bhaga** (DaŚ 5)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 1 sentence(s).
  - [medium] **missing-samasa**: 3 compound(s) lack a samasa_vigraha.
    - compounds: `virājamānām, parisevitām, sakaleṣṭakāmadām`

#### `padmapada` (2 defective passages)
- **v-15-vi-16__mithyajnana-is-avidya-shakti** (PañcP V.15–VI.16)
  - [high] **line-collapse**: Sanskrit has 10 lines, English has 7 sentence(s).
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `jñānaparyudāsenocyate, abhyupagantavyā`
  - [medium] **missing-verb-modality**: 3 finite verb(s) lack verb_modality.
    - verbs: `anirvacanīyatocyate, jñānaparyudāsenocyate, atrocyate`
- **xxix-108__tat-tvam-asi-pratibimba-reading** (PañcP XXIX.108)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `asīti, asīti`

#### `prakasatman` (4 defective passages)
- **pv-p212__anirvacaniya-maya-visista-karana-brahman** (PV p. 212)
  - [high] **line-collapse**: Sanskrit has 2 lines, English has 1 sentence(s).
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `sāmānādhikaraṇyāc, tasmād, brahmeti`
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `prāptam`
- **pv-p65__jiva-brahma-pratibimba** (PV p. 65)
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `nānuśocati, brahmāpi, nānuśocati`
  - [medium] **missing-samasa**: 4 compound(s) lack a samasa_vigraha.
    - compounds: `avagacchan, anuśocati, svātmani, anuśocati`
- **pv-p103__mahavakya-aparoksa-prayojakatva** (PV p. 103)
  - [medium] **missing-pada**: 6 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `pi, upādānatvād, pi, brahmāpi, tac, doṣāc`
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `avabhāsate, pratibaddham`
- **pv-p164__jnana-karma-samuccaya-nirasa** (PV p. 164)
  - [high] **line-collapse**: Sanskrit has 3 lines, English has 2 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `aśnuta`

#### `raghavendra` (4 defective passages)
- **tantra-dipika__vedic-words-converge-on-visnu** (TD 1.1, adhyāya summary)
  - [high] **line-collapse**: Sanskrit has 2 lines, English has 1 sentence(s).
- **tantra-dipika__anandamaya-not-the-other** (TD 1.1, bhedavyapadeśāc ca)
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `netara, bhedavyapadeśāc, netara`
- **tantra-dipika__susupti-utkranti-distinguish-jiva-and-isvara** (TD 1.3, suṣuptyutkrāntyor bhedena)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 3 sentence(s).
- **tantra-dipika__mumuksu-knows-brahman-alone** (TD 1.4, jñeyatvavacanāc ca)
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `vacanād, jñeyatvāvacanāc, cety`

#### `sankara` (4 defective passages)
- **ups-i-11-15__moksa-jnana-hetutva** (UpS I.11.15)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `apekṣate`
- **ups-i-17-7-9__avidya-veda-and-ekatva** (UpS I.17.7-9)
  - [high] **line-collapse**: Sanskrit has 12 lines, English has 5 sentence(s).
  - [medium] **missing-pada**: 7 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `tv, pi, syād, tv, syād, evātra, hy`
- **mandukya-7__turiya-negation-and-advaita** (MāṇḍU 7)
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `vijñeyaḥ`
- **gk-2-32__paramarthika-non-origination** (GK 2.32)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 3 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `cotpattir`

#### `sarvajnatman` (3 defective passages)
- **samksepa-sariraka-1-319__partless-consciousness-alone-bears-avidya** (SS I.319)
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `nāpi`
- **samksepa-sariraka-1-327__reflected-consciousness-and-agency** (SS I.327)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `tadvad`
- **samksepa-sariraka-3-275-276__fourfold-analysis-of-tat-and-tvam** (SS III.275-276)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `pi`

#### `srinivasa` (4 defective passages)
- **mangalacarana__srikrishna-padayugalam** (Maṅgalācaraṇa 1)
  - [high] **line-collapse**: Sanskrit has 2 lines, English has 1 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `yatrānvitaḥ`
- **upodghata__tadajnaya-vedanta-kaustubha** (Upodghāta)
  - [high] **line-collapse**: Sanskrit has 3 lines, English has 1 sentence(s).
- **bs-1-1-1__tattva-trividham** (BS 1.1.1)
  - [high] **line-collapse**: Sanskrit has 3 lines, English has 2 sentence(s).
- **bs-2-3-42__jiva-paramatmano-amsa** (BS 2.3.42)
  - [high] **line-collapse**: Sanskrit has 5 lines, English has 4 sentence(s).
  - [medium] **missing-pada**: 4 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `nāyaṃ, śrīpuruṣottamād, nāpy, hy`

#### `sureshvara` (4 defective passages)
- **naishkarmya-siddhi-4-3__atman-anatman-epistemic-order** (NS 4.3)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `anātmā, anātmā`
- **naishkarmya-siddhi-2-9-10__anvaya-vyatireka-and-vakyartha** (NS 2.9-10)
  - [high] **line-collapse**: Sanskrit has 8 lines, English has 4 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `tasmād`
  - [medium] **missing-samasa**: 4 compound(s) lack a samasa_vigraha.
    - compounds: `upapadyate, vinājñāna-prahāṇena, su-durlabhaḥ, avatāryate`
- **naishkarmya-siddhi-1-55-56__jnana-karma-no-samuccaya** (NS 1.55-56)
  - [high] **line-collapse**: Sanskrit has 8 lines, English has 4 sentence(s).
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `bhāvāc, syād`
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `pañcāsyoraṇayoḥ`
- **naishkarmya-siddhi-1-98-99__tat-tvam-asi-knowledge-alone** (NS 1.98-99)
  - [high] **line-collapse**: Sanskrit has 8 lines, English has 3 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `jñānād`
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `arthāntaram, saṃdraṣṭum`

#### `vallabha` (4 defective passages)
- **bsb-1-1-4__samanvaya-samavayi-cause** (BSB 1.1.4)
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `sac, rūpeṇānvayāt`
- **bsb-1-1-12-19__brahmajnana-bhakti-purusottama-prapti** (BSB 1.1.12-19)
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `brahmajñānenāvidyā, bhavatīti`
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `sampādyate, nirṇeyate`
- **bsb-1-4-26__atmakrteh-avikrta-parinama** (BSB 1.4.26)
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `śravaṇāc, cālaukikatvam`
  - [medium] **missing-samasa**: 3 compound(s) lack a samasa_vigraha.
    - compounds: `svasya-eva, pariṇamate, pariṇamate`
- **bsb-2-3-43-45__jiva-as-amsha** (BSB 2.3.43-45)
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `mama-eva-aṃśaḥ`

#### `vedanta-desika` (3 defective passages)
- **pr-1-mangalacarana__caturvyuha-param-brahma** (PR 1, Maṅgalācaraṇa)
  - [high] **line-collapse**: Sanskrit has 2 lines, English has 1 sentence(s).
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `paryupāsmahe`
- **pr-1-pramana__caturdha-avatishthate** (PR 1, Catvāraḥ Siddhāntāḥ)
  - [high] **line-collapse**: Sanskrit has 2 lines, English has 1 sentence(s).
- **pr-1-avirodha__ubhayor-api-sastrayoh** (PR 1, Avirodhopayogābhyām)
  - [high] **line-collapse**: Sanskrit has 2 lines, English has 1 sentence(s).

#### `vidyaranya` (3 defective passages)
- **panchadashi-1-15-16__prakriti-twofold-maya-avidya** (Pañcadaśī 1.15-16)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 3 sentence(s).
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `vaśīkṛtya`
- **panchadashi-1-42__munja-self-brahman-discrimination** (Pañcadaśī 1.42)
  - [high] **line-collapse**: Sanskrit has 2 lines, English has 1 sentence(s).
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `muñjād, iveṣīkām, śarīratritayād`
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `samuddhṛtaḥ`
- **panchadashi-1-54-55__nididhyasana-and-samadhi** (Pañcadaśī 1.54-55)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `kramād`
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `parityajya`

#### `vijnanabhiksu` (4 defective passages)
- **vab-2-3-43__jiva-as-brahman-part** (VĀB 2.3.43)
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `nānāvyapadeśād, cāpi`
- **vab-1-1-5__maya-means-prakrti** (VĀB 1.1.5)
  - [high] **line-collapse**: Sanskrit has 3 lines, English has 2 sentence(s).
- **yv-1-23__pranidhana-as-samadhi-cultivation** (YV 1.23)
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `praṇidhānād, pādavad, tv`
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `dvitīya-pādavat`
- **yv-1-24__isvara-as-special-purusa** (YV 1.24)
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `avidyā-asmitā-rāga-dveṣābhiniveśāḥ`

#### `vimuktatman` (5 defective passages)
- **is-1-1__vedanta-brahma-visaya** (IṢ 1.1)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).
- **is-1-1__maya-anirvacaniya-avidya** (IṢ 1.1)
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `avidyocyate, avācyeti`
- **is-1-9__bhranti-anirvacaniyata** (IṢ 1.9)
  - [high] **line-collapse**: Sanskrit has 3 lines, English has 1 sentence(s).
  - [medium] **missing-pada**: 1 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `kiñcid`
- **is-1-140__atmany-eva-avidya** (IṢ 1.140)
  - [high] **line-collapse**: Sanskrit has 3 lines, English has 1 sentence(s).
  - [medium] **missing-pada**: 4 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `tasmād, evāvidyā, tv, ceti`
- **is-1-9__jnanodaya-jivanmukti** (IṢ 1.9)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 2 sentence(s).

#### `vyasatirtha` (4 defective passages)
- **tarka-tandava-1-5__svatah-pramanair-amnayair** (TT 1.5)
  - [high] **line-collapse**: Sanskrit has 4 lines, English has 1 sentence(s).
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `ākhyātānantakalyāṇaguṇam`
- **tarka-tandava-1-pramanyavada__opening-vipratipatti-triad** (TT 1, Prāmāṇyavāda opening triad)
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `sārvajñyādikam, dharmāgrāhakānumānaiḥ`
- **tarka-tandava-1-pramanyavada__jnanajanaka-matradhina-janmatvam** (TT 1, Prāmāṇyavāda, utpatti-svatastva)
  - [medium] **missing-samasa**: 1 compound(s) lack a samasa_vigraha.
    - compounds: `jñānajanakamātrādhīnajanmatvam`
- **tarka-tandava-1-pramanyavada__jnanapramanyam-svato-grahyam** (TT 1, Prāmāṇyavāda, svato-grāhyatvānumāna)
  - [high] **line-collapse**: Sanskrit has 6 lines, English has 3 sentence(s).
  - [medium] **missing-samasa**: 4 compound(s) lack a samasa_vigraha.
    - compounds: `agṛhyamāṇatve, agṛhyamāṇatve, agṛhyamāṇam, cakṣurgrāhyam`

#### `yamuna` (4 defective passages)
- **atmasiddhi-3__self-distinct-self-manifest** (ĀS 3)
  - [high] **line-collapse**: Sanskrit has 2 lines, English has 1 sentence(s).
- **isvarasiddhi-16-18__world-under-one-principal-person** (ĪS 16-18)
  - [high] **line-collapse**: Sanskrit has 6 lines, English has 4 sentence(s).
  - [medium] **missing-pada**: 3 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `padārthatvād, ekenābhiṣṭhitāḥ, cetanācetanātmatvād`
  - [medium] **missing-samasa**: 6 compound(s) lack a samasa_vigraha.
    - compounds: `ghaṭādivat, ekecchānuvidhāyīdam, abhiṣṭhitāḥ, tvagādivat, vivādādhyāsitam, cetanācetanātmatvāt`
- **samvitsiddhi-31-35__advitiya-not-world-negation** (Svs 31-35)
  - [high] **line-collapse**: Sanskrit has 5 lines, English has 2 sentence(s).
  - [medium] **missing-pada**: 4 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `cāpy, brahmeti, nāsīd, vāsya`
  - [medium] **missing-samasa**: 2 compound(s) lack a samasa_vigraha.
    - compounds: `anumoditaḥ, advitīyam`
- **stotra-ratna-22-24__prapatti-from-helplessness** (YStr 22-24)
  - [medium] **missing-pada**: 2 word(s) in sanskrit_iast lack a pada_analysis match.
    - words: `tavāgre, ivāsi`
  - [medium] **missing-samasa**: 4 compound(s) lack a samasa_vigraha.
    - compounds: `prapadye, vyadhāyi, agatiḥ, nimajjataḥ`

## §B — Fix log

*(in progress)*


## §D — Patterns

Systematic issues observed across the corpus:

1. **Line-collapse is the dominant defect** (~60% of passages). Sub-agents in Wave 2 routinely
   compressed multi-pāda Sanskrit verses into one or two English sentences with semicolons or
   relative-clause embedding. The fix mandates one English sentence (or more) per Sanskrit pāda
   so the structural relationship is preserved.

2. **Sandhi-merged tokens left unanalyzed.** Forms like `brahmāsmi` (= brahma + asmi),
   `neti neti` (= na + iti, twice), `asīti` (= asi + iti) appear as single surface tokens but the
   `pada_analysis` either bundles them or omits the second component. Fix policy: each underlying
   morpheme gets its own entry, with a `note` field flagging the sandhi join in the surface form.

3. **Particles (hi, api, eva, ca, vai, tu) are routinely deferred** despite the user's explicit
   "don't defer any word" instruction. Fix: every occurrence gets an entry, even if `gloss` is
   trivially "indeed" or "but".

4. **Compounds in `pada_analysis` not always echoed in `samasa_vigrahas`.** Wherever a stem like
   `jñāna-hetutva` appears, a samāsa entry should resolve it; this is uneven across the corpus.

5. **`karaka_structure` and `verb_modality` are mostly populated** but a few passages with multiple
   finite verbs only annotate the principal verb; subordinate verbs (especially in samuccaya
   constructions) are sometimes omitted.

6. **`why_this_passage` is generally above the 30-word floor** — this defect is rare and shows the
   `why_this_passage` field has been taken seriously by Wave 2 agents.
