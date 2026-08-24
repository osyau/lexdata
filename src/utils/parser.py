import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def validar_ruta_archivo(file_path):
    "valida la ruta de entrada antes de intentar abrirla; retorna un mensaje de error o None si es válida."
    ruta = Path(file_path)
    if not ruta.exists():
        return f"la ruta no existe: {file_path}"
    if not ruta.is_file():
        return f"la ruta no apunta a un archivo: {file_path}"
    return None


def parse_data(file_path):
    # Ojo: Aquí entra la data sucia (CSVs, Excels, etc.). Toca limpiarla y estructurarla.
    logger.info(f"Parseando archivo de datos: {file_path}")
    try:
        # 1. cargar el archivo como texto crudo; la conversión de tipos se hace explícita abajo.
        df = pd.read_csv(file_path, dtype=str)

        # Limpiamos espacios en los nombres de las columnas por si acaso
        df.columns = df.columns.str.strip()

        # Espacios sueltos en los valores rompen la inferencia de formato de fecha
        # de pandas cuando se parsea la columna completa de una vez (formato mixto).
        for columna in ('client_id', 'amount', 'transaction_date'):
            df[columna] = df[columna].str.strip()

        # 2. intentamos convertir cada campo crítico; lo que no convierte queda como NaN
        client_id_numeric = pd.to_numeric(df['client_id'], errors='coerce')
        amount_numeric = pd.to_numeric(df['amount'], errors='coerce')
        date_parsed = pd.to_datetime(df['transaction_date'], errors='coerce')

        # 3. cualquier fila con algún campo crítico inválido va a cuarentena, no se corrige sola
        invalid_mask = client_id_numeric.isna() | amount_numeric.isna() | date_parsed.isna()

        clean_index = df.index[~invalid_mask]
        clean_data = pd.DataFrame({
            'client_id': client_id_numeric.loc[clean_index].astype(int),
            'amount': amount_numeric.loc[clean_index].astype(float),
            'transaction_date': date_parsed.loc[clean_index],
        }).reset_index(drop=True)

        rejected_data = _build_rejected_rows(df, client_id_numeric, amount_numeric, date_parsed, invalid_mask)

        logger.info(f"Parseo completo: {len(clean_data)} filas validas, {len(rejected_data)} filas rechazadas.")
        return clean_data, rejected_data

    except Exception as e:
        #si el archivo no existe en la ruta indicada, atajo el error aquí
        logger.error(f"Error al parsear el archivo: {e}")
        return None, None


def _build_rejected_rows(df, client_id_numeric, amount_numeric, date_parsed, invalid_mask):
    "arma el detalle de motivo de rechazo por fila, preservando los valores crudos originales."
    motivos = []
    for idx in df.index[invalid_mask]:
        motivos_fila = []
        if pd.isna(client_id_numeric.loc[idx]):
            motivos_fila.append('client_id inválido')
        if pd.isna(amount_numeric.loc[idx]):
            motivos_fila.append('amount inválido')
        if pd.isna(date_parsed.loc[idx]):
            motivos_fila.append('fecha no parseable')
        motivos.append('; '.join(motivos_fila))

    # dtype=object explícito: el dtype "str" por defecto de pandas 3.x convierte None
    # de vuelta a NaN al construir la columna, lo cual rompe el NULL real que queremos guardar.
    rejected_data = pd.DataFrame({
        'raw_client_id': pd.Series([_valor_crudo(v) for v in df.loc[invalid_mask, 'client_id']], dtype=object),
        'raw_amount': pd.Series([_valor_crudo(v) for v in df.loc[invalid_mask, 'amount']], dtype=object),
        'raw_date': pd.Series([_valor_crudo(v) for v in df.loc[invalid_mask, 'transaction_date']], dtype=object),
        'reason': motivos,
    })
    return rejected_data.reset_index(drop=True)


def _valor_crudo(valor):
    "convierte un valor faltante (NaN/NA) a None; conserva el string original si existe."
    if pd.isna(valor):
        return None
    return valor
