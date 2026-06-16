"""Grand mode (DESIGN.md §21): the world-scale board and the global norms /
precedent layer that makes every choice ripple into every theater at once.

The discipline under test: the layer is LIVE in grand mode (choices propagate
worldwide through plausible channels) but DORMANT in single-theater scenarios
(so the Sahel history calibration is untouched by construction)."""

import json
from pathlib import Path

import jsonschema
import pytest

from sim import Engine, PassivePolicy, PureHeartsMindsPolicy, PureKineticPolicy, load_rules
from sim import norms as norms_mod

RULES = Path(__file__).resolve().parent.parent / "rules"
GRAND = RULES / "scenarios" / "grand"


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def test_grand_data_validates():
    jsonschema.validate(load(GRAND / "nodes.json"), load(RULES / "schema/node.schema.json"))
    jsonschema.validate(load(GRAND / "edges.json"), load(RULES / "schema/edge.schema.json"))
    jsonschema.validate(load(GRAND / "factions.json"), load(RULES / "schema/faction.schema.json"))
    jsonschema.validate(load(GRAND / "scenario.json"), load(RULES / "schema/scenario.schema.json"))
    # scenario constants are a PARTIAL override (§18.9) — validate the MERGED result
    jsonschema.validate(load_rules(scenario="grand")["constants"],
                        load(RULES / "schema/constants.schema.json"))


def test_grand_is_a_world_not_a_region():
    rules = load_rules(scenario="grand")
    assert len(rules["nodes"]) >= 36, "grand mode should span the world (v0.12: ~40 nations)"
    theaters = {n.get("theater") for n in rules["nodes"]}
    assert len(theaters) >= 12, "nations should span many theaters"
    # inter-theater edges exist (the global network, not isolated regions)
    by_theater = {n["id"]: n.get("theater") for n in rules["nodes"]}
    cross = [e for e in rules["edges"] if by_theater[e["a"]] != by_theater[e["b"]]]
    assert cross, "there must be cross-theater edges — the world is connected"


def test_grand_referential_integrity():
    nodes = {n["id"] for n in load(GRAND / "nodes.json")}
    factions = {f["id"] for f in load(GRAND / "factions.json")}
    for e in load(GRAND / "edges.json"):
        assert e["a"] in nodes and e["b"] in nodes, f"dangling edge {e['id']}"
    for n in load(GRAND / "nodes.json"):
        for fid in n.get("presence", {}):
            assert fid in factions


@pytest.mark.parametrize("seed", [0, 1])
def test_grand_full_horizon_deterministic_and_in_range(seed):
    a = Engine(rules=load_rules(scenario="grand"), seed=seed, policy=PassivePolicy())
    b = Engine(rules=load_rules(scenario="grand"), seed=seed, policy=PassivePolicy())
    a.run(100)
    b.run(100)
    assert a.state_hash() == b.state_hash()
    assert '"norms"' in a.checkpoint()
    for n in a.world.nodes_sorted():
        assert 0 <= n.local_legitimacy <= 100
        for p in n.presence.values():
            assert 0 <= p.strength <= 100 and 0 <= p.entrenchment <= 100
    for v in a.world.norms.values():
        assert 0 <= v <= 100


def test_global_precedent_ripples_worldwide():
    """The keystone: a kinetic way of war raises the world kinetic norm and the
    GLOBAL recruitment multiplier; a lawful one lowers it. The choice in some
    theaters changes insurgency in all of them."""
    kin = Engine(rules=load_rules(scenario="grand"), seed=5, policy=PureKineticPolicy())
    law = Engine(rules=load_rules(scenario="grand"), seed=5, policy=PureHeartsMindsPolicy())
    kin.run(60)
    law.run(60)
    assert kin.world.norms["kinetic"] > 70
    assert law.world.norms["rule_of_law"] > 70
    assert norms_mod.recruit_multiplier(kin.world, kin.consts) > 1.0
    assert norms_mod.recruit_multiplier(law.world, law.consts) < 1.0
    # and the precedent is punished/rewarded at the world table (International)
    assert any(e["source"] == "world_norms" for r in kin.reports for e in r["ledger"])


def test_norms_dormant_in_single_theater():
    """norm_feedback is 0 in the Sahel scenario, so even a kinetic player never
    moves the world norms or the recruit multiplier — the calibration is safe
    by construction."""
    eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=2, policy=PureKineticPolicy())
    eng.run(60)
    assert eng.world.norms == {"kinetic": 50.0, "rule_of_law": 50.0, "autocracy": 50.0}
    assert norms_mod.recruit_multiplier(eng.world, eng.consts) == 1.0


def test_sahel_calibration_unbroken_by_grand_work():
    """Smoke of the enforced baseline: a passive Mali still falls to a junta in
    the window after all the grand-mode engine changes."""
    eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=0, policy=PassivePolicy())
    eng.run(168)
    assert eng.world.capital_of("ML").government == "junta"
    assert eng.world.norms["kinetic"] == 50.0  # untouched
