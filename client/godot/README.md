# PaxStressia — Godot 4 client scaffold

A **starting skeleton** for the production client (DESIGN §13.4): a third consumer of the JSON
rules core, after the Python sim (`sim/`) and the JS proto (`proto/`). Built against the
[thin-client contract](../../docs/CLIENT.md).

## ⚠️ Status: UNVERIFIED scaffold

This was authored **without a Godot binary in the build environment**, so it has **not been run**.
Treat it as a structural starting point to open and validate in **Godot 4.x**, not as working
software. It is deliberately **isolated** — it lives only here under `client/godot/` and touches
nothing in `sim/` or `proto/`, so it cannot affect the tested game (105 tests / 0 xfail,
calibration 10/10). Expect to fix small API/syntax things on first open; that's the point of a
scaffold.

## What it does (today)

Loads the rules (`nodes/edges/factions/initiatives/events/constants/patrons` + scenario layering
per §18.9) and renders the **starting state** of the Sahel arc read-only, in plain words
(§13.3): the three standings and a region list with who-rules / Control / Anger. It's the
"display" half of the contract; the turn loop (§3 of the contract) is the next step.

## Run it

1. Install **Godot 4.x** (standard editor; no C#/.NET needed — this is pure GDScript).
2. **Bundle the rules** (the client can't read the repo's `rules/` across the project boundary):
   copy or symlink the repo's `rules/` directory into `client/godot/rules/`. From the repo root:
   ```sh
   cp -r rules client/godot/rules        # or: ln -s ../../rules client/godot/rules
   ```
   A future `client/godot/build.py` should automate this, mirroring `proto/build.py` so the core
   stays single-source. (`rules/` is intentionally not committed under here.)
3. Open `client/godot/project.godot` in Godot and press Play (the main scene is `Main.tscn`).

## Roadmap (against `docs/CLIENT.md`)

1. **Display** (this scaffold) — load + render starting state. ✅ skeleton
2. **Turn loop** — choose orders → resolve → report. Decide *embed* (port `sim/` resolution to
   GDScript, like the proto did in JS) vs *display* (run the Python `sim/` as a backend). §1 of
   the contract weighs both.
3. **The board, not a list** — the situation-map visual language (§13.3): colour = who-rules, a
   red ring's thickness = insurgent strength, ★ = capital. The proto + `proto/preview.mjs` are the
   reference; Godot is where this becomes the lit "situation table" the design aspires to (§13.4).
4. **Parity gate** — like `proto/smoke.mjs`, a headless determinism/▢ check so this client stays
   true to the core.
