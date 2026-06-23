/* =============================================================
   Bhagavad-Gītā 2.54–72 — "Across traditions" parallels.
   window.GITA_PARALLELS — keyed by verse locus.

   These are not Gītā commentary. Each entry is a separate text in
   another tradition that describes the same state — the realized one
   (sthitaprajña / jīvanmukta / vītarāga / arahant) — presented as a
   thematic parallel, attributed, not derived from the Gītā, and mapped
   to the Gītā verse it most closely illuminates.

   Every `sanskrit` field is verbatim from the cited source (Sanskrit,
   Pali, or Prakrit, in the source's own orthography). `ourRendering`
   is a literal English translation by this project — no source's
   translation is reproduced. Sources are on-disk paths or stable URLs.

   Entry shape:
     { school, thinker, work, locus,
       sanskrit:<verbatim>, ourRendering:<literal English>, source:<path|url> }
   ============================================================= */

window.GITA_PARALLELS = {

  // 2.55 — "When he abandons all desires of the mind and is content
  //         in the self by the self, then he is called sthitaprajña."
  "2.55": [
    {
      school: "Advaita Vedānta",
      thinker: "attributed to Śaṅkara",
      work: "Vivekacūḍāmaṇi",
      locus: "426",
      sanskrit: "sthitaprajño yatir ayaṃ yaḥ sadānandam aśnute | brahmaṇy eva vilīnātmā nirvikāro viniṣkriyaḥ ||",
      ourRendering: "This ascetic of settled wisdom (sthitaprajña) is one who feeds on unbroken bliss — his self dissolved in Brahman alone, unchanging, free of all activity.",
      source: "data/sources/sanskrit/vedanta/full_corpus/shankara_vivekacudamani_gretil.txt (v. 426)",
      words: [
        {
          i: 0,
          iast: "sthitaprajñaḥ",
          gloss: "of settled wisdom",
          parts: [
            { form: "sthita", gloss: "stood firm, steady, settled, established" },
            { form: "prajñā", gloss: "wisdom, insight, discernment, understanding" }
          ],
          stem: "sthita-prajña",
          root: "√jñā",
          rootGloss: "to know, to understand, to discern",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc.",
          karaka: "kartṛ (agent of aśnute)",
          compound: { type: "bahuvrīhi", vigraha: "sthitā prajñā yasya saḥ", members: ["sthita", "prajñā"] },
          glossaryKey: "sthitaprajna",
          translatable: true
        },
        {
          i: 1,
          iast: "yatiḥ",
          gloss: "ascetic",
          parts: [
            { form: "√yam", gloss: "to restrain" },
            { form: "-ti", gloss: "(agent noun: one who restrains himself)" }
          ],
          stem: "yati",
          root: "√yam (saṃyamane, bhvādi, 1P, 'to restrain')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc.",
          karaka: "kartṛ (in apposition to sthitaprajñaḥ)",
          glossaryKey: "samnyasa",
          translatable: true
        },
        {
          i: 2,
          iast: "ayam",
          gloss: "this",
          parts: [
            { form: "idam", gloss: "this" }
          ],
          stem: "idam",
          root: null,
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc. (demonstrative pronoun)",
          translatable: true
        },
        {
          i: 3,
          iast: "yaḥ",
          gloss: "who",
          parts: [
            { form: "yad", gloss: "who, which" }
          ],
          stem: "yad",
          root: null,
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc. (relative pronoun)",
          karaka: "kartṛ (subject of the relative clause)",
          translatable: true
        },
        {
          i: 4,
          iast: "sadānandam",
          gloss: "ever-bliss",
          parts: [
            { form: "sadā", gloss: "always, ever, at all times" },
            { form: "ānanda", gloss: "bliss, joy, felicity, beatitude" }
          ],
          stem: "sadānanda",
          root: null,
          affix: "am (dvitīyā ekavacana)",
          morph: "acc. sg. masc.",
          karaka: "karman (object of aśnute)",
          compound: { type: "karmadhāraya", vigraha: "sadā ānandaḥ", members: ["sadā", "ānanda"] },
          glossaryKey: "ananda",
          translatable: true
        },
        {
          i: 5,
          iast: "aśnute",
          gloss: "feeds on, enjoys",
          parts: [
            { form: "√aś", gloss: "to eat, to partake of, to enjoy, to feed on" },
            { form: "-te", gloss: "(present, 3rd sg. ātmanepada)" }
          ],
          stem: null,
          root: "√aś (aśnoteḥ, svādi, 5A, 'to partake of, enjoy')",
          affix: "ta (tiṅ, present, prathama-puruṣa ekavacana, ātmanepada)",
          morph: "pres. indic. 3rd sg. ātmanepada",
          translatable: true
        },
        {
          i: 6,
          iast: "brahmaṇi",
          gloss: "in Brahman",
          parts: [
            { form: "brahman", gloss: "the Absolute; the supreme reality, the vast, the boundless" }
          ],
          stem: "brahman",
          root: null,
          affix: "ṅi (saptamī ekavacana)",
          morph: "loc. sg. neut.",
          karaka: "adhikaraṇa (locus of vilīna)",
          glossaryKey: "brahman",
          translatable: false
        },
        {
          i: 7,
          iast: "eva",
          gloss: "alone, only",
          parts: [
            { form: "eva", gloss: "indeed, alone (restrictive particle)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "indeclinable (avyaya)",
          translatable: true
        },
        {
          i: 8,
          iast: "vilīnātmā",
          gloss: "his self dissolved",
          parts: [
            { form: "vi-", gloss: "completely, away, apart" },
            { form: "√lī", gloss: "to dissolve, to merge, to melt away, to cling" },
            { form: "-na", gloss: "(past participle)" },
            { form: "ātman", gloss: "self, the innermost self, soul" }
          ],
          stem: "vilīna-ātman",
          root: "√lī (līṅ, divādi, 4A / juhotyādi, 'to dissolve, cling, melt')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc.",
          karaka: "kartṛ (predicative of yaḥ)",
          compound: { type: "bahuvrīhi", vigraha: "vilīnaḥ ātmā yasya saḥ", members: ["vilīna", "ātman"] },
          glossaryKey: "atman",
          translatable: true
        },
        {
          i: 9,
          iast: "nirvikāraḥ",
          gloss: "unchanging",
          parts: [
            { form: "nis-", gloss: "without, free of, devoid of" },
            { form: "vikāra", gloss: "modification, change, alteration, transformation" }
          ],
          stem: "nirvikāra",
          root: null,
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc.",
          karaka: "kartṛ (predicative of yaḥ)",
          compound: { type: "bahuvrīhi", vigraha: "nirgataḥ vikāraḥ yasmāt saḥ", members: ["nis", "vikāra"] },
          translatable: true
        },
        {
          i: 10,
          iast: "viniṣkriyaḥ",
          gloss: "free of all activity",
          parts: [
            { form: "vi-", gloss: "completely, out" },
            { form: "nis-", gloss: "without, free of, devoid of" },
            { form: "kriyā", gloss: "action, activity, doing, performance" }
          ],
          stem: "viniṣkriya",
          root: "√kṛ (ḍukṛñ, tanādi, 8U, 'to do, make')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc.",
          karaka: "kartṛ (predicative of yaḥ)",
          compound: { type: "bahuvrīhi", vigraha: "viniṣkrāntā kriyā yasmāt saḥ", members: ["vi", "nis", "kriyā"] },
          glossaryKey: "kriya",
          translatable: true
        }
      ],
      english: "{2:This} {1:ascetic} {0:of settled wisdom} is {3:one who} {5:feeds on} {4:ever-bliss} — {8:his self dissolved} {6:in Brahman} {7:alone}, {9:unchanging}, {10:free of all activity}."
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "1.15",
      sanskrit: "dṛṣṭānuśravikaviṣayavitṛṣṇasya vaśīkārasaṃjñā vairāgyam ||",
      ourRendering: "Dispassion (vairāgya) is the mark of mastery in one who has ceased to thirst for objects seen or heard-of.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 1.15)",
      words: [
        {
          i: 0,
          iast: "dṛṣṭānuśravikaviṣayavitṛṣṇasya",
          gloss: "of one who has ceased to thirst for objects seen or heard-of",
          parts: [
            { form: "dṛṣṭa", gloss: "seen (√dṛś + kta)" },
            { form: "ānuśravika", gloss: "heard-of, scriptural (derived from anuśrava 'tradition, what is heard')" },
            { form: "viṣaya", gloss: "object, sense-object, sphere, domain" },
            { form: "vi-", gloss: "away from, free of" },
            { form: "tṛṣṇā", gloss: "thirst, craving, longing, eager desire" }
          ],
          stem: "dṛṣṭa-ānuśravika-viṣaya-vitṛṣṇa",
          root: "√tṛṣ (tṛṣa pipāsāyām, divādi, 4P, 'to be thirsty')",
          affix: "ṅas (ṣaṣṭhī ekavacana)",
          morph: "gen. sg. masc.",
          karaka: "sambandha (relational genitive: 'of/in one who…')",
          compound: { type: "bahuvrīhi", vigraha: "dṛṣṭe ānuśravike ca viṣaye vigatā tṛṣṇā yasya saḥ", members: ["dṛṣṭa", "ānuśravika", "viṣaya", "vitṛṣṇa"] },
          glossaryKey: "trsna",
          translatable: true
        },
        {
          i: 1,
          iast: "vaśīkārasaṃjñā",
          gloss: "named/marked by mastery",
          parts: [
            { form: "vaśī-kāra", gloss: "the act of bringing under control, mastery (vaśa + √kṛ + cvi)" },
            { form: "saṃjñā", gloss: "designation, name, mark, sign" }
          ],
          stem: "vaśīkāra-saṃjñā",
          root: null,
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. fem.",
          karaka: "kartṛ (predicate of the nominal sentence)",
          compound: { type: "bahuvrīhi", vigraha: "vaśīkārasya saṃjñā yasya tat", members: ["vaśīkāra", "saṃjñā"] },
          translatable: true
        },
        {
          i: 2,
          iast: "vairāgyam",
          gloss: "dispassion",
          parts: [
            { form: "vi-", gloss: "away from, free of" },
            { form: "rāga", gloss: "coloring, hue, dye; attachment, attraction" },
            { form: "-ya", gloss: "(abstract-noun taddhita, with vṛddhi: 'the state of being uncolored')" }
          ],
          stem: "vairāgya",
          root: "√rañj (raji rāge, bhvādi, 1U, 'to be dyed, to be attached')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut.",
          karaka: "kartṛ (grammatical subject of the nominal sentence)",
          glossaryKey: "vairagya",
          translatable: true
        }
      ],
      english: "{2:Dispassion} is the {1:mark of mastery} {0:in one who has ceased to thirst for objects seen or heard-of}."
    }
  ],

  // 2.56 — "Unshaken in mind amid sorrows, without longing amid pleasures,
  //         free of passion, fear and anger — the sage of steady wisdom."
  "2.56": [
    {
      school: "Buddhism (Theravāda)",
      thinker: "Dhammapada",
      work: "Dhammapada, Arahantavagga",
      locus: "99",
      sanskrit: "ramaṇīyāni araññāni, yattha na ramatī jano; vītarāgā ramissanti, na te kāmagavesino.",
      ourRendering: "Delightful are the forests where ordinary folk find no delight; the passion-free (vītarāga) will delight there — they are not the seekers of pleasures.",
      source: "data/sources/pali/suttacentral/dhammapada_arahantavagga_90-99_root-pli-ms.json (dhp 99)",
      words: [
        {
          i: 0,
          iast: "ramaṇīyāni",
          gloss: "delightful",
          parts: [
            { form: "√ram", gloss: "to delight, take pleasure (Skt cognate √ram)" },
            { form: "-aṇīya", gloss: "(gerundive / potential participle: 'to be delighted in')" }
          ],
          stem: "ramaṇīya",
          root: "√ram (Pali; Skt √ram, bhvādi, 1A, 'to delight')",
          affix: "-ni (nom. pl. neut., Pali a-stem)",
          morph: "Pali nom. pl. neut. (gerundive)",
          translatable: true
        },
        {
          i: 1,
          iast: "araññāni",
          gloss: "forests",
          parts: [
            { form: "arañña", gloss: "forest, wilderness (Skt araṇya)" }
          ],
          stem: "arañña",
          root: null,
          affix: "-ni (nom. pl. neut., Pali a-stem)",
          morph: "Pali nom. pl. neut.",
          translatable: true
        },
        {
          i: 2,
          iast: "yattha",
          gloss: "where",
          parts: [
            { form: "yattha", gloss: "where (relative adverb of place; Skt yatra)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (relative adverb)",
          translatable: true
        },
        {
          i: 3,
          iast: "na",
          gloss: "not",
          parts: [
            { form: "na", gloss: "not (negation)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (negative particle)",
          translatable: true
        },
        {
          i: 4,
          iast: "ramatī",
          gloss: "delights",
          parts: [
            { form: "√ram", gloss: "to delight (Skt √ram)" },
            { form: "-ti", gloss: "(present, 3rd sg.; metrically lengthened -ī)" }
          ],
          stem: null,
          root: "√ram (Pali; Skt √ram, bhvādi, 1A)",
          affix: "-ti (Pali present, 3rd sg.)",
          morph: "Pali pres. 3rd sg. (-ī metri causa)",
          translatable: true
        },
        {
          i: 5,
          iast: "jano",
          gloss: "ordinary folk",
          parts: [
            { form: "jana", gloss: "people, folk (Skt jana)" }
          ],
          stem: "jana",
          root: null,
          affix: "-o (nom. sg. masc., Pali a-stem; Skt -aḥ)",
          morph: "Pali nom. sg. masc. (collective)",
          translatable: true
        },
        {
          i: 6,
          iast: "vītarāgā",
          gloss: "the passion-free",
          parts: [
            { form: "vīta", gloss: "gone away, departed, vanished (vi + √i + ta; Skt vīta)" },
            { form: "rāga", gloss: "coloring, hue; attachment, attraction (Skt rāga)" }
          ],
          stem: "vīta-rāga",
          root: null,
          affix: "-ā (nom. pl. masc., Pali a-stem)",
          morph: "Pali nom. pl. masc. (bahubbīhi)",
          compound: { type: "bahuvrīhi", vigraha: "vīto rāgo yesaṃ te (Skt: vīto rāgo yeṣāṃ te)", members: ["vīta", "rāga"] },
          glossaryKey: "raga",
          translatable: true
        },
        {
          i: 7,
          iast: "ramissanti",
          gloss: "will delight",
          parts: [
            { form: "√ram", gloss: "to delight (Skt √ram)" },
            { form: "-issanti", gloss: "(future, 3rd pl.)" }
          ],
          stem: null,
          root: "√ram (Pali; Skt √ram, bhvādi, 1A)",
          affix: "-issanti (Pali future, 3rd pl.)",
          morph: "Pali fut. 3rd pl.",
          translatable: true
        },
        {
          i: 8,
          iast: "na",
          gloss: "not",
          parts: [
            { form: "na", gloss: "not (negation)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (negative particle)",
          translatable: true
        },
        {
          i: 9,
          iast: "te",
          gloss: "they",
          parts: [
            { form: "ta", gloss: "that, he/they (Skt tad)" }
          ],
          stem: "ta",
          root: null,
          affix: "-e (nom. pl. masc., Pali pronoun)",
          morph: "Pali nom. pl. masc. (demonstrative pronoun)",
          translatable: true
        },
        {
          i: 10,
          iast: "kāmagavesino",
          gloss: "seekers of pleasures",
          parts: [
            { form: "kāma", gloss: "desire, longing, wish; sense-pleasure (Skt kāma)" },
            { form: "gavesin", gloss: "seeking, searching for, in quest of (Skt gaveṣin, from gaveṣ 'to seek')" }
          ],
          stem: "kāma-gavesin",
          root: null,
          affix: "-no (nom. pl. masc., Pali -in stem; Skt -inaḥ)",
          morph: "Pali nom. pl. masc.",
          compound: { type: "tatpuruṣa", vigraha: "kāmānaṃ gavesino (Skt: kāmānāṃ gaveṣiṇaḥ)", members: ["kāma", "gavesin"] },
          glossaryKey: "kama",
          translatable: true
        }
      ],
      english: "{0:Delightful} are the {1:forests} {2:where} {5:ordinary folk} {4:find} {3:no} delight; {6:the passion-free} {7:will delight} there — {9:they} are {8:not} the {10:seekers of pleasures}."
    },
    {
      school: "Jainism",
      thinker: "Uttarādhyayana",
      work: "Uttarajjhayā (Uttarādhyayana-sūtra), ch. 32 Pamāyaṭhāṇa",
      locus: "32.100",
      sanskrit: "evindiyatthā ya maṇassa atthā | dukkhassa heuṃ maṇuyassa rāgiṇo | te ceva thovaṃ pi kayāi dukkhaṃ | na vīyarāgassa karenti kiṃci ||",
      ourRendering: "Thus the objects of the senses and the objects of the mind are a cause of suffering for the man who has passion (rāgin); those very same objects never cause the passion-free one (vītarāga) the least suffering.",
      source: "data/sources/prakrit/jaina/uttarajjhaya_gretil_plaintext.txt (Uttar 32.100)",
      words: [
        {
          i: 0,
          iast: "ev(a)",
          gloss: "thus",
          parts: [
            { form: "eva", gloss: "thus, so (Skt evam; here eva- by sandhi before indiya-)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit (Ardha-Māgadhī) indeclinable (Skt evam)",
          translatable: true
        },
        {
          i: 1,
          iast: "indiyatthā",
          gloss: "the objects of the senses",
          parts: [
            { form: "indiya", gloss: "sense-faculty, sense-organ, power (Skt indriya)" },
            { form: "attha", gloss: "object, thing, aim (Skt artha)" }
          ],
          stem: "indiya-attha",
          root: null,
          affix: "-ā (nom. pl. masc., Prakrit a-stem; Skt -āḥ)",
          morph: "Prakrit nom. pl. masc.",
          compound: { type: "tatpuruṣa", vigraha: "indiyāṇaṃ atthā (Skt: indriyāṇām arthāḥ)", members: ["indiya", "attha"] },
          glossaryKey: "indriya",
          translatable: true
        },
        {
          i: 2,
          iast: "ya",
          gloss: "and",
          parts: [
            { form: "ya", gloss: "and (Skt ca)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit indeclinable (conjunction; Skt ca)",
          translatable: true
        },
        {
          i: 3,
          iast: "maṇassa",
          gloss: "of the mind",
          parts: [
            { form: "maṇa", gloss: "mind; the inner organ of thought (Skt manas)" }
          ],
          stem: "maṇa",
          root: null,
          affix: "-ssa (gen. sg.; Skt -asya)",
          morph: "Prakrit gen. sg. (Skt manasaḥ)",
          glossaryKey: "manas",
          translatable: true
        },
        {
          i: 4,
          iast: "atthā",
          gloss: "the objects",
          parts: [
            { form: "attha", gloss: "object (Skt artha)" }
          ],
          stem: "attha",
          root: null,
          affix: "-ā (nom. pl. masc.; Skt -āḥ)",
          morph: "Prakrit nom. pl. masc.",
          translatable: true
        },
        {
          i: 5,
          iast: "dukkhassa",
          gloss: "of suffering",
          parts: [
            { form: "dukkha", gloss: "suffering, sorrow, pain, distress (Skt duḥkha)" }
          ],
          stem: "dukkha",
          root: null,
          affix: "-ssa (gen. sg.; Skt -asya)",
          morph: "Prakrit gen. sg. neut. (Skt duḥkhasya)",
          glossaryKey: "duhkha",
          translatable: true
        },
        {
          i: 6,
          iast: "heuṃ",
          gloss: "a cause",
          parts: [
            { form: "heu", gloss: "cause (Skt hetu)" }
          ],
          stem: "heu",
          root: null,
          affix: "-ṃ (acc./predicative sg.; Skt hetum)",
          morph: "Prakrit sg. (Skt hetum, predicative)",
          translatable: true
        },
        {
          i: 7,
          iast: "maṇuyassa",
          gloss: "for the man",
          parts: [
            { form: "maṇuya", gloss: "man, human (Skt manuja / manuṣya)" }
          ],
          stem: "maṇuya",
          root: null,
          affix: "-ssa (gen./dat. sg.; Skt -asya)",
          morph: "Prakrit gen. sg. masc. (Skt manujasya)",
          translatable: true
        },
        {
          i: 8,
          iast: "rāgiṇo",
          gloss: "who has passion",
          parts: [
            { form: "rāga", gloss: "coloring, hue; attachment, attraction (Skt rāga)" },
            { form: "-in", gloss: "(possessive: 'having'; Skt -in)" }
          ],
          stem: "rāgin",
          root: null,
          affix: "-ṇo (gen. sg., -in stem; Skt -iṇaḥ)",
          morph: "Prakrit gen. sg. masc. (Skt rāgiṇaḥ)",
          glossaryKey: "raga",
          translatable: true
        },
        {
          i: 9,
          iast: "te",
          gloss: "those",
          parts: [
            { form: "ta", gloss: "that, those (Skt tad)" }
          ],
          stem: "ta",
          root: null,
          affix: "-e (nom. pl. masc.; Skt te)",
          morph: "Prakrit nom. pl. masc. (demonstrative)",
          translatable: true
        },
        {
          i: 10,
          iast: "ceva",
          gloss: "very same",
          parts: [
            { form: "ca", gloss: "and (Skt ca)" },
            { form: "eva", gloss: "indeed, very (Skt eva)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit indeclinable (ca + eva, emphatic)",
          translatable: true
        },
        {
          i: 11,
          iast: "thovaṃ",
          gloss: "a little",
          parts: [
            { form: "thova", gloss: "little, slight (Skt stoka)" }
          ],
          stem: "thova",
          root: null,
          affix: "-ṃ (acc. sg. neut.; Skt stokam)",
          morph: "Prakrit acc. sg. neut. (adverbial: 'in the least')",
          translatable: true
        },
        {
          i: 12,
          iast: "pi",
          gloss: "even",
          parts: [
            { form: "pi", gloss: "even, also (Skt api)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit indeclinable (Skt api)",
          translatable: true
        },
        {
          i: 13,
          iast: "kayāi",
          gloss: "ever",
          parts: [
            { form: "kayāi", gloss: "at any time, ever (Skt kadācit)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit indeclinable (adverb of time; Skt kadācit)",
          translatable: true
        },
        {
          i: 14,
          iast: "dukkhaṃ",
          gloss: "suffering",
          parts: [
            { form: "dukkha", gloss: "suffering, sorrow, pain, distress (Skt duḥkha)" }
          ],
          stem: "dukkha",
          root: null,
          affix: "-ṃ (acc. sg. neut.; Skt duḥkham)",
          morph: "Prakrit acc. sg. neut. (object of karenti)",
          glossaryKey: "duhkha",
          translatable: true
        },
        {
          i: 15,
          iast: "na",
          gloss: "not",
          parts: [
            { form: "na", gloss: "not (Skt na)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit indeclinable (negation)",
          translatable: true
        },
        {
          i: 16,
          iast: "vīyarāgassa",
          gloss: "for the passion-free one",
          parts: [
            { form: "vīya", gloss: "gone away, departed (Skt vīta)" },
            { form: "rāga", gloss: "coloring, hue; attachment, attraction (Skt rāga)" }
          ],
          stem: "vīya-rāga",
          root: null,
          affix: "-ssa (gen./dat. sg.; Skt -asya)",
          morph: "Prakrit gen. sg. masc. (Skt vītarāgasya)",
          compound: { type: "bahuvrīhi", vigraha: "vīo rāgo jassa so (Skt: vīto rāgo yasya saḥ)", members: ["vīya", "rāga"] },
          glossaryKey: "raga",
          translatable: true
        },
        {
          i: 17,
          iast: "karenti",
          gloss: "cause, make",
          parts: [
            { form: "√kar", gloss: "to do, make (Skt √kṛ)" },
            { form: "-enti", gloss: "(present, 3rd pl.)" }
          ],
          stem: null,
          root: "√kar (Prakrit; Skt √kṛ, tanādi, 8U, 'to do, make')",
          affix: "-enti (Prakrit present, 3rd pl.)",
          morph: "Prakrit pres. 3rd pl. (Skt kurvanti)",
          translatable: true
        },
        {
          i: 18,
          iast: "kiṃci",
          gloss: "the least, anything",
          parts: [
            { form: "kiṃ", gloss: "what (Skt kim)" },
            { form: "-ci", gloss: "(indefinite particle; Skt -cit)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit indefinite (Skt kiṃcit): 'anything (at all)'",
          translatable: true
        }
      ],
      english: "{0:Thus} {1:the objects of the senses} {2:and} {4:the objects} {3:of the mind} are {6:a cause} {5:of suffering} {7:for the man} {8:who has passion}; {9:those} {10:very same} objects {15:never} {13:ever} {17:cause} {16:the passion-free one} {11:the least} {14:suffering} — {12:even} {18:anything at all}."
    },
    {
      school: "Advaita Vedānta",
      thinker: "attributed to Śaṅkara",
      work: "Vivekacūḍāmaṇi",
      locus: "434",
      sanskrit: "iṣṭāniṣṭārthasamprāptau samadarśitayātmani | ubhayatrāvikāritvaṃ jīvanmuktasya lakṣaṇam ||",
      ourRendering: "When the welcome and the unwelcome arrive, to remain unchanged toward both, even-sighted in oneself — that is the mark of one liberated while living.",
      source: "data/sources/sanskrit/vedanta/full_corpus/shankara_vivekacudamani_gretil.txt (v. 434)",
      words: [
        {
          i: 0,
          iast: "iṣṭāniṣṭārthasamprāptau",
          gloss: "when the welcome and the unwelcome arrive",
          parts: [
            { form: "iṣṭa", gloss: "desired, wished-for, welcome (√iṣ + kta)" },
            { form: "an-", gloss: "not, un-" },
            { form: "iṣṭa", gloss: "desired, wished-for" },
            { form: "artha", gloss: "thing, object, aim, purpose" },
            { form: "sam-", gloss: "together, fully" },
            { form: "pra-", gloss: "forth" },
            { form: "āpti", gloss: "arrival, attainment, reaching (√āp + ktin)" }
          ],
          stem: "iṣṭa-aniṣṭa-artha-samprāpti",
          root: "√āp (āpḷ vyāptau, svādi, 5P, 'to reach, attain')",
          affix: "ṅi (saptamī ekavacana)",
          morph: "loc. sg. fem.",
          karaka: "adhikaraṇa (locative absolute / temporal locus: 'on the arriving')",
          compound: { type: "tatpuruṣa", vigraha: "iṣṭasya ca aniṣṭasya ca arthasya samprāptiḥ", members: ["iṣṭa", "aniṣṭa", "artha", "samprāpti"] },
          translatable: true
        },
        {
          i: 1,
          iast: "samadarśitayā",
          gloss: "by even-sightedness",
          parts: [
            { form: "sama", gloss: "even, equal, alike, impartial" },
            { form: "darśin", gloss: "seeing, beholding, regarding (√dṛś + ṇini)" },
            { form: "-tā", gloss: "(abstract-noun taddhita: 'the state of')" }
          ],
          stem: "sama-darśi-tā",
          root: "√dṛś (dṛśir prekṣaṇe, bhvādi, 1P, 'to see')",
          affix: "ṭā (tṛtīyā ekavacana)",
          morph: "instr. sg. fem.",
          karaka: "karaṇa (means: 'by/with even-sightedness')",
          compound: { type: "bahuvrīhi", vigraha: "samaṃ darśanaṃ yasya saḥ, tasya bhāvaḥ", members: ["sama", "darśin"] },
          translatable: true
        },
        {
          i: 2,
          iast: "ātmani",
          gloss: "in oneself",
          parts: [
            { form: "ātman", gloss: "self" }
          ],
          stem: "ātman",
          root: null,
          affix: "ṅi (saptamī ekavacana)",
          morph: "loc. sg. masc.",
          karaka: "adhikaraṇa (locus of even-sightedness)",
          glossaryKey: "atman",
          translatable: false
        },
        {
          i: 3,
          iast: "ubhayatra",
          gloss: "toward both",
          parts: [
            { form: "ubhaya", gloss: "both" },
            { form: "-tra", gloss: "(locative taddhita adverb: 'in/toward')" }
          ],
          stem: null,
          root: null,
          affix: "tral (taddhita, 'in/at')",
          morph: "indeclinable adverb (avyaya): 'in both cases'",
          translatable: true
        },
        {
          i: 4,
          iast: "avikāritvam",
          gloss: "remaining unchanged",
          parts: [
            { form: "a-", gloss: "not" },
            { form: "vikārin", gloss: "subject to change (vi + √kṛ + ṇini)" },
            { form: "-tva", gloss: "(abstract-noun taddhita: 'the state of')" }
          ],
          stem: "a-vikāri-tva",
          root: "√kṛ (ḍukṛñ, tanādi, 8U, 'to do, make')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut.",
          karaka: "kartṛ (grammatical subject of the nominal sentence)",
          translatable: true
        },
        {
          i: 5,
          iast: "jīvanmuktasya",
          gloss: "of one liberated while living",
          parts: [
            { form: "jīvat", gloss: "living, alive, while living (√jīv + śatṛ)" },
            { form: "mukta", gloss: "liberated, released, freed, set loose (√muc + kta)" }
          ],
          stem: "jīvan-mukta",
          root: "√muc (muca mocane, tudādi, 6U, 'to release, free')",
          affix: "ṅas (ṣaṣṭhī ekavacana)",
          morph: "gen. sg. masc.",
          karaka: "sambandha (possessive genitive: 'mark of…')",
          compound: { type: "tatpuruṣa", vigraha: "jīvan muktaḥ", members: ["jīvat", "mukta"] },
          glossaryKey: "jivanmukta",
          translatable: true
        },
        {
          i: 6,
          iast: "lakṣaṇam",
          gloss: "the mark",
          parts: [
            { form: "√lakṣ", gloss: "to mark, to characterize, to define, to denote" },
            { form: "-ana", gloss: "(action/instrument noun: 'characteristic')" }
          ],
          stem: "lakṣaṇa",
          root: "√lakṣ (lakṣa darśanāṅkanayoḥ, curādi, 10U, 'to mark, observe')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut.",
          karaka: "kartṛ (predicate nominative)",
          glossaryKey: "laksana",
          translatable: true
        }
      ],
      english: "{0:When the welcome and the unwelcome arrive}, {4:to remain unchanged} {3:toward both}, {1:even-sighted} {2:in oneself} — that is {6:the mark} {5:of one liberated while living}."
    }
  ],

  // 2.57 — "He who is unattached on every side, who neither rejoices nor
  //         recoils at good or ill fortune — his wisdom stands firm."
  "2.57": [
    {
      school: "Buddhism (Theravāda)",
      thinker: "Dhammapada",
      work: "Dhammapada, Arahantavagga",
      locus: "95",
      sanskrit: "pathavisamo no virujjhati, indakhilupamo tādi subbato; rahadova apetakaddamo, saṃsārā na bhavanti tādino.",
      ourRendering: "Like the earth he offers no resistance; like a city's pillar such a one stands, true to his vow; like a lake cleared of mud — for the one who is Such (tādin) there are no more rounds of wandering.",
      source: "data/sources/pali/suttacentral/dhammapada_arahantavagga_90-99_root-pli-ms.json (dhp 95)",
      words: [
        {
          i: 0,
          iast: "pathavisamo",
          gloss: "like the earth",
          parts: [
            { form: "pathavī", gloss: "earth, ground, soil (Skt pṛthivī)" },
            { form: "sama", gloss: "equal to, like, the same as (Skt sama)" }
          ],
          stem: "pathavi-sama",
          root: null,
          affix: "-o (nom. sg. masc., Pali a-stem; Skt -aḥ)",
          morph: "Pali nom. sg. masc.",
          compound: { type: "tatpuruṣa", vigraha: "pathaviyā samo (Skt: pṛthivyā samaḥ)", members: ["pathavī", "sama"] },
          translatable: true
        },
        {
          i: 1,
          iast: "no",
          gloss: "not",
          parts: [
            { form: "no", gloss: "not, indeed not (emphatic negation; Skt no)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (negative particle)",
          translatable: true
        },
        {
          i: 2,
          iast: "virujjhati",
          gloss: "offers resistance, is opposed",
          parts: [
            { form: "vi-", gloss: "apart, against (Skt vi-)" },
            { form: "√rudh", gloss: "to obstruct, oppose (Skt √rudh)" },
            { form: "-ya-ti", gloss: "(passive/middle present, 3rd sg.)" }
          ],
          stem: null,
          root: "√rudh (Pali; Skt √rudh, rudhādi, 7U, 'to obstruct')",
          affix: "-ti (Pali present, 3rd sg.)",
          morph: "Pali pres. 3rd sg. (Skt virudhyate)",
          translatable: true
        },
        {
          i: 3,
          iast: "indakhilupamo",
          gloss: "like a city's gate-pillar",
          parts: [
            { form: "inda-khila", gloss: "Indra's post — the firm pillar/threshold at a city gate (Skt indra-khila)" },
            { form: "upama", gloss: "resembling, like (Skt upama)" }
          ],
          stem: "indakhila-upama",
          root: null,
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Pali nom. sg. masc.",
          compound: { type: "tatpuruṣa", vigraha: "indakhilena upamo (Skt: indrakhilenopamaḥ)", members: ["inda-khila", "upama"] },
          translatable: true
        },
        {
          i: 4,
          iast: "tādi",
          gloss: "such a one",
          parts: [
            { form: "tādin", gloss: "of such a kind, the Such (the unshaken sage; Skt tādṛś / tādin)" }
          ],
          stem: "tādin",
          root: null,
          affix: "-i (nom. sg. masc., Pali -in stem; Skt tādī)",
          morph: "Pali nom. sg. masc.",
          translatable: true
        },
        {
          i: 5,
          iast: "subbato",
          gloss: "true to his vow",
          parts: [
            { form: "su-", gloss: "good, well (Skt su-)" },
            { form: "vata", gloss: "vow, observance (Skt vrata)" }
          ],
          stem: "su-vata",
          root: null,
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Pali nom. sg. masc. (bahubbīhi)",
          compound: { type: "bahuvrīhi", vigraha: "sundaraṃ vataṃ yassa so (Skt: śobhanaṃ vrataṃ yasya saḥ)", members: ["su", "vata"] },
          translatable: true
        },
        {
          i: 6,
          iast: "rahado",
          gloss: "a lake",
          parts: [
            { form: "rahada", gloss: "a deep lake, pool (Skt hrada)" }
          ],
          stem: "rahada",
          root: null,
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Pali nom. sg. masc.",
          translatable: true
        },
        {
          i: 7,
          iast: "va",
          gloss: "like",
          parts: [
            { form: "va", gloss: "like, as (Skt iva)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (comparative particle; Skt iva)",
          translatable: true
        },
        {
          i: 8,
          iast: "apetakaddamo",
          gloss: "cleared of mud",
          parts: [
            { form: "apeta", gloss: "gone away, removed (apa + √i + ta; Skt apeta)" },
            { form: "kaddama", gloss: "mud, mire (Skt kardama)" }
          ],
          stem: "apeta-kaddama",
          root: null,
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Pali nom. sg. masc. (bahubbīhi)",
          compound: { type: "bahuvrīhi", vigraha: "apeto kaddamo yamhā so (Skt: apeto kardamo yasmāt saḥ)", members: ["apeta", "kaddama"] },
          translatable: true
        },
        {
          i: 9,
          iast: "saṃsārā",
          gloss: "the rounds of wandering",
          parts: [
            { form: "saṃ-", gloss: "together, around (Skt saṃ-)" },
            { form: "√sar", gloss: "to flow, to run on, to move, to wander (Skt √sṛ)" },
            { form: "-a", gloss: "(action noun: 'faring on, transmigration')" }
          ],
          stem: "saṃsāra",
          root: "√sar (Pali; Skt √sṛ, bhvādi, 1P, 'to flow, move')",
          affix: "-ā (nom. pl. masc.; Skt -āḥ)",
          morph: "Pali nom. pl. masc.",
          glossaryKey: "samsara",
          translatable: false
        },
        {
          i: 10,
          iast: "na",
          gloss: "not",
          parts: [
            { form: "na", gloss: "not (Skt na)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (negation)",
          translatable: true
        },
        {
          i: 11,
          iast: "bhavanti",
          gloss: "are, come to be",
          parts: [
            { form: "√bhū", gloss: "to be, become (Skt √bhū)" },
            { form: "-anti", gloss: "(present, 3rd pl.)" }
          ],
          stem: null,
          root: "√bhū (Pali; Skt √bhū, bhvādi, 1P, 'to be, become')",
          affix: "-anti (Pali present, 3rd pl.)",
          morph: "Pali pres. 3rd pl.",
          translatable: true
        },
        {
          i: 12,
          iast: "tādino",
          gloss: "for the one who is Such",
          parts: [
            { form: "tādin", gloss: "of such a kind, the Such (Skt tādin)" }
          ],
          stem: "tādin",
          root: null,
          affix: "-no (gen./dat. sg., -in stem; Skt tādinaḥ)",
          morph: "Pali gen. sg. masc. ('for/of such a one')",
          translatable: true
        }
      ],
      english: "{0:Like the earth} he is {1:not} {2:opposed/offers no resistance}; {3:like a city's gate-pillar} {4:such a one} stands, {5:true to his vow}; {7:like} {6:a lake} {8:cleared of mud} — {12:for the one who is Such} the {9:rounds of wandering} {10:do not} {11:come to be}."
    }
  ],

  // 2.58 — "When, like a tortoise drawing in its limbs from every side,
  //         he withdraws the senses from their objects — his wisdom stands firm."
  "2.58": [
    {
      school: "Buddhism (Theravāda)",
      thinker: "Saṃyutta Nikāya",
      work: "Kummopama-sutta (SN 35.240)",
      locus: "verse",
      sanskrit: "kummova aṅgāni sake kapāle, samodahaṃ bhikkhu manovitakke; anissito aññamaheṭhayāno, parinibbuto nūpavadeyya kañcī.",
      ourRendering: "As a tortoise its limbs within its own shell, let the monk gather in the mind's stirrings; unsupported, harming no other, fully gone out, let him reproach no one.",
      source: "data/sources/pali/suttacentral/sn35.240_kummopamasutta_root-pli-ms.json (SN 35.240, closing verse)",
      words: [
        {
          i: 0,
          iast: "kummo",
          gloss: "a tortoise",
          parts: [
            { form: "kumma", gloss: "tortoise (Skt kūrma)" }
          ],
          stem: "kumma",
          root: null,
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Pali nom. sg. masc.",
          translatable: true
        },
        {
          i: 1,
          iast: "va",
          gloss: "as, like",
          parts: [
            { form: "va", gloss: "like, as (Skt iva)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (comparative particle; Skt iva)",
          translatable: true
        },
        {
          i: 2,
          iast: "aṅgāni",
          gloss: "its limbs",
          parts: [
            { form: "aṅga", gloss: "limb (Skt aṅga)" }
          ],
          stem: "aṅga",
          root: null,
          affix: "-āni (acc. pl. neut.; Skt aṅgāni)",
          morph: "Pali acc. pl. neut. (object of samodahaṃ, by analogy)",
          translatable: true
        },
        {
          i: 3,
          iast: "sake",
          gloss: "its own",
          parts: [
            { form: "saka", gloss: "own (Skt svaka)" }
          ],
          stem: "saka",
          root: null,
          affix: "-e (loc. sg. neut.; Skt svake)",
          morph: "Pali loc. sg. neut.",
          translatable: true
        },
        {
          i: 4,
          iast: "kapāle",
          gloss: "within its shell",
          parts: [
            { form: "kapāla", gloss: "shell, carapace, skull-bowl (Skt kapāla)" }
          ],
          stem: "kapāla",
          root: null,
          affix: "-e (loc. sg. neut.; Skt kapāle)",
          morph: "Pali loc. sg. neut. ('within the shell')",
          translatable: true
        },
        {
          i: 5,
          iast: "samodahaṃ",
          gloss: "gathering in, drawing together",
          parts: [
            { form: "saṃ-", gloss: "together (Skt saṃ-)" },
            { form: "ava-", gloss: "down (Skt ava-)" },
            { form: "√dhā", gloss: "to place, put (Skt √dhā)" },
            { form: "-aṃ", gloss: "(present participle, nom. sg. masc.)" }
          ],
          stem: "samodaha",
          root: "√dhā (Pali; Skt √dhā, juhotyādi, 3U, 'to place')",
          affix: "-aṃ (Pali pres. participle, nom. sg. masc.)",
          morph: "Pali pres. participle nom. sg. masc. (Skt samavadadhat)",
          translatable: true
        },
        {
          i: 6,
          iast: "bhikkhu",
          gloss: "the monk",
          parts: [
            { form: "bhikkhu", gloss: "monk, mendicant (Skt bhikṣu, from √bhikṣ 'to beg')" }
          ],
          stem: "bhikkhu",
          root: null,
          affix: "-u (nom. sg. masc., Pali u-stem; Skt bhikṣuḥ)",
          morph: "Pali nom. sg. masc.",
          translatable: true
        },
        {
          i: 7,
          iast: "manovitakke",
          gloss: "the mind's stirrings",
          parts: [
            { form: "mano", gloss: "mind; the inner organ of thought (Skt manas)" },
            { form: "vitakka", gloss: "thought, applied thinking, reasoning, stirring (Skt vitarka)" }
          ],
          stem: "mano-vitakka",
          root: null,
          affix: "-e (acc. pl. masc.; Skt -ān)",
          morph: "Pali acc. pl. masc. (object of samodahaṃ)",
          compound: { type: "tatpuruṣa", vigraha: "manaso vitakkā (Skt: manaso vitarkāḥ)", members: ["mano", "vitakka"] },
          glossaryKey: "manas",
          translatable: true
        },
        {
          i: 8,
          iast: "anissito",
          gloss: "unsupported",
          parts: [
            { form: "an-", gloss: "not (Skt an-)" },
            { form: "nissita", gloss: "dependent on, supported by (ni + √śri + ta; Skt niḥśrita)" }
          ],
          stem: "an-issita",
          root: "√śri (Pali √sī/√si; Skt √śri, bhvādi, 1U, 'to lean on, resort to')",
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Pali nom. sg. masc. (past participle, negated)",
          translatable: true
        },
        {
          i: 9,
          iast: "aññamaheṭhayāno",
          gloss: "harming no other",
          parts: [
            { form: "añña", gloss: "another, other (Skt anya)" },
            { form: "a-", gloss: "not (Skt a-)" },
            { form: "heṭhayāna", gloss: "harming, troubling (√heṭh, pres. middle participle)" }
          ],
          stem: "añña-a-heṭhayāna",
          root: "√heṭh (Pali, 'to harm, vex'; Skt √heḍ / heṭh-)",
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Pali nom. sg. masc. (pres. middle participle, negated)",
          translatable: true
        },
        {
          i: 10,
          iast: "parinibbuto",
          gloss: "fully gone out",
          parts: [
            { form: "pari-", gloss: "completely, all round (Skt pari-)" },
            { form: "nibbuta", gloss: "gone out, extinguished, at peace (nir + √vā + ta; Skt nirvṛta)" }
          ],
          stem: "pari-nibbuta",
          root: "√vā (Pali; Skt √vā, adādi, 2P, 'to blow' — here the flame's going out)",
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Pali nom. sg. masc. (past participle; Skt parinirvṛtaḥ)",
          glossaryKey: "nibbana",
          translatable: true
        },
        {
          i: 11,
          iast: "na",
          gloss: "not",
          parts: [
            { form: "na", gloss: "not (Skt na; here n- before upavadeyya)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (negation)",
          translatable: true
        },
        {
          i: 12,
          iast: "upavadeyya",
          gloss: "let him reproach",
          parts: [
            { form: "upa-", gloss: "near, against (Skt upa-)" },
            { form: "√vad", gloss: "to speak (Skt √vad)" },
            { form: "-eyya", gloss: "(optative, 3rd sg.)" }
          ],
          stem: null,
          root: "√vad (Pali; Skt √vad, bhvādi, 1P, 'to speak')",
          affix: "-eyya (Pali optative, 3rd sg.)",
          morph: "Pali opt. 3rd sg. (Skt upavadet)",
          translatable: true
        },
        {
          i: 13,
          iast: "kañci",
          gloss: "anyone",
          parts: [
            { form: "kaṃ", gloss: "whom (Skt kam)" },
            { form: "-ci", gloss: "(indefinite particle; Skt -cit)" }
          ],
          stem: null,
          root: null,
          affix: "(acc. sg. masc., indefinite; Skt kaṃcit)",
          morph: "Pali acc. sg. masc. indefinite ('anyone'; -ī metri causa)",
          translatable: true
        }
      ],
      english: "{1:As} {0:a tortoise} {2:its limbs} {3:its own} {4:within its shell}, {5:let the monk gather in} {6:} {7:the mind's stirrings}; {8:unsupported}, {9:harming no other}, {10:fully gone out}, {12:let him} {11:not} reproach {13:anyone}."
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "2.54",
      sanskrit: "svaviṣayāsaṃprayoge cittasvarūpānukāra ivendriyāṇāṃ pratyāhāraḥ ||",
      ourRendering: "Withdrawal (pratyāhāra) is the senses' disengagement from their own objects, as if conforming to the nature of the mind itself.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 2.54)",
      words: [
        {
          i: 0,
          iast: "svaviṣayāsaṃprayoge",
          gloss: "in the disengagement from their own objects",
          parts: [
            { form: "sva", gloss: "own, one's own" },
            { form: "viṣaya", gloss: "object, sense-object, sense-field, domain" },
            { form: "a-", gloss: "non-, un-" },
            { form: "sam-", gloss: "together" },
            { form: "pra-", gloss: "forth" },
            { form: "yoga", gloss: "joining, union, contact, conjunction (√yuj + ghañ)" }
          ],
          stem: "sva-viṣaya-asaṃprayoga",
          root: "√yuj (yujir yoge, rudhādi, 7U, 'to join')",
          affix: "ṅi (saptamī ekavacana)",
          morph: "loc. sg. masc.",
          karaka: "adhikaraṇa (locative absolute: 'when there is non-contact')",
          compound: { type: "tatpuruṣa", vigraha: "svaviṣayaiḥ saha asaṃprayogaḥ", members: ["sva", "viṣaya", "asaṃprayoga"] },
          glossaryKey: "visaya",
          translatable: true
        },
        {
          i: 1,
          iast: "cittasvarūpānukāraḥ",
          gloss: "conforming to the nature of the mind",
          parts: [
            { form: "citta", gloss: "mind, mind-stuff, the thinking faculty, consciousness" },
            { form: "svarūpa", gloss: "own-form, intrinsic nature, essential character" },
            { form: "anu-", gloss: "after, following, in conformity with" },
            { form: "kāra", gloss: "doing, making, conforming (√kṛ + ghañ)" }
          ],
          stem: "citta-svarūpa-anukāra",
          root: "√kṛ (ḍukṛñ, tanādi, 8U, 'to do, make')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc.",
          karaka: "kartṛ (predicate of the nominal sentence)",
          compound: { type: "tatpuruṣa", vigraha: "cittasya svarūpasya anukāraḥ", members: ["citta", "svarūpa", "anukāra"] },
          glossaryKey: "citta",
          translatable: true
        },
        {
          i: 2,
          iast: "iva",
          gloss: "as if",
          parts: [
            { form: "iva", gloss: "as if, like (particle of comparison)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "indeclinable (avyaya)",
          translatable: true
        },
        {
          i: 3,
          iast: "indriyāṇām",
          gloss: "of the senses",
          parts: [
            { form: "indriya", gloss: "sense-faculty, sense-organ, power" }
          ],
          stem: "indriya",
          root: null,
          affix: "ām (ṣaṣṭhī bahuvacana)",
          morph: "gen. pl. neut.",
          karaka: "sambandha (subjective genitive: 'the senses' [withdrawal]')",
          glossaryKey: "indriya",
          translatable: false
        },
        {
          i: 4,
          iast: "pratyāhāraḥ",
          gloss: "withdrawal",
          parts: [
            { form: "prati-", gloss: "back, against" },
            { form: "ā-", gloss: "toward, in" },
            { form: "√hṛ", gloss: "to draw, carry" },
            { form: "-a", gloss: "(action noun: 'a drawing back')" }
          ],
          stem: "pratyāhāra",
          root: "√hṛ (hṛñ haraṇe, bhvādi, 1U, 'to carry, draw')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc.",
          karaka: "kartṛ (grammatical subject of the nominal sentence)",
          glossaryKey: "pratyahara",
          translatable: true
        }
      ],
      english: "{4:Withdrawal} is the {3:senses'} {0:disengagement from their own objects}, {2:as if} {1:conforming to the nature of the mind} itself."
    }
  ],

  // 2.59 — "Objects turn away from the abstinent embodied one, but the
  //         relish stays — until, seeing the Supreme, his relish too ends."
  "2.59": [
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "1.16",
      sanskrit: "tat paraṃ puruṣakhyāter guṇavaitṛṣṇyam ||",
      ourRendering: "That higher [dispassion] is the cessation of thirst even for the guṇas, which comes from the discernment of the puruṣa.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 1.16)",
      words: [
        {
          i: 0,
          iast: "tat",
          gloss: "that",
          parts: [
            { form: "tad", gloss: "that" }
          ],
          stem: "tad",
          root: null,
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut. (demonstrative pronoun)",
          karaka: "kartṛ (subject; refers to vairāgya from the prior sūtra)",
          translatable: true
        },
        {
          i: 1,
          iast: "param",
          gloss: "the higher",
          parts: [
            { form: "para", gloss: "highest, supreme, further" }
          ],
          stem: "para",
          root: null,
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut.",
          karaka: "kartṛ (attribute of tat)",
          translatable: true
        },
        {
          i: 2,
          iast: "puruṣakhyāteḥ",
          gloss: "from the discernment of the puruṣa",
          parts: [
            { form: "puruṣa", gloss: "the spirit, the conscious self, the witnessing person" },
            { form: "khyāti", gloss: "discernment, clear vision, discriminative insight (√khyā + ktin)" }
          ],
          stem: "puruṣa-khyāti",
          root: "√khyā (khyā prakathane, adādi, 2P, 'to make known, perceive')",
          affix: "ṅasi (pañcamī ekavacana)",
          morph: "abl. sg. fem.",
          karaka: "apādāna (source/cause: 'arising from the discernment')",
          compound: { type: "tatpuruṣa", vigraha: "puruṣasya khyātiḥ", members: ["puruṣa", "khyāti"] },
          glossaryKey: "purusa",
          translatable: true
        },
        {
          i: 3,
          iast: "guṇavaitṛṣṇyam",
          gloss: "the cessation of thirst even for the guṇas",
          parts: [
            { form: "guṇa", gloss: "strand, constituent, quality; the constituent strand of prakṛti" },
            { form: "vi-", gloss: "away from, free of" },
            { form: "tṛṣṇā", gloss: "thirst, craving, longing, eager desire" },
            { form: "-ya", gloss: "(abstract-noun taddhita, with vṛddhi: 'the state of being free of')" }
          ],
          stem: "guṇa-vaitṛṣṇya",
          root: "√tṛṣ (tṛṣa pipāsāyām, divādi, 4P, 'to be thirsty')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut.",
          karaka: "kartṛ (predicate of the nominal sentence)",
          compound: { type: "tatpuruṣa", vigraha: "guṇeṣu vaitṛṣṇyam", members: ["guṇa", "vaitṛṣṇya"] },
          glossaryKey: "guna",
          translatable: true
        }
      ],
      english: "{0:That} {1:higher} dispassion is {3:the cessation of thirst even for the guṇas}, {2:which comes from the discernment of the puruṣa}."
    }
  ],

  // 2.61 — "Restraining all of them, let him sit absorbed, intent on Me;
  //         for one whose senses are mastered, wisdom stands firm."
  "2.61": [
    {
      school: "Buddhism (Theravāda)",
      thinker: "Dhammapada",
      work: "Dhammapada, Arahantavagga",
      locus: "94",
      sanskrit: "yassindriyāni samathaṅgatāni, assā yathā sārathinā sudantā; pahīnamānassa anāsavassa, devāpi tassa pihayanti tādino.",
      ourRendering: "Whose senses have come to calm, like horses well-tamed by the charioteer — with conceit abandoned, free of taints — even the gods envy such a one, the one who is Such.",
      source: "data/sources/pali/suttacentral/dhammapada_arahantavagga_90-99_root-pli-ms.json (dhp 94)",
      words: [
        {
          i: 0,
          iast: "yassa",
          gloss: "whose",
          parts: [
            { form: "ya", gloss: "who, which (Skt yad)" }
          ],
          stem: "ya",
          root: null,
          affix: "-ssa (gen. sg. masc.; Skt yasya)",
          morph: "Pali gen. sg. masc. (relative pronoun)",
          translatable: true
        },
        {
          i: 1,
          iast: "indriyāni",
          gloss: "senses",
          parts: [
            { form: "indriya", gloss: "sense-faculty, sense-organ, power (Skt indriya)" }
          ],
          stem: "indriya",
          root: null,
          affix: "-āni (nom. pl. neut.; Skt indriyāṇi)",
          morph: "Pali nom. pl. neut.",
          glossaryKey: "indriya",
          translatable: false
        },
        {
          i: 2,
          iast: "samathaṅgatāni",
          gloss: "have come to calm",
          parts: [
            { form: "samatha", gloss: "calm, tranquillity (Skt śamatha)" },
            { form: "gata", gloss: "gone, come to (√gam + ta; Skt gata)" }
          ],
          stem: "samatha-gata",
          root: "√gam (Pali; Skt √gam, bhvādi, 1P, 'to go')",
          affix: "-āni (nom. pl. neut.; Skt -gatāni)",
          morph: "Pali nom. pl. neut. (past participle)",
          compound: { type: "tatpuruṣa", vigraha: "samathaṃ gatāni (Skt: śamathaṃ gatāni)", members: ["samatha", "gata"] },
          translatable: true
        },
        {
          i: 3,
          iast: "assā",
          gloss: "horses",
          parts: [
            { form: "assa", gloss: "horse (Skt aśva)" }
          ],
          stem: "assa",
          root: null,
          affix: "-ā (nom. pl. masc.; Skt aśvāḥ)",
          morph: "Pali nom. pl. masc.",
          translatable: true
        },
        {
          i: 4,
          iast: "yathā",
          gloss: "as, like",
          parts: [
            { form: "yathā", gloss: "as, just as (Skt yathā)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (comparative)",
          translatable: true
        },
        {
          i: 5,
          iast: "sārathinā",
          gloss: "by the charioteer",
          parts: [
            { form: "sārathi", gloss: "charioteer (Skt sārathi)" }
          ],
          stem: "sārathi",
          root: null,
          affix: "-nā (instr. sg. masc.; Skt sārathinā)",
          morph: "Pali instr. sg. masc. (agent of the taming)",
          translatable: true
        },
        {
          i: 6,
          iast: "sudantā",
          gloss: "well-tamed",
          parts: [
            { form: "su-", gloss: "well, thoroughly (Skt su-)" },
            { form: "danta", gloss: "tamed, subdued, restrained, disciplined (√dam + ta; Skt dānta)" }
          ],
          stem: "su-danta",
          root: "√dam (Pali; Skt √dam, divādi, 4P, 'to tame, subdue')",
          affix: "-ā (nom. pl. masc.; Skt -dāntāḥ)",
          morph: "Pali nom. pl. masc. (past participle)",
          translatable: true
        },
        {
          i: 7,
          iast: "pahīnamānassa",
          gloss: "with conceit abandoned",
          parts: [
            { form: "pahīna", gloss: "abandoned, given up, relinquished (pra + √hā + ta/na; Skt prahīṇa)" },
            { form: "māna", gloss: "conceit, pride, self-regard (Skt māna)" }
          ],
          stem: "pahīna-māna",
          root: "√hā (Pali; Skt √hā, juhotyādi, 3P, 'to abandon')",
          affix: "-ssa (gen. sg. masc.; Skt -asya)",
          morph: "Pali gen. sg. masc. (bahubbīhi)",
          compound: { type: "bahuvrīhi", vigraha: "pahīno māno yassa so (Skt: prahīṇo māno yasya saḥ)", members: ["pahīna", "māna"] },
          translatable: true
        },
        {
          i: 8,
          iast: "anāsavassa",
          gloss: "free of taints",
          parts: [
            { form: "an-", gloss: "without (Skt an-)" },
            { form: "āsava", gloss: "taint, influx, canker (ā + √sru; Skt āsrava)" }
          ],
          stem: "an-āsava",
          root: "√sru (Pali √su; Skt √sru, bhvādi, 1P, 'to flow')",
          affix: "-ssa (gen. sg. masc.; Skt -asya)",
          morph: "Pali gen. sg. masc. (bahubbīhi)",
          compound: { type: "bahuvrīhi", vigraha: "natthi āsavā yassa so (Skt: na santi āsravā yasya saḥ)", members: ["an", "āsava"] },
          translatable: true
        },
        {
          i: 9,
          iast: "devā",
          gloss: "the gods",
          parts: [
            { form: "deva", gloss: "god, deity (Skt deva)" }
          ],
          stem: "deva",
          root: null,
          affix: "-ā (nom. pl. masc.; Skt devāḥ)",
          morph: "Pali nom. pl. masc.",
          translatable: true
        },
        {
          i: 10,
          iast: "pi",
          gloss: "even",
          parts: [
            { form: "pi", gloss: "even, also (Skt api)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (Skt api)",
          translatable: true
        },
        {
          i: 11,
          iast: "tassa",
          gloss: "such a one",
          parts: [
            { form: "ta", gloss: "that, him (Skt tad)" }
          ],
          stem: "ta",
          root: null,
          affix: "-ssa (gen./dat. sg. masc.; Skt tasya)",
          morph: "Pali gen./dat. sg. masc. (object of pihayanti, which governs the dative)",
          translatable: true
        },
        {
          i: 12,
          iast: "pihayanti",
          gloss: "envy, long for",
          parts: [
            { form: "√pih", gloss: "to envy, yearn for (Skt √spṛh, desiderative-like)" },
            { form: "-anti", gloss: "(present, 3rd pl.)" }
          ],
          stem: null,
          root: "√pih (Pali; Skt √spṛh, curādi, 10P, 'to long for, envy')",
          affix: "-anti (Pali present, 3rd pl.)",
          morph: "Pali pres. 3rd pl. (governs the dative/genitive)",
          translatable: true
        },
        {
          i: 13,
          iast: "tādino",
          gloss: "the one who is Such",
          parts: [
            { form: "tādin", gloss: "of such a kind, the Such (Skt tādin)" }
          ],
          stem: "tādin",
          root: null,
          affix: "-no (gen./dat. sg., -in stem; Skt tādinaḥ)",
          morph: "Pali gen./dat. sg. masc. (in apposition to tassa)",
          translatable: true
        }
      ],
      english: "{0:Whose} {1:senses} {2:have come to calm}, {4:like} {3:horses} {6:well-tamed} {5:by the charioteer} — {7:with conceit abandoned}, {8:free of taints} — {9:the gods} {10:even} {12:envy} {11:such a one}, {13:the one who is Such}."
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "2.55",
      sanskrit: "tataḥ paramā vaśyatendriyāṇām ||",
      ourRendering: "From that [withdrawal] comes the supreme mastery of the senses.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 2.55)",
      words: [
        {
          i: 0,
          iast: "tataḥ",
          gloss: "from that",
          parts: [
            { form: "tad", gloss: "that" },
            { form: "-tas", gloss: "(ablatival taddhita: 'from')" }
          ],
          stem: "tad",
          root: null,
          affix: "tasil (taddhita, ablative sense)",
          morph: "indeclinable (ablative force): 'from that [withdrawal]'",
          karaka: "apādāna (source: 'from that')",
          translatable: true
        },
        {
          i: 1,
          iast: "paramā",
          gloss: "supreme",
          parts: [
            { form: "parama", gloss: "highest, supreme" }
          ],
          stem: "parama",
          root: null,
          affix: "ṭāp + su (prathamā ekavacana, strī)",
          morph: "nom. sg. fem.",
          karaka: "kartṛ (attribute of vaśyatā)",
          translatable: true
        },
        {
          i: 2,
          iast: "vaśyatā",
          gloss: "mastery, subjugation",
          parts: [
            { form: "vaśya", gloss: "to be controlled, subject to will, governable (√vaś + ṇyat)" },
            { form: "-tā", gloss: "(abstract-noun taddhita: 'the state of')" }
          ],
          stem: "vaśya-tā",
          root: "√vaś (vaśa kāntau, adādi, 2P, 'to will, command')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. fem.",
          karaka: "kartṛ (grammatical subject of the nominal sentence)",
          translatable: true
        },
        {
          i: 3,
          iast: "indriyāṇām",
          gloss: "of the senses",
          parts: [
            { form: "indriya", gloss: "sense-faculty, sense-organ, power" }
          ],
          stem: "indriya",
          root: null,
          affix: "ām (ṣaṣṭhī bahuvacana)",
          morph: "gen. pl. neut.",
          karaka: "sambandha (objective genitive: 'mastery over the senses')",
          glossaryKey: "indriya",
          translatable: false
        }
      ],
      english: "{0:From that} withdrawal comes the {1:supreme} {2:mastery} {3:of the senses}."
    }
  ],

  // 2.70 — "As waters enter the sea, brimful yet unmoved in its bed, so the
  //         one whom all desires enter attains peace — not the desire-driven."
  "2.70": [
    {
      school: "Buddhism (Theravāda)",
      thinker: "Dhammapada",
      work: "Dhammapada, Arahantavagga",
      locus: "96",
      sanskrit: "santaṃ tassa manaṃ hoti, santā vācā ca kamma ca; sammadaññāvimuttassa, upasantassa tādino.",
      ourRendering: "Calm is his mind, calm his speech, and calm his action — for the one freed by right knowledge, at peace, the one who is Such.",
      source: "data/sources/pali/suttacentral/dhammapada_arahantavagga_90-99_root-pli-ms.json (dhp 96)",
      words: [
        {
          i: 0,
          iast: "santaṃ",
          gloss: "calm",
          parts: [
            { form: "santa", gloss: "calmed, stilled, at peace (√sam + ta; Skt śānta)" }
          ],
          stem: "santa",
          root: "√sam (Pali; Skt √śam, divādi, 4P, 'to be quiet, cease')",
          affix: "-ṃ (nom. sg. neut.; Skt śāntam)",
          morph: "Pali nom. sg. neut. (past participle, predicative)",
          translatable: true
        },
        {
          i: 1,
          iast: "tassa",
          gloss: "his",
          parts: [
            { form: "ta", gloss: "that, his (Skt tad)" }
          ],
          stem: "ta",
          root: null,
          affix: "-ssa (gen. sg. masc.; Skt tasya)",
          morph: "Pali gen. sg. masc. (possessive)",
          translatable: true
        },
        {
          i: 2,
          iast: "manaṃ",
          gloss: "mind",
          parts: [
            { form: "mana", gloss: "mind; the inner organ of thought (Skt manas)" }
          ],
          stem: "mana",
          root: null,
          affix: "-ṃ (nom. sg. neut.; Skt manaḥ)",
          morph: "Pali nom. sg. neut.",
          glossaryKey: "manas",
          translatable: true
        },
        {
          i: 3,
          iast: "hoti",
          gloss: "is",
          parts: [
            { form: "√bhū", gloss: "to be (Skt √bhū; Pali ho-)" },
            { form: "-ti", gloss: "(present, 3rd sg.)" }
          ],
          stem: null,
          root: "√bhū (Pali ho-; Skt √bhū, bhvādi, 1P, 'to be')",
          affix: "-ti (Pali present, 3rd sg.)",
          morph: "Pali pres. 3rd sg. (Skt bhavati)",
          translatable: true
        },
        {
          i: 4,
          iast: "santā",
          gloss: "calm",
          parts: [
            { form: "santa", gloss: "calmed, stilled (√sam + ta; Skt śānta)" }
          ],
          stem: "santa",
          root: "√sam (Pali; Skt √śam, divādi, 4P)",
          affix: "-ā (nom. sg. fem.; Skt śāntā)",
          morph: "Pali nom. sg. fem. (agreeing with vācā)",
          translatable: true
        },
        {
          i: 5,
          iast: "vācā",
          gloss: "speech",
          parts: [
            { form: "vācā", gloss: "speech, word (Skt vāc)" }
          ],
          stem: "vācā",
          root: null,
          affix: "-ā (nom. sg. fem.; Skt vāk)",
          morph: "Pali nom. sg. fem.",
          translatable: true
        },
        {
          i: 6,
          iast: "ca",
          gloss: "and",
          parts: [
            { form: "ca", gloss: "and (Skt ca)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (conjunction)",
          translatable: true
        },
        {
          i: 7,
          iast: "kamma",
          gloss: "action",
          parts: [
            { form: "kamma", gloss: "action, deed, work (Skt karman)" }
          ],
          stem: "kamma",
          root: null,
          affix: "-(aṃ) (nom. sg. neut.; Skt karma)",
          morph: "Pali nom. sg. neut.",
          glossaryKey: "karma",
          translatable: false
        },
        {
          i: 8,
          iast: "ca",
          gloss: "and",
          parts: [
            { form: "ca", gloss: "and (Skt ca)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Pali indeclinable (conjunction)",
          translatable: true
        },
        {
          i: 9,
          iast: "sammadaññāvimuttassa",
          gloss: "for the one freed by right knowledge",
          parts: [
            { form: "sammad", gloss: "rightly, perfectly, fully (sammā before vowel; Skt samyak)" },
            { form: "aññā", gloss: "final knowledge, perfect knowing, gnosis (ā + √ñā; Skt ājñā)" },
            { form: "vimutta", gloss: "released, liberated, set free, delivered (vi + √muc + ta; Skt vimukta)" }
          ],
          stem: "sammadaññā-vimutta",
          root: "√muc (Pali; Skt √muc, tudādi, 6U, 'to release')",
          affix: "-ssa (gen./dat. sg. masc.; Skt -asya)",
          morph: "Pali gen./dat. sg. masc. (past participle)",
          compound: { type: "tatpuruṣa", vigraha: "sammā aññāya vimutto (Skt: samyag-ājñayā vimuktaḥ)", members: ["sammā", "aññā", "vimutta"] },
          translatable: true
        },
        {
          i: 10,
          iast: "upasantassa",
          gloss: "at peace",
          parts: [
            { form: "upa-", gloss: "thoroughly (Skt upa-)" },
            { form: "santa", gloss: "calmed, stilled (√sam + ta; Skt śānta)" }
          ],
          stem: "upa-santa",
          root: "√sam (Pali; Skt √śam, divādi, 4P)",
          affix: "-ssa (gen./dat. sg. masc.; Skt -asya)",
          morph: "Pali gen./dat. sg. masc. (past participle; Skt upaśāntasya)",
          translatable: true
        },
        {
          i: 11,
          iast: "tādino",
          gloss: "the one who is Such",
          parts: [
            { form: "tādin", gloss: "of such a kind, the Such (Skt tādin)" }
          ],
          stem: "tādin",
          root: null,
          affix: "-no (gen./dat. sg., -in stem; Skt tādinaḥ)",
          morph: "Pali gen./dat. sg. masc. (in apposition)",
          translatable: true
        }
      ],
      english: "{0:Calm} {3:is} {1:his} {2:mind}, {4:calm} {1:his} {5:speech}, {6:and} {1:his} {7:action} {8:too} — {9:for the one freed by right knowledge}, {10:at peace}, {11:the one who is Such}."
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "1.33",
      sanskrit: "maitrīkaruṇāmuditopekṣāṇāṃ sukhaduḥkhapuṇyāpuṇyaviṣayāṇāṃ bhāvanātaś cittaprasādanam ||",
      ourRendering: "By cultivating friendliness, compassion, gladness and equanimity toward the happy, the suffering, the meritorious and the unmeritorious, the mind becomes serene.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 1.33)",
      words: [
        {
          i: 0,
          iast: "maitrīkaruṇāmuditopekṣāṇām",
          gloss: "of friendliness, compassion, gladness and equanimity",
          parts: [
            { form: "maitrī", gloss: "friendliness, loving-kindness, goodwill (from mitra 'friend')" },
            { form: "karuṇā", gloss: "compassion, pity, mercy" },
            { form: "muditā", gloss: "gladness, sympathetic joy, rejoicing" },
            { form: "upekṣā", gloss: "equanimity, even-mindedness, indifference (upa + √īkṣ)" }
          ],
          stem: "maitrī-karuṇā-muditā-upekṣā",
          root: null,
          affix: "ām (ṣaṣṭhī bahuvacana)",
          morph: "gen. pl. fem.",
          karaka: "sambandha (objective genitive governed by bhāvanā: 'cultivation of…')",
          compound: { type: "dvandva", vigraha: "maitrī ca karuṇā ca muditā ca upekṣā ca", members: ["maitrī", "karuṇā", "muditā", "upekṣā"] },
          translatable: true
        },
        {
          i: 1,
          iast: "sukhaduḥkhapuṇyāpuṇyaviṣayāṇām",
          gloss: "having as their objects the happy, the suffering, the meritorious and the unmeritorious",
          parts: [
            { form: "sukha", gloss: "pleasure, happiness, ease; the happy" },
            { form: "duḥkha", gloss: "sorrow, suffering, pain; the suffering" },
            { form: "puṇya", gloss: "merit, virtue, the meritorious" },
            { form: "a-", gloss: "non-, un-" },
            { form: "puṇya", gloss: "merit, virtue" },
            { form: "viṣaya", gloss: "object, sphere, domain, field" }
          ],
          stem: "sukha-duḥkha-puṇya-apuṇya-viṣaya",
          root: null,
          affix: "ām (ṣaṣṭhī bahuvacana)",
          morph: "gen. pl. fem. (agreeing with the four attitudes)",
          karaka: "sambandha (genitive: specifying the objects of each attitude)",
          compound: { type: "bahuvrīhi", vigraha: "sukha-duḥkha-puṇya-apuṇyāni viṣayāḥ yeṣāṃ tāni", members: ["sukha", "duḥkha", "puṇya", "apuṇya", "viṣaya"] },
          glossaryKey: "visaya",
          translatable: true
        },
        {
          i: 2,
          iast: "bhāvanātaḥ",
          gloss: "by cultivating",
          parts: [
            { form: "bhāvanā", gloss: "cultivation, repeated practice, meditative development (√bhū caus. + yuc)" },
            { form: "-tas", gloss: "(ablatival taddhita: 'from, by means of')" }
          ],
          stem: "bhāvanā",
          root: "√bhū (bhū sattāyām, bhvādi, 1P, 'to be, become'; causative bhāvayati)",
          affix: "tasil (taddhita, ablative/instrumental sense)",
          morph: "indeclinable (ablative force): 'through cultivation'",
          karaka: "karaṇa (means: 'by cultivation')",
          glossaryKey: "bhavana",
          translatable: true
        },
        {
          i: 3,
          iast: "cittaprasādanam",
          gloss: "the serenity of the mind",
          parts: [
            { form: "citta", gloss: "mind, mind-stuff, the thinking faculty, consciousness" },
            { form: "pra-", gloss: "forth, fully" },
            { form: "√sad", gloss: "to settle, to sink, to become clear, to grow calm" },
            { form: "-ana", gloss: "(action noun: 'a making serene')" }
          ],
          stem: "citta-prasādana",
          root: "√sad (ṣad ḷ viśaraṇagatyavasādaneṣu, bhvādi/tudādi, 'to settle, sink'; caus. 'to clarify')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut.",
          karaka: "kartṛ (grammatical subject of the nominal sentence; result)",
          compound: { type: "tatpuruṣa", vigraha: "cittasya prasādanam", members: ["citta", "prasādana"] },
          glossaryKey: "citta",
          translatable: true
        }
      ],
      english: "{2:By cultivating} the four — {0:friendliness, compassion, gladness and equanimity} — {1:toward the happy, the suffering, the meritorious and the unmeritorious}, comes {3:the serenity of the mind}."
    }
  ],

  // 2.71 — "The man who, abandoning all desires, moves about free of longing,
  //         without 'mine', without 'I' — he attains peace."
  "2.71": [
    {
      school: "Advaita Vedānta",
      thinker: "attributed to Śaṅkara",
      work: "Vivekacūḍāmaṇi",
      locus: "431",
      sanskrit: "vartamāne 'pi dehe 'smiñ chāyāvad anuvartini | ahantāmamatābhāvo jīvanmuktasya lakṣaṇam ||",
      ourRendering: "Even while this body persists, following him like a shadow, the absence of 'I' and 'mine' — that is the mark of one liberated while living.",
      source: "data/sources/sanskrit/vedanta/full_corpus/shankara_vivekacudamani_gretil.txt (v. 431)",
      words: [
        {
          i: 0,
          iast: "vartamāne",
          gloss: "persisting, continuing",
          parts: [
            { form: "√vṛt", gloss: "to turn, to continue, to persist, to exist" },
            { form: "-māna", gloss: "(present middle participle, śānac)" }
          ],
          stem: "vartamāna",
          root: "√vṛt (vṛtu vartane, bhvādi, 1A, 'to turn, be, continue')",
          affix: "ṅi (saptamī ekavacana)",
          morph: "loc. sg. masc. (present participle, locative absolute)",
          karaka: "adhikaraṇa (locative absolute: 'while it persists')",
          translatable: true
        },
        {
          i: 1,
          iast: "api",
          gloss: "even",
          parts: [
            { form: "api", gloss: "even, although" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "indeclinable (avyaya)",
          translatable: true
        },
        {
          i: 2,
          iast: "dehe",
          gloss: "the body",
          parts: [
            { form: "deha", gloss: "body (√dih 'to plaster, build up')" }
          ],
          stem: "deha",
          root: null,
          affix: "ṅi (saptamī ekavacana)",
          morph: "loc. sg. masc. (subject of the locative absolute)",
          karaka: "adhikaraṇa (locative absolute)",
          translatable: true
        },
        {
          i: 3,
          iast: "asmin",
          gloss: "this",
          parts: [
            { form: "idam", gloss: "this" }
          ],
          stem: "idam",
          root: null,
          affix: "ṅi (saptamī ekavacana)",
          morph: "loc. sg. masc. (demonstrative; agreeing with dehe)",
          karaka: "adhikaraṇa (with the locative absolute)",
          translatable: true
        },
        {
          i: 4,
          iast: "chāyāvat",
          gloss: "like a shadow",
          parts: [
            { form: "chāyā", gloss: "shadow, shade" },
            { form: "-vat", gloss: "(comparative taddhita: 'like, as')" }
          ],
          stem: "chāyā",
          root: null,
          affix: "vati (taddhita, 'in the manner of')",
          morph: "indeclinable adverb (vati-pratyaya): 'shadow-like'",
          translatable: true
        },
        {
          i: 5,
          iast: "anuvartini",
          gloss: "following after",
          parts: [
            { form: "anu-", gloss: "after, along, following" },
            { form: "√vṛt", gloss: "to turn, to follow, to attend, to accompany" },
            { form: "-in", gloss: "(possessive/agentive: 'one who follows', ṇini)" }
          ],
          stem: "anuvartin",
          root: "√vṛt (vṛtu vartane, bhvādi, 1A, 'to turn, follow')",
          affix: "ṅi (saptamī ekavacana)",
          morph: "loc. sg. masc. (agreeing with dehe)",
          karaka: "adhikaraṇa (with the locative absolute)",
          translatable: true
        },
        {
          i: 6,
          iast: "ahantāmamatābhāvaḥ",
          gloss: "the absence of 'I'-ness and 'mine'-ness",
          parts: [
            { form: "ahantā", gloss: "I-ness, the sense of 'I', egoity (aham + tā)" },
            { form: "mamatā", gloss: "mine-ness, the sense of 'mine', possessiveness (mama + tā)" },
            { form: "abhāva", gloss: "absence, non-existence, want (a + bhāva)" }
          ],
          stem: "ahantā-mamatā-abhāva",
          root: null,
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc.",
          karaka: "kartṛ (grammatical subject of the nominal sentence)",
          compound: { type: "tatpuruṣa", vigraha: "ahantāyāḥ ca mamatāyāḥ ca abhāvaḥ", members: ["ahantā", "mamatā", "abhāva"] },
          glossaryKey: "ahankara",
          translatable: true
        },
        {
          i: 7,
          iast: "jīvanmuktasya",
          gloss: "of one liberated while living",
          parts: [
            { form: "jīvat", gloss: "living, alive, while living (√jīv + śatṛ)" },
            { form: "mukta", gloss: "liberated, released, freed, set loose (√muc + kta)" }
          ],
          stem: "jīvan-mukta",
          root: "√muc (muca mocane, tudādi, 6U, 'to release, free')",
          affix: "ṅas (ṣaṣṭhī ekavacana)",
          morph: "gen. sg. masc.",
          karaka: "sambandha (possessive genitive: 'mark of…')",
          compound: { type: "tatpuruṣa", vigraha: "jīvan muktaḥ", members: ["jīvat", "mukta"] },
          glossaryKey: "jivanmukta",
          translatable: true
        },
        {
          i: 8,
          iast: "lakṣaṇam",
          gloss: "the mark",
          parts: [
            { form: "√lakṣ", gloss: "to mark, to characterize, to define, to denote" },
            { form: "-ana", gloss: "(action/instrument noun: 'characteristic')" }
          ],
          stem: "lakṣaṇa",
          root: "√lakṣ (lakṣa darśanāṅkanayoḥ, curādi, 10U, 'to mark, observe')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut.",
          karaka: "kartṛ (predicate nominative)",
          glossaryKey: "laksana",
          translatable: true
        }
      ],
      english: "{1:Even} {0:while} {3:this} {2:body} {0:persists}, {5:following him} {4:like a shadow}, {6:the absence of 'I' and 'mine'} — that is {8:the mark} {7:of one liberated while living}."
    },
    {
      school: "Jainism",
      thinker: "Uttarādhyayana",
      work: "Uttarajjhayā (Uttarādhyayana-sūtra), ch. 32 Pamāyaṭhāṇa",
      locus: "32.99",
      sanskrit: "bhāve viratto maṇuo visogo | eeṇa dukkhohaparaṃpareṇa | na lippaī bhavamajjhe vi santo | jaleṇa vā pokkhariṇīpalāsaṃ ||",
      ourRendering: "The man detached from objects, free of sorrow, is not stained by this succession of floods of suffering — though present in the very midst of existence — just as a lotus-pond's leaf is not stained by water.",
      source: "data/sources/prakrit/jaina/uttarajjhaya_gretil_plaintext.txt (Uttar 32.99)",
      words: [
        {
          i: 0,
          iast: "bhāve",
          gloss: "from objects/things",
          parts: [
            { form: "bhāva", gloss: "existing thing, object, state of being, mental object (Skt bhāva)" }
          ],
          stem: "bhāva",
          root: null,
          affix: "-e (loc. sg. masc.; Skt bhāve)",
          morph: "Prakrit loc. sg. masc. ('with respect to objects'; complement of viratta)",
          glossaryKey: "bhava",
          translatable: true
        },
        {
          i: 1,
          iast: "viratto",
          gloss: "detached",
          parts: [
            { form: "vi-", gloss: "away from, free of (Skt vi-)" },
            { form: "ratta", gloss: "attached, colored, dyed, impassioned (√raj + ta; Skt rakta)" }
          ],
          stem: "vi-ratta",
          root: "√raj (Prakrit; Skt √rañj, bhvādi, 1U, 'to be dyed, attached')",
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Prakrit nom. sg. masc. (past participle; Skt virakta)",
          translatable: true
        },
        {
          i: 2,
          iast: "maṇuo",
          gloss: "the man",
          parts: [
            { form: "maṇua", gloss: "man, human (Skt manuja)" }
          ],
          stem: "maṇua",
          root: null,
          affix: "-o (nom. sg. masc.; Skt manujaḥ)",
          morph: "Prakrit nom. sg. masc.",
          translatable: true
        },
        {
          i: 3,
          iast: "visogo",
          gloss: "free of sorrow",
          parts: [
            { form: "vi-", gloss: "without, free of (Skt vi-)" },
            { form: "soga", gloss: "sorrow, grief, lamentation (Skt śoka)" }
          ],
          stem: "vi-soga",
          root: null,
          affix: "-o (nom. sg. masc.; Skt -aḥ)",
          morph: "Prakrit nom. sg. masc. (bahuvrīhi; Skt viśokaḥ)",
          compound: { type: "bahuvrīhi", vigraha: "vigao sogo jassa so (Skt: vigataḥ śoko yasya saḥ)", members: ["vi", "soga"] },
          translatable: true
        },
        {
          i: 4,
          iast: "eeṇa",
          gloss: "by this",
          parts: [
            { form: "ea", gloss: "this (Skt etad)" }
          ],
          stem: "ea",
          root: null,
          affix: "-eṇa (instr. sg. masc.; Skt etena)",
          morph: "Prakrit instr. sg. masc. (demonstrative; Skt etena)",
          translatable: true
        },
        {
          i: 5,
          iast: "dukkhohaparaṃpareṇa",
          gloss: "succession of floods of suffering",
          parts: [
            { form: "dukkha", gloss: "suffering, sorrow, pain, distress (Skt duḥkha)" },
            { form: "oha", gloss: "flood, stream (Skt ogha)" },
            { form: "paraṃparā", gloss: "succession, unbroken series (Skt paramparā)" }
          ],
          stem: "dukkha-oha-paraṃparā",
          root: null,
          affix: "-eṇa (instr. sg. fem.; Skt -ayā)",
          morph: "Prakrit instr. sg. (Skt duḥkhaughaparamparayā)",
          compound: { type: "tatpuruṣa", vigraha: "dukkhāṇaṃ ohāṇaṃ paraṃparā (Skt: duḥkhānām oghānāṃ paramparā)", members: ["dukkha", "oha", "paraṃparā"] },
          glossaryKey: "duhkha",
          translatable: true
        },
        {
          i: 6,
          iast: "na",
          gloss: "not",
          parts: [
            { form: "na", gloss: "not (Skt na)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit indeclinable (negation)",
          translatable: true
        },
        {
          i: 7,
          iast: "lippaī",
          gloss: "is stained, smeared",
          parts: [
            { form: "√lip", gloss: "to smear, stain (Skt √lip)" },
            { form: "-ppa-ī", gloss: "(passive present, 3rd sg.)" }
          ],
          stem: null,
          root: "√lip (Prakrit; Skt √lip, tudādi, 6U, 'to smear, stain')",
          affix: "-ī (Prakrit passive present, 3rd sg.; Skt lipyate)",
          morph: "Prakrit pass. pres. 3rd sg. (Skt lipyate)",
          translatable: true
        },
        {
          i: 8,
          iast: "bhavamajjhe",
          gloss: "in the midst of existence",
          parts: [
            { form: "bhava", gloss: "existence, becoming, worldly being (Skt bhava)" },
            { form: "majjha", gloss: "middle, midst, center (Skt madhya)" }
          ],
          stem: "bhava-majjha",
          root: null,
          affix: "-e (loc. sg. masc./neut.; Skt madhye)",
          morph: "Prakrit loc. sg. (Skt bhavamadhye)",
          compound: { type: "tatpuruṣa", vigraha: "bhavassa majjhe (Skt: bhavasya madhye)", members: ["bhava", "majjha"] },
          glossaryKey: "samsara",
          translatable: true
        },
        {
          i: 9,
          iast: "vi",
          gloss: "even",
          parts: [
            { form: "vi", gloss: "even, also (Skt api)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit indeclinable (Skt api; emphatic)",
          translatable: true
        },
        {
          i: 10,
          iast: "santo",
          gloss: "being, present",
          parts: [
            { form: "√as", gloss: "to be (Skt √as)" },
            { form: "-nta", gloss: "(present participle; Skt sat)" }
          ],
          stem: "santa",
          root: "√as (Prakrit; Skt √as, adādi, 2P, 'to be')",
          affix: "-o (nom. sg. masc.; Skt san)",
          morph: "Prakrit pres. participle nom. sg. masc. (Skt san)",
          translatable: true
        },
        {
          i: 11,
          iast: "jaleṇa",
          gloss: "by water",
          parts: [
            { form: "jala", gloss: "water (Skt jala)" }
          ],
          stem: "jala",
          root: null,
          affix: "-eṇa (instr. sg. neut.; Skt jalena)",
          morph: "Prakrit instr. sg. neut.",
          translatable: true
        },
        {
          i: 12,
          iast: "vā",
          gloss: "just as",
          parts: [
            { form: "vā", gloss: "as, like (here comparative; Skt iva/vā)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "Prakrit indeclinable (comparative particle)",
          translatable: true
        },
        {
          i: 13,
          iast: "pokkhariṇīpalāsaṃ",
          gloss: "a lotus-pond's leaf",
          parts: [
            { form: "pokkhariṇī", gloss: "lotus-pond (Skt puṣkariṇī)" },
            { form: "palāsa", gloss: "leaf, foliage (Skt palāśa)" }
          ],
          stem: "pokkhariṇī-palāsa",
          root: null,
          affix: "-ṃ (nom./acc. sg. neut.; Skt palāśam)",
          morph: "Prakrit nom. sg. neut. (subject of the elliptical comparison)",
          compound: { type: "tatpuruṣa", vigraha: "pokkhariṇīe palāsaṃ (Skt: puṣkariṇyāḥ palāśam)", members: ["pokkhariṇī", "palāsa"] },
          translatable: true
        }
      ],
      english: "{2:The man} {1:detached} {0:from objects}, {3:free of sorrow}, {6:is not} {7:stained} {4:by this} {5:succession of floods of suffering} — {9:even} {10:though present} {8:in the very midst of existence} — {12:just as} a {13:lotus-pond's leaf} is not stained {11:by water}."
    }
  ],

  // 2.72 — "This is the state grounded in Brahman, Pārtha; reaching it one is
  //         not deluded. Standing in it even at the last hour, one attains
  //         the going-out into Brahman (brahma-nirvāṇa)."
  "2.72": [
    {
      school: "Trika (Pratyabhijñā)",
      thinker: "Kṣemarāja",
      work: "Pratyabhijñāhṛdaya",
      locus: "sūtra 16",
      sanskrit: "cidānandalābhe dehādiṣu cetyamāneṣv api cidaikātmyapratipattidārḍhyaṃ jīvanmuktiḥ ||",
      ourRendering: "When the bliss of consciousness is attained, the firm conviction of oneness with consciousness — even while body and the rest are still being experienced — is liberation-while-living.",
      source: "data/sources/sanskrit/kashmir_shaiva/ksemaraja_pratyabhijna_hrdayam.txt (PH sūtra 16)",
      words: [
        {
          i: 0,
          iast: "cidānandalābhe",
          gloss: "on the attainment of the bliss of consciousness",
          parts: [
            { form: "cit", gloss: "consciousness, pure awareness, sentience" },
            { form: "ānanda", gloss: "bliss, joy, felicity, beatitude" },
            { form: "lābha", gloss: "attainment, gaining, obtaining, acquisition (√labh + ghañ)" }
          ],
          stem: "cit-ānanda-lābha",
          root: "√labh (ḍulabhaṣ prāptau, bhvādi, 1A, 'to obtain')",
          affix: "ṅi (saptamī ekavacana)",
          morph: "loc. sg. masc.",
          karaka: "adhikaraṇa (locative absolute: 'when… is attained')",
          compound: { type: "tatpuruṣa", vigraha: "cidānandasya lābhaḥ (cit ca ānandaḥ ca, tasya lābhaḥ)", members: ["cit", "ānanda", "lābha"] },
          glossaryKey: "ananda",
          translatable: true
        },
        {
          i: 1,
          iast: "dehādiṣu",
          gloss: "in the body and the rest",
          parts: [
            { form: "deha", gloss: "body" },
            { form: "ādi", gloss: "beginning, 'and the rest', et cetera" }
          ],
          stem: "deha-ādi",
          root: null,
          affix: "sup (saptamī bahuvacana)",
          morph: "loc. pl. masc.",
          karaka: "adhikaraṇa (with the locative absolute cetyamāneṣu: 'while body etc. …')",
          compound: { type: "bahuvrīhi", vigraha: "dehaḥ ādiḥ yeṣāṃ tāni", members: ["deha", "ādi"] },
          translatable: true
        },
        {
          i: 2,
          iast: "cetyamāneṣu",
          gloss: "being experienced/objectified",
          parts: [
            { form: "√cit", gloss: "to perceive, be aware of" },
            { form: "-ya-māna", gloss: "(passive present participle: 'being made an object')" }
          ],
          stem: "cetyamāna",
          root: "√cit (cita saṃjñāne, bhvādi, 1P, 'to perceive, be conscious of')",
          affix: "sup (saptamī bahuvacana)",
          morph: "loc. pl. masc. (passive present participle, locative absolute)",
          karaka: "adhikaraṇa (locative absolute: 'while they are being experienced')",
          translatable: true
        },
        {
          i: 3,
          iast: "api",
          gloss: "even",
          parts: [
            { form: "api", gloss: "even, although" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "indeclinable (avyaya): concessive ('even though')",
          translatable: true
        },
        {
          i: 4,
          iast: "cidaikātmyapratipattidārḍhyam",
          gloss: "the firmness of the realization of oneness with consciousness",
          parts: [
            { form: "cit", gloss: "consciousness, pure awareness, sentience" },
            { form: "aikātmya", gloss: "oneness, identity of self, sameness of essence (eka-ātman + ṣyañ, vṛddhi)" },
            { form: "pratipatti", gloss: "realization, ascertainment, conviction (prati + √pad + ktin)" },
            { form: "dārḍhya", gloss: "firmness, steadfastness, solidity (dṛḍha + ṣyañ)" }
          ],
          stem: "cit-aikātmya-pratipatti-dārḍhya",
          root: "√pad (pada gatau, divādi, 4A, 'to go, attain')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut.",
          karaka: "kartṛ (grammatical subject of the nominal sentence)",
          compound: { type: "tatpuruṣa", vigraha: "cidaikātmyasya pratipatteḥ dārḍhyam", members: ["cit", "aikātmya", "pratipatti", "dārḍhya"] },
          glossaryKey: "abheda",
          translatable: true
        },
        {
          i: 5,
          iast: "jīvanmuktiḥ",
          gloss: "liberation-while-living",
          parts: [
            { form: "jīvat", gloss: "living (√jīv + śatṛ)" },
            { form: "mukti", gloss: "liberation, release, freedom, deliverance (√muc + ktin)" }
          ],
          stem: "jīvan-mukti",
          root: "√muc (muca mocane, tudādi, 6U, 'to release, free')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. fem.",
          karaka: "kartṛ (predicate of the nominal sentence)",
          compound: { type: "tatpuruṣa", vigraha: "jīvataḥ muktiḥ (jīvan eva muktiḥ)", members: ["jīvat", "mukti"] },
          glossaryKey: "jivanmukta",
          translatable: true
        }
      ],
      english: "{0:When the bliss of consciousness is attained}, {4:the firm conviction of oneness with consciousness} — {3:even} while {1:the body and the rest} are {2:still being experienced} — is {5:liberation-while-living}."
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "4.34",
      sanskrit: "puruṣārthaśūnyānāṃ guṇānāṃ pratiprasavaḥ kaivalyaṃ svarūpapratiṣṭhā vā citiśaktir iti ||",
      ourRendering: "Aloneness (kaivalya) is the return of the guṇas, now empty of any purpose for the puruṣa, to their source — or, the power of pure consciousness standing firm in its own nature.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 4.34)",
      words: [
        {
          i: 0,
          iast: "puruṣārthaśūnyānām",
          gloss: "empty of any purpose for the puruṣa",
          parts: [
            { form: "puruṣa", gloss: "the spirit, the conscious self, the witnessing person" },
            { form: "artha", gloss: "purpose, goal, aim, object" },
            { form: "śūnya", gloss: "empty, void, devoid of, without" }
          ],
          stem: "puruṣārtha-śūnya",
          root: null,
          affix: "ām (ṣaṣṭhī bahuvacana)",
          morph: "gen. pl. masc. (agreeing with guṇānām)",
          karaka: "sambandha (attributive genitive of guṇānām)",
          compound: { type: "tatpuruṣa", vigraha: "puruṣārthena śūnyāḥ (puruṣasya arthaḥ puruṣārthaḥ, tena śūnyāḥ)", members: ["puruṣa", "artha", "śūnya"] },
          glossaryKey: "purusartha",
          translatable: true
        },
        {
          i: 1,
          iast: "guṇānām",
          gloss: "of the guṇas",
          parts: [
            { form: "guṇa", gloss: "strand, constituent, quality; the constituent strand of prakṛti" }
          ],
          stem: "guṇa",
          root: null,
          affix: "ām (ṣaṣṭhī bahuvacana)",
          morph: "gen. pl. masc.",
          karaka: "sambandha (subjective genitive: 'the guṇas' return')",
          glossaryKey: "guna",
          translatable: false
        },
        {
          i: 2,
          iast: "pratiprasavaḥ",
          gloss: "the return to the source, re-absorption",
          parts: [
            { form: "prati-", gloss: "back, in reverse" },
            { form: "pra-", gloss: "forth" },
            { form: "√sū", gloss: "to bring forth, generate" },
            { form: "-a", gloss: "(action noun: 'a counter-issuing', i.e. dissolution)" }
          ],
          stem: "pratiprasava",
          root: "√sū (ṣūṅ prāṇiprasave, divādi/adādi, 'to bring forth, generate')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. masc.",
          karaka: "kartṛ (grammatical subject of the first nominal clause)",
          translatable: true
        },
        {
          i: 3,
          iast: "kaivalyam",
          gloss: "aloneness",
          parts: [
            { form: "kevala", gloss: "alone, sole, isolated, pure, absolute" },
            { form: "-ya", gloss: "(abstract-noun taddhita, with vṛddhi: 'the state of being alone')" }
          ],
          stem: "kaivalya",
          root: null,
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. neut.",
          karaka: "kartṛ (predicate of the nominal sentence)",
          glossaryKey: "kaivalya",
          translatable: true
        },
        {
          i: 4,
          iast: "svarūpapratiṣṭhā",
          gloss: "standing firm in its own nature",
          parts: [
            { form: "svarūpa", gloss: "own-form, intrinsic nature, essential character" },
            { form: "prati-", gloss: "firmly" },
            { form: "√sthā", gloss: "to stand, to stay, to abide, to be established" },
            { form: "-ā", gloss: "(action noun: 'establishment', with strī -ā)" }
          ],
          stem: "svarūpa-pratiṣṭhā",
          root: "√sthā (ṣṭhā gatinivṛttau, bhvādi, 1P, 'to stand')",
          affix: "ṭāp + su (prathamā ekavacana, strī)",
          morph: "nom. sg. fem.",
          karaka: "kartṛ (predicate of the alternative clause)",
          compound: { type: "tatpuruṣa", vigraha: "svarūpe pratiṣṭhā", members: ["svarūpa", "pratiṣṭhā"] },
          glossaryKey: "svarupa",
          translatable: true
        },
        {
          i: 5,
          iast: "vā",
          gloss: "or",
          parts: [
            { form: "vā", gloss: "or (disjunctive particle)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "indeclinable (avyaya)",
          translatable: true
        },
        {
          i: 6,
          iast: "citiśaktiḥ",
          gloss: "the power of pure consciousness",
          parts: [
            { form: "citi", gloss: "pure consciousness, awareness, the power of awareness (√cit + ktin)" },
            { form: "śakti", gloss: "power, capacity, energy, potency" }
          ],
          stem: "citi-śakti",
          root: "√cit (cita saṃjñāne, bhvādi, 1P, 'to perceive, be conscious')",
          affix: "su (prathamā ekavacana)",
          morph: "nom. sg. fem.",
          karaka: "kartṛ (grammatical subject of the alternative clause)",
          compound: { type: "tatpuruṣa", vigraha: "citeḥ śaktiḥ", members: ["citi", "śakti"] },
          glossaryKey: "sakti",
          translatable: true
        },
        {
          i: 7,
          iast: "iti",
          gloss: "thus (close of the work)",
          parts: [
            { form: "iti", gloss: "thus, so (quotation/closing marker)" }
          ],
          stem: null,
          root: null,
          affix: null,
          morph: "indeclinable (avyaya): marks the end of the sūtra/text",
          translatable: true
        }
      ],
      english: "{3:Aloneness} is {2:the return to their source} {1:of the guṇas}, {0:now empty of any purpose for the puruṣa} — {5:or}, {6:the power of pure consciousness} {4:standing firm in its own nature} — {7:thus}."
    }
  ]

};
