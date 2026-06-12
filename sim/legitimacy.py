"""The legitimacy economy's bookkeeping (DESIGN.md §6, §18.6).

Hard requirement, mechanized: every change to Domestic, International, or any
node's Local legitimacy flows through Ledger.apply() and produces an itemized
entry whose delta is the *applied* (post-clamp) amount. The engine guarantees —
and tests enforce — that each gauge's movement in a turn equals the sum of its
entries. The player must always be able to trace why a number moved.
"""

from __future__ import annotations

from dataclasses import dataclass

from .world import WorldState, clamp

DOMESTIC = "domestic"
INTERNATIONAL = "international"


def local_gauge(node_id: str) -> str:
    return f"local:{node_id}"


@dataclass
class LedgerEntry:
    turn: int
    gauge: str
    source: str
    delta: float

    def to_dict(self) -> dict:
        return {
            "turn": self.turn,
            "gauge": self.gauge,
            "source": self.source,
            "delta": round(self.delta, 4),
        }


class Ledger:
    """Run-long itemized record of every legitimacy movement."""

    def __init__(self) -> None:
        self.entries: list[LedgerEntry] = []

    def apply(self, world: WorldState, gauge: str, source: str, delta: float) -> float:
        """Apply a delta to a gauge, clamped to 0–100; record and return what stuck."""
        if gauge == DOMESTIC:
            old = world.player.domestic
            world.player.domestic = clamp(old + delta)
            applied = world.player.domestic - old
        elif gauge == INTERNATIONAL:
            old = world.player.international
            world.player.international = clamp(old + delta)
            applied = world.player.international - old
        elif gauge.startswith("local:"):
            node = world.nodes[gauge.split(":", 1)[1]]
            old = node.local_legitimacy
            node.local_legitimacy = clamp(old + delta)
            applied = node.local_legitimacy - old
        else:
            raise ValueError(f"unknown gauge: {gauge}")
        if applied != 0.0:
            self.entries.append(LedgerEntry(world.turn, gauge, source, applied))
        return applied

    def entries_for_turn(self, turn: int) -> list[LedgerEntry]:
        return [e for e in self.entries if e.turn == turn]

    def sum_for(self, turn: int, gauge: str) -> float:
        return sum(e.delta for e in self.entries if e.turn == turn and e.gauge == gauge)
