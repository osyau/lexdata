def evaluate_rule(datos_transaccion):
    "evalua si una transaccion cumple con ciertas reglas de negocio. "
    "por ahora, una regla de prueba: marcar como sospechoso si el monto es mayor a 200.00$"
    #Regla de prueba basica usando el diccionario de pandas" 
    monto = datos_transaccion.get('amount', 0.0)
    if monto >200.0:
        return True # cumple la regla, se dispara la alerta.
    return False 
