from src.config import settings
from src.core.rule_engine import evaluate_rules


def test_regla_historica_monto_mayor_200_sigue_disparando_igual():
    # Regresion: el comportamiento original era "amount > 200.0 dispara alerta"
    assert "monto_mayor_200" in evaluate_rules({"amount": 250.5}, settings.RULES)
    assert "monto_mayor_200" not in evaluate_rules({"amount": 200.0}, settings.RULES)
    assert "monto_mayor_200" not in evaluate_rules({"amount": 50.0}, settings.RULES)


def test_segunda_regla_monto_bajo_sospechoso():
    assert "monto_bajo_sospechoso" in evaluate_rules({"amount": 0.5}, settings.RULES)
    assert "monto_bajo_sospechoso" not in evaluate_rules({"amount": 5.0}, settings.RULES)


def test_evaluate_rules_soporta_multiples_reglas_configurables():
    reglas = [
        {"name": "mayor_10", "field": "amount", "operator": ">", "threshold": 10},
        {"name": "igual_client_1", "field": "client_id", "operator": "==", "threshold": 1},
    ]

    resultado = evaluate_rules({"amount": 20, "client_id": 1}, reglas)

    assert resultado == ["mayor_10", "igual_client_1"]


def test_evaluate_rules_ignora_campo_ausente():
    reglas = [{"name": "regla_x", "field": "campo_inexistente", "operator": ">", "threshold": 1}]

    assert evaluate_rules({"amount": 5}, reglas) == []
