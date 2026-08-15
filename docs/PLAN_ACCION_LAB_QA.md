# Plan de acción — Laboratorio de QA de datos

> Documento de control versionado junto con el laboratorio.

## Objetivo

Dejar un laboratorio local, reproducible y orientado al trabajo de Data QA, donde
sea posible investigar datos manualmente, diseñar casos, automatizarlos, provocar
fallas controladas, diagnosticar evidencia y volver a validar el flujo completo.

La infraestructura es el escenario de práctica, no el objetivo profesional. El
lab debe exigir dominio práctico de QA y sólo conocimiento operativo o conceptual
de arquitectura, administración de plataformas y despliegue.

## Definición vigente de “lab completo” — 9 de agosto de 2026

El lab se considerará completo y listo para quedar en **modo práctica** cuando se
cumplan todos los puntos obligatorios de este bloque. El historial posterior se
conserva como evidencia de construcción y recuperación, pero ya no define por sí
solo el cierre actual.

El cierre se divide en tres hitos acumulativos:

1. **Técnicamente listo:** entorno estable, reproducible y validado.
2. **Modo práctica:** catálogo de ejercicios y ruta de aprendizaje disponibles.
3. **Portfolio completo:** repositorios publicados de forma segura, primera CI
   remota validada y CV actualizado con evidencia defendible.

El laboratorio sólo se marcará como **completo** después del tercer hito. Ninguna
publicación se realizará antes de la revisión final ni sin autorización explícita
del usuario en ese momento.

“Portfolio completo” significa una **primera versión pública estable**, no un
portfolio cerrado. Después de esa base, el laboratorio podrá crecer con escenarios
de práctica independientes, nuevas automatizaciones y evidencia adicional, sin
perder una versión demostrable que permanezca siempre en verde.

### Base ya terminada

- [x] Flujo activo único `raw → dbt_staging → dbt_intermediate → dbt_marts`.
- [x] Quality gate local de dbt y pytest estable.
- [x] DAG reducido y corrida real con cuatro de cuatro tareas en `success`.
- [x] API y panel web de sólo lectura sobre `dbt_marts`.
- [x] Cinco pruebas pytest de API, dos recorridos Playwright y colección
  Postman/Newman con diez assertions en verde.
- [x] PostgreSQL, DBeaver, Airflow y OpenMetadata recorridos en la visita guiada.
- [x] Catálogo de 13 modelos y 25 relaciones de linaje de tablas en OpenMetadata.
- [x] Documentación técnica, mapa de ejecución, guía introductoria y registro de
  defectos actualizados para la arquitectura vigente.

### Cierre técnico obligatorio

- [x] Migrar el datadir MySQL de OpenMetadata desde el bind mount de Windows a un
  volumen nombrado de Docker, preservando y verificando antes un respaldo lógico,
  para reducir el riesgo de una nueva corrupción InnoDB.
- [x] Completar una integración representativa de dbt con OpenMetadata: importar
  descripciones y resultados de pruebas, y documentar linaje por columnas para
  los campos críticos de `fct_transaction_quality`. No se requiere mapear todas
  las columnas del catálogo.
- [x] Dejar preparada la práctica con Postman Desktop: colección y entorno local
  importables, casos positivos y negativos y comparación con el runner automático.
  La aplicación quedó instalada y su Runner confirmó cinco requests y diez
  assertions; los ejercicios autónomos permanecen en el modo práctica.
- [x] Preparar el módulo mínimo de QA sobre Power BI: lector de marts, consultas,
  medidas, visuales especificados y reconciliación automática contra SQL y API.
  La página `QA Overview` quedó construida como PBIP versionable y no requiere
  aprender desarrollo avanzado de BI.
- [x] Unificar la guía de terminal para PowerShell y CMD, incluyendo variables de
  entorno, uso obligatorio del `.venv`, puertos ocupados y cierre de Uvicorn.
- [x] Ejecutar una prueba de reproducibilidad desde servicios detenidos: levantar
  el núcleo, cargar RAW, construir dbt, ejecutar gates de datos y aplicación,
  lanzar una corrida Airflow y comprobar el catálogo opcional.
- [x] Revisar y registrar localmente los cambios de `data-qa-lab` y `airflow-lab`
  en commits coherentes, sin publicar GitHub ni descartar cambios previos.

Estas dos casillas históricas quedaron verificadas por los cierres fechados **6B**
y **6C** del 10 de agosto de 2026, documentados más abajo. No incluyen la prueba
por una segunda persona ni la publicación y CI remotas, que conservan sus propias
casillas abiertas.

### Cierre pedagógico obligatorio

- [x] Crear una ruta de aprendizaje por herramienta con tres niveles: dominar
  para Data QA, manejar operativamente y conocer sólo de forma conceptual.
- [x] Crear un catálogo de prácticas que conecte cada validación manual con su
  automatización, una falla controlada, la evidencia esperada y su diagnóstico.
- [x] Incluir errores intermedios y operativos dentro de las prácticas: credencial
  incorrecta, variable ausente, puerto ocupado, servicio caído, selección o
  parámetro mal aplicado, error esperado `404/422`, fallo real de datos, fallo de
  infraestructura y tarea Airflow `upstream_failed`.
- [x] Preparar un resumen defendible para entrevistas: arquitectura en lenguaje
  simple, responsabilidades propias de QA, defectos investigados y decisiones.

### Cierre de portfolio obligatorio

- [ ] Auditar qué se publicará: estructura de los repositorios, historial,
  licencias, README, capturas, archivos generados, respaldos, volúmenes y secretos.
- [ ] Preparar commits locales finales y decidir la presentación pública de
  `data-qa-lab` y `airflow-lab`; `om-lab` no debe publicar datos, respaldos ni
  volúmenes operativos.
- [ ] Publicar en GitHub sólo después de la aprobación explícita del usuario.
- [ ] Ejecutar y validar la primera CI remota, incluyendo gates y artefactos que
  sean seguros y útiles para revisión.
- [ ] Incorporar el proyecto al CV con una descripción breve, resultados medibles
  y responsabilidades reales de QA.
- [ ] Actualizar habilidades/herramientas únicamente con tecnologías que puedan
  demostrarse mediante el lab y explicarse en entrevista; distinguir uso práctico
  de conocimiento operativo o conceptual.
- [ ] Definir la evolución posterior del portfolio: conservar una rama principal
  estable, desarrollar cada práctica en cambios acotados, registrar evidencia y
  publicar hitos relevantes mediante versiones o releases comprensibles.

### Validación final obligatoria

- [x] Confirmar nuevamente dbt `PASS=80`, pytest de datos `17 passed / 3 xfailed`,
  pytest API `5 passed`, Playwright `2 passed` y Postman `10 assertions / 0 failed`.
- [x] Confirmar una corrida nueva de Airflow con cuatro de cuatro tareas exitosas.
- [x] Confirmar PostgreSQL disponible y OpenMetadata saludable con la persistencia
  nueva, catálogo enriquecido y linaje verificable.
- [x] Confirmar técnicamente la reconciliación SQL ↔ API ↔ panel web y el contrato
  de lectura preparado para Power BI sobre las métricas seleccionadas. El PBIP
  visual conserva los mismos oráculos y un detalle filtrado reproducible.
