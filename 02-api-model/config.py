import os
from dotenv import load_dotenv
import pyomo.environ as pyo

load_dotenv()

SOLVERS = {
    "cplex":  lambda: pyo.SolverFactory("cplex", solver_io="nl", executable="cplex"),
    "highs":  lambda: pyo.SolverFactory("appsi_highs"),
    "glpk":   lambda: pyo.SolverFactory("glpk"),
    "cbc":    lambda: pyo.SolverFactory("cbc"),
}


def get_solver(name: str = None):
    if name is None:
        name = os.getenv("SOLVER", "highs").lower()
    name = name.lower()
    if name not in SOLVERS:
        raise ValueError(f"Solver '{name}' no reconocido. Opciones: {list(SOLVERS)}")
    return SOLVERS[name]()
