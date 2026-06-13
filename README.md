# PaxStressia

*A turn-based strategy game about being the world police in a world that keeps score.*

**Pax at the cost of stress** — the "Pax …ia" eras, with the price in the name. Being lied about without dealing in lies yourself; or trying your best to. *(Title decided at v0.2.2; formerly working title MANDATE.)*

You lead a real-world democracy holding the line against insurgencies that grow, network, and — left untended — capture states and weld them into authoritarian blocs. Your constraints are your own: voters, allies, law, and a free press. Every lever that wins faster abroad corrodes something at home. **Can you hold the line abroad without breaking the thing you're defending?**

**Status: v0.5** — Scenario 1 "The Arc" (Sahel 2012–2026) is calibrated to history (a passive player reproduces the record on 10/10 seeds) and playable in any browser.

**▶ Play it:** once GitHub Pages is enabled (Settings → Pages → Source: **GitHub Actions**, one time), the game is live at **https://stan2032.github.io/PaxStressia/** — no install. Locally instead: `python3 -m http.server 8080` from the repo root → `http://localhost:8080/proto/` (this needs the repo cloned onto the machine running the server). Other hosts: [`docs/DEPLOY.md`](docs/DEPLOY.md).

Underneath: JSON rules + schemas, headless Python sim, **three enforced design-thesis tests**, CI with a Monte Carlo + history-calibration harness and a prototype engine smoke test. Roadmap: [`docs/DESIGN.md`](docs/DESIGN.md) §15.

## Read first

| Doc | What it is |
|---|---|
| [`docs/DESIGN.md`](docs/DESIGN.md) | **Canonical design document** (cumulative; §18 is the sim spec the code implements) |
| [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md) | Full project handoff: governing prompt, research record, every decision and the alternatives it beat |

## Layout

```
rules/        THE source of truth — all game rules as JSON (schemas in rules/schema/)
sim/          headless simulation core (stdlib-only: runs in bare Termux Python)
tests/        pytest — schemas, determinism, ledger integrity, and the design-thesis suite
harness/      Monte Carlo runner → runs.json + balance.png
proto/        Phase-0 web prototype (lands v0.3)
```

## Quickstart (Termux-friendly)

```sh
# the sim itself needs nothing beyond the standard library:
python -c "from sim import Engine; e = Engine(seed=42); e.run(60); print(e.score())"

# dev tools (tests + lint) and the optional plot dependency:
pip install -e ".[dev,harness]"
pytest -q
python harness/run.py --runs 10 --turns 60 --policy passive --out artifacts
```

## The thesis is a test suite

`tests/test_thesis.py` asserts the design's claims as regression tests — passive play should approximately reproduce the Sahel's 2012–2026 history; pure force loses Local legitimacy; pure development loses to momentum; emergency powers tempt and are scored. They are `xfail` until calibration (v0.5); once green, a balance change that breaks the thesis breaks CI.

## License

**PolyForm Noncommercial 1.0.0** — source-available; read, run, mod, and share for any noncommercial purpose; commercial rights reserved (so the Steam/itch path stays open). Full terms and rationale in [`LICENSE.md`](LICENSE.md). Reversible toward more-open later.
