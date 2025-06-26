import streamlit as st
import numpy as np
import pandas as pd

# Importa tus funciones de los otros archivos
from markov_chain import crear_matriz_transicion, simular_cadena_markov, calcular_distribucion_estado
from queueing_theory import calcular_mm1_metrics, simular_mm1_fila
from visualizations import plot_markov_path, plot_queue_occupancy, plot_state_distribution
from decision_games import calcular_valor_esperado, matriz_pagos_a_dataframe, analizar_juego_normal_forma

# --- Configuración y Título de la Aplicación ---
st.set_page_config(layout="wide") # Opcional: para que la aplicación ocupe más ancho
st.title("Explorador de Teorías: Markov, Colas y Decisiones/Juegos")
st.sidebar.title("Navegación")

# --- Menú en la barra lateral ---
selected_theory = st.sidebar.radio(
    "Elige una teoría para explorar:",
    ["Cadenas de Markov", "Teoría de Colas", "Análisis de Decisiones y Juegos", "Conceptos Básicos", "Acerca de"]
)

if selected_theory == "Cadenas de Markov":
    st.header("Cadenas de Markov")
    st.write("Aquí puedes explorar cómo los sistemas cambian de un estado a otro con probabilidades fijas.")

    st.subheader("Crea tu propia Matriz de Transición")
    st.write("Define los estados y las probabilidades de transición.")

    # --- Botón para cargar el ejemplo del Clima ---
    if st.button("Cargar Ejemplo: Clima (Soleado, Nublado, Lluvioso)", key="load_markov_example"):
        st.session_state.num_estados_markov = 3
        st.session_state.estado_nombre_0 = "Soleado"
        st.session_state.estado_nombre_1 = "Nublado"
        st.session_state.estado_nombre_2 = "Lluvioso"

        st.session_state.prob_0_0 = 0.7
        st.session_state.prob_0_1 = 0.2
        st.session_state.prob_0_2 = 0.1

        st.session_state.prob_1_0 = 0.3
        st.session_state.prob_1_1 = 0.4
        st.session_state.prob_1_2 = 0.3

        st.session_state.prob_2_0 = 0.2
        st.session_state.prob_2_1 = 0.4
        st.session_state.prob_2_2 = 0.4
        
        st.rerun() # Fuerza la recarga para que los inputs se actualicen

    # Entradas para la matriz de transición
    num_estados = st.number_input("Número de estados:", min_value=2, max_value=5, value=st.session_state.get("num_estados_markov", 3), step=1, key="num_estados_markov")
    estados_nombres = []
    for i in range(num_estados):
        estados_nombres.append(st.text_input(f"Nombre del estado {i+1}:", value=st.session_state.get(f"estado_nombre_{i}", f"Estado {i+1}"), key=f"estado_nombre_{i}"))

    st.subheader("Probabilidades de Transición:")
    probabilidades = {}
    for origen_idx, origen_nombre in enumerate(estados_nombres):
        st.write(f"--- Desde {origen_nombre} ---")
        probabilidades[origen_nombre] = {}
        cols = st.columns(num_estados)
        fila_suma = 0.0
        for destino_idx, destino_nombre in enumerate(estados_nombres):
            key = f"prob_{origen_idx}_{destino_idx}"
            prob = cols[destino_idx].number_input(
                f"a {destino_nombre}",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.get(key, 0.0), # Carga el valor del session_state
                step=0.01,
                key=key
            )
            probabilidades[origen_nombre][destino_nombre] = prob
            fila_suma += prob
        st.write(f"Suma actual de probabilidades desde {origen_nombre}: {fila_suma:.2f}")
        if not np.isclose(fila_suma, 1.0) and fila_suma > 0:
            st.warning(f"¡Advertencia! Las probabilidades desde {origen_nombre} no suman 1.0. Suman {fila_suma:.2f}")

    if st.button("Calcular Matriz y Simular", key="btn_markov_simular"):
        try:
            matriz_transicion = crear_matriz_transicion(estados_nombres, probabilidades)
            st.write("Matriz de Transición:")
            st.dataframe(pd.DataFrame(matriz_transicion, index=estados_nombres, columns=estados_nombres))

            st.subheader("Simulación y Análisis:")
            num_pasos_sim = st.slider("Número de pasos para simular:", 10, 200, 50, key="slider_markov_pasos_exec") # Cambié key para evitar conflicto
            estado_inicial_sim = st.selectbox("Estado inicial para la simulación:", options=estados_nombres, key="select_markov_inicial_exec") # Cambié key
            estado_inicial_idx = estados_nombres.index(estado_inicial_sim)

            camino_simulado = simular_cadena_markov(matriz_transicion, estado_inicial_idx, num_pasos_sim, estados_nombres)
            st.write(f"Camino simulado (primeros 20 pasos): {camino_simulado[:20]}...")
            plot_markov_path(camino_simulado, title="Simulación de Camino de Markov")

            distribucion_inicial_arr = np.zeros(num_estados)
            distribucion_inicial_arr[estado_inicial_idx] = 1.0
            distribucion_final = calcular_distribucion_estado(matriz_transicion, distribucion_inicial_arr, num_pasos_sim)
            st.write("Distribución de probabilidad después de los pasos simulados:")
            st.dataframe(pd.DataFrame({"Estado": estados_nombres, "Probabilidad": distribucion_final}))
            plot_state_distribution(distribucion_final, estados_nombres, title="Distribución de Estados Final")

        except Exception as e:
            st.error(f"Ocurrió un error: {e}. Por favor, revise sus entradas.")


elif selected_theory == "Teoría de Colas":
    st.header("Teoría de Colas (M/M/1)")
    st.write("Explora cómo se comportan las colas en un sistema con llegadas aleatorias y un solo servidor.")

    # --- Botón para cargar el ejemplo de Cola de Banco ---
    if st.button("Cargar Ejemplo: Cola de Banco (M/M/1)", key="load_queue_example"):
        st.session_state.lambda_cola = 10.0
        st.session_state.mu_cola = 12.0
        st.session_state.sim_time_cola = 100 # Para que el slider también tenga un valor de ejemplo
        st.rerun() # Fuerza la recarga para que los inputs se actualicen

    st.subheader("Parámetros del Sistema M/M/1")
    lambda_val = st.number_input("Tasa de Llegada (λ):", min_value=0.1, value=st.session_state.get("lambda_cola", 5.0), step=0.1, key="lambda_cola")
    mu_val = st.number_input("Tasa de Servicio (μ):", min_value=0.1, value=st.session_state.get("mu_cola", 7.0), step=0.1, key="mu_cola")

    if st.button("Calcular Métricas", key="btn_calcular_metricas_cola"):
        metrics = calcular_mm1_metrics(lambda_val, mu_val)
        if "error" in metrics:
            st.error(metrics["error"])
        else:
            st.subheader("Métricas Calculadas:")
            st.json(metrics)

    st.subheader("Simulación de Cola M/M/1")
    sim_time = st.slider("Tiempo de Simulación:", min_value=10, max_value=500, value=st.session_state.get("sim_time_cola", 100), key="sim_time_cola")

    if st.button("Simular Cola", key="btn_simular_cola"):
        results = simular_mm1_fila(lambda_val, mu_val, sim_time)
        st.write("Resultados de la simulación (Tiempo, Clientes en sistema):")
        st.dataframe(pd.DataFrame(results, columns=["Tiempo", "Clientes en Sistema"]).head(20))
        plot_queue_occupancy(results, title="Ocupación de la Cola M/M/1 Simulada")

