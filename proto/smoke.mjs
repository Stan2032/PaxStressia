// Headless smoke test for the proto's JS engine (run by CI: `node proto/smoke.mjs`).
// Extracts the DOM-free engine block from index.html and drives full games:
// determinism, gauge/presence ranges, event resolution, scoring, save/restore.
import { readFileSync } from "node:fs";

const html = readFileSync(new URL("./index.html", import.meta.url), "utf8");
const match = html.match(/<script id="engine-js">([\s\S]*?)<\/script>/);
if (!match) { console.error("engine-js block not found"); process.exit(1); }
const mod = { exports: {} };
new Function("module", match[1])(mod);
const PaxEngine = mod.exports;

const rules = {};
for (const f of ["nodes", "edges", "factions", "initiatives", "events", "constants", "patrons"]) {
  rules[f] = JSON.parse(readFileSync(new URL(`../rules/${f}.json`, import.meta.url), "utf8"));
}
// Arc scenario, merged the way the UI and sim/world.py merge (§18.9)
const arcRules = Object.assign({}, rules);
for (const f of ["nodes", "edges", "factions", "events"]) {
  arcRules[f] = JSON.parse(readFileSync(
    new URL(`../rules/scenarios/sahel_arc/${f}.json`, import.meta.url), "utf8"));
}
// Grand scenario: replace nodes/edges/factions, MERGE constants (§18.9, §21).
const grandRules = Object.assign({}, rules);
for (const f of ["nodes", "edges", "factions"]) {
  grandRules[f] = JSON.parse(readFileSync(
    new URL(`../rules/scenarios/grand/${f}.json`, import.meta.url), "utf8"));
}
grandRules.constants = Object.assign({}, rules.constants, JSON.parse(readFileSync(
  new URL("../rules/scenarios/grand/constants.json", import.meta.url), "utf8")));

let failures = 0;
const check = (cond, msg) => {
  if (!cond) { failures += 1; console.error("FAIL:", msg); }
};

function run(seed, turns, ordersFor) {
  const g = PaxEngine.Game(rules, seed);
  for (let t = 0; t < turns; t++) {
    let r = g.endTurn(ordersFor ? ordersFor(g) : []);
    if (r.phase === "event") r = g.resolveEvent(0);
  }
  return g;
}
const kinetic = (g) => [
  { initiative: "presence_patrols", node: "mopti" },
  { initiative: "drone_strike", node: "gao" },
  { initiative: "un_mandate", node: null },
];

// determinism: same seed + same orders => identical serialized state
const a = run(7, 60, kinetic), b = run(7, 60, kinetic);
check(a.serialize() === b.serialize(), "same seed must give identical state");
const c = run(8, 60, kinetic);
check(a.serialize() !== c.serialize(), "different seeds must diverge");

// ranges + report shape over passive and kinetic runs
for (const g of [run(3, 60), a]) {
  const p = g.state.player;
  check(p.domestic >= 0 && p.domestic <= 100, "domestic in range");
  check(p.international >= 0 && p.international <= 100, "international in range");
  for (const n of g.nodesSorted()) {
    check(n.local >= 0 && n.local <= 100, "local in range @" + n.id);
    for (const f of Object.keys(n.presence)) {
      const pr = n.presence[f];
      check(pr.s >= 0 && pr.s <= 100 && pr.e >= 0 && pr.e <= 100 &&
        pr.v >= 0 && pr.v <= 100, "presence in range @" + n.id);
    }
  }
  check(g.state.hist.truth.length === 60, "one history sample per turn");
  const s = g.score();
  check(Number.isFinite(s.final), "score is finite");
  check(typeof g.ending().name === "string", "ending resolves");
}

// passive player pays no blood and no drift (mirrors the Python test)
const passive = run(4, 60);
check(passive.state.player.casualties === 0, "passive: no casualties");
check(passive.state.player.drift === 0, "passive: no drift");

// ledger itemization: per-turn gauge movement equals the sum of its entries
{
  const g = PaxEngine.Game(rules, 11);
  for (let t = 0; t < 30; t++) {
    const before = g.state.player.domestic, turn = g.state.turn;
    let r = g.endTurn(kinetic(g));
    if (r.phase === "event") r = g.resolveEvent(0);
    const sum = g.state.ledger.filter((e) => e.turn === turn && e.gauge === "domestic")
      .reduce((s, e) => s + e.delta, 0);
    check(Math.abs((g.state.player.domestic - before) - sum) < 1e-6,
      "domestic ledger itemization @turn " + turn);
  }
}

// save/restore round-trip resumes identically
{
  const g1 = run(9, 20, kinetic);
  const blob = g1.serialize();
  const g2 = PaxEngine.Game(rules, 0).restore(blob);
  check(g2.serialize() === blob, "restore round-trips");
  for (let t = 0; t < 10; t++) {
    let r1 = g1.endTurn(kinetic(g1)); if (r1.phase === "event") r1 = g1.resolveEvent(0);
    let r2 = g2.endTurn(kinetic(g2)); if (r2.phase === "event") r2 = g2.resolveEvent(0);
  }
  check(g1.serialize() === g2.serialize(), "restored game evolves identically");
}

// the Arc (v0.4): full-horizon determinism, ranges, once-beats, spread
{
  const runArc = (seed) => {
    const g = PaxEngine.Game(arcRules, seed);
    for (let t = 0; t < 168; t++) {
      let r = g.endTurn([]);
      if (r.phase === "event") r = g.resolveEvent(0);
    }
    return g;
  };
  const a1 = runArc(5), a2 = runArc(5);
  check(a1.serialize() === a2.serialize(), "arc: same seed identical");
  for (const n of a1.nodesSorted()) {
    for (const f of Object.keys(n.presence)) {
      const p = n.presence[f];
      check(p.s >= 0 && p.s <= 100 && p.e >= 0 && p.e <= 100, "arc presence range @" + n.id);
    }
  }
  const onceIds = arcRules.events.filter((c) => c.once).map((c) => c.id);
  for (const id of onceIds)
    check(a1.state.fired.filter((x) => x === id).length <= 1, "arc once-beat " + id);
  const emptyAtStart = arcRules.nodes.filter((n) =>
    !Object.keys(n.presence || {}).length).map((n) => n.id);
  const ignited = emptyAtStart.filter((id) =>
    Object.values(a1.state.nodes[id].presence).some((p) => p.s > 5));
  check(ignited.length > 0, "arc: spread should ignite at least one empty region");
}

// Transparency Dial (v0.6): driving the "bury" branch must register leak clocks,
// stay deterministic, and keep gauges in range as leaks resolve.
{
  const runBury = (seed) => {
    const g = PaxEngine.Game(arcRules, seed);
    let everBuried = false;
    for (let t = 0; t < 120; t++) {
      let r = g.endTurn([{ initiative: "partnered_raids", node: "mopti" }]);
      if (r.phase === "event") r = g.resolveEvent(1);  // prefer the suppress/decline branch
      if (g.state.player.suppressClocks.length) everBuried = true;
    }
    return { g, everBuried };
  };
  const a = runBury(2), b = runBury(2);
  check(a.g.serialize() === b.g.serialize(), "dial: same seed identical with bury branch");
  check(Array.isArray(a.g.state.player.suppressClocks), "dial: suppressClocks present");
  for (const p of [a.g.state.player]) {
    check(p.domestic >= 0 && p.domestic <= 100, "dial: domestic in range");
    check(p.international >= 0 && p.international <= 100, "dial: international in range");
  }
}

// v0.7 endgame systems: exposure builds, blocs/exposure serialize, determinism holds.
{
  const runExpose = (seed) => {
    const g = PaxEngine.Game(arcRules, seed);
    for (let t = 0; t < 120; t++) {
      let r = g.endTurn([
        { initiative: "fund_research", node: "bamako" },
        { initiative: "negotiate_settlement", node: "gao" },
      ]);
      if (r.phase === "event") r = g.resolveEvent(0);
    }
    return g;
  };
  const a = runExpose(1), b = runExpose(1);
  check(a.serialize() === b.serialize(), "v0.7: same seed identical with exposure/negotiate");
  check(a.serialize().includes('"exposure"'), "v0.7: exposure serialized");
  check(a.serialize().includes('"blocs"'), "v0.7: blocs serialized");
  check((a.state.exposure.ML || 0) > 10, "v0.7: funded research builds exposure on ML");
  for (const c of Object.keys(a.state.exposure))
    check(a.state.exposure[c] >= 0 && a.state.exposure[c] <= 100, "v0.7: exposure in range " + c);
}

// Grand mode (§21): world-scale board + global norms ripple, both deterministic.
{
  const runGrand = (seed, kinetic) => {
    const g = PaxEngine.Game(grandRules, seed);
    for (let t = 0; t < 60; t++) {
      const orders = kinetic ? [{ initiative: "drone_strike", node: "afghanistan" },
        { initiative: "presence_patrols", node: "somalia" }] : [];
      let r = g.endTurn(orders);
      if (r.phase === "event") r = g.resolveEvent(0);
    }
    return g;
  };
  const a = runGrand(4, true), b = runGrand(4, true);
  check(a.serialize() === b.serialize(), "grand: same seed identical");
  check(Object.keys(a.state.nodes).length >= 36, "grand: the world (v0.12: ~40 nations)");
  check(a.serialize().includes('"norms"'), "grand: norms serialized");
  check(a.state.norms.kinetic > 60, "grand: kinetic play raises the world kinetic norm");
  const passive = runGrand(4, false);
  check(Math.abs(passive.state.norms.kinetic - 50) < 0.01,
    "grand: passive leaves norms neutral");
  for (const n of a.nodesSorted()) for (const f of Object.keys(n.presence))
    check(n.presence[f].s >= 0 && n.presence[f].s <= 100, "grand: presence in range @" + n.id);
  // v0.11 markets + multi-patron rivalry (serialized, deterministic, ripples move)
  check(a.serialize().includes('"markets"') && a.serialize().includes('"rivalry"'),
    "grand: markets/rivalry serialized");
  check(passive.state.markets.arms > 55, "grand: conflict heats the arms market");
  const winners = Object.values(passive.state.patronStrength).filter((v) => v > 5).length;
  check(winners >= 1, "grand: the patron contest produces winners");
  // single-theater gating: markets stay neutral on the arc
  const arc = PaxEngine.Game(arcRules, 2);
  for (let t = 0; t < 40; t++) { const r = arc.endTurn([{ initiative: "drone_strike", node: "gao" }]);
    if (r.phase === "event") arc.resolveEvent(0); }
  check(arc.state.markets.arms === 50 && arc.state.rivalry === 0,
    "single-theater: markets/rivalry dormant");
}

if (failures) { console.error(failures + " smoke failures"); process.exit(1); }
console.log("proto smoke ok — determinism, ranges, ledger, save/restore, scoring, arc, dial, endgame, grand");
