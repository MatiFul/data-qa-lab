from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_ROOT = PROJECT_ROOT / "reports"
DBT_REPORTS = REPORTS_ROOT / "dbt"
PYTEST_REPORTS = REPORTS_ROOT / "pytest"


def run_command(command: list[str]) -> int:
    print(f"\n> {' '.join(command)}", flush=True)
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=os.environ.copy(),
        check=False,
    ).returncode


def main() -> int:
    if not os.getenv("QA_DB_PASSWORD"):
        raise SystemExit(
            "Falta QA_DB_PASSWORD. Definila en la terminal, no en el repositorio."
        )

    DBT_REPORTS.mkdir(parents=True, exist_ok=True)
    PYTEST_REPORTS.mkdir(parents=True, exist_ok=True)

    dbt_exit_code = run_command(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "dbt_cli.py"),
            "build",
            "--project-dir",
            str(PROJECT_ROOT / "dbt"),
            "--profiles-dir",
            str(PROJECT_ROOT / "dbt"),
            "--target-path",
            str(DBT_REPORTS / "target"),
            "--log-path",
            str(DBT_REPORTS / "logs"),
        ]
    )

    pytest_exit_code: int | None = None
    if dbt_exit_code == 0:
        pytest_exit_code = run_command(
            [
                sys.executable,
                "-m",
                "pytest",
                "-p",
                "no:cacheprovider",
                "tests",
                "--ignore",
                "tests/api",
                "--junitxml",
                str(PYTEST_REPORTS / "junit.xml"),
            ]
        )
    else:
        print("\npytest omitido: dbt no aprobó el primer quality gate.")

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dbt_exit_code": dbt_exit_code,
        "pytest_exit_code": pytest_exit_code,
        "status": (
            "success"
            if dbt_exit_code == 0 and pytest_exit_code == 0
            else "failed"
        ),
    }
    (REPORTS_ROOT / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"\nResumen: {summary['status']}")
    print(f"Artefactos: {REPORTS_ROOT}")

    return 0 if summary["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
