"""Global arms & oil markets and the multi-patron rivalry (DESIGN.md §21/§8) —
the v0.11 "deepen the ripples" systems. Same discipline as norms: live in grand
mode, dormant (and so calibration-safe) in single-theater play."""

import pytest

from sim import Engine, PassivePolicy, PureKineticPolicy, load_rules
from sim import markets as markets_mod
from sim import patrons as patrons_mod


def grand(**kw):
    return Engine(rules=load_rules(scenario="grand"), **kw)


# ---------------------------------------------------------------- arms market

def test_world_conflict_heats_the_arms_market_and_lifts_supply_everywhere():
    eng = grand(seed=2, policy=PassivePolicy())
    eng.run(60)
    # an unopposed world is a violent one → the arms market runs hot
    assert eng.world.markets["arms"] > 55
    # and a hot arms market arms insurgencies in every theater
    assert markets_mod.arms_mult(eng.world, eng.consts) > 1.0


def test_oil_market_drags_domestic_in_a_grand_run():
    eng = grand(seed=1, policy=PassivePolicy())
    eng.run(60)
    saw_oil = any(
        e["source"] == "oil_market" for r in eng.reports for e in r["ledger"]
    )
    assert saw_oil, "the oil market should move Domestic at least once"


# ---------------------------------------------------------------- multi-patron

def test_the_patron_contest_is_real():
    """In grand mode more than one patron archetype should win reach — Iran's
    neighbourhood and China's economic sphere carve out their own, not a single
    mercenary sweep."""
    eng = grand(seed=3, policy=PassivePolicy())
    eng.run(100)
    winners = [p for p, v in eng.world.patron_strength.items() if v > 5]
    assert len(winners) >= 2, "the allegiance market should be a contest, not a monopoly"


def test_rivalry_tracks_the_share_of_the_world_captured():
    eng = grand(seed=0, policy=PassivePolicy())
    eng.run(100)
    assert eng.world.rivalry > 0, "as states fall the rival bloc's rivalry score rises"


def test_designation_strips_a_patron_globally():
    """Deny a patron one state and it is weaker in all of them (§8) — the clearest
    'every choice connects' payoff."""
    eng = grand(seed=4, policy=PassivePolicy())
    eng.run(40)
    # find a country with a backing patron and force the evidence in
    country = next(c for c in eng.world.countries()
                   if (cap := eng.world.capital_of(c)) and cap.government != "civilian")
    patron = patrons_mod.dominant_patron(eng.world, country)
    eng.world.patron_strength[patron] = 60.0
    eng.world.exposure[country] = 80.0
    cap = eng.world.capital_of(country)
    eng._designate(cap.id, "sanc", [])
    assert eng.world.patron_strength[patron] < 60.0


# ---------------------------------------------------------------- gating

def test_markets_and_rivalry_dormant_in_single_theater():
    eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=2, policy=PureKineticPolicy())
    eng.run(60)
    assert eng.world.markets == {"arms": 50.0, "oil": 50.0}
    assert eng.world.rivalry == 0.0
    assert markets_mod.arms_mult(eng.world, eng.consts) == 1.0
    assert not any(
        e["source"] == "oil_market" for r in eng.reports for e in r["ledger"]
    )


def test_patrons_data_validates_and_loads():
    import json
    from pathlib import Path
    rules = Path(__file__).resolve().parent.parent / "rules"
    import jsonschema
    with open(rules / "patrons.json") as fh:
        data = json.load(fh)
    with open(rules / "schema/patrons.schema.json") as fh:
        schema = json.load(fh)
    jsonschema.validate(data, schema)
    ids = {p["id"] for p in data}
    assert {"mercenary", "investor", "proxy"} <= ids


@pytest.mark.parametrize("seed", [0, 1])
def test_grand_with_markets_deterministic(seed):
    a = grand(seed=seed, policy=PassivePolicy())
    b = grand(seed=seed, policy=PassivePolicy())
    a.run(60)
    b.run(60)
    assert a.state_hash() == b.state_hash()
    for k in ('"markets"', '"patron_strength"', '"rivalry"'):
        assert k in a.checkpoint()
