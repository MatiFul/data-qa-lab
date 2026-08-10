"""Ejecuta Playwright en modo gate, visible, Inspector o con trazas."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ejecuta los recorridos web con evidencia adecuada al objetivo."
    )
    parser.add_argument(
        "--mode",
        choices=("gate", "headed", "inspector", "trace"),
        default="gate",
        help="gate=CI; headed=ventana; inspector=paso a paso; trace=evidencia completa",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("QA_APP_PORT", "8000")),
        help="Puerto usado si el script inicia una API temporal.",
    )
    parser.add_argument(
        "--base-url",
        help="Usa una API ya iniciada y evita crear otra instancia de Uvicorn.",
    )
    parser.add_argument(
        "--test",
        default="e2e",
        help="Archivo, directorio o node id de pytest. Por defecto: e2e.",
    )
    return parser.parse_args()


def playwright_command(args: argparse.Namespace, base_url: str) -> list[str]:
    output_directory = PROJECT_ROOT / "reports" / "playwright" / args.mode
    output_directory.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "pytest",
        args.test,
        "--base-url",
        base_url,
        "--browser",
        "chromium",
        "--output",
        str(output_directory / "artifacts"),
        "--junitxml",
        str(output_directory / "junit.xml"),
    ]

    if args.mode == "trace":
        command.extend(["--tracing", "on", "--screenshot", "on"])
    else:
        command.extend(
            ["--tracing", "retain-on-failure", "--screenshot", "only-on-failure"]
        )

    if args.mode in {"headed", "inspector"}:
        command.append("--headed")
    if args.mode != "inspector":
        command.append("-q")
    return command


def main() -> int:
    args = parse_args()
    base_url = args.base_url or f"http://127.0.0.1:{args.port}"
    environment = os.environ.copy()
    if args.mode == "inspector":
        environment["PWDEBUG"] = "1"

    server: subprocess.Popen | None = None
    log_handle = None
    try:
        if args.base_url is None:
            log_path = PROJECT_ROOT / "reports" / "playwright" / "api.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_handle = log_path.open("w", encoding="utf-8")
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            server = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "app.main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(args.port),
                ],
                cwd=PROJECT_ROOT,
                env=environment,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                creationflags=creation_flags,
            )
            wait_for_api(f"{base_url}/health", server)

        result = subprocess.run(
            playwright_command(args, base_url),
            cwd=PROJECT_ROOT,
            env=environment,
            check=False,
        )
        return result.returncode
    except (OSError, RuntimeError, TimeoutError) as error:
        print(f"No fue posible ejecutar Playwright: {error}")
        return 1
    finally:
        if server is not None:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)
        if log_handle is not None:
            log_handle.close()


if __name__ == "__main__":
    raise SystemExit(main())
