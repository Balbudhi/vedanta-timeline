#!/usr/bin/env python3
"""Every analysis of a pada form, or one analysis with its derivation, from the stage-A store.

    python3 scripts/gita/show_analysis.py FORM            # all readings (one line each), ranked as in the packet
    python3 scripts/gita/show_analysis.py --id ANALYSIS_ID   # the full Analysis and Derivation as JSON
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from gitapipe import common as C  # noqa: E402

C.fix_sys_path()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("form", nargs="?")
    ap.add_argument("--id")
    a = ap.parse_args(argv)
    from gitapipe.store import Store, summary
    st = Store()
    if a.id:
        got = st.get(a.id)
        if not got:
            print(f"unknown analysis id {a.id}")
            return 1
        print(json.dumps({"analysis": got[0], "derivation": got[1]}, ensure_ascii=False, indent=1))
        return 0
    if not a.form:
        ap.error("FORM or --id")
    rows = st.con.execute("select id from analyses where form=?", (C.form_key(a.form),)).fetchall()
    for (i,) in rows:
        print(json.dumps(summary(st.get(i)[0] | {"derivation": st.get(i)[1]}), ensure_ascii=False))
    print(f"{len(rows)} analyses of {a.form}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
