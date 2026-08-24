from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    client_id: int
    amount: float
    transaction_date: datetime
    id: int | None = None
    ingested_at: str | None = None


@dataclass
class RuleAlert:
    transaction_id: int
    rule_name: str
    source: str = "regla"
    id: int | None = None
    triggered_at: str | None = None


@dataclass
class RejectedRow:
    reason: str
    raw_client_id: str | None = None
    raw_amount: str | None = None
    raw_date: str | None = None
    id: int | None = None
    ingested_at: str | None = None
