"""Monte Carlo balance harness (DESIGN.md §13.3 Phase 1).

Runs N seeded headless games under a named policy and writes:
  - runs.json      per-run final scores + per-turn gauge/strength series
  - balance.png    trajectory plot + final-score strip (if matplotlib present)

Stdlib-only except the optional plot — degrades gracefully in bare Termux.

Usage:
  python harness/run.py --runs 10 --turns 60 --policy passive --out artifacts
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim import POLICIES, Engine  # noqa: E402


def run_one(seed: int, turns: int, policy_name: str) -> dict:
    eng = Engine(seed=seed, policy=POLICIES[policy_name]())
    series = {"domestic": [], "international": [], "local_avg": [], "insurgent_strength": []}
    for _ in range(turns):
        eng.run_turn()
        world = eng.world
        series["domestic"].append(round(world.player.domestic, 2))
        series["international"].append(round(world.player.international, 2))
        series["local_avg"].append(
            round(sum(n.local_legitimacy for n in world.nodes_sorted()) / len(world.nodes), 2)
        )
        series["insurgent_strength"].append(
            round(sum(p.strength for n in world.nodes_sorted() for p in n.presence.values()), 2)
        )
    collapses = [
        entry for report in eng.reports for entry in report["log"]
        if entry.get("event") == "state_collapse"
    ]
    return {"seed": seed, "score": eng.score(), "collapses": collapses, "series": series}


def maybe_plot(results: list[dict], config: dict, out_dir: Path) -> bool:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    turns = range(1, config["turns"] + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    colors = {"domestic": "tab:blue", "international": "tab:green",
              "local_avg": "tab:orange", "insurgent_strength": "tab:red"}
    for key, color in colors.items():
        rows = [r["series"][key] for r in results]
        mean = [sum(col) / len(col) for col in zip(*rows)]
        lo = [min(col) for col in zip(*rows)]
        hi = [max(col) for col in zip(*rows)]
        ax1.plot(turns, mean, label=key, color=color)
        ax1.fill_between(turns, lo, hi, color=color, alpha=0.15)
    ax1.set_title(f"{config['policy']} × {config['runs']} runs — trajectories (mean, min–max)")
    ax1.set_xlabel("turn")
    ax1.legend(fontsize=8)
    finals = [r["score"]["final"] for r in results]
    ax2.plot([0] * len(finals), finals, "o", alpha=0.6)
    ax2.set_xticks([])
    ax2.set_title(f"final scores — mean {sum(finals) / len(finals):.1f}")
    fig.suptitle("MANDATE balance harness (v0.2 skeleton — constants uncalibrated)")
    fig.tight_layout()
    fig.savefig(out_dir / "balance.png", dpi=120)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--turns", type=int, default=60)
    parser.add_argument("--policy", choices=sorted(POLICIES), default="passive")
    parser.add_argument("--seed-base", type=int, default=0)
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    config = {"runs": args.runs, "turns": args.turns, "policy": args.policy,
              "seed_base": args.seed_base}
    results = [run_one(args.seed_base + i, args.turns, args.policy) for i in range(args.runs)]

    with open(args.out / "runs.json", "w", encoding="utf-8") as fh:
        json.dump({"config": config, "results": results}, fh, indent=1)

    finals = [r["score"]["final"] for r in results]
    juntas = sum(r["score"]["juntas"] for r in results)
    plotted = maybe_plot(results, config, args.out)
    print(
        f"{args.runs} runs × {args.turns} turns [{args.policy}] — "
        f"final score mean {sum(finals) / len(finals):.1f} "
        f"(min {min(finals):.1f}, max {max(finals):.1f}), juntas {juntas} — "
        f"wrote runs.json{' + balance.png' if plotted else ' (no matplotlib, plot skipped)'}"
    )


if __name__ == "__main__":
    main()
