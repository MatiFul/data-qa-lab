import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import psycopg
from psycopg.rows import dict_row


def database_settings() -> dict[str, Any]:
    """Construye la conexión desde variables de entorno, sin guardar secretos."""
    password = os.getenv("QA_DB_PASSWORD")
    if not password:
        raise RuntimeError(
            "Falta QA_DB_PASSWORD. Definila en la terminal o en una configuración "
            "local no versionada."
        )

    return {
        "host": os.getenv("QA_DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("QA_DB_PORT", "5434")),
        "dbname": os.getenv("QA_DB_NAME", "qa_lab"),
        "user": os.getenv("QA_DB_USER", "qa_user"),
        "password": password,
        "connect_timeout": 5,
        "application_name": "data_qa_api",
        "options": "-c default_transaction_read_only=on -c statement_timeout=10000",
        "row_factory": dict_row,
    }


@contextmanager
def read_only_connection() -> Iterator[psycopg.Connection]:
    """Abre una conexión corta y forzada a modo de sólo lectura."""
    with psycopg.connect(**database_settings()) as connection:
        yield connection
