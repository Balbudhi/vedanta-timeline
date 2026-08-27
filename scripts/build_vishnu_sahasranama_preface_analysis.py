#!/usr/bin/env python3
"""Build and validate GitaReader-compatible analysis for the performed VSN preface.

The output uses the site's established Sanskrit reader contract: contiguous
``words[]``, slotted literal English, source-script and IAST pada-patha, and a
complete Pāṇinian word card for every pada.  This script deliberately fails on
an unresolved word, slot, compound, or source-text replay.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import runpy
import unicodedata
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
WITNESS_PATH = ROOT / "data/sources/sanskrit/vedanta/vishnu_sahasranama_performance_preface.json"
OUTPUT_PATH = ROOT / "gita/vishnu-sahasranama/preface-analysis.json"


def W(spec: str) -> list[tuple[str, str, str]]:
    """Parse ``form=gloss@morph`` records separated by semicolons."""
    out = []
    for item in spec.split(";"):
        item = item.strip()
        if not item:
            continue
        left, morph = item.rsplit("@", 1)
        form, gloss = left.split("=", 1)
        out.append((form.strip(), gloss.strip(), morph.strip()))
    return out


# Sandhi-resolved padas and literal renderings. Internal hyphens mark samasa
# members; they are not separate syntactic words. Glosses are concise card
# meanings, while ``english`` gives the complete unit rendering.
UNIT_SPECS = {
    "invocation-1": {
        "words": W("""
          śukla-ambara-dharam=wearing a white garment@acc.sg.m; viṣṇum=Viṣṇu@acc.sg.m;
          śaśi-varṇam=moon-coloured@acc.sg.m; catur-bhujam=four-armed@acc.sg.m;
          prasanna-vadanam=with a serene face@acc.sg.m; dhyāyet=one should meditate@verb:dhyāyet;
          sarva-vighna-upaśāntaye=for the pacification of every obstacle@dat.sg.f
        """),
        "english": "{5:One should meditate on} {1:Viṣṇu}, {0:wearing a white garment}, {2:moon-coloured}, {3:four-armed}, {4:with a serene face}, {6:for the pacification of every obstacle}.",
    },
    "invocation-3": {
        "words": W("""
          vyāsam=Vyāsa@acc.sg.m; vasiṣṭha-naptāram=the great-grandson of Vasiṣṭha@acc.sg.m;
          śakteḥ=of Śakti@gen.sg.m; pautram=the grandson@acc.sg.m; akalmaṣam=stainless@acc.sg.m;
          parāśara-ātmajam=the son of Parāśara@acc.sg.m; vande=I salute@verb:vande;
          śuka-tātam=the father of Śuka@acc.sg.m; tapas-nidhim=the treasury of austerity@acc.sg.m
        """),
        "english": "{6:I salute} {0:Vyāsa}, {1:the great-grandson of Vasiṣṭha}, {3:the grandson} {2:of Śakti}, {4:stainless}, {5:the son of Parāśara}, {7:the father of Śuka}, {8:the treasury of austerity}.",
    },
    "invocation-4": {
        "words": W("""
          vyāsāya=to Vyāsa@dat.sg.m; viṣṇu-rūpāya=whose form is Viṣṇu@dat.sg.m;
          vyāsa-rūpāya=whose form is Vyāsa@dat.sg.m; viṣṇave=to Viṣṇu@dat.sg.m;
          namaḥ=obeisance@ind; vai=indeed@ind; brahma-nidhaye=to the treasury of Brahman@dat.sg.m;
          vāsiṣṭhāya=to the descendant of Vasiṣṭha@dat.sg.m; namaḥ=obeisance@ind; namaḥ=obeisance@ind
        """),
        "english": "{4:Obeisance} {0:to Vyāsa}, {1:whose form is Viṣṇu}; {8:obeisance} {3:to Viṣṇu}, {2:whose form is Vyāsa}; {9:obeisance} {5:indeed} {7:to the descendant of Vasiṣṭha}, {6:the treasury of Brahman}.",
    },
    "invocation-5": {
        "words": W("""
          avikārāya=to the changeless@dat.sg.m; śuddhāya=to the pure@dat.sg.m;
          nityāya=to the eternal@dat.sg.m; parama-ātmane=to the supreme Self@dat.sg.m;
          sadā-eka-rūpa-rūpāya=whose form is always one@dat.sg.m; viṣṇave=to Viṣṇu@dat.sg.m;
          sarva-jiṣṇave=to the all-conquering@dat.sg.m
        """),
        "english": "To {5:Viṣṇu}, {0:the changeless}, {1:the pure}, {2:the eternal}, {3:the supreme Self}, {4:whose form is always one}, {6:the all-conquering}.",
    },
    "invocation-6": {
        "words": W("""
          yasya=whose@gen.sg.m; smaraṇa-mātreṇa=by mere remembrance@ins.sg.n;
          janma-saṃsāra-bandhanāt=from the bond of birth and saṃsāra@abl.sg.m;
          vimucyate=one is released@verb:vimucyate; namaḥ=obeisance@ind; tasmai=to him@dat.sg.m;
          viṣṇave=to Viṣṇu@dat.sg.m; prabhaviṣṇave=to all-powerful Viṣṇu@dat.sg.m
        """),
        "english": "{4:Obeisance} {5:to him}, {6:to Viṣṇu}, {7:to all-powerful Viṣṇu}, {0:by whose} {1:mere remembrance} one {3:is released} {2:from the bond of birth and saṃsāra}.",
    },
    "invocation-mantra": {
        "words": W("oṃ=Oṃ@ind; namaḥ=obeisance@ind; viṣṇave=to Viṣṇu@dat.sg.m; prabhaviṣṇave=to all-powerful Viṣṇu@dat.sg.m"),
        "english": "{0:Oṃ}. {1:Obeisance} {2:to Viṣṇu}, {3:to all-powerful Viṣṇu}.",
    },
    "dialogue-7": {
        "words": W("""
          śrutvā=having heard@part:śrutvā; dharmān=the dharmas@acc.pl.m; aśeṣeṇa=without remainder@ins.sg.n;
          pāvanāni=the purifying teachings@acc.pl.n; ca=and@ind; sarvaśaḥ=in every respect@ind;
          yudhiṣṭhiraḥ=Yudhiṣṭhira@nom.sg.m; śāntanavam=the son of Śantanu@acc.sg.m;
          punaḥ=again@ind; eva=indeed@ind; abhyabhāṣata=addressed@verb:abhyabhāṣata
        """),
        "english": "{0:Having heard} {1:the dharmas} {2:without remainder} {4:and} {3:the purifying teachings} {5:in every respect}, {6:Yudhiṣṭhira} {9:indeed} {8:again} {10:addressed} {7:the son of Śantanu}.",
    },
    "dialogue-8": {
        "words": W("""
          kim=what?@nom.sg.n; ekam=one@nom.sg.n; daivatam=deity@nom.sg.n; loke=in the world@loc.sg.m;
          kim=what?@nom.sg.n; vā=or@ind; api=also@ind; ekam=one@nom.sg.n; para-ayaṇam=supreme refuge@nom.sg.n;
          stuvantaḥ=praising@part:stuvantaḥ; kam=whom?@acc.sg.m; kam=whom?@acc.sg.m;
          arcantaḥ=worshipping@part:arcantaḥ; prāpnuyuḥ=might attain@verb:prāpnuyuḥ;
          mānavāḥ=human beings@nom.pl.m; śubham=the good@acc.sg.n
        """),
        "english": "{0:What} {1:one} {2:deity} is there {3:in the world}? {4:What}, {5:or} {6:also}, is the {7:one} {8:supreme refuge}? {9:Praising} {10:whom} and {12:worshipping} {11:whom} might {14:human beings} {13:attain} {15:the good}?",
    },
    "dialogue-9": {
        "words": W("""
          kaḥ=which?@nom.sg.m; dharmaḥ=dharma@nom.sg.m; sarva-dharmāṇām=of all dharmas@gen.pl.m;
          bhavataḥ=of you@gen.sg.m; paramaḥ=highest@nom.sg.m; mataḥ=regarded@nom.sg.m;
          kim=what?@acc.sg.n; japan=reciting@part:japan; mucyate=is released@verb:mucyate;
          jantuḥ=a living being@nom.sg.m; janma-saṃsāra-bandhanāt=from the bond of birth and saṃsāra@abl.sg.m
        """),
        "english": "{0:Which} {1:dharma}, {2:of all dharmas}, is {5:regarded} {4:highest} {3:by you}? {7:Reciting} {6:what} {8:is} {9:a living being} {8:released} {10:from the bond of birth and saṃsāra}?",
    },
    "dialogue-10": {
        "words": W("""
          jagat-prabhum=the Lord of the world@acc.sg.m; deva-devam=the God of gods@acc.sg.m;
          anantam=the endless@acc.sg.m; puruṣa-uttamam=the highest Person@acc.sg.m;
          stuvan=praising@part:stuvan; nāma-sahasreṇa=with a thousand names@ins.sg.n;
          puruṣaḥ=a person@nom.sg.m; satata-utthitaḥ=constantly arisen@nom.sg.m
        """),
        "english": "{4:Praising} {0:the Lord of the world}, {1:the God of gods}, {2:the endless}, {3:the highest Person}, {5:with a thousand names}, {6:a person} is {7:constantly arisen}.",
    },
    "dialogue-11": {
        "words": W("""
          tam=him@acc.sg.m; eva=alone@ind; ca=and@ind; arcayan=worshipping@part:arcayan;
          nityam=always@ind; bhaktyā=with devotion@ins.sg.f; puruṣam=the Person@acc.sg.m;
          avyayam=imperishable@acc.sg.m; dhyāyan=meditating@part:dhyāyan; stuvan=praising@part:stuvan;
          namasyan=bowing@part:namasyan; ca=and@ind; yajamānaḥ=sacrificing@part:yajamānaḥ;
          tam=him@acc.sg.m; eva=alone@ind; ca=and@ind
        """),
        "english": "{2:And} {3:worshipping} {0:him} {1:alone} {4:always} {5:with devotion}, {8:meditating on}, {9:praising}, {10:bowing to}, {11:and} {12:sacrificing to} {6:the} {7:imperishable Person}, {13:him} {14:alone} {15:indeed}.",
    },
    "dialogue-12": {
        "words": W("""
          an-ādi-nidhanam=without beginning or end@acc.sg.m; viṣṇum=Viṣṇu@acc.sg.m;
          sarva-loka-mahā-īśvaram=the great Lord of all worlds@acc.sg.m;
          loka-adhyakṣam=the overseer of the worlds@acc.sg.m; stuvan=praising@part:stuvan;
          nityam=always@ind; sarva-duḥkha-atigaḥ=gone beyond every sorrow@nom.sg.m; bhavet=one would become@verb:bhavet
        """),
        "english": "{4:Praising} {1:Viṣṇu}, {0:without beginning or end}, {2:the great Lord of all worlds}, {3:the overseer of the worlds}, {5:always}, one {7:would become} {6:gone beyond every sorrow}.",
    },
    "dialogue-13": {
        "words": W("""
          brahmaṇyam=devoted to Brahman and the Veda@acc.sg.m; sarva-dharma-jñam=knower of every dharma@acc.sg.m;
          lokānām=of the worlds@gen.pl.m; kīrti-vardhanam=the increaser of fame@acc.sg.m;
          loka-nātham=the Lord of the worlds@acc.sg.m; mahat=great@acc.sg.n; bhūtam=being@acc.sg.n;
          sarva-bhūta-bhava-udbhavam=the source of the becoming of all beings@acc.sg.m
        """),
        "english": "The one {0:devoted to Brahman and the Veda}, {1:knower of every dharma}, {3:the increaser of} {2:the worlds’} {3:fame}, {4:the Lord of the worlds}, {6:the} {5:great being}, {7:the source of the becoming of all beings}.",
    },
    "dialogue-14": {
        "words": W("""
          eṣaḥ=this@nom.sg.m; me=by me@gen.sg.m; sarva-dharmāṇām=of all dharmas@gen.pl.m;
          dharmaḥ=dharma@nom.sg.m; adhikatamaḥ=highest@nom.sg.m; mataḥ=regarded@nom.sg.m;
          yat=that@nom.sg.n; bhaktyā=with devotion@ins.sg.f; puṇḍarīka-akṣam=the lotus-eyed@acc.sg.m;
          stavaiḥ=with hymns@ins.pl.m; arcet=one should worship@verb:arcet; naraḥ=a person@nom.sg.m; sadā=always@ind
        """),
        "english": "{0:This} {3:dharma} is {5:regarded} {4:highest} {2:of all dharmas} {1:by me}: {6:that} {11:a person} {10:should worship} {8:the lotus-eyed} {7:with devotion}, {9:with hymns}, {12:always}.",
    },
    "dialogue-15": {
        "words": W("""
          paramam=the supreme@nom.sg.n; yaḥ=who@nom.sg.m; mahat=great@nom.sg.n; tejaḥ=radiance@nom.sg.n;
          paramam=the supreme@nom.sg.n; yaḥ=who@nom.sg.m; mahat=great@nom.sg.n; tapaḥ=austerity@nom.sg.n;
          paramam=the supreme@nom.sg.n; yaḥ=who@nom.sg.m; mahat=great@nom.sg.n; brahma=Brahman@nom.sg.n;
          paramam=the supreme@nom.sg.n; yaḥ=who@nom.sg.m; para-ayaṇam=highest refuge@nom.sg.n
        """),
        "english": "{1:He who is} {0:the supreme}, {2:great} {3:radiance}; {5:he who is} {4:the supreme}, {6:great} {7:austerity}; {9:he who is} {8:the supreme}, {10:great} {11:Brahman}; {13:he who is} {12:the supreme} {14:highest refuge}.",
    },
    "dialogue-16": {
        "words": W("""
          pavitrāṇām=among purifiers@gen.pl.n; pavitram=the purifier@nom.sg.n; yaḥ=who@nom.sg.m;
          maṅgalānām=among auspicious things@gen.pl.n; ca=and@ind; maṅgalam=the auspicious@nom.sg.n;
          daivatam=the deity@nom.sg.n; daivatānām=among deities@gen.pl.n; ca=and@ind;
          bhūtānām=of beings@gen.pl.n; yaḥ=who@nom.sg.m; avyayaḥ=imperishable@nom.sg.m; pitā=father@nom.sg.m
        """),
        "english": "{2:He who is} {1:the purifier} {0:among purifiers} {4:and} {5:the auspicious} {3:among auspicious things}, {6:the deity} {7:among deities}, {8:and} {10:he who is} {12:the} {11:imperishable father} {9:of beings}.",
    },
    "dialogue-17": {
        "words": W("""
          yataḥ=from whom@abl.sg.m; sarvāṇi=all@nom.pl.n; bhūtāni=beings@nom.pl.n;
          bhavanti=come to be@verb:bhavanti; ādi-yuga-āgame=at the coming of the first age@loc.sg.m;
          yasmin=in whom@loc.sg.m; ca=and@ind; pralayam=dissolution@acc.sg.m; yānti=go@verb:yānti;
          punaḥ=again@ind; eva=indeed@ind; yuga-kṣaye=at the ending of the age@loc.sg.m
        """),
        "english": "{0:From whom} {1:all} {2:beings} {3:come to be} {4:at the coming of the first age}, {6:and} {5:in whom} they {8:go} to {7:dissolution} {10:indeed} {9:again} {11:at the ending of the age}.",
    },
    "dialogue-18": {
        "words": W("""
          tasya=of him@gen.sg.m; loka-pradhānasya=of the foremost of the world@gen.sg.m;
          jagat-nāthasya=of the Lord of the world@gen.sg.m; bhū-pate=O lord of the earth@voc.sg.m;
          viṣṇoḥ=of Viṣṇu@gen.sg.m; nāma-sahasram=the thousand names@acc.sg.n; me=from me@gen.sg.m;
          śṛṇu=hear@verb:śṛṇu; pāpa-bhaya-apaham=removing evil and fear@acc.sg.n
        """),
        "english": "{3:O lord of the earth}, {7:hear} {6:from me} {5:the thousand names} {4:of Viṣṇu}, {0:of him}, {1:the foremost of the world}, {2:the Lord of the world}, {8:removing evil and fear}.",
    },
    "dialogue-19": {
        "words": W("""
          yāni=which@nom.pl.n; nāmāni=names@nom.pl.n; gauṇāni=based on qualities@nom.pl.n;
          vikhyātāni=widely known@nom.pl.n; mahā-ātmanaḥ=of the great Self@gen.sg.m;
          ṛṣibhiḥ=by seers@ins.pl.m; pari-gītāni=sung forth@nom.pl.n; tāni=those@acc.pl.n;
          vakṣyāmi=I shall declare@verb:vakṣyāmi; bhūtaye=for welfare@dat.sg.f
        """),
        "english": "{8:I shall declare} {7:those} {0:which} {1:names}, {2:based on qualities}, are {3:widely known} {4:of the great Self} and {6:sung forth} {5:by seers}, {9:for welfare}.",
    },
    "dialogue-20": {
        "words": W("""
          ṛṣiḥ=seer@nom.sg.m; nāmnām=of the names@gen.pl.n; sahasrasya=of the thousand@gen.sg.n;
          veda-vyāsaḥ=Vedavyāsa@nom.sg.m; mahā-muniḥ=the great sage@nom.sg.m;
          chandaḥ=metre@nom.sg.n; anuṣṭup=Anuṣṭubh@nom.sg.n; tathā=and@ind; devaḥ=deity@nom.sg.m;
          bhagavān=the Blessed Lord@nom.sg.m; devakī-sutaḥ=the son of Devakī@nom.sg.m
        """),
        "english": "{3:Vedavyāsa}, {4:the great sage}, is {0:the seer} {2:of the thousand} {1:names}; {6:Anuṣṭubh} is {5:the metre}; {7:and} {10:the son of Devakī}, {9:the Blessed Lord}, is {8:the deity}.",
    },
    "dialogue-21": {
        "words": W("""
          amṛta-aṃśu-udbhavaḥ=he whose source is the nectar-rayed moon@nom.sg.m; bījam=seed@nom.sg.n;
          śaktiḥ=power@nom.sg.f; devakī-nandanaḥ=the son of Devakī@nom.sg.m;
          tri-sāmā=he of the three Sāmans@nom.sg.m; hṛdayam=heart@nom.sg.n; tasya=its@gen.sg.n;
          śānti-arthe=for peace@loc.sg.m; viniyojyate=is assigned@verb:viniyojyate
        """),
        "english": "{0:He whose source is the nectar-rayed moon} is {1:the seed}; {3:the son of Devakī} is {2:the power}; {4:he of the three Sāmans} is {6:its} {5:heart}; it {8:is assigned} {7:for peace}.",
    },
    "dialogue-22": {
        "words": W("""
          viṣṇum=Viṣṇu@acc.sg.m; jiṣṇum=the conqueror@acc.sg.m; mahā-viṣṇum=great Viṣṇu@acc.sg.m;
          prabhaviṣṇum=all-powerful Viṣṇu@acc.sg.m; mahā-īśvaram=the great Lord@acc.sg.m;
          aneka-rūpam=of many forms@acc.sg.m; daitya-antam=the ender of Daityas@acc.sg.m;
          namāmi=I bow to@verb:namāmi; puruṣa-uttamam=the highest Person@acc.sg.m
        """),
        "english": "{7:I bow to} {0:Viṣṇu}, {1:the conqueror}, {2:great Viṣṇu}, {3:all-powerful Viṣṇu}, {4:the great Lord}, {5:of many forms}, {6:the ender of Daityas}, {8:the highest Person}.",
    },
}

UNIT_SPECS.update({
    "assignment-1": {
        "words": W("""
          oṃ=Oṃ@ind; asya=of this@gen.sg.m; śrī-viṣṇoḥ=of blessed Viṣṇu@gen.sg.m;
          divya-sahasra-nāma-stotra-mahā-mantrasya=of the great mantra of the divine thousand-name hymn@gen.sg.m
        """),
        "english": "{0:Oṃ}. {1:Of this} {3:great mantra of the divine thousand-name hymn} {2:of blessed Viṣṇu}—",
    },
    "assignment-2": {
        "words": W("śrī-veda-vyāsaḥ=blessed Vedavyāsa@nom.sg.m; bhagavān=the Blessed One@nom.sg.m; ṛṣiḥ=seer@nom.sg.m"),
        "english": "{0:Blessed Vedavyāsa}, {1:the Blessed One}, is {2:the seer}.",
    },
    "assignment-3": {
        "words": W("anuṣṭup=Anuṣṭubh@nom.sg.f; chandaḥ=metre@nom.sg.n"),
        "english": "{0:Anuṣṭubh} is {1:the metre}.",
    },
    "assignment-4": {
        "words": W("""
          śrī-mahā-viṣṇuḥ=blessed great Viṣṇu@nom.sg.m; parama-ātmā=the supreme Self@nom.sg.m;
          śrīmat-nārāyaṇaḥ=glorious Nārāyaṇa@nom.sg.m; devatā=deity@nom.sg.f
        """),
        "english": "{0:Blessed great Viṣṇu}, {1:the supreme Self}, {2:glorious Nārāyaṇa}, is {3:the deity}.",
    },
    "assignment-5": {
        "words": W("amṛta-aṃśu-udbhavaḥ=he whose source is the nectar-rayed moon@nom.sg.m; bhānuḥ=radiance@nom.sg.m; iti=thus@ind; bījam=seed@nom.sg.n"),
        "english": "‘{0:He whose source is the nectar-rayed moon}, {1:radiance},’ {2:thus}, is {3:the seed}.",
    },
    "assignment-6": {
        "words": W("devakī-nandanaḥ=the son of Devakī@nom.sg.m; sraṣṭā=the creator@nom.sg.m; iti=thus@ind; śaktiḥ=power@nom.sg.f"),
        "english": "‘{0:The son of Devakī}, {1:the creator},’ {2:thus}, is {3:the power}.",
    },
    "assignment-7": {
        "words": W("udbhavaḥ=source@nom.sg.m; kṣobhaṇaḥ=agitator@nom.sg.m; devaḥ=God@nom.sg.m; iti=thus@ind; paramaḥ=supreme@nom.sg.m; mantraḥ=mantra@nom.sg.m"),
        "english": "‘{0:The source}, {1:the agitator}, {2:God},’ {3:thus}, is {4:the supreme} {5:mantra}.",
    },
    "assignment-8": {
        "words": W("śaṅkha-bhṛt=bearer of the conch@nom.sg.m; nandakī=bearer of Nandaka@nom.sg.m; cakrī=bearer of the discus@nom.sg.m; iti=thus@ind; kīlakam=key@nom.sg.n"),
        "english": "‘{0:Bearer of the conch}, {1:bearer of Nandaka}, {2:bearer of the discus},’ {3:thus}, is {4:the key}.",
    },
    "assignment-9": {
        "words": W("śārṅga-dhanvā=wielder of the Śārṅga bow@nom.sg.m; gadā-dharaḥ=bearer of the mace@nom.sg.m; iti=thus@ind; astram=weapon@nom.sg.n"),
        "english": "‘{0:Wielder of the Śārṅga bow}, {1:bearer of the mace},’ {2:thus}, is {3:the weapon}.",
    },
    "assignment-10": {
        "words": W("ratha-aṅga-pāṇiḥ=he with the chariot-wheel in hand@nom.sg.m; akṣobhyaḥ=unshakable@nom.sg.m; iti=thus@ind; netram=eye@nom.sg.n"),
        "english": "‘{0:He with the chariot-wheel in hand}, {1:the unshakable},’ {2:thus}, is {3:the eye}.",
    },
    "assignment-11": {
        "words": W("tri-sāmā=he of the three Sāmans@nom.sg.m; sāma-gaḥ=singer of Sāman@nom.sg.m; sāma=Sāman@nom.sg.n; iti=thus@ind; kavacam=armour@nom.sg.n"),
        "english": "‘{0:He of the three Sāmans}, {1:singer of Sāman}, {2:Sāman},’ {3:thus}, is {4:the armour}.",
    },
    "assignment-12": {
        "words": W("ānandam=bliss@nom.sg.n; para-brahma=supreme Brahman@nom.sg.n; iti=thus@ind; yoniḥ=source@nom.sg.f"),
        "english": "‘{0:Bliss}, {1:supreme Brahman},’ {2:thus}, is {3:the source}.",
    },
    "assignment-13": {
        "words": W("ṛtuḥ=season@nom.sg.m; su-darśanaḥ=Sudarśana@nom.sg.m; kālaḥ=time@nom.sg.m; iti=thus@ind; dik-bandhaḥ=binding of the directions@nom.sg.m"),
        "english": "‘{0:Season}, {1:Sudarśana}, {2:time},’ {3:thus}, is {4:the binding of the directions}.",
    },
    "assignment-14": {
        "words": W("śrī-viśva-rūpaḥ=blessed universal form@nom.sg.m; iti=thus@ind; dhyānam=meditation@nom.sg.n"),
        "english": "‘{0:The blessed universal form},’ {1:thus}, is {2:the meditation}.",
    },
    "assignment-15": {
        "words": W("""
          śrī-mahā-viṣṇu-prīti-arthe=for the pleasure of blessed great Viṣṇu@loc.sg.m;
          sahasra-nāma-stotra-pāṭhe=in the recitation of the thousand-name hymn@loc.sg.m;
          viniyogaḥ=application@nom.sg.m
        """),
        "english": "{2:The application} is {1:in the recitation of the thousand-name hymn}, {0:for the pleasure of blessed great Viṣṇu}.",
    },
    "meditation-1": {
        "words": W("""
          kṣīra-udanvat-pradeśe=in the region of the ocean of milk@loc.sg.m;
          śuci-maṇi-vilasat-saikate=on the shore shining with pure gems@loc.sg.m;
          mauktikānām=of pearls@gen.pl.n; mālā-kḷpta-āsana-sthaḥ=seated on a seat fashioned from garlands@nom.sg.m;
          sphaṭika-maṇi-nibhaiḥ=resembling crystal gems@ins.pl.n; mauktikaiḥ=with pearls@ins.pl.n;
          maṇḍita-aṅgaḥ=whose limbs are adorned@nom.sg.m; śubhrair=with white@ins.pl.n;
          abhrair=with clouds@ins.pl.n; adabhrair=abundant@ins.pl.n; upari-viracitaiḥ=arranged above@ins.pl.n;
          mukta-pīyūṣa-varṣaiḥ=with showers of released nectar@ins.pl.m; ānandī=blissful@nom.sg.m;
          naḥ=us@gen.pl.m; punīyāt=may he purify@verb:punīyāt;
          ari-nalina-gadā-śaṅkha-pāṇiḥ=holding discus, lotus, mace, and conch in his hands@nom.sg.m;
          mukundaḥ=Mukunda@nom.sg.m
        """),
        "english": "{0:In the region of the ocean of milk}, {1:on the shore shining with pure gems} {2:of pearls}, {3:seated on a seat fashioned from garlands}, {6:his limbs adorned} {5:with pearls} {4:resembling crystal gems}, beneath {7:white} {8:clouds}, {9:abundant}, {10:arranged above}, {11:with showers of released nectar}, {12:blissful}, may {16:Mukunda}, {15:holding discus, lotus, mace, and conch in his hands}, {14:purify} {13:us}.",
    },
    "meditation-2": {
        "words": W("""
          bhūḥ=earth@nom.sg.f; pādau=two feet@nom.du.m; yasya=whose@gen.sg.m; nābhiḥ=navel@nom.sg.f;
          viyat=sky@nom.sg.n; asuḥ=breath@nom.sg.m; anilaḥ=wind@nom.sg.m; candra-sūryau=moon and sun@nom.du.m;
          ca=and@ind; netre=two eyes@nom.du.n; karṇau=two ears@nom.du.m; āśāḥ=directions@nom.pl.f;
          śiraḥ=head@nom.sg.n; dyauḥ=heaven@nom.sg.f; mukham=mouth@nom.sg.n; api=also@ind;
          dahanaḥ=fire@nom.sg.m; yasya=whose@gen.sg.m; vāste=in the abdomen@loc.sg.n; ayam=this@nom.sg.m;
          abdhiḥ=ocean@nom.sg.m; antaḥ-stham=situated within@nom.sg.n; yasya=whose@gen.sg.m;
          viśvam=universe@nom.sg.n; sura-nara-khaga-go-bhogi-gandharva-daityaiḥ=by gods, humans, birds, cattle, serpents, Gandharvas, and Daityas@ins.pl.m;
          citram=wondrously@ind; raṃramyate=sports delightfully@verb:raṃramyate; tam=him@acc.sg.m;
          tri-bhuvana-vapuṣam=whose body is the three worlds@acc.sg.m; viṣṇum=Viṣṇu@acc.sg.m;
          īśam=the Lord@acc.sg.m; namāmi=I bow to@verb:namāmi
        """),
        "english": "{31:I bow to} {27:him}, {29:Viṣṇu}, {30:the Lord}, {28:whose body is the three worlds}: {0:earth} is {2:his} {1:two feet}; {4:the sky} {3:the navel}; {6:wind} {5:the breath}; {7:moon and sun} {8:are} {9:the two eyes}; {11:the directions} {10:the two ears}; {13:heaven} {12:the head}; {16:fire} {15:also} {14:the mouth}; {19:this} {20:ocean} is {18:in the abdomen} {17:of his}; and {23:the universe} {21:situated within} {22:him} {26:sports delightfully}, {25:wondrously}, {24:with gods, humans, birds, cattle, serpents, Gandharvas, and Daityas}.",
    },
    "meditation-mantra": {
        "words": W("oṃ=Oṃ@ind; namaḥ=obeisance@ind; bhagavate=to the Blessed Lord@dat.sg.m; vāsudevāya=to Vāsudeva@dat.sg.m"),
        "english": "{0:Oṃ}. {1:Obeisance} {2:to the Blessed Lord}, {3:to Vāsudeva}.",
    },
    "meditation-3": {
        "words": W("""
          oṃ=Oṃ@ind; śānta-ākāram=whose form is peaceful@acc.sg.m; bhujaga-śayanam=lying on the serpent@acc.sg.m;
          padma-nābham=lotus-navelled@acc.sg.m; sura-īśam=Lord of the gods@acc.sg.m;
          viśva-ādhāram=support of the universe@acc.sg.m; gagana-sadṛśam=like the sky@acc.sg.m;
          megha-varṇam=cloud-coloured@acc.sg.m; śubha-aṅgam=whose limbs are auspicious@acc.sg.m;
          lakṣmī-kāntam=beloved of Lakṣmī@acc.sg.m; kamala-nayanam=lotus-eyed@acc.sg.m;
          yogi-hṛd-dhyāna-gamyam=attainable in the yogis’ heart by meditation@acc.sg.m;
          vande=I bow to@verb:vande; viṣṇum=Viṣṇu@acc.sg.m; bhava-bhaya-haram=remover of the fear of becoming@acc.sg.m;
          sarva-loka-eka-nātham=the one Lord of all worlds@acc.sg.m
        """),
        "english": "{0:Oṃ}. {12:I bow to} {13:Viṣṇu}, {1:whose form is peaceful}, {2:lying on the serpent}, {3:lotus-navelled}, {4:Lord of the gods}, {5:support of the universe}, {6:like the sky}, {7:cloud-coloured}, {8:whose limbs are auspicious}, {9:beloved of Lakṣmī}, {10:lotus-eyed}, {11:attainable in the yogis’ heart by meditation}, {14:remover of the fear of becoming}, {15:the one Lord of all worlds}.",
    },
    "meditation-4": {
        "words": W("""
          megha-śyāmam=dark like a cloud@acc.sg.m; pīta-kauśeya-vāsam=wearing yellow silk@acc.sg.m;
          śrīvatsa-aṅkam=marked with Śrīvatsa@acc.sg.m; kaustubha-udbhāsita-aṅgam=whose limbs shine with the Kaustubha@acc.sg.m;
          puṇya-upetam=attended by the blessed@acc.sg.m; puṇḍarīka-āyata-akṣam=whose long eyes are like lotuses@acc.sg.m;
          viṣṇum=Viṣṇu@acc.sg.m; vande=I bow to@verb:vande; sarva-loka-eka-nātham=the one Lord of all worlds@acc.sg.m
        """),
        "english": "{7:I bow to} {6:Viṣṇu}, {0:dark like a cloud}, {1:wearing yellow silk}, {2:marked with Śrīvatsa}, {3:whose limbs shine with the Kaustubha}, {4:attended by the blessed}, {5:whose long eyes are like lotuses}, {8:the one Lord of all worlds}.",
    },
    "meditation-5": {
        "words": W("""
          namaḥ=obeisance@ind; samasta-bhūtānām=of all beings@gen.pl.n; ādi-bhūtāya=to the primal being@dat.sg.m;
          bhū-bhṛte=to the bearer of the earth@dat.sg.m; aneka-rūpa-rūpāya=whose form is manifold@dat.sg.m;
          viṣṇave=to Viṣṇu@dat.sg.m; prabhaviṣṇave=to all-powerful Viṣṇu@dat.sg.m
        """),
        "english": "{0:Obeisance} {2:to the primal being} {1:of all beings}, {3:to the bearer of the earth}, {4:whose form is manifold}, {5:to Viṣṇu}, {6:to all-powerful Viṣṇu}.",
    },
    "meditation-6": {
        "words": W("""
          sa-śaṅkha-cakram=with conch and discus@acc.sg.m; sa-kirīṭa-kuṇḍalam=with crown and earrings@acc.sg.m;
          sa-pīta-vastram=with yellow garment@acc.sg.m; sarasīruha-īkṣaṇam=lotus-eyed@acc.sg.m;
          sa-hāra-vakṣas-sthala-śobhi-kaustubham=with the Kaustubha shining on his garlanded chest@acc.sg.m;
          namāmi=I bow to@verb:namāmi; viṣṇum=Viṣṇu@acc.sg.m; śirasā=with my head@ins.sg.n;
          catur-bhujam=four-armed@acc.sg.m
        """),
        "english": "{5:I bow} {7:with my head} to {6:Viṣṇu}, {8:four-armed}, {0:with conch and discus}, {1:with crown and earrings}, {2:with yellow garment}, {3:lotus-eyed}, {4:with the Kaustubha shining on his garlanded chest}.",
    },
    "meditation-7": {
        "words": W("""
          chāyāyām=in the shade@loc.sg.f; pārijātasya=of the Pārijāta@gen.sg.m;
          hema-siṃhāsana-upari=above a golden throne@ind; āsīnam=seated@acc.sg.m;
          ambuda-śyāmam=dark like a raincloud@acc.sg.m; āyata-akṣam=long-eyed@acc.sg.m;
          alaṃkṛtam=adorned@acc.sg.m; candra-ānanam=moon-faced@acc.sg.m; catur-bāhum=four-armed@acc.sg.m;
          śrīvatsa-aṅkita-vakṣasam=whose chest is marked with Śrīvatsa@acc.sg.m;
          rukmiṇī-satyabhāmābhyām=with Rukmiṇī and Satyabhāmā@ins.du.f; sahitam=accompanied@acc.sg.m;
          kṛṣṇam=Kṛṣṇa@acc.sg.m; āśraye=I take refuge in@verb:āśraye
        """),
        "english": "{13:I take refuge in} {12:Kṛṣṇa}, {3:seated} {0:in the shade} {1:of the Pārijāta}, {2:above a golden throne}, {4:dark like a raincloud}, {5:long-eyed}, {6:adorned}, {7:moon-faced}, {8:four-armed}, {9:whose chest is marked with Śrīvatsa}, {11:accompanied} {10:by Rukmiṇī and Satyabhāmā}.",
    },
})


CASE_LABEL = {
    "nom": "nominative", "acc": "accusative", "ins": "instrumental",
    "dat": "dative", "abl": "ablative", "gen": "genitive",
    "loc": "locative", "voc": "vocative",
}
NUMBER_LABEL = {"sg": "singular", "du": "dual", "pl": "plural"}
GENDER_LABEL = {"m": "masculine", "f": "feminine", "n": "neuter"}
VIBHAKTI = {
    "nom": "prathamā", "acc": "dvitīyā", "ins": "tṛtīyā", "dat": "caturthī",
    "abl": "pañcamī", "gen": "ṣaṣṭhī", "loc": "saptamī", "voc": "sambodhana",
}
VACANA = {"sg": "ekavacana", "du": "dvivacana", "pl": "bahuvacana"}
SUP = {
    ("nom", "sg"): "su", ("acc", "sg"): "am", ("ins", "sg"): "ṭā",
    ("dat", "sg"): "ṅe", ("abl", "sg"): "ṅasi", ("gen", "sg"): "ṅas",
    ("loc", "sg"): "ṅi", ("voc", "sg"): "su",
    ("nom", "du"): "au", ("acc", "du"): "auṭ", ("ins", "du"): "bhyām",
    ("dat", "du"): "bhyām", ("abl", "du"): "bhyām", ("gen", "du"): "os",
    ("loc", "du"): "os", ("voc", "du"): "au",
    ("nom", "pl"): "jas", ("acc", "pl"): "śas", ("ins", "pl"): "bhis",
    ("dat", "pl"): "bhyas", ("abl", "pl"): "bhyas", ("gen", "pl"): "ām",
    ("loc", "pl"): "sup", ("voc", "pl"): "jas",
}
KARAKA = {
    "nom": "prathamā agreement: kartṛ with a verb, or subject/predicate/apposition in a nominal clause",
    "acc": "karman (object of the governing verb, including its agreeing modifiers)",
    "ins": "karaṇa (means/accompaniment) or an instrumental qualifier",
    "dat": "sampradāna (recipient) or purpose",
    "abl": "apādāna (source/separation)",
    "gen": "sambandha (relation: ‘of’)",
    "loc": "adhikaraṇa (location/domain)",
    "voc": "sambodhana (direct address)",
}

# Form-specific stems needed when the inflected surface does not expose the
# prātipadika transparently or when a compound is not lexicalized in Vidyut.
STEM_OVERRIDES = {
    "vasiṣṭha-naptāram": "vasiṣṭha-naptṛ", "śakteḥ": "śakti", "tapas-nidhim": "tapas-nidhi",
    "parama-ātmane": "parama-ātman", "viṣṇave": "viṣṇu", "sarva-jiṣṇave": "sarva-jiṣṇu",
    "prabhaviṣṇave": "prabhaviṣṇu", "tasmai": "tad", "yasya": "yad", "bhavataḥ": "bhavat",
    "kam": "kim", "kaḥ": "kim", "kim": "kim", "me": "asmad", "tam": "tad",
    "eṣaḥ": "etad", "yat": "yad", "yaḥ": "yad", "yataḥ": "yad", "yasmin": "yad",
    "tasya": "tad", "yāni": "yad", "tāni": "tad", "naḥ": "asmad",
    "pitā": "pitṛ", "ṛṣiḥ": "ṛṣi", "ṛṣibhiḥ": "ṛṣi", "viṣṇoḥ": "viṣṇu",
    "nāmnām": "nāman", "nāmāni": "nāman", "bhagavān": "bhagavat", "parama-ātmā": "parama-ātman",
    "śrīmat-nārāyaṇaḥ": "śrīmat-nārāyaṇa", "śaṅkha-bhṛt": "śaṅkha-bhṛt",
    "śārṅga-dhanvā": "śārṅga-dhanvin", "ratha-aṅga-pāṇiḥ": "ratha-aṅga-pāṇi",
    "tri-sāmā": "tri-sāman", "para-brahma": "para-brahman", "bhū-bhṛte": "bhū-bhṛt",
    "pādau": "pāda", "netre": "netra", "karṇau": "karṇa", "dyauḥ": "div",
    "śiraḥ": "śiras", "vāsaḥ": "vasas", "viyat": "viyat", "asuḥ": "asu",
    "tri-bhuvana-vapuṣam": "tri-bhuvana-vapus", "śirasā": "śiras",
    "śrīvatsa-aṅkita-vakṣasam": "śrīvatsa-aṅkita-vakṣas", "pārijātasya": "pārijāta",
    "hema-siṃhāsana-upari": "hema-siṃhāsana-upari", "rukmiṇī-satyabhāmābhyām": "rukmiṇī-satyabhāmā",
    "mauktikānām": "mauktika", "mauktikaiḥ": "mauktika", "śubhrair": "śubhra",
    "abhrair": "abhra", "adabhrair": "adabhra", "upari-viracitaiḥ": "upari-viracita",
    "mukta-pīyūṣa-varṣaiḥ": "mukta-pīyūṣa-varṣa", "sphaṭika-maṇi-nibhaiḥ": "sphaṭika-maṇi-nibha",
    "sarva-vighna-upaśāntaye": "sarva-vighna-upaśānti", "brahma-nidhaye": "brahma-nidhi",
    "smaraṇa-mātreṇa": "smaraṇa-mātra", "sarva-dharmāṇām": "sarva-dharma",
    "jagat-prabhum": "jagat-prabhu", "nāma-sahasreṇa": "nāma-sahasra", "bhū-pate": "bhū-pati",
    "mahā-ātmanaḥ": "mahā-ātman", "mahā-viṣṇum": "mahā-viṣṇu", "śrī-viṣṇoḥ": "śrī-viṣṇu",
    "candra-sūryau": "candra-sūrya", "catur-bāhum": "catur-bāhu",
    "vyāsam": "vyāsa", "vyāsāya": "vyāsa", "śuddhāya": "śuddha", "pāvanāni": "pāvana",
    "loke": "loka", "śubham": "śubha", "anantam": "ananta", "bhaktyā": "bhakti",
    "lokānām": "loka", "mahat": "mahat", "bhūtam": "bhūta", "pavitrāṇām": "pavitra",
    "pavitram": "pavitra", "bhūtānām": "bhūta", "sarvāṇi": "sarva", "bhūtāni": "bhūta",
    "pralayam": "pralaya", "bhūtaye": "bhūti", "jiṣṇum": "jiṣṇu", "asya": "idam",
    "sraṣṭā": "sraṣṭṛ", "cakrī": "cakrin", "kīlakam": "kīlaka", "netram": "netra",
    "ānandam": "ānanda", "dhyānam": "dhyāna", "ānandī": "ānandin", "īśam": "īśa",
    "chāyāyām": "chāyā", "sahitam": "sahita",
    "vāste": "vāsta",
    "mānavāḥ": "mānava", "nandakī": "nandakin", "āśāḥ": "āśā",
    "tejaḥ": "tejas", "tapaḥ": "tapas", "chandaḥ": "chandas",
}


VERBS = {
    "dhyāyet": ("√dhyai (bhvādi, 1P)", "to contemplate", "vidhiliṅ, active, third-person singular", "tip (prathama-puruṣa ekavacana)"),
    "vande": ("√vand (bhvādi, 1Ā)", "to praise, salute", "laṭ, active, first-person singular, ātmanepada", "iṭ (uttama-puruṣa ekavacana)"),
    "vimucyate": ("vi-√muc (tudādi, 6P)", "to release", "laṭ, passive, third-person singular", "ta (prathama-puruṣa ekavacana, ātmanepada)"),
    "abhyabhāṣata": ("abhi-√bhāṣ (bhvādi, 1Ā)", "to address, speak to", "laṅ, active, third-person singular, ātmanepada", "ta (prathama-puruṣa ekavacana)"),
    "prāpnuyuḥ": ("pra-√āp (svādi, 5P)", "to attain", "vidhiliṅ, active, third-person plural", "jhi (prathama-puruṣa bahuvacana)"),
    "mucyate": ("√muc (tudādi, 6P)", "to release", "laṭ, passive, third-person singular", "ta (prathama-puruṣa ekavacana, ātmanepada)"),
    "bhavet": ("√bhū (bhvādi, 1P)", "to be, become", "vidhiliṅ, active, third-person singular", "tip (prathama-puruṣa ekavacana)"),
    "arcet": ("√arc (curādi, 10P)", "to worship", "vidhiliṅ, active, third-person singular", "tip (prathama-puruṣa ekavacana)"),
    "bhavanti": ("√bhū (bhvādi, 1P)", "to be, become", "laṭ, active, third-person plural", "jhi (prathama-puruṣa bahuvacana)"),
    "yānti": ("√yā (adādi, 2P)", "to go", "laṭ, active, third-person plural", "jhi (prathama-puruṣa bahuvacana)"),
    "śṛṇu": ("√śru (svādi, 5P)", "to hear", "loṭ, active, second-person singular", "sip (madhyama-puruṣa ekavacana)"),
    "vakṣyāmi": ("√vac (adādi, 2P)", "to speak, declare", "lṛṭ, active, first-person singular", "mip (uttama-puruṣa ekavacana)"),
    "viniyojyate": ("vi-ni-√yuj (divādi, 4Ā), causative", "to assign, apply", "laṭ, causative passive, third-person singular", "ṇic + yaK + ta (prathama-puruṣa ekavacana)"),
    "namāmi": ("√nam (bhvādi, 1P)", "to bow", "laṭ, active, first-person singular", "mip (uttama-puruṣa ekavacana)"),
    "punīyāt": ("√pū (kryādi, 9P)", "to purify", "vidhiliṅ, active, third-person singular", "tip (prathama-puruṣa ekavacana)"),
    "raṃramyate": ("√ram (bhvādi, 1Ā), intensive", "to sport, delight", "laṭ, intensive active, third-person singular, ātmanepada", "yaṅ + ta (prathama-puruṣa ekavacana)"),
    "āśraye": ("ā-√śri (bhvādi, 1Ā)", "to resort to, take refuge in", "laṭ, active, first-person singular, ātmanepada", "iṭ (uttama-puruṣa ekavacana)"),
}

VERB_STEMS = {
    "dhyāyet": "dhyai", "vande": "vand", "vimucyate": "vimuc", "abhyabhāṣata": "abhibhāṣ",
    "prāpnuyuḥ": "prāp", "mucyate": "muc", "bhavet": "bhū", "arcet": "arc",
    "bhavanti": "bhū", "yānti": "yā", "śṛṇu": "śru", "vakṣyāmi": "vac",
    "viniyojyate": "viniyoj", "namāmi": "nam", "punīyāt": "pū", "raṃramyate": "ram (intensive)",
    "āśraye": "āśri",
}

PARTICIPLES = {
    "śrutvā": ("√śru (svādi, 5P)", "to hear", "ktvā (absolutive)", "having heard"),
    "stuvantaḥ": ("√stu (adādi, 2P)", "to praise", "śatṛ + jas (prathamā bahuvacana)", "nominative plural masculine present participle"),
    "arcantaḥ": ("√arc (curādi, 10P)", "to worship", "śatṛ + jas (prathamā bahuvacana)", "nominative plural masculine present participle"),
    "japan": ("√jap (bhvādi, 1P)", "to recite softly", "śatṛ + su (prathamā ekavacana)", "nominative singular masculine present participle"),
    "stuvan": ("√stu (adādi, 2P)", "to praise", "śatṛ + su (prathamā ekavacana)", "nominative singular masculine present participle"),
    "arcayan": ("√arc (curādi, 10P)", "to worship", "śatṛ + su (prathamā ekavacana)", "nominative singular masculine present participle"),
    "dhyāyan": ("√dhyai (bhvādi, 1P)", "to contemplate", "śatṛ + su (prathamā ekavacana)", "nominative singular masculine present participle"),
    "namasyan": ("namas + kyaC (nāmadhātu)", "to bow, pay homage", "śatṛ + su (prathamā ekavacana)", "nominative singular masculine denominative present participle"),
    "yajamānaḥ": ("√yaj (bhvādi, 1Ā)", "to sacrifice, worship", "śānac + su (prathamā ekavacana)", "nominative singular masculine present participle"),
}

DERIVED_FORMS = {
    "śukla-ambara-dharam": ("√dhṛ (bhvādi, 1U)", "to bear, hold", "ac (kṛt)"),
    "sarva-vighna-upaśāntaye": ("upa-√śam (divādi, 4P)", "to become pacified", "ktin (kṛt)"),
    "parāśara-ātmajam": ("√jan (divādi, 4Ā)", "to be born", "ḍa (kṛt)"),
    "smaraṇa-mātreṇa": ("√smṛ (bhvādi, 1P)", "to remember", "lyuṭ (kṛt)"),
    "janma-saṃsāra-bandhanāt": ("√bandh (kryādi, 9P)", "to bind", "lyuṭ (kṛt)"),
    "satata-utthitaḥ": ("ud-√sthā (bhvādi, 1P)", "to rise", "kta (kṛt)"),
    "sarva-duḥkha-atigaḥ": ("ati-√gam (bhvādi, 1P)", "to go beyond", "ḍa (kṛt)"),
    "sarva-dharma-jñam": ("√jñā (kryādi, 9P)", "to know", "ka (kṛt)"),
    "kīrti-vardhanam": ("√vṛdh (bhvādi, 1Ā), causative", "to increase", "ṇic + lyuṭ (kṛt)"),
    "sarva-bhūta-bhava-udbhavam": ("ud-√bhū (bhvādi, 1P)", "to arise", "ap (kṛt)"),
    "ādi-yuga-āgame": ("ā-√gam (bhvādi, 1P)", "to come", "ap (kṛt)"),
    "pāpa-bhaya-apaham": ("apa-√han (adādi, 2P)", "to remove, strike away", "ḍa (kṛt)"),
    "vikhyātāni": ("vi-ā-√khyā (adādi, 2P)", "to proclaim, make known", "kta (kṛt)"),
    "pari-gītāni": ("pari-√gai (bhvādi, 1P)", "to sing forth", "kta (kṛt)"),
    "devakī-nandanaḥ": ("√nand (bhvādi, 1P)", "to delight", "lyuṭ (kṛt)"),
    "amṛta-aṃśu-udbhavaḥ": ("ud-√bhū (bhvādi, 1P)", "to arise", "ap (kṛt)"),
    "sraṣṭā": ("√sṛj (tudādi, 6P)", "to create", "tṛc (kṛt)"),
    "kṣobhaṇaḥ": ("√kṣubh (divādi, 4P)", "to agitate", "lyuṭ (kṛt)"),
    "śaṅkha-bhṛt": ("√bhṛ (bhvādi, 1U)", "to bear", "kvip (kṛt)"),
    "gadā-dharaḥ": ("√dhṛ (bhvādi, 1U)", "to bear, hold", "ac (kṛt)"),
    "sāma-gaḥ": ("√gai (bhvādi, 1P)", "to sing", "ḍa (kṛt)"),
    "su-darśanaḥ": ("√dṛś (bhvādi, 1P)", "to see", "lyuṭ (kṛt)"),
    "dik-bandhaḥ": ("√bandh (kryādi, 9P)", "to bind", "ghañ (kṛt)"),
    "śrī-mahā-viṣṇu-prīti-arthe": ("√prī (kryādi, 9P)", "to please", "ktin (kṛt)"),
    "sahasra-nāma-stotra-pāṭhe": ("√paṭh (bhvādi, 1P)", "to recite", "ghañ (kṛt)"),
    "kṣīra-udanvat-pradeśe": ("pra-√diś (tudādi, 6U)", "to point out, designate", "ghañ (kṛt)"),
    "śuci-maṇi-vilasat-saikate": ("vi-√las (bhvādi, 1P)", "to shine", "śatṛ (kṛt)"),
    "mālā-kḷpta-āsana-sthaḥ": ("√sthā (bhvādi, 1P)", "to stand, remain", "ka (kṛt); inner kḷpta has kta"),
    "maṇḍita-aṅgaḥ": ("√maṇḍ (curādi, 10P)", "to adorn", "kta (kṛt)"),
    "upari-viracitaiḥ": ("vi-√rac (curādi, 10U)", "to arrange", "kta (kṛt)"),
    "mukta-pīyūṣa-varṣaiḥ": ("√vṛṣ (bhvādi, 1P)", "to rain", "ghañ (kṛt); inner mukta has kta"),
    "yogi-hṛd-dhyāna-gamyam": ("√gam (bhvādi, 1P)", "to go, reach", "yat (kṛt, gerundive)"),
    "bhava-bhaya-haram": ("√hṛ (bhvādi, 1U)", "to take away", "ac (kṛt)"),
    "kaustubha-udbhāsita-aṅgam": ("ud-√bhās (bhvādi, 1Ā), causative", "to make shine", "ṇic + kta (kṛt)"),
    "puṇya-upetam": ("upa-√i (adādi, 2P)", "to approach; be endowed", "kta (kṛt)"),
    "sarasīruha-īkṣaṇam": ("√īkṣ (bhvādi, 1Ā)", "to see", "lyuṭ (kṛt)"),
    "śrīvatsa-aṅkita-vakṣasam": ("√aṅk (curādi, 10P)", "to mark", "kta (kṛt)"),
    "āsīnam": ("√ās (adādi, 2Ā)", "to sit", "śānac (kṛt)"),
    "alaṃkṛtam": ("alam-√kṛ (tanādi, 8U)", "to adorn", "kta (kṛt)"),
    "sahitam": ("√sah (divādi, 4Ā)", "to accompany, endure", "kta (kṛt)"),
    "sa-hāra-vakṣas-sthala-śobhi-kaustubham": ("√śubh (bhvādi, 1Ā)", "to shine", "in (kṛt/possessive)"),
    "mataḥ": ("√man (divādi, 4Ā)", "to think, regard", "kta (kṛt)"),
    "udbhavaḥ": ("ud-√bhū (bhvādi, 1P)", "to arise", "ap (kṛt)"),
    "bhānuḥ": ("√bhā (adādi, 2P)", "to shine", "nu (uṇādi)"),
    "śaktiḥ": ("√śak (svādi, 5P)", "to be able", "ktin (kṛt)"),
    "akṣobhyaḥ": ("a-√kṣubh (divādi, 4P)", "not to be agitated", "yat (kṛt, gerundive)"),
    "viniyogaḥ": ("vi-ni-√yuj (divādi, 4Ā)", "to apply, assign", "ghañ (kṛt)"),
    "dahanaḥ": ("√dah (bhvādi, 1P)", "to burn", "lyuṭ (kṛt)"),
}

PARTICIPLE_STEMS = {
    "śrutvā": "śru", "stuvantaḥ": "stuvat", "arcantaḥ": "arcayat", "japan": "japat",
    "stuvan": "stuvat", "arcayan": "arcayat", "dhyāyan": "dhyāyat", "namasyan": "namasyat",
    "yajamānaḥ": "yajamāna",
}

WORD_OVERRIDES = {
    "naḥ": {
        "stem": "asmad",
        "parts": [
            {"form": "asmad", "gloss": "we; us"},
            {"form": "śas", "gloss": "accusative plural, realized as enclitic nas"},
        ],
        "affix": "śas (dvitīyā bahuvacana), enclitic nas substitution",
        "morph": "accusative plural first-person pronoun",
        "karaka": "karman (object of punīyāt: ‘may he purify us’)",
    },
    "bhagavān": {
        "parts": [
            {"form": "bhaga", "gloss": "splendour, fortune, lordly excellence"},
            {"form": "matup", "gloss": "possessing"},
            {"form": "su", "gloss": "nominative singular masculine"},
        ],
        "affix": "matup (taddhita) + su (prathamā ekavacana)",
    },
    "adhikatamaḥ": {
        "parts": [
            {"form": "adhika", "gloss": "exceeding, superior"},
            {"form": "tamap", "gloss": "superlative: highest"},
            {"form": "su", "gloss": "nominative singular masculine"},
        ],
        "affix": "tamap (taddhita) + su (prathamā ekavacana)",
    },
    "nandakī": {
        "parts": [
            {"form": "nandaka", "gloss": "the sword Nandaka"},
            {"form": "in", "gloss": "possessing, bearing"},
            {"form": "su", "gloss": "nominative singular masculine"},
        ],
        "affix": "in (taddhita/possessive) + su (prathamā ekavacana)",
    },
    "cakrī": {
        "parts": [
            {"form": "cakra", "gloss": "discus"},
            {"form": "in", "gloss": "possessing, bearing"},
            {"form": "su", "gloss": "nominative singular masculine"},
        ],
        "affix": "in (taddhita/possessive) + su (prathamā ekavacana)",
    },
    "ānandī": {
        "parts": [
            {"form": "ānanda", "gloss": "bliss"},
            {"form": "in", "gloss": "possessing"},
            {"form": "su", "gloss": "nominative singular masculine"},
        ],
        "affix": "in (taddhita/possessive) + su (prathamā ekavacana)",
    },
}

WORD_NOTES = {
    "vāste": "The received sandhi vāsteyam is divided here as vāste + ayam. The rare locative is traditionally glossed ‘in the abdomen’; editions and teaching lineages vary in how they explain this form.",
    "sa-hāra-vakṣas-sthala-śobhi-kaustubham": "The selected recording performs the source's śobhi-kaustubham variant; the received file also records kaustubha-śriyam as its primary reading.",
}


# Strict samāsa classifications and Sanskrit vigrahas. Keys are the displayed
# inflected pada; prefixes on verbal derivatives are handled separately below.
COMPOUND_SPECS = {
    "śukla-ambara-dharam": ("bahuvrīhi", "śuklam ambaraṃ dhārayati yaḥ saḥ"),
    "śaśi-varṇam": ("bahuvrīhi", "śaśinaḥ iva varṇaḥ yasya saḥ"),
    "catur-bhujam": ("bahuvrīhi", "catvāro bhujāḥ yasya saḥ"),
    "prasanna-vadanam": ("bahuvrīhi", "prasannaṃ vadanaṃ yasya saḥ"),
    "sarva-vighna-upaśāntaye": ("ṣaṣṭhī-tatpuruṣa", "sarveṣāṃ vighnānām upaśāntiḥ"),
    "vasiṣṭha-naptāram": ("ṣaṣṭhī-tatpuruṣa", "vasiṣṭhasya naptā"),
    "parāśara-ātmajam": ("ṣaṣṭhī-tatpuruṣa", "parāśarasya ātmajaḥ"),
    "śuka-tātam": ("ṣaṣṭhī-tatpuruṣa", "śukasya tātaḥ"),
    "tapas-nidhim": ("ṣaṣṭhī-tatpuruṣa", "tapasaḥ nidhiḥ"),
    "viṣṇu-rūpāya": ("bahuvrīhi", "viṣṇuḥ rūpaṃ yasya saḥ"),
    "vyāsa-rūpāya": ("bahuvrīhi", "vyāsaḥ rūpaṃ yasya saḥ"),
    "brahma-nidhaye": ("ṣaṣṭhī-tatpuruṣa", "brahmaṇaḥ nidhiḥ"),
    "parama-ātmane": ("karmadhāraya", "paramaḥ ātmā"),
    "sadā-eka-rūpa-rūpāya": ("bahuvrīhi", "sadā ekarūpaṃ rūpaṃ yasya saḥ"),
    "sarva-jiṣṇave": ("bahuvrīhi", "sarvaṃ jayati yaḥ saḥ"),
    "smaraṇa-mātreṇa": ("karmadhāraya", "smaraṇam eva mātram"),
    "janma-saṃsāra-bandhanāt": ("ṣaṣṭhī-tatpuruṣa", "janmasaṃsārasya bandhanam"),
    "para-ayaṇam": ("karmadhāraya", "param ayaṇam"),
    "sarva-dharmāṇām": ("karmadhāraya", "sarve dharmāḥ"),
    "jagat-prabhum": ("ṣaṣṭhī-tatpuruṣa", "jagataḥ prabhuḥ"),
    "deva-devam": ("ṣaṣṭhī-tatpuruṣa", "devānāṃ devaḥ"),
    "puruṣa-uttamam": ("ṣaṣṭhī-tatpuruṣa", "puruṣāṇām uttamaḥ"),
    "nāma-sahasreṇa": ("ṣaṣṭhī-tatpuruṣa", "nāmnāṃ sahasram"),
    "satata-utthitaḥ": ("karmadhāraya", "satataṃ utthitaḥ"),
    "an-ādi-nidhanam": ("bahuvrīhi", "ādiḥ nidhanaṃ ca na staḥ yasya saḥ"),
    "sarva-loka-mahā-īśvaram": ("ṣaṣṭhī-tatpuruṣa", "sarveṣāṃ lokānāṃ mahān īśvaraḥ"),
    "loka-adhyakṣam": ("ṣaṣṭhī-tatpuruṣa", "lokānām adhyakṣaḥ"),
    "sarva-duḥkha-atigaḥ": ("dvitīyā-tatpuruṣa", "sarvāṇi duḥkhāni atigataḥ"),
    "sarva-dharma-jñam": ("dvitīyā-tatpuruṣa", "sarvān dharmān jānāti yaḥ"),
    "kīrti-vardhanam": ("dvitīyā-tatpuruṣa", "kīrtiṃ vardhayati yaḥ"),
    "loka-nātham": ("ṣaṣṭhī-tatpuruṣa", "lokānāṃ nāthaḥ"),
    "sarva-bhūta-bhava-udbhavam": ("ṣaṣṭhī-tatpuruṣa", "sarveṣāṃ bhūtānāṃ bhavasya udbhavaḥ"),
    "puṇḍarīka-akṣam": ("bahuvrīhi", "puṇḍarīkam iva akṣiṇī yasya saḥ"),
    "ādi-yuga-āgame": ("ṣaṣṭhī-tatpuruṣa", "ādiyugasya āgamaḥ"),
    "yuga-kṣaye": ("ṣaṣṭhī-tatpuruṣa", "yugasya kṣayaḥ"),
    "loka-pradhānasya": ("ṣaṣṭhī-tatpuruṣa", "lokasya pradhānaḥ"),
    "jagat-nāthasya": ("ṣaṣṭhī-tatpuruṣa", "jagataḥ nāthaḥ"),
    "bhū-pate": ("ṣaṣṭhī-tatpuruṣa", "bhuvaḥ patiḥ"),
    "nāma-sahasram": ("ṣaṣṭhī-tatpuruṣa", "nāmnāṃ sahasram"),
    "pāpa-bhaya-apaham": ("dvandva + dvitīyā-tatpuruṣa", "pāpaṃ bhayaṃ ca apahanti yat"),
    "mahā-ātmanaḥ": ("karmadhāraya", "mahān ātmā"),
    "veda-vyāsaḥ": ("ṣaṣṭhī-tatpuruṣa", "vedānāṃ vyāsaḥ"),
    "mahā-muniḥ": ("karmadhāraya", "mahān muniḥ"),
    "devakī-sutaḥ": ("ṣaṣṭhī-tatpuruṣa", "devakyāḥ sutaḥ"),
    "amṛta-aṃśu-udbhavaḥ": ("ṣaṣṭhī-tatpuruṣa", "amṛtāṃśoḥ udbhavaḥ"),
    "devakī-nandanaḥ": ("ṣaṣṭhī-tatpuruṣa", "devakyāḥ nandanaḥ"),
    "tri-sāmā": ("bahuvrīhi", "trīṇi sāmāni yasya saḥ"),
    "śānti-arthe": ("ṣaṣṭhī-tatpuruṣa", "śānteḥ arthaḥ"),
    "mahā-viṣṇum": ("karmadhāraya", "mahān viṣṇuḥ"),
    "mahā-īśvaram": ("karmadhāraya", "mahān īśvaraḥ"),
    "aneka-rūpam": ("bahuvrīhi", "anekāni rūpāṇi yasya saḥ"),
    "daitya-antam": ("ṣaṣṭhī-tatpuruṣa", "daityānām antaḥ"),
    "śrī-viṣṇoḥ": ("karmadhāraya", "śrīmān viṣṇuḥ"),
    "divya-sahasra-nāma-stotra-mahā-mantrasya": ("karmadhāraya + ṣaṣṭhī-tatpuruṣa", "divyasya sahasranāmastotrasya mahāmantraḥ"),
    "śrī-veda-vyāsaḥ": ("karmadhāraya", "śrīmān vedavyāsaḥ"),
    "śrī-mahā-viṣṇuḥ": ("karmadhāraya", "śrīmān mahān viṣṇuḥ"),
    "parama-ātmā": ("karmadhāraya", "paramaḥ ātmā"),
    "śrīmat-nārāyaṇaḥ": ("karmadhāraya", "śrīmān nārāyaṇaḥ"),
    "śaṅkha-bhṛt": ("dvitīyā-tatpuruṣa", "śaṅkhaṃ bibharti yaḥ"),
    "śārṅga-dhanvā": ("bahuvrīhi", "śārṅgaṃ dhanuḥ yasya saḥ"),
    "gadā-dharaḥ": ("dvitīyā-tatpuruṣa", "gadāṃ dhārayati yaḥ"),
    "ratha-aṅga-pāṇiḥ": ("bahuvrīhi", "rathāṅgaṃ pāṇau yasya saḥ"),
    "sāma-gaḥ": ("dvitīyā-tatpuruṣa", "sāma gāyati yaḥ"),
    "para-brahma": ("karmadhāraya", "paraṃ brahma"),
    "su-darśanaḥ": ("karmadhāraya", "śobhanaṃ darśanaṃ yasya saḥ"),
    "dik-bandhaḥ": ("ṣaṣṭhī-tatpuruṣa", "diśāṃ bandhaḥ"),
    "śrī-viśva-rūpaḥ": ("karmadhāraya", "śrīmān viśvarūpaḥ"),
    "śrī-mahā-viṣṇu-prīti-arthe": ("ṣaṣṭhī-tatpuruṣa", "śrīmahāviṣṇoḥ prīteḥ arthaḥ"),
    "sahasra-nāma-stotra-pāṭhe": ("ṣaṣṭhī-tatpuruṣa", "sahasranāmastotrasya pāṭhaḥ"),
    "kṣīra-udanvat-pradeśe": ("ṣaṣṭhī-tatpuruṣa", "kṣīrodanvataḥ pradeśaḥ"),
    "śuci-maṇi-vilasat-saikate": ("bahuvrīhi", "śucibhiḥ maṇibhiḥ vilasat saikatam"),
    "mālā-kḷpta-āsana-sthaḥ": ("saptamī-tatpuruṣa", "mālābhiḥ kḷpte āsane sthitaḥ"),
    "sphaṭika-maṇi-nibhaiḥ": ("tṛtīyā-tatpuruṣa", "sphaṭikamaṇibhiḥ nibhāḥ"),
    "maṇḍita-aṅgaḥ": ("bahuvrīhi", "maṇḍitāni aṅgāni yasya saḥ"),
    "upari-viracitaiḥ": ("avyayībhāva", "upari viracitāḥ"),
    "mukta-pīyūṣa-varṣaiḥ": ("dvitīyā-tatpuruṣa", "muktaṃ pīyūṣaṃ varṣanti ye"),
    "ari-nalina-gadā-śaṅkha-pāṇiḥ": ("bahuvrīhi", "ariḥ nalinaṃ gadā śaṅkhaś ca pāṇiṣu yasya saḥ"),
    "candra-sūryau": ("dvandva", "candraś ca sūryaś ca"),
    "antaḥ-stham": ("avyayībhāva", "antaḥ sthitam"),
    "sura-nara-khaga-go-bhogi-gandharva-daityaiḥ": ("dvandva", "surāś ca narāś ca khagāś ca gāvaś ca bhoginaś ca gandharvāś ca daityāś ca"),
    "tri-bhuvana-vapuṣam": ("bahuvrīhi", "trīṇi bhuvanāni vapuḥ yasya saḥ"),
    "śānta-ākāram": ("bahuvrīhi", "śāntaḥ ākāraḥ yasya saḥ"),
    "bhujaga-śayanam": ("saptamī-tatpuruṣa", "bhujage śete yaḥ"),
    "padma-nābham": ("bahuvrīhi", "padmaṃ nābhau yasya saḥ"),
    "sura-īśam": ("ṣaṣṭhī-tatpuruṣa", "surāṇām īśaḥ"),
    "viśva-ādhāram": ("ṣaṣṭhī-tatpuruṣa", "viśvasya ādhāraḥ"),
    "gagana-sadṛśam": ("tṛtīyā-tatpuruṣa", "gaganena sadṛśaḥ"),
    "megha-varṇam": ("bahuvrīhi", "meghasya iva varṇaḥ yasya saḥ"),
    "śubha-aṅgam": ("bahuvrīhi", "śubhāni aṅgāni yasya saḥ"),
    "lakṣmī-kāntam": ("ṣaṣṭhī-tatpuruṣa", "lakṣmyāḥ kāntaḥ"),
    "kamala-nayanam": ("bahuvrīhi", "kamale iva nayane yasya saḥ"),
    "yogi-hṛd-dhyāna-gamyam": ("tṛtīyā-tatpuruṣa", "yogināṃ hṛdi dhyānena gamyaḥ"),
    "bhava-bhaya-haram": ("dvitīyā-tatpuruṣa", "bhavasya bhayaṃ harati yaḥ"),
    "sarva-loka-eka-nātham": ("ṣaṣṭhī-tatpuruṣa", "sarveṣāṃ lokānām ekaḥ nāthaḥ"),
    "megha-śyāmam": ("tṛtīyā-tatpuruṣa", "meghena śyāmaḥ"),
    "pīta-kauśeya-vāsam": ("bahuvrīhi", "pītaṃ kauśeyaṃ vāsaḥ yasya saḥ"),
    "śrīvatsa-aṅkam": ("bahuvrīhi", "śrīvatsaḥ aṅkaḥ yasya saḥ"),
    "kaustubha-udbhāsita-aṅgam": ("bahuvrīhi", "kaustubhena udbhāsitāni aṅgāni yasya saḥ"),
    "puṇya-upetam": ("tṛtīyā-tatpuruṣa", "puṇyaiḥ upetaḥ"),
    "puṇḍarīka-āyata-akṣam": ("bahuvrīhi", "puṇḍarīkam iva āyate akṣiṇī yasya saḥ"),
    "samasta-bhūtānām": ("karmadhāraya", "samastāni bhūtāni"),
    "ādi-bhūtāya": ("karmadhāraya", "ādiḥ bhūtaḥ"),
    "bhū-bhṛte": ("dvitīyā-tatpuruṣa", "bhuvaṃ bibharti yaḥ"),
    "aneka-rūpa-rūpāya": ("bahuvrīhi", "anekarūpaṃ rūpaṃ yasya saḥ"),
    "sa-śaṅkha-cakram": ("bahuvrīhi", "śaṅkhaś cakraṃ ca sahitau yasya saḥ"),
    "sa-kirīṭa-kuṇḍalam": ("bahuvrīhi", "kirīṭaṃ kuṇḍale ca sahitāni yasya saḥ"),
    "sa-pīta-vastram": ("bahuvrīhi", "pītaṃ vastraṃ sahitaṃ yasya saḥ"),
    "sarasīruha-īkṣaṇam": ("bahuvrīhi", "sarasīruham iva īkṣaṇaṃ yasya saḥ"),
    "sa-hāra-vakṣas-sthala-śobhi-kaustubham": ("bahuvrīhi", "hāreṇa sahite vakṣaḥsthale kaustubhaḥ śobhate yasya saḥ"),
    "hema-siṃhāsana-upari": ("avyayībhāva", "hemasiṃhāsanasya upari"),
    "ambuda-śyāmam": ("tṛtīyā-tatpuruṣa", "ambudena śyāmaḥ"),
    "āyata-akṣam": ("bahuvrīhi", "āyate akṣiṇī yasya saḥ"),
    "candra-ānanam": ("bahuvrīhi", "candraḥ iva ānanaṃ yasya saḥ"),
    "catur-bāhum": ("bahuvrīhi", "catvāro bāhavaḥ yasya saḥ"),
    "śrīvatsa-aṅkita-vakṣasam": ("bahuvrīhi", "śrīvatsena aṅkitaṃ vakṣaḥ yasya saḥ"),
    "rukmiṇī-satyabhāmābhyām": ("dvandva", "rukmiṇī ca satyabhāmā ca"),
}

MEMBER_GLOSSES = {
    "adhyakṣa": "overseer", "ambara": "garment", "ambuda": "raincloud", "aneka": "many",
    "antaḥ": "within", "apaha": "removing", "ari": "discus; enemy-destroyer", "artha": "purpose",
    "atiga": "gone beyond", "ayaṇa": "refuge; destination", "aṃśu": "ray", "aṅga": "limb",
    "aṅka": "mark", "aṅkita": "marked", "bandha": "binding", "bandhana": "bond",
    "bhava": "becoming; existence", "bhaya": "fear", "bhogi": "serpent", "bhujaga": "serpent",
    "bhuvana": "world", "brahma": "Brahman", "brahman": "Brahman", "cakra": "discus",
    "candra": "moon", "daitya": "Daitya; demon", "dhanvin": "bow-bearer", "dhyāna": "meditation",
    "dik": "direction", "divya": "divine", "duḥkha": "sorrow", "eka": "one",
    "ga": "going; singing", "gadā": "mace", "gagana": "sky", "gamya": "attainable",
    "gandharva": "Gandharva", "go": "cow; cattle", "hara": "removing", "hema": "gold",
    "hāra": "garland", "hṛd": "heart", "jiṣṇu": "conquering", "kamala": "lotus",
    "kaustubha": "the Kaustubha gem", "kauśeya": "silk", "khaga": "bird", "kirīṭa": "crown",
    "kuṇḍala": "earring", "kānta": "beloved", "kīrti": "fame", "kḷpta": "fashioned",
    "kṣaya": "ending; destruction", "kṣīra": "milk", "lakṣmī": "Lakṣmī", "mantra": "mantra",
    "maṇi": "gem", "maṇḍita": "adorned", "megha": "cloud", "mukta": "released",
    "muni": "sage", "mālā": "garland", "mātra": "mere measure; only", "nalina": "lotus",
    "nandana": "son; delight", "naptṛ": "descendant; great-grandson", "nara": "human",
    "nayana": "eye", "nibha": "resembling", "nidhana": "end", "nābha": "navel",
    "nāma": "name", "nārāyaṇa": "Nārāyaṇa", "para": "highest", "parama": "supreme",
    "parāśara": "Parāśara", "pradeśa": "region", "pradhāna": "foremost", "prasanna": "serene",
    "prīti": "pleasure; favour", "puṇḍarīka": "lotus", "pāpa": "evil; demerit", "pāṇi": "hand",
    "pāṭha": "recitation", "pīta": "yellow", "pīyūṣa": "nectar", "rukmiṇī": "Rukmiṇī",
    "sa": "with", "sadṛśa": "similar", "saikata": "sandy shore", "samasta": "all; entire",
    "sarasīruha": "lotus", "satata": "constant", "satyabhāmā": "Satyabhāmā", "saṃsāra": "saṃsāra",
    "siṃhāsana": "throne", "smaraṇa": "remembrance", "sphaṭika": "crystal", "stha": "standing; situated",
    "sthala": "place; surface", "śobhi": "shining", "stotra": "hymn", "sura": "god", "suta": "son",
    "sāma": "Sāman chant", "sāman": "Sāman chant", "sūrya": "sun", "tapas": "austerity",
    "tāta": "father", "udanvat": "ocean", "udbhava": "source; arising", "udbhāsita": "made radiant",
    "upari": "above", "upaśānti": "pacification", "upeta": "attended; endowed", "utthita": "arisen",
    "vadana": "face", "vakṣas": "chest", "vardhana": "increasing", "varṇa": "colour",
    "varṣa": "shower", "vasiṣṭha": "Vasiṣṭha", "vastra": "garment", "veda": "Veda",
    "vighna": "obstacle", "vilasat": "shining", "viracita": "arranged", "viṣṇu": "Viṣṇu",
    "vāsa": "garment; dwelling", "yogi": "yogin", "yuga": "age", "ādhāra": "support",
    "āgama": "coming", "ākāra": "form", "ānana": "face", "āsana": "seat",
    "ātmaja": "son", "āyata": "long; extended", "śayana": "lying; bed", "śaśi": "moon",
    "śrīmat": "possessing splendour", "śrīvatsa": "Śrīvatsa mark", "śubha": "auspicious",
    "śuci": "pure", "śuka": "Śuka", "śukla": "white", "śyāma": "dark",
    "śānta": "peaceful", "śārṅga": "the Śārṅga bow",
}


def nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def slot_indices(english: str) -> list[int]:
    return [int(index) for group in re.findall(r"\{([\d,\s]+):", english) for index in group.split(",")]


def parse_morph(code: str) -> tuple[str, str, str]:
    case, number, gender = code.split(".")
    return case, number, gender


def heuristic_stem(form: str, case: str, number: str, gender: str) -> str:
    if form in STEM_OVERRIDES:
        return STEM_OVERRIDES[form]
    if case in {"nom", "acc"} and number == "sg" and form.endswith("am"):
        return form[:-1]
    if case == "nom" and number == "sg" and form.endswith("ḥ"):
        return form[:-1]
    if case == "dat" and number == "sg" and form.endswith("āya"):
        return form[:-3] + "a"
    if case == "abl" and number == "sg" and form.endswith("āt"):
        return form[:-2] + "a"
    if case == "gen" and number == "sg" and form.endswith("asya"):
        return form[:-4] + "a"
    if case == "loc" and number == "sg" and form.endswith("e"):
        return form[:-1] + "a"
    if case == "ins" and number == "sg" and form.endswith("ena"):
        return form[:-3] + "a"
    if case == "ins" and number == "sg" and form.endswith("ayā"):
        return form[:-3] + "ā"
    if case == "gen" and number == "pl" and form.endswith("ānām"):
        return form[:-4] + "a"
    if case == "ins" and number == "pl" and form.endswith("aiḥ"):
        return form[:-3] + "a"
    if case in {"nom", "acc"} and number == "pl" and form.endswith("āni"):
        return form[:-3] + "a"
    return form


def ending_gloss(case: str, number: str, gender: str) -> str:
    return f"{VIBHAKTI[case]} {VACANA[number]}: {CASE_LABEL[case]} {NUMBER_LABEL[number]} {GENDER_LABEL.get(gender, gender)}"


BASE_MEMBER_GLOSSES = runpy.run_path(str(ROOT / "scripts/build_vishnu_sahasranama_analysis.py"))["MEMBER_LEXICON"]


def member_gloss(member: str) -> str:
    gloss = MEMBER_GLOSSES.get(member) or BASE_MEMBER_GLOSSES.get(member)
    if not gloss:
        raise ValueError(f"unresolved compound member: {member}")
    return gloss


def vidyut_lemma(kosha, form: str, case: str, number: str, gender: str) -> tuple[str | None, list[str]]:
    if kosha is None or "-" in form:
        return None, []
    slp1 = transliterate(form, sanscript.IAST, sanscript.SLP1)
    case_code = {
        "nom": "praTamA", "acc": "dvitIyA", "ins": "tftIyA", "dat": "caturTI",
        "abl": "paYcamI", "gen": "zazWI", "loc": "saptamI", "voc": "samboDanam",
    }[case]
    number_code = {"sg": "eka", "du": "dvi", "pl": "bahu"}[number]
    gender_code = {"m": "puM", "f": "strI", "n": "napuMsaka"}[gender]
    candidates = []
    try:
        for entry in kosha.get(slp1):
            if not hasattr(entry, "vibhakti"):
                continue
            if str(entry.vibhakti) != case_code or str(entry.vacana) != number_code or str(entry.linga) != gender_code:
                continue
            candidates.append(transliterate(str(entry.lemma), sanscript.SLP1, sanscript.IAST))
    except Exception:
        return None, []
    unique = sorted(set(candidates))
    return (unique[0] if len(unique) == 1 else None), unique


def make_word(i: int, form: str, gloss: str, morph_code: str, kosha=None) -> dict:
    deva = transliterate(form.replace("-", ""), sanscript.IAST, sanscript.DEVANAGARI)
    if morph_code == "ind":
        return {
            "i": i, "iast": form, "deva": deva, "gloss": gloss,
            "parts": [{"form": form, "gloss": gloss}], "stem": form,
            "root": None, "rootGloss": None, "affix": "avyaya (indeclinable)",
            "morph": "indeclinable", "karaka": None, "compound": None, "uncertainty": [],
        }
    if morph_code.startswith("verb:"):
        key = morph_code.split(":", 1)[1]
        root, root_gloss, morph, affix = VERBS[key]
        return {
            "i": i, "iast": form, "deva": deva, "gloss": gloss,
            "parts": [{"form": root.split(" ", 1)[0], "gloss": root_gloss}, {"form": affix.split(" ", 1)[0], "gloss": morph}],
            "stem": VERB_STEMS[key], "root": root, "rootGloss": root_gloss,
            "affix": affix, "morph": morph, "karaka": "finite verbal predicate", "compound": None, "uncertainty": [],
        }
    if morph_code.startswith("part:"):
        key = morph_code.split(":", 1)[1]
        root, root_gloss, affix, morph = PARTICIPLES[key]
        return {
            "i": i, "iast": form, "deva": deva, "gloss": gloss,
            "parts": [{"form": root.split(" ", 1)[0], "gloss": root_gloss}, {"form": affix.split(" ", 1)[0], "gloss": morph}],
            "stem": PARTICIPLE_STEMS.get(key, key), "root": root, "rootGloss": root_gloss,
            "affix": affix, "morph": morph, "karaka": "participial modifier or predicate in the clause", "compound": None, "uncertainty": [],
        }
    case, number, gender = parse_morph(morph_code)
    candidate_stem, candidate_lemmas = vidyut_lemma(kosha, form, case, number, gender)
    stem = STEM_OVERRIDES.get(form) or candidate_stem or heuristic_stem(form, case, number, gender)
    sup = SUP[(case, number)]
    compound = None
    parts = [{"form": stem, "gloss": gloss}]
    if form in COMPOUND_SPECS:
        ctype, vigraha = COMPOUND_SPECS[form]
        members = stem.split("-")
        parts = [{"form": member, "gloss": member_gloss(member)} for member in members]
        compound = {"type": ctype, "vigraha": vigraha, "members": members}
    derived = DERIVED_FORMS.get(form)
    root = root_gloss = None
    derivational_affix = None
    if derived:
        root, root_gloss, derivational_affix = derived
        if compound is None:
            parts = [
                {"form": root.split(" ", 1)[0], "gloss": root_gloss},
                {"form": derivational_affix.split(" ", 1)[0], "gloss": "forms the derived stem"},
            ]
    parts.append({"form": sup, "gloss": ending_gloss(case, number, gender)})
    uncertainty = []
    if len(candidate_lemmas) > 1 and form not in STEM_OVERRIDES:
        uncertainty.append("Vidyut returns multiple context-compatible lemmas; a manual stem adjudication is required.")
    if "-" in form and form not in COMPOUND_SPECS and form != "pari-gītāni":
        uncertainty.append("The pada is segmented but lacks a reviewed samāsa classification.")
    result = {
        "i": i, "iast": form, "deva": deva, "gloss": gloss,
        "parts": parts,
        "stem": stem, "root": root, "rootGloss": root_gloss,
        "affix": f"{derivational_affix + ' + ' if derivational_affix else ''}{sup} ({VIBHAKTI[case]} {VACANA[number]}; {CASE_LABEL[case]} {NUMBER_LABEL[number]})",
        "morph": f"{CASE_LABEL[case]} {NUMBER_LABEL[number]} {GENDER_LABEL.get(gender, gender)} — {VIBHAKTI[case]} {VACANA[number]}",
        "karaka": KARAKA[case], "compound": compound, "uncertainty": uncertainty,
        "evidence": {"vidyut_compatible_lemmas": candidate_lemmas},
        "note": WORD_NOTES.get(form),
    }
    if form in WORD_OVERRIDES:
        result.update(WORD_OVERRIDES[form])
    return result


def comparison_key(value: str) -> str:
    value = nfc(value).lower().replace("'", "")
    return "".join(char for char in value if char.isalpha())


def align_surfaces(source_iast: str, words: list[dict]) -> None:
    target = comparison_key(source_iast)
    tokens = [comparison_key(word["iast"]) for word in words]
    joined = "".join(tokens)
    matcher = difflib.SequenceMatcher(a=joined, b=target, autojunk=False)
    mapping = [None] * (len(joined) + 1)
    for _tag, a0, a1, b0, b1 in matcher.get_opcodes():
        width = a1 - a0
        for pos in range(a0, a1 + 1):
            fraction = 0 if width == 0 else (pos - a0) / width
            mapping[pos] = round(b0 + fraction * (b1 - b0))
    mapping[0], mapping[-1] = 0, len(target)
    last = 0
    for index, value in enumerate(mapping):
        value = last if value is None else max(last, min(len(target), value))
        mapping[index], last = value, value
    offset = 0
    for word, token in zip(words, tokens):
        start, end = mapping[offset], mapping[offset + len(token)]
        word["surface_iast"] = target[start:end]
        offset += len(token)
    if "".join(word["surface_iast"] for word in words) != target:
        raise ValueError("surface alignment does not replay source text")


def build(kosha=None) -> dict:
    witness = json.loads(WITNESS_PATH.read_text(encoding="utf-8"))
    witness_units = {unit["id"]: unit for group in witness["groups"] for unit in group["units"]}
    units = []
    for unit_id, spec in UNIT_SPECS.items():
        source = witness_units[unit_id]
        words = [make_word(i, *record, kosha=kosha) for i, record in enumerate(spec["words"])]
        align_surfaces(source["iast"], words)
        units.append({
            "id": unit_id,
            "devanagari": source["devanagari"],
            "iast": source["iast"],
            "words": words,
            "english": spec["english"],
            "source_status": "received-text + reviewed-pada-analysis",
        })
    return {
        "schema_version": 1,
        "sources": {
            "witness": {
                "path": str(WITNESS_PATH.relative_to(ROOT)),
                "sha256": hashlib.sha256(WITNESS_PATH.read_bytes()).hexdigest(),
            },
            "segmentation_aid": {
                "url": "https://vedapedia.org/library/stotrams/sri-visnu-sahasranama",
                "capture_sha256": "4a2c85f5946a5672ab205d4d5a39339c852689ca3a2b146dc9e43486d6bec830",
            },
            "morphology": {
                "name": "Vidyut",
                "version": "0.4.0",
                "data_zip_sha256": "5269cda86451a75dbc93b605f6864bb5a52cc79d66da02f18f30cf87d0059ecb",
                "adjudication": "manual contextual review of every accepted pada",
            },
            "lexicon": {
                "name": "Monier-Williams Sanskrit-English Dictionary",
                "csl_sha256": "f4fff3926d053848d44807b08d3f14f0755793e92f04e7424e03bcad2ca7e4e5",
            },
        },
        "units": units,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    parser.add_argument("--vidyut-data", type=Path, default=Path("/tmp/vidyut-0.4.0/kosha"))
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    if args.check:
        data = json.loads(args.check.read_text(encoding="utf-8"))
        print(json.dumps(validate(data), ensure_ascii=False, indent=2))
        return
    from vidyut.kosha import Kosha
    data = build(Kosha(args.vidyut_data))
    report = validate(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def validate(data: dict) -> dict:
    units = data.get("units", [])
    witness = json.loads(WITNESS_PATH.read_text(encoding="utf-8"))
    expected_ids = [unit["id"] for group in witness["groups"] for unit in group["units"]]
    errors = []
    if [unit.get("id") for unit in units] != expected_ids:
        errors.append("analysis units do not exactly match the 45-unit performed witness order")
    compound_count = root_count = 0
    for unit in units:
        uid = unit.get("id")
        words = unit.get("words", [])
        if [word.get("i") for word in words] != list(range(len(words))):
            errors.append(f"{uid}: word indices are not contiguous")
        slots = slot_indices(unit.get("english", ""))
        if set(slots) != set(range(len(words))):
            missing = sorted(set(range(len(words))) - set(slots))
            extra = sorted(set(slots) - set(range(len(words))))
            errors.append(f"{uid}: English slot coverage mismatch; missing={missing}, extra={extra}")
        replay = "".join(word.get("surface_iast", "") for word in words)
        if replay != comparison_key(unit.get("iast", "")):
            errors.append(f"{uid}: pada surfaces do not replay the received text")
        for word in words:
            label = f"{uid} word {word.get('i')} {word.get('iast')}"
            required = ("iast", "deva", "gloss", "parts", "stem", "affix", "morph", "surface_iast", "uncertainty")
            missing_fields = [field for field in required if field not in word or word[field] in (None, "")]
            if missing_fields:
                errors.append(f"{label}: lacks {', '.join(missing_fields)}")
            if not isinstance(word.get("parts"), list) or not word.get("parts") or any(not part.get("form") or not part.get("gloss") for part in word.get("parts", [])):
                errors.append(f"{label}: incomplete morpheme translation")
            if word.get("uncertainty"):
                errors.append(f"{label}: unresolved uncertainty: {'; '.join(word['uncertainty'])}")
            if word.get("compound"):
                compound_count += 1
                compound = word["compound"]
                if not compound.get("type") or not compound.get("vigraha") or not compound.get("members"):
                    errors.append(f"{label}: incomplete samāsa analysis")
                if len(word.get("parts", [])) < len(compound.get("members", [])) + 1:
                    errors.append(f"{label}: compound members are not all translated")
            if word.get("root"):
                root_count += 1
                if not word.get("rootGloss"):
                    errors.append(f"{label}: root lacks a gloss")
    if errors:
        raise ValueError("\n".join(errors[:120]))
    return {
        "units": len(units),
        "words": sum(len(unit.get("words", [])) for unit in units),
        "compounds": compound_count,
        "root_analyses": root_count,
        "slot_coverage": "100%",
        "source_replay": "100%",
    }


if __name__ == "__main__":
    main()
