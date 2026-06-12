"""Rival patrons (DESIGN.md §8) — v0.2 stub, honestly labeled (§18.8).

At this version the mercenary patron exists as influence drift only: where a
state has collapsed out of civilian rule, the no-strings offer wins by default
and influence accretes turn by turn. The full allegiance market — competing
offers, conditionality, mid-game defections — lands at v0.7.
"""

from __future__ import annotations

from .world import WorldState, clamp

MERCENARY = "mercenary"


def drift(world: WorldState, consts: dict) -> list[dict]:
    """Resolution substep g."""
    log: list[dict] = []
    for country in world.countries():
        capital = world.capital_of(country)
        if capital is None or capital.government == "civilian":
            continue
        for node in world.country_nodes(country):
            old = node.patron_influence.get(MERCENARY, 0.0)
            new = clamp(old + consts["patron_drift_junta"])
            node.patron_influence[MERCENARY] = new
            if old < 50.0 <= new:
                log.append(
                    {
                        "event": "patron_dominant",
                        "patron": MERCENARY,
                        "node": node.id,
                        "turn": world.turn,
                    }
                )
    return log
