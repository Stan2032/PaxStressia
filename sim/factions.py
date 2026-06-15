"""The insurgency model (DESIGN.md §5, formulas §18.5).

Strength accretes from grievance, sponsors, and alliances; decays under
pressure and defection. Uncontested strength converts into entrenchment
(shadow governance). Contestation makes insurgencies loud; entrenchment makes
them quiet — visibility is what the player's map will believe (sim.fog).
Every ΔStrength term is computed and logged separately: balance work reads
causes, not net effects.
"""

from __future__ import annotations

import random

from .legitimacy import Ledger
from .world import Presence, WorldState, clamp


def route_factor(world: WorldState, node_id: str) -> float:
    """Mean open capacity of the node's edges — sponsor flow rides the graph."""
    edges = world.edges_of(node_id)
    if not edges:
        return 0.0
    return sum(e.capacity * (1.0 - e.interdiction) for e in edges) / len(edges)


def growth_terms(
    world: WorldState, consts: dict, faction_id: str, node_id: str, amnesty_rate: float,
    recruit_mult: float = 1.0,
) -> dict[str, float]:
    """The §5.1 equation, term by term, for one (faction, node)."""
    node = world.nodes[node_id]
    pres = node.presence[faction_id]
    faction = world.factions[faction_id]
    junta_amp = 1.0 + (consts["junta_recruit_amp"] if node.government == "junta" else 0.0)
    n_links = len(faction.links)
    # Absorptive capacity (v0.5): positive growth scales with remaining headroom —
    # recruitment pools deplete; strength approaches saturation asymptotically.
    headroom = 1.0 - pres.strength / 100.0
    recruitment = (
        consts["k_recruit"] * (node.grievance / 100.0) * (1.0 - node.governance / 100.0)
        * junta_amp * headroom * recruit_mult
    )
    external = (
        consts["sponsor_flow"] * route_factor(world, node_id) * (1.0 + consts["k_pool"] * n_links)
        * headroom
        if faction.sponsor
        else 0.0
    )
    alliance = consts["k_alliance"] * n_links * headroom
    attrition = (
        (node.ops_pressure + node.partner_capacity * consts["k_partner"])
        * consts["k_attrit"]
        * (pres.strength / 100.0)
    )
    defection = amnesty_rate * pres.strength
    return {
        "recruitment": recruitment,
        "external_support": external,
        "alliance_bonus": alliance,
        "attrition": -attrition,
        "defection": -defection,
    }


def apply_growth(
    world: WorldState, consts: dict, amnesty_rates: dict[str, float], recruit_mult: float = 1.0
) -> tuple[list[dict], dict[str, float]]:
    """Resolution substep c. Returns (itemized growth log, attrition dealt per faction).
    `recruit_mult` is the global precedent multiplier (§21); 1.0 in single-theater play."""
    log: list[dict] = []
    attrition_dealt: dict[str, float] = {f.id: 0.0 for f in world.factions_sorted()}
    for faction in world.factions_sorted():
        for node in world.nodes_sorted():
            if faction.id not in node.presence:
                continue
            pres = node.presence[faction.id]
            if pres.strength <= 0 and pres.entrenchment <= 0:
                continue
            rate = amnesty_rates.get(node.id, 0.0)
            terms = growth_terms(world, consts, faction.id, node.id, rate, recruit_mult)
            delta = sum(terms.values())
            pres.strength = clamp(pres.strength + delta)
            attrition_dealt[faction.id] += -terms["attrition"]
            log.append(
                {
                    "faction": faction.id,
                    "node": node.id,
                    "terms": {k: round(v, 4) for k, v in terms.items()},
                    "strength": round(pres.strength, 4),
                }
            )
    return log, attrition_dealt


def apply_spread(world: WorldState, consts: dict) -> list[dict]:
    """Resolution substep c2 (v0.4): strength above the threshold replicates
    over open edges into adjacent grievance. Spread is replication, not
    movement — momentum recruits locally; the source is not depleted (§18.5).
    The arc's historical test: northern Burkina must ignite from Mopti."""
    log: list[dict] = []
    inflow: dict[tuple[str, str], float] = {}
    for faction in world.factions_sorted():
        for node in world.nodes_sorted():
            pres = node.presence.get(faction.id)
            if pres is None or pres.strength <= consts["spread_threshold"]:
                continue
            for edge in sorted(world.edges_of(node.id), key=lambda e: e.id):
                other_id = edge.b if edge.a == node.id else edge.a
                other = world.nodes[other_id]
                # infiltration meets state capacity, quadratically: governed cores
                # suffer raids, not occupation (v0.5 — no Sahel capital was ever held)
                resist = (1.0 - other.governance / 100.0) ** 2
                flow = (
                    consts["k_spread"] * pres.strength
                    * edge.capacity * (1.0 - edge.interdiction)
                    * (other.grievance / 100.0)
                    * resist
                )
                if flow > 0:
                    key = (faction.id, other_id)
                    inflow[key] = inflow.get(key, 0.0) + flow
    for (fid, nid) in sorted(inflow):
        node = world.nodes[nid]
        pres = node.presence.get(fid)
        if pres is None:
            pres = node.presence[fid] = Presence(visibility=25.0)
            log.append({"event": "spread", "faction": fid, "node": nid, "turn": world.turn})
        # absorptive capacity applies to spread too (v0.5): arriving momentum
        # recruits into the same finite pool local growth draws from
        pres.strength = clamp(pres.strength + inflow[(fid, nid)] * (1.0 - pres.strength / 100.0))
    return log


def entrench_and_visibility(world: WorldState, consts: dict) -> None:
    """Resolution substep d. Uncontested strength becomes shadow governance;
    visibility relaxes toward its contested/quiet target (Pillar 4)."""
    for node in world.nodes_sorted():
        for fid in sorted(node.presence):
            pres = node.presence[fid]
            uncontested = (
                pres.strength >= consts["entrench_strength_min"]
                and node.ops_pressure < consts["entrench_pressure_max"]
            )
            if uncontested:
                node.uncontested_turns[fid] = node.uncontested_turns.get(fid, 0) + 1
                pres.entrenchment = clamp(
                    pres.entrenchment + consts["k_entrench"] * pres.strength / 100.0
                )
            else:
                node.uncontested_turns[fid] = 0
            # Entrenchment decays only through Local legitimacy (§6): the slow gauge
            # is the only thing that permanently starves an insurgency.
            pres.entrenchment = clamp(
                pres.entrenchment - consts["k_entrench_decay"] * node.local_legitimacy / 100.0
            )
            contest = min(1.0, node.ops_pressure / consts["pressure_ref"])
            target = clamp(
                consts["vis_floor"]
                + consts["vis_contest"] * contest
                - consts["vis_quiet"] * pres.entrenchment
            )
            pres.visibility = clamp(
                pres.visibility + consts["vis_smooth"] * (target - pres.visibility)
            )


def networking_check(
    world: WorldState, consts: dict, attrition_dealt: dict[str, float]
) -> list[dict]:
    """Resolution substep e (§5.2). Deterministic threshold:
    affinity_eff × mutual_need × route_access ≥ link_threshold.
    The affinity floor keeps ideologically unlike alliances possible."""
    log: list[dict] = []
    factions = world.factions_sorted()
    for i, f in enumerate(factions):
        for g in factions[i + 1 :]:
            if f.linked_with(g.id):
                continue
            affinity_eff = max(f.relations.get(g.id, 0.0), consts["affinity_floor"])
            mutual_need = min(
                2.0, 1.0 + (attrition_dealt.get(f.id, 0.0) + attrition_dealt.get(g.id, 0.0)) / 20.0
            )
            access = _shared_route_access(world, f.id, g.id)
            score = affinity_eff * mutual_need * access
            if score >= consts["link_threshold"]:
                f.links.append({"with": g.id, "turn": world.turn})
                g.links.append({"with": f.id, "turn": world.turn})
                log.append(
                    {
                        "event": "faction_link",
                        "factions": [f.id, g.id],
                        "score": round(score, 4),
                        "turn": world.turn,
                    }
                )
    return log


def _shared_route_access(world: WorldState, fid: str, gid: str) -> float:
    """1.0 if the factions share a node; else best open edge between their nodes."""
    def held_nodes(faction_id: str) -> set[str]:
        return {
            n.id
            for n in world.nodes_sorted()
            if faction_id in n.presence and n.presence[faction_id].strength > 0
        }

    f_nodes, g_nodes = held_nodes(fid), held_nodes(gid)
    if not f_nodes or not g_nodes:
        return 0.0
    if f_nodes & g_nodes:
        return 1.0
    best = 0.0
    for edge in sorted(world.edges, key=lambda e: e.id):
        if (edge.a in f_nodes and edge.b in g_nodes) or (edge.b in f_nodes and edge.a in g_nodes):
            best = max(best, edge.capacity * (1.0 - edge.interdiction))
    return best


def hops_from(world: WorldState, origin_id: str) -> dict[str, int]:
    """BFS graph distance from a node, in edge hops."""
    dist = {origin_id: 0}
    frontier = [origin_id]
    while frontier:
        nxt = []
        for nid in frontier:
            for edge in world.edges_of(nid):
                other = edge.b if edge.a == nid else edge.a
                if other not in dist:
                    dist[other] = dist[nid] + 1
                    nxt.append(other)
        frontier = nxt
    return dist


def collapse_rolls(
    world: WorldState, consts: dict, rng: random.Random, ledger: Ledger
) -> list[dict]:
    """Resolution substep f (§5.3). One collapse per country at v0.2.
    Junta is the most common outcome in fragile-but-functional states — and the
    coup seeds you planted with Train & Equip are in the weights.
    v0.5: threat is distance-discounted — the far north held for eight years
    without toppling Bamako; it was the center's deterioration that did."""
    log: list[dict] = []
    for country in world.countries():
        if world.collapsed[country]:
            continue
        capital = world.capital_of(country)
        if capital is None:
            continue  # off-map capital (Sahel-lite NE): cannot collapse in this dataset
        hops = hops_from(world, capital.id)
        threat = 0.0
        for node in world.country_nodes(country):
            dist_factor = 1.0 / (1.0 + consts["collapse_dist_decay"] * hops.get(node.id, 9))
            for fid in sorted(node.presence):
                pres = node.presence[fid]
                threat = max(
                    threat,
                    pres.strength * (0.5 + pres.entrenchment / 200.0) * dist_factor,
                )
        ratio = threat / max(1.0, capital.governance)
        if ratio < consts["collapse_ratio"]:
            continue
        cap_entrench_share = max(
            (p.entrenchment / 100.0 for p in capital.presence.values()), default=0.0
        )
        outcomes = ["junta", "failed", "emirate"]
        weights = [
            consts["w_junta"] + world.coup_risk[country],
            consts["w_failed"],
            consts["w_emirate"] * cap_entrench_share,
        ]
        if sum(weights) <= 0:
            continue
        outcome = rng.choices(outcomes, weights=weights, k=1)[0]
        world.collapsed[country] = True
        capital.government = outcome
        if outcome == "junta":
            capital.governance = clamp(capital.governance - consts["junta_gov_hit"])
            capital.patron_influence["mercenary"] = clamp(
                capital.patron_influence.get("mercenary", 0.0) + consts["junta_patron_gain"]
            )
            for node in world.country_nodes(country):
                node.grievance = clamp(node.grievance + consts["junta_grievance_hit"])
                node.government = "junta"
        elif outcome == "failed":
            capital.governance = clamp(capital.governance * 0.5)
            for node in world.country_nodes(country):
                node.government = "failed"
        else:  # emirate: the strongest faction governs; sanctuary dynamics land v0.7
            capital.governance = clamp(capital.governance - consts["junta_gov_hit"])
            for node in world.country_nodes(country):
                node.government = "emirate"
        log.append(
            {
                "event": "state_collapse",
                "country": country,
                "outcome": outcome,
                "threat_ratio": round(ratio, 4),
                "coup_risk": round(world.coup_risk[country], 4),
                "turn": world.turn,
            }
        )
    return log

