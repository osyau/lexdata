import pandas as pd

DEFAULT_Z_SCORE_THRESHOLD = 3.0


def detect_amount_outliers(df, z_score_threshold=DEFAULT_Z_SCORE_THRESHOLD):
    "detecta transacciones cuyo monto se aleja demasiado del promedio del lote (outlier por z-score)."
    if df.empty or len(df) < 2:
        return _resultado_vacio(df)

    media = df['amount'].mean()
    desviacion = df['amount'].std()

    if not desviacion or pd.isna(desviacion):
        # sin variación en los montos (o desviación indefinida), no hay outliers que detectar
        return _resultado_vacio(df)

    z_scores = (df['amount'] - media) / desviacion
    es_outlier = z_scores.abs() > z_score_threshold

    outliers = df.loc[es_outlier].copy()
    outliers['z_score'] = z_scores.loc[es_outlier]
    return outliers


def _resultado_vacio(df):
    columnas = list(df.columns) + ['z_score']
    return pd.DataFrame(columns=columnas)
