# LexData | Auditoría Inteligente de Datos Empresariales
LexData es una plataforma de software desarrollada en Python diseñada para la auditoría inteligente, análisis y detección de anomalías en datos transaccionales empresariales. El sistema integra un motor de reglas de negocio configurable y un detector estadístico de anomalías (z-score) para identificar patrones irregulares, automatizar el control de calidad de la información y generar reportes de auditoría.

El proyecto está construido bajo una arquitectura modular por capas, con persistencia real en SQLite, configuración centralizada por variables de entorno, y una suite de tests automatizados con `pytest`.

---

## Arquitectura del Sistema (Capas)

*   **A. Capa de Base de Datos:** SQLite real (`src/database/`). El schema (`schema.sql`), los modelos (`models.py`) y los repositorios parametrizados (`repositories.py`) están implementados; no hay SQL construido por concatenación en ningún punto.
*   **B. Motor de Reglas:** reglas de negocio configurables (`src/core/rule_engine.py`), definidas como datos en `src/config/settings.py` en vez de funciones fijas. Cada regla evaluada que se cumple genera una alerta persistida.
*   **C. Detección de Anomalías:** primer detector estadístico real (`src/core/anomaly_detect.py`), outliers de monto por z-score sobre el lote procesado.
*   **D. Dashboard & Reportes:** dos salidas — un reporte agregado exportable a CSV/consola (`src/core/report.py`) y un dashboard de solo lectura en Streamlit (`src/dashboard/app.py`) sobre lo ya persistido.

Todas las capas están conectadas de punta a punta: no hay datos simulados ni conexiones mockeadas.

```
  [ Capa D: Dashboard (Streamlit) / Reportes (CSV) ]
                    ▲
                    │  lee lo ya persistido
                    │
  [ Capa B: Motor de Reglas ] ◄──(evalúa junto a)──► [ Capa C: Detección de Anomalías ]
                    │                                            │
                    └──────────────── persisten alertas ─────────┘
                    ▼
  [ Capa A: SQLite — transactions / rule_alerts / rejected_rows ]
                    ▲
                    │
  [ Parser + cuarentena de datos invalidos (src/utils/parser.py) ]
                    ▲
                    │
              [ CSV de entrada ]
```

Filas con `client_id`, `amount` o `transaction_date` inválidos no se corrigen ni se descartan en silencio: se separan en cuarentena (`rejected_rows`) con el motivo exacto del rechazo.

---

## Stack Tecnológico
*   **Lenguaje base:** Python 3.13
*   **Datos:** `pandas` 3.0.3, `numpy` 2.4.6
*   **Persistencia:** SQLite (`sqlite3`, estándar de Python) — sin ORM
*   **Configuración:** `python-dotenv` (variables de entorno, ver `.env.example`)
*   **Dashboard:** `Streamlit`
*   **Tests:** `pytest`
*   **CLI:** `argparse` + `logging` (estándar de Python)
*   **Control de versiones:** Git & GitHub

---

## Estructura del Proyecto
```text
LEXDATA/
├── src/
│   ├── main.py                     # punto de entrada CLI
│   ├── config/
│   │   └── settings.py             # config centralizada (env vars, reglas, umbrales)
│   ├── core/
│   │   ├── rule_engine.py          # motor de reglas configurable
│   │   ├── anomaly_detect.py       # detector de anomalias (z-score)
│   │   └── report.py               # agregacion de reportes + export CSV
│   ├── database/
│   │   ├── connection.py           # conexion SQLite + auto-aplicacion de schema
│   │   ├── schema.sql              # DDL: transactions, rule_alerts, rejected_rows
│   │   ├── models.py                # dataclasses: Transaction, RuleAlert, RejectedRow
│   │   └── repositories.py         # acceso a datos parametrizado
│   ├── dashboard/
│   │   └── app.py                  # dashboard Streamlit (solo lectura)
│   └── utils/
│       ├── parser.py               # parseo + cuarentena de filas invalidas
│       └── logging_config.py       # configuracion de logging del proyecto
├── tests/                          # suite pytest (parser, repos, reglas, anomalias, CLI, reportes)
├── data/                           # base SQLite local (gitignored, se crea automaticamente)
├── .env.example                    # plantilla de configuracion
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Instalación y Uso

### Prerrequisitos
* Python 3.10 o superior
* Git

### Clonar e Instalar
```bash
git clone https://github.com/osyau/lexdata.git
cd lexdata
python -m venv venv
# Windows (Git Bash, CMD o PowerShell):
.\venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### Configuración (opcional)
```bash
cp .env.example .env
```
Todas las variables tienen un valor por defecto razonable; `.env` solo hace falta si querés ajustar rutas, umbrales de reglas o el nivel de log. Ver `.env.example` para la lista completa.

### Correr la auditoría (CLI)
```bash
python -m src.main tests/mock_transaction.csv
# o, para exportar el reporte agregado:
python -m src.main tests/mock_transaction.csv --export reporte.csv
python -m src.main --help
```
Esto parsea el CSV, separa filas inválidas en cuarentena, evalúa las reglas y el detector de anomalías, y persiste todo en `data/lexdata.db`.

### Ver el dashboard
```bash
streamlit run src/dashboard/app.py
```

### Correr los tests
```bash
pytest
```

---

## Estado del Proyecto

LexData tiene un **núcleo funcional de punta a punta**: CSV → cuarentena de datos inválidos → persistencia real en SQLite → reglas configurables + detección de anomalías → alertas persistidas → reporte exportable y dashboard de solo lectura.

### Completado
- [x] Configuración centralizada por variables de entorno
- [x] Persistencia real en SQLite (schema, modelos, repositorios parametrizados)
- [x] Cuarentena de datos inválidos con motivo de rechazo (sin coerción silenciosa a cero)
- [x] Validación de ruta de entrada antes de tocar disco/base de datos
- [x] Motor de reglas configurable (múltiples reglas, no una función fija)
- [x] Primer detector de anomalías (outliers de monto por z-score)
- [x] CLI con `argparse` (`--help`, `--export`) y logging estructurado
- [x] Reporte de auditoría agregado, exportable a CSV
- [x] Dashboard de solo lectura en Streamlit
- [x] Suite de tests automatizados con `pytest`

### Pendiente / roadmap
- [ ] Vectorizar la evaluación de reglas y el detector de anomalías (hoy es fila por fila; se justifica solo con volumen real de datos)
- [ ] Ampliar el catálogo de reglas y algoritmos de detección de anomalías
- [ ] Reglas administrables sin tocar código (hoy viven en `settings.py`)
- [ ] Autenticación / multiusuario en el dashboard
- [ ] Motor SQL alternativo (Postgres/MySQL) si el proyecto necesita concurrencia real más allá de SQLite
