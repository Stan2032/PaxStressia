# Changelog

Small incremental releases, every balance change a readable diff (working convention, `docs/PROJECT_CONTEXT.md` §4).

## v0.25.0 — 2026-06-26

**The horizon finding, diagnosed — and the benchmark sharpened** (§19.7; the measured follow-through on v0.24). The v0.24 audit found that balanced play loses to pure hearts-minds at the arc's full 168-turn horizon and named a fix. Before building it, I measured *why* — and the first explanation was wrong. Recording that correction is the point: *measure, never assume.*

- **The real mechanism:** capital collapse is driven by insurgent **strength ÷ capital governance** (`factions.collapse_rolls`), **not by grievance directly** — so the way to keep juntas low (and `order_mult` high) is to keep total insurgent **strength** low. All-in development aimed at the worst-**grievance** regions starves recruitment at the source and does exactly that; spending budget on any other tool costs that throughput. Over a long run the concentration wins, because **development has no diminishing-returns / co-option downside yet** (Galula's *development without security is captured*, under-modelled).
- **What it is *not*:** conceded countryside does **not** "drop out of the average" (Stabilization is a mean over *all* nodes and actually rewards holding more ground — balanced play's stabilization is higher), and it is **not** security costs piling up (the benchmark barely uses force — zero casualties). Both were in the v0.24 prose; both are now corrected across the docs.
- **The calibration-safe half of the fix, shipped:** `CompetentPolicy` now aims its development where **grievance** is worst — the prevention-at-source lever its own docstring always named — instead of at the highest-force regions (where development is largely co-opted). One targeting change, no world-dynamics touched. Effect: the §19.7 120-turn margin goes from ~1 point to **~9** (competent 12→**20**, dominating every pure), and the 168-turn gap narrows (1.3→**4.8**). Calibration **10/10 by construction** — policies never touch the passive world.
- **The deeper fix stays named, not done:** diminishing-returns / co-option on development, so all-in development plateaus and balanced play that protects its gains wins at the horizon. A player-effect change (calibration-safe — passive never develops) that must still hold the 120-turn gate and the hearts-minds characterization, so it's a focused future milestone. `test_no_pure_strategy_dominates_at_the_full_horizon` still **xfails** (4.8 < 8.3) until it lands.
- **Sim + docs only** — no rules / proto / calibration change. **Sahel calibration still 10/10; 104 tests pass / 1 xfail.**

## v0.24.0 — 2026-06-26

**Balance audit — the horizon-dominance finding, surfaced not hidden** (§19.7). A new player-side instrument that grades the *player*, where calibrate.py grades the passive *world*.

- **`harness/audit.py`** — runs every policy archetype (passive / kinetic / hearts-minds / mixed / competent / emergency) on the Sahel arc at **both** the 120-turn subset the enforced thesis test checks **and** the arc's full **168-turn horizon**, printing the score spread, the ending distribution, and the §19.7 "balanced tops every pure" gate at each length. Report-only — it never fails CI.
- **The finding:** §19.7 **holds at 120 turns but breaks at 168** — pure hearts-minds overtakes balanced play once the run is long enough. (The mechanism here was first mis-attributed; **v0.25 diagnosed it by measurement and corrected the story** — see below. Recording the wrong first guess and its correction *is* the discipline.)
- **Named, not papered over:** a fifth thesis assertion — `test_no_pure_strategy_dominates_at_the_full_horizon` (`tests/test_thesis.py`) — asserts the destination at the full horizon and **xfails** until it's closed. The xfail test is the gate; the audit harness is the instrument.
- **Docs + tests + harness only** — no rules / sim / proto / calibration change. **Sahel calibration still 10/10; 104 tests pass / 1 xfail** (the named destination).

## v0.23.0 — 2026-06-18

**Named people, kept — the closed-society realities, made personal** (the emotional payoff of v0.22's moral layer; §20.2 / §19.10). Consequences become individual, not statistical.

- **Four composite people you meet and lose:** **Aminata** the teacher (→ the new curriculum, in a town that fell), **Ousmane** the reporter (→ "mobilised" to the front, filing nothing), **Dr. Fatou** the clinic (→ requisitioned; she went north), **Judge Ibrahim** (→ his court "suspended pending reform"). Each is a two-card arc in the Sahel deck — a *met* beat (a good moment, early) and a *kept* beat that fires **only after their region falls**.
- **A new `requires_fired` event-chain predicate** (added to the Python sim, the JS proto, and the event schema): a follow-up card is eligible only once a named setup card has fired — a clean, reusable primitive for narrative chains. A chain-integrity test proves a *kept* beat never fires without its *met* setup, and that the arcs complete in passive runs.
- **The post-mortem capstone:** the proto end-screen now closes with **"And the people you met,"** listing each person's fate — red if their region fell, green if it held. The §20.2 reveal of *what the regime did with the quiet you left it*.
- **Calibration-safe:** the *kept* losses live on choice 1, which the passive baseline never picks, so they never touch the §12 junta-timing — **Sahel calibration still 10/10; 103 tests pass / 0 xfail; both engines + smoke green.** The people are fictional composites (like the factions); their fates are drawn from the documented record (flagged in `rules/sources.json`).

## v0.22.0 — 2026-06-17

**The Closed Society layer — the moral weight, made mechanical** (Stan's founding ask: *remind the player of the harsh, brutal realities citizens of authoritarian states endure*). Seven grounded event cards now surface the documented authoritarian playbook, in both the base deck (base + grand) and the Sahel-arc deck (the primary playable).

- **The cards** (all `any_junta`-gated, sober — aftermath and number, never the act): **The Cordon** (the Moura massacre — UN OHCHR: ≥500 unlawfully killed), **What Everyone Knows** (the African-Initiative FIMI operation staging the denial), **Until Further Notice** (party dissolution by decree), **Mobilised** (punitive conscription of critics — the BF 2023 decree), **The Quiet** (the media-ban ladder; *quiet is not calm*), **Who Is Left to Count** (MINUSMA gone, the sanctions Panel vetoed), **Struck Off** (the March-2026 sanctions reversal — documentation exposes but rarely punishes).
- **Each is a choice the player must make with their instruments:** *bear witness* — fund the documentation into the §20.4 **Exposure** track — or *look away*, which costs Local legitimacy and feeds grievance. The realities aren't narrated at the player; they arrive as decisions.
- **Honest sourcing (§20.6):** grounded in a verified research pass (UN OHCHR, Human Rights Watch, CPJ/RSF, the EEAS–VIGINUM report) and added to `rules/sources.json` with checkable URLs and confidence flags. Built from existing ops (added `exposure` to the event-effect schema enum; no new ops).
- **Calibration-safe:** the cards fire only after juntas form and never move the §12 junta-timing baseline — **Sahel calibration still 10/10; 103 tests pass / 0 xfail; both engines + smoke green.**
- *Honest note:* a coalition inner/outer-ring tiering was prototyped first and **reverted** — it measured ~0 effect (Regional Commands don't persist long enough for the nuance to matter), so it wasn't shipped. The real lever is grand-mode command persistence, a future pass.

## v0.21.0 — 2026-06-17

**The panels speak in objects too** (UI pass 5; finishing the "less wordy / ideas as objects" direction). The last text-heavy corner — the action list and region detail — now matches the header and map, so the whole interface is one visual language.

- **Costs are objects:** every action and the budget line read **🏛️ n · 💰 n**, not "n Mandate / n Funds".
- **Each action at a glance:** its family is an icon (⚔️ force · 🏗️ build · 🕵️ intel · 🤝 talk · 🏛️ home), its risk a **⚠️ %** (the backfire channel moved into the tooltip), its target a 📍 "tap a region".
- **Effect previews lead with the same icons:** 🏠 Home · 🤝 Allies · 🛡️ Local · 🏛️ Control · 🔥 Grievance · ☂️ UN cover · 🕵️ Intel · ⛓️ Drift — so a trade-off reads "🏠 −4 · 🛡️ −2" at a glance.
- **Region detail iconified:** 💥 Forces · 🏚️ Dug-in · ⚡ Activity · 🛡️ Local support · 🔥 Grievance · 🕵️ Visibility · 🪖 Pressure · 🏴 Foreign patron · 🔦 Exposure. The doctrinal terms stay in the tooltips (the legibility-gloss rule, DESIGN §13.3).
- Proto/UI only: engine, rules, and `rules/*.json` untouched, so the **103-test suite, both-engine smoke, and calibration (10/10) hold**. Completes the interactive UI arc (objects → situation-map → pan/zoom → motion → consistent object-panels).

## v0.20.0 — 2026-06-17

**Motion — the map reacts to a turn** (UI pass 4; what Stan asked for: "animate changes — a junta falling, a command planting, heat flaring"). Consequences are now *shown* on the board, not just itemised in the ledger.

- The board **snapshots itself before a turn resolves**; after it re-renders, exactly the nodes that changed get a **one-shot animation**: a **capital falling** flashes white, a theatre where **the insurgency flared** pulses its heat ring, a **newly-planted command** unfurls its flag.
- Driven by a pre/post diff (government rank worsened · estimated strength jumped >8 · a new theatre command), adding transient CSS-keyframe classes to just those node groups and auto-removing them before any later re-render — so panning/zooming never re-triggers them.
- Honours **`prefers-reduced-motion`** (animations off for users who ask). Subtle and purposeful — legibility motion, not decoration.
- Pure proto interaction: engine, rules, and `rules/*.json` untouched, so the **103-test suite, both-engine smoke, and calibration (10/10) hold**. This rounds out the "interactive & intuitive" UI arc (object-icons → situation-map → pan/zoom → motion).

## v0.19.0 — 2026-06-16

**Pan & zoom — the 40-nation board becomes legible up close** (UI pass 3; the density gap the last two passes flagged). The intuitive fix Stan's direction asked for.

- **The map's `viewBox` is now live:** drag to pan, pinch / mouse-wheel / buttons to zoom (pointer events throughout, `getScreenCTM` for cursor-anchored zoom, clamped to the board and to a sensible max zoom). Zooming just re-points the existing SVG — no re-render per frame, so it's smooth.
- **Tap vs. drag is disambiguated:** a small-movement tap selects a nation; a drag pans without mis-selecting. So selection and panning coexist on touch.
- **Zoom in and the names come back:** zoomed out, the dense board speaks in colour + heat and you tap to identify; once you zoom past a threshold, few nations are on screen so the labels and capital stars return automatically. Best of both — a clean overview *and* a readable close-up.
- A small **`+ / − / ⤢`** control sits on the map for discoverability (and the whole-map reset).
- Pure proto interaction: engine, rules, and `rules/*.json` untouched, so the **103-test suite, both-engine smoke, and calibration (10/10) hold**. `proto/preview.mjs` gained a `viewBox` argument so a zoomed-in theatre can be rendered for review. This closes the "make it interactive and intuitive" UI arc; production-grade pan/zoom and motion are the Godot client's to inherit.

## v0.18.0 — 2026-06-16

**A situation map, not a void — "can we make it prettier?"** (Stan). The board stops being circles on black and becomes a strategic map.

- **A real backdrop:** a deep-ocean radial gradient, a faint cartographic **graticule** (lat/long grid), and a soft **landmass under each theatre's nodes** — a padded, rounded convex hull, so adjacent theatres merge into a coastline — with faint region labels (SAHEL, MAGHREB, HORN…). The world now reads like an ops map.
- **The 40-nation world was re-laid-out** with breathing room (rough geography, grouped by theatre) so nodes stop piling up and the land shows through; node sizes and heat-rings tuned down to match. The 12-node Arc reads as a clean regional map (the Sahel as a landmass on the ocean).
- **The headless `proto/preview.mjs` gained the same backdrop** and drove every iteration (SVG → PNG via cairosvg) — the visual language was tuned without a browser.
- **Honest split** (answering "or is that future plans?"): the *vector situation-map aesthetic* is doable now in the greybox; *photoreal terrain, 3D situation-room lighting, and motion* remain the production-client goal (Godot, DESIGN §13.4), kept cheap by the JSON-core / swappable-renderer split. The greybox stays a legibility-and-balance instrument, never the ship look.
- Proto/UI only: engine, rules, and `rules/*.json` untouched, so the **103-test suite, both-engine smoke, and Sahel calibration (10/10) hold**; snapshot fresh. Next UI step: **pan/zoom** for the dense grand board.

## v0.17.0 — 2026-06-16

**Show, don't tell — the map starts speaking (UI pass 1)** (per Stan: less wordy, understand the game by inference from the screen, make each "idea" a concrete object). A presentation turn, not a systems one — no engine, rules, or calibration change.

- **The board carries the state now.** Insurgent strength is a **red ring whose thickness *is* the strength** — you read the hot spots at a glance instead of parsing numbers. Node colour is who-rules (green civilian · red junta · purple emirate · grey collapsed); your standing **Regional Command is a planted flag**; a **petro-state is an oil drop**; capitals a **★**.
- **A 40-nation board can't carry 40 labels**, so when the map is dense it drops them and you **tap a nation** to learn its name and read its detail — interactive and intuitive, not a wall of text. (The 12-node Arc stays fully labelled.)
- **Every resource is an object, not a word:** the header reads 🏛️ Mandate · 💰 Funds · 🏠 Home · 🤝 Allies · 🛡️ Local · ⛓️ Drift, with the explanations moved to tooltips and a concise visual map legend added to the Key. (Emoji/SVG glyphs stand in for the production art; the *principle* is what's binding — DESIGN §13.3 extended.)
- **New dev tool `proto/preview.mjs`** renders the board headlessly (SVG → PNG via cairosvg) so the visual language can be reviewed without a browser. It immediately earned its keep: it caught a real bug — the population-based node radius blew up at grand scale (India's 1.3M population drew a node covering half the map) — now **log-scaled and capped**.
- Proto/UI only: the engine, rules, and `rules/*.json` are untouched, so the **103-test suite, both-engine smoke, and Sahel calibration (10/10) are unaffected**; the proto snapshot stays fresh. Honest scope: the 40-node board is legible but **dense** — a pan/zoom pass is the next UI step.

## v0.16.0 — 2026-06-16

**The Emergency Powers track — and the thesis-as-test-suite is now complete.** The game's most central theme made fully mechanical: a democracy can win ugly with authoritarian powers, but the score knows. This promotes the **last remaining `xfail`** design-thesis test to enforced — all four of the design's load-bearing claims are now true by force.

- **The escalating ladder** (§7), each tier grounded in a real measure and built from existing ops (no new ops): **I — Surveillance Mandate** (existing; PATRIOT §215 / RIPA) → **II — Administrative Detention** (`administrative_detention`; Belmarsh, India's MISA, the French *Micas*: strong attrition + imposed governance, the threat removed without trial) → **III — Censorship & Martial Law** (`martial_law`; India 1975, Turkey's decrees: a large control/Order boost, the unrest blacked out). Each is cheap and front-loaded — **genuinely tempting**, real raw power a crisis-chasing player wants — and each adds permanent, one-way **Authoritarian Drift** (the ratchet: emergency powers are rarely repealed — France's 2017 SILT law folded the *état d'urgence* into ordinary law).
- **The cost is mechanical, never a scold** (Frostpunk's chief criticism, avoided by design): the new `drift_score_cost` makes Drift a **direct** score cost *as well as* the IntegrityMultiplier — the democracy is the prize, and every step toward autocracy spends it; blood (casualties) and backsliding (drift) now sit on the same ledger. A modest accidental-guerrilla backfire (Kilcullen) remains on each tier, but the decisive cost is the Drift, not luck.
- **The thesis, enforced:** `test_emergency_powers_tempting_but_scored` is promoted from `xfail` to enforced — `EmergencyPowersPolicy` now produces strictly **stronger raw** Stabilization×Order than pure kinetic (~16 vs ~10 across seeds: genuinely tempting) yet a strictly **worse final** score (~−9 vs ~−1: the game still knows). *Win ugly, score poorly.* **All four design-thesis tests are now true by force.**
- Ported to both engines (the drift cost mirrored in the proto score; the new tiers auto-listed from the snapshot). Calibration-safe: passive, competent, and kinetic play never drift, so the cost is zero for them — **Sahel calibration still 10/10**, the other three thesis tests untouched. Grounded in a research pass on real states of emergency, the ratchet effect, and the tempting-but-losing calibration. **103 tests pass / 0 xfail; calibration 10/10; determinism holds on both engines.**

## v0.15.0 — 2026-06-16

**Coalition burden-sharing — the second world-scale lever** (the follow-on to v0.14's Regional Commands). Allies share the upkeep so you can stretch further, but they free-ride and fray — depth, not a cost-multiplier.

- **The lever** (`sim/coalition.py`; new `rally_coalition` initiative + `coalition` op): one cohesion gauge (0–100). Allies bear `coalition_max_share · cohesion/100` of both the treasury upkeep **and** the accelerating home-front strain of your Regional Commands — modeled on the 87-member Global Coalition to Defeat ISIS, NATO, and the Lake-Chad MNJTF. A strong coalition lets you sustain more theatres than your home front could carry alone.
- **The thesis from a second angle** (Olson & Zeckhauser 1966, the economics of alliances): collective security is a public good, so partners under-provide. Cohesion **free-rides away** every turn; it frays **faster when the rival bloc is ascendant** (fair-weather members hedge toward the winning side — the §8 rivalry) and **faster the more commands you lean on it to carry** (over-extension feeds the case against you). You hold it up only by spending political capital to rally (with a burden-sharing-dispute backfire). You never escape free-riding — in play cohesion settles mid-range (NATO's 2% reality), not full.
- **Gated** by `coalition_enabled` (0 single-theatre → dormant, menu-filtered → **Sahel calibration still 10/10**; 1 grand).
- **Measured deepening:** giving `GrandCompetentPolicy` the coalition (rally when cohesion bleeds low) lifts it from beating passive 6/8 → **7/8 seeds**, ~19 → ~22 mean score, bending the world ~21 → ~18 juntas — a clear, **earned** improvement (cohesion costs capital and decays), still **bounded** (the world mostly burns; you hold the lines you choose). Pure doctrines still lose, kinetic worst.
- Ported to both engines (proto: a Rally-the-Coalition action + a cohesion line in the Regional-Commands readout). The briefing carries your own coalition cohesion (public). `tests/test_coalition.py` (7) pins the burden-share, the free-riding/rival fraying, the deepened win, and the gating. Design grounded in a research pass on coalition/alliance mechanics (Vic3 power blocs, EU4 favors/trust/aggressive-expansion, Stellaris federation cohesion, Five-Eyes inner/outer tiering). **102 tests pass / 1 xfail; calibration 10/10; determinism holds on both engines.**

## v0.14.0 — 2026-06-16

**Regional Commands — the first world-scale lever, and grand mode becomes winnable** (the milestone v0.13 named). v0.13 *measured* that the player's levers were too **local** to bend a 40-nation world, so abdication scored as well as effort. This builds the lever the research points to — and reaches the win, earned, not tuned.

- **The lever** (`sim/commands.py`; new `establish_command` initiative + `command` op): a **Regional Command** is a standing posture over a whole *theatre* (the real AFRICOM/CENTCOM, Operation Barkhane, the Lake-Chad MNJTF; the HoI4 garrison-template pattern) that passively **contains** insurgency across every one of its nodes each turn — light attrition on the strongest faction, a governance buffer, a local-legitimacy buffer. **Breadth, not depth:** it bends the trajectory and buys time but does not *resolve* a theatre — crises still need your hands-on actions. Posture sets the board; agency wins it.
- **The counterweight is the thesis** (Kennedy's imperial overstretch · Merom's home front · Mueller's logarithmic casualty curve): every command bleeds treasury upkeep and, more bindingly, **home legitimacy** each turn — and the home strain is **triangular in the count**, so the 2nd/3rd theatre costs far more than the first. A hard **cap** forbids policing everywhere (triage), and withdrawal fires on **politics, not defeat** (treasury can't sustain it, or Domestic falls through the floor) — leaving a vacuum, as Barkhane did.
- **Gated** by `commands_enabled` (0 single-theatre → dormant, inert, *filtered out of the action menu* → **Sahel calibration still 10/10 by construction**; 1 in grand).
- **The win, measured & earned:** a new `GrandCompetentPolicy` — lead with commands over the most volatile theatres, then triage hands-on, and don't over-extend a weak home front — **out-scores a passive world on 7 of 8 seeds and is the single best strategy**, above every pure doctrine, pure-kinetic still worst. The edge is **causal** (commands ON vs OFF moves both score and junta count) and **modest by design** (bends the world ~25→~21 juntas — helps without trivialising; you hold the lines you choose, never the whole world).
- Ported to both engines (proto: an Establish-Regional-Command action + a "Regional Commands" readout). The briefing now carries each node's `theater` and your own standing `commands` (both public). Grounded in three parallel research passes (coalition/burden-sharing COIN; grand-strategy scale mechanics; imperial-overstretch cost). `tests/test_commands.py` (7) pins the lever, the accelerating cost, the win, and the gating. **95 tests pass / 1 xfail; calibration 10/10; determinism holds on both engines.**

## v0.13.0 — 2026-06-16

**Grand-mode scoring made scale-invariant — and the winnability problem measured, not faked** (the milestone the v0.12 expansion made concrete). The headline is a structural fix plus an honest finding; it deliberately does **not** claim a balanced grand mode, because the evidence says one isn't reachable by tuning yet.

- **The bug:** at 40 nodes the single-theatre score (§11) degenerated — `order_mult = 1/(1 + junta_weight·junta_count + …)` uses an *absolute* count, so ~30 juntas drove it to ≈0.08 and crushed every policy's score to ≈0 (kinetic indistinguishable from competent). A scale bug, not a balance call.
- **The fix (`sim/markets`-style gating):** a new `grand_scoring` constant (0 in single-theatre → **byte-identical, Sahel calibration untouched, still 10/10**; 1 in grand) switches in a **scale-invariant containment** score — a world police can't stabilise 40 theatres, so it's judged on *containment*: **population-weighted quality** (√population, so protecting a consequential state counts for more than a micro-state) blended with the **free fraction** of the world's capitals (`1 − junta_share`), dragged down by consolidated authoritarian **blocs**. Scores are interpretable again and rank **kinetic abdication-of-restraint strictly worst** at every scale. Ported to both engines.
- **The honest finding (DESIGN §21.6), measured across seeds:** even with the corrected score, **no policy robustly out-scores passive at 40 nodes.** A benchmark containment policy (defend the capitals nearest collapse, hold the umbrella, sanction patrons) beat passive in **0–1 of 6 seeds** across a grid of scoring-weight × bandwidth settings; raising the per-turn mandate budget (a "global operation has more bandwidth" lever) let a competent player bend the world only from ~25 to ~19 juntas — a real but **marginal** edge its blood-and-treasure costs (the thesis: democracies pay at home) then erase. Diagnosis: the player's strategic levers are **too local to bend a global trajectory.**
- **Why ship it this way:** forcing competent > passive by tuning constants is exactly the dishonesty the thesis-as-tests discipline (§3.8) exists to prevent. So v0.13 ships the scoring **foundation** and *names the real milestone* — **winnable grand mode needs new world-scale levers** (coalition-building, regional commands that multiply reach, sanctions/economic statecraft with teeth, intelligence-sharing) plus a scoring stance that letting the bloc consolidate is a failing grade. That is the next design pass.
- `tests/test_grand.py` adds the scale-invariance + gating test; smoke checks proto parity. **87 tests pass / 1 xfail; calibration 10/10.**

## v0.12.0 — 2026-06-16

**The world widens — grand mode goes from ~20 to ~40 nations** (per Stan: "such scale there are as many nations on earth"). The scale the vision keeps asking for, with every new nation wired into the connective systems so it is part of one world, not an isolated region.

- **+20 nations** (`rules/scenarios/grand/nodes.json`), each grounded in a real 2001–2026 conflict: Sahel/Lake Chad (Burkina Faso, Chad, Mauritania, Cameroon), the Horn & Great Lakes (Ethiopia, Kenya, South Sudan, DR Congo, Central African Republic), MENA/Levant (Egypt, Tunisia, Lebanon), South & SE Asia (India's Naxalite belt + Kashmir, Myanmar's civil war, Bangladesh, Indonesia), Central Asia (Tajikistan), and the Americas/Caribbean (Mexico's cartels, Haiti's gang collapse, Ecuador). Now **40 nations across 15 theaters**.
- **One connected graph, not a bigger pile of regions:** +40 inter-theater **edges** (border / smuggling / arms / sea / ideology / diaspora) thread the new nations into the existing world; **regional patron leanings** exercise the v0.11 three-archetype contest (Wagner→Sahel & CAR, Iran→Lebanon & the Gulf, China→Myanmar & the Horn); petro-states (Chad, South Sudan, Egypt, Mexico, Ecuador) feed the oil market.
- **Realism pass:** genuinely resilient states (India, Egypt, Indonesia, Mexico, Kenya, Tunisia, Ethiopia, Bangladesh) are seeded to resist capture, so they hold while fragile states (Haiti, CAR, South Sudan, DR Congo, Myanmar) can fall — the world burns where it realistically would.
- **Both engines:** all 40 nations placed on the proto's world-map layout; `tests/test_grand.py` and `proto/smoke.mjs` now assert the ~40-nation scale; grand determinism holds on both. **Sahel history calibration still 10/10** (grand is a separate, gated scenario — untouched by construction). The `test_the_patron_contest_is_real` assertion was rewritten to hold **across seeds** (a distributional claim — "not a mercenary monopoly" — shouldn't pin one seed; across seeds all three archetypes win reach).
- **Honest scope (DESIGN §21.5):** scale is now done. The expansion makes the **next milestone** concrete and names it: a passive 40-node world burns (~30/40 capitals fall over 25 years — the thesis at scale), and the Sahel-tuned `CompetentPolicy` is spread too thin to out-score passive — grand mode needs its own **scoring weighting + a grand-scaled competent benchmark** (the way v0.5/v0.8 made the single-theater game winnable). Not faked here. **86 tests pass / 1 xfail; calibration 10/10.**

## v0.11.0 — 2026-06-16

**Deepen the ripples — global markets and a multi-patron contest** (per Stan: "deepen the ripples" — more realistic cross-theater channels so the world is genuinely interconnected, not isolated regions sharing a score). Two new systems on the §21.2 norms template, both gated calibration-safe.

- **Global arms & oil markets** (`sim/markets.py`, §21.3): two world prices (0–100, neutral 50) that the whole board moves and that move it back. **Arms** rises with worldwide insurgent strength and lifts insurgent **ExternalSupport in every theater** (an `arms_mult` on the external term, sibling to the norms' `recruit_mult`) — a violent world arms every front. **Oil** rises with petro-state instability (nodes whose `resources` include `oil`) and drags the importer-democracy's **Domestic** each turn through the ledger (`oil_market`) — the home front pays at the pump.
- **Rival patrons + global rivalry** (`rules/patrons.json` + generalized `sim/patrons.py`, §21.4): the §8 allegiance market becomes a **contest** of three real archetypes — **mercenary** (Wagner/Africa-Corps: fast, coup-proofing, oil-funded), **investor** (infrastructure-and-debt, non-interference), **proxy** (arms-and-advisers via the faction graph). Each captured state picks the highest-**appeal** patron (local standing + a bandwagon on its *global* `patron_strength` + speed + oil boost); a `rivalry` score tracks the share of the world the rival bloc holds, and a winning bloc captures faster.
- **Every choice connects, made literal:** targeted **sanctions** (the §20 `designate` op) now also dock the dominant patron's **global** strength — deny a patron one state and it is weaker in *all* of them.
- **Calibration-safe by construction:** both systems gated by `market_feedback` / `rivalry_feedback` — **0 in single-theater** (markets pinned at 50, `arms_mult==1`, no `oil_market` ledger line, mercenary-only pull byte-identical to v0.10 → **Sahel history still 10/10**), **>0 in grand mode**.
- Ported to both the Python sim and the JS prototype (a "World markets & rivals" readout joins "World precedent" in grand mode); `markets`/`patron_strength`/`rivalry` serialize. Fixed two JS-port parity bugs found in verification: node state now carries `resources` (so the oil market sees petro-states) and the smoke harness loads `patrons`. `tests/test_markets.py` (9 tests) enforces the ripples and the gating. **86 tests pass / 1 xfail; calibration 10/10; grand determinism holds on both engines.**
- Honest scope (DESIGN §21.5): this deepens the *systems* interconnection; grand mode is still **not** history-calibrated, and ~45 nodes, ideology contagion, and the map-UI pass remain the backlog.

## v0.10.0 — 2026-06-15

**Grand mode — the world scale, and the layer that makes every choice ripple everywhere** (per Stan: "go fully global now"). The v2.0 vision pulled forward; this is the tested foundation, with markets/multi-patron/more-nations to follow.

- **A world, not a region** (`rules/scenarios/grand/`): ~20 nations across ~11 theaters (Sahel, Maghreb, Horn, Gulf, Levant, AfPak, Caucasus, Central Asia, SE Asia, Andes, E/W Africa), composited *global* faction families (al-Qaeda-network, IS-lineage, ethno-separatist, narco-insurgency), and **inter-theater edges** (ideology, diaspora, sea lane, arms route) so contagion and blocs cross theaters. Quarter turns, 2001 start, 100-turn horizon.
- **The global norms / precedent layer** (`sim/norms.py`) — the keystone: how you fight (kinetic / lawful / autocratic) accumulates into three world norms that feed back into **every theater at once** — insurgent recruitment worldwide, your International standing, and rival-patron appeal. Verified ripple: pure-kinetic world → global recruitment ×1.25; pure development → ×0.76; emergency powers → ×1.49.
- **Calibration-safe by construction:** the layer is gated by `norm_feedback` — 0 in single-theater scenarios (so a passive Sahel never moves a norm; **history calibration still 10/10**), >0 in grand mode.
- Ported to both the Python sim and the JS prototype (grand in the scenario picker, world map layout, a "World precedent" readout); leak/exposure/bloc/norms state all serialized. `tests/test_grand.py` (8 tests) enforces the worldwide ripple and the single-theater gating. 76 tests pass / 1 xfail; smoke covers grand determinism.
- Honest scope (DESIGN §21.3): grand mode is the systems at world scale, **not yet history-calibrated**; node count toward ~45, arms/commodity markets, and multi-patron rivalry are the backlog.

## v0.9.2 — 2026-06-14

**Map legibility fix** (from Stan's playtest screenshot: region names rendered huge and ran off the right edge).

- SVG map text resized from ~11 to ~4 map-units, so names fit the board.
- Labels **flip to the left** for right-side nodes (`text-anchor:end`) so they can't overflow the edge; over-long names truncate (e.g. "Ouagadou…").
- Node radii trimmed; estimate/pip placement follows the flipped side. Proto-only; no state-shape change (saves stay valid).

## v0.9.1 — 2026-06-14

**Playtest fixes from Stan's first real session on the deployed build.**

- **Fixed: the map (and panel) showed nothing.** Root cause: a stale `localStorage` save from an older build was being restored into the current engine — the save format changed enormously across v0.3→v0.9 and `restore()` blindly merged it, so `renderMap()` threw and aborted the rest of the render (header survived, board went black). Fix: the save is now **version-gated** (`SAVE_VERSION`) and old-shape saves are discarded; rendering is **defensive** (unmapped nodes/edges and missing estimates can no longer throw); and the three panels render independently so a fault in one never blanks the others. *(Returning players may need one hard refresh to pick up the new build.)*
- **Less wordy / easier to read:** every event choice now shows a plain, colour-coded **preview of what it does** ("Home −4 · Local −2", "buries it (may leak later)") — the trade-off is legible without parsing prose. Flavor text on the base events trimmed to one or two punchy lines; the cryptic "Context: gao" is now "Where: Gao" (region name, not id).
- No engine/rules-logic or calibration change; 68 tests pass / 1 xfail.

## v0.9.0 — 2026-06-14

**Scenario 1 becomes a story you finish and learn from — endings, post-mortem, and the Sources screen** (the roadmap's v0.9). Preceded by a deliberate audit + bibliography-verification pass (per Stan's "ensure nothing obvious is overlooked, and more than enough research is done").

- **Endings matrix (§11), both engines:** `Engine.ending()` resolves Pax / Fortress / Retreat / Collapse on two data-driven axes — ABROAD (Stabilization × Order, so juntas/blocs count) and HOME (Integrity). Tests enforce that a passive player never earns Pax, that drift forces Fortress over Pax, and that a competent player reaches a held-line ending on some seeds (endings are reachable, not decorative).
- **Post-mortem reveal (§9):** `Engine.post_mortem()` and the proto end-screen surface the regions where the calm most lied — true vs last-believed insurgent strength — the deceptive-calm lesson made concrete, alongside the believed-vs-true chart.
- **Sources screen (§14/§17):** `rules/sources.json` ships the bibliography as schema-validated data, every entry carrying an honest confidence flag — `verified` (live-checked), `established` (canonical), or `alt_history` (the game's projection, explicitly not fact) — behind a disclaimer. Rendered in the proto's Key tab. Integrity is test-enforced: near-future material is labelled, not passed off as record. Live-verified this build: the Moura massacre figures (UN, May 2023) and the *Afghanistan '11* App-Store removal (2018).
- **Audit:** removed dead `detect_proto_blocs` (superseded by `sim/blocs.py` at v0.7); confirmed all 20 effect-ops are handled in both the Python and JS engines; sim/proto scoring and endings kept in lockstep.
- 68 tests pass / 1 xfail (emergency-powers, honestly deferred); calibration 10/10; lint + smoke + snapshot-drift green.

## v0.8.0 — 2026-06-13

**The game is winnable — and the design thesis is now fully enforced by CI.** Tuned the **player's tools and the scoring only**, never the passive world dynamics, so the Sahel history calibration held **10/10 throughout** while a genuine win path opened (the discipline honoured, not gamed).

- **Insurgent-grip discount (§11):** a region's stabilization is multiplied by `(1 − max(0.5·strength + 0.5·entrenchment)/100)` — a region painted with services but run by an entrenched insurgency counts as *unstabilized*. Pillar 4 (quiet ≠ peace) in the score itself; this is what makes hearts-minds-without-security lose on the scoreboard, not just on the strength axis.
- **Rebalance:** OrderMultiplier weights bloc *consolidation* and bites harder per junta; programmes made affordable (lower spend/casualty cost weights; Development cheaper and stronger, now also cuts grievance); treasury income up slightly. All player-facing or score-only — calibration-safe by construction.
- **`CompetentPolicy`** — the §3.7 "reasonable player": triages the capital nearest collapse, negotiates stalemates, sees-and-suppresses the worst regions, keeps an umbrella up, exposes blocs, and avoids casualty/drift-heavy tools. The balanced benchmark.
- **Outcome (mean final, arc):** Competent ≈ 12 > Passive ≈ 2 > every pure strategy (all negative-to-single-digit).
- **Two thesis tests promoted xfail → ENFORCED:** `test_no_pure_strategy_dominates_the_balanced_baseline` (§19.7) and `test_a_reasonable_player_can_beat_history` (§3.7). Emergency-powers stays xfail honestly — scored-worse holds but tier-1 surveillance isn't yet *genuinely tempting* (§3.5; awaits the full track).
- Grip discount ported to the prototype so both engines score alike. 60 tests pass / 1 xfail; calibration 10/10.

## v0.7.0 — 2026-06-13

**The endgame layer — the milestone where the game gains contest and clean exits, and Stan's expose-the-regime feature comes alive.** Four interlocking systems, in both the Python sim and the JS prototype, doc-code in lockstep.

- **Bloc consolidation clock (§5.4, `sim/blocs.py`):** adjacent non-civilian states federate and consolidate by stage over time, draining International via pooled propaganda and exporting grievance to civilian neighbours — *left alone, it grows.* Scoring's OrderMultiplier now weights blocs by consolidation, not just count.
- **Patron allegiance market (§8, `sim/patrons.py:market`):** the no-strings mercenary patron's capture of a regime is resisted by your International standing and the regime's Exposure — a credible offer competes; a weak one loses by default.
- **The Exposure system (§20, first cut):** `world.exposure[country]`, the `exposure`/`designate` ops, and four new initiatives — **Fund Independent Research**, **Support Exile Media**, **Targeted Designations**, **Negotiate a Settlement** — each with a documented backfire (funder's paradox, transnational repression, patron retaliation, spoiler attack). Exposure raises the patron's price, blunts bloc propaganda, and unlocks sanctions that strip patron influence and roll back consolidation.
- **Negotiation endgame (§7):** the `negotiate` op settles a *stalemated* faction (drains Forces, costs Domestic, earns International) — often the only clean exit.
- New constants for all four systems; new world state (`exposure`, `blocs`) serialized so determinism holds. `tests/test_endgame.py` (10 tests) covers each; **the history calibration still passes 10/10** after the changes. 57 tests pass / 2 xfail.
- The §19.7 dominance check stays `xfail` — honestly: the systems exist but their balance doesn't yet out-earn its cost (every policy still loses the arc). Making the balanced path win is the v0.8 tuning/playtest job; faking it would betray the thesis suite.
- Prototype: regime **Exposure** and **Foreign patron** readouts in the region detail, bloc-consolidation / designation / settlement headlines, the four new initiatives auto-listed, and a Key-glossary section on blocs/patrons/exposure.

## v0.6.0 — 2026-06-13

**The Transparency Dial — the thesis in one mechanic.** Plus a documented answer to "can we use newer tech?"

- **Disclose vs. suppress** (DESIGN §6): incidents with your fingerprints (partner atrocity, errant strike) now offer honesty (a reduced cost now) or burial (nothing now — but a **leak clock**). Each turn a buried scandal may leak; the chance rises with **press freedom** and the scandal's age, and a leak costs `leak_multiplier ×` the buried severity across all three gauges. A free press is what makes suppression dangerous — Merom, mechanized.
- New `suppress_clock` op and `press_freedom` / `leak_base` / `leak_age_factor` / `leak_clock_turns` / `leak_multiplier` constants, in both the Python sim and the JS prototype; leak-clock state is serialized so determinism holds.
- `tests/test_transparency.py` (6 tests) enforces the economics: suppression costs more on average than disclosure, yet sometimes costs nothing (the gamble is real), and more press freedom yields more leaks. 47 tests pass / 2 xfail.
- Prototype: a **Buried** counter in the header, leak/buried-safely headlines, and a Key-glossary entry; JS smoke now exercises the bury branch.
- **DESIGN §13.4 — presentation-technology evaluation:** Godot 4 as the primary production-client recommendation (Vulkan/OpenGL, real 3D, web+Android+Steam exports, Python-like GDScript), WebGPU+Babylon.js as the stay-on-web fallback that reuses the existing JS engine, raw OpenGL/Bevy/Unity assessed and declined. The JSON core makes the eventual 3D client a re-skin, not a rewrite.

## v0.5.2 — 2026-06-13

**Legibility pass on the prototype** — first playtest feedback was "too collated, words too specific, can't tell how the numbers relate." All UI; no engine/rules/calibration change.

- **Plain language, doctrine kept as gloss:** the insurgent axes now read **Forces / Dug-in / Activity** (Strength/Entrenchment/Visibility in the tooltip); gauges read **Home / Allies / Local**; **Mandate / Funds** instead of M/T.
- **Number relationships made visible:** every region stat is a labelled meter, coloured green/red for whether high is good or bad *for you*, with its ± uncertainty shown; a "dug-in but quiet" region is flagged with the deceptive-calm warning in plain words.
- **A "Key" tab** (always reachable): full plain-language glossary, the causal loop (grievance→forces; control+support→resist; unwatched→dug-in; region→capital→junta), and the map legend. Plus a one-time first-run orientation card and a header **?** button.
- De-cluttered map labels (forces estimate only); actions dim when unaffordable.
- DESIGN §13.3 gains two recorded directions: the long-horizon **3D/production-presentation goal** (Godot-leaning) and the **legibility principle** (readable without a manual; jargon-without-explanation = bug).

## v0.5.1 — 2026-06-13

**License resolved + the prototype is actually reachable.**

- **LICENSE.md — PolyForm Noncommercial 1.0.0** (canonical text + plain-English summary and rationale): source-available for any noncommercial use — play, modding, study, journalism — with commercial rights reserved so the Steam/itch.io path stays open; reversible toward more-open later. Resolves DESIGN.md open question #5.
- **GitHub Pages deploy** (`.github/workflows/pages.yml`) + a root `index.html` redirect → the game is live at `https://stan2032.github.io/PaxStressia/` (redirects to `/proto/`) once Pages is set to "GitHub Actions" (one-time toggle). The whole repo root is published so the proto fetches `rules/*.json` live — same source of truth as the sim. Fixes the earlier dead `localhost` instruction, which assumed a local clone + server that didn't exist.
- No engine/rules changes; constants and calibration unchanged.

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
