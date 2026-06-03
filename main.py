from modules.fba import run_fba
from modules.thermo import run_thermo
from modules.ode import run_ode
from modules.report import run_report

print("=" * 50)
print("  ButanolPathOptimizer — запуск пайплайна")
print("=" * 50)

print("\n[Шаг 1] Стехиометрическое моделирование (FBA)...")
fba_result = run_fba()

print("\n[Шаг 2] Термодинамический анализ...")
thermo_result = run_thermo()

print("\n[Шаг 3] Кинетическое моделирование (ODE)...")
ode_result = run_ode()

print("\n[Шаг 4] Генерация PDF-отчёта...")
run_report(fba_result, thermo_result, ode_result)

print("\n" + "=" * 50)
print("  Готово! Отчёт сохранён в output/report.pdf")
print("=" * 50)