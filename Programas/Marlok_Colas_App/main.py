

import numpy as np
from markov_chain import crear_matriz_transicion, simular_cadena_markov, calcular_distribucion_estado
from queueing_theory import calcular_mm1_metrics, simular_mm1_fila
from visualizations import plot_markov_path, plot_queue_occupancy, plot_state_distribution

def main_menu():
    """
    Presenta un menú al usuario para seleccionar qué teoría o ejemplo ver.
    """
    while True:
        print("\n--- Programa de Teoria de Markov y Colas ---")
        print("1. Demostraciones de Cadena de Markov")
        print("2. Demostraciones de Teoria de Colas (M/M/1)")
        print("3. Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            run_markov_demos()
        elif choice == '2':
            run_queueing_demos()
        elif choice == '3':
            print("Salir")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

def run_markov_demos():
    print("\n--- Demostraciones de Cadena de Markov ---")
    estados_clima = ['Soleado', 'Nublado', 'Lluvioso']
    probabilidades_clima = {
        'Soleado': {'Soleado': 0.7, 'Nublado': 0.2, 'Lluvioso': 0.1},
        'Nublado': {'Soleado': 0.3, 'Nublado': 0.4, 'Lluvioso': 0.3},
        'Lluvioso': {'Soleado': 0.2, 'Nublado': 0.4, 'Lluvioso': 0.4}
    }
    matriz_clima = crear_matriz_transicion(estados_clima, probabilidades_clima)

    print("\n1. Simulación de un camino de Markov (50 pasos):")
    camino_simulado_nombres = simular_cadena_markov(matriz_clima, 0, 50, estados_clima)
    print("Camino:", camino_simulado_nombres)
    plot_markov_path(camino_simulado_nombres, title="Simulación del Clima con Cadena de Markov")
    input("Presione Enter para continuar...")

    print("\n2. Distribución de probabilidad de estados después de 10 pasos:")
    distribucion_inicial = np.array([1.0, 0.0, 0.0]) # Empezar 100% Soleado
    distribucion_final = calcular_distribucion_estado(matriz_clima, distribucion_inicial, 10)
    print("Distribución final:", [f"{p:.4f}" for p in distribucion_final])
    plot_state_distribution(distribucion_final, estados_clima, title="Distribución de Estados del Clima (10 Pasos)")
    input("Presione Enter para continuar...")


def run_queueing_demos():
    print("\n--- Demostraciones de Teoria de Colas (M/M/1) ---")
    lambda_ejemplo = 5  
    mu_ejemplo = 7     

    print(f"\n1. Cálculos de métricas para M/M/1 (λ={lambda_ejemplo}, μ={mu_ejemplo}):")
    metricas = calcular_mm1_metrics(lambda_ejemplo, mu_ejemplo)
    if "error" in metricas:
        print(f"Error: {metricas['error']}")
    else:
        for key, value in metricas.items():
            print(f"{key}: {value:.4f}")
    input("Presione Enter para continuar...")

    print("\n2. Simulación de ocupación de la cola a lo largo del tiempo (200 unidades de tiempo):")
    sim_lambda = 2
    sim_mu = 3
    sim_tiempo = 200
    resultados_simulacion_cola = simular_mm1_fila(sim_lambda, sim_mu, sim_tiempo)
    plot_queue_occupancy(resultados_simulacion_cola, title="Ocupación de la Cola M/M/1 Simulada")
    input("Presione Enter para continuar...")

if __name__ == '__main__':
    main_menu()