"""Exact naming tables: an Analysis's grammatical values (in any of the spellings the oracle or a
producer may use: IAST, Vidyut enum names, English abbreviations, numbers) → one canonical
value, and canonical values → the Pāṇinian affix names and the plain-English morphology the
card prints. Tables only; nothing is inferred from a form."""
from __future__ import annotations

import re
import unicodedata

from . import common as C


def _k(s) -> str:
    return C.latin_key(str(s)) if s is not None else ""


VIBHAKTI = {  # canonical 1..8 (8 = sambodhana)
    1: ["prathama", "prathamaa", "nom", "nominative", "1"], 2: ["dvitiya", "dvitiyaa", "acc", "accusative", "2"],
    3: ["trtiya", "tritiya", "instr", "ins", "instrumental", "3"], 4: ["caturthi", "chaturthi", "dat", "dative", "4"],
    5: ["pancami", "panchami", "abl", "ablative", "5"], 6: ["sasthi", "shashthi", "sashthi", "gen", "genitive", "6"],
    7: ["saptami", "loc", "locative", "7"], 8: ["sambodhana", "voc", "vocative", "8"],
}
_VIB = {a: n for n, al in VIBHAKTI.items() for a in al}
VIB_IAST = {1: "prathamā", 2: "dvitīyā", 3: "tṛtīyā", 4: "caturthī", 5: "pañcamī", 6: "ṣaṣṭhī", 7: "saptamī", 8: "sambodhana"}
VIB_EN = {1: "nom.", 2: "acc.", 3: "instr.", 4: "dat.", 5: "abl.", 6: "gen.", 7: "loc.", 8: "voc."}

VACANA = {"sg": ["eka", "ekavacana", "sg", "singular", "s", "1"], "du": ["dvi", "dvivacana", "du", "dual", "d", "2"],
          "pl": ["bahu", "bahuvacana", "pl", "plural", "p", "3"]}
_VAC = {a: n for n, al in VACANA.items() for a in al}
VAC_IAST = {"sg": "ekavacana", "du": "dvivacana", "pl": "bahuvacana"}
VAC_IDX = {"sg": 0, "du": 1, "pl": 2}

LINGA = {"masc": ["pum", "pumlinga", "punlinga", "pumllinga", "masc", "masculine", "m"],
         "fem": ["stri", "strilinga", "fem", "feminine", "f"],
         "neut": ["napumsaka", "napumsakalinga", "napunsaka", "neut", "neuter", "n"]}
_LIN = {a: n for n, al in LINGA.items() for a in al}

PURUSHA = {3: ["prathama", "prathamapurusa", "third", "3rd", "3"], 2: ["madhyama", "madhyamapurusa", "second", "2nd", "2"],
           1: ["uttama", "uttamapurusa", "first", "1st", "1"]}
_PUR = {a: n for n, al in PURUSHA.items() for a in al}
PUR_EN = {3: "3rd", 2: "2nd", 1: "1st"}
PUR_IAST = {3: "prathama-puruṣa", 2: "madhyama-puruṣa", 1: "uttama-puruṣa"}

LAKARA = {  # canonical IAST → English
    "laṭ": "present indicative", "liṭ": "perfect", "luṭ": "periphrastic future", "lṛṭ": "future",
    "leṭ": "subjunctive", "loṭ": "imperative", "laṅ": "imperfect", "vidhiliṅ": "optative",
    "āśīrliṅ": "benedictive", "luṅ": "aorist", "lṛṅ": "conditional",
}
_LAK = {"lat": "laṭ", "lit": "liṭ", "lut": "luṭ", "lrt": "lṛṭ", "let": "leṭ", "lot": "loṭ", "lan": "laṅ",
        "vidhilin": "vidhiliṅ", "vidhilim": "vidhiliṅ", "lin": "vidhiliṅ", "optative": "vidhiliṅ",
        "ashirlin": "āśīrliṅ", "asirlin": "āśīrliṅ", "lun": "luṅ", "lrn": "lṛṅ",
        "present": "laṭ", "perfect": "liṭ", "future": "lṛṭ", "imperative": "loṭ", "imperfect": "laṅ", "aorist": "luṅ"}

