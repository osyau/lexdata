_OPERADORES = {
    '>': lambda valor, umbral: valor > umbral,
    '<': lambda valor, umbral: valor < umbral,
    '>=': lambda valor, umbral: valor >= umbral,
    '<=': lambda valor, umbral: valor <= umbral,
    '==': lambda valor, umbral: valor == umbral,
    '!=': lambda valor, umbral: valor != umbral,
}


def evaluate_rules(datos_transaccion, reglas):
    "evalua una transaccion contra una lista de reglas configurables (ver settings.RULES); retorna los nombres de las que se cumplen."
    alertas = []
    for regla in reglas:
        valor = datos_transaccion.get(regla['field'])
        if valor is None:
            continue
        comparador = _OPERADORES[regla['operator']]
        if comparador(valor, regla['threshold']):
            alertas.append(regla['name'])
    return alertas
