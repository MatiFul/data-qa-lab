"""Reconcilia el contrato de Power BI contra marts y la API real."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from decimal import Decimal
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = PROJECT_ROOT / "reports" / "powerbi" / "reconciliation.json"

SUMMARY_QUERY = """
    select
        count(*)::integer as total_transactions,
        coalesce(sum(inconsistent_amount_flag), 0)::integer
            as inconsistent_transactions,
        coalesce(sum(has_no_items_flag), 0)::integer
            as transactions_without_items,
        round(
            coalesce(sum(inconsistent_amount_flag), 0)::numeric
            / nullif(count(*), 0),
            4
        ) as inconsistency_rate,
        min(transaction_date) as first_transaction_date,
        max(transaction_date) as last_transaction_date
    from dbt_marts.fct_transaction_quality
"""

DAILY_QUERY = """
    select
        sum(transaction_count)::integer as total_transactions,
        sum(inconsistent_transactions)::integer as inconsistent_transactions,
        sum(transactions_without_items)::integer as transactions_without_items,
        round(
            sum(inconsistent_transactions)::numeric
            / nullif(sum(transaction_count), 0),
            4
        ) as inconsistency_rate,
        min(transaction_date) as first_transaction_date,
        max(transaction_date) as last_transaction_date
    from dbt_marts.mart_daily_quality
"""


def json_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def normalized(row: dict[str, Any]) -> dict[str, Any]:
    return {key: json_value(value) for key, value in row.items()}


def database_settings() -> dict[str, Any]:
    password = os.getenv("QA_BI_PASSWORD")
    if not password:
        raise RuntimeError(
            "Falta QA_BI_PASSWORD. Definila en la terminal para qa_bi_reader."
        )
    return {
        "host": os.getenv("QA_DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("QA_DB_PORT", "5434")),
        "dbname": os.getenv("QA_DB_NAME", "qa_lab"),
        "user": os.getenv("QA_BI_USER", "qa_bi_reader"),
        "password": password,
        "connect_timeout": 5,
        "options": "-c default_transaction_read_only=on -c statement_timeout=10000",
        "row_factory": dict_row,
    }


def wait_for_api(url: str, process: subprocess.Popen, timeout: int = 20) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("La API se detuvo antes de quedar disponible.")
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.25)
    raise TimeoutError(f"La API no respondió a tiempo en {url}.")


def main() -> int:
    with psycopg.connect(**database_settings()) as connection:
        fact = normalized(connection.execute(SUMMARY_QUERY).fetchone())
        daily = normalized(connection.execute(DAILY_QUERY).fetchone())
        read_only = connection.execute(
            "show transaction_read_only"
        ).fetchone()["transaction_read_only"] == "on"
        can_write_mart = connection.execute(
            """
            select
                has_table_privilege(
                    current_user,
                    'dbt_marts.fct_transaction_quality',
                    'INSERT'
                )
                or has_table_privilege(
                    current_user,
                    'dbt_marts.fct_transaction_quality',
                    'UPDATE'
                )
                or has_table_privilege(
                    current_user,
                    'dbt_marts.fct_transaction_quality',
                    'DELETE'
                ) as can_write
            """
        ).fetchone()["can_write"]
        can_read_non_mart_layer = connection.execute(
            """
            select
                has_schema_privilege(current_user, 'raw', 'USAGE')
                or has_schema_privilege(
                    current_user,
                    'dbt_intermediate',
                    'USAGE'
                ) as can_read
            """
        ).fetchone()["can_read"]

    port = int(os.getenv("QA_POWERBI_API_PORT", "8015"))
    base_url = f"http://127.0.0.1:{port}"
    api_environment = os.environ.copy()
    api_environment["QA_DB_USER"] = "qa_user"
    api_environment["QA_DB_PASSWORD"] = os.getenv("QA_DB_PASSWORD", "")
    if not api_environment["QA_DB_PASSWORD"]:
        raise RuntimeError("Falta QA_DB_PASSWORD para consultar la API real.")

    log_path = PROJECT_ROOT / "reports" / "powerbi" / "api.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    with log_path.open("w", encoding="utf-8") as log_file:
        server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
            ],
            cwd=PROJECT_ROOT,
            env=api_environment,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            creationflags=creation_flags,
        )
        try:
            wait_for_api(f"{base_url}/health", server)
            with urllib.request.urlopen(
                f"{base_url}/api/quality/summary", timeout=5
            ) as response:
                api = json.loads(response.read().decode("utf-8"))
                api["inconsistency_rate"] = float(api["inconsistency_rate"])
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)

    checks = {
        "fact_matches_daily_mart": fact == daily,
        "fact_matches_api": fact == api,
        "reader_transaction_is_read_only": read_only,
        "reader_has_no_write_privilege_on_mart": not can_write_mart,
        "reader_cannot_read_non_mart_layers": not can_read_non_mart_layer,
    }
    payload = {
        "status": "success" if all(checks.values()) else "failed",
        "checks": checks,
        "sql_fact": fact,
        "sql_daily_mart": daily,
        "api_summary": api,
        "power_bi_expected_cards": {
            "Total Transactions": daily["total_transactions"],
            "Inconsistent Transactions": daily["inconsistent_transactions"],
            "Transactions Without Items": daily["transactions_without_items"],
            "Inconsistency Rate": daily["inconsistency_rate"],
        },
    }
    REPORT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
