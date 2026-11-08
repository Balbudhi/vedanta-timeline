#!/usr/bin/env python3
"""Measure the technical quality of a recitation recording (plan §15.2).

Usage:
    python scripts/audio/measure_quality.py AUDIO [--out quality.json]
                                                 [--ffmpeg /opt/homebrew/bin/ffmpeg]

Measurements (all from ffmpeg/ffprobe plus a PCM pass in numpy):
  container     codec, sample rate, channels, declared bitrate, duration
  ebur128       integrated loudness (LUFS), loudness range (LU), true peak (dBTP)
  astats        overall peak, RMS, DC offset, noise floor, flat factor
  pcm           clipping (samples at |x| >= 0.999 and clipped runs >= 3 samples),
                stereo correlation (Pearson, L vs R; null for mono),
                noise floor in silent gaps: the recording is cut into 50 ms frames;
                a frame is "gap" when its RMS is >= 25 dB below the median RMS of
                all frames and lies in a run of gap frames lasting >= 300 ms; the
                reported value is the median RMS (dBFS) of gap frames, with the
                total gap time and gap count.

The script never modifies the input. Output is a JSON document (stdout or --out).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

FRAME_MS = 50
GAP_REL_DB = 25.0
GAP_MIN_MS = 300
CLIP_LEVEL = 0.999
CLIP_RUN = 3


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed ({proc.returncode}): {proc.stderr[-2000:]}")
    return proc.stderr + proc.stdout


def probe(ffprobe: str, path: Path) -> dict:
    out = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries",
         "format=duration,bit_rate,format_name:stream=codec_name,sample_rate,channels,bit_rate",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    stream = next(s for s in data["streams"] if "sample_rate" in s)
    fmt = data["format"]
    return {
        "codec": stream.get("codec_name"),
        "container": fmt.get("format_name"),
        "sample_rate_hz": int(stream["sample_rate"]),
        "channels": int(stream["channels"]),
        "bitrate_bps": int(stream.get("bit_rate") or fmt.get("bit_rate") or 0),
        "duration_s": round(float(fmt["duration"]), 3),
    }


def ebur128_and_astats(ffmpeg: str, path: Path) -> dict:
    log = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(path), "-af",
               "ebur128=peak=true,"
               "astats=measure_overall=Peak_level+RMS_level+Noise_floor+Flat_factor+Peak_count+DC_offset"
               ":measure_perchannel=none",
               "-f", "null", "-"])
    summary = log[log.rfind("Summary:"):]

    def grab(pattern: str) -> float | None:
        m = re.search(pattern, summary)
        return float(m.group(1)) if m else None

    return {
        "ebur128": {
            "integrated_lufs": grab(r"I:\s+(-?[\d.]+) LUFS"),
            "loudness_range_lu": grab(r"LRA:\s+(-?[\d.]+) LU"),
            "lra_low_lufs": grab(r"LRA low:\s+(-?[\d.]+) LUFS"),
            "lra_high_lufs": grab(r"LRA high:\s+(-?[\d.]+) LUFS"),
            "true_peak_dbtp": grab(r"Peak:\s+(-?[\d.]+) dBFS"),
        },
        "astats_overall": {
            "peak_level_db": grab(r"Peak level dB: (-?[\d.]+)"),
            "rms_level_db": grab(r"RMS level dB: (-?[\d.]+)"),
            "dc_offset": grab(r"DC offset: (-?[\d.]+)"),
            "noise_floor_db": grab(r"Noise floor dB: (-?[\d.]+)"),
            "flat_factor": grab(r"Flat factor: (-?[\d.]+)"),
            "peak_count": grab(r"Peak count: (-?[\d.]+)"),
        },
    }


def decode_pcm(ffmpeg: str, path: Path, sample_rate: int, channels: int) -> np.ndarray:
    raw = subprocess.run(
        [ffmpeg, "-v", "error", "-i", str(path), "-f", "f32le", "-acodec", "pcm_f32le", "-"],
        capture_output=True, check=True).stdout
    pcm = np.frombuffer(raw, dtype=np.float32)
    return pcm.reshape(-1, channels)


def db(x: float) -> float:
    return float(20.0 * np.log10(max(x, 1e-12)))


def pcm_measurements(pcm: np.ndarray, sample_rate: int) -> dict:
    channels = pcm.shape[1]
    mono = pcm.mean(axis=1)

    # Clipping: samples at/above the clip level, and runs of >= CLIP_RUN such samples.
    over = np.abs(pcm) >= CLIP_LEVEL
    clipped_samples = int(over.sum())
    clipped_runs = 0
    for ch in range(channels):
        col = over[:, ch].astype(np.int8)
        edges = np.diff(np.concatenate(([0], col, [0])))
        starts = np.flatnonzero(edges == 1)
        ends = np.flatnonzero(edges == -1)
        clipped_runs += int(((ends - starts) >= CLIP_RUN).sum())

    # Stereo correlation.
    correlation = None
    if channels >= 2:
        left, right = pcm[:, 0].astype(np.float64), pcm[:, 1].astype(np.float64)
        if left.std() > 0 and right.std() > 0:
            correlation = float(np.corrcoef(left, right)[0, 1])

    # Frame RMS.
    frame = int(sample_rate * FRAME_MS / 1000)
    n_frames = len(mono) // frame
    frames = mono[: n_frames * frame].reshape(n_frames, frame).astype(np.float64)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    rms_db = 20.0 * np.log10(np.maximum(rms, 1e-12))
    median_db = float(np.median(rms_db))
    threshold_db = median_db - GAP_REL_DB
    quiet = rms_db <= threshold_db
    min_run = max(1, GAP_MIN_MS // FRAME_MS)
    edges = np.diff(np.concatenate(([0], quiet.astype(np.int8), [0])))
    starts = np.flatnonzero(edges == 1)
    ends = np.flatnonzero(edges == -1)
    gap_mask = np.zeros_like(quiet)
    gaps = []
    for s, e in zip(starts, ends):
        if e - s >= min_run:
            gap_mask[s:e] = True
            gaps.append([round(s * FRAME_MS / 1000, 3), round(e * FRAME_MS / 1000, 3)])
    gap_floor = float(np.median(rms_db[gap_mask])) if gap_mask.any() else None

    return {
        "clipping": {
            "level": CLIP_LEVEL,
            "clipped_samples": clipped_samples,
            "clipped_runs_ge_3": clipped_runs,
        },
        "stereo_correlation": None if correlation is None else round(correlation, 6),
        "peak_abs": round(float(np.abs(pcm).max()), 6),
        "frame_rms_median_dbfs": round(median_db, 2),
        "gap_noise_floor": {
            "method": f"median RMS of {FRAME_MS} ms frames >= {GAP_REL_DB} dB below the median "
                      f"frame RMS, in quiet runs >= {GAP_MIN_MS} ms",
            "gap_threshold_dbfs": round(threshold_db, 2),
            "noise_floor_dbfs": None if gap_floor is None else round(gap_floor, 2),
            "gap_count": len(gaps),
            "gap_total_s": round(sum(e - s for s, e in gaps), 3),
            "gaps": gaps,
        },
    }


def measure(path: Path, ffmpeg: str, ffprobe: str) -> dict:
    info = probe(ffprobe, path)
    filters = ebur128_and_astats(ffmpeg, path)
    pcm = decode_pcm(ffmpeg, path, info["sample_rate_hz"], info["channels"])
    result = {
        "file": str(path),
        "measured_duration_s": round(len(pcm) / info["sample_rate_hz"], 3),
        **info,
        **filters,
        **pcm_measurements(pcm, info["sample_rate_hz"]),
        "tool": {"ffmpeg": run([ffmpeg, "-version"]).splitlines()[0]},
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--ffmpeg", default="/opt/homebrew/bin/ffmpeg")
    args = ap.parse_args()
    ffprobe = str(Path(args.ffmpeg).with_name("ffprobe"))
    result = measure(args.audio, args.ffmpeg, ffprobe)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
