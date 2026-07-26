# Guía introductoria del laboratorio de QA de datos

> Documento introductorio versionado junto con el laboratorio.

## 1. ¿Qué estamos construyendo?

Este laboratorio sirve para practicar cómo comprobar que los datos de un sistema sean correctos, completos, coherentes y confiables.

El trabajo suele aparecer en búsquedas laborales con nombres como:

- Data QA
- Data Quality
- Data Testing
- ETL Testing
- Database Testing
- QA de datos
- QA de pipelines
- Data Quality Engineer
- QA Automation orientado a datos

La idea principal es sencilla:

> Un dato no es confiable sólo porque llegó a una tabla. Hay que comprobar de dónde vino, qué transformaciones recibió y si el resultado cumple las reglas esperadas.

En este laboratorio usamos transacciones, cuentas, clientes, productos e ítems. Los datos atraviesan varias capas y contienen algunos errores intencionales para aprender a detectarlos.

## 2. El recorrido de los datos

```text
Generador de datos
        |
        v
Archivos y datos de origen
        |
        v
PostgreSQL: RAW
        |
        v
PostgreSQL: CURADO
        |
        v
PostgreSQL: REFINADO
        |
        v
PostgreSQL: CONSUMO
        |
        v
Power BI o una aplicación
```

Las herramientas acompañan ese recorrido:

```text
Docker Compose levanta los servicios

Airflow ejecuta el pipeline
        |
        v
PostgreSQL guarda y transforma los datos
        ^
        |
Python + pytest ejecutan pruebas automáticas

DBeaver permite investigar manualmente con SQL
VS Code permite escribir pruebas, SQL y configuración
OpenMetadata registra catálogo, metadata y lineage
Git guarda el historial del código
```

## 3. Las capas de datos

### RAW

También se conoce como capa cruda, bronze, landing o staging inicial.

Contiene los datos muy parecidos a como llegaron del origen. Puede tener nulos, duplicados, formatos incorrectos o relaciones rotas. No significa que todo error sea aceptable: significa que todavía no se aplicaron todas las reglas de limpieza.

### CURADO

También puede llamarse cleansed, cleaned, silver o staging depurado.

Contiene datos filtrados, normalizados y relacionados con sus catálogos. En esta capa esperamos menos defectos que en RAW.

### REFINADO

También puede llamarse enriched, business, gold o intermediate.

Agrega cálculos y reglas de negocio. En nuestro caso calcula el monto de los ítems y genera indicadores como `flag_sin_items` y `flag_inconsistencia_monto`.

### CONSUMO

También se conoce como serving, presentation, mart o capa analítica.

Es la versión preparada para dashboards, reportes, APIs o usuarios finales. Debe ser fácil de consultar y mantener consistencia con la capa anterior.

Estos nombres no son universales. Una empresa puede usar `bronze/silver/gold`, mientras otra usa `raw/staging/marts`. Lo importante es entender la función de cada capa.

## 4. Herramientas que ya usamos

### Visual Studio Code

**También se conoce como:** VS Code, editor de código o IDE liviano.

**Qué es:** una aplicación para trabajar con archivos de código, SQL y configuración.

**Para qué la usamos:** escribir y ejecutar pruebas de Python y pytest, revisar SQL, editar DAGs de Airflow y trabajar con Git.

**Para qué más se usa:** desarrollo web, APIs, automatización, análisis de datos, infraestructura y prácticamente cualquier lenguaje.

**Herramientas parecidas:** PyCharm, IntelliJ IDEA, Cursor, Sublime Text, Notepad++.

### DBeaver

**También se conoce como:** cliente SQL, cliente de base de datos, database client o SQL IDE.

**Qué es:** una interfaz visual para conectarse a bases de datos.

**Para qué la usamos:** explorar esquemas y tablas, ejecutar SQL, buscar ejemplos de datos defectuosos y reunir evidencia antes de automatizar una regla.

**Para qué más se usa:** administrar conexiones, exportar resultados, revisar planes de ejecución y trabajar con distintos motores desde una sola aplicación.

**Herramientas parecidas:** DataGrip, pgAdmin, SQL Developer, HeidiSQL, Azure Data Studio.

### PostgreSQL

**También se conoce como:** Postgres, motor de base de datos, DBMS o RDBMS.

**Qué es:** un sistema de base de datos relacional que guarda información en tablas y permite consultarla con SQL.

