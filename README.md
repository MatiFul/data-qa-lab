# Laboratorio Data QA Enterprise

## Objetivo

Este laboratorio es un proyecto práctico de Data QA para entornos enterprise. Su propósito es construir una base de observabilidad y control de calidad de datos mediante pipelines de ingestión y transformación, con validaciones automáticas y soporte de metadata.

## Stack

- StarRocks
- OpenMetadata
- Apache Airflow
- Docker
- PostgreSQL
- Python
- pytest
- DBeaver
- Visual Studio Code

## Arquitectura

La solución se organiza en capas de datos y herramientas de orquestación:

- `airflow-lab/`: contiene los DAGs, configuraciones Docker y plugins para ejecutar las pipelines en Airflow.
- `data-qa-lab/`: incluye generadores de datos y artefactos de datasets de prueba para QA.
- `qa_lab_v3/`: contiene datos de ejemplo, scripts de generación y pruebas adicionales de calidad.
- `sql/`: almacena los DDL de creación de tablas y las consultas de quality checks para las distintas capas de datos.
- `om-lab/`: infraestructura de respaldo y volúmenes de base de datos, principalmente para MySQL/OpenMetadata.

El flujo de datos esperado es:

1. Ingesta de datos en capa `raw`.
2. Transformación a capa `curado`.
3. Transformación a capa `refinado`.
4. Validaciones de calidad en cada capa.
5. Monitoreo y catalogación mediante OpenMetadata.

## Flujo conceptual

Python Generator
↓
CSV
↓
Stream Load
↓
RAW
↓
CURADO
↓
REFINADO
↓
QA Checks
↓
OpenMetadata

## Conceptos clave

- OpenMetadata observa y documenta
- Airflow orquesta ejecución
- OpenMetadata no reemplaza Airflow
- Observabilidad ≠ ejecución

## Foco actual

El foco principal del laboratorio es:

- Data QA enterprise
- observabilidad
- profiling
- quality checks
- troubleshooting
- arquitectura de pipelines

Airflow se utiliza únicamente a nivel funcional/orquestación básica.

No es objetivo actual profundizar en:
- Kubernetes
- CI/CD
- despliegues cloud
- arquitecturas distribuidas complejas



## Estructura del proyecto

- `airflow-lab/`
  - `dags/`
  - `docker/`
  - `plugins/`
  - `logs airflow/`
- `backups/`
- `data-qa-lab/`
  - `data_generator/`
  - `output/`
- `qa_lab_v3/`
  - `data/`
  - `scripts/`
- `sql/`
  - `ddl/`
    - `raw/`
    - `curado/`
    - `refinado/`
  - `qa_checks/`
    - `Raw/`
    - `curado/`
    - `Refinado/`
  - `transformations/`
- `om-lab/`
  - `docker-compose.yml`
  - `docker-volume/`

## Estado actual

- El pipeline PostgreSQL vigente es `airflow-lab/dags/qa_pipeline_postgres_v1.py`.
- El generador crea un dataset reproducible con anomalías controladas.
- Las dependencias del generador están registradas en `requirements-generator.txt`.
- El flujo PostgreSQL utiliza las capas `raw`, `curado`, `refinado` y `consumo`.
- dbt crea dos vistas `staging`, dos tablas `marts` y ejecuta 33 pruebas.
- Las once tareas del DAG fueron validadas en `success`.
- La suite pytest contiene 23 pruebas: 19 aprobadas y 4 anomalías esperadas.
- Airflow ejecuta `dbt build` y luego pytest como gates del DAG PostgreSQL.
- La infraestructura incluye soporte Docker para los servicios principales.
- OpenMetadata conserva el catálogo y lineage del laboratorio.
- El enfoque actual es funcionalidad local, sin Kubernetes ni CI/CD establecido.

## Aprendizajes importantes

### Airflow 3

Airflow 3 requiere el componente separado:

- airflow-dag-processor

Sin este componente:
- los DAGs pueden parsearse
- pero no aparecen correctamente en la UI

Esto fue uno de los primeros problemas reales resueltos del laboratorio.

### dbt local

Definir la contraseña únicamente en la terminal y ejecutar:

```powershell
$env:QA_DB_PASSWORD="<contraseña local>"
.\.venv\Scripts\dbt.exe build --project-dir dbt --profiles-dir dbt
```

El proyecto crea objetos únicamente en `dbt_staging` y `dbt_marts`. Los artefactos temporales de `dbt/target` no se versionan.

## Documentación

- `docs/GUIA_INTRODUCTORIA_LAB_QA.md`: introducción al laboratorio y sus herramientas.
- `docs/PLAN_ACCION_LAB_QA.md`: avance y próximos pasos.
- `docs/REGISTRO_DEFECTOS_LAB_QA.md`: defectos, evidencia y recuperación.
- `docs/GUIA_GIT.md`: flujo de versionado utilizado en el laboratorio.

## Próximos pasos

1. Generar reportes persistentes de pytest y dbt.
2. Ejecutar la suite desde GitHub Actions.
3. Completar el README orientado a portfolio.
4. Evaluar una segunda etapa con API, Postman, interfaz web y Playwright.
