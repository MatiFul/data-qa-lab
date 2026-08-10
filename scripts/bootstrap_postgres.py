from __future__ import annotations

import os
from pathlib import Path

import psycopg


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_ROOT = PROJECT_ROOT / "sql" / "postgres"
DATA_ROOT = PROJECT_ROOT / "data_generator" / "output"

DDL_FILES = [
    SQL_ROOT / "ddl" / "raw" / "01_create_raw_tables.sql",
    SQL_ROOT / "ddl" / "security" / "01_create_qa_bi_reader.sql",
]

RAW_FILES = [
    ("clientes_raw.csv", "raw.clientes_raw"),
    ("cuentas_raw.csv", "raw.cuentas_raw"),
    ("productos_raw.csv", "raw.productos_raw"),
    ("estados_transaccion_raw.csv", "raw.estados_transaccion_raw"),
    ("canales_raw.csv", "raw.canales_raw"),
    ("sucursales_raw.csv", "raw.sucursales_raw"),
    ("transacciones_raw.csv", "raw.transacciones_raw"),
    ("items_transaccion_raw.csv", "raw.items_transaccion_raw"),
]

def database_settings() -> dict[str, object]:
    password = os.getenv("QA_DB_PASSWORD", "")
    if not password:
        raise SystemExit(
            "Falta QA_DB_PASSWORD. Definila en la terminal, no en el repositorio."
        )

    return {
        "host": os.getenv("QA_DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("QA_DB_PORT", "5434")),
        "dbname": os.getenv("QA_DB_NAME", "qa_lab"),
        "user": os.getenv("QA_DB_USER", "qa_user"),
        "password": password,
    }


def execute_sql_file(
    cursor: psycopg.Cursor[tuple[object, ...]],
    sql_path: Path,
) -> None:
    cursor.execute(sql_path.read_text(encoding="utf-8"))


def load_raw_files(cursor: psycopg.Cursor[tuple[object, ...]]) -> None:
    missing_files = [
        str(DATA_ROOT / file_name)
        for file_name, _ in RAW_FILES
        if not (DATA_ROOT / file_name).is_file()
    ]
    if missing_files:
        raise FileNotFoundError(
            "Faltan CSV. Ejecutá primero data_generator/generate_dataset.py:\n"
            + "\n".join(missing_files)
        )

    for _, table_name in RAW_FILES:
        cursor.execute(f"TRUNCATE TABLE {table_name}")

    for file_name, table_name in RAW_FILES:
        csv_path = DATA_ROOT / file_name
        with cursor.copy(
            f"COPY {table_name} FROM STDIN WITH (FORMAT csv, HEADER true)"
        ) as copy:
            with csv_path.open("r", encoding="utf-8") as csv_file:
                while chunk := csv_file.read(64 * 1024):
                    copy.write(chunk)


def main() -> None:
    with psycopg.connect(**database_settings()) as connection:
        with connection.cursor() as cursor:
            for sql_path in DDL_FILES:
                execute_sql_file(cursor, sql_path)

            load_raw_files(cursor)

            cursor.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM raw.transacciones_raw),
                    (SELECT COUNT(*) FROM raw.items_transaccion_raw)
                """
            )
            transactions, items = cursor.fetchone()

    print(
        "Carga raw completada: "
        f"transacciones={transactions}, items={items}. "
        "Ejecutá luego dbt build o scripts/run_quality_checks.py."
    )


if __name__ == "__main__":
    main()
