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
- dbt
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

- Hay un pipeline Airflow básico definido en `airflow-lab/dags/qa_pipeline_v1.py`.
- Existen scripts de generación de datasets en `data-qa-lab/data_generator/generate_dataset.py`.
- El proyecto cuenta con DDL de tablas y checks de calidad para las capas `raw`, `curado` y `refinado`.
- La infraestructura incluye soporte Docker para los servicios principales.
- El enfoque actual es funcionalidad local / laboratorio, sin despliegue Kubernetes ni CI/CD establecido.

## Aprendizajes importantes

### Airflow 3

Airflow 3 requiere el componente separado:

- airflow-dag-processor

Sin este componente:
- los DAGs pueden parsearse
- pero no aparecen correctamente en la UI

Esto fue uno de los primeros problemas reales resueltos del laboratorio.

## Próximos pasos

1. Integrar ejecución real de SQL desde Airflow hacia StarRocks.
2. Añadir más QA checks de negocio y controles relacionales entre capas.
3. Mejorar la documentación de Airflow y los hooks/conexiones necesarias.
