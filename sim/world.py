"""World state: rules loading and the mutable state vectors of DESIGN.md §18.2.

All rules live in JSON under rules/ (the architectural law, §13.2). This module
is the only place that reads them. Runtime fields the engine owns (ops_pressure,
partner_capacity, coup_risk, interdiction, links, uncontested counters) are
initialized here and never appear in the data files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

RULES_DIR = Path(__file__).resolve().parent.parent / "rules"

RULE_FILES = ("nodes", "edges", "factions", "initiatives", "events", "constants")


def load_rules(rules_dir: Path | None = None) -> dict:
    """Load every rules file into one dict keyed by file stem."""
    base = Path(rules_dir) if rules_dir is not None else RULES_DIR
    rules = {}
    for name in RULE_FILES:
        with open(base / f"{name}.json", encoding="utf-8") as fh:
            rules[name] = json.load(fh)
    return rules


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


@dataclass
class Presence:
    strength: float = 0.0
    entrenchment: float = 0.0
    visibility: float = 0.0

    def to_dict(self) -> dict:
        return {
            "strength": round(self.strength, 4),
            "entrenchment": round(self.entrenchment, 4),
            "visibility": round(self.visibility, 4),
        }


@dataclass
class Node:
    id: str
    name: str
    country: str
    capital: bool
    governance: float
    development: float
    grievance: float
    population_k: float
    access: float
    government: str
    local_legitimacy: float
    intel_base: float
    patron_influence: dict[str, float]
    presence: dict[str, Presence]
    resources: list[str] = field(default_factory=list)
    # runtime, engine-owned
    ops_pressure: float = 0.0
    intel_coverage: float = 0.0
    partner_capacity: float = 0.0
    uncontested_turns: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "country": self.country,
            "capital": self.capital,
            "governance": round(self.governance, 4),
            "development": round(self.development, 4),
            "grievance": round(self.grievance, 4),
            "government": self.government,
            "local_legitimacy": round(self.local_legitimacy, 4),
            "intel_coverage": round(self.intel_coverage, 4),
            "ops_pressure": round(self.ops_pressure, 4),
            "partner_capacity": round(self.partner_capacity, 4),
            "patron_influence": {k: round(v, 4) for k, v in sorted(self.patron_influence.items())},
            "presence": {f: p.to_dict() for f, p in sorted(self.presence.items())},
            "uncontested_turns": dict(sorted(self.uncontested_turns.items())),
        }


@dataclass
class Edge:
    id: str
    a: str
    b: str
    types: list[str]
    capacity: float
    interdiction: float = 0.0  # runtime; capped below 1.0 — never fully closable (§4)

    def touches(self, node_id: str) -> bool:
        return node_id in (self.a, self.b)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "a": self.a,
            "b": self.b,
            "capacity": round(self.capacity, 4),
            "interdiction": round(self.interdiction, 4),
        }


@dataclass
class Faction:
    id: str
    name: str
    composite_of: str
    ideology: list[str]
    sponsor: str | None
    capability_tier: int
    relations: dict[str, float]
    links: list[dict] = field(default_factory=list)  # runtime: {"with": id, "turn": n}

    def linked_with(self, other_id: str) -> bool:
        return any(link["with"] == other_id for link in self.links)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "capability_tier": self.capability_tier,
            "links": sorted(self.links, key=lambda x: (x["with"], x["turn"])),
        }


@dataclass
class PlayerState:
    domestic: float
    international: float
    treasury: float
    mandate: int = 0
    authoritarian_drift: int = 0
    casualties: int = 0
    turns_since_election: int = 0
    honeymoon_left: int = 0
    spent_total: float = 0.0
    suppress_clocks: list[dict] = field(default_factory=list)  # reserved for v0.6

    def to_dict(self) -> dict:
        return {
            "domestic": round(self.domestic, 4),
            "international": round(self.international, 4),
            "treasury": round(self.treasury, 4),
            "mandate": self.mandate,
            "authoritarian_drift": self.authoritarian_drift,
            "casualties": self.casualties,
            "turns_since_election": self.turns_since_election,
            "honeymoon_left": self.honeymoon_left,
            "spent_total": round(self.spent_total, 4),
        }


@dataclass
class WorldState:
    turn: int
    nodes: dict[str, Node]
    edges: list[Edge]
    factions: dict[str, Faction]
    player: PlayerState
    coup_risk: dict[str, float]
    collapsed: dict[str, bool]
    proto_blocs: list[list[str]] = field(default_factory=list)

    def nodes_sorted(self) -> list[Node]:
        return [self.nodes[k] for k in sorted(self.nodes)]

    def factions_sorted(self) -> list[Faction]:
        return [self.factions[k] for k in sorted(self.factions)]

    def country_nodes(self, country: str) -> list[Node]:
        return [n for n in self.nodes_sorted() if n.country == country]

    def countries(self) -> list[str]:
        return sorted({n.country for n in self.nodes.values()})

    def capital_of(self, country: str) -> Node | None:
        for node in self.country_nodes(country):
            if node.capital:
                return node
        return None

    def edges_of(self, node_id: str) -> list[Edge]:
        return [e for e in self.edges if e.touches(node_id)]

    def avg_grievance(self) -> float:
        nodes = self.nodes_sorted()
        return sum(n.grievance for n in nodes) / len(nodes)

    def junta_count(self) -> int:
        return sum(
            1 for c in self.countries()
            if (cap := self.capital_of(c)) is not None and cap.government in ("junta", "emirate")
        )

    def to_dict(self) -> dict:
        return {
            "turn": self.turn,
            "nodes": {k: n.to_dict() for k, n in sorted(self.nodes.items())},
            "edges": [e.to_dict() for e in sorted(self.edges, key=lambda e: e.id)],
            "factions": {k: f.to_dict() for k, f in sorted(self.factions.items())},
            "player": self.player.to_dict(),
            "coup_risk": {k: round(v, 4) for k, v in sorted(self.coup_risk.items())},
            "collapsed": dict(sorted(self.collapsed.items())),
            "proto_blocs": sorted(self.proto_blocs),
        }


def build_world(rules: dict) -> WorldState:
    consts = rules["constants"]
    factions = {
        f["id"]: Faction(
            id=f["id"],
            name=f["name"],
            composite_of=f["composite_of"],
            ideology=list(f["ideology"]),
            sponsor=f.get("sponsor"),
            capability_tier=f["capability_tier"],
            relations=dict(f.get("relations", {})),
        )
        for f in rules["factions"]
    }
    nodes = {}
    for n in rules["nodes"]:
        presence = {
            fid: Presence(p["strength"], p["entrenchment"], p["visibility"])
            for fid, p in n.get("presence", {}).items()
        }
        nodes[n["id"]] = Node(
            id=n["id"],
            name=n["name"],
            country=n["country"],
            capital=n["capital"],
            governance=n["governance"],
            development=n["development"],
            grievance=n["grievance"],
            population_k=n["population_k"],
            access=n["access"],
            government=n.get("government", "civilian"),
            local_legitimacy=n["local_legitimacy"],
            intel_base=n["intel_coverage"],
            intel_coverage=n["intel_coverage"],
            patron_influence=dict(n.get("patron_influence", {})),
            presence=presence,
            resources=list(n.get("resources", [])),
        )
    edges = [
        Edge(id=e["id"], a=e["a"], b=e["b"], types=list(e["types"]), capacity=e["capacity"])
        for e in rules["edges"]
    ]
    countries = sorted({n.country for n in nodes.values()})
    player = PlayerState(
        domestic=consts["starting"]["domestic"],
        international=consts["starting"]["international"],
        treasury=consts["starting"]["treasury"],
    )
    return WorldState(
        turn=0,
        nodes=nodes,
        edges=edges,
        factions=factions,
        player=player,
        coup_risk={c: 0.0 for c in countries},
        collapsed={c: False for c in countries},
    )
