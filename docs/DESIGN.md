# MANDATE
### Design Document — v0.2
*Working title. A turn-based grand strategy game about being the world police in a world that keeps score.*

---

## 0. Document Conventions

- This document is **cumulative**: future versions expand from this one; nothing is removed without explicit instruction. Changelog at bottom.
- Every design call is tagged **DECIDED** (locked for v1 unless overturned), **PROPOSED** (my recommendation, awaiting sign-off), or **OPEN** (genuinely undecided, listed in §16).
- Sources for grounding claims are in §17. The design intends to *cite its homework in-game* (see §14).

---

## 1. Vision & Thesis

You lead a real-world democracy acting as the world's policeman. Your enemies are insurgencies that grow, network, and — left untended — capture states and weld them into authoritarian blocs that then export the problem outward. Your constraints are your own: voters, allies, law, and a free press.

The central thesis comes from Gil Merom's *How Democracies Lose Small Wars*: democracies are rarely defeated on the battlefield in counterinsurgency — they are defeated **at home**, when the domestic tolerance for cost and brutality collapses before the insurgency does. The game's job is to make that thesis *playable*: every lever that wins faster abroad corrodes something at home or among allies, and vice versa.

The secondary thesis comes from the Sahel, 2012–2026, where the premise of this game ran live: jihadist insurgencies metastasized across Mali, Burkina Faso, and Niger; coups followed; the juntas formed the Alliance of Sahel States, expelled Western forces, imported Russian mercenaries, dissolved political parties — and the insurgencies *kept growing anyway*, while the insurgents themselves began forming their own alliances. Both sides of the player's nightmare — networking insurgencies *and* consolidating authoritarian blocs — are documented, datable, and mechanizable.

**The question the game asks:** can you hold the line abroad without breaking the thing you're defending?

### Design Pillars

1. **Legitimacy is the only real resource.** Money and troops are instruments. Every cost in the game ultimately converts into one of three legitimacies: Domestic, International, or Local. (§6)
2. **The enemy is a network, not an army.** Insurgent power lives in edges — sanctuary, funding routes, ideological affinity — not in unit counts. Killing leaders feels good and accomplishes little; RAND's cross-conflict research is the rulebook here. (§5)
3. **Every tool cuts both ways.** No strictly-good buttons exist. FM 3-24's paradoxes ("the more force you use, the less effective you may be") are action-design law. (§7)
4. **Quiet is not peace.** Fog of war includes *deceptive calm*: an entrenched insurgency running shadow courts and taxes produces fewer incidents than a contested one. Without intel spend, the map lies to you. (§9)
5. **You can win ugly, but the game knows.** Emergency powers, dirty partnerships, and censorship are mechanically strong and permanently corrosive. The scoring system tracks democratic integrity to the end. Becoming the thing you fight is a playable — and scored — dark ending. (§7, §11)

---

## 2. World Framing

**DECIDED (per Stan, 2026-06-12): real world / alt-history.**

- **Lead nation:** the player chooses a real democracy. v1 roster **PROPOSED**: **United States** and **France** (the two with the deepest stabilization portfolios and the most distinct flavors — global reach + war-weariness vs. post-colonial baggage + regional depth). Stretch roster: UK, an EU-coalition seat, India. Each lead nation differs in: alliance web, basing access, domestic political system (presidential vs. parliamentary changes election cadence and Mandate mechanics, §6), historical-baggage modifiers on Local legitimacy per region, and starting patron relations.
- **States on the map:** real, named, with real starting conditions at the chosen start date.
- **Insurgent factions:** **PROPOSED — composited factions closely modeled on real groups**, openly sourced in briefing text (e.g., *Ansar al-Sahel* ≈ JNIM; *Wilayat composite* ≈ IS-Sahel/ISWAP; a Tuareg national front). Rationale: keeps journalistic grounding while granting design freedom (we can tune capabilities without misrepresenting real organizations), reduces defamation/platform friction, and lets alt-history diverge cleanly. An optional **"historical names" toggle** (Paradox-style) is **OPEN** (§16).
- **Patrons:** real states (Russia, China, Iran) acting as systemic rival patrons in grand mode; in scenarios they appear as the relevant patron archetype with real behavior models (Wagner/Africa Corps playbook, non-interference investment playbook, proxy-network playbook). (§8)
- **Alt-history divergence:** scenarios start at real historical junctures and let the player diverge from the record. Grand mode start date **PROPOSED: September 12, 2001** — the franchising-and-networking phenomenon this game is about (AQ affiliates → IS provinces → Sahel consolidation) is fundamentally the post-2001 story, and the player inherits the actual hand history dealt. A 1991 "Unipolar Moment" start is a stretch goal, not v1.
- **Tone:** sober, dossier-driven — Le Carré meets the situation room. No cartoon villainy. Local populations are treated as what COIN doctrine says they are: the prize, and too often the victim. Civilian harm is abstracted into grievance/legitimacy numbers and event text; never gore.

**Platform consequence of real-world framing (DECIDED as planning assumption):** Apple removed *Afghanistan '11* from the App Store for depicting a real conflict. Distribution order is therefore **web → Android → Steam/itch.io → iOS last (if ever)**. This also happens to fit the development stack (§13).

---

## 3. Player Fantasy & Core Loop

You are not a general. You are the executive of a democracy managing a global stabilization portfolio with limited attention, limited money, and a clock made of elections.

**Turn scale:** grand mode = 1 quarter per turn; scenario mode = 1 month per turn (**PROPOSED**).

**Turn structure (the loop):**

1. **Briefing phase.** The intel digest: what your agencies *believe* (estimates with confidence bands, §9), domestic headlines, ally requests, UN docket, patron movements. This is the game's signature screen — a morning folder, not a god's-eye map.
2. **Policy phase.** Spend **Mandate** (your action-point currency, §6) on Initiatives (§7) across theaters, plus diplomatic and domestic tracks. Queue covert operations (they resolve later, with risk).
3. **Resolution phase.** The world steps forward simultaneously: insurgent networks grow, spread, and link (§5); patrons act (§8); allies act according to *their own* domestic politics; queued ops resolve; events fire (§10).
4. **Consequence phase.** Itemized legitimacy deltas (the player must always be able to trace *why* a number moved — feedback clarity is a hard requirement), media cycle, election countdown ticks.

**Session shapes (DECIDED per Stan): both.** Scenario mode ships first (45–90 min runs, single theater, chained into a campaign); grand mode (the long Civ-style global game) follows once scenarios validate the systems. (§12)

---

## 4. The Map

**Region nodes, not hexes.** This is a strategic-portfolio game, not a tile-empire game — which is also half the reason an Unciv fork was rejected (§13).

- **Grand mode:** ~40–50 region nodes grouped into theaters (Sahel, Maghreb, Horn, Levant, AfPak, Central Asia, SE Asia, Andes, Caucasus, Gulf...). Twilight-Struggle scale, not Civ scale.
- **Scenario mode:** one theater at higher resolution — 8–15 nodes at province/district level, Rebel Inc intimacy.
- **Each node carries:** Governance, Development, Grievance, Population, Terrain/Access, Resources, your Presence & Posture, Patron influence, and an **insurgent presence vector** per faction: Strength, Entrenchment, Visibility (§5, §9).
- **Edges between nodes:** borders, smuggling routes, ethnic/ideological ties, sea lanes, diaspora links. **Edges are where the networking lives** — they carry insurgent funding, fighters, arms, and alliance formation, and they are targetable (interdiction) but never fully closable.

---

## 5. The Insurgency Model (the heart of the game)

Insurgencies are simulated as a **living graph**: faction nodes within map regions, with edges forming between them. The model is deliberately in the same family as decay/accretion/threshold network systems — strength accretes from inputs, decays under pressure, and crosses thresholds into new states.

### 5.1 Per-node growth

For each faction, in each region, per turn:

```
ΔStrength = Recruitment(Grievance, 1/Governance, Displacement, Unemployment)
          + ExternalSupport(Σ sponsor flow over connected edges)
          + AllianceBonus(linked-faction pooling)
          − Attrition(your ops, partner forces, rival factions)
          − Defection(amnesty programs, reconciliation, war exhaustion)
```

**Entrenchment** is the second axis: when Strength persists *uncontested* in a region, it converts into shadow governance — taxation, courts, recruitment pipelines. Entrenchment is what makes an insurgency survivable; Strength is what makes it dangerous this turn.

**Visibility** is the third: contested insurgencies produce incidents (high visibility); entrenched ones go quiet (low visibility). **High entrenchment + low intel coverage renders on your map as peace.** (§9 — this is Pillar 4, and it is drawn directly from 2026 Sahel analysis, where falling attack counts reflected insurgent entrenchment into local political and economic systems, not security gains.)

### 5.2 Networking (the player's nightmare, phase 1)

Factions form edges with each other when `(ideological affinity × mutual need × route access)` clears a threshold. Linked factions:

- pool external funding and arms (smoothing your interdiction wins),
- share TTPs — capability tier-ups (IEDs → SVBIEDs → drones → coordinated multi-region offensives),
- and can launch **joint offensives** — the historical model is the April 2026 JNIM + Tuareg-separatist coordinated attacks in Mali that killed the defense minister. Ideologically *unlike* groups allying out of shared interest must be possible and should surprise the player the first time.

Decapitation strikes remove a leader trait and disrupt temporarily; the succession roll can **radicalize** the faction (per RAND: leadership removal rarely ends insurgencies and sometimes worsens them).

### 5.3 State capture (the player's nightmare, phase 2)

When a faction's Strength-to-Governance ratio in a state's core region crosses threshold, a **collapse roll** fires. Outcomes:

1. **Failed state** — governance vacuum; every faction's recruitment accelerates; refugee event chains begin.
2. **Insurgent emirate** — the faction governs; becomes a sanctuary node and exporter.
3. **Junta** — *the military seizes power claiming only it can defeat the insurgency.* This is the Sahel pattern, and it should be the most common outcome in fragile-but-functional states. Crucially: **a junta is not your ally.** It dissolves parties, jails journalists, demands you drop conditionality — and its repression feeds Grievance, which feeds the insurgency it claimed it would crush.

