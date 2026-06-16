// Headless board preview (dev tool): drive the proto's JS engine, render the map
// the way index.html's renderMap() does, and write an SVG + PNG so the visual
// language can be reviewed without a browser. Mirrors the proto's encoding —
// run after changing renderMap to confirm what the screen says at a glance.
//   node proto/preview.mjs [scenario] [seed] [turns]   (default: grand 4 36)
import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

const HTML = readFileSync(new URL("./index.html", import.meta.url), "utf8");
const engine = HTML.match(/<script id="engine-js">([\s\S]*?)<\/script>/);
const mod = { exports: {} };
new Function("module", engine[1])(mod);
const PaxEngine = mod.exports;

// pull the map layout straight from the proto so the preview can't drift from it
const POS = {};
for (const m of HTML.matchAll(/([a-z0-9_]+):\s*\[(\d+),\s*(\d+)\]/g))
  POS[m[1]] = [Number(m[2]), Number(m[3])];

const [scenario = "grand", seed = "4", turns = "36"] = process.argv.slice(2);
const R = (f) => JSON.parse(readFileSync(new URL(`../rules/${f}.json`, import.meta.url), "utf8"));
const opt = (f) => { try { return R(f); } catch { return null; } };  // absent scenario files fall through
const rules = {};
for (const f of ["nodes", "edges", "factions", "initiatives", "events", "constants", "patrons"])
  rules[f] = R(f);
if (scenario !== "base") {
  for (const f of ["nodes", "edges", "factions", "events"]) {
    const o = opt(`scenarios/${scenario}/${f}`); if (o) rules[f] = o;
  }
  const sc = opt(`scenarios/${scenario}/constants`);
  if (sc) rules.constants = Object.assign({}, R("constants"), sc);
}

const g = PaxEngine.Game(rules, Number(seed));
// stand up a couple of commands early so the posture shows on the board
const seeds = scenario === "grand" ? [["establish_command", "mali"], ["establish_command", "afghanistan"]] : [];
for (let t = 0; t < Number(turns); t++) {
  let r = g.endTurn(t < seeds.length ? [{ initiative: seeds[t][0], node: seeds[t][1] }] : []);
  if (r.phase === "event") g.resolveEvent(0);
}

const GOV = { civilian: "#33691e", junta: "#b71c1c", emirate: "#4a148c", failed: "#37474f" };
const commands = g.state.commands || [];
const dense = g.nodesSorted().length > 20;
let body = "";
for (const e of g.state.edges) {
  if (!POS[e.a] || !POS[e.b]) continue;
  const [ax, ay] = POS[e.a], [bx, by] = POS[e.b];
  const smug = e.types.includes("smuggling");
  const dash = smug ? ' stroke-dasharray="5 4"' : "";
  body += `<line x1="${ax}" y1="${ay}" x2="${bx}" y2="${by}" stroke="${smug ? "#5d4037" : "#3a4750"}" stroke-width="1.5"${dash}/>`;
}
for (const n of g.nodesSorted()) {
  const [x, y] = POS[n.id] || [50, 50];
  const r = 2.2 + Math.min(2.8, Math.log10(Math.max(10, n.population_k)) * 0.55);
  const est = g.state.estimates[n.id] || { factions: {} };
  const tot = Object.values(est.factions || {}).reduce((s, f) => s + f.s, 0);
  const heatW = Math.min(3.5, tot / 20);
  const right = x > 62, lx = right ? x - r - 1.5 : x + r + 1.5, anchor = right ? "end" : "start";
  let label = n.name.split(/[ /]/)[0]; if (label.length > 9) label = label.slice(0, 8) + "…";
  body += "<g>";
  if (tot > 12) body += `<circle cx="${x}" cy="${y}" r="${(r + 1).toFixed(1)}" fill="none" stroke="#ef5350" stroke-width="${heatW.toFixed(1)}" opacity="0.85"/>`;
  body += `<circle cx="${x}" cy="${y}" r="${r}" fill="${GOV[n.government]}" stroke="#000" stroke-width="1.2"/>`;
  if (n.capital && !dense) body += `<text x="${x - 1.8}" y="${y - r - 1}" fill="#ffb300" font-size="4.5">★</text>`;
  if (commands.includes(n.theater)) {
    const fx = (x + r * 0.7).toFixed(1), fy = (y - r - 2.6).toFixed(1);
    body += `<path d="M${fx} ${fy} v3.4 M${fx} ${fy} l2.2 0.8 -2.2 0.8" stroke="#26a69a" stroke-width="0.7" fill="none"/>`;
  }
  if ((n.resources || []).includes("oil"))
    body += `<circle cx="${(x + r * 0.8).toFixed(1)}" cy="${(y + r * 0.8).toFixed(1)}" r="0.9" fill="#111"/>`;
  if (!dense) body += `<text x="${lx}" y="${y - 0.3}" text-anchor="${anchor}" fill="#cfd8dc" font-size="4">${label}</text>`;
  body += "</g>";
}
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="1000" height="1000">` +
  `<rect width="100" height="100" fill="#14181d"/>${body}</svg>`;
const out = new URL("./preview.svg", import.meta.url);
writeFileSync(out, svg);
const png = new URL("./preview.png", import.meta.url);
execFileSync("cairosvg", [out.pathname, "-o", png.pathname]);
const juntas = g.state.commands;
console.log(`rendered ${scenario} seed ${seed} @${turns}t -> proto/preview.png ` +
  `(${g.nodesSorted().length} nodes, commands: ${commands.join(", ") || "none"})`);
