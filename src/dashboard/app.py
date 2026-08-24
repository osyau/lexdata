import sys
from pathlib import Path

# streamlit ejecuta este archivo como script suelto, no como parte del paquete "src",
# asi que la raiz del proyecto no queda en sys.path por defecto. Se agrega a mano.
_RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
if str(_RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(_RAIZ_PROYECTO))

import pandas as pd
import streamlit as st

from src.core.report import generar_reporte
from src.database.connection import connect_db
from src.database.repositories import AlertRepository, RejectedRowRepository, TransactionRepository

st.set_page_config(page_title="LexData - Panel de auditoria", layout="wide")


def _a_dataframe(objetos, columnas):
    return pd.DataFrame([{col: getattr(obj, col) for col in columnas} for obj in objetos])


def main():
    st.title("LexData — Panel de auditoria")
    st.caption("Vista de solo lectura sobre lo que ya proceso `python -m src.main`.")

    # conexion nueva por rerun: st.cache_resource compartiria esta conexion SQLite entre
    # threads distintos de Streamlit, y sqlite3 no lo permite por defecto (check_same_thread).
    conexion = connect_db()
    transaction_repo = TransactionRepository(conexion)
    alert_repo = AlertRepository(conexion)
    rejected_repo = RejectedRowRepository(conexion)

    if transaction_repo.count() == 0:
        st.info("Todavia no hay datos procesados. Corre `python -m src.main <archivo.csv>` primero.")
        return

    reporte = generar_reporte(transaction_repo, alert_repo, rejected_repo)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Transacciones procesadas", reporte.total_transacciones)
    col2.metric("Alertas generadas", reporte.total_alertas)
    col3.metric("Filas rechazadas", reporte.total_rechazadas)
    col4.metric("Tasa de rechazo", f"{reporte.tasa_rechazo:.1%}")

    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("Alertas por regla")
        if reporte.alertas_por_regla:
            df_reglas = pd.DataFrame(reporte.alertas_por_regla, columns=["regla", "alertas"])
            st.bar_chart(df_reglas.set_index("regla"))
        else:
            st.caption("Sin alertas registradas todavia.")

    with col_der:
        st.subheader("Clientes mas senalados")
        if reporte.clientes_mas_senalados:
            df_clientes = pd.DataFrame(reporte.clientes_mas_senalados, columns=["client_id", "alertas"])
            st.dataframe(df_clientes, width='stretch', hide_index=True)
        else:
            st.caption("Sin alertas registradas todavia.")

    st.subheader("Transacciones")
    st.dataframe(
        _a_dataframe(transaction_repo.all(), ["id", "client_id", "amount", "transaction_date", "ingested_at"]),
        width='stretch',
        hide_index=True,
    )

    st.subheader("Alertas")
    alertas = alert_repo.all()
    if alertas:
        st.dataframe(
            _a_dataframe(alertas, ["id", "transaction_id", "rule_name", "source", "triggered_at"]),
            width='stretch',
            hide_index=True,
        )
    else:
        st.caption("Sin alertas registradas todavia.")

    st.subheader("Filas rechazadas")
    rechazadas = rejected_repo.all()
    if rechazadas:
        st.dataframe(
            _a_dataframe(rechazadas, ["id", "raw_client_id", "raw_amount", "raw_date", "reason", "ingested_at"]),
            width='stretch',
            hide_index=True,
        )
    else:
        st.caption("Sin filas rechazadas.")


main()
