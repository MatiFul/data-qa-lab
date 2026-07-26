"""Ejecuta las pruebas web y Postman contra una API temporal del lab."""

from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIRECTORY = PROJECT_ROOT / "reports"
POSTMAN_DIRECTORY = PROJECT_ROOT / "postman"
COLLECTION_FILE = POSTMAN_DIRECTORY / "data-qa-api.postman_collection.json"
NEWMAN_IMAGE = "postman/newman:6.1.3-alpine"


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


def newman_command(port: int, report_directory: Path) -> list[str]:
    command = ["docker", "run", "--rm"]
    if sys.platform.startswith("linux"):
        command.extend(["--network", "host"])
        newman_base_url = f"http://127.0.0.1:{port}"
    else:
        command.extend(
            ["--add-host", "host.docker.internal:host-gateway"]
        )
        newman_base_url = f"http://host.docker.internal:{port}"

    command.extend(
        [
            "-v",
            f"{POSTMAN_DIRECTORY}:/etc/newman:ro",
            "-v",
            f"{report_directory}:/reports",
            NEWMAN_IMAGE,
            "run",
            f"/etc/newman/{COLLECTION_FILE.name}",
            "--env-var",
            f"baseUrl={newman_base_url}",
            "--reporters",
            "cli,junit",
            "--reporter-junit-export",
            "/reports/junit.xml",
        ]
    )
    return command


def main() -> int:
    port = int(os.getenv("QA_APP_PORT", "8000"))
    local_base_url = f"http://127.0.0.1:{port}"
    playwright_reports = REPORTS_DIRECTORY / "playwright"
    postman_reports = REPORTS_DIRECTORY / "postman"
    playwright_reports.mkdir(parents=True, exist_ok=True)
    postman_reports.mkdir(parents=True, exist_ok=True)

    server_log_path = REPORTS_DIRECTORY / "api.log"
    creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    playwright_return_code = 1
    newman_return_code = 1
    with server_log_path.open("w", encoding="utf-8") as server_log:
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
            env=os.environ.copy(),
            stdout=server_log,
            stderr=subprocess.STDOUT,
            creationflags=creation_flags,
        )

        try:
            wait_for_api(f"{local_base_url}/health", server)
            playwright_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "e2e",
                    "--base-url",
                    local_base_url,
                    "--browser",
                    "chromium",
                    "--junitxml",
                    str(playwright_reports / "junit.xml"),
                    "-q",
                ],
                cwd=PROJECT_ROOT,
                check=False,
            )
            playwright_return_code = playwright_result.returncode
            newman_result = subprocess.run(
                newman_command(port, postman_reports),
                cwd=PROJECT_ROOT,
                check=False,
            )
            newman_return_code = newman_result.returncode
        except (OSError, RuntimeError, TimeoutError) as error:
            print(f"No fue posible completar la etapa 2: {error}")
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)

    if playwright_return_code or newman_return_code:
        print(
            "Etapa 2 con fallas: "
            f"Playwright={playwright_return_code}, "
            f"Newman={newman_return_code}."
        )
        return 1

    print("Etapa 2 OK: Playwright y Newman finalizaron sin fallas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
