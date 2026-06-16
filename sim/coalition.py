"""Coalition burden-sharing — the second world-scale lever (DESIGN.md §21.8, v0.15).

Regional Commands (§21.7) let you contain a theatre, but a hard home-front cost
caps you at one or two — you cannot police the world alone. The way real lead
democracies stretch further is a **coalition**: the 87-member Global Coalition to
Defeat ISIS, NATO, the Lake-Chad MNJTF's troop-contributing neighbours. Allies
share the *upkeep* of your commands, so a strong coalition lets you sustain more
theatres than your own home front could carry.

But a coalition is not free, and it is the thesis again from a second angle
(Olson & Zeckhauser 1966): collective security is a public good, so partners
**free-ride** — cohesion decays every turn as members drift back to letting you
pay (NATO's 2% target: only 3 of 28 met it in 2014). You sustain it by spending
political capital to rally them. And it **frays** when the rival bloc is
ascendant — fair-weather members hedge toward the winning side (the §8 rivalry
erodes cohesion). So the burden you offload is real but perishable: lean on the
coalition and keep it fed, or watch it melt exactly when the world turns against
you.

Gated by `coalition_enabled` (0 in single-theatre → dormant, calibration-safe;
1 in grand)."""

from __future__ import annotations

from .world import WorldState, clamp


def enabled(consts: dict) -> bool:
    return consts.get("coalition_enabled", 0) > 0


def rally(world: WorldState, consts: dict) -> None:
    """Spend political capital to push partners toward their fair share (the
    §18.4 `coalition` op) — raises cohesion, fighting the free-riding drift."""
    if not enabled(consts):
        return
    world.coalition = clamp(world.coalition + consts["coalition_rally_gain"])


def burden_share(world: WorldState, consts: dict) -> float:
    """The fraction of a command's home-front and treasury cost the coalition
    carries — proportional to cohesion, capped (you always pay the lead's share)."""
    if not enabled(consts):
        return 0.0
    return consts["coalition_max_share"] * (world.coalition / 100.0)


def decay(world: WorldState, consts: dict) -> None:
    """Cohesion bleeds every turn: free-riding drift (Olson–Zeckhauser), faster
    fraying under a rising rival bloc (fair-weather members hedge toward the
    ascendant side — the §8 rivalry), and faster still the more commands you lean
    on it to carry (the EU4 lesson: over-extension feeds the case against you)."""
    if not enabled(consts):
        return
    erosion = (
        consts["coalition_decay"]
        + consts["coalition_rivalry_erosion"] * world.rivalry / 100.0
        + consts["coalition_command_strain"] * len(world.commands)
    )
    world.coalition = clamp(world.coalition - erosion)
