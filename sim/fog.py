"""Information and fog (DESIGN.md §9, §18.5).

Every insurgent number the player sees is an estimate with an honest confidence
band. The bias term IS deceptive calm: high entrenchment under low coverage
reads *low* — the map shows peace where there is shadow government. Intel buys
variance reduction, not omniscience. Truth is logged every turn for the
post-mortem reveal (engine.history).
"""

from __future__ import annotations

import random

from .world import WorldState


def estimate_value(
    rng: random.Random, consts: dict, true_value: float, coverage: float, entrenchment: float,
    sigma_mult: float = 1.0,
) -> tuple[float, float]:
    """Return (displayed, band) for one true value under given coverage."""
    sigma = consts["fog_sigma_max"] * (1.0 - coverage) * sigma_mult
    bias = -consts["fog_calm_bias"] * (entrenchment / 100.0) * (1.0 - coverage)
    noise = rng.gauss(0.0, sigma)
    displayed = max(0.0, true_value * (1.0 + bias + noise))
    band = 1.64 * sigma * true_value  # ~90% band, rendered honestly in the briefing
    return displayed, band


def briefing_estimates(world: WorldState, consts: dict, rng: random.Random) -> dict:
    """What the agencies believe, node by node, faction by faction."""
    estimates: dict = {}
    for node in world.nodes_sorted():
        per_faction = {}
        for fid in sorted(node.presence):
            pres = node.presence[fid]
            s_est, s_band = estimate_value(
                rng, consts, pres.strength, node.intel_coverage, pres.entrenchment
            )
            # Entrenchment is the hardest thing to see — the truth HUMINT exists to buy.
            e_est, e_band = estimate_value(
                rng, consts, pres.entrenchment, node.intel_coverage, pres.entrenchment,
                sigma_mult=consts["fog_entrench_mult"],
            )
            per_faction[fid] = {
                "strength_est": round(s_est, 2),
                "strength_band": round(s_band, 2),
                "entrenchment_est": round(e_est, 2),
                "entrenchment_band": round(e_band, 2),
                "visibility": round(pres.visibility, 2),  # incidents are observable
            }
        estimates[node.id] = {
            "coverage": round(node.intel_coverage, 3),
            "grievance": round(node.grievance, 2),  # polling/press: public
            "governance": round(node.governance, 2),
            "government": node.government,
            "local_legitimacy": round(node.local_legitimacy, 2),
            "theater": node.theater,  # public grouping (§21.1) — for Regional Commands
            "factions": per_faction,
        }
    return estimates
