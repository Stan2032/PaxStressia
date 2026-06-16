# PaxStressia
### Design Document — v0.2.2
*A turn-based grand strategy game about being the world police in a world that keeps score. (Title DECIDED at v0.2.2; formerly working title MANDATE, v0.1–v0.2.1 — historical mentions kept as record.)*

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

### The Name (v0.2.2 — **DECIDED** per Stan, 2026-06-12)

**PaxStressia.** Stan's rationale, near-verbatim: it encapsulates the *"Pax …ia"* eras of history — Pax Romana, Pax Britannica, Pax Americana — **pax at the cost of stress**; and *"being lied about but not dealing in lies yourself. or, trying your best to."* The name is the thesis compressed: the peace is real and so is what holding it costs (the Mandate economy, §6); the world lies about you (hostile fog and the propaganda layer, §20.3) while the game scores whether you kept your own hands clean — and *trying your best to* is exactly the gap the Transparency Dial (§6), Authoritarian Drift (§11), and the Exposure system (§20) play in. You can fail at it; the game scores the trying. Supersedes the working title MANDATE (open questions #4 and #7 resolved, §16).

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

**Implemented v0.7** (`sim/blocs.py`). Adjacent non-civilian states form a Bloc (connected components over graph adjacency); each turn its **stage** rises by `bloc_consolidate_rate` (cap `bloc_max_stage`). A bloc drains International by `bloc_pressure × stage` (pooled propaganda) and exports `bloc_expansion_grievance × stage/10` to adjacent civilian regions — the threat that grows the longer it's left. Exposure is the counter (§20): mean member Exposure blunts the propaganda (`exposure_bloc_relief`), and a designation rolls the clock back (`sanctions_bloc_slow`). Scoring's OrderMultiplier now weights blocs by consolidation, not just count (`bloc_containment_term = Σ stage/max_stage`). The passive arc reproduces the AES: a three-state bloc forms and consolidates, and the history calibration still passes 10/10.

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

**Implemented v0.6.** Fingerprint incidents (partner atrocity, errant strike) are now Transparency-Dial events: **disclose** applies a reduced immediate cost; **suppress** (the `suppress_clock` op, §18.4) registers a hidden scandal that carries no cost now but rolls each turn to **leak** — probability `= (leak_base + leak_age_factor × age) × press_freedom`, so a free press (`press_freedom` high for our democracies) is precisely what makes suppression dangerous, mechanizing Merom. A leak costs `leak_multiplier ×` the buried severity, spread across all three gauges (Domestic full, International ×0.7, Local ×0.5); survive `leak_clock_turns` and it's buried for good. Tests (`tests/test_transparency.py`) hold the thesis to account: mean suppression cost exceeds honest disclosure, yet `min == 0` (the gamble is real), and more press freedom ⇒ more leaks. The UI shows a **Buried** counter and headlines the leak when it breaks.

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

