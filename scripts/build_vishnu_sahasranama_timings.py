#!/usr/bin/env python3
"""Build unit timings for the selected Sanjeev Abhyankar recitation.

No transcription model is run. The builder aligns the already-verified reader
text to the official publisher video's existing original-language word
timestamps, then applies a small reviewed boundary table for the heterogeneous
opening. The homogeneous 107-name chant is aligned globally and monotonically.
"""

from __future__ import annotations

import argparse
import bisect
import difflib
import hashlib
import json
import unicodedata
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
READER_PATH = ROOT / "gita/vishnu-sahasranama/reader-core.json"
OUTPUT_PATH = ROOT / "gita/vishnu-sahasranama/timings.json"
AUDIO_SHA256 = "9e3b185314c009376eb1b6b07936b1077bc665a29f9bbdba52491b92a8c5f342"
AUDIO_DURATION = 1636.031565
VIDEO_URL = "https://www.youtube.com/watch?v=s9S6umIoH6I"

# Starts read from the official video's existing word timestamps. Boundaries
# with omitted/misrecognized ASR words use the adjacent caption event and the
# monotonic text alignment; no new transcription is involved.
PREFACE_STARTS = {
    "invocation-1": 7.720, "invocation-3": 17.359, "invocation-4": 27.439,
    "invocation-5": 37.960, "invocation-6": 47.760, "invocation-mantra": 57.920,
    "dialogue-7": 61.480, "dialogue-8": 80.560, "dialogue-9": 98.240,
    "dialogue-10": 109.479, "dialogue-11": 130.120, "dialogue-12": 144.040,
    "dialogue-13": 153.760, "dialogue-14": 164.800, "dialogue-15": 175.640,
    "dialogue-16": 184.440, "dialogue-17": 194.200, "dialogue-18": 204.319,
    "dialogue-19": 214.400, "dialogue-20": 224.640, "dialogue-21": 234.640,
    "dialogue-22": 244.799,
    "assignment-1": 258.079, "assignment-2": 263.680, "assignment-3": 269.800,
    "assignment-4": 270.800, "assignment-5": 278.622, "assignment-6": 281.440,
    "assignment-7": 285.440, "assignment-8": 290.600, "assignment-9": 294.460,
    "assignment-10": 298.320, "assignment-11": 303.560, "assignment-12": 307.280,
    "assignment-13": 311.639, "assignment-14": 315.440, "assignment-15": 319.039,
    "meditation-1": 327.000, "meditation-2": 361.800, "meditation-mantra": 388.479,
    "meditation-3": 397.000, "meditation-4": 421.720, "meditation-5": 436.440,
    "meditation-6": 446.759, "meditation-7": 466.759,
}
NAMES_START = 498.080
CLOSING_NAME_START = 1589.279
PROTECTION_START = 1593.240
PROTECTION_END = 1624.610


def phonetic_key(value: str, *, devanagari: bool = False) -> str:
    if devanagari:
        value = transliterate(value, sanscript.DEVANAGARI, sanscript.IAST)
    value = (value.lower().replace("ś", "s").replace("ṣ", "s")
             .replace("ṃ", "").replace("ṁ", "").replace("ḥ", "").replace("v", "w"))
    value = unicodedata.normalize("NFD", value)
    return "".join(char for char in value if unicodedata.category(char) != "Mn" and char.isalpha())