PADA = {"P": ["p", "parasmai", "parasmaipada"], "A": ["a", "atmane", "atmanepada"], "U": ["u", "ubhaya", "ubhayapada"]}
_PAD = {a: n for n, al in PADA.items() for a in al}
PADA_IAST = {"P": "parasmaipada", "A": "ātmanepada", "U": "ubhayapada"}

PRAYOGA = {"kartari": ["kartari", "kartr", "active"], "karmani": ["karmani", "passive"], "bhave": ["bhave", "impersonal"]}
_PRA = {a: n for n, al in PRAYOGA.items() for a in al}

GANA_NAMES = {1: "bhvādi", 2: "adādi", 3: "juhotyādi", 4: "divādi", 5: "svādi", 6: "tudādi", 7: "rudhādi",
              8: "tanādi", 9: "kryādi", 10: "curādi"}

TIN = {"P": {3: ["tip", "tas", "jhi"], 2: ["sip", "thas", "tha"], 1: ["mip", "vas", "mas"]},
       "A": {3: ["ta", "ātām", "jha"], 2: ["thās", "āthām", "dhvam"], 1: ["iṭ", "vahi", "mahiṅ"]}}
SUP = {1: ["su", "au", "jas"], 2: ["am", "auṭ", "śas"], 3: ["ṭā", "bhyām", "bhis"], 4: ["ṅe", "bhyām", "bhyas"],
       5: ["ṅasi", "bhyām", "bhyas"], 6: ["ṅas", "os", "ām"], 7: ["ṅi", "os", "sup"], 8: ["su", "au", "jas"]}

KRT_GLOSS = {
    "kta": "past participle (niṣṭhā)", "ktavatu": "past active participle (niṣṭhā)", "śatṛ": "present participle",
    "śānac": "present participle (middle)", "ktvā": "absolutive", "lyap": "absolutive after a prefix",
    "tumun": "infinitive", "tavya": "gerundive", "tavyat": "gerundive", "anīyar": "gerundive", "yat": "gerundive",
    "ṇyat": "gerundive", "kyap": "gerundive", "ṇvul": "agent noun", "tṛc": "agent noun", "tṛn": "agent noun",
    "lyuṭ": "action noun", "ghañ": "action noun", "ktin": "action noun", "ap": "action noun", "ac": "noun of action or agent",
    "ka": "noun of action or agent", "kvip": "agent (zero affix)", "ṇini": "agent (habitual)", "aṇ": "agent",
    "khaś": "agent", "ṭa": "agent", "ḍa": "agent", "ini": "possessive", "u": "agent noun", "manin": "action noun",
    "asun": "noun", "ṇic": "causative",
}
KRT_FORM_CAT = {"kta": "participle_past", "ktavatu": "participle_past_active", "śatṛ": "participle_present",
                "śānac": "participle_present", "ktvā": "absolutive", "lyap": "absolutive", "tumun": "infinitive"}
INDECLINABLE_KRT = {"ktvā", "lyap", "tumun", "ṇamul"}

UPASARGA_GLOSS = {
    "pra": "forth", "parā": "away", "apa": "away", "sam": "together", "anu": "after, along", "ava": "down",
    "nis": "out", "nir": "out", "dus": "ill", "dur": "ill", "vi": "apart", "ā": "toward, near", "āṅ": "toward, near",
    "ni": "down, in", "adhi": "over", "api": "on", "ati": "beyond", "su": "well", "ud": "up", "ut": "up",
    "abhi": "toward", "prati": "back, toward", "pari": "around, wholly", "upa": "near",
}

PARTICLES = {"ca", "na", "eva", "api", "hi", "tu", "iti", "vā", "sma", "ha", "u", "atha", "tathā", "yathā", "iva",
             "evam", "ced", "cet", "nu", "khalu", "kila", "tatas", "tataḥ", "yadi", "yatra", "tatra", "punar",
             "punaḥ", "ā", "mā", "nā", "aho", "bata", "he", "bhoḥ", "om", "tat", "iha", "atra", "kva", "katham"}
