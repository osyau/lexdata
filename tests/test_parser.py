from src.utils.parser import parse_data, validar_ruta_archivo

MOCK_CSV_PATH = "tests/mock_transaction.csv"


def test_parse_data_separates_clean_and_rejected_rows():
    clean_df, rejected_df = parse_data(MOCK_CSV_PATH)

    assert len(clean_df) == 1
    assert len(rejected_df) == 3

    clean_row = clean_df.iloc[0]
    assert clean_row["client_id"] == 1001
    assert clean_row["amount"] == 250.5


def test_parse_data_rejected_rows_have_correct_reasons():
    _, rejected_df = parse_data(MOCK_CSV_PATH)

    reasons = list(rejected_df["reason"])

    assert "client_id inválido" in reasons
    assert "amount inválido" in reasons
    assert "fecha no parseable" in reasons


def test_parse_data_does_not_zero_fill_invalid_values():
    _, rejected_df = parse_data(MOCK_CSV_PATH)

    client_id_row = rejected_df[rejected_df["reason"] == "client_id inválido"].iloc[0]

    assert client_id_row["raw_client_id"] is None
    assert client_id_row["raw_amount"] == "120.00"


def test_parse_data_rejected_rows_preserve_none_via_itertuples():
    # main.py recorre df_rechazado con itertuples(), no con iterrows(): iterrows()
    # reconstruye cada fila como una Serie homogénea y reintroduce NaN donde debería
    # haber None. Este test fija ese comportamiento como regresión.
    _, rejected_df = parse_data(MOCK_CSV_PATH)

    filas = list(rejected_df.itertuples(index=False))
    fila_sin_client_id = next(f for f in filas if f.reason == "client_id inválido")

    assert fila_sin_client_id.raw_client_id is None


def test_validar_ruta_archivo_rechaza_ruta_inexistente():
    error = validar_ruta_archivo("esta/ruta/no/existe.csv")

    assert error is not None
    assert "no existe" in error


def test_validar_ruta_archivo_rechaza_directorio(tmp_path):
    error = validar_ruta_archivo(str(tmp_path))

    assert error is not None
    assert "no apunta a un archivo" in error


def test_validar_ruta_archivo_acepta_archivo_existente():
    assert validar_ruta_archivo(MOCK_CSV_PATH) is None
