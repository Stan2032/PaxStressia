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


def market(world: WorldState, consts: dict, patrons: list[dict] | None = None) -> list[dict]:
    """Resolution substep g (§8). Patron influence rises in non-civilian states,
    resisted by your International standing and the regime's Exposure. In grand
    mode (`rivalry_feedback` > 0) this is a *contest* between rival patron
    archetypes, with a global rivalry score and bandwagon dynamics; in single-
    theater play it stays the simple mercenary-only pull (calibration-safe)."""
    log: list[dict] = []
    intl = world.player.international
    norm_bonus = norms_mod.patron_norm_bonus(world, consts)  # autocratic precedent aids the patron
    multi = consts["rivalry_feedback"] > 0 and patrons

    def competitiveness(country: str) -> float:
        exposure = world.exposure.get(country, 0.0)
        return clamp(
            consts["patron_competitiveness_intl"] * (intl / 100.0)
            + consts["patron_competitiveness_exposure"] * (exposure / 100.0)
            - norm_bonus,
            0.0, 0.9,
        )

    if not multi:
        for country in world.countries():
            capital = world.capital_of(country)
            if capital is None or capital.government == "civilian":
                continue
            delta = consts["patron_drift_junta"] * (1.0 - competitiveness(country))
            for node in world.country_nodes(country):
                old = node.patron_influence.get(MERCENARY, 0.0)
                node.patron_influence[MERCENARY] = clamp(old + delta)
                if old < 50.0 <= node.patron_influence[MERCENARY]:
                    log.append({"event": "patron_dominant", "patron": MERCENARY,
                                "node": node.id, "turn": world.turn})
        return log

    # --- grand mode: the contest ---
    defs = {p["id"]: p for p in patrons}
    oil = world.markets["oil"]
    countries = world.countries()
    for country in countries:
        capital = world.capital_of(country)
        if capital is None or capital.government == "civilian":
            continue

        def appeal(pid: str) -> float:
            d = defs[pid]
            oil_boost = (oil - 50.0) * 0.2 if d.get("oil_funded") else 0.0
            return (capital.patron_influence.get(pid, 0.0)
                    + consts["patron_bandwagon"] * world.patron_strength.get(pid, 0.0)
                    + d.get("speed", 1.0) * 3.0 + oil_boost)

        chosen = max(sorted(defs), key=appeal)
        delta = (consts["patron_drift_junta"] * (1.0 - competitiveness(country))
                 * defs[chosen].get("speed", 1.0)
                 * (1.0 + consts["rivalry_bandwagon"] * world.rivalry / 100.0))
        world.patron_strength[chosen] = clamp(
            world.patron_strength.get(chosen, 0.0) + consts["patron_strength_gain"]
        )
        for node in world.country_nodes(country):
            old = node.patron_influence.get(chosen, 0.0)
            node.patron_influence[chosen] = clamp(old + delta)
            if old < 50.0 <= node.patron_influence[chosen]:
                log.append({"event": "patron_dominant", "patron": chosen,
                            "node": node.id, "turn": world.turn})

    # rivalry tracks the share of the world the rival bloc holds — left alone it
    # grows, and a winning bloc captures faster (the bandwagon above).
    captured = sum(
        1 for c in countries
        if (cap := world.capital_of(c)) is not None and cap.government != "civilian"
    )
    target = 100.0 * captured / max(1, len(countries))
    world.rivalry += (target - world.rivalry) * consts["rivalry_adjust"]
    return log


def dominant_patron(world: WorldState, country: str) -> str:
    """The patron with the most influence in a country's capital (for sanctions)."""
    cap = world.capital_of(country)
    if cap is None or not cap.patron_influence:
        return MERCENARY
    return max(sorted(cap.patron_influence), key=lambda p: cap.patron_influence[p])


def decay_exposure(world: WorldState, consts: dict) -> None:
    """Exposure erodes without sustained funding — documented truth needs upkeep."""
    for country in list(world.exposure):
        world.exposure[country] = max(0.0, world.exposure[country] - consts["exposure_decay"])
