"""
Trabajo EDO - Grupo 9
Aplicación: Almacenamiento de energía renovable en una batería
Integrantes: [Nicolás Escobar Rodríguez
              Cristian D. Hurtado
              Simón López Arcila]
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandas as pd

# -------------------------------------------------------------------
# PARAMETROS DEL GRUPO 9
# -------------------------------------------------------------------
Q_max = 75          # Capacidad maxima (Ah)
P_elec = 80         # Potencia del dispositivo (W)
SOC_ini = 50        # Estado de carga inicial (%)
Q_ini = Q_max * SOC_ini / 100   # 37.5 Ah

V_min = 22          # Voltaje minimo (V)
V_max = 26          # Voltaje maximo (V)

print("=" * 50)
print("TRABAJO EDO - GRUPO 9")
print("Aplicación: Almacenamiento de energía renovable en una batería")
print(f"Q_max = {Q_max} Ah")
print(f"P_elec = {P_elec} W")
print(f"SOC_ini = {SOC_ini}% -> Q_ini = {Q_ini} Ah")
print("=" * 50)

# -------------------------------------------------------------------
# FUNCIONES DEL MODELO 
# -------------------------------------------------------------------

def Pin(t):
    """
    Potencia solar en funcion del tiempo (horas)
    Periodo de 24 horas. Usa modulo para que sea periodica.
    """
    t_mod = t % 24
    return 100 * np.sin(np.pi * t_mod / 24)

def V_bateria(Q):
    """Voltaje en funcion de la carga Q (Ah)"""
    Q = np.clip(Q, 0, Q_max)
    SOC = Q / Q_max  # SOC en fraccion (0 a 1)
    return 22 + 4 * SOC  # V entre 22V y 26V

def dQdt(t, Q):
    """Ecuacion diferencial dQ/dt"""
    Q = np.clip(Q, 0, Q_max)
    P_in_actual = Pin(t)

    # Limitadores fisicos
    if Q <= 0 and P_in_actual < P_elec:
        return 0
    if Q >= Q_max and P_in_actual > P_elec:
        return 0

    V_actual = V_bateria(Q)
    return (P_in_actual - P_elec) / V_actual

# -------------------------------------------------------------------
# GRAFICA DE POTENCIA SOLAR
# -------------------------------------------------------------------

t_24h = np.linspace(0, 24, 1000)
Pin_24h = Pin(t_24h)

plt.figure(figsize=(12, 6))
plt.plot(t_24h, Pin_24h, 'b-', linewidth=2, label='$P_{in}(t)$')
plt.fill_between(t_24h, 0, Pin_24h, alpha=0.3, color='orange')
plt.xlabel('Tiempo (horas)', fontsize=12)
plt.ylabel('Potencia Solar (W)', fontsize=12)
plt.title('Potencia Generada por el Panel Solar vs Tiempo', fontsize=14)
plt.grid(True, alpha=0.3)
plt.xlim(0, 24)
plt.ylim(0, 110)
plt.axhline(y=80, color='r', linestyle='--', label='$P_{elec} = 80$ W (consumo)')
plt.legend(loc='upper right')
plt.xticks(np.arange(0, 25, 2))
plt.tight_layout()
plt.savefig('figura1_Pin.png', dpi=150)
plt.show()

# Verificar que la potencia no se hace cero despues de 24h
t_48h = np.linspace(0, 48, 2000)
Pin_48h = Pin(t_48h)

plt.figure(figsize=(12, 6))
plt.plot(t_48h, Pin_48h, 'b-', linewidth=2)
plt.xlabel('Tiempo (horas)', fontsize=12)
plt.ylabel('Potencia Solar (W)', fontsize=12)
plt.title('Potencia del Panel Solar - Periodo de 48 horas', fontsize=14)
plt.grid(True, alpha=0.3)
plt.xlim(0, 48)
plt.axhline(y=80, color='r', linestyle='--', label='Consumo constante')
plt.legend()
plt.tight_layout()
plt.savefig('figura1b_Pin_48h.png', dpi=150)
plt.show()

print("Grafica de Pin(t) generada")

# -------------------------------------------------------------------
# SIMULACION DEL SISTEMA ORIGINAL
# -------------------------------------------------------------------

t_span = (0, 48)
t_eval = np.linspace(0, 48, 2000)

sol = solve_ivp(dQdt, t_span, [Q_ini], t_eval=t_eval, method='RK45', rtol=1e-6)

t_sol = sol.t
Q_sol = np.clip(sol.y[0], 0, Q_max)
SOC_sol = Q_sol / Q_max * 100
V_sol = V_bateria(Q_sol)

print(f"EDO resuelta numericamente para t = [0, 48] horas")
print(f"  Q(0) = {Q_sol[0]:.2f} Ah")
print(f"  Q(48) = {Q_sol[-1]:.2f} Ah")
print(f"  SOC(48) = {SOC_sol[-1]:.1f}%")

# Verificacion de que SOC no es 0
if SOC_sol[-1] <= 1.0:
    print("\n*** ADVERTENCIA: SOC final es 0% o muy bajo ***")
    print("Verificar que Pin(t) esta definida correctamente")
else:
    print("\n*** OK: SOC final es razonable ***")

# -------------------------------------------------------------------
# GRAFICAS DE Q(t) y SOC(t)
# -------------------------------------------------------------------

fig, axes = plt.subplots(2, 1, figsize=(12, 10))

axes[0].plot(t_sol, Q_sol, 'b-', linewidth=2)
axes[0].set_xlabel('Tiempo (horas)', fontsize=12)
axes[0].set_ylabel('Carga Q(t) (Ah)', fontsize=12)
axes[0].set_title('Carga Almacenada en la Bateria vs Tiempo', fontsize=14)
axes[0].grid(True, alpha=0.3)
axes[0].axhline(y=Q_max, color='r', linestyle='--', linewidth=2, label=f'Maxima carga ({Q_max} Ah)')
axes[0].axhline(y=0, color='darkred', linestyle='--', linewidth=2, label='Descarga total (0 Ah)')
axes[0].axhline(y=Q_ini, color='g', linestyle=':', alpha=0.7, label=f'Carga inicial ({Q_ini:.1f} Ah)')
axes[0].legend(loc='best')
axes[0].set_ylim(-5, Q_max + 10)

axes[1].plot(t_sol, SOC_sol, 'g-', linewidth=2)
axes[1].set_xlabel('Tiempo (horas)', fontsize=12)
axes[1].set_ylabel('Estado de Carga SOC (%)', fontsize=12)
axes[1].set_title('Estado de Carga de la Bateria vs Tiempo', fontsize=14)
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=100, color='r', linestyle='--', linewidth=2, label='100% (completamente cargada)')
axes[1].axhline(y=0, color='darkred', linestyle='--', linewidth=2, label='0% (completamente descargada)')
axes[1].axhline(y=SOC_ini, color='b', linestyle=':', alpha=0.7, label=f'SOC inicial = {SOC_ini}%')
axes[1].legend(loc='best')
axes[1].set_ylim(-10, 110)

plt.tight_layout()
plt.savefig('figura2_Q_y_SOC.png', dpi=150)
plt.show()

# -------------------------------------------------------------------
# CORRIENTES Y VOLTAJE
# -------------------------------------------------------------------

P_in_sol = Pin(t_sol)
i_in_sol = P_in_sol / V_sol
i_out_sol = P_elec / V_sol

# Cuando la bateria esta llena, la corriente de entrada se anula
i_in_sol[Q_sol >= Q_max] = 0

fig, axes = plt.subplots(2, 1, figsize=(12, 10))

axes[0].plot(t_sol, V_sol, 'purple', linewidth=2)
axes[0].set_xlabel('Tiempo (horas)', fontsize=12)
axes[0].set_ylabel('Voltaje V(t) (V)', fontsize=12)
axes[0].set_title('Voltaje de la Bateria vs Tiempo', fontsize=14)
axes[0].grid(True, alpha=0.3)
axes[0].axhline(y=V_min, color='r', linestyle='--', label=f'Voltaje minimo ({V_min} V)')
axes[0].axhline(y=V_max, color='g', linestyle='--', label=f'Voltaje maximo ({V_max} V)')
axes[0].legend()
axes[0].set_ylim(20, 28)

axes[1].plot(t_sol, i_in_sol, 'b-', linewidth=2, label='$i_{in}(t)$ (corriente de entrada)')
axes[1].plot(t_sol, i_out_sol, 'r-', linewidth=2, label='$i_{out}(t)$ (corriente de salida)')
axes[1].fill_between(t_sol, i_in_sol, i_out_sol, where=(i_in_sol > i_out_sol),
                     alpha=0.3, color='green', label='Carga neta')
axes[1].fill_between(t_sol, i_in_sol, i_out_sol, where=(i_in_sol < i_out_sol),
                     alpha=0.3, color='red', label='Descarga neta')
axes[1].set_xlabel('Tiempo (horas)', fontsize=12)
axes[1].set_ylabel('Corriente (A)', fontsize=12)
axes[1].set_title('Corrientes de Entrada y Salida vs Tiempo', fontsize=14)
axes[1].grid(True, alpha=0.3)
axes[1].legend(loc='best')

plt.tight_layout()
plt.savefig('figura3_voltaje_corrientes.png', dpi=150)
plt.show()

# -------------------------------------------------------------------
# ESCENARIO 1: SOBRECARGA (P_elec = 40W)
# -------------------------------------------------------------------

print("\n--- Escenario 1: Sobrecarga (P_elec = 40 W) ---")
P_elec_over = 40

def dQdt_over(t, Q):
    Q = np.clip(Q, 0, Q_max)
    P_in_actual = Pin(t)

    if Q <= 0 and P_in_actual < P_elec_over:
        return 0
    if Q >= Q_max and P_in_actual > P_elec_over:
        return 0

    V_actual = V_bateria(Q)
    return (P_in_actual - P_elec_over) / V_actual

sol_over = solve_ivp(dQdt_over, (0, 48), [Q_ini], t_eval=t_eval, method='RK45')
Q_over = np.clip(sol_over.y[0], 0, Q_max)
SOC_over = Q_over / Q_max * 100

print(f"  SOC inicial: {SOC_over[0]:.2f}%")
print(f"  SOC final: {SOC_over[-1]:.2f}%")

# -------------------------------------------------------------------
# ESCENARIO 2: SOBREDESCARGA (P_elec = 120W)
# -------------------------------------------------------------------

print("\n--- Escenario 2: Sobredescarga (P_elec = 120 W) ---")
P_elec_under = 120

def dQdt_under(t, Q):
    Q = np.clip(Q, 0, Q_max)
    P_in_actual = Pin(t)

    if Q <= 0 and P_in_actual < P_elec_under:
        return 0
    if Q >= Q_max and P_in_actual > P_elec_under:
        return 0

    V_actual = V_bateria(Q)
    return (P_in_actual - P_elec_under) / V_actual

sol_under = solve_ivp(dQdt_under, (0, 48), [Q_ini], t_eval=t_eval, method='RK45')
Q_under = np.clip(sol_under.y[0], 0, Q_max)
SOC_under = Q_under / Q_max * 100

print(f"  SOC inicial: {SOC_under[0]:.2f}%")
print(f"  SOC final: {SOC_under[-1]:.2f}%")

# -------------------------------------------------------------------
# GRAFICA COMPARATIVA DE ESCENARIOS
# -------------------------------------------------------------------

plt.figure(figsize=(12, 8))
plt.plot(t_sol, SOC_sol, 'b-', linewidth=2, label=f'Original (P_elec = 80 W)')
plt.plot(t_sol, SOC_over, 'g-', linewidth=2, label=f'Sobrecarga (P_elec = {P_elec_over} W)')
plt.plot(t_sol, SOC_under, 'r-', linewidth=2, label=f'Sobredescarga (P_elec = {P_elec_under} W)')
plt.xlabel('Tiempo (horas)', fontsize=12)
plt.ylabel('Estado de Carga SOC (%)', fontsize=12)
plt.title('Comparacion de Escenarios Extremos', fontsize=14)
plt.grid(True, alpha=0.3)
plt.axhline(y=100, color='darkgreen', linestyle='--', alpha=0.7, label='100%')
plt.axhline(y=0, color='darkred', linestyle='--', alpha=0.7, label='0%')
plt.legend(loc='best')
plt.xlim(0, 48)
plt.ylim(-10, 110)
plt.tight_layout()
plt.savefig('figura4_escenarios_extremos.png', dpi=150)
plt.show()

# -------------------------------------------------------------------
# MODELO CON VOLTAJE CONSTANTE
# -------------------------------------------------------------------

V_cte = 24

def dQdt_cte(t, Q):
    Q = np.clip(Q, 0, Q_max)
    P_in_actual = Pin(t)

    if Q <= 0 and P_in_actual < P_elec:
        return 0
    if Q >= Q_max and P_in_actual > P_elec:
        return 0

    return (P_in_actual - P_elec) / V_cte

sol_cte = solve_ivp(dQdt_cte, (0, 48), [Q_ini], t_eval=t_eval, method='RK45')
Q_cte = np.clip(sol_cte.y[0], 0, Q_max)
SOC_cte = Q_cte / Q_max * 100

fig, axes = plt.subplots(2, 1, figsize=(12, 10))

axes[0].plot(t_sol, SOC_sol, 'b-', linewidth=2, label='Voltaje variable (modelo original)')
axes[0].plot(t_sol, SOC_cte, 'r--', linewidth=2, label='Voltaje constante (24 V)')
axes[0].set_xlabel('Tiempo (horas)', fontsize=12)
axes[0].set_ylabel('SOC (%)', fontsize=12)
axes[0].set_title('Comparacion: Voltaje Variable vs Voltaje Constante', fontsize=14)
axes[0].grid(True, alpha=0.3)
axes[0].legend(loc='best')
axes[0].set_ylim(0, 100)

diferencia = SOC_sol - SOC_cte
axes[1].plot(t_sol, diferencia, 'g-', linewidth=2)
axes[1].fill_between(t_sol, 0, diferencia, alpha=0.3, color='green')
axes[1].set_xlabel('Tiempo (horas)', fontsize=12)
axes[1].set_ylabel('Diferencia de SOC (%)', fontsize=12)
axes[1].set_title('Diferencia entre Modelos (Variable - Constante)', fontsize=14)
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=0, color='k', linestyle='-', alpha=0.5)

plt.tight_layout()
plt.savefig('figura5_comparacion_voltaje.png', dpi=150)
plt.show()

# -------------------------------------------------------------------
# EXPORTAR DATOS A CSV
# -------------------------------------------------------------------

df = pd.DataFrame({
    'tiempo_horas': t_sol,
    'Q_Ah': Q_sol,
    'SOC_porcentaje': SOC_sol,
    'V_voltios': V_sol,
    'Pin_W': Pin(t_sol),
    'iin_A': i_in_sol,
    'iout_A': i_out_sol
})
df.to_csv('results_python.csv', index=False)
print("\nDatos exportados a 'results_python.csv'")

df_over = pd.DataFrame({
    'tiempo_horas': t_sol,
    'SOC_sobrecarga': SOC_over
})
df_over.to_csv('Overcharge_python.csv', index=False)

df_under = pd.DataFrame({
    'tiempo_horas': t_sol,
    'SOC_sobredescarga': SOC_under
})
df_under.to_csv('OverDischarge_python.csv', index=False)

print("Todos los datos exportados correctamente")

# -------------------------------------------------------------------
# RESUMEN FINAL
# -------------------------------------------------------------------

print("\n" + "=" * 50)
print("RESUMEN FINAL DEL ANALISIS")
print("=" * 50)
print(f"""
1. Potencia solar maxima: 100 W (al mediodia)
2. Consumo constante: {P_elec} W
3. Capacidad bateria: {Q_max} Ah

4. Comportamiento del sistema original:
   - SOC inicial: {SOC_ini}%
   - SOC despues de 48h: {SOC_sol[-1]:.1f}%
   - ¿Se sostiene el dispositivo? {'SI' if SOC_sol[-1] > 0 else 'NO'}
   - ¿Hay sobrecarga? {'SI' if np.max(SOC_sol) >= 99.9 else 'NO'}

5. Escenario sobrecarga (P_elec = {P_elec_over} W):
   - SOC despues de 48h: {SOC_over[-1]:.1f}%
   - ¿Se sobrecarga? {'SI' if np.max(SOC_over) >= 99.9 else 'NO'}

6. Escenario sobredescarga (P_elec = {P_elec_under} W):
   - SOC despues de 48h: {SOC_under[-1]:.1f}%
   - ¿Se descarga completamente? {'SI' if SOC_under[-1] <= 0 else 'NO'}

7. Voltaje constante (24 V):
   - Diferencia maxima con modelo original: {np.max(np.abs(diferencia)):.1f}%
""")

print("=" * 50)
print("FIN DEL ANALISIS")
print("=" * 50)