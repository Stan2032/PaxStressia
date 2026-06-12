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
for (const f of ["nodes", "edges", "factions", "initiatives", "events", "constants"]) {
  rules[f] = JSON.parse(readFileSync(new URL(`../rules/${f}.json`, import.meta.url), "utf8"));
}

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

if (failures) { console.error(failures + " smoke failures"); process.exit(1); }
console.log("proto smoke ok — determinism, ranges, ledger, save/restore, scoring");