def caption_tokens(path: Path) -> list[tuple[str, float]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for event in data.get("events", []):
        if event.get("aAppend") or not event.get("segs"):
            continue
        for segment in event["segs"]:
            raw = segment.get("utf8", "").strip()
            if not raw or raw.startswith("["):
                continue
            start = (event.get("tStartMs", 0) + segment.get("tOffsetMs", 0)) / 1000
            out.extend((word, start) for word in raw.split())
    return out


def monotonic_name_starts(stanzas: list[dict], tokens: list[tuple[str, float]]) -> tuple[list[float], float]:
    timed = [(word, start) for word, start in tokens if 495 <= start <= CLOSING_NAME_START + 2]
    caption_text = ""
    caption_times = []
    for word, start in timed:
        normalized = phonetic_key(word, devanagari=True)
        caption_text += normalized
        caption_times.extend([start] * len(normalized))

    canonical = ""
    boundaries = [0]
    for stanza in stanzas:
        canonical += phonetic_key(stanza["iast"])
        boundaries.append(len(canonical))

    matcher = difflib.SequenceMatcher(None, canonical, caption_text, autojunk=False)
    blocks = [block for block in matcher.get_matching_blocks() if block.size]
    anchors = [(0, NAMES_START)]
    for block in blocks:
        anchors.append((block.a, caption_times[block.b]))
        anchors.append((block.a + block.size, caption_times[min(len(caption_times) - 1, block.b + block.size - 1)]))
    anchors.append((len(canonical), CLOSING_NAME_START))

    clean = []
    for offset, start in sorted(anchors):
        if clean and offset == clean[-1][0]:
            clean[-1] = (offset, min(clean[-1][1], start))
        elif not clean or start >= clean[-1][1] - 1:
            clean.append((offset, max(start, clean[-1][1] if clean else start)))
    offsets = [offset for offset, _start in clean]

    def interpolate(offset: int) -> float:
        index = bisect.bisect_right(offsets, offset)
        if index == 0:
            return clean[0][1]
        if index >= len(clean):
            return clean[-1][1]
        x0, t0 = clean[index - 1]
        x1, t1 = clean[index]
        return t0 if x1 == x0 else t0 + (offset - x0) / (x1 - x0) * (t1 - t0)

    starts = [interpolate(offset) for offset in boundaries]
    starts[0], starts[-1] = NAMES_START, CLOSING_NAME_START
    return starts, matcher.ratio()


def build(captions_path: Path) -> dict:
    reader = json.loads(READER_PATH.read_text(encoding="utf-8"))
    preface_ids = [unit["id"] for group in reader["preface"]["groups"] for unit in group["units"]]
    if preface_ids != list(PREFACE_STARTS):
        raise ValueError("reviewed preface timing table no longer matches reader order")
    tokens = caption_tokens(captions_path)
    name_starts, alignment_ratio = monotonic_name_starts(reader["stanzas"], tokens)

    units = []
    preface_starts = [PREFACE_STARTS[unit_id] for unit_id in preface_ids] + [NAMES_START]
    for index, unit_id in enumerate(preface_ids):
        units.append({"id": unit_id, "kind": "preface", "start": preface_starts[index], "end": preface_starts[index + 1]})
    for index, stanza in enumerate(reader["stanzas"]):
        units.append({"id": f"stanza-{stanza['number']}", "kind": "stanza", "start": name_starts[index], "end": name_starts[index + 1]})
    units.extend([
        {"id": "closing-name", "kind": "postlude", "start": CLOSING_NAME_START, "end": PROTECTION_START},
        {"id": "protection", "kind": "postlude", "start": PROTECTION_START, "end": PROTECTION_END},
    ])
    for unit in units:
        unit["start"] = round(unit["start"], 3)
        unit["end"] = round(unit["end"], 3)
    return {
        "schema_version": 1,
        "timing_status": "start-only-reviewed",
        "audio": {"sha256": AUDIO_SHA256, "duration_seconds": AUDIO_DURATION},
        "alignment": {
            "method": "monotonic alignment of verified units to existing official-video word timestamps; no new transcription",
            "official_video": VIDEO_URL,
            "captions_sha256": hashlib.sha256(captions_path.read_bytes()).hexdigest(),
            "global_name_alignment_ratio": round(alignment_ratio, 6),
            "reviewed_preface_boundaries": len(PREFACE_STARTS),
        },
        "units": units,
    }


def validate(data: dict) -> dict:
    reader = json.loads(READER_PATH.read_text(encoding="utf-8"))
    expected = ([unit["id"] for group in reader["preface"]["groups"] for unit in group["units"]]
                + [f"stanza-{stanza['number']}" for stanza in reader["stanzas"]]
                + ["closing-name", "protection"])
    units = data.get("units", [])
    errors = []
    if [unit.get("id") for unit in units] != expected:
        errors.append("timed unit population/order does not exactly match the 154 displayed units")
    previous_end = 0.0
    for unit in units:
        start, end = unit.get("start"), unit.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or start < 0 or end <= start or end > AUDIO_DURATION:
            errors.append(f"invalid timing for {unit.get('id')}: {start}–{end}")
        if start < previous_end - 0.001:
            errors.append(f"overlapping timing at {unit.get('id')}")
        previous_end = end
    if errors:
        raise ValueError("\n".join(errors))
    return {
        "units": len(units),
        "first_start": units[0]["start"],
        "last_end": units[-1]["end"],
        "name_stanzas": sum(unit["kind"] == "stanza" for unit in units),
        "global_name_alignment_ratio": data["alignment"]["global_name_alignment_ratio"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--captions", type=Path)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    if args.check:
        data = json.loads(args.check.read_text(encoding="utf-8"))
    else:
        if not args.captions:
            parser.error("--captions is required when building")
        data = build(args.captions)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(validate(data), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