- [x] Validar documentación, mapa interactivo, `git diff --check` y estado final
  de ambos repositorios.

### No bloquea el cierre

- Instalar Jira o registrar tickets en una plataforma externa.
- Dominar arquitectura, administración avanzada de Airflow/OpenMetadata,
  Elasticsearch o MySQL.
- Implementar todos los patrones futuros de carga, índices, triggers, stored
  procedures, snapshots y recuperación administrativa de Airflow.
- Completar linaje columna por columna para todos los modelos o gobierno de datos
  avanzado con owners, dominios y data products.
- Actualizar en una práctica de mantenimiento la imagen de ingesta de OpenMetadata
  antes del fin de soporte de Python 3.10 anunciado para octubre de 2026 y revisar
  la dependencia obsoleta de `pkg_resources`. Son avisos actuales, no fallas del
  servicio ni del workflow.

Al completar este bloque no se agregarán más componentes al entorno base. Las
ideas restantes pasarán a ser escenarios de práctica independientes.

## Secuencia de ejecución por bloques

Cada bloque debe cerrar un resultado coherente y validado. Dentro del bloque se
aplica el ciclo **diagnosticar → ejecutar → validar → corregir** hasta tres veces
sobre el mismo impedimento. Si el tercer ciclo no resuelve el objetivo, el bloque
se cierra como bloqueado con evidencia y una decisión explícita; no se prolonga de
forma indefinida. Las ideas nuevas se envían al backlog sin ampliar el alcance del
bloque activo.

### Bloque 1 — Persistencia segura de OpenMetadata

- respaldo lógico nuevo y checksum verificado;
- migración de MySQL desde bind mount de Windows a volumen Docker nombrado;
- conservación intacta del directorio anterior como recuperación;
- restauración, migración oficial y validación de conteos, catálogo, linaje y UI;
- actualización del defecto técnico y de la guía operativa.

**Cierre:** MySQL, Elasticsearch y OpenMetadata saludables, HTTP 200, 13 modelos
dbt y 25 relaciones vigentes después de reiniciar sobre la persistencia nueva.

**Estado:** completado el 9 de agosto de 2026. Respaldo y evidencia en
`om-lab/recovery-backups/20260809_pre_named_volume/BACKUP_MANIFEST.md`.

### Bloque 2 — Catálogo útil y operación clara

- descripciones y resultados dbt representativos en OpenMetadata;
- linaje de columnas crítico y práctica del explorador general;
- instrucciones equivalentes para PowerShell y CMD, `.venv`, variables, puertos y
  cierre de procesos.

**Cierre:** OpenMetadata muestra metadata útil para QA y la operación local no
depende de recordar qué terminal se está utilizando.

**Estado:** completado el 9 de agosto de 2026. La ingesta oficial desde
`manifest.json`, `catalog.json` y `run_results.json` catalogó los 67 tests dbt y
sus resultados; `fct_transaction_quality` muestra 12 pruebas exitosas. Se
documentaron 15 columnas del fact y 7 del mart diario, y se validaron por API y UI
3 aristas con 23 mapeos críticos de columnas. El explorador general funciona
buscando el FQN completo; buscar sólo el nombre corto puede devolver `No data` en
OpenMetadata 1.12.6. La guía operativa distingue PowerShell de CMD y cubre `.venv`,
variables, puertos y cierre seguro de Uvicorn.

### Bloque 3 — Superficies de automatización QA

- Postman Desktop preparado con la colección existente;
- comparación Postman ↔ runner automático;
- Playwright visible, Inspector y trazas;
- casos positivos, negativos y errores intermedios diagnosticables.

**Cierre:** cada validación de API/web puede recorrerse manualmente, automatizarse
y depurarse mediante evidencia visual o reportes.

**Estado:** completado técnicamente el 9 de agosto y recorrido visualmente el 15
de agosto de 2026. Se agregó el entorno local
importable de Postman y el contrato negativo `422`; Newman validó cinco requests y
diez assertions sin fallas. `scripts/run_playwright_lab.py` ofrece los modos
`gate`, `headed`, `inspector` y `trace`; la traza real de los dos recorridos se
generó correctamente y el gate combinado cerró con pytest API `5 passed`,
Playwright `2 passed` y Newman `10/10`. En la introducción guiada, Postman Desktop
ejecutó también cinco requests y diez assertions desde Runner; Playwright se
recorrió en Chrome visible, Inspector y Trace Viewer. La práctica autónoma queda
separada para el modo práctica.

### Bloque 4 — QA mínimo de Power BI

- conexión de sólo lectura a marts;
- visuales mínimos de calidad;
- reconciliación documentada contra SQL, API y panel web.

**Cierre:** las métricas seleccionadas coinciden de extremo a extremo sin exigir
desarrollo avanzado de BI.

**Estado:** completado técnicamente el 9 de agosto y visualmente el 15 de agosto de
2026. Se incorporó un rol
`qa_bi_reader` con sesión de sólo lectura y sin permisos de escritura sobre marts;
dbt reaplica sus grants en cada reconstrucción. Quedaron versionadas dos consultas
Power Query M, cuatro medidas DAX, la especificación de la página y los casos de
diagnóstico. La reconciliación real confirmó fact = mart diario = API con 4.825
transacciones, 200 inconsistentes, 100 sin items y tasa 4,15 %. Power BI Desktop
creó y validó el proyecto textual `powerbi/Data QA Lab.pbip`: cuatro tarjetas,
volumen y tasa por día, y detalle de las 200 transacciones con flag inconsistente.
El repositorio excluye el caché `.pbi` y las credenciales locales.

### Bloque 5 — Modo práctica y defensa profesional

- ruta de aprendizaje por niveles;
- catálogo de ejercicios manual → automático → fallo → diagnóstico → regresión;
- resumen de arquitectura, responsabilidades QA, defectos y decisiones para
  entrevistas.

**Cierre:** el entorno deja de ser sólo una demo y queda preparado para prácticas
repetibles y acumulativas.

**Estado:** completado el 9 de agosto de 2026. `MODO_PRACTICA_DATA_QA.md` organiza
15 ejercicios en tres niveles y obliga a cerrar cada sesión con diagnóstico,
recuperación y regresión. Incluye una matriz por herramienta que separa dominio
Data QA, manejo operativo y conocimiento conceptual. La defensa profesional quedó
preparada en `DEFENSA_PROFESIONAL_DATA_QA.md` con presentaciones de 30 segundos,
dos y cinco minutos, límites de responsabilidad, decisiones, cuatro historias
reales, preguntas de entrevista y afirmaciones respaldadas por evidencia. No se
ejecutaron las prácticas ni se modificó el CV en este bloque.

### Bloque 6 — Reproducibilidad y aceptación final local

- **6B — Aceptación técnica:** arranque desde servicios detenidos y validación
  de los gates de datos, API, web, Airflow y OpenMetadata, sin eliminar volúmenes.
- **6C — Cierre Git local:** revisión de reportes, mapa, cambios y archivos
  publicables; preparación de commits coherentes sin publicación.
