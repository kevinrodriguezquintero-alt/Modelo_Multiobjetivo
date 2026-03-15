# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-objective optimization of a sustainable three-tier fruit (citrus) supply chain. The model minimizes cost and emissions while maximizing employment across Producers → Intermediaries → Retailers.

Exposed as a **REST API** (FastAPI) so a frontend can consume results as JSON.

## Running the API

```bash
venv/bin/uvicorn api.main:app --reload --port 8000
```

Interactive docs available at `http://localhost:8000/docs`.

## Solver Configuration

Set the solver in `.env`:
```
SOLVER=highs   # Options: highs, cplex, glpk, cbc
```

`config.py` exposes `get_solver(name=None)` — uses the argument if provided, otherwise falls back to the env var. CPLEX requires the ASL interface (`solver_io="nl"`).

## Architecture

```
api/
├── main.py          # FastAPI app, CORS, startup
├── state.py         # AppState singleton — active solver + in-memory params
└── routers/
    ├── config.py    # GET/PUT /config/solver
    ├── params.py    # GET /params, PUT /params, POST /params/reset
    └── solve.py     # POST /solve/lgp, POST /solve/er

solvers/
├── build_model.py   # Shared Pyomo model builder (sets, params, vars, constraints, expressions)
├── lgp.py           # run_lgp(params_obj, solver_name) → dict
└── er.py            # run_er(params_obj, solver_name, steps) → dict

data/
└── params.py        # Default parameter values (source of truth — never modified at runtime)

config.py            # get_solver(name) + SOLVERS dict
```

### Params lifecycle

`data/params.py` is loaded into `AppState.params` (in-memory dict) on startup.
`PUT /params` edits that dict. `POST /params/reset` reloads from `data/params.py`.
The file itself is never written to.

### Pyomo model

All models are built with **Pyomo** (`pyomo.environ`). The supply chain has:
- **Sets:** `I` (producers), `U` (producer variants), `J` (intermediaries), `K` (retailers)
- **Decision variables:** `X`/`Y` (product flows), `Z`/`ZZ` (trips), `W` (hectares), `S`/`SS` (staff), `B` (binary producer selection)
- **Three objectives** (expressions on `model`):
  1. `Obj_Cost` — sum of production, processing, transport, labor, and damage costs
  2. `Obj_Env` — `∑ Z_ij · DPI_ij · IT_j + ∑ ZZ_jk · DID_jk · IT_j` — **currently using placeholder 1.0 values**
  3. `Obj_Social` — `∑ S_j + ∑ SS_k` (total employment)

`solvers/lgp.py` fixes each solved objective as a constraint before optimizing the next priority (tolerance `1e-4`).

`solvers/er.py` computes a payoff table first, then iterates epsilon over the emissions range to build the Pareto frontier.

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/health` | Health check |
| GET | `/config/solver` | Active solver and available options |
| PUT | `/config/solver` | Change solver: `{"solver": "highs"}` |
| GET | `/params` | All current parameters as JSON |
| PUT | `/params` | Partial parameter update (same JSON format) |
| POST | `/params/reset` | Restore defaults from `data/params.py` |
| POST | `/solve/lgp` | Run LGP → structured JSON |
| POST | `/solve/er` | Run ER → `{"steps": 5}` → Pareto frontier JSON |

## Pending Work

- Replace placeholder `1.0` values for environmental parameters `DPI`, `DID`, `IT` in `data/params.py` with real empirical data.
