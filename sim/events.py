"""Deck-driven events (DESIGN.md §10, §18.3 substep h).

Cards are historically sourced data (rules/events.json), gated by `requires`
predicates over world state and drawn weight-proportionally. Every card is a
choice with a legitimacy-triangle trade; the policy picks (default: first
choice). Effects are applied through the engine's shared op applicator so the
ledger stays itemized.
"""

from __future__ import annotations

import random

from .world import WorldState


def _eligible(world: WorldState, card: dict) -> bool:
    req = card.get("requires", {})
    if "min_turn" in req and world.turn < req["min_turn"]:
        return False
    if "max_turn" in req and world.turn > req["max_turn"]:
        return False
    if "min_avg_grievance" in req and world.avg_grievance() < req["min_avg_grievance"]:
        return False
    if req.get("any_junta") and world.junta_count() == 0:
        return False
    if "min_coup_risk" in req:
        if max(world.coup_risk.values(), default=0.0) < req["min_coup_risk"]:
            return False
    if "min_partner_capacity" in req:
        best = max((n.partner_capacity for n in world.nodes_sorted()), default=0.0)
        if best < req["min_partner_capacity"]:
            return False
    if "min_casualties" in req and world.player.casualties < req["min_casualties"]:
        return False
    if "country_collapsed" in req and not world.collapsed.get(req["country_collapsed"]):
        return False
    if "country_not_collapsed" in req and world.collapsed.get(req["country_not_collapsed"]):
        return False
    if "min_collapsed" in req:
        if sum(1 for v in world.collapsed.values() if v) < req["min_collapsed"]:
            return False
    if "min_links" in req:
        pairs = sum(len(f.links) for f in world.factions_sorted()) // 2
        if pairs < req["min_links"]:
            return False
    if "requires_fired" in req and req["requires_fired"] not in world.fired_events:
        return False  # narrative chains (§20.2): a follow-up needs its setup to have fired
    return True


def context_node(world: WorldState) -> str:
    """Deterministic default target for node-scoped event effects: the node with
    the highest total insurgent strength (ties broken by id order)."""
    best_id, best_strength = None, -1.0
    for node in world.nodes_sorted():
        total = sum(p.strength for p in node.presence.values())
        if total > best_strength:
            best_id, best_strength = node.id, total
    return best_id if best_id is not None else world.nodes_sorted()[0].id


def draw(world: WorldState, consts: dict, rng: random.Random, deck: list[dict]) -> dict | None:
    """At most one event per turn; None on a quiet news cycle."""
    if rng.random() >= consts["event_chance"]:
        return None
    eligible = [
        c for c in deck
        if c["weight"] > 0 and _eligible(world, c)
        and not (c.get("once") and c["id"] in world.fired_events)
    ]
    if not eligible:
        return None
    weights = [c["weight"] for c in eligible]
    return rng.choices(eligible, weights=weights, k=1)[0]
