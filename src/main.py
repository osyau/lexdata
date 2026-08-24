import argparse
import logging
import sys

from src.config import settings
from src.utils.logging_config import configure_logging
from src.utils.parser import parse_data, validar_ruta_archivo
from src.database import connect_db
from src.database.models import RejectedRow, RuleAlert, Transaction
from src.database.repositories import AlertRepository, RejectedRowRepository, TransactionRepository
from src.core.rule_engine import evaluate_rules
from src.core.anomaly_detect import detect_amount_outliers
from src.core.report import generar_reporte, formatear_reporte_consola, exportar_csv

logger = logging.getLogger(__name__)


def init_project():
    """Función para inicializar el proyecto, configurando el entorno y preparando los recursos necesarios."""
    logger.info("Inicializando el proyecto...")
    # Aquí irá más adelante la lectura de archivos/conexiones database
    # Si todo está listo, permitimos el arranque
    return True


def _parse_args():
    parser = argparse.ArgumentParser(
        prog="lexdata",
        description="LexData: audita un archivo CSV de transacciones contra reglas de negocio y deteccion de anomalias.",
    )
    parser.add_argument(
        "ruta_csv",
        nargs="?",
        default=settings.DEFAULT_CSV_PATH,
        help=f"ruta al archivo CSV de transacciones a procesar (default: {settings.DEFAULT_CSV_PATH})",
    )
    parser.add_argument(
        "--export",
        metavar="ARCHIVO_CSV",
        default=None,
        help="ruta donde exportar el reporte de auditoria en CSV (opcional)",
    )
    return parser.parse_args()


def main():
    configure_logging()
    args = _parse_args()

    logger.info("=========================================")
    logger.info("       LEXDATA - SYSTEM INITIALIZED      ")
    logger.info("=========================================")

    if not init_project():
        logger.error("No se pudo inicializar el proyecto.")
        sys.exit(1)

    logger.info("Proyecto inicializado correctamente.")

    # 1. Validar la ruta de entrada antes de tocar la base de datos o el disco
    ruta_datos = args.ruta_csv
    error_ruta = validar_ruta_archivo(ruta_datos)
    if error_ruta:
        logger.error(error_ruta)
        sys.exit(1)

    # 2. Conectar a la Base de Datos
    logger.info("Conectando a la base de datos...")
    db_connection = connect_db()
    if not db_connection:
        logger.error("Fallo la conexion a la base de datos.")
        sys.exit(1)

    # 3. Parsear y limpiar los datos de negocio
    df_limpio, df_rechazado = parse_data(ruta_datos)

    if df_limpio is None or df_limpio.empty:
        logger.error("No se pudieron procesar los datos o el archivo esta vacio.")
        sys.exit(1)

    # 3.1 filas que no pasaron validación van a cuarentena, no se descartan sin registro
    rejected_repo = RejectedRowRepository(db_connection)
    if df_rechazado is not None and not df_rechazado.empty:
        logger.warning(f"{len(df_rechazado)} fila(s) rechazada(s) por datos invalidos:")
        # nota: se usa itertuples() en vez de iterrows() porque iterrows() reconstruye
        # cada fila como una Serie homogénea y eso reintroduce NaN donde debería ir None.
        for fila_rechazada in df_rechazado.itertuples(index=False):
            datos_rechazo = fila_rechazada._asdict()
            logger.warning(f"  Rechazada: {datos_rechazo}")
            rejected_repo.insert(RejectedRow(
                raw_client_id=datos_rechazo.get('raw_client_id'),
                raw_amount=datos_rechazo.get('raw_amount'),
                raw_date=datos_rechazo.get('raw_date'),
                reason=datos_rechazo['reason'],
            ))

    # 4. motor de reglas: se evalua cada transaccion y se persiste todo
    logger.info("Ejecutando el motor de reglas sobre los datos limpios...")
    transaction_repo = TransactionRepository(db_connection)
    alert_repo = AlertRepository(db_connection)

    transaction_ids_por_indice = {}

    # Como los DataFrames tienen muchas filas, lo normal es recorrerlas
    # o pasarle el lote completo a tu motor. Aquí te dejo un ejemplo fila por fila:
    for indice, fila in df_limpio.iterrows():
        # Todo lo que esté aquí adentro debe llevar 1 tabulación o 4 espacios más que el 'for'
        datos_transaccion = dict(fila)

        transaction_id = transaction_repo.insert(Transaction(
            client_id=datos_transaccion.get('client_id', 0),
            amount=datos_transaccion.get('amount', 0.0),
            transaction_date=datos_transaccion.get('transaction_date'),
        ))
        transaction_ids_por_indice[indice] = transaction_id

        # Evaluamos la transacción contra todas las reglas configuradas (ver settings.RULES)
        reglas_cumplidas = evaluate_rules(datos_transaccion, settings.RULES)

        for nombre_regla in reglas_cumplidas:
            logger.warning(f"Alerta/regla: transaccion indice {indice} cumple '{nombre_regla}': {datos_transaccion}")
            alert_repo.insert(RuleAlert(transaction_id=transaction_id, rule_name=nombre_regla, source="regla"))

    # 5. deteccion de anomalias: requiere ver el lote completo, no fila por fila
    logger.info("Ejecutando deteccion de anomalias (z-score) sobre los montos...")
    outliers = detect_amount_outliers(df_limpio, settings.ANOMALY_ZSCORE_THRESHOLD)

    for indice, fila_outlier in outliers.iterrows():
        transaction_id = transaction_ids_por_indice[indice]
        logger.warning(
            f"Alerta/anomalia: transaccion indice {indice} outlier de monto "
            f"(z_score={fila_outlier['z_score']:.2f}): {dict(fila_outlier)}"
        )
        alert_repo.insert(RuleAlert(transaction_id=transaction_id, rule_name="anomalia_monto_zscore", source="anomalia"))

    # 6. reporte de auditoria: agrega lo persistido, se muestra siempre y se exporta si se pidio
    logger.info("Procesamiento LexData finalizado con exito.")
    reporte = generar_reporte(transaction_repo, alert_repo, rejected_repo)
    logger.info("\n" + formatear_reporte_consola(reporte))

    if args.export:
        exportar_csv(reporte, args.export)
        logger.info(f"Reporte exportado a: {args.export}")


if __name__ == "__main__":
    main()
