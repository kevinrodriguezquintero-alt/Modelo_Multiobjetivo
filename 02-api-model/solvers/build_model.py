"""Shared Pyomo model builder for both LGP and ER solvers."""
import pyomo.environ as pyo


def build_model(model: pyo.ConcreteModel, p) -> pyo.ConcreteModel:
    """
    Populate a blank ConcreteModel with sets, params, variables,
    objective expressions, and constraints.

    Parameters
    ----------
    model : pyo.ConcreteModel  — empty model to populate
    p     : namespace/module   — object with all param attributes

    Returns
    -------
    The same model, now fully built (ready to attach objectives and solve).
    Objective expressions available:
        model.Obj_Cost, model.Obj_Env, model.Obj_Social
    """

    # --- SETS ---
    model.I = pyo.Set(initialize=p.PRODUCERS)
    model.J = pyo.Set(initialize=p.INTERMEDIARIES)
    model.K = pyo.Set(initialize=p.RETAILERS)
    model.U = pyo.Set(initialize=p.PRODUCER_VARIANTS)

    # --- PARAMETERS ---
    model.RA  = pyo.Param(model.U, initialize=p.RA)
    model.RB  = pyo.Param(initialize=p.RB)
    model.RC  = pyo.Param(model.I, initialize=p.RC)
    model.RD  = pyo.Param(model.I, initialize=p.RD)
    model.CA  = pyo.Param(model.J, initialize=p.CA)
    model.CB  = pyo.Param(model.K, initialize=p.CB)
    model.CP  = pyo.Param(model.I, initialize=p.CP)
    model.CI  = pyo.Param(model.J, initialize=p.CI)
    model.CT  = pyo.Param(model.I, model.J, initialize=p.CT)
    model.CTT = pyo.Param(model.J, model.K, initialize=p.CTT)
    model.CD  = pyo.Param(model.K, initialize=p.CD)
    model.CDA = pyo.Param(model.I, model.J, initialize=p.CDA)
    model.CDF = pyo.Param(model.J, model.K, initialize=p.CDF)
    model.P   = pyo.Param(model.I, model.J, initialize=p.P)
    model.PP  = pyo.Param(model.J, model.K, initialize=p.PP)
    model.CN  = pyo.Param(model.I, initialize=p.CN)
    model.CH  = pyo.Param(model.I, initialize=p.CH)
    model.CHI = pyo.Param(model.J, initialize=p.CHI)
    model.CR  = pyo.Param(model.K, initialize=p.CR)
    model.DI  = pyo.Param(model.J, initialize=p.DI)
    model.DD  = pyo.Param(model.K, initialize=p.DD)
    model.CV  = pyo.Param(model.J, initialize=p.CV)
    model.CMO = pyo.Param(model.J, initialize=p.CMO)
    model.H   = pyo.Param(model.U, initialize=p.H)

    # Environmental parameters
    model.DPI = pyo.Param(model.I, model.J, initialize=p.DPI)
    model.DID = pyo.Param(model.J, model.K, initialize=p.DID)
    model.IT  = pyo.Param(model.J, initialize=p.IT)

    # --- VARIABLES ---
    model.X  = pyo.Var(model.I, model.J, within=pyo.NonNegativeReals)
    model.Y  = pyo.Var(model.J, model.K, within=pyo.NonNegativeReals)
    model.Z  = pyo.Var(model.I, model.J, within=pyo.NonNegativeIntegers)
    model.ZZ = pyo.Var(model.J, model.K, within=pyo.NonNegativeIntegers)
    model.W  = pyo.Var(model.I,          within=pyo.NonNegativeReals)
    model.S  = pyo.Var(model.J,          within=pyo.NonNegativeIntegers)
    model.SS = pyo.Var(model.K,          within=pyo.NonNegativeIntegers)
    model.B  = pyo.Var(model.U,          within=pyo.Binary)

    # --- OBJECTIVE EXPRESSIONS ---

    def obj_cost_expr(m):
        return (
            sum(m.CP[i]  * m.X[i, j]  for i in m.I for j in m.J) +
            sum(m.CI[j]  * m.X[i, j]  for i in m.I for j in m.J) +
            sum(m.CMO[j] * m.S[j]     for i in m.I for j in m.J) +
            sum(m.CT[i, j]  * m.X[i, j]  for i in m.I for j in m.J) +
            sum(m.CTT[j, k] * m.Y[j, k]  for j in m.J for k in m.K) +
            sum(m.CD[k]  * m.SS[k]    for j in m.J for k in m.K) +
            sum(m.CDA[i, j] * m.P[i, j]  * m.X[i, j] for i in m.I for j in m.J) +
            sum(m.CDF[j, k] * m.PP[j, k] * m.Y[j, k] for j in m.J for k in m.K)
        )
    model.Obj_Cost = pyo.Expression(rule=obj_cost_expr)

    def obj_env_expr(m):
        return (
            sum(m.Z[i, j]  * m.DPI[i, j] * m.IT[j] for i in m.I for j in m.J) +
            sum(m.ZZ[j, k] * m.DID[j, k] * m.IT[j] for j in m.J for k in m.K)
        )
    model.Obj_Env = pyo.Expression(rule=obj_env_expr)

    def obj_social_expr(m):
        return sum(m.S[j] for j in m.J) + sum(m.SS[k] for k in m.K)
    model.Obj_Social = pyo.Expression(rule=obj_social_expr)

    # --- CONSTRAINTS ---

    def cap_pro_rule(m):
        return sum(m.RC[i] * m.W[i] for i in m.I) == sum(m.CN[i] for i in m.I)
    model.cap_pro = pyo.Constraint(rule=cap_pro_rule)

    def cap_desI_rule(m, i):
        return sum(m.X[i, j] for j in m.J) <= m.CH[i]
    model.cap_desI = pyo.Constraint(model.I, rule=cap_desI_rule)

    def cap_desJ_rule(m, j):
        return sum(m.Y[j, k] for k in m.K) <= m.CHI[j]
    model.cap_desJ = pyo.Constraint(model.J, rule=cap_desJ_rule)

    def cap_rec_rule(m, k):
        return sum(m.Y[j, k] for j in m.J) <= m.CR[k]
    model.cap_rec = pyo.Constraint(model.K, rule=cap_rec_rule)

    def cap_veh_rule(m, j):
        return sum(m.X[i, j] for i in m.I) <= m.CV[j] * sum(m.Z[i, j] for i in m.I)
    model.cap_veh = pyo.Constraint(model.J, rule=cap_veh_rule)

    def cap_vehh_rule(m, j):
        return sum(m.Y[j, k] for k in m.K) <= m.CV[j] * sum(m.ZZ[j, k] for k in m.K)
    model.cap_vehh = pyo.Constraint(model.J, rule=cap_vehh_rule)

    def cap_demI_rule(m, j):
        return sum(m.X[i, j] for i in m.I) >= m.DI[j]
    model.cap_demI = pyo.Constraint(model.J, rule=cap_demI_rule)

    def cap_demD_rule(m, k):
        return sum(m.Y[j, k] for j in m.J) >= m.DD[k]
    model.cap_demD = pyo.Constraint(model.K, rule=cap_demD_rule)

    def cap_balce_rule(m, j):
        return (
            sum(m.X[i, j] * (1 - m.P[i, j]) - m.X[i, j] * m.P[i, j] for i in m.I) ==
            sum(m.Y[j, k] * (1 - m.PP[j, k]) for k in m.K)
        )
    model.cap_balce = pyo.Constraint(model.J, rule=cap_balce_rule)

    def cap_opemax_rule(m, i):
        return sum(m.X[i, j] for j in m.J) <= m.RC[i] * m.W[i]
    model.cap_opemax = pyo.Constraint(model.I, rule=cap_opemax_rule)

    def cap_opemin_rule(m, i):
        return sum(m.X[i, j] for j in m.J) >= m.RD[i] * m.W[i]
    model.cap_opemin = pyo.Constraint(model.I, rule=cap_opemin_rule)

    def cap_opeB_rule(m, j):
        return sum(m.Z[i, j] for i in m.I) <= sum(m.X[i, j] / m.CV[j] for i in m.I) + 1
    model.cap_opeB = pyo.Constraint(model.J, rule=cap_opeB_rule)

    def cap_opeC_rule(m, j):
        return sum(m.ZZ[j, k] for k in m.K) <= sum(m.Y[j, k] / m.CV[j] for k in m.K) + 1
    model.cap_opeC = pyo.Constraint(model.J, rule=cap_opeC_rule)

    def cap_perI_rule(m, j):
        return sum(m.X[i, j] for i in m.I) == m.S[j] * m.CA[j]
    model.cap_perI = pyo.Constraint(model.J, rule=cap_perI_rule)

    def cap_perD_rule(m, k):
        return sum(m.Y[j, k] for j in m.J) == m.SS[k] * m.CB[k]
    model.cap_perD = pyo.Constraint(model.K, rule=cap_perD_rule)

    def var_bina_rule(m):
        return sum(m.RA[u] * m.B[u] for u in m.U) <= m.RB
    model.var_bina = pyo.Constraint(rule=var_bina_rule)

    def suma_w_rule(m, i):
        return sum(m.B[u] * m.H[u] for u in m.U) == m.W[i]
    model.suma_w = pyo.Constraint(model.I, rule=suma_w_rule)

    return model


def extract_variables(model) -> dict:
    """Extract decision variable values from a solved model into JSON-serializable dicts."""
    def v(x):
        val = pyo.value(x)
        return val if val is not None else 0.0

    return {
        "X":  [{"i": i, "j": j, "value": v(model.X[i, j])}
               for i in model.I for j in model.J if v(model.X[i, j]) > 1e-8],
        "Y":  [{"j": j, "k": k, "value": v(model.Y[j, k])}
               for j in model.J for k in model.K if v(model.Y[j, k]) > 1e-8],
        "Z":  [{"i": i, "j": j, "value": int(round(v(model.Z[i, j])))}
               for i in model.I for j in model.J if v(model.Z[i, j]) > 0.5],
        "ZZ": [{"j": j, "k": k, "value": int(round(v(model.ZZ[j, k])))}
               for j in model.J for k in model.K if v(model.ZZ[j, k]) > 0.5],
        "W":  [{"i": i, "value": v(model.W[i])} for i in model.I],
        "S":  [{"j": j, "value": int(round(v(model.S[j])))}
               for j in model.J if v(model.S[j]) > 0.5],
        "SS": [{"k": k, "value": int(round(v(model.SS[k])))}
               for k in model.K if v(model.SS[k]) > 0.5],
        "B":  [{"u": u, "value": 1}
               for u in model.U if v(model.B[u]) > 0.5],
    }


def _solver_status(results) -> str:
    import pyomo.environ as pyo
    if (results.solver.status == pyo.SolverStatus.ok and
            results.solver.termination_condition == pyo.TerminationCondition.optimal):
        return "optimal"
    return "infeasible"