**Para qué lo usamos:** almacenar las capas `raw`, `curado`, `refinado` y `consumo`, ejecutar transformaciones y validar datos.

**Para qué más se usa:** backends de aplicaciones, sistemas transaccionales, reporting, geolocalización y almacenamiento de documentos JSON.

**Herramientas parecidas:** MySQL, SQL Server, Oracle Database, MariaDB, SQLite.

### Docker Desktop y Docker Compose

**También se conocen como:** Docker, contenedores, container runtime y Compose.

**Qué son:** Docker ejecuta aplicaciones en contenedores aislados. Docker Compose describe varios contenedores en un archivo YAML y permite iniciarlos juntos.

**Para qué los usamos:** levantar PostgreSQL, Airflow, OpenMetadata, MySQL y Elasticsearch sin instalarlos y configurarlos uno por uno en Windows.

**Para qué más se usan:** desarrollo local, pruebas de integración, microservicios, CI/CD y despliegues.

**Herramientas parecidas:** Podman, Rancher Desktop, containerd, Kubernetes.

Docker no es una máquina virtual completa. Un contenedor empaqueta una aplicación y sus dependencias, pero comparte parte de la infraestructura del sistema anfitrión.

### Python

**También se conoce como:** lenguaje de programación, lenguaje de scripting o runtime de Python.

**Qué es:** un lenguaje utilizado para automatización, testing, datos, APIs e inteligencia artificial.

**Para qué lo usamos:** escribir pruebas automáticas, conectarnos a PostgreSQL y convertir reglas SQL en controles repetibles.

**Para qué más se usa:** análisis de datos, machine learning, desarrollo de APIs, scraping, automatización y procesamiento de archivos.

**Herramientas o lenguajes parecidos:** Java, JavaScript/TypeScript, C#, R, Scala.

### psycopg

**También se conoce como:** driver, conector o cliente PostgreSQL para Python.

**Qué es:** una librería que permite que un programa Python se conecte a PostgreSQL.

**Para qué la usamos:** pytest envía consultas SQL a la base mediante psycopg y recibe los resultados para validarlos.

**Para qué más se usa:** aplicaciones Python, APIs, procesos batch y scripts de carga.

**Herramientas parecidas:** SQLAlchemy, asyncpg, pg8000.

### pytest

**También se conoce como:** framework de testing, test runner o framework de automatización.

**Qué es:** una herramienta de Python que descubre, ejecuta y reporta pruebas automáticas.

**Para qué la usamos:** comprobar nulos, duplicados, dominios, relaciones, conteos, cálculos y reconciliaciones entre capas.

**Para qué más se usa:** unit testing, pruebas de APIs, integración, regresión, aplicaciones Python y validación de archivos.

**Herramientas parecidas:** unittest, Robot Framework, JUnit, NUnit, Jest.

pytest es el coordinador de las pruebas, pero no reemplaza automáticamente todas las herramientas de QA:

- Puede probar una API si lo combinamos con una librería HTTP.
- No controla un navegador por sí solo; para eso puede combinarse con Playwright o Selenium.
- No controla una aplicación móvil por sí solo; para eso suele usarse Appium.
- No reemplaza Postman como herramienta visual de exploración manual de APIs.

### Apache Airflow

**También se conoce como:** Airflow, orquestador, workflow orchestrator o scheduler.

**Qué es:** una plataforma para definir tareas, dependencias y horarios de ejecución.

**Para qué la usamos:** ejecutar en orden las cargas y transformaciones del pipeline y disparar pytest como control final de calidad.

**Para qué más se usa:** pipelines ETL/ELT, tareas batch, machine learning, reportes programados y coordinación de procesos.

**Herramientas parecidas:** Dagster, Prefect, Luigi, Azure Data Factory, AWS Step Functions.

En Airflow un flujo se representa mediante un **DAG**: un grafo que indica qué tareas existen y en qué orden deben ejecutarse.

Airflow no guarda los datos principales y no reemplaza PostgreSQL. Su función es coordinar procesos.

### OpenMetadata

**También se conoce como:** catálogo de datos, metadata platform, data catalog o herramienta de lineage.

**Qué es:** una plataforma que registra información acerca de los datos.

**Para qué la usamos:** explorar tablas y columnas, documentar servicios, visualizar lineage y observar ejecuciones de ingesta de metadata.

