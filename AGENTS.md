# AGENTS.md

Guía para agentes y colaboradores que mantengan este repositorio de scripts de automatización.

## 1. Propósito

Biblioteca personal de scripts reutilizables (Python, PowerShell y Bash). El objetivo es que cada script esté **documentado, indexado y sea fácil de localizar**. `README.md` es la puerta de entrada y se genera automáticamente; la documentación extensa vive en `docs/`.

## 2. Estructura

```text
.
├── AGENTS.md              # este archivo
├── README.md              # GENERADO: no editar a mano
├── generar_readme_automatico.py      # indexador que genera README.md
├── <script>.py            # scripts ejecutables en la raíz
├── <script>.ps1
├── <script>.sh
├── docs/                  # TODA la documentación del proyecto
│   ├── GUIA Cabeceras Scripts.md
│   ├── PROMPT - Generar Cabecera Scripts.md
│   └── SPEC - Estado Proyecto.md
├── .gitignore
└── LICENSE
```

Reglas de ubicación:

- **Los scripts van en la raíz.** El indexador solo recorre la raíz, no `docs/` ni subcarpetas.
- **Toda la documentación va en `docs/`**, incluida la nueva. No crear `.md` de documentación en la raíz salvo `README.md` (generado) y este `AGENTS.md`.
- No versionar `__pycache__/`, entornos virtuales ni salidas generadas (`.png`, `.zip`, `.md` temporales).

## 3. Comandos de trabajo

```bash
# Comprobar sintaxis de todos los scripts Python
python3 -m py_compile *.py

# Regenerar el índice del README (obligatorio tras cambiar cabeceras o renombrar)
python3 generar_readme_automatico.py

# Si se toca index.php
php -l index.php
```

No hay framework de tests ni `requirements.txt`. Las dependencias externas conocidas son `pathspec` (`versionar_carpeta_ignore.py`) y `Pillow` (`generar_cartografia*.py`).

## 4. Convención de nombres

- **Python:** `snake_case` descriptivo. Ej.: `generar_cartografia.py`, `backup_carpeta_zip.py`.
- Sin prefijos raros (`x-`, `0`, `X`) ni números de versión en el nombre (la versión va en la cabecera).
- El nombre debe explicar qué hace el script.
- Al renombrar, usar `git mv` para conservar historial y actualizar todas las referencias en el mismo cambio: cabecera (`Uso:`, `Ejemplo:`), `README.md` (regenerándolo) y cualquier `docs/`.
- Si existe un `<nombre>_README.md`, renombrarlo junto al script o eliminarlo.

## 5. Cabecera obligatoria de cada script

Formato canónico (detalle en `docs/GUIA Cabeceras Scripts.md`):

```text
Título descriptivo del script

Versión: X.Y.Z

Descripción:
Una línea de máximo 200 caracteres explicando qué hace el script.

Dependencias:
- os
- argparse

Uso:
comando de ejemplo

Ejemplo:
comando concreto
```

- `Versión:` y `Descripción:` son **obligatorias**. Sin ellas el script sale como `⚠️` en el README.
- `Dependencias:`, `Uso:` y `Ejemplo:` son opcionales pero recomendadas.
- Usa **exactamente** esas etiquetas, en ese orden, sin markdown ni emojis dentro de la cabecera.
- Versión semántica `X.Y.Z`. Sube la versión en el mismo cambio que altere el comportamiento.
- Ubicación por lenguaje:
  - **Python:** docstring del módulo, primera sentencia tras shebang/encoding.
  - **PowerShell:** primer bloque `<# ... #>`.
  - **Bash:** bloque entre dos líneas `# ====`.

Ejemplo Python:

```python
#!/usr/bin/env python3
"""
Título descriptivo del script

Versión: 1.0.0

Descripción:
Qué hace el script en una línea.

Dependencias:
- os
- argparse

Uso:
python script.py <ruta>

Ejemplo:
python script.py /ruta/de/ejemplo
"""
```

## 6. README generado

`README.md` se escribe con `python3 generar_readme_automatico.py`. **No editarlo a mano**: cualquier cambio manual se pierde.

Comportamiento del indexador (`generar_readme_automatico.py`):

1. Recorre **solo la raíz** y procesa `.py`, `.sh` y `.ps1`.
2. Se excluye a sí mismo.
3. Da prioridad a `<nombre>_README.md` / `<nombre>_readme.md` sobre la cabecera del script (legado).
4. Extrae `Versión`, `Descripción`, `Dependencias`, `Uso`, `Ejemplo` y `Requisitos`.
5. Marca `⚠️` si falta `Descripción` o `Versión`; imprime un reporte con `PROCESADOS`, `INCOMPLETOS` y `ERRORES`.
6. Recorta la descripción a 200 caracteres.

Si añades o renombras documentación, actualiza los enlaces del bloque `README_HEADER` en `generar_readme_automatico.py` y regenera.

## 7. Documentación en `docs/`

- Un tema por archivo, título claro y contenido accionable.
- Al cerrar una fase de trabajo, añade una entrada fechada en `docs/SPEC - Estado Proyecto.md`.
- Los enlaces desde `README.md` deben apuntar a `docs/<archivo>` con la ruta correcta.
- Mantén `docs/GUIA Cabeceras Scripts.md` y `docs/PROMPT - Generar Cabecera Scripts.md` sincronizados con el comportamiento real de `generar_readme_automatico.py`.

## 8. Buenas prácticas de los scripts

- Evita rutas absolutas hardcodeadas (`/home/...`, `/discosecundario/...`, `C:\...`): usa argumentos o constantes fáciles de configurar.
- No incluyas secretos. `.gitignore` ya excluye `_KEYS.md`.
- Maneja errores con mensajes claros y códigos de salida no nulos.
- No añadas dependencias externas sin documentarlas en la cabecera.
- Comprime los backups salvo que el tamaño/velocidad exija lo contrario (`ZIP_STORED` no comprime).

## 9. Checklist antes de cerrar un cambio

- [ ] El script tiene cabecera con `Versión:` y `Descripción:`.
- [ ] El nombre está en `snake_case` y es descriptivo.
- [ ] Las referencias al nombre antiguo están actualizadas (cabecera, docs, `*_README.md`).
- [ ] `python3 -m py_compile *.py` pasa sin errores.
- [ ] `python3 generar_readme_automatico.py` no reporta `INCOMPLETOS` ni `ERRORES` (o se justifica).
- [ ] `README.md` refleja el script con `✅`.
- [ ] No se añaden `__pycache__`, temporales ni secretos al commit.
- [ ] Los cambios de documentación están en `docs/`.