**Implemented v0.16.** The escalating ladder, each tier grounded in a real measure and built from existing ops: **I — Surveillance Mandate** (`surveillance_expansion`, PATRIOT §215 / RIPA: intel everywhere); **II — Administrative Detention** (`administrative_detention`, Belmarsh / India's MISA / the French *Micas*: strong attrition + imposed governance *now*, the threat removed without trial); **III — Censorship & Martial Law** (`martial_law`, India 1975 / Turkey's decrees: a large control boost, the unrest blacked out). Each is cheap and front-loaded — *real* raw power, so it is genuinely tempting (a player chasing the current crisis wants it) — and each adds permanent, one-way **Authoritarian Drift** (the ratchet: emergency powers are rarely repealed — France's 2017 SILT law folded the *état d'urgence* into ordinary law). The cost is **mechanical, never a "you crossed the line" scold** (Frostpunk's chief criticism, avoided by design): Drift both crushes the **IntegrityMultiplier** *and*, since v0.16, is a **direct score cost** (`drift_score_cost`) — the democracy is the prize, and every step toward autocracy spends it, blood and backsliding on the same ledger. Test-enforced (the §13.3 thesis suite): `EmergencyPowersPolicy` produces strictly **stronger raw** Stabilization×Order than pure kinetic (tempting) yet a strictly **worse final** score (the game knows) — *win ugly, score poorly*. A modest **accidental-guerrilla backfire** (Kilcullen) remains on each tier, but the decisive cost is the Drift, not luck. Honest scope: the formal **Tier 4 "Emergency Normalized" point-of-no-return** (a distinct locked-in ending) is approximated by the IntegrityMultiplier's floor for now — a future explicit mechanic.

---

## 8. Patrons & the Allegiance Market

Two to three systemic rival patrons (grand mode), modeled on documented playbooks:

- **The mercenary patron** (Russia/Wagner–Africa Corps model): coup-proofing services, no human-rights strings, payment in mining concessions, arrives fast.
- **The investor patron** (China model): infrastructure-for-influence, non-interference doctrine, debt leverage, plays the long game.
- **The proxy patron** (Iran model): arms and ideology through the faction graph itself.

**The market mechanic:** every weak or client state continuously compares offers. Yours comes with conditionality — human-rights strings, transparency requirements, election timelines. The patron's comes with none. Your International legitimacy raises the perceived value of your offer; your scandals raise theirs. Clients **can and will defect mid-game** (the Mali-expels-France beat). When a junta forms (§5.3), the patron's offer usually beats yours by default — unless you drop your conditions, which costs International and Integrity.

**You are competing in a market for allegiance, not just fighting a war.** Half the game's losses should happen at the negotiating table you weren't invited to.

**Implemented v0.7.** `sim/patrons.py:market` replaces the v0.2 flat-drift stub: in every non-civilian state the mercenary patron's influence rises by `patron_drift_junta × (1 − competitiveness)`, where `competitiveness = patron_competitiveness_intl × (International/100) + patron_competitiveness_exposure × (Exposure/100)`, capped at 0.9. A strong, credible offer — high International, and a regime you've *exposed* — slows the capture; a weak one lets the no-strings offer win by default. Test-enforced: weak standing ⇒ faster capture (`tests/test_endgame.py`).

---

## 9. Information & Fog

Every insurgent number the player sees is an **estimate**: `displayed = true × noise(intel coverage)`, with confidence bands rendered honestly in the briefing.

- Low coverage + high Entrenchment = **the map shows peace where there is shadow government.**
- Intel initiatives buy variance reduction, not omniscience.
- **Post-mortem reveal:** at scenario end, the game replays the true history against what you believed at each turn. This is the signature learning loop — and the replayability engine. **Implemented v0.9:** the proto end-screen draws believed-vs-true insurgent strength over the whole run and names the regions where the calm most lied (`Engine.post_mortem()` returns the worst fog gaps — true strength minus last-briefing belief, per region).

---

## 10. Events

Deck-driven, historically sourced, weighted by world state. Every event is a choice with a legitimacy-triangle trade. Representative cards:

leak/whistleblower (suppression clocks come due) · partner-force atrocity (your flag on it) · hostage crisis (rescue/ransom/refuse) · refugee wave (Local → International → Domestic cascade) · base access revoked · election shock at home · patron false-flag · aid-worker kidnapping · client demands you silence criticism · "Mission Accomplished" trap (declare victory now for a Domestic spike; relapse risk doubles) · journalist killed with partner's weapon · your trained battalion announces a "transitional council."

---

## 11. Win, Loss & Scoring

Grand mode runs a fixed horizon (e.g., 100 turns / 25 years) or ends early in collapse. Scenarios use bespoke objectives plus the same integrity accounting.

```
Final Score = StabilizationIndex × OrderMultiplier × IntegrityMultiplier − Costs

StabilizationIndex = Σ (Local legitimacy × Governance × (1 − insurgent grip)) over regions
OrderMultiplier    = f(Bloc containment: count, size, consolidation stage)
IntegrityMultiplier = 1.0 at zero Authoritarian Drift, decaying per tier used
```

**Balanced & made winnable, v0.8.** The scoring was tuned so the design's claims hold as numbers, *without touching the passive world trajectory the §12 calibration measures* — only the player's tools and the score were changed, so calibration stays 10/10 by construction. The decisive addition is the **insurgent-grip discount**: a region's contribution is multiplied by `(1 − max(0.5·strength + 0.5·entrenchment)/100)`, so a region painted with services but run by an entrenched insurgency counts as *unstabilized* — Pillar 4 (quiet ≠ peace) in the score itself. This is what makes pure hearts-minds-without-security lose on the scoreboard, not just on the strength axis. Alongside: OrderMultiplier weights bloc *consolidation* (not count) and bites harder per junta; player programmes were made affordable (lower spend/casualty cost weights, cheaper+stronger Development) so engaged play can pay for itself. Result (mean final, arc): **Competent 12 > Passive 2 > pure strategies (all negative-to-single-digit)** — a reasonable player beats history, and no pure doctrine dominates. Both are now **enforced thesis tests** (§13.3, §19.7).

**Endings matrix** (each a written epilogue, judged by the three axes):

- **Pax** — stabilized abroad, intact at home, allies still answer the phone. The hard ending.
- **Fortress** — you won abroad and hollowed out the republic. *"You kept the peace and lost the thing it was for."* High Stabilization, gutted Integrity. The game's signature dark ending.
- **Retreat** — clean hands, burning world. Integrity pristine, Blocs ascendant.
- **Collapse** — quagmire abroad, exhaustion at home, the Bloc sets the terms now.

Losing an election ≠ game over (**OPEN** continuity model, §16). Becoming an autocracy to win *is* mechanically possible — and the epilogue will say so plainly.

**Implemented v0.9.** `Engine.ending()` (mirrored in the proto) resolves the four endings on two axes with data-driven thresholds: **ABROAD** = StabilizationIndex × OrderMultiplier ≥ `pax_abroad_min` (so juntas and consolidating blocs count against you), and **HOME** = IntegrityMultiplier ≥ `integrity_clean_min`. Pax = abroad ∧ home; Fortress = abroad ∧ ¬home (the signature dark ending — won, but the integrity multiplier records what it cost); Retreat = ¬abroad ∧ home; Collapse = neither. Test-enforced: a passive player never earns Pax; a competent player reaches a held-line ending on some seeds (endings are reachable, not decorative); drift forces Fortress rather than Pax.

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
  *(As of v0.16 **all four are enforced**, not xfail — the design document is true by force.)*
  GitHub Actions CI mirrors the existing pipeline patterns (lint, tests, artifact outputs: balance plots, run logs, JSON checkpoints). This phase is deliberately in familiar territory: the sim *is* a decay/accretion network with thresholds — the same machinery family as prior network projects, pointed at geopolitics.
- **Phase 2 — Production client:** re-evaluated after Phase 1 with real data. Candidates: stay web (PWA; itch.io; Steam via wrapper) vs **Godot 4** (GDScript reads like Python; GitHub Actions can build Android APKs, keeping the phone-based workflow viable). The JSON core makes this a presentation decision, not a rewrite.

**Production presentation — long-term direction (DECIDED-as-aspiration per Stan, 2026-06-13):** the eventual client should *look and feel like a real game* — a tactile, possibly 3D, situation-room presentation (a lit war table / globe, physical dossiers, readable motion), not a spreadsheet with a map. This is explicitly a **long-horizon goal**, gated behind the systems being fun and true first (§13.3 phase order stands); it is recorded now so the JSON-core/thin-client split keeps it cheap to reach. **Godot 4 is the leading candidate** precisely because it makes a 3D/animated table feasible while still consuming the same `rules/*.json`. The greybox (`proto/`) is a *legibility and balance* instrument, never the shipping look.

**Legibility principle (DECIDED per Stan's v0.5 playtest, 2026-06-13):** the game must be *readable by a newcomer without a manual*. Concretely, binding from now on: (a) lead with plain language, keep the doctrinal term as the gloss — *Forces / Dug-in / Activity* in front, *(Strength / Entrenchment / Visibility)* behind; (b) every number shows its **direction** (is high good or bad for the player) and, when it's an estimate, its **uncertainty**; (c) the causal links between numbers are stated in-product, not left implicit; (d) a one-tap plain-language **Key** is always reachable, and a first-run orientation shows once. Jargon with no in-product explanation is treated as a bug. (First pass shipped v0.5.2.) **Extended v0.17 (per Stan): show, don't tell.** (e) the *screen itself* carries the state — you should infer what's happening from the map by colour, shape, and motion before reading a word (insurgent strength is a red ring whose thickness *is* the strength; who-rules is the node's colour; your Regional Command is a planted flag; a petro-state is an oil drop; a dense 40-nation board drops labels and you *tap* a nation to learn it — interactive, not a wall of text); (f) every abstract "idea" is rendered as a **concrete object** — Mandate 🏛️, Funds 💰, Home 🏠, Allies 🤝, Local 🛡️, Drift ⛓️ — not a word. The greybox uses emoji/SVG glyphs as stand-ins for the production art (§13.4); the principle, not the asset, is what's binding. A headless board renderer (`proto/preview.mjs` → SVG/PNG via cairosvg) lets the visual language be reviewed without a browser.

### 13.4 Presentation technology — the "can we use newer tech?" evaluation (2026-06-13)

Stan asked whether we can build this on something more modern than HTML — OpenGL or other cutting-edge tech. Yes, and the architecture was designed for exactly that: the **JSON-rules core + headless sim is the asset; the renderer is swappable** (§13.2). The brain is never rewritten; only the face changes. So this is a free, deferred choice — which is the whole payoff of the early data-driven decision. The discipline is *not* to chase novelty before the systems are fun and true (the §13.3 phase order stands, and the greybox is a legibility/balance instrument, never the ship look). Options weighed:

- **Godot 4 — PRIMARY recommendation for the production client.** Modern GPU rendering (Vulkan, with an OpenGL3 fallback) — so it *is* "OpenGL/Vulkan", just not hand-written; real 3D for a lit war-table / globe; one project exports to **web (WASM), Android APK, Windows/Mac/Linux, and Steam**, matching our distribution order (§2); GDScript reads like Python (low friction from our Python sim); GitHub Actions can build every target headlessly, preserving the phone-first workflow. Best capability-per-effort for a solo dev, and already the doc's standing candidate.
- **WebGPU + Three.js / Babylon.js — the stay-on-the-web alternative, and the genuinely "cutting edge" web answer.** WebGPU is the modern successor to WebGL (built on Vulkan/Metal/D3D12); Three.js and Babylon.js both target it today and give real 3D (a 3D globe, depth, shaders, post-processing) **while reusing the JavaScript engine we already wrote for the prototype** — no rewrite of the client logic, only the view. Strong if we want one language end-to-end and instant browser reach. Trade-off: WebGPU support is still maturing on some mobile browsers (WebGL2 is the safe fallback), and packaging for Steam/stores means a wrapper.
- **Raw OpenGL / Vulkan / wgpu by hand — assessed and rejected for now.** Writing the renderer ourselves is building an engine: enormous effort, little gain for a turn-based dossier-and-map game, and hostile to a solo/Termux workflow. "Cutting edge for its own sake" is the trap here.
- **Bevy (Rust, wgpu/WebGPU) — assessed, deferred.** Genuinely modern (ECS, WebGPU), compiles to web + native, but Rust is a steep tax and would orphan the Python sim. Reconsider only if performance or a native-engine need ever demands it.
- **Unity / Unreal — rejected.** AAA 3D but the wrong scale: heavyweight, licensing strings, not phone-buildable, and Unreal especially is enormous overkill for this design. Unity is *possible* but Godot wins on openness, footprint, and our workflow.

**Decision (PROPOSED):** keep proving the loop in the cheap greybox through the systems milestones (v0.6–v0.9); when systems are content-complete and fun (around the §15 v0.8 playtest gate), build the production client in **Godot 4** as Phase 2, with **WebGPU+Babylon.js** held as the fallback if we choose to stay web-native. Either way the `rules/*.json` and the design's numbers are reused wholesale — the move is a re-skin, not a rebuild. A small, *verifiable* 3D proof-of-concept can be spiked earlier on request; it was deliberately not built blind now, since a renderer can't be validated headlessly in this environment and shipping an unverified client would violate the project's no-phantom-work rule.

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
| **v0.3** | Web prototype: core loop playable (Sahel-lite, 6 nodes) |
| **v0.4** | Full Scenario 1 map + event deck in data |
| **v0.5** | Balance harness + history-calibration passing |
| **v0.6** | Fog/intel + transparency dial + elections |
| **v0.7** | Patrons + bloc formation + negotiation endgame |
| **v0.8** | Scenario 1 content-complete; playtest round |
| **v0.9** | Post-mortem reveal, endings, sources screen |
| **v1.0** | Scenario 1 ("The Arc") ships |
| v1.x | Colombia, AfPak scenarios |
| v2.0 | Grand mode *(pulled forward per Stan, 2026-06-14; foundation shipped v0.10 — §21)* |

*Roadmap annotations (v0.2.1, cumulative):* v0.3 must include fog rendering in the greybox (§19.5); v0.5 adds the MixedPolicy dominance check to CI (§19.7); v0.7 additionally carries the Exposure-system mechanics and hostile-fog propaganda term (§20.3–20.4); v0.8–v0.9 carry the closed-society content pass and its verification ledger (§20.2, §20.6).

---

## 16. Open Questions (for Stan)

1. **Election-loss continuity:** when you lose an election — do you (a) keep playing as the state with a changed mandate profile (continuity-of-government model), (b) score out and end the run, or (c) optionally switch seats to the new administration with shifted modifiers? *(My lean: (a) for scenarios, (c) as a grand-mode option.)*
2. **Historical-names toggle:** ship real insurgent-group names behind an optional toggle, or composites only? *(My lean: composites only at v1.0; revisit.)*
3. **Lead-nation roster at v1.0:** US-only, or US + France? *(France is the natural Scenario 1 seat; my lean: both, one event deck.)*
4. **Working title:** **MANDATE** — chosen for the triple meaning (electoral mandate / UN mandate / the colonial League-of-Nations mandates the word can't escape — intentionally uncomfortable). Alternates considered: *Pax*, *The Long War*, *Thin Blue Marble*. Keep MANDATE? *(RESOLVED 2026-06-12, v0.2.2: the title is **PaxStressia** — see §1 "The Name". MANDATE retired.)*
5. **License/openness:** open-source like Unciv (community + mods + your public-repo workflow) vs. closed (commercial option preserved)? Affects repo setup at v0.2. *(RESOLVED 2026-06-13, v0.5.1: **PolyForm Noncommercial 1.0.0** — source-available for any noncommercial use (community, modding, learning, journalism), commercial rights reserved (preserves the Steam/itch path), and reversible toward more-open later. The "forecloses nothing" choice. See `LICENSE.md`.)*
6. **Multiplayer:** ever? *(My lean: no — the design is a solitaire system game like Rebel Inc; a "shared world, compared scores" async mode is the only plausible shape, post-v2.)*
7. **Repo name vs. working title** *(added v0.2)*: the GitHub repo is **PaxStressia**; the docs' working title is **MANDATE** (and *Pax* was a shelved alternate, §16.4). Is *PaxStressia* (a) just a repo codename, (b) the new title, or (c) a placeholder until #4 is answered? Docs keep MANDATE until you call it. *(My lean: treat as codename; decide title at v0.8 when store pages exist.)* *(v0.2.1 note: Stan authorized "set up the repo however you wish" — `main` trunk + PR workflow created; the title half of this question remains open.)* *(RESOLVED 2026-06-12, v0.2.2: answer is (b) — the repo name **is** the title. See §1 "The Name".)*

---

## 17. Sources & Grounding (to ship in-game)

**Shipped v0.9 as `rules/sources.json` → the in-game Sources screen** (a section of the Key tab in the proto). The bibliography is now data, schema-validated, with an **honest confidence flag on every entry** — `verified` (live-checked this build), `established` (canonical scholarship/record), or `alt_history` (the game's projection beyond the reliable record, explicitly *not* presented as fact). The screen leads with a disclaimer: composited factions are not the real groups; the post-2023 Sahel trajectory is extrapolation. Integrity rule, test-enforced: nothing ships as fact that isn't real, and the near-future material is labelled, not hidden. Two specific shippable claims were live-verified this build — the Moura massacre figures (UN, May 2023) and the *Afghanistan '11* App Store removal (2018) — and carry URLs. The prose lists below remain the human-readable source of that data.

**Doctrine & theory:** Galula, *Counterinsurgency Warfare* (the 80% political rule) · US Army/USMC FM 3-24 (the paradoxes) · Kilcullen, *The Accidental Guerrilla* (occupation antibodies) · Merom, *How Democracies Lose Small Wars* (the domestic-tolerance thesis) · RAND, *How Insurgencies End* and *Paths to Victory* (sanctuaries & sponsors decide; decapitation doesn't; ~decade durations).

**The live case:** the Sahel arc 2012–2026 — JNIM/IS-Sahel expansion; the Mali–Burkina–Niger coup cascade; Alliance of Sahel States formation, ECOWAS exit, party dissolutions, Africa Corps arrival; the April 2026 insurgent-alliance offensives; analyst findings that falling incident counts reflected entrenchment, not peace. (CFR Global Conflict Tracker; ACLED; ICG reporting.)

**Design precedents:** *Rebel Inc.* (reputation, intel fog, civ/mil initiative balance, negotiated endings) · GMT's COIN board-game series — *Fire in the Lake*, *A Distant Plain* (proof this problem space is fun turn-based) · *Twilight Struggle* (global influence at node scale) · *Afghanistan '11* (hearts-and-minds ops layer; cautionary platform tale) · *Plague Inc.* (network-growth pacing as antagonist).

**Design craft (added v0.2.1, feeding §19):** Vaughan/Ndemic on Rebel Inc's research grounding and balance (`paxsims.wordpress.com/2019/04/30/an-interview-with-rebel-inc-designer-james-vaughn-ndemic-creations/`) · player-reception record on its whack-a-mole failure mode (Steam/Metacritic, §19.2) · Ruhnke on the COIN system's asymmetry of goals (`theplayersaid.com/2016/08/22/interview-with-coin-series-creator-designer-volko-ruhnke-part-i/`) · 11 bit on Frostpunk's Book of Laws (`pcgamer.com/frostpunk-developers-on-hope-misery-and-the-ultimately-terrifying-book-of-laws/`) · *This War of Mine* GDC 2015 (`gdcvault.com/play/1022335/This-War-of-Mine-Raising`) · Lucas Pope on *Papers, Please* (`gamedeveloper.com/design/road-to-the-igf-lucas-pope-s-i-papers-please-i-`) · Sid Meier, GDC 2012 (`gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions`) · anti-snowball design (`waywardstrategy.com/2020/07/06/anti-snowball-design/`) · automated balancing literature (`arxiv.org/pdf/1908.01423`, `arxiv.org/html/2503.18748v1`) · difficulty-mode design (`gamedeveloper.com/design/difficulty-is-difficult-designing-for-hard-modes-in-games`).

**The closed society & exposure (added v0.2.1, feeding §20):** UN OHCHR on Moura and on Mali's party dissolution · HRW on Burkina Faso's punitive conscription, abductions, and civic-space closure, and on the 2026 US sanctions reversal · Freedom House, *Transnational Repression* · EU EUvsDisinfo/EEAS on "African Initiative" (FIMI) · Forbidden Stories on Russia's Sahel information offensive and the Pegasus Project · Amnesty Security Lab (Pegasus forensics) · Global Witness / Human Rights First on the Magnitsky designation pipeline · US Treasury OFAC (Wagner-Mali designations, 2023) · OCCRP funding-and-independence FAQ · Al Jazeera (UN Mali panel veto; Ngefa expulsion) · VOA/Euronews (the media-ban ladder). Full URLs inline in §20; the in-game Sources screen ships them.

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
   c2. *(v0.4)* spread over edges (18.5) — momentum replicates into adjacent grievance,
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
| `presence {faction, strength, entrenchment}` *(v0.4, events only)* | node | seeds or boosts a faction's presence — the franchise-arrives beat; deliberately unavailable to initiatives |
| `patron {patron, delta}` *(v0.4, events only)* | node | shifts patron influence — the mercenary-arrival beat |
| `suppress_clock {severity}` *(v0.6, events only)* | global/node | the Transparency Dial's suppress branch (§6): no cost now; registers a leak clock resolved in the consequence phase |
| `exposure {delta}` *(v0.7)* | node→country / global→all regimes | raise a regime's Exposure track (§20) |
| `designate` *(v0.7)* | node→country | spend Exposure on a targeted sanction; thin case below `sanctions_exposure_min` |
| `negotiate` *(v0.7)* | node | settle the strongest *stalemated* faction (§7 endgame) |

**Backfire block** (required on every initiative — schema-enforced; Pillar 3 as a validation rule): `{channel, probability, effects[], note}` rolled at substep 3b. A deferred-clock form (`{clock: turns}`) is reserved for the Transparency Dial at v0.6. Reserved ops (documented now, implemented per roadmap): `interdict_edge, decapitate, surge, contractors, sanction, summit, negotiate, messaging, war_powers, veterans` — and, for the §20 Exposure system (v0.7+): `fund_research, support_exile_media, osint_unit, designate_sanctions, propaganda_pressure`.

### 18.5 v0.2 formulas (constants in **bold** are keys in `rules/constants.json`)
Per (faction *f*, node *n*) each turn, with all gauges 0–100 and clamped:

- `Recruitment = `**k_recruit**` × (grievance/100) × (1 − governance/100) × junta_amp` where `junta_amp = 1 + `**junta_recruit_amp** if the node's government is a junta (repression feeds the loop, §5.3) else 1.
- `ExternalSupport = `**sponsor_flow**` × route_factor × (1 + `**k_pool**` × n_links)` where `route_factor` = mean over *n*'s edges of `capacity × (1 − interdiction)` — sanctuary/sponsor flow rides the edges (Pillar 2), and links pool it (§5.2).
- `AllianceBonus = `**k_alliance**` × n_links` (faction-level link count).
- `Attrition = (ops_pressure + partner_capacity × `**k_partner**`) × `**k_attrit**` × (strength/100)`.
- `Defection = amnesty_rate × strength` (while an amnesty op is active).
- **Absorptive capacity (v0.5):** every *positive* growth term (Recruitment, ExternalSupport, AllianceBonus) is scaled by `headroom = 1 − strength/100` — recruitment pools deplete and strength approaches saturation asymptotically rather than blowing through the clamp. This is what makes the calibrated curves S-shaped (fast in contested mid-strength regions, slow near saturation) instead of linear-then-pinned.
- `ΔStrength = (Recruitment + ExternalSupport + AllianceBonus) × headroom − Attrition − Defection` — **each term logged separately** in the TurnReport so balance work reads causes, not net effects.
- **Spread (v0.4, governance-resisted v0.5):** where `strength > `**spread_threshold**, each open edge carries `flow = `**k_spread**` × strength × capacity × (1 − interdiction) × (grievance_neighbor/100) × (1 − governance_neighbor/100)²` into the neighbor (also headroom-scaled) — seeding presence where none existed. Spread is *replication, not movement*: momentum recruits locally and the source keeps its strength. The quadratic governance term means governed cores suffer raids, not occupation — **no Sahel capital was ever actually held**, and the model must not let one be. The arc's historical test: northern Burkina ignites from Mopti around the 2015–16 window without being scripted (it does, 10/10 seeds).
- **Entrenchment:** if `strength ≥ `**entrench_strength_min** and `ops_pressure < `**entrench_pressure_max**, the node is *uncontested* for *f*: `entrenchment += `**k_entrench**` × strength/100`. Entrenchment decays only through Local legitimacy: `−`**k_entrench_decay**` × local_legitimacy/100` per turn. (Strength is the danger now; entrenchment is the survivability — §5.1.)
- **Visibility** relaxes toward `target = `**vis_floor**` + `**vis_contest**` × min(1, ops_pressure/`**pressure_ref**`) × 100 − `**vis_quiet**` × entrenchment` at rate **vis_smooth** per turn. Contested = loud; entrenched = quiet (Pillar 4).
- **Networking (§5.2):** for factions *f, g* sharing or adjacent to common nodes, a link forms when `affinity_eff × mutual_need × route_access ≥ `**link_threshold**, where `affinity_eff = max(affinity, `**affinity_floor**`)` — the floor keeps ideologically *unlike* alliances possible (the JNIM+FLA surprise), `mutual_need` rises with both factions' recent attrition, and `route_access` is the best shared-route factor.
- **Collapse roll (§5.3),** capital node of country *c*: `threat = max over c's nodes of strength × (0.5 + entrenchment/200) × dist_factor`, where `dist_factor = 1/(1 + `**collapse_dist_decay**` × hops_from_capital)` (v0.5 — the far north menaced Bamako far less than central Mali did; it was the *center's* deterioration that toppled the capital, and the distance discount encodes that the eight-year northern stalemate didn't itself end the state). When `threat / governance_capital ≥ `**collapse_ratio**, roll outcome weights `{junta: `**w_junta**` + coup_risk, failed: `**w_failed**`, emirate: `**w_emirate**` × (capital entrenchment share)}`. Junta: governance −**junta_gov_hit**, grievance +**junta_grievance_hit** country-wide, mercenary patron influence +**junta_patron_gain**, government = junta. One collapse per country at v0.2 (re-collapse chains land with blocs, v0.7).
- **Fog estimate (§9):** `σ = `**fog_sigma_max**` × (1 − coverage)`; `bias = −`**fog_calm_bias**` × (entrenchment/100) × (1 − coverage)`; `displayed = max(0, true × (1 + bias + ε))`, `ε ~ N(0, σ)`; the briefing renders `displayed ± 1.64σ·true` as a 90% band. The bias term **is** deceptive calm: entrenched and unwatched reads *low*, honestly delivered as a confident-looking wrong number. Entrenchment estimates use `σ × `**fog_entrench_mult** (the truth HUMINT exists to buy).
- **Mandate income (§6):** `mandate = max(1, round(`**mandate_base**` × (0.5 + domestic/100) × phase))` with `phase` = **honeymoon_mult** for **honeymoon_turns** after a won election, **lameduck_mult** in the last **lameduck_turns** before an election while `domestic < 50`, else 1.0.
- **Election** every **election_period_turns** (60 at month scale — France-analog seat): `P(win) = 1/(1+e^{−(domestic−50)/`**election_k**`})`. Win → honeymoon. Loss → v0.2 implements continuity model (a): play continues, `domestic → 50 + (domestic−50)×`**continuity_reversion**, and a thin-mandate spell follows. (Open question #1 still stands; this is the scenario-mode placeholder.)
- **Scoring (§11):** `Stabilization = 100 × Σ(local/100 × governance/100)/n_nodes`; `OrderMult = 1/(1 + `**order_junta_weight**` × juntas + `**order_bloc_weight**` × blocs)` (blocs are detection-only at v0.2); `IntegrityMult = max(`**integrity_floor**`, 1 − `**drift_per_tier**` × drift)`; `Costs = casualties × `**cost_per_casualty**` + spent × `**cost_spend_norm**`. `Final = Stabilization × OrderMult × IntegrityMult − Costs`.

### 18.6 The itemized ledger (feedback clarity, mechanized)
Every change to any gauge goes through one function and produces a `LedgerEntry{turn, gauge, source, delta}` where `gauge ∈ {domestic, international, local:<node_id>}` and `source` is the initiative/event/system id that caused it. The engine **guarantees** (test-enforced) that each gauge's change in a turn equals the sum of its entries. The TurnReport carries the entries verbatim — this is the §3 Consequence-phase contract, the balance-tuning instrument, and the data spine of the v0.9 post-mortem reveal.

### 18.7 Policy interface (the harness's hands)
`Policy.choose(briefing, actions) → [orders]` and `Policy.choose_event(event) → choice_index`. Built-ins, named for the thesis tests they serve (§13.3): `PassivePolicy` (does nothing — the history-calibration baseline), `PureKineticPolicy` (military family only), `PureHeartsMindsPolicy` (governance/development only), `EmergencyPowersPolicy` (kinetic + every drift tier available), `MixedPolicy` (a crude doctrine portfolio), `RandomPolicy` (seeded chaos for fuzzing), and — added v0.8 — **`CompetentPolicy`**, the *§3.7 reasonable player*: triage the civilian capital nearest collapse with development, settle stalemated factions by negotiation, see-and-suppress the worst contested regions, keep an umbrella up, expose consolidating blocs — and avoid the casualty/drift-heavy tools (competence is restraint). It is the balanced baseline the dominance check (§19.7) holds pure strategies against, and the benchmark for "a reasonable player can beat history."

### 18.9 Scenario loading & historical beats (v0.4 — PROPOSED)
A scenario is a directory `rules/scenarios/<id>/` containing `scenario.json` (meta: name, description, seat, sources) plus any of the rules files: `nodes/edges/factions/events.json` **replace** the top-level file wholesale (a deck is a curated whole); `constants.json` **merges** partially (a scenario tunes, it doesn't refound). Absent files fall through to `rules/`. Both the Python sim (`load_rules(scenario=…)`) and the proto implement the same semantics. **Historical beats** are event cards with `once: true` and window/state predicates (`min_turn/max_turn`, `country_collapsed`, `country_not_collapsed`, `min_collapsed`, `min_links`). The dividing line, stated as law: **beats supply the political texture the system cannot generate; they never script what the system must produce endogenously** — Azawad's declaration and the franchise split are beats; the coups are collapse rolls, or the §12 calibration means nothing.

### 18.8 Deliberately stubbed at v0.2 (so no one mistakes scaffolding for systems)
Faction links form and pool support, but **joint offensives** don't fire yet *(v0.4 note: the `insurgent_concord` beat fires a scripted one when a link exists; systemic joint offensives still land v0.7)* · presence does not yet **spread to new nodes** over edges (growth is per-seeded-node; spread lands with the full arc map, v0.4) *(DELIVERED at v0.4 — see 18.5)* · proto-blocs (adjacent juntas) are **detected and logged**, but the consolidation clock doesn't run · the patron exists as **influence drift only** — the allegiance market (§8) lands v0.7 · the Transparency Dial and suppression clocks are schema-ready but inert until v0.6 · negotiation endgame v0.7 · war exhaustion, occupation-duration antibodies, ally caveats, decapitation/succession, capability tier-ups, surge/withdrawal cliff, contractors, sanctions, summits — all reserved, per the §15 roadmap. The four thesis tests exist as `xfail` stubs so the suite *names* the destination before the road is built.

---

## 19. Playability, Pacing & Balance (v0.2.1 — PROPOSED; research-backed design commitments)

*Added after a dedicated game-design/balancing research pass (2026-06-12) into the precedent games and balance methodology. Each lesson below is a documented finding → a commitment binding future versions. Sources inline and in §17. Honesty note: most findings rest on interviews, postmortems, and player-reception records retrieved at snippet level; items marked [unverified] are background knowledge pending primary-source confirmation. Highest-value unread primaries for a follow-up pass: the PAXsims Vaughan interview and the Ruhnke podcast notes (`conflictsimulations.com/2018/03/28/harold-on-games-podcast-1-with-volko-ruhnke-notes/`).*

### 19.1 The fun gate, hardened (Papers, Please)
Lucas Pope's method was "make it fun, then make it mean something": the inspection loop was compelling *before* the empathy layer landed — and the bureaucratic procedure itself induces the dehumanized mindset the game critiques (`gamedeveloper.com/design/road-to-the-igf-lucas-pope-s-i-papers-please-i-`). **Commitments:** (a) the v0.3 greybox prototype validates the bare loop with placeholder text — if pushing numbers around the Sahel-lite map isn't engaging for 20 minutes, no amount of meaning rescues it; (b) where possible, the game's point of view should emerge from *procedures the player executes* (the Transparency Dial, the drift tiers, triage under thin Mandate) rather than from editorializing text.

### 19.2 The anti-whack-a-mole package (Rebel Inc's documented failure mode)
Rebel Inc's most-repeated criticism is literally our named risk: "glorified whack-a-mole simulator," insurgents who "pop out of nowhere," one dominant (military) style, and warning-spam fatigue ("Done with this game. Tired of seeing 'Lack of stability critically affecting your reputation'") — while its praised core is "directing, rather than commanding" (`steamcommunity.com/app/1088790/discussions/`, `metacritic.com/game/rebel-inc-escalation/user-reviews/`). **Commitments:**
1. **Legibility law:** every insurgent resurgence must be *explicable in hindsight* — the per-term growth ledger (§18.5) and post-mortem reveal must let the player reconstruct exactly which grievance, route, or link fed it. Nothing pops out of nowhere; it pops out of somewhere you could have watched.
2. **Doctrine plurality:** multiple viable strategy mixes is a balance *target*, not a hope — enforced by the §19.7 harness check.
3. **Alert rationing:** the briefing carries a severity budget; recurring conditions escalate in form (footnote → item → lead story) instead of repeating verbatim. UI law from v0.3 on.
4. Stay at the "directing" altitude: no encirclement micro, no unit pushing — the player sets posture and policy, the theater answers.

### 19.3 The interesting-decisions audit (Sid Meier)
A decision is uninteresting if one option always wins or the choice is effectively random; good ones trade short-term vs long-term and let players "envision the future." Players also credit themselves for wins and blame the game for losses — so show cause chains generously (`gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions`). **Commitments:** every initiative menu, event card, and Emergency Powers tier passes the audit (no dominant option, no coin-flip, a visible short/long tension) — reviewed at each content version; the itemized ledger and post-mortem exist precisely to make losses *attributable* ("you lost because X fed Y" is the game teaching, not the game cheating).

### 19.4 Forced portfolio balance is the genre's proven core (Rebel Inc)
Vaughan's loop punishes purity in both directions: pure military breeds popular resistance, pure civilian lets rebels undo progress (`en.wikipedia.org/wiki/Rebel_Inc._(video_game)`). Both failure modes must be *equally vivid*. This is already encoded as thesis tests #2 and #3 (§13.3) — the lesson confirms the suite and raises the bar: the failures must not merely occur, they must be **felt and legible** when they do. Vaughan's research-grounded method (SIGAR reports, expert interviews, the Colombia/FARC process; World Bank praise, a peace-conference invitation — `paxsims.wordpress.com/2019/04/30/an-interview-with-rebel-inc-designer-james-vaughn-ndemic-creations/`) is also the external validation of our §12 calibration plan: history-grounding is a proven playbook, and the credibility doubles as identity.

### 19.5 Asymmetry of goals, not stats (GMT COIN / Ruhnke)
The COIN system's appeal is faction-specific action menus and victory logic — "asymmetry of goals and options," population control as legitimacy, and **dual-use event cards where every card helps someone** (`en.wikipedia.org/wiki/COIN_(board_game)`, `theplayersaid.com/2016/08/22/interview-with-coin-series-creator-designer-volko-ruhnke-part-i/`). **Commitments:** (a) the two composite factions diverge in *behavioral logic*, not stat lines — entrenchment-first vs strength-first is already seeded in the data; their AI doctrines (v0.4+) must keep that contrast visible; (b) event cards should tempt: choices that are good for you *and* feed something else (§10 cards get an adversarial-benefit review at v0.4). Ruhnke also called hidden information a years-long "conundrum" even for him — confirmation that deceptive-calm fog is a first-class design risk: **the v0.3 prototype must include the fog rendering**, not defer it, because the loop's fun partly *is* the fog.

### 19.6 Calibrating the temptation (Frostpunk's Book of Laws)
11 bit tuned dilemmas to be "not too subtle to notice or too exaggerated to become comical" — the Book of Laws works as a *self-test* the player runs on their own stated morals (`pcgamer.com/frostpunk-developers-on-hope-misery-and-the-ultimately-terrifying-book-of-laws/`). The ending judgment ("the city survived, but was it worth it?") provoked exactly the lasting reflection we want — **but players revolted where the moral line felt arbitrary** (one step past prisons = "you went too far"). [unverified: laws being irreversible and cooldown-gated, benefit-now/cost-later asymmetry — background knowledge.] **Commitments for the Emergency Powers track (§7):**
1. Each tier's cost is *felt and visible* at signing — never subtle, never lurid.
2. Benefit lands immediately and concretely; the corrosion is deferred and social (drift already works this way — keep it).
3. Tiers are **one-way and rate-limited** (a cooldown between tiers; no same-turn cascade to autocracy) — the "crossing the line" moment is a deliberate ritual, not a shopping spree.
4. Integrity is judged **continuously and transparently** (the multiplier, visible all game; epilogue text scales in gradations) — no single binary "you went too far" cliff.

### 19.7 Balance methodology: personas, fitness targets, dominance checks
Automated balancing is established practice — MCTS "procedural personas" simulating player archetypes, iterative tuning for asymmetric games, self-play optimization (`arxiv.org/pdf/1908.01423`, `arxiv.org/html/2503.18748v1`). Our policy archetypes (§18.7) *are* procedural personas, and the §12 passive-replay calibration is a **fitness target**: distance between the do-nothing run and the historical trajectory is the loss function for constants tuning. **The dominance check:** the harness gains a `MixedPolicy` (doctrine portfolio) and CI compares archetype mean scores across the seed battery; if any *pure* archetype matches or beats the mixed baseline, that is a balance regression. Pillar 3 becomes a number. *(Status history: the `MixedPolicy` instrument shipped v0.5; the systems a balanced path needs landed v0.7; **enforced at v0.8** once the scoring's insurgent-grip discount and affordable player tools opened a real win path. The hard gate now reads against `CompetentPolicy` (§18.7): it must outscore every pure archetype, and beat passive by a clear margin — `test_no_pure_strategy_dominates_the_balanced_baseline` and `test_a_reasonable_player_can_beat_history`. Crucially this was achieved by tuning **player tools + scoring only**, never the passive world dynamics, so the history calibration stayed 10/10 throughout — the discipline the suite exists to enforce, honoured rather than gamed.)*

### 19.8 Anti-snowball: intrinsic, never rubber-banded
Engineered pity bonuses are resented; durable anti-snowball comes from diminishing returns, nonlinear costs, and attention limits (`waywardstrategy.com/2020/07/06/anti-snowball-design/`). Insurgency natively anti-snowballs (holding territory costs the holder; entrenchment decays under Local legitimacy; Mandate caps player tempo). **Commitment:** no hidden catch-up modifiers in either direction — the comeback arcs are *systemic* (negotiation unlocks at stalemate, §7) and the difficulty knobs are honest (§19.9).

### 19.9 Difficulty changes situations, not arithmetic
Good hard modes add behaviors and systems rather than inflating numbers — Rebel Inc's Mega-Brutal adds road quality, desperation attacks, and deeper negotiations; Halo raises AI aggression (`gamedeveloper.com/design/difficulty-is-difficult-designing-for-hard-modes-in-games`, `rebelinc.wiki.gg/wiki/Difficulty`). **Commitments:** difficulty = constants *presets* plus system toggles (e.g., patron aggressiveness, faction link eagerness, press-freedom leak speed) — never information unfairness, never rule changes that break legibility. The genre-native model, and our JSON-rules core makes each preset a readable diff.

### 19.10 Misery counterweights (This War of Mine)
11 bit staged dilemmas as concrete micro-scenes with personal stakes, and deliberately included "pride and satisfaction" in the emotional palette — misery alone numbs (`gdcvault.com/play/1022335/This-War-of-Mine-Raising`, `gamedeveloper.com/design/the-secrets-behind-i-this-war-of-mine-i-s-emotional-impact`). **Commitments:** (a) **writing law** — legitimacy deltas arrive attached to named places, named composite people, and specific incidents, never as bare modifiers; (b) **pride beats** — stabilization produces visible, earned positive moments (a market reopens, an election held safely, a road travels without escort) with the same dramaturgical care as the failures. The §14 misery-sim mitigation row now has teeth.

---

## 20. The Closed Society & the Exposure System (v0.2.1 — direction **DECIDED** per Stan, 2026-06-12; mechanization **PROPOSED**; scheduled, not yet built)

*Stan's directive, verbatim intent: when the fundamentals are stable, the game must remind the player of the harsh and often brutal realities citizens of authoritarian states endure; the hidden, subtle ways these regimes behave and lie on the international stage; and give the player the ability to fund think tanks and academics doing empirical research into those regimes so the reality reaches the global stage and pressure rises. This section designs that now so it lands integrated, not bolted on. Grounding research pass: 2026-06-12; sources inline and in §17. Implementation: mechanics with the patron/bloc systems at **v0.7** (same subsystem family — legitimacy warfare); content pass at **v0.8–v0.9** with the Sources screen. Gated on the §19.1 fun gate clearing first.*

### 20.1 Design stance
The §14 point-of-view row, extended: the cost of authoritarian "stability" must be *visible inside the systems*, not asserted by narration. Two laws carry over: **procedures, not sermons** (§19.1 — the player should encounter the closed society through what their instruments can and cannot see, fund, or save), and **sober, abstracted, never gore** (§2). And one mirror, deliberately: the Emergency Powers track (§7) means the player who drifts sees the same machinery from the inside — the Fortress ending is this section pointed at yourself.

### 20.2 The Closed Society layer (content: documented patterns → event cards and dossiers)
When a state collapses out of civilian rule (§5.3), its nodes change *register*: briefing dossiers shift to "inside the closed sector" reporting — thinner, sourced from exiles and monitors, and (deceptive-calm synergy, §9) less precise exactly when it matters most. The event pool for junta/emirate states draws on the documented record, each card carrying its citation:

- **Party dissolution by decree** — Mali, May 2025: all political parties dissolved, members banned from meeting, after a boycotted "national consultation"; UN experts condemned it (`ohchr.org/en/press-releases/2025/05/mali-dissolution-political-parties-step-wrong-direction-warn-un-experts`).
- **Conscription as punishment** — Burkina Faso's 2023 general-mobilization decree used to forcibly conscript journalists, activists, even prosecutors and judges who pursued junta allies; abductions and enforced disappearances of critics (`hrw.org/news/2024/08/21/burkina-faso-conscription-used-punish-prosecutors-judges`, `hrw.org/news/2024/02/27/burkina-faso-abductions-used-crack-down-dissent`).
- **Mass civic-space closure** — 118 civil-society organizations dissolved in one announcement, Burkina Faso, April 2026 (`hrw.org/news/2026/04/20/burkina-faso-crackdown-on-civil-society`).
- **The massacre that quiet hides** — Moura, Mali, March 2022: UN fact-finding documented 500+ killed over five days by Malian troops and "foreign military personnel" (Wagner), mostly summary executions; possible crimes against humanity (`ohchr.org/en/press-releases/2023/05/malian-troops-foreign-military-personnel-killed-over-500-people-during`).
- **The media-ban ladder** — escalation as a reusable arc: French broadcasters banned (2022–23) → BBC/VOA suspended *specifically for covering an HRW massacre report* (2024) → ten outlets suspended at once (Niger, 2026) (`voanews.com/a/burkina-faso-bans-french-state-broadcaster-in-blow-to-press-freedom/6863277.html`, `euronews.com/my-europe/2026/05/09/niger-suspends-nine-french-media-outlets-over-alleged-threats-to-public-order`).
- **The threat follows the refugees** — transnational repression as *domestic* events for the player: Freedom House documents 1,375 direct physical incidents by 54 governments in 107 host countries (2014–2025); detention the top method (`freedomhouse.org/report/transnational-repression`). Dissidents who fled the bloc are reached inside *your* country — a Local/Domestic/International triangle card.
- **Named people, kept** (§19.10 law doing double duty): composite people introduced in pride-beats and earlier events reappear in closed-society dossiers and the post-mortem — the teacher whose school you built, under the new curriculum; the journalist you quoted, conscripted. The post-mortem reveal shows what the regime did with the quiet you left it.

### 20.3 The lying layer (regimes deceive internationally — the player's information environment is contested)
§5.4 gave blocs "pooled propaganda reach"; this grounds it:

- **The fake news agency** — Russia's "African Initiative," built from repurposed Wagner media assets (late 2023), posing as a pan-African agency, FSB-linked editor, paying and training local influencers, publishing in five languages; EU-sanctioned as a FIMI operation (`euvsdisinfo.eu/african-initiative-russian-fimi-operation-disguised-as-a-news-agency/`, `forbiddenstories.org/propaganda-machine-russias-information-offensive-in-the-sahel/`). Field note from our own research pass: searches on Sahel media bans surfaced `news-pravda.com` and `afrinz.ru` framing the bans sympathetically — the flood is measurable first-hand.
- **Mechanic — hostile fog:** bloc/patron `propaganda_pressure` adds a *hostile term* to the §18.5 fog model (bias and variance up in affected theaters) and contests International legitimacy with counter-narratives after your incidents. Disinformation attacks the player's *epistemics*, not their units — that is the honest model of the threat.
- **Killing the referee** — Russia's August 2023 veto terminated the UN Mali sanctions regime and its Panel of Experts after the panel documented Wagner-linked abuses (`aljazeera.com/news/2023/8/31/russia-vetoes-un-resolution-to-extend-sanctions-monitoring-in-mali`). Event: your monitoring umbrella is voted out of existence — and independent Exposure assets (§20.4) become more valuable the moment official instruments die.

### 20.4 The Exposure system (the player's counter — Stan's mechanic, mechanized)
A per-regime/per-bloc **Exposure track (0–100)**: how thoroughly the world's institutions, markets, and publics *know* what the regime does, with evidence that survives denial.

**Instruments (new initiative cluster across Intelligence/Diplomatic families; ~4 initiatives, each with the §7-mandated backfire):**
1. **Endow independent research programs** (think tanks, V-Dem/Freedom-House-style indices, academic field networks) — slow, durable Exposure growth; the empirical backbone.
2. **Support exile media & in-country journalists** — faster Exposure, *human* risk carried by named composite people (§20.2).
3. **OSINT / forensic-accountability units** (Bellingcat/OCCRP-model) — converts incidents from *alleged* to *documented*: upgrades the evidence tier of past events, retroactively.
4. **Targeted-designation diplomacy** — spends Exposure to trigger Magnitsky-style sanctions on regime figures.

**Implemented v0.7 (first cut).** `world.exposure[country]` (0–100) is the track, raised by the `exposure` op and decaying by `exposure_decay` each turn (truth needs upkeep). Shipped initiatives: **Fund Independent Research** (`fund_research`, slow durable Exposure; *funder's-paradox* backfire), **Support Exile Media** (`support_exile_media`, faster; *transnational-repression* backfire on the people you fund), **Targeted Designations** (`targeted_sanctions` → the `designate` op: at/above `sanctions_exposure_min` it adds International, strips `sanctions_patron` influence, and rolls back a bloc's stage, spending `sanctions_exposure_cost`; below threshold the thin case is dismissed and costs credibility), and **Negotiate a Settlement** (`negotiate_settlement` → the `negotiate` op, the §7 endgame). Conversions wired: Exposure raises the patron's price (§8 market) and blunts bloc propaganda (§5.4). Deferred to a later pass (honestly): the OSINT *retroactive evidence-tier upgrade*, the funding-channel choice (overt grant vs arms-length endowment) and its election-dependence, the separate credibility bank, and the regime counter-move *event* cards (the backfires model retaliation for now). The §19.7 dominance gate stays `xfail`: the systems exist but don't yet out-earn their cost — that balance is the v0.8 job, and faking it would betray the thesis suite.

**Exposure converts into pressure (each channel grounded):**
- (a) counters propaganda reach (§20.3) — the antidote to hostile fog is documented truth;
- (b) raises the *reputational price* third parties pay for the patron's no-strings offer (allegiance-market modifier, §8);
- (c) gates and scales targeted sanctions — the documented chain: Global Witness/Sentry research → the first Global Magnitsky tranche (Gertler network, 2017) (`globalwitness.org/en/blog/its-the-end-of-the-year-the-global-magnitsky-sanctions-are-here/`); UN/HRW/Amnesty Wagner documentation → OFAC designations of Wagner's Mali head and Mali's defense minister (2023) (`home.treasury.gov/news/press-releases/jy1645`); NGO coalitions formally submit designation dossiers (`humanrightsfirst.org/library/u-s-global-magnitsky-sanctions/`);
- (d) feeds UN panels, mandates, and ICC-referral events;
- (e) at home, inoculates Domestic against "quiet sector" complacency (§10's deceptive-calm card weakens at high Exposure).

**The sobering counterweight (event, sourced):** pressure is *reversible by geopolitics* — the US lifted the Wagner-linked Mali sanctions in March 2026 amid realignment (`hrw.org/news/2026/03/17/us-lifts-sanctions-on-wagner-linked-officials-in-mali`). Exposure persists; its conversion rate can be politically gutted overnight. The truth outlives the policy that acted on it — and has to wait for the next one.

**Backfire channels (design law §7; all documented):**
- **The funder's paradox** — the OCCRP case: ~52% of 2014–23 funding from the US government, with veto rights over key hires; deniable editorial influence, undeniable attack surface; then the 2025 USAID freeze gutted the stream (`occrp.org/en/frequently-asked-questions-on-occrps-funding-and-editorial-policies`). Mechanic: choose the funding channel — **overt state grant** (cheap, fast, "foreign puppet"-attackable, and *election-dependent: your own domestic politics can kill your exposure network mid-game*) vs **arms-length endowment** (expensive, slow, resilient).
- **Regime counter-moves**, each an event with your fingerprints on the consequences: expel the investigator (Mali PNG'd the UN mission's human-rights chief over witness choices, 2023 — `aljazeera.com/news/2023/2/6/mali-expels-u-n-missions-human-rights-chief`); ban the funder's NGOs wholesale (Mali banned all French-funded NGOs, Nov 2022 — `africanews.com/2022/11/22/mali-bans-ngos-funded-or-supported-by-france/`); punish the coverage itself (the 2024 BBC/VOA bans, §20.2); conscript or disappear local staff (§20.2 — *your funded researchers' local partners pay the price; the game must not flinch from this*); spyware against your networks (Pegasus Project: forensically confirmed targeting of journalists and human-rights defenders, including HRW staff — `securitylab.amnesty.org/case-study-the-pegasus-project/`, `hrw.org/news/2022/01/26/human-rights-watch-among-pegasus-spyware-targets`).
- **The credibility bank** — rushed or wrong claims spend it: a failed allegation reduces Exposure and International both. Empirical care is mechanically rewarded; that is the point of funding *empirical* research over messaging.

### 20.5 Resonance, named
The game itself behaves like the organizations it depicts: it cites its homework (the §14 Sources screen) and treats documentation as a weapon against manufactured quiet. The Exposure system is the game's own method, handed to the player.

### 20.6 Verification ledger (no-phantom discipline for the content pipeline)
Flagged by the research pass as plausible but **unverified — confirm before any card ships**: Mali's 2022 RFI/France 24 suspension specifics; the 49 Ivorian soldiers detention (2022) as hostage diplomacy; President Bazoum's continued detention; the jailed Malian economist Étienne Fakaba Sissoko; Wagner-linked AFRIC fake election observers; Sahel juntas hiring Western PR/lobbying firms (FARA-searchable). Also not yet researched: internet-shutdown statistics (Access Now #KeepItOn), "foreign agent" law diffusion, SLAPP/lawfare cases, astroturfed think tanks.

---

## 21. Grand Mode — the world, and the global precedent layer (v0.10 — DECIDED per Stan, 2026-06-14; foundation built, expanding)

Stan's directive: the game should be *world scale* — as many nations as the real earth — where **every choice ripples through every plausible variable, everywhere**, not a self-contained theater. This is the §4/§12 grand-mode vision, pulled forward from v2.0. The architecture was built for it: the engine is theater-agnostic (it runs on whatever nodes/edges/factions load), and Domestic/International, patrons, blocs, and exposure already couple globally. Grand mode is therefore **a bigger dataset + cross-theater coupling systems, not a rewrite.**

### 21.1 The world dataset (`rules/scenarios/grand/`)
**~40 nations** (v0.12 reached the §4 target band of ~40–50; was ~20 at v0.10), each a capital node grouped by `theater` (sahel, west_africa, maghreb, horn, gulf, levant, afpak, south_asia, central_asia, caucasus, se_asia, andes, north_america, caribbean, east Africa). Quarter turns, a 2001 start, a 25-year (100-turn) horizon. Composited *global* faction families — an al-Qaeda-network composite, an IS-lineage composite, an ethno-separatist composite, a narco-insurgency composite — seeded across their real theaters (Sahel/Lake Chad jihadism, the Horn and Great Lakes, the Shia crescent, the Naxalite belt and Kashmir, Myanmar's civil war, Latin-American narco-insurgency, the Caribbean's gang collapse, and more). Each addition is grounded in a real 2001–2026 conflict and carries plausible governance/development/grievance and regional **patron leanings** that exercise the v0.11 three-archetype contest (Wagner→Sahel/CAR, Iran→Lebanon and the Gulf, China→Myanmar and the Horn). **Inter-theater edges** (ideology, diaspora, sea lane, arms route) make the world a single connected graph, not isolated regions: contagion, sponsor flow, and bloc adjacency cross theaters. *Honest scope: grand mode is the systems at world scale; it is **not** history-calibrated like Scenario 1 (a future milestone). At 40 nodes an unopposed passive world burns (≈30/40 capitals fall over 25 years — the thesis "left alone, it grows" at scale), and the Sahel-tuned `CompetentPolicy` no longer scales — a grand-mode scoring pass and a grand-scaled competent benchmark are the clear next milestone (§21.5).*

### 21.2 The global norms / precedent layer (the keystone — `sim/norms.py`)
This is what makes "every choice ripples worldwide" *true and mechanical* rather than rhetorical. Three world norms (0–100, neutral 50) accumulate from **how you fight, everywhere**:
- **kinetic** — raised by every military initiative;
- **rule_of_law** — raised by governance/diplomatic/exposure initiatives;
- **autocracy** — raised by each Emergency-Powers (drift) tier.

Each turn they decay toward neutral (`norm_decay` — the world forgets), and they **feed back into every theater at once** through plausible channels:
- a kinetic, autocratic precedent multiplies insurgent **recruitment in all theaters** (Kilcullen's accidental guerrilla and your hypocrisy, at global scale): `recruit_mult = 1 + norm_feedback·norm_recruit_weight·((kinetic−50)+(autocracy−50)−(rule_of_law−50))/100`;
- world norms move **International** each turn (law rewarded, force/autocracy punished);
- an autocratic norm raises **rival-patron appeal** worldwide (you legitimised the model you oppose) via a competitiveness penalty in the §8 market.

**The discipline (the design's anti-noise rule):** propagation is through *named, realistic channels* — not literal all-to-all wiring. And the whole layer is gated by `norm_feedback`: **0 in single-theater scenarios** (so the Sahel history calibration is untouched *by construction* — a passive player takes no actions, norms never leave neutral, feedback is exactly zero), **>0 in grand mode**. Verified: pure-kinetic global play → kinetic≈100, recruit ×1.25; pure development → law≈100, ×0.76; emergency powers → kinetic+autocracy high, ×1.49. The thesis, at world scale, and test-enforced (`tests/test_grand.py`).

### 21.3 Global arms & oil markets (the commodity ripple — `sim/markets.py`, v0.11)
The second cross-theater channel, built on the §21.2 norms template: two world prices (0–100, neutral 50) that the *whole board* moves and that then move the board back, so a war in one theater is felt in every other through the market, not a shared scoreboard.
- **arms** rises with total active insurgent strength worldwide and decays toward neutral (`arms = arms + (target − arms)·market_adjust`, `target = 50 + arms_conflict_weight·(mean_node_strength − arms_baseline)`). A violent world is a well-supplied one.
- **oil** rises with instability in **petro-states** (nodes whose `resources` include `oil`: governance collapse + insurgent presence) and decays toward neutral. The Maghreb and Gulf are the price-setters.

The feedback — two more *named, realistic* channels:
- a hot **arms** market lifts insurgent **ExternalSupport in every theater** via an `arms_mult` on the §18.5 external term, exactly as `recruit_mult` rides the norms (`arms_mult = max(0.5, 1 + market_feedback·arms_supply_weight·(arms−50)/50)`) — the sponsor's flow is cheaper when the world is awash in weapons;
- a high **oil** price drags the importer-democracy's **Domestic** each turn through the ledger (source `oil_market`) — the home front pays for other people's wars at the pump.

Gated by `market_feedback` (0 in single-theater → markets never leave 50, `arms_mult==1`, no `oil_market` ledger line → **calibration untouched by construction**; >0 in grand). Verified: an unopposed grand world runs the arms market hot (>55) and the oil drag appears in the ledger; the Sahel arc never moves either.

### 21.4 Rival patrons & the global rivalry score (the allegiance contest — `sim/patrons.py`, v0.11)
v0.7's §8 market was a single mercenary patron. Grand mode makes it a **contest** between the three real archetypes (`rules/patrons.json`): **mercenary** (Wagner/Africa-Corps — fast, coup-proofing, oil-funded), **investor** (infrastructure-and-debt, non-interference, patient), **proxy** (arms-and-advisers through the faction graph). Each non-civilian state picks the patron with the highest **appeal** = its standing seed there + a **bandwagon** on that patron's *global* strength + the archetype's speed + (if oil-funded) an oil-price boost; the winner's influence and its `patron_strength` (global reach) grow, and a **rivalry** score (0–100) tracks the share of the world the rival bloc holds — a winning bloc captures faster (the bandwagon).

The cross-theater payoff — the clearest expression of "every choice connects": **targeted sanctions** (the §20 `designate` op) now also dock the dominant patron's **global** `patron_strength`, so denying a patron one state makes it weaker in *all* of them. Gated by `rivalry_feedback` (0 in single-theater → the market stays today's mercenary-only pull, byte-for-byte the calibrated behavior; >0 in grand → the contest, with `patron_strength`/`rivalry` live). Verified: in a grand run ≥2 archetypes win reach (not a monopoly), rivalry rises as states fall, and a designation drops the targeted patron's global strength. Enforced by `tests/test_markets.py` (9) + `tests/test_grand.py`.

### 21.5 What's next for grand mode (honest backlog)
Node count is **done** (v0.12: ~40 nations across 15 theaters); grand **scoring** is scale-invariant (v0.13, §21.6); **winnability** — engaged play out-scoring abdication — is reached by the first world-scale lever, **Regional Commands** (v0.14, §21.7), and deepened by the second, **Coalition burden-sharing** (v0.15, §21.8). What remains: further world-scale levers (an inner-ring/outer-ring coalition tiering, intelligence-sharing, sanctions/economic statecraft with teeth — the §21.8 brief lists them); cross-theater **tactic/ideology contagion** (capability tier-ups propagating along ideology edges); per-theater reporting and a pan/zoom map UI; and eventually a grand-mode history-calibration pass. The v0.10–v0.11 channels (norms, markets, patron rivalry) are the connective tissue these build on. This section is the spec those build against.

### 21.6 Grand-mode scoring, and the winnability finding (v0.13)
At 40 nodes the single-theatre score (§11) **degenerated**: `order_mult = 1/(1 + junta_w·junta_count + …)` uses an *absolute* count, so ~30 juntas drove it to ≈0.08 and crushed every score to ≈0 — a scale bug, not a balance call. v0.13 replaces it, **gated by `grand_scoring`** (0 in single-theatre → byte-identical, calibration untouched; 1 in grand), with a **scale-invariant containment** score: a world police can't stabilise forty theatres at once, so it is judged on *containment*, not omnipotence — (a) **population-weighted quality** (`√population` weighting, so protecting a consequential state counts for more than a micro-state), blended with (b) the **free fraction** of the world's capitals (`1 − junta_share`), the whole dragged down by consolidated authoritarian **blocs** (the §5.4 loss condition). Scores are interpretable again and rank **kinetic abdication-of-restraint strictly worst** at every scale.

**The honest finding (measured, not assumed):** even with the corrected score, *no policy robustly out-scores passive at 40 nodes.* A swept benchmark containment policy (defend the civilian capitals nearest collapse, hold the umbrella, sanction patrons) beats passive in **0–1 of 6 seeds** across a grid of scoring-weight × bandwidth settings; raising the per-turn mandate budget (a "global operation has more bandwidth" lever) lets a competent player bend the world only from ~25 to ~19 juntas — a real but **marginal** edge that its blood-and-treasure costs (the thesis: democracies pay at home) then erase. The diagnosis is not the scoring: it is that **the player's strategic levers are too local to bend a global trajectory.** Forcing a win by tuning constants is exactly the dishonesty the thesis-as-tests discipline (§3.8) exists to prevent, so v0.13 ships the scoring foundation and *names the real milestone*: **winnable grand mode needs new world-scale levers** — coalition-building, regional commands that multiply reach, economic/sanctions statecraft with teeth, intelligence-sharing — that let engaged play change outcomes across many theatres at once, plus an explicit scoring stance that abdication (letting the authoritarian bloc consolidate) is a failing grade. **v0.14 (§21.7) builds the first of those levers and reaches the win.**

### 21.7 Regional Commands — the first world-scale lever (v0.14)
The v0.13 finding was diagnostic: the player's hands (a few actions a turn) can't reach a 40-nation world, so abdication scored as well as effort. A **Regional Command** is the lever the research pointed to — the real **AFRICOM/CENTCOM theatre commands**, **Operation Barkhane**, the Lake-Chad **Multinational Joint Task Force**, and, as a game pattern, **HoI4's garrison templates** ("a standing suppression investment, paid in upkeep, auto-applied across held nodes"). It is a **standing posture over a whole theatre** that passively *contains* insurgency across every one of its nodes each turn: light per-node attrition on the strongest faction, a small governance buffer, a local-legitimacy buffer. It buys **breadth, not depth** — it bends the trajectory and buys time but does **not** resolve a theatre (crises still need your hands-on actions). Posture sets the board; agency wins it.

Its counterweight is the thesis made mechanical, from the matching research (Kennedy's *imperial overstretch*; Merom's home front as the true ceiling; Mueller's logarithmic casualty curve): every command bleeds **treasury upkeep** and, more bindingly, **home legitimacy** each turn — and the home strain is **triangular in the count** (`strain · k(k+1)/2`), so the second and third theatre cost far more than the first. A hard **cap** (`command_max`, the CK3 "domain limit" pattern) forbids policing everywhere; you must triage where to stand. Withdrawal fires on **politics, not defeat** (Barkhane): if treasury can't sustain the upkeep, or Domestic falls through `command_domestic_floor`, a command is forced home, leaving a vacuum. Gated by `commands_enabled` (0 single-theatre → dormant, inert, and filtered out of the action menu, so calibration is untouched by construction; 1 in grand).

**The win, measured and earned (not tuned):** the `GrandCompetentPolicy` — lead with commands over the most volatile theatres, then triage hands-on, and *don't over-extend a weak home front* — **out-scores a passive world on 7 of 8 seeds and is the single best strategy**, above every pure doctrine, with pure-kinetic still worst. The edge is causal (commands ON vs OFF moves both the score and the junta count) and modest by design: commands bend the world from ~25 juntas to ~21, helping without trivialising — you can hold the line in the theatres you choose, never the whole world. This is the §3.7 reasonable player, finally rewarded at world scale. The next levers (coalition burden-sharing with free-riding, intel-sharing rings, sanctions with teeth) extend this pattern; §21.5 tracks them.

### 21.8 Coalition burden-sharing — the second world-scale lever (v0.15)
Regional Commands cap out fast because the home front can carry only one or two (§21.7). The way real lead democracies stretch further is a **coalition** — the 87-member Global Coalition to Defeat ISIS, NATO, the Lake-Chad MNJTF's troop-contributing neighbours. So `sim/coalition.py` (new `rally_coalition` initiative + `coalition` op) adds a single cohesion gauge (0–100): allies **share the upkeep** of your commands — `burden_share = coalition_max_share · cohesion/100` of both the treasury upkeep and the accelerating home-front strain — so a strong coalition lets you sustain more theatres than you could alone.

But a coalition is the thesis from a second angle (**Olson & Zeckhauser 1966**: collective security is a public good, so partners under-provide). Cohesion **free-rides away** every turn (`coalition_decay`); it frays **faster when the rival bloc is ascendant** (`coalition_rivalry_erosion · rivalry/100` — fair-weather members hedge toward the winning side, the EU4/Vic3 leverage-contest pattern) and **faster the more commands you lean on it to carry** (`coalition_command_strain · |commands|` — over-extension feeds the case against you). You hold it up only by spending political capital to `rally` (which itself risks a burden-sharing-dispute backfire). So the burden you offload is real but perishable — and you never escape free-riding: in play, cohesion settles around the mid-range (the NATO-2% reality), not 100. Gated by `coalition_enabled` (0 single-theatre → dormant, menu-filtered, calibration-safe; 1 grand).

**Measured effect:** giving `GrandCompetentPolicy` the coalition (rally when cohesion bleeds low) lifts it from beating passive 6/8 to **7/8 seeds and from ~19 to ~22 mean score**, bending the world from ~21 juntas to ~18 — a clear, *earned* deepening (cohesion costs capital and decays), still bounded (the world mostly burns; you hold the lines you choose). Pure doctrines still lose, kinetic worst. `tests/test_coalition.py` (7) pins the burden-share, the free-riding/rival fraying, the deepened win, and the gating. Design grounded in a research pass on coalition/alliance mechanics (Vic3 power blocs, EU4 favors/trust/aggressive-expansion, Stellaris federation cohesion, the inner-ring/outer-ring Five-Eyes tiering) and burden-sharing economics. Future tiers from that brief — an inner high-trust ring vs a fair-weather outer ring, intel-sharing, pressing members toward their pledge — extend this gauge; §21.5 tracks them.

---

## Changelog

- **v0.1** — 2026-06-12 — Initial full draft from core prompt + research session (Unciv feasibility check; Sahel 2012–2026 record). Framing locked: real world / alt-history; scenarios-first; design-doc-first per Stan's three scoping answers.
- **v0.2** — 2026-06-12 — Repo bootstrapped (`stan2032/PaxStressia`). Added §18 Simulation Specification (determinism law, state vectors, resolution order, effect-op vocabulary, v0.2 formulas bound to `rules/constants.json`, itemized-ledger contract, policy interface, stub inventory). Added open question #7 (repo name *PaxStressia* vs working title *MANDATE*). §15 roadmap: v0.2 row marked delivered. No prior content removed.
- **v0.2.1** — 2026-06-12 — Docs-only growth from two research passes. Added §19 Playability, Pacing & Balance (precedent-game lessons → binding commitments: fun gate, anti-whack-a-mole package, interesting-decisions audit, asymmetry-of-goals, Emergency Powers calibration, dominance check, intrinsic anti-snowball, situational difficulty, misery counterweights). Added §20 The Closed Society & the Exposure System (Stan's directive DECIDED; mechanization PROPOSED for v0.7–v0.9: closed-society content layer, hostile-fog disinformation, Exposure track with documented pressure chains and backfires). §17 gained two source blocks; §18.4 reserved-op list extended for §20. Repair note: the §19 insertion briefly dropped the changelog header and v0.1 entry by edit-anchor mistake — restored in the same session, verified against v0.2 git history; no other content touched.
- **v0.2.2** — 2026-06-12 — **Title DECIDED: PaxStressia** (per Stan: the "Pax …ia" eras; pax at the cost of stress; "being lied about but not dealing in lies yourself. or, trying your best to."). Added §1 "The Name"; resolved open questions #4 and #7; header retitled; live project files (README, pyproject, schema titles, sim/harness strings) renamed. MANDATE retained in historical sections per the cumulative rule.
- **v0.5** — 2026-06-13 — **History calibration: reality is now the baseline, enforced.** Tuned constants until a passive player reproduces the Sahel arc on 10/10 seeds — Mali junta in the coup-cascade window, cascade ML→BF→NE in the historical order, bloc formed, insurgency still growing at the horizon. New engine mechanics, doc-code lockstep: absorptive capacity (headroom-scaled growth → S-curves), distance-discounted collapse threat (`collapse_dist_decay` — the center's deterioration topples the capital, not the far north), governance-resisted spread (quadratic — capitals are raided, never held). `harness/calibrate.py` grades the battery (5 checks) and runs in CI with an uploaded artifact. **Three of four thesis tests promoted from xfail to ENFORCED** (calibration, kinetic-loses-Local, hearts-minds-loses-to-momentum) — the design document is now true by force. `MixedPolicy` + the §19.7 dominance check ship as instruments, honestly xfail until a winnable balanced path exists (v0.7). Constants status flipped from PROPOSED to CALIBRATED. One known compression: BF→NE spacing is tighter than history (ordered, but ~5 turns vs ~18 months) — acceptable within the generous window, flagged for v0.6.
- **v0.10** — 2026-06-15 — **Grand mode foundation (§21): the world, and the global precedent layer.** Per Stan's "go fully global now." New `rules/scenarios/grand/` — ~20 nations across ~11 theaters, composited global faction families, inter-theater edges (ideology/diaspora/sea/arms) making the world one connected graph; quarter turns, 2001 start, 100-turn horizon. New **`sim/norms.py`** — the keystone that makes "every choice ripples worldwide" mechanical: three world norms (kinetic/rule_of_law/autocracy) accumulate from how you fight and feed back into recruitment in *every* theater, into International, and into rival-patron appeal. Gated by `norm_feedback` (0 in single-theater → **Sahel calibration untouched by construction, still 10/10**; >0 in grand). Ported to both engines; `tests/test_grand.py` (8) enforces the ripple and the gating. Proto: grand in the scenario picker, world layout, and a "World precedent" readout. Honest scope: systems at world scale, not yet history-calibrated; markets, multi-patron rivalry, and ~45 nodes are the backlog (§21.3).
- **v0.18** — 2026-06-16 — **A situation map, not a void (UI pass 2: "can we make it prettier?").** The black background becomes a strategic map: a deep-ocean radial gradient, a faint cartographic **graticule**, and a soft **landmass under each theatre's nodes** (a padded convex hull; adjacent theatres merge into coastline) with faint region labels — so the board reads like a real ops map, not circles in a void. The 40-nation world was also **re-laid-out** with breathing room (rough geography, grouped by theatre) so the nodes stop piling up and the land shows; node radius/heat tuned down to match. The headless `preview.mjs` gained the same backdrop and drove the iteration. Honest split (answering Stan's "or is that future plans?"): a *vector situation-map aesthetic* is doable now in the greybox; *photoreal terrain + 3D situation-room lighting + motion* remain the production-client (Godot, §13.4) goal, kept cheap by the swappable-renderer split. Proto/UI only; engine/rules/calibration untouched (103 tests, smoke, 10/10 all hold). Next UI step: pan/zoom for the dense grand board.
- **v0.17** — 2026-06-16 — **Show, don't tell — the map starts speaking (UI pass 1; §13.3 legibility principle extended).** Per Stan: less text, understanding by inference from the screen, every "idea" a concrete object. The board now carries the state: insurgent strength is a **red ring whose thickness is the strength** (the eye finds the hot spots), node colour is who-rules, your Regional Command is a planted **flag**, a petro-state an **oil drop**, capitals a **★**; a dense 40-nation board **drops its labels and you tap a nation** to identify it (interactive, not a wall of text). Resources became objects in the header — 🏛️ Mandate, 💰 Funds, 🏠 Home, 🤝 Allies, 🛡️ Local, ⛓️ Drift — with the words moved to tooltips and a concise visual map legend in the Key. New dev tool `proto/preview.mjs` renders the board headlessly (SVG → PNG via cairosvg) so the visual language is reviewable without a browser; it immediately caught a real bug — the population-based node radius exploded at grand scale (India's 1.3M ≈ half the map) — now log-scaled and capped. Proto/UI only (no engine, rules, or calibration change); both engines' smoke + the 103-test suite + calibration unaffected. Honest scope: the 40-node board is legible but dense — a pan/zoom pass is the next UI step.
- **v0.16** — 2026-06-16 — **The Emergency Powers track lands, and the thesis suite is complete (§7; the last xfail promoted).** Built the full escalating ladder the design always named — **I Surveillance** (existing) → **II Administrative Detention** (`administrative_detention`: strong attrition + imposed control, Belmarsh/MISA/Micas) → **III Censorship & Martial Law** (`martial_law`: a large governance/Order boost, India 1975/Turkey) — each cheap, front-loaded, *genuinely powerful* (so a crisis-chasing player is tempted), each adding permanent one-way **Authoritarian Drift**. New `drift_score_cost`: Drift is now a **direct** score cost as well as the IntegrityMultiplier — the democracy is the prize, every step toward autocracy spends it (the Frostpunk lesson: the loss is **mechanical, not a "you crossed the line" scold**). With this, `test_emergency_powers_tempting_but_scored` is **ENFORCED**: `EmergencyPowersPolicy` now produces strictly *stronger raw* Stabilization×Order than pure kinetic (tempting: ~16 vs ~10 across seeds) yet a strictly *worse final* (~−9 vs ~−1) — win ugly, score poorly. **All four design-thesis tests are now true by force** (the project's most-protected idea, complete). Built from existing ops (no new ops); both engines (the drift cost mirrored in the proto score); tiers grounded in a research pass on real states of emergency and the ratchet effect. Gating-safe — passive/competent/kinetic never drift, so calibration is **10/10** and the other thesis tests are untouched. **103 tests pass / 0 xfail.**
- **v0.15** — 2026-06-16 — **Coalition burden-sharing: the second world-scale lever (§21.8).** Allies share the upkeep of your Regional Commands so you can stretch further — `sim/coalition.py`, new `rally_coalition` initiative + `coalition` op, one cohesion gauge whose `burden_share` lightens both the treasury upkeep and the accelerating home-front strain of commands. The thesis from a second angle (Olson–Zeckhauser free-riding): cohesion bleeds every turn, frays faster under an ascendant rival bloc (the §8 rivalry) and the more commands you lean on it to carry, and must be re-rallied (with a burden-sharing-dispute backfire) — you never escape free-riding, so it settles mid-range (NATO's 2% reality), not full. Gated by `coalition_enabled` (0 single-theatre → dormant + menu-filtered → **calibration still 10/10**; 1 grand). Measured: giving `GrandCompetentPolicy` the coalition lifts it from beating passive 6/8 → **7/8 seeds**, ~19 → ~22 mean, ~21 → ~18 juntas — earned (cohesion costs capital, decays) and bounded (the world mostly still burns); pures still lose, kinetic worst. Both engines (proto: a Rally-the-Coalition action + cohesion in the Regional-Commands readout); `tests/test_coalition.py` (7). Grounded in a research pass on coalition/alliance mechanics + burden-sharing economics. 102 tests / 1 xfail.
- **v0.14** — 2026-06-16 — **Regional Commands: the first world-scale lever, and grand mode becomes winnable (§21.7).** v0.13 measured that the player's levers were too *local* to bend a 40-nation world; this builds the lever the research points to (AFRICOM/Barkhane/MNJTF; HoI4 garrison templates). A **Regional Command** (`sim/commands.py`, new `establish_command` initiative + `command` op) is a standing posture over a whole theatre that passively **contains** insurgency across all its nodes each turn — breadth, not depth — at an **accelerating home-front cost** (treasury upkeep + triangular Domestic strain = Kennedy overstretch + Merom + Mueller), a hard cap (triage), and withdrawal on home-front collapse not defeat (Barkhane). Gated by `commands_enabled` (0 single-theatre → dormant + filtered from the menu → **calibration still 10/10 by construction**; 1 grand). New `GrandCompetentPolicy` leads with commands then triages: **out-scores passive on 7/8 seeds and is the best strategy, kinetic still worst** — the win is causal (commands ON vs OFF) and modest (bends ~25→~21 juntas: helps, doesn't trivialise). Both engines (proto: establish menu + "Regional Commands" readout); briefing now carries `theater` and your own `commands`. `tests/test_commands.py` (7) pins the lever, the cost, the win, and the gating. Grounded in three parallel research passes (coalition COIN, grand-strategy scale mechanics, imperial overstretch). 95 tests / 1 xfail.
- **v0.13** — 2026-06-16 — **Grand-mode scoring made scale-invariant, and the winnability problem measured honestly (§21.6).** The single-theatre score degenerated at 40 nodes (absolute junta count → `order_mult`≈0.08 → every score ≈0). New **gated** (`grand_scoring`) scale-invariant **containment** score: population-weighted quality blended with the free fraction of the world's capitals, dragged by consolidated blocs; order folded in (==1). Single-theatre byte-identical (calibration 10/10); kinetic ranks worst at every scale. Then the **honest finding, measured not assumed:** no policy robustly out-scores passive at 40 nodes (a swept benchmark containment policy wins 0–1/6 seeds across scoring-weight × bandwidth grids; more mandate bends the world only ~25→~19 juntas, an edge its costs erase). Diagnosis: the player's levers are **too local to bend a global trajectory** — so v0.13 ships the scoring foundation and names the real milestone (world-scale levers: coalitions, regional commands, sanctions with teeth) rather than fake-tuning a win. Both engines; `tests/test_grand.py` adds the scale-invariance + gating test. 87 tests / 1 xfail.
- **v0.12** — 2026-06-16 — **The world widens (§21.1): grand mode goes from ~20 to ~40 nations.** Per Stan's "as many nations on earth." Twenty more capitals, each grounded in a real 2001–2026 conflict and wired into every existing connective system — Sahel/Lake Chad (Burkina Faso, Chad, Mauritania, Cameroon), the Horn and Great Lakes (Ethiopia, Kenya, South Sudan, DR Congo, CAR), MENA/Levant (Egypt, Tunisia, Lebanon), South/SE Asia (India, Myanmar, Bangladesh, Indonesia), Central Asia (Tajikistan), and the Americas/Caribbean (Mexico, Haiti, Ecuador). +40 inter-theater edges (border/smuggling/arms/sea/ideology/diaspora) keep the world one connected graph; regional patron leanings exercise the v0.11 contest (Wagner→Sahel/CAR, Iran→Lebanon, China→Myanmar/Horn); petro-states feed the oil market. A **realism pass** keeps genuinely resilient states (India, Egypt, Indonesia, Mexico…) from collapsing as readily as fragile ones (Haiti, CAR, South Sudan). Both engines (40 mapped on the world layout); `test_grand`/smoke now assert the ~40-nation scale; determinism holds, **Sahel calibration still 10/10** (gated, untouched). The `test_the_patron_contest_is_real` claim was made **across seeds** (a distributional claim shouldn't pin one seed). Honest scope (§21.5): scale is done; the expansion makes **grand-mode scoring + a grand-scaled competent policy** the next milestone — at 40 nodes a passive world burns (≈30/40 fall) and the Sahel-tuned CompetentPolicy can't yet out-score passive. 86 tests / 1 xfail.
- **v0.11** — 2026-06-16 — **Deepen the ripples (§21.3–21.4): global arms/oil markets + a multi-patron allegiance contest.** Per Stan's "deepen the ripples — more realistic cross-theater channels, not isolated regions sharing a score." Two new norms-pattern systems. New **`sim/markets.py`** — world **arms** (rises with global conflict → lifts insurgent ExternalSupport in *every* theater via `arms_mult`) and **oil** (rises with petro-state instability → drags home **Domestic** through the ledger) prices. New **`rules/patrons.json`** + generalized **`sim/patrons.py`** — the §8 market becomes a contest of three archetypes (mercenary/investor/proxy) with a global `patron_strength` bandwagon and a `rivalry` score; **targeted sanctions now dock a patron's global reach** — deny it one state, weaken it everywhere (the clearest "every choice connects"). Both gated (`market_feedback`/`rivalry_feedback` = 0 in single-theater → markets pinned at 50, rivalry 0, mercenary-only pull byte-identical → **Sahel still 10/10 by construction**; >0 in grand). Ported to both engines (proto gains a "World markets & rivals" readout); `tests/test_markets.py` (9) enforces the ripples and the gating. 86 tests pass / 1 xfail; calibration 10/10; grand determinism holds on both engines. Honest scope unchanged (§21.5): connective systems deepened, grand mode still not history-calibrated; ~45 nodes, ideology contagion, and the map-UI pass remain.
- **v0.9** — 2026-06-14 — **Scenario 1 made legible as a story: endings, post-mortem, and the Sources screen.** `Engine.ending()` (both engines) resolves the four endings (§11) on two data-driven axes — ABROAD (Stabilization × Order) and HOME (Integrity); passive never earns Pax, drift forces Fortress, competent reaches a held-line ending on some seeds. `Engine.post_mortem()` + the proto end-screen surface where the fog most lied (true vs believed strength per region) — the §9 reveal made concrete. **`rules/sources.json`** ships the bibliography as schema-validated data with an honest per-entry confidence flag (verified / established / **alt_history**) and a disclaimer, rendered as the in-game Sources screen; two specific claims (Moura figures; *Afghanistan '11* App-Store removal, 2018) were live-verified this build. Pre-build **audit**: removed dead `detect_proto_blocs` (superseded by `sim/blocs.py`); confirmed all 20 effect-ops are handled in both engines. 68 tests pass / 1 xfail; calibration 10/10.
- **v0.8** — 2026-06-13 — **The game is winnable, and the thesis is fully enforced.** Tuned *player tools + scoring only* (never the passive world), so the history calibration held 10/10 throughout while a real win path opened. Headline change: the **insurgent-grip discount** to StabilizationIndex (§11) — a region run by an entrenched insurgency counts as unstabilized however good its surface numbers, putting Pillar 4 (quiet ≠ peace) in the score. Plus harder junta/bloc OrderMultiplier weights, affordable programmes (lower cost weights, cheaper+stronger Development), and a new **`CompetentPolicy`** (§18.7) — the §3.7 reasonable player. Outcome (mean final on the arc): Competent ≈ 12 > Passive ≈ 2 > every pure strategy. **Two thesis tests promoted to ENFORCED:** `test_no_pure_strategy_dominates_the_balanced_baseline` (§19.7 Pillar 3 as a number) and `test_a_reasonable_player_can_beat_history` (§3.7). Emergency-powers stays xfail — honestly: scored-worse holds, but tier-1 surveillance isn't yet *genuinely tempting* (§3.5), which awaits the full track. Grip discount ported to the proto so both engines score alike. 60 tests pass / 1 xfail.
- **v0.7** — 2026-06-13 — **The endgame layer: the game gets contest and exits.** Four interlocking systems, both engines, doc-code lockstep: **bloc consolidation clock** (`sim/blocs.py` — adjacent juntas federate and consolidate by stage, draining International via propaganda and exporting grievance; scoring now weights consolidation, not count); the **patron allegiance market** (`sim/patrons.py:market` — the no-strings patron's capture is resisted by your International standing and the regime's Exposure); the **Exposure system** (§20, first cut — `world.exposure`, the `exposure`/`designate` ops, and the *fund research / exile media / targeted sanctions* initiatives, with documented backfires; conversions into patron price and bloc propaganda relief); and the **negotiation endgame** (`negotiate` op — settles a stalemated faction, soft at home and respected abroad). New constants for all four; new state serialized for determinism. `tests/test_endgame.py` (10) covers each; **history calibration still 10/10** after the changes. The §19.7 dominance check stays `xfail` — systems exist but their balance doesn't yet out-earn its cost (the v0.8 tuning job). Prototype ported in full (exposure/patron/bloc readouts, the new ops and initiatives, Key-glossary section).
- **v0.6** — 2026-06-13 — **The Transparency Dial (§6), implemented** — the thesis in one mechanic. Fingerprint incidents (partner atrocity, errant strike) become disclose-or-suppress choices; suppression starts a leak clock whose odds rise with press freedom and age, detonating across all three gauges at a multiple of the honest cost. New `suppress_clock` op + five `leak_*`/`press_freedom` constants (both engines, doc-code lockstep); leak-clock state serialized for determinism. `tests/test_transparency.py` enforces the thesis economics (disclose cheaper on average; suppression a real gamble with `min == 0`; free press ⇒ more leaks). Proto: a **Buried** counter, leak/bury headlines, and a Key-glossary entry. Also added **§13.4 Presentation-technology evaluation** answering "can we use newer tech?" — Godot 4 primary, WebGPU+Babylon.js the stay-web fallback, raw GL/Bevy/Unity assessed and declined; the JSON core makes the eventual 3D client a re-skin, not a rewrite. (Fog estimates and elections already shipped v0.2–v0.3; the dial is the milestone's new system and deepens both.)
- **v0.5.2** — 2026-06-13 — **Legibility pass on the prototype**, from Stan's first playtest ("too collated; words too specific; can't see how the numbers relate"). Plain-language relabel led by everyday words with the doctrinal term kept as gloss (Forces/Dug-in/Activity, Home/Allies/Local, Mandate/Funds); each region stat is now a labelled meter coloured for good/bad direction with its ± uncertainty; a new always-available **Key** tab (plain glossary + causal loop + map legend) and a one-time first-run orientation; de-cluttered map labels; affordability dimming on actions. Recorded in §13.3 two binding directions: the **production-presentation/3D goal** (long-horizon, Godot-leaning) and the **legibility principle** (readable without a manual). No engine/rules/calibration changes.
- **v0.5.1** — 2026-06-13 — Open question #5 RESOLVED: **PolyForm Noncommercial 1.0.0** (`LICENSE.md`). GitHub Pages deploy (`.github/workflows/pages.yml`) + root redirect → playable at `stan2032.github.io/PaxStressia/` after the one-time Pages toggle; replaces the dead-localhost instruction.
- **v0.4** — 2026-06-12 — **Scenario 1 "The Arc" in data**: 12-node map (Niamey on-map — Niger's cascade can complete endogenously; coastal-spillover marker measures southward bleed), third faction *Azawad National Front* (MNLA→CMA→FLA composite; ambivalent −0.1 affinity keeps the 2026-style concord reachable), 8 historical beats + 6 generic cards. Engine growth, doc-and-code in lockstep: **spread over edges** (§18.5 — the promised v0.4 system; northern Burkina ignites from Mopti unscripted), **scenario loading** (§18.9: replace/merge/fall-through semantics, both engines), `once` beats with collapse/link predicates, `presence`/`patron` event ops (§18.4, events-only by design). Beats-vs-system law stated in §18.9. Thesis suite now runs history calibration on the arc; **second thesis test XPASSes pre-calibration** (pure-kinetic loses Local — FM 3-24's paradox holds on all five seeds). Proto: scenario picker, 12-node layout, arc in the snapshot, arc smoke in CI.
- **v0.3** — 2026-06-12 — **Phase 0 delivered: the greybox web prototype** (`proto/index.html`, single file, phone-browser). Implements the §18 loop client-side from the same `rules/*.json` (fetched live when served; CI-checked embedded snapshot as `file://` fallback): fog estimates with ±90% bands in the greybox per §19.5, alert-rationed headlines per §19.2, itemized ledger per §18.6, player-chosen events, elections, collapse rolls, scoring + four endings, saves, and the believed-vs-true post-mortem chart. Node smoke test (`proto/smoke.mjs`) enforces engine determinism/ranges/ledger/save-restore in CI. `docs/DEPLOY.md` added (Cloudflare Pages first). §15 row marked delivered. The Phase-0 question — *is the core loop fun in 20 minutes?* — is now answerable by playtest, which is the v0.4 gate.
