# Power BI — módulo mínimo de Data QA

Este módulo prepara Power BI como consumidor y superficie de validación. No
convierte al lab en un proyecto de desarrollo BI: el objetivo de QA es comprobar
permisos, origen, medidas, filtros, actualización y reconciliación.

## Activos versionados

```text
powerbi/
|-- queries/
|   |-- fct_transaction_quality.pq
|   `-- mart_daily_quality.pq
|-- dax/
|   `-- quality_measures.dax
|-- reconciliation/
|   `-- expected_metrics.sql
`-- README.md
```

Las consultas `.pq` son código M listo para pegar en el Editor avanzado de Power
Query. Las medidas `.dax` son los oráculos del reporte. No contienen contraseñas.

## Conexión de menor privilegio

El bootstrap crea `qa_bi_reader` y dbt reaplica `SELECT` sobre los modelos de
`dbt_marts` cada vez que los reconstruye. La sesión del rol inicia además con
`default_transaction_read_only=on`.

Datos locales de conexión:

```text
Servidor:    127.0.0.1:5434
Base:        qa_lab
Modo:        Importar
Usuario:     qa_bi_reader
Contraseña: qa_bi_pass
```

La credencial se introduce en Power BI Desktop y queda en el almacenamiento local
de la aplicación; no se agrega al reporte ni al repositorio. Es una credencial
exclusiva del laboratorio local, equivalente a la ya declarada en Docker Compose.

## Construcción visual pendiente para la práctica manual

Crear una página `QA Overview` de 16:9 con estos elementos:

| Visual | Campo o medida | Oráculo actual |
|---|---|---:|
| Tarjeta | `Total Transactions` | 4.825 |
| Tarjeta | `Inconsistent Transactions` | 200 |
| Tarjeta | `Transactions Without Items` | 100 |
| Tarjeta | `Inconsistency Rate` | 4,15 % |
| Líneas | eje `transaction_date`; valores `transaction_count` e `inconsistency_rate` | 90 fechas |
| Tabla de detalle | ID, montos, diferencia y ambos flags | filtrar `inconsistent_amount_flag = 1` |

Formato recomendado:

- tasa como porcentaje con dos decimales;
- montos con dos decimales;
- fechas sin jerarquía automática;
- rojo para inconsistencias y verde sólo para un estado aprobado;
- títulos que describan la regla, no el tipo de gráfico.

La tabla de detalle usa `fct_transaction_quality`; las tarjetas y la serie diaria
usan `mart_daily_quality`. No hace falta relacionar ambas tablas para este alcance:
cada una responde una pregunta distinta y la reconciliación controla que sus
totales coincidan.

## Secuencia de armado en Desktop

1. Levantar PostgreSQL y ejecutar `dbt build`.
2. Abrir Power BI Desktop y elegir `Obtener datos > Consulta en blanco`.
3. Abrir el Editor avanzado y pegar cada archivo `.pq`; nombrar las consultas como
   sus marts.
4. Elegir autenticación de base de datos e ingresar `qa_bi_reader`.
5. Crear las medidas desde `quality_measures.dax`.
6. Construir los visuales de `QA Overview` y actualizar.
7. Comparar las cuatro tarjetas con `reports/powerbi/reconciliation.json`.
8. Guardar primero el binario local bajo `powerbi/local/`, que está excluido de
   Git. Cuando el reporte esté aprobado, guardarlo como proyecto PBIP versionable
   dentro de `powerbi/` y revisar el diff antes de publicarlo.

No se genera un PBIX o PBIP falso desde scripts. Power BI Desktop es quien debe
crear inicialmente esos formatos; después, el PBIP permite versionar como texto el
modelo semántico y el reporte.

## Reconciliación automática

PowerShell:

```powershell
$env:QA_DB_PASSWORD="qa_pass"
$env:QA_BI_PASSWORD="qa_bi_pass"
.\.venv\Scripts\python.exe scripts\run_powerbi_reconciliation.py
```

CMD:

```bat
set QA_DB_PASSWORD=qa_pass
set QA_BI_PASSWORD=qa_bi_pass
.\.venv\Scripts\python.exe scripts\run_powerbi_reconciliation.py
```

El reconciliador compara:

```text
fct_transaction_quality
        ↔ mart_daily_quality
        ↔ GET /api/quality/summary
        ↔ tarjetas esperadas de Power BI
```

También falla si `qa_bi_reader` no inicia en modo de sólo lectura o recibe
permisos `INSERT`, `UPDATE` o `DELETE` sobre el fact. El resultado queda en
`reports/powerbi/reconciliation.json`.

## Casos para la futura práctica

| Caso | Evidencia esperada |
|---|---|
| Actualización normal | cuatro tarjetas iguales al JSON de reconciliación |
| Filtro por fecha | tarjetas y tabla cambian al mismo contexto |
| Filtro de inconsistencias | la tabla sólo contiene flag `1` |
| PostgreSQL detenido | error de refresh identificable como conectividad |
| Credencial incorrecta | error de autenticación, no diferencia de datos |
| Mart desactualizado | diferencia reproducible frente al oráculo nuevo |
| Medida DAX alterada | SQL y API coinciden, sólo Power BI difiere |

La clasificación importa: no toda tarjeta incorrecta es un defecto de datos. Puede
fallar el refresh, el modelo, el DAX, un filtro o el formato del visual.

## Referencias oficiales

- Power Query M para PostgreSQL:
  <https://learn.microsoft.com/powerquery-m/postgresql-database>
- Proyectos Power BI Desktop:
  <https://learn.microsoft.com/power-bi/developer/projects/projects-overview>
- Carpeta de reporte PBIP/PBIR:
  <https://learn.microsoft.com/power-bi/developer/projects/projects-report>