elif selected_theory == "Análisis de Decisiones y Juegos":
    st.header("Análisis de Decisiones y Juegos")
    st.write("Esta sección te ayuda a entender cómo tomar decisiones bajo incertidumbre y a analizar interacciones estratégicas en juegos.")

    st.subheader("1. Valor Esperado (Teoría de Decisiones)")
    st.markdown("""
    El **Valor Esperado** es una métrica clave en la teoría de decisiones.
    Representa el promedio ponderado de los posibles resultados de una decisión,
    donde cada resultado se pondera por su probabilidad de ocurrencia. Es útil
    para elegir la opción que maximice el beneficio o minimice la pérdida a largo plazo
    cuando se enfrentan a múltiples estados de la naturaleza.
    """)

    # --- Botón para cargar ejemplo de Valor Esperado (Inversión) ---
    if st.button("Cargar Ejemplo: Decisión de Inversión", key="load_ve_example"):
        st.session_state.num_estados_decision = 2
        st.session_state.prob_decision_0 = 0.6
        st.session_state.res_decision_0 = 1000.0 # Ganancia si hay éxito
        st.session_state.prob_decision_1 = 0.4
        st.session_state.res_decision_1 = -500.0 # Pérdida si fracasa
        st.rerun() # Fuerza la recarga para que los inputs se actualicen


    num_estados_decision = st.number_input("Número de estados de la naturaleza:", min_value=1, value=st.session_state.get("num_estados_decision", 2), step=1, key="num_estados_decision")
    
    probabilidades_decision = []
    resultados_decision = []
    total_prob = 0.0

    st.write("Introduce las probabilidades y los resultados para cada estado:")
    cols_prob, cols_res = st.columns(2)
    for i in range(num_estados_decision):
        with cols_prob:
            default_prob_val = st.session_state.get(f"prob_decision_{i}", 1.0 / num_estados_decision if num_estados_decision > 0 else 0.0)
            prob = st.number_input(f"Probabilidad Estado {i+1}:", min_value=0.0, max_value=1.0, value=default_prob_val, step=0.01, key=f"prob_decision_{i}")
            probabilidades_decision.append(prob)
            total_prob += prob
        with cols_res:
            default_res_val = st.session_state.get(f"res_decision_{i}", 100.0 if i == 0 else (50.0 if i == 1 else 0.0))
            res = st.number_input(f"Resultado Estado {i+1}:", value=default_res_val, step=1.0, key=f"res_decision_{i}")
            resultados_decision.append(res)
    
    st.info(f"Suma actual de probabilidades: {total_prob:.2f}")
    if not np.isclose(total_prob, 1.0) and num_estados_decision > 0:
        st.warning("La suma de las probabilidades debe ser 1.0 para un cálculo exacto del Valor Esperado.")

    if st.button("Calcular Valor Esperado", key="btn_calcular_ve"):
        try:
            ve = calcular_valor_esperado(probabilidades_decision, resultados_decision)
            st.success(f"**El Valor Esperado de esta decisión es: {ve:.2f}**")
        except ValueError as e:
            st.error(f"Error en los datos: {e}")
        except Exception as e:
            st.error(f"Ocurrió un error inesperado: {e}")

    st.markdown("---")

    st.subheader("2. Juegos en Forma Normal (Teoría de Juegos)")
    st.markdown("""
    En la **Teoría de Juegos**, analizamos situaciones donde las decisiones de múltiples jugadores se afectan mutuamente.
    Un juego en forma normal se representa por matrices de pago que muestran los resultados para cada jugador
    dadas las combinaciones de estrategias elegidas. Aquí buscaremos **Equilibrios de Nash** (simplificado).
    """)

    # --- Botón para cargar ejemplo del Dilema del Prisionero (2x2) ---
    if st.button("Cargar Ejemplo: Dilema del Prisionero (2x2)", key="load_game_example"):
        st.session_state.estr_j1 = "Cooperar,Defraudar"
        st.session_state.estr_j2 = "Cooperar,Defraudar"

        # Pagos (J1, J2) para el Dilema del Prisionero
        # Cooperar, Cooperar: (3, 3)
        st.session_state.p1_0_0 = 3.0
        st.session_state.p2_0_0 = 3.0
        # Cooperar, Defraudar: (0, 5)
        st.session_state.p1_0_1 = 0.0
        st.session_state.p2_0_1 = 5.0
        # Defraudar, Cooperar: (5, 0)
        st.session_state.p1_1_0 = 5.0
        st.session_state.p2_1_0 = 0.0
        # Defraudar, Defraudar: (1, 1)
        st.session_state.p1_1_1 = 1.0
        st.session_state.p2_1_1 = 1.0
        st.rerun() # Fuerza la recarga para que los inputs se actualicen


    st.write("Define las estrategias y los pagos para un juego de dos jugadores.")

    estrategias_j1_str = st.text_input("Estrategias Jugador 1 (separadas por coma, ej: Cooperar,Defraudar):", st.session_state.get("estr_j1", "A,B"), key="estr_j1")
    estrategias_j1 = [e.strip() for e in estrategias_j1_str.split(',') if e.strip()]

    estrategias_j2_str = st.text_input("Estrategias Jugador 2 (separadas por coma, ej: Izquierda,Derecha):", st.session_state.get("estr_j2", "X,Y"), key="estr_j2")
    estrategias_j2 = [e.strip() for e in estrategias_j2_str.split(',') if e.strip()]

    num_estr_j1 = len(estrategias_j1)
    num_estr_j2 = len(estrategias_j2)

    if num_estr_j1 == 0 or num_estr_j2 == 0:
        st.warning("Define al menos una estrategia para cada jugador.")
    else:
        st.write("Introduce los pagos (Pago J1, Pago J2) para cada combinación de estrategias:")
        pagos_j1 = np.zeros((num_estr_j1, num_estr_j2))
        pagos_j2 = np.zeros((num_estr_j1, num_estr_j2))

        for i, estr1 in enumerate(estrategias_j1):
            st.write(f"**Cuando Jugador 1 elige: {estr1}**")
            cols_game = st.columns(num_estr_j2)
            for j, estr2 in enumerate(estrategias_j2):
                with cols_game[j]:
                    st.markdown(f"**Si Jugador 2 elige: {estr2}**")
                    p1 = st.number_input(f"Pago J1:", value=st.session_state.get(f"p1_{i}_{j}", 0.0), key=f"p1_{i}_{j}")
                    p2 = st.number_input(f"Pago J2:", value=st.session_state.get(f"p2_{i}_{j}", 0.0), key=f"p2_{i}_{j}")
                    pagos_j1[i, j] = p1
                    pagos_j2[i, j] = p2
        
        if st.button("Analizar Juego", key="btn_analizar_juego"):
            df_pagos_j1 = matriz_pagos_a_dataframe(pagos_j1.tolist(), estrategias_j1, estrategias_j2)
            df_pagos_j2 = matriz_pagos_a_dataframe(pagos_j2.tolist(), estrategias_j1, estrategias_j2)

            st.subheader("Matrices de Pagos:")
            st.markdown("**Jugador 1 (Filas)**")
            st.dataframe(df_pagos_j1)
            st.markdown("**Jugador 2 (Columnas)**")
            st.dataframe(df_pagos_j2)

            try:
                analisis_result = analizar_juego_normal_forma(pagos_j1.tolist(), pagos_j2.tolist(), estrategias_j1, estrategias_j2)
                
                if "error" in analisis_result:
                    st.error(analisis_result["error"])
                else:
                    st.subheader("Análisis de Equilibrio de Nash (Estrategias Puras):")
                    if analisis_result["equilibrios_nash"]:
                        for eq_nash in analisis_result["equilibrios_nash"]:
                            st.success(f"Equilibrio de Nash encontrado: {eq_nash[0]} y {eq_nash[1]} con pagos ({eq_nash[2][0]}, {eq_nash[2][1]})")
                    else:
                        st.info("No se encontraron equilibrios de Nash de estrategia pura con este análisis básico.")
                    st.markdown("""
                    **Nota:** Este es un análisis muy simplificado que busca equilibrios de Nash en **estrategias puras**.
                    Juegos más complejos pueden tener equilibrios en **estrategias mixtas** que requieren un análisis más avanzado.
                    """)
            except Exception as e:
                st.error(f"Ocurrió un error al analizar el juego: {e}")

