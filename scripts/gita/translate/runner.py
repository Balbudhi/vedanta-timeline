#!/usr/bin/env python3
"""One model call, through Codex or Claude: the only place that knows how a model is invoked
(docs/GITA_FULL_TRANSLATION_PLAN.md §3; scripts/gita/translate/README.md "Runners").

    run(text, cwd, files=None, sandbox="read-only", log=None) -> Result(raw, usage, seconds, commands)

GITA_RUNNER selects the backend:
  codex   `codex exec` (GITA_MODEL, default gpt-6-astra; GITA_EFFORT, default high; CODEX_HOME from
          GITA_CODEX_HOME, default ~/.codex-gita). Runs in `cwd` with the given sandbox; the model may read
          the files there.
  claude  `claude -p` (GITA_CLAUDE_MODEL, default claude-opus-5-5; GITA_EFFORT) with every tool disabled,
          no MCP servers, no hooks, no saved session. The model cannot read files, so `files` are inlined
          after the prompt, each under its own name.
Both are tool-free for every current stage; a backend failure (no output, non-zero exit) is returned
as an empty `raw` with the error in `usage["error"]`, never as an answer.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

RUNNER = os.environ.get("GITA_RUNNER", "codex")
MODEL = os.environ.get("GITA_MODEL", "gpt-6-astra")
CLAUDE_MODEL = os.environ.get("GITA_CLAUDE_MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("GITA_EFFORT", "high")
CODEX_HOME = os.environ.get("GITA_CODEX_HOME", str(Path.home() / ".codex-gita"))


@dataclass
class Result:
    raw: str
    usage: dict = field(default_factory=dict)
    seconds: float = 0.0
    commands: int = 0


def model_name() -> str:
    return CLAUDE_MODEL if RUNNER == "claude" else MODEL


def run(text: str, cwd: Path, files: dict[str, Path] | None = None, sandbox: str = "read-only",
        log: Path | None = None, env: dict | None = None) -> Result:
    if RUNNER == "claude":
        return _claude(text, files or {}, log)
    if RUNNER == "codex":
        return _codex(text, Path(cwd), sandbox, log, env or {})
    raise SystemExit(f"GITA_RUNNER must be codex or claude, not {RUNNER!r}")


def _codex(text: str, cwd: Path, sandbox: str, log: Path | None, env: dict) -> Result:
    t = time.time()
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "out.txt"
        r = subprocess.run(["codex", "exec", "--skip-git-repo-check", "-s", sandbox, "-C", str(cwd), "-m", MODEL,
                            "-c", f"model_reasoning_effort={EFFORT}", "-c", "project_doc_max_bytes=0", "--json",
                            "-o", str(out), text], stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           env={**os.environ, **env, "CODEX_HOME": CODEX_HOME})
        raw = out.read_text(encoding="utf-8") if out.exists() else ""
    if log:
        log.write_text(r.stdout + r.stderr, encoding="utf-8")
    usage = [json.loads(l).get("usage") or {} for l in r.stdout.splitlines() if '"turn.completed"' in l]
    u = {"input_tokens": sum(x.get("input_tokens", 0) for x in usage),
         "output_tokens": sum(x.get("output_tokens", 0) for x in usage)}
    if not raw:
        u["error"] = f"codex exit {r.returncode}: {r.stderr[-300:]}"
    cmds = sum(1 for l in r.stdout.splitlines() if '"command_execution"' in l and '"item.started"' in l)
    return Result(raw, u, round(time.time() - t, 1), cmds)


def _claude(text: str, files: dict[str, Path], log: Path | None) -> Result:
    t = time.time()
    for name, p in files.items():
        if Path(p).exists():
            text += f"\n\n==== FILE {name} ====\n" + Path(p).read_text(encoding="utf-8")
    text += "\n\n(The files named above are given inline; you have no tools.)" if files else ""
    with tempfile.TemporaryDirectory() as d:  # outside any repository: no project instructions are loaded
        r = subprocess.run(["claude", "-p", "--bare", "--tools", "", "--strict-mcp-config", "--no-session-persistence",
                            "--output-format", "json", "--model", CLAUDE_MODEL, "--effort", EFFORT],
                           input=text, capture_output=True, text=True, cwd=d)
    if log:
        log.write_text(r.stdout + r.stderr, encoding="utf-8")
    try:
        j = json.loads(r.stdout)
    except json.JSONDecodeError:
        return Result("", {"error": f"claude exit {r.returncode}: {(r.stderr or r.stdout)[-300:]}"}, round(time.time() - t, 1))
    u = j.get("usage") or {}
    usage = {"input_tokens": u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
             + u.get("cache_creation_input_tokens", 0), "output_tokens": u.get("output_tokens", 0)}
    if j.get("is_error"):
        usage["error"] = str(j.get("result"))[:300]
        return Result("", usage, round(time.time() - t, 1))
    return Result(j.get("result") or "", usage, round(time.time() - t, 1))