**Para qué más se usa:** gobierno de datos, propietarios, glosarios, clasificación, profiling, calidad y descubrimiento de activos.

**Herramientas parecidas:** DataHub, Apache Atlas, Collibra, Alation, Microsoft Purview.

**Metadata** significa “datos acerca de los datos”: nombre de una tabla, descripción de una columna, tipo, propietario, etiquetas o fecha de actualización.

**Lineage** significa linaje o trazabilidad: muestra de dónde salió un dato, por qué transformaciones pasó y qué elementos dependen de él.

OpenMetadata observa y documenta. Airflow ejecuta. PostgreSQL almacena. Son funciones diferentes.

### Git

**También se conoce como:** control de versiones o VCS.

**Qué es:** un sistema que guarda el historial de cambios de archivos.

**Para qué lo usamos:** versionar SQL, pruebas, DAGs y documentación del laboratorio.

**Para qué más se usa:** desarrollo colaborativo, ramas, revisión de cambios y recuperación de versiones anteriores.

**Herramientas parecidas:** Mercurial, Subversion.

Git no es lo mismo que GitHub. Git funciona localmente; GitHub es un servicio que aloja repositorios Git y agrega colaboración y automatización.

## 5. Herramientas que incorporaremos después

### dbt Core

**También se conoce como:** dbt, herramienta de transformación SQL o analytics engineering tool.

**Qué es:** organiza transformaciones SQL como modelos versionados y permite agregar pruebas y documentación.

**Para qué lo usaremos:** reemplazar progresivamente SQL suelto por modelos, dependencias y tests mantenibles.

**Para qué más se usa:** data warehouses, documentación, lineage y CI/CD de transformaciones.

**Herramientas parecidas:** Dataform, SQLMesh, Matillion, Coalesce.

### Postman

**También se conoce como:** API client o herramienta de API testing.

**Qué es:** una interfaz visual para enviar peticiones a una API y revisar sus respuestas.

**Para qué lo usaremos:** explorar manualmente la futura API del laboratorio y guardar ejemplos positivos y negativos.

**Para qué más se usa:** documentación de APIs, colecciones, variables de entorno y pruebas automáticas básicas.

**Herramientas parecidas:** Insomnia, Bruno, Hoppscotch, SoapUI.

### Playwright

**También se conoce como:** browser automation, UI automation o framework E2E.

**Qué es:** una herramienta que controla navegadores y automatiza acciones de usuario.

**Para qué lo usaremos:** validar que lo mostrado en la futura interfaz web coincida con la API y PostgreSQL.

**Para qué más se usa:** regresión web, capturas, pruebas en varios navegadores y pruebas visuales.

**Herramientas parecidas:** Selenium, Cypress, WebdriverIO, Puppeteer.

### Power BI

**También se conoce como:** herramienta de BI, reporting o visualización.

**Qué es:** una aplicación para crear modelos, métricas y dashboards.

**Para qué lo usaremos:** conectar la capa `consumo` y verificar que totales, filtros y agregaciones coincidan con SQL.

**Para qué más se usa:** análisis de negocio, modelos semánticos, reportes ejecutivos y publicación de tableros.

**Herramientas parecidas:** Tableau, Looker, Qlik Sense, Metabase.

### GitHub Actions

**También se conoce como:** CI/CD, pipeline de integración continua o workflow.

**Qué es:** la automatización de GitHub que ejecuta tareas cuando cambia un repositorio.

**Para qué lo usaremos:** ejecutar pytest y dbt automáticamente y bloquear cambios si fallan reglas importantes.

**Para qué más se usa:** builds, despliegues, análisis de seguridad y publicación de artefactos.

**Herramientas parecidas:** GitLab CI, Jenkins, Azure DevOps Pipelines, CircleCI.

## 6. Cómo se conectan en una ejecución real

Un ciclo completo puede verse así:

1. Docker Compose inicia PostgreSQL y Airflow.
2. Airflow ejecuta SQL para cargar RAW.
3. Airflow ejecuta las transformaciones hacia curado, refinado y consumo.
4. pytest se conecta a PostgreSQL mediante psycopg.
5. Cada prueba ejecuta una consulta y compara el resultado con una regla.
6. Si una regla falla, DBeaver ayuda a investigar las filas involucradas.
7. OpenMetadata muestra las tablas, columnas y relaciones de lineage.
8. Power BI consulta la capa de consumo.
9. Git registra los cambios realizados en pruebas y transformaciones.
10. GitHub Actions podrá repetir las pruebas automáticamente.

