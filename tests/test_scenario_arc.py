"""Scenario 1 — "The Arc" (rules/scenarios/sahel_arc): schema validity,
referential integrity, scenario loading semantics, and full-horizon runs
exercising v0.4 systems (spread, once-beats, presence/patron ops)."""

import json
from pathlib import Path

import jsonschema
import pytest

from sim import Engine, PassivePolicy, load_rules

RULES = Path(__file__).resolve().parent.parent / "rules"
ARC = RULES / "scenarios" / "sahel_arc"
SCHEMAS = RULES / "schema"


def load(path: Path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.mark.parametrize(("data_file", "schema_file"), [
    ("scenario.json", "scenario.schema.json"),
    ("nodes.json", "node.schema.json"),
    ("edges.json", "edge.schema.json"),
    ("factions.json", "faction.schema.json"),
    ("events.json", "event.schema.json"),
])
def test_arc_files_validate(data_file, schema_file):
    jsonschema.validate(load(ARC / data_file), load(SCHEMAS / schema_file))


def test_arc_referential_integrity():
    nodes = {n["id"] for n in load(ARC / "nodes.json")}
    factions = {f["id"] for f in load(ARC / "factions.json")}
    assert len(nodes) == 12 and len(factions) == 3
    for edge in load(ARC / "edges.json"):
        assert edge["a"] in nodes and edge["b"] in nodes, f"dangling edge {edge['id']}"
    for node in load(ARC / "nodes.json"):
        for fid in node.get("presence", {}):
            assert fid in factions
    node_targets = {
        eff["node"]
        for card in load(ARC / "events.json") for ch in card["choices"]
        for eff in ch["effects"] if "node" in eff
    }
    assert node_targets <= nodes, f"event ops target unknown nodes: {node_targets - nodes}"
    faction_targets = {
        eff["faction"]
        for card in load(ARC / "events.json") for ch in card["choices"]
        for eff in ch["effects"] if "faction" in eff
    }
    assert faction_targets <= factions


def test_scenario_loading_semantics():
    base = load_rules()
    arc = load_rules(scenario="sahel_arc")
    assert len(arc["nodes"]) == 12 and len(base["nodes"]) == 6  # replace, not merge
    assert arc["initiatives"] == base["initiatives"]  # fall-through for absent files
    assert arc["constants"] == base["constants"]  # no constants override in the arc
    assert arc["scenario"]["id"] == "sahel_arc"


def test_arc_collapsible_countries():
    # Unlike Sahel-lite, all three states have on-map capitals; the marker doesn't.
    rules = load_rules(scenario="sahel_arc")
    eng = Engine(rules=rules, seed=0)
    for country in ("ML", "BF", "NE"):
        assert eng.world.capital_of(country) is not None
    assert eng.world.capital_of("GLF") is None


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_arc_full_horizon_passive_run(seed):
    eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=seed, policy=PassivePolicy())
    eng.run(168)
    for node in eng.world.nodes_sorted():
        assert 0 <= node.local_legitimacy <= 100
        for pres in node.presence.values():
            assert 0 <= pres.strength <= 100
            assert 0 <= pres.entrenchment <= 100
    # once-beats never repeat
    fired = [
        ev["id"] for report in eng.reports for ev in report["events"]
    ]
    deck = {c["id"]: c for c in eng.rules["events"]}
    for event_id in set(fired):
        if deck[event_id].get("once"):
            assert fired.count(event_id) == 1, f"once-beat {event_id} repeated"


def test_narrative_chains_are_consistent():
    """The §20.2 named-people arcs use `requires_fired`: every chained event must
    reference a real setup event, and across passive runs a 'kept' beat must never
    fire without its 'met' beat — the chain primitive holds, and the arcs complete."""
    rules = load_rules(scenario="sahel_arc")
    deck = {c["id"] for c in rules["events"]}
    chained = [c for c in rules["events"] if "requires_fired" in c.get("requires", {})]
    assert chained, "the arc deck should carry narrative chains (named-people arcs)"
    for c in chained:
        assert c["requires"]["requires_fired"] in deck, \
            f"{c['id']} chains off a missing event"
    completed = False
    for seed in range(6):
        eng = Engine(rules=load_rules(scenario="sahel_arc"), seed=seed, policy=PassivePolicy())
        eng.run(168)
        fired = eng.world.fired_events
        for c in chained:
            if c["id"] in fired:
                assert c["requires"]["requires_fired"] in fired, \
                    f"{c['id']} fired without its setup"
                completed = True
    assert completed, "named-people arcs should complete (met → kept) in some passive run"


def test_spread_ignites_empty_nodes():
    """The arc's historical test for the v0.4 spread mechanic: regions that
    start empty (northern Burkina, the coastal marker's neighbors) must be
    reachable by momentum over edges — in at least most passive runs."""
    ignitions = 0
    for seed in range(4):
        rules = load_rules(scenario="sahel_arc")
        empty_at_start = {
            n["id"] for n in rules["nodes"] if not n.get("presence")
        }
        eng = Engine(rules=rules, seed=seed, policy=PassivePolicy())
        eng.run(168)
        gained = {
            n.id for n in eng.world.nodes_sorted()
            if n.id in empty_at_start
            and any(p.strength > 5 for p in n.presence.values())
        }
        if gained:
            ignitions += 1
    assert ignitions >= 3, "spread should ignite initially-empty regions in most runs"


def test_spread_is_deterministic():
    a = Engine(rules=load_rules(scenario="sahel_arc"), seed=9)
    b = Engine(rules=load_rules(scenario="sahel_arc"), seed=9)
    a.run(80)
    b.run(80)
    assert a.state_hash() == b.state_hash()
