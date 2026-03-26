model VariableVoltage
  "Modelo de batería solar con voltaje variable - Grupo 9"
  
  // Parámetros del Grupo 9
  parameter Real Q_max = 75 "Capacidad máxima de la batería (Ah)";
  parameter Real P_elec = 80 "Potencia del dispositivo (W)";
  parameter Real Q_0 = 37.5 "Carga inicial (Ah) - 50% de 75";
  
  // Constantes
  parameter Real V_min = 22 "Voltaje mínimo (V)";
  parameter Real V_max = 26 "Voltaje máximo (V)";
  constant Real pi = 3.141592653589793;
  
  // Variables
  Real Q(start=Q_0) "Carga almacenada (Ah)";
  Real SOC "Estado de carga (%)";
  Real V "Voltaje de la batería (V)";
  Real i_in "Corriente de entrada del panel solar (A)";
  Real i_out "Corriente de salida al dispositivo (A)";
  Real P_in "Potencia del panel solar (W)";
  
equation
  // Potencia solar (solo positiva)
  P_in = max(0, 100 * sin(pi * time / 24));
  
  // Estado de carga
  SOC = Q / Q_max * 100;
  
  // Voltaje de la batería
  V = V_min + (V_max - V_min) * SOC / 100;
  
  // Corrientes (protección contra división por cero)
  i_in = P_in / max(V, 1e-6);
  i_out = P_elec / max(V, 1e-6);
  
  // Dinámica de la batería (con límites físicos y unidades correctas)
  der(Q) = if Q >= Q_max then min(0, (i_in - i_out)/3600)
           elseif Q <= 0 then max(0, (i_in - i_out)/3600)
           else (i_in - i_out)/3600;
  
annotation (
  experiment(StartTime=0, StopTime=48, Tolerance=1e-6, Interval=0.1),
  Documentation(info="<html>
    <p>Modelo de batería solar para el Grupo 9</p>
    <p>Parámetros:</p>
    <ul>
      <li>Q_max = 75 Ah</li>
      <li>P_elec = 80 W</li>
      <li>SOC inicial = 50%</li>
    </ul>
  </html>"));
end VariableVoltage;
