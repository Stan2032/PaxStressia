"""Rival patrons & the allegiance market (DESIGN.md §8, v0.7).

Every state out of civilian rule is courted by the mercenary patron (the
Wagner/Africa-Corps model): coup-proofing with no human-rights strings,
arriving fast. Your counter-offer comes with conditionality, so it only
competes when your standing is high — and when independent **Exposure** (§20)
has made the patron's bargain look expensive. The market is the §8 thesis:
half the game's losses happen at a table you weren't invited to.

v0.7 replaces the v0.2 flat-drift stub with this comparative pull, and adds the
per-turn decay of Exposure (the truth fades without upkeep).
"""

from __future__ import annotations

from . import norms as norms_mod
from .world import WorldState, clamp

MERCENARY = "mercenary"


def market(world: WorldState, consts: dict) -> list[dict]:
    """Resolution substep g. Patron influence rises in non-civilian states,
    resisted by your International standing and the regime's Exposure."""
    log: list[dict] = []
    intl = world.player.international
    norm_bonus = norms_mod.patron_norm_bonus(world, consts)  # autocratic precedent aids the patron
    for country in world.countries():
        capital = world.capital_of(country)
        if capital is None or capital.government == "civilian":
            continue
        exposure = world.exposure.get(country, 0.0)
        # Your competitiveness: a strong, credible offer slows the capture; a
        # world that has normalised autocracy (norm_bonus) erodes it everywhere.
        competitiveness = clamp(
            consts["patron_competitiveness_intl"] * (intl / 100.0)
            + consts["patron_competitiveness_exposure"] * (exposure / 100.0)
            - norm_bonus,
            0.0, 0.9,
        )
        delta = consts["patron_drift_junta"] * (1.0 - competitiveness)
        for node in world.country_nodes(country):
            old = node.patron_influence.get(MERCENARY, 0.0)
            new = clamp(old + delta)
            node.patron_influence[MERCENARY] = new
            if old < 50.0 <= new:
                log.append({"event": "patron_dominant", "patron": MERCENARY,
                            "node": node.id, "turn": world.turn})
    return log


def decay_exposure(world: WorldState, consts: dict) -> None:
    """Exposure erodes without sustained funding — documented truth needs upkeep."""
    for country in list(world.exposure):
        world.exposure[country] = max(0.0, world.exposure[country] - consts["exposure_decay"])
