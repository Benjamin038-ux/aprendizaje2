

import numpy as np
import math

def calcular_mm1_metrics(lambda_llegadas, mu_servicio):
    if lambda_llegadas >= mu_servicio:
        return {"error": "El sistema es inestable (tasa de llegada >= tasa de servicio)"}
    # Utilización del servidor (ρ)
    rho = lambda_llegadas / mu_servicio
    # Probabilidad de que el sistema esté vacío (P0)
    p0 = 1 - rho
    # Número promedio de clientes en el sistema (Ls)
    ls = lambda_llegadas / (mu_servicio - lambda_llegadas)
    # Número promedio de clientes en la cola (Lq)
    lq = (lambda_llegadas**2) / (mu_servicio * (mu_servicio - lambda_llegadas))
    # Tiempo promedio que un cliente pasa en el sistema (Ws)
    ws = 1 / (mu_servicio - lambda_llegadas)
    # Tiempo promedio que un cliente pasa en la cola (Wq)
    wq = lambda_llegadas / (mu_servicio * (mu_servicio - lambda_llegadas))

    return {
        "utilizacion_servidor (rho)": rho,
        "prob_sistema_vacio (P0)": p0,
        "num_promedio_sistema (Ls)": ls,
        "num_promedio_cola (Lq)": lq,
        "tiempo_promedio_sistema (Ws)": ws,
        "tiempo_promedio_cola (Wq)": wq
    }

def simular_mm1_fila(lambda_llegadas, mu_servicio, tiempo_simulacion_max):
    tiempos = [0.0]
    num_clientes = [0]
    tiempo_actual = 0.0

    while tiempo_actual < tiempo_simulacion_max:

        t_llegada = np.random.exponential(1.0 / lambda_llegadas)
        t_salida = float('inf') 

        if num_clientes[-1] > 0:
            t_salida = np.random.exponential(1.0 / mu_servicio)

        if t_llegada <= t_salida:
            tiempo_actual += t_llegada
            num_clientes.append(num_clientes[-1] + 1)
        else:
            tiempo_actual += t_salida
            num_clientes.append(num_clientes[-1] - 1)

        tiempos.append(tiempo_actual)

    if tiempos[-1] > tiempo_simulacion_max:
        tiempos[-1] = tiempo_simulacion_max
    return list(zip(tiempos, num_clientes))

if __name__ == '__main__':
    print("--- Cálculos M/M/1 ---")
    lambda_ejemplo = 5  # Llegadas por hora
    mu_ejemplo = 7      # Servicios por hora

    metricas = calcular_mm1_metrics(lambda_ejemplo, mu_ejemplo)

    if "error" in metricas:
        print(f"Error: {metricas['error']}")
    else:
        for key, value in metricas.items():
            print(f"{key}: {value:.4f}") 

    print("\n--- Simulación M/M/1 ---")
    sim_lambda = 2      # Llegadas por unidad de tiempo
    sim_mu = 3          # Servicios por unidad de tiempo
    sim_tiempo = 20     # Unidades de tiempo

    resultados_simulacion = simular_mm1_fila(sim_lambda, sim_mu, sim_tiempo)
    print("Tiempo | Clientes en sistema")
    for t, n_c in resultados_simulacion[:10]: 
        print(f"{t: .2f}   | {n_c}")
    if len(resultados_simulacion) > 10:
        print(f"... y {len(resultados_simulacion) - 10} eventos más.")