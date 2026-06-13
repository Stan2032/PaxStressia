"""History-calibration harness (DESIGN.md §12, §19.7 — the v0.5 instrument).

Runs a passive-player battery on Scenario 1 and scores it against the
historical record of the Sahel arc, 2012–2026 (turn 0 = 2012-01):

  - ML collapses to a junta in the coup-cascade window (~2020 ± slack)
  - cascade order: ML before BF before NE
  - a proto-bloc is detected by the end (the AES, Sept 2023 ≈ turn 140)
  - insurgent reach expands (≥2× total strength) and is STILL growing in the
    final two years — the ICG finding: the juntas don't solve the problem

Usage:
  python3 harness/calibrate.py --runs 10 --out artifacts-calibration
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim import Engine, PassivePolicy, load_rules  # noqa: E402

TARGETS = {
    "ml_window": (60, 140),     # 2017-01 .. 2023-09 — generous around the 2020/21 coups
    "ml_outcome": "junta",
    "bloc_by": 168,
    "expansion_min": 2.0,
    "still_growing_tail": 24,   # final two years
}


def run_one(seed: int, turns: int) -> dict:
    rules = load_rules(scenario="sahel_arc")
    eng = Engine(rules=rules, seed=seed, policy=PassivePolicy())
    start_strength = sum(
        p.strength for n in eng.world.nodes_sorted() for p in n.presence.values()
    )
    strength_series = []
    for _ in range(turns):
        eng.run_turn()
        strength_series.append(round(sum(
            p.strength for n in eng.world.nodes_sorted() for p in n.presence.values()
        ), 1))
    collapses = {}
    for report in eng.reports:
        for entry in report["log"]:
            if entry.get("event") == "state_collapse":
                collapses[entry["country"]] = {
                    "turn": entry["turn"], "outcome": entry["outcome"],
                }
    bloc_turn = None
    for report in eng.reports:
        for entry in report["log"]:
            if entry.get("event") == "proto_bloc_detected" and bloc_turn is None:
                bloc_turn = entry["turn"]
    tail = TARGETS["still_growing_tail"]
    return {
        "seed": seed,
        "collapses": collapses,
        "bloc_turn": bloc_turn,
        "expansion": round(strength_series[-1] / max(1.0, start_strength), 2),
        "still_growing": strength_series[-1] > strength_series[-tail - 1],
        "final_strength": strength_series[-1],
        "score": eng.score(),
    }


def grade(result: dict) -> dict:
    ml = result["collapses"].get("ML")
    lo, hi = TARGETS["ml_window"]
    checks = {
        "ml_junta_in_window": bool(
            ml and ml["outcome"] == TARGETS["ml_outcome"] and lo <= ml["turn"] <= hi
        ),
        "cascade_order": _cascade_ordered(result["collapses"]),
        "bloc_detected": result["bloc_turn"] is not None
        and result["bloc_turn"] <= TARGETS["bloc_by"],
        "expansion": result["expansion"] >= TARGETS["expansion_min"],
        "still_growing": result["still_growing"],
    }
    checks["passed"] = sum(checks.values())
    return checks


def _cascade_ordered(collapses: dict) -> bool:
    """ML before BF before NE, for those that fell (ML must fall)."""
    if "ML" not in collapses:
        return False
    t_ml = collapses["ML"]["turn"]
    t_bf = collapses.get("BF", {}).get("turn")
    t_ne = collapses.get("NE", {}).get("turn")
    if t_bf is not None and t_bf < t_ml:
        return False
    if t_ne is not None and t_bf is not None and t_ne < t_bf:
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--turns", type=int, default=168)
    parser.add_argument("--seed-base", type=int, default=0)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    results = []
    for i in range(args.runs):
        result = run_one(args.seed_base + i, args.turns)
        result["grade"] = grade(result)
        results.append(result)
        ml = result["collapses"].get("ML")
        bf = result["collapses"].get("BF")
        ne = result["collapses"].get("NE")

        def fmt(c):
            return f"{c['outcome']}@{c['turn']}" if c else "stands"

        print(
            f"seed {result['seed']:>3}  ML {fmt(ml):>12}  BF {fmt(bf):>12}  "
            f"NE {fmt(ne):>12}  bloc@{result['bloc_turn']}  "
            f"x{result['expansion']}  grade {result['grade']['passed']}/5"
        )

    summary = {
        check: sum(1 for r in results if r["grade"][check])
        for check in ("ml_junta_in_window", "cascade_order", "bloc_detected",
                      "expansion", "still_growing")
    }
    summary["runs"] = args.runs
    print("\ncalibration summary:", json.dumps(summary))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        with open(args.out / "calibration.json", "w", encoding="utf-8") as fh:
            json.dump({"targets": TARGETS, "summary": summary, "results": results},
                      fh, indent=1)
        print(f"wrote {args.out / 'calibration.json'}")


if __name__ == "__main__":
    main()
