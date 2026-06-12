# Changelog

Small incremental releases, every balance change a readable diff (working convention, `docs/PROJECT_CONTEXT.md` §4).

## v0.2.1 — 2026-06-12

Docs-only growth from two research passes; no code or rules changes.

- **DESIGN.md §19 — Playability, Pacing & Balance:** research-backed binding commitments — the fun gate (greybox before meaning), the anti-whack-a-mole package (legibility law, doctrine plurality, alert rationing), the interesting-decisions audit, asymmetry-of-goals + dual-use events, Frostpunk-calibrated Emergency Powers (felt costs, one-way rate-limited tiers, continuous integrity judgment), procedural-persona balancing with a v0.5 CI dominance check, intrinsic anti-snowball, situational difficulty, misery counterweights (named people, pride beats).
- **DESIGN.md §20 — The Closed Society & the Exposure System** (Stan's directive, direction DECIDED; mechanics PROPOSED for v0.7–v0.9): documented-pattern closed-society events, hostile-fog disinformation grounded in the "African Initiative" record, and the Exposure track (fund research/exile media/OSINT/designations; documented exposure→sanctions chains; funder's-paradox and regime-retaliation backfires; credibility bank; §20.6 verification ledger).
- **Repo:** `main` trunk created at the v0.2 state (authorized); PR workflow from here on. Default-branch flip pending (GitHub settings, one tap).

## v0.2 — 2026-06-12

The §5.3 milestone, delivered in full; repo bootstrapped from the v0.1 handoff.

- **Docs:** `docs/PROJECT_CONTEXT.md` (handoff committed verbatim + post-handoff log), `docs/DESIGN.md` grown cumulatively to v0.2 — new **§18 Simulation Specification** (determinism law, state vectors, resolution order, effect-op vocabulary, formulas bound to constants, ledger contract, policy interface, stub inventory) and new open question #7 (repo name *PaxStressia* vs working title *MANDATE*).
- **Rules:** six JSON Schemas (`rules/schema/`) — backfire channels are *schema-required* on every initiative (Pillar 3 as validation). Sahel-lite dataset: 6 nodes, 8 edges, 2 composited factions (sourcing shipped in-data), 9 initiatives across all five families, 6 events, ~50 named constants (all PROPOSED pending v0.5 calibration).
- **Sim:** stdlib-only package implementing the four-phase turn loop (Briefing → Policy → Resolution → Consequence) with seeded-RNG determinism, itemized legitimacy ledger, per-term insurgent growth logging, entrenchment/visibility dynamics, deceptive-calm fog estimates with confidence bands, election/Mandate coupling, collapse rolls (junta path live), faction link formation, proto-bloc detection (log-only), patron drift stub, and per-turn true-state snapshots (post-mortem spine).
- **Tests:** schema + referential validation, byte-identical determinism, ledger-itemization invariant, mandate bounds, smoke runs across all policies, and the four design-thesis tests as real simulations marked `xfail` until v0.5.
- **CI:** ruff + pytest + 10-run mini-harness (passive and kinetic) uploading `runs.json` + `balance.png` artifacts.
- **Deliberately absent:** LICENSE (open question #5 gates it).

## v0.1 — 2026-06-12

Design document and full project context (produced in the design/research session; committed here at v0.2).
