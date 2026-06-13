"""Policies — the harness's hands (DESIGN.md §18.7).

A Policy sees the briefing (fog estimates, not truth) and returns orders.
The built-ins are named for the thesis tests they serve (§13.3):
PassivePolicy is the history-calibration baseline; the strategy archetypes
exist so the design's claims about them can be asserted in pytest.
"""

from __future__ import annotations

import random


class Policy:
    """Base: do nothing, accept the first choice of every event."""

    name = "base"

    def choose(self, briefing: dict, actions: dict) -> list[dict]:
        return []

    def choose_event(self, card: dict) -> int:
        return 0


class PassivePolicy(Policy):
    """The calibration baseline: an executive who never acts.
    Run against history — reality is the balance baseline (§12)."""

    name = "passive"


class _BudgetedPolicy(Policy):
    """Shared helper: greedily emit orders from a preference list while the
    briefing's mandate/treasury budgets last."""

    preferences: list[str] = []

    def _rank_nodes(self, briefing: dict) -> list[str]:
        raise NotImplementedError

    def choose(self, briefing: dict, actions: dict) -> list[dict]:
        budget_m = briefing["mandate"]
        budget_t = briefing["treasury"]
        initiatives = {i["id"]: i for i in actions["initiatives"]}
        targets = self._rank_nodes(briefing)
        orders: list[dict] = []
        node_cycle = 0
        for pref in self.preferences * 3:  # up to three passes while budget lasts
            init = initiatives.get(pref)
            if init is None:
                continue
            if init["mandate_cost"] > budget_m or init["treasury_cost"] > budget_t:
                continue
            node = None
            if init["target"] == "node":
                if not targets:
                    continue
                node = targets[node_cycle % len(targets)]
                node_cycle += 1
            orders.append({"initiative": pref, "node": node})
            budget_m -= init["mandate_cost"]
            budget_t -= init["treasury_cost"]
        return orders


class PureKineticPolicy(_BudgetedPolicy):
    """Military family only, aimed where the estimates look worst."""

    name = "pure_kinetic"
    preferences = ["presence_patrols", "drone_strike", "partnered_raids", "train_equip"]

    def _rank_nodes(self, briefing: dict) -> list[str]:
        def est_strength(item: tuple[str, dict]) -> float:
            return sum(f["strength_est"] for f in item[1]["factions"].values())

        ranked = sorted(briefing["estimates"].items(), key=est_strength, reverse=True)
        return [node_id for node_id, _ in ranked[:3]]


class PureHeartsMindsPolicy(_BudgetedPolicy):
    """Governance/development only, no security component — the design claims
    this loses to momentum, and the thesis test will hold it to that."""

    name = "pure_hearts_minds"
    preferences = ["development_program", "amnesty_reintegration"]

    def _rank_nodes(self, briefing: dict) -> list[str]:
        ranked = sorted(
            briefing["estimates"].items(), key=lambda kv: kv[1]["grievance"], reverse=True
        )
        return [node_id for node_id, _ in ranked[:3]]


class EmergencyPowersPolicy(PureKineticPolicy):
    """Kinetic plus every drift tier on offer: tempting, scored (§11)."""

    name = "emergency_powers"
    preferences = ["surveillance_expansion", *PureKineticPolicy.preferences]


class MixedPolicy(_BudgetedPolicy):
    """A doctrine portfolio — security with restraint, paired with governance
    and intel where grievance is worst. The §19.7 dominance baseline: if any
    *pure* archetype matches or beats this, Pillar 3 ('every tool cuts both
    ways; no dominant strategy') has sprung a leak, and CI says so."""

    name = "mixed"
    preferences = ["humint_network", "development_program", "presence_patrols",
                   "partnered_raids", "amnesty_reintegration", "un_mandate"]

    def _rank_nodes(self, briefing: dict) -> list[str]:
        # worst-grievance regions first — meet the recruitment pool where it fills
        ranked = sorted(
            briefing["estimates"].items(), key=lambda kv: kv[1]["grievance"], reverse=True
        )
        return [node_id for node_id, _ in ranked[:4]]


class RandomPolicy(Policy):
    """Seeded chaos for fuzzing. Owns its own RNG — player input is not
    world entropy, so the engine's determinism stream stays clean."""

    name = "random"

    def __init__(self, seed: int = 0) -> None:
        self.rng = random.Random(seed)

    def choose(self, briefing: dict, actions: dict) -> list[dict]:
        budget_m = briefing["mandate"]
        budget_t = briefing["treasury"]
        orders: list[dict] = []
        node_ids = sorted(briefing["estimates"])
        pool = sorted(actions["initiatives"], key=lambda i: i["id"])
        for _ in range(self.rng.randrange(0, 4)):
            init = self.rng.choice(pool)
            if init["mandate_cost"] > budget_m or init["treasury_cost"] > budget_t:
                continue
            node = self.rng.choice(node_ids) if init["target"] == "node" else None
            orders.append({"initiative": init["id"], "node": node})
            budget_m -= init["mandate_cost"]
            budget_t -= init["treasury_cost"]
        return orders

    def choose_event(self, card: dict) -> int:
        return self.rng.randrange(0, len(card["choices"]))


POLICIES = {
    cls.name: cls
    for cls in (PassivePolicy, PureKineticPolicy, PureHeartsMindsPolicy,
                EmergencyPowersPolicy, MixedPolicy)
}