### 5.4 Bloc formation (the player's nightmare, endgame)

Juntas and emirates adjacent in the graph can **federate** into a Bloc: mutual defense, a shared patron (§8), pooled propaganda reach (legitimacy warfare against you in *other* regions), and expansion pressure on neighbors. Blocs run an **institutional consolidation clock** — joint forces, shared currency plans, treaty deepening (the AES went from a 5,000-troop joint force to 15,000 within years, while leaving ECOWAS and dissolving domestic opposition). The longer a Bloc exists, the more expensive every option against it becomes. *Left alone, it grows. Connected, it accelerates.* This is the core prompt, mechanized.

---

## 6. The Legitimacy Economy

Three gauges, 0–100. Nearly every action in the game trades between them. **Itemized deltas every turn** — the player must always see why.

### Domestic Legitimacy (your voters)
- **Fed by:** visible wins, low casualties, low cost, homeland safety, honored promises.
- **Drained by:** body bags, taxes/deficits, quagmire turns (presence without progress), scandals, attacks at home.
- **Converts into Mandate**, the action-point currency: `Mandate/turn = f(Domestic, election proximity, crisis state)`. Post-election honeymoons are fat; lame-duck and post-scandal turns are thin. **This single coupling makes domestic politics the engine room of the entire game.**
- **Elections** every 16 turns (US, quarter-scale) or per parliamentary rules (France/UK rosters). Losing an election is not losing the game (continuity model **OPEN**, §16) — but it reshapes your mandate profile mid-campaign.

### International Legitimacy (allies, institutions, world opinion)
- **Fed by:** multilateralism, transparency, legal process, burden-sharing, keeping commitments.
- **Drained by:** unilateral strikes, civilian casualties, hypocrisy events (preaching democracy while backing a junta), abandoning partners.
- **Gates access to:** coalition troops (with **ally caveats** — allied contingents whose domestic politics restrict their rules of engagement, the NATO-in-Afghanistan mechanic), basing rights, sanctions efficacy, UN mandates (a cheap legitimacy umbrella that is slow and vetoable).

