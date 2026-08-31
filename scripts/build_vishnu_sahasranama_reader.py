#!/usr/bin/env python3
"""Build and validate the Viṣṇusahasranāma reader corpus.

The builder keeps four concerns separate:

* the received 107-stanza chant text (a pinned ITRANS transcription),
* the BORI critical-edition witness and its stable loci,
* deterministic 1–1000 name boundaries (a pinned word-split aid), and
* Swami Chinmayananda's scan-checked English commentary.

No English from the word-split aid is copied into the reader.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import tempfile
import unicodedata
import urllib.request
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from chinmayananda_sanskrit_blocks import promote_non_gita_blocks
from chinmayananda_inline_sanskrit import (
    ASCII_ACCEPTED_IDS, ASCII_STRUCTURED_IDS, phrase_gloss_for_unit,
    promote_inline_blocks, slot_plain_text, word_for_word_slots,
)
from validate_chinmayananda_derivation_reviews import alternatives_by_name
from validate_chinmayananda_footnote_apparatus import merged_footnotes


ROOT = Path(__file__).resolve().parents[1]
BORI_PATH = ROOT / "data/sources/sanskrit/vedanta/vishnu_sahasranama_bori_critical_excerpt.txt"
COMMENTARY_PATH = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
ANALYSIS_PATH = ROOT / "gita/vishnu-sahasranama/analysis.json"
COMMENTARY_QUOTES_PATH = ROOT / "gita/vishnu-sahasranama/commentary-quotes.json"
COMMENTARY_QUOTE_ANALYSIS_PATH = ROOT / "gita/vishnu-sahasranama/commentary-quote-analysis.json"
COMMENTARY_QUOTE_REVIEW_PATH = ROOT / "gita/vishnu-sahasranama/gita-quote-panini-review.json"
PREFACE_COMMENTARY_PATH = ROOT / "gita/vishnu-sahasranama/preface-commentary.json"
PREFACE_WITNESS_PATH = ROOT / "data/sources/sanskrit/vedanta/vishnu_sahasranama_performance_preface.json"
PREFACE_ANALYSIS_PATH = ROOT / "gita/vishnu-sahasranama/preface-analysis.json"
TIMINGS_PATH = ROOT / "gita/vishnu-sahasranama/timings.json"
FOOTNOTE_PUBLIC_OVERRIDE_PATHS = tuple(
    ROOT / f"internal/sanskrit_reviews/fn-override-part{index}.json"
    for index in range(1, 6)
)
FOOTNOTE_PUBLIC_OVERRIDE_IDS = {
    "cm-vs-fn-p020-n01",
    "cm-vs-fn-p043-n02", "cm-vs-fn-p107-n02", "cm-vs-fn-p111-n02",
    "cm-vs-fn-p114-n03", "cm-vs-fn-p141-n03", "cm-vs-fn-p150-n01",
    "cm-vs-fn-p150-n02", "cm-vs-fn-p199-n01", "cm-vs-fn-p202-n02",
    "cm-vs-fn-p215-n01", "cm-vs-fn-p227-n01",
}
FOOTNOTE_OVERRIDE_REPLACED_ASCII_IDS = {
    "name-1-paragraph-1-ascii-0", "name-1-paragraph-1-ascii-1",
    "name-1-paragraph-1-ascii-2",
    "name-545-paragraph-1-ascii-0", "name-545-paragraph-2-ascii-0",
    "name-545-paragraph-2-ascii-1", "name-770-paragraph-1-ascii-0",
    "name-779-paragraph-3-ascii-0", "name-779-paragraph-3-ascii-1",
    "name-779-paragraph-3-ascii-2", "name-779-paragraph-3-ascii-3",
    "name-888-paragraph-2-ascii-0",
}
OUTPUT_PATH = ROOT / "gita/vishnu-sahasranama/reader.json"
WEB_CORE_PATH = ROOT / "gita/vishnu-sahasranama/reader-core.json"
WEB_DETAILS_PATH = ROOT / "gita/vishnu-sahasranama/reader-details.json"
WEB_DETAIL_FIELDS = ("word_analysis", "chinmayananda", "traditional_derivation")
PRESENTATION_OVERRIDES_PATH = ROOT / "gita/vishnu-sahasranama/reader_review_overrides.json"

RECEIVED_URL = "https://sanskritdocuments.org/doc_vishhnu/vsahasranew.itx"
RECEIVED_SHA256 = "b53e64398d0a340dd01d2a83979c13346d6b27ec29f50a46a41b9d14080bb19b"
WORD_SPLIT_URL = (
    "https://raw.githubusercontent.com/shreevatsa/word-split-sahasranama/"
    "2d1fe249574a63680ca8a9703b158377f9eaf468/data.js"
)
WORD_SPLIT_SHA256 = "a1ed8575023cdad456376b24e99e3b6d62a6427443e51af5c4b2cd8260a1ac27"

FORBIDDEN_OCR_FRAGMENTS = (
    "newpage",
    "Vishnii Sahasranaama",
    "Glorifs Of The Lord",
    "effinewpage",
    "yudhishnewpage",
)

# Conjunctions and discourse particles belong to the stanza but are not part
# of the numbered name. The boundary aid intentionally omits them; keep these
# exact name surfaces clean instead of attaching the residual text to a name.
SURFACE_OVERRIDES = {
    11: "paramātmā",
    17: "akṣara",
    262: "vardhamānaś",
    305: "vyaktarūpaś",
    447: "mahejyaś",
    715: "durdharo",
    716: "aparājitaḥ",
    984: "annāda",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def commentary_quote_source_sha256(commentary: dict[int, dict]) -> str:
    rows = [
        {"number": number, "commentary": commentary[number]["commentary"]}
        for number in sorted(commentary)
    ]
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8"))


SANSKRIT_LETTER_RE = re.compile(r"[\u0900-\u097fāīūṛṝḷṅñṭḍṇśṣṃḥ]")
LATIN_LETTER_RE = re.compile(r"[A-Za-z]")


def block_is_sanskrit_quote(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if not re.match(r'^[“"‘’\(\s]*[\u0900-\u097f]', stripped):
        return False
    return bool(SANSKRIT_LETTER_RE.search(stripped))


def block_quote_iast(text: str) -> str | None:
    stripped = text.strip()
    if not stripped:
        return None
    paren_candidates = re.findall(r"\(([^()]*)\)", stripped)
    for candidate in paren_candidates:
        candidate = candidate.strip().strip('"“”‘’')
        if candidate and LATIN_LETTER_RE.search(candidate) and not re.search(r"[\u0900-\u097f]", candidate):
            return candidate
    if not re.search(r"[\u0900-\u097f]", stripped):
        return None
    if not LATIN_LETTER_RE.search(stripped):
        return normalize_iast(transliterate(stripped, sanscript.DEVANAGARI, sanscript.IAST))
    lead = re.split(r"[A-Za-z]", stripped, maxsplit=1)[0].strip()
    lead = lead.rstrip("—–-.:;၊।॥, ").strip()
    if not lead:
        return None
    if re.search(r"[\u0900-\u097f]", lead):
        return normalize_iast(transliterate(lead, sanscript.DEVANAGARI, sanscript.IAST))
    return None


def assert_public_analysis_gate(analysis_path: Path | None) -> None:
    """Refuse publication while any Sanskrit card rests on provisional tools."""
    blockers = []
    if not analysis_path or not analysis_path.exists():
        blockers.append("the 1,000-name analysis corpus is missing")
    else:
        name_data = json.loads(analysis_path.read_text(encoding="utf-8"))
        if name_data.get("review_status") != "primary-grammar-reviewed-complete":
            blockers.append("the 1,000-name analysis corpus lacks complete primary-grammar review")

    preface_data = json.loads(PREFACE_ANALYSIS_PATH.read_text(encoding="utf-8"))
    if preface_data.get("review_status") != "primary-grammar-reviewed-complete":
        blockers.append("the performed-preface analysis lacks complete primary-grammar review")

    if not COMMENTARY_QUOTE_ANALYSIS_PATH.exists():
        blockers.append("the Gītā quote analysis corpus is missing")
    else:
        review = json.loads(COMMENTARY_QUOTE_ANALYSIS_PATH.read_text(encoding="utf-8"))
        if review.get("review_status") != "primary-grammar-reviewed-complete":
            blockers.append("the embedded-Gītā analysis lacks complete primary-source review")

    if blockers:
        raise ValueError(
            "public Sanskrit-analysis gate failed: " + "; ".join(blockers)
            + ". Computational comparison output may not be published."
        )


def load_pinned(path: Path | None, url: str, expected: str) -> str:
    if path:
        data = path.read_bytes()
    else:
        request = urllib.request.Request(url, headers={"User-Agent": "vedanta-timeline-source-builder/1.0"})
        with urllib.request.urlopen(request, timeout=45) as response:
            data = response.read()
    actual = sha256(data)
    if actual != expected:
        raise ValueError(f"source checksum mismatch: expected {expected}, got {actual}")
    return data.decode("utf-8")


def normalize_iast(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    return (
        value.replace("ṁ", "ṃ")
        .replace("r̥", "ṛ")
        .replace("r̥̄", "ṝ")
        .replace("l̥", "ḷ")
        .replace("ō", "o")
        .replace("ē", "e")
        .replace("’", "'")
        .replace("‘", "'")
        .replace(" ", " ")
    )


def comparison_key(value: str) -> str:
    value = normalize_iast(value).lower().replace("'", "")
    value = re.sub(r"\(\d+\)", "", value)
    return "".join(ch for ch in value if ch.isalpha())


def parse_received_itx(source: str) -> list[dict]:
    start = source.index("\\section{stotram}")
    end = source.index("sarvapraharaNAyudha OM nama iti", start)
    lines = [line.strip() for line in source[start:end].splitlines()]
    lines = [line for line in lines if line and not line.startswith("\\section") and line != "hariH OM |"]
    if len(lines) != 214:
        raise ValueError(f"received text must contain 214 pāda lines, found {len(lines)}")

    stanzas = []
    for offset in range(0, len(lines), 2):
        first, second = lines[offset : offset + 2]
        number = offset // 2 + 1
        marker = re.search(r"\|\|\s*(\d+)\|\|", second)
        if not marker or int(marker.group(1)) != number:
            raise ValueError(f"received stanza numbering failure at {number}: {second}")
        variants = re.findall(r"\(([^)]+)\)", first)
        variants.extend(re.findall(r"\(([^)]+)\)", second[marker.end() :]))
        first = re.sub(r"\s*\([^)]+\)\s*", " ", first).strip()
        second = second[: marker.start()].rstrip()
        first = first.removesuffix("|").strip()
        # The source uses .h for an explicit halant. The transliteration library
        # expects the adjacent consonants directly in this lexical environment.
        itx_lines = [first.replace(".h", ""), second.replace(".h", "")]
        iast_lines = [normalize_iast(transliterate(line, sanscript.ITRANS, sanscript.IAST)) for line in itx_lines]
        deva_lines = [transliterate(line, sanscript.ITRANS, sanscript.DEVANAGARI) for line in itx_lines]
        stanza = {
                "number": number,
                "locus": f"VSN {number}",
                "devanagari": f"{deva_lines[0]} ।\n{deva_lines[1]} ॥",
                "iast": f"{iast_lines[0]} |\n{iast_lines[1]} ||",
                "received_itx": f"{itx_lines[0]} |\n{itx_lines[1]} || {number} ||",
            }
        if variants:
            stanza["received_variant_itx"] = variants
        stanzas.append(stanza)
    return stanzas


def transliterate_preface_unit(lines: list[str], unit_id: str, label: str, speaker: str | None = None) -> dict:
    cleaned = []
    for line in lines:
        line = re.sub(r"\s*\([^)]*\)\s*", " ", line).strip()
        line = line.replace("\\-", "").replace(".h", "")
        line = re.sub(r"\s*\|{1,2}\s*$", "", line).strip()
        if line:
            cleaned.append(line)
    if not cleaned:
        raise ValueError(f"performance preface unit {unit_id} is empty")
    iast = [normalize_iast(transliterate(line, sanscript.ITRANS, sanscript.IAST)) for line in cleaned]
    deva = [transliterate(line, sanscript.ITRANS, sanscript.DEVANAGARI) for line in cleaned]
    unit = {
        "id": unit_id,
        "label": label,
        "devanagari": "\n".join(f"{line} {'॥' if index == len(deva) - 1 else '।'}" for index, line in enumerate(deva)),
        "iast": "\n".join(f"{line} {'||' if index == len(iast) - 1 else '|'}" for index, line in enumerate(iast)),
        "received_itx": "\n".join(cleaned),
    }
    if speaker:
        unit["speaker"] = speaker
    return unit


def parse_numbered_preface_units(section: str, selected: set[int], prefix: str, speakers: dict[int, str] | None = None) -> list[dict]:
    for speaker_line in (
        "shrIvaishampAyana uvAcha \\-\\-\\-",
        "yudhiShThira uvAcha \\-\\-\\-",
        "bhIShma uvAcha \\-\\-\\-",
    ):
        section = section.replace(speaker_line, "")
    section = section.replace("\\-\n", "")
    lines = [line.strip() for line in section.splitlines() if line.strip()]
    units = []
    buffered = []
    for line in lines:
        if line.startswith("\\section"):
            continue
        buffered.append(line)
        marker = re.search(r"\|\|\s*(\d+)\|\|", line)
        if not marker:
            continue
        number = int(marker.group(1))
        buffered[-1] = line[: marker.start()].strip()
        if number in selected:
            units.append(transliterate_preface_unit(
                buffered,
                f"{prefix}-{number}",
                str(number),
                (speakers or {}).get(number),
            ))
        buffered = []
    if [int(unit["label"]) for unit in units] != sorted(selected):
        raise ValueError(f"could not recover the selected {prefix} units from the pinned witness")
    return units


def build_performance_preface(source: str) -> dict:
    """Recover only the prefatory material actually heard on the selected recording."""
    opening_start = source.index("shuklAmbaradharaM")
    opening_end = source.index("\\section{pUrvanyAsaH}", opening_start)
    opening = source[opening_start:opening_end]
    opening = re.sub(
        r"\(namaH samastabhUtAnAm.*?viShNave prabhaviShNave \|\|\)",
        "",
        opening,
        flags=re.S,
    )
    standalone_opening = "OM namo viShNave prabhaviShNave ||"
    opening_numbered = opening.replace(standalone_opening, "")
    invocation = parse_numbered_preface_units(opening_numbered, {1, 3, 4, 5, 6}, "invocation")
    invocation.append(transliterate_preface_unit([standalone_opening], "invocation-mantra", "Mantra"))

    dialogue = parse_numbered_preface_units(
        opening_numbered,
        set(range(7, 23)),
        "dialogue",
        {7: "Vaiśampāyana", 8: "Yudhiṣṭhira", 10: "Bhīṣma"},
    )

    assignment_start = source.index("OM asya shrIviShNor", opening_end)
    assignment_end = source.index("           atha nyAsaH", assignment_start)
    assignment_lines = [line.strip() for line in source[assignment_start:assignment_end].splitlines() if line.strip()]
    assignment_labels = (
        "Assignment", "Seer", "Metre", "Deity", "Seed", "Power", "Supreme mantra", "Key",
        "Weapon", "Eyes", "Armour", "Source", "Boundary", "Meditation", "Purpose",
    )
    assignment = [
        transliterate_preface_unit([line], f"assignment-{index}", assignment_labels[index - 1])
        for index, line in enumerate(assignment_lines, 1)
    ]

    meditation_start = source.index("kShIrodanvatpradeshe", assignment_end)
    meditation_end = source.index("\\section{stotram}", meditation_start)
    meditation_source = source[meditation_start:meditation_end]
    meditation_mantra = "OM namo bhagavate vAsudevAya ||"
    meditation_numbered = meditation_source.replace(meditation_mantra, "")
    # Abhyankar performs the source's parenthetical śobhi-kaustubham variant,
    # not its primary kaustubha-śriyam reading.
    meditation_numbered = meditation_numbered.replace(
        "sahAravakShaHsthalakaustubhashriyaM (sthalashobhikaustubhaM)",
        "sahAravakShaHsthalashobhikaustubhaM",
    )
    meditation = parse_numbered_preface_units(meditation_numbered, set(range(1, 8)), "meditation")
    meditation.insert(2, transliterate_preface_unit([meditation_mantra], "meditation-mantra", "Mantra"))

    groups = [
        {"id": "invocation", "title": "Invocation", "units": invocation},
        {"id": "dialogue", "title": "Yudhiṣṭhira and Bhīṣma", "units": dialogue},
        {"id": "assignment", "title": "Ritual assignment", "units": assignment},
        {"id": "meditation", "title": "Meditation", "units": meditation},
    ]
    return {
        "schema_version": 1,
        "title": "Opening performed before the thousand names",
        "source": {
            "url": RECEIVED_URL,
            "sha256": RECEIVED_SHA256,
            "selection_basis": "Exact sequence matched to the selected Sanjeev Abhyankar recording through the official publisher video and its original-language captions; variants and unperformed nyāsa passages are excluded.",
            "sequence_status": "official-publisher-caption-assisted",
        },
        "audio": {
            "official_reference": "https://www.youtube.com/watch?v=s9S6umIoH6I",
            "thousand_names_begin_approx_seconds": 498.08,
            "timing_status": "provisional-section-boundary",
        },
        "groups": groups,
    }


def attach_preface_commentary(preface: dict, commentary_path: Path | None) -> dict:
    enriched = json.loads(json.dumps(preface, ensure_ascii=False))
    if not commentary_path or not commentary_path.exists():
        return enriched
    commentary = json.loads(commentary_path.read_text(encoding="utf-8"))
    commentary_groups = commentary.get("groups", {})
    unit_commentary = commentary.get("units", {})
    for group in enriched["groups"]:
        context = commentary_groups.get(group["id"])
        if context:
            group["chinmayananda"] = context
        for unit in group["units"]:
            context = unit_commentary.get(unit["id"])
            if context:
                unit["chinmayananda"] = context
    return enriched


def attach_preface_analysis(preface: dict, analysis_path: Path) -> dict:
    enriched = json.loads(json.dumps(preface, ensure_ascii=False))
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    rows = analysis.get("units", [])
    expected = [unit["id"] for group in enriched["groups"] for unit in group["units"]]
    if [row.get("id") for row in rows[:len(expected)]] != expected:
        raise ValueError("performance-preface analysis does not exactly cover the performed unit sequence")
    by_id = {row["id"]: row for row in rows}
    for group in enriched["groups"]:
        for unit in group["units"]:
            row = by_id[unit["id"]]
            unit["words"] = row["words"]
            unit["english"] = row["english"]
            unit["analysis_status"] = row["source_status"]
    return enriched


def load_postlude_analysis(analysis_path: Path) -> list[dict]:
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    rows = analysis.get("units", [])
    postlude = [row for row in rows if row.get("id") in {"closing-name", "protection"}]
    if [row.get("id") for row in postlude] != ["closing-name", "protection"]:
        raise ValueError("performance analysis lacks the two recorded closing units")
    return postlude


def parse_bori(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    devanagari, roman = text.split("[DEVANAGARI]\n", 1)[1].split("\n\n[ROMAN_ISO_15919]\n", 1)
    deva_rows = [line.split(" ", 1) for line in devanagari.strip().splitlines()]
    roman_rows = [line.split(" ", 1) for line in roman.strip().splitlines()]
    if len(deva_rows) != 214 or len(roman_rows) != 214:
        raise ValueError("BORI excerpt must contain 214 Devanāgarī and 214 Roman rows")
    out = []
    for offset in range(0, 214, 2):
        d = deva_rows[offset : offset + 2]
        r = roman_rows[offset : offset + 2]
        expected = 13135014 + offset // 2
        if not all(int(row[0][:8]) == expected for row in d + r):
            raise ValueError(f"BORI locus mismatch near stanza {offset // 2 + 1}")
        out.append(
            {
                "loci": [d[0][0], d[1][0]],
                "devanagari": f"{d[0][1]} ।\n{d[1][1]} ॥",
                "iast": f"{normalize_iast(r[0][1])} |\n{normalize_iast(r[1][1])} ||",
            }
        )
    return out


def parse_word_split(source: str) -> tuple[list[dict], list[dict]]:
    prefix = "const data = "
    if not source.startswith(prefix):
        raise ValueError("word-split aid has an unexpected wrapper")
    payload = source[len(prefix) :].strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    data = json.loads(payload)
    named_stanzas = []
    all_names = []
    for record in data:
        stanza_names = []
        for line_index, line in enumerate(record.get("lines", [])):
            for item in line:
                if not (isinstance(item, list) and len(item) >= 3 and isinstance(item[2], int)):
                    continue
                # The aid's numeric labels contain one known transposition
                # (Anagha/Achintya). The chant sequence itself is continuous,
                # so assign the canonical number from performance order while
                # retaining the aid label for audit.
                number = len(all_names) + 1
                citation = normalize_iast(item[1].split(":", 1)[0]).strip().lower()
                surface = normalize_iast(item[0]).strip().lower()
                name = {
                    "number": number,
                    "citation_iast": citation,
                    "surface_iast": surface,
                    "line_index": line_index,
                }
                if item[2] != number:
                    name["boundary_aid_number"] = item[2]
                stanza_names.append(name)
                all_names.append(name)
        if stanza_names:
            named_stanzas.append({"names": stanza_names})
    all_names.sort(key=lambda item: item["number"])
    if len(named_stanzas) != 107:
        raise ValueError(f"word-split aid must contain 107 named stanzas, found {len(named_stanzas)}")
    if [item["number"] for item in all_names] != list(range(1, 1001)):
        raise ValueError("word-split aid does not provide exactly names 1–1000")
    return named_stanzas, all_names


def align_name_surfaces(stanza_iast: str, names: list[dict]) -> list[int]:
    """Project approximate name boundaries onto the exact received text."""
    target = comparison_key(stanza_iast)
    if target.startswith("oṃ"):
        target = target[2:]
    aid_tokens = [comparison_key(name["surface_iast"]) for name in names]
    source = "".join(aid_tokens)
    matcher = difflib.SequenceMatcher(a=source, b=target, autojunk=False)
    mapping: list[int | None] = [None] * (len(source) + 1)
    for _tag, a0, a1, b0, b1 in matcher.get_opcodes():
        width = a1 - a0
        for pos in range(a0, a1 + 1):
            fraction = 0 if width == 0 else (pos - a0) / width
            mapping[pos] = round(b0 + fraction * (b1 - b0))
    mapping[0] = 0
    mapping[-1] = len(target)
    last = 0
    for index, value in enumerate(mapping):
        if value is None:
            value = last
        value = max(last, min(len(target), value))
        mapping[index] = value
        last = value

    changed = []
    source_offset = 0
    recovered = []
    for name, token in zip(names, aid_tokens):
        start = mapping[source_offset]
        end = mapping[source_offset + len(token)]
        exact = target[start:end]
        if not exact:
            raise ValueError(f"empty aligned surface for name {name['number']}")
        old = comparison_key(name["surface_iast"])
        if old != exact:
            name["boundary_aid_surface"] = name["surface_iast"]
            name["surface_iast"] = exact
            changed.append(name["number"])
        recovered.append(comparison_key(name["surface_iast"]))
        source_offset += len(token)
    if "".join(recovered) != target:
        raise ValueError(f"name boundaries do not replay stanza text; names {names[0]['number']}–{names[-1]['number']}")
    return changed


def first_definition(commentary: str) -> str:
    paragraph = next((part.strip() for part in commentary.split("\n\n") if part.strip()), commentary.strip())
    paragraph = re.sub(r"^[—–\-\s]+", "", paragraph)
    paragraph = re.sub(r"\s+", " ", paragraph)
    # Keep a complete opening sentence where possible, but do not turn a long
    # first paragraph into a second copy of the commentary on the reading line.
    match = re.search(r"(?<=[.!?])(?:[\"'”’)]*)\s", paragraph)
    if match and match.end() <= 420:
        return paragraph[: match.end()].strip()
    if len(paragraph) <= 420:
        return paragraph
    return paragraph[:417].rstrip() + "…"


def traditional_derivation(commentary: str) -> str | None:
    sentences = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", commentary))
    selected = [
        sentence.strip()
        for sentence in sentences
        if re.search(r"\b(root|derived|derivation|dissolved|means?|etymolog|paanini|panini)\b", sentence, re.I)
    ]
    if not selected:
        return None
    text = " ".join(selected[:3])
    return text if len(text) <= 900 else text[:897].rstrip() + "…"


def commentary_detail(commentary: str, concise_meaning: str) -> str:
    """Return only Chinmayananda's explanation beyond the concise definition."""
    text = commentary.strip()
    concise = concise_meaning.strip()
    target = comparison_key(concise)
    collected = ""
    for index, char in enumerate(text):
        collected += comparison_key(char)
        if not target.startswith(collected):
            break
        if collected == target:
            return re.sub(r"^[\s.;:*†‡\"'“”‘’()\[\]—–-]+", "", text[index + 1 :]).strip()
    if text.startswith(concise):
        return re.sub(r"^[\s.;:—–-]+", "", text[len(concise) :]).strip()

    first_paragraph = text.split("\n\n", 1)[0]
    boundary = re.search(r"(?<=[.!?])(?:[\"'”’)]*)\s", first_paragraph)
    opening = first_paragraph[: boundary.end()].strip() if boundary else first_paragraph.strip()
    opening_without_asides = re.sub(r"\([^)]*\)", "", opening)
    opening_without_asides = re.sub(r"[*†‡]+", "", opening_without_asides)
    similarity = max(
        difflib.SequenceMatcher(a=comparison_key(candidate), b=comparison_key(concise), autojunk=False).ratio()
        for candidate in (opening, opening_without_asides)
    )
    if similarity >= 0.62:
        return re.sub(r"^[\s.;:—–-]+", "", text[len(opening) :]).strip()
    return text


def load_commentary(path: Path | None) -> dict[int, dict]:
    if not path or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("names", [])
    if [row.get("number") for row in rows] != list(range(1, 1001)):
        raise ValueError("Chinmayananda commentary must contain contiguous names 1–1000")
    return {row["number"]: row for row in rows}


def load_analysis(path: Path | None) -> dict[int, dict]:
    if not path or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("names", [])
    if [row.get("number") for row in rows] != list(range(1, 1001)):
        raise ValueError("Sanskrit analysis must contain contiguous names 1–1000")
    return {row["number"]: row for row in rows}


def english_source_key(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", ascii_text)


def lexical_phrase_range(text: str, phrase: str) -> tuple[int, int] | None:
    target = english_source_key(phrase)
    if not target:
        return None
    normalized = []
    source_indices = []
    for index, char in enumerate(text):
        folded = unicodedata.normalize("NFKD", char).encode("ascii", "ignore").decode().lower()
        for item in folded:
            if item.isalnum():
                normalized.append(item)
                source_indices.append(index)
    joined = "".join(normalized)
    start = joined.find(target)
    if start < 0:
        return None
    source_start = source_indices[start]
    source_end = source_indices[start + len(target) - 1] + 1
    while source_start > 0 and text[source_start - 1] in "\"'“‘":
        source_start -= 1
    while source_end < len(text) and text[source_end] in "\"'”’":
        source_end += 1
    return source_start, source_end


def lexical_phrase_ranges(text: str, phrase: str) -> list[tuple[int, int]]:
    """Return every normalized phrase occurrence with exact source offsets."""
    target = english_source_key(phrase)
    if not target:
        return []
    normalized = []
    source_indices = []
    for index, char in enumerate(text):
        folded = unicodedata.normalize("NFKD", char).encode("ascii", "ignore").decode().lower()
        for item in folded:
            if item.isalnum():
                normalized.append(item)
                source_indices.append(index)
    joined = "".join(normalized)
    result = []
    cursor = 0
    while True:
        start = joined.find(target, cursor)
        if start < 0:
            break
        source_start = source_indices[start]
        source_end = source_indices[start + len(target) - 1] + 1
        while source_start > 0 and text[source_start - 1] in "\"'“‘":
            source_start -= 1
        while source_end < len(text) and text[source_end] in "\"'”’":
            source_end += 1
        result.append((source_start, source_end))
        cursor = start + len(target)
    return result


def split_prose_block(block: dict, offset: int) -> tuple[dict | None, dict | None]:
    text = block.get("text", "")
    before_text = text[:offset].rstrip()
    raw_after = text[offset:]
    after_trim = len(raw_after) - len(raw_after.lstrip())
    after_text = raw_after.lstrip()
    existing_calls = list(block.get("footnote_calls", []))
    before = {
        key: value for key, value in block.items()
        if key not in {"text", "inline_sanskrit", "footnote_calls"}
    }
    after = dict(before)
    before["text"] = before_text
    after["text"] = after_text
    before_annotations = []
    after_annotations = []
    for annotation in block.get("inline_sanskrit", []):
        if int(annotation["end"]) <= offset:
            before_annotations.append(annotation)
        elif int(annotation["start"]) >= offset:
            value = dict(annotation)
            value["start"] = int(value["start"]) - offset - after_trim
            value["end"] = int(value["end"]) - offset - after_trim
            after_annotations.append(value)
        else:
            raise ValueError(
                f"footnote anchor splits Sanskrit annotation {annotation.get('id')}"
            )
    if before_annotations:
        before["inline_sanskrit"] = before_annotations
    if after_annotations:
        after["inline_sanskrit"] = after_annotations
    if existing_calls:
        (after if after_text else before)["footnote_calls"] = existing_calls
    return (
        before if re.search(r"[A-Za-z\u0900-\u097f]", before_text) else None,
        after if re.search(r"[A-Za-z\u0900-\u097f]", after_text) else None,
    )


def apply_footnote_apparatus(by_number: dict[int, dict], footnotes: list[dict]) -> None:
    """Move every page-bottom note from its OCR paragraph to its printed call."""
    public_overrides = {}
    for path in FOOTNOTE_PUBLIC_OVERRIDE_PATHS:
        override_data = json.loads(path.read_text(encoding="utf-8"))
        if override_data.get("schema_version") != 1 or override_data.get("review_status") != "complete":
            raise ValueError(f"{path.name}: footnote public payload override review is incomplete")
        if set(override_data.get("rows", {})) != set(override_data.get("expected_ids", [])):
            raise ValueError(f"{path.name}: public payload rows differ from expected_ids")
        overlap = set(public_overrides) & set(override_data["rows"])
        if overlap:
            raise ValueError(f"duplicate footnote public payload overrides: {sorted(overlap)}")
        public_overrides.update(override_data["rows"])
    if set(public_overrides) != FOOTNOTE_PUBLIC_OVERRIDE_IDS:
        raise ValueError("footnote public payload override population must be exactly 12 corrected notes")
    payloads = {}
    for footnote in footnotes:
        block_ids = footnote["current_containment"]["block_ids"]
        locations = []
        for block_id in block_ids:
            match = re.fullmatch(r"name-(\d+)-paragraph-(\d+)", block_id)
            if not match:
                raise ValueError(f"invalid footnote containment block id {block_id}")
            locations.append(tuple(map(int, match.groups())))
        source_numbers = {number for number, _index in locations}
        if len(source_numbers) != 1:
            raise ValueError(f"footnote {footnote['id']} payload spans multiple names")
        source_number = next(iter(source_numbers))
        paragraph_indices = {index for _number, index in locations}
        quote_ids = set(footnote["current_containment"].get("quote_ids", []))
        blocks = by_number[source_number]["chinmayananda"]["blocks"]
        source_payload = [
            block for block in blocks
            if block.get("source_paragraph_index") in paragraph_indices
            or block.get("id") in quote_ids
        ]
        payload = source_payload
        if not source_payload:
            source_note = footnote.get("note_text_normalized", "").strip()
            if len(source_note) <= 160 and not re.search(r"[\u0900-\u097f]", source_note):
                payload = [{
                    "type": "source-note",
                    "text": source_note,
                    "source_paragraph_indices": sorted(paragraph_indices),
                }]
            else:
                raise ValueError(f"footnote {footnote['id']} has no rendered payload blocks")
        if footnote["id"] in public_overrides:
            payload = public_overrides[footnote["id"]]["blocks"]
        payload_prose_key = english_source_key(" ".join(
            block.get("text", "") for block in payload if block.get("type") == "prose"
        ))
        for block in payload:
            english_key = english_source_key(block.get("english", ""))
            if (
                block.get("type") in ("gita-quote", "sanskrit-quote")
                and block.get("english_source") == "Swami Chinmayananda"
                and english_key
                and english_key not in payload_prose_key
            ):
                block["display_english"] = True
        payloads[footnote["id"]] = payload
        by_number[source_number]["chinmayananda"]["blocks"] = [
            block for block in blocks if block not in source_payload
        ]

    for footnote in footnotes:
        number = int(footnote["owner_name_number"])
        note = {
            "type": "footnote",
            "id": footnote["id"],
            "marker": footnote["marker_printed"],
            "pdf_page": footnote["pdf_page"],
            "printed_page": footnote["printed_page"],
            "blocks": payloads[footnote["id"]],
            "additional_name_numbers": footnote.get("additional_name_numbers", []),
        }
        if footnote.get("anchor_scope") == "root-text":
            call_number = int(footnote["root_call_name_number"])
            by_number[call_number].setdefault("root_footnote_calls", []).append({
                "id": footnote["id"],
                "marker": footnote["marker_printed"],
            })
            note["additional_name_numbers"] = sorted({
                number,
                *(int(value) for value in footnote.get("additional_name_numbers", [])),
            } - {call_number})
            by_number[call_number]["chinmayananda"]["blocks"].insert(0, note)
            continue
        blocks = by_number[number]["chinmayananda"]["blocks"]
        anchor = footnote["anchor_text_normalized"]
        matches = []
        for index, block in enumerate(blocks):
            if block.get("type") != "prose":
                continue
            for start, end in lexical_phrase_ranges(block.get("text", ""), anchor):
                matches.append((index, start, end))
        occurrence = int(footnote.get("anchor_occurrence", 0))
        if occurrence >= len(matches):
            raise ValueError(
                f"footnote {footnote['id']} anchor occurrence {occurrence} missing from name {number}"
            )
        block_index, _start, end = matches[occurrence]
        text = blocks[block_index].get("text", "")
        open_parens = text[:end].count("(") - text[:end].count(")")
        while open_parens > 0 and end < len(text):
            if text[end] == "(":
                open_parens += 1
            elif text[end] == ")":
                open_parens -= 1
            end += 1
        while end < len(text) and text[end] in "\"'”’)]}.,;:":
            end += 1
        before, after = split_prose_block(blocks[block_index], end)
        if not before:
            raise ValueError(f"footnote {footnote['id']} has no prose before its call")
        before.setdefault("footnote_calls", []).append({
            "id": footnote["id"],
            "marker": footnote["marker_printed"],
        })
        blocks[block_index:block_index + 1] = [before, note] + ([after] if after else [])

    # Scan review p.227 showed that this sentence continuation belongs to name
    # 887's body, not to the following name's footnote. Keep the source
    # transcription untouched, but repair the public block boundary.
    blocks_887 = by_number[887]["chinmayananda"]["blocks"]
    residue = next((block for block in blocks_887 if block.get("text") == "worldly and heavenly."), None)
    body = next((block for block in blocks_887 if block.get("source_paragraph_index") == 0), None)
    if not residue or not body:
        raise ValueError("reviewed p.227 name-887 continuation is missing")
    body_text = re.sub(r"forms\.$", "forms,", body["text"].rstrip())
    body["text"] = f"{body_text} worldly and heavenly."
    blocks_887.remove(residue)

    for item in by_number.values():
        blocks = item.get("chinmayananda", {}).get("blocks", [])
        index = 0
        while index < len(blocks):
            block = blocks[index]
            if block.get("type") != "prose" or not block.get("footnote_calls"):
                index += 1
                continue
            end = index + 1
            while end < len(blocks) and blocks[end].get("type") == "footnote":
                end += 1
            if end == index + 1:
                index = end
                continue
            order = {call["id"]: position for position, call in enumerate(block["footnote_calls"])}
            reordered = sorted(blocks[index + 1:end], key=lambda note: order.get(note.get("id"), len(order)))
            blocks[index + 1:end] = reordered
            index = end


def quote_word_for_reader(word: dict, index: int) -> dict:
    result = {
        "i": index, "iast": word["iast"], "deva": word["deva"],
        "gloss": word["gloss"], "parts": word["parts"], "stem": word["stem"],
        "affix": word["affix"], "morph": word["morph"],
    }
    notes = []
    root = word.get("root")
    if root:
        result["root"] = root["form"]
        result["rootGloss"] = root["gloss"]
        notes.append(f"{root['gana']}; {root['pada']}")
        dhatu = root.get("dhatupatha")
        if dhatu:
            notes.append(f"Dhātupāṭha {dhatu['locus']}: {dhatu['artha_sanskrit']}")
    if word.get("karaka"):
        notes.append(word["karaka"])
    if word.get("panini_rules"):
        notes.append("Pāṇini: " + ", ".join(rule["id"] for rule in word["panini_rules"]))
    if word.get("note"):
        notes.append(word["note"])
    if notes:
        result["note"] = " · ".join(notes)
    return result


def load_reviewed_quotes() -> dict[str, dict]:
    review = json.loads(COMMENTARY_QUOTE_ANALYSIS_PATH.read_text(encoding="utf-8"))
    if review.get("review_status") != "primary-grammar-reviewed-complete":
        return {}
    return {
        quote_id: row
        for quote_id, row in review.get("quotes", {}).items()
        if row.get("review_status") == "primary-text-reviewed"
    }


def normalize_author_translation_quotes(value: str, paragraph_placements: list[tuple[int, str, dict]]) -> str:
    for _position, basis, quote in paragraph_placements:
        if basis != "chinmayananda-translation-position":
            continue
        translation = str(quote.get("chinmayananda_translation", ""))
        start = value.find(translation)
        if start < 0:
            continue
        end = start + len(translation)
        has_open = start > 0 and value[start - 1] in "\"“"
        has_close = bool(re.match(r"^[,.;:!?]?[\"”’']", value[end:]))
        if has_open and not has_close:
            value = value[:end] + "\"" + value[end:]
        elif has_close and not has_open:
            value = value[:start] + "\"" + value[start:]
    return re.sub(r'^[“"]\s*[“"]', "“", value)


def remove_unmatched_parentheses(value: str) -> str:
    stack = []
    remove = set()
    for index, char in enumerate(value):
        if char == "(":
            stack.append(index)
        elif char == ")":
            if stack:
                stack.pop()
            else:
                remove.add(index)
    remove.update(stack)
    return "".join(char for index, char in enumerate(value) if index not in remove)


def parenthetical_is_romanization(value: str, rows: list[dict]) -> bool:
    """Distinguish a printed roman line from Chinmayananda's English gloss."""
    english_markers = re.findall(
        r"\b(?:the|a|an|is|am|are|among|which|where|all|beings|serpents?|sage|one|who|in|to|of)\b",
        value,
        flags=re.I,
    )
    if len(english_markers) >= 2:
        return False
    candidate = comparison_key(value)
    if not candidate:
        return False
    return max(
        difflib.SequenceMatcher(
            a=candidate,
            b=comparison_key(row.get("canonical_iast", "")),
            autojunk=False,
        ).ratio()
        for row in rows
    ) >= 0.40


def clean_rendered_commentary_prose(value: str, has_structured_quote: bool = False) -> str:
    """Remove punctuation shells left after a Sanskrit source line is lifted out."""
    if has_structured_quote:
        value = re.sub(
            r"\bIn\s+Gītā\.\s*\(\s*Ch\.?\s*[IVXLC\d]+\.?\s*St\.?\s*\d+\s*\)\s*",
            "In the Gītā, ",
            value,
            flags=re.I,
        )
        value = re.sub(
            r"\s*[—–-]*\s*\(\s*(?:Bhagavad\s+)?Gītā[^)]*\)",
            " ", value, flags=re.I,
        )
    value = re.sub(r"'{2,}", '"', value)
    value = re.sub(
        r'\b(says?)\s*["“”’\']+\s*\(([^)]+)\)',
        lambda match: f'{match.group(1)}: “{match.group(2).strip()}”',
        value,
        flags=re.I,
    )
    value = re.sub(r'-\s*"1"\s*', " ", value)
    value = re.sub(r"\s*[—–-]*\s*\(\s*\)", " ", value)
    value = re.sub(r"“\s*”", " ", value)
    value = re.sub(r'"\s*"(?=\s*(?:[—–),.;:]|$))', " ", value)
    value = re.sub(r'(?<=[(—–:-])"\s*"', " ", value)
    value = re.sub(r'^"\s*"', "", value)
    value = re.sub(r"\s*[—–-]*\s*\(\s*\)", " ", value)
    value = re.sub(r"\s*[—–-]+\s*([,.;])", r"\1", value)
    value = re.sub(r"\s*[—–-]+\s*[—–-]+\s*", " — ", value)
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    value = re.sub(r'(["”’])\s+\.', r"\1.", value)
    value = re.sub(r'([.!?])([\"”])\s*\.', r"\1\2", value)
    value = re.sub(r"([:;,])\s*\.", ".", value)
    value = remove_unmatched_parentheses(value)
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    value = re.sub(r"\s+-\s+(?=[A-ZĀ-Ž“\"])", " ", value)
    value = re.sub(r"\s+", " ", value).strip(" \t\n—–-*†‡")
    if re.fullmatch(r'(?:Refer\s*)?["“”\s—–-]*(?:Bhagavad\s+)?Gītā(?:,\s*Chapter\s+[IVXLC\d]+)?[.\s]*', value, re.I):
        return ""
    return value


def build_commentary_blocks(commentary: str, quotes: list[dict], reviewed_quotes: dict[str, dict]) -> list[dict]:
    paragraphs = commentary.split("\n\n")
    operations: dict[int, list[tuple[int, int, str]]] = {}
    placements: dict[int, list[tuple[int, str, dict]]] = {}
    placed_ids = set()
    claimed_translation_ranges: dict[int, list[tuple[int, int]]] = {}

    # First freeze the printed source ranges. They are removed from prose and
    # re-rendered once as compact Sanskrit blocks at paragraph boundaries.
    grouped: dict[tuple[int, int, int], list[dict]] = {}
    for quote in quotes:
        grouped.setdefault((quote["paragraph_index"], quote["source_start"], quote["source_end"]), []).append(quote)
    source_ranges: dict[int, list[tuple[int, int]]] = {}
    normalized_groups = []
    for (paragraph_index, start, end), rows in grouped.items():
        paragraph = paragraphs[paragraph_index]
        if end > 0 and paragraph[end - 1] == "(":
            roman_end = paragraph.find(")", end)
            if roman_end >= 0 and parenthetical_is_romanization(paragraph[end:roman_end], rows):
                end = roman_end + 1
        else:
            roman = re.match(r"\s*[\"'”’]*\s*\(([^)]{2,800})(?:\)|$)", paragraph[end:])
            if roman and parenthetical_is_romanization(roman.group(1), rows):
                end += roman.end()
        normalized_groups.append((paragraph_index, start, end, sorted(rows, key=lambda row: row["id"])))
        source_ranges.setdefault(paragraph_index, []).append((start, end))
        operations.setdefault(paragraph_index, []).append((start, end, ""))

    # Keep Chinmayananda's English in his prose. The matching Sanskrit block is
    # appended after that complete paragraph instead of replacing the English
    # mid-sentence. A mislabelled Roman source duplicate is removed, but its
    # block follows the paragraph by the same rule.
    for quote in sorted(quotes, key=lambda row: row["id"]):
        translation = quote.get("chinmayananda_translation")
        if not translation:
            continue
        reviewed = reviewed_quotes.get(quote["id"], {})
        author_english = reviewed.get("english_source") == "Swami Chinmayananda"
        for paragraph_index, paragraph in enumerate(paragraphs):
            found = lexical_phrase_range(paragraph, translation)
            if not found:
                continue
            if any(found[0] < end and found[1] > start for start, end in claimed_translation_ranges.get(paragraph_index, [])):
                continue
            claimed_translation_ranges.setdefault(paragraph_index, []).append(found)
            basis = "chinmayananda-translation-position" if author_english else "printed-romanization-position"
            placements.setdefault(paragraph_index, []).append((found[0], basis, quote))
            placed_ids.add(quote["id"])
            if not author_english and not any(
                found[0] < end and found[1] > start
                for start, end in source_ranges.get(paragraph_index, [])
            ):
                operations.setdefault(paragraph_index, []).append((found[0], found[1], ""))
            break

    for paragraph_index, start, _end, rows in normalized_groups:
        for quote in rows:
            if quote["id"] not in placed_ids:
                placements.setdefault(paragraph_index, []).append((start, "printed-source-position", quote))

    for paragraph_index, paragraph_operations in operations.items():
        value = paragraphs[paragraph_index]
        for start, end, replacement in sorted(paragraph_operations, reverse=True):
            value = value[:start] + replacement + value[end:]
        paragraphs[paragraph_index] = value

    def quote_block(quote: dict, paragraph_index: int, placement_basis: str) -> dict:
        reviewed = reviewed_quotes.get(quote["id"], {})
        words = reviewed.get("words", [])
        return {
            "type": "gita-quote", "id": quote["id"],
            "content_class": "complete_quote",
            "render_mode": "footnote_quote",
            "source_authority": "independently_verified_primary",
            "citation_completeness": "complete",
            "promotion_eligible": True,
            "literal_translation_source": (
                "chinmayananda" if reviewed.get("english_source") == "Swami Chinmayananda"
                else "site_literal" if reviewed.get("english_source") == "site-literal-translation"
                else "none"
            ),
            "source_paragraph_index": paragraph_index,
            "placement_basis": placement_basis,
            "devanagari": quote["canonical_devanagari"],
            "iast": quote["canonical_iast"],
            "english": reviewed.get("english"),
            "english_slots": reviewed.get("english_slots"),
            "english_source": reviewed.get("english_source"),
            "source_segments": reviewed.get("source_segments"),
            "words": [quote_word_for_reader(word, index) for index, word in enumerate(words)],
            "word_analysis_status": "primary-grammar-reviewed" if words else "withheld-pending-primary-grammar-review",
            "printed_loci": quote["printed_loci"],
            "canonical_locus": quote["canonical_locus"],
            "textual_notes": quote["textual_notes"],
        }

    blocks = []
    for paragraph_index, paragraph in enumerate(paragraphs):
        paragraph = re.sub(
            r"\s*[-—–]*\s*Gītā(?:\s*(?:Ch(?:apter)?\.?))?[\s,.:—–-]*"
            r"(?:XVIII|XVII|XVI|XIV|XIII|XII|XI|XV|VIII|VII|VI|IV|III|II|IX|X|V|I|\d{1,2})"
            r"[\s,.:—–-]*(?:St(?:anza)?\.?)?[\s,.:—–-]*\d{1,2}\.?",
            " ", paragraph, flags=re.I,
        )
        paragraph_placements = placements.get(paragraph_index, [])
        paragraph = normalize_author_translation_quotes(paragraph, paragraph_placements)
        paragraph = re.sub(r"\s*[,;:]\s*[.;]\s*", ". ", paragraph)
        paragraph = re.sub(r"\s+([,.;:!?])", r"\1", paragraph)
        prose = clean_rendered_commentary_prose(paragraph, bool(paragraph_placements))
        prose = re.sub(r"^[.;:]+[\"”’]*\s*", "", prose)
        if paragraph_placements and re.search(r"\b(?:so says|we read|declares|as follows)$", prose, re.I):
            prose += ":"
        if prose.endswith(","):
            prose = prose[:-1].rstrip()
            if not re.search(r'[.!?][\"”]$', prose):
                prose += "."
        if prose and re.search(r"[A-Za-z\u0900-\u097f]", prose):
            block = {"type": "prose", "text": prose, "source_paragraph_index": paragraph_index}
            if block_is_sanskrit_quote(prose):
                quote_iast = block_quote_iast(prose)
                if quote_iast:
                    block["sanskrit_quote_iast"] = quote_iast
            blocks.append(block)
        for position, basis, quote in sorted(paragraph_placements, key=lambda row: (row[0], row[2]["id"])):
            blocks.append(quote_block(quote, paragraph_index, basis))
    return blocks


def classify_rendered_commentary_blocks(blocks: list[dict], in_footnote: bool = False) -> None:
    """Attach canonical rendering metadata to every legacy and generated block."""
    for block in blocks:
        kind = block.get("type")
        if kind == "footnote":
            block.setdefault("content_class", "printed_footnote_prose")
            block.setdefault("render_mode", "footnote_note")
            block.setdefault("source_authority", "chinmayananda_prose")
            block.setdefault("citation_completeness", "derivational")
            block.setdefault("promotion_eligible", False)
            block.setdefault("literal_translation_source", "none")
            classify_rendered_commentary_blocks(block.get("blocks", []), in_footnote=True)
            continue
        if kind in ("gita-quote", "sanskrit-quote"):
            block.setdefault("content_class", "complete_quote")
            block.setdefault("render_mode", "footnote_quote" if in_footnote else "prose")
            block.setdefault(
                "source_authority",
                "independently_verified_primary" if kind == "gita-quote" else "chinmayananda_printed_quote",
            )
            block.setdefault("citation_completeness", "complete")
            block.setdefault("promotion_eligible", True)
            block.setdefault(
                "literal_translation_source",
                "chinmayananda" if block.get("english_source") == "Swami Chinmayananda"
                else "site_literal" if block.get("english_source") == "site-literal-translation"
                else "none",
            )
            continue
        if kind == "prose":
            if block.get("display_devanagari"):
                block.setdefault("content_class", "partial_cited_fragment")
                block.setdefault("render_mode", "display_fragment")
                block.setdefault("source_authority", "site_normalized_fragment")
                block.setdefault("citation_completeness", "fragment")
                block.setdefault("promotion_eligible", False)
                block.setdefault("literal_translation_source", "none")
            else:
                block.setdefault("content_class", "printed_footnote_prose" if in_footnote else "prose_sanskrit_term")
                block.setdefault("render_mode", "footnote_note" if in_footnote else "prose")
                block.setdefault("source_authority", "chinmayananda_prose")
                block.setdefault("citation_completeness", "term_only")
                block.setdefault("promotion_eligible", False)
                block.setdefault("literal_translation_source", "none")


def trim_inline_quotation_punctuation(annotation: dict) -> None:
    """Keep surrounding quotation marks in prose, never inside a Sanskrit token."""
    source = annotation.get("text", "")
    leading = len(source) - len(source.lstrip("‘’'“\""))
    trailing = len(source) - len(source.rstrip("‘’'“\""))
    if not leading and not trailing:
        return
    core_end = len(source) - trailing if trailing else len(source)
    core = source[leading:core_end]
    if not core:
        raise ValueError(f"inline Sanskrit quote trim erased annotation: {annotation.get('id')}")
    annotation["text"] = core
    annotation["start"] += leading
    annotation["end"] -= trailing
    segments = [dict(segment) for segment in annotation.get("source_segments", [])]
    remaining = leading
    for segment in segments:
        if not remaining:
            break
        amount = min(remaining, len(segment.get("text", "")))
        segment["text"] = segment.get("text", "")[amount:]
        remaining -= amount
    remaining = trailing
    for segment in reversed(segments):
        if not remaining:
            break
        amount = min(remaining, len(segment.get("text", "")))
        segment["text"] = segment.get("text", "")[:-amount] if amount else segment.get("text", "")
        remaining -= amount
    if remaining or any(not segment.get("text") for segment in segments):
        raise ValueError(f"inline Sanskrit quote trim cannot preserve source segments: {annotation.get('id')}")
    annotation["source_segments"] = segments


def infer_analysis_mode(word: dict) -> str:
    """State the reviewed analysis route without inventing a verbal root."""
    morphology = " ".join(str(word.get(field, "")) for field in ("morph", "affix", "note")).lower()
    if word.get("root"):
        return "rooted_derivation"
    if word.get("compound") or "compound" in morphology:
        return "compound_analysis"
    if "indeclinable" in morphology or "avyaya" in morphology or "particle" in morphology:
        return "indeclinable"
    if "title" in morphology or "work" in morphology or "proper name" in morphology:
        return "title_or_work_reference"
    if "citation" in morphology or "lexical" in morphology or "nominal" in morphology:
        return "inflected_lexeme"
    return "root_not_asserted"


def enrich_commentary_presentation(blocks: list[dict]) -> None:
    """Attach the reviewed literal layer required by every interactive Sanskrit surface."""
    for block in blocks:
        if block.get("type") == "footnote":
            for word in block.get("formula_payload", {}).get("words", []):
                word.setdefault("analysis_mode", infer_analysis_mode(word))
            enrich_commentary_presentation(block.get("blocks", []))
            continue
        if block.get("content_class") == "prose_sanskrit_term" and block.get("literal_translation_source") == "site_literal":
            block.pop("site_literal", None)
            block["literal_translation_source"] = "none"
        word_sets = [block.get("words", []), block.get("display_words", []), block.get("display_payload", {}).get("words", [])]
        if block.get("formula_payload"):
            word_sets.append(block["formula_payload"].get("words", []))
        for words in word_sets:
            for word in words:
                word.setdefault("analysis_mode", infer_analysis_mode(word))
        for annotation in block.get("inline_sanskrit", []):
            words = annotation.get("words", [])
            for word in words:
                word.setdefault("analysis_mode", infer_analysis_mode(word))
            if len(words) > 1:
                gloss = phrase_gloss_for_unit(annotation.get("unit_key", ""), words)
                if not gloss:
                    raise ValueError(f"multiword inline Sanskrit lacks reviewed phrase gloss: {annotation.get('id')}")
                for segment in annotation.get("source_segments", []):
                    if segment.get("word_indices"):
                        segment.setdefault("group_gloss", gloss)
        if block.get("site_literal"):
            literal = block["site_literal"]
            slots = literal.get("english_slots") or literal.get("englishSlots")
            if slots and not literal.get("text"):
                literal["text"] = slot_plain_text(slots)
        if block.get("render_mode") == "display_fragment":
            words = block.get("display_payload", {}).get("words") or block.get("display_words", [])
            if not words:
                raise ValueError(f"display fragment lacks reviewed words: {block.get('id', block.get('source_paragraph_index'))}")
            literal = block.setdefault("site_literal", {})
            literal.setdefault("english_slots", word_for_word_slots(words))
            literal.setdefault("text", slot_plain_text(literal["english_slots"]))
            literal.setdefault("note", "Word-for-word rendering — site")
            block["literal_translation_source"] = "site_literal"


def assign_presentation_contract(blocks: list[dict], overrides: dict, parent_footnote_id: str | None = None) -> None:
    """Map reviewed evidence roles to the only renderer surfaces the reader permits."""
    fragment_roles = overrides.get("display_fragment_role_overrides", {})
    mixed_roles = overrides.get("mixed_bundle_child_role_overrides", {})
    boundary_repairs = overrides.get("inline_boundary_repairs", {})
    for block in blocks:
        if block.get("type") == "footnote":
            block["evidence_role"] = "derivation_formula" if block.get("formula_payload") else "note_prose"
            block["evidence_shape"] = "formula" if block.get("formula_payload") else "none"
            block["interaction_mode"] = "derivation_block" if block.get("formula_payload") else "prose_note"
            block["translation_surface"] = "visible_literal_line" if block.get("formula_payload") else "none"
            assign_presentation_contract(block.get("blocks", []), overrides, block.get("id"))
            child_roles = {child.get("evidence_role") for child in block.get("blocks", [])}
            if "claim_evidence" in child_roles and len(child_roles - {"claim_evidence"}) > 0:
                block["bundle_contract"] = "typed_children"
            continue
        if block.get("type") in {"gita-quote", "sanskrit-quote"} or block.get("content_class") == "complete_quote":
            block["evidence_role"] = "claim_evidence"
            block["evidence_shape"] = "complete_quote"
            block["interaction_mode"] = "evidence_block"
            block["translation_surface"] = "visible_literal_line"
            continue
        annotations = block.get("inline_sanskrit", [])
        drop_ids = set(boundary_repairs.get("drop", []))
        annotations = [annotation for annotation in annotations if annotation.get("id") not in drop_ids]
        for annotation in annotations:
            clip = boundary_repairs.get("clip", {}).get(annotation.get("id"))
            if not clip:
                continue
            text = clip["text"]
            offset = annotation.get("text", "").find(text)
            if offset < 0:
                raise ValueError(f"inline boundary repair does not replay source: {annotation.get('id')}")
            annotation["text"] = text
            annotation["start"] += offset
            annotation["end"] = annotation["start"] + len(text)
            indices = clip["word_indices"]
            annotation["words"] = [word for word in annotation.get("words", []) if word.get("i") in indices]
            annotation["source_segments"] = [{"text": text, "word_indices": indices}]
        if annotations != block.get("inline_sanskrit", []):
            block["inline_sanskrit"] = annotations
        if block.get("render_mode") == "display_fragment":
            role = fragment_roles.get(parent_footnote_id, "claim_evidence.fragment_quote")
            if role == "note_prose.inline_list" or role == "translation_shadow.shadow":
                for key in (
                    "display_devanagari", "display_words", "display_source_segments", "display_before",
                    "display_after", "display_citation", "display_policy", "display_payload", "site_literal",
                ):
                    block.pop(key, None)
                block["content_class"] = "printed_footnote_prose" if parent_footnote_id else "prose_sanskrit_term"
                block["render_mode"] = "footnote_note" if parent_footnote_id else "prose"
                block["source_authority"] = "chinmayananda_prose"
                block["citation_completeness"] = "term_only"
                block["promotion_eligible"] = False
                block["literal_translation_source"] = "none"
            role_name, shape = role.split(".")
            block["evidence_role"] = role_name
            block["evidence_shape"] = shape
            block["interaction_mode"] = (
                "derivation_block" if role_name == "derivation_formula"
                else "prose_note" if role_name == "translation_shadow"
                else "inline_phrase" if role_name == "note_prose"
                else "evidence_block"
            )
            block["translation_surface"] = (
                "visible_literal_line" if role_name in {"claim_evidence", "derivation_formula"}
                else "source_owned_only" if role_name == "translation_shadow" else "inline_only"
            )
            continue
        role = mixed_roles.get(parent_footnote_id)
        if role:
            role_name, shape = role.split(".")
            block["evidence_role"] = role_name
            block["evidence_shape"] = shape
            block["interaction_mode"] = "prose_note"
            block["translation_surface"] = "source_owned_only" if role_name == "translation_shadow" else "none"
        else:
            block["evidence_role"] = "note_prose" if parent_footnote_id else "inline_mention"
            block["evidence_shape"] = "none"
            block["interaction_mode"] = "inline_phrase" if any(len(row.get("words", [])) > 1 for row in block.get("inline_sanskrit", [])) else "inline_token"
            block["translation_surface"] = "inline_only" if block.get("inline_sanskrit") else "none"


def apply_presentation_overrides(number: int, blocks: list[dict], overrides: dict, parent_footnote_id: str | None = None) -> None:
    """Apply reviewed display corrections from canonical data, never the UI."""
    for block in blocks:
        block.update(overrides.get("block_overrides", {}).get(block.get("id"), {}))
        if block.get("type") == "footnote":
            formula = overrides.get("formula_overrides", {}).get(block.get("id"))
            if formula:
                formula = dict(formula)
                payload_ref = formula.pop("payload_ref", None)
                if payload_ref:
                    payload = overrides.get("display_payload_overrides", {}).get(payload_ref)
                    if not payload:
                        raise ValueError(f"formula override payload is missing: {payload_ref}")
                    formula = {**payload, **formula}
                block["content_class"] = formula["content_class"]
                block["render_mode"] = formula["render_mode"]
                block["literal_translation_source"] = formula["literal_translation_source"]
                block["formula_payload"] = formula
            apply_presentation_overrides(number, block.get("blocks", []), overrides, block.get("id"))
            continue
        block_id = block.get("id")
        word_overrides = overrides["quote_word_overrides"].get(block_id, {})
        for index_text, fields in word_overrides.items():
            index = int(index_text)
            if index >= len(block.get("words", [])):
                raise ValueError(f"presentation override index out of range: {block_id} {index}")
            block["words"][index].update(fields)
        if block_id in overrides["quote_english_slot_overrides"]:
            block["english_slots"] = overrides["quote_english_slot_overrides"][block_id]
            block["english"] = re.sub(r"\{[\d,\s]+:([^}]*)\}", r"\1", block["english_slots"])
        literal_key = block_id or parent_footnote_id or f"name-{number}-paragraph-{block.get('source_paragraph_index')}"
        literal = overrides["site_literal_overrides"].get(literal_key)
        for override in overrides.get("site_literal_block_overrides", {}).get(str(number), []):
            if block.get("text") == override["text"]:
                literal = override["literal"]
        if literal:
            block["site_literal"] = literal
            block["literal_translation_source"] = "site_literal"
        display_payload = overrides.get("display_payload_overrides", {}).get(parent_footnote_id)
        if display_payload and block.get("display_devanagari"):
            block["display_payload"] = display_payload
        group_key = f"{number}:{block.get('source_paragraph_index')}"
        for group in overrides.get("coalesced_inline_overrides", {}).get(group_key, []):
            source_text = group["text"]
            if source_text not in block.get("text", ""):
                continue
            starts = [match.start() for match in re.finditer(re.escape(source_text), block.get("text", ""))]
            if len(starts) != 1:
                raise ValueError(f"coalesced inline override did not resolve uniquely: {group['id']}")
            start = starts[0]
            end = start + len(source_text)
            payload = overrides.get("standalone_payload_overrides", {}).get(group["id"])
            if not payload:
                raise ValueError(f"coalesced inline override lacks reviewed payload: {group['id']}")
            contained = [
                annotation for annotation in block.get("inline_sanskrit", [])
                if start <= annotation.get("start", -1) and annotation.get("end", -1) <= end
            ]
            if not contained:
                raise ValueError(f"coalesced inline override has no source annotations: {group['id']}")
            annotation = {
                "id": group["id"], "unit_key": group["unit_key"], "text": source_text,
                "language": group["language"], "start": start, "end": end,
                "words": payload["words"], "source_segments": payload["source_segments"],
                "presentation_payload": payload,
            }
            block["inline_sanskrit"] = [
                existing for existing in block.get("inline_sanskrit", [])
                if existing not in contained
            ] + [annotation]
            block["inline_sanskrit"].sort(key=lambda row: (row["start"], row["end"], row["id"]))
        for annotation in block.get("inline_sanskrit", []):
            presentation_payload = overrides.get("standalone_payload_overrides", {}).get(annotation.get("id"))
            if presentation_payload:
                annotation["presentation_payload"] = presentation_payload
            item_override = overrides.get("inline_item_overrides", {}).get(annotation.get("id"))
            if item_override:
                annotation.update(item_override)
            for index_text, fields in overrides.get("inline_word_overrides", {}).get(annotation.get("id"), {}).items():
                index = int(index_text)
                if index >= len(annotation.get("words", [])):
                    raise ValueError(f"inline word override index out of range: {annotation.get('id')} {index}")
                annotation["words"][index].update(fields)
            trim_inline_quotation_punctuation(annotation)
        if block.get("type") == "prose":
            block.update(overrides.get("prose_overrides", {}).get(f"{number}:{block.get('source_paragraph_index')}", {}))
            for override in overrides.get("prose_block_overrides", {}).get(str(number), []):
                if block.get("text") == override["text"]:
                    block.update(override["fields"])
    if parent_footnote_id is not None:
        return
    for addition in overrides.get("inline_additions", {}).get(str(number), []):
        candidates = [block for block in blocks if block.get("type") == "prose" and addition["block_contains"] in block.get("text", "")]
        if len(candidates) != 1:
            raise ValueError(f"inline presentation addition did not resolve uniquely: name {number} {addition['id']}")
        block = candidates[0]
        anchor_end = block["text"].index(addition["after"], block["text"].index(addition["block_contains"])) + len(addition["after"])
        start = anchor_end
        end = start + len(addition["token"])
        if block["text"][start:end] != addition["token"]:
            raise ValueError(f"inline presentation addition does not replay source: {addition['id']}")
        annotation = {
            "id": addition["id"], "unit_key": addition["id"], "text": addition["token"],
            "language": addition["language"], "start": start, "end": end,
            "words": addition["words"],
            "source_segments": [{"text": addition["token"], "word_indices": [word["i"] for word in addition["words"]]}],
        }
        if any(row.get("id") == annotation["id"] for row in block.get("inline_sanskrit", [])):
            raise ValueError(f"duplicate inline presentation addition: {annotation['id']}")
        block.setdefault("inline_sanskrit", []).append(annotation)
        block["inline_sanskrit"].sort(key=lambda row: (row["start"], row["end"], row["id"]))


def build(received: str, word_split: str, commentary_path: Path | None, analysis_path: Path | None) -> dict:
    generated_preface = build_performance_preface(received)
    if not PREFACE_WITNESS_PATH.exists():
        raise ValueError(f"performance preface witness is missing: {PREFACE_WITNESS_PATH}")
    preface_witness = json.loads(PREFACE_WITNESS_PATH.read_text(encoding="utf-8"))
    if preface_witness != generated_preface:
        raise ValueError("performance preface witness does not replay the pinned received text")
    preface = attach_preface_commentary(preface_witness, PREFACE_COMMENTARY_PATH)
    preface = attach_preface_analysis(preface, PREFACE_ANALYSIS_PATH)
    postlude = load_postlude_analysis(PREFACE_ANALYSIS_PATH)
    timings = json.loads(TIMINGS_PATH.read_text(encoding="utf-8"))
    stanzas = parse_received_itx(received)
    bori = parse_bori(BORI_PATH)
    boundaries, all_names = parse_word_split(word_split)
    commentary = load_commentary(commentary_path)
    presentation_overrides = json.loads(PRESENTATION_OVERRIDES_PATH.read_text(encoding="utf-8"))
    if presentation_overrides.get("schema_version") != 1:
        raise ValueError("reader presentation overrides have an unsupported schema")
    analyses = load_analysis(analysis_path)
    parallel_derivations = alternatives_by_name()
    quote_registry = json.loads(COMMENTARY_QUOTES_PATH.read_text(encoding="utf-8"))
    reviewed_quotes = load_reviewed_quotes()
    if quote_registry["source_commentary"]["sha256"] != commentary_quote_source_sha256(commentary):
        raise ValueError("commentary quote registry is stale against Chinmayananda's transcription")
    quotes_by_name: dict[int, list[dict]] = {}
    for quote in quote_registry["quotes"]:
        quotes_by_name.setdefault(quote["name_number"], []).append(quote)

    alignment_changes = {}
    for index, stanza in enumerate(stanzas):
        changed = align_name_surfaces(stanza["iast"], boundaries[index]["names"])
        if changed:
            alignment_changes[index] = changed

    by_number = {item["number"]: dict(item) for item in all_names}
    for number, item in by_number.items():
        if number in SURFACE_OVERRIDES:
            item["surface_iast"] = SURFACE_OVERRIDES[number]
        item["deva_surface"] = transliterate(item["surface_iast"], sanscript.IAST, sanscript.DEVANAGARI)
        item["morph"] = "A nominal epithet or nominal expression applied to Viṣṇu in the stanza."
        item["analysis_status"] = "surface-and-citation-form"
        item["cite"] = f"cite://chinmayananda/thousand-ways-to-the-transcendental/name/{number}"
        analysis = analyses.get(number)
        if analysis:
            analysis = dict(analysis)
            analysis["parallel_derivations"] = parallel_derivations.get(number, [])
            item["citation_iast"] = analysis["citation_iast"]
            item["deva"] = analysis["citation_devanagari"]
            item["word_analysis"] = analysis
            item["analysis_status"] = analysis["status"]
        else:
            item["deva"] = item["deva_surface"]
        source = commentary.get(number)
        if source:
            item["citation_iast_ocr"] = source.get("source_heading_roman", source.get("heading_roman", ""))
            if source.get("source_heading_devanagari_ocr"):
                item["deva_ocr"] = source["source_heading_devanagari_ocr"]
            source_definition = source.get("short_meaning") or first_definition(source["commentary"])
            item["meaning"] = source["simple_meaning"]
            item["meaning_status"] = source.get("simple_meaning_status", "derived-direct")
            item["meaning_source"] = source.get("simple_meaning_source")
            if item.get("word_analysis", {}).get("derivation") and comparison_key(item["word_analysis"]["derivation"]) == comparison_key(item["meaning"]):
                item["word_analysis"] = dict(item["word_analysis"])
                item["word_analysis"]["derivation"] = None
            item["chinmayananda"] = {
                "opening_excerpt": source_definition,
                "commentary": source["commentary"],
                "detail": commentary_detail(source["commentary"], source_definition),
                "scan_pages": source["scan_pages"],
                "verification_status": source["verification_status"],
                "ocr_notes": source.get("ocr_notes", []),
                "blocks": promote_inline_blocks(
                    number,
                    promote_non_gita_blocks(
                        number,
                        build_commentary_blocks(
                            source["commentary"], quotes_by_name.get(number, []), reviewed_quotes
                        ),
                    ),
                ),
            }
            derivation = traditional_derivation(source["commentary"])
            if derivation and comparison_key(derivation) != comparison_key(item["meaning"]):
                item["traditional_derivation"] = derivation
                item["analysis_status"] = "chinmayananda-derivation-present"

    apply_footnote_apparatus(by_number, merged_footnotes())
    for item in by_number.values():
        classify_rendered_commentary_blocks(item.get("chinmayananda", {}).get("blocks", []))
        apply_presentation_overrides(item["number"], item.get("chinmayananda", {}).get("blocks", []), presentation_overrides)
        enrich_commentary_presentation(item.get("chinmayananda", {}).get("blocks", []))
        assign_presentation_contract(item.get("chinmayananda", {}).get("blocks", []), presentation_overrides)

    for index, stanza in enumerate(stanzas):
        stanza["critical_edition"] = bori[index]
        stanza["critical_text_differs"] = comparison_key(stanza["iast"]) != comparison_key(bori[index]["iast"])
        boundary_rows = boundaries[index]["names"]
        numbers = [name["number"] for name in boundary_rows]
        stanza["name_numbers"] = numbers
        if index in alignment_changes:
            stanza["boundary_alignment_changes"] = alignment_changes[index]
        stanza["names"] = [by_number[number] for number in numbers]
        stanza["cite"] = f"cite://vyasa/vishnu-sahasranama/stanza/{index + 1}"

    return {
        "schema_version": 1,
        "title": "Viṣṇu Sahasranāma",
        "subtitle": "The thousand names, with Swami Chinmayananda's traditional Advaita commentary",
        "attribution": {
            "root_text": "Mahābhārata, Anuśāsanaparvan",
            "commentary": "Swami Chinmayananda, Thousand Ways to the Transcendental",
            "commentary_thinker_id": "chinmayananda",
            "permission_notice": "Published with permission as stated by the site owner.",
        },
        "sources": {
            "received_text": {"url": RECEIVED_URL, "sha256": RECEIVED_SHA256},
            "critical_edition": {
                "path": str(BORI_PATH.relative_to(ROOT)),
                "locus": "Mahābhārata 13.135.14–120",
            },
            "name_boundary_aid": {"url": WORD_SPLIT_URL, "sha256": WORD_SPLIT_SHA256},
            "commentary": {
                "path": str(commentary_path.relative_to(ROOT)),
                "sha256": sha256(commentary_path.read_bytes()),
            } if commentary_path and commentary_path.exists() else None,
            "sanskrit_analysis": {
                "path": str(analysis_path.relative_to(ROOT)),
                "sha256": sha256(analysis_path.read_bytes()),
            } if analysis_path and analysis_path.exists() else None,
            "commentary_quotes": {
                "path": str(COMMENTARY_QUOTES_PATH.relative_to(ROOT)),
                "sha256": sha256(COMMENTARY_QUOTES_PATH.read_bytes()),
            },
            "commentary_quote_primary_review": {
                "path": str(COMMENTARY_QUOTE_ANALYSIS_PATH.relative_to(ROOT)),
                "sha256": sha256(COMMENTARY_QUOTE_ANALYSIS_PATH.read_bytes()),
            },
            "performance_preface": {
                "path": str(PREFACE_WITNESS_PATH.relative_to(ROOT)),
                "sha256": sha256(PREFACE_WITNESS_PATH.read_bytes()),
            },
            "preface_commentary": {
                "path": str(PREFACE_COMMENTARY_PATH.relative_to(ROOT)),
                "sha256": sha256(PREFACE_COMMENTARY_PATH.read_bytes()),
            },
            "preface_analysis": {
                "path": str(PREFACE_ANALYSIS_PATH.relative_to(ROOT)),
                "sha256": sha256(PREFACE_ANALYSIS_PATH.read_bytes()),
            },
            "audio_timings": {
                "path": str(TIMINGS_PATH.relative_to(ROOT)),
                "sha256": sha256(TIMINGS_PATH.read_bytes()),
            },
        },
        "audio": {
            "src": "https://github.com/Balbudhi/vedanta-timeline/releases/download/media-v1/vishnu-sahasranama-sanjeev-abhyankar.m4a?download=1",
            "performer": "Sanjeev Abhyankar",
            "album": "Vishnu Sahastranaam",
            "duration_seconds": 1636.031565,
            "codec": "AAC-LC",
            "sample_rate_hz": 44100,
            "channels": 2,
            "bit_rate_bps": 262312,
            "file_size_bytes": 53943037,
            "sha256": "9e3b185314c009376eb1b6b07936b1077bc665a29f9bbdba52491b92a8c5f342",
            "delivery": "Original purchased M4A stream; no lossy re-encode; GitHub release asset media-v1.",
            "timing_status": timings["timing_status"],
            "units": timings["units"],
            "alignment": timings["alignment"],
        },
        "preface": preface,
        "stanzas": stanzas,
        "postlude": postlude,
    }


INLINE_IAST_TOKEN_RE = re.compile(r"(?<![A-Za-zĀ-ỹÑñ])(?:√)?[A-Za-zĀ-ỹÑñ'’\-]+")
INLINE_IAST_MARK_RE = re.compile(r"[āīūṛṝḷṅñṭḍṇśṣṃṁḥ]|^√")
PROSE_FORMAT_DAMAGE_RE = re.compile(
    r'["“]\s*["”](?=\s*(?:[—–),.;:]|$))|\(\s*\)|["“]\s*\d+\s*["”]|,\s*$|\bIn\s+Gītā\.\s*\(\s*Ch\.'
)


def unannotated_sanskrit(text: str, annotations: list[dict]) -> bool:
    remaining = list(text)
    for annotation in annotations:
        start, end = int(annotation["start"]), int(annotation["end"])
        if text[start:end] != annotation.get("text"):
            return True
        for index in range(start, end):
            remaining[index] = " "
    value = "".join(remaining)
    if re.search(r"[\u0900-\u097f]", value):
        return True
    return any(INLINE_IAST_MARK_RE.search(match.group()) for match in INLINE_IAST_TOKEN_RE.finditer(value))


def walk_commentary_blocks(blocks: list[dict]):
    """Yield top-level commentary blocks and the contents of attached notes."""
    for block in blocks:
        yield block
        if block.get("type") == "footnote":
            yield from walk_commentary_blocks(block.get("blocks", []))


def validate(data: dict, require_commentary: bool, require_reviewed_analysis: bool = True) -> dict:
    errors = []
    commentary_source = {}
    if require_commentary and COMMENTARY_PATH.exists():
        source_rows = json.loads(COMMENTARY_PATH.read_text(encoding="utf-8")).get("names", [])
        commentary_source = {row.get("number"): row for row in source_rows}
    preface = data.get("preface", {})
    preface_groups = preface.get("groups", [])
    expected_preface_counts = {"invocation": 6, "dialogue": 16, "assignment": 15, "meditation": 8}
    if [group.get("id") for group in preface_groups] != list(expected_preface_counts):
        errors.append("performance preface groups are missing or out of recording order")
    if {group.get("id"): len(group.get("units", [])) for group in preface_groups} != expected_preface_counts:
        errors.append("performance preface must contain the exact 6/16/15/8-unit recording sequence")
    preface_ids = [unit.get("id") for group in preface_groups for unit in group.get("units", [])]
    if len(preface_ids) != len(set(preface_ids)):
        errors.append("performance preface has duplicate unit ids")
    for group in preface_groups:
        for unit in group.get("units", []):
            if not unit.get("devanagari") or not unit.get("iast"):
                errors.append(f"performance preface unit {unit.get('id')} lacks source text")
            words = unit.get("words", [])
            if not words or [word.get("i") for word in words] != list(range(len(words))):
                errors.append(f"performance preface unit {unit.get('id')} lacks contiguous word analysis")
            slots = {int(index) for group_text in re.findall(r"\{([\d,\s]+):", unit.get("english", "")) for index in group_text.split(",")}
            if slots != set(range(len(words))):
                errors.append(f"performance preface unit {unit.get('id')} lacks complete English slot coverage")
    stanzas = data.get("stanzas", [])
    postlude = data.get("postlude", [])
    if [unit.get("id") for unit in postlude] != ["closing-name", "protection"]:
        errors.append("recorded postlude is not exactly closing-name + protection")
    for unit in postlude:
        words = unit.get("words", [])
        if not words or [word.get("i") for word in words] != list(range(len(words))):
            errors.append(f"postlude unit {unit.get('id')} lacks contiguous word analysis")
        slots = {int(index) for group_text in re.findall(r"\{([\d,\s]+):", unit.get("english", "")) for index in group_text.split(",")}
        if slots != set(range(len(words))):
            errors.append(f"postlude unit {unit.get('id')} lacks complete English slot coverage")
    expected_timing_ids = ([unit.get("id") for group in preface_groups for unit in group.get("units", [])]
                           + [f"stanza-{stanza.get('number')}" for stanza in stanzas]
                           + [unit.get("id") for unit in postlude])
    timed_units = data.get("audio", {}).get("units", [])
    if [unit.get("id") for unit in timed_units] != expected_timing_ids:
        errors.append("audio timing manifest does not exactly cover displayed units")
    previous_end = 0
    for unit in timed_units:
        start, end = unit.get("start"), unit.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or start < previous_end - 0.001 or end <= start:
            errors.append(f"invalid or overlapping audio timing for {unit.get('id')}")
        previous_end = end
    names = [name for stanza in stanzas for name in stanza.get("names", [])]
    quote_blocks = []
    non_gita_quote_blocks = []
    normalized_display_quotes = []
    parallel_derivation_ids = []
    names_with_parallel_derivations = set()
    inline_sanskrit_occurrences = 0
    ascii_inline_ids = []
    footnote_blocks = []
    footnote_call_ids = []
    if len(stanzas) != 107:
        errors.append(f"expected 107 stanzas, found {len(stanzas)}")
    if [item.get("number") for item in names] != list(range(1, 1001)):
        errors.append("name population is not exactly contiguous 1–1000")
    for stanza in stanzas:
        if not stanza.get("devanagari") or not stanza.get("iast"):
            errors.append(f"stanza {stanza.get('number')} lacks source text")
        if len(stanza.get("critical_edition", {}).get("loci", [])) != 2:
            errors.append(f"stanza {stanza.get('number')} lacks BORI loci")
    for item in names:
        number = item.get("number")
        for call in item.get("root_footnote_calls", []):
            if call.get("id"):
                footnote_call_ids.append(call["id"])
        if not item.get("citation_iast") or not item.get("deva") or not item.get("deva_surface"):
            errors.append(f"name {number} lacks citation forms")
        if require_commentary:
            source = item.get("chinmayananda")
            source_row = commentary_source.get(number, {})
            if not item.get("meaning") or not source or not source.get("opening_excerpt") or not source.get("commentary"):
                errors.append(f"name {number} lacks Chinmayananda English")
            meaning = item.get("meaning")
            if not isinstance(meaning, str) or not 3 <= len(meaning) <= 260 or "\n" in meaning:
                errors.append(f"name {number} has an invalid Simplified summary length/shape")
                meaning = meaning or ""
            if re.search(r"[*†‡\u0900-\u0dff]", meaning):
                errors.append(f"name {number} Simplified summary contains a footnote marker or source script")
            if meaning != source_row.get("simple_meaning"):
                errors.append(f"name {number} Simplified summary differs from the reviewed editorial corpus")
            if item.get("meaning_status") != source_row.get("simple_meaning_status"):
                errors.append(f"name {number} Simple status differs from the reviewed source corpus")
            if source.get("commentary") != source_row.get("commentary"):
                errors.append(f"name {number} Full commentary does not exactly replay Chinmayananda's transcription")
            analysis = item.get("word_analysis")
            if not analysis:
                errors.append(f"name {number} lacks structured word analysis")
            else:
                required = ("citation_iast", "citation_devanagari", "whole_gloss", "parts", "stem", "affix", "morph", "sandhi", "grammar", "source_basis", "status", "uncertainty")
                missing = [field for field in required if field not in analysis or analysis[field] in ("", None)]
                if missing:
                    errors.append(f"name {number} word analysis lacks {', '.join(missing)}")
                for nullable_field in ("root", "compound", "derivation"):
                    if nullable_field not in analysis:
                        errors.append(f"name {number} word analysis omits {nullable_field}")
                if not analysis.get("citation_iast") or not re.search(r"[\u0900-\u097f]", analysis.get("citation_devanagari", "")):
                    errors.append(f"name {number} lacks validated citation forms")
                parts = analysis.get("parts", [])
                if not isinstance(parts, list) or not parts or any(not all(part.get(field) for field in ("form_iast", "gloss", "kind")) for part in parts):
                    errors.append(f"name {number} has incomplete word-analysis structure")
                root = analysis.get("root")
                if root is not None and not all(root.get(field) for field in ("form", "gana", "pada", "gloss")):
                    errors.append(f"name {number} has an incomplete verbal-root record")
                compound = analysis.get("compound")
                if compound is not None and (not all(compound.get(field) for field in ("type", "vigraha", "members")) or not isinstance(compound.get("members"), list)):
                    errors.append(f"name {number} has an incomplete compound analysis")
                derivation = analysis.get("derivation")
                if derivation and comparison_key(derivation) == comparison_key(meaning):
                    errors.append(f"name {number} derivation merely repeats its English meaning")
                parallel = analysis.get("parallel_derivations", [])
                if parallel:
                    names_with_parallel_derivations.add(number)
                for alternative in parallel:
                    parallel_derivation_ids.append(alternative.get("id"))
                    for field in (
                        "id", "label", "kind", "meaning", "parts", "formation",
                        "morphology", "qualification", "evidence",
                    ):
                        if alternative.get(field) in (None, "", [], {}):
                            errors.append(f"name {number} parallel derivation lacks {field}")
                    if alternative.get("kind") not in {"grammatical", "traditional-nirvacana"}:
                        errors.append(f"name {number} parallel derivation has invalid kind")
            if source and not source.get("scan_pages"):
                errors.append(f"name {number} lacks scan-page provenance")
            if source and "detail" not in source:
                errors.append(f"name {number} lacks the non-duplicative commentary detail field")
            blocks = source.get("blocks", []) if source else []
            if source and not blocks:
                errors.append(f"name {number} lacks structured commentary blocks")
            if number == 887 and any(block.get("text") == "worldly and heavenly." for block in blocks):
                errors.append("name 887 retains the reviewed detached p.227 sentence fragment")
            all_blocks = list(walk_commentary_blocks(blocks))
            for block in all_blocks:
                for call in block.get("footnote_calls", []):
                    if call.get("id"):
                        footnote_call_ids.append(call["id"])
                if block.get("type") == "footnote":
                    footnote_blocks.append(block)
                    if not block.get("id") or not block.get("marker") or not block.get("blocks"):
                        errors.append(f"name {number} has an incomplete footnote block")
                    continue
                if block.get("type") == "prose":
                    annotations = block.get("inline_sanskrit", [])
                    inline_sanskrit_occurrences += len(annotations)
                    ascii_inline_ids.extend(
                        annotation.get("id") for annotation in annotations
                        if annotation.get("id") in ASCII_ACCEPTED_IDS
                    )
                    if not block.get("display_devanagari") and unannotated_sanskrit(block.get("text", ""), annotations):
                        errors.append(f"name {number} prose retains unannotated Sanskrit")
                    if not block.get("footnote_calls") and PROSE_FORMAT_DAMAGE_RE.search(block.get("text", "")):
                        errors.append(f"name {number} prose retains an empty quotation/citation shell")
                    if block.get("text", "").count("(") != block.get("text", "").count(")"):
                        errors.append(f"name {number} prose retains unmatched parentheses")
                    if block.get("display_devanagari"):
                        normalized_display_quotes.append((number, block))
                        display_words = block.get("display_words", [])
                        display_segments = block.get("display_source_segments", [])
                        if block.get("content_class") != "partial_cited_fragment":
                            errors.append(f"name {number} normalized display lacks partial-fragment classification")
                        if block.get("render_mode") != "display_fragment":
                            errors.append(f"name {number} normalized display lacks display-fragment render mode")
                        if block.get("promotion_eligible") is not False:
                            errors.append(f"name {number} normalized fragment may be promoted as a quote")
                        if block.get("display_policy") != "normalized-devanagari-from-reviewed-word-records":
                            errors.append(f"name {number} normalized quotation lacks its display policy")
                        if re.search(r"[A-Za-z]", block.get("display_devanagari", "")):
                            errors.append(f"name {number} normalized quotation retains Roman text")
                        if [word.get("i") for word in display_words] != list(range(len(display_words))):
                            errors.append(f"name {number} normalized quotation has non-contiguous word analysis")
                        if "".join(segment.get("text", "") for segment in display_segments) != block.get("display_devanagari"):
                            errors.append(f"name {number} normalized quotation segments change Devanāgarī")
                        display_indices = {
                            int(index)
                            for segment in display_segments
                            for index in segment.get("word_indices", [])
                        }
                        if display_indices != set(range(len(display_words))):
                            errors.append(f"name {number} normalized quotation does not map every displayed word")
                    for annotation in annotations:
                        words = annotation.get("words", [])
                        word_indices = [word.get("i") for word in words]
                        if not words or any(index is None for index in word_indices) or len(word_indices) != len(set(word_indices)):
                            errors.append(f"name {number} inline Sanskrit {annotation.get('id')} lacks uniquely indexed word analysis")
                        source_segments = annotation.get("source_segments", [])
                        if "".join(segment.get("text", "") for segment in source_segments) != annotation.get("text"):
                            errors.append(f"name {number} inline Sanskrit {annotation.get('id')} source segments change the source text")
                        source_indices = {
                            int(index)
                            for segment in source_segments
                            for index in segment.get("word_indices", [])
                        }
                        if source_indices != set(word_indices):
                            errors.append(f"name {number} inline Sanskrit {annotation.get('id')} source segments do not cover every word")
                if block.get("type") in ("gita-quote", "sanskrit-quote"):
                    if block.get("type") == "gita-quote":
                        quote_blocks.append(block)
                    else:
                        non_gita_quote_blocks.append(block)
                    words = block.get("words", [])
                    if block.get("content_class") != "complete_quote":
                        errors.append(f"name {number} quote {block.get('id')} lacks complete-quote classification")
                    if block.get("citation_completeness") != "complete" or block.get("promotion_eligible") is not True:
                        errors.append(f"name {number} quote {block.get('id')} has invalid promotion metadata")
                    if not block.get("devanagari") or not block.get("iast") or (require_reviewed_analysis and not words):
                        errors.append(f"name {number} quote {block.get('id')} lacks its three-script source structure")
                    if words and [word.get("i") for word in words] != list(range(len(words))):
                        errors.append(f"name {number} quote {block.get('id')} has non-contiguous word indices")
                    english = block.get("english")
                    slots = block.get("english_slots")
                    if english:
                        if block.get("english_source") not in ("Swami Chinmayananda", "site-literal-translation"):
                            errors.append(f"name {number} quote {block.get('id')} lacks translation provenance")
                        if block.get("display_english") and block.get("english_source") != "Swami Chinmayananda":
                            errors.append(f"name {number} quote {block.get('id')} exposes non-author English")
                        allowed_placements = {
                            "chinmayananda-translation-position",
                            "printed-romanization-position",
                            "printed-source-position",
                        }
                        if block.get("type") == "gita-quote" and block.get("placement_basis") not in allowed_placements:
                            errors.append(f"name {number} quote {block.get('id')} lacks a valid placement basis")
                        if (
                            block.get("type") == "gita-quote"
                            and block.get("english_source") == "Swami Chinmayananda"
                            and not block.get("display_english")
                            and block.get("placement_basis") != "chinmayananda-translation-position"
                        ):
                            errors.append(f"name {number} quote {block.get('id')} is not placed at Chinmayananda's English")
                        if not slots:
                            errors.append(f"name {number} quote {block.get('id')} lacks interactive English")
                        else:
                            replay = re.sub(r"\{[\d,\s]+:([^}]*)\}", r"\1", slots)
                            if replay != english:
                                errors.append(f"name {number} quote {block.get('id')} changes its reviewed English")
                            slot_indices = {
                                int(value)
                                for group in re.findall(r"\{([\d,\s]+):", slots)
                                for value in group.split(",") if value.strip()
                            }
                            if slot_indices - set(range(len(words))):
                                errors.append(f"name {number} quote {block.get('id')} has an invalid English word link")
                            free_english = re.sub(r"\{[\d,\s]+:[^}]*\}", "", slots)
                            if re.search(r"[A-Za-zÀ-ž]", free_english):
                                errors.append(f"name {number} quote {block.get('id')} has non-interactive English wording")
                    source_segments = block.get("source_segments")
                    if not source_segments:
                        errors.append(f"name {number} quote {block.get('id')} lacks interactive source-script segments")
                    elif "".join(segment.get("text", "") for segment in source_segments) != block.get("devanagari"):
                        errors.append(f"name {number} quote {block.get('id')} source segments change Devanāgarī")
                    else:
                        source_indices = {
                            int(index)
                            for segment in source_segments
                            for index in segment.get("word_indices", [])
                        }
                        if source_indices != set(range(len(words))):
                            errors.append(f"name {number} quote {block.get('id')} source segments do not cover every word")
            visible_prose_key = english_source_key(" ".join(
                block.get("text", "") for block in all_blocks if block.get("type") == "prose"
            ))
            for block in all_blocks:
                if (
                    block.get("type") in ("gita-quote", "sanskrit-quote")
                    and block.get("english_source") == "Swami Chinmayananda"
                    and not block.get("display_english")
                    and english_source_key(block.get("english", "")) not in visible_prose_key
                ):
                    errors.append(f"name {number} quote {block.get('id')} drops Chinmayananda's English from prose")
            detail = source.get("detail", "") if source else ""
            opening_excerpt = source.get("opening_excerpt", "") if source else ""
            if opening_excerpt and detail and re.match(
                rf"^{re.escape(opening_excerpt.strip())}(?:\s|[.,;:])", detail.lstrip()
            ):
                errors.append(f"name {number} detailed commentary repeats the opening excerpt")
    serialized = json.dumps(data, ensure_ascii=False)
    for fragment in FORBIDDEN_OCR_FRAGMENTS:
        if fragment.lower() in serialized.lower():
            errors.append(f"forbidden OCR artifact remains: {fragment}")
    if errors:
        raise ValueError("\n".join(errors[:80]))
    quote_ids = [block.get("id") for block in quote_blocks]
    if require_commentary and (len(quote_ids) != 142 or len(quote_ids) != len(set(quote_ids))):
        raise ValueError(f"structured Gītā quotation population is not exactly 142 unique blocks: {len(quote_ids)}")
    non_gita_ids = [block.get("id") for block in non_gita_quote_blocks]
    if require_commentary and (len(non_gita_ids) != 59 or len(non_gita_ids) != len(set(non_gita_ids))):
        raise ValueError(f"structured non-Gītā quotation population is not exactly 59 unique blocks: {len(non_gita_ids)}")
    # Eight reviewed former display fragments are deliberately demoted to
    # inline lists or translation shadows by the presentation contract.
    if require_commentary and len(normalized_display_quotes) != 91:
        raise ValueError(
            "normalized standalone Sanskrit evidence population is not exactly 91: "
            f"{len(normalized_display_quotes)}"
        )
    if require_commentary and (
        len(parallel_derivation_ids) != 92
        or len(set(parallel_derivation_ids)) != 92
        or len(names_with_parallel_derivations) != 81
    ):
        raise ValueError(
            "parallel derivation population differs: "
            f"records={len(parallel_derivation_ids)} unique={len(set(parallel_derivation_ids))} "
            f"names={len(names_with_parallel_derivations)}"
        )
    footnote_ids = [block.get("id") for block in footnote_blocks]
    if require_commentary and (
        len(footnote_ids) != 328
        or len(set(footnote_ids)) != 328
        or sorted(footnote_ids) != sorted(footnote_call_ids)
    ):
        raise ValueError(
            "printed footnote apparatus differs: "
            f"notes={len(footnote_ids)} unique={len(set(footnote_ids))} "
            f"calls={len(footnote_call_ids)} unique_calls={len(set(footnote_call_ids))}"
        )
    expected_ascii_inline = (
        ASCII_ACCEPTED_IDS - ASCII_STRUCTURED_IDS - FOOTNOTE_OVERRIDE_REPLACED_ASCII_IDS
    )
    if require_commentary:
        if len(ascii_inline_ids) != len(set(ascii_inline_ids)):
            raise ValueError("reviewed ASCII Sanskrit occurrence ids are duplicated in rendered prose")
        if set(ascii_inline_ids) != expected_ascii_inline:
            missing_ascii = sorted(expected_ascii_inline - set(ascii_inline_ids))
            extra_ascii = sorted(set(ascii_inline_ids) - expected_ascii_inline)
            raise ValueError(
                "reviewed ASCII Sanskrit render population differs: "
                f"missing={len(missing_ascii)} {missing_ascii[:10]}, "
                f"extra={len(extra_ascii)} {extra_ascii[:10]}"
            )
    return {
        "preface_units": sum(len(group.get("units", [])) for group in preface_groups),
        "postlude_units": len(postlude),
        "stanzas": len(stanzas),
        "names": len(names),
        "with_commentary": sum("chinmayananda" in item for item in names),
        "with_traditional_derivation": sum("traditional_derivation" in item for item in names),
        "critical_text_differences": sum(bool(stanza.get("critical_text_differs")) for stanza in stanzas),
        "structured_gita_quotes": len(quote_blocks),
        "structured_non_gita_quotes": len(non_gita_quote_blocks),
        "normalized_standalone_sanskrit_quotes": len(normalized_display_quotes),
        "public_parallel_derivations": len(parallel_derivation_ids),
        "names_with_parallel_derivations": len(names_with_parallel_derivations),
        "printed_footnotes": len(footnote_ids),
        "printed_footnote_calls": len(footnote_call_ids),
        "interactive_inline_sanskrit_occurrences": inline_sanskrit_occurrences,
        "reviewed_ascii_sanskrit_occurrences": len(ASCII_ACCEPTED_IDS),
        "interactive_ascii_sanskrit_in_prose": len(ascii_inline_ids),
        "ascii_sanskrit_represented_by_structured_blocks": len(ASCII_STRUCTURED_IDS),
        "interactive_gita_translations": sum(bool(block.get("english_slots")) for block in quote_blocks),
        "chinmayananda_gita_translations": sum(block.get("english_source") == "Swami Chinmayananda" for block in quote_blocks),
        "site_literal_gita_translations": sum(block.get("english_source") == "site-literal-translation" for block in quote_blocks),
        "full_commentary_replay": sum(
            item.get("chinmayananda", {}).get("commentary") == commentary_source.get(item.get("number"), {}).get("commentary")
            for item in names
        ) if require_commentary else None,
    }


def write_web_payloads(data: dict, core_path: Path, details_path: Path) -> dict:
    """Split the validated corpus into fast initial and lazy detail payloads."""
    core = json.loads(json.dumps(data, ensure_ascii=False))
    details = []
    for stanza in core["stanzas"]:
        for name in stanza["names"]:
            record = {"number": name["number"]}
            for field in WEB_DETAIL_FIELDS:
                if field in name:
                    record[field] = name.pop(field)
            details.append(record)
    if [record["number"] for record in details] != list(range(1, 1001)):
        raise ValueError("web detail payload is not exactly contiguous names 1–1000")
    validate(core, require_commentary=False)
    detail_payload = {"schema_version": 1, "names": details}
    core_path.parent.mkdir(parents=True, exist_ok=True)
    details_path.parent.mkdir(parents=True, exist_ok=True)
    core_path.write_text(json.dumps(core, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    details_path.write_text(json.dumps(detail_payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    return {
        "web_core_bytes": core_path.stat().st_size,
        "web_details_bytes": details_path.stat().st_size,
    }


def update_citation_index(data: dict, path: Path) -> int:
    index = json.loads(path.read_text(encoding="utf-8"))
    entries = index.setdefault("entries", {})
    prefixes = (
        "vyasa/vishnu-sahasranama/",
        "chinmayananda/thousand-ways-to-the-transcendental/",
    )
    for key in [key for key in entries if key.startswith(prefixes)]:
        del entries[key]
    for stanza in data["stanzas"]:
        n = stanza["number"]
        entries[f"vyasa/vishnu-sahasranama/stanza/{n}"] = {
            "thinker_id": "vyasa",
            "work_id": "vishnu-sahasranama",
            "locus": f"Mahābhārata, Anuśāsanaparvan, Viṣṇusahasranāma stanza {n}",
            "locus_short": f"VSN {n}",
            "sanskrit_iast": stanza["iast"],
            "source": f"gita/vishnu-sahasranama/reader.json#stanzas[{n - 1}]",
            "witness": "data/sources/sanskrit/vedanta/vishnu_sahasranama_bori_critical_excerpt.txt#"
                + ",".join(stanza["critical_edition"]["loci"]),
            "verified": True,
        }
        for name in stanza["names"]:
            number = name["number"]
            entries[f"chinmayananda/thousand-ways-to-the-transcendental/name/{number}"] = {
                "thinker_id": "chinmayananda",
                "work_id": "thousand-ways-to-the-transcendental",
                "locus": f"Viṣṇusahasranāma name {number}; scan page(s) "
                    + ", ".join(str(page) for page in name["chinmayananda"]["scan_pages"]),
                "locus_short": f"VSN name {number}",
                "sanskrit_iast": name["surface_iast"],
                "english_close": name.get("meaning"),
                "source": f"gita/vishnu-sahasranama/chinmayananda.json#names[{number - 1}]",
                "verified": "scan-checked"
                    if name["chinmayananda"]["verification_status"] == "scan-checked"
                    else "working-witness",
            }
    index["entries"] = entries
    path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return sum(key.startswith(prefixes) for key in entries)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--received-source", type=Path)
    parser.add_argument("--word-split-source", type=Path)
    parser.add_argument("--commentary", type=Path, default=COMMENTARY_PATH)
    parser.add_argument("--analysis", type=Path, default=ANALYSIS_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--web-core-output", type=Path, default=WEB_CORE_PATH)
    parser.add_argument("--web-details-output", type=Path, default=WEB_DETAILS_PATH)
    parser.add_argument("--split-only", type=Path)
    parser.add_argument("--enrich-presentation", type=Path)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--require-commentary", action="store_true")
    parser.add_argument(
        "--allow-provisional-analysis",
        action="store_true",
        help="development audit only; never use output for deployment",
    )
    parser.add_argument("--update-citation-index", type=Path)
    parser.add_argument("--write-preface-witness", action="store_true")
    args = parser.parse_args()

    if args.write_preface_witness:
        received = load_pinned(args.received_source, RECEIVED_URL, RECEIVED_SHA256)
        preface = build_performance_preface(received)
        PREFACE_WITNESS_PATH.parent.mkdir(parents=True, exist_ok=True)
        PREFACE_WITNESS_PATH.write_text(json.dumps(preface, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"preface_units": sum(len(group["units"]) for group in preface["groups"]), "output": str(PREFACE_WITNESS_PATH)}, ensure_ascii=False, indent=2))
        return

    if args.split_only:
        data = json.loads(args.split_only.read_text(encoding="utf-8"))
        report = validate(data, require_commentary=True, require_reviewed_analysis=False)
        report.update(write_web_payloads(data, args.web_core_output, args.web_details_output))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    if args.enrich_presentation:
        data = json.loads(args.enrich_presentation.read_text(encoding="utf-8"))
        presentation_overrides = json.loads(PRESENTATION_OVERRIDES_PATH.read_text(encoding="utf-8"))
        for stanza in data["stanzas"]:
            for name in stanza["names"]:
                enrich_commentary_presentation(name.get("chinmayananda", {}).get("blocks", []))
                assign_presentation_contract(name.get("chinmayananda", {}).get("blocks", []), presentation_overrides)
        report = validate(data, require_commentary=True, require_reviewed_analysis=False)
        args.enrich_presentation.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report.update(write_web_payloads(data, args.web_core_output, args.web_details_output))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    if args.check:
        report = validate(json.loads(args.check.read_text(encoding="utf-8")), args.require_commentary)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    if not args.allow_provisional_analysis:
        assert_public_analysis_gate(args.analysis)

    received = load_pinned(args.received_source, RECEIVED_URL, RECEIVED_SHA256)
    word_split = load_pinned(args.word_split_source, WORD_SPLIT_URL, WORD_SPLIT_SHA256)
    data = build(received, word_split, args.commentary, args.analysis)
    report = validate(data, args.require_commentary, require_reviewed_analysis=not args.allow_provisional_analysis)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report.update(write_web_payloads(data, args.web_core_output, args.web_details_output))
    if args.update_citation_index:
        report["citation_entries"] = update_citation_index(data, args.update_citation_index)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
