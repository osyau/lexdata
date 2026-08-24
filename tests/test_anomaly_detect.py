import pandas as pd

from src.core.anomaly_detect import detect_amount_outliers


def test_detect_amount_outliers_encuentra_outlier_conocido():
    # 8 montos normales muy agrupados + 1 outlier claro. Con pocos datos, un solo valor
    # extremo infla mucho la desviación estándar (efecto de "masking"); por eso el lote
    # base va agrupado de cerca, para que el z-score del outlier supere el umbral.
    df = pd.DataFrame({
        'client_id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'amount': [100.0, 101.0, 99.0, 100.0, 102.0, 98.0, 101.0, 99.0, 5000.0],
    })

    outliers = detect_amount_outliers(df, z_score_threshold=2.0)

    assert len(outliers) == 1
    assert outliers.iloc[0]['amount'] == 5000.0
    assert outliers.iloc[0]['z_score'] > 2.0


def test_detect_amount_outliers_sin_variacion_no_marca_nada():
    df = pd.DataFrame({'client_id': [1, 2, 3], 'amount': [100.0, 100.0, 100.0]})

    outliers = detect_amount_outliers(df)

    assert outliers.empty


def test_detect_amount_outliers_con_pocos_datos_no_falla():
    df = pd.DataFrame({'client_id': [1], 'amount': [100.0]})

    outliers = detect_amount_outliers(df)

    assert outliers.empty
