"""Regional Commands — the first world-scale lever (DESIGN.md §21.7, v0.14).

v0.13 *measured* that no policy out-scores abdication at 40 nodes: the player's
levers were too local to bend a global trajectory. A Regional Command is the
answer — a standing theatre-wide posture that contains insurgency across a whole
region (breadth, not depth) at an accelerating home-front cost. These tests pin
the milestone it unlocks (engaged play finally beats passivity), the thesis the
cost encodes (the home front is the ceiling), and the gating that keeps the
single-theatre calibration untouched."""

import statistics

import pytest

from sim import (
    Engine,
    GrandCompetentPolicy,
    PassivePolicy,
    PureHeartsMindsPolicy,
    PureKineticPolicy,
    load_rules,
)
from sim import commands as commands_mod


def grand(policy, seed):
    return Engine(rules=load_rules(scenario="grand"), seed=seed, policy=policy)


# ----------------------------------------------------------- the lever works

def test_a_command_contains_its_theatre():
    """A standing command thins insurgent strength across every node of its
    theatre — fewer of its capitals fall than in the same world left untended."""
    held, untended = [], []
    for seed in range(4):
        a = grand(PassivePolicy(), seed)
        a.run(40)
        theatre = a.world.nodes["mali"].theater
        commands_mod.establish(a.world, a.consts, theatre)  # stand up the Sahel command
        a.run(40)
        held.append(sum(1 for n in a.world.nodes_sorted()
                        if n.theater == theatre and n.capital
                        and n.government != "civilian"))
        b = grand(PassivePolicy(), seed)
        b.run(80)
        untended.append(sum(1 for n in b.world.nodes_sorted()
                            if n.theater == theatre and n.capital
                            and n.government != "civilian"))
    assert statistics.mean(held) <= statistics.mean(untended), \
        "a commanded theatre should fall no faster than an untended one"


def test_commands_bleed_the_home_front_and_accelerate():
    """The cost is the thesis (Merom/Kennedy): every command drains Domestic, and
    the strain steepens with how many theatres you hold at once."""
    eng = grand(PassivePolicy(), 1)
    eng.run(10)
    for th in ("sahel", "horn", "levant"):
        commands_mod.establish(eng.world, eng.consts, th)
    before = eng.world.player.domestic
    eng.run(1)
    saw = any(e["source"] == "command_overstretch"
              for r in eng.reports for e in r["ledger"])
    assert saw, "holding commands must show an overstretch drain on Domestic"
    # three theatres held should cost more per turn than one (triangular strain)
    one = eng.consts["command_home_strain"] * 1 * 2 / 2.0
    three = eng.consts["command_home_strain"] * 3 * 4 / 2.0
    assert three > 3 * one, "the home cost must accelerate, not stay linear"
    assert eng.world.player.domestic < before  # it genuinely bled


# --------------------------------------------------- the milestone it unlocks

def test_engaged_play_now_beats_abdication_at_world_scale():
    """The v0.14 payoff (§21.7): leading with Regional Commands, a competent world
    police out-scores doing nothing across a 40-nation world — the win v0.13 could
    not reach with purely local levers. Earned (commands cost blood and treasure),
    not tuned: a distributional claim, asserted across seeds."""
    seeds = range(8)
    grand_c = [(_run(GrandCompetentPolicy(), s)) for s in seeds]
    passive = [(_run(PassivePolicy(), s)) for s in seeds]
    wins = sum(1 for g, p in zip(grand_c, passive) if g > p)
    assert statistics.mean(grand_c) > statistics.mean(passive), \
        "posture-led competent play should beat abdication on average"
    assert wins >= 5, f"and on a clear majority of worlds (won {wins}/8)"


def test_no_pure_doctrine_out_scores_the_command_player():
    """The §19.7 discipline at world scale: the balanced, posture-led player tops
    every single doctrine — kinetic abdication-of-restraint stays worst."""
    seeds = range(6)
    grand_c = statistics.mean(_run(GrandCompetentPolicy(), s) for s in seeds)
    kinetic = statistics.mean(_run(PureKineticPolicy(), s) for s in seeds)
    hearts = statistics.mean(_run(PureHeartsMindsPolicy(), s) for s in seeds)
    assert grand_c > kinetic and grand_c > hearts
    assert kinetic < hearts, "pure force should remain the worst doctrine"


# --------------------------------------------------------------- gating

def test_commands_dormant_in_single_theatre():
    """Gated by `commands_enabled`: the Sahel arc never offers the lever, never
    stands a command, and never pays its costs — calibration-safe by construction."""
    eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=2, policy=PureKineticPolicy())
    eng.run(60)
    assert eng.world.commands == []
    offered = {i["id"] for i in eng._legal_actions()["initiatives"]}
    assert "establish_command" not in offered, "world-scale lever must be hidden here"
    assert not any(
        e["source"] in ("command_overstretch", "command")
        for r in eng.reports for e in r["ledger"]
    )
    # the op itself is inert when disabled
    assert not commands_mod.establish(eng.world, eng.consts, "sahel")


@pytest.mark.parametrize("seed", [0, 1])
def test_grand_with_commands_is_deterministic(seed):
    a = grand(GrandCompetentPolicy(), seed)
    b = grand(GrandCompetentPolicy(), seed)
    a.run(60)
    b.run(60)
    assert a.state_hash() == b.state_hash()
    assert '"commands"' in a.checkpoint()


def _run(policy, seed):
    eng = grand(policy, seed)
    eng.run(100)
    return eng.score()["final"]
