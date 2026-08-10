# Modo práctica — Data QA Lab

El modo práctica reutiliza el laboratorio estable para aprender tareas de Data QA
sin convertir cada ejercicio en una modificación permanente. Ninguna práctica es
un requisito para preparar el entorno: se ejecutan después, de a una, cuando el
objetivo sea estudiar.

## Ciclo obligatorio de cada práctica

```text
Línea base verde
  → pregunta o regla de calidad
  → comprobación manual
  → automatización equivalente
  → falla controlada
  → evidencia y diagnóstico
  → recuperación
  → regresión verde
```

Una práctica no termina al encontrar el error. Termina cuando se puede explicar
la causa, diferenciarla del síntoma y demostrar que la regresión volvió a aprobar.

## Reglas de seguridad

- Ejecutar un solo ejercicio por vez.
- No usar `git reset`, `git clean` ni restauraciones masivas para salir de una
  práctica.
- Preferir variables, configuración de corrida, puertos alternativos o copias
  temporales antes que editar el estado base.
- No borrar volúmenes Docker como parte de un ejercicio normal.
- No marcar tareas Airflow manualmente sin anotar qué estado se forzó.
- No convertir una falla esperada en `xfail` solamente para dejar el gate verde.
- Repetir como máximo tres ciclos sobre el mismo bloqueo; después registrar la
  evidencia y detener el ejercicio.

## Línea base y cierre

Antes de una práctica que modifique estado, comprobar que PostgreSQL esté
disponible y conservar el resultado inicial. El cierre completo utiliza:

```powershell
$env:QA_DB_PASSWORD="qa_pass"
.\.venv\Scripts\python.exe scripts\run_quality_checks.py
.\.venv\Scripts\python.exe scripts\run_app_checks.py
$env:QA_BI_PASSWORD="qa_bi_pass"
.\.venv\Scripts\python.exe scripts\run_powerbi_reconciliation.py
```

Resultado normal:

```text
dbt                         80 PASS / 0 ERROR
pytest datos                17 passed / 3 xfailed
pytest API                  5 passed
Playwright                  2 passed
Postman/Newman              10 assertions / 0 failed
Reconciliación BI          success
```

Airflow y OpenMetadata se incluyen sólo cuando la práctica los involucra. El
arranque integral desde servicios detenidos pertenece al bloque de reproducibilidad.

## Catálogo de prácticas

| ID | Herramienta | Pregunta de QA | Manual | Automatización | Falla o variación | Evidencia y recuperación |
|---|---|---|---|---|---|---|
| P01 | DBeaver/PostgreSQL | ¿La transacción 58 conserva montos y flags entre capas? | Seguir el ID por staging, intermediate y mart. | Test dbt de flags y pytest de integración. | Cambiar temporalmente el ID consultado por uno inexistente. | Distinguir cero filas de dato inconsistente; volver al ID 58. |
| P02 | DBeaver/dbt | ¿Por qué se rechazó la transacción 55? | Revisar RAW y `int_rejected_transactions`. | Tests de partición y reglas de rechazo. | Comparar motivo esperado con uno incorrecto. | SQL de detalle; no modificar el dataset. |
| P03 | SQL/pytest | ¿RAW mantiene las anomalías controladas? | Contar 175 rechazadas: 100 nulas y 75 negativas. | `xfail(strict=True)` de RAW y tests de transformación. | Corregir el dato en una copia de ejercicio. | Un XPASS también exige investigación; regenerar el dataset. |
| P04 | dbt | ¿El gate rechaza una tasa demasiado estricta? | Calcular `200 / 4825`. | Test `assert_inconsistency_rate_below_threshold`. | Ejecutar con `max_inconsistency_rate: 0`. | FAIL esperado; repetir con `0.05` y exigir PASS. |
| P05 | dbt | ¿Los flags coinciden con el cálculo de negocio? | Comparar `amount_difference` y flags en casos elegidos. | `assert_quality_flags_match_calculation`. | Alterar el oráculo sólo en una rama de práctica. | Filas devueltas por el singular test; revertir el cambio acotado. |
| P06 | Airflow | ¿La corrida completa respeta las dependencias? | Observar Graph/Grid y logs. | DAG de cuatro tareas. | Configurar umbral `0.01`. | `run_dbt_build=failed` y pytest=`upstream_failed`; nueva corrida normal. |
| P07 | Airflow | ¿Qué implica forzar el estado de una tarea? | Marcar una instancia aislada y revisar downstream. | No aplica: es operación del orquestador. | Cambiar estado y usar la opción downstream en una corrida de práctica. | Historial de la corrida; nunca presentar el estado forzado como ejecución real. |
| P08 | Swagger/Postman/Newman | ¿La API distingue dato ausente de request inválido? | Ejecutar `404` y `422`. | Misma colección con Newman y tests API. | ID inexistente y `limit=101`. | Status, body y assertion; restauración no necesaria. |
| P09 | Playwright | ¿El panel muestra la misma línea base que la API? | Abrir panel y aplicar filtro. | Dos recorridos E2E. | Cambiar temporalmente un texto esperado o usar URL inválida. | Screenshot/trace/DOM; restaurar oráculo y ejecutar gate. |
| P10 | Uvicorn/FastAPI | ¿Es un error de aplicación o de operación? | Abrir `/health` y `/docs`. | pytest API y `run_app_checks.py`. | Omitir variable, usar contraseña errónea o puerto ocupado. | `api.log`, HTTP y error de bind/autenticación; corregir entorno o puerto. |
| P11 | OpenMetadata | ¿De dónde llega un campo del mart? | Buscar por FQN y recorrer lineage. | Sincronizador dbt y verificación API. | Buscar por nombre corto o inspeccionar una arista manual. | `No data` por búsqueda no equivale a lineage ausente; usar FQN completo. |
| P12 | OpenMetadata/dbt | ¿El catálogo refleja los tests ejecutados? | Revisar 12 tests del fact y mapeos críticos. | `sync_openmetadata_dbt.py`. | Artefacto dbt desactualizado. | Comparar fecha y resultados de `run_results.json`; regenerar y resincronizar. |
| P13 | Power BI | ¿Las tarjetas coinciden con todos los oráculos? | Refrescar el reporte y comparar cuatro valores. | `run_powerbi_reconciliation.py`. | Credencial incorrecta, refresh omitido o medida DAX alterada. | Clasificar conexión vs modelo vs DAX; restaurar medida y refrescar. |
| P14 | PostgreSQL/seguridad | ¿El consumidor BI realmente es de sólo lectura? | Consultar marts como `qa_bi_reader`. | Reconciliador comprueba sesión y privilegios. | Intentar una escritura dentro de una práctica controlada. | Debe fallar; no otorgar permisos para hacer aprobar el ejercicio. |
| P15 | Git | ¿El cambio es revisable y no incluye secretos? | Revisar status, diff y archivos nuevos. | `git diff --check` y futura CI. | Introducir whitespace o un archivo generado en una rama de práctica. | Diff acotado; retirar sólo el cambio del ejercicio, sin limpiar trabajo ajeno. |

## Orden recomendado

### Nivel 1 — Núcleo Data QA

P01, P02, P03, P04 y P05. El objetivo es dominar la regla de negocio, escribir SQL,
entender las capas, leer una falla y relacionar control manual con automatización.

### Nivel 2 — Aplicación y orquestación

P06, P08, P09 y P10. El objetivo es distinguir fallo de datos, contrato, interfaz,
configuración y dependencia.

### Nivel 3 — Gobierno, consumo y operación

P07 y P11 a P15. El objetivo es trabajar con evidencia, permisos, lineage,
reconciliación y cambios versionables sin transformarse en administrador experto.

## Ruta de aprendizaje por profundidad

| Herramienta o tema | Dominar para Data QA | Manejar operativamente | Conocer conceptualmente |
|---|---|---|---|
| Calidad de datos | reglas, oráculos, severidad, evidencia, regresión | umbrales y excepciones controladas | gobierno corporativo avanzado |
| SQL/PostgreSQL | joins, filtros, agregaciones, nulos, duplicados, reconciliación | vistas, permisos, planes simples, índices básicos | administración, HA, tuning profundo |
| Python/pytest | leer y escribir tests, fixtures simples, asserts y parametrización | entorno virtual, dependencias y JUnit | desarrollo de frameworks complejos |
| dbt | sources, `ref`, materializaciones, tests y lineage | selección, variables, artefactos y logs | macros avanzadas y administración de plataforma |
| Airflow | estados, dependencias, logs, retry y `upstream_failed` | disparar, configurar y reejecutar una corrida | diseño y administración de clúster |
| API/Postman | contrato HTTP, casos positivos/negativos y assertions | entornos, colecciones y Newman | diseño avanzado de APIs |
| Playwright | locator, acción, assertion y evidencia | headed, Inspector y trazas | arquitectura interna del navegador |
| Docker Compose | servicios, contenedores, logs, puertos y volúmenes | iniciar, detener y comprobar health | orquestación productiva con Kubernetes |
| Git/CI-CD | status, diff, commit, rama, PR y lectura de CI | resolver cambios acotados y artefactos | administración avanzada de runners |
| OpenMetadata | buscar activos, tests y lineage | ejecutar ingesta y distinguir metadata obsoleta | gobierno y administración avanzada |
| Power BI | validar filtros, medidas, refresh y reconciliación | importar marts y leer Power Query/DAX básico | desarrollo BI avanzado y administración Fabric |
| FastAPI/Uvicorn | entender qué se está probando | iniciar, detener y leer logs | desarrollo backend completo |

La prioridad no se mide por cantidad de herramientas. Se mide por la capacidad de
formular una regla, encontrar evidencia, automatizarla y explicar el resultado.

## Plantilla para registrar una sesión futura

```text
Práctica:
Fecha:
Hipótesis:
Línea base:
Acción manual:
Automatización:
Falla observada:
Evidencia:
Causa:
Corrección o recuperación:
Regresión:
Qué podría explicar en una entrevista:
```

La evidencia de una sesión no se mezcla automáticamente con el portfolio. Primero
se revisa; sólo los hitos claros y reproducibles se publican posteriormente.
