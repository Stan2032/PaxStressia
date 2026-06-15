"""The global norms / precedent layer (DESIGN.md §21, grand mode).

This is the mechanism that makes the core promise true at world scale: *every
choice ripples through every plausible variable, everywhere.* Your way of war —
how kinetic, how lawful, how authoritarian — accumulates into three world norms
(0–100, neutral 50). Those norms then feed back into **every theater at once**:

  - a kinetic, autocratic precedent fuels insurgent recruitment worldwide
    (Kilcullen's accidental guerrilla and your hypocrisy, at global scale);
  - a lawful, restrained precedent earns International standing and starves it;
  - an autocratic precedent raises every rival patron's appeal (you legitimised
    the model you claim to oppose).

The whole layer is gated by `norm_feedback`: 0 in single-theater scenarios (so
the Sahel history calibration is untouched by construction), > 0 in grand mode.
The propagation is through *plausible channels*, not all-to-all noise — that is
the design discipline (§21).
"""

from __future__ import annotations

from .legitimacy import INTERNATIONAL, Ledger
from .world import WorldState, clamp

MILITARY = "military"
LAWFUL_FAMILIES = ("governance", "diplomatic")


def update_norms(world: WorldState, consts: dict, executed: list[dict], initiatives: dict,
                 drift_tiers_this_turn: int) -> None:
    """Resolution step: move the world norms from this turn's choices, then
    decay them toward neutral. No-op when norm_feedback is 0."""
    if consts["norm_feedback"] <= 0:
        return
    norms = world.norms
    for order in executed:
        fam = initiatives[order["initiative"]]["family"]
        if fam == MILITARY:
            norms["kinetic"] = clamp(norms["kinetic"] + consts["norm_kinetic_per_use"])
        elif fam in LAWFUL_FAMILIES:
            norms["rule_of_law"] = clamp(norms["rule_of_law"] + consts["norm_law_per_use"])
    if drift_tiers_this_turn:
        norms["autocracy"] = clamp(
            norms["autocracy"] + consts["norm_autocracy_per_tier"] * drift_tiers_this_turn
        )
    # decay toward neutral — the world forgets a precedent over time
    for key in norms:
        if norms[key] > 50:
            norms[key] = max(50.0, norms[key] - consts["norm_decay"])
        elif norms[key] < 50:
            norms[key] = min(50.0, norms[key] + consts["norm_decay"])


def recruit_multiplier(world: WorldState, consts: dict) -> float:
    """Global recruitment multiplier from the precedent layer — applied to every
    theater's Recruitment term. >1 when the world has seen a kinetic/autocratic
    hand; ≤1 when it has seen restraint and law."""
    if consts["norm_feedback"] <= 0:
        return 1.0
    n = world.norms
    pressure = ((n["kinetic"] - 50.0) + (n["autocracy"] - 50.0) - (n["rule_of_law"] - 50.0)) / 100.0
    return max(0.5, 1.0 + consts["norm_feedback"] * consts["norm_recruit_weight"] * pressure)


def apply_feedback(world: WorldState, consts: dict, ledger: Ledger) -> None:
    """Consequence step: world norms move International (law rewarded, force and
    autocracy punished) and raise rival-patron appeal when autocracy is in vogue."""
    if consts["norm_feedback"] <= 0:
        return
    n = world.norms
    intl = (
        (n["rule_of_law"] - 50.0) - (n["kinetic"] - 50.0) - (n["autocracy"] - 50.0)
    ) / 100.0
    delta = consts["norm_feedback"] * consts["norm_intl_weight"] * intl
    if abs(delta) > 1e-9:
        ledger.apply(world, INTERNATIONAL, "world_norms", delta)


def patron_norm_bonus(world: WorldState, consts: dict) -> float:
    """Extra patron competitiveness worldwide from an autocratic world norm."""
    if consts["norm_feedback"] <= 0:
        return 0.0
    return consts["norm_feedback"] * consts["norm_patron_weight"] * max(
        0.0, (world.norms["autocracy"] - 50.0) / 100.0
    )
