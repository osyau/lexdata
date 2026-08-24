import subprocess
import sys


def _run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "src.main", *args],
        capture_output=True,
        text=True,
    )


def test_cli_help_muestra_uso():
    resultado = _run_cli("--help")

    assert resultado.returncode == 0
    assert "usage" in resultado.stdout.lower()
    assert "ruta_csv" in resultado.stdout


def test_cli_exit_code_0_en_corrida_valida():
    resultado = _run_cli("tests/mock_transaction.csv")

    assert resultado.returncode == 0


def test_cli_exit_code_distinto_de_0_en_ruta_invalida():
    resultado = _run_cli("esta/ruta/no/existe.csv")

    assert resultado.returncode != 0
