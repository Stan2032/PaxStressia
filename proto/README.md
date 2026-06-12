# proto/ — Phase 0 web prototype (landed at v0.3)

`index.html` — the single-file greybox playable of *Sahel-lite*: the legitimacy
triangle, insurgent growth/entrenchment/visibility, fog-of-estimates with
confidence bands (§19.5: fog ships in the greybox), all 9 initiatives with
backfires, events with player choices, elections and Mandate, collapse rolls,
scoring with the four endings, localStorage saves, and the believed-vs-true
post-mortem chart at game end.

The question it exists to answer (DESIGN.md §13.3 Phase 0):
**is the core loop fun in 20 minutes?**

## Run it

```sh
python3 -m http.server 8080      # from the repo root
# phone browser → http://localhost:8080/proto/
```

Served over http it fetches `../rules/*.json` live (single source of truth);
opened as `file://` it uses the embedded snapshot. Deployment: `docs/DEPLOY.md`.

## Companions (the playable stays one file)

- `build.py` — injects the rules snapshot into `index.html`; `--check` runs in
  CI and fails if the snapshot drifted from `rules/`.
- `smoke.mjs` — Node smoke test; extracts the DOM-free engine block and drives
  full headless games (determinism, ranges, ledger itemization, save/restore).

The JS engine is a port of `sim/` against the same DESIGN.md §18 spec and the
same JSON rules. It is *self-consistently* deterministic, not bit-compatible
with the Python sim — the rules data is the shared truth, not the RNG stream.
