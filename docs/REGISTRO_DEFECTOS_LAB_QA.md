# Registro de defectos del laboratorio

> Evidencia y seguimiento versionados junto con el laboratorio.

## Objetivo

Documentar los controles que inicialmente estaban marcados como `xfail`, identificar sus causas y registrar qué ocurrió después de corregir el generador y la transformación.

La investigación inicial se realizó con consultas de sólo lectura. Antes de reemplazar los datos se creó un respaldo lógico de PostgreSQL y una copia de los CSV originales.

## Resultado general

| ID | Problema inicial | Antes | Después | Estado |
|---|---|---:|---:|---|
| DQA-001 | Montos nulos en RAW | 123 | 100 controlados | Aceptado en RAW |
| DQA-002 | Montos negativos en RAW | 73 | 75 controlados | Aceptado en RAW |
| DQA-003 | Montos negativos llegan a curado | 73 | 0 | Cerrado |
| DQA-004 | Transacciones RAW sin ítems | 477 | 100 controladas | Rediseñado |
| DQA-005 | Montos inconsistentes en refinado | 4877 | 200 controlados | Rediseñado |

La nueva suite contiene 23 pruebas:

```text
19 passed
4 xfailed
0 failed
```

Los cuatro `xfail` actuales representan anomalías deliberadas, no fallos técnicos sin investigar.

## Respaldo previo

```text
data-qa-lab\backups\20260726_pre_generator_fix
```

Incluye:

- dump restaurable de PostgreSQL;
- copia de los ocho CSV anteriores;
- instrucciones de restauración;
- hash SHA-256 del dump.

## DQA-001 — Montos nulos en RAW

**Regla:** toda transacción debería tener un monto informado.

**Resultado inicial:**

```text
123 de 5000
2,46 %
```

**Resultado actual:**

```text
100 de 5000
2,00 %
```

**Causa:** anomalía introducida intencionalmente por el generador.

**Decisión:** conservarla en RAW para practicar completitud. La transformación la excluye y curado queda con cero montos nulos.

**Estado:** anomalía controlada; el test RAW permanece como `xfail(strict=True)`.

Consulta para DBeaver:

```sql
SELECT id_transaccion, monto
FROM raw.transacciones_raw
WHERE monto IS NULL
ORDER BY id_transaccion;
```

## DQA-002 — Montos negativos en RAW

**Regla:** el monto no debería ser negativo para este caso de negocio.

**Resultado inicial:**

```text
73 de 5000
1,46 %
```

**Resultado actual:**

```text
75 de 5000
1,50 %
```

**Causa:** anomalía introducida intencionalmente por el generador.

**Decisión:** conservarla en RAW para practicar reglas de dominio, pero impedir que avance.

**Estado:** anomalía controlada; el test RAW permanece como `xfail(strict=True)`.

Consulta para DBeaver:

```sql
SELECT id_transaccion, monto
FROM raw.transacciones_raw
WHERE monto < 0
ORDER BY id_transaccion;
```

## DQA-003 — Montos negativos llegaban a curado

**Regla:** una capa curada no debe conservar montos inválidos.

**Resultado inicial:**

```text
Negativos RAW:       73
Negativos curado:    73
```

**Causa:** la transformación controlaba `monto IS NOT NULL`, pero no controlaba `monto >= 0`.

**Corrección aplicada:**

```sql
AND r.monto >= 0
```

**Resultado actual:**

```text
Negativos RAW:       75
Negativos curado:     0
Negativos refinado:   0
Negativos consumo:    0
```

**Estado:** cerrado. La regla de pytest dejó de ser `xfail` y ahora debe aprobar siempre.

Consulta para DBeaver:

```sql
SELECT COUNT(*) AS negativos_curado
FROM curado.transacciones_curado
WHERE monto < 0;
```

Resultado esperado: `0`.

## DQA-004 — Transacciones sin ítems

**Regla:** la mayoría de las transacciones debe tener al menos un ítem.

**Resultado inicial:**

```text
477 de 5000 sin ítems
La cantidad era accidental y podía variar
```

**Causa:** los 12000 ítems se asignaban al azar y ninguna regla garantizaba un detalle por transacción.

**Corrección aplicada:**

1. Seleccionar explícitamente 100 transacciones anómalas.
2. Asignar al menos un ítem a las otras 4900.
3. Distribuir los ítems restantes sólo entre transacciones con detalle.

**Resultado actual:**

```text
100 de 5000 sin ítems
2,00 %
Cantidad reproducible
```

**Estado:** generador rediseñado. La anomalía se conserva como `xfail(strict=True)` porque es útil para practicar integridad.

Consulta para DBeaver:

```sql
SELECT transaction.id_transaccion, transaction.monto
FROM raw.transacciones_raw transaction
LEFT JOIN raw.items_transaccion_raw item
  USING (id_transaccion)
WHERE item.id_transaccion IS NULL
ORDER BY transaction.id_transaccion;
```

## DQA-005 — Todos los montos refinados eran inconsistentes

**Regla:** el monto de cabecera debe coincidir con la suma de cantidad por precio de los ítems, excepto anomalías controladas.

**Resultado inicial:**

```text
Total refinado:       4877
Inconsistentes:       4877
Consistentes:            0
Tasa de error:          100 %
```

**Causa:** el generador creaba el monto de cabecera y los ítems de manera independiente.

