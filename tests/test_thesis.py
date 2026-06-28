"""The design-thesis regression suite (DESIGN.md §13.3, PROJECT_CONTEXT §3.8) —
the idea to protect above all others: the design's claims, asserted in pytest.

As of v0.16 **all four are enforced**: the Sahel history calibration, the
pure-kinetic paradox, hearts-minds-loses-to-momentum, and — once the full
Emergency Powers track (§7) landed — emergency-powers-tempting-but-scored. A
balance change that breaks any of them now fails CI: the design document stays
true by force.

v0.24 added a fifth, *stronger* assertion — §19.7 (no pure strategy dominates the
balanced baseline) at the arc's **full 168-turn horizon**, not only the 120-turn
subset — and it began life xfailing. The road to enforcing it is a case study in
*measure, never assume*: v0.24's first mechanism guess was wrong (it is NOT that
conceded countryside drops out of the score, NOR that sustained security's costs
pile up — the benchmark barely uses force). v0.25 measured the truth — capital
collapse is driven by insurgent strength ÷ capital governance
(`factions.collapse_rolls`), not grievance directly, so the long-game winner is
whoever ends with the *smallest* insurgency — and sharpened the benchmark's
targeting. Two candidate world-dynamics fixes (grip-scaled co-option; a
low-grievance coercion channel) were then built and **measured to point the wrong
way** — both reward the lowest-strength strategy (pure prevention) — and reverted.
The fix that worked is a *benchmark* fix, calibration-safe: a **concentrated
political-primacy** player (prevent at scale via grievance-targeted development
**and** shrink the established force via negotiation) ends with a smaller
insurgency than pure prevention and **robustly tops every pure at both 120 and 168
turns**. **Enforced at v0.28.** (Honest caveat, §19.7: the win comes from
concentration, not breadth — the support tools are currently too low-leverage to
earn the scarce budget, a separate tuning question.)
"""

from sim import (
    CompetentPolicy,
    EmergencyPowersPolicy,
    Engine,
    PassivePolicy,
    PureHeartsMindsPolicy,
    PureKineticPolicy,
    load_rules,
)

SEEDS = range(5)


def mean_final(policy_cls, turns: int = 120, seeds=SEEDS) -> float:
    scores = []
    for seed in seeds:
        eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=seed, policy=policy_cls())
        eng.run(turns)
        scores.append(eng.score()["final"])
    return sum(scores) / len(scores)


def total_strength(engine: Engine) -> float:
    return sum(
        p.strength for n in engine.world.nodes_sorted() for p in n.presence.values()
    )


def run(policy_cls, seed: int, turns: int) -> Engine:
    eng = Engine(seed=seed, policy=policy_cls())
    eng.run(turns)
    return eng


def _collapse_turn(eng: Engine, country: str) -> int | None:
    for report in eng.reports:
        for entry in report["log"]:
            if entry.get("event") == "state_collapse" and entry.get("country") == country:
                return entry["turn"]
    return None


def test_passive_player_reproduces_history():
    """ENFORCED (v0.5). Untouched, the sim replays the Sahel arc 2012–2026: Mali
    falls to a junta in the coup-cascade window, the cascade runs ML→BF→NE, a
    bloc forms, and the insurgency keeps growing to the end (the ICG finding —
    the juntas don't solve it). Reality is the balance baseline (DESIGN §12)."""
    ml_junta_window = 0
    cascade_ordered = 0
    for seed in SEEDS:
        eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=seed,
                     policy=PassivePolicy())
        start = total_strength(eng)
        eng.run(168)
        assert total_strength(eng) > 2.0 * start, "insurgency should expand unopposed"
        # still growing in the final two years
        late = eng.history[-1]
        tail = eng.history[-25]
        late_s = sum(p["strength"] for n in late["nodes"].values()
                     for p in n["presence"].values())
        tail_s = sum(p["strength"] for n in tail["nodes"].values()
                     for p in n["presence"].values())
        assert late_s > tail_s, "insurgency should still be growing at the horizon"
        t_ml = _collapse_turn(eng, "ML")
        cap = eng.world.capital_of("ML")
        if t_ml is not None and cap.government == "junta" and 60 <= t_ml <= 140:
            ml_junta_window += 1
        t_bf, t_ne = _collapse_turn(eng, "BF"), _collapse_turn(eng, "NE")
        if t_ml is not None and (t_bf is None or t_ml <= t_bf) and (
            t_bf is None or t_ne is None or t_bf <= t_ne
        ):
            cascade_ordered += 1
    assert ml_junta_window >= 4, "Mali junta in the historical window must be near-universal"
    assert cascade_ordered >= 4, "the cascade must run ML→BF→NE (the historical order)"


