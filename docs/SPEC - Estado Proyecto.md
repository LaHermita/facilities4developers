# Estado del proyecto

> Estado actual del repositorio. Se actualiza al cerrar cada fase de trabajo. No conserva referencias a nombres o archivos retirados.

## Estado actual

- **Última actualización:** 2026-11-11
- **Scripts indexados:** 10
- **Incompletos:** 0
- **Errores:** 0

## Estructura

- Scripts ejecutables en la raíz.
- Documentación en `docs/`.
- `README.md` generado por `generar_readme_automatico.py`; no editar a mano.
- `AGENTS.md` define las convenciones de mantenimiento.

## Scripts

| Script | Versión | Función |
| --- | --- | --- |
| `backup_carpeta_zip.py` | 1.0.0 | Copia de seguridad ZIP de una carpeta. |
| `comprobador_enlaces_archivos.py` | 1.0.3 | Verifica recursos multimedia referenciados. |
| `copiadeseguridad_docker_4w10.ps1` | 1.0.0 | Backup con Docker Compose. |
| `generar_arbol_contenidos_md.py` | 1.4.2 | Árbol de contenidos en Markdown. |
| `generar_cartografia.py` | 2.3.1 | Cartografía LH en PNG y Markdown. |
| `generar_cartografia_total.py` | 2.8.1 | Cartografía total LH. |
| `generar_cartografia_total_cacsa.py` | 2.5.1 | Cartografía corporativa CACSA. |
| `generar_mapa_vivero.py` | 1.19.1 | Mapa de proyectos desde manifest.json. |
| `versionar_carpeta.py` | 2.1.1 | Versiona subcarpetas copiadas. |
| `versionar_carpeta_ignore.py` | 1.1.1 | Snapshots ignorando .gitignore. |

## Generador

`generar_readme_automatico.py` (`1.0.3`):

1. Recorre solo la raíz y procesa `.py`, `.sh` y `.ps1`.
2. Se excluye a sí mismo.
3. Usa `<nombre>_README.md` si existe; si no, la cabecera del script.
4. Extrae `Versión`, `Descripción`, `Dependencias`, `Uso`, `Ejemplo` y `Requisitos`.
5. Marca `⚠️` si falta `Versión` o `Descripción`.
6. Recorta la descripción a 200 caracteres.

## Verificación

```bash
python3 -m py_compile *.py
python3 generar_readme_automatico.py
```

```text
PROCESADOS: 10
INCOMPLETOS: 0
ERRORES: 0
```

## Pendiente

1. Sustituir los regex de secciones por un parser de líneas que conserve el contenido multilínea.
2. Renderizar `Uso` y `Ejemplo` como bloques de código y `Dependencias` como lista.
3. Dar prioridad a la cabecera del script sobre los `*_README.md` externos.
4. Añadir `--check` y `--strict` para validar el índice en pre-commit o CI.
5. Añadir tests de las tres sintaxis de cabecera (`.py`, `.ps1`, `.sh`).
