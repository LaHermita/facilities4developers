# Guía de cabeceras para scripts

> Cómo documentar un script para que `generar_readme_automatico.py` lo indexe correctamente y el README del repositorio quede siempre completo.

## 1. Formato canónico

Todas las cabeceras usan las mismas etiquetas, en el mismo orden y con el contenido en la línea siguiente:

```text
Título descriptivo del script

Versión: X.Y.Z

Descripción:
Una línea de máximo 200 caracteres explicando qué hace el script.

Dependencias:
- os
- argparse

Uso:
comando de ejemplo (puede ocupar varias líneas)

Ejemplo:
comando concreto de uso
```

Solo `Versión` y `Descripción` son obligatorias. `Dependencias`, `Uso` y `Ejemplo` se incluyen cuando aportan información.

## 2. Reglas

1. La primera línea del bloque es el título, sin prefijos, negritas ni markdown.
2. `Versión:` debe existir siempre y usar el formato `X.Y.Z`.
3. `Descripción:` debe existir siempre; máximo 200 caracteres.
4. Usa exactamente estas etiquetas al inicio de línea:
   - `Versión:`
   - `Descripción:`
   - `Dependencias:`
   - `Uso:`
   - `Ejemplo:`
5. El contenido de cada sección empieza en la línea siguiente.
6. Deja una línea en blanco entre secciones.
7. No uses `##`, `**`, bloques de código ni otros elementos markdown dentro de la cabecera.
8. No repitas secciones ni cambies su orden.
9. `Uso` solo es necesario si el script acepta argumentos o parámetros.
10. `Ejemplo` es opcional, pero muy recomendable.

## 3. Dónde va la cabecera

| Lenguaje | Ubicación |
| --- | --- |
| Python | Docstring del módulo, como primera sentencia después del shebang y del encoding. |
| PowerShell | Primer bloque de comentario `<# ... #>` al inicio del archivo. |
| Bash | Bloque delimitado por dos líneas `# ============================================================`. |

Para Python, el indexador usa `ast.get_docstring()`. Si el texto no es el docstring real del módulo, no se detectará.

## 4. Plantillas

### Python

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Título descriptivo del script

Versión: 1.0.0

Descripción:
Una línea de máximo 200 caracteres explicando qué hace el script.

Dependencias:
- os
- argparse

Uso:
python script.py <argumento>

Ejemplo:
python script.py /ruta/de/ejemplo
"""
```

### PowerShell

```powershell
<#
Título descriptivo del script

Versión: 1.0.0

Descripción:
Una línea de máximo 200 caracteres explicando qué hace el script.

Dependencias:
- Docker Compose
- 7-Zip

Uso:
.\script.ps1 [-parametro <valor>]

Ejemplo:
.\script.ps1 -parametro C:\ruta
#>
```

### Bash

```bash
#!/usr/bin/env bash
# ============================================================
# Título descriptivo del script
#
# Versión: 1.0.0
#
# Descripción:
#   Una línea de máximo 200 caracteres explicando qué hace el script.
#
# Dependencias:
#   - tar
#   - gzip
#
# Uso:
#   ./script.sh <argumento>
#
# Ejemplo:
#   ./script.sh /ruta/de/ejemplo
# ============================================================
```

## 5. Cómo lo procesa `generar_readme_automatico.py`

Versión actual del generador: `1.0.3`.

1. Busca un `{nombre_script}_README.md` o `{nombre_script}_readme.md`.
2. Si existe, lo usa como fuente de la entrada del índice.
3. Si no existe, extrae la cabecera del propio script.
4. Extrae versión, descripción, dependencias, uso, ejemplo y requisitos.
5. La descripción se recorta a 200 caracteres.
6. Marca con `⚠️` los scripts sin `Descripción` o sin `Versión`.
7. Excluye al propio generador del índice.

> Importante: mientras un `*_README.md` exista, manda sobre la cabecera del script. Si creas uno, mantén las mismas secciones o elimínalo para que la cabecera sea la fuente de verdad. En la Fase 2 se prevé invertir esta prioridad.

## 6. Checklist para un script nuevo

- [ ] El nombre del archivo es descriptivo y no empieza por `x-`.
- [ ] La cabecera está en la ubicación correcta según el lenguaje.
- [ ] Incluye `Versión: X.Y.Z`.
- [ ] Incluye `Descripción:` con una línea de menos de 200 caracteres.
- [ ] `Dependencias:` distingue módulos estándar de dependencias externas.
- [ ] Incluye `Uso:` si acepta parámetros.
- [ ] Incluye `Ejemplo:` con un caso real.
- [ ] No hay markdown dentro de la cabecera.
- [ ] El nombre del script en `Uso` es el nombre actual del archivo.
- [ ] Se ejecutó `python3 generar_readme_automatico.py` y el script aparece como `✅`.
- [ ] Si existe un `*_README.md`, está sincronizado con la cabecera.

## 7. Errores comunes

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| `Sin descripción` | Falta la etiqueta `Descripción:` o no está al inicio de línea. | Añadir la sección con el contenido en la línea siguiente. |
| `Versión no especificada` | La versión solo está en una constante o en prosa. | Añadir `Versión: X.Y.Z` en la cabecera. |
| La cabecera no se detecta en Python | El texto no es el docstring real del módulo. | Moverlo a la primera sentencia del archivo. |
| La cabecera no se detecta en Bash | Faltan las líneas separadoras `# ====`. | Delimitar el bloque con dos separadores. |
| La cabecera no se detecta en PowerShell | Falta el bloque `<# ... #>`. | Envolver la cabecera en ese bloque. |
| El índice muestra texto antiguo | Existe un `*_README.md` con prioridad. | Actualizarlo o eliminarlo. |
| El comando de uso no coincide | Se renombró el script y no la cabecera. | Actualizar `Uso:` y `Ejemplo:`. |

## 8. Versionado

- Usa versionado semántico `X.Y.Z`.
- Sube `Z` para correcciones compatibles.
- Sube `Y` para funcionalidad nueva compatible.
- Sube `X` para cambios incompatibles.
- Actualiza la versión de la cabecera en el mismo cambio que modifica el comportamiento del script.

## 9. Validación

Antes de dar por terminado un script:

```bash
python3 generar_readme_automatico.py
```

Revisa el reporte final:

- `PROCESADOS`: scripts indexados correctamente.
- `INCOMPLETOS`: deben corregirse antes de hacer commit.
- `ERRORES`: revisar la excepción indicada.

El README se regenera automáticamente; no lo edites a mano.
