#!/usr/bin/env python3
"""Inject the rules/*.json snapshot into proto/index.html (single-file law).

The proto fetches ../rules/*.json live when served over http; the embedded
snapshot is the file:// fallback so the single file works standalone.
rules/ stays the only source of truth: this script writes the snapshot, and
`--check` (run in CI) fails if the embedded copy has drifted from rules/.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = Path(__file__).resolve().parent / "index.html"
RULE_FILES = ("nodes", "edges", "factions", "initiatives", "events", "constants")
# Presentation-only data bundled into the snapshot but not part of the sim rules.
EXTRA_FILES = ("sources",)
BLOCK = re.compile(
    r'(<script id="rules-snapshot" type="application/json">)(.*?)(</script>)', re.DOTALL
)


def snapshot() -> str:
    base = {}
    for name in RULE_FILES:
        with open(ROOT / "rules" / f"{name}.json", encoding="utf-8") as fh:
            base[name] = json.load(fh)
    for name in EXTRA_FILES:
        path = ROOT / "rules" / f"{name}.json"
        if path.exists():
            with open(path, encoding="utf-8") as fh:
                base[name] = json.load(fh)
    scenarios = {}
    scen_root = ROOT / "rules" / "scenarios"
    for sdir in sorted(p for p in scen_root.iterdir() if (p / "scenario.json").exists()):
        pack = {}
        for name in ("scenario", *RULE_FILES):
            path = sdir / f"{name}.json"
            if path.exists():
                with open(path, encoding="utf-8") as fh:
                    pack[name] = json.load(fh)
        scenarios[sdir.name] = pack
    return json.dumps({"base": base, "scenarios": scenarios},
                      sort_keys=True, separators=(",", ":"))


def main() -> int:
    check = "--check" in sys.argv
    html = HTML.read_text(encoding="utf-8")
    match = BLOCK.search(html)
    if match is None:
        print("proto/index.html: rules-snapshot block not found", file=sys.stderr)
        return 1
    fresh = snapshot()
    current = match.group(2).strip()
    if check:
        if current != fresh:
            print(
                "proto snapshot is stale — run `python3 proto/build.py` and commit",
                file=sys.stderr,
            )
            return 1
        print("proto snapshot matches rules/")
        return 0
    HTML.write_text(html[: match.start(2)] + "\n" + fresh + "\n" + html[match.end(2) :],
                    encoding="utf-8")
    print(f"injected snapshot ({len(fresh)} bytes) into {HTML.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
