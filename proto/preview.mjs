// Headless board preview (dev tool): drive the proto's JS engine, render the map
// the way index.html's renderMap() does, and write an SVG + PNG so the visual
// language can be reviewed without a browser. Mirrors the proto's encoding —
// run after changing renderMap to confirm what the screen says at a glance.
//   node proto/preview.mjs [scenario] [seed] [turns] [viewBox]
//   e.g. node proto/preview.mjs grand 4 40 "44 26 36 36"   (a zoomed-in theatre)
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

const [scenario = "grand", seed = "4", turns = "36", vb = "0 0 100 100"] = process.argv.slice(2);
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
const showLabels = !dense || Number(vb.split(/[ ,]+/)[2]) < 46;  // names return when zoomed in

function convexHull(pts) {
  if (pts.length < 3) return pts.slice();
  const p = pts.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lo = [], up = [];
  for (const q of p) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], q) <= 0) lo.pop(); lo.push(q); }
  for (let i = p.length - 1; i >= 0; i--) { const q = p[i]; while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], q) <= 0) up.pop(); up.push(q); }
  lo.pop(); up.pop(); return lo.concat(up);
}
let back = '<defs><radialGradient id="ocean" cx="50%" cy="40%" r="78%">' +
  '<stop offset="0%" stop-color="#16323f"/><stop offset="100%" stop-color="#0b1014"/>' +
  '</radialGradient></defs><rect x="0" y="0" width="100" height="100" fill="url(#ocean)"/>';
for (let gl = 10; gl < 100; gl += 10)
  back += `<line x1="${gl}" y1="0" x2="${gl}" y2="100" stroke="#33444e" stroke-width="0.25" opacity="0.5"/>` +
    `<line x1="0" y1="${gl}" x2="100" y2="${gl}" stroke="#33444e" stroke-width="0.25" opacity="0.5"/>`;
const groups = {};
for (const n of g.nodesSorted()) {
  const [x, y] = POS[n.id] || [50, 50];
  (groups[n.theater || "_region"] = groups[n.theater || "_region"] || []).push([x, y]);
}
const LAND = 'fill="#36493d" stroke="#3f5446" stroke-width="5" stroke-linejoin="round" opacity="0.95"';
for (const key of Object.keys(groups).sort()) {
  const pts = groups[key];
  const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length, cy = pts.reduce((s, p) => s + p[1], 0) / pts.length;
  if (pts.length < 3) back += `<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="6.5" ${LAND}/>`;
  else {
    const hull = convexHull(pts).map(([x, y]) => {
      const dx = x - cx, dy = y - cy, m = Math.hypot(dx, dy) || 1;
      return `${(x + dx / m * 3).toFixed(1)},${(y + dy / m * 3).toFixed(1)}`;
    });
    back += `<polygon points="${hull.join(" ")}" ${LAND}/>`;
  }
  if (dense && key !== "_region")
    back += `<text x="${cx.toFixed(1)}" y="${(cy - 7).toFixed(1)}" text-anchor="middle" fill="#5a6b72" font-size="2.6">${key.replace(/_/g, " ").toUpperCase()}</text>`;
}
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
  const r = 1.9 + Math.min(2.3, Math.log10(Math.max(10, n.population_k)) * 0.5);
  const est = g.state.estimates[n.id] || { factions: {} };
  const tot = Object.values(est.factions || {}).reduce((s, f) => s + f.s, 0);
  const heatW = Math.min(2.6, tot / 26);
  const right = x > 62, lx = right ? x - r - 1.5 : x + r + 1.5, anchor = right ? "end" : "start";
  let label = n.name.split(/[ /]/)[0]; if (label.length > 9) label = label.slice(0, 8) + "…";
  body += "<g>";
  if (tot > 12) body += `<circle cx="${x}" cy="${y}" r="${(r + 0.8).toFixed(1)}" fill="none" stroke="#ef5350" stroke-width="${heatW.toFixed(1)}" opacity="0.7"/>`;
  body += `<circle cx="${x}" cy="${y}" r="${r}" fill="${GOV[n.government]}" stroke="#000" stroke-width="1.2"/>`;
  if (n.capital && showLabels) body += `<text x="${x - 1.8}" y="${y - r - 1}" fill="#ffb300" font-size="4.5">★</text>`;
  if (commands.includes(n.theater)) {
    const fx = (x + r * 0.7).toFixed(1), fy = (y - r - 2.6).toFixed(1);
    body += `<path d="M${fx} ${fy} v3.4 M${fx} ${fy} l2.2 0.8 -2.2 0.8" stroke="#26a69a" stroke-width="0.7" fill="none"/>`;
  }
  if ((n.resources || []).includes("oil"))
    body += `<circle cx="${(x + r * 0.8).toFixed(1)}" cy="${(y + r * 0.8).toFixed(1)}" r="0.9" fill="#111"/>`;
  if (showLabels) body += `<text x="${lx}" y="${y - 0.3}" text-anchor="${anchor}" fill="#cfd8dc" font-size="4">${label}</text>`;
  body += "</g>";
}
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}" width="1000" height="1000">` +
  `${back}${body}</svg>`;
const out = new URL("./preview.svg", import.meta.url);
writeFileSync(out, svg);
const png = new URL("./preview.png", import.meta.url);
execFileSync("cairosvg", [out.pathname, "-o", png.pathname]);
const juntas = g.state.commands;
console.log(`rendered ${scenario} seed ${seed} @${turns}t -> proto/preview.png ` +
  `(${g.nodesSorted().length} nodes, commands: ${commands.join(", ") || "none"})`);