- **6A — Gobierno documental, al final:** inventario y sincronización con
  Obsidian usando el estado técnico definitivo. Obsidian queda como fuente de
  verdad para aprendizaje, conceptos, prácticas y desarrollo profesional; los
  repositorios conservan código, operación y evidencia técnica.

**Cierre:** todos los criterios locales quedan en verde desde un arranque limpio.
La secuencia deliberada es `6B → 6C → 6A`, para no sincronizar documentación
provisional ni duplicar contenido que todavía pueda cambiar durante la aceptación.

**Estado 6B:** completado el 10 de agosto de 2026. Se detuvieron los servicios sin
eliminar contenedores, redes ni volúmenes y se reconstruyó el flujo desde RAW. dbt
cerró `PASS=80`, pytest de datos `17 passed / 3 xfailed`, pytest API `5 passed`,
Playwright `2 passed` y Newman `10/10`. La reconciliación confirmó 4.825
transacciones aceptadas, 200 inconsistentes, 100 sin items y tasa 4,15 %. Airflow
ejecutó `manual__2026-08-10T01:54:06.807302+00:00` con cuatro de cuatro tareas en
`success`. OpenMetadata quedó en HTTP 200 con MySQL, Elasticsearch y servidor
saludables; la sincronización confirmó 13 modelos dbt activos, 67 tests
catalogados, 25 relaciones de linaje y 23 mapeos críticos de columnas. El mapa
interactivo pasó la validación de pestañas, selección, consola, layout normal y
ancho reducido sin desborde horizontal.

**Estado 6C:** completado localmente el 10 de agosto de 2026, sin `push`. La
auditoría no encontró JWT, claves privadas, archivos grandes accidentales ni
enlaces locales rotos; los JSON, YAML y módulos Python pasaron validación de
sintaxis. Los cambios quedaron separados en los commits de datos `6058f89`,
automatización y consumidores `0957fc6`, y Airflow `d9f74a7`; la documentación y
el mapa se agrupan en el commit de cierre del bloque. Ambos repositorios pasan
`git diff --check`. Los avisos LF/CRLF describen la conversión futura configurada
por Git y no son errores de whitespace.

**Estado 6A:** completado el 10 de agosto de 2026. El vault activo de Obsidian
quedó sincronizado con la arquitectura `raw → dbt_staging → dbt_intermediate →
dbt_marts`, la línea base validada, los gates, la operación, el linaje y el modo
práctica. Se separaron arquitectura, prácticas y defensa profesional; las notas
de las capas antiguas y de implementaciones previas quedaron identificadas como
históricas en vez de borrarse. Los conceptos CLI/GUI y CI/CD ya estaban incluidos
y la guía futura de Hadoop/Cloudera permanece fuera del lab. No se modificó el
vault de backup ni se cambiaron el CV, LinkedIn o una publicación remota.

### Bloque 7 — Portfolio público y CV

- auditoría de publicación y secretos;
- aprobación explícita del usuario;
- GitHub y primera CI remota;
- actualización del CV y matriz de habilidades con evidencia demostrable;
- definición de la evolución posterior mediante prácticas versionadas.

**Cierre:** existe una primera versión pública estable y defendible, lista para
seguir creciendo sin perder su baseline.

## Stack mínimo acordado

- PostgreSQL
- Python, pytest y pandas
- dbt Core
- Apache Airflow
- Postman
- Playwright
- Docker Compose
- Git y GitHub Actions
- Power BI como capa de visualización
- OpenMetadata como extensión de catálogo y linaje

## Estado general

- [x] Definir el objetivo del laboratorio.
- [x] Seleccionar un stack mínimo sin herramientas redundantes.
- [x] Definir un caso de uso inicial: ventas, clientes, productos, pedidos y pagos.
- [x] Revisar el entorno local y las herramientas disponibles.
- [x] Confirmar la arquitectura definitiva.
- [x] Extender y actualizar el laboratorio existente.
- [x] Completar el núcleo práctico y la documentación de portfolio de la versión 1.
- [x] Completar localmente la aplicación, API y automatización web de la versión 2.

## Fase 0 — Relevamiento del entorno

- [x] Revisar los archivos existentes en el workspace.
- [x] Verificar Python y pip.
- [x] Verificar Git.
- [x] Verificar Docker y Docker Compose.
- [x] Verificar PostgreSQL y sus herramientas de cliente.
- [x] Verificar dbt Core.
- [x] Verificar Apache Airflow.
- [x] Verificar Node.js y npm para Playwright.
- [x] Verificar Postman.
- [x] Verificar Power BI Desktop.
- [x] Buscar una instalación o configuración existente de OpenMetadata.
- [x] Revisar memoria, procesador y espacio disponible.
- [x] Registrar qué está listo, qué falta y qué es opcional.

## Fase 1 — Recuperar y validar la base existente

- [x] Localizar los repositorios `data-qa-lab` y `airflow-lab`.
- [x] Confirmar que ambos repositorios están limpios respecto de `origin/main`.
- [x] Confirmar que existen Docker Compose, SQL por capas, generador de datos y DAG.
- [x] Trasladar `data-qa-lab`, `airflow-lab` y `om-lab` al workspace actual.
- [x] Verificar que las rutas relativas y los tres archivos Compose sigan siendo válidos.
- [x] Crear un entorno virtual propio con Python 3.12.
- [x] Corregir el acceso a Python para el proyecto sin depender del alias de Microsoft Store.
- [x] Preparar variables de entorno de ejemplo sin secretos.
- [x] Iniciar Docker Desktop.
- [x] Levantar y verificar PostgreSQL existente.
- [x] Levantar y verificar el Airflow reducido existente.
- [x] Ejecutar el DAG `qa_pipeline_postgres_v1`.
- [x] Confirmar tablas, conteos y datos actuales.
- [x] Crear una copia de recuperación del volumen MySQL actual de OpenMetadata.
- [x] Intentar extraer la metadata mediante recuperación controlada de InnoDB.
- [x] Recrear MySQL y Elasticsearch de OpenMetadata sólo después de preservar lo recuperable.
- [x] Verificar servidor, UI, servicio PostgreSQL, ingestion y lineage de OpenMetadata.
- [x] Documentar inicio, detención y reinicio del laboratorio.
- [ ] Verificar que otra persona pueda reproducir el entorno.

## Fase 2 — Aplicación bajo prueba

- [x] Crear una API mínima de sólo lectura sobre las métricas y transacciones.
- [x] Crear una interfaz web mínima.
- [x] Reutilizar los datos y defectos controlados de la versión 1.
- [x] Documentar las reglas expuestas por la aplicación.
- [x] Verificar los endpoints, el escenario negativo y los flujos principales.

## Fase 3 — QA de datos con SQL y pytest

- [x] Configurar pytest.
- [x] Configurar la conexión de pruebas a PostgreSQL.
- [x] Validar valores nulos, duplicados y dominios.
- [x] Validar integridad referencial.
- [x] Validar totales de transacciones e ítems.
- [x] Implementar reconciliaciones entre origen y destino.
- [x] Crear pruebas de regresión.
- [x] Generar reportes de ejecución.

## Fase 4 — Transformaciones con dbt

