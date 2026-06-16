"""Global arms & oil markets (DESIGN.md §21, grand mode).

Two more channels through which a choice in one theater is felt in all of them:

  - ARMS: world conflict raises the arms market; a hot market means weapons flow
    more freely, lifting insurgent ExternalSupport (sponsor flow) in *every*
    theater — let a war run anywhere and it arms insurgencies everywhere.
  - OIL: instability in oil-producing nations raises the oil market; a high oil
    price drags the importer-democracy's economy (a Domestic hit) and enriches
    the petro-funded rival patrons.

Gated by `market_feedback` (0 in single-theater scenarios → markets never move,
the Sahel calibration is untouched by construction; >0 in grand mode).
Modeled on `sim/norms.py`.
"""

from __future__ import annotations

from .legitimacy import DOMESTIC, Ledger
from .world import WorldState, clamp


def _mean_node_strength(world: WorldState) -> float:
    nodes = world.nodes_sorted()
    if not nodes:
        return 0.0
    return sum(
        max((p.strength for p in n.presence.values()), default=0.0) for n in nodes
    ) / len(nodes)


def _oil_instability(world: WorldState) -> float | None:
    oil = [n for n in world.nodes_sorted() if "oil" in n.resources]
    if not oil:
        return None
    return sum(
        0.5 * (100.0 - n.governance)
        + 0.5 * max((p.strength for p in n.presence.values()), default=0.0)
        for n in oil
    ) / len(oil)


def update_markets(world: WorldState, consts: dict) -> None:
    """Resolution step: arms and oil drift toward targets set by world conflict
    and petro-state instability. No-op when market_feedback is 0."""
    if consts["market_feedback"] <= 0:
        return
    m = world.markets
    conflict = _mean_node_strength(world) - consts["arms_baseline"]
    arms_target = clamp(50.0 + consts["arms_conflict_weight"] * conflict)
    m["arms"] += (arms_target - m["arms"]) * consts["market_adjust"]
    instab = _oil_instability(world)
    oil_target = 50.0 if instab is None else clamp(
        50.0 + consts["oil_instability_weight"] * (instab - 50.0)
    )
    m["oil"] += (oil_target - m["oil"]) * consts["market_adjust"]
    m["arms"] = clamp(m["arms"])
    m["oil"] = clamp(m["oil"])


def arms_mult(world: WorldState, consts: dict) -> float:
    """Global ExternalSupport multiplier — a hot arms market arms insurgencies
    everywhere. Applied alongside the norms recruit multiplier in growth."""
    if consts["market_feedback"] <= 0:
        return 1.0
    return max(
        0.5,
        1.0 + consts["market_feedback"] * consts["arms_supply_weight"]
        * ((world.markets["arms"] - 50.0) / 50.0),
    )


def apply_feedback(world: WorldState, consts: dict, ledger: Ledger) -> None:
    """Consequence step: the oil market moves the importer-democracy's economy —
    a price spike is felt at home (Domestic), cheap energy is a small relief."""
    if consts["market_feedback"] <= 0:
        return
    drag = -consts["market_feedback"] * consts["oil_domestic_weight"] * (
        (world.markets["oil"] - 50.0) / 50.0
    )
    if abs(drag) > 1e-9:
        ledger.apply(world, DOMESTIC, "oil_market", drag)
