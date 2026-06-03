def run_thermo():
    reactions = ['Glycolysis', 'ThlA', 'Hbd', 'Crt', 'Ter', 'AdhE', 'BdhB']
    dg_std = [-85.0, 26.1, -7.0, -2.5, -19.5, -11.5, -24.0]
    dg_min = [-97.0,  9.5, -16.5, -12.0, -26.5, -21.0, -33.5]
    dg_max = [-50.0, 23.5,   1.5,   6.0,  -4.0,  -2.5, -11.0]

    flags = []
    for r, dg in zip(reactions, dg_std):
        if dg > 0:
            flag = 'УЗКОЕ МЕСТО'
        elif dg > -5:
            flag = 'ВНИМАНИЕ'
        else:
            flag = 'OK'
        flags.append(flag)
        print(f"[Thermo] {r}: ΔG = {dg} кДж/моль → {flag}")

    result = {
        'reactions': reactions,
        'dg_std': dg_std,
        'dg_min': dg_min,
        'dg_max': dg_max,
        'flags': flags
    }

    return result