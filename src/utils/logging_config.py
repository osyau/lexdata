import logging
import sys

from src.config import settings


def configure_logging():
    "configura el logging del proyecto una sola vez: nivel desde settings, salida UTF-8 legible en consola."
    # la consola de Windows por defecto no es UTF-8; sin esto, los acentos salen como '?'/mojibake.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    nivel = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        level=nivel,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        # logging.basicConfig() usa stderr por defecto; el código original (print) siempre
        # escribió a stdout, así que se preserva ese comportamiento explícitamente.
        stream=sys.stdout,
    )
