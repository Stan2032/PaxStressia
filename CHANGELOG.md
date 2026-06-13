# Changelog

Small incremental releases, every balance change a readable diff (working convention, `docs/PROJECT_CONTEXT.md` §4).

## v0.5.0 — 2026-06-13

**History calibration — reality is the baseline, and now it's enforced.** Tuned the constants until a passive player reproduces the Sahel arc 2012–2026 on 10/10 seeds.

- **Calibration result** (`harness/calibrate.py`, 5-check battery): Mali junta in the coup-cascade window, cascade order ML→BF→NE (the historical sequence), proto-bloc detected, insurgent reach ≥2× and still growing at the horizon — all 10/10.
- **New engine mechanics** (Python + JS, doc-code lockstep): absorptive capacity (headroom-scaled growth → realistic S-curves), distance-discounted collapse threat (`collapse_dist_decay` — the far north menaced Bamako less than the center did), governance-resisted spread (quadratic — capitals are raided, never occupied, as in reality).
- **Thesis suite: 3 of 4 promoted xfail → ENFORCED** — `test_passive_player_reproduces_history`, `test_pure_kinetic_strategy_loses_integrity_and_local`, `test_pure_hearts_minds_without_security_loses_to_momentum`. A balance change that breaks any now fails CI.
- **`MixedPolicy` + §19.7 dominance check** ship as instruments, honestly `xfail` until a winnable balanced path exists (v0.7) — asserting mixed-dominance today would be false (every policy loses the not-yet-winnable arc; cheapest loser wins on cost), and faking it by tuning costs is the dishonesty the suite exists to prevent.
- **CI** runs the calibration battery and uploads `calibration.json`. Constants status flipped PROPOSED → CALIBRATED.
- Known compression (flagged, not hidden): BF→NE collapse spacing is tighter than history (correctly ordered, ~5 turns vs ~18 months); within the generous window, queued for v0.6.

## v0.4.0 — 2026-06-12

**Scenario 1 — "The Arc" (Sahel 2012–2026) — full map and event deck in data**, playable in the proto via the scenario picker.

- `rules/scenarios/sahel_arc/`: 12 nodes (Niamey on-map; coastal-spillover marker), 18 edges, 3 factions (new: *Azawad National Front*, the MNLA→CMA→FLA composite), 14-card deck — 8 sourced historical beats (northern collapse, the intervention window, franchise declared, the Bamako crisis, ECOWAS rupture, mercenary arrival, AES declaration, the concord of enemies) + the 6 generic cards.
- Engine (both Python and JS, doc in lockstep): **spread over edges** (§18.5 — replication into adjacent grievance; northern Burkina ignites unscripted), **scenario loading** (§18.9 replace/merge/fall-through), `once` beats, new requires predicates (`country_collapsed`, `country_not_collapsed`, `min_collapsed`, `min_links`), events-only `presence`/`patron` ops.
- Beats-vs-system law (§18.9): beats supply political texture; coups stay endogenous or calibration means nothing.
- Tests: arc schema/integrity suite, full-horizon passive runs, spread-ignition and once-ness assertions, scenario-semantics test; history-calibration thesis test now targets the arc. **Second thesis test XPASSes pre-calibration** (pure-kinetic loses Local legitimacy on all seeds — FM 3-24's paradox). Node smoke extended with a 168-turn arc battery.

## v0.3.0 — 2026-06-12

**The greybox prototype — PaxStressia is playable.** `proto/index.html`: single-file, phone-browser, dark-dossier greybox of Sahel-lite answering Phase 0's question (*is the core loop fun in 20 minutes?*).

- Full §18 loop in the client: briefing with fog estimates ±90% bands (deceptive calm experiencable — §19.5 honored), 9 initiatives with budgets/backfires/casualty risk, player-chosen event cards with sources, itemized ledger report (§18.6 rendered), elections/Mandate, collapse rolls, patron/bloc signals, scoring with the four endings, and the **believed-vs-true post-mortem chart** at game end.
- §19 commitments live: alert-rationed headlines (max 3, escalating phrasing), directing-not-commanding altitude, localStorage saves, session length 36/60/168.
- Single-source-of-truth preserved: fetches `rules/*.json` live when served; embedded snapshot (via `proto/build.py`) only as `file://` fallback, with a CI drift check.
- `proto/smoke.mjs`: Node smoke test extracts the DOM-free engine and verifies determinism, ranges, ledger itemization, and save/restore round-trips in CI.
- `docs/DEPLOY.md`: Cloudflare Pages guide (repo-root deploy → live rules + per-PR playtest previews), wrangler and GitHub Pages alternatives.

## v0.2.2 — 2026-06-12

**The title is decided: PaxStressia** (per Stan: the "Pax …ia" eras of history — pax at the cost of stress; "being lied about but not dealing in lies yourself. or, trying your best to."). Resolves DESIGN.md open questions #4 and #7.

- DESIGN.md: §1 gains "The Name"; header retitled; #4/#7 marked RESOLVED.
- Live files renamed: README, pyproject (`paxstressia-sim`, v0.2.2), `sim/__init__` docstring + `__version__`, harness plot title, all six schema titles.
- MANDATE remains in historical sections (handoff doc, changelogs, decision records) per the cumulative rule.

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
