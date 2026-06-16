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

from . import blocs as blocs_mod
from . import coalition as coalition_mod
from . import commands as commands_mod
from . import events as events_mod
from . import factions as factions_mod
from . import markets as markets_mod
from . import norms as norms_mod
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
        scenario: str | None = None,
    ) -> None:
        self.rules = rules if rules is not None else load_rules(rules_dir, scenario=scenario)
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
        # gate world-scale-only initiatives (Regional Commands §21.7, Coalition
        # §21.8) out of single-theatre play, where they are inert — no dead
        # options offered.
        gated_off = set()
        if not commands_mod.enabled(self.consts):
            gated_off.add("command")
        if not coalition_mod.enabled(self.consts):
            gated_off.add("coalition")
        return {
            "initiatives": [
                self.initiatives[k] for k in sorted(self.initiatives)
                if not any(e["op"] in gated_off for e in self.initiatives[k]["effects"])
            ],
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
        elif op == "presence":
            from .world import Presence

            node = world.nodes[node_id]
            pres = node.presence.get(op_dict["faction"])
            if pres is None:
                pres = node.presence[op_dict["faction"]] = Presence(visibility=30.0)
                log.append({"event": "presence_seeded", "faction": op_dict["faction"],
                            "node": node_id, "source": source})
            pres.strength = clamp(pres.strength + op_dict.get("strength", 0.0))
            pres.entrenchment = clamp(pres.entrenchment + op_dict.get("entrenchment", 0.0))
        elif op == "patron":
            node = world.nodes[node_id]
            pid = op_dict["patron"]
            node.patron_influence[pid] = clamp(
                node.patron_influence.get(pid, 0.0) + op_dict["delta"]
            )
        elif op == "suppress_clock":
            # Transparency Dial (§6): the player chose to bury an incident with
            # their fingerprints. No cost now; a leak clock starts (resolved in
            # the consequence phase). In a free press, the truth tends to out.
            world.player.suppress_clocks.append(
                {"severity": op_dict["severity"], "age": 0, "source": source,
                 "node": node_id}
            )
            log.append({"event": "suppressed", "source": source, "severity": op_dict["severity"]})
        elif op == "exposure":
            # §20: fund documentation of a regime. Node target → that country;
            # global → every regime out of civilian rule.
            targets = (
                [world.nodes[node_id].country] if node_id
                else [c for c in world.countries()
                      if (cap := world.capital_of(c)) is not None
                      and cap.government != "civilian"]
            )
            for country in targets:
                world.exposure[country] = clamp(
                    world.exposure.get(country, 0.0) + op_dict["delta"]
                )
            if targets:
                log.append({"event": "exposure", "countries": targets, "source": source})
        elif op == "command":
            # §21.7: stand up a standing Regional Command over the target node's
            # theatre (grand-mode, capped, gated). Itemised in the turn log.
            theater = world.nodes[node_id].theater if node_id else None
            if commands_mod.establish(world, self.consts, theater):
                log.append({"event": "command_established", "theater": theater,
                            "node": node_id, "source": source})
        elif op == "coalition":
            # §21.8: rally partners toward their fair share — raises coalition
            # cohesion (which then shares Regional-Command upkeep). Gated.
            before = world.coalition
            coalition_mod.rally(world, self.consts)
            if world.coalition != before:
                log.append({"event": "coalition_rallied", "cohesion": round(world.coalition, 1),
                            "source": source})
        elif op == "designate":
            self._designate(node_id, source, log)
        elif op == "negotiate":
            self._negotiate(node_id, source, log)
        else:
            raise ValueError(f"unknown op: {op}")

    def _designate(self, node_id: str | None, source: str, log: list) -> None:
        """Targeted-sanctions op (§20.4): spend Exposure to bite a regime. A thin
        case (low Exposure) is dismissed and costs a little credibility."""
        world, consts = self.world, self.consts
        country = world.nodes[node_id].country if node_id else None
        if country is None:
            return
        if world.exposure.get(country, 0.0) >= consts["sanctions_exposure_min"]:
            world.exposure[country] -= consts["sanctions_exposure_cost"]
            self.ledger.apply(world, INTERNATIONAL, source, consts["sanctions_intl"])
            patron = patrons_mod.dominant_patron(world, country)
            for node in world.country_nodes(country):
                node.patron_influence[patron] = max(
                    0.0, node.patron_influence.get(patron, 0.0) - consts["sanctions_patron"]
                )
            # deny the patron one state and it is weaker in all of them (§8, grand)
            if patron in world.patron_strength:
                world.patron_strength[patron] = max(
                    0.0, world.patron_strength[patron] - consts["sanctions_patron_global"]
                )
            for bloc in world.blocs:
                if country in bloc["countries"]:
                    bloc["stage"] = max(1.0, bloc["stage"] - consts["sanctions_bloc_slow"])
            log.append({"event": "designation", "country": country, "patron": patron,
                        "source": source})
        else:
            self.ledger.apply(world, INTERNATIONAL, f"{source}:thin_case", -1.0)
            log.append({"event": "designation_failed", "country": country, "source": source})

    def _negotiate(self, node_id: str | None, source: str, log: list) -> None:
        """Negotiation endgame (§7): settle a *stalemated* faction. Outside the
        stalemate band, talks fail and cost a little at home."""
        world, consts = self.world, self.consts
        if node_id is None:
            return
        node = world.nodes[node_id]
        target = max(
            sorted(node.presence), key=lambda f: node.presence[f].strength, default=None
        )
        if target is None:
            return
        pres = node.presence[target]
        if consts["negotiate_min"] <= pres.strength <= consts["negotiate_max"]:
            pres.strength = clamp(pres.strength - consts["negotiate_strength_drain"])
            pres.entrenchment = clamp(pres.entrenchment - consts["negotiate_strength_drain"] / 2.0)
            self.ledger.apply(world, DOMESTIC, source, -consts["negotiate_domestic_cost"])
            self.ledger.apply(world, INTERNATIONAL, source, consts["negotiate_international_gain"])
            log.append({"event": "negotiated", "node": node_id, "faction": target,
                        "source": source})
        else:
            self.ledger.apply(world, DOMESTIC, f"{source}:talks_failed", -1.0)
            log.append({"event": "negotiate_failed", "node": node_id, "source": source})

    def _process_suppress_clocks(self, log: list) -> None:
        """Consequence-phase substep (§6, §18.5). Each buried scandal rolls to
        leak; press freedom raises the odds and age compounds them. A leak costs
        a multiple of honest disclosure, spread across all three gauges; survive
        long enough and it's buried for good."""
        world, consts = self.world, self.consts
        survivors = []
        for clock in world.player.suppress_clocks:
            leak_p = (
                (consts["leak_base"] + consts["leak_age_factor"] * clock["age"])
                * consts["press_freedom"]
            )
            if self.rng.random() < leak_p:
                sev = clock["severity"] * consts["leak_multiplier"]
                src = f"leak:{clock['source']}"
                self.ledger.apply(world, DOMESTIC, src, -sev)
                self.ledger.apply(world, INTERNATIONAL, src, -sev * 0.7)
                if clock["node"] is not None and clock["node"] in world.nodes:
                    self.ledger.apply(world, local_gauge(clock["node"]), src, -sev * 0.5)
                log.append({"event": "leak", "source": clock["source"],
                            "age": clock["age"], "cost": round(sev, 2)})
            elif clock["age"] + 1 >= consts["leak_clock_turns"]:
                log.append({"event": "buried_safely", "source": clock["source"]})
            else:
                clock["age"] += 1
                survivors.append(clock)
        world.player.suppress_clocks = survivors

    # ------------------------------------------------------------------ the loop

    def run_turn(self) -> dict:
        world, consts, player = self.world, self.consts, self.world.player
        turn_log: list[dict] = []
        fired_events: list[dict] = []
        casualties_before = player.casualties
        drift_before = player.authoritarian_drift

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
            "commands": sorted(world.commands),  # your own standing posture (§21.7), public
            "coalition": round(world.coalition, 2),  # burden-sharing cohesion (§21.8), public
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
        # c) faction growth, itemized — scaled by the global precedent + arms market (§21)
        recruit_mult = norms_mod.recruit_multiplier(world, consts)
        arms_mult = markets_mod.arms_mult(world, consts)
        growth_log, attrition_dealt = factions_mod.apply_growth(
            world, consts, amnesty_rates, recruit_mult, arms_mult
        )
        # c2) spread over edges (v0.4)
        turn_log += factions_mod.apply_spread(world, consts)
        # d) entrenchment conversion + visibility
        factions_mod.entrench_and_visibility(world, consts)
        # e) faction networking
        turn_log += factions_mod.networking_check(world, consts, attrition_dealt)
        # e2) standing Regional Commands contain their theatres (§21.7, grand) —
        # before collapse, so a buffered capital can be held; bleeds the home front.
        commands_mod.apply(world, consts, self.ledger, turn_log)
        # f) state-capture collapse rolls
        turn_log += factions_mod.collapse_rolls(world, consts, self.rng, self.ledger)
        # f2) bloc formation + consolidation clock (§5.4)
        turn_log += blocs_mod.update_blocs(world, consts, self.ledger)
        # g) patron allegiance market (multi-patron in grand) + markets + exposure decay
        turn_log += patrons_mod.market(world, consts, self.rules.get("patrons", []))
        markets_mod.update_markets(world, consts)
        patrons_mod.decay_exposure(world, consts)
        # h) event draw
        card = events_mod.draw(world, consts, self.rng, self.deck)
        if card is not None:
            idx = min(self.policy.choose_event(card), len(card["choices"]) - 1)
            choice = card["choices"][idx]
            ctx = events_mod.context_node(world)
            for eff in choice["effects"]:
                self._apply_op(eff, eff.get("node", ctx), f"event:{card['id']}", turn_log)
            world.fired_events.add(card["id"])
            fired_events.append({"id": card["id"], "choice": choice["label"], "node": ctx})

        # i) global norms: this turn's choices set a worldwide precedent (§21)
        norms_mod.update_norms(
            world, consts, executed, self.initiatives,
            player.authoritarian_drift - drift_before,
        )

        # Phase 4 — Consequence
        norms_mod.apply_feedback(world, consts, self.ledger)
        markets_mod.apply_feedback(world, consts, self.ledger)
        coalition_mod.decay(world, consts)  # partners free-ride back unless rallied (§21.8)
        new_casualties = player.casualties - casualties_before
        if new_casualties:
            self.ledger.apply(
                world, DOMESTIC, "casualties",
                -consts["domestic_hit_per_casualty"] * new_casualties,
            )
        self._process_suppress_clocks(turn_log)
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

        def grip(n) -> float:
            # insurgent shadow-control of a region (Pillar 4): a region painted
            # with services but run by an entrenched insurgency is NOT stabilized.
            if not n.presence:
                return 0.0
            return clamp(
                max((0.5 * p.strength + 0.5 * p.entrenchment) for p in n.presence.values()),
                0.0, 100.0,
            ) / 100.0

        if consts.get("grand_scoring", 0) > 0:
            # Grand mode (§21.5): a world police can't stabilise 40 theatres at
            # once, so it is judged on CONTAINMENT, not omnipotence — scale-
            # invariant by construction. (a) population-weighted QUALITY, so
            # protecting a consequential state counts for more than a micro-
            # state; (b) the FREE fraction of the world's capitals (1 − junta
            # share); blended, then dragged down by consolidated authoritarian
            # blocs (the §5.4 loss condition). order_mult is folded in here.
            def wt(n):
                return max(1.0, n.population_k) ** 0.5
            wsum = sum(wt(n) for n in nodes) or 1.0
            quality = 100.0 * sum(
                wt(n) * (n.local_legitimacy / 100.0) * (n.governance / 100.0) * (1.0 - grip(n))
                for n in nodes
            ) / wsum
            n_c = max(1, len(world.countries()))
            free_frac = 1.0 - world.junta_count() / n_c
            bloc_pen = 1.0 / (
                1.0
                + consts["order_bloc_weight_grand"]
                * blocs_mod.bloc_containment_term(world, consts)
                / consts["grand_bloc_ref"]
            )
            fw = consts["grand_free_weight"]
            stabilization = (fw * 100.0 * free_frac + (1.0 - fw) * quality) * bloc_pen
            order_mult = 1.0
        else:
            stabilization = 100.0 * sum(
                (n.local_legitimacy / 100.0) * (n.governance / 100.0) * (1.0 - grip(n))
                for n in nodes
            ) / len(nodes)
            order_mult = 1.0 / (
                1.0
                + consts["order_junta_weight"] * world.junta_count()
                + consts["order_bloc_weight"] * blocs_mod.bloc_containment_term(world, consts)
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

    # ------------------------------------------------------------------ endings

    def ending(self) -> dict:
        """The §11 endings matrix on two axes: ABROAD (did you hold the line —
        Stabilization × OrderMultiplier, so juntas/blocs count against you) and
        HOME (did you stay clean — the IntegrityMultiplier). Thresholds are
        data-driven (`pax_abroad_min`, `integrity_clean_min`)."""
        s = self.score()
        abroad_ok = s["stabilization"] * s["order_mult"] >= self.consts["pax_abroad_min"]
        home_ok = s["integrity_mult"] >= self.consts["integrity_clean_min"]
        if abroad_ok and home_ok:
            name, text = "Pax", (
                "Stabilized abroad, intact at home, allies still answer the phone. "
                "The hard ending — and you found it."
            )
        elif abroad_ok and not home_ok:
            name, text = "Fortress", (
                "You kept the peace and lost the thing it was for. The republic still "
                "stands; ask it what it has become."
            )
        elif not abroad_ok and home_ok:
            name, text = "Retreat", (
                "Clean hands, burning world. The blocs write the next chapter; your "
                "conscience writes the footnotes."
            )
        else:
            name, text = "Collapse", (
                "Quagmire abroad, exhaustion at home. The terms are set elsewhere now."
            )
        return {"name": name, "text": text,
                "abroad": round(s["stabilization"] * s["order_mult"], 4),
                "home": s["integrity_mult"], "score": s}

    def post_mortem(self) -> dict:
        """The signature learning loop (§9): at run's end, surface where the fog
        hid the most — the regions whose true insurgent strength most exceeded
        what your last briefing believed. Deceptive calm, revealed."""
        est = briefing_estimates(self.world, self.consts, random.Random(self.seed))
        gaps = []
        for nid in sorted(self.world.nodes):
            node = self.world.nodes[nid]
            true_total = sum(p.strength for p in node.presence.values())
            believed_total = sum(f["strength_est"] for f in est[nid]["factions"].values())
            if true_total > 0:
                gaps.append({
                    "node": nid,
                    "true": round(true_total, 1),
                    "believed": round(believed_total, 1),
                    "gap": round(true_total - believed_total, 1),
                })
        gaps.sort(key=lambda g: g["gap"], reverse=True)
        return {"worst_fog_gaps": gaps[:5], "turns": len(self.reports)}

    # ------------------------------------------------------------------ determinism

    def checkpoint(self) -> str:
        """Canonical JSON of the true world state (§18.1)."""
        return json.dumps(self.world.to_dict(), sort_keys=True, separators=(",", ":"))

    def state_hash(self) -> str:
        return hashlib.sha256(self.checkpoint().encode("utf-8")).hexdigest()
