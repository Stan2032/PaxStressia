"""Regional Commands — the first world-scale lever (DESIGN.md §21.7, v0.14).

A grand-mode player acts in only a few nodes a turn, so at 40-nation scale their
hands never reach most of the world — v0.13 *measured* that no policy out-scores
abdication, because the levers are too local to bend a global trajectory. A
**Regional Command** is the answer the research points to (HoI4 garrison
templates; the real AFRICOM / Operation Barkhane / the Lake-Chad MNJTF): a
STANDING posture over a whole theatre that passively *contains* insurgency across
every one of its nodes each turn. It buys breadth, not depth — it bends the
trajectory and buys time; it does **not** resolve a theatre (crises still need
your hands-on actions). Posture sets the board; agency wins it.

Its counterweight is the game's thesis made mechanical (Kennedy's imperial
overstretch; Merom's home front as the true ceiling; Mueller's logarithmic
casualty curve): every command bleeds treasury AND home legitimacy each turn, and
the home cost **accelerates** with how many theatres you hold at once — the second
and third command cost far more than the first. Over-extension craters Domestic
and forces a drawdown (Barkhane: democracies withdraw on politics, not defeat),
which leaves a vacuum. A hard cap (`command_max`) forces triage: you cannot police
the whole world, only choose where to stand.

Gated by `commands_enabled` (0 in single-theatre → dormant, calibration-safe by
construction; 1 in grand)."""

from __future__ import annotations

from .legitimacy import DOMESTIC, Ledger, local_gauge
from .world import WorldState, clamp


def enabled(consts: dict) -> bool:
    return consts.get("commands_enabled", 0) > 0


def establish(world: WorldState, consts: dict, theater: str | None) -> bool:
    """Stand up a regional command over `theater` (the §18.4 `command` op). Capped
    by `command_max` — you cannot be everywhere — and a no-op outside grand."""
    if not enabled(consts) or not theater:
        return False
    if theater in world.commands or len(world.commands) >= consts["command_max"]:
        return False
    world.commands.append(theater)
    world.commands.sort()
    return True


def _theater_nodes(world: WorldState, theater: str) -> list:
    return [n for n in world.nodes_sorted() if getattr(n, "theater", None) == theater]


def apply(world: WorldState, consts: dict, ledger: Ledger, log: list) -> None:
    """Resolution substep: standing commands CONTAIN their theatres and BLEED the
    home front. Containment is deliberately light per node (posture, not victory);
    the home cost accelerates with the number of commands (overstretch). Runs
    before the collapse rolls so the buffer can save a wavering capital."""
    if not enabled(consts) or not world.commands:
        return
    # --- containment: a light, theatre-wide suppression on every node held ---
    for theater in list(world.commands):
        for node in _theater_nodes(world, theater):
            if node.presence:
                strongest = max(sorted(node.presence), key=lambda f: node.presence[f].strength)
                pres = node.presence[strongest]
                pres.strength = clamp(pres.strength - consts["command_attrition"])
            node.governance = clamp(node.governance + consts["command_gov_buffer"])
            ledger.apply(world, local_gauge(node.id), "command", consts["command_local_buffer"])

    # --- cost: treasury upkeep (linear) + accelerating home-front strain ---
    k = len(world.commands)
    upkeep = consts["command_upkeep"] * k
    if world.player.treasury >= upkeep:
        world.player.treasury -= upkeep
    else:
        # can't be sustained — forced drawdown of one theatre (Barkhane: politics,
        # not defeat). The vacuum is left for the insurgency/rival to refill.
        world.player.treasury = 0.0
        dropped = world.commands.pop()
        ledger.apply(world, DOMESTIC, "command_withdrawn", -consts["command_withdraw_hit"])
        log.append({"event": "command_withdrawn", "theater": dropped,
                    "reason": "unaffordable", "turn": world.turn})
        k = len(world.commands)
    # home legitimacy is the true ceiling (Merom): strain grows triangularly with
    # the count, so the 2nd/3rd theatre costs far more than the first.
    if k:
        strain = consts["command_home_strain"] * k * (k + 1) / 2.0
        ledger.apply(world, DOMESTIC, "command_overstretch", -strain)
    # drawdown trigger: a home front past its floor rejects the over-extension and
    # forces one command home, defeat ratified at home (Merom), not on the field.
    if world.commands and world.player.domestic < consts["command_domestic_floor"]:
        dropped = world.commands.pop()
        ledger.apply(world, DOMESTIC, "command_withdrawn", -consts["command_withdraw_hit"])
        log.append({"event": "command_withdrawn", "theater": dropped,
                    "reason": "home_front", "turn": world.turn})