### Local Legitimacy (per region — the actual COIN win condition)
- **Fed by:** services that work, security *with restraint*, functioning courts, jobs, respected local agency.
- **Drained by:** collateral damage, abusive partner forces, corruption of the client you protect, and **occupation duration itself** — presence past a welcome threshold generates antibodies (Kilcullen's "accidental guerrilla" dynamic).
- Local legitimacy is the slowest gauge to raise and the only one that *permanently* starves an insurgency.

### The Transparency Dial (the Pentagon Papers mechanic)
Every incident with your fingerprints (errant strike, partner atrocity, detainee abuse) offers a choice:
- **Disclose:** immediate Domestic hit, International largely preserved, Local damage reduced (honesty registers).
- **Suppress:** no immediate cost — but a **leak clock** starts, scaling with press freedom and time. A leak multiplies the original damage across *all three* gauges and can fire election-shock events.

This dial is the thesis in miniature: transparency is expensive every single time, and cheaper than the alternative on average — *if* you survive the variance.

---

## 7. Initiatives (the action catalog)

Five families, ~8–12 initiatives each. **Design law: every initiative has a cost, a benefit, and a documented backfire channel.** No strictly-good buttons (Pillar 3). Representative entries:

### Military
| Initiative | Benefit | Backfire channel |
|---|---|---|
| Presence patrols | Suppresses Strength, raises Visibility of insurgents | Casualty drip → Domestic; duration → Local antibodies |
| Partnered raids | Cheap attrition | Partner conduct events → Local, International |
| Drone strikes | Fast, no body bags | Collateral roll → Local crater + martyrdom recruitment spike |
| Surge | Large suppression window | Huge Mandate/treasure cost; withdrawal cliff scheduled the day it starts |
| Train & equip | Cheap force multiplier | **Coup-seed** (trained officers raise junta odds — several Sahel coup leaders were Western-trained) + arms leakage to the graph |
| Private contractors | No body-bag Domestic cost | Accountability scandals at 2× magnitude |

### Governance & Development
Wells/roads/schools (slow Local gains; insurgent tax target), anti-corruption drives (Local up, **client cooperation down** — you are threatening your host's patronage network), election support, **amnesty & reintegration** (drains insurgent Strength via Defection; "soft on terror" Domestic hit).

### Intelligence
HUMINT networks (reveals Entrenchment truth — the only counter to deceptive calm), SIGINT dragnet (cheap broad intel; **civil-liberties scandal channel at home**), infiltration (enables precision ops; blown-agent event risk).

### Diplomatic
UN mandate seeking, coalition building (burden-sharing + caveats), sanctions (pressure + humanitarian blowback that patrons exploit in the propaganda war), patron summits (détente trades — expensive, occasionally decisive), and **negotiation with insurgents** — the Rebel Inc endgame, unlockable when strength ratios stalemate; splits Domestic and International in opposite directions and is often the only clean exit.

### Domestic
Strategic messaging, war-powers requests, veterans programs (slowly heals war exhaustion), and the **Emergency Powers track**: surveillance expansion → press restrictions → detention authorities → executive emergency rule. Each tier grants *real, immediate mechanical power* — and permanently raises your **Authoritarian Drift** score (§11). The track must be genuinely tempting. That is the point.

---

## 8. Patrons & the Allegiance Market

Two to three systemic rival patrons (grand mode), modeled on documented playbooks:

- **The mercenary patron** (Russia/Wagner–Africa Corps model): coup-proofing services, no human-rights strings, payment in mining concessions, arrives fast.
- **The investor patron** (China model): infrastructure-for-influence, non-interference doctrine, debt leverage, plays the long game.
- **The proxy patron** (Iran model): arms and ideology through the faction graph itself.

**The market mechanic:** every weak or client state continuously compares offers. Yours comes with conditionality — human-rights strings, transparency requirements, election timelines. The patron's comes with none. Your International legitimacy raises the perceived value of your offer; your scandals raise theirs. Clients **can and will defect mid-game** (the Mali-expels-France beat). When a junta forms (§5.3), the patron's offer usually beats yours by default — unless you drop your conditions, which costs International and Integrity.

**You are competing in a market for allegiance, not just fighting a war.** Half the game's losses should happen at the negotiating table you weren't invited to.

---

## 9. Information & Fog

Every insurgent number the player sees is an **estimate**: `displayed = true × noise(intel coverage)`, with confidence bands rendered honestly in the briefing.

- Low coverage + high Entrenchment = **the map shows peace where there is shadow government.**
- Intel initiatives buy variance reduction, not omniscience.
- **Post-mortem reveal:** at scenario end, the game replays the true history against what you believed at each turn. This is the signature learning loop — and the replayability engine.

---

## 10. Events

Deck-driven, historically sourced, weighted by world state. Every event is a choice with a legitimacy-triangle trade. Representative cards:

leak/whistleblower (suppression clocks come due) · partner-force atrocity (your flag on it) · hostage crisis (rescue/ransom/refuse) · refugee wave (Local → International → Domestic cascade) · base access revoked · election shock at home · patron false-flag · aid-worker kidnapping · client demands you silence criticism · "Mission Accomplished" trap (declare victory now for a Domestic spike; relapse risk doubles) · journalist killed with partner's weapon · your trained battalion announces a "transitional council."

---

## 11. Win, Loss & Scoring

Grand mode runs a fixed horizon (e.g., 100 turns / 25 years) or ends early in collapse. Scenarios use bespoke objectives plus the same integrity accounting.

```
Final Score = StabilizationIndex × OrderMultiplier × IntegrityMultiplier − Costs

StabilizationIndex = Σ (Local legitimacy × Governance) across contested theaters
OrderMultiplier    = f(Bloc containment: count, size, consolidation stage)
IntegrityMultiplier = 1.0 at zero Authoritarian Drift, decaying per tier used
```

**Endings matrix** (each a written epilogue, judged by the three axes):

- **Pax** — stabilized abroad, intact at home, allies still answer the phone. The hard ending.
- **Fortress** — you won abroad and hollowed out the republic. *"You kept the peace and lost the thing it was for."* High Stabilization, gutted Integrity. The game's signature dark ending.
- **Retreat** — clean hands, burning world. Integrity pristine, Blocs ascendant.
- **Collapse** — quagmire abroad, exhaustion at home, the Bloc sets the terms now.

Losing an election ≠ game over (**OPEN** continuity model, §16). Becoming an autocracy to win *is* mechanically possible — and the epilogue will say so plainly.

---

## 12. Modes & Content Plan

**DECIDED (per Stan): scenarios first, grand mode later.** Scenarios are the systems-validation ladder; grand mode is gated on Scenario 1 being *fun*, not just correct.

### Scenario 1 — vertical slice: **"The Arc" — Sahel, 2012–2026**
- **Map:** ~12 nodes — Bamako, Mopti, Gao, Kidal, Ménaka, Ouagadougou, northern Burkina, Niamey, Tillabéri, Tahoua, Lake Chad rim, coastal-spillover marker (Benin/Togo north).
- **Factions:** *Ansar al-Sahel* (≈ JNIM composite), *Wilayat* composite (≈ IS-Sahel), Tuareg national front, three fragile states, mercenary-patron actor.
- **Player seat:** France-analog or US seat (both shippable from one event deck with different baggage modifiers).
- **Historical beats as event deck:** 2012 northern collapse, 2013 intervention window, 2020–23 coup cascade, ECOWAS rupture, AES formation, mercenary arrival, 2026 insurgent-alliance offensives. The player can prevent, divert, or ride each beat.
- **Calibration test (this is the special sauce):** run the sim with a *passive* player. It should approximately reproduce history — coups by ~turn 100±, Bloc formed, insurgent territory expanded. **Reality is our balance baseline.** If untouched-sim ≠ history, the constants are wrong. If a reasonable player can beat history, the game has hope in it. (§13.3)

### Scenario 2–3 (later)
- **Colombia / Plan Colombia (1999–2016):** the qualified COIN success — proves the design isn't an unwinnable misery sim, and exercises the negotiation endgame (Havana accords).
- **AfPak (2001–2021):** the sanctuary problem and the withdrawal cliff, at maximum difficulty.

### Grand mode
Global ~45-node map, Sept 2001 start (**PROPOSED**, §2), 25-year horizon, all systems live. Ships only after two scenarios validate.

---

## 13. Technical Architecture

### 13.1 Decision: why not Unciv
- Unciv mods are JSON files that alter the data of *existing* game objects; even total-conversion "base ruleset" mods operate inside vanilla mechanics. There are no scripting hooks for legitimacy gauges, network propagation, patron markets, or election engines — every system in §5–§10 is engine work, not data work.
- A Kotlin fork could do it, but inherits a hex/tile-empire chassis this design rejects (§4), and Unciv's own docs recommend against mod development from a phone — a poor match for a Termux-centered workflow.
- **DECIDED: build fresh.**

### 13.2 Data-driven core (the architectural law)
**All rules live in JSON**: region nodes, edges, factions, initiatives, event cards, constants. One source of truth, consumed by both the simulation core and every client. Consequences: traceability (every balance change is a diff), modding support for free (our own mods directory from day one — the Unciv lesson kept, the engine limits dropped), and clean separation of sim from presentation.

### 13.3 Phases
- **Phase 0 — Web prototype (next step after this doc):** a single-file HTML/JS playable of *Sahel-lite* — 6 nodes, 3 systems only (legitimacy triangle, network growth, ~8 initiatives), persistent saves. Runs in a phone browser. Question it answers: **is the core loop fun in 20 minutes?**
- **Phase 1 — Repo + Python simulation core:** GitHub repo, `sim/` package implementing §5–§10 headlessly, pytest suite, and a **Monte Carlo balance harness** — 1,000 headless runs per config, with *design-thesis regression tests*:
  - `test_passive_player_reproduces_history` (the Sahel calibration, §12)
  - `test_pure_kinetic_strategy_loses_integrity_and_local`
  - `test_pure_hearts_minds_without_security_loses_to_momentum`
  - `test_emergency_powers_tempting_but_scored`
  GitHub Actions CI mirrors the existing pipeline patterns (lint, tests, artifact outputs: balance plots, run logs, JSON checkpoints). This phase is deliberately in familiar territory: the sim *is* a decay/accretion network with thresholds — the same machinery family as prior network projects, pointed at geopolitics.
- **Phase 2 — Production client:** re-evaluated after Phase 1 with real data. Candidates: stay web (PWA; itch.io; Steam via wrapper) vs **Godot 4** (GDScript reads like Python; GitHub Actions can build Android APKs, keeping the phone-based workflow viable). The JSON core makes this a presentation decision, not a rewrite.

---

## 14. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| **Misery-sim / whack-a-mole feel** | Scenario scoping; itemized feedback; negotiation comeback arcs; post-mortem reveals that make losses *interesting*; Colombia scenario proves winnability |
| **Political heat** (real-world framing) | Sober tone; composited factions; civilian harm abstracted; an in-game **Sources screen** — the bibliography (§17) shipped as a feature, framing the game as systems journalism |
| **App Store removal precedent** | Distribution order web → Android → Steam/itch → iOS last |
| **Scope creep** | Scenario ladder gates grand mode; this doc's DECIDED/OPEN discipline; versioned roadmap |
| **Solo dev, mobile-first workflow** | Everything data-driven; headless sim testable in Termux; CI builds clients; thin presentation layers |
| **Both-sides-ism / false equivalence** | The game has a point of view: legitimacy is real, autocracy is scored as loss even when it "works." The thesis is the spine, not a shrug |

---

## 15. Roadmap (versioned)

| Version | Deliverable |
|---|---|
| **v0.1** | This document |
| **v0.2** | JSON schemas (nodes, factions, initiatives, events) + sim skeleton + first tests |
| v0.3 | Web prototype: core loop playable (Sahel-lite, 6 nodes) |
| v0.4 | Full Scenario 1 map + event deck in data |
| v0.5 | Balance harness + history-calibration passing |
| v0.6 | Fog/intel + transparency dial + elections |
| v0.7 | Patrons + bloc formation + negotiation endgame |
| v0.8 | Scenario 1 content-complete; playtest round |
| v0.9 | Post-mortem reveal, endings, sources screen |
| **v1.0** | Scenario 1 ("The Arc") ships |
| v1.x | Colombia, AfPak scenarios |
| v2.0 | Grand mode |

---

## 16. Open Questions (for Stan)

1. **Election-loss continuity:** when you lose an election — do you (a) keep playing as the state with a changed mandate profile (continuity-of-government model), (b) score out and end the run, or (c) optionally switch seats to the new administration with shifted modifiers? *(My lean: (a) for scenarios, (c) as a grand-mode option.)*
2. **Historical-names toggle:** ship real insurgent-group names behind an optional toggle, or composites only? *(My lean: composites only at v1.0; revisit.)*
3. **Lead-nation roster at v1.0:** US-only, or US + France? *(France is the natural Scenario 1 seat; my lean: both, one event deck.)*
4. **Working title:** **MANDATE** — chosen for the triple meaning (electoral mandate / UN mandate / the colonial League-of-Nations mandates the word can't escape — intentionally uncomfortable). Alternates considered: *Pax*, *The Long War*, *Thin Blue Marble*. Keep MANDATE?
5. **License/openness:** open-source like Unciv (community + mods + your public-repo workflow) vs. closed (commercial option preserved)? Affects repo setup at v0.2.
6. **Multiplayer:** ever? *(My lean: no — the design is a solitaire system game like Rebel Inc; a "shared world, compared scores" async mode is the only plausible shape, post-v2.)*
7. **Repo name vs. working title** *(added v0.2)*: the GitHub repo is **PaxStressia**; the docs' working title is **MANDATE** (and *Pax* was a shelved alternate, §16.4). Is *PaxStressia* (a) just a repo codename, (b) the new title, or (c) a placeholder until #4 is answered? Docs keep MANDATE until you call it. *(My lean: treat as codename; decide title at v0.8 when store pages exist.)*

---

## 17. Sources & Grounding (to ship in-game)

**Doctrine & theory:** Galula, *Counterinsurgency Warfare* (the 80% political rule) · US Army/USMC FM 3-24 (the paradoxes) · Kilcullen, *The Accidental Guerrilla* (occupation antibodies) · Merom, *How Democracies Lose Small Wars* (the domestic-tolerance thesis) · RAND, *How Insurgencies End* and *Paths to Victory* (sanctuaries & sponsors decide; decapitation doesn't; ~decade durations).

**The live case:** the Sahel arc 2012–2026 — JNIM/IS-Sahel expansion; the Mali–Burkina–Niger coup cascade; Alliance of Sahel States formation, ECOWAS exit, party dissolutions, Africa Corps arrival; the April 2026 insurgent-alliance offensives; analyst findings that falling incident counts reflected entrenchment, not peace. (CFR Global Conflict Tracker; ACLED; ICG reporting.)

**Design precedents:** *Rebel Inc.* (reputation, intel fog, civ/mil initiative balance, negotiated endings) · GMT's COIN board-game series — *Fire in the Lake*, *A Distant Plain* (proof this problem space is fun turn-based) · *Twilight Struggle* (global influence at node scale) · *Afghanistan '11* (hearts-and-minds ops layer; cautionary platform tale) · *Plague Inc.* (network-growth pacing as antagonist).

---

## 18. Simulation Specification (v0.2 — PROPOSED; the contract between this document and the code)

*Added at v0.2. This section binds the prose of §3–§11 to the implementation in `sim/` and the data in `rules/`. Everything here is PROPOSED until the v0.5 calibration pass; constants live in `rules/constants.json` so every balance change is a readable diff (§13.2). Where this section and the code disagree, that is a bug in one of them — file it, fix it, and keep them in lockstep.*

### 18.1 Determinism law
- The engine owns exactly **one** RNG: `random.Random(seed)`. Every stochastic draw in a run flows through it. No other entropy source may be touched by sim code.
- Wherever iteration order can affect outcomes, collections are iterated in **sorted id order**.
- World state serializes to **canonical JSON** (sorted keys). Two runs with equal rules + equal seed + equal policy must produce **byte-identical** checkpoints at every turn. This is test-enforced (`tests/test_determinism.py`) and is a precondition for the Monte Carlo harness, replays, and the post-mortem reveal.

### 18.2 State vectors (normative shapes live in `rules/schema/`)
- **Node:** `id, name, country, capital, governance, development, grievance, population_k, access, resources, government (civilian|junta|emirate|failed), local_legitimacy, intel_coverage, patron_influence{patron→0–100}, presence{faction→{strength, entrenchment, visibility}}` plus runtime fields the engine owns: `ops_pressure, partner_capacity, coup_risk, uncontested_turns{faction}`.
- **Edge:** `id, a, b, types[] (border|road|river|smuggling|ethnic|…), capacity (0–1), interdiction (0–1, runtime)`. Edges are first-class and targetable; never fully closable (interdiction is capped below 1.0 by `edge_interdiction_cap`).
- **Faction:** `id, name, composite_of (the sourcing note — journalistic grounding lives in the data), ideology[], sponsor, capability_tier, relations{faction→affinity −1..1}, links[] (runtime: formed faction–faction edges with formed_turn)`.
- **PlayerState:** `domestic, international (0–100), mandate, treasury, authoritarian_drift, emergency_tier, casualties, turns_since_election, honeymoon_left, suppress_clocks[] (reserved for v0.6), spent_total`.
- Local legitimacy is **per node** (§6); Domestic and International are global gauges.

### 18.3 Turn resolution order (fixed; the §3 loop made executable)
1. **Briefing** — compute fog estimates (18.6), mandate income (18.7), headlines; hand the briefing to the policy.
2. **Policy** — `policy.choose(briefing, legal_actions) → orders`; engine validates targets and debits Mandate/treasury. Unaffordable orders are rejected, not partially applied.
3. **Resolution** — substeps in this exact order:
   a. apply initiative effects (immediate ops; register lingering effects with expiry),
   b. roll backfire channels for initiatives used this turn,
   c. per-(faction, node) growth, sorted — each ΔStrength term computed and **logged separately** (18.5),
   d. entrenchment conversion and visibility update,
   e. faction networking check (link formation, §5.2),
   f. state-capture collapse rolls on capital nodes (§5.3),
   g. patron influence drift (v0.2 stub: mercenary patron gains in junta states),
   h. event draw and resolution (weights + `requires` predicates; the policy picks a choice, default = first).
4. **Consequence** — expire lingering effects; convert the turn's casualties/spending into Domestic ledger entries; election tick and resolution (18.7); compile the **TurnReport** (itemized ledger + true-state snapshot appended to run history for the post-mortem).

### 18.4 Effect-op vocabulary (the data → engine contract)
Initiatives and event choices express consequences as lists of typed ops. Implemented at v0.2:

| op | target | meaning |
|---|---|---|
| `ops_pressure {amount, turns}` | node | military pressure; feeds Attrition and contests entrenchment while active |
| `attrit {amount}` | node | immediate Strength hit to the strongest faction present (v0.2 simplification: true strongest; later: strongest *estimated*) |
| `intel {delta, turns}` | node | intel coverage boost (variance reduction, not omniscience) |
| `local_legitimacy {delta}` | node | itemized Local change |
| `domestic_legitimacy {delta}` / `international_legitimacy {delta}` | global | itemized gauge change |
| `governance {delta}` / `development {delta}` / `grievance {delta}` | node | structural shifts |
| `amnesty {rate, turns}` | node | defection drain on Strength while active |
| `partner_capacity {delta}` | node | host-force multiplier (feeds Attrition) |
| `coup_seed {delta}` | node's country | raises junta odds on collapse rolls — the Train & Equip backfire made persistent |
| `drift {tiers}` | global | permanent Authoritarian Drift increment (scoring multiplier, §11) |
| `intl_umbrella {delta, turns}` | global | UN-mandate style per-turn International trickle while active |

**Backfire block** (required on every initiative — schema-enforced; Pillar 3 as a validation rule): `{channel, probability, effects[], note}` rolled at substep 3b. A deferred-clock form (`{clock: turns}`) is reserved for the Transparency Dial at v0.6. Reserved ops (documented now, implemented per roadmap): `interdict_edge, decapitate, surge, contractors, sanction, summit, negotiate, messaging, war_powers, veterans`.

### 18.5 v0.2 formulas (constants in **bold** are keys in `rules/constants.json`)
Per (faction *f*, node *n*) each turn, with all gauges 0–100 and clamped:

- `Recruitment = `**k_recruit**` × (grievance/100) × (1 − governance/100) × junta_amp` where `junta_amp = 1 + `**junta_recruit_amp** if the node's government is a junta (repression feeds the loop, §5.3) else 1.
- `ExternalSupport = `**sponsor_flow**` × route_factor × (1 + `**k_pool**` × n_links)` where `route_factor` = mean over *n*'s edges of `capacity × (1 − interdiction)` — sanctuary/sponsor flow rides the edges (Pillar 2), and links pool it (§5.2).
- `AllianceBonus = `**k_alliance**` × n_links` (faction-level link count).
- `Attrition = (ops_pressure + partner_capacity × `**k_partner**`) × `**k_attrit**` × (strength/100)`.
- `Defection = amnesty_rate × strength` (while an amnesty op is active).
- `ΔStrength = Recruitment + ExternalSupport + AllianceBonus − Attrition − Defection` — **each term logged separately** in the TurnReport so balance work reads causes, not net effects.
- **Entrenchment:** if `strength ≥ `**entrench_strength_min** and `ops_pressure < `**entrench_pressure_max**, the node is *uncontested* for *f*: `entrenchment += `**k_entrench**` × strength/100`. Entrenchment decays only through Local legitimacy: `−`**k_entrench_decay**` × local_legitimacy/100` per turn. (Strength is the danger now; entrenchment is the survivability — §5.1.)
- **Visibility** relaxes toward `target = `**vis_floor**` + `**vis_contest**` × min(1, ops_pressure/`**pressure_ref**`) × 100 − `**vis_quiet**` × entrenchment` at rate **vis_smooth** per turn. Contested = loud; entrenched = quiet (Pillar 4).
- **Networking (§5.2):** for factions *f, g* sharing or adjacent to common nodes, a link forms when `affinity_eff × mutual_need × route_access ≥ `**link_threshold**, where `affinity_eff = max(affinity, `**affinity_floor**`)` — the floor keeps ideologically *unlike* alliances possible (the JNIM+FLA surprise), `mutual_need` rises with both factions' recent attrition, and `route_access` is the best shared-route factor.
- **Collapse roll (§5.3),** capital node of country *c*: `threat = max over c's nodes of strength × (0.5 + entrenchment/200)`; when `threat / governance_capital ≥ `**collapse_ratio**, roll outcome weights `{junta: `**w_junta**` + coup_risk, failed: `**w_failed**`, emirate: `**w_emirate**` × (capital entrenchment share)}`. Junta: governance −**junta_gov_hit**, grievance +**junta_grievance_hit** country-wide, mercenary patron influence +**junta_patron_gain**, government = junta. One collapse per country at v0.2 (re-collapse chains land with blocs, v0.7).
- **Fog estimate (§9):** `σ = `**fog_sigma_max**` × (1 − coverage)`; `bias = −`**fog_calm_bias**` × (entrenchment/100) × (1 − coverage)`; `displayed = max(0, true × (1 + bias + ε))`, `ε ~ N(0, σ)`; the briefing renders `displayed ± 1.64σ·true` as a 90% band. The bias term **is** deceptive calm: entrenched and unwatched reads *low*, honestly delivered as a confident-looking wrong number. Entrenchment estimates use `σ × `**fog_entrench_mult** (the truth HUMINT exists to buy).
- **Mandate income (§6):** `mandate = max(1, round(`**mandate_base**` × (0.5 + domestic/100) × phase))` with `phase` = **honeymoon_mult** for **honeymoon_turns** after a won election, **lameduck_mult** in the last **lameduck_turns** before an election while `domestic < 50`, else 1.0.
- **Election** every **election_period_turns** (60 at month scale — France-analog seat): `P(win) = 1/(1+e^{−(domestic−50)/`**election_k**`})`. Win → honeymoon. Loss → v0.2 implements continuity model (a): play continues, `domestic → 50 + (domestic−50)×`**continuity_reversion**, and a thin-mandate spell follows. (Open question #1 still stands; this is the scenario-mode placeholder.)
- **Scoring (§11):** `Stabilization = 100 × Σ(local/100 × governance/100)/n_nodes`; `OrderMult = 1/(1 + `**order_junta_weight**` × juntas + `**order_bloc_weight**` × blocs)` (blocs are detection-only at v0.2); `IntegrityMult = max(`**integrity_floor**`, 1 − `**drift_per_tier**` × drift)`; `Costs = casualties × `**cost_per_casualty**` + spent × `**cost_spend_norm**`. `Final = Stabilization × OrderMult × IntegrityMult − Costs`.

### 18.6 The itemized ledger (feedback clarity, mechanized)
Every change to any gauge goes through one function and produces a `LedgerEntry{turn, gauge, source, delta}` where `gauge ∈ {domestic, international, local:<node_id>}` and `source` is the initiative/event/system id that caused it. The engine **guarantees** (test-enforced) that each gauge's change in a turn equals the sum of its entries. The TurnReport carries the entries verbatim — this is the §3 Consequence-phase contract, the balance-tuning instrument, and the data spine of the v0.9 post-mortem reveal.

### 18.7 Policy interface (the harness's hands)
`Policy.choose(briefing, actions) → [orders]` and `Policy.choose_event(event) → choice_index`. Built-ins shipped at v0.2, named for the thesis tests they serve (§13.3): `PassivePolicy` (does nothing — the history-calibration baseline), `PureKineticPolicy` (military family only), `PureHeartsMindsPolicy` (governance/development only), `EmergencyPowersPolicy` (kinetic + every drift tier available), `RandomPolicy` (seeded chaos for fuzzing).

### 18.8 Deliberately stubbed at v0.2 (so no one mistakes scaffolding for systems)
Faction links form and pool support, but **joint offensives** don't fire yet · presence does not yet **spread to new nodes** over edges (growth is per-seeded-node; spread lands with the full arc map, v0.4) · proto-blocs (adjacent juntas) are **detected and logged**, but the consolidation clock doesn't run · the patron exists as **influence drift only** — the allegiance market (§8) lands v0.7 · the Transparency Dial and suppression clocks are schema-ready but inert until v0.6 · negotiation endgame v0.7 · war exhaustion, occupation-duration antibodies, ally caveats, decapitation/succession, capability tier-ups, surge/withdrawal cliff, contractors, sanctions, summits — all reserved, per the §15 roadmap. The four thesis tests exist as `xfail` stubs so the suite *names* the destination before the road is built.

---

## Changelog

- **v0.1** — 2026-06-12 — Initial full draft from core prompt + research session (Unciv feasibility check; Sahel 2012–2026 record). Framing locked: real world / alt-history; scenarios-first; design-doc-first per Stan's three scoping answers.
- **v0.2** — 2026-06-12 — Repo bootstrapped (`stan2032/PaxStressia`). Added §18 Simulation Specification (determinism law, state vectors, resolution order, effect-op vocabulary, v0.2 formulas bound to `rules/constants.json`, itemized-ledger contract, policy interface, stub inventory). Added open question #7 (repo name *PaxStressia* vs working title *MANDATE*). §15 roadmap: v0.2 row marked delivered. No prior content removed.
