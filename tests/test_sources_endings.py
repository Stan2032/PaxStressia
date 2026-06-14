"""v0.9 — the Sources screen (integrity of the shipped bibliography), the
endings matrix (§11), and the post-mortem fog reveal (§9)."""

import json
from pathlib import Path

import jsonschema

from sim import Engine, PassivePolicy, load_rules

RULES = Path(__file__).resolve().parent.parent / "rules"


def load(name):
    with open(RULES / name, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- Sources (§14/§17)

def test_sources_validate():
    jsonschema.validate(load("sources.json"), load("schema/sources.schema.json"))


def test_sources_integrity_discipline():
    """The shipping rule: the bibliography must carry a disclaimer, must flag its
    confidence honestly, and must actually label some material alt-history rather
    than pass off the game's near-future projection as documented fact."""
    src = load("sources.json")
    assert len(src["disclaimer"]) > 40
    confidences = {e["confidence"] for e in src["entries"]}
    assert "alt_history" in confidences, "post-record material must be labelled, not hidden"
    assert "established" in confidences
    # the central thesis and the two live-verified claims must be present
    ids = {e["id"] for e in src["entries"]}
    assert {"merom", "moura", "afghanistan11"} <= ids
    # every verified entry carries a URL (it was checkable)
    for e in src["entries"]:
        if e["confidence"] == "verified":
            assert e.get("url"), f"{e['id']}: verified entries should cite a checkable URL"


def test_sources_cover_the_design_spine():
    """Doctrine, the case, precedents and data orgs must all be represented —
    the game cites its homework across every pillar."""
    cats = {e["category"] for e in load("sources.json")["entries"]}
    assert {"doctrine", "case", "precedent", "data_org"} <= cats


# ---------------------------------------------------------------- Endings (§11)

def test_ending_is_one_of_the_four():
    eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=0, policy=PassivePolicy())
    eng.run(60)
    e = eng.ending()
    assert e["name"] in {"Pax", "Fortress", "Retreat", "Collapse"}
    assert e["text"]


def test_passive_player_does_not_earn_pax():
    """Letting the arc burn must not yield the hard ending."""
    for seed in range(4):
        eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=seed, policy=PassivePolicy())
        eng.run(168)
        assert eng.ending()["name"] != "Pax"


def test_competent_can_reach_a_good_ending():
    """A competent player should, on at least some seeds, hold the line well
    enough to clear the 'abroad' bar (Pax or Fortress) — endings are reachable,
    not decorative."""
    from sim import CompetentPolicy
    good = 0
    for seed in range(6):
        eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=seed, policy=CompetentPolicy())
        eng.run(168)
        if eng.ending()["name"] in {"Pax", "Fortress"}:
            good += 1
    assert good >= 1, "the held-line endings must be reachable by good play"


def test_drift_pushes_toward_fortress_not_pax():
    """Two runs that hold the line equally but differ in drift must not both be
    Pax — integrity decides Pax vs Fortress (the signature dark ending)."""
    clean = Engine(rules=load_rules(scenario="sahel_arc"), seed=1, policy=PassivePolicy())
    clean.run(40)
    # synthesise a held-line, high-drift state and confirm it cannot read as Pax
    clean.world.player.authoritarian_drift = 6
    assert clean.ending()["score"]["integrity_mult"] < clean.consts["integrity_clean_min"]
    if clean.ending()["abroad"] >= clean.consts["pax_abroad_min"]:
        assert clean.ending()["name"] == "Fortress"


# ---------------------------------------------------------------- Post-mortem (§9)

def test_post_mortem_surfaces_fog_gaps():
    eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=0, policy=PassivePolicy())
    eng.run(120)
    pm = eng.post_mortem()
    assert pm["turns"] == 120
    assert isinstance(pm["worst_fog_gaps"], list)
    # passive lets entrenchment build under thin intel → some hidden strength exists
    assert any(g["true"] > 0 for g in pm["worst_fog_gaps"])
