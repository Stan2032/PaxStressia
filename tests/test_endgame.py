"""v0.7 endgame systems — the Exposure system (§20), the negotiation endgame
(§7), bloc consolidation (§5.4), and the patron allegiance market (§8). These
are the tools that make the arc *winnable* and bring Stan's expose-the-regime
mechanic alive."""

from sim import Engine, MixedPolicy, PassivePolicy
from sim.world import load_rules

ARC = lambda **kw: Engine(rules=load_rules(scenario="sahel_arc"), **kw)  # noqa: E731


# ---------------------------------------------------------------- Exposure (§20)

def test_exposure_op_raises_and_decays():
    eng = ARC(seed=0, policy=PassivePolicy())
    eng._apply_op({"op": "exposure", "delta": 30}, "bamako", "test", [])
    assert eng.world.exposure["ML"] == 30
    # decays without upkeep (patrons.decay_exposure runs each turn)
    eng.run(5)
    assert 0 < eng.world.exposure["ML"] < 30


def test_fund_research_builds_exposure_over_a_run():
    class Funder(PassivePolicy):
        name = "funder"
        def choose(self, briefing, actions):
            return [{"initiative": "fund_research", "node": "bamako"}]

    eng = ARC(seed=1, policy=Funder())
    eng.run(20)
    assert eng.world.exposure["ML"] > 20, "sustained funding should accumulate Exposure"


# ---------------------------------------------------------------- Designations

def test_designation_needs_evidence():
    """Below the Exposure threshold a designation is a thin case: it fails and
    costs a little International. Above it, it bites."""
    weak = ARC(seed=2)
    intl0 = weak.world.player.international
    weak._apply_op({"op": "designate"}, "bamako", "sanc", [])
    assert weak.world.player.international < intl0  # thin case penalised

    strong = ARC(seed=2)
    strong.world.exposure["ML"] = 80
    strong.world.nodes["bamako"].patron_influence["mercenary"] = 40
    intl1 = strong.world.player.international
    strong._apply_op({"op": "designate"}, "bamako", "sanc", [])
    assert strong.world.player.international > intl1
    assert strong.world.exposure["ML"] < 80  # evidence spent
    assert strong.world.nodes["bamako"].patron_influence["mercenary"] < 40  # patron stripped


# ---------------------------------------------------------------- Negotiation (§7)

def test_negotiation_settles_a_stalemated_faction():
    eng = ARC(seed=3)
    node = eng.world.nodes["gao"]
    target = max(node.presence, key=lambda f: node.presence[f].strength)
    # nudge into the stalemate band
    node.presence[target].strength = 50.0
    intl0 = eng.world.player.international
    dom0 = eng.world.player.domestic
    eng._apply_op({"op": "negotiate"}, "gao", "talks", [])
    assert node.presence[target].strength < 50.0, "settlement should drain Forces"
    assert eng.world.player.international > intl0, "a clean exit earns International"
    assert eng.world.player.domestic < dom0, "and costs 'soft on terror' at home"


def test_negotiation_fails_outside_the_stalemate_band():
    eng = ARC(seed=4)
    node = eng.world.nodes["gao"]
    target = max(node.presence, key=lambda f: node.presence[f].strength)
    node.presence[target].strength = 95.0  # too strong to settle
    before = node.presence[target].strength
    eng._apply_op({"op": "negotiate"}, "gao", "talks", [])
    assert node.presence[target].strength == before, "no settlement when not stalemated"


# ---------------------------------------------------------------- Blocs (§5.4)

def test_bloc_forms_and_consolidates():
    eng = ARC(seed=0, policy=PassivePolicy())
    eng.run(168)
    assert eng.world.blocs, "adjacent juntas should federate into a bloc"
    assert max(b["stage"] for b in eng.world.blocs) > 1.0, "the clock should advance"
    propaganda = any(
        e["source"] == "bloc_propaganda"
        for r in eng.reports for e in r["ledger"]
    )
    assert propaganda, "a consolidated bloc should drain International via propaganda"


def test_designation_rolls_back_consolidation():
    eng = ARC(seed=0, policy=PassivePolicy())
    eng.run(168)
    bloc = eng.world.blocs[0]
    country = bloc["countries"][0]
    eng.world.exposure[country] = 90
    stage_before = bloc["stage"]
    cap = eng.world.capital_of(country)
    eng._apply_op({"op": "designate"}, cap.id, "sanc", [])
    assert eng.world.blocs[0]["stage"] < stage_before


# ---------------------------------------------------------------- Patron market (§8)

def test_higher_standing_resists_patron_capture():
    """The allegiance market (§8): a strong, credible offer slows the no-strings
    patron. Same junta, different International ⇒ different capture speed."""
    def capture_after(international: float) -> float:
        eng = ARC(seed=5)
        eng.world.collapsed["ML"] = True
        for n in eng.world.country_nodes("ML"):
            n.government = "junta"
            n.patron_influence["mercenary"] = 10.0
        eng.world.player.international = international
        from sim import patrons
        for _ in range(10):
            patrons.market(eng.world, eng.consts)
        return eng.world.nodes["bamako"].patron_influence["mercenary"]

    assert capture_after(20) > capture_after(90), "weak standing ⇒ faster patron capture"


# ---------------------------------------------------------------- Plumbing

def test_endgame_state_serializes_and_stays_deterministic():
    a = ARC(seed=7, policy=MixedPolicy())
    b = ARC(seed=7, policy=MixedPolicy())
    a.run(60)
    b.run(60)
    assert a.state_hash() == b.state_hash()
    assert '"exposure"' in a.checkpoint() and '"blocs"' in a.checkpoint()


def test_calibration_unbroken_by_endgame_systems():
    """The enforced history calibration must survive the new systems — a passive
    Mali still falls to a junta in the window (smoke of the §12 baseline)."""
    eng = ARC(seed=0, policy=PassivePolicy())
    eng.run(168)
    cap = eng.world.capital_of("ML")
    assert cap.government == "junta"