elif selected_theory == "Conceptos Básicos":
    st.header("Conceptos Básicos de las Teorías")
    st.write("Aquí encontrarás una breve introducción a cada teoría y su utilidad.")

    st.subheader("Cadenas de Markov")
    st.markdown("""
    Las **Cadenas de Markov** son modelos matemáticos que describen una secuencia de eventos
    en la que la probabilidad de que ocurra un evento futuro depende *únicamente* del estado
    actual, no de la secuencia de eventos que lo precedieron. Esta propiedad se conoce como
    la "propiedad de Markov".

    **¿Para qué son útiles?**
    * **Modelado de sistemas dinámicos:** Simular cambios en el clima, estados de ánimo,
        comportamiento del cliente (transiciones entre productos), etc.
    * **Predicción a largo plazo:** Calcular la probabilidad de que un sistema esté en
        cierto estado después de muchos pasos (distribución estacionaria).
    * **Optimización:** En procesos estocásticos donde las decisiones afectan las
        transiciones entre estados.
    * **Ejemplos:** Análisis de texto (secuencias de palabras), genética (cambios en el ADN),
        finanzas (movimientos de precios), marketing (fidelidad a la marca).
    """)
    st.image("images/markov_chain.png",
             caption="Diagrama de una Cadena de Markov para el Clima")


    st.subheader("Teoría de Colas")
    st.markdown("""
    La **Teoría de Colas** (o teoría de líneas de espera) es el estudio matemático de las
    líneas de espera o "colas". Analiza procesos como la llegada de clientes, el tiempo de
    servicio y el número de servidores para predecir el comportamiento del sistema.

    **¿Para qué son útiles?**
    * **Optimización de recursos:** Determinar el número óptimo de cajeros en un banco,
        personal en un centro de llamadas, o máquinas en una fábrica.
    * **Reducción de tiempos de espera:** Mejorar la satisfacción del cliente al
        minimizar el tiempo que pasan en una cola.
    * **Planificación:** Diseñar sistemas eficientes, desde aeropuertos hasta
        servicios de emergencia o sistemas informáticos.
    * **Ejemplos:** Filas en supermercados, llamadas en centros de atención, tráfico vehicular,
        tareas en un servidor de computadoras.
    """)
    st.image("images/queue_system.png",
             caption="Diagrama de un Sistema de Colas")


    st.subheader("Análisis de Decisiones y Teoría de Juegos")
    st.markdown("""
    El **Análisis de Decisiones** se enfoca en cómo tomar la mejor elección cuando
    se enfrentan múltiples opciones con resultados inciertos. Utiliza herramientas
    como árboles de decisión y el cálculo de valor esperado.

    La **Teoría de Juegos** estudia interacciones estratégicas entre dos o más
    agentes racionales, donde el resultado de la decisión de cada agente
    depende de las decisiones de los otros. Conceptos clave incluyen la
    matriz de pagos, estrategias dominantes y el equilibrio de Nash.

    **¿Para qué son útiles?**
    * **Toma de decisiones empresariales:** Inversiones, lanzamientos de productos,
        estrategias de precios, negociaciones.
    * **Ciencias políticas:** Análisis de conflictos, votaciones, diplomacia.
    * **Economía:** Competencia entre empresas, subastas, mercados.
    * **Vida cotidiana:** Decisiones personales bajo incertidumbre, elegir una
        carrera, comprar una casa.
    """)
    st.image("images/nash_equilibrium.png",
             caption="Matriz de Pagos de un Juego (Ejemplo de Equilibrio de Nash)")

elif selected_theory == "Acerca de":
    st.header("Acerca de esta Aplicación")
    st.write("Esta es una aplicación educativa para explorar conceptos fundamentales de Cadenas de Markov, Teoría de Colas y Análisis de Decisiones y Juegos.")
    st.write("Desarrollada con Python y Streamlit.")
    st.write("¡Espero que te sea útil para entender estos complejos temas!")