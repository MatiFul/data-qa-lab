# Guía operativa del laboratorio

## Alcance

Esta guía permite iniciar, verificar, ejecutar y detener el laboratorio sin reconstruirlo. No utiliza `docker compose down -v`, por lo que los volúmenes persistentes se conservan.

## Elegir la terminal antes de copiar comandos

PowerShell y CMD ejecutan los mismos programas, pero no usan la misma sintaxis para
variables de entorno. El prompt permite reconocerlos:

| Terminal | Ejemplo de prompt | Definir la contraseña local |
|---|---|---|
| PowerShell | `PS C:\...>` | `$env:QA_DB_PASSWORD="<contraseña local>"` |
| CMD | `C:\...>` | `set QA_DB_PASSWORD=<contraseña local>` |

No pegar una línea que comienza con `$env:` en CMD. Para evitar depender del Python
global, todos los comandos del lab deben usar explícitamente:

```text
.\.venv\Scripts\python.exe
```

En ambos casos, ubicarse primero en la raíz de `data-qa-lab`. En PowerShell:

```powershell
Set-Location "<ruta-del-workspace>\data-qa-lab"
```

En CMD:

```bat
cd /d "<ruta-del-workspace>\data-qa-lab"
```

## Qué iniciar según la práctica

No es necesario encender todo:

| Objetivo | Servicios necesarios |
|---|---|
| SQL y DBeaver | Docker Desktop + PostgreSQL |
| Pipeline completo | Docker Desktop + PostgreSQL + Airflow |
| Catálogo y lineage | Agregar OpenMetadata |
| API y panel web | PostgreSQL + FastAPI; Airflow no necesita quedar abierto si los marts ya existen |
| Power BI | PostgreSQL; los marts deben estar construidos |

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

MySQL persiste en el volumen Docker nombrado
`data-qa-openmetadata-mysql`. El antiguo directorio
`om-lab/docker-volume/db-data` se conserva únicamente como recuperación y no debe
volver a configurarse como datadir activo. Antes de modificar metadata o ejecutar
una recuperación, consultar:

```text
om-lab/recovery-backups/20260809_pre_named_volume/BACKUP_MANIFEST.md
```

Comprobar el montaje activo:

```powershell
docker inspect openmetadata_mysql --format "{{range .Mounts}}{{.Type}}|{{.Name}}|{{.Destination}}{{end}}"
```

Resultado esperado:

```text
volume|data-qa-openmetadata-mysql|/var/lib/mysql
```

Interfaz:

```text
http://localhost:8585
```

### Sincronizar dbt con OpenMetadata

La integración usa los tres artefactos oficiales de dbt:

- `manifest.json`: modelos, SQL compilado, dependencias y descripciones;
- `catalog.json`: columnas y tipos observados en PostgreSQL;
- `run_results.json`: resultado de la última ejecución de tests.

Primero ejecutar el gate de datos y generar el catálogo con una ruta absoluta. En
PowerShell:

```powershell
$env:QA_DB_PASSWORD="<contraseña local>"
.\.venv\Scripts\python.exe scripts\run_quality_checks.py
$target=(Resolve-Path "reports\dbt").Path + "\target"
$logs=(Resolve-Path "reports\dbt").Path + "\logs"
.\.venv\Scripts\python.exe scripts\dbt_cli.py docs generate --project-dir dbt --profiles-dir dbt --target-path $target --log-path $logs
.\.venv\Scripts\python.exe scripts\sync_openmetadata_dbt.py
```

En CMD:

```bat
set QA_DB_PASSWORD=<contraseña local>
.\.venv\Scripts\python.exe scripts\run_quality_checks.py
.\.venv\Scripts\python.exe scripts\dbt_cli.py docs generate --project-dir dbt --profiles-dir dbt --target-path "%CD%\reports\dbt\target" --log-path "%CD%\reports\dbt\logs"
.\.venv\Scripts\python.exe scripts\sync_openmetadata_dbt.py
```

El sincronizador copia los artefactos a un directorio temporal del contenedor,
reutiliza la credencial del bot que OpenMetadata ya administra y elimina esa copia
al terminar. No escribe JWT ni contraseñas en el repositorio. También completa las
tres aristas críticas y los 23 mapeos de columnas alrededor de
`fct_transaction_quality`, porque el parser dbt no infiere de forma confiable todas
las expresiones derivadas.

Resultado esperado:

```text
Workflow Success %: 100.0
Linaje crítico validado: 3 aristas y 23 mapeos de columnas.
Sincronización dbt -> OpenMetadata completada.
```

Puede aparecer un aviso que indica que no existe un usuario o equipo llamado
`qa_user`. Es esperado: ése es el owner técnico de PostgreSQL, no una persona del
catálogo, y no invalida la ingesta.

### Comprobar la metadata desde la interfaz

1. Buscar `fct_transaction_quality` y abrir el activo.
2. En **Resumen** comprobar su descripción y en **Esquema** abrir las descripciones
   de `amount_difference`, `has_no_items_flag` e `inconsistent_amount_flag`.
3. En **Observabilidad → Calidad de datos** comprobar los 12 resultados `Éxito`,
   incluidos
   `assert_quality_flags_match_calculation`, `assert_mart_matches_intermediate` y
   `assert_inconsistency_rate_below_threshold`.
4. En **Linaje**, expandir las columnas: deben verse dos entradas desde
   `dbt_intermediate`, una salida a `mart_daily_quality` y los mapeos de campos.
5. Para practicar la vista general, abrir **Linaje** desde el menú izquierdo,
   buscar el FQN completo
   `postgres_lab.qa_lab.dbt_marts.fct_transaction_quality`, elegir el resultado y
   pulsar el nodo para centrar el grafo. Con sólo el nombre corto esta versión puede
   mostrar `No data`. Esa pantalla no parte de un activo; la pestaña Linaje de una
   tabla sí abre el contexto ya centrado.

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
.\.venv\Scripts\python.exe scripts\dbt_cli.py build --project-dir dbt --profiles-dir dbt
```

El bootstrap sólo prepara RAW. dbt reemplaza las transformaciones SQL sueltas y construye `dbt_staging`, `dbt_intermediate` y `dbt_marts`.

## Ejecutar todos los controles

```powershell
.\.venv\Scripts\python.exe scripts\run_quality_checks.py
.\.venv\Scripts\python.exe scripts\run_app_checks.py
```

Resultado normal:

```text
dbt PASS=80, ERROR=0
pytest datos 17 passed, 3 xfailed
pytest API 5 passed
Playwright 2 passed
Newman 5 requests, 10 assertions, 0 failed
reports/summary.json = success
```

El primer comando ejecuta dbt y, sólo si aprueba, las 20 pruebas pytest de datos. El segundo inicia la API sólo durante la prueba, ejecuta las 5 pruebas de API, Playwright y Newman, y la detiene al terminar. Usa el Chromium propio de Playwright y Newman en Docker; Chrome puede permanecer cerrado.

Para ejecutar Playwright con navegador visible, Inspector o trazas, y para
importar la misma colección en Postman Desktop, consultar
`docs/GUIA_AUTOMATIZACION_API_WEB.md`. El gate normal sigue siendo headless y no
necesita mantener una interfaz abierta.

## Preparar y reconciliar Power BI

El reporte debe conectarse con `qa_bi_reader`, no con el owner `qa_user`. El
bootstrap crea ese rol, dbt le concede `SELECT` en los marts y la sesión queda en
modo de sólo lectura.

Validar el contrato antes o después de refrescar el reporte:

```powershell
$env:QA_BI_PASSWORD="qa_bi_pass"
.\.venv\Scripts\python.exe scripts\run_powerbi_reconciliation.py
```

Resultado esperado:

```text
fact = mart diario = API
4.825 transacciones
200 inconsistentes
100 sin items
4,15 % de inconsistencia
lector sin permisos de escritura
```

El proyecto versionable se abre desde `powerbi/Data QA Lab.pbip`. Las consultas M,
medidas DAX, visuales implementados y casos de diagnóstico están explicados en
`powerbi/README.md`. El gate automático valida los oráculos; Desktop permite
refrescar y examinar la presentación visual.

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

## Puertos ocupados y cierre seguro de procesos

Si Uvicorn informa `Errno 10048`, el puerto ya está ocupado. Eso suele significar
que la API anterior continúa funcionando; no hay que iniciar una segunda copia.

En PowerShell, localizar el PID exacto:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen | Select-Object LocalAddress,LocalPort,OwningProcess
Get-CimInstance Win32_Process -Filter "ProcessId = <PID>" | Select-Object ProcessId,Name,CommandLine
```

En CMD:

```bat
netstat -ano | findstr LISTENING | findstr :8000
tasklist /FI "PID eq <PID>"
```

La forma normal de detener Uvicorn es `Ctrl+C` en su terminal. Sólo si quedó
huérfano y después de verificar que el PID corresponde a este lab, usar
`Stop-Process -Id <PID>` en PowerShell o `taskkill /PID <PID> /F` en CMD. Un PID
puede reutilizarse, por eso nunca se fuerza un número recordado de otra sesión.

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

El DAG actual tiene cuatro tareas:

```text
create_raw_tables
→ load_raw_postgres
→ run_dbt_build
→ run_pytest_quality_gate
```

El perfil local de dbt usa `threads: 1`. Esta configuración es intencional: evita
el deadlock ocasional observado en PostgreSQL cuando dbt recreaba varias vistas en
paralelo con cuatro hilos. No aumentar la concurrencia sin repetir una corrida
completa del DAG y comprobar las cuatro tareas.

## Orden de detención

Detener primero los consumidores. La red compartida puede seguir existiendo aunque los contenedores estén apagados.

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

`docker compose down` apaga y elimina los contenedores recreables, pero conserva los datos mientras no se agregue `--volumes`. `docker compose up --detach` los crea o inicia nuevamente.

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
