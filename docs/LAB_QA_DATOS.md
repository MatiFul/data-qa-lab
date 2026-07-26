# Aplicaciones para un laboratorio de QA de datos

> Documento general versionado junto con el laboratorio.

## Base del laboratorio

| Aplicación | Uso resumido |
|---|---|
| Visual Studio Code | Escribir y ejecutar consultas SQL, scripts de Python, pruebas y archivos de configuración. |
| Git | Versionar pruebas, datos de ejemplo, pipelines y cambios del laboratorio. |
| Docker Desktop | Levantar bases de datos, servicios y herramientas aisladas sin ensuciar el sistema. |
| Python | Automatizar validaciones, comparar datasets y probar pipelines mediante `pytest`, `pandas` y conectores de bases de datos. |
| DBeaver Community | Explorar bases de datos, ejecutar SQL y comparar resultados de forma visual. |

## Bases de datos y almacenamiento

| Aplicación | Uso resumido |
|---|---|
| PostgreSQL | Practicar validaciones SQL, integridad, calidad, migraciones y reconciliación entre origen y destino. |
| DuckDB | Analizar localmente archivos CSV, JSON y Parquet, y probar transformaciones sin montar un servidor. |
| MinIO | Simular almacenamiento de objetos compatible con S3 para probar data lakes y cargas de archivos. |
| Snowflake (cuenta de prueba) | Practicar QA sobre un data warehouse cloud muy solicitado: cargas, transformaciones, permisos y reconciliaciones. |

## Pipelines, transformación y calidad

| Aplicación | Uso resumido |
|---|---|
| dbt Core | Crear transformaciones SQL y probar unicidad, valores nulos, relaciones, reglas de negocio y linaje. |
| Great Expectations | Definir y automatizar expectativas de calidad sobre datasets y generar reportes de validación. |
| Apache Airflow | Orquestar pipelines ETL/ELT y probar dependencias, reintentos, fallos, alertas y ejecuciones programadas. |
| Apache Spark / PySpark | Probar transformaciones y controles de calidad sobre volúmenes grandes o procesamiento distribuido. |

## APIs, web y aplicaciones móviles

| Aplicación | Uso resumido |
|---|---|
| Postman | Probar APIs que crean, consultan o modifican datos y automatizar validaciones de respuestas. |
| Playwright | Validar flujos web de punta a punta y comprobar que los datos visibles coincidan con la API o la base. |
| Appium | Automatizar flujos móviles y validar la consistencia de datos entre la app, las APIs y el backend. |
| Android Studio | Ejecutar emuladores, inspeccionar logs y bases locales, y analizar tráfico y comportamiento de apps Android. |
| Apache JMeter | Probar carga y rendimiento de APIs, consultas y procesos de ingestión de datos. |

## BI, observabilidad y entrega

| Aplicación | Uso resumido |
|---|---|
| Power BI Desktop | Practicar pruebas de métricas, filtros, agregaciones y reconciliación entre dashboards y datos fuente. |
| Metabase | Crear dashboards locales y validar rápidamente resultados analíticos sobre PostgreSQL o DuckDB. |
| Grafana | Monitorear métricas de pipelines, calidad, latencia y fallos mediante tableros y alertas. |
| Jenkins | Integrar pruebas SQL, Python, dbt y calidad de datos en pipelines de CI/CD. |
