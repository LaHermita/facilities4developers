# Estado del proyecto

> Registro cronológico de los cambios y decisiones del repositorio. Se actualiza al cerrar cada fase de trabajo.

## Fase 1 - Corrección del generador y normalización de cabeceras

- **Fecha:** 2026-11-04
- **Estado:** completada
- **Alcance:** `generar_readme.py`, cabeceras de los scripts, `README.md` y documentación.

### Objetivo

Eliminar los fallos visibles del índice generado y dejar una base fiable antes de reescribir el parser:

1. Evitar que el generador se indexe a sí mismo.
2. Detectar la cabecera de Python de forma fiable.
3. Corregir la detección de cabeceras en Bash.
4. Normalizar las cabeceras incompletas.
5. Alinear la validación con el formato definido en `PROMPT - Generar Cabecera Scripts.md`.

### Cambios realizados

| Archivo | Cambio |
| --- | --- |
| `generar_readme.py` | Auto-exclusión dinámica mediante `os.path.basename(__file__)`. |
| `generar_readme.py` | Cabecera Python extraída con `ast.get_docstring()` en lugar de buscar el primer bloque `"""..."""`. |
| `generar_readme.py` | Nuevas funciones `extraer_cabecera_python`, `extraer_cabecera_powershell` y `extraer_cabecera_bash`. |
| `generar_readme.py` | Corregido el patrón Bash: ahora acepta `# ====` y `#====`, con o sin espacio. |
| `generar_readme.py` | La versión ausente se representa como `None`; ya no se confunde con una versión `1.0` real. |
| `generar_readme.py` | `Uso` y `Ejemplo` dejan de ser obligatorios, en línea con el `PROMPT`. Solo `Descripción` y `Versión` marcan un script como incompleto. |
| `generar_readme.py` | Su propia cabecera se actualizó (`Versión: 1.0.1`, `Uso` correcto y `Ejemplo`). |
| `generar_readme.py` | El README generado incluye ahora enlaces a esta guía y a `GUIA_CABECERAS_SCRIPTS.md`. |
| `generar_mapa.py` | Añadidas las secciones `Versión: 1.0.1` y `Descripción:`, más la lista de dependencias. |
| `filtrador_logs_4_multigenerico.py` | Añadidas las secciones `Uso` y `Ejemplo` a la cabecera. |
| `PROMPT - Generar Cabecera Scripts.md` | Actualizada la referencia al generador (`generar_readme.py`) y añadido enlace a la guía. |
| `README.md` | Regenerado automáticamente. |

### Decisiones tomadas

- **El generador se excluye a sí mismo del índice.** Se conserva la intención del antiguo `ARCHIVOS_EXCLUIDOS`, pero ahora la exclusión usa el nombre real del archivo y no se rompe si se renombra.
- **La versión ausente no se inventa.** Para mostrar el índice se usa `1.0` como texto de respaldo, pero la validación distingue entre "versión 1.0" y "versión no especificada".
- **`Uso` y `Ejemplo` son opcionales.** El `PROMPT` ya los definía así; la validación ahora lo respeta.
- **Los `*_README.md` externos mantienen prioridad** sobre la cabecera del script. Esto se revisará en la Fase 2 para que la cabecera sea la única fuente de verdad del índice.

### Verificación

Comandos ejecutados:

```bash
python3 -m py_compile generar_readme.py generar_mapa.py filtrador_logs_4_multigenerico.py
python3 generar_readme.py
```

Resultado del generador:

```text
PROCESADOS: 6
INCOMPLETOS: 0
ERRORES: 0
```

Scripts indexados:

- `comprobadorarhivos`
- `controladorversionescarpetas`
- `controladorversionescarpetasmanual`
- `copiadeseguridad_docker_4w10`
- `filtrador_logs_4_multigenerico`
- `generar_mapa`

También se probaron de forma aislada la extracción de una cabecera Bash y de una cabecera PowerShell, incluida la lectura de la versión.

### Pendiente para la Fase 2

1. Sustituir los regex de secciones por un parser de líneas que conserve el contenido multilínea.
2. Renderizar `Uso` y `Ejemplo` como bloques de código y `Dependencias` como lista.
3. Dar prioridad a la cabecera del script sobre los `*_README.md` externos.
4. Añadir `--check` y `--strict` para validar el índice en pre-commit o CI.
5. Añadir tests de las tres sintaxis de cabecera (`.py`, `.ps1`, `.sh`).

## Fase 2 - Renombrado de scripts y normalización de cabeceras

- **Fecha:** 2026-11-11
- **Estado:** completada
- **Alcance:** `generar_readme_automatico.py`, cabeceras de scripts, `README.md`, `AGENTS.md` y `docs/`.

### Objetivo

Dejar todos los scripts indexables sin avisos, alinear los nombres con su función y trasladar toda la documentación a `docs/`.

### Cambios realizados

| Archivo | Cambio |
| --- | --- |
| `comprobadorarhivos.py` | Renombrado a `comprobador_enlaces_arhivos.py`; `Uso`/`Ejemplo` actualizados; versión `1.0.2`. |
| `controladorversionescarpetas.py` | Renombrado a `versionar_carpeta.py`; cabecera canónica; versión `2.1.1`. |
| `controladorversionescarpetasmanual.py` | Renombrado a `versionar_carpeta_ignore.py`; cabecera canónica; versión `1.1.1`. |
| `generar_mapa.py` | Renombrado a `generar_mapa_vivero.py`; cabecera canónica; versión `1.19.1`. |
| `generar_cartografia.py` | Cabecera canónica; versión `2.3.1`. |
| `generar_cartografia_total.py` | Cabecera canónica; versión `2.8.1`. |
| `generar_cartografia_total_cacsa.py` | Cabecera canónica; versión `2.5.1`. |
| `generar_arbol_contenidos_md.py` | Cabecera canónica; versión `1.4.2`. |
| `backup_viveros.py` | Renombrado a `backup_carpeta_zip.py`; cabecera añadida; versión `1.0.0`. |
| `generar_readme.py` | Renombrado a `generar_readme_automatico.py`; enlaces a `docs/`, badges sin destinos inexistentes; versión `1.0.3`. |
| `AGENTS.md` | Nuevo. Convenciones de estructura, nombres, cabeceras y validación. |
| `.gitignore` | Añadidos `__pycache__/`, `*.pyc`, `.venv/` y `venv/`. |

### Verificación

```bash
python3 -m py_compile *.py
python3 generar_readme_automatico.py
```

```text
PROCESADOS: 10
INCOMPLETOS: 0
ERRORES: 0
```
