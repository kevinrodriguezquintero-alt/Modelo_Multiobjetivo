"""Lexicographic Goal Programming solver."""
import io
import contextlib
import pyomo.environ as pyo
from config import get_solver
from solvers.build_model import build_model, extract_variables, _solver_status

TOLERANCE = 1e-4


def _solve(solver, model):
    """Solve and capture tee output. Returns (results, log_str)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = solver.solve(model, tee=True)
    return res, buf.getvalue()


def run_lgp(params_obj, solver_name: str) -> dict:
    """
    Run Lexicographic Goal Programming.

    Priority order: Cost → Emissions → Employment (maximize)

    Parameters
    ----------
    params_obj  : namespace with all model parameters
    solver_name : solver identifier string

    Returns
    -------
    dict with keys: method, solver, status, steps, objectives, variables, logs
    """
    solver = get_solver(solver_name)

    model = pyo.ConcreteModel()
    build_model(model, params_obj)

    steps = []

    def _objs():
        return {
            "cost":       pyo.value(model.Obj_Cost),
            "emissions":  pyo.value(model.Obj_Env),
            "employment": pyo.value(model.Obj_Social),
        }

    # ── STEP 1: Minimize Cost ──────────────────────────────────────────────
    model.objective = pyo.Objective(expr=model.Obj_Cost, sense=pyo.minimize)
    res, log1 = _solve(solver, model)
    status1 = _solver_status(res)

    step1 = {"step": 1, "priority": "Costo", "status": status1, "objectives": _objs(), "log": log1}
    steps.append(step1)

    if status1 != "optimal":
        return _error_response(solver_name, steps, "infeasible_step1")

    val_cost = pyo.value(model.Obj_Cost)
    model.cons_priority1 = pyo.Constraint(
        expr=model.Obj_Cost <= val_cost * (1 + TOLERANCE)
    )

    # ── STEP 2: Minimize Emissions ─────────────────────────────────────────
    model.del_component(model.objective)
    model.objective = pyo.Objective(expr=model.Obj_Env, sense=pyo.minimize)
    res, log2 = _solve(solver, model)
    status2 = _solver_status(res)

    step2 = {"step": 2, "priority": "Emisiones", "status": status2, "objectives": _objs(), "log": log2}
    steps.append(step2)

    if status2 != "optimal":
        return _error_response(solver_name, steps, "infeasible_step2")

    val_env = pyo.value(model.Obj_Env)
    model.cons_priority2 = pyo.Constraint(
        expr=model.Obj_Env <= val_env * (1 + TOLERANCE)
    )

    # ── STEP 3: Maximize Employment ────────────────────────────────────────
    model.del_component(model.objective)
    model.objective = pyo.Objective(expr=model.Obj_Social, sense=pyo.maximize)
    res, log3 = _solve(solver, model)
    status3 = _solver_status(res)

    final_objs = _objs()
    step3 = {"step": 3, "priority": "Social", "status": status3, "objectives": final_objs, "log": log3}
    steps.append(step3)

    return {
        "method":     "lgp",
        "solver":     solver_name,
        "status":     status3,
        "steps":      steps,
        "objectives": final_objs,
        "variables":  extract_variables(model),
    }


def _error_response(solver_name, steps, status):
    return {
        "method":     "lgp",
        "solver":     solver_name,
        "status":     status,
        "steps":      steps,
        "objectives": None,
        "variables":  None,
    }