Ejemplo de una regla:

```text
Regla de negocio:
Toda transacción debe tener una cuenta existente.

SQL:
Buscar transacciones cuyo id_cuenta no aparece en cuentas.

pytest:
Ejecutar el SQL y exigir que el resultado sea cero.

DBeaver:
Si el resultado no es cero, abrir las filas y reunir evidencia.

Airflow:
Evitar que el pipeline continúe si la regla es crítica.
```

## 7. Qué valida un QA de datos

### Completitud

¿Faltan datos obligatorios? Ejemplo: montos nulos.

### Unicidad

¿Un identificador aparece más de una vez?

### Validez o dominio

¿El valor pertenece al rango esperado? Ejemplo: cantidad mayor que cero.

### Integridad referencial

¿Las relaciones existen? Ejemplo: una transacción apunta a una cuenta válida.

### Consistencia

¿El mismo dato coincide entre dos capas o sistemas?

### Exactitud

¿El cálculo representa correctamente la realidad o la regla de negocio?

### Reconciliación

¿Los conteos, importes y registros de origen coinciden con los del destino?

### Actualidad

¿Los datos llegaron dentro del tiempo esperado?

### Regresión

¿Una transformación que antes funcionaba sigue funcionando después de un cambio?

## 8. Defectos conocidos y `xfail`

Nuestro dataset tiene anomalías intencionales para practicar:

- montos RAW nulos;
- montos negativos;
- transacciones sin ítems;
- algunas diferencias entre el monto de cabecera y el calculado desde los ítems.

Las capas confiables aplican reglas adicionales: los montos nulos y negativos permanecen visibles en RAW para practicar detección, pero no pasan a curado.

pytest las marca como `xfail`, abreviatura de **expected failure** o fallo esperado.

Esto no significa ignorarlas. Significa:

1. La regla está automatizada.
2. El defecto está reconocido.
3. La suite puede continuar mientras se decide la corrección.
4. Si el defecto desaparece, `strict=True` obliga a revisar el test.

En un trabajo real, cada `xfail` debería estar relacionado con un ticket, una decisión o una fecha de revisión.

## 9. Carpetas principales

```text
07 QA nuevo/
|
|-- data-qa-lab/       Datos, SQL y pruebas pytest
|   |-- .venv/         Python aislado del proyecto
|   |-- docs/          Plan, guías y registro de defectos
|   |-- sql/           DDL y transformaciones
|   |-- tests/         Pruebas automáticas
|   |-- pytest.ini     Configuración de pytest
|
|-- airflow-lab/       DAGs y configuración de Airflow
|
|-- om-lab/            OpenMetadata, MySQL y Elasticsearch
```

## 10. Orden recomendado para aprender

1. Comprender las cuatro capas de PostgreSQL.
2. Abrir tablas y ejecutar consultas sencillas en DBeaver.
3. Leer una prueba de `tests/test_raw_quality.py`.
4. Relacionar su SQL con la regla que valida.
5. Ejecutar pytest desde VS Code.
6. Investigar un `xfail` en DBeaver.
7. Revisar el DAG y entender el orden del pipeline.
8. Abrir OpenMetadata y observar tablas y lineage.
9. Incorporar dbt.
10. Agregar API, Postman, interfaz web y Playwright.

No hace falta dominar todas las herramientas al mismo tiempo. Para empezar, el núcleo práctico es:

```text
SQL + PostgreSQL + DBeaver
Python + pytest + VS Code
Docker Compose
Airflow básico
Git básico
```

OpenMetadata, dbt, Postman, Playwright, Power BI y CI/CD se agregan cuando el flujo principal ya se entiende.

## 11. Explicación corta del laboratorio

Si tuvieras que explicárselo a alguien sin experiencia técnica:

> El laboratorio simula el recorrido de datos de una empresa. PostgreSQL guarda la información en distintas etapas, Airflow ejecuta los procesos, Python y pytest comprueban automáticamente que los datos cumplan reglas, DBeaver permite investigar errores, OpenMetadata muestra de dónde vienen los datos y VS Code es el lugar donde escribimos y mantenemos todo. Docker permite ejecutar los componentes de forma aislada y Git conserva el historial de cambios.