- [x] Inicializar el proyecto dbt.
- [x] Crear modelos `staging`.
- [x] Crear modelos analíticos `marts`.
- [x] Agregar pruebas estándar de dbt.
- [x] Crear pruebas SQL personalizadas.
- [x] Documentar modelos, columnas y linaje.
- [x] Ejecutar `dbt build` correctamente.

## Fase 5 — Orquestación con Airflow

- [x] Integrar la instalación reducida de Airflow existente si resulta adecuada.
- [x] Crear un DAG del pipeline.
- [x] Ejecutar carga, transformación y validaciones.
- [x] Configurar dependencias del flujo.
- [x] Simular y diagnosticar fallos.
- [x] Incorporar controles de calidad como condición del pipeline.
- [x] Integrar `dbt build` como gate previo a pytest.

## Fase 6 — Pruebas de API y web

- [x] Crear una colección de Postman.
- [x] Probar endpoints positivos y escenarios negativos.
- [x] Automatizar pruebas de API con pytest.
- [x] Instalar y configurar Playwright para Python.
- [x] Automatizar flujos web principales.
- [x] Validar consistencia entre web, API y base de datos.

## Fase 7 — CI/CD

- [x] Preparar un comando único para dbt y pytest.
- [x] Crear el workflow de GitHub Actions.
- [ ] Ejecutar pruebas en cada cambio.
- [ ] Publicar reportes o artefactos de prueba.
- [x] Verificar localmente que una falla de calidad bloquee el pipeline.

## Fase 8 — BI, metadatos y portfolio

- [x] Conectar Power BI a los modelos analíticos.
- [x] Validar métricas y agregaciones contra SQL.
- [x] Integrar OpenMetadata si aporta valor al laboratorio.
- [x] Documentar casos de prueba.
- [x] Documentar defectos encontrados y evidencia.
- [x] Crear un README orientado a entrevistas.
- [x] Preparar una explicación breve de arquitectura y decisiones.

## Criterio de finalización

El criterio vigente es el bloque **Definición vigente de “lab completo” — 9 de
agosto de 2026** ubicado al inicio. El cierre exige reproducibilidad y gates
locales, una práctica mínima de reconciliación sobre Power BI, materiales de
práctica y un cierre de portfolio con publicación y primera CI remota verificadas.
La publicación ocurre al final y requiere autorización explícita.

## Resultado del relevamiento

### Conclusión

No conviene crear otro laboratorio desde cero. Ya existe una base avanzada en:

```text
<workspace>/data-qa-lab
<workspace>/airflow-lab
<workspace>/om-lab
```

La estrategia recomendada es recuperar, validar y extender esos repositorios. El valor nuevo debe concentrarse en automatización de QA, dbt, API, Playwright y CI/CD.

### Disponible

| Componente | Estado observado |
|---|---|
| Equipo | 15,9 GB de RAM y 12 procesadores lógicos. |
| Disco | C: 24,6 GB libres; D: 475,8 GB libres. |
| Git | Instalado, versión 2.42.0. Los dos repositorios existentes están limpios sobre `main`. |
| Docker | Docker Desktop 4.73.1, Docker Engine CLI 29.4.3 y Compose 5.1.3 instalados. El daemon estaba detenido durante el relevamiento. |
| PostgreSQL | PostgreSQL 14 y `psql` instalados. El lab además define PostgreSQL 15 en Docker sobre el puerto 5434. |
| DBeaver | Instalado, versión 26.1.0. |
| Python | Python 3.12.2 y Anaconda Python 3.11.5 instalados. El comando global `python` apunta incorrectamente al alias de Microsoft Store. |
| pandas | Disponible en ambas instalaciones de Python. |
| pytest | Versión 9.1.1 instalada en el entorno virtual Python 3.12 del proyecto. |
| Airflow | Implementación reducida existente con Airflow 3.2.1, LocalExecutor y DAG `qa_pipeline_postgres_v1`. |
| OpenMetadata | Instalación Docker 1.12.6 recuperada sobre MySQL y Elasticsearch nuevos. Servidor, UI, ingesta, búsqueda y lineage validados. |
| Power BI | Instalado; Windows registra dos versiones, 2.122 y 2.149. |
| VS Code | Instalado. |

### Falta incorporar o corregir

| Componente | Acción recomendada |
|---|---|
| Python del proyecto | Completado: `.venv` con Python 3.12.2. |
| pytest del proyecto | Completado: pytest y psycopg aislados dentro de `.venv`. |
| dbt Core | Instalado en `.venv`, versión 1.11.12, con adaptador PostgreSQL 1.11.0. |
| Node.js y npm | No están instalados ni son necesarios: Playwright usa Python y Newman usa Docker. |
| Playwright | Instalado en `.venv` con Chromium aislado. |
| Postman | Colección versionada y ejecutada automáticamente mediante Newman en Docker. |
| CI/CD | Workflow local preparado; falta publicar los repositorios y validar la primera ejecución remota. |
| API y web | FastAPI y panel web incorporados sobre `dbt_marts` en modo de sólo lectura. |
| QA automático | Suite estable e integrada como gate de Airflow y del workflow de GitHub Actions. |

### Restricciones y decisiones

- Con 16 GB de RAM, PostgreSQL y el Airflow reducido son adecuados.
- OpenMetadata debe levantarse sólo cuando se practique catálogo o lineage; no necesita ejecutarse durante todas las pruebas.
- Con 24,6 GB libres en C:, se debe vigilar el crecimiento de imágenes y volúmenes de Docker.
- El lab fue trasladado al workspace, no duplicado; las tres carpetas originales ya no permanecen en `C:\entorno-personal`.
- Las rutas relativas de Airflow hacia `data-qa-lab` continúan resolviendo correctamente.
- Los archivos Compose de PostgreSQL, Airflow y OpenMetadata pasan la validación de configuración.
- OpenMetadata informa que la propiedad `version` de Compose es obsoleta, pero no bloquea la configuración.
- La arquitectura base queda confirmada: PostgreSQL y Airflow como núcleo; OpenMetadata se usa bajo demanda para catálogo y lineage.

## Validación operativa — 25 de julio de 2026

### Docker

- [x] Docker Desktop 4.73.1 operativo.
- [x] Docker Engine 29.4.3 operativo.
- [x] Recursos asignados: 4 CPU y aproximadamente 10 GB de RAM.

### PostgreSQL del lab

- [x] Contenedor `qa_lab_postgres` activo sin reinicios.
- [x] PostgreSQL 15.17 acepta conexiones.
- [x] Base `qa_lab` disponible.
- [x] Esquemas `raw`, `curado`, `refinado` y `consumo` disponibles.
- [x] Se encontraron 18 tablas del flujo vigente.
- [x] Conteos posteriores a la ejecución:

```text
raw.transacciones_raw              5000
curado.transacciones_curado        4877
curado.items_transaccion_curado    11691
refinado.transacciones_refinado    4877
consumo.transacciones_consumo      4877
```

### Airflow

- [x] Base interna de Airflow disponible.
- [x] `airflow-init` finalizó con código 0.
- [x] API Server, Scheduler y DAG Processor saludables y sin reinicios.
- [x] No hay errores de importación de DAGs.
- [x] El DAG `qa_pipeline_postgres_v1` está cargado y despausado.
- [x] Ejecución manual `manual__2026-07-26T01:00:31.250422+00:00` finalizada en `success`.
- [x] Las nueve tareas del DAG finalizaron correctamente.
- [x] Los conteos de PostgreSQL permanecieron correctos después del pipeline.

