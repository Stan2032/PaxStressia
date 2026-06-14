# MANDATE — Full Project Context & Handoff
**v0.1 · 2026-06-12 · Origin: design/research session (Claude chat) → Destination: code session and/or repo**

---

## 0. To the receiving agent / session — read this first

This single file contains the **complete state** of the MANDATE game project: the governing prompt, the research record with sources, the reasoning behind every decision *including alternatives that were considered and rejected*, the full canonical design document (Part D, embedded verbatim at the end), the developer's working conventions, and the next milestone.

How to use it:
1. **Best:** commit this as `docs/PROJECT_CONTEXT.md` in the repo and read it in full before any work.
2. Or paste it whole into a session as context.
3. **Part D (the design doc) is canonical.** Sections 1–5 are the *why* behind it. If they ever conflict, Part D wins; flag the conflict to Stan.
4. Honor the conventions in §4 — they are non-negotiable working rules, not suggestions.
5. The next milestone is **v0.2: JSON schemas + Python sim skeleton + first tests** (task list in §5.3).

---

## 1. The Governing Prompt (Stan, verbatim intent — the core of everything)

> A strategy turn-based game, such as Civ or AoE, but also like *Rebel Inc*: you act as a "world police," juggling the international pressure of being a transparent democracy along with your allies, against the real threat of insurgencies — and of them grouping together and creating their own authoritarian placement, **which grows the longer it's left, and connects with others.** A very wide range of possibilities to deal with, balanced for still-fun gameplay. Research reality and history deeply and use it to decide. This is the CORE PROMPT for the game project.

