"""Every rules file validates against its schema, and the dataset is
referentially intact. The schemas are normative (DESIGN.md §18.2); Pillar 3
is enforced here too — an initiative without a documented backfire channel
is a schema violation, not a balance choice."""

import json
from pathlib import Path

import jsonschema
import pytest

RULES = Path(__file__).resolve().parent.parent / "rules"
SCHEMAS = RULES / "schema"

PAIRS = [
    ("nodes.json", "node.schema.json"),
    ("edges.json", "edge.schema.json"),
    ("factions.json", "faction.schema.json"),
    ("initiatives.json", "initiative.schema.json"),
    ("events.json", "event.schema.json"),
    ("constants.json", "constants.schema.json"),
    ("patrons.json", "patrons.schema.json"),
]


def load(path: Path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.mark.parametrize(("data_file", "schema_file"), PAIRS)
def test_rules_validate(data_file, schema_file):
    jsonschema.validate(load(RULES / data_file), load(SCHEMAS / schema_file))


def test_referential_integrity():
    nodes = {n["id"] for n in load(RULES / "nodes.json")}
    factions = {f["id"] for f in load(RULES / "factions.json")}
    for edge in load(RULES / "edges.json"):
        assert edge["a"] in nodes and edge["b"] in nodes, f"dangling edge {edge['id']}"
        assert edge["a"] != edge["b"], f"self-loop {edge['id']}"
    for node in load(RULES / "nodes.json"):
        for fid in node.get("presence", {}):
            assert fid in factions, f"unknown faction {fid} in node {node['id']}"
    for faction in load(RULES / "factions.json"):
        for other in faction.get("relations", {}):
            assert other in factions, f"unknown relation target {other} in {faction['id']}"


def test_every_initiative_documents_its_backfire():
    for init in load(RULES / "initiatives.json"):
        note = init["backfire"]["note"]
        assert len(note) > 20, f"{init['id']}: backfire note must actually explain the channel"


def test_capitals_exist_for_collapsible_countries():
    nodes = load(RULES / "nodes.json")
    countries_with_capital = {n["country"] for n in nodes if n["capital"]}
    assert {"ML", "BF"} <= countries_with_capital  # NE's capital is off-map at lite scale


def test_all_five_families_present():
    families = {i["family"] for i in load(RULES / "initiatives.json")}
    assert families == {"military", "governance", "intelligence", "diplomatic", "domestic"}
