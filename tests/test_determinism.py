"""The determinism law (DESIGN.md §18.1): same rules + seed + policy ⇒
byte-identical state at every turn. This is the precondition for the Monte
Carlo harness, replays, and the post-mortem reveal."""

from sim import Engine, PureKineticPolicy, RandomPolicy


def test_same_seed_identical_history():
    a = Engine(seed=42, policy=PureKineticPolicy())
    b = Engine(seed=42, policy=PureKineticPolicy())
    for _ in range(24):
        a.run_turn()
        b.run_turn()
        assert a.checkpoint() == b.checkpoint()


def test_same_seed_identical_with_random_policy():
    a = Engine(seed=7, policy=RandomPolicy(seed=99))
    b = Engine(seed=7, policy=RandomPolicy(seed=99))
    a.run(24)
    b.run(24)
    assert a.state_hash() == b.state_hash()


def test_different_seeds_diverge():
    a = Engine(seed=1)
    b = Engine(seed=2)
    a.run(24)
    b.run(24)
    assert a.state_hash() != b.state_hash()


def test_checkpoint_is_canonical_json():
    eng = Engine(seed=5)
    eng.run(3)
    import json

    state = json.loads(eng.checkpoint())
    assert state["turn"] == 3
    assert list(state["nodes"]) == sorted(state["nodes"])
