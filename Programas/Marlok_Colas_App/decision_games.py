# decision_games.py

import numpy as np
import pandas as pd

def calcular_valor_esperado(probabilidades, resultados):
    """
    Calcula el valor esperado para una decisión.
    :param probabilidades: Lista/array de probabilidades de los estados de la naturaleza.
    :param resultados: Lista/array de resultados (pagos) para cada estado.
    :return: Valor esperado.
    """
    if len(probabilidades) != len(resultados):
        raise ValueError("Las listas de probabilidades y resultados deben tener la misma longitud.")
    if not np.isclose(np.sum(probabilidades), 1.0):
        raise ValueError("La suma de las probabilidades debe ser 1.0.")

    return np.sum(np.array(probabilidades) * np.array(resultados))

def matriz_pagos_a_dataframe(matriz_pagos, estrategias_filas, estrategias_columnas):
    """
    Convierte una matriz de pagos a un DataFrame de pandas para mostrarla mejor.
    :param matriz_pagos: Lista de listas representando la matriz.
    :param estrategias_filas: Nombres de las estrategias del jugador de fila.
    :param estrategias_columnas: Nombres de las estrategias del jugador de columna.
    :return: pandas.DataFrame
    """
    return pd.DataFrame(matriz_pagos, index=estrategias_filas, columns=estrategias_columnas)

def analizar_juego_normal_forma(matriz_pagos_jugador1, matriz_pagos_jugador2,
                                estrategias_jugador1, estrategias_jugador2):
    """
    Analiza un juego en forma normal (solo para 2x2 o juegos pequeños) e intenta encontrar
    estrategias dominantes/dominadas y equilibrios de Nash (muy básico).
    """
    num_estr_j1 = len(estrategias_jugador1)
    num_estr_j2 = len(estrategias_jugador2)

    if num_estr_j1 != len(matriz_pagos_jugador1) or \
       num_estr_j2 != len(matriz_pagos_jugador2[0]) or \
       num_estr_j1 != len(matriz_pagos_jugador2) or \
       num_estr_j2 != len(matriz_pagos_jugador1[0]):
        return {"error": "Las dimensiones de las matrices de pagos o estrategias no coinciden."}

    equilibrios_nash = []
    # Buscar equilibrios de Nash (estrategia pura, muy simplificado)
    for i in range(num_estr_j1):
        for j in range(num_estr_j2):
            # Comprobar si (estrategia i de J1, estrategia j de J2) es un equilibrio de Nash
            # J1 no tiene incentivo para desviarse
            es_nash_j1 = True
            for k in range(num_estr_j1):
                if matriz_pagos_jugador1[k][j] > matriz_pagos_jugador1[i][j]:
                    es_nash_j1 = False
                    break
            
            # J2 no tiene incentivo para desviarse
            es_nash_j2 = True
            for l in range(num_estr_j2):
                if matriz_pagos_jugador2[i][l] > matriz_pagos_jugador2[i][j]:
                    es_nash_j2 = False
                    break
            
            if es_nash_j1 and es_nash_j2:
                equilibrios_nash.append((f"J1: {estrategias_jugador1[i]}", f"J2: {estrategias_jugador2[j]}",
                                         (matriz_pagos_jugador1[i][j], matriz_pagos_jugador2[i][j])))

    return {
        "equilibrios_nash": equilibrios_nash
    }

# if __name__ == '__main__':
#     # Ejemplo de uso de Valor Esperado
#     prob = [0.6, 0.4]
#     res = [100, 50]
#     ve = calcular_valor_esperado(prob, res)
#     print(f"Valor Esperado: {ve}")

#     # Ejemplo de uso de Matriz de Pagos (para un juego)
#     matriz_j1 = [[3, 0], [4, 2]]
#     matriz_j2 = [[3, 4], [0, 2]]
#     estr_j1 = ["Estrategia A", "Estrategia B"]
#     estr_j2 = ["Estrategia X", "Estrategia Y"]
#     df_j1 = matriz_pagos_a_dataframe(matriz_j1, estr_j1, estr_j2)
#     df_j2 = matriz_pagos_a_dataframe(matriz_j2, estr_j1, estr_j2)
#     print("\nMatriz de Pagos J1:\n", df_j1)
#     print("\nMatriz de Pagos J2:\n", df_j2)

#     analisis_juego = analizar_juego_normal_forma(matriz_j1, matriz_j2, estr_j1, estr_j2)
#     print("\nAnálisis del Juego:", analisis_juego)