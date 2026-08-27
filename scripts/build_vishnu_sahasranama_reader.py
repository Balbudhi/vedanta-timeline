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


ROOT = Path(__file__).resolve().parents[1]
BORI_PATH = ROOT / "data/sources/sanskrit/vedanta/vishnu_sahasranama_bori_critical_excerpt.txt"
COMMENTARY_PATH = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
ANALYSIS_PATH = ROOT / "gita/vishnu-sahasranama/analysis.json"
PREFACE_COMMENTARY_PATH = ROOT / "gita/vishnu-sahasranama/preface-commentary.json"
PREFACE_WITNESS_PATH = ROOT / "data/sources/sanskrit/vedanta/vishnu_sahasranama_performance_preface.json"
OUTPUT_PATH = ROOT / "gita/vishnu-sahasranama/reader.json"
WEB_CORE_PATH = ROOT / "gita/vishnu-sahasranama/reader-core.json"
WEB_DETAILS_PATH = ROOT / "gita/vishnu-sahasranama/reader-details.json"
WEB_DETAIL_FIELDS = ("word_analysis", "chinmayananda", "traditional_derivation")

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


def build(received: str, word_split: str, commentary_path: Path | None, analysis_path: Path | None) -> dict:
    generated_preface = build_performance_preface(received)
    if not PREFACE_WITNESS_PATH.exists():
        raise ValueError(f"performance preface witness is missing: {PREFACE_WITNESS_PATH}")
    preface_witness = json.loads(PREFACE_WITNESS_PATH.read_text(encoding="utf-8"))
    if preface_witness != generated_preface:
        raise ValueError("performance preface witness does not replay the pinned received text")
    preface = attach_preface_commentary(preface_witness, PREFACE_COMMENTARY_PATH)
    stanzas = parse_received_itx(received)
    bori = parse_bori(BORI_PATH)
    boundaries, all_names = parse_word_split(word_split)
    commentary = load_commentary(commentary_path)
    analyses = load_analysis(analysis_path)

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
            item["meaning"] = source.get("short_meaning") or first_definition(source["commentary"])
            item["meaning_status"] = source.get("short_meaning_status", "derived-opening")
            item["chinmayananda"] = {
                "commentary": source["commentary"],
                "detail": commentary_detail(source["commentary"], item["meaning"]),
                "scan_pages": source["scan_pages"],
                "verification_status": source["verification_status"],
                "ocr_notes": source.get("ocr_notes", []),
            }
            derivation = traditional_derivation(source["commentary"])
            if derivation:
                item["traditional_derivation"] = derivation
                item["analysis_status"] = "chinmayananda-derivation-present"

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
            "performance_preface": {
                "path": str(PREFACE_WITNESS_PATH.relative_to(ROOT)),
                "sha256": sha256(PREFACE_WITNESS_PATH.read_bytes()),
            },
            "preface_commentary": {
                "path": str(PREFACE_COMMENTARY_PATH.relative_to(ROOT)),
                "sha256": sha256(PREFACE_COMMENTARY_PATH.read_bytes()),
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
            "timing_status": "unsynchronised",
        },
        "preface": preface,
        "stanzas": stanzas,
    }


def validate(data: dict, require_commentary: bool) -> dict:
    errors = []
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
    stanzas = data.get("stanzas", [])
    names = [name for stanza in stanzas for name in stanza.get("names", [])]
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
        if not item.get("citation_iast") or not item.get("deva") or not item.get("deva_surface"):
            errors.append(f"name {number} lacks citation forms")
        if require_commentary:
            source = item.get("chinmayananda")
            if not item.get("meaning") or not source or not source.get("commentary"):
                errors.append(f"name {number} lacks Chinmayananda English")
            meaning = item.get("meaning", "")
            if not 5 <= len(meaning) <= 240 or "\n" in meaning:
                errors.append(f"name {number} has an invalid concise meaning length/shape")
            if re.search(r"[*†‡\u0900-\u0dff]", meaning):
                errors.append(f"name {number} concise meaning contains a footnote marker or source script")
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
            if source and not source.get("scan_pages"):
                errors.append(f"name {number} lacks scan-page provenance")
            if source and "detail" not in source:
                errors.append(f"name {number} lacks the non-duplicative commentary detail field")
            detail = source.get("detail", "") if source else ""
            if detail and detail.lstrip().startswith(meaning.strip()):
                errors.append(f"name {number} detailed commentary repeats the concise definition")
    serialized = json.dumps(data, ensure_ascii=False)
    for fragment in FORBIDDEN_OCR_FRAGMENTS:
        if fragment.lower() in serialized.lower():
            errors.append(f"forbidden OCR artifact remains: {fragment}")
    if errors:
        raise ValueError("\n".join(errors[:80]))
    return {
        "preface_units": sum(len(group.get("units", [])) for group in preface_groups),
        "stanzas": len(stanzas),
        "names": len(names),
        "with_commentary": sum("chinmayananda" in item for item in names),
        "with_traditional_derivation": sum("traditional_derivation" in item for item in names),
        "critical_text_differences": sum(bool(stanza.get("critical_text_differs")) for stanza in stanzas),
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
                "english_close": name["meaning"],
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
    parser.add_argument("--check", type=Path)
    parser.add_argument("--require-commentary", action="store_true")
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
        report = validate(data, require_commentary=True)
        report.update(write_web_payloads(data, args.web_core_output, args.web_details_output))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    if args.check:
        report = validate(json.loads(args.check.read_text(encoding="utf-8")), args.require_commentary)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    received = load_pinned(args.received_source, RECEIVED_URL, RECEIVED_SHA256)
    word_split = load_pinned(args.word_split_source, WORD_SPLIT_URL, WORD_SPLIT_SHA256)
    data = build(received, word_split, args.commentary, args.analysis)
    report = validate(data, args.require_commentary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report.update(write_web_payloads(data, args.web_core_output, args.web_details_output))
    if args.update_citation_index:
        report["citation_entries"] = update_citation_index(data, args.update_citation_index)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
