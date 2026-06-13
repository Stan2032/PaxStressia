"""The Transparency Dial / leak clocks (DESIGN.md §6, v0.6).

Disclose pays now (less, honesty registers); suppress pays nothing now but
starts a leak clock that — scaled by press freedom and time — can detonate
later across all three gauges at a multiple of the honest cost. The thesis in
one mechanic: transparency is expensive every time, cheaper on average, if you
survive the variance.
"""

from sim import Engine, PassivePolicy
from sim.world import load_rules


def _suppress_op(engine, severity=8, node=None):
    engine._apply_op(
        {"op": "suppress_clock", "severity": severity}, node, "test:incident", []
    )


def test_suppress_registers_a_clock_no_immediate_cost():
    eng = Engine(seed=0, policy=PassivePolicy())
    before = eng.world.player.domestic
    _suppress_op(eng, severity=8)
    assert len(eng.world.player.suppress_clocks) == 1
    assert eng.world.player.domestic == before  # nothing paid yet


def test_a_suppressed_scandal_eventually_resolves():
    """Over its lifetime a buried scandal must either leak or bury safely —
    never linger forever."""
    eng = Engine(seed=1, policy=PassivePolicy())
    _suppress_op(eng, severity=8)
    leaked = buried = False
    for _ in range(eng.consts["leak_clock_turns"] + 2):
        log = []
        eng._process_suppress_clocks(log)
        for entry in log:
            if entry["event"] == "leak":
                leaked = True
            if entry["event"] == "buried_safely":
                buried = True
        if not eng.world.player.suppress_clocks:
            break
    assert leaked or buried
    assert eng.world.player.suppress_clocks == []


def test_a_leak_costs_more_than_disclosure_would_have():
    """Across many seeds, the expected suppression cost exceeds the honest cost —
    but with real variance (sometimes you pay nothing)."""
    honest_cost = 7.0  # partner_atrocity disclose ≈ 4 + 1 + 2
    suppress_costs = []
    for seed in range(40):
        eng = Engine(seed=seed, policy=PassivePolicy())
        _suppress_op(eng, severity=7)
        paid = 0.0
        for _ in range(eng.consts["leak_clock_turns"] + 1):
            d_before = eng.world.player.domestic
            i_before = eng.world.player.international
            eng._process_suppress_clocks([])
            paid += (d_before - eng.world.player.domestic) + (
                i_before - eng.world.player.international
            )
            if not eng.world.player.suppress_clocks:
                break
        suppress_costs.append(paid)
    mean = sum(suppress_costs) / len(suppress_costs)
    assert mean > honest_cost, "suppression should cost more on average than honesty"
    assert min(suppress_costs) == 0.0, "and sometimes you get away clean — the gamble"


def test_press_freedom_raises_leak_odds():
    """A free press is what makes suppression dangerous (Merom): higher
    press_freedom ⇒ more leaks over a fixed horizon."""
    def leaks_under(press_freedom: float) -> int:
        rules = load_rules()
        rules["constants"] = {**rules["constants"], "press_freedom": press_freedom}
        total = 0
        for seed in range(30):
            eng = Engine(rules=rules, seed=seed, policy=PassivePolicy())
            eng._apply_op({"op": "suppress_clock", "severity": 8}, None, "t", [])
            for _ in range(eng.consts["leak_clock_turns"] + 1):
                log = []
                eng._process_suppress_clocks(log)
                total += sum(1 for e in log if e["event"] == "leak")
                if not eng.world.player.suppress_clocks:
                    break
        return total
    assert leaks_under(0.95) > leaks_under(0.2)


def test_suppress_clocks_serialize_for_determinism():
    eng = Engine(seed=3, policy=PassivePolicy())
    _suppress_op(eng, severity=8, node="bamako")
    assert '"suppress_clocks"' in eng.checkpoint()
    a = Engine(seed=3, policy=PassivePolicy())
    b = Engine(seed=3, policy=PassivePolicy())
    a._apply_op({"op": "suppress_clock", "severity": 8}, "bamako", "t", [])
    b._apply_op({"op": "suppress_clock", "severity": 8}, "bamako", "t", [])
    for _ in range(15):
        a.run_turn()
        b.run_turn()
    assert a.state_hash() == b.state_hash()


def test_arc_dial_events_use_suppress():
    """The Arc deck must actually wire the dial — at least one card offers a
    suppress_clock choice (else the system is dead data)."""
    rules = load_rules(scenario="sahel_arc")
    has_suppress = any(
        eff.get("op") == "suppress_clock"
        for card in rules["events"] for ch in card["choices"] for eff in ch["effects"]
    )
    assert has_suppress
