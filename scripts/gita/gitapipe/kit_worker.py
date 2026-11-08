"""JSON-lines server for the grammar oracle, run under the Vidyut venv (prakriya
tmp/vidyut-venv/bin/python -I). One request per line: {"op": "analyze"|"derive"|"split",
"args": [...]}; one reply per line: {"ok": result} or {"error": "..."}. The engine is loaded
once per process. Standalone: imports nothing from the pipeline."""
import importlib.util
import json
import sys
from pathlib import Path

KIT = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("gita_kit_grammar", KIT / "grammar.py")
grammar = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(KIT))
spec.loader.exec_module(grammar)
out = sys.stdout
sys.stdout = sys.stderr          # anything the oracle prints must not corrupt the protocol
out.write(json.dumps({"ready": True, "path": str(KIT / "grammar.py")}) + "\n")
out.flush()
for line in sys.stdin:
    try:
        req = json.loads(line)
        res = getattr(grammar, req["op"])(*req.get("args", []))
        out.write(json.dumps({"ok": res}, ensure_ascii=False, default=str) + "\n")
    except Exception as e:  # noqa: BLE001 - every failure is reported to the caller
        out.write(json.dumps({"error": f"{type(e).__name__}: {e}"}) + "\n")
    out.flush()