PRONOUNS = {"asmad", "yuṣmad", "tad", "yad", "idam", "etad", "kim", "adas", "bhavat", "svayam", "anya", "eka"}
COPULA_ROOTS = {"as"}


def vibhakti(v) -> int | None:
    if isinstance(v, int):
        return v if 1 <= v <= 8 else None
    return _VIB.get(_k(v).rstrip("a") if _k(v) not in _VIB else _k(v)) or _VIB.get(_k(v))


def vacana(v) -> str | None:
    return _VAC.get(_k(v)) if v is not None else None


def linga(v) -> str | None:
    return _LIN.get(_k(v)) if v is not None else None


def purusha(v) -> int | None:
    if isinstance(v, int):
        return v if v in (1, 2, 3) else None
    return _PUR.get(_k(v)) if v is not None else None


def lakara(v) -> str | None:
    if v is None:
        return None
    s = unicodedata.normalize("NFC", str(v))
    if s in LAKARA:
        return s
    return _LAK.get(_k(v))


def pada(v) -> str | None:
    if v is None:
        return None
    if str(v) in ("P", "A", "U"):
        return str(v)
    return _PAD.get(_k(v))


def prayoga(v) -> str | None:
    return _PRA.get(_k(v)) if v is not None else None


def gana(v) -> int | None:
    try:
        g = int(v)
        return g if g in GANA_NAMES else None
    except (TypeError, ValueError):
        k = _k(v)
        return next((n for n, nm in GANA_NAMES.items() if C.latin_key(nm) == k), None)


def affix_name(a: str | None) -> str | None:
    if not a:
        return None
    s = unicodedata.normalize("NFC", str(a)).strip()
    for known in list(KRT_GLOSS) + ["tamap", "tarap", "matup", "vatup", "tva", "tal", "ṭhak", "aṇ", "yat", "cha", "ṭhañ"]:
        if C.latin_key(known) == C.latin_key(s):
            return known
    return s


def ending_pada(an: dict) -> str | None:
    """Pada of the tiṅ ending: an explicit oracle field, else passive/impersonal → A, else the
    root's own P or A; None for an ubhayapada root without an explicit field."""
    extra = an.get("extra") or {}
    for k in ("pada", "ending_pada", "tin_pada"):
        p = pada(an.get(k)) or pada(extra.get(k))
        if p in ("P", "A"):
            return p
    if prayoga(an.get("prayoga")) in ("karmani", "bhave"):
        return "A"
    d = an.get("dhatu") or {}
    p = pada(d.get("pada"))
    return p if p in ("P", "A") else None


def sup_name(vib: int | None, vac: str | None) -> str | None:
    if vib is None or vac is None:
        return None
    return SUP[vib][VAC_IDX[vac]]


def tin_name(pd: str | None, pur: int | None, vac: str | None) -> str | None:
    if pd not in ("P", "A") or pur is None or vac is None:
        return None
    return TIN[pd][pur][VAC_IDX[vac]]


def morph_text(an: dict) -> str:
    kind = an.get("kind")
    krt = affix_name(an.get("krt"))
    if kind == "tinanta":
        lk, pur, vac = lakara(an.get("lakara")), purusha(an.get("purusha")), vacana(an.get("vacana"))
        parts = [LAKARA.get(lk, lk or "finite verb")]
        if pur and vac:
            parts.append(f"{PUR_EN[pur]} {vac}.")
        pd = ending_pada(an)
        if prayoga(an.get("prayoga")) == "karmani":
            parts.append("passive")
        elif pd:
            parts.append(PADA_IAST[pd])
        return ", ".join(parts)
    if kind == "avyaya" or (krt in INDECLINABLE_KRT):
        if krt in ("ktvā", "lyap"):
            return "absolutive"
        if krt == "tumun":
            return "infinitive"
        return "indeclinable"
    vib, vac, lin = vibhakti(an.get("vibhakti")), vacana(an.get("vacana")), linga(an.get("linga"))
    if C.nfc(an.get("stem") or "") in ("asmad", "yuṣmad"):
        lin = None                       # personal pronouns have no gender
    bits = [VIB_EN.get(vib, ""), f"{vac}." if vac else "", f"{lin}." if lin else ""]
    s = " ".join(b for b in bits if b)
    if krt in KRT_FORM_CAT and KRT_FORM_CAT[krt].startswith("participle"):
        s += f" ({KRT_GLOSS[krt]})"
    return s or "form not specified"


