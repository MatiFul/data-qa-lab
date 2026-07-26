import os
from collections.abc import Callable
from typing import Any

import psycopg
import pytest


def _database_settings() -> dict[str, Any]:
    return {
        "host": os.getenv("QA_DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("QA_DB_PORT", "5434")),
        "dbname": os.getenv("QA_DB_NAME", "qa_lab"),
        "user": os.getenv("QA_DB_USER", "qa_user"),
        "password": os.getenv("QA_DB_PASSWORD"),
        "connect_timeout": 5,
        "application_name": "data_qa_pytest",
        "options": "-c default_transaction_read_only=on -c statement_timeout=10000",
    }


@pytest.fixture(scope="session")
def db_connection() -> psycopg.Connection:
    settings = _database_settings()
    if not settings["password"]:
        pytest.fail(
            "Falta QA_DB_PASSWORD. Definila sólo en la terminal o en una configuración "
            "local no versionada."
        )

    try:
        connection = psycopg.connect(**settings)
    except psycopg.Error as error:
        pytest.fail(f"No fue posible conectar con PostgreSQL: {error}")

    yield connection
    connection.close()


@pytest.fixture
def db_scalar(
    db_connection: psycopg.Connection,
) -> Callable[[str, tuple[Any, ...] | None], Any]:
    def execute(query: str, params: tuple[Any, ...] | None = None) -> Any:
        with db_connection.cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row is None:
                pytest.fail("La consulta de QA no devolvió resultados.")
            return row[0]

    return execute
