"""Engine contracts: the itemized ledger (DESIGN.md §18.6), mandate bounds,
turn-report shape, and smoke runs across every built-in policy."""

import pytest

from sim import POLICIES, Engine, PassivePolicy, PureKineticPolicy


def test_ledger_itemization_matches_gauge_movement():
    """The hard requirement: every gauge moves exactly by the sum of its
    itemized entries — nothing mutates legitimacy behind the ledger's back."""
    eng = Engine(seed=3, policy=PureKineticPolicy())
    node_ids = sorted(eng.world.nodes)
    for _ in range(40):
        before_d = eng.world.player.domestic
        before_i = eng.world.player.international
        before_local = {nid: eng.world.nodes[nid].local_legitimacy for nid in node_ids}
        turn = eng.world.turn
        eng.run_turn()
        assert eng.world.player.domestic - before_d == pytest.approx(
            eng.ledger.sum_for(turn, "domestic"), abs=1e-9
        )
        assert eng.world.player.international - before_i == pytest.approx(
            eng.ledger.sum_for(turn, "international"), abs=1e-9
        )
        for nid in node_ids:
            assert eng.world.nodes[nid].local_legitimacy - before_local[nid] == pytest.approx(
                eng.ledger.sum_for(turn, f"local:{nid}"), abs=1e-9
            )


def test_mandate_income_bounds():
    eng = Engine(seed=0)
    consts = eng.consts
    for _ in range(70):  # crosses one election
        report = eng.run_turn()
        assert report["mandate_income"] >= 1
        assert report["mandate_income"] <= round(
            consts["mandate_base"] * 1.5 * consts["honeymoon_mult"]
        )


def test_turn_report_shape():
    eng = Engine(seed=1, policy=PureKineticPolicy())
    report = eng.run_turn()
    for key in ("turn", "date", "mandate_income", "orders", "ledger", "growth",
                "events", "log", "gauges"):
        assert key in report
    assert report["turn"] == 0
    assert report["date"] == "2012-01"
    # growth entries are itemized term by term — causes, not net effects
    assert all(
        {"recruitment", "external_support", "alliance_bonus", "attrition", "defection"}
        == set(entry["terms"])
        for entry in report["growth"]
    )


def test_date_arithmetic():
    eng = Engine(seed=0)
    eng.run(13)
    assert eng.date_str() == "2013-02"


@pytest.mark.parametrize("policy_name", sorted(POLICIES))
def test_smoke_60_turns_all_policies(policy_name):
    eng = Engine(seed=11, policy=POLICIES[policy_name]())
    eng.run(60)
    player = eng.world.player
    assert 0 <= player.domestic <= 100
    assert 0 <= player.international <= 100
    for node in eng.world.nodes_sorted():
        assert 0 <= node.local_legitimacy <= 100
        for pres in node.presence.values():
            assert 0 <= pres.strength <= 100
            assert 0 <= pres.entrenchment <= 100
            assert 0 <= pres.visibility <= 100
    score = eng.score()
    assert set(score) >= {"stabilization", "order_mult", "integrity_mult", "costs", "final"}
    assert len(eng.history) == 60  # post-mortem spine: one true snapshot per turn


def test_passive_player_never_pays_blood_or_drift():
    eng = Engine(seed=4, policy=PassivePolicy())
    eng.run(60)
    assert eng.world.player.casualties == 0
    assert eng.world.player.authoritarian_drift == 0


def test_unaffordable_orders_rejected_not_partial():
    class Spendthrift(PureKineticPolicy):
        def choose(self, briefing, actions):
            return [{"initiative": "presence_patrols", "node": "mopti"}] * 50

    eng = Engine(seed=2, policy=Spendthrift())
    report = eng.run_turn()
    assert 0 < len(report["orders"]) < 50
    assert eng.world.player.mandate >= 0
    assert eng.world.player.treasury >= 0
