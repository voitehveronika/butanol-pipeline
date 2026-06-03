from scipy.integrate import odeint
import numpy as np
import csv

def load_params(csv_path='data/params.csv'):
    enzymes = []
    kd_free = {}
    immob_factor = {}
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            e = row['enzyme']
            enzymes.append(e)
            kd_free[e] = float(row['kd_free'])
            immob_factor[e] = float(row['immob_factor'])
    print(f"[ODE] Загружено ферментов: {len(enzymes)}, kd_free: {kd_free}")
    return enzymes, kd_free, immob_factor

def run_ode():
    enzymes, kd_free, immob_factor = load_params()
    kd_immob = {e: kd_free[e] / immob_factor[e] for e in enzymes}

    Vmax = 1.0
    Km_S = 0.5
    S0   = 10.0
    E0   = 1.0
    n    = len(enzymes)

    t = np.linspace(0, 24, 500)

    def pathway_odes(y, t, kd_dict):
        E = list(y[:n])
        S = max(float(y[n]), 0)
        E_min = max(min(E), 0) if n > 0 else 0
        v = Vmax * E_min * S / (Km_S + S)
        dE = [-kd_dict[enzymes[i]] * E[i] for i in range(n)]
        return dE + [-v, v]

    y0 = [E0] * n + [S0, 0.0]

    sol_free  = odeint(pathway_odes, y0, t, args=(kd_free,))
    sol_immob = odeint(pathway_odes, y0, t, args=(kd_immob,))

    yield_free  = float(sol_free[-1, n+1])
    yield_immob = float(sol_immob[-1, n+1])

    print(f"[ODE] Выход (своб.):  {yield_free:.2f} ммоль/л = {yield_free/S0*100:.1f}%")
    print(f"[ODE] Выход (иммоб.): {yield_immob:.2f} ммоль/л = {yield_immob/S0*100:.1f}%")

    return {
        'enzymes': enzymes,
        't': t,
        'sol_free': sol_free,
        'sol_immob': sol_immob,
        'kd_free': kd_free,
        'kd_immob': kd_immob,
        'yield_free': yield_free,
        'yield_immob': yield_immob,
        'S0': S0
    }