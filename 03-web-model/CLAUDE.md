# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Vanilla JS + HTML frontend for the citrus supply chain multi-objective optimizer.
Consumes the REST API from `../02-api-model` and displays LGP and ER results.

## Running

```bash
# 1. Start the API (port 8000)
cd ../02-api-model
venv/bin/uvicorn api.main:app --reload --port 8000

# 2. Serve the frontend (port 3000)
cd ../03-web-model
python3 -m http.server 3000
```

Open **http://localhost:3000**. Both processes must be running simultaneously.

## Architecture

```
index.html        # Single-page app, Tailwind CDN + Chart.js CDN
css/
└── app.css       # Custom styles (tabs, badges, tables, terminal block, spinner)
js/
├── api.js        # Thin fetch wrapper; BASE = http://localhost:8000
├── render.js     # Pure functions → HTML strings (no DOM writes)
└── app.js        # DOM wiring, event listeners, Chart.js scatter plot
```

### Module structure

- **`api.js`** exports a single `api` object with methods:
  `health`, `getSolver`, `setSolver`, `getParams`, `updateParams`, `resetParams`, `solveLgp`, `solveEr`

- **`render.js`** exports:
  - `renderSolverConfig(data, badgeEl, selectEl)` — updates solver badge + select
  - `renderParams(data)` → HTML table with editable inputs (scalar / list / dict1 / dict2)
  - `renderLgpResult(data)` → steps cards + decision variable tables + solver log terminal
  - `renderErResult(data)` → payoff table + Pareto frontier table + scatter chart placeholder + variables

- **`app.js`** initialises tabs, wires buttons, calls `api.*`, injects `render.*` output into the DOM.
  The Pareto scatter chart (`Chart.js`) is drawn by `drawErChart()` after ER HTML is injected.

### Param input kinds (used in `renderParams` / `collectParamsPatch`)

| `data-kind` | Shape | Example |
|-------------|-------|---------|
| `scalar`    | single number | `NP = 3` |
| `list`      | comma-separated ints | `I = [1, 2, 3]` |
| `dict1`     | `{key: number}` | `CP = {1: 10.5, 2: 8.0}` |
| `dict2`     | `[{k1, k2, value}]` | `TC = [{i:1, j:2, value:5.0}]` |

### Tabs

Outer tabs: `config` · `params` · `lgp` · `er` (URL param `?tab=` persists state).
Inner tabs (injected dynamically): `resultado` / `logs` — wired via event delegation in `initInnerTabs()`.

## API Contract

The frontend expects these endpoints on `http://localhost:8000`:

| Method | Path | Used by |
|--------|------|---------|
| GET | `/config/solver` | Config tab on load |
| PUT | `/config/solver` | "Cambiar solver" button |
| GET | `/params` | Params tab on load |
| PUT | `/params` | "Guardar cambios" button |
| POST | `/params/reset` | "Restaurar defaults" button |
| POST | `/solve/lgp` | "Ejecutar LGP" button |
| POST | `/solve/er` | "Ejecutar ER" button (body: `{"steps": N}`) |

## No build step

Pure ES modules loaded directly by the browser — no bundler, no npm.
Do not introduce build tools or package managers without explicit instruction.
