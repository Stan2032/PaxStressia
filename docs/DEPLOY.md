# Deploying PaxStressia (the web prototype) — v0.3

The proto (`proto/index.html`) is a static single file; anything that serves files can host it. Distribution order is web-first by design (DESIGN.md §2). Three paths, phone-friendliest first.

## A. Cloudflare Pages via GitHub (recommended — no CLI, auto-deploys, free)

1. **dash.cloudflare.com** → sign in (free plan is fine) → **Workers & Pages → Create → Pages → Connect to Git**.
2. Authorize GitHub and pick **Stan2032/PaxStressia**.
3. Build settings:
   - **Production branch:** `main`
   - **Framework preset:** None
   - **Build command:** *(leave empty)* — the rules snapshot is committed and CI guarantees it's fresh. (Optional belt-and-braces: `python3 proto/build.py`.)
   - **Build output directory:** `/` (the repo root)
4. **Save and Deploy.** You get `https://<project-name>.pages.dev`; the game lives at **`/proto/`**.

Why repo root as output: the proto fetches `../rules/*.json` **live** when served — so the deployed game reads the same JSON source of truth as the sim, and a balance change merged to `main` is live on the next auto-deploy. Every push to `main` redeploys; **every PR gets its own preview URL** — free playtest links per change.

Notes:
- Serving the repo root publishes *everything* in it (docs included). The repo is public anyway; just be aware.
- No LICENSE yet (open question #5): deployed ≠ licensed. Default copyright still applies.
- Free tier: unlimited static requests, 500 builds/month — far beyond our needs.
- Custom domain later: Pages project → **Custom domains** (Cloudflare walks you through DNS).

## B. Wrangler from Termux (direct upload, no git integration)

```sh
npm install -g wrangler
wrangler login
wrangler pages deploy . --project-name paxstressia
```

Deploys the current working tree as-is. Useful for one-off experiments; path A is better for the standing site.

## C. GitHub Pages (zero new accounts)

Repo **Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)`**.
Game at `https://stan2032.github.io/PaxStressia/proto/`. Slower deploys than Cloudflare, no PR previews on the free path, but zero setup beyond the toggle.

## Local (Termux, day-to-day dev)

```sh
python3 -m http.server 8080     # from the repo root
# phone browser → http://localhost:8080/proto/
```

Served this way the proto uses the live `rules/*.json`; opened as a bare `file://` it falls back to the embedded snapshot (`proto/build.py` keeps that snapshot in sync; CI fails if it drifts).
