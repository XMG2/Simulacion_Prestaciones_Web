import numpy as np


def calcular_tasa_operaciones_por_estado(tasa_global, v_a, v_b, f_a, f_b):
    """Calculo de λr
    tasa_global = tasa media de llegada de operaciones global (λ)
    v_a = porcentaje de visitas del usuario A a cada estado
    v_b = porcentaje de visitas del usuario B a cada estado
    f_a = frecuencia de aparición del usuario A
    f_b = frecuencia de aparición del usuario B
    """
    tasas_llegada = []
    for v_a_i, v_b_i in zip(v_a, v_b):
        tasas_llegada.append(tasa_global * (v_a_i * f_a + v_b_i * f_b))
    return tasas_llegada


def calcular_utilizacion_recurso(tasas_llegada, demandas_rec, ni):
    """Cálculo de Ui,
    ni = nº de unidades del recurso i
    demandas_rec = demanda del recurso i por las diferentes operaciones(D_i)
    tasas_llegada = tasa de llegada de operaciones para cada estado r (vector de λr)
    """
    sumatorio = 0
    for demanda, tasa in zip(demandas_rec, tasas_llegada):
        sumatorio += demanda * tasa
    return sumatorio / ni


def calcular_tiempo_residencia_operacion_por_recurso(
    demandas, tasas_llegada, vector_n, i, r
):
    """Cálculo de Tir
    demandas = matriz de demandas (D)
    tasas_llegada = tasa de llegada de operaciones para cada estado (vector de λr)
    vector_n = vector que contiene el nº de unidades de cada recurso
    i = índice del recurso
    r = índice de la clase de operación
    """
    return demandas[i, r] / (
        1 - calcular_utilizacion_recurso(tasas_llegada, demandas[i, :], vector_n[i])
    )


def calcular_tiempo_respuesta_por_operacion(demandas, tasas_llegada, vector_n):
    """Cálculo del valor Tr para cada clase de operación (vector de Tr)
    demandas = matriz de demandas (D)
    tasas_llegada = tasa de llegada de operaciones para cada estado (vector de λr)
    vector_n = vector que contiene el nº de unidades de cada recurso
    """
    T = np.zeros(demandas.shape)
    for i in range(len(demandas)):
        for r in range(len(demandas[i])):
            T[i, r] = calcular_tiempo_residencia_operacion_por_recurso(
                demandas, tasas_llegada, vector_n, i, r
            )
    # sumar la matriz por filas
    return np.sum(T, axis=1)


def calcular_tiempo_residencia_operacion_por_recurso_multiservidor(
    demandas, tasas_llegada, vector_n, i, r
):
    """Cálculo de Tir con multiservidor
    demandas = matriz de demandas (D)
    tasas_llegada = tasa de llegada de operaciones para cada estado (vector de λr)
    vector_n = vector que contiene el nº de unidades de cada recurso
    i = índice del recurso
    r = índice de la clase de operación
    """
    return demandas[i, r] * ((vector_n[i] - 1) / vector_n[i]) + demandas[i, r] / (
        1 - calcular_utilizacion_recurso(tasas_llegada, demandas[i, :], vector_n[i])
    )


def calcular_tiempo_respuesta_por_operacion_multiservidor(
    demandas, tasas_llegada, vector_n
):
    """Cálculo del valor Tr para cada clase de operación (vector de Tr) con multiservidor
    demandas = matriz de demandas (D)
    tasas_llegada = tasa de llegada de operaciones para cada estado (vector de λr)
    vector_n = vector que contiene el nº de unidades de cada recurso
    """
    T = np.zeros(demandas.shape)
    for i in range(len(demandas)):
        for r in range(len(demandas[i])):
            T[i, r] = calcular_tiempo_residencia_operacion_por_recurso_multiservidor(
                demandas, tasas_llegada, vector_n, i, r
            )
    # sumar la matriz por filas
    return np.sum(T, axis=1)


def calcular_tiempo_medio_respuesta_operaciones(
    tasas_llegada, tasa_global, tiempos_res_op
):
    """Cálculo de T
    tasas_llegada = tasa de llegada de operaciones para cada estado r (vector de λr)
    tasa_global = tasa media de llegada de operaciones global (λ)
    tiempos_res_op = tiempo de respuesta para cada operación r (vector de Tr)
    """
    return np.sum(tiempos_res_op * tasas_llegada) / tasa_global
