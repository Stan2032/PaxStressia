"""Balance-audit harness (DESIGN.md §19.7 — the v0.24 instrument; companion to
calibrate.py). Where calibrate checks the passive WORLD against history, this
checks the PLAYER side: the score spread, the ending distribution, and the §19.4
forced-portfolio / §19.7 no-dominant-strategy discipline — and at BOTH the
120-turn subset the thesis suite tests and the arc's full 168-turn horizon.

It surfaced the v0.24 finding (diagnosed v0.25): balanced play tops the pures at
120 turns but not at 168. The mechanism, measured: capital collapse is driven by
insurgent strength / capital governance (factions.collapse_rolls), not grievance,
so keeping juntas low means keeping total strength low — and all-in development
aimed at the worst-GRIEVANCE regions starves recruitment best. Over a long run
that concentration wins, because development has no diminishing-returns / co-option
downside yet (Galula under-modelled). Report-only — it never fails CI; the xfail
thesis test is the gate.

Usage:
  python3 harness/audit.py --runs 8
"""

from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim import (  # noqa: E402
    CompetentPolicy,
    EmergencyPowersPolicy,
    Engine,
    MixedPolicy,
    PassivePolicy,
    PureHeartsMindsPolicy,
    PureKineticPolicy,
    load_rules,
)

POLICIES = [
    ("passive", PassivePolicy), ("kinetic", PureKineticPolicy),
    ("heartsmind", PureHeartsMindsPolicy), ("mixed", MixedPolicy),
    ("competent", CompetentPolicy), ("emergency", EmergencyPowersPolicy),
]
BALANCED = "competent"
PURES = {"kinetic", "heartsmind", "emergency"}


def audit(scenario: str, turns: int, runs: int) -> dict:
    rules = load_rules(scenario=scenario)
    rows, endings = {}, {}
    for name, P in POLICIES:
        finals = []
        for seed in range(runs):
            eng = Engine(rules=rules, seed=seed, policy=P())
            eng.run(turns)
            finals.append(eng.score()["final"])
            e = eng.ending()["name"]
            endings[e] = endings.get(e, 0) + 1
        rows[name] = statistics.mean(finals)
        print(f"  {name:11s} mean={statistics.mean(finals):6.1f}  "
              f"range=[{min(finals):6.1f}, {max(finals):6.1f}]")
    dominates = all(rows[BALANCED] > rows[p] for p in PURES)
    print(f"  endings: {dict(sorted(endings.items()))}")
    print(f"  §19.7 (balanced tops every pure): {'OK' if dominates else 'FAIL'}")
    return {"means": rows, "no_pure_dominates": dominates}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=8)
    args = ap.parse_args()
    holds = {}
    for turns in (120, 168):
        print(f"\n===== sahel_arc · {turns} turns · {args.runs} seeds =====")
        holds[turns] = audit("sahel_arc", turns, args.runs)["no_pure_dominates"]
    print(f"\nsummary: §19.7 holds @120={holds[120]}  @168={holds[168]} "
          f"(168 is the arc's real horizon; the v0.24 finding is the gap)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
