"""Elections and the Mandate coupling (DESIGN.md §6, §18.5).

Mandate = f(Domestic, election proximity) is the single most important coupling
in the game: domestic politics is the engine room. Honeymoons are fat,
lame-duck turns are thin, and losing an election is not losing the game
(continuity model (a) as the v0.2 placeholder; open question #1 stands).
"""

from __future__ import annotations

import math
import random

from .legitimacy import DOMESTIC, Ledger
from .world import WorldState


def mandate_income(world: WorldState, consts: dict) -> int:
    player = world.player
    phase = 1.0
    if player.honeymoon_left > 0:
        phase = consts["honeymoon_mult"]
    else:
        to_election = consts["election_period_turns"] - player.turns_since_election
        if to_election <= consts["lameduck_turns"] and player.domestic < 50:
            phase = consts["lameduck_mult"]
    return max(1, round(consts["mandate_base"] * (0.5 + player.domestic / 100.0) * phase))


def election_tick(
    world: WorldState, consts: dict, rng: random.Random, ledger: Ledger
) -> dict | None:
    """Consequence-phase tick; resolves an election when the period elapses."""
    player = world.player
    player.turns_since_election += 1
    if player.honeymoon_left > 0:
        player.honeymoon_left -= 1
    if player.turns_since_election < consts["election_period_turns"]:
        return None
    player.turns_since_election = 0
    win_p = 1.0 / (1.0 + math.exp(-(player.domestic - 50.0) / consts["election_k"]))
    won = rng.random() < win_p
    if won:
        player.honeymoon_left = consts["honeymoon_turns"]
    else:
        # Continuity model (a): the state plays on; standing reverts toward 50.
        target = 50.0 + (player.domestic - 50.0) * consts["continuity_reversion"]
        ledger.apply(world, DOMESTIC, "election:loss_reversion", target - player.domestic)
    return {"event": "election", "won": won, "win_p": round(win_p, 4), "turn": world.turn}
