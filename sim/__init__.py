"""PaxStressia headless simulation core.

Data-driven by design: all rules live in JSON under rules/ (DESIGN.md §13.2).
This package is stdlib-only so it runs in bare Termux Python — jsonschema is
test-only, matplotlib harness-only.
"""

from .engine import Engine
from .legitimacy import Ledger, LedgerEntry
from .policies import (
    POLICIES,
    CompetentPolicy,
    EmergencyPowersPolicy,
    GrandCompetentPolicy,
    MixedPolicy,
    PassivePolicy,
    Policy,
    PureHeartsMindsPolicy,
    PureKineticPolicy,
    RandomPolicy,
)
from .world import WorldState, build_world, load_rules

__version__ = "0.30.0"

__all__ = [
    "POLICIES",
    "CompetentPolicy",
    "EmergencyPowersPolicy",
    "GrandCompetentPolicy",
    "Engine",
    "Ledger",
    "LedgerEntry",
    "MixedPolicy",
    "PassivePolicy",
    "Policy",
    "PureHeartsMindsPolicy",
    "PureKineticPolicy",
    "RandomPolicy",
    "WorldState",
    "build_world",
    "load_rules",
    "__version__",
]