**Corrección aplicada:**

1. Crear los ítems.
2. Calcular su total por transacción.
3. Usar ese resultado como monto de cabecera.
4. Alterar explícitamente 100 montos.
5. Conservar 100 transacciones sin ítems.

**Resultado actual:**

```text
Total refinado:       4825
Consistentes:         4625
Inconsistentes:        200
Tasa controlada:      4,15 %
```

Las 200 inconsistencias se componen de:

- 100 montos alterados explícitamente;
- 100 transacciones controladas sin ítems.

pytest exige que la tasa exista pero no supere el 5 %.

**Estado:** diseño corregido. Se mantiene un `xfail(strict=True)` para representar el defecto de negocio deliberado.

Consulta para DBeaver:

```sql
SELECT
    id_transaccion,
    monto_transaccion,
    monto_calculado_items,
    diferencia_monto,
    cantidad_items,
    flag_inconsistencia_monto
FROM refinado.transacciones_refinado
WHERE flag_inconsistencia_monto = 1
ORDER BY ABS(diferencia_monto) DESC;
```

## Resultado del pipeline

Ejecución:

```text
generator_fix_validation_20260726T143258Z
```

Las nueve tareas finalizaron en `success`:

```text
create_raw_tables
create_curado_tables
create_refinado_tables
create_consumo_tables
load_raw_postgres
raw_to_curado_postgres
curado_to_refinado_postgres
refinado_to_consumo_postgres
apply_postgres_documentation
```

Conteos finales:

```text
raw.transacciones_raw              5000
raw.items_transaccion_raw         12000
curado.transacciones_curado        4825
curado.items_transaccion_curado   11541
refinado.transacciones_refinado    4825
consumo.transacciones_consumo      4825
```

La reconciliación entre refinado y consumo devuelve cero diferencias.

## Reproducibilidad

El generador utiliza una semilla fija y cantidades explícitas:

```text
Semilla                             42
Montos nulos                       100
Montos negativos                    75
Transacciones sin ítems            100
Montos alterados                   100
```

Se generaron dos veces los ocho CSV y se compararon sus hashes:

```text
Archivos comparados                  8
Diferencias de hash                  0
```

Esto permite repetir el laboratorio con el mismo resultado y distinguir claramente los defectos intencionales de los accidentales.

## Control automático en Airflow

pytest quedó integrado como última tarea del DAG:

```text
run_pytest_quality_gate
```

La tarea ejecuta la misma suite contra PostgreSQL mediante una conexión de sólo lectura. Si pytest devuelve un código distinto de cero, Airflow marca la tarea y el DAG como fallidos.

Validación:

```text
DAG run: pytest_gate_validation_20260726T144513Z
Tareas: 10 de 10 en success
pytest: 19 passed, 4 xfailed, 0 failed
```

Los resultados completos quedan disponibles en el log de la tarea dentro de Airflow.

## Ejercicio de detección y recuperación

Se ejecutó una simulación sin introducir nuevos defectos en el dataset. Para esa corrida se redujo temporalmente el máximo aceptable de inconsistencias de 5 % a 1 %.

```text
Corrida: controlled_failure_20260726T1454Z
Tasa real: 4,15 %
Máximo temporal: 1 %
Resultado: DAG failed
Detalle: 18 passed, 4 xfailed, 1 failed
```

Las nueve tareas de preparación de datos terminaron en `success`; el único fallo ocurrió en `run_pytest_quality_gate`. Esto confirma que el control de calidad funciona como condición de aprobación y no como un reporte informativo.

La recuperación se validó con el criterio normal:

```text
Corrida: controlled_recovery_20260726T1455Z
Máximo normal: 5 %
Resultado: DAG success
Detalle: 10 de 10 tareas en success
```

Los conteos finales permanecieron en 5000 transacciones RAW, 12000 ítems RAW, 4825 transacciones en las capas curada, refinada y consumo, y 200 inconsistencias controladas.

## DQA-006 — El DDL destruía estructuras con dependencias

**Regla:** una ejecución repetida del pipeline no debe destruir tablas ni invalidar modelos analíticos dependientes.

**Detección:** primera corrida de Airflow después de incorporar dbt:

```text
dbt_integration_validation_20260726T1529Z
```

**Error observado:**

```text
cannot drop table curado.transacciones_curado because other objects depend on it
view dbt_staging.stg_transactions depends on table curado.transacciones_curado
```

**Causa:** los archivos DDL ejecutaban `DROP TABLE` y `CREATE TABLE` en cada corrida. Esto funcionaba mientras no existían consumidores persistentes, pero dejó de ser válido cuando dbt creó vistas sobre la capa curada.

**Corrección:** cambiar los DDL de `raw`, `curado`, `refinado` y `consumo` a `CREATE TABLE IF NOT EXISTS`. Las tareas de carga y transformación conservan sus `TRUNCATE`, por lo que refrescan los datos sin eliminar las estructuras.

**Validación:**

```text
dbt_integration_recovery_20260726T1532Z
11 de 11 tareas en success
dbt PASS=37, ERROR=0
pytest 19 passed, 4 xfailed
```

**Estado:** cerrado.

Este defecto es un ejemplo de impacto por dependencia: un componente nuevo y correcto —dbt— reveló que una decisión histórica del pipeline no era idempotente ni segura para consumidores posteriores.
