#!/usr/bin/env python3
"""Master and encode a recitation for the reader (plan §15.5, format shift only).

    python scripts/audio/master_encode.py SOURCE OUT.mp3 [--target-lufs -18]
           [--true-peak -1] [--highpass 60] [--bitrate 64k] [--report report.json]
           [--title ...] [--artist ...] [--comment ...]

Pass 1 measures the mono, high-passed signal with ffmpeg's loudnorm (EBU R128).
Pass 2 applies one linear gain (target − measured integrated loudness) and a
true-peak limiter at the true-peak ceiling, run at 192 kHz oversampling, then
encodes CBR MP3 (libmp3lame, Xing/Info header). The limiter is the only
non-linear step; the report records how much audio it touched. loudnorm's own
second pass is not used: when the source's peak-to-loudness ratio exceeds the
target's, loudnorm silently falls back to its "dynamic" mode, a continuous gain
curve that reshapes the loudness range, which the plan excludes.
Pass 3 measures the encoded file and checks integrated loudness within
--tolerance LU of the target, true peak at or under the ceiling (+0.3 dB codec
overshoot allowance) and duration equal to the source within 50 ms.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

OVERSAMPLE = 192000


def sh(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:3])} failed: {p.stderr[-3000:]}")
    return p.stderr + p.stdout


def loudnorm_measure(ffmpeg: str, src: Path, pre: str, target: float, tp: float) -> dict:
    log = sh([ffmpeg, "-hide_banner", "-nostats", "-i", str(src), "-af",
              f"{pre},loudnorm=I={target}:TP={tp}:LRA=11:print_format=json", "-f", "null", "-"])
    return json.loads(log[log.rfind("{"):log.rfind("}") + 1])


def ebur128(ffmpeg: str, path: Path, pre: str | None = None) -> dict:
    af = (pre + "," if pre else "") + "ebur128=peak=true"
    log = sh([ffmpeg, "-hide_banner", "-nostats", "-i", str(path), "-af", af, "-f", "null", "-"])
    s = log[log.rfind("Summary:"):]
    g = lambda pat: float(re.search(pat, s).group(1))
    return {"integrated_lufs": g(r"I:\s+(-?[\d.]+) LUFS"), "loudness_range_lu": g(r"LRA:\s+(-?[\d.]+) LU"),
            "true_peak_dbtp": g(r"Peak:\s+(-?[\d.]+) dBFS")}


def duration(ffprobe: str, path: Path) -> float:
    return float(sh([ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)]).strip())


def limiter_touch(ffmpeg: str, src: Path, pre: str, gain_db: float, ceiling_db: float) -> dict:
    """How much of the gained, oversampled signal lies above the ceiling before limiting."""
    raw = subprocess.run([ffmpeg, "-v", "error", "-i", str(src), "-af",
                          f"{pre},volume={gain_db}dB,aresample={OVERSAMPLE}", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.abs(np.frombuffer(raw, dtype=np.float32))
    over = x > 10 ** (ceiling_db / 20)
    edges = np.diff(np.concatenate(([0], over.astype(np.int8), [0])))
    return {"samples_over_ceiling": int(over.sum()), "ms_over_ceiling": round(float(over.sum()) / OVERSAMPLE * 1000, 2),
            "peak_runs": int((edges == 1).sum()), "max_dbfs_before_limiting": round(float(20 * np.log10(max(x.max(), 1e-9))), 2)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--target-lufs", type=float, default=-18.0)
    ap.add_argument("--true-peak", type=float, default=-1.0)
    ap.add_argument("--highpass", type=float, default=60.0)
    ap.add_argument("--bitrate", default="64k")
    ap.add_argument("--sample-rate", type=int, default=44100)
    ap.add_argument("--tolerance", type=float, default=0.5, help="LU tolerance on the encoded file")
    ap.add_argument("--report", type=Path)
    ap.add_argument("--title"); ap.add_argument("--artist"); ap.add_argument("--comment")
    ap.add_argument("--ffmpeg", default="/opt/homebrew/bin/ffmpeg")
    args = ap.parse_args()
    ffprobe = str(Path(args.ffmpeg).with_name("ffprobe"))

    channels = int(sh([ffprobe, "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=channels",
                       "-of", "default=nw=1:nk=1", str(args.source)]).strip())
    downmix = "pan=mono|c0=0.5*c0+0.5*c1" if channels == 2 else "pan=mono|c0=c0"
    pre = f"{downmix},highpass=f={args.highpass}"

    m = loudnorm_measure(args.ffmpeg, args.source, pre, args.target_lufs, args.true_peak)
    gain_db = round(args.target_lufs - float(m["input_i"]), 2)
    touch = limiter_touch(args.ffmpeg, args.source, pre, gain_db, args.true_peak)
    limit_lin = 10 ** (args.true_peak / 20)
    chain = (f"{pre},volume={gain_db}dB,aresample={OVERSAMPLE},"
             f"alimiter=limit={limit_lin:.6f}:attack=5:release=50:level=false,aresample={args.sample_rate}")
    meta = []
    for k in ("title", "artist", "comment"):
        if getattr(args, k):
            meta += ["-metadata", f"{k}={getattr(args, k)}"]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    sh([args.ffmpeg, "-hide_banner", "-nostats", "-y", "-i", str(args.source), "-af", chain,
        "-c:a", "libmp3lame", "-b:a", args.bitrate, "-write_xing", "1", "-id3v2_version", "3", *meta, str(args.out)])

    out_m = ebur128(args.ffmpeg, args.out)
    d_src, d_out = duration(ffprobe, args.source), duration(ffprobe, args.out)
    checks = {
        "loudness_within_tolerance": abs(out_m["integrated_lufs"] - args.target_lufs) <= args.tolerance,
        "true_peak_under_ceiling": out_m["true_peak_dbtp"] <= args.true_peak + 0.3,
        "duration_unchanged_50ms": abs(d_out - d_src) <= 0.05,
    }
    report = {
        "source": str(args.source), "out": str(args.out), "source_channels": channels,
        "pass1_loudnorm_measurement": m,
        "linear_gain_db": gain_db, "limiter": {"ceiling_dbtp": args.true_peak, "oversample_hz": OVERSAMPLE, **touch},
        "filter_chain": chain, "encoder": f"libmp3lame CBR {args.bitrate}, Xing/Info header",
        "encoded": {**out_m, "duration_s": d_out, "source_duration_s": d_src, "delta_ms": round((d_out - d_src) * 1000, 1)},
        "checks": checks,
    }
    text = json.dumps(report, indent=2)
    if args.report:
        args.report.write_text(text + "\n")
    print(text)
    if not all(checks.values()):
        print("FAILED checks", [k for k, v in checks.items() if not v], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
