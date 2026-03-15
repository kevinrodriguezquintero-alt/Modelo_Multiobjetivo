"""Singleton application state: active solver + in-memory params."""
import importlib
import os
from types import SimpleNamespace
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Param metadata: name -> (kind, index_keys_or_None)
#   kind: "scalar" | "list" | "dict1" | "dict2"
# ---------------------------------------------------------------------------
PARAM_SCHEMA: dict[str, tuple] = {
    "PRODUCERS":         ("list",   None),
    "INTERMEDIARIES":    ("list",   None),
    "RETAILERS":         ("list",   None),
    "PRODUCER_VARIANTS": ("list",   None),
    # scalars
    "RB":  ("scalar", None),
    "IT":  ("scalar", None),
    # single-index dicts
    "RA":  ("dict1", None),
    "RC":  ("dict1", None),
    "RD":  ("dict1", None),
    "CA":  ("dict1", None),
    "CB":  ("dict1", None),
    "CP":  ("dict1", None),
    "CI":  ("dict1", None),
    "CD":  ("dict1", None),
    "CN":  ("dict1", None),
    "CH":  ("dict1", None),
    "CHI": ("dict1", None),
    "CR":  ("dict1", None),
    "DI":  ("dict1", None),
    "DD":  ("dict1", None),
    "CV":  ("dict1", None),
    "CMO": ("dict1", None),
    "H":   ("dict1", None),
    # two-index dicts  (keys: [first_index_name, second_index_name])
    "CT":  ("dict2", ["i", "j"]),
    "CTT": ("dict2", ["j", "k"]),
    "CDA": ("dict2", ["i", "j"]),
    "CDF": ("dict2", ["j", "k"]),
    "P":   ("dict2", ["i", "j"]),
    "PP":  ("dict2", ["j", "k"]),
    "DPI": ("dict2", ["i", "j"]),
    "DID": ("dict2", ["j", "k"]),
}


def _load_params_dict() -> dict:
    """Load data.params module and return all params as a native Python dict."""
    m = importlib.import_module("data.params")
    return {name: getattr(m, name) for name in PARAM_SCHEMA}


def serialize_params(params: dict) -> dict:
    """Convert native Python params dict to JSON-serializable format."""
    result = {}
    for name, (kind, keys) in PARAM_SCHEMA.items():
        v = params[name]
        if kind in ("scalar", "list"):
            result[name] = v
        elif kind == "dict1":
            result[name] = {str(k): val for k, val in v.items()}
        elif kind == "dict2":
            k1, k2 = keys
            result[name] = [
                {k1: idx[0], k2: idx[1], "value": val}
                for idx, val in v.items()
            ]
    return result


def deserialize_params(data: dict, current: dict) -> dict:
    """Merge a partial JSON-format update into the current native params dict."""
    result = dict(current)
    for name, value in data.items():
        if name not in PARAM_SCHEMA:
            continue
        kind, keys = PARAM_SCHEMA[name]
        if kind == "scalar":
            result[name] = float(value)
        elif kind == "list":
            result[name] = [int(x) for x in value]
        elif kind == "dict1":
            result[name] = {int(k): val for k, val in value.items()}
        elif kind == "dict2":
            k1, k2 = keys
            result[name] = {
                (int(item[k1]), int(item[k2])): item["value"]
                for item in value
            }
    return result


class AppState:
    """Singleton holding active solver name and mutable in-memory parameters."""

    _instance: "AppState | None" = None

    def __new__(cls) -> "AppState":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize(self) -> None:
        if self._initialized:
            return
        self.solver_name: str = os.getenv("SOLVER", "highs").lower()
        self.params: dict = _load_params_dict()
        self._initialized = True

    # -- params helpers -------------------------------------------------------

    def get_params_object(self) -> SimpleNamespace:
        """Return a SimpleNamespace compatible with build_model(model, p)."""
        return SimpleNamespace(**self.params)

    def get_serialized_params(self) -> dict:
        return serialize_params(self.params)

    def update_params(self, data: dict) -> None:
        self.params = deserialize_params(data, self.params)

    def reset_params(self) -> None:
        self.params = _load_params_dict()

    # -- solver helpers -------------------------------------------------------

    VALID_SOLVERS = ["highs", "glpk", "cbc", "cplex"]

    def set_solver(self, name: str) -> None:
        from config import SOLVERS
        if name.lower() not in SOLVERS:
            raise ValueError(f"Solver '{name}' no reconocido. Opciones: {list(SOLVERS)}")
        self.solver_name = name.lower()


# Module-level singleton instance
app_state = AppState()
