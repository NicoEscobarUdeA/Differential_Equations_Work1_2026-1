"""
Comparacion entre Python y OpenModelica - Grupo 9
Bateria Solar
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-darkgrid')

print("=" * 60)
print("COMPARACION PYTHON vs OPENMODELICA - GRUPO 9")
print("=" * 60)

# -------------------------------------------------------------------
# 1. CARGAR DATOS DE PYTHON
# -------------------------------------------------------------------

python_var = pd.read_csv('results_python.csv')
python_over = pd.read_csv('Overcharge_python.csv')
python_under = pd.read_csv('OverDischarge_python.csv')

print("\nDatos de Python cargados:")
print(f"  results_python.csv: {len(python_var)} registros")
print(f"  Overcharge_python_csv: {len(python_over)} registros")
print(f"  OverDischarge_python.csv: {len(python_under)} registros")

# -------------------------------------------------------------------
# 2. CARGAR DATOS DE OPENMODELICA Y CONVERTIR TIEMPO (segundos a horas)
# -------------------------------------------------------------------

modelica_var = pd.read_csv('VariableVoltage_Variables.csv')
modelica_cte = pd.read_csv('ConstantVoltage_Variables.csv')
modelica_over = pd.read_csv('Overcharge_Variables.csv')
modelica_under = pd.read_csv('OverDischarge_Variables.csv')

print("\nDatos de OpenModelica cargados:")
print(f"  VariableVoltage_Variables.csv: {len(modelica_var)} registros")
print(f"  ConstantVoltage_Variables.csv: {len(modelica_cte)} registros")
print(f"  Overcharge_Variables.csv: {len(modelica_over)} registros")
print(f"  OverDischarge_Variables.csv: {len(modelica_under)} registros")

# Convertir tiempo de segundos a horas (los datos de Modelica estan en segundos)
# Verificamos por el valor maximo de tiempo
for df, name in [(modelica_var, 'VariableVoltage'),
                  (modelica_cte, 'ConstantVoltage'),
                  (modelica_over, 'Overcharge'),
                  (modelica_under, 'OverDischarge')]:
    t_max = df['time'].max()
    if t_max > 100:  # Esta en segundos
        df['time_horas'] = df['time'] / 3600
        print(f"  {name}: tiempo convertido de segundos a horas")
    else:
        df['time_horas'] = df['time']

# -------------------------------------------------------------------
# 3. CASO 1: VOLTAJE VARIABLE
# -------------------------------------------------------------------

print("\n" + "=" * 60)
print("CASO 1: Voltaje Variable")
print("=" * 60)

t_py = python_var['tiempo_horas'].values
soc_py = python_var['SOC_porcentaje'].values

t_om = modelica_var['time_horas'].values
soc_om = modelica_var['SOC'].values

# Interpolar para tener los mismos puntos de tiempo
from scipy.interpolate import interp1d
soc_om_interp = interp1d(t_om, soc_om, bounds_error=False, fill_value='extrapolate')(t_py)

diferencia = soc_py - soc_om_interp

print(f"SOC inicial Python: {soc_py[0]:.1f}%")
print(f"SOC inicial Modelica: {soc_om[0]:.1f}%")
print(f"SOC final Python: {soc_py[-1]:.1f}%")
print(f"SOC final Modelica: {soc_om[-1]:.1f}%")
print(f"Diferencia maxima: {np.max(np.abs(diferencia)):.4f}%")

# Grafica
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

axes[0].plot(t_py, soc_py, 'b-', linewidth=2, label='Python')
axes[0].plot(t_om, soc_om, 'r--', linewidth=2, label='OpenModelica')
axes[0].set_xlabel('Tiempo (horas)')
axes[0].set_ylabel('SOC (%)')
axes[0].set_title('Caso 1: Voltaje Variable')
axes[0].grid(True, alpha=0.3)
axes[0].legend()
axes[0].set_ylim(0, 100)

axes[1].plot(t_py, diferencia, 'g-', linewidth=2)
axes[1].fill_between(t_py, 0, diferencia, alpha=0.3, color='green')
axes[1].set_xlabel('Tiempo (horas)')
axes[1].set_ylabel('Diferencia SOC (%)')
axes[1].set_title('Diferencia (Python - OpenModelica)')
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=0, color='k', linestyle='-', alpha=0.5)

plt.tight_layout()
plt.savefig('comparacion_caso1.png', dpi=150)
plt.show()

# -------------------------------------------------------------------
# 4. CASO 2: VOLTAJE CONSTANTE (solo OpenModelica)
# -------------------------------------------------------------------

print("\n" + "=" * 60)
print("CASO 2: Voltaje Constante (24V)")
print("=" * 60)

t_cte = modelica_cte['time_horas'].values
soc_cte = modelica_cte['SOC'].values

print(f"SOC inicial: {soc_cte[0]:.1f}%")
print(f"SOC final: {soc_cte[-1]:.1f}%")

plt.figure(figsize=(12, 5))
plt.plot(t_cte, soc_cte, 'g-', linewidth=2)
plt.xlabel('Tiempo (horas)')
plt.ylabel('SOC (%)')
plt.title('Caso 2: Voltaje Constante (24V) - OpenModelica')
plt.grid(True, alpha=0.3)
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig('comparacion_caso2.png', dpi=150)
plt.show()

# -------------------------------------------------------------------
# 5. CASO 3: SOBRECARGA
# -------------------------------------------------------------------

print("\n" + "=" * 60)
print("CASO 3: Sobrecarga (P_elec = 40W)")
print("=" * 60)

soc_py_over = python_over['SOC_sobrecarga'].values
soc_om_over = modelica_over['SOC'].values
t_om_over = modelica_over['time_horas'].values

soc_om_over_interp = interp1d(t_om_over, soc_om_over, bounds_error=False, fill_value='extrapolate')(t_py)
diferencia_over = soc_py_over - soc_om_over_interp

print(f"SOC final Python: {soc_py_over[-1]:.1f}%")
print(f"SOC final Modelica: {soc_om_over[-1]:.1f}%")
print(f"La bateria alcanza 100%: {'SI' if soc_py_over[-1] >= 99 else 'NO'}")

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

axes[0].plot(t_py, soc_py_over, 'b-', linewidth=2, label='Python')
axes[0].plot(t_om_over, soc_om_over, 'r--', linewidth=2, label='OpenModelica')
axes[0].set_xlabel('Tiempo (horas)')
axes[0].set_ylabel('SOC (%)')
axes[0].set_title('Caso 3: Sobrecarga (P_elec = 40W)')
axes[0].grid(True, alpha=0.3)
axes[0].legend()
axes[0].axhline(y=100, color='darkgreen', linestyle=':', alpha=0.7)

axes[1].plot(t_py, diferencia_over, 'g-', linewidth=2)
axes[1].fill_between(t_py, 0, diferencia_over, alpha=0.3, color='green')
axes[1].set_xlabel('Tiempo (horas)')
axes[1].set_ylabel('Diferencia SOC (%)')
axes[1].set_title('Diferencia (Python - OpenModelica)')
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=0, color='k', linestyle='-', alpha=0.5)

plt.tight_layout()
plt.savefig('comparacion_caso3.png', dpi=150)
plt.show()

# -------------------------------------------------------------------
# 6. CASO 4: SOBREDESCARGA
# -------------------------------------------------------------------

print("\n" + "=" * 60)
print("CASO 4: Sobredescarga (P_elec = 120W)")
print("=" * 60)

soc_py_under = python_under['SOC_sobredescarga'].values
soc_om_under = modelica_under['SOC'].values
t_om_under = modelica_under['time_horas'].values

soc_om_under_interp = interp1d(t_om_under, soc_om_under, bounds_error=False, fill_value='extrapolate')(t_py)
diferencia_under = soc_py_under - soc_om_under_interp

print(f"SOC final Python: {soc_py_under[-1]:.1f}%")
print(f"SOC final Modelica: {soc_om_under[-1]:.1f}%")
print(f"La bateria se descarga: {'SI' if soc_py_under[-1] <= 1 else 'NO'}")

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

axes[0].plot(t_py, soc_py_under, 'b-', linewidth=2, label='Python')
axes[0].plot(t_om_under, soc_om_under, 'r--', linewidth=2, label='OpenModelica')
axes[0].set_xlabel('Tiempo (horas)')
axes[0].set_ylabel('SOC (%)')
axes[0].set_title('Caso 4: Sobredescarga (P_elec = 120W)')
axes[0].grid(True, alpha=0.3)
axes[0].legend()
axes[0].axhline(y=0, color='darkred', linestyle=':', alpha=0.7)

axes[1].plot(t_py, diferencia_under, 'g-', linewidth=2)
axes[1].fill_between(t_py, 0, diferencia_under, alpha=0.3, color='green')
axes[1].set_xlabel('Tiempo (horas)')
axes[1].set_ylabel('Diferencia SOC (%)')
axes[1].set_title('Diferencia (Python - OpenModelica)')
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=0, color='k', linestyle='-', alpha=0.5)

plt.tight_layout()
plt.savefig('comparacion_caso4.png', dpi=150)
plt.show()

# -------------------------------------------------------------------
# 7. GRAFICA RESUMEN
# -------------------------------------------------------------------

print("\nGenerando grafica resumen...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Caso 1
axes[0, 0].plot(t_py, soc_py, 'b-', linewidth=2, label='Python')
axes[0, 0].plot(t_om, soc_om, 'r--', linewidth=2, label='Modelica')
axes[0, 0].set_title('Voltaje Variable')
axes[0, 0].set_ylabel('SOC (%)')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].legend()
axes[0, 0].set_ylim(0, 100)

# Caso 2
axes[0, 1].plot(t_cte, soc_cte, 'g-', linewidth=2)
axes[0, 1].set_title('Voltaje Constante (24V)')
axes[0, 1].set_ylabel('SOC (%)')
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].set_ylim(0, 100)

# Caso 3
axes[1, 0].plot(t_py, soc_py_over, 'b-', linewidth=2, label='Python')
axes[1, 0].plot(t_om_over, soc_om_over, 'r--', linewidth=2, label='Modelica')
axes[1, 0].set_title('Sobrecarga (P_elec = 40W)')
axes[1, 0].set_xlabel('Tiempo (horas)')
axes[1, 0].set_ylabel('SOC (%)')
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].legend()
axes[1, 0].axhline(y=100, color='darkgreen', linestyle=':', alpha=0.5)

# -------------------------------------------------------------------
# 8. TABLA DE RESULTADOS
# -------------------------------------------------------------------

resultados = pd.DataFrame({
    'Caso': ['Voltaje Variable', 'Voltaje Constante', 'Sobrecarga', 'Sobredescarga'],
    'SOC_Final_Python': [f"{soc_py[-1]:.1f}%", '-', f"{soc_py_over[-1]:.1f}%", f"{soc_py_under[-1]:.1f}%"],
    'SOC_Final_Modelica': [f"{soc_om[-1]:.1f}%", f"{soc_cte[-1]:.1f}%", f"{soc_om_over[-1]:.1f}%", f"{soc_om_under[-1]:.1f}%"]
})

resultados.to_csv('results_table.csv', index=False)
print("\nTabla de resultados guardada en 'results_table.csv'")