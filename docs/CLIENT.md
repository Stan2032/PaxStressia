# PaxStressia — Thin-Client Contract

*How any presentation client (the JS proto, a Godot 4 client, anything else) consumes the
JSON rules core. The architectural law (DESIGN §13.2, §13.4): **the rules are the source of
truth; the client is thin and swappable; choosing a renderer is a presentation decision, not a
rewrite.** Two clients already prove this — the Python sim (`sim/`, the reference engine) and the
single-file JS proto (`proto/index.html`). This document is the spec a third client (e.g. Godot,
§13.4) is built against.*

---

## 1. Two ways to be a client

A client either **embeds an engine** or **displays one**:

- **Embed (port the engine).** Re-implement the deterministic resolution rules (§5–§11, §18) over
  the same `rules/*.json`. The JS proto does this — its `<script id="engine-js">` block is a
  full port of `sim/`. A Godot client can do the same in GDScript. The engines are
  *self-consistently* deterministic (seeded RNG); they are **not** bit-compatible with each other,
  and that is fine — each is internally reproducible.
- **Display (call a backend).** Run the Python `sim/` as the engine (it is stdlib-only and
  headless) and have the client render the serialized state it returns. No rules logic in the
  client at all. Best when you want one canonical engine; costs you a runtime dependency.

The proto chose *embed* (zero backend, runs in a phone browser). A production Godot client may
choose either; the contract below is the same regardless.

## 2. Loading the rules (`rules/`, §18.9)

Files (all JSON), loaded by stem into one dict — mirror of `sim.world.load_rules`:

`nodes` · `edges` · `factions` · `initiatives` · `events` · `constants` · `patrons` (+ `sources`
for the in-game "homework" screen; + `schema/` for validation, dev-only).

**Scenario layering** — load the base files, then for a scenario `rules/scenarios/<id>/`:

- `scenario.json` → lands under `rules["scenario"]` (start date, horizon, theatre metadata).
- `nodes` / `edges` / `factions` / `initiatives` / `events` / `patrons` present in the scenario
  dir **REPLACE** the base file wholesale.
- `constants` **MERGES** over the base (`{**base, **scenario}`) — a scenario overrides only the
  constants it names; the rest fall through.
- A file absent from the scenario dir falls through to the base.

The playable scenarios today: `sahel_lite` (the proto default, 6 nodes), `sahel_arc` (the
history-calibrated 168-turn arc — the one the tests and `harness/calibrate.py` grade), and `grand`
(~40 nations; gated world-scale systems on).

**Bundling.** A browser/Godot client can't read the repo's `rules/` at runtime across origins, so
bundle them at build time. The proto does this with `proto/build.py` (injects a JSON snapshot into
a `<script id="rules-snapshot">` tag; `proto/build.py --check` keeps it fresh in CI). A Godot
build step should likewise copy `rules/` into the project (e.g. `client/godot/rules/`) — keep one
copy mechanism so the core stays single-source.

## 3. The turn loop (engine contract)

The reference engine (`sim/engine.py`, class `Engine`) is the spec:

- `Engine(rules=..., seed=int, policy=...)` — construct from loaded rules. `seed` makes the run
  reproducible. `policy` is the order source; an interactive client *is* the policy (it supplies
  the player's chosen orders each turn).
- **Per turn:** Briefing → the player picks orders → resolve → report. Resolution order is fixed
  (§18.3): refresh lingering effects → apply initiative effects → backfire rolls → faction growth
  → spread → collapse rolls → patron market → events → norms/markets (grand) → bookkeeping.
- **Orders** are `[{"initiative": <id>, "node": <node_id or null>}]`. Affordability is the
  player's Mandate (🏛️ Backing) and Treasury (💰 Money) for the turn.
- **Events** (§10): at most one card per turn, drawn weight-proportionally from the eligible deck
  (predicates in `requires`; see `sim/events.py` / the proto's `eligible()`). The client presents
  the card and returns the chosen branch index.

## 4. State to render (serialization)

The world serializes to plain JSON (`sim.world.WorldState.snapshot()` / the proto's `st`). The
display-relevant shape:

- **Player:** `mandate`, `treasury`, `domestic`, `international`, `drift`, `casualties`,
  `spent_total`, `suppress_clocks` (buried secrets).
- **Per node:** `id`, `name`, `country`, `capital`, `government` (civilian/junta/emirate/failed),
  `governance`, `local_legitimacy`, `grievance`, `development`, `population_k`, `intel_coverage`,
  `ops_pressure`, `patron_influence{}`, and `presence{faction_id: {strength, entrenchment,
  visibility}}`.
- **World:** `exposure{country: 0–100}`, `collapsed{country: bool}`, `coup_risk{}`, `proto_blocs`,
  `blocs`, and (grand only) `norms`, `markets`, `patron_strength`, `rivalry`, `commands`,
  `coalition`.
- **Briefing** (what the player actually sees — fog, not truth, §9): insurgent figures are
  **estimates** with a ± band scaled by `intel_coverage`; a region can read calm while quietly
  lost. Render the band, never the hidden truth.
- **Score / ending** (§11): `Final = Stabilization × OrderMult × IntegrityMult − Costs`; the
  ending matrix is two axes (abroad = Stabilization×Order; home = IntegrityMult). The score uses
  Local legitimacy, juntas/blocs, and drift — **not** the Home/Allies gauges (those drive Mandate
  income and coalitions, and the in-fiction stakes).

## 5. The display contract (what the player should infer, §13.3)

The legibility law: **a newcomer reads the screen without a manual.** Two binding rules a client
must honour:

1. **Plain words on screen; model terms only in the data/docs.** The UI vocabulary is a plain
   skin over the model vocabulary (the canonical map, DESIGN §13.3):
   Backing = mandate · Money = funds · Home = domestic legitimacy · Allies = international
   legitimacy · Trust = local legitimacy · Anger = grievance · Control = governance ·
   Dug in = entrenchment · Violence = activity/visibility · Your view = intel coverage ·
   Spotlight = exposure · Overreach = authoritarian drift · Foreign backer = patron.
2. **Show, don't tell.** State is carried by the board — colour is who-rules, a red ring's
   thickness *is* insurgent strength, a ★ is a capital — before any words. The proto is the
   reference for the visual language (and `proto/preview.mjs` renders it headlessly). A production
   client (§13.4) is free to make this photoreal (a lit situation table) so long as the *same
   inferences* are readable.

## 6. What must stay true (the discipline)

- **The rules are the only source of truth.** A client never hard-codes a number that belongs in
  `rules/*.json`. New balance lives in the JSON; clients re-bundle.
- **The history calibration is sacred.** A passive run of `sahel_arc` must reproduce the Sahel arc
  (`harness/calibrate.py`, 10/10). Clients that embed an engine must preserve this; the test suite
  (`tests/`) and the JS smoke test (`proto/smoke.mjs`) are the gate.
- **Determinism.** Same rules + same seed + same orders → same run, within one engine.

---

*Status: the Python sim and JS proto are the two living reference clients. A Godot 4 scaffold under
`client/godot/` is the start of a third (see its README) — built against this contract.*