def affix_text(an: dict) -> str:
    kind = an.get("kind")
    krt, tad = affix_name(an.get("krt")), affix_name(an.get("taddhita"))
    pieces = []
    if krt:
        pieces.append(f"{krt} (kṛt)")
    if tad:
        pieces.append(f"{tad} (taddhita)")
    if kind == "tinanta":
        lk = lakara(an.get("lakara"))
        pur, vac = purusha(an.get("purusha")), vacana(an.get("vacana"))
        tin = (an.get("ending") or {}).get("name") or tin_name(ending_pada(an), pur, vac)
        label = f"{PUR_IAST[pur]} {VAC_IAST[vac]}" if pur and vac else ""
        pieces.append(f"{lk or 'lakāra not given'}" + (f", {tin}" if tin else "") + (f" ({label})" if label else ""))
    elif kind == "avyaya" or krt in INDECLINABLE_KRT:
        pieces.append("avyaya")
    else:
        vib, vac = vibhakti(an.get("vibhakti")), vacana(an.get("vacana"))
        sup = (an.get("ending") or {}).get("name") if (an.get("ending") or {}).get("type") == "sup" else sup_name(vib, vac)
        if sup and vib and vac:
            pieces.append(f"{sup} ({VIB_IAST[vib]} {VAC_IAST[vac]})")
        if kind == "samasa":
            pieces.insert(0, "samāsa")
    return " + ".join(pieces) if pieces else "not specified"


def form_category(an: dict) -> str:
    krt = affix_name(an.get("krt"))
    if krt in KRT_FORM_CAT:
        return KRT_FORM_CAT[krt]
    if krt in ("tṛc", "tṛn", "ṇvul", "ṇini"):
        return "agent"
    return "finite" if an.get("kind") == "tinanta" else "noun"


def word_class(an: dict) -> str:
    stem = C.nfc(an.get("stem") or "")
    d = an.get("dhatu") or {}
    if an.get("kind") == "tinanta" and C.nfc(d.get("root") or "") in COPULA_ROOTS and not d.get("upasargas"):
        return "copula"
    if stem in PRONOUNS:
        return "pronoun"
    if an.get("kind") == "avyaya" and (stem in PARTICLES or C.form_key(an.get("form") or "") in PARTICLES):
        return "particle"
    return "content"


def verb_stem(an: dict) -> str | None:
    """'pari-upa-√ās' for a tiṅanta (upasargas, the root, sanādi affixes)."""
    d = an.get("dhatu") or {}
    if an.get("kind") != "tinanta" or not d.get("root"):
        return None
    ups = [u for u in d.get("upasargas") or [] if isinstance(u, str)]
    s = "-".join(ups + [f"√{d['root']}"])
    san = [str(x) for x in d.get("sanadi") or []]
    return s + (f" ({', '.join(san)})" if san else "")


def root_string(d: dict) -> str | None:
    if not d or not d.get("root"):
        return None
    g, p = gana(d.get("gana")), pada(d.get("pada"))
    if not g or not p:
        return f"√{d['root']}"
    s = f"√{d['root']} ({GANA_NAMES[g]}, {g}{p}"
    if d.get("artha"):
        s += f", '{d['artha']}'"
    return s + ")"


def dp_id(d: dict | None) -> str | None:
    """The Dhātupāṭha record serial from an Analysis.dhatu.dp_locus ('…dhatupatha.json#1011153')."""
    if not d:
        return None
    for k in ("dp_record", "root_id", "dp_locus"):
        m = re.search(r"dhatupatha\.json#(\d{6,8})$|^(\d{6,8})$", str(d.get(k) or ""))
        if m:
            return m.group(1) or m.group(2)
    return None
