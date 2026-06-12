"""The turn engine: Briefing → Policy → Resolution → Consequence (DESIGN.md §3, §18.3).

Determinism law (§18.1): one seeded RNG, sorted iteration, canonical
serialization. Same rules + seed + policy ⇒ byte-identical checkpoints.
Every legitimacy movement is itemized through the Ledger (§18.6); the true
world state is snapshotted every turn (the post-mortem spine, §9).
"""

from __future__ import annotations

import hashlib
import json
import random

from . import events as events_mod
from . import factions as factions_mod
from . import patrons as patrons_mod
from .elections import election_tick, mandate_income
from .fog import briefing_estimates
from .legitimacy import DOMESTIC, INTERNATIONAL, Ledger, local_gauge
from .policies import PassivePolicy, Policy
from .world import build_world, clamp, load_rules

MILITARY = "military"


class Engine:
    def __init__(
        self,
        rules: dict | None = None,
        seed: int = 0,
        policy: Policy | None = None,
        rules_dir=None,
    ) -> None:
        self.rules = rules if rules is not None else load_rules(rules_dir)
        self.consts = self.rules["constants"]
        self.world = build_world(self.rules)
        self.seed = seed
        self.rng = random.Random(seed)
        self.policy = policy if policy is not None else PassivePolicy()
        self.ledger = Ledger()
        self.initiatives = {i["id"]: i for i in self.rules["initiatives"]}
        self.deck = self.rules["events"]
        self.active_effects: list[dict] = []
        self.history: list[dict] = []  # true snapshots, one per resolved turn
        self.reports: list[dict] = []

    # ------------------------------------------------------------------ helpers

    def date_str(self) -> str:
        year, month = (int(x) for x in self.consts["start_date"].split("-"))
        total = (month - 1) + self.world.turn
        return f"{year + total // 12}-{total % 12 + 1:02d}"

    def _legal_actions(self) -> dict:
        return {
            "initiatives": [self.initiatives[k] for k in sorted(self.initiatives)],
            "nodes": sorted(self.world.nodes),
        }

    def _refresh_actives(self) -> tuple[dict[str, float], float]:
        """Prune expired lingering effects and recompute the derived runtime
        fields (ops_pressure, intel coverage, amnesty rates, UN umbrella)."""
        world = self.world
        self.active_effects = [e for e in self.active_effects if e["expires"] > world.turn]
        for node in world.nodes_sorted():
            node.ops_pressure = 0.0
            node.intel_coverage = node.intel_base
        amnesty: dict[str, float] = {}
        umbrella = 0.0
        for eff in self.active_effects:
            op = eff["op"]
            if op == "ops_pressure":
                world.nodes[eff["node"]].ops_pressure += eff["params"]["amount"]
            elif op == "intel":
                delta = eff["params"]["delta"]
                targets = [eff["node"]] if eff["node"] else sorted(world.nodes)
                for nid in targets:
                    world.nodes[nid].intel_coverage += delta
            elif op == "amnesty":
                amnesty[eff["node"]] = amnesty.get(eff["node"], 0.0) + eff["params"]["rate"]
            elif op == "intl_umbrella":
                umbrella += eff["params"]["delta"]
        for node in world.nodes_sorted():
            node.intel_coverage = clamp(node.intel_coverage, 0.05, 0.95)
        return amnesty, umbrella

    def _apply_op(self, op_dict: dict, node_id: str | None, source: str, log: list) -> None:
        """The §18.4 op vocabulary, one entry point for initiatives and events."""
        world, op = self.world, op_dict["op"]
        if op in ("ops_pressure", "intel", "amnesty", "intl_umbrella"):
            self.active_effects.append(
                {
                    "op": op,
                    "params": {
                        k: v for k, v in op_dict.items() if k not in ("op", "turns", "node")
                    },
                    "node": node_id if op != "intl_umbrella" else None,
                    "source": source,
                    "expires": world.turn + op_dict.get("turns", 1),
                }
            )
        elif op == "attrit":
            node = world.nodes[node_id]
            target = max(
                sorted(node.presence), key=lambda f: node.presence[f].strength, default=None
            )
            if target is not None:
                pres = node.presence[target]
                pres.strength = clamp(pres.strength - op_dict["amount"])
                log.append(
                    {"event": "attrit", "node": node_id, "faction": target,
                     "amount": op_dict["amount"], "source": source}
                )
        elif op == "local_legitimacy":
            self.ledger.apply(world, local_gauge(node_id), source, op_dict["delta"])
        elif op == "domestic_legitimacy":
            self.ledger.apply(world, DOMESTIC, source, op_dict["delta"])
        elif op == "international_legitimacy":
            self.ledger.apply(world, INTERNATIONAL, source, op_dict["delta"])
        elif op in ("governance", "development", "grievance"):
            node = world.nodes[node_id]
            setattr(node, op, clamp(getattr(node, op) + op_dict["delta"]))
        elif op == "partner_capacity":
            node = world.nodes[node_id]
            node.partner_capacity = max(0.0, node.partner_capacity + op_dict["delta"])
        elif op == "coup_seed":
            country = world.nodes[node_id].country if node_id else max(
                world.coup_risk, key=lambda c: world.coup_risk[c]
            )
            world.coup_risk[country] += op_dict["delta"]
        elif op == "drift":
            world.player.authoritarian_drift += op_dict["tiers"]
        else:
            raise ValueError(f"unknown op: {op}")

    # ------------------------------------------------------------------ the loop

    def run_turn(self) -> dict:
        world, consts, player = self.world, self.consts, self.world.player
        turn_log: list[dict] = []
        fired_events: list[dict] = []
        casualties_before = player.casualties

        # Phase 1 — Briefing
        self._refresh_actives()
        income = mandate_income(world, consts)
        player.mandate += income
        player.treasury += consts["treasury_income"]
        estimates = briefing_estimates(world, consts, self.rng)
        briefing = {
            "turn": world.turn,
            "date": self.date_str(),
            "mandate": player.mandate,
            "treasury": player.treasury,
            "domestic": player.domestic,
            "international": player.international,
            "estimates": estimates,
            "headlines": self.reports[-1]["log"][-3:] if self.reports else [],
        }

        # Phase 2 — Policy
        executed: list[dict] = []
        for order in self.policy.choose(briefing, self._legal_actions()):
            init = self.initiatives.get(order.get("initiative"))
            node_id = order.get("node")
            if init is None:
                continue
            if init["target"] == "node" and node_id not in world.nodes:
                continue
            if init["mandate_cost"] > player.mandate or init["treasury_cost"] > player.treasury:
                continue
            player.mandate -= init["mandate_cost"]
            player.treasury -= init["treasury_cost"]
            player.spent_total += init["treasury_cost"]
            executed.append({"initiative": init["id"], "node": node_id})

        # Phase 3 — Resolution
        # a) initiative effects
        for order in executed:
            init = self.initiatives[order["initiative"]]
            for eff in init["effects"]:
                self._apply_op(eff, order["node"], init["id"], turn_log)
            risk = init.get("casualty_risk", 0.0)
            if init["family"] == MILITARY and risk > 0 and self.rng.random() < risk:
                player.casualties += 1
                turn_log.append(
                    {"event": "casualties", "initiative": init["id"], "node": order["node"]}
                )
        # b) backfire rolls
        for order in executed:
            init = self.initiatives[order["initiative"]]
            backfire = init["backfire"]
            if self.rng.random() < backfire["probability"]:
                for eff in backfire["effects"]:
                    self._apply_op(eff, order["node"], f"{init['id']}:backfire", turn_log)
                turn_log.append(
                    {"event": "backfire", "initiative": init["id"],
                     "channel": backfire["channel"], "node": order["node"]}
                )
        amnesty_rates, umbrella = self._refresh_actives()
        if umbrella > 0:
            self.ledger.apply(world, INTERNATIONAL, "un_umbrella", umbrella)
        # c) faction growth, itemized
        growth_log, attrition_dealt = factions_mod.apply_growth(world, consts, amnesty_rates)
        # d) entrenchment conversion + visibility
        factions_mod.entrench_and_visibility(world, consts)
        # e) faction networking
        turn_log += factions_mod.networking_check(world, consts, attrition_dealt)
        # f) state-capture collapse rolls
        turn_log += factions_mod.collapse_rolls(world, consts, self.rng, self.ledger)
        turn_log += factions_mod.detect_proto_blocs(world)
        # g) patron drift (stub)
        turn_log += patrons_mod.drift(world, consts)
        # h) event draw
        card = events_mod.draw(world, consts, self.rng, self.deck)
        if card is not None:
            idx = min(self.policy.choose_event(card), len(card["choices"]) - 1)
            choice = card["choices"][idx]
            ctx = events_mod.context_node(world)
            for eff in choice["effects"]:
                self._apply_op(eff, eff.get("node", ctx), f"event:{card['id']}", turn_log)
            fired_events.append({"id": card["id"], "choice": choice["label"], "node": ctx})

        # Phase 4 — Consequence
        new_casualties = player.casualties - casualties_before
        if new_casualties:
            self.ledger.apply(
                world, DOMESTIC, "casualties",
                -consts["domestic_hit_per_casualty"] * new_casualties,
            )
        election = election_tick(world, consts, self.rng, self.ledger)
        if election is not None:
            turn_log.append(election)
        report = {
            "turn": world.turn,
            "date": self.date_str(),
            "mandate_income": income,
            "orders": executed,
            "ledger": [e.to_dict() for e in self.ledger.entries_for_turn(world.turn)],
            "growth": growth_log,
            "events": fired_events,
            "log": turn_log,
            "gauges": {
                "domestic": round(player.domestic, 4),
                "international": round(player.international, 4),
                "local_avg": round(
                    sum(n.local_legitimacy for n in world.nodes_sorted()) / len(world.nodes), 4
                ),
            },
        }
        self.history.append(world.to_dict())
        self.reports.append(report)
        world.turn += 1
        return report

    def run(self, turns: int | None = None) -> list[dict]:
        n = turns if turns is not None else self.consts["horizon_turns"]
        for _ in range(n):
            self.run_turn()
        return self.reports

    # ------------------------------------------------------------------ scoring

    def score(self) -> dict:
        """Final Score = Stabilization × OrderMult × IntegrityMult − Costs (§11, §18.5)."""
        world, consts, player = self.world, self.consts, self.world.player
        nodes = world.nodes_sorted()
        stabilization = 100.0 * sum(
            (n.local_legitimacy / 100.0) * (n.governance / 100.0) for n in nodes
        ) / len(nodes)
        order_mult = 1.0 / (
            1.0
            + consts["order_junta_weight"] * world.junta_count()
            + consts["order_bloc_weight"] * len(world.proto_blocs)
        )
        integrity_mult = max(
            consts["integrity_floor"],
            1.0 - consts["drift_per_tier"] * player.authoritarian_drift,
        )
        costs = (
            player.casualties * consts["cost_per_casualty"]
            + player.spent_total * consts["cost_spend_norm"]
        )
        return {
            "stabilization": round(stabilization, 4),
            "order_mult": round(order_mult, 4),
            "integrity_mult": round(integrity_mult, 4),
            "costs": round(costs, 4),
            "authoritarian_drift": player.authoritarian_drift,
            "casualties": player.casualties,
            "juntas": world.junta_count(),
            "proto_blocs": len(world.proto_blocs),
            "final": round(stabilization * order_mult * integrity_mult - costs, 4),
        }

    # ------------------------------------------------------------------ determinism

    def checkpoint(self) -> str:
        """Canonical JSON of the true world state (§18.1)."""
        return json.dumps(self.world.to_dict(), sort_keys=True, separators=(",", ":"))

    def state_hash(self) -> str:
        return hashlib.sha256(self.checkpoint().encode("utf-8")).hexdigest()
