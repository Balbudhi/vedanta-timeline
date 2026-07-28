/* =============================================================
   Bhagavad-Gītā 3.36–43 (close of adhyāya III).
   window.GITA3_VERSES — one object per verse.
   Schema + policy: docs/SANSKRIT_TRANSLATION_STANDARD.md (§3 data, §6
   Pāṇinian formalism, §7 faithful rendering, §8 preserve/translate).
   Site renders IAST only; words[].deva / devanagari are kept for local use.
   Interactive line = pada-pāṭha built from words[]; `iast` = saṃhitā.

   Mūla witnesses on disk, cross-checked against one another:
     data/sources/sanskrit/vedanta/shankara_gita_bhasya.txt  (IAST, BhG_3.36–43)
     data/sources/sanskrit/vedanta/ramanuja_gita_bhasya.txt  (IAST, BhG_3.36–43)
     data/sources/sanskrit/vedanta/madhva_gita_bhasya.txt    (Devanāgarī, 36–43)
   ============================================================= */

window.GITA3_VERSES = [
  {
    "locus": "3.36",
    "speaker": "arjuna",
    "meter": "anuṣṭubh",
    "devanagari": "अथ केन प्रयुक्तोऽयं पापं चरति पूरुषः।\nअनिच्छन्नपि वार्ष्णेय बलादिव नियोजितः॥",
    "iast": "atha kena prayukto 'yaṃ pāpaṃ carati pūruṣaḥ |\nanicchann api vārṣṇeya balād iva niyojitaḥ ||",
    "sense": "Arjuna asks the question the whole passage answers: what is the thing that drives a man into evil against his own will, as though someone had harnessed him to it?",
    "english": "{0:Now}, {9:O descendant of Vṛṣṇi} — {1:by what} is {3:this} {6:man} {2:impelled}, that {5:he engages in} {4:evil} {8:even though} {7:he does not wish it}, {11:as if} {12:harnessed to it} {10:by force}?",
    "words": [
      {
        "i": 0,
        "deva": "अथ",
        "iast": "atha",
        "gloss": "now, next; and so (opening a fresh question)",
        "stem": "atha",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable particle",
        "karaka": "— (discourse particle, no kāraka role)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "atha", "gloss": "now, next, thereupon; and so" }
        ],
        "note": "Madhva reads it as arthāntara — the marker of a new topic — and ties the question back to 3.34 (‘let him not come under the sway of those two’)."
      },
      {
        "i": 1,
        "deva": "केन",
        "iast": "kena",
        "gloss": "by what?; by whom?",
        "stem": "kim",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc. or neut.",
        "karaka": "hetu (instrumental of cause), and agent of the passive kta prayuktaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ka-", "gloss": "the interrogative stem: who?, what?" },
          { "form": "-ena", "gloss": "(instrumental singular: ‘by’)" }
        ],
        "note": "Masculine and neuter are formally identical here; Arjuna's question leaves it open whether the impelling thing is a who or a what."
      },
      {
        "i": 2,
        "deva": "प्रयुक्तः",
        "iast": "prayuktaḥ",
        "gloss": "set to work, harnessed, impelled",
        "stem": "prayukta",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach; to set to a task",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive part.",
        "karaka": "predicate of pūruṣaḥ; its agent is kena",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "pra-", "gloss": "forth, forward; onward into action" },
          { "form": "√yuj", "gloss": "to yoke, to harness, to set to a task" },
          { "form": "-ta", "gloss": "(past passive participle: ‘having been —ed’)" }
        ],
        "note": "Śaṅkara supplies the image the participle carries: ‘set to it as a servant is by a king’ (rājñeva bhṛtyaḥ)."
      },
      {
        "i": 3,
        "deva": "अयम्",
        "iast": "ayam",
        "gloss": "this (one here)",
        "stem": "idam",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute of pūruṣaḥ (kartṛ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "idam", "gloss": "this, this one here (proximate demonstrative)" }
        ],
        "sandhi": "prayukto 'yam ← prayuktaḥ + ayam (visarga → o before a-, and the a- elided as 'a)"
      },
      {
        "i": 4,
        "deva": "पापम्",
        "iast": "pāpam",
        "gloss": "evil, wrong; an evil deed",
        "stem": "pāpa",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of carati",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "pāpa", "gloss": "evil, bad, wrong; evil-doing, wickedness" }
        ],
        "note": "Śaṅkara supplies the noun: pāpaṃ karma, ‘evil action’. Rāmānuja narrows it to the specific evil in view — the pull back into sense-experience that wrecks jñāna-yoga."
      },
      {
        "i": 5,
        "deva": "चरति",
        "iast": "carati",
        "gloss": "engages in, practises, carries on",
        "stem": null,
        "root": "√car (bhvādi, 1P)",
        "rootGloss": "to move, to roam, to walk; with an object: to engage in, to practise, to commit",
        "affix": "tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. parasmaipada",
        "karaka": "the verb; kartṛ pūruṣaḥ, karman pāpam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "√car", "gloss": "to move, to roam; to engage in, to practise" },
          { "form": "-a-", "gloss": "(śap, the present-stem marker of the bhvādi class)" },
          { "form": "-ti", "gloss": "(3rd person singular, active)" }
        ],
        "note": "√car takes an object here, so the sense is engagement — ‘practises evil’ — not the merely spatial ‘moves’. Śaṅkara glosses it with ācarati, ‘carries out’."
      },
      {
        "i": 6,
        "deva": "पूरुषः",
        "iast": "pūruṣaḥ",
        "gloss": "man, person",
        "stem": "pūruṣa (= puruṣa; pṛṣodarādi lengthening, metri causa)",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of carati",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "pūruṣa", "gloss": "man, person, human being" }
        ],
        "note": "Śaṅkara equates the forms outright — ‘pūruṣaḥ puruṣaḥ’. Here the word is the ordinary ‘man’, not the puruṣa of Sāṅkhya."
      },
      {
        "i": 7,
        "deva": "अनिच्छन्",
        "iast": "anicchan",
        "gloss": "not wishing, not wanting to",
        "stem": "an-icchat",
        "root": "√iṣ (tudādi, 6P)",
        "rootGloss": "to wish, to want, to desire, to seek",
        "affix": "nañ + śatṛ + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; pres. act. part., negated",
        "karaka": "attribute of pūruṣaḥ (concessive)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "an-", "gloss": "not (the negative prefix nañ, an- before a vowel)" },
          { "form": "√iṣ", "gloss": "to wish, to want, to desire" },
          { "form": "-cch-", "gloss": "(śa, the present-stem marker of the tudādi class, with the ch of icchati)" },
          { "form": "-at", "gloss": "(present active participle: ‘—ing’)" }
        ],
        "sandhi": "anicchann api ← anicchan + api (n doubled before a vowel after a short vowel)"
      },
      {
        "i": 8,
        "deva": "अपि",
        "iast": "api",
        "gloss": "even, although",
        "stem": "api",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable particle",
        "karaka": "— (concessive particle over anicchan)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "api", "gloss": "even, also; although (concessive, after a participle)" }
        ]
      },
      {
        "i": 9,
        "deva": "वार्ष्णेय",
        "iast": "vārṣṇeya",
        "gloss": "O descendant of Vṛṣṇi",
        "stem": "vārṣṇeya",
        "root": null,
        "affix": "ḍhak (taddhita, gotra) + su (sambodhana prathamā ekavacana)",
        "morph": "voc. sg. masc.",
        "karaka": "āmantraṇa (the one addressed)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "vṛṣṇi", "gloss": "Vṛṣṇi, the Yādava clan-ancestor" },
          { "form": "-eya", "gloss": "(taddhita ḍhak: ‘descendant of —’, with vṛddhi of the first vowel)" }
        ],
        "note": "Śaṅkara reads the epithet out: vṛṣṇi-kula-prasūta, ‘born in the line of Vṛṣṇi’."
      },
      {
        "i": 10,
        "deva": "बलात्",
        "iast": "balāt",
        "gloss": "by force, forcibly",
        "stem": "bala",
        "root": null,
        "affix": "ṅasi (pañcamī ekavacana)",
        "morph": "abl. sg. neut.",
        "karaka": "hetu in the ablative (‘from force’ → ‘by force’), under iva",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "bala", "gloss": "strength, force, might" },
          { "form": "-āt", "gloss": "(ablative singular: ‘from’, here of cause)" }
        ]
      },
      {
        "i": 11,
        "deva": "इव",
        "iast": "iva",
        "gloss": "as if, as it were",
        "stem": "iva",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable particle of comparison",
        "karaka": "— (marks the whole phrase as a simile)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "iva", "gloss": "like, as if, as it were" }
        ],
        "note": "iva keeps the coercion a comparison, not a claim: the man is not literally harnessed by another — he acts, and yet as though driven."
      },
      {
        "i": 12,
        "deva": "नियोजितः",
        "iast": "niyojitaḥ",
        "gloss": "made to be yoked to it, set to the task",
        "stem": "niyojita",
        "root": "√yuj (rudhādi, 7U)",
        "rootGloss": "to yoke, to harness, to join, to attach; to set to a task",
        "affix": "ṇic (causative) + kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; causative past passive part.",
        "karaka": "predicate of pūruṣaḥ; karman of the unnamed causer",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ni-", "gloss": "down, into; fastened down onto" },
          { "form": "√yuj", "gloss": "to yoke, to harness, to set to a task" },
          { "form": "-i-", "gloss": "(ṇic, the causative marker: ‘to make —’)" },
          { "form": "-ta", "gloss": "(past passive participle: ‘having been —ed’)" }
        ],
        "note": "The causative is the point of the verse: someone made him do it. Arjuna's question is who or what that someone is."
      }
    ],
    "grammar": {
      "karakaSummary": "A single interrogative sentence. pūruṣaḥ — kartṛ (nom.) of carati; pāpam — karman (acc.); kena — hetu (instr.) and the agent of the passive participle prayuktaḥ; ayam — attribute of pūruṣaḥ; anicchan api — concessive participial phrase over the same subject; vārṣṇeya — āmantraṇa (voc.); balāt — ablative of cause governed by iva; niyojitaḥ — the second predicate participle.",
      "verbalModality": "One finite verb, carati (laṭ, present indicative) — the evil-doing is stated as ongoing fact, not as possibility. The two participles (prayuktaḥ, niyojitaḥ) are both passive: the man is grammatically done-to even while he is the one acting."
    }
  },

  {
    "locus": "3.37",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "काम एष क्रोध एष रजोगुणसमुद्भवः।\nमहाशनो महापाप्मा विद्ध्येनमिह वैरिणम्॥",
    "iast": "kāma eṣa krodha eṣa rajo-guṇa-samudbhavaḥ |\nmahāśano mahā-pāpmā viddhy enam iha vairiṇam ||",
    "sense": "Kṛṣṇa names it: kāma — and anger, which is the same thing turned back on itself. Born of the guṇa rajas, it eats without end and does great harm; know it for the enemy.",
    "english": "{1:This is} {0:kāma}, {3:this is} {2:anger} — {4:arisen from the guṇa rajas}, {5:the great devourer}, {6:the great evildoer}. {7:Know} {8:it} {9:here} to be {10:the enemy}.",
    "words": [
      {
        "i": 0,
        "deva": "कामः",
        "iast": "kāmaḥ",
        "gloss": "kāma — desire as craving, the wanting that reaches for its object",
        "stem": "kāma",
        "root": "√kam (bhvādi, 1Ā)",
        "rootGloss": "to wish, to long for, to desire, to love",
        "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ (subject of the implied copula)",
        "glossaryKey": "kama",
        "translatable": false,
        "parts": [
          { "form": "√kam", "gloss": "to wish, to long for, to desire" },
          { "form": "-a", "gloss": "(ghañ, forming the action-noun with vṛddhi: ‘the wanting’)" }
        ],
        "note": "Rāmānuja specifies it as kāma for the objects of sense (śabdādi-viṣaya), thrown up by prior vāsanās."
      },
      {
        "i": 1,
        "deva": "एषः",
        "iast": "eṣaḥ",
        "gloss": "this (one), the one just asked about",
        "stem": "etad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate of the implied copula",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "etad", "gloss": "this, this here (the nearer demonstrative)" }
        ],
        "sandhi": "kāma eṣa ← kāmaḥ + eṣaḥ (visarga → a before e; and eṣaḥ → eṣa before a following consonant)"
      },
      {
        "i": 2,
        "deva": "क्रोधः",
        "iast": "krodhaḥ",
        "gloss": "anger, wrath",
        "stem": "krodha",
        "root": "√krudh (divādi, 4P)",
        "rootGloss": "to be angry, to grow wroth",
        "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ (subject of the implied copula)",
        "glossaryKey": "krodha",
        "translatable": true,
        "parts": [
          { "form": "√krudh", "gloss": "to be angry, to grow wroth" },
          { "form": "-a", "gloss": "(ghañ, forming the action-noun with guṇa: ‘the being-angry’)" }
        ],
        "note": "Śaṅkara: the same kāma, when blocked by something, turns into anger — so the two are one enemy under two aspects. Madhva presses it further: without kāma no anger arises at all."
      },
      {
        "i": 3,
        "deva": "एषः",
        "iast": "eṣaḥ",
        "gloss": "this (one), the one just asked about",
        "stem": "etad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "predicate of the implied copula",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "etad", "gloss": "this, this here (the nearer demonstrative)" }
        ]
      },
      {
        "i": 4,
        "deva": "रजोगुणसमुद्भवः",
        "iast": "rajo-guṇa-samudbhavaḥ",
        "gloss": "whose arising is from the guṇa rajas",
        "stem": "rajo-guṇa-samudbhava",
        "root": "√bhū (bhvādi, 1P)",
        "rootGloss": "to be, to become, to arise, to come into being",
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute of kāmaḥ / krodhaḥ",
        "glossaryKey": "guna",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi (with a karmadhāraya first member)",
          "vigraha": "rajaś ca sa guṇaś ca rajo-guṇaḥ; rajo-guṇaḥ samudbhavo yasya saḥ",
          "members": ["rajas", "guṇa", "samudbhava"]
        },
        "parts": [
          { "form": "rajas", "gloss": "rajas — the guṇa of motion, urge and restlessness" },
          { "form": "guṇa", "gloss": "guṇa — one of the three constitutive strands of prakṛti" },
          { "form": "sam-ud-√bhū", "gloss": "to arise fully up out of; to originate" },
          { "form": "-a", "gloss": "(the action-noun ending: ‘the arising’)" }
        ],
        "note": "Śaṅkara offers the alternative reading too — either ‘whose origin is the guṇa rajas’ (bahuvrīhi) or ‘the arising of the guṇa rajas’ (ṣaṣṭhī-tatpuruṣa), since kāma once risen sets rajas going."
      },
      {
        "i": 5,
        "deva": "महाशनः",
        "iast": "mahāśanaḥ",
        "gloss": "the great devourer — whose eating is huge",
        "stem": "mahā-aśana",
        "root": "√aś (kryādi, 9P)",
        "rootGloss": "to eat, to consume, to devour",
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute of kāmaḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "mahad aśanaṃ yasya saḥ",
          "members": ["mahat", "aśana"]
        },
        "parts": [
          { "form": "mahā-", "gloss": "great, vast (the compounding form of mahat)" },
          { "form": "√aś", "gloss": "to eat, to consume, to devour" },
          { "form": "-ana", "gloss": "(lyuṭ, the action-noun: ‘eating’)" }
        ],
        "note": "Śaṅkara's vigraha is exactly this — mahad aśanam asyeti mahāśanaḥ. Madhva turns it the other way: what kāma has to eat is itself vast."
      },
      {
        "i": 6,
        "deva": "महापाप्मा",
        "iast": "mahā-pāpmā",
        "gloss": "the great evildoer — whose evil is huge",
        "stem": "mahā-pāpman",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "attribute of kāmaḥ",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "mahān pāpmā yasya saḥ",
          "members": ["mahat", "pāpman"]
        },
        "parts": [
          { "form": "mahā-", "gloss": "great, vast (the compounding form of mahat)" },
          { "form": "pāpman", "gloss": "evil, wickedness; the evil in a person" }
        ],
        "note": "Śaṅkara grounds it in the causal chain: driven by kāma a creature does evil. Madhva makes it the cause of the gravest evils of all, brahmin-killing and the like."
      },
      {
        "i": 7,
        "deva": "विद्धि",
        "iast": "viddhi",
        "gloss": "know!, recognize!",
        "stem": null,
        "root": "√vid (adādi, 2P)",
        "rootGloss": "to know, to be aware of, to recognize",
        "affix": "hi (loṭ, madhyama-puruṣa ekavacana)",
        "morph": "2nd sg. imperative parasmaipada",
        "karaka": "the verb; kartṛ is Arjuna (understood), karman enam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "√vid", "gloss": "to know, to be aware of, to recognize" },
          { "form": "-dhi", "gloss": "(hi, the 2nd-singular imperative, as -dhi after a consonant)" }
        ],
        "sandhi": "viddhy enam ← viddhi + enam (i → y before a dissimilar vowel)"
      },
      {
        "i": 8,
        "deva": "एनम्",
        "iast": "enam",
        "gloss": "this one, him (the one under discussion)",
        "stem": "enad (the enclitic anaphoric)",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of viddhi",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "enad", "gloss": "him, this one (the unstressed anaphoric pronoun, only ever non-initial)" }
        ]
      },
      {
        "i": 9,
        "deva": "इह",
        "iast": "iha",
        "gloss": "here, in this world",
        "stem": "iha",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb of place",
        "karaka": "adhikaraṇa in adverbial form (‘here’)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "iha", "gloss": "here, in this place, in this world" }
        ],
        "note": "Śaṅkara reads iha as iha saṃsāre — ‘here in saṃsāra’."
      },
      {
        "i": 10,
        "deva": "वैरिणम्",
        "iast": "vairiṇam",
        "gloss": "the enemy, the hostile one",
        "stem": "vairin",
        "root": null,
        "affix": "ini (taddhita) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "predicate accusative with viddhi (‘know him as —’)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "vaira", "gloss": "enmity, hostility, feud" },
          { "form": "-in", "gloss": "(taddhita ini: ‘the one who has —’)" }
        ],
        "note": "Madhva gives the reason for the word: it opposes every one of the puruṣārthas, the ends a human life is for."
      }
    ],
    "grammar": {
      "karakaSummary": "Two nominal sentences and one imperative. Line 1: kāmaḥ and krodhaḥ — kartṛ of the implied copula, with eṣaḥ predicate each time; rajo-guṇa-samudbhavaḥ, mahāśanaḥ, mahā-pāpmā — three further nominatives in apposition. Line 2: viddhi — imperative addressed to Arjuna; enam — karman; vairiṇam — predicate accusative; iha — adverbial adhikaraṇa.",
      "verbalModality": "One finite form only, and it is an imperative (loṭ): the verse does not argue, it identifies and commands recognition. Everything else is nominal apposition piling up epithets on the one named thing."
    }
  },

  {
    "locus": "3.38",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "धूमेनाव्रियते वह्निर्यथाऽऽदर्शो मलेन च।\nयथोल्बेनावृतो गर्भस्तथा तेनेदमावृतम्॥",
    "iast": "dhūmenāvriyate vahnir yathādarśo malena ca |\nyatholbenāvṛto garbhas tathā tenedam āvṛtam ||",
    "sense": "Three images of covering, graded by how total it is: smoke over fire, dirt on a mirror, the caul around an embryo — so is this covered by kāma.",
    "english": "{3:As} {2:fire} {1:is covered} {0:by smoke}, {6:and} {4:a mirror} {5:by dirt}, {7:as} {10:an embryo} {9:is covered} {8:by the caul} — {11:so} {13:this} {14:is covered} {12:by that}.",
    "words": [
      {
        "i": 0,
        "deva": "धूमेन",
        "iast": "dhūmena",
        "gloss": "by smoke",
        "stem": "dhūma",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "karaṇa of āvriyate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "dhūma", "gloss": "smoke" },
          { "form": "-ena", "gloss": "(instrumental singular: ‘by, with’)" }
        ],
        "note": "Śaṅkara marks the smoke as sahaja — born together with the fire, not added to it from outside. The image is chosen for that."
      },
      {
        "i": 1,
        "deva": "आव्रियते",
        "iast": "āvriyate",
        "gloss": "is covered over, is veiled",
        "stem": null,
        "root": "√vṛ (kryādi, 9U)",
        "rootGloss": "to cover, to enclose, to veil, to shut in",
        "affix": "yak (bhāve/karmaṇi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. passive",
        "karaka": "the verb; karman vahniḥ (in the nominative, as passive subject), karaṇa dhūmena",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ā-", "gloss": "all over, right around" },
          { "form": "√vṛ", "gloss": "to cover, to enclose, to veil" },
          { "form": "-ya-", "gloss": "(yak, the passive marker)" },
          { "form": "-te", "gloss": "(3rd person singular, ātmanepada)" }
        ]
      },
      {
        "i": 2,
        "deva": "वह्निः",
        "iast": "vahniḥ",
        "gloss": "fire",
        "stem": "vahni",
        "root": "√vah (bhvādi, 1U)",
        "rootGloss": "to carry, to bear, to convey",
        "affix": "ni (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "karman of the passive āvriyate, standing in the nominative",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "√vah", "gloss": "to carry, to bear, to convey" },
          { "form": "-ni", "gloss": "(kṛt ni: ‘the carrier’ — fire as what bears the offering)" }
        ],
        "note": "Śaṅkara sets the terms in opposition: fire is prakāśātmaka, of the nature of light; smoke aprakāśātmaka, of the nature of not-light."
      },
      {
        "i": 3,
        "deva": "यथा",
        "iast": "yathā",
        "gloss": "as, just as",
        "stem": "yathā",
        "root": null,
        "affix": "thāl (taddhita) — avyaya",
        "morph": "indeclinable, correlative with tathā",
        "karaka": "— (marks the comparison clause)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "yad", "gloss": "which, what (the relative stem)" },
          { "form": "-thā", "gloss": "(taddhita thāl: ‘in the manner of —’)" }
        ]
      },
      {
        "i": 4,
        "deva": "आदर्शः",
        "iast": "ādarśaḥ",
        "gloss": "a mirror",
        "stem": "ādarśa",
        "root": "√dṛś (bhvādi, 1P)",
        "rootGloss": "to see, to look at, to behold",
        "affix": "ghañ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "karman of the passive āvriyate, carried over into this clause",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ā-", "gloss": "back, towards (the seeing turned back on itself)" },
          { "form": "√dṛś", "gloss": "to see, to look at, to behold" },
          { "form": "-a", "gloss": "(ghañ, forming the instrument-noun with vṛddhi: ‘what one sees by’)" }
        ],
        "sandhi": "yathādarśaḥ ← yathā + ādarśaḥ (ā + ā → ā)",
        "note": "Madhva takes the mirror as the antaḥkaraṇa: dirtied, it stops being the thing by which something else shows up."
      },
      {
        "i": 5,
        "deva": "मलेन",
        "iast": "malena",
        "gloss": "by dirt, by tarnish",
        "stem": "mala",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. neut.",
        "karaka": "karaṇa of the carried-over āvriyate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "mala", "gloss": "dirt, filth, impurity, tarnish" },
          { "form": "-ena", "gloss": "(instrumental singular: ‘by, with’)" }
        ]
      },
      {
        "i": 6,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (joins the mirror-image to the fire-image)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ca", "gloss": "and, also (enclitic — never first in its clause)" }
        ]
      },
      {
        "i": 7,
        "deva": "यथा",
        "iast": "yathā",
        "gloss": "as, just as",
        "stem": "yathā",
        "root": null,
        "affix": "thāl (taddhita) — avyaya",
        "morph": "indeclinable, correlative with tathā",
        "karaka": "— (marks the third comparison clause)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "yad", "gloss": "which, what (the relative stem)" },
          { "form": "-thā", "gloss": "(taddhita thāl: ‘in the manner of —’)" }
        ]
      },
      {
        "i": 8,
        "deva": "उल्बेन",
        "iast": "ulbena",
        "gloss": "by the caul, by the membrane enclosing the womb",
        "stem": "ulba",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. neut.",
        "karaka": "karaṇa of āvṛtaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ulba", "gloss": "the caul, the amnion; the membrane around the embryo" }
        ],
        "sandhi": "yatholbena ← yathā + ulbena (ā + u → o)",
        "note": "Śaṅkara glosses it jarāyu, garbha-veṣṭana — the womb-wrapping. This third image is the strongest: the covering is total and the covered thing has never yet been seen."
      },
      {
        "i": 9,
        "deva": "आवृतः",
        "iast": "āvṛtaḥ",
        "gloss": "covered, enclosed",
        "stem": "āvṛta",
        "root": "√vṛ (kryādi, 9U)",
        "rootGloss": "to cover, to enclose, to veil, to shut in",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. masc.; past passive part.",
        "karaka": "predicate of garbhaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ā-", "gloss": "all over, right around" },
          { "form": "√vṛ", "gloss": "to cover, to enclose, to veil" },
          { "form": "-ta", "gloss": "(past passive participle: ‘having been —ed’)" }
        ]
      },
      {
        "i": 10,
        "deva": "गर्भः",
        "iast": "garbhaḥ",
        "gloss": "the embryo, the child in the womb",
        "stem": "garbha",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "the one qualified by āvṛtaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "garbha", "gloss": "womb; what is in the womb, the embryo" }
        ],
        "note": "Madhva reads the image allegorically: as the caul binds the embryo, so kāma binds the jīva."
      },
      {
        "i": 11,
        "deva": "तथा",
        "iast": "tathā",
        "gloss": "so, in that same way",
        "stem": "tathā",
        "root": null,
        "affix": "thāl (taddhita) — avyaya",
        "morph": "indeclinable, correlative answering yathā",
        "karaka": "— (closes the comparison)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "tad", "gloss": "that (the correlative stem)" },
          { "form": "-thā", "gloss": "(taddhita thāl: ‘in the manner of —’)" }
        ]
      },
      {
        "i": 12,
        "deva": "तेन",
        "iast": "tena",
        "gloss": "by that (by kāma)",
        "stem": "tad",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "karaṇa of āvṛtam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "tad", "gloss": "that, it (the anaphoric demonstrative)" },
          { "form": "-ena", "gloss": "(instrumental singular: ‘by, with’)" }
        ],
        "note": "The referent is left as a pronoun in the verse; both Śaṅkara and Rāmānuja supply kāmena."
      },
      {
        "i": 13,
        "deva": "इदम्",
        "iast": "idam",
        "gloss": "this",
        "stem": "idam",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "karman of the passive āvṛtam, in the nominative",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "idam", "gloss": "this, this here (proximate demonstrative)" }
        ],
        "note": "Deliberately unspecified — 3.39 takes it up and says what ‘this’ is. Rāmānuja supplies jantu-jātam, ‘the whole race of creatures’; Madhva reads it of the paramātman and the antaḥkaraṇa alike."
      },
      {
        "i": 14,
        "deva": "आवृतम्",
        "iast": "āvṛtam",
        "gloss": "covered, veiled over",
        "stem": "āvṛta",
        "root": "√vṛ (kryādi, 9U)",
        "rootGloss": "to cover, to enclose, to veil, to shut in",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.; past passive part.",
        "karaka": "predicate of idam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ā-", "gloss": "all over, right around" },
          { "form": "√vṛ", "gloss": "to cover, to enclose, to veil" },
          { "form": "-ta", "gloss": "(past passive participle: ‘having been —ed’)" }
        ]
      }
    ],
    "grammar": {
      "karakaSummary": "Three yathā-clauses answered by one tathā-clause. In each, the covered thing stands in the nominative as karman of a passive (vahniḥ, ādarśaḥ, garbhaḥ, idam) and the coverer in the instrumental as karaṇa (dhūmena, malena, ulbena, tena). The second clause borrows its verb from the first; the third and fourth use the participle āvṛta rather than a finite form.",
      "verbalModality": "One finite verb for the whole verse — āvriyate, present passive. Nothing here is commanded or wished; the covering is stated as what is simply the case."
    }
  },

  {
    "locus": "3.39",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "आवृतं ज्ञानमेतेन ज्ञानिनो नित्यवैरिणा।\nकामरूपेण कौन्तेय दुष्पूरेणानलेन च॥",
    "iast": "āvṛtaṃ jñānam etena jñānino nitya-vairiṇā |\nkāma-rūpeṇa kaunteya duṣpūreṇānalena ca ||",
    "sense": "What is covered is knowledge — and the enemy is the knower's, permanently: a thing shaped as kāma, which can never be filled and never has enough.",
    "english": "{1:Knowledge} {0:is covered} {2:by this} {4:perpetual enemy} {3:of the knower}, {5:whose form is kāma}, {6:O son of Kuntī} — {7:hard to fill} {9:and} {8:never having enough}.",
    "words": [
      {
        "i": 0,
        "deva": "आवृतम्",
        "iast": "āvṛtam",
        "gloss": "covered, veiled over",
        "stem": "āvṛta",
        "root": "√vṛ (kryādi, 9U)",
        "rootGloss": "to cover, to enclose, to veil, to shut in",
        "affix": "kta (niṣṭhā) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.; past passive part.",
        "karaka": "predicate of jñānam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ā-", "gloss": "all over, right around" },
          { "form": "√vṛ", "gloss": "to cover, to enclose, to veil" },
          { "form": "-ta", "gloss": "(past passive participle: ‘having been —ed’)" }
        ],
        "note": "Picks up āvṛtam from the end of 3.38 and answers its ‘this’."
      },
      {
        "i": 1,
        "deva": "ज्ञानम्",
        "iast": "jñānam",
        "gloss": "knowledge",
        "stem": "jñāna",
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to come to know, to understand, to recognize",
        "affix": "lyuṭ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "karman of the passive āvṛtam, standing in the nominative",
        "glossaryKey": "jnana",
        "translatable": true,
        "parts": [
          { "form": "√jñā", "gloss": "to know, to understand, to recognize" },
          { "form": "-ana", "gloss": "(lyuṭ, the action-noun: ‘the knowing’)" }
        ],
        "note": "Śaṅkara takes it as the understanding of the self and the rest, got from śāstra and from a teacher; Rāmānuja as knowledge whose object is the nature of the self."
      },
      {
        "i": 2,
        "deva": "एतेन",
        "iast": "etena",
        "gloss": "by this",
        "stem": "etad",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "karaṇa of āvṛtam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "etad", "gloss": "this, this here (the nearer demonstrative)" },
          { "form": "-ena", "gloss": "(instrumental singular: ‘by, with’)" }
        ]
      },
      {
        "i": 3,
        "deva": "ज्ञानिनः",
        "iast": "jñāninaḥ",
        "gloss": "of the one who knows, of the knower",
        "stem": "jñānin",
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to come to know, to understand, to recognize",
        "affix": "ini (taddhita) + ṅas (ṣaṣṭhī ekavacana)",
        "morph": "gen. sg. masc.",
        "karaka": "sambandha (whose enemy it is)",
        "glossaryKey": "jnana",
        "translatable": true,
        "parts": [
          { "form": "jñāna", "gloss": "knowledge, the knowing" },
          { "form": "-in", "gloss": "(taddhita ini: ‘the one who has —’)" }
        ],
        "note": "Śaṅkara's point turns on the genitive: kāma is the knower's perpetual enemy and not the fool's, because only the knower sees, at the time of craving, what the craving is doing to him. The fool sees it as a friend and only learns better once the pain arrives."
      },
      {
        "i": 4,
        "deva": "नित्यवैरिणा",
        "iast": "nitya-vairiṇā",
        "gloss": "by the perpetual enemy",
        "stem": "nitya-vairin",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "karaṇa of āvṛtam, in apposition to etena",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "karmadhāraya",
          "vigraha": "nityaś cāsau vairī ca — nitya-vairī; tena",
          "members": ["nitya", "vairin"]
        },
        "parts": [
          { "form": "nitya", "gloss": "constant, perpetual, unceasing" },
          { "form": "vaira", "gloss": "enmity, hostility, feud" },
          { "form": "-in", "gloss": "(taddhita ini: ‘the one who has —’)" }
        ]
      },
      {
        "i": 5,
        "deva": "कामरूपेण",
        "iast": "kāma-rūpeṇa",
        "gloss": "whose form is kāma",
        "stem": "kāma-rūpa",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "karaṇa of āvṛtam, in apposition to etena",
        "glossaryKey": "kama",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "kāma eva rūpaṃ yasya saḥ — tena",
          "members": ["kāma", "rūpa"]
        },
        "parts": [
          { "form": "kāma", "gloss": "kāma — desire as craving, the wanting that reaches for its object" },
          { "form": "rūpa", "gloss": "form, shape; the visible aspect a thing has" }
        ],
        "note": "Śaṅkara's vigraha: kāma icchaiva rūpam asya — its form is nothing but wanting."
      },
      {
        "i": 6,
        "deva": "कौन्तेय",
        "iast": "kaunteya",
        "gloss": "O son of Kuntī",
        "stem": "kaunteya",
        "root": null,
        "affix": "ḍhak (taddhita, apatya) + su (sambodhana prathamā ekavacana)",
        "morph": "voc. sg. masc.",
        "karaka": "āmantraṇa (the one addressed)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "kuntī", "gloss": "Kuntī, Arjuna's mother" },
          { "form": "-eya", "gloss": "(taddhita ḍhak: ‘son of —’, with vṛddhi of the first vowel)" }
        ]
      },
      {
        "i": 7,
        "deva": "दुष्पूरेण",
        "iast": "duṣpūreṇa",
        "gloss": "hard to fill",
        "stem": "duṣpūra",
        "root": "√pṝ (kryādi, 9P)",
        "rootGloss": "to fill, to fill up, to satisfy",
        "affix": "khal (kṛt, after dus-) + ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "attribute of nitya-vairiṇā",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "dus-", "gloss": "hard to —, ill, difficult (as duṣ- before p)" },
          { "form": "√pṝ", "gloss": "to fill, to fill up, to satisfy" },
          { "form": "-a", "gloss": "(khal, the kṛt affix that makes ‘hard to be —ed’)" }
        ],
        "note": "Śaṅkara: duḥkhena pūraṇam asya — the filling of it is done only with pain. Madhva: the rank of Indra is not got easily.",
        "sandhi": "duṣ- ← dus- (s → ṣ before the following p, by ṣatva)"
      },
      {
        "i": 8,
        "deva": "अनलेन",
        "iast": "analena",
        "gloss": "never having enough; insatiable",
        "stem": "anala",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "attribute of nitya-vairiṇā",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "an-", "gloss": "not (the negative prefix nañ, an- before a vowel)" },
          { "form": "alam", "gloss": "enough, sufficient" },
          { "form": "-a", "gloss": "(the derivational vowel of the resulting adjective/noun)" }
        ],
        "note": "The commentators take the etymology and not the ordinary lexical sense: Śaṅkara — nāsyālaṃ paryāptir vidyata ity analaḥ, ‘there is no “enough”, no sufficiency, for it — hence analá’; Madhva makes the same point with the ladder from Indra's rank to Brahmā's. The word's other and commoner meaning, ‘fire’, is not what is being read here, though the fire of 3.38 is still in earshot."
      },
      {
        "i": 9,
        "deva": "च",
        "iast": "ca",
        "gloss": "and",
        "stem": "ca",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable conjunction",
        "karaka": "— (joins duṣpūreṇa and analena)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ca", "gloss": "and, also (enclitic — never first in its clause)" }
        ],
        "sandhi": "duṣpūreṇānalena ← duṣpūreṇa + analena (a + a → ā)"
      }
    ],
    "grammar": {
      "karakaSummary": "A single nominal sentence built on a passive participle. jñānam — karman of āvṛtam, standing in the nominative; āvṛtam — the predicate; etena, nitya-vairiṇā, kāma-rūpeṇa, duṣpūreṇa, analena — one karaṇa expressed five times over, the pronoun first and then four epithets in apposition to it; jñāninaḥ — sambandha (‘the knower's’); kaunteya — āmantraṇa (voc.).",
      "verbalModality": "No finite verb at all. The whole verse is one participial predication, which is why it reads as a description of a standing condition rather than an event."
    }
  },

  {
    "locus": "3.40",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "इन्द्रियाणि मनो बुद्धिरस्याधिष्ठानमुच्यते।\nएतैर्विमोहयत्येष ज्ञानमावृत्य देहिनम्॥",
    "iast": "indriyāṇi mano buddhir asyādhiṣṭhānam ucyate |\netair vimohayaty eṣa jñānam āvṛtya dehinam ||",
    "sense": "Where the enemy is stationed: the indriyas, manas and buddhi. Working from that station it covers knowledge over and throws the embodied one into delusion.",
    "english": "{0:The indriyas}, {1:manas}, {2:buddhi} {5:are said to be} {4:the seat} {3:of this one}. {8:This one}, {10:having covered over} {9:knowledge} {6:by means of these}, {7:casts into delusion} {11:the embodied one}.",
    "words": [
      {
        "i": 0,
        "deva": "इन्द्रियाणि",
        "iast": "indriyāṇi",
        "gloss": "the indriyas — the powers of sense and action",
        "stem": "indriya",
        "root": null,
        "affix": "jas (prathamā bahuvacana)",
        "morph": "nom. pl. neut.",
        "karaka": "kartṛ of the passive ucyate (‘are called’)",
        "glossaryKey": "indriya",
        "translatable": false,
        "parts": [
          { "form": "indra", "gloss": "Indra; the lord, the ruling power" },
          { "form": "-iya", "gloss": "(taddhita ghac: ‘belonging to Indra’ — hence a power of the indwelling ruler)" }
        ]
      },
      {
        "i": 1,
        "deva": "मनः",
        "iast": "manaḥ",
        "gloss": "manas — the faculty that intends, hesitates and turns things over",
        "stem": "manas",
        "root": "√man (divādi, 4Ā)",
        "rootGloss": "to think, to consider, to have in mind, to deem",
        "affix": "asun (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "kartṛ of the passive ucyate",
        "glossaryKey": "manas",
        "translatable": false,
        "parts": [
          { "form": "√man", "gloss": "to think, to consider, to have in mind" },
          { "form": "-as", "gloss": "(asun, the neuter action/agent noun)" }
        ],
        "note": "Śaṅkara's definition, given at 3.42: saṅkalpa-vikalpātmaka — manas is the faculty of proposing and doubting, as against buddhi which decides."
      },
      {
        "i": 2,
        "deva": "बुद्धिः",
        "iast": "buddhiḥ",
        "gloss": "buddhi — the faculty that discriminates and settles a matter",
        "stem": "buddhi",
        "root": "√budh (bhvādi, 1U)",
        "rootGloss": "to wake, to awaken; to be aware of, to understand, to notice",
        "affix": "ktin (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. fem.",
        "karaka": "kartṛ of the passive ucyate",
        "glossaryKey": "buddhi",
        "translatable": false,
        "parts": [
          { "form": "√budh", "gloss": "to wake, to be aware of, to understand" },
          { "form": "-ti", "gloss": "(ktin, the feminine action-noun: ‘the awakening / the understanding’)" }
        ],
        "note": "Śaṅkara at 3.42: niścayātmikā — buddhi is of the nature of settling what is the case."
      },
      {
        "i": 3,
        "deva": "अस्य",
        "iast": "asya",
        "gloss": "of this one (of kāma)",
        "stem": "idam",
        "root": null,
        "affix": "ṅas (ṣaṣṭhī ekavacana)",
        "morph": "gen. sg. masc.",
        "karaka": "sambandha (whose seat it is)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "idam", "gloss": "this, this one here (proximate demonstrative)" }
        ]
      },
      {
        "i": 4,
        "deva": "अधिष्ठानम्",
        "iast": "adhiṣṭhānam",
        "gloss": "seat, standing-place; the base something operates from",
        "stem": "adhiṣṭhāna",
        "root": "√sthā (bhvādi, 1P)",
        "rootGloss": "to stand, to stand firm, to abide, to be situated",
        "affix": "lyuṭ (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "predicate nominative of ucyate",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "adhi-", "gloss": "over, upon; taking one's stand on" },
          { "form": "√sthā", "gloss": "to stand, to abide, to be situated" },
          { "form": "-ana", "gloss": "(lyuṭ, the place-noun: ‘the place of —ing’)" }
        ],
        "sandhi": "asyādhiṣṭhānam ← asya + adhiṣṭhānam (a + a → ā)",
        "note": "Śaṅkara glosses it āśraya, ‘support’; Rāmānuja upakaraṇa, ‘the instruments by which it takes its stand on the self’. Both readings are of the same military image — the enemy's position, which is why 3.41 says to take it first."
      },
      {
        "i": 5,
        "deva": "उच्यते",
        "iast": "ucyate",
        "gloss": "is said, is called",
        "stem": null,
        "root": "√vac (adādi, 2P)",
        "rootGloss": "to speak, to say, to tell, to call",
        "affix": "yak (karmaṇi) + ta (laṭ, prathama-puruṣa ekavacana ātmanepada)",
        "morph": "3rd sg. pres. indic. passive",
        "karaka": "the verb; its kartṛ is left unstated (‘it is said’ — by those who know)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "√vac", "gloss": "to speak, to say, to call" },
          { "form": "-uc-", "gloss": "(samprasāraṇa: the va of √vac becomes u before the passive)" },
          { "form": "-ya-", "gloss": "(yak, the passive marker)" },
          { "form": "-te", "gloss": "(3rd person singular, ātmanepada)" }
        ],
        "note": "Singular verb with a plural-plus-singular subject: it agrees with the predicate adhiṣṭhānam, not with the list."
      },
      {
        "i": 6,
        "deva": "एतैः",
        "iast": "etaiḥ",
        "gloss": "by these",
        "stem": "etad",
        "root": null,
        "affix": "bhis (tṛtīyā bahuvacana)",
        "morph": "instr. pl. neut.",
        "karaka": "karaṇa of vimohayati",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "etad", "gloss": "this, this here (the nearer demonstrative)" },
          { "form": "-aiḥ", "gloss": "(instrumental plural: ‘by, with’)" }
        ]
      },
      {
        "i": 7,
        "deva": "विमोहयति",
        "iast": "vimohayati",
        "gloss": "casts into delusion, bewilders every which way",
        "stem": null,
        "root": "√muh (divādi, 4P)",
        "rootGloss": "to be bewildered, to lose one's bearings, to be deluded",
        "affix": "ṇic (causative) + tip (laṭ, prathama-puruṣa ekavacana)",
        "morph": "3rd sg. pres. indic. causative parasmaipada",
        "karaka": "the verb; kartṛ eṣaḥ, karman dehinam, karaṇa etaiḥ",
        "glossaryKey": "moha",
        "translatable": true,
        "parts": [
          { "form": "vi-", "gloss": "apart, in various directions (here: in every way)" },
          { "form": "√muh", "gloss": "to be bewildered, to be deluded" },
          { "form": "-aya-", "gloss": "(ṇic, the causative marker: ‘to make —’)" },
          { "form": "-ti", "gloss": "(3rd person singular, active)" }
        ],
        "note": "Śaṅkara reads the prefix distributively — vividhaṃ mohayati, ‘deludes in many ways’."
      },
      {
        "i": 8,
        "deva": "एषः",
        "iast": "eṣaḥ",
        "gloss": "this one (kāma)",
        "stem": "etad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of vimohayati",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "etad", "gloss": "this, this here (the nearer demonstrative)" }
        ],
        "sandhi": "vimohayaty eṣa ← vimohayati + eṣaḥ (i → y before a dissimilar vowel)"
      },
      {
        "i": 9,
        "deva": "ज्ञानम्",
        "iast": "jñānam",
        "gloss": "knowledge",
        "stem": "jñāna",
        "root": "√jñā (kryādi, 9U)",
        "rootGloss": "to know, to come to know, to understand, to recognize",
        "affix": "lyuṭ (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. neut.",
        "karaka": "karman of āvṛtya",
        "glossaryKey": "jnana",
        "translatable": true,
        "parts": [
          { "form": "√jñā", "gloss": "to know, to understand, to recognize" },
          { "form": "-ana", "gloss": "(lyuṭ, the action-noun: ‘the knowing’)" }
        ]
      },
      {
        "i": 10,
        "deva": "आवृत्य",
        "iast": "āvṛtya",
        "gloss": "having covered over, having veiled",
        "stem": null,
        "root": "√vṛ (kryādi, 9U)",
        "rootGloss": "to cover, to enclose, to veil, to shut in",
        "affix": "lyap (kṛt — ktvā after a prefixed root)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same kartṛ (eṣaḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ā-", "gloss": "all over, right around" },
          { "form": "√vṛ", "gloss": "to cover, to enclose, to veil" },
          { "form": "-ya", "gloss": "(lyap: ‘having —ed’, the absolutive used when the root carries a prefix)" }
        ],
        "note": "The absolutive fixes the order of operations: the covering comes first, the delusion follows from it. Śaṅkara glosses it ācchādya, ‘having screened off’."
      },
      {
        "i": 11,
        "deva": "देहिनम्",
        "iast": "dehinam",
        "gloss": "the embodied one, the one who has a body",
        "stem": "dehin",
        "root": null,
        "affix": "ini (taddhita) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of vimohayati",
        "glossaryKey": "dehin",
        "translatable": true,
        "parts": [
          { "form": "deha", "gloss": "body" },
          { "form": "-in", "gloss": "(taddhita ini: ‘the one who has —’)" }
        ],
        "note": "Śaṅkara glosses it śarīrin, ‘the one possessed of a body’; Rāmānuja prakṛti-saṃsṛṣṭa, ‘the one bound up with prakṛti’."
      }
    ],
    "grammar": {
      "karakaSummary": "Two sentences. First: indriyāṇi, manaḥ, buddhiḥ — kartṛ of the passive ucyate; adhiṣṭhānam — predicate nominative (with which the verb agrees, hence the singular); asya — sambandha. Second: eṣaḥ — kartṛ of vimohayati; dehinam — karman; etaiḥ — karaṇa; jñānam — karman of the absolutive āvṛtya, which fixes the covering as prior to the deluding.",
      "verbalModality": "A passive present (ucyate) reporting settled usage, then a causative present (vimohayati) for what kāma actively does. The switch from ‘is said’ to ‘this one deludes’ is the verse turning from a definition into an account of an attack."
    }
  },

  {
    "locus": "3.41",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "तस्मात्त्वमिन्द्रियाण्यादौ नियम्य भरतर्षभ।\nपाप्मानं प्रजहि ह्येनं ज्ञानविज्ञाननाशनम्॥",
    "iast": "tasmāt tvam indriyāṇy ādau niyamya bharatarṣabha |\npāpmānaṃ prajahi hy enaṃ jñāna-vijñāna-nāśanam ||",
    "sense": "The instruction that follows from it: take the outposts first — rein in the indriyas — and then cast off the evil thing that destroys both knowledge and the discernment of it.",
    "english": "{0:Therefore} {1:you}, {3:at the outset} {4:having reined in} {2:the indriyas}, {5:O bull of the Bharatas} — {8:do} {7:cast off} {9:this} {6:evil one}, {10:the destroyer of knowledge and of discernment}.",
    "words": [
      {
        "i": 0,
        "deva": "तस्मात्",
        "iast": "tasmāt",
        "gloss": "therefore, from that",
        "stem": "tad",
        "root": null,
        "affix": "ṅasi (pañcamī ekavacana)",
        "morph": "abl. sg. neut.",
        "karaka": "hetu in the ablative (‘it being so’)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "tad", "gloss": "that, it (the anaphoric demonstrative)" },
          { "form": "-smāt", "gloss": "(ablative singular of the pronominal declension: ‘from that’)" }
        ]
      },
      {
        "i": 1,
        "deva": "त्वम्",
        "iast": "tvam",
        "gloss": "you",
        "stem": "yuṣmad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg.",
        "karaka": "kartṛ of prajahi (expressed, though the imperative already carries it)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "yuṣmad", "gloss": "you (the second-person stem)" }
        ],
        "note": "The pronoun is not needed grammatically; it is there for emphasis — you, Arjuna, are the one who must do this."
      },
      {
        "i": 2,
        "deva": "इन्द्रियाणि",
        "iast": "indriyāṇi",
        "gloss": "the indriyas — the powers of sense and action",
        "stem": "indriya",
        "root": null,
        "affix": "śas (dvitīyā bahuvacana)",
        "morph": "acc. pl. neut.",
        "karaka": "karman of niyamya",
        "glossaryKey": "indriya",
        "translatable": false,
        "parts": [
          { "form": "indra", "gloss": "Indra; the lord, the ruling power" },
          { "form": "-iya", "gloss": "(taddhita ghac: ‘belonging to Indra’ — hence a power of the indwelling ruler)" }
        ],
        "sandhi": "indriyāṇy ādau ← indriyāṇi + ādau (i → y before a dissimilar vowel)"
      },
      {
        "i": 3,
        "deva": "आदौ",
        "iast": "ādau",
        "gloss": "at the outset, first of all",
        "stem": "ādi",
        "root": null,
        "affix": "ṅi (saptamī ekavacana)",
        "morph": "loc. sg. masc.",
        "karaka": "adhikaraṇa of time (‘at the beginning’)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ādi", "gloss": "beginning, start; the first of a series" },
          { "form": "-au", "gloss": "(locative singular: ‘in, at’)" }
        ],
        "note": "Śaṅkara reads it pūrvam eva, ‘right at the start’; Rāmānuja mokṣopāya-ārambha-samaya eva, ‘at the very moment of beginning the means to liberation’. The word is doing strategic work — this is the first move, not one move among others."
      },
      {
        "i": 4,
        "deva": "नियम्य",
        "iast": "niyamya",
        "gloss": "having reined in, having brought under control",
        "stem": null,
        "root": "√yam (bhvādi, 1P)",
        "rootGloss": "to hold, to hold in, to check, to restrain (the image is of reins)",
        "affix": "lyap (kṛt — ktvā after a prefixed root)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same kartṛ (tvam)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ni-", "gloss": "down, in; holding down and in" },
          { "form": "√yam", "gloss": "to hold, to check, to rein in" },
          { "form": "-ya", "gloss": "(lyap: ‘having —ed’, the absolutive used when the root carries a prefix)" }
        ],
        "note": "Śaṅkara glosses it vaśīkṛtya, ‘having brought under your sway’."
      },
      {
        "i": 5,
        "deva": "भरतर्षभ",
        "iast": "bharatarṣabha",
        "gloss": "O bull of the Bharatas",
        "stem": "bharata-ṛṣabha",
        "root": null,
        "affix": "su (sambodhana prathamā ekavacana)",
        "morph": "voc. sg. masc.",
        "karaka": "āmantraṇa (the one addressed)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī)",
          "vigraha": "bharatānām ṛṣabhaḥ",
          "members": ["bharata", "ṛṣabha"]
        },
        "parts": [
          { "form": "bharata", "gloss": "Bharata; the line descended from him" },
          { "form": "ṛṣabha", "gloss": "a bull; by extension, the best and strongest of a kind" }
        ],
        "sandhi": "bharatarṣabha ← bharata + ṛṣabha (a + ṛ → ar)"
      },
      {
        "i": 6,
        "deva": "पाप्मानम्",
        "iast": "pāpmānam",
        "gloss": "the evil one, the thing that is evil",
        "stem": "pāpman",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of prajahi",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "pāpa", "gloss": "evil, bad, wrong" },
          { "form": "-man", "gloss": "(manin, forming the masculine noun: ‘the evil one’)" }
        ],
        "note": "Śaṅkara glosses it pāpācāraṃ kāmam — ‘kāma, whose conduct is evil’; the epithet from 3.37 (mahā-pāpmā) returns here as the name."
      },
      {
        "i": 7,
        "deva": "प्रजहि",
        "iast": "prajahi",
        "gloss": "cast off!, throw away!",
        "stem": null,
        "root": "√hā (juhotyādi, 3P)",
        "rootGloss": "to leave, to abandon, to let go, to give up",
        "affix": "hi (loṭ, madhyama-puruṣa ekavacana)",
        "morph": "2nd sg. imperative parasmaipada",
        "karaka": "the verb; kartṛ tvam, karman pāpmānam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "pra-", "gloss": "forth, away (throwing clean away)" },
          { "form": "√hā", "gloss": "to leave, to abandon, to let go" },
          { "form": "ja-", "gloss": "(the reduplicating syllable of the juhotyādi present)" },
          { "form": "-hi", "gloss": "(the 2nd-singular imperative ending)" }
        ],
        "note": "Śaṅkara reads the form as prajahihi and glosses parityaja, ‘let it go entirely’ — an abandoning, not a killing. The killing word comes only at 3.43 (jahi, √han)."
      },
      {
        "i": 8,
        "deva": "हि",
        "iast": "hi",
        "gloss": "surely, indeed",
        "stem": "hi",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable emphatic particle",
        "karaka": "— (emphasis on the imperative)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "hi", "gloss": "for, indeed, surely (enclitic — never first in its clause)" }
        ],
        "sandhi": "prajahi hy enam ← prajahi hi + enam (i → y before a dissimilar vowel)"
      },
      {
        "i": 9,
        "deva": "एनम्",
        "iast": "enam",
        "gloss": "this one, him (the one under discussion)",
        "stem": "enad (the enclitic anaphoric)",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of prajahi, in apposition to pāpmānam",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "enad", "gloss": "him, this one (the unstressed anaphoric pronoun, only ever non-initial)" }
        ]
      },
      {
        "i": 10,
        "deva": "ज्ञानविज्ञाननाशनम्",
        "iast": "jñāna-vijñāna-nāśanam",
        "gloss": "the destroyer of knowledge and of discernment",
        "stem": "jñāna-vijñāna-nāśana",
        "root": "√naś (divādi, 4P)",
        "rootGloss": "to perish, to be lost, to vanish; (causative) to destroy",
        "affix": "lyuṭ (kṛt) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "attribute of pāpmānam / enam",
        "glossaryKey": "jnana",
        "translatable": true,
        "compound": {
          "type": "tatpuruṣa (ṣaṣṭhī), with a dvandva first member",
          "vigraha": "jñānaṃ ca vijñānaṃ ca jñāna-vijñāne; tayor nāśanam",
          "members": ["jñāna", "vijñāna", "nāśana"]
        },
        "parts": [
          { "form": "jñāna", "gloss": "knowledge, the knowing" },
          { "form": "vijñāna", "gloss": "discernment — knowledge that distinguishes, taken to its particular case" },
          { "form": "√naś", "gloss": "to perish, to be lost; (causative) to destroy" },
          { "form": "-ana", "gloss": "(lyuṭ, here agentive: ‘what destroys’)" }
        ],
        "note": "The two commentators divide the pair differently. Śaṅkara: jñāna is what one comes to understand of the self from śāstra and teacher, vijñāna the particular first-hand experience of it. Rāmānuja: jñāna has the self's own nature for its object, vijñāna the discriminating of it. Both keep vijñāna as the finer, more particular knowing — which is why it is rendered by a different English word than jñāna, not by the same one twice."
      }
    ],
    "grammar": {
      "karakaSummary": "One imperative sentence with a subordinate absolutive clause. tasmāt — hetu in the ablative; tvam — kartṛ, expressed for emphasis; indriyāṇi — karman of the absolutive niyamya; ādau — adhikaraṇa of time; bharatarṣabha — āmantraṇa (voc.); pāpmānam, enam and jñāna-vijñāna-nāśanam — one karman of prajahi, named three times over.",
      "verbalModality": "One finite verb, and it is an imperative (loṭ) — the first thing in this passage Arjuna is told to do. The absolutive niyamya subordinates the reining-in to it, so the verse also states the order: the indriyas first, then the enemy behind them."
    }
  },

  {
    "locus": "3.42",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "इन्द्रियाणि पराण्याहुरिन्द्रियेभ्यः परं मनः।\nमनसस्तु परा बुद्धिर्यो बुद्धेः परतस्तु सः॥",
    "iast": "indriyāṇi parāṇy āhur indriyebhyaḥ paraṃ manaḥ |\nmanasas tu parā buddhir yo buddheḥ paratas tu saḥ ||",
    "sense": "A ladder, each rung higher than the last: the indriyas, then manas, then buddhi — and then, unnamed, whatever stands beyond buddhi. The commentators divide sharply over what that last one is.",
    "english": "{1:Higher} {2:they call} {0:the indriyas}; {4:higher} {3:than the indriyas} {5:is manas}; {7:but} {8:higher} {6:than manas} {9:is buddhi}; {13:and} {10:he who} {12:is beyond} {11:buddhi} — {14:he}.",
    "words": [
      {
        "i": 0,
        "deva": "इन्द्रियाणि",
        "iast": "indriyāṇi",
        "gloss": "the indriyas — the powers of sense and action",
        "stem": "indriya",
        "root": null,
        "affix": "śas (dvitīyā bahuvacana)",
        "morph": "acc. pl. neut.",
        "karaka": "karman of āhuḥ",
        "glossaryKey": "indriya",
        "translatable": false,
        "parts": [
          { "form": "indra", "gloss": "Indra; the lord, the ruling power" },
          { "form": "-iya", "gloss": "(taddhita ghac: ‘belonging to Indra’ — hence a power of the indwelling ruler)" }
        ]
      },
      {
        "i": 1,
        "deva": "पराणि",
        "iast": "parāṇi",
        "gloss": "higher, beyond, superior",
        "stem": "para",
        "root": null,
        "affix": "śas (dvitīyā bahuvacana)",
        "morph": "acc. pl. neut.",
        "karaka": "predicate accusative with āhuḥ (‘call them —’)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "para", "gloss": "further, beyond, higher; other" }
        ],
        "note": "Śaṅkara supplies the comparison the verse leaves out: higher than the body — subtler, more inward, more pervading.",
        "sandhi": "parāṇy āhuḥ ← parāṇi + āhuḥ (i → y before a dissimilar vowel)"
      },
      {
        "i": 2,
        "deva": "आहुः",
        "iast": "āhuḥ",
        "gloss": "they say, they call",
        "stem": null,
        "root": "√brū (adādi, 2U)",
        "rootGloss": "to speak, to say, to declare, to call",
        "affix": "jhi (laṭ, prathama-puruṣa bahuvacana), with the āha- substitute of A 3.4.84 (brūñaḥ pañcānām ādita āhau bruvaḥ)",
        "morph": "3rd pl. pres. indic.",
        "karaka": "the verb; its kartṛ is unnamed — ‘they’, those who know",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "āha-", "gloss": "(the substitute stem prescribed for the first five endings of √brū)" },
          { "form": "-uḥ", "gloss": "(3rd person plural)" }
        ],
        "note": "The form looks like a perfect but is not: Pāṇini substitutes āha for bravī- in the first five present endings, so this is a present tense. Śaṅkara names the unnamed speakers: paṇḍitāḥ, those who have thought it through."
      },
      {
        "i": 3,
        "deva": "इन्द्रियेभ्यः",
        "iast": "indriyebhyaḥ",
        "gloss": "than the indriyas",
        "stem": "indriya",
        "root": null,
        "affix": "bhyas (pañcamī bahuvacana)",
        "morph": "abl. pl. neut.",
        "karaka": "the standard of comparison in the ablative (‘than’)",
        "glossaryKey": "indriya",
        "translatable": false,
        "parts": [
          { "form": "indra", "gloss": "Indra; the lord, the ruling power" },
          { "form": "-iya", "gloss": "(taddhita ghac: ‘belonging to Indra’ — hence a power of the indwelling ruler)" },
          { "form": "-bhyaḥ", "gloss": "(ablative plural: ‘from, than’)" }
        ]
      },
      {
        "i": 4,
        "deva": "परम्",
        "iast": "param",
        "gloss": "higher, beyond, superior",
        "stem": "para",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "predicate of manaḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "para", "gloss": "further, beyond, higher; other" }
        ]
      },
      {
        "i": 5,
        "deva": "मनः",
        "iast": "manaḥ",
        "gloss": "manas — the faculty that intends, hesitates and turns things over",
        "stem": "manas",
        "root": "√man (divādi, 4Ā)",
        "rootGloss": "to think, to consider, to have in mind, to deem",
        "affix": "asun (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. neut.",
        "karaka": "the subject of the implied copula",
        "glossaryKey": "manas",
        "translatable": false,
        "parts": [
          { "form": "√man", "gloss": "to think, to consider, to have in mind" },
          { "form": "-as", "gloss": "(asun, the neuter action/agent noun)" }
        ],
        "note": "Śaṅkara here gives the definition: saṅkalpa-vikalpātmaka — manas is what proposes and what doubts."
      },
      {
        "i": 6,
        "deva": "मनसः",
        "iast": "manasaḥ",
        "gloss": "than manas",
        "stem": "manas",
        "root": "√man (divādi, 4Ā)",
        "rootGloss": "to think, to consider, to have in mind, to deem",
        "affix": "ṅasi (pañcamī ekavacana)",
        "morph": "abl. sg. neut.",
        "karaka": "the standard of comparison in the ablative (‘than’)",
        "glossaryKey": "manas",
        "translatable": false,
        "parts": [
          { "form": "√man", "gloss": "to think, to consider, to have in mind" },
          { "form": "-as", "gloss": "(asun, the neuter action/agent noun)" },
          { "form": "-aḥ", "gloss": "(ablative singular: ‘from, than’)" }
        ]
      },
      {
        "i": 7,
        "deva": "तु",
        "iast": "tu",
        "gloss": "but, however",
        "stem": "tu",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adversative particle",
        "karaka": "— (marks the step up to buddhi as a distinct move)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "tu", "gloss": "but, however, on the other hand (enclitic — never first in its clause)" }
        ]
      },
      {
        "i": 8,
        "deva": "परा",
        "iast": "parā",
        "gloss": "higher, beyond, superior",
        "stem": "para",
        "root": null,
        "affix": "su (prathamā ekavacana), strī (ṭāp)",
        "morph": "nom. sg. fem.",
        "karaka": "predicate of buddhiḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "para", "gloss": "further, beyond, higher; other" },
          { "form": "-ā", "gloss": "(ṭāp, the feminine ending, agreeing with the feminine buddhi)" }
        ]
      },
      {
        "i": 9,
        "deva": "बुद्धिः",
        "iast": "buddhiḥ",
        "gloss": "buddhi — the faculty that discriminates and settles a matter",
        "stem": "buddhi",
        "root": "√budh (bhvādi, 1U)",
        "rootGloss": "to wake, to awaken; to be aware of, to understand, to notice",
        "affix": "ktin (kṛt) + su (prathamā ekavacana)",
        "morph": "nom. sg. fem.",
        "karaka": "the subject of the implied copula",
        "glossaryKey": "buddhi",
        "translatable": false,
        "parts": [
          { "form": "√budh", "gloss": "to wake, to be aware of, to understand" },
          { "form": "-ti", "gloss": "(ktin, the feminine action-noun: ‘the awakening / the understanding’)" }
        ],
        "note": "Śaṅkara here: niścayātmikā — buddhi is of the nature of settling what is the case."
      },
      {
        "i": 10,
        "deva": "यः",
        "iast": "yaḥ",
        "gloss": "he who, the one who",
        "stem": "yad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "kartṛ of the relative clause, answered by saḥ",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "yad", "gloss": "who, which (the relative stem)" }
        ],
        "note": "Masculine, where the three rungs below were neuter and feminine — the change of gender is itself part of what the commentators argue about."
      },
      {
        "i": 11,
        "deva": "बुद्धेः",
        "iast": "buddheḥ",
        "gloss": "than buddhi",
        "stem": "buddhi",
        "root": "√budh (bhvādi, 1U)",
        "rootGloss": "to wake, to awaken; to be aware of, to understand, to notice",
        "affix": "ṅasi (pañcamī ekavacana)",
        "morph": "abl. sg. fem.",
        "karaka": "the standard of comparison in the ablative (‘than’), governed by parataḥ",
        "glossaryKey": "buddhi",
        "translatable": false,
        "parts": [
          { "form": "√budh", "gloss": "to wake, to be aware of, to understand" },
          { "form": "-ti", "gloss": "(ktin, the feminine action-noun)" },
          { "form": "-eḥ", "gloss": "(ablative singular: ‘from, than’)" }
        ]
      },
      {
        "i": 12,
        "deva": "परतः",
        "iast": "parataḥ",
        "gloss": "beyond, further on",
        "stem": "para",
        "root": null,
        "affix": "tasil (taddhita) — avyaya",
        "morph": "indeclinable, with ablative force",
        "karaka": "— (adverbial; governs buddheḥ)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "para", "gloss": "further, beyond, higher; other" },
          { "form": "-tas", "gloss": "(taddhita tasil: ‘from —’, ‘on the — side’)" }
        ]
      },
      {
        "i": 13,
        "deva": "तु",
        "iast": "tu",
        "gloss": "but, and yet",
        "stem": "tu",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adversative particle",
        "karaka": "— (sets the fourth term apart from the three below it)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "tu", "gloss": "but, however, on the other hand (enclitic — never first in its clause)" }
        ]
      },
      {
        "i": 14,
        "deva": "सः",
        "iast": "saḥ",
        "gloss": "he, that one",
        "stem": "tad",
        "root": null,
        "affix": "su (prathamā ekavacana)",
        "morph": "nom. sg. masc.",
        "karaka": "the correlative answering yaḥ; predicate of the implied copula",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "tad", "gloss": "that, he (the correlative demonstrative)" }
        ],
        "note": "The verse simply says ‘he’ and stops, and the three commentators fill the blank in three different ways: for Śaṅkara it is the ātman, the seer of buddhi; for Rāmānuja it is kāma itself, which outranks buddhi because it can still move buddhi; for Madhva it is the paramātman, higher even than the unmanifest. The English keeps the blank."
      }
    ],
    "grammar": {
      "karakaSummary": "Line 1 is a transitive sentence: āhuḥ with an unnamed kartṛ, indriyāṇi as karman and parāṇi as predicate accusative. The rest is a chain of nominal sentences with an implied copula, each rung's standard of comparison in the ablative (indriyebhyaḥ, manasaḥ, buddheḥ) and each rung's name in the nominative (manaḥ, buddhiḥ). The last clause is a relative–correlative pair, yaḥ … saḥ, with no predicate noun at all.",
      "verbalModality": "One finite verb in the whole verse (āhuḥ, present), and it belongs to the reporting frame rather than to the ladder. What is being described is not an event but a standing order of things — hence the copula is left unsaid throughout."
    }
  },

  {
    "locus": "3.43",
    "speaker": "krishna",
    "meter": "anuṣṭubh",
    "devanagari": "एवं बुद्धेः परं बुद्ध्वा संस्तभ्यात्मानमात्मना।\nजहि शत्रुं महाबाहो कामरूपं दुरासदम्॥",
    "iast": "evaṃ buddheḥ paraṃ buddhvā saṃstabhyātmānam ātmanā |\njahi śatruṃ mahābāho kāma-rūpaṃ durāsadam ||",
    "sense": "The close of the chapter: know what stands above buddhi, hold yourself steady by yourself, and kill the enemy — the one shaped as kāma, that will not let itself be got at.",
    "english": "{0:Thus}, {3:having known} {2:what is higher} {1:than buddhi}, {4:having steadied} {5:the self} {6:by the self} — {7:slay} {8:the enemy}, {9:O mighty-armed one}, {10:whose form is kāma}, {11:hard to get at}.",
    "words": [
      {
        "i": 0,
        "deva": "एवम्",
        "iast": "evam",
        "gloss": "thus, in this way",
        "stem": "evam",
        "root": null,
        "affix": "— (nipāta; avyaya)",
        "morph": "indeclinable adverb of manner",
        "karaka": "— (gathers up what 3.42 has just laid out)",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "evam", "gloss": "thus, so, in this way" }
        ]
      },
      {
        "i": 1,
        "deva": "बुद्धेः",
        "iast": "buddheḥ",
        "gloss": "than buddhi",
        "stem": "buddhi",
        "root": "√budh (bhvādi, 1U)",
        "rootGloss": "to wake, to awaken; to be aware of, to understand, to notice",
        "affix": "ṅasi (pañcamī ekavacana)",
        "morph": "abl. sg. fem.",
        "karaka": "the standard of comparison in the ablative, governed by param",
        "glossaryKey": "buddhi",
        "translatable": false,
        "parts": [
          { "form": "√budh", "gloss": "to wake, to be aware of, to understand" },
          { "form": "-ti", "gloss": "(ktin, the feminine action-noun)" },
          { "form": "-eḥ", "gloss": "(ablative singular: ‘from, than’)" }
        ]
      },
      {
        "i": 2,
        "deva": "परम्",
        "iast": "param",
        "gloss": "what is higher, what lies beyond",
        "stem": "para",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of buddhvā",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "para", "gloss": "further, beyond, higher; other" }
        ],
        "note": "The same blank as at the end of 3.42, and filled the same three ways: Śaṅkara reads ātmānam, Rāmānuja kāmam, Madhva the paramātman."
      },
      {
        "i": 3,
        "deva": "बुद्ध्वा",
        "iast": "buddhvā",
        "gloss": "having known, having come to understand",
        "stem": null,
        "root": "√budh (bhvādi, 1U)",
        "rootGloss": "to wake, to awaken; to be aware of, to understand, to notice",
        "affix": "ktvā (kṛt)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same kartṛ as jahi",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "√budh", "gloss": "to wake, to be aware of, to understand" },
          { "form": "-tvā", "gloss": "(ktvā: ‘having —ed’, the absolutive of an unprefixed root)" }
        ],
        "note": "Śaṅkara glosses it jñātvā. The waking sense of the root is not dead in it: the knowing here is a coming-to, not a piece of information."
      },
      {
        "i": 4,
        "deva": "संस्तभ्य",
        "iast": "saṃstabhya",
        "gloss": "having steadied, having made firm",
        "stem": null,
        "root": "√stambh (kryādi, 9P)",
        "rootGloss": "to prop, to make firm, to hold fast, to stiffen",
        "affix": "lyap (kṛt — ktvā after a prefixed root)",
        "morph": "indeclinable absolutive",
        "karaka": "prior action of the same kartṛ as jahi",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "sam-", "gloss": "together, fully, thoroughly" },
          { "form": "√stambh", "gloss": "to prop, to make firm, to hold fast" },
          { "form": "-ya", "gloss": "(lyap: ‘having —ed’, the absolutive used when the root carries a prefix)" }
        ],
        "sandhi": "saṃstabhyātmānam ← saṃstabhya + ātmānam (a + ā → ā)",
        "note": "Śaṅkara: samyak stambhanaṃ kṛtvā — having made it fully firm; and he reads the result as samādhāya, a gathering of the manas into composure."
      },
      {
        "i": 5,
        "deva": "आत्मानम्",
        "iast": "ātmānam",
        "gloss": "the self",
        "stem": "ātman",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of saṃstabhya",
        "glossaryKey": "atman",
        "translatable": true,
        "parts": [
          { "form": "ātman", "gloss": "the self; oneself" }
        ],
        "note": "Both Śaṅkara and Rāmānuja read this first ātman as the manas, and Madhva says so in as many words — ātmānaṃ manaḥ. The word in the verse is ātman all the same, and stays so here."
      },
      {
        "i": 6,
        "deva": "आत्मना",
        "iast": "ātmanā",
        "gloss": "by the self",
        "stem": "ātman",
        "root": null,
        "affix": "ṭā (tṛtīyā ekavacana)",
        "morph": "instr. sg. masc.",
        "karaka": "karaṇa of saṃstabhya",
        "glossaryKey": "atman",
        "translatable": true,
        "parts": [
          { "form": "ātman", "gloss": "the self; oneself" },
          { "form": "-ā", "gloss": "(instrumental singular: ‘by, with’)" }
        ],
        "note": "The second ātman is read differently by each: Śaṅkara, by one's own manas once it has been refined; Rāmānuja and Madhva, by the buddhi. The verse itself repeats one word, and the repetition is the point — the steadying has no instrument outside the one being steadied."
      },
      {
        "i": 7,
        "deva": "जहि",
        "iast": "jahi",
        "gloss": "slay!, strike down!",
        "stem": null,
        "root": "√han (adādi, 2P)",
        "rootGloss": "to strike, to kill, to slay, to destroy",
        "affix": "hi (loṭ, madhyama-puruṣa ekavacana), with han → ja by A 6.4.36 (hanter jaḥ)",
        "morph": "2nd sg. imperative parasmaipada",
        "karaka": "the verb; kartṛ Arjuna (understood), karman śatrum",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "ja-", "gloss": "(the substitute Pāṇini prescribes for han before this imperative ending)" },
          { "form": "-hi", "gloss": "(the 2nd-singular imperative ending)" }
        ],
        "note": "3.41 said prajahi, ‘cast it off’ (√hā). This is a different root and a harder word: √han, to kill. The chapter ends by escalating from abandonment to killing."
      },
      {
        "i": 8,
        "deva": "शत्रुम्",
        "iast": "śatrum",
        "gloss": "the enemy, the foe",
        "stem": "śatru",
        "root": "√śad (bhvādi, 1P)",
        "rootGloss": "to fall, to fall away, to perish",
        "affix": "ru (kṛt, uṇādi) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "karman of jahi",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "√śad", "gloss": "to fall, to fall away, to perish" },
          { "form": "-tru", "gloss": "(the uṇādi affix: ‘the one who makes another fall’)" }
        ]
      },
      {
        "i": 9,
        "deva": "महाबाहो",
        "iast": "mahābāho",
        "gloss": "O mighty-armed one",
        "stem": "mahā-bāhu",
        "root": null,
        "affix": "su (sambodhana prathamā ekavacana)",
        "morph": "voc. sg. masc.",
        "karaka": "āmantraṇa (the one addressed)",
        "glossaryKey": null,
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "mahāntau bāhū yasya saḥ",
          "members": ["mahat", "bāhu"]
        },
        "parts": [
          { "form": "mahā-", "gloss": "great, vast (the compounding form of mahat)" },
          { "form": "bāhu", "gloss": "arm" }
        ],
        "note": "The epithet is chosen for the sentence it sits in: the arm that is being called great is being told to strike."
      },
      {
        "i": 10,
        "deva": "कामरूपम्",
        "iast": "kāma-rūpam",
        "gloss": "whose form is kāma",
        "stem": "kāma-rūpa",
        "root": null,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "attribute of śatrum",
        "glossaryKey": "kama",
        "translatable": true,
        "compound": {
          "type": "bahuvrīhi",
          "vigraha": "kāma eva rūpaṃ yasya saḥ — tam",
          "members": ["kāma", "rūpa"]
        },
        "parts": [
          { "form": "kāma", "gloss": "kāma — desire as craving, the wanting that reaches for its object" },
          { "form": "rūpa", "gloss": "form, shape; the visible aspect a thing has" }
        ]
      },
      {
        "i": 11,
        "deva": "दुरासदम्",
        "iast": "durāsadam",
        "gloss": "hard to get at, hard to come up against",
        "stem": "durāsada",
        "root": "√sad (bhvādi, 1P)",
        "rootGloss": "to sit, to settle; with ā-: to approach, to reach, to come at",
        "affix": "khal (kṛt, after dur-) + am (dvitīyā ekavacana)",
        "morph": "acc. sg. masc.",
        "karaka": "attribute of śatrum",
        "glossaryKey": null,
        "translatable": true,
        "parts": [
          { "form": "dur-", "gloss": "hard to —, ill, difficult (dus- before a vowel)" },
          { "form": "ā-", "gloss": "up to, towards" },
          { "form": "√sad", "gloss": "to sit, to settle; to approach, to reach" },
          { "form": "-a", "gloss": "(khal, the kṛt affix that makes ‘hard to be —ed’)" }
        ],
        "note": "Śaṅkara's gloss is exactly the compound taken apart — duḥkhena āsadaḥ āsādanaṃ prāptir yasya, ‘the one whose being-reached is got only with difficulty’ — and he adds why: it has endless forms, and they are hard to tell apart."
      }
    ],
    "grammar": {
      "karakaSummary": "One imperative sentence with two absolutive clauses before it. jahi — the finite verb, with Arjuna as unstated kartṛ; śatrum (with kāma-rūpam and durāsadam attributive to it) — karman; mahābāho — āmantraṇa (voc.). In the subordinate clauses: param — karman of buddhvā, with buddheḥ as its ablative of comparison; ātmānam — karman of saṃstabhya; ātmanā — its karaṇa.",
      "verbalModality": "One finite verb, an imperative (loṭ), held back to the last line and preceded by two absolutives — so the verse states its two conditions (know, and steady yourself) before it issues the order. The chapter ends on a command, not a description."
    }
  }
];
