def cal_tasas_llegada(tasa_op_global, v_a, v_b, f_a, f_b):
    tasas_llegada = []
    for v_a_i, v_b_i in zip(v_a, v_b):
        tasas_llegada.append(tasa_op_global * (v_a_i * f_a + v_b_i * f_b))
    return tasas_llegada


def cal_tiempo_res_op_rec(demanda: int, tasas_llegada: list, ni: int):
    """Calculo de Tir
    Ni = nº de unidades del recurso i
    demanda = D_ir
    tasas_llegada = lambda_r
    """
    return demanda / (1 - (sum(tasas_llegada) / ni) * demanda)


def cal_tiempo_res_op(
    demandas_op: list[int], tasas_llegada: list[int], vector_ni: list[int]
) -> int:
    """Calculo de Tr
    vector_ni = nº de unidades de los recursos
    demandas_op = D_r
    tasas_llegada = lambda_r
    """
    tiempos_res_op = []
    for demanda, ni in zip(demandas_op, vector_ni):
        tiempos_res_op.append(cal_tiempo_res_op_rec(demanda, tasas_llegada, ni))
    return sum(tiempos_res_op)


def cal_utilizacion_recurso(tasas_llegada, demandas_rec, ni):
    """Calculo de Ui,
    Ni = nº de unidades del recurso i,
    demandas_rec = D_i,
    tasas_llegada = lambda_r
    """
    sumatorio = 0
    for demanda, tasa in zip(demandas_rec, tasas_llegada):
        sumatorio += demanda * tasa
    return sumatorio / ni


def cal_tiempo_med_res_op(tasas_llegada, tasa_op_global, tiempos_res_op):
    """Calculo de Tr"""
    sumatorio = 0
    for tasa_llegada, tiempo_res_op in zip(tasas_llegada, tiempos_res_op):
        sumatorio += tasa_llegada * tiempo_res_op
    return sumatorio / tasa_op_global