def test_pure_kinetic_strategy_loses_integrity_and_local():
    """ENFORCED (v0.5). Force suppresses Strength but corrodes Local and bleeds
    Domestic — FM 3-24's paradox as a regression test."""
    for seed in SEEDS:
        kinetic = run(PureKineticPolicy, seed, 96)
        passive = run(PassivePolicy, seed, 96)
        local_k = sum(n.local_legitimacy for n in kinetic.world.nodes_sorted())
        local_p = sum(n.local_legitimacy for n in passive.world.nodes_sorted())
        assert local_k < local_p, "kinetic-only play should end with less Local than doing nothing"
        assert kinetic.world.player.casualties > 0
        assert kinetic.world.player.domestic < passive.world.player.domestic


def test_pure_hearts_minds_without_security_loses_to_momentum():
    """ENFORCED (v0.5). Development without any security component must not stop
    a growing insurgency — Galula's 80% political still needs the other 20%."""
    for seed in SEEDS:
        hearts = run(PureHeartsMindsPolicy, seed, 96)
        start = sum(
            p.strength
            for n in Engine(seed=seed).world.nodes_sorted()
            for p in n.presence.values()
        )
        assert total_strength(hearts) > start, "unopposed momentum should outpace pure development"


def test_no_pure_strategy_dominates_the_balanced_baseline():
    """ENFORCED (v0.8, §19.7). Pillar 3 as a number: competent *balanced* play
    (security with restraint + governance + negotiation + exposure) must outscore
    every pure archetype on the arc. If a single pure strategy matched or beat it,
    a dominant strategy would exist and 'every tool cuts both ways' would have
    sprung a leak. Calibration stays history-true (the passive WORLD is unchanged);
    only the player's tools and the scoring were tuned to open a real win path."""
    balanced = mean_final(CompetentPolicy)
    for pure in (PureKineticPolicy, PureHeartsMindsPolicy, EmergencyPowersPolicy):
        assert balanced > mean_final(pure), (
            f"{pure.__name__} matches/beats competent balanced play — dominant strategy"
        )


def test_a_reasonable_player_can_beat_history():
    """ENFORCED (v0.8, §3.7). The design's hope, asserted: a competent player
    must end the arc meaningfully better than a passive one who lets it burn —
    fewer captured states and a higher score. If doing nothing were as good as
    playing well, there would be no game."""
    competent = mean_final(CompetentPolicy)
    passive = mean_final(PassivePolicy)
    assert competent > passive + 5.0, "skilled play must clearly beat inaction"


def test_no_pure_strategy_dominates_at_the_full_horizon():
    """ENFORCED at v0.28 (§19.7) — the §19.7 discipline at the arc's *actual* play
    length (168 turns), not only the 120-turn subset the test above checks. Balanced
    play must top every pure archetype over the whole run, or a dominant strategy
    exists at the horizon players reach. Promoted from xfail once a *concentrated
    political-primacy* benchmark — prevent at scale (grievance-targeted development)
    **and** shrink the established force (negotiation) — was shown to end with a
    smaller insurgency than pure prevention and so to win robustly at both horizons.
    Calibration-safe: only the player benchmark changed; the passive WORLD (§12) is
    untouched. (§19.7 caveat: the win is from concentration, not breadth — the
    support tools are currently too low-leverage to earn the scarce budget.)"""
    balanced = mean_final(CompetentPolicy, turns=168)
    for pure in (PureKineticPolicy, PureHeartsMindsPolicy, EmergencyPowersPolicy):
        assert balanced > mean_final(pure, turns=168), (
            f"{pure.__name__} out-scores balanced play at the full 168-turn horizon"
        )


def test_emergency_powers_tempting_but_scored():
    """ENFORCED at v0.16 (the full Emergency Powers track, §7): the authoritarian
    toolkit must be genuinely strong (tempting) and the scoring must still know
    (IntegrityMultiplier + the direct drift cost). Win ugly, score poorly — and
    mechanically, never by a 'you crossed the line' scold (Frostpunk's lesson)."""
    for seed in SEEDS:
        emergency = run(EmergencyPowersPolicy, seed, 96)
        kinetic = run(PureKineticPolicy, seed, 96)
        s_e, s_k = emergency.score(), kinetic.score()
        assert s_e["integrity_mult"] < 1.0, "drift must be permanent and visible in scoring"
        raw_e = s_e["stabilization"] * s_e["order_mult"]
        raw_k = s_k["stabilization"] * s_k["order_mult"]
        assert raw_e >= raw_k, "the emergency toolkit must actually be tempting (stronger raw)"
        assert s_e["final"] < s_k["final"], "and the game must still know (integrity-scaled loss)"
