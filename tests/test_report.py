import sqlite3
from datetime import datetime

import pytest

from src.database.connection import apply_schema
from src.database.models import RejectedRow, RuleAlert, Transaction
from src.database.repositories import AlertRepository, RejectedRowRepository, TransactionRepository
from src.core.report import generar_reporte, exportar_csv, formatear_reporte_consola


@pytest.fixture
def repos():
    conn = sqlite3.connect(":memory:")
    apply_schema(conn)
    yield TransactionRepository(conn), AlertRepository(conn), RejectedRowRepository(conn)
    conn.close()


def test_generar_reporte_calcula_cifras_correctas(repos):
    transaction_repo, alert_repo, rejected_repo = repos

    t1 = transaction_repo.insert(Transaction(client_id=1001, amount=250.5, transaction_date=datetime(2026, 5, 20)))
    t2 = transaction_repo.insert(Transaction(client_id=1001, amount=999.0, transaction_date=datetime(2026, 5, 21)))
    alert_repo.insert(RuleAlert(transaction_id=t1, rule_name="monto_mayor_200", source="regla"))
    alert_repo.insert(RuleAlert(transaction_id=t2, rule_name="monto_mayor_200", source="regla"))
    alert_repo.insert(RuleAlert(transaction_id=t2, rule_name="anomalia_monto_zscore", source="anomalia"))
    rejected_repo.insert(RejectedRow(reason="client_id inválido", raw_amount="120.00"))

    reporte = generar_reporte(transaction_repo, alert_repo, rejected_repo)

    assert reporte.total_transacciones == 2
    assert reporte.total_rechazadas == 1
    assert reporte.total_alertas == 3
    assert reporte.tasa_rechazo == pytest.approx(1 / 3)
    assert ("monto_mayor_200", 2) in reporte.alertas_por_regla
    assert ("anomalia_monto_zscore", 1) in reporte.alertas_por_regla
    assert reporte.clientes_mas_senalados == [(1001, 3)]


def test_generar_reporte_sin_datos_no_falla(repos):
    transaction_repo, alert_repo, rejected_repo = repos

    reporte = generar_reporte(transaction_repo, alert_repo, rejected_repo)

    assert reporte.total_transacciones == 0
    assert reporte.tasa_rechazo == 0.0
    assert reporte.alertas_por_regla == []
    assert reporte.clientes_mas_senalados == []


def test_formatear_reporte_consola_incluye_cifras_clave(repos):
    transaction_repo, alert_repo, rejected_repo = repos
    transaction_repo.insert(Transaction(client_id=1001, amount=250.5, transaction_date=datetime(2026, 5, 20)))

    reporte = generar_reporte(transaction_repo, alert_repo, rejected_repo)
    texto = formatear_reporte_consola(reporte)

    assert "Transacciones procesadas: 1" in texto
    assert "Tasa de rechazo" in texto


def test_exportar_csv_produce_archivo_con_cifras_correctas(repos, tmp_path):
    transaction_repo, alert_repo, rejected_repo = repos
    t1 = transaction_repo.insert(Transaction(client_id=1001, amount=250.5, transaction_date=datetime(2026, 5, 20)))
    alert_repo.insert(RuleAlert(transaction_id=t1, rule_name="monto_mayor_200", source="regla"))

    reporte = generar_reporte(transaction_repo, alert_repo, rejected_repo)
    ruta_salida = tmp_path / "reporte.csv"
    exportar_csv(reporte, ruta_salida)

    contenido = ruta_salida.read_text(encoding="utf-8")

    assert "resumen,total_transacciones,1" in contenido
    assert "alertas_por_regla,monto_mayor_200,1" in contenido
