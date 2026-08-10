# Defensa profesional — Data QA Lab

Esta guía ayuda a explicar el laboratorio con precisión. No busca memorizar un
discurso ni adjudicarse responsabilidades ajenas: organiza evidencia para responder
preguntas técnicas y contar decisiones reales.

## Presentación de 30 segundos

> Construí un laboratorio local de Data QA que procesa un dataset bancario
> controlado desde RAW hasta marts en PostgreSQL. dbt transforma y valida cada
> capa, pytest cubre reglas de integración y Airflow orquesta los gates. También
> validé la misma información desde API, interfaz web y un contrato preparado para
> Power BI, con lineage y resultados dbt visibles en OpenMetadata. El foco no fue
> montar herramientas por sí mismas, sino detectar defectos, reunir evidencia y
> asegurar que una falla impida publicar datos incorrectos.

## Presentación de dos minutos

1. **Problema:** simular un flujo donde RAW contiene defectos conocidos y el
   consumo necesita datos confiables.
2. **Arquitectura:** PostgreSQL recibe RAW; dbt construye staging, intermediate y
   marts; pytest agrega controles integrados; Airflow coordina el orden.
3. **Trabajo QA:** definir reglas, reconciliar cantidades y montos, probar flags,
   investigar rechazos y validar el comportamiento ante fallos.
4. **Cobertura:** SQL y datos, API con pytest/Postman, panel con Playwright,
   metadata con OpenMetadata y contrato de consumo para Power BI.
5. **Evidencia:** 13 modelos, 67 tests dbt, 80 nodos dbt en verde, 17 pruebas de
   datos aprobadas y tres anomalías RAW controladas, además de gates API/web.
6. **Aprendizaje:** separar construcción de datos, orquestación y validación; usar
   cada herramienta por su responsabilidad y diagnosticar la capa exacta que falla.

## Presentación de cinco minutos

Usar la versión de dos minutos y ampliar solamente tres puntos:

- seguir una transacción concreta por las capas;
- contar un defecto investigado con evidencia y regresión;
- explicar una decisión técnica y su trade-off.

No enumerar todas las herramientas. Una historia completa demuestra más que una
lista extensa de nombres.

## Responsabilidad propia de Data QA

### Sí es defendible

- Analizar reglas de negocio y convertirlas en consultas y assertions.
- Diseñar casos positivos, negativos, límites y regresiones.
- Investigar datos desde RAW hasta marts y reconciliar capas.
- Crear y mantener tests dbt, pytest, API y web dentro del laboratorio.
- Leer logs y diferenciar fallo de datos, configuración, infraestructura o test.
- Validar dependencias y bloqueos del pipeline en Airflow.
- Revisar lineage, metadata y resultados de tests para acelerar el análisis.
- Mantener evidencia y cambios versionables.

### Es conocimiento operativo, no especialidad declarada

- Levantar contenedores y diagnosticar health de Airflow u OpenMetadata.
- Configurar un DAG sencillo o una ingesta de metadata.
- Exponer una API mínima con FastAPI para contar con una aplicación bajo prueba.
- Preparar consultas y medidas básicas para validar Power BI.

### No afirmar a partir de este lab

- Administración productiva de PostgreSQL, Airflow, OpenMetadata o Fabric.
- Diseño de plataformas distribuidas o alta disponibilidad.
- Desarrollo backend o BI avanzado.
- Experiencia productiva con volúmenes, SLA o incidentes empresariales que el lab
  no reproduce.

## Decisiones que se pueden explicar

| Decisión | Motivo defendible | Trade-off |
|---|---|---|
| RAW como tablas, staging/intermediate como vistas y marts como tablas | preservar entrada, evitar copias intermedias y acelerar consumo | las vistas recalculan al consultarse |
| dbt para transformaciones y tests cercanos al modelo | dependencias con `ref`, documentación y selección de tests | requiere aprender convenciones propias |
| Airflow llama un solo `dbt build` | el orquestador coordina; dbt resuelve su grafo interno | el detalle de modelos se investiga en artefactos/logs dbt |
| `threads: 1` en local | elimina un deadlock real y prioriza determinismo | menor paralelismo |
| pytest separado en datos y aplicación | evita mezclar dependencias y responsabilidades | existen dos gates coordinados |
| Postman y Newman sobre la misma colección | exploración visual y regresión automática sin duplicar casos | hay que mantener el JSON como fuente común |
| Consumidor BI con rol propio | aplica menor privilegio y hace comprobable el acceso | agrega una credencial local |
| Anomalías RAW como `xfail(strict=True)` | conserva datos defectuosos para practicar sin ocultarlos | un XPASS también obliga a revisar la clasificación |
| PBIP futuro, creado primero desde Desktop | evita fabricar un binario o proyecto no validado | el armado visual inicial es manual |

## Historias reales para entrevistas

### 1. Regla incompleta para montos negativos

**Situación:** la transformación descartaba montos nulos, pero permitía montos
negativos.

**Tarea:** impedir que esos registros llegaran a capas válidas.

**Acción:** se siguió el dato desde RAW, se corrigió la regla, se agregaron tests
y se reconcilió la partición entre válidos y rechazados.

**Resultado:** 100 nulos y 75 negativos quedan entre 175 rechazos; ninguna fila se
pierde silenciosamente.

### 2. Deadlock dbt dentro de Airflow

**Situación:** una corrida falló ocasionalmente al recrear vistas con cuatro hilos;
pytest quedó `upstream_failed`.

**Tarea:** distinguir defecto de datos de problema técnico y recuperar un pipeline
determinista.

**Acción:** se revisaron logs y estados, se redujo dbt a un hilo y se repitió la
corrida completa.

**Resultado:** cuatro de cuatro tareas en `success`, conservando documentada la
falla original.

### 3. OpenMetadata recuperado sin perder catálogo

**Situación:** MySQL/InnoDB del catálogo no iniciaba de forma confiable sobre un
bind mount de Windows.

**Tarea:** recuperar el servicio sin ocultar el incidente ni perder metadata.

**Acción:** se validó respaldo lógico, se migró a volumen nombrado y se verificaron
servicios, activos y lineage.

**Resultado:** OpenMetadata saludable, 13 modelos y 25 relaciones conservadas,
con una estrategia de recuperación documentada.

### 4. Gate que mezclaba responsabilidades

**Situación:** Airflow empezó a recopilar tests API aunque el contenedor no montaba
la aplicación.

**Tarea:** evitar un falso fallo sin eliminar cobertura.

**Acción:** se separó el gate de datos del gate de aplicación.

**Resultado:** Airflow valida datos; el runner de aplicación ejecuta pytest API,
Playwright y Newman con reportes separados.

## Preguntas probables y respuesta central

### ¿Por qué no usar solamente pytest?

pytest cubre reglas e integración en Python. dbt prueba modelos cerca de la
transformación; Postman facilita explorar el contrato; Newman repite esa colección;
Playwright comprueba el navegador; Airflow prueba la secuencia operativa. Se busca
separar responsabilidades, no acumular herramientas.

### ¿Por qué Airflow y dbt no son redundantes?

Airflow decide cuándo corre el proceso y qué gate habilita al siguiente. dbt
decide cómo se construyen y prueban los modelos SQL según su grafo de referencias.

### ¿Qué hacés cuando falla un test?

Primero clasifico el fallo: datos, regla, automatización, configuración o
infraestructura. Después sigo una fila o métrica hasta la primera capa donde cambia,
conservo la evidencia, corrijo la causa y ejecuto una regresión proporcional.

### ¿Por qué hay datos defectuosos conocidos?

Porque el objetivo es practicar detección y tratamiento. RAW conserva la entrada;
los defectos conocidos se declaran como `xfail(strict=True)` y las capas válidas
deben rechazarlos o marcarlos según la regla.

### ¿Qué harías distinto en producción?

Usaría secretos administrados, roles corporativos, ambientes separados, alertas,
SLA, revisión por pull request, datos anonimizados y capacidad dimensionada. El lab
demuestra el patrón de QA, no simula toda una plataforma productiva.

## Evidencia verificable

| Afirmación | Evidencia del lab |
|---|---|
| Pipeline de datos probado | dbt `80 PASS`; pytest `17 passed / 3 xfailed` |
| Orquestación con bloqueo real | DAG de cuatro tareas y corrida estable documentada |
| API y web automatizadas | pytest API `5`, Playwright `2`, Newman `10/10` |
| Metadata y lineage | 13 modelos, 67 tests catalogados, 25 aristas y 23 mapeos críticos |
| Reconciliación de consumo | fact = mart diario = API; contrato Power BI documentado |
| Seguridad de consumo | rol BI sin escritura ni acceso a capas internas |
| Gestión de defectos | `REGISTRO_DEFECTOS_LAB_QA.md` con causa, corrección y estado |

## Formulaciones para CV o LinkedIn

Estas frases son borradores para el bloque de portfolio; todavía no se incorporan
al CV ni se publican:

- Desarrollé un laboratorio reproducible de Data QA sobre PostgreSQL y dbt con 13
  modelos, 67 tests dbt y controles integrados en pytest.
- Automaticé gates de datos, API y web con Airflow, pytest, Newman y Playwright,
  preservando evidencia JUnit y bloqueo downstream ante fallos.
- Implementé reconciliación entre marts, API, panel web y contrato Power BI, con
  acceso de sólo lectura para el consumidor.
- Investigué y documenté defectos de reglas, dependencias, concurrencia y
  persistencia, incluyendo su causa y regresión.

La selección final se hará después de la auditoría de publicación. En una
entrevista se debe poder abrir el archivo o reporte que respalda cada afirmación.
