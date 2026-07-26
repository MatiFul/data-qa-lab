# Guía operativa del laboratorio

## Alcance

Esta guía permite iniciar, verificar, ejecutar y detener el laboratorio sin reconstruirlo. No utiliza `docker compose down -v`, por lo que los volúmenes persistentes se conservan.

## Orden de inicio

### 1. Docker Desktop

Docker Desktop debe estar iniciado antes de ejecutar comandos Docker.

### 2. Red compartida

PostgreSQL, Airflow y OpenMetadata utilizan la red:

```text
om-lab_app_net
```

OpenMetadata la crea normalmente. Si se desea usar sólo el núcleo de Data QA y la red no existe:

```powershell
docker network create om-lab_app_net
```

### 3. PostgreSQL

Desde `data-qa-lab`:

```powershell
docker compose --file docker\docker-compose.postgres.yml up --detach
```

Verificación:

```powershell
docker ps --filter name=qa_lab_postgres
docker exec qa_lab_postgres pg_isready -U qa_user -d qa_lab
```

PostgreSQL se publica localmente en el puerto `5434`.

### 4. Airflow

Desde `airflow-lab\Compose`:

```powershell
docker compose --file docker-compose.yaml up --detach
```

Verificación:

```powershell
docker ps --filter name=airflow_
docker exec airflow_scheduler airflow dags list-import-errors --output=json
```

Interfaz:

```text
http://localhost:8081
```

### 5. OpenMetadata opcional

Iniciarlo únicamente para practicar catálogo, búsqueda o lineage.

Desde `om-lab`:

```powershell
docker compose --file docker-compose.yml up --detach
```

Interfaz:

```text
http://localhost:8585
```

## Preparar los datos sin Airflow

Desde `data-qa-lab`, definir la conexión:

```powershell
$env:QA_DB_HOST="127.0.0.1"
$env:QA_DB_PORT="5434"
$env:QA_DB_NAME="qa_lab"
$env:QA_DB_USER="qa_user"
$env:QA_DB_PASSWORD="<contraseña local>"
```

Generar y cargar:

```powershell
.\.venv\Scripts\python.exe data_generator\generate_dataset.py
.\.venv\Scripts\python.exe scripts\bootstrap_postgres.py
```

## Ejecutar todos los controles

```powershell
.\.venv\Scripts\python.exe scripts\run_quality_checks.py
.\.venv\Scripts\python.exe scripts\run_app_checks.py
```

Resultado normal:

```text
dbt PASS=37, ERROR=0
pytest 24 passed, 4 xfailed
Playwright 2 passed
Newman 4 requests, 8 assertions, 0 failed
reports/summary.json = success
```

El segundo comando inicia la API sólo durante la prueba y la detiene al terminar. Usa el Chromium propio de Playwright y Newman en Docker; Chrome puede permanecer cerrado.

## Abrir la aplicación para explorarla

Con las variables de conexión ya definidas:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Direcciones:

```text
Panel web:         http://127.0.0.1:8000
Documentación API: http://127.0.0.1:8000/docs
Health check:      http://127.0.0.1:8000/health
```

La aplicación consulta `dbt_marts` con una conexión de sólo lectura. Para detenerla, usar `Ctrl+C` en la misma terminal.

## Ejecutar desde Airflow

En la UI, abrir:

```text
qa_pipeline_postgres_v1
```

Una ejecución normal utiliza el máximo de inconsistencias del 5 %. Para una simulación pedagógica puede indicarse en la configuración:

```json
{
  "qa_max_inconsistency_rate": 0.01
}
```

Con ese valor, `run_dbt_build` debe fallar y bloquear pytest.

## Orden de detención

Detener primero los consumidores y al final OpenMetadata, que administra la red compartida.

Airflow:

```powershell
docker compose --file airflow-lab\Compose\docker-compose.yaml down
```

PostgreSQL:

```powershell
docker compose --file data-qa-lab\docker\docker-compose.postgres.yml down
```

OpenMetadata:

```powershell
docker compose --file om-lab\docker-compose.yml down
```

No agregar `--volumes` ni `-v` salvo que se desee eliminar expresamente las bases persistentes.

## Reinicio

Para reiniciar un servicio sin eliminarlo:

```powershell
docker restart qa_lab_postgres
docker restart airflow_apiserver airflow_scheduler airflow_dag_processor
```

Si se modificó la imagen de Airflow:

```powershell
docker compose --file airflow-lab\Compose\docker-compose.yaml build
docker compose --file airflow-lab\Compose\docker-compose.yaml up --detach
```

## Diagnóstico rápido

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
docker logs --tail 100 airflow_scheduler
docker logs --tail 100 qa_lab_postgres
```

Las evidencias detalladas de una tarea se consultan desde la UI de Airflow. Las pruebas locales conservan sus artefactos dentro de `data-qa-lab\reports`.
