# Sets
PRODUCERS = [1]
INTERMEDIARIES = [1, 2, 3, 4, 5, 6, 7]
RETAILERS = [1, 2, 3, 4]
PRODUCER_VARIANTS = list(range(1, 11))

# RB: Rendimiento maximo (Kg/Ha) semana
RB = 2585.02

# RA: Rendimiento para cada productor u (Kg/Ha) semana
RA = {1: 6.25, 2: 10.74, 3: 18, 4: 25.78, 5: 35.54, 6: 60, 7: 82.03, 8: 117.18, 9: 225, 10: 450}

# RC: Rendimiento maximo del cultivo base (Kg/Ha) semana
RC = {1: 750}

# RD: Rendimiento minimo del cultivo base (Kg/Ha) semana
RD = {1: 100}

# CA: Capacidad productiva de una persona (Kg/persona) en intermediario j
CA = {1: 20, 2: 25, 3: 23, 4: 18, 5: 17, 6: 20, 7: 30}

# CB: Capacidad productiva de una persona (Kg/persona) en detallista k
CB = {1: 130, 2: 140, 3: 120, 4: 100}

# CP: Costo de producción en el productor i ($/Kg)
CP = {1: 551}

# CI: Costo de procesamiento del intermediario j ($/Kg)
CI = {1: 100, 2: 80, 3: 70, 4: 120, 5: 170, 6: 200, 7: 90}

# CT: Costo de transporte productor i -> intermediario j ($/Kg)
CT = {(1, 1): 29.73, (1, 2): 39.71, (1, 3): 4.43, (1, 4): 4.43, (1, 5): 17.5, (1, 6): 20, (1, 7): 40}

# CTT: Costo de transporte intermediario j -> detallista k ($/Kg)
CTT = {
    (1, 1): 69.3,  (1, 2): 87.03, (1, 3): 12,  (1, 4): 22,
    (2, 1): 0,     (2, 2): 45,    (2, 3): 90,  (2, 4): 50,
    (3, 1): 33.77, (3, 2): 53.17, (3, 3): 100, (3, 4): 10,
    (4, 1): 33.77, (4, 2): 53.17, (4, 3): 60,  (4, 4): 90,
    (5, 1): 21,    (5, 2): 80,    (5, 3): 37,  (5, 4): 38,
    (6, 1): 40,    (6, 2): 25,    (6, 3): 20,  (6, 4): 70,
    (7, 1): 100,   (7, 2): 30,    (7, 3): 180, (7, 4): 27,
}

# CD: Costo de mano de obra en detallista k
CD = {1: 60000, 2: 130000, 3: 200000, 4: 100000}

# CDA: Costo por daño productor i -> intermediario j ($/Kg)
CDA = {(1, 1): 675.73, (1, 2): 685.71, (1, 3): 650.43, (1, 4): 650.43, (1, 5): 600, (1, 6): 610, (1, 7): 500}

# CDF: Costo por daño intermediario j -> detallista k ($/Kg)
CDF = {
    (1, 1): 1715.3,  (1, 2): 1733.03, (1, 3): 1700, (1, 4): 1800,
    (2, 1): 1446,    (2, 2): 1491,    (2, 3): 1400, (2, 4): 1440,
    (3, 1): 1379.7,  (3, 2): 1399.17, (3, 3): 1300, (3, 4): 1200,
    (4, 1): 1879.7,  (4, 2): 1899.17, (4, 3): 1900, (4, 4): 1990,
    (5, 1): 1900,    (5, 2): 1910,    (5, 3): 1880, (5, 4): 1800,
    (6, 1): 1500,    (6, 2): 1450,    (6, 3): 1370, (6, 4): 1510,
    (7, 1): 1200,    (7, 2): 1220,    (7, 3): 1280, (7, 4): 1290,
}

# P: Porcentaje (%) de daño productor i -> intermediario j
P = {(1, 1): 0.02, (1, 2): 0.03, (1, 3): 0.05, (1, 4): 0.08, (1, 5): 0.01, (1, 6): 0.03, (1, 7): 0.045}

# PP: Porcentaje (%) de daño intermediario j -> detallista k
PP = {
    (1, 1): 0.08, (1, 2): 0.07, (1, 3): 0.09, (1, 4): 0.08,
    (2, 1): 0.07, (2, 2): 0.05, (2, 3): 0.06, (2, 4): 0.01,
    (3, 1): 0.12, (3, 2): 0.09, (3, 3): 0.08, (3, 4): 0.1,
    (4, 1): 0.18, (4, 2): 0.03, (4, 3): 0.12, (4, 4): 0.1,
    (5, 1): 0.06, (5, 2): 0.06, (5, 3): 0.05, (5, 4): 0.04,
    (6, 1): 0.02, (6, 2): 0.03, (6, 3): 0.04, (6, 4): 0.05,
    (7, 1): 0.11, (7, 2): 0.07, (7, 3): 0.08, (7, 4): 0.1,
}

# CN: Capacidad de producción en el productor i (Kg/día)
CN = {1: 38025}

# CH: Capacidad de despacho en el productor i (Kg/día)
CH = {1: 38025}

# CHI: Capacidad de despacho en el intermediario j (Kg/día)
CHI = {1: 5000, 2: 2000, 3: 800, 4: 7000, 5: 6000, 6: 9000, 7: 3000}

# CR: Capacidad de recepción en el detallista k (Kg/día)
CR = {1: 3000, 2: 10000, 3: 2000, 4: 11100}

# DI: Demanda en el intermediario j (Kg/día)
DI = {1: 1100, 2: 850, 3: 700, 4: 4500, 5: 3000, 6: 5340, 7: 1290}

# DD: Demanda en el detallista k (Kg/día)
DD = {1: 1300, 2: 2800, 3: 1000, 4: 8000}

# CV: Capacidad del vehiculo en el intermediario j (Kg/viaje)
CV = {1: 7000, 2: 4500, 3: 1000, 4: 4500, 5: 1000, 6: 1000, 7: 1000}

# CMO: Costo de mano de obra en el intermediario j ($/semana)
CMO = {1: 130207, 2: 100000, 3: 50000, 4: 130207, 5: 60000, 6: 80000, 7: 14000}

# H: numero de hectareas (Ha) semana para cada productor u
H = {1: 3.2, 2: 25.6, 3: 10, 4: 6.4, 5: 38.4, 6: 0.5, 7: 6.4, 8: 6.4, 9: 5, 10: 10}

# Environmental parameters (placeholders — replace with real empirical data)
# DPI: Distancia/Impacto Productor -> Intermediario (i, j)
# DID: Distancia/Impacto Intermediario -> Detallista (j, k)
# IT:  Impacto Transporte / Factor Intermediario (j)
DPI = 1.0
DID = 1.0
IT  = 1.0
