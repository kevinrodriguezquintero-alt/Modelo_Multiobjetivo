# PRIMERA VERSION DEL MODELO DE AMPL MIGRADO A PYTHON

import pyomo.environ as pyo

def solve_model():
    model = pyo.ConcreteModel()

    # --- SETS ---
    model.I = pyo.Set(initialize=[1])  # Productor i
    model.J = pyo.Set(initialize=[1, 2, 3, 4, 5, 6, 7])  # Intermediarios j
    model.K = pyo.Set(initialize=[1, 2, 3, 4])  # Detallistas k
    model.U = pyo.Set(initialize=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Productores u

    # --- PARAMETERS ---
    
    # RA: Rendimiento para cada productor u (Kg/Ha) semana
    ra_data = {1: 6.25, 2: 10.74, 3: 18, 4: 25.78, 5: 35.54, 6: 60, 7: 82.03, 8: 117.18, 9: 225, 10: 450}
    model.RA = pyo.Param(model.U, initialize=ra_data)

    # RB: Rendimiento maximo (Kg/Ha) semana
    model.RB = pyo.Param(initialize=2585.02)

    # RC: Rendimiento maximo del cultivo base (Kg/Ha) semana
    rc_data = {1: 750}
    model.RC = pyo.Param(model.I, initialize=rc_data)

    # RD: Rendimiento minimo del cultivo base (Kg/Ha) semana
    rd_data = {1: 100}
    model.RD = pyo.Param(model.I, initialize=rd_data)

    # CA: Capacidad productiva de una persona (Kg/persona) en intermediario j
    ca_data = {1: 20, 2: 25, 3: 23, 4: 18, 5: 17, 6: 20, 7: 30}
    model.CA = pyo.Param(model.J, initialize=ca_data)

    # CB: Capacidad productiva de una persona (Kg/persona) en detallista k
    cb_data = {1: 130, 2: 140, 3: 120, 4: 100}
    model.CB = pyo.Param(model.K, initialize=cb_data)

    # CP: Costo de producción en el productor i ($/Kg)
    cp_data = {1: 551}
    model.CP = pyo.Param(model.I, initialize=cp_data)

    # CI: Costo de procesamiento del intermediario j ($/Kg)
    ci_data = {1: 100, 2: 80, 3: 70, 4: 120, 5: 170, 6: 200, 7: 90}
    model.CI = pyo.Param(model.J, initialize=ci_data)

    # CT: Costo de transporte productor i -> intermediario j ($/Kg)
    ct_data = { (1, 1): 29.73, (1, 2): 39.71, (1, 3): 4.43, (1, 4): 4.43, (1, 5): 17.5, (1, 6): 20, (1, 7): 40 }
    model.CT = pyo.Param(model.I, model.J, initialize=ct_data)

    # CTT: Costo de transporte intermediario j -> detallista k ($/Kg)
    ctt_data = {
        (1, 1): 69.3, (1, 2): 87.03, (1, 3): 12, (1, 4): 22,
        (2, 1): 0, (2, 2): 45, (2, 3): 90, (2, 4): 50,
        (3, 1): 33.77, (3, 2): 53.17, (3, 3): 100, (3, 4): 10,
        (4, 1): 33.77, (4, 2): 53.17, (4, 3): 60, (4, 4): 90,
        (5, 1): 21, (5, 2): 80, (5, 3): 37, (5, 4): 38,
        (6, 1): 40, (6, 2): 25, (6, 3): 20, (6, 4): 70,
        (7, 1): 100, (7, 2): 30, (7, 3): 180, (7, 4): 27
    }
    model.CTT = pyo.Param(model.J, model.K, initialize=ctt_data)

    # CD: Costo de mano de obra en detallista k ($/persona/semana?) 
    # NOTE: In AMPL it says ($/Kg) in comment, but data is like 60000. 
    # Actually, in objective it is CD[k] * SS[k] (SS is people).
    cd_data = {1: 60000, 2: 130000, 3: 200000, 4: 100000}
    model.CD = pyo.Param(model.K, initialize=cd_data)

    # CDA: Costo por daño productor i -> intermediario j ($/Kg)
    cda_data = { (1, 1): 675.73, (1, 2): 685.71, (1, 3): 650.43, (1, 4): 650.43, (1, 5): 600, (1, 6): 610, (1, 7): 500 }
    model.CDA = pyo.Param(model.I, model.J, initialize=cda_data)

    # CDF: Costo por daño intermediario j -> detallista k ($/Kg)
    cdf_data = {
        (1, 1): 1715.3, (1, 2): 1733.03, (1, 3): 1700, (1, 4): 1800,
        (2, 1): 1446, (2, 2): 1491, (2, 3): 1400, (2, 4): 1440,
        (3, 1): 1379.7, (3, 2): 1399.17, (3, 3): 1300, (3, 4): 1200,
        (4, 1): 1879.7, (4, 2): 1899.17, (4, 3): 1900, (4, 4): 1990,
        (5, 1): 1900, (5, 2): 1910, (5, 3): 1880, (5, 4): 1800,
        (6, 1): 1500, (6, 2): 1450, (6, 3): 1370, (6, 4): 1510,
        (7, 1): 1200, (7, 2): 1220, (7, 3): 1280, (7, 4): 1290
    }
    model.CDF = pyo.Param(model.J, model.K, initialize=cdf_data)

    # P: Porcentaje (%) de daño productor i -> intermediario j
    p_data = { (1, 1): 0.02, (1, 2): 0.03, (1, 3): 0.05, (1, 4): 0.08, (1, 5): 0.01, (1, 6): 0.03, (1, 7): 0.045 }
    model.P = pyo.Param(model.I, model.J, initialize=p_data)

    # PP: Porcentaje (%) de daño intermediario j -> detallista k
    pp_data = {
        (1, 1): 0.08, (1, 2): 0.07, (1, 3): 0.09, (1, 4): 0.08,
        (2, 1): 0.07, (2, 2): 0.05, (2, 3): 0.06, (2, 4): 0.01,
        (3, 1): 0.12, (3, 2): 0.09, (3, 3): 0.08, (3, 4): 0.1,
        (4, 1): 0.18, (4, 2): 0.03, (4, 3): 0.12, (4, 4): 0.1,
        (5, 1): 0.06, (5, 2): 0.06, (5, 3): 0.05, (5, 4): 0.04,
        (6, 1): 0.02, (6, 2): 0.03, (6, 3): 0.04, (6, 4): 0.05,
        (7, 1): 0.11, (7, 2): 0.07, (7, 3): 0.08, (7, 4): 0.1
    }
    model.PP = pyo.Param(model.J, model.K, initialize=pp_data)

    # CN: Capacidad de producción en el productor i (Kg/día)
    cn_data = {1: 38025}
    model.CN = pyo.Param(model.I, initialize=cn_data)

    # CH: Capacidad de despacho en el productor i (Kg/día)
    ch_data = {1: 38025}
    model.CH = pyo.Param(model.I, initialize=ch_data)

    # CHI: Capacidad de despacho en el intermediario j (Kg/día)
    chi_data = {1: 5000, 2: 2000, 3: 800, 4: 7000, 5: 6000, 6: 9000, 7: 3000}
    model.CHI = pyo.Param(model.J, initialize=chi_data)

    # CR: Capacidad de recepción en el detallista k (Kg/día)
    cr_data = {1: 3000, 2: 10000, 3: 2000, 4: 11100}
    model.CR = pyo.Param(model.K, initialize=cr_data)

    # DI: Demanda en el intermediario j (Kg/día)
    di_data = {1: 1100, 2: 850, 3: 700, 4: 4500, 5: 3000, 6: 5340, 7: 1290}
    model.DI = pyo.Param(model.J, initialize=di_data)

    # DD: Demanda en el detallista k (Kg/día)
    dd_data = {1: 1300, 2: 2800, 3: 1000, 4: 8000}
    model.DD = pyo.Param(model.K, initialize=dd_data)

    # CV: Capacidad del vehiculo en el intermediario j (Kg/viaje)
    cv_data = {1: 7000, 2: 4500, 3: 1000, 4: 4500, 5: 1000, 6: 1000, 7: 1000}
    model.CV = pyo.Param(model.J, initialize=cv_data)

    # CMO: Costo de mano de obra en el intermediario j ($/semana)
    cmo_data = {1: 130207, 2: 100000, 3: 50000, 4: 130207, 5: 60000, 6: 80000, 7: 14000}
    model.CMO = pyo.Param(model.J, initialize=cmo_data)

    # H: numero de hectareas (Ha) semana para cada productor u
    h_data = {1: 3.2, 2: 25.6, 3: 10, 4: 6.4, 5: 38.4, 6: 0.5, 7: 6.4, 8: 6.4, 9: 5, 10: 10}
    model.H = pyo.Param(model.U, initialize=h_data)

    # --- VARIABLES ---
    model.X = pyo.Var(model.I, model.J, within=pyo.NonNegativeReals)  # kg
    model.Y = pyo.Var(model.J, model.K, within=pyo.NonNegativeReals)  # kg
    model.Z = pyo.Var(model.I, model.J, within=pyo.NonNegativeIntegers)  # Viajes i -> j
    model.ZZ = pyo.Var(model.J, model.K, within=pyo.NonNegativeIntegers)  # Viajes j -> k
    model.W = pyo.Var(model.I, within=pyo.NonNegativeReals)  # Ha
    model.S = pyo.Var(model.J, within=pyo.NonNegativeIntegers)  # personas
    model.SS = pyo.Var(model.K, within=pyo.NonNegativeIntegers)  # personas
    model.B = pyo.Var(model.U, within=pyo.Binary)  # binaria productor u

    # --- OBJECTIVE ---
    def objective_rule(model):
        return (
            sum(model.CP[i] * model.X[i, j] for i in model.I for j in model.J) +
            sum(model.CI[j] * model.X[i, j] for i in model.I for j in model.J) +
            # AMPL: sum{i in I, j in J} (CMO[j]*S[j])
            sum(model.CMO[j] * model.S[j] for i in model.I for j in model.J) +
            sum(model.CT[i, j] * model.X[i, j] for i in model.I for j in model.J) +
            sum(model.CTT[j, k] * model.Y[j, k] for j in model.J for k in model.K) +
            # AMPL: sum{j in J, k in K} (CD[k]*SS[k])
            sum(model.CD[k] * model.SS[k] for j in model.J for k in model.K) +
            sum(model.CDA[i, j] * model.P[i, j] * model.X[i, j] for i in model.I for j in model.J) +
            sum(model.CDF[j, k] * model.PP[j, k] * model.Y[j, k] for j in model.J for k in model.K)
        )
    model.costo = pyo.Objective(rule=objective_rule, sense=pyo.minimize)

    # --- CONSTRAINTS ---

    # cap_pro
    def cap_pro_rule(model):
        return sum(model.RC[i] * model.W[i] for i in model.I) == sum(model.CN[i] for i in model.I)
    model.cap_pro = pyo.Constraint(rule=cap_pro_rule)

    # cap_desI
    def cap_desI_rule(model, i):
        return sum(model.X[i, j] for j in model.J) <= model.CH[i]
    model.cap_desI = pyo.Constraint(model.I, rule=cap_desI_rule)

    # cap_desJ
    def cap_desJ_rule(model, j):
        return sum(model.K for k in model.K) <= model.CHI[j] # Wait, error in my manual reading?
        # AMPL: sum{k in K} (Y[j,k]) <= CHI[j];
    def cap_desJ_rule_fixed(model, j):
        return sum(model.Y[j, k] for k in model.K) <= model.CHI[j]
    model.cap_desJ = pyo.Constraint(model.J, rule=cap_desJ_rule_fixed)

    # cap_rec
    def cap_rec_rule(model, k):
        return sum(model.Y[j, k] for j in model.J) <= model.CR[k]
    model.cap_rec = pyo.Constraint(model.K, rule=cap_rec_rule)

    # cap_veh
    def cap_veh_rule(model, j):
        return sum(model.X[i, j] for i in model.I) <= model.CV[j] * sum(model.Z[i, j] for i in model.I)
    model.cap_veh = pyo.Constraint(model.J, rule=cap_veh_rule)

    # cap_vehh
    def cap_vehh_rule(model, j):
        return sum(model.Y[j, k] for k in model.K) <= model.CV[j] * sum(model.ZZ[j, k] for k in model.K)
    model.cap_vehh = pyo.Constraint(model.J, rule=cap_vehh_rule)

    # cap_demI
    def cap_demI_rule(model, j):
        return sum(model.X[i, j] for i in model.I) >= model.DI[j]
    model.cap_demI = pyo.Constraint(model.J, rule=cap_demI_rule)

    # cap_demD
    def cap_demD_rule(model, k):
        return sum(model.Y[j, k] for j in model.J) >= model.DD[k]
    model.cap_demD = pyo.Constraint(model.K, rule=cap_demD_rule)

    # cap_balce
    def cap_balce_rule(model, j):
        return (sum(model.X[i, j] * (1 - model.P[i, j]) - model.X[i, j] * model.P[i, j] for i in model.I) == 
                sum(model.Y[j, k] * (1 - model.PP[j, k]) for k in model.K))
    model.cap_balce = pyo.Constraint(model.J, rule=cap_balce_rule)

    # cap_opemax
    def cap_opemax_rule(model, i):
        return sum(model.X[i, j] for j in model.J) <= model.RC[i] * model.W[i]
    model.cap_opemax = pyo.Constraint(model.I, rule=cap_opemax_rule)

    # cap_opemin
    def cap_opemin_rule(model, i):
        return sum(model.X[i, j] for j in model.J) >= model.RD[i] * model.W[i]
    model.cap_opemin = pyo.Constraint(model.I, rule=cap_opemin_rule)

    # cap_opeB
    def cap_opeB_rule(model, j):
        return sum(model.Z[i, j] for i in model.I) <= sum(model.X[i, j] / model.CV[j] for i in model.I) + 1
    model.cap_opeB = pyo.Constraint(model.J, rule=cap_opeB_rule)

    # cap_opeC
    def cap_opeC_rule(model, j):
        return sum(model.ZZ[j, k] for k in model.K) <= sum(model.Y[j, k] / model.CV[j] for k in model.K) + 1
    model.cap_opeC = pyo.Constraint(model.J, rule=cap_opeC_rule)

    # cap_perI
    def cap_perI_rule(model, j):
        return sum(model.X[i, j] for i in model.I) == model.S[j] * model.CA[j]
    model.cap_perI = pyo.Constraint(model.J, rule=cap_perI_rule)

    # cap_perD
    def cap_perD_rule(model, k):
        return sum(model.Y[j, k] for j in model.J) == model.SS[k] * model.CB[k]
    model.cap_perD = pyo.Constraint(model.K, rule=cap_perD_rule)

    # var_bina
    def var_bina_rule(model):
        return sum(model.RA[u] * model.B[u] for u in model.U) <= model.RB
    model.var_bina = pyo.Constraint(rule=var_bina_rule)

    # suma_w
    def suma_w_rule(model, i):
        return sum(model.B[u] * model.H[u] for u in model.U) == model.W[i]
    model.suma_w = pyo.Constraint(model.I, rule=suma_w_rule)

    # --- SOLVE ---
    # --- SOLVE ---
    # Use CPLEX specifically as requested
    solver_name = 'cplex'
    try:
        # The available 'cplex' command seems to be an ASL solver (AMPL Solver Library),
        # so we must use solver_io='nl'.
        # We specify executable='cplex' to be sure, and skip the available() check 
        # which sometimes fails for ASL solvers on Windows.
        solver = pyo.SolverFactory(solver_name, solver_io='nl', executable='cplex')
        
        print(f"Using solver: {solver_name} (ASL interface)")
        results = solver.solve(model, tee=True)
        
        # Check solver status
        if (results.solver.status == pyo.SolverStatus.ok) and \
           (results.solver.termination_condition == pyo.TerminationCondition.optimal):
            print("Solución óptima encontrada.")
        elif results.solver.termination_condition == pyo.TerminationCondition.infeasible:
            print("El modelo es infactible.")
            return
        else:
            print(f"Solver Status: {results.solver.status}")
            print(f"Termination Condition: {results.solver.termination_condition}")

    except Exception as e:
        print(f"Ocurrió un error al intentar usar el solver '{solver_name}': {e}")
        return

    # --- DISPLAY ---
    print("\n\n*************************************")
    print("RESULTADOS DEL PROBLEMA")
    print("*************************************\n")

    print(f"COSTO  = \t{pyo.value(model.costo):9.1f}")

    print("\nCantidad de producto a enviar del produtor al intermediario (X):")
    for i in model.I:
        for j in model.J:
            if pyo.value(model.X[i, j]) > 0:
                print(f"X[{i},{j}] = {pyo.value(model.X[i, j]):.2f}")

    print("\nCantidad de producto a enviar del intermediario al detallista (Y):")
    for j in model.J:
        for k in model.K:
            if pyo.value(model.Y[j, k]) > 0:
                print(f"Y[{j},{k}] = {pyo.value(model.Y[j, k]):.2f}")

    print("\nNumero de viajes del productor al intermediario (Z):")
    for i in model.I:
        for j in model.J:
            if pyo.value(model.Z[i, j]) > 0:
                print(f"Z[{i},{j}] = {pyo.value(model.Z[i, j])}")

    print("\nNumero de viajes del intermediario al detallista (ZZ):")
    for j in model.J:
        for k in model.K:
            if pyo.value(model.ZZ[j, k]) > 0:
                print(f"ZZ[{j},{k}] = {pyo.value(model.ZZ[j, k])}")

    print("\nCantidad de Hectareas (W):")
    for i in model.I:
        print(f"W[{i}] = {pyo.value(model.W[i]):.2f}")

    print("\nNumero de personas a contratar en el intermediario (S):")
    for j in model.J:
        if pyo.value(model.S[j]) > 0:
            print(f"S[{j}] = {pyo.value(model.S[j])}")

    print("\nNumero de personas a contratar en el detallista (SS):")
    for k in model.K:
        if pyo.value(model.SS[k]) > 0:
            print(f"SS[{k}] = {pyo.value(model.SS[k])}")

    print("\nVariable binaria (B):")
    for u in model.U:
        if pyo.value(model.B[u]) > 0.5:
            print(f"B[{u}] = 1")

if __name__ == "__main__":
    solve_model()
