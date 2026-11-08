#!/usr/bin/env python3
"""Align a Gītā chapter recitation to its BORI text and write the verse manifest.

Plan: docs/GITA_FULL_TRANSLATION_PLAN.md §5.2 and §15.6; standard:
docs/AUDIO_ALIGNMENT_STANDARD.md. The manifest written here is `provisional`
until the owner has listened (standard, Alignment workflow 3–4).

Pipeline
  a. ffmpeg: source → 16 kHz mono PCM WAV in --workdir (private store).
  b. Transcript units from packet.json in verse order: optional speaker lines
     (verses[].speaker_line) and the verses (verses[].iast / .devanagari), one
     token per whitespace-separated word, "|" "||" "।" "॥" dropped; verse, line
     and unit boundaries are recorded by token index.
  c. Primary aligner: torchaudio.pipelines.MMS_FA (wav2vec2, CC BY-NC 4.0) on the
     uroman romanisation of the IAST restricted to its a–z vocabulary.
  d. Second aligner sharing no acoustic model: Harveenchadha/vakyansh-wav2vec2-
     sanskrit-sam-60 (wav2vec2 CTC, Devanāgarī vocabulary, MIT) via transformers,
     with torchaudio.functional.forced_align over the Devanāgarī transcript.
     Both: emissions per VAD-gap-delimited chunk (≤ --chunk-s), one Viterbi forced
     alignment over the concatenated emissions.
  e. Silero VAD speech regions. Verse start = start of the speech region that
     contains the first token's onset (shift ≤ --snap-s); verse end = end of the
     region containing the last token's onset, measured from the last token's end
     (shift ≤ --snap-end-s: a CTC emission marks the onset of the final character,
     and the chanted final vowel runs on to the region end). A boundary with no region within tolerance stays
     at the raw time and is marked unsnapped.
  f. Corroboration: a verse is corroborated when, for both start and end, the two
     aligners' snapped times lie in the same VAD gap and agree within --agree-s.

  Untranscribed speech (announcements, chapter heading, colophon) would attract
  neighbouring transcript tokens in a forced alignment, so it is found without the
  forced path: each aligner's free greedy decode of every VAD region is globally
  aligned (Needleman–Wunsch, characters) to the whole transcript; a region whose
  decoded characters are matched below --min-coverage is masked to blank before
  any forced alignment. Optional units (speaker lines) are then decided by a
  likelihood-ratio test on the masked emissions: chanted when the forced-path
  score with the unit exceeds the score without it. The greedy decodes of the
  masked regions are kept as evidence of what the audio contains.

Outputs
  --out-raw       per-token times from both aligners, VAD regions, coverage,
                  masks, likelihood ratios, snapping decisions (private).
  --out-manifest  gita/chN/audio.js in the shape of gita/sthitaprajna/audio.js
                  plus licence, source_url, timing_status, method, corroboration.

Determinism: CPU inference, fixed torch seed, argmax decoding, no sampling.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
import unicodedata
import wave
from dataclasses import dataclass, field, asdict
from pathlib import Path

import numpy as np
import torch
import torchaudio
import torchaudio.functional as F

SR = 16000
FRAME_S = 320 / SR  # wav2vec2 frame hop (20 ms)
VAKYANSH_ID = "Harveenchadha/vakyansh-wav2vec2-sanskrit-sam-60"
VAKYANSH_REV = "28c2078678b3674c2a29734d2e473c1e9325c295"
NEG = -1e4

# ---------------------------------------------------------------------------
# Transcript units and tokens
# ---------------------------------------------------------------------------

IAST_PUNCT = {"|", "||"}
DEVA_PUNCT = {"।", "॥"}


@dataclass
class Unit:
    """A run of tokens aligned as one block: a verse or a speaker line."""
    uid: str                 # "12.1" or "12.1:speaker"
    kind: str                # "verse" | "speaker"
    locus: str
    optional: bool
    tokens_iast: list[str] = field(default_factory=list)
    tokens_deva: list[str] = field(default_factory=list)
    line_starts: list[int] = field(default_factory=list)  # token index (within unit) of each line


_VOWELS = {"a": ("अ", ""), "ā": ("आ", "ा"), "i": ("इ", "ि"), "ī": ("ई", "ी"), "u": ("उ", "ु"),
           "ū": ("ऊ", "ू"), "ṛ": ("ऋ", "ृ"), "ṝ": ("ॠ", "ॄ"), "ḷ": ("ऌ", "ॢ"), "e": ("ए", "े"),
           "ai": ("ऐ", "ै"), "o": ("ओ", "ो"), "au": ("औ", "ौ")}
_CONS = {"k": "क", "kh": "ख", "g": "ग", "gh": "घ", "ṅ": "ङ", "c": "च", "ch": "छ", "j": "ज", "jh": "झ",
         "ñ": "ञ", "ṭ": "ट", "ṭh": "ठ", "ḍ": "ड", "ḍh": "ढ", "ṇ": "ण", "t": "त", "th": "थ", "d": "द",
         "dh": "ध", "n": "न", "p": "प", "ph": "फ", "b": "ब", "bh": "भ", "m": "म", "y": "य", "r": "र",
         "l": "ल", "v": "व", "ś": "श", "ṣ": "ष", "s": "स", "h": "ह", "ḻ": "ळ"}
_MARKS = {"ṃ": "ं", "ḥ": "ः", "m̐": "ँ", "'": "ऽ"}


def iast_to_devanagari(word: str) -> str:
    """Deterministic IAST → Devanāgarī for one word. Checked against the packet's
    Devanāgarī for every verse token; used to spell the speaker lines."""
    word = unicodedata.normalize("NFC", word)
    out: list[str] = []
    i = 0
    pending_cons = False
    while i < len(word):
        two, one = word[i:i + 2], word[i]
        key, step = (two, 2) if (two in _CONS or two in _VOWELS or two in _MARKS) else (one, 1)
        if key in _CONS:
            if pending_cons:
                out.append("्")
            out.append(_CONS[key])
            pending_cons = True
        elif key in _VOWELS:
            indep, sign = _VOWELS[key]
            out.append(sign if pending_cons else indep)
            pending_cons = False
        elif key in _MARKS:
            if pending_cons:
                out.append("्")
                pending_cons = False
            out.append(_MARKS[key])
        else:
            raise ValueError(f"cannot transliterate {key!r} in {word!r}")
        i += step
    if pending_cons:
        out.append("्")
    return "".join(out)


def split_tokens(text: str, punct: set[str]) -> list[list[str]]:
    lines = []
    for line in text.split("\n"):
        toks = [t for t in line.split() if t not in punct]
        if toks:
            lines.append(toks)
    return lines


def build_units(packet: dict) -> list[Unit]:
    units: list[Unit] = []
    for v in packet["verses"]:
        locus = v["locus"]
        sp = v.get("speaker_line")
        if sp and sp.get("text"):
            toks = sp["text"].split()
            units.append(Unit(uid=f"{locus}:speaker", kind="speaker", locus=locus, optional=True,
                              tokens_iast=toks, tokens_deva=[iast_to_devanagari(t) for t in toks],
                              line_starts=[0]))
        iast_lines = split_tokens(v["iast"], IAST_PUNCT)
        deva_lines = split_tokens(v["devanagari"], DEVA_PUNCT)
        if [len(l) for l in iast_lines] != [len(l) for l in deva_lines]:
            raise ValueError(f"{locus}: IAST/Devanāgarī token counts differ")
        u = Unit(uid=locus, kind="verse", locus=locus, optional=False)
        for il, dl in zip(iast_lines, deva_lines):
            u.line_starts.append(len(u.tokens_iast))
            u.tokens_iast.extend(il)
            u.tokens_deva.extend(dl)
            for a, b in zip(il, dl):
                if iast_to_devanagari(a) != b:
                    raise ValueError(f"{locus}: packet Devanāgarī {b!r} != transliterated IAST {a!r} "
                                     f"({iast_to_devanagari(a)!r})")
        units.append(u)
    return units


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------

def normalise_audio(ffmpeg: str, src: Path, wav_path: Path) -> np.ndarray:
    subprocess.run([ffmpeg, "-y", "-v", "error", "-i", str(src), "-ac", "1", "-ar", str(SR),
                    "-c:a", "pcm_s16le", str(wav_path)], check=True)
    with wave.open(str(wav_path)) as w:
        assert w.getnchannels() == 1 and w.getframerate() == SR and w.getsampwidth() == 2
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0


def vad_regions(pcm: np.ndarray, min_silence_ms: int, pad_ms: int) -> list[dict]:
    from silero_vad import load_silero_vad, get_speech_timestamps
    model = load_silero_vad()
    ts = get_speech_timestamps(torch.from_numpy(pcm), model, sampling_rate=SR, threshold=0.5,
                               min_silence_duration_ms=min_silence_ms, speech_pad_ms=pad_ms,
                               return_seconds=True)
    return [{"start": float(r["start"]), "end": float(r["end"])} for r in ts]


def make_chunks(regions: list[dict], total_s: float, max_chunk_s: float) -> list[tuple[float, float]]:
    """Cut the timeline at VAD-gap midpoints so no chunk exceeds max_chunk_s where
    the gaps allow. Chunks tile the whole timeline."""
    cuts = [0.0]
    chunk_start = 0.0
    for i in range(len(regions) - 1):
        if regions[i + 1]["end"] - chunk_start > max_chunk_s:
            mid = (regions[i]["end"] + regions[i + 1]["start"]) / 2
            if mid > chunk_start:
                cuts.append(mid)
                chunk_start = mid
    cuts.append(total_s)
    return [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)]


# ---------------------------------------------------------------------------
# Aligners
# ---------------------------------------------------------------------------

class Aligner:
    name: str
    labels: list[str]
    blank: int
    space: int | None = None  # word-delimiter label id, if the vocabulary has one

    def tokens_of(self, unit: Unit) -> list[str]:
        raise NotImplementedError

    def encode(self, token: str) -> list[int]:
        raise NotImplementedError

    def emit(self, pcm_chunk: np.ndarray) -> torch.Tensor:  # [T, C] log-probs
        raise NotImplementedError

    def emissions(self, pcm: np.ndarray, chunks) -> tuple[torch.Tensor, np.ndarray]:
        parts, times = [], []
        for (a, b) in chunks:
            s0, s1 = int(round(a * SR)), int(round(b * SR))
            lp = self.emit(pcm[s0:s1])
            parts.append(lp)
            times.append(s0 / SR + np.arange(lp.shape[0]) * FRAME_S)
        return torch.cat(parts, 0), np.concatenate(times)

    def greedy_ids(self, lp: torch.Tensor) -> list[int]:
        """Collapsed argmax decode without blanks and word delimiters."""
        ids = lp.argmax(-1).tolist()
        out, prev = [], None
        for i in ids:
            if i != prev and i != self.blank and i != self.space:
                out.append(i)
            prev = i
        return out

    def text(self, ids: list[int]) -> str:
        return "".join(self.labels[i] for i in ids)


class MMSAligner(Aligner):
    name = "mms_fa"

    def __init__(self, device: str):
        from torchaudio.pipelines import MMS_FA
        import uroman
        self.model = MMS_FA.get_model(with_star=False).eval().to(device)
        self.labels = list(MMS_FA.get_labels(star=None))
        self.blank = 0
        self.dictionary = {c: i for i, c in enumerate(self.labels)}
        self.uroman = uroman.Uroman()
        self.device = device

    def tokens_of(self, unit: Unit) -> list[str]:
        return unit.tokens_iast

    def romanise(self, token: str) -> str:
        rom = self.uroman.romanize_string(token).lower()
        return "".join(c for c in rom if c in self.dictionary and c not in ("-", "*", "'"))

    def encode(self, token: str) -> list[int]:
        return [self.dictionary[c] for c in self.romanise(token)]

    def emit(self, pcm_chunk: np.ndarray) -> torch.Tensor:
        x = torch.from_numpy(pcm_chunk).unsqueeze(0).to(self.device)
        with torch.inference_mode():
            em, _ = self.model(x)
        return torch.log_softmax(em[0].float().cpu(), dim=-1)


class VakyanshAligner(Aligner):
    name = "vakyansh_sanskrit"

    def __init__(self, device: str):
        from transformers import Wav2Vec2ForCTC, Wav2Vec2FeatureExtractor
        from huggingface_hub import hf_hub_download
        self.model = Wav2Vec2ForCTC.from_pretrained(VAKYANSH_ID, revision=VAKYANSH_REV).eval().to(device)
        self.fe = Wav2Vec2FeatureExtractor.from_pretrained(VAKYANSH_ID, revision=VAKYANSH_REV)
        vocab = json.load(open(hf_hub_download(VAKYANSH_ID, "vocab.json", revision=VAKYANSH_REV)))
        self.dictionary = {k: int(v) for k, v in vocab.items()}
        self.labels = [k for k, _ in sorted(self.dictionary.items(), key=lambda kv: kv[1])]
        # fairseq-trained wav2vec2 CTC: the blank is the dictionary's bos "<s>" (index 0),
        # not the HF pad token (checked: 84% of frames argmax to 0, none to 1).
        self.blank = self.dictionary["<s>"]
        self.space = self.dictionary["|"]
        self.special = {self.dictionary[k] for k in ("<s>", "<pad>", "</s>", "<unk>", "|")}
        self.device = device

    def tokens_of(self, unit: Unit) -> list[str]:
        return unit.tokens_deva

    def encode(self, token: str) -> list[int]:
        return [self.dictionary[c] for c in unicodedata.normalize("NFC", token)
                if c in self.dictionary and self.dictionary[c] not in self.special]

    def emit(self, pcm_chunk: np.ndarray) -> torch.Tensor:
        inp = self.fe(pcm_chunk, sampling_rate=SR, return_tensors="pt")
        with torch.inference_mode():
            logits = self.model(inp.input_values.to(self.device)).logits
        return torch.log_softmax(logits[0].float().cpu(), dim=-1)


# ---------------------------------------------------------------------------
# Untranscribed speech: greedy decode vs transcript (global character alignment)
# ---------------------------------------------------------------------------

def nw_matches(a: np.ndarray, b: np.ndarray, match: int = 2, mismatch: int = -1, gap: int = -1) -> np.ndarray:
    """Needleman–Wunsch over int sequences; returns, for every position of `a`, 1 if
    it is aligned to an equal symbol of `b`, else 0. Row-vectorised numpy."""
    n, m = len(a), len(b)
    dp = np.empty((n + 1, m + 1), dtype=np.int32)
    dp[0] = np.arange(m + 1) * gap
    jj = np.arange(m + 1)
    for i in range(1, n + 1):
        sub = np.where(b == a[i - 1], match, mismatch)
        cand = np.empty(m + 1, dtype=np.int32)
        cand[0] = dp[i - 1, 0] + gap
        cand[1:] = np.maximum(dp[i - 1, :-1] + sub, dp[i - 1, 1:] + gap)
        # horizontal gaps: dp[i,j] = max_{j'<=j} (cand[j'] + (j - j') * gap)
        dp[i] = np.maximum.accumulate(cand - jj * gap) + jj * gap
    matched = np.zeros(n, dtype=np.int8)
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1] and dp[i, j] == dp[i - 1, j - 1] + match:
            matched[i - 1] = 1
            i -= 1; j -= 1
        elif dp[i, j] == dp[i - 1, j - 1] + mismatch:
            i -= 1; j -= 1
        elif dp[i, j] == dp[i - 1, j] + gap:
            i -= 1
        else:
            j -= 1
    return matched


def region_coverage(aligner: Aligner, lp: torch.Tensor, frame_t: np.ndarray, regions: list[dict],
                    units: list[Unit]) -> list[dict]:
    """Per VAD region: greedy decode, its length, and the share of decoded characters
    matched to the transcript in a global alignment of the whole recording."""
    decoded, owner = [], []
    rows = []
    for i, r in enumerate(regions):
        sel = torch.from_numpy((frame_t >= r["start"]) & (frame_t < r["end"]))
        ids = aligner.greedy_ids(lp[sel])
        rows.append({"region": i, "start": r["start"], "end": r["end"], "decoded": aligner.text(ids),
                     "decoded_len": len(ids)})
        decoded.extend(ids)
        owner.extend([i] * len(ids))
    transcript = [s for u in units for tok in aligner.tokens_of(u) for s in aligner.encode(tok)]
    matched = nw_matches(np.array(decoded, dtype=np.int32), np.array(transcript, dtype=np.int32))
    owner_arr = np.array(owner, dtype=np.int32)
    for row in rows:
        n = row["decoded_len"]
        k = int(matched[owner_arr == row["region"]].sum()) if n else 0
        row["matched"] = k
        row["coverage"] = round(k / n, 3) if n else None
    return rows


def mask_regions(lp: torch.Tensor, frame_t: np.ndarray, regions: list[dict], idxs: list[int],
                 blank: int) -> torch.Tensor:
    lp = lp.clone()
    mask = np.zeros(len(frame_t), dtype=bool)
    for i in idxs:
        mask |= (frame_t >= regions[i]["start"]) & (frame_t < regions[i]["end"])
    m = torch.from_numpy(mask)
    lp[m] = NEG
    lp[m, blank] = 0.0
    return lp


# ---------------------------------------------------------------------------
# Forced alignment
# ---------------------------------------------------------------------------

@dataclass
class TokenTime:
    unit: str
    idx: int
    text: str
    start: float
    end: float
    score: float  # mean log-prob over the token's emitted frames


def align_tokens(aligner: Aligner, lp: torch.Tensor, frame_t: np.ndarray, units: list[Unit],
                 use: set[str]) -> tuple[list[TokenTime], float]:
    """Viterbi forced alignment of the selected units; returns token times and the
    path log-probability (sum of per-frame log-probs along the best path)."""
    seq: list[int] = []
    owners: list[tuple[str, int, str]] = []
    for u in units:
        if u.uid not in use:
            continue
        for k, tok in enumerate(aligner.tokens_of(u)):
            ids = aligner.encode(tok)
            if not ids:
                raise ValueError(f"{u.uid} token {tok!r} has no symbols in {aligner.name} vocabulary")
            seq.extend(ids)
            owners.extend([(u.uid, k, tok)] * len(ids))
    targets = torch.tensor([seq], dtype=torch.int32)
    aligned, scores = F.forced_align(lp.unsqueeze(0), targets, blank=aligner.blank)
    aligned, scores = aligned[0], scores[0]
    spans = F.merge_tokens(aligned, scores.exp(), blank=aligner.blank)
    if len(spans) != len(seq):
        raise RuntimeError(f"{aligner.name}: {len(spans)} spans for {len(seq)} symbols")
    out: list[TokenTime] = []
    cur, n = None, 0
    for sym_i, sp in enumerate(spans):
        uid, k, text = owners[sym_i]
        t0, t1 = float(frame_t[sp.start]), float(frame_t[sp.end - 1] + FRAME_S)
        lg = math.log(max(sp.score, 1e-12))
        if cur is None or (cur.unit, cur.idx) != (uid, k):
            if cur is not None:
                out.append(cur)
            cur, n = TokenTime(uid, k, text, t0, t1, lg), 1
        else:
            cur.end = t1
            cur.score = (cur.score * n + lg) / (n + 1)
            n += 1
    out.append(cur)
    return out, float(scores.sum())


# ---------------------------------------------------------------------------
# Snapping and corroboration
# ---------------------------------------------------------------------------

def containing_region(t: float, regions: list[dict]) -> int | None:
    for i, r in enumerate(regions):
        if r["start"] <= t <= r["end"]:
            return i
    return None


def snap(t: float, regions: list[dict], kind: str, tol: float, anchor: float | None = None) -> dict:
    """kind 'start': start of the region containing `anchor` (default t), gap = i-1;
    kind 'end': end of that region, gap = i. For verse ends the anchor is the last
    token's onset (reliable) while t is the token's end (early by the chanted final
    vowel). Falls back to the nearest edge of that kind; unsnapped beyond `tol`."""
    i = containing_region(t if anchor is None else anchor, regions)
    edge_key = "start" if kind == "start" else "end"
    if i is None:
        i = min(range(len(regions)), key=lambda k: abs(regions[k][edge_key] - t))
    edge = regions[i][edge_key]
    gap = i - 1 if kind == "start" else i
    if abs(edge - t) <= tol + 1e-9:
        return {"raw": round(t, 3), "snapped": round(edge, 3), "shift": round(edge - t, 3), "gap": gap,
                "snapped_ok": True}
    return {"raw": round(t, 3), "snapped": round(t, 3), "shift": 0.0, "gap": None, "snapped_ok": False}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_aligner(aligner: Aligner, pcm: np.ndarray, chunks, units: list[Unit], regions: list[dict], args) -> dict:
    t0 = time.time()
    lp, frame_t = aligner.emissions(pcm, chunks)
    t_emit = time.time() - t0

    coverage = region_coverage(aligner, lp, frame_t, regions, units)
    flagged = [c["region"] for c in coverage
               if c["decoded_len"] >= args.min_decoded_chars and (c["coverage"] or 0.0) < args.min_coverage]
    lp_m = mask_regions(lp, frame_t, regions, flagged, aligner.blank) if flagged else lp

    verse_uids = {u.uid for u in units if not u.optional}
    all_uids = {u.uid for u in units}
    _, s_full = align_tokens(aligner, lp_m, frame_t, units, all_uids)
    lr = {}
    for u in (u for u in units if u.optional):
        _, s_minus = align_tokens(aligner, lp_m, frame_t, units, all_uids - {u.uid})
        lr[u.uid] = {"score_with": round(s_full, 2), "score_without": round(s_minus, 2),
                     "log_likelihood_ratio": round(s_full - s_minus, 2), "chanted": s_full > s_minus}
    use = verse_uids | {uid for uid, r in lr.items() if r["chanted"]}
    tokens, path_score = align_tokens(aligner, lp_m, frame_t, units, use)
    t_total = time.time() - t0

    # Onset of the last token outside the last unit's region would show stretching.
    long_tokens = [asdict(t) for t in tokens if t.end - t.start > args.long_token_s]
    return {
        "aligner": aligner.name,
        "frames": int(lp.shape[0]),
        "runtime_s": {"emissions": round(t_emit, 1), "total": round(t_total, 1)},
        "region_coverage": coverage,
        "untranscribed_region_indices": flagged,
        "optional_units": lr,
        "units_aligned": [u.uid for u in units if u.uid in use],
        "path_score": round(path_score, 2),
        "tokens": [asdict(t) for t in tokens],
        "long_tokens": long_tokens,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--packet", required=True, type=Path)
    ap.add_argument("--audio", required=True, type=Path, help="source recording (private)")
    ap.add_argument("--workdir", required=True, type=Path, help="private dir for the 16 kHz WAV")
    ap.add_argument("--out-raw", required=True, type=Path)
    ap.add_argument("--out-manifest", required=True, type=Path)
    ap.add_argument("--encoded", type=Path, help="published MP3; duration must match the source within 50 ms")
    ap.add_argument("--src-name", default="recitation.mp3")
    ap.add_argument("--reciter", required=True)
    ap.add_argument("--attribution", required=True)
    ap.add_argument("--licence", required=True)
    ap.add_argument("--source-url", required=True)
    ap.add_argument("--ffmpeg", default="/opt/homebrew/bin/ffmpeg")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--chunk-s", type=float, default=30.0)
    ap.add_argument("--snap-s", type=float, default=0.6, help="max shift for verse starts")
    ap.add_argument("--snap-end-s", type=float, default=1.0, help="max shift for verse ends (CTC final-onset bias)")
    ap.add_argument("--agree-s", type=float, default=0.25)
    ap.add_argument("--vad-min-silence-ms", type=int, default=300)
    ap.add_argument("--vad-pad-ms", type=int, default=100)
    ap.add_argument("--min-coverage", type=float, default=0.4,
                    help="a region whose greedy decode matches the transcript below this share is untranscribed")
    ap.add_argument("--min-decoded-chars", type=int, default=5)
    ap.add_argument("--long-token-s", type=float, default=2.0)
    ap.add_argument("--skip-second", action="store_true", help="debug: primary aligner only")
    args = ap.parse_args()

    torch.manual_seed(0)

    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    units = build_units(packet)
    verses = [u for u in units if not u.optional]
    print(f"[align] {len(units)} units, {len(verses)} verses, {sum(len(u.tokens_iast) for u in units)} tokens",
          file=sys.stderr)

    args.workdir.mkdir(parents=True, exist_ok=True)
    wav_path = args.workdir / (args.audio.stem + "_16k.wav")
    pcm = normalise_audio(args.ffmpeg, args.audio, wav_path)
    total_s = len(pcm) / SR
    regions = vad_regions(pcm, args.vad_min_silence_ms, args.vad_pad_ms)
    chunks = make_chunks(regions, total_s, args.chunk_s)
    print(f"[align] {total_s:.2f} s, {len(regions)} VAD regions, {len(chunks)} chunks", file=sys.stderr)

    aligners = [MMSAligner(args.device)] + ([] if args.skip_second else [VakyanshAligner(args.device)])
    results = []
    for al in aligners:
        print(f"[align] running {al.name}", file=sys.stderr)
        res = run_aligner(al, pcm, chunks, units, regions, args)
        print(f"[align] {al.name}: {res['runtime_s']}, untranscribed regions {res['untranscribed_region_indices']}, "
              f"optional {{{', '.join(f'{k}: {v['chanted']}' for k, v in res['optional_units'].items())}}}",
              file=sys.stderr)
        results.append(res)

    # Per-verse boundaries, snapping, corroboration.
    primary = results[0]
    per_verse, disagreements = [], []
    for u in verses:
        row = {"locus": u.locus, "aligners": {}}
        for res in results:
            toks = [TokenTime(**t) for t in res["tokens"] if t["unit"] == u.uid]
            first, last = min(toks, key=lambda t: t.start), max(toks, key=lambda t: t.start)
            row["aligners"][res["aligner"]] = {
                "start": snap(first.start, regions, "start", args.snap_s),
                "end": {**snap(last.end, regions, "end", args.snap_end_s, anchor=last.start),
                        "last_token_onset": round(last.start, 3)},
                "tokens": len(toks), "mean_token_score": round(sum(t.score for t in toks) / len(toks), 3),
            }
        if len(results) == 2:
            a, b = (row["aligners"][r["aligner"]] for r in results)
            agree = lambda x, y: (x["gap"] is not None and x["gap"] == y["gap"]
                                  and abs(x["snapped"] - y["snapped"]) <= args.agree_s)
            row["start_corroborated"] = agree(a["start"], b["start"])
            row["end_corroborated"] = agree(a["end"], b["end"])
            row["delta_raw"] = {"start": round(a["start"]["raw"] - b["start"]["raw"], 3),
                                "end": round(a["end"]["raw"] - b["end"]["raw"], 3)}
            row["corroborated"] = row["start_corroborated"] and row["end_corroborated"]
        else:
            row["corroborated"] = False
        if not row["corroborated"]:
            disagreements.append(u.locus)
        per_verse.append(row)

    segs = []
    for row in per_verse:
        p = row["aligners"][primary["aligner"]]
        segs.append({"locus": row["locus"], "start": p["start"]["snapped"], "end": p["end"]["snapped"]})
    fixes = []
    for i in range(len(segs)):
        if segs[i]["end"] <= segs[i]["start"]:
            raise RuntimeError(f"{segs[i]['locus']}: end <= start")
        if i + 1 < len(segs) and segs[i]["end"] > segs[i + 1]["start"]:
            mid = round((segs[i]["end"] + segs[i + 1]["start"]) / 2, 3)
            fixes.append({"locus": segs[i]["locus"], "end_was": segs[i]["end"],
                          "next_start_was": segs[i + 1]["start"], "set_to": mid})
            segs[i]["end"] = segs[i + 1]["start"] = mid

    duration_check = None
    if args.encoded:
        ffprobe = str(Path(args.ffmpeg).with_name("ffprobe"))
        dur = lambda p: float(subprocess.run([ffprobe, "-v", "error", "-show_entries", "format=duration", "-of",
                                              "default=nw=1:nk=1", str(p)], capture_output=True, text=True,
                                             check=True).stdout.strip())
        d_src, d_enc = dur(args.audio), dur(args.encoded)
        duration_check = {"source_s": d_src, "encoded_s": d_enc, "delta_ms": round((d_enc - d_src) * 1000, 1),
                          "ok": abs(d_enc - d_src) <= 0.05}
        if not duration_check["ok"]:
            raise RuntimeError(f"encoded duration differs from source by {duration_check['delta_ms']} ms; re-derive")
        if segs[-1]["end"] > d_enc:
            raise RuntimeError("last segment ends after the encoded file")

    flagged_any = sorted({i for res in results for i in res["untranscribed_region_indices"]})
    contents = {
        "speaker_lines": {res["aligner"]: res["optional_units"] for res in results},
        "untranscribed_speech": [
            {"region": i, "start": regions[i]["start"], "end": regions[i]["end"],
             "flagged_by": [res["aligner"] for res in results if i in res["untranscribed_region_indices"]],
             "greedy_decode": {res["aligner"]: res["region_coverage"][i]["decoded"] for res in results},
             "coverage": {res["aligner"]: res["region_coverage"][i]["coverage"] for res in results}}
            for i in flagged_any],
    }

    corroboration = {"verses_total": len(verses), "corroborated": sum(1 for r in per_verse if r["corroborated"]),
                     "disagreements": disagreements}
    import transformers, silero_vad
    method = {
        "primary": {"name": "torchaudio.pipelines.MMS_FA", "model": "MMS forced aligner (wav2vec2, uroman vocabulary)",
                    "torchaudio": torchaudio.__version__, "torch": torch.__version__,
                    "licence": "CC BY-NC 4.0 (model weights)", "transcript": "BORI IAST romanised with uroman 1.3.1.1"},
        "secondary": {"name": VAKYANSH_ID, "revision": VAKYANSH_REV,
                      "model": "wav2vec2 CTC fine-tuned for Sanskrit (Vakyansh / Open-Speech-EkStep)",
                      "licence": "MIT (Open-Speech-EkStep/vakyansh-models LICENSE); no licence field on the Hugging Face card",
                      "transcript": "BORI text in Devanāgarī (packet verses[].devanagari)",
                      "framework": f"transformers {transformers.__version__}, torchaudio.functional.forced_align"},
        "vad": {"name": "silero-vad", "version": silero_vad.__version__, "licence": "MIT",
                "min_silence_ms": args.vad_min_silence_ms, "speech_pad_ms": args.vad_pad_ms},
        "boundary_rule": "start = start of the VAD speech region containing the first token onset "
                         f"(shift <= {args.snap_s} s); end = end of the region containing the last token onset, "
                         f"measured from the last token end (shift <= {args.snap_end_s} s; CTC marks the onset "
                         "of the final character, the chanted final vowel runs to the region end)",
        "corroboration_rule": f"both aligners snapped into the same VAD gap and within {args.agree_s} s, for start and end",
        "untranscribed_speech_rule": f"VAD regions whose greedy decode matches the transcript below {args.min_coverage} "
                                     "in a global character alignment are masked to blank before forced alignment",
        "optional_units_rule": "speaker lines kept when the forced-path log-likelihood with the unit exceeds the one without",
        "boundary_source": "primary aligner",
        "text_edition": packet.get("mula_witness", {}),
        "device": args.device,
        "generated": time.strftime("%Y-%m-%d"),
    }
    manifest = {
        "src": args.src_name, "reciter": args.reciter, "attribution": args.attribution,
        "licence": args.licence, "source_url": args.source_url, "timing_status": "provisional",
        "method": method, "corroboration": corroboration, "verses": segs,
    }
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text("window.GITA_AUDIO = " + json.dumps(manifest, indent=2, ensure_ascii=False) + ";\n",
                                 encoding="utf-8")

    raw = {
        "source": str(args.audio), "wav16k": str(wav_path), "duration_s": round(total_s, 3),
        "packet": str(args.packet),
        "args": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
        "units": [{"uid": u.uid, "kind": u.kind, "optional": u.optional, "tokens_iast": u.tokens_iast,
                   "tokens_deva": u.tokens_deva, "line_starts": u.line_starts} for u in units],
        "vad_regions": regions, "chunks": chunks,
        "contents": contents,
        "aligners": results,
        "per_verse": per_verse,
        "overlap_fixes": fixes,
        "duration_check": duration_check,
        "manifest_segments": segs,
    }
    args.out_raw.parent.mkdir(parents=True, exist_ok=True)
    args.out_raw.write_text(json.dumps(raw, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"[align] corroborated {corroboration['corroborated']}/{corroboration['verses_total']}; "
          f"disagreements {disagreements}; wrote {args.out_manifest} and {args.out_raw}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
