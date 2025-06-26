

import numpy as np
import matplotlib.pyplot as plt 

def crear_matriz_transicion(estados, probabilidades): 
    n = len(estados)
    matriz = np.zeros((n, n))
    estado_indices = {estado: i for i, estado in enumerate(estados)}

    for estado_origen, transiciones in probabilidades.items():
        i = estado_indices[estado_origen]
        for estado_destino, prob in transiciones.items():
            j = estado_indices[estado_destino]
            matriz[i, j] = prob
    return matriz

def simular_cadena_markov(matriz_transicion, estado_inicial_idx, num_pasos, estados_nombres=None): 
    num_estados = matriz_transicion.shape[0]
    camino = [estado_inicial_idx]
    estado_actual_idx = estado_inicial_idx

    for _ in range(num_pasos):
        siguiente_estado_idx = np.random.choice(
            num_estados,
            p=matriz_transicion[estado_actual_idx, :]
        )
        camino.append(siguiente_estado_idx)
        estado_actual_idx = siguiente_estado_idx

    if estados_nombres:
        return [estados_nombres[i] for i in camino]
    return camino

def calcular_distribucion_estado(matriz_transicion, distribucion_inicial, num_pasos):
    distribucion_actual = distribucion_inicial
    for _ in range(num_pasos):
        distribucion_actual = np.dot(distribucion_actual, matriz_transicion)
    return distribucion_actual

def visualizar_matriz(matriz, estados):
    fig, ax = plt.subplots(figsize=(len(estados)*0.8, len(estados)*0.8))
    cax = ax.matshow(matriz, cmap='Blues')
    fig.colorbar(cax)
    ax.set_xticks(np.arange(len(estados)))
    ax.set_yticks(np.arange(len(estados)))
    ax.set_xticklabels(estados, rotation=45, ha="left")
    ax.set_yticklabels(estados)
    plt.title("Matriz de Transición")
    plt.show()

if __name__ == '__main__':
    estados_clima = ['Soleado', 'Nublado', 'Lluvioso']
    probabilidades_clima = {
        'Soleado': {'Soleado': 0.7, 'Nublado': 0.2, 'Lluvioso': 0.1},
        'Nublado': {'Soleado': 0.3, 'Nublado': 0.4, 'Lluvioso': 0.3},
        'Lluvioso': {'Soleado': 0.2, 'Nublado': 0.4, 'Lluvioso': 0.4}
    }

    matriz_clima = crear_matriz_transicion(estados_clima, probabilidades_clima)
    print("Matriz de Transición del Clima:\n", matriz_clima)

    camino_simulado = simular_cadena_markov(matriz_clima, 0, 10, estados_clima) 
    print("\nCamino simulado:", camino_simulado)

    distribucion_inicial = np.array([1.0, 0.0, 0.0]) # 100% Soleado al inicio
    distribucion_despues_5_pasos = calcular_distribucion_estado(matriz_clima, distribucion_inicial, 5)
    print(f"\nDistribución después de 5 pasos (inicial={estados_clima[0]}):", distribucion_despues_5_pasos)

    try:
        visualizar_matriz(matriz_clima, estados_clima)
    except Exception as e:
        print(f"\nNo se pudo visualizar la matriz (¿Matplotlib instalado?): {e}")