import sqlite3

from src.database.models import RejectedRow, RuleAlert, Transaction


class TransactionRepository:
    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection

    def insert(self, transaction: Transaction) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO transactions (client_id, amount, transaction_date)
            VALUES (?, ?, ?)
            """,
            (transaction.client_id, transaction.amount, transaction.transaction_date.isoformat()),
        )
        self._connection.commit()
        return cursor.lastrowid

    def all(self) -> list[Transaction]:
        rows = self._connection.execute(
            "SELECT id, client_id, amount, transaction_date, ingested_at FROM transactions"
        ).fetchall()
        return [
            Transaction(
                id=row[0],
                client_id=row[1],
                amount=row[2],
                transaction_date=row[3],
                ingested_at=row[4],
            )
            for row in rows
        ]

    def count(self) -> int:
        return self._connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]


class AlertRepository:
    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection

    def insert(self, alert: RuleAlert) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO rule_alerts (transaction_id, rule_name, source)
            VALUES (?, ?, ?)
            """,
            (alert.transaction_id, alert.rule_name, alert.source),
        )
        self._connection.commit()
        return cursor.lastrowid

    def all(self) -> list[RuleAlert]:
        rows = self._connection.execute(
            "SELECT id, transaction_id, rule_name, source, triggered_at FROM rule_alerts"
        ).fetchall()
        return [
            RuleAlert(
                id=row[0],
                transaction_id=row[1],
                rule_name=row[2],
                source=row[3],
                triggered_at=row[4],
            )
            for row in rows
        ]

    def count_by_rule(self) -> list[tuple[str, int]]:
        rows = self._connection.execute(
            "SELECT rule_name, COUNT(*) FROM rule_alerts GROUP BY rule_name ORDER BY COUNT(*) DESC"
        ).fetchall()
        return [(row[0], row[1]) for row in rows]

    def top_flagged_clients(self, limit: int = 5) -> list[tuple[int, int]]:
        rows = self._connection.execute(
            """
            SELECT t.client_id, COUNT(*) AS total
            FROM rule_alerts a
            JOIN transactions t ON t.id = a.transaction_id
            GROUP BY t.client_id
            ORDER BY total DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [(row[0], row[1]) for row in rows]


class RejectedRowRepository:
    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection

    def insert(self, rejected_row: RejectedRow) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO rejected_rows (raw_client_id, raw_amount, raw_date, reason)
            VALUES (?, ?, ?, ?)
            """,
            (rejected_row.raw_client_id, rejected_row.raw_amount, rejected_row.raw_date, rejected_row.reason),
        )
        self._connection.commit()
        return cursor.lastrowid

    def all(self) -> list[RejectedRow]:
        rows = self._connection.execute(
            "SELECT id, raw_client_id, raw_amount, raw_date, reason, ingested_at FROM rejected_rows"
        ).fetchall()
        return [
            RejectedRow(
                id=row[0],
                raw_client_id=row[1],
                raw_amount=row[2],
                raw_date=row[3],
                reason=row[4],
                ingested_at=row[5],
            )
            for row in rows
        ]

    def count(self) -> int:
        return self._connection.execute("SELECT COUNT(*) FROM rejected_rows").fetchone()[0]
