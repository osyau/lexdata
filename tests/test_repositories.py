import sqlite3
from datetime import datetime

import pytest

from src.database.connection import apply_schema
from src.database.models import RuleAlert, Transaction
from src.database.repositories import AlertRepository, TransactionRepository


@pytest.fixture
def connection():
    conn = sqlite3.connect(":memory:")
    apply_schema(conn)
    yield conn
    conn.close()


def test_transaction_repository_insert_and_read(connection):
    repo = TransactionRepository(connection)
    transaction_id = repo.insert(
        Transaction(client_id=1001, amount=250.5, transaction_date=datetime(2026, 5, 20))
    )

    stored = repo.all()

    assert transaction_id == 1
    assert len(stored) == 1
    assert stored[0].client_id == 1001
    assert stored[0].amount == 250.5


def test_alert_repository_insert_and_read(connection):
    transaction_repo = TransactionRepository(connection)
    alert_repo = AlertRepository(connection)

    transaction_id = transaction_repo.insert(
        Transaction(client_id=1001, amount=250.5, transaction_date=datetime(2026, 5, 20))
    )
    alert_repo.insert(RuleAlert(transaction_id=transaction_id, rule_name="monto_mayor_200"))

    alerts = alert_repo.all()

    assert len(alerts) == 1
    assert alerts[0].transaction_id == transaction_id
    assert alerts[0].rule_name == "monto_mayor_200"
    assert alerts[0].source == "regla"
