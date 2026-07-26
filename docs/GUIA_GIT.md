# Guía breve de Git para el laboratorio

## Objetivo

Usar Git como parte del trabajo de QA: aislar una mejora, revisar exactamente qué cambió, guardar avances comprensibles y volver a un estado estable cuando sea necesario.

## Organización elegida

El laboratorio conserva dos repositorios:

- `data-qa-lab`: datos, generador, SQL, pytest y documentación.
- `airflow-lab`: imagen de Airflow, Docker Compose y DAGs.

Cada repositorio mantiene su propio historial. OpenMetadata queda fuera de estos commits porque contiene infraestructura, volúmenes y respaldos que no deben agregarse accidentalmente.

## Ciclo de trabajo

```text
main estable
    ↓
crear rama feature/...
    ↓
modificar y ejecutar pruebas
    ↓
revisar git status y git diff
    ↓
agregar archivos relacionados
    ↓
crear un commit pequeño
    ↓
volver a validar
    ↓
fusionar en main
```

## Comandos esenciales

Consultar la situación actual:

```powershell
git status
git diff
git log --oneline --decorate --graph
```

Crear una rama:

```powershell
git switch -c feature/nombre-corto
```

Preparar únicamente archivos relacionados:

```powershell
git add ruta/al/archivo
git diff --staged
```

Crear el commit:

```powershell
git commit -m "tipo(area): descripción breve"
```

Volver a `main` y fusionar una rama validada:

```powershell
git switch main
git merge --no-ff feature/nombre-corto
```

## Tipos de commit utilizados

| Tipo | Uso |
|---|---|
| `feat` | Nueva capacidad. |
| `fix` | Corrección de un defecto. |
| `test` | Pruebas nuevas o modificadas. |
| `docs` | Documentación. |
| `build` | Imagen, dependencias o configuración de construcción. |
| `chore` | Mantenimiento que no cambia la funcionalidad. |

Ejemplos:

```text
feat(generator): make QA dataset reproducible
fix(transform): reject negative curated amounts
test(data): add PostgreSQL quality suite
feat(airflow): add pytest quality gate
docs: document controlled failure exercise
```

## Reglas prácticas

- No agregar contraseñas, archivos `.env`, entornos virtuales, logs, volúmenes o backups.
- Revisar `git diff --staged` antes de cada commit.
- No mezclar una corrección SQL, documentación y configuración Docker sin una razón.
- Ejecutar las pruebas antes de fusionar.
- Mantener `main` como el último estado estable demostrado.
- Publicar en GitHub sólo después de revisar el historial local.

## Próxima evolución

Cuando este flujo resulte natural, el siguiente nivel será publicar las ramas en GitHub, abrir pull requests y ejecutar pytest automáticamente mediante GitHub Actions.
