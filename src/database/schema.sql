CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    transaction_date TEXT NOT NULL,
    ingested_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS rule_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL REFERENCES transactions(id),
    rule_name TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'regla',
    triggered_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Filas de origen que el parser no pudo validar (Fase 3: integridad de datos).
CREATE TABLE IF NOT EXISTS rejected_rows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_client_id TEXT,
    raw_amount TEXT,
    raw_date TEXT,
    reason TEXT NOT NULL,
    ingested_at TEXT NOT NULL DEFAULT (datetime('now'))
);
