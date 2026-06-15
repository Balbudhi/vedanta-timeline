/* =============================================================
   Bhagavad-Gītā 2.54–72 — "Across traditions" parallels.
   window.GITA_PARALLELS — keyed by verse locus.

   These are NOT Gītā commentary. Each entry is a DIFFERENT text in
   another tradition that describes the SAME state — the realized one
   (sthitaprajña / jīvanmukta / vītarāga / arahant) — mapped to the
   Gītā verse it most closely illuminates.

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
      source: "data/sources/sanskrit/vedanta/full_corpus/shankara_vivekacudamani_gretil.txt (v. 426)"
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "1.15",
      sanskrit: "dṛṣṭānuśravikaviṣayavitṛṣṇasya vaśīkārasaṃjñā vairāgyam ||",
      ourRendering: "Dispassion (vairāgya) is the mark of mastery in one who has ceased to thirst for objects seen or heard-of.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 1.15)"
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
      source: "data/sources/pali/suttacentral/dhammapada_arahantavagga_90-99_root-pli-ms.json (dhp 99)"
    },
    {
      school: "Jainism",
      thinker: "Uttarādhyayana",
      work: "Uttarajjhayā (Uttarādhyayana-sūtra), ch. 32 Pamāyaṭhāṇa",
      locus: "32.100",
      sanskrit: "evindiyatthā ya maṇassa atthā | dukkhassa heuṃ maṇuyassa rāgiṇo | te ceva thovaṃ pi kayāi dukkhaṃ | na vīyarāgassa karenti kiṃci ||",
      ourRendering: "Thus the objects of the senses and the objects of the mind are a cause of suffering for the man who has passion (rāgin); those very same objects never cause the passion-free one (vītarāga) the least suffering.",
      source: "data/sources/prakrit/jaina/uttarajjhaya_gretil_plaintext.txt (Uttar 32.100)"
    },
    {
      school: "Advaita Vedānta",
      thinker: "attributed to Śaṅkara",
      work: "Vivekacūḍāmaṇi",
      locus: "434",
      sanskrit: "iṣṭāniṣṭārthasamprāptau samadarśitayātmani | ubhayatrāvikāritvaṃ jīvanmuktasya lakṣaṇam ||",
      ourRendering: "When the welcome and the unwelcome arrive, to remain unchanged toward both, even-sighted in oneself — that is the mark of one liberated while living.",
      source: "data/sources/sanskrit/vedanta/full_corpus/shankara_vivekacudamani_gretil.txt (v. 434)"
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
      source: "data/sources/pali/suttacentral/dhammapada_arahantavagga_90-99_root-pli-ms.json (dhp 95)"
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
      sanskrit: "kummova aṅgāni sake kapāle, samodahaṃ bhikkhu manovitakke; anissito aññamaheṭhayāno, parinibbuto nūpavadeyya kañci.",
      ourRendering: "As a tortoise its limbs within its own shell, let the monk gather in the mind's stirrings; unsupported, harming no other, fully quenched, let him reproach no one.",
      source: "data/sources/pali/suttacentral/sn35.240_kummopamasutta_root-pli-ms.json (SN 35.240, closing verse)"
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "2.54",
      sanskrit: "svaviṣayāsaṃprayoge cittasvarūpānukāra ivendriyāṇāṃ pratyāhāraḥ ||",
      ourRendering: "Withdrawal (pratyāhāra) is the senses' disengagement from their own objects, as if conforming to the nature of the mind itself.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 2.54)"
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
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 1.16)"
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
      source: "data/sources/pali/suttacentral/dhammapada_arahantavagga_90-99_root-pli-ms.json (dhp 94)"
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "2.55",
      sanskrit: "tataḥ paramā vaśyatendriyāṇām ||",
      ourRendering: "From that [withdrawal] comes the supreme mastery of the senses.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 2.55)"
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
      source: "data/sources/pali/suttacentral/dhammapada_arahantavagga_90-99_root-pli-ms.json (dhp 96)"
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "1.33",
      sanskrit: "maitrīkaruṇāmuditopekṣāṇāṃ sukhaduḥkhapuṇyāpuṇyaviṣayāṇāṃ bhāvanātaś cittaprasādanam ||",
      ourRendering: "By cultivating friendliness, compassion, gladness and equanimity toward the happy, the suffering, the meritorious and the unmeritorious, the mind becomes serene.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 1.33)"
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
      source: "data/sources/sanskrit/vedanta/full_corpus/shankara_vivekacudamani_gretil.txt (v. 431)"
    },
    {
      school: "Jainism",
      thinker: "Uttarādhyayana",
      work: "Uttarajjhayā (Uttarādhyayana-sūtra), ch. 32 Pamāyaṭhāṇa",
      locus: "32.99",
      sanskrit: "bhāve viratto maṇuo visogo | eeṇa dukkhohaparaṃpareṇa | na lippaī bhavamajjhe vi santo | jaleṇa vā pokkhariṇīpalāsaṃ ||",
      ourRendering: "The man detached from objects, free of sorrow, is not stained by this succession of floods of suffering — though present in the very midst of existence — just as a lotus-pond's leaf is not stained by water.",
      source: "data/sources/prakrit/jaina/uttarajjhaya_gretil_plaintext.txt (Uttar 32.99)"
    }
  ],

  // 2.72 — "This is the state grounded in Brahman, Pārtha; reaching it one is
  //         not deluded. Standing in it even at the last hour, one attains
  //         extinction in Brahman."
  "2.72": [
    {
      school: "Trika (Pratyabhijñā)",
      thinker: "Kṣemarāja",
      work: "Pratyabhijñāhṛdaya",
      locus: "sūtra 16",
      sanskrit: "cidānandalābhe dehādiṣu cetyamāneṣv api cidaikātmyapratipattidārḍhyaṃ jīvanmuktiḥ ||",
      ourRendering: "When the bliss of consciousness is attained, the firm conviction of oneness with consciousness — even while body and the rest are still being experienced — is liberation-while-living.",
      source: "data/sources/sanskrit/kashmir_shaiva/ksemaraja_pratyabhijna_hrdayam.txt (PH sūtra 16)"
    },
    {
      school: "Yoga (Pātañjala)",
      thinker: "Patañjali",
      work: "Yoga-sūtra",
      locus: "4.34",
      sanskrit: "puruṣārthaśūnyānāṃ guṇānāṃ pratiprasavaḥ kaivalyaṃ svarūpapratiṣṭhā vā citiśaktir iti ||",
      ourRendering: "Aloneness (kaivalya) is the return of the guṇas, now empty of any purpose for the puruṣa, to their source — or, the power of pure consciousness standing firm in its own nature.",
      source: "data/sources/sanskrit/comparator/patanjali_yoga_sutra.txt (ys 4.34)"
    }
  ]

};
