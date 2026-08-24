import logging
import sqlite3
from pathlib import Path

from src.config import settings

logger = logging.getLogger(__name__)

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def connect_db() -> sqlite3.Connection:
    "conecta a la base de datos SQLite del proyecto, creando el archivo y el schema si no existen."
    db_path = Path(settings.DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    apply_schema(connection)

    logger.info(f"Conexion a base de datos establecida: {db_path}")
    return connection


def apply_schema(connection: sqlite3.Connection) -> None:
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    connection.executescript(schema_sql)
    connection.commit()
