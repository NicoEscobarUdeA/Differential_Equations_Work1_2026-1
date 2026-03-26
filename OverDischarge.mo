model OverDischarge
  "Modelo de batería solar con sobredescarga - Grupo 9"
  
  // Parámetros modificados para sobredescarga
  parameter Real Q_max = 75 "Capacidad máxima de la batería (Ah)";
  parameter Real P_elec = 120 "Potencia del dispositivo AUMENTADA (W)";
  parameter Real Q_0 = 37.5 "Carga inicial (Ah)";
  
  // Constantes
  parameter Real V_min = 22 "Voltaje mínimo (V)";
  parameter Real V_max = 26 "Voltaje máximo (V)";
  constant Real pi = 3.141592653589793;
  
  // Variables
  Real Q(start=Q_0) "Carga (Ah)";
  Real SOC "Estado de carga (%)";
  Real V "Voltaje (V)";
  Real i_in "Corriente de entrada (A)";
  Real i_out "Corriente de salida (A)";
  Real P_in "Potencia solar (W)";
  
equation
  // Potencia solar (solo positiva)
  P_in = max(0, 100 * sin(pi * time / 24));
  
  // Estado de carga
  SOC = Q / Q_max * 100;
  
  // Voltaje dependiente del SOC
  V = V_min + (V_max - V_min) * SOC / 100;
  
  // Corrientes (protegidas)
  i_in = P_in / max(V, 1e-6);
  i_out = P_elec / max(V, 1e-6);
  
  // Dinámica con límites físicos y unidades correctas
  der(Q) = if Q >= Q_max then min(0, (i_in - i_out)/3600)
           elseif Q <= 0 then max(0, (i_in - i_out)/3600)
           else (i_in - i_out)/3600;
  
annotation (
  experiment(StartTime=0, StopTime=48, Tolerance=1e-6),
  Documentation(info="<html>
    <p>Escenario de sobredescarga: P_elec aumentada a 120W</p>
    <p>Se espera que la batería se descargue completamente</p>
  </html>"));
end OverDischarge;
