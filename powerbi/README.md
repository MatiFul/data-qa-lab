# Power BI — módulo mínimo de Data QA

Este módulo prepara Power BI como consumidor y superficie de validación. No
convierte al lab en un proyecto de desarrollo BI: el objetivo de QA es comprobar
permisos, origen, medidas, filtros, actualización y reconciliación.

## Activos versionados

```text
powerbi/
|-- Data QA Lab.pbip
|-- Data QA Lab.Report/
|-- Data QA Lab.SemanticModel/
|-- queries/
|   |-- fct_transaction_quality.pq
|   `-- mart_daily_quality.pq
|-- dax/
|   `-- quality_measures.dax
|-- reconciliation/
|   `-- expected_metrics.sql
`-- README.md
```

`Data QA Lab.pbip` abre el proyecto textual y versionable ya construido en Power
BI Desktop. Las consultas `.pq` y medidas `.dax` se conservan además como fuentes
legibles y reutilizables. Ninguno de estos activos contiene contraseñas; las
carpetas locales `.pbi` y `powerbi/local/` están excluidas de Git.

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

## Página visual implementada

La página `QA Overview` de 16:9 contiene:

| Visual | Campo o medida | Oráculo actual |
|---|---|---:|
| Tarjeta | `Total Transactions` | 4.825 |
| Tarjeta | `Inconsistent Transactions` | 200 |
| Tarjeta | `Transactions Without Items` | 100 |
| Tarjeta | `Inconsistency Rate` | 4,15 % |
| Columnas y línea | eje `transaction_date`; columnas `transaction_count`; línea `inconsistency_rate` | 90 fechas |
| Tabla de detalle | ID, fecha, montos, diferencia, cantidad de ítems y ambos flags | 200 filas con `inconsistent_amount_flag = 1` |

El reporte guarda la tasa como porcentaje, los montos con dos decimales, las
fechas sin jerarquía automática, títulos orientados a la regla y la fila total de
la tabla desactivada.

- tasa como porcentaje con dos decimales;
- montos con dos decimales;
- fechas sin jerarquía automática;
- rojo para inconsistencias y verde sólo para un estado aprobado;
- títulos que describan la regla, no el tipo de gráfico.

La tabla de detalle usa `fct_transaction_quality`; las tarjetas y la serie diaria
usan `mart_daily_quality`. No hace falta relacionar ambas tablas para este alcance:
cada una responde una pregunta distinta y la reconciliación controla que sus
totales coincidan.

## Apertura y actualización en Desktop

1. Levantar PostgreSQL y ejecutar `dbt build`.
2. Abrir `powerbi/Data QA Lab.pbip` con Power BI Desktop.
3. Si Desktop solicita credenciales, elegir autenticación de base de datos e
   ingresar `qa_bi_reader`; la contraseña queda en el almacén local de Power BI.
4. Elegir `Actualizar` y comprobar que las cuatro tarjetas muestran los oráculos
   indicados arriba.
5. Ejecutar la reconciliación y comparar el reporte con
   `reports/powerbi/reconciliation.json`.

Power BI Desktop creó inicialmente el proyecto. El repositorio sólo versiona sus
definiciones PBIP/PBIR/TMDL; no fabrica un PBIX opaco ni conserva cachés locales.

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
