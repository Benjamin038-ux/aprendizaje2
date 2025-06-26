

import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def plot_markov_path(path_states, title="Simulación de Cadena de Markov"):
    """
    Visualiza un camino simulado de una cadena de Markov.
    """
    if not path_states:
        print("No hay datos para visualizar el camino de Markov.")
        return
    steps = list(range(len(path_states)))

    fig = go.Figure(data=go.Scatter(x=steps, y=path_states, mode='lines+markers', name='Estados'))
    fig.update_layout(
        title=title,
        xaxis_title="Paso de Tiempo",
        yaxis_title="Estado",
        hovermode="x unified" 
    )
    fig.show()

def plot_queue_occupancy(simulation_data, title="Ocupación de la Cola (M/M/1)"):
    if not simulation_data:
        print("No hay datos para visualizar la ocupación de la cola.")
        return

    times = [data[0] for data in simulation_data]
    num_clients = [data[1] for data in simulation_data]

    fig = go.Figure(data=go.Scatter(x=times, y=num_clients, mode='lines', fill='tozeroy', name='Clientes'))
    fig.update_layout(
        title=title,
        xaxis_title="Tiempo",
        yaxis_title="Número de Clientes en el Sistema",
        hovermode="x unified"
    )
    fig.show()

def plot_state_distribution(distribution, states, title="Distribución de Estados de Markov"):
    """
    Visualiza la distribución de probabilidad de los estados de Markov.
    """
    if not distribution.any() or not states:
        print("No hay datos para visualizar la distribución de estados.")
        return

    fig = px.bar(
        x=states,
        y=distribution,
        labels={'x': 'Estado', 'y': 'Probabilidad'},
        title=title
    )
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()

if __name__ == '__main__':
    print("Probando funciones de visualización (requiere datos de Markov y Colas)...")
    from markov_chain import simular_cadena_markov, crear_matriz_transicion, calcular_distribucion_estado

    estados_clima = ['Soleado', 'Nublado', 'Lluvioso']
    probabilidades_clima = {
        'Soleado': {'Soleado': 0.7, 'Nublado': 0.2, 'Lluvioso': 0.1},
        'Nublado': {'Soleado': 0.3, 'Nublado': 0.4, 'Lluvioso': 0.3},
        'Lluvioso': {'Soleado': 0.2, 'Nublado': 0.4, 'Lluvioso': 0.4}
    }
    matriz_clima = crear_matriz_transicion(estados_clima, probabilidades_clima)

    camino_simulado_nombres = simular_cadena_markov(matriz_clima, 0, 50, estados_clima)
    print("Visualizando camino de Markov (se abrirá en el navegador)...")
    plot_markov_path(camino_simulado_nombres, title="Simulación del Clima con Cadena de Markov")

    distribucion_inicial = np.array([1.0, 0.0, 0.0])
    distribucion_final = calcular_distribucion_estado(matriz_clima, distribucion_inicial, 10)
    print("Visualizando distribución de estados (se abrirá en el navegador)...")
    plot_state_distribution(distribucion_final, estados_clima, title="Distribución de Estados del Clima después de 10 Pasos")
    from queueing_theory import simular_mm1_fila

    sim_lambda = 2
    sim_mu = 3
    sim_tiempo = 50

    resultados_simulacion_cola = simular_mm1_fila(sim_lambda, sim_mu, sim_tiempo)
    print("Visualizando ocupación de la cola (se abrirá en el navegador)...")
    plot_queue_occupancy(resultados_simulacion_cola, title="Ocupación de la Cola M/M/1 a lo largo del Tiempo")