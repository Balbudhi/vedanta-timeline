#!/usr/bin/env python3
"""Build a quarantined computational comparison for quoted Gītā fragments.

This script is retained only to reproduce the parser output used during the
audit that exposed the earlier methodology error. Its Sūtrakṛt, Vidyut, and
auxiliary-gloss results are non-authoritative candidates. The output must not be
joined into a public reader or described as Pāṇinian analysis. Public word cards
are independently derived from the BORI witness and traditional grammar under
docs/SANSKRIT_TRANSLATION_STANDARD.md §6.1.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import difflib
import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUOTES_PATH = ROOT / "gita/vishnu-sahasranama/commentary-quotes.json"
PACKET_PATH = ROOT / "data/sources/sanskrit/vedanta/bhagavadgita_sutrakrit_word_analysis.json"
OUTPUT_PATH = ROOT / "gita/vishnu-sahasranama/commentary-quote-analysis.json"
GLOSS_URL = "https://vedicscriptures.github.io/slok/{chapter}/{verse}"

SUP = {
    ("nominative", "singular"): "su (prathamā ekavacana)",
    ("nominative", "dual"): "au (prathamā dvivacana)",
    ("nominative", "plural"): "jas (prathamā bahuvacana)",
    ("accusative", "singular"): "am (dvitīyā ekavacana)",
    ("accusative", "dual"): "auṭ (dvitīyā dvivacana)",
    ("accusative", "plural"): "śas (dvitīyā bahuvacana)",
    ("instrumental", "singular"): "ṭā (tṛtīyā ekavacana)",
    ("instrumental", "dual"): "bhyām (tṛtīyā dvivacana)",
    ("instrumental", "plural"): "bhis (tṛtīyā bahuvacana)",
    ("dative", "singular"): "ṅe (caturthī ekavacana)",
    ("dative", "dual"): "bhyām (caturthī dvivacana)",
    ("dative", "plural"): "bhyas (caturthī bahuvacana)",
    ("ablative", "singular"): "ṅasi (pañcamī ekavacana)",
    ("ablative", "dual"): "bhyām (pañcamī dvivacana)",
    ("ablative", "plural"): "bhyas (pañcamī bahuvacana)",
    ("genitive", "singular"): "ṅas (ṣaṣṭhī ekavacana)",
    ("genitive", "dual"): "os (ṣaṣṭhī dvivacana)",
    ("genitive", "plural"): "ām (ṣaṣṭhī bahuvacana)",
    ("locative", "singular"): "ṅi (saptamī ekavacana)",
    ("locative", "dual"): "os (saptamī dvivacana)",
    ("locative", "plural"): "sup (saptamī bahuvacana)",
    ("vocative", "singular"): "su, elided/modified in address (sambodhana ekavacana)",
    ("vocative", "dual"): "au (sambodhana dvivacana)",
    ("vocative", "plural"): "jas (sambodhana bahuvacana)",
}
FUNCTION_GLOSSES = {
    "na": "not", "ca": "and", "vā": "or", "tu": "but; whereas", "api": "also; even",
    "eva": "just; indeed", "hi": "for; indeed", "iti": "thus", "iva": "like; as if",
    "aham": "I", "mām": "me", "me": "to/of me", "tvam": "you", "te": "to/of you",
    "ayam": "this one", "idam": "this", "tat": "that", "yaḥ": "who; which",
    "yat": "which; what", "saḥ": "he; that one", "kim": "what", "om": "oṃ",
    "punar": "again", "bhūyas": "again; further", "kadācid": "at any time",
    "sarvatra": "everywhere", "sarvatas": "on every side", "satatam": "continually",
    "nityam": "always", "nityaśas": "always; daily", "iha": "here", "tathā": "thus; likewise",
    "yathā": "as; just as", "tasmāt": "therefore; from that", "tena": "by that",
    "kutas": "from where; how then", "adhas": "below", "yugapad": "simultaneously",
}
MEMBER_GLOSSES = {
    "acala": "unmoving", "acintya": "inconceivable", "adbhuta": "wonderful",
    "aiśvarya": "lordship; power", "akṣi": "eye", "an": "not; without",
    "ananta": "endless", "aneka": "many", "anya": "other", "avyakta": "unmanifest",
    "aṃśa": "portion", "bahu": "many", "bhakti": "devotion", "bhoga": "enjoyment",
    "bhārata": "descendant of Bharata", "bhūta": "being", "bāhu": "arm",
    "cañcala": "restless", "dharma": "dharma; right order", "eka": "one",
    "guṇa": "quality; strand", "hṛd": "heart", "japa": "recitation",
    "kuru": "Kuru", "kāma": "desire", "kṛt": "maker; doer", "loka": "world",
    "mad": "me; my", "maṇi": "jewel", "mṛtyu": "death", "nandana": "delight; descendant",
    "nitya": "eternal", "nivāta": "windless", "paratas": "beyond", "prakṛti": "nature",
    "pāṇi": "hand", "rasa": "essence", "rūpa": "form", "sama": "equal; same",
    "sarva": "all", "saṃsthāpana": "establishment", "saṃsāra": "cycle of becoming",
    "sūrya": "sun", "tvad": "you", "udara": "belly", "vaktra": "face; mouth",
    "vat": "like; as", "veda": "Veda; knowledge", "vedānta": "end of the Veda",
    "vid": "knowing", "viśva": "all; universe", "viśāla": "wide; great",
    "vyavasāya": "resolve", "vyātta": "opened wide", "yantra": "machine",
    "yoga": "yoga; yoking", "āditya": "sun", "āścarya": "wonder",
    "śrutimat": "endowed with hearing", "ūrdhva": "above", "ūru": "thigh",
    "antarātman": "inner self", "anumantṛ": "permitter", "bhakta": "devotee",
    "bhartṛ": "supporter", "bhoktṛ": "enjoyer", "cetas": "mind", "citta": "mind",
    "darśana": "seeing; vision", "daṃṣṭra": "fang", "deha": "body", "deśa": "place",
    "div": "heaven", "dīp": "shine", "etad": "this", "gati": "going; goal",
    "gaṇa": "group", "gati": "destination; goal",
}
REVIEWED_WEAK_FORMS = {
    "adhikataraḥ", "anusmaran", "bhrāmayan", "dhanaṃjayaḥ", "enam", "kaścid",
    "nivartanti", "patram", "prāhuḥ", "śaṃkaraḥ", "tvāt", "upetya", "ātmikā",
    "āpṛthivyoḥ", "duh", "prasaviṣyadhvam", "dhanaṃjaya", "kiṃcid",
}
FORM_OVERRIDES = {
    "aham": {"stem": "asmad", "morph": "nominative singular first-person pronoun"},
    "mām": {"stem": "asmad", "morph": "accusative singular first-person pronoun"},
    "mama": {"stem": "asmad", "morph": "genitive singular first-person pronoun"},
    "mayi": {"stem": "asmad", "morph": "locative singular first-person pronoun"},
    "me": {"stem": "asmad"},
    "tvam": {"stem": "yuṣmad", "morph": "nominative singular second-person pronoun"},
    "tvā": {"stem": "yuṣmad", "morph": "accusative singular second-person pronoun"},
    "tvām": {"stem": "yuṣmad", "morph": "accusative singular second-person pronoun"},
    "tvayā": {"stem": "yuṣmad", "morph": "instrumental singular second-person pronoun"},
    "tava": {"stem": "yuṣmad", "morph": "genitive singular second-person pronoun"},
    "te": {"stem": "yuṣmad"},
    "prāhuḥ": {"stem": "pra-√brū", "morph": "perfect indicative third-person plural verb", "affix": "liṭ, prathamapuruṣa bahuvacana"},
    "nivartanti": {"stem": "ni-√vṛt", "morph": "present indicative third-person plural verb", "affix": "laṭ + jhi (prathamapuruṣa bahuvacana)"},
    "bhrāmayan": {"stem": "bhrāmaya", "morph": "nominative masculine singular causative present participle", "affix": "śatṛ (present active participle)"},
    "anusmaran": {"stem": "anu-√smṛ", "morph": "nominative masculine singular present participle", "affix": "śatṛ (present active participle)"},
    "upetya": {"stem": "upa-√i", "morph": "absolutive (converb)", "affix": "lyap (absolutive after a preverb)"},
    "dhātāram": {"stem": "dhātṛ", "morph": "accusative masculine singular agent noun", "affix": "am (dvitīyā ekavacana)"},
    "patram": {"stem": "patra"},
    "ātmikā": {"stem": "ātmaka", "morph": "nominative feminine singular adjective"},
    "pravyathitam": {"stem": "pravyathita", "morph": "nominative neuter singular past participle", "affix": "kta (past passive participle)"},
    "pravyathitāḥ": {"stem": "pravyathita", "morph": "nominative masculine plural past participle", "affix": "kta + jas (past participle, prathamā bahuvacana)"},
    "ūrjitam": {"stem": "ūrjita", "morph": "nominative neuter singular past participle", "affix": "kta + su (past participle, prathamā ekavacana)"},
    "māmakam": {"stem": "māmaka"},
    "jagat": {"stem": "jagat"},
    "saṃbhavam": {"stem": "saṃbhava"},
    "duratyayā": {"stem": "duratyaya"},
    "mayī": {"stem": "maya"},
    "daivī": {"stem": "daiva"},
    "duṣkṛtām": {"stem": "duṣkṛt"},
    "avāptavyam": {"stem": "ava-√āp", "morph": "nominative neuter singular gerundive", "affix": "tavya (gerundive kṛt affix)"},
    "āpūryamāṇam": {"stem": "ā-√pṝ", "morph": "accusative masculine singular present passive participle", "affix": "śānac (present middle/passive participle)"},
    "iṅgate": {"stem": "√iṅg", "affix": "laṭ + ta (prathamapuruṣa ekavacana, Ātmanepada)"},
    "bhūtvā": {"stem": "√bhū", "root": {"form": "√bhū", "gana": "bhvādi (1)", "pada": "Parasmaipada", "gloss": "to be; become"}},
    "kariṣye": {"stem": "√kṛ", "root": {"form": "√kṛ", "gana": "tanādi (8)", "pada": "Ātmanepada in this form", "gloss": "to do; make"}},
    "āhuḥ": {"stem": "√ah", "root": {"form": "√ah", "gana": "adādi (2)", "pada": "Parasmaipada", "gloss": "to say"}, "morph": "perfect indicative third-person plural verb", "affix": "liṭ, prathamapuruṣa bahuvacana"},
    "veda": {"stem": "√vid", "root": {"form": "√vid", "gana": "adādi (2)", "pada": "Parasmaipada", "gloss": "to know"}, "morph": "perfect indicative third-person singular verb", "affix": "liṭ, prathamapuruṣa ekavacana"},
    "viddhi": {"stem": "√vid", "root": {"form": "√vid", "gana": "adādi (2)", "pada": "Parasmaipada", "gloss": "to know"}},
    "vidyate": {"stem": "√vid", "root": {"form": "√vid", "gana": "adādi (2)", "pada": "passive Ātmanepada form", "gloss": "to find; be found, exist"}},
    "vijñāya": {"stem": "vi-√jñā", "root": {"form": "√jñā", "gana": "kryādi (9)", "pada": "Parasmaipada", "gloss": "to know"}, "affix": "lyap (absolutive after a preverb)"},
    "viṣṭabhya": {"stem": "vi-√stambh", "root": {"form": "√stambh", "gana": "svādi (5)", "pada": "Parasmaipada", "gloss": "to support; prop"}, "affix": "lyap (absolutive after a preverb)"},
    "āviśya": {"stem": "ā-√viś", "root": {"form": "√viś", "gana": "tudādi (6)", "pada": "Parasmaipada", "gloss": "to enter"}, "affix": "lyap (absolutive after a preverb)"},
    "āvṛtya": {"stem": "ā-√vṛ", "root": {"form": "√vṛ", "gana": "svādi (5)", "pada": "Parasmaipada", "gloss": "to cover"}, "affix": "lyap (absolutive after a preverb)"},
    "āvṛtam": {"stem": "ā-√vṛ", "root": {"form": "√vṛ", "gana": "svādi (5)", "pada": "Parasmaipada", "gloss": "to cover"}},
    "prakāśayati": {"stem": "pra-√kāś", "root": {"form": "√kāś", "gana": "bhvādi (1)", "pada": "Parasmaipada causative", "gloss": "to shine; make visible"}},
    "bhāsayate": {"stem": "√bhās", "root": {"form": "√bhās", "gana": "bhvādi (1)", "pada": "Ātmanepada causative", "gloss": "to shine; illumine"}},
    "dhārayāmi": {"stem": "√dhṛ", "root": {"form": "√dhṛ", "gana": "bhvādi (1)", "pada": "Parasmaipada causative", "gloss": "to hold; support"}},
    "saṃbhavāmi": {"stem": "sam-√bhū", "root": {"form": "√bhū", "gana": "bhvādi (1)", "pada": "Parasmaipada", "gloss": "to be; become"}},
    "taranti": {"stem": "√tṝ", "root": {"form": "√tṝ", "gana": "bhvādi (1)", "pada": "Parasmaipada", "gloss": "to cross over"}},
    "paryupāsate": {"stem": "pari-upa-√ās", "root": {"form": "√ās", "gana": "adādi (2)", "pada": "Ātmanepada", "gloss": "to sit near; worship"}},
    "duh": {"stem": "duh", "morph": "nominative masculine singular agent noun", "affix": "su (prathamā ekavacana)"},
    "prasaviṣyadhvam": {"stem": "pra-√sū", "morph": "future second-person plural Ātmanepada verb", "affix": "lṛṭ + dhvam (madhyamapuruṣa bahuvacana)"},
    "dhanaṃjaya": {"stem": "dhanaṃjaya", "morph": "vocative masculine singular proper name"},
    "kiṃcid": {"stem": "kim + cit", "morph": "nominative neuter singular indefinite pronoun"},
}


def key(text: str) -> str:
    return re.sub(r"[^a-zāīūṛṝḷṅñṭḍṇśṣṃḥ]", "", text.lower())


def align_words(fragment: str, words: list[dict]) -> tuple[float, int, int]:
    target = key(fragment)
    best = (0.0, 0, 0)
    for start in range(len(words)):
        for end in range(start + 1, len(words) + 1):
            candidate = key(" ".join(word["surface_form"] for word in words[start:end]))
            ratio = min(len(target), len(candidate)) / max(len(target), len(candidate))
            if ratio < 0.60:
                continue
            score = difflib.SequenceMatcher(None, target, candidate, autojunk=False).ratio() * ratio ** 0.5
            best = max(best, (score, start, end))
    return best


def parse_glosses(ec: str) -> dict[str, list[str]]:
    prefix = ec.split("Commentary", 1)[0]
    prefix = re.sub(r"^\s*\d+\.\d+\s*", "", prefix)
    result: dict[str, list[str]] = {}
    for part in prefix.split("?"):
        part = part.strip(" .")
        match = re.match(r"^([\u0900-\u097f\s]+?)\s+([^\u0900-\u097f].*)$", part)
        if not match:
            continue
        deva = re.sub(r"\s+", "", match.group(1))
        gloss = match.group(2).strip(" .")
        if deva and gloss:
            result.setdefault(deva, []).append(gloss)
    return result


def fetch_glosses(key_and_record: tuple[str, dict]) -> tuple[str, dict[str, list[str]]]:
    ref, record = key_and_record
    api_ref = record.get("api_verse_id", ref)
    chapter, verse = api_ref.split(".")
    with urllib.request.urlopen(GLOSS_URL.format(chapter=chapter, verse=verse), timeout=30) as response:
        payload = json.loads(response.read())
    return ref, parse_glosses(payload.get("siva", {}).get("ec", ""))


def load_gloss_aid(packet: dict) -> dict[str, dict[str, list[str]]]:
    result = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(fetch_glosses, item) for item in packet["verses"].items()]
        for future in concurrent.futures.as_completed(futures):
            ref, glosses = future.result()
            result[ref] = glosses
    return result


def enum_text(value) -> str:
    raw = str(value).split(".")[-1]
    return {
        "la~w": "laṭ", "lo~w": "loṭ", "li~w": "liṭ", "lf~w": "lṛṭ", "lu~w": "luṭ",
        "viDili~N": "vidhiliṅ", "Satf~": "śatṛ", "SAnac": "śānac", "Ryat": "ṇyat",
        "ktvA": "ktvā", "lyap": "lyap", "kyap": "lyap", "praTama": "prathama",
        "maDyama": "madhyama", "uttama": "uttama", "eka": "eka", "dvi": "dvi", "bahu": "bahu",
        "BvAdi": "bhvādi (1)", "adAdi": "adādi (2)", "juhotyAdi": "juhotyādi (3)",
        "divAdi": "divādi (4)", "svAdi": "svādi (5)", "tudAdi": "tudādi (6)",
        "ruDAdi": "rudhādi (7)", "tanAdi": "tanādi (8)", "kryAdi": "kryādi (9)",
        "curAdi": "curādi (10)",
    }.get(raw, raw)


def get_kosha_entries(kosha, surface_iast: str, transliterate, Scheme) -> list:
    slp = transliterate(surface_iast, Scheme.Iast, Scheme.Slp1)
    queries = [slp]
    if slp.endswith("H"):
        queries = [slp[:-1] + "s", slp[:-1] + "r"]
    return [entry for query in queries for entry in kosha.get(query)]


def candidate_score(entry, source: dict, PadaEntry, transliterate, Scheme) -> int:
    expected_lemma = source.get("lemma", "").lstrip("√")
    lemma = transliterate(entry.lemma, Scheme.Slp1, Scheme.Iast)
    score = 20 if key(lemma) == key(expected_lemma) else 0
    grammar = source.get("grammar", "").lower()
    if isinstance(entry, PadaEntry.Tinanta):
        score += 8 if "verb" in grammar else -4
        if "pass" in grammar and enum_text(entry.prayoga) == "karmaRi":
            score += 5
        for english, enum in (("singular", "eka"), ("dual", "dvi"), ("plural", "bahu")):
            if english in grammar and enum_text(entry.vacana) == enum:
                score += 3
    else:
        score += 6 if "noun" in grammar or "participle" in grammar else 0
        fields = {
            "nominative": "praTamA", "accusative": "dvitIyA", "instrumental": "tftIyA",
            "dative": "caturTI", "ablative": "paYcamI", "genitive": "zazWI",
            "locative": "saptamI", "vocative": "samboDanam",
            "masculine": "puM", "feminine": "strI", "neuter": "napuMsaka",
            "singular": "eka", "dual": "dvi", "plural": "bahu",
        }
        actual = {enum_text(entry.vibhakti), enum_text(entry.linga), enum_text(entry.vacana)}
        score += sum(3 for word, enum in fields.items() if word in grammar and enum in actual)
    return score


def affix_for(source: dict, selected, PadaEntry) -> str:
    grammar = source.get("grammar", "").lower()
    if "compound member" in grammar:
        return "compound member; the final member carries the compound's inflection"
    if not grammar:
        return "avyaya (indeclinable; no sup or tiṅ ending)"
    if "conv" in grammar:
        if selected and isinstance(selected, PadaEntry.Subanta) and hasattr(selected.pratipadika_entry, "krt"):
            return f"{enum_text(selected.pratipadika_entry.krt)} (kṛt converb affix)"
        return "ktvā/lyap converb formation; exact allomorph pending"
    if "participle" in grammar or "gdv" in grammar:
        if selected and isinstance(selected, PadaEntry.Subanta) and hasattr(selected.pratipadika_entry, "krt"):
            return f"{enum_text(selected.pratipadika_entry.krt)} (kṛt affix)"
    if "verb" in grammar:
        if selected and isinstance(selected, PadaEntry.Tinanta):
            person = enum_text(selected.purusha)
            number = enum_text(selected.vacana)
            surface = source.get("surface_form", "")
            atmanepada = enum_text(selected.prayoga) == "karmaRi" or surface.endswith(("te", "ante", "se"))
            endings = {
                ("prathama", "eka", False): "tip", ("prathama", "dvi", False): "tas", ("prathama", "bahu", False): "jhi",
                ("madhyama", "eka", False): "sip", ("madhyama", "dvi", False): "thas", ("madhyama", "bahu", False): "tha",
                ("uttama", "eka", False): "mip", ("uttama", "dvi", False): "vas", ("uttama", "bahu", False): "mas",
                ("prathama", "eka", True): "ta", ("prathama", "dvi", True): "ātām", ("prathama", "bahu", True): "jha",
                ("madhyama", "eka", True): "thās", ("madhyama", "dvi", True): "āthām", ("madhyama", "bahu", True): "dhvam",
                ("uttama", "eka", True): "iṭ", ("uttama", "dvi", True): "vahi", ("uttama", "bahu", True): "mahiṅ",
            }
            ending = endings.get((person, number, atmanepada), "tiṅ")
            return f"{enum_text(selected.lakara)} + {ending} ({person}puruṣa {number}vacana)"
        return "finite tiṅ ending; exact pada pending"
    case = next((case for case in ("nominative", "accusative", "instrumental", "dative", "ablative", "genitive", "locative", "vocative") if case in grammar), None)
    number = next((number for number in ("singular", "dual", "plural") if number in grammar), None)
    return SUP.get((case, number), "sup nominal ending; exact case/number pending")


def analyze_word(source: dict, gloss_map: dict[str, list[str]], kosha, PadaEntry, transliterate, Scheme) -> dict:
    surface = source["surface_form"]
    deva = source["surface_devanagari"]
    lemma = source.get("lemma", surface)
    lookup = re.sub(r"\s+", "", deva)
    gloss = (gloss_map.get(lookup) or [None])[0]
    if not gloss:
        gloss = (FUNCTION_GLOSSES.get(key(surface)) or FUNCTION_GLOSSES.get(key(lemma))
                 or MEMBER_GLOSSES.get(key(lemma)) or lemma.lstrip("√"))
    if gloss == lemma.lstrip("√") and key(lemma) in MEMBER_GLOSSES:
        gloss = MEMBER_GLOSSES[key(lemma)]
    if surface == "diśaḥ" and gloss == "arters":
        gloss = "quarters; directions"
    if surface == "duh":
        gloss = "yielding; milking"
    if surface == "dhanaṃjaya":
        gloss = "O Dhanaṃjaya"
    if surface == "kiṃcid":
        gloss = "anything"
    entries = get_kosha_entries(kosha, surface, transliterate, Scheme)
    selected = max(entries, key=lambda entry: candidate_score(entry, source, PadaEntry, transliterate, Scheme), default=None)
    selected_score = candidate_score(selected, source, PadaEntry, transliterate, Scheme) if selected else 0
    root = None
    stem = lemma.lstrip("√")
    derivational = any(marker in source.get("grammar", "") for marker in ("verb", "participle", "conv", "gdv"))
    if derivational and selected_score >= 20 and selected and isinstance(selected, PadaEntry.Tinanta):
        dhatu = selected.dhatu_entry
        root_iast = transliterate(dhatu.clean_text, Scheme.Slp1, Scheme.Iast)
        root = {
            "form": f"√{root_iast}",
            "gana": enum_text(dhatu.dhatu.gana),
            "pada": "Ātmanepada in this form" if surface.endswith(("te", "ante")) or enum_text(selected.prayoga) == "karmaRi" else "Parasmaipada in this form",
            "gloss": dhatu.artha_en or gloss,
        }
        stem = root_iast
    elif derivational and selected_score >= 20 and selected and isinstance(selected, PadaEntry.Subanta) and hasattr(selected.pratipadika_entry, "dhatu_entry"):
        dhatu = selected.pratipadika_entry.dhatu_entry
        root_iast = transliterate(dhatu.clean_text, Scheme.Slp1, Scheme.Iast)
        root = {
            "form": f"√{root_iast}", "gana": enum_text(dhatu.dhatu.gana),
            "pada": "not applicable to this kṛdanta form", "gloss": dhatu.artha_en or gloss,
        }
        stem = root_iast
    affix = affix_for(source, selected, PadaEntry)
    parts = [{"form": stem, "gloss": gloss}]
    if not affix.startswith(("compound member", "avyaya")):
        parts.append({"form": affix.split(" ", 1)[0], "gloss": affix})
    override = FORM_OVERRIDES.get(surface, {})
    stem = override.get("stem", stem)
    affix = override.get("affix", affix)
    morph = override.get("morph", source.get("grammar") or "indeclinable (avyaya)")
    root = override.get("root", root)
    parts = [{"form": stem, "gloss": gloss}]
    if not affix.startswith(("compound member", "avyaya")):
        parts.append({"form": affix.split(" ", 1)[0], "gloss": affix})
    uncertainty = []
    if selected_score < 10 and surface not in REVIEWED_WEAK_FORMS and source.get("grammar") not in ("", "compound (compound member)", "compound participle (compound member)"):
        uncertainty.append("Vidyut did not return a uniquely strong contextual match; the Sūtrakṛt parse is retained as a working reading.")
    return {
        "iast": surface, "deva": deva, "gloss": gloss, "parts": parts, "stem": stem,
        "root": root, "affix": affix, "morph": morph,
        "note": "; ".join(uncertainty) if uncertainty else None,
        "evidence": {"sutrakrit_lemma": lemma, "vidyut_candidate_count": len(entries), "vidyut_selected_score": selected_score},
    }


def build(vidyut_data: Path) -> dict:
    from vidyut.kosha import Kosha, PadaEntry
    from vidyut.lipi import Scheme, transliterate

    quotes = json.loads(QUOTES_PATH.read_text(encoding="utf-8"))["quotes"]
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    gloss_aid = load_gloss_aid(packet)
    kosha = Kosha(str(vidyut_data / "kosha"))
    analyses = {}
    for quote in quotes:
        verse = packet["verses"][quote["analysis_ref"]]
        score, start, end = align_words(quote["canonical_iast"], verse["word_by_word"])
        if score < 0.73:
            raise ValueError(f"weak word alignment for {quote['id']}: {score:.3f}")
        words = [analyze_word(word, gloss_aid.get(quote["analysis_ref"], {}), kosha, PadaEntry, transliterate, Scheme)
                 for word in verse["word_by_word"][start:end]]
        for index, word in enumerate(words):
            word["i"] = index
        translation = quote.get("chinmayananda_translation")
        english = f"{{{','.join(str(i) for i in range(len(words)))}:{translation}}}" if translation else None
        analyses[quote["id"]] = {
            "quote_id": quote["id"], "canonical_locus": quote["canonical_locus"],
            "words": words, "english": english, "alignment_score": round(score, 4),
            "status": "review-required" if any(word.get("note") for word in words) else "source-joined",
        }
    return {"schema_version": 1, "quotes": analyses}


def validate(data: dict) -> dict:
    rows = data.get("quotes", {})
    errors = []
    for quote_id, row in rows.items():
        words = row.get("words", [])
        if [word.get("i") for word in words] != list(range(len(words))):
            errors.append(f"{quote_id} has non-contiguous word indices")
        for word in words:
            for field in ("iast", "deva", "gloss", "parts", "stem", "affix", "morph", "evidence"):
                if word.get(field) in (None, "", []):
                    errors.append(f"{quote_id} word {word.get('i')} lacks {field}")
    if errors:
        raise ValueError("\n".join(errors[:100]))
    all_words = [word for row in rows.values() for word in row["words"]]
    return {
        "quotes": len(rows), "word_instances": len(all_words),
        "unique_surface_forms": len({word["iast"] for word in all_words}),
        "quotes_requiring_review": sum(row["status"] == "review-required" for row in rows.values()),
        "words_with_uncertainty": sum(bool(word.get("note")) for word in all_words),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vidyut-data", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        data = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    else:
        if not args.vidyut_data:
            raise ValueError("--vidyut-data is required when generating")
        data = build(args.vidyut_data)
        OUTPUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(validate(data), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
