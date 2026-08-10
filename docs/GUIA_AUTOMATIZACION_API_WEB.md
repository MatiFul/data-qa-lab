# Guía de automatización API y web

Esta guía separa las superficies visuales de los runners automáticos. No son
tres automatizaciones distintas: son maneras diferentes de crear, observar,
ejecutar y diagnosticar las mismas validaciones.

## Qué usar para cada objetivo

| Objetivo | Superficie | Rol en el lab |
|---|---|---|
| Explorar el contrato de la API | Swagger UI (`/docs`) | Probar requests y leer parámetros; no mantiene una suite de regresión. |
| Diseñar y depurar casos de API | Postman Desktop | Ver request, response, variables y assertions. |
| Repetir la colección sin interfaz | Newman | Ejecutar en terminal, scripts y CI exactamente la colección de Postman. |
| Validar la experiencia web | Playwright | Manejar un navegador real y comprobar lo que ve el usuario. |
| Investigar un fallo web | Playwright visible, Inspector y Trace Viewer | Ver la acción, pausar y reconstruir la ejecución. |

El trabajo transferible de QA es decidir escenarios y oráculos, mantener las
assertions, interpretar fallos y conservar evidencia. La interfaz ayuda a explorar
y depurar; el código hace que esa comprobación sea repetible.

## Postman Desktop y Newman

Los archivos versionados son:

```text
postman/data-qa-api.postman_collection.json
postman/data-qa-local.postman_environment.json
```

Cuando Postman Desktop esté disponible, importar ambos archivos y seleccionar el
entorno `Data QA Lab - Local`. La API debe estar iniciada en
`http://127.0.0.1:8000`. No hay secretos en el entorno: `baseUrl` sólo identifica
la instancia local.

La colección contiene cinco requests y diez assertions:

| Caso | Resultado esperado | Tipo |
|---|---:|---|
| API y PostgreSQL disponibles | `200` | positivo operativo |
| Resumen con línea base conocida | `200` y métricas esperadas | positivo de negocio |
| Filtro de inconsistencias | `200` y todas las filas marcadas | positivo de negocio |
| Transacción inexistente | `404` con mensaje controlado | negativo funcional |
| Límite mayor que 100 | `422` asociado a `limit` | negativo de contrato |

Postman permite abrir cada caso y examinar `Body`, `Headers`, `Console` y
`Test Results`. Newman no reemplaza ese trabajo exploratorio: ejecuta el mismo JSON
sin interfaz y produce salida de terminal y JUnit.

El gate completo inicia y detiene una API temporal:

```powershell
.\.venv\Scripts\python.exe scripts\run_app_checks.py
```

El archivo JUnit de Newman queda en `reports/postman/junit.xml`. Si una assertion
falla, primero se identifica el nombre del request y de la assertion; después se
compara el status y body reales con el oráculo del script `pm.test`.

## Playwright: cuatro formas de ejecutar lo mismo

El wrapper inicia una API temporal salvo que se indique `--base-url`. En PowerShell
y CMD se usa el mismo comando porque la variable sensible ya debe estar definida
con la sintaxis correspondiente a cada terminal.

Gate rápido y sin ventana:

```powershell
.\.venv\Scripts\python.exe scripts\run_playwright_lab.py --mode gate
```

Navegador visible:

```powershell
.\.venv\Scripts\python.exe scripts\run_playwright_lab.py --mode headed
```

Inspector, con pausa y ejecución paso a paso:

```powershell
.\.venv\Scripts\python.exe scripts\run_playwright_lab.py --mode inspector
```

Traza y capturas aun cuando el caso aprueba:

```powershell
.\.venv\Scripts\python.exe scripts\run_playwright_lab.py --mode trace
```

Para reducir la ejecución a un caso puede agregarse, por ejemplo:

```powershell
--test e2e/test_quality_dashboard.py::test_inconsistent_filter_updates_visible_rows
```

`gate` conserva traza y captura sólo ante un fallo. `trace` siempre genera
evidencia bajo `reports/playwright/trace/artifacts/`. Esos artefactos son locales y
están excluidos de Git.

Una traza se abre con:

```powershell
.\.venv\Scripts\python.exe -m playwright show-trace <ruta-al-trace.zip>
```

## Diagnóstico por punto de falla

| Evidencia | Punto probable | Primera comprobación |
|---|---|---|
| Uvicorn no inicia o `/health` no responde | API, puerto o variable de conexión | `reports/playwright/api.log` o `reports/api.log`. |
| HTTP `503` en health | conexión API → PostgreSQL | contenedor, puerto y `QA_DB_*`. |
| HTTP correcto y assertion Postman/Newman roja | contrato u oráculo | body real frente a `pm.test`. |
| API verde y locator Playwright rojo | interfaz o selector | captura, traza y DOM observado. |
| Timeout de navegación | API inaccesible o carga web bloqueada | URL base, log de API y pestaña Network de la traza. |
| Datos visibles distintos del resumen | transformación o caché obsoleto | reconciliar mart → API → panel. |

No se guarda una prueba intencionalmente rota dentro del gate. Para practicar un
defecto se modifica temporalmente un oráculo o se apunta a una URL controladamente
inválida, se observa la evidencia y se revierte el ejercicio. El estado normal del
repositorio siempre debe cerrar en verde.
