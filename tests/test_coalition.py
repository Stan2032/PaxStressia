"""Coalition burden-sharing — the second world-scale lever (DESIGN.md §21.8, v0.15).

Regional Commands (§21.7) let you hold a theatre but a hard home-front cost caps
you at one or two. A coalition shares that upkeep so you can stretch further —
but partners free-ride (cohesion decays) and fair-weather members hedge toward an
ascendant rival (the §8 rivalry frays it). These tests pin that it lightens the
command burden, that it must be maintained, that it deepens the win, and that it
is dormant — and so calibration-safe — in single-theatre play."""

import statistics

import pytest

from sim import Engine, GrandCompetentPolicy, PassivePolicy, PureKineticPolicy, load_rules
from sim import coalition as coalition_mod


def grand(policy, seed):
    return Engine(rules=load_rules(scenario="grand"), seed=seed, policy=policy)


# ------------------------------------------------------ the lever behaves

def test_rallying_builds_cohesion_and_shares_the_burden():
    eng = grand(PassivePolicy(), 1)
    eng.run(5)
    assert coalition_mod.burden_share(eng.world, eng.consts) == 0.0  # nothing rallied yet
    for _ in range(4):
        coalition_mod.rally(eng.world, eng.consts)
    assert eng.world.coalition > 0
    share = coalition_mod.burden_share(eng.world, eng.consts)
    assert 0.0 < share <= eng.consts["coalition_max_share"]  # allies bear part, never all


def test_cohesion_free_rides_away_and_frays_faster_under_a_rival():
    """Decay is the thesis from a second angle (Olson–Zeckhauser): without rallying
    cohesion bleeds, and a rising rival bloc bleeds it faster."""
    calm = grand(PassivePolicy(), 2)
    calm.run(3)
    calm.world.coalition = 80.0
    calm.world.rivalry = 0.0
    coalition_mod.decay(calm.world, calm.consts)
    drop_calm = 80.0 - calm.world.coalition

    rival = grand(PassivePolicy(), 2)
    rival.run(3)
    rival.world.coalition = 80.0
    rival.world.rivalry = 90.0
    coalition_mod.decay(rival.world, rival.consts)
    drop_rival = 80.0 - rival.world.coalition

    assert drop_calm > 0, "cohesion free-rides away when unrallied"
    assert drop_rival > drop_calm, "an ascendant rival frays the coalition faster"


def test_a_coalition_lightens_the_command_home_cost():
    """With allies sharing the load, the same commands bleed the home front less —
    the whole point of the lever."""
    def overstretch_drain(coh):
        eng = grand(PassivePolicy(), 3)
        eng.run(8)
        for th in ("sahel", "horn", "levant"):
            commands_establish(eng, th)
        eng.world.coalition = coh
        before = eng.world.player.domestic
        eng.run(1)
        return before - eng.world.player.domestic
    solo = overstretch_drain(0.0)
    allied = overstretch_drain(100.0)
    assert allied < solo, "a strong coalition must reduce the home-front drain of commands"


# --------------------------------------------------- it deepens the win

def test_coalition_deepens_the_grand_win():
    """The §21.8 payoff: leaning on allies lets the competent world police sustain
    more containment and beat abdication more decisively than commands alone — a
    distributional claim, asserted across seeds, earned (cohesion costs and bleeds)."""
    seeds = range(8)
    grand_c = [_final(GrandCompetentPolicy(), s) for s in seeds]
    passive = [_final(PassivePolicy(), s) for s in seeds]
    wins = sum(1 for g, p in zip(grand_c, passive) if g > p)
    assert statistics.mean(grand_c) > statistics.mean(passive)
    assert wins >= 5, f"posture + coalition should beat abdication on most worlds (won {wins}/8)"


# --------------------------------------------------------------- gating

def test_coalition_dormant_in_single_theatre():
    eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=2, policy=PureKineticPolicy())
    eng.run(60)
    assert eng.world.coalition == 0.0
    coalition_mod.rally(eng.world, eng.consts)  # the op is inert when gated off
    assert eng.world.coalition == 0.0
    assert coalition_mod.burden_share(eng.world, eng.consts) == 0.0
    offered = {i["id"] for i in eng._legal_actions()["initiatives"]}
    assert "rally_coalition" not in offered


@pytest.mark.parametrize("seed", [0, 1])
def test_grand_with_coalition_is_deterministic(seed):
    a = grand(GrandCompetentPolicy(), seed)
    b = grand(GrandCompetentPolicy(), seed)
    a.run(60)
    b.run(60)
    assert a.state_hash() == b.state_hash()
    assert '"coalition"' in a.checkpoint()


def commands_establish(eng, theater):
    from sim import commands as commands_mod
    commands_mod.establish(eng.world, eng.consts, theater)


def _final(policy, seed):
    eng = grand(policy, seed)
    eng.run(100)
    return eng.score()["final"]