### OpenMetadata

- [x] Compose e imágenes de OpenMetadata 1.12.6 disponibles.
- [x] MySQL nuevo y saludable, sin reinicios.
- [x] Elasticsearch nuevo y saludable, sin reinicios.
- [x] OpenMetadata Server disponible y saludable.
- [x] UI disponible en `http://localhost:8585` con respuesta HTTP 200.
- [x] API de sistema disponible; versión informada: 1.12.6.
- [x] Airflow interno de ingestion saludable.
- [x] Servicio `postgres_lab` y sus tablas recuperados.
- [x] Pipeline de metadata de PostgreSQL ejecutado nuevamente en `success`.
- [x] Pipeline de lineage de PostgreSQL ejecutado nuevamente en `success`.
- [x] Relaciones de lineage recuperadas.
- [x] Índices de búsqueda reconstruidos y sus alias activos.

## Recuperación de OpenMetadata — 25 de julio de 2026

### Diagnóstico inicial

```text
openmetadata_mysql reiniciaba continuamente
InnoDB assertion failure: dict0dict.cc
posible corrupción de tablas y foreign keys
```

### Medidas de seguridad

- [x] OpenMetadata se detuvo antes de manipular los datos.
- [x] Se creó una copia física verificada del MySQL corrupto.
- [x] El directorio corrupto original se apartó sin eliminarlo.
- [x] Se respaldó el volumen original de Elasticsearch.
- [x] Todas las pruebas de recuperación se hicieron sobre copias de trabajo.
- [x] La restauración lógica se validó primero contra un MySQL temporal vacío.

Los artefactos se conservaron en:

```text
<workspace>/om-lab/recovery-backups/20260725_2205_pre_recovery
```

Copias principales:

```text
mysql-original-corrupt
mysql-physical-snapshot
mysql-force-recovery-working
elasticsearch-volume.tar
openmetadata-recovered-rowwise-fixed.sql
```

Verificación de integridad:

```text
openmetadata-recovered-rowwise-fixed.sql
SHA256 23360F3EA743CAFAC58D9738D2D667E1621B5FD6DCEEDD043FB1736FAA5D15D5

elasticsearch-volume.tar
SHA256 D90E117858E768EEE34F5ECB90009FC78C4BC398B8C3CDBD36E1D38FBBAAFFDA
```

### Recuperación realizada

- [x] `innodb_force_recovery=1` se probó sobre una copia, pero no alcanzó para estabilizar InnoDB.
- [x] `innodb_force_recovery=2` permitió iniciar la copia en modo de recuperación.
- [x] Se extrajeron `openmetadata_db` y `airflow_db`.
- [x] Se corrigió mecánicamente un defecto de `mysqldump` 8.0.32 al exportar tablas con columnas generadas.
- [x] El dump corregido se restauró completamente en una base temporal.
- [x] Se creó un MySQL persistente nuevo y se restauró allí el dump validado.
- [x] Se ejecutó la migración de OpenMetadata.
- [x] Se creó un Elasticsearch persistente nuevo.
- [x] Se ejecutó el reindexado completo recomendado por OpenMetadata.

La migración emitió una advertencia no bloqueante al intentar crear la plantilla opcional de búsqueda vectorial de OpenSearch sobre Elasticsearch. La búsqueda normal quedó reconstruida y validada.

### Datos recuperados y validados

```text
airflow_db                         50 tablas
openmetadata_db                   168 tablas
table_entity                      56 registros
dbservice_entity                  2 registros
ingestion_pipeline_entity         10 registros
user_entity                       17 registros
test_case                         6 registros
entity_relationship               295 registros
relaciones tabla-a-tabla del lab  17 registros
```

El catálogo conserva las tablas principales:

```text
postgres_lab.qa_lab.raw.transacciones_raw
postgres_lab.qa_lab.curado.transacciones_curado
postgres_lab.qa_lab.refinado.transacciones_refinado
postgres_lab.qa_lab.consumo.transacciones_consumo
```

Después del reindexado, el índice de tablas contiene los 56 documentos recuperados y el índice de pipelines contiene los 10 pipelines.

## Primera automatización con pytest — 26 de julio de 2026

### Entorno

- [x] `.venv` creado dentro de `data-qa-lab` con Python 3.12.2.
- [x] pytest 9.1.1 instalado únicamente en el entorno virtual.
- [x] psycopg 3.3.4 instalado únicamente en el entorno virtual.
- [x] `requirements-dev.txt` agregado con las dependencias directas.
- [x] `.venv`, cachés, `.env` y resultados locales excluidos de Git.
- [x] `.env.example` agregado sin contraseñas reales.
- [x] La conexión de prueba fuerza `default_transaction_read_only=on`.
- [x] Dependencias verificadas con `pip check`.

### Cobertura inicial

La primera suite cubre:

- conexión, esquemas y tablas indispensables;
- identificadores nulos o duplicados;
- dominios de cantidad, precio y monto;
- integridad entre transacciones, cuentas, canales, estados, ítems y productos;
- reconciliación de conteos entre `raw`, `curado`, `refinado` y `consumo`;
- consistencia entre las capas `refinado` y `consumo`;
- cálculo de flags de calidad;
- dimensiones de fecha de consumo;
- defectos controlados documentados con `xfail(strict=True)`.

Resultado:

```text
23 pruebas recopiladas
19 passed
4 xfailed
0 failed
```

Los cuatro `xfail` actuales no son errores técnicos de pytest: representan anomalías intencionales y controladas del dataset. Si una deja de reproducirse, `strict=True` obliga a revisar y retirar su clasificación.

### Ejecución desde VS Code

Abrir como carpeta:

```text
<workspace>/data-qa-lab
```

Seleccionar como intérprete:

```text
.\.venv\Scripts\python.exe
```

En una terminal PowerShell local, definir la contraseña sin guardarla en Git y ejecutar:

```powershell
$env:QA_DB_PASSWORD="<contraseña local>"
.\.venv\Scripts\python.exe -m pytest
```

Ejecuciones parciales:

```powershell
.\.venv\Scripts\python.exe -m pytest -m smoke
.\.venv\Scripts\python.exe -m pytest -m quality
.\.venv\Scripts\python.exe -m pytest -m "quality and not known_defect"
```

### Uso complementario de DBeaver

DBeaver queda como herramienta de investigación manual: explorar las filas detectadas, ejecutar la consulta SQL de una regla, reunir evidencia y comprender el defecto. VS Code y pytest se usan para convertir esa regla en una prueba repetible. No es necesario instalar otro editor ni otro cliente SQL.

## Guía introductoria — 26 de julio de 2026

- [x] Crear `GUIA_INTRODUCTORIA_LAB_QA.md`.
- [x] Explicar qué es QA de datos y sus nombres habituales.
- [x] Explicar las capas `raw`, `curado`, `refinado` y `consumo`.
- [x] Explicar cada herramienta actual con lenguaje sencillo.
- [x] Diferenciar herramientas actuales de incorporaciones futuras.
- [x] Enumerar alternativas similares sin ampliar innecesariamente el stack.
- [x] Mostrar cómo se conectan las herramientas.
- [x] Explicar qué cubre pytest y por qué no reemplaza Postman o Playwright.
- [x] Agregar un orden recomendado de lectura y aprendizaje.
- [x] Incluir una explicación corta del laboratorio para entrevistas o personas no técnicas.

