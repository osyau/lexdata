import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_CSV_PATH = os.getenv("LEXDATA_DEFAULT_CSV_PATH", "tests/mock_transaction.csv")
RULE_AMOUNT_THRESHOLD = float(os.getenv("LEXDATA_RULE_AMOUNT_THRESHOLD", "200.0"))
RULE_LOW_AMOUNT_THRESHOLD = float(os.getenv("LEXDATA_RULE_LOW_AMOUNT_THRESHOLD", "1.0"))
LOG_LEVEL = os.getenv("LEXDATA_LOG_LEVEL", "INFO")
DATABASE_PATH = os.getenv("LEXDATA_DATABASE_PATH", "data/lexdata.db")
ANOMALY_ZSCORE_THRESHOLD = float(os.getenv("LEXDATA_ANOMALY_ZSCORE_THRESHOLD", "3.0"))

# Reglas de negocio configurables. "monto_mayor_200" es la regla histórica del proyecto,
# preservada con su mismo nombre y umbral. "monto_bajo_sospechoso" es la segunda regla
# que demuestra que el motor ya soporta múltiples condiciones, no una función fija.
RULES = [
    {"name": "monto_mayor_200", "field": "amount", "operator": ">", "threshold": RULE_AMOUNT_THRESHOLD},
    {"name": "monto_bajo_sospechoso", "field": "amount", "operator": "<", "threshold": RULE_LOW_AMOUNT_THRESHOLD},
]