**Stan's three scoping decisions (2026-06-12):**
1. **World framing: real world / alt-history** (chosen knowing the Apple/*Afghanistan '11* removal precedent — see §2.3 and §3.6).
2. **Session shape: both** — Rebel-Inc-length scenarios (45–90 min) first, Civ-style grand mode later.
3. **First move: full design doc first** (delivered as v0.1; embedded as Part D).

---

## 2. Research Record (what was checked, what was found)

### 2.1 Unciv feasibility — checked 2026-06-12
- Unciv mods are **JSON files that alter the data of existing game objects** (nations, units, buildings, techs, uniques). Even total-conversion "base ruleset" mods replace content *inside* vanilla mechanics. There is **no scripting layer** — no hooks for new systems.
- Every system this game needs (legitimacy gauges, network propagation, patron market, elections, fog-of-estimates) is **engine work, not data work** → a pure mod is impossible.
- A Kotlin **fork** could do it, but inherits a hex/tile-empire chassis the design rejects, and Unciv's own docs recommend against mod development from a phone — bad fit for a Termux workflow.
- Sources: `github.com/yairm210/Unciv` → `docs/Modders/Mods.md`; `yairm210.github.io/Unciv/Modders/Mods/`; `yairm210.github.io/Unciv/Modders/Scenarios/`
- **Verdict: build fresh.** (Reasoning in §3.1. One thing kept from Unciv: its GitHub-repo-as-mod distribution idea — our JSON-rules core gives us that for free.)

### 2.2 The live case — the Sahel, 2012–2026 (the premise running in reality, on both sides)
Checked 2026-06-12. Key findings, each one a mechanic:
- Jihadist insurgencies (JNIM/al-Qaeda-linked; IS-Sahel/ISWAP) expanded across Mali, Burkina Faso, Niger from 2012 onward → **coup cascade** followed (Mali 2020/21, Burkina 2022×2, Niger 2023), each junta claiming only it could defeat the insurgency.
- The juntas formed the **Alliance of Sahel States (AES)** (mutual-defense pact Sept 2023), exited ECOWAS, expelled French/Western/UN forces, and brought in **Russian Wagner / Africa Corps** mercenaries → an authoritarian bloc literally manufactured by insurgency pressure, aligned with a rival patron.
- Bloc consolidation is a **clock**: AES joint force grew 5,000 → 15,000 troops; common-currency plans; Mali dissolved all political parties in 2025, Burkina Faso in Jan 2026. Repression erodes citizen trust → which feeds insurgent recruitment. The loop is documented.
- **Despite everything, insurgent territorial control EXPANDED rather than contracted since 2022** (ICG analysis). The authoritarian "solution" does not solve the problem — it scores differently, and worse.
- **Insurgents network too:** April 2026, JNIM and the Tuareg separatist FLA — ideologically unlike groups — ran coordinated offensives in Mali and killed the defense minister. Capability tier-ups, joint operations, pooled pressure.
- **"Quiet ≠ peace":** analysts warned in 2026 that falling attack counts in parts of the Sahel reflected insurgent **entrenchment** into local political/economic systems (shadow taxation, courts), not improved security. This finding alone created the game's Visibility axis and deceptive-calm fog (Part D §5, §9).
- Sources (plain URLs for verification):
  - CFR Global Conflict Tracker — Violent Extremism in the Sahel: `cfr.org/global-conflict-tracker/conflict/violent-extremism-sahel`
  - AES overview & consolidation status: `worldatlas.com/geography/what-is-the-alliance-of-sahel-states.html`
  - Joint force 5k→15k, joint air campaigns: `africanews.com/2026/05/01/alliance-of-sahel-states-confirms-joint-airstrikes-in-mali/`
  - Insurgent alliance vs state alliance analysis (ACLED figures): `authorityngr.com/2026/05/18/between-alliance-of-terror-groups-and-alliance-of-sahel-states/`
  - 2026 Mali offensives record: `en.wikipedia.org/wiki/2026_Mali_offensives`
  - Sahel crisis overview: `defconlevel.com/sahel-security-crisis`

### 2.3 Doctrine, theory & design precedent (stable knowledge — the game's intellectual spine)
- **Galula, *Counterinsurgency Warfare***: COIN is ~80% political, 20% military. The population is the prize.
- **US Army/USMC FM 3-24** (Petraeus-era field manual): legitimacy is the main objective; the paradoxes ("the more force you use, the less effective you may be"; "tactical success guarantees nothing") are this game's action-design law.
- **Kilcullen, *The Accidental Guerrilla***: heavy-handed presence *creates* insurgents; occupation past a welcome threshold generates antibodies → Local-legitimacy decay-by-duration.
- **Merom, *How Democracies Lose Small Wars***: democracies lose COIN **at home**, when domestic tolerance for cost/brutality collapses before the insurgency does. This is the game's central thesis → the Domestic gauge and the Mandate coupling.
- **RAND, *How Insurgencies End* / *Paths to Victory***: insurgencies average ~a decade; **sanctuaries and external sponsors** are the decisive survival variables; leadership decapitation rarely ends anything and can radicalize successors → edges matter more than nodes; decapitation deliberately weak.
- **Train-and-equip blowback is real**: several Sahel coup leaders were Western-trained officers → the coup-seed backfire channel on Train & Equip.
- **Design precedents**: *Rebel Inc.* (single reputation stat, intel fog, civ/mil initiative balance, negotiated endings — our model splits its one reputation into three); **GMT COIN board-game series** (*Fire in the Lake*, *A Distant Plain*) — existence proof that this exact problem space is *fun* turn-based; *Twilight Struggle* (node-scale global influence map, two-bloc tug); *Plague Inc.* (network growth as antagonist pacing); ***Afghanistan '11*** — hearts-and-minds ops layer, and the cautionary tale: **Apple removed it from the App Store for depicting a real conflict** → drives our distribution order (web → Android → Steam/itch → iOS last).

---

## 3. Reasoning & Alternatives Considered (the deliberation record)

This section preserves *why* — including the roads not taken — so future sessions don't re-litigate blind.

### 3.1 Platform: four options weighed
1. **Unciv JSON mod** — rejected: no scripting; every core system is engine work (§2.1).
2. **Unciv Kotlin fork** — rejected: wrong chassis (hex/tile empire vs. our region-node portfolio game); Kotlin/Gradle toolchain hostile to a Termux-first workflow; we'd spend the project fighting inherited mechanics instead of building ours.
3. **Godot-first** — deferred, not rejected: excellent production target (GDScript reads like Python; GitHub Actions can build Android APKs, keeping a phone-based workflow viable), but starting in an engine front-loads presentation before the *fun* of the core loop is proven.
4. **Fresh, two-layer build** — **chosen**: a data-driven core (all rules in JSON) consumed by (a) a headless **Python simulation package** for testing/balance — Stan's exact stack — and (b) thin clients, beginning with a single-file web prototype that runs in a phone browser. The JSON core makes the Phase-2 engine choice (stay web vs. Godot) a *presentation* decision, not a rewrite. This is the architectural law (Part D §13.2).

### 3.2 Map: hexes vs. region nodes
Node graph chosen (~40–50 regions grand / 8–15 per scenario, Twilight-Struggle scale). The game's verbs — legitimacy, influence, interdiction, alliance formation — act on **regions and relations**, not tiles. Edges between nodes are first-class objects (smuggling routes, ethnic ties, sea lanes) because **the networking premise lives in the edges**. This decision also killed the last appeal of an Unciv fork.

### 3.3 The insurgency model: why three axes
- **Strength** alone (most strategy games) can't express the Sahel finding that quiet regions were *more* captured, not less. So: **Strength** (danger now) / **Entrenchment** (survivability; shadow governance) / **Visibility** (what your map shows). High entrenchment + low intel coverage **renders as peace**. The fog system (estimates with confidence bands, post-mortem reveal) exists to weaponize this honestly.
- **Decapitation deliberately weak** with a radicalization succession roll — RAND-true, and it punishes the most "gamey" instinct.
- **Junta as the most common state-collapse outcome** in fragile-but-functional states (the Sahel pattern), and the critical design stance: **a junta is not your ally.** It demands you drop conditionality; its repression feeds the grievance loop. The player's "stabilizing" coup partner is a trap with a clock on it.
- **Bloc formation runs a consolidation clock** (joint forces, currency, treaty depth — AES-modeled): the longer left, the costlier every option. This is the core prompt's "grows the longer it's left, and connects with others," mechanized at the state level; faction edge-formation mechanizes it at the insurgent level.

### 3.4 Economy: why three legitimacies, not one reputation
*Rebel Inc* uses a single reputation stat. Our thesis **requires a triangle** — Domestic / International / Local — because the interesting decisions are the splits: the Transparency Dial (disclose = Domestic hit, International preserved; suppress = leak-clock gamble) is impossible with one number. Ally caveats, "soft on terror" amnesty costs, hypocrisy events — all live in the gaps between the three gauges.
**Mandate (action points) = f(Domestic, election proximity)** is the single most important coupling in the game: it makes domestic politics the engine room and mechanizes Merom directly. Lame-duck turns are thin; honeymoons are fat.

### 3.5 Why Emergency Powers must be genuinely strong
If the authoritarian toolkit is weak, the thesis is a strawman. Each tier grants real, immediate mechanical power — and permanently raises **Authoritarian Drift**, which enters final scoring as a **multiplier** (not a flat penalty) so it scales with success: winning big and ugly still scores poorly. The "Fortress" ending ("you kept the peace and lost the thing it was for") is the game's signature dark ending and must be *reachable by a tempted, competent player*.

### 3.6 Framing decisions within "real world / alt-history"
- **Real, named states; composited insurgent factions** closely modeled on real groups (e.g., *Ansar al-Sahel* ≈ JNIM), openly sourced in briefing text. Rationale: journalistic grounding + design freedom (tune capabilities without misrepresenting real organizations) + lower defamation/platform risk. "Historical names" toggle is OPEN.
- **Grand-mode start: Sept 12, 2001** (PROPOSED) — the franchising/networking phenomenon (AQ affiliates → IS provinces → Sahel consolidation) is the post-2001 story; 1991 "Unipolar Moment" start is a stretch goal, not v1.
- **Lead nations: US + France** (PROPOSED) — deepest stabilization portfolios, most distinct flavors (global reach + war-weariness vs. post-colonial depth + baggage); one shared event deck, different modifiers.
- **Distribution order: web → Android → Steam/itch → iOS last** — the *Afghanistan '11* precedent.
- **Tone**: sober, dossier-driven; civilian harm abstracted into grievance/legitimacy and event text, never gore; the game has a point of view (legitimacy is real; autocracy is scored as loss even when it "works") — deliberately *not* both-sides-ist.

### 3.7 Why scenarios first, and why the Sahel is Scenario 1
Scenarios are the systems-validation ladder; grand mode is **gated on Scenario 1 being fun**, not merely correct. The Sahel is first because **we possess the outcome data**: run the sim with a *passive* player and it should approximately reproduce history — coup cascade, AES formation, insurgent expansion. **Reality is the balance baseline.** If untouched-sim ≠ history, the constants are wrong; if a reasonable player can beat history, the game has hope in it. Scenario 2 is Colombia/Plan Colombia — the qualified COIN success — to prove the design isn't an unwinnable misery sim and to exercise the negotiation endgame. AfPak is Scenario 3, maximum difficulty.

### 3.8 The thesis as a test suite (the idea to protect above all others)
The Phase-1 Monte Carlo balance harness (1,000 headless runs/config) includes **design-thesis regression tests** — the design's claims, asserted in pytest:
- `test_passive_player_reproduces_history` (Sahel calibration)
- `test_pure_kinetic_strategy_loses_integrity_and_local`
- `test_pure_hearts_minds_without_security_loses_to_momentum`
- `test_emergency_powers_tempting_but_scored`
If a balance change breaks the thesis, CI fails. The design document stays true by force.

### 3.9 Naming
**MANDATE** (working title) — triple meaning: electoral mandate / UN mandate / the colonial League-of-Nations mandates the word can't escape, intentionally uncomfortable. Alternates considered and shelved: *Pax*, *The Long War*, *Thin Blue Marble*. Open question #4.

### 3.10 Known risks (full table in Part D §14)
Misery-sim/whack-a-mole feel → scenario scoping, itemized deltas, negotiation comebacks, post-mortem reveals, Colombia winnability proof. Political heat → tone, composites, in-game **Sources screen** (ship the bibliography as a feature: systems journalism). Store policy → distribution order. Scope → the scenario ladder and DECIDED/PROPOSED/OPEN discipline. Solo dev on mobile → everything data-driven, headless-testable in Termux, CI-built clients.

---

## 4. Developer Environment & Working Conventions (non-negotiable)

- **Developer:** Stan. **Environment:** Termux on Android; Python, shell, git, GitHub Actions. Development happens on a phone — headless-testability and CI-built artifacts are requirements, not preferences.
- **Editing rule: cumulative.** Always start from the latest preserved full version and expand; never remove prior content unless explicitly instructed.
- **Versioning:** small incremental releases (v0.x ladder), changelogs, traceability. Every balance change should be a readable diff (hence JSON rules).
- **Progress updates:** concise and high-level; no low-level operational noise.
- **No phantom promises:** never claim background/future work will happen unless an actual automation exists.
- **Shorthand:** `R` = act on the best next step without waiting; `L` = deep self-check (logic, contextual integrity, omissions, alignment) before continuing.
- **CI patterns already in use by Stan** (mirror them): lint + test workflows, artifact outputs (plots, logs, JSON checkpoints) on each run.
- **Proposed repo layout** (instantiate at v0.2):

```
mandate/
├── docs/
│   ├── PROJECT_CONTEXT.md      # this file
│   └── DESIGN.md               # Part D, maintained cumulatively
├── rules/                      # THE source of truth — all JSON
│   ├── schema/                 # JSON Schemas for everything below
│   ├── nodes.json  edges.json  factions.json
│   ├── initiatives.json  events.json  constants.json
│   └── scenarios/sahel_arc/    # Scenario 1 data
├── sim/                        # headless Python package
│   ├── engine.py  world.py  factions.py  legitimacy.py
│   ├── patrons.py  events.py  fog.py  elections.py
│   └── __init__.py
├── tests/                      # pytest, incl. thesis tests (§3.8)
├── harness/                    # Monte Carlo runner + balance plots
├── proto/                      # single-file web prototype (Phase 0)
└── .github/workflows/ci.yml
```

---

## 5. Current State

### 5.1 DECIDED
Real world / alt-history · scenarios first, grand mode later · build fresh (no Unciv) · data-driven JSON core + Python sim + thin clients · region-node map, not hexes · three-legitimacy economy with Mandate coupling · insurgency graph with Strength/Entrenchment/Visibility · bloc consolidation clocks · every initiative has a documented backfire channel · Authoritarian Drift as a scoring multiplier · distribution order web → Android → Steam/itch → iOS last · Scenario 1 = "The Arc" (Sahel 2012–2026).

### 5.2 PROPOSED (Claude's calls, standing unless Stan overturns)
Working title MANDATE · grand start Sept 12, 2001 · lead roster US + France · composited insurgent factions, real states · turn scale: quarter (grand) / month (scenario).

### 5.3 Next milestone — v0.2 task list
1. JSON Schemas for nodes, edges, factions, initiatives, events, constants (`rules/schema/`).
2. Minimal Sahel-lite dataset: 6 nodes, 2 factions, ~8 initiatives, ~6 events.
3. `sim/` skeleton: world state, turn resolution order (Briefing → Policy → Resolution → Consequence), legitimacy deltas itemized in the engine output.
4. First pytest set: schema validation, turn determinism under seeded RNG, and stub versions of the four thesis tests (§3.8) marked `xfail` until systems land.
5. CI workflow: lint + tests + a 10-run mini-harness producing a balance-plot artifact.

### 5.4 OPEN questions awaiting Stan (full text in Part D §16)
(1) election-loss continuity model · (2) historical-names toggle · (3) lead-nation roster size · (4) keep the name MANDATE? · (5) open-source vs closed license — affects v0.2 repo setup · (6) multiplayer ever (lean: no).

---

# PART D — THE DESIGN DOCUMENT (canonical, v0.1, verbatim)

# MANDATE
### Design Document — v0.1
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
| v0.2 | JSON schemas (nodes, factions, initiatives, events) + sim skeleton + first tests |
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

---

## 17. Sources & Grounding (to ship in-game)

**Doctrine & theory:** Galula, *Counterinsurgency Warfare* (the 80% political rule) · US Army/USMC FM 3-24 (the paradoxes) · Kilcullen, *The Accidental Guerrilla* (occupation antibodies) · Merom, *How Democracies Lose Small Wars* (the domestic-tolerance thesis) · RAND, *How Insurgencies End* and *Paths to Victory* (sanctuaries & sponsors decide; decapitation doesn't; ~decade durations).

**The live case:** the Sahel arc 2012–2026 — JNIM/IS-Sahel expansion; the Mali–Burkina–Niger coup cascade; Alliance of Sahel States formation, ECOWAS exit, party dissolutions, Africa Corps arrival; the April 2026 insurgent-alliance offensives; analyst findings that falling incident counts reflected entrenchment, not peace. (CFR Global Conflict Tracker; ACLED; ICG reporting.)

**Design precedents:** *Rebel Inc.* (reputation, intel fog, civ/mil initiative balance, negotiated endings) · GMT's COIN board-game series — *Fire in the Lake*, *A Distant Plain* (proof this problem space is fun turn-based) · *Twilight Struggle* (global influence at node scale) · *Afghanistan '11* (hearts-and-minds ops layer; cautionary platform tale) · *Plague Inc.* (network-growth pacing as antagonist).

---

## Changelog

- **v0.1** — 2026-06-12 — Initial full draft from core prompt + research session (Unciv feasibility check; Sahel 2012–2026 record). Framing locked: real world / alt-history; scenarios-first; design-doc-first per Stan's three scoping answers.

---
*End of handoff. One file, full scope: prompt, research, reasoning, design, conventions, next steps.*

---

# POST-HANDOFF LOG (cumulative additions; never edit above this line)

## 6. Repo instantiation — v0.2 (2026-06-12, code session)

- **Repo:** `stan2032/PaxStressia` — received **empty** (no commits); bootstrapped from this handoff. Note: the repo name is *PaxStressia* while the working title is *MANDATE* (open question #4 alternates included *Pax*). Logged as **new open question #7** in `docs/DESIGN.md` §16 — codename or title decision? Awaiting Stan; all docs keep MANDATE as working title until answered.
- **Canon split:** `docs/DESIGN.md` is now the **live canonical design document**, maintained cumulatively. Part D embedded above is the frozen v0.1 handoff snapshot; if they diverge, the latest `DESIGN.md` wins.
- **Layout instantiated** per §4 at repo root (not nested under `mandate/` — the repo *is* the project root).
- **§5.3 v0.2 milestone executed in full:** six JSON Schemas (`rules/schema/`); Sahel-lite dataset (6 nodes, 8 edges, 2 factions, 9 initiatives across all five families, 6 events, constants); `sim/` package implementing the four-phase turn loop with itemized legitimacy ledger, seeded-RNG determinism, fog estimates with deceptive-calm bias, election/mandate coupling, entrenchment/visibility dynamics, collapse-roll stub (junta path live), bloc/patron/negotiation stubs logged-only; pytest suite (schema validation, determinism, ledger integrity, smoke runs, four thesis tests stubbed `xfail`); Monte Carlo harness (`harness/run.py`, JSON log + balance plot, degrades gracefully without matplotlib); CI (`.github/workflows/ci.yml`: ruff + pytest + 10-run mini-harness with uploaded artifacts).
- **Design growth:** `DESIGN.md` gained **§18 Simulation Specification** (PROPOSED) — the concrete contract between the prose design and the code: determinism law, state vectors, resolution substep order, effect-op vocabulary, v0.2 formulas with constants bound to `rules/constants.json`, ledger format, policy interface, and an explicit list of what is stubbed (no phantom systems).
- **License deliberately absent** (open question #5 gates it). Until answered, default copyright applies.
- **Sim package is stdlib-only by design** — runs in bare Termux Python with zero third-party installs; `jsonschema` is test-only, `matplotlib` harness-only. This is the Termux-first convention, hardened.

## 7. Research deepening & the Exposure directive — v0.2.1 (2026-06-12, same code session)

- **Stan's challenge:** "have you done enough research into game mechanics and balancing…?" Honest answer recorded: domain research (COIN doctrine, Sahel record) was deep; *game-design/balancing* research was precedent-level only, with balance deferred to v0.5 calibration. Gap closed the same day with two dedicated research passes (sub-agent web research; budget-limited, snippet-sourced, gaps flagged in-doc):
  1. **Design craft** → `DESIGN.md` **§19** (binding commitments): Papers-Please fun-gate ("make it fun, then make it mean something"); the anti-whack-a-mole package answering Rebel Inc's *documented* #1 criticism; Sid Meier's interesting-decisions audit; Ruhnke's asymmetry-of-goals + dual-use events; Frostpunk-calibrated Emergency Powers (felt costs, one-way rate-limited tiers, continuous integrity judgment — no arbitrary moral cliffs); procedural-persona balancing with a CI dominance check (v0.5); intrinsic anti-snowball; situational (never arithmetic) difficulty; This-War-of-Mine misery counterweights (named people, pride beats).
  2. **Authoritarian-reality empirics** → `DESIGN.md` **§20**.
- **Stan's second directive (DECIDED, scheduled):** the game must convey the brutal realities citizens of authoritarian states endure, the regimes' international deception, and let the player fund think tanks/academics whose empirical research raises global pressure. Mechanized as **§20: the Closed Society layer** (documented-pattern event cards: party dissolutions, punitive conscription, Moura, the media-ban ladder, transnational repression), **the lying layer** (African-Initiative-grounded hostile fog; the UN referee-killing veto), and **the Exposure system** (per-regime Exposure track; research/exile-media/OSINT/designation instruments; documented exposure→sanctions chains; funder's-paradox and regime-retaliation backfires; credibility bank). Lands v0.7 (mechanics) / v0.8–v0.9 (content), gated on the fun gate. §20.6 carries the unverified-items ledger.
- **Repo setup authorized by Stan** ("setup the repo however you wish"): `main` trunk created at the v0.2 state; development continues on work branches with PRs into `main`. Default-branch flip to `main` requires a one-tap GitHub settings change (Stan). Open question #7's *title* half remains open.
- **Process incident, logged per the cumulative rule:** a §19 edit-anchor mistake briefly dropped DESIGN.md's changelog header and v0.1 entry; restored verbatim in-session and verified against git history (diff shows only additions + three in-place line extensions).

## 8. Title decision — v0.2.2 (2026-06-12, same code session)

- **Stan, near-verbatim:** "I like the name PaxStressia, it encapsulates the 'Pax …ia' eras in history, pax at the cost of stress. and being lied about but not dealing in lies yourself. or, trying your best to."
- **DECIDED: the title is PaxStressia.** Open questions #4 and #7 resolved (answer to #7: the repo name *is* the title). MANDATE retired as working title; it remains throughout the historical sections of this handoff and the early changelog entries as record, per the cumulative rule. The rationale is captured as design material in `DESIGN.md` §1 "The Name" — the name is the thesis compressed, and "trying your best to" is the exact gap the Transparency Dial, Authoritarian Drift, and the Exposure system play in.
- Repo state at this point: `main` is the default branch (Stan flipped it); PR #1 (v0.2.1 docs) merged; CI green on every push so far.

## 9. Phase 0 delivered — v0.3 (2026-06-12, same code session)

- **The greybox prototype is playable** (`proto/index.html`): single-file HTML/JS, phone-browser, dark-dossier greybox of Sahel-lite implementing the §18 loop client-side — fog with confidence bands (§19.5 honored: deceptive calm is experiencable in the greybox), 9 initiatives, player-chosen events, itemized ledger reports, elections, collapse rolls, four endings, localStorage saves, and the believed-vs-true post-mortem chart.
- **Single-source-of-truth held:** served over http the proto fetches `rules/*.json` live; `proto/build.py` embeds a snapshot only as the `file://` fallback, and CI fails if it drifts. The JS engine is a §18-spec port — self-consistently deterministic, not bit-compatible with Python (rules data is the shared truth, not the RNG stream); `proto/smoke.mjs` enforces determinism/ranges/ledger/save-restore headlessly in CI via Node.
- **Deployment guide** at `docs/DEPLOY.md` per Stan's request: Cloudflare Pages from GitHub (repo-root deploy → live rules + per-PR playtest preview URLs), wrangler-from-Termux, GitHub Pages alternatives. Cloudflare setup itself is a dashboard action only Stan can do.
- **The v0.4 gate is now a human question:** Stan playtests; if the 20-minute loop isn't fun, we iterate the proto before building the full arc map.

## 10. Scenario 1 in data — v0.4 (2026-06-12, same code session)

- **"The Arc" delivered as data** (`rules/scenarios/sahel_arc/`): the §12 map at full 12-node resolution (Niamey on-map so Niger's collapse can complete the cascade endogenously; the coastal marker measures southward bleed), the *Azawad National Front* as the third faction, and the historical beat deck — every beat sourced, every beat `once`.
- **The promised v0.4 engine growth landed in both engines**: spread over edges (§18.5), scenario loading (§18.9), beat predicates, events-only `presence`/`patron` ops. The **beats-vs-system law** is now stated in §18.9: beats supply what the system cannot generate (declarations, splits, arrivals); coups remain endogenous collapse rolls — otherwise the §3.7 calibration test would be circular.
- **Thesis suite status: two of four XPASS pre-calibration** (hearts-minds-loses-to-momentum; kinetic-loses-Local). History calibration now runs against the arc and remains the honest xfail — that is v0.5's job, now with the map it needs.
- Proto gained the scenario picker; the arc is playable today.

### Changelog (post-handoff)
- **v0.2** — 2026-06-12 — Repo bootstrapped; §5.3 task list delivered (schemas, Sahel-lite data, sim skeleton, tests, CI); DESIGN.md grown with §18; open question #7 (repo name) raised.
- **v0.2.1** — 2026-06-12 — Two research passes (design craft; authoritarian-reality empirics) → DESIGN.md §19 & §20; Exposure directive recorded as DECIDED; `main` trunk + PR workflow established.
- **v0.2.2** — 2026-06-12 — Title DECIDED: **PaxStressia**; questions #4/#7 resolved; live files renamed; MANDATE kept in historical record.
- **v0.3** — 2026-06-12 — Phase 0 greybox prototype delivered (playable, fog-first, smoke-tested); DEPLOY.md (Cloudflare Pages); playtest gate armed.
- **v0.4** — 2026-06-12 — Scenario 1 "The Arc" in data (12 nodes, 3 factions, beat deck); spread + scenario loading in both engines; beats-vs-system law; two thesis tests XPASS pre-calibration.
- **v0.5** — 2026-06-13 — History calibration: passive player reproduces the arc 10/10 (Mali junta in window, cascade ML→BF→NE, bloc, still growing). New mechanics (absorptive capacity, distance-discounted collapse, governance-resisted spread). Three thesis tests promoted xfail→ENFORCED; MixedPolicy + dominance check shipped as instruments (xfail until v0.7). `harness/calibrate.py` in CI; constants CALIBRATED.
- **v0.5.1** — 2026-06-13 — Open question #5 RESOLVED: **PolyForm Noncommercial 1.0.0** (`LICENSE.md`). GitHub Pages deploy workflow + root redirect → playable at `https://stan2032.github.io/PaxStressia/` after the one-time Pages toggle (fixes the dead-localhost confusion). Stan also delegated milestone choice ("go with what you wish") → v0.6 next.
- **v0.5.2** — 2026-06-13 — Legibility pass from Stan's first playtest (too cramped; jargon; opaque number relations): plain-language relabel (Forces/Dug-in/Activity, Home/Allies/Local, Mandate/Funds), good/bad-coloured meters with uncertainty, a Key glossary tab + first-run orientation, de-cluttered map. Recorded the long-horizon 3D/production-presentation goal and a binding legibility principle in DESIGN §13.3. UI-only.
- **v0.6** — 2026-06-13 — Transparency Dial implemented (disclose vs suppress + leak clocks scaled by press freedom; `suppress_clock` op, leak constants, both engines, determinism-serialized; `tests/test_transparency.py` enforces the thesis economics). Answered Stan's "newer tech?" with DESIGN §13.4 (Godot 4 primary, WebGPU+Babylon.js stay-web fallback; JSON core ⇒ 3D client is a re-skin). Proto: Buried counter + leak headlines.
- **v0.7** — 2026-06-13 — Endgame layer: bloc consolidation clock (§5.4), patron allegiance market (§8), Exposure system first cut (§20 — fund research/exile media/sanctions + `exposure`/`designate` ops + track) and negotiation endgame (§7 `negotiate` op). Both engines, new state serialized, `tests/test_endgame.py` (10), calibration still 10/10. Dominance check stays xfail (systems exist; balance is the v0.8 job). Proto fully ported (exposure/patron readouts, new initiatives, Key section).
- **v0.8** — 2026-06-13 — **The game is winnable; thesis fully enforced.** Tuned player tools + scoring only (calibration-safe by construction → stayed 10/10). Insurgent-grip discount to StabilizationIndex (Pillar 4 in the score), harder junta/bloc weights, affordable+stronger Development, new `CompetentPolicy` (the §3.7 reasonable player). Competent ≈12 > Passive ≈2 > all pure strategies. Promoted to ENFORCED: dominance check (§19.7) and reasonable-player-beats-history (§3.7). Emergency-powers stays xfail (scored-worse holds; not yet *tempting* — needs the full track). Grip ported to proto. 60 pass / 1 xfail.
- **v0.9** — 2026-06-14 — Endings matrix (Pax/Fortress/Retreat/Collapse on abroad×home axes, both engines), post-mortem fog-gap reveal, Sources screen (`rules/sources.json`, confidence-flagged, alt-history labelled). Pre-build audit (removed dead `detect_proto_blocs`; op parity confirmed) + live bibliography verification (Moura; Afghanistan '11 removal = 2018). 68 tests / 1 xfail.
- **v0.9.1** — 2026-06-14 — Playtest fixes from Stan's first deployed session: **fixed the blank map** (a stale cross-version localStorage save crashed `renderMap`; now save-version-gated + defensive rendering + isolated panels) and **reduced wordiness** (per-choice plain effect previews, trimmed event text, "Where: <region>" not "Context: <id>"). Proto/data only; calibration untouched.