La guía está pensada como punto de entrada teórico. El plan de acción continúa siendo el documento de control operativo.

## Investigación de defectos conocidos — 26 de julio de 2026

- [x] Crear `REGISTRO_DEFECTOS_LAB_QA.md`.
- [x] Investigar los cinco `xfail` con SQL de sólo lectura.
- [x] Revisar el generador de datos vigente.
- [x] Revisar la transformación RAW → curado.
- [x] Medir el impacto en RAW, curado y refinado.
- [x] Agrupar los síntomas por causa raíz.
- [x] Clasificar anomalías intencionales, defectos de transformación y defectos del generador.
- [x] Definir criterios de aceptación.
- [x] Proponer un orden de corrección.
- [x] Aprobar la modificación del generador y la transformación.
- [x] Crear un respaldo lógico de PostgreSQL y copiar los CSV originales.
- [x] Regenerar el dataset controlado.
- [x] Ejecutar nuevamente el DAG y pytest.

Resultado inicial:

```text
DQA-001  123 montos nulos RAW                anomalía intencional
DQA-002   73 montos negativos RAW            anomalía intencional
DQA-003   73 negativos llegan a curado       defecto de transformación
DQA-004  477 transacciones RAW sin ítems     defecto del generador
DQA-005 4877 montos refinados inconsistentes defecto del generador
```

Los cinco síntomas corresponden a tres causas raíz. No se modificaron datos, transformaciones ni DAGs durante la investigación.

Resultado después de la corrección:

```text
DQA-001  100 montos nulos RAW                anomalía controlada
DQA-002   75 montos negativos RAW            anomalía controlada
DQA-003    0 negativos en curado             defecto cerrado
DQA-004  100 transacciones RAW sin ítems     anomalía controlada
DQA-005  200 inconsistencias refinadas       anomalía controlada
```

El generador ahora es reproducible y la transformación rechaza montos negativos.

## Corrección del dataset y pipeline — 26 de julio de 2026

### Respaldo

- [x] Dump PostgreSQL en formato custom.
- [x] Inventario validado con `pg_restore --list`.
- [x] Copia de los ocho CSV originales.
- [x] Backup excluido de Git.

```text
Ruta:
<workspace>/data-qa-lab/backups/20260726_pre_generator_fix

Archivo:
qa_lab_pre_generator_fix.dump

Tamaño:
843689 bytes

SHA256:
6AFA1F555A2E095B7B0B216EF9EB4FD252AC5935FB34DC4ABBB530F4A3DDE6A8
```

### Generador

- [x] Semilla fija `42`.
- [x] Rutas de salida independientes del directorio actual.
- [x] Dependencias registradas en `requirements-generator.txt`.
- [x] Cada transacción normal recibe al menos un ítem.
- [x] El monto normal se deriva de cantidad por precio.
- [x] Anomalías separadas y explícitas.
- [x] Dos ejecuciones consecutivas produjeron los mismos hashes en los ocho CSV.

```text
Montos nulos controlados              100
Montos negativos controlados           75
Transacciones sin ítems controladas   100
Montos alterados controlados          100
```

### Transformación

- [x] RAW conserva las anomalías para practicar detección.
- [x] RAW → curado excluye montos nulos.
- [x] RAW → curado excluye montos negativos.

### Ejecución

```text
DAG run:
generator_fix_validation_20260726T143258Z

Estado:
success

Tareas:
9 de 9 en success
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

Calidad final:

```text
Montos nulos en curado                 0
Montos negativos en curado             0
Transacciones refinadas consistentes 4625
Anomalías refinadas controladas       200
Diferencias refinado vs. consumo        0
pytest passed                          19
pytest xfailed                          4
pytest failed                           0
```

## Quality gate de pytest en Airflow — 26 de julio de 2026

### Implementación

- [x] Crear la imagen `data-qa-airflow:3.2.1`.
- [x] Mantener Apache Airflow 3.2.1 como imagen base.
- [x] Instalar pytest 9.1.1 y psycopg 3.3.4 en la imagen.
- [x] Montar `tests/` y `pytest.ini` como sólo lectura.
- [x] Configurar la conexión del gate hacia `qa_lab_postgres`.
- [x] Mantener `default_transaction_read_only=on` desde la fixture.
- [x] Agregar `run_pytest_quality_gate` como última tarea.
- [x] Hacer que un código de salida distinto de cero falle la tarea.
- [x] Deshabilitar únicamente la caché de pytest dentro del montaje de sólo lectura.
- [x] Actualizar el import de `PythonOperator` para Airflow 3.

Flujo:

```text
crear tablas
    ↓
cargar RAW
    ↓
RAW → curado
    ↓
curado → refinado
    ↓
refinado → consumo
    ↓
aplicar documentación
    ↓
run_pytest_quality_gate
```

### Validación

```text
DAG run:
pytest_gate_validation_20260726T144513Z

Estado:
success

Tareas:
10 de 10 en success

Quality gate:
19 passed
4 xfailed
0 failed
```

- [x] API Server saludable.
- [x] Scheduler saludable.
- [x] DAG Processor saludable.
- [x] Cero errores de importación.
- [x] Contenedores sin reinicios.
- [x] PostgreSQL del lab no fue recreado.
- [x] Base interna de Airflow no fue recreada.

### Estado dejado al finalizar la validación

- PostgreSQL del lab: activo.
- Airflow reducido: activo y saludable.
- OpenMetadata: activo y saludable.
- Ingestion de OpenMetadata: activo y saludable.
- MySQL y Elasticsearch de OpenMetadata: activos y saludables.
- No se modificaron instalaciones globales; pytest y psycopg existen sólo dentro de `data-qa-lab\.venv`.

## Simulación controlada del quality gate — 26 de julio de 2026

### Preparación

- [x] Mantener el umbral normal de inconsistencias en 5 %.
- [x] Permitir un umbral temporal por corrida mediante `qa_max_inconsistency_rate`.
- [x] Verificar la suite normal antes de simular: 19 passed, 4 xfailed y 0 failed.
- [x] Confirmar que Airflow carga el DAG sin errores.

### Corrida fallida intencional

```text
DAG run:
controlled_failure_20260726T1454Z

Umbral temporal:
1 %

Tasa observada:
4,15 %

Estado:
failed

Tareas:
9 success
1 failed: run_pytest_quality_gate

pytest:
18 passed
4 xfailed
1 failed
```

El gate bloqueó correctamente el DAG porque la tasa observada superó el límite solicitado para la simulación. Los datos no se corrigieron ni ocultaron para obtener este resultado: se cambió únicamente el criterio temporal de aceptación de esa corrida.

### Recuperación

```text
DAG run:
controlled_recovery_20260726T1455Z

Umbral normal:
5 %

Estado:
success

Tareas:
10 de 10 en success
```

- [x] Restaurar el criterio normal mediante una nueva corrida.
- [x] Confirmar que el quality gate vuelve a verde.
- [x] Confirmar que los conteos esperados permanecen iguales.

```text
raw.transacciones_raw              5000
raw.items_transaccion_raw         12000
curado.transacciones_curado        4825
refinado.transacciones_refinado    4825
consumo.transacciones_consumo      4825
anomalías refinadas controladas     200
```

## Primer flujo de versionado Git — 26 de julio de 2026

- [x] Conservar `data-qa-lab` y `airflow-lab` como repositorios separados.
- [x] Verificar identidad Git, ramas, remotos e historial.
- [x] Crear `feature/data-quality-foundation`.
- [x] Crear `feature/airflow-quality-gate`.
- [x] Separar generador, transformación, pruebas, documentación, imagen y DAG en commits coherentes.
- [x] Revisar el área de preparación antes de cada commit.
- [x] Ejecutar pytest y validar Airflow antes de fusionar.
- [x] Fusionar las ramas estables a `main` mediante commits de merge.
- [x] Agregar `docs/GUIA_GIT.md`.
- [ ] Publicar los nuevos commits en GitHub.
- [ ] Incorporar GitHub Actions en una etapa posterior.

Los repositorios remotos ya existen, pero este primer ejercicio se mantiene local hasta revisar el historial final y decidir expresamente su publicación.

## Incorporación de dbt — 26 de julio de 2026

### Entorno y proyecto

- [x] Instalar `dbt-core==1.11.12` dentro de `.venv`.
- [x] Instalar `dbt-postgres==1.11.0`.
- [x] Verificar dependencias con `pip check`.
- [x] Mantener la contraseña fuera de los archivos versionados.
- [x] Crear los esquemas aislados `dbt_staging` y `dbt_marts`.
- [x] Excluir `target`, logs y paquetes descargados de Git.

Modelos:

```text
dbt_staging.stg_transactions             vista
dbt_staging.stg_transaction_items        vista
dbt_marts.fct_transaction_quality        tabla, 4825 filas
dbt_marts.mart_daily_quality             tabla, 90 filas
```

Pruebas:

```text
Pruebas estándar y personalizadas        33
Modelos construidos                       4
Fuentes declaradas                        2
Resultado de dbt build                   PASS=37, ERROR=0
```

Las pruebas cubren claves, nulos, relaciones, valores aceptados, flags recalculados, reconciliación con `consumo` y una tasa máxima configurable de inconsistencias.

### Hallazgo de integración

La primera corrida integrada detectó un defecto real de diseño:

```text
DAG run:
dbt_integration_validation_20260726T1529Z

Problema:
el DDL intentaba borrar curado.transacciones_curado

Impacto:
PostgreSQL bloqueó el DROP porque la vista dbt_staging.stg_transactions
dependía de esa tabla
```

La corrección reemplazó los `DROP TABLE` por `CREATE TABLE IF NOT EXISTS` en las cuatro capas. Las transformaciones continúan usando `TRUNCATE`, por lo que los datos se refrescan sin destruir las tablas ni romper sus dependencias.

### Integración estable en Airflow

```text
DAG run:
dbt_integration_recovery_20260726T1532Z

Estado:
success

Tareas:
11 de 11 en success

dbt:
PASS=37, WARN=0, ERROR=0

pytest:
19 passed, 4 xfailed
```

Flujo final:

```text
crear tablas idempotentes
    ↓
cargar y transformar datos
    ↓
dbt build
    ↓
pytest quality gate
```

### Simulación y recuperación

```text
Corrida fallida:
dbt_gate_failure_20260726T1534Z

Umbral temporal:
1 %

Resultado:
run_dbt_build failed
run_pytest_quality_gate upstream_failed
```

La prueba `assert_inconsistency_rate_below_threshold` bloqueó correctamente la ejecución. Después se restauró el umbral normal:

```text
Corrida recuperada:
dbt_gate_recovery_20260726T1536Z

Umbral:
5 %

Resultado:
11 de 11 tareas en success
```

## Reportes, reproducibilidad y CI — 26 de julio de 2026

### Comandos reutilizables

- [x] Crear `scripts/bootstrap_postgres.py`.
- [x] Crear `scripts/run_quality_checks.py`.
- [x] Generar artefactos dbt en `reports/dbt`.
- [x] Generar JUnit de pytest en `reports/pytest/junit.xml`.
- [x] Generar `reports/summary.json`.
- [x] Excluir reportes y artefactos temporales de Git.

Resultado:

```text
Bootstrap:
raw=5000, curado=4825, refinado=4825, consumo=4825

dbt:
PASS=37, ERROR=0

pytest:
19 passed, 4 xfailed

summary.json:
success
```

### Simulación local de CI

Se creó un PostgreSQL 15 temporal y completamente vacío en el puerto `55432`. Sobre ese entorno se ejecutaron los mismos pasos definidos para GitHub Actions:

1. generar el dataset;
2. crear las tablas;
3. cargar y transformar las cuatro capas;
4. ejecutar dbt;
5. ejecutar pytest;
6. generar reportes.

Todos los pasos aprobaron. El contenedor temporal se eliminó después de la validación y no utilizó un volumen persistente.

### GitHub Actions

- [x] Crear `.github/workflows/data-quality.yml`.
- [x] Configurar PostgreSQL 15 como servicio temporal.
- [x] Instalar dependencias versionadas.
- [x] Ejecutar el bootstrap desde cero.
- [x] Ejecutar el comando único de quality gates.
- [x] Configurar la publicación de `reports/` como artefacto.
- [ ] Publicar los commits en GitHub.
- [ ] Verificar la primera ejecución remota.

### Operación

- [x] Crear `docs/GUIA_OPERATIVA.md`.
- [x] Documentar inicio, controles, simulación, diagnóstico y detención.
- [x] Advertir que no se deben eliminar volúmenes durante una detención normal.

## Etapa 2 — API, web y pruebas de aplicación — 26 de julio de 2026

### Aplicación

- [x] Crear la API de la versión 2 con FastAPI sobre `dbt_marts.fct_transaction_quality`.
- [x] Forzar las conexiones PostgreSQL a sólo lectura.
- [x] Publicar `health`, resumen, listado filtrable y detalle por ID.
- [x] Servir un panel web sin agregar otro framework.
- [x] Mantener la contraseña fuera del repositorio.

Endpoints:

```text
GET /health
GET /api/quality/summary
GET /api/transactions?only_inconsistent=true&limit=10
GET /api/transactions/{transaction_id}
```

### Automatización

```text
pytest API                 5 passed
pytest de datos           19 passed, 4 xfailed
suite completa directa    24 passed, 4 xfailed
Playwright                 2 passed
Postman/Newman             5 requests, 10 assertions, 0 failed
```

- [x] Crear `requirements-app.txt` con versiones fijas.
- [x] Usar Playwright para Python y su Chromium aislado.
- [x] Ejecutar la colección Postman con Newman en Docker.
- [x] Evitar instalar Node.js porque no agrega valor necesario a este alcance.
- [x] Crear `scripts/run_app_checks.py`.
- [x] Separar el gate de datos del gate de aplicación.
- [x] Generar JUnit de pytest API, Playwright y Newman dentro de `reports/`.
- [x] Ampliar GitHub Actions con los controles de API y web.
- [x] Confirmar que una credencial inválida bloquea el gate.
- [x] Recuperar el gate con la conexión correcta y dejar los reportes en verde.
- [x] Actualizar README y guías.

La aplicación se inicia sólo durante el control automático y se detiene al terminar. No depende de Chrome abierto ni modifica los datos.

## Migración al flujo dbt único — 27 de julio de 2026

### Arquitectura

- [x] Definir el flujo objetivo `raw → dbt_staging → dbt_intermediate → dbt_marts`.
- [x] Cambiar las fuentes dbt para leer directamente desde RAW.
- [x] Crear seis modelos de staging.
- [x] Crear cinco modelos intermedios para válidos, rechazados y reglas reutilizables.
- [x] Conservar el motivo de rechazo de transacciones e ítems.
- [x] Adaptar los dos marts para depender de `dbt_intermediate`.
- [x] Reemplazar las reconciliaciones contra la antigua capa `consumo`.
- [x] Retirar `curado`, `refinado` y `consumo` del pipeline activo.
- [x] Mover el SQL anterior a `sql/postgres/legacy/` como referencia histórica.

### Quality gates

- [x] Dejar el DAG en cuatro tareas: crear RAW, cargar RAW, ejecutar dbt y ejecutar pytest.
- [x] Confirmar que pytest sólo se habilita después de un `dbt build` exitoso.
- [x] Aplicar la misma regla de corte al runner local.
- [x] Validar dbt: 13 modelos, 67 pruebas, `PASS=80`, `ERROR=0`.
- [x] Validar pytest de datos: 17 passed, 3 xfailed, 0 failed.
- [x] Ejecutar el DAG real desde Airflow: 4 de 4 tareas en `success`.

Corrida validada en la aceptación final local:

```text
manual__2026-08-10T01:54:06.807302+00:00
create_raw_tables          success
load_raw_postgres          success
run_dbt_build              success
run_pytest_quality_gate    success
```

Defecto técnico detectado y resuelto:

```text
manual__2026-07-27T19:23:08.876914+00:00
run_dbt_build              failed (deadlock ocasional de PostgreSQL)
run_pytest_quality_gate    upstream_failed
```

La recreación concurrente de vistas con `threads: 4` podía producir un deadlock.
Se fijó `threads: 1` en `dbt/profiles.yml`; la corrida validada inmediatamente
posterior confirmó las cuatro tareas en `success`, y la aceptación final del 10 de
agosto volvió a confirmarlas después de un arranque desde servicios detenidos.

### OpenMetadata

- [x] Detener la instalación dañada antes de intervenir.
- [x] Verificar el SHA-256 del respaldo SQL recuperado.
- [x] Mover el volumen MySQL averiado a `db-data-corrupt-20260727` sin eliminarlo.
- [x] Inicializar un volumen MySQL limpio y restaurar el respaldo verificado.
- [x] Ejecutar la migración oficial de OpenMetadata 1.12.6.
- [x] Confirmar MySQL, Elasticsearch y OpenMetadata Server saludables.
- [x] Ejecutar manualmente la ingesta de metadata en `success`.
- [x] Ejecutar manualmente la ingesta de lineage en `success`.
- [x] Confirmar los 13 modelos dbt nuevos en el catálogo.
- [x] Marcar como eliminadas en el catálogo las capas antiguas que ya no existen.
- [x] Confirmar 25 relaciones de linaje activas para el flujo dbt, incluidas las tres dependencias de marts.

### Documentación

- [x] Actualizar README, guía introductoria, guía operativa y mapa técnico.
- [x] Actualizar el mapa interactivo sin cambiar su estilo aprobado.
- [x] Mantener el historial anterior claramente separado del estado actual.

## Próximo paso

La visita guiada y los bloques locales 1 a 6 quedaron completados. El próximo paso
es conversar y decidir el bloque 7 de portfolio público y CV antes de publicar o
modificar perfiles profesionales. Las introducciones guiadas de Postman Desktop,
Playwright y Power BI quedaron completadas; los ejercicios autónomos pertenecen al
modo práctica y no son defectos técnicos.
## Backlog pedagógico — evolución de patrones de carga y PostgreSQL

Conservar el dataset actual y su recarga completa como escenario base reproducible.
Incorporar más adelante ejercicios separados y acumulativos, sin mezclar todos los
patrones en una sola práctica:

- cargas append con lotes de transacciones nuevas y control de duplicados;
- upsert incremental para altas y modificaciones;
- historial de versiones, llegadas tardías y reprocesamiento idempotente;
- trazabilidad por `batch_id`, archivo de origen, fecha y estado del lote;
- índices simples y compuestos, unicidad y comparación con `EXPLAIN ANALYZE`;
- triggers de auditoría o historial, incluyendo sus costos y riesgos operativos;
- stored procedures para procesamiento de lotes y comparación con modelos dbt;
- ejercicios de full refresh, append, incremental y snapshot conservados como
  escenarios independientes;
- simulación controlada de una tarea fallida en Airflow y análisis de `failed`
  frente a `upstream_failed`;
- práctica de `Clear` sobre una instancia, primero aislada y después con alcance
  downstream, verificando qué tareas vuelven a ejecutarse;
- comparación de los alcances upstream, downstream, past, future y failed antes
  de confirmar una limpieza;
- demostración de `Mark success` y `Mark failed` como cambios administrativos de
  estado que no ejecutan código ni revierten efectos, usando una corrida creada
  específicamente para la práctica;
- comprobación de idempotencia y de los datos resultantes después de reejecutar
  el pipeline desde distintos puntos;
- diferenciación práctica entre el grafo downstream de Airflow y el grafo de
  modelos downstream que dbt construye mediante `ref()`.
- practicar propietarios, dominios y responsabilidades sobre los activos ya
  enriquecidos en OpenMetadata, sin convertir administración avanzada del catálogo
  en un requisito del perfil Data QA;
- estudiar por separado la diferencia entre el lenguaje SQL, sus dialectos y
  motores —con PostgreSQL como caso práctico— y el rol de compilación de dbt;
- diseñar casos nuevos en Postman Desktop y comparar su ejecución manual con
  Swagger UI y con Newman, partiendo de la introducción guiada ya completada;
- al terminar la visita guiada, auditar el laboratorio herramienta por herramienta
  y separar claramente el núcleo terminado, las integraciones incompletas, las
  prácticas pendientes y las mejoras opcionales;
- construir una ruta de aprendizaje enfocada en el perfil Data QA que indique qué
  conceptos dominar, cuáles conocer de forma operativa y cuáles dejar fuera de
  alcance en PostgreSQL, SQL, Python, pytest, dbt, Airflow, OpenMetadata, FastAPI,
  Postman/Newman, Playwright, Docker y Git;
- relacionar cada comprobación manual realizada durante la visita con su posible
  automatización y preparar ejemplos concretos que puedan explicarse y defenderse
  en entrevistas, sin exigir dominar por completo cada herramienta.

Este backlog contiene escenarios de práctica posteriores. No debe ampliar la
definición de terminado ni retrasar el paso del laboratorio a modo práctica.
