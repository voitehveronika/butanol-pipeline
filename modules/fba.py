from cobra import Model, Reaction, Metabolite

def run_fba():
    # -- Метаболиты
    glc_e = Metabolite('glc_e', name='Glucose', compartment='e')
    accoa = Metabolite('accoa_c', name='Acetyl-CoA', compartment='c')
    aacoa = Metabolite('aacoa_c', name='Acetoacetyl-CoA', compartment='c')
    hbcoa = Metabolite('hbcoa_c', name='3-Hydroxybutyryl-CoA', compartment='c')
    ccoa  = Metabolite('ccoa_c',  name='Crotonoyl-CoA', compartment='c')
    bcoa  = Metabolite('bcoa_c',  name='Butyryl-CoA', compartment='c')
    btal  = Metabolite('btal_c',  name='Butanal', compartment='c')
    btol  = Metabolite('btol_c',  name='n-Butanol', compartment='c')
    coa   = Metabolite('coa_c',   name='CoA', compartment='c')
    nadh  = Metabolite('nadh_c',  name='NADH', compartment='c')
    nad   = Metabolite('nad_c',   name='NAD+', compartment='c')
    h2o   = Metabolite('h2o_c',   name='H2O', compartment='c')
    co2   = Metabolite('co2_c',   name='CO2', compartment='c')

    r_ex_glc = Reaction('EX_glc')
    r_ex_glc.lower_bound = -10
    r_ex_glc.upper_bound = 0
    r_ex_glc.add_metabolites({glc_e: -1})

    r_glycolysis = Reaction('Glycolysis')
    r_glycolysis.lower_bound = 0
    r_glycolysis.upper_bound = 1000
    r_glycolysis.add_metabolites({glc_e: -1, nad: -4, coa: -2, accoa: +2, nadh: +4, co2: +2})

    r_thla = Reaction('ThlA'); r_thla.lower_bound=0; r_thla.upper_bound=1000
    r_thla.add_metabolites({accoa: -2, aacoa: +1, coa: +1})

    r_hbd = Reaction('Hbd'); r_hbd.lower_bound=0; r_hbd.upper_bound=1000
    r_hbd.add_metabolites({aacoa: -1, nadh: -1, hbcoa: +1, nad: +1})

    r_crt = Reaction('Crt'); r_crt.lower_bound=0; r_crt.upper_bound=1000
    r_crt.add_metabolites({hbcoa: -1, ccoa: +1, h2o: +1})

    r_ter = Reaction('Ter'); r_ter.lower_bound=0; r_ter.upper_bound=1000
    r_ter.add_metabolites({ccoa: -1, nadh: -1, bcoa: +1, nad: +1})

    r_adhe = Reaction('AdhE'); r_adhe.lower_bound=0; r_adhe.upper_bound=1000
    r_adhe.add_metabolites({bcoa: -1, nadh: -1, btal: +1, coa: +1, nad: +1})

    r_bdhb = Reaction('BdhB'); r_bdhb.lower_bound=0; r_bdhb.upper_bound=1000
    r_bdhb.add_metabolites({btal: -1, nadh: -1, btol: +1, nad: +1})

    r_ex_btol = Reaction('EX_btol'); r_ex_btol.lower_bound=0; r_ex_btol.upper_bound=1000
    r_ex_btol.add_metabolites({btol: -1})

    r_ex_co2 = Reaction('EX_co2'); r_ex_co2.lower_bound=0; r_ex_co2.upper_bound=1000
    r_ex_co2.add_metabolites({co2: -1})

    r_ex_h2o = Reaction('EX_h2o'); r_ex_h2o.lower_bound=-1000; r_ex_h2o.upper_bound=1000
    r_ex_h2o.add_metabolites({h2o: -1})

    r_ex_nad = Reaction('EX_nad'); r_ex_nad.lower_bound=-1000; r_ex_nad.upper_bound=1000
    r_ex_nad.add_metabolites({nad: -1})

    model = Model('butanol_pathway')
    model.add_reactions([
        r_ex_glc, r_glycolysis,
        r_thla, r_hbd, r_crt, r_ter, r_adhe, r_bdhb,
        r_ex_btol, r_ex_co2, r_ex_h2o, r_ex_nad
    ])

    model.objective = 'EX_btol'
    solution = model.optimize()

    flux_btol = solution.fluxes['EX_btol']
    flux_glc  = abs(solution.fluxes['EX_glc'])
    yield_mol = flux_btol / flux_glc
    yield_g_g = yield_mol * (74.12 / 180.16)

    result = {
        'status': solution.status,
        'flux_btol': flux_btol,
        'flux_glc': flux_glc,
        'yield_mol': yield_mol,
        'yield_g_g': yield_g_g
    }

    print(f"[FBA] Статус: {result['status']}")
    print(f"[FBA] Молярный выход: {yield_mol:.3f} моль/моль")
    print(f"[FBA] Массовый выход: {yield_g_g:.3f} г/г")

    return result