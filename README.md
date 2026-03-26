# Differential_Equations_Work1_2026-1

## Descripción de los Archivos

### 1. `Primera_EDO.py`
Un script introductorio que analiza la ecuación diferencial:
`3y + 9y' = 7xy³`.

- **Funcionalidad**:
  - Visualiza el campo de pendientes de la EDO.
  - Resuelve la EDO de forma simbólica con `SymPy`.
  - Grafica la familia de soluciones para diferentes valores de la constante de integración `C`.

### 2. `AplicationAllModels.py`
El núcleo de la simulación en Python. Modela una batería solar con las siguientes características:

- **Parámetros**: Capacidad `Q_max = 75 Ah`, consumo `P_elec = 80 W`, SOC inicial `50%`.
- **Entrada de potencia solar**: `P_in(t) = max(0, 100 * sin(π * t / 24))` (solo positiva).
- **Modelo de voltaje**: `V = 22 + 4 * (Q / Q_max)`, variando entre 22V y 26V.
- **Ecuación diferencial**: `dQ/dt = (P_in - P_elec) / V`, con limitadores para evitar sobrecarga y descarga completa.
- **Análisis**:
  - Simulación del caso nominal por 48 horas.
  - Dos escenarios extremos: sobrecarga (`P_elec = 40 W`) y sobredescarga (`P_elec = 120 W`).
  - Comparación con un modelo de voltaje constante (`V = 24V`).
  - Exporta todos los resultados a archivos CSV para análisis posterior.

### 3. `Comparison.py`
Script que compara los resultados obtenidos con Python y OpenModelica.

- **Funcionalidad**:
  - Carga los archivos CSV generados por ambos entornos.
  - Interpola los datos para una comparación punto a punto.
  - Genera gráficas de superposición y de diferencia para validar ambos modelos.
  - Produce una tabla resumen (`results_table.csv`) con los SOC finales de cada escenario.

### 4. Archivos de OpenModelica (`.mo`)
Modelos desarrollados en Modelica para la simulación del sistema. Cada uno representa un escenario diferente:

- **`VariableVoltage.mo`**: Modelo principal con voltaje variable, análogo al de Python.
- **`ConstantVoltage.mo`**: Versión con voltaje constante (24V) para comparación.
- **`Overcharge.mo`**: Escenario de sobrecarga con `P_elec = 40W`.
- **`OverDischarge.mo`**: Escenario de sobredescarga con `P_elec = 120W`.

### 5. Archivos de Datos (`.csv`)
Archivos generados por OpenModelica y Python que contienen las variables de simulación (tiempo, Q, SOC, V, corrientes, etc.). Son la base para el análisis y la comparación.

## Resultados y Gráficas

La ejecución de los scripts generará las siguientes figuras y archivos de datos:

- **`figura1_Pin.png`**: Potencia solar en un periodo de 24h.
- **`figura2_Q_y_SOC.png`**: Evolución de la carga `Q(t)` y el SOC en el caso nominal.
- **`figura3_voltaje_corrientes.png`**: Voltaje y corrientes de entrada/salida en el caso nominal.
- **`figura4_escenarios_extremos.png`**: Comparación del SOC para los casos de sobrecarga y sobredescarga.
- **`figura5_comparacion_voltaje.png`**: Comparación entre los modelos de voltaje variable y constante.
- **Archivos CSV**: `results_python.csv`, `Overcharge_python.csv`, `OverDischarge_python.csv`, `results_table.csv`.
- **Gráficas de comparación**: `comparacion_caso1.png`, `comparacion_caso2.png`, `comparacion_caso3.png`, `comparacion_caso4.png`.

## Cómo Ejecutar

### Requisitos
Asegúrate de tener instaladas las siguientes bibliotecas de Python:
```bash
pip install numpy matplotlib scipy sympy pandas
