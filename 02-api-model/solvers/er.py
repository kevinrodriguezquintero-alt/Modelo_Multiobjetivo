"""Epsilon-Constraint Method solver (Pareto frontier: Cost vs. Emissions)."""
import io
import contextlib
import pyomo.environ as pyo
from config import get_solver
from solvers.build_model import build_model, extract_variables, _solver_status


def _solve(solver, model):
    """Solve and capture tee output. Returns (results, log_str)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = solver.solve(model, tee=True)
    return res, buf.getvalue()


def run_er(params_obj, solver_name: str, steps: int = 5) -> dict:
    """
    Run Epsilon-Constraint Method.

    Builds payoff table first, then iterates epsilon over the emissions range
    while minimizing cost.

    Parameters
    ----------
    params_obj  : namespace with all model parameters
    solver_name : solver identifier string
    steps       : number of epsilon iterations for the Pareto frontier

    Returns
    -------
    dict with keys: method, solver, steps, payoff_table, pareto_frontier,
                    last_iteration_variables, log
    """
    solver = get_solver(solver_name)

    model = pyo.ConcreteModel()
    build_model(model, params_obj)

    log_parts = []

    def _objs():
        return {
            "cost":       pyo.value(model.Obj_Cost),
            "emissions":  pyo.value(model.Obj_Env),
            "employment": pyo.value(model.Obj_Social),
        }

    # ── PAYOFF TABLE ───────────────────────────────────────────────────────

    # 1. Minimize Cost
    model.objective = pyo.Objective(expr=model.Obj_Cost, sense=pyo.minimize)
    _, log = _solve(solver, model)
    log_parts.append("=== Payoff: Min Costo ===\n" + log)
    payoff_min_cost = _objs()

    # 2. Minimize Emissions
    model.del_component(model.objective)
    model.objective = pyo.Objective(expr=model.Obj_Env, sense=pyo.minimize)
    _, log = _solve(solver, model)
    log_parts.append("=== Payoff: Min Emisiones ===\n" + log)
    payoff_min_env = _objs()

    # 3. Maximize Social
    model.del_component(model.objective)
    model.objective = pyo.Objective(expr=model.Obj_Social, sense=pyo.maximize)
    _, log = _solve(solver, model)
    log_parts.append("=== Payoff: Max Social ===\n" + log)
    payoff_max_soc = _objs()

    payoff_table = {
        "min_cost":      payoff_min_cost,
        "min_emissions": payoff_min_env,
        "max_social":    payoff_max_soc,
    }

    # ── EPSILON LOOP ───────────────────────────────────────────────────────
    env_ideal = payoff_min_env["emissions"]
    env_nadir = max(payoff_min_cost["emissions"], payoff_max_soc["emissions"])

    step_size = (env_nadir - env_ideal) / (steps - 1) if steps > 1 else 0

    model.del_component(model.objective)
    model.objective = pyo.Objective(expr=model.Obj_Cost, sense=pyo.minimize)
    model.epsilon_constr = pyo.Constraint(expr=model.Obj_Env <= env_nadir)

    pareto_frontier = []
    last_vars = None

    for i in range(steps):
        epsilon = env_nadir - i * step_size

        model.del_component(model.epsilon_constr)
        model.epsilon_constr = pyo.Constraint(expr=model.Obj_Env <= epsilon)

        res, log = _solve(solver, model)
        status = _solver_status(res)
        log_parts.append(f"=== Iteración {i + 1} — ε={epsilon:.4f} ===\n" + log)

        entry = {
            "iteration": i + 1,
            "epsilon":   epsilon,
            "status":    status,
            "objectives": _objs() if status == "optimal" else None,
        }
        pareto_frontier.append(entry)

        if status == "optimal":
            last_vars = extract_variables(model)

    return {
        "method":                   "er",
        "solver":                   solver_name,
        "steps":                    steps,
        "payoff_table":             payoff_table,
        "pareto_frontier":          pareto_frontier,
        "last_iteration_variables": last_vars,
        "log":                      "\n".join(log_parts),
    }
