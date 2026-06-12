"""The design-thesis regression suite (DESIGN.md §13.3, PROJECT_CONTEXT §3.8) —
the idea to protect above all others: the design's claims, asserted in pytest.

All four are real simulations already, marked xfail (non-strict) until the
systems and the v0.5 calibration land. When one starts passing, pytest reports
XPASS — that is the roadmap telling us a milestone arrived. If a balance change
ever breaks one after it passes, CI fails and the design document stays true
by force.
"""

import pytest

from sim import (
    EmergencyPowersPolicy,
    Engine,
    PassivePolicy,
    PureHeartsMindsPolicy,
    PureKineticPolicy,
    load_rules,
)

SEEDS = range(5)


def total_strength(engine: Engine) -> float:
    return sum(
        p.strength for n in engine.world.nodes_sorted() for p in n.presence.values()
    )


def run(policy_cls, seed: int, turns: int) -> Engine:
    eng = Engine(seed=seed, policy=policy_cls())
    eng.run(turns)
    return eng


@pytest.mark.xfail(
    strict=False,
    reason="Sahel calibration is the v0.5 milestone; constants are first guesses (DESIGN §12)",
)
def test_passive_player_reproduces_history():
    """Untouched, the sim should approximately replay 2012–2026 on the full
    arc map (v0.4): Mali collapses to a junta around the coup-cascade window,
    and insurgent reach expands."""
    junta_runs = 0
    for seed in SEEDS:
        eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=seed,
                     policy=PassivePolicy())
        eng.run(168)
        start = sum(
            p.strength
            for n in Engine(rules=load_rules(scenario="sahel_arc"),
                            seed=seed).world.nodes_sorted()
            for p in n.presence.values()
        )
        assert total_strength(eng) > 1.5 * start, "insurgency should expand unopposed"
        capital = eng.world.capital_of("ML")
        if eng.world.collapsed["ML"] and capital is not None and capital.government == "junta":
            collapse_turns = [
                entry["turn"]
                for report in eng.reports
                for entry in report["log"]
                if entry.get("event") == "state_collapse" and entry.get("country") == "ML"
            ]
            if collapse_turns and 60 <= collapse_turns[0] <= 140:
                junta_runs += 1
    assert junta_runs >= 3, "Mali junta in the historical window should be the modal outcome"


@pytest.mark.xfail(
    strict=False,
    reason="needs occupation antibodies + calibrated casualty/collateral rates (v0.5–v0.6)",
)
def test_pure_kinetic_strategy_loses_integrity_and_local():
    """Force suppresses Strength but corrodes Local and bleeds Domestic —
    FM 3-24's paradox as a regression test."""
    for seed in SEEDS:
        kinetic = run(PureKineticPolicy, seed, 96)
        passive = run(PassivePolicy, seed, 96)
        local_k = sum(n.local_legitimacy for n in kinetic.world.nodes_sorted())
        local_p = sum(n.local_legitimacy for n in passive.world.nodes_sorted())
        assert local_k < local_p, "kinetic-only play should end with less Local than doing nothing"
        assert kinetic.world.player.casualties > 0
        assert kinetic.world.player.domestic < passive.world.player.domestic


@pytest.mark.xfail(
    strict=False,
    reason="needs spread + joint offensives so momentum can actually punish (v0.4–v0.7)",
)
def test_pure_hearts_minds_without_security_loses_to_momentum():
    """Development without any security component must not stop a growing
    insurgency — Galula's 80% political still needs the other 20%."""
    for seed in SEEDS:
        hearts = run(PureHeartsMindsPolicy, seed, 96)
        start = sum(
            p.strength
            for n in Engine(seed=seed).world.nodes_sorted()
            for p in n.presence.values()
        )
        assert total_strength(hearts) > start, "unopposed momentum should outpace pure development"


@pytest.mark.xfail(
    strict=False,
    reason="only Emergency Powers tier 1 exists; the full track lands per §7/§11 (v0.6+)",
)
def test_emergency_powers_tempting_but_scored():
    """The authoritarian toolkit must be genuinely strong (tempting) and the
    scoring must still know (IntegrityMultiplier). Win ugly, score poorly."""
    for seed in SEEDS:
        emergency = run(EmergencyPowersPolicy, seed, 96)
        kinetic = run(PureKineticPolicy, seed, 96)
        s_e, s_k = emergency.score(), kinetic.score()
        assert s_e["integrity_mult"] < 1.0, "drift must be permanent and visible in scoring"
        raw_e = s_e["stabilization"] * s_e["order_mult"]
        raw_k = s_k["stabilization"] * s_k["order_mult"]
        assert raw_e >= raw_k, "the emergency toolkit must actually be tempting (stronger raw)"
        assert s_e["final"] < s_k["final"], "and the game must still know (integrity-scaled loss)"
