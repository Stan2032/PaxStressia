"""Bloc formation & the consolidation clock (DESIGN.md §5.4, v0.7).

Adjacent non-civilian states federate into a Bloc that runs an institutional
consolidation clock — joint forces, shared patron, pooled propaganda. *Left
alone, it grows; connected, it accelerates.* The longer a bloc exists, the more
its propaganda drains your International standing and the more grievance it
exports to its civilian neighbours. Exposure (§20) is the counter: documented
truth blunts the propaganda and (via sanctions) rolls the clock back.

This replaces the v0.2 detection-only stub. `world.proto_blocs` is kept in sync
as the list of member-country groups so older scoring/logging still reads it.
"""

from __future__ import annotations

from .legitimacy import INTERNATIONAL, Ledger, local_gauge
from .world import WorldState, clamp


def _hostile_countries(world: WorldState) -> set[str]:
    return {
        c for c in world.countries()
        if (cap := world.capital_of(c)) is not None and cap.government != "civilian"
    }


def _adjacent(world: WorldState, a: str, b: str) -> bool:
    for edge in world.edges:
        if world.nodes[edge.a].country == a and world.nodes[edge.b].country == b:
            return True
        if world.nodes[edge.a].country == b and world.nodes[edge.b].country == a:
            return True
    return False


def _components(world: WorldState, members: set[str]) -> list[list[str]]:
    """Connected components of hostile countries under graph adjacency."""
    seen: set[str] = set()
    groups: list[list[str]] = []
    for start in sorted(members):
        if start in seen:
            continue
        stack, group = [start], []
        seen.add(start)
        while stack:
            cur = stack.pop()
            group.append(cur)
            for other in sorted(members):
                if other not in seen and _adjacent(world, cur, other):
                    seen.add(other)
                    stack.append(other)
        if len(group) >= 2:
            groups.append(sorted(group))
    return groups


def update_blocs(world: WorldState, consts: dict, ledger: Ledger) -> list[dict]:
    """Resolution substep (after collapse rolls). Form/extend blocs, advance the
    consolidation clock, and apply propaganda pressure + expansion."""
    log: list[dict] = []
    groups = _components(world, _hostile_countries(world))

    # Match new groups to existing blocs by country overlap, preserving stage.
    surviving: list[dict] = []
    for group in groups:
        prior = next(
            (b for b in world.blocs if set(b["countries"]) & set(group)), None
        )
        if prior is None:
            bloc = {"countries": group, "stage": 1.0, "formed_turn": world.turn}
            log.append({"event": "proto_bloc_detected", "countries": "+".join(group),
                        "turn": world.turn})
        else:
            bloc = {"countries": group, "stage": prior["stage"],
                    "formed_turn": prior["formed_turn"]}
        surviving.append(bloc)
    world.blocs = surviving
    world.proto_blocs = [b["countries"] for b in surviving]

    for bloc in world.blocs:
        before = bloc["stage"]
        bloc["stage"] = min(
            consts["bloc_max_stage"], bloc["stage"] + consts["bloc_consolidate_rate"]
        )
        if int(bloc["stage"]) > int(before):
            log.append({"event": "bloc_consolidates", "countries": "+".join(bloc["countries"]),
                        "stage": int(bloc["stage"]), "turn": world.turn})
        # pooled propaganda → International drain, blunted by mean exposure of members
        mean_exposure = sum(world.exposure.get(c, 0.0) for c in bloc["countries"]) / len(
            bloc["countries"]
        )
        relief = 1.0 - consts["exposure_bloc_relief"] * (mean_exposure / 100.0)
        drain = consts["bloc_pressure"] * bloc["stage"] * relief
        if drain > 0:
            ledger.apply(world, INTERNATIONAL, "bloc_propaganda", -drain)
        # expansion: grievance exported to adjacent civilian regions
        member_set = set(bloc["countries"])
        for node in world.nodes_sorted():
            if node.country in member_set:
                continue
            cap = world.capital_of(node.country)
            if cap is not None and cap.government != "civilian":
                continue
            if any(
                _node_adjacent_to_country(world, node.id, c) for c in bloc["countries"]
            ):
                node.grievance = clamp(
                    node.grievance + consts["bloc_expansion_grievance"] * bloc["stage"] / 10.0
                )
    return log


def _node_adjacent_to_country(world: WorldState, node_id: str, country: str) -> bool:
    for edge in world.edges_of(node_id):
        other = edge.b if edge.a == node_id else edge.a
        if world.nodes[other].country == country:
            return True
    return False


def bloc_containment_term(world: WorldState, consts: dict) -> float:
    """For scoring (§11 OrderMultiplier): number of blocs weighted by how
    consolidated each is (a fresh bloc ≈ 0.1, a fully consolidated one ≈ 1)."""
    return sum(b["stage"] / consts["bloc_max_stage"] for b in world.blocs)


# Re-exported so the local gauge helper stays available to callers importing here.
__all__ = ["update_blocs", "bloc_containment_term", "local_gauge"]
