#!/usr/bin/env python3
"""
Controlador de versiones automático para subcarpetas copiadas

Versión: 2.1

Descripción:
Observa una carpeta y renombra automáticamente subcarpetas cuyo nombre contenga un patrón configurable (por defecto "(copia)"), generando versiones numeradas secuenciales (_cv001, _cv002, ...).

Dependencias:
- os
- time
- re
- sys

Uso:
python controladorversionescarpetas.py [ruta_a_observar]

Ejemplo:
python controladorversionescarpetas.py /home/usuario/miscarpetas
"""

import os
import time
import re
import sys

# Intervalo de escaneo en segundos
SCAN_INTERVAL = 2

# Texto que identifica una carpeta duplicada
# Ejemplos:
#   Windows/macOS: " copy"
#   Linux (Nautilus): "(copia)"
PATRON_COPIA = "(copia)"


def watch_folder(folder_path: str) -> None:
    print(f"👀 Vigilando la carpeta (solo carpetas): {folder_path}")
    print(f"🔎 Patrón de copia configurado: '{PATRON_COPIA}'")
    seen_items = set(os.listdir(folder_path))

    try:
        while True:
            current_items = set(os.listdir(folder_path))
            new_items = current_items - seen_items

            for item in new_items:
                full_path = os.path.join(folder_path, item)

                # Solo actuar sobre carpetas nuevas
                if not os.path.isdir(full_path):
                    continue

                if PATRON_COPIA in item:
                    new_name = generate_versioned_folder_name(item, current_items)
                    new_path = os.path.join(folder_path, new_name)

                    try:
                        os.rename(full_path, new_path)
                        print(f"📁 Renombrado: {item} → {new_name}")
                    except Exception as e:
                        print(f"⚠️ Error al renombrar {item}: {e}")

            seen_items = current_items
            time.sleep(SCAN_INTERVAL)

    except KeyboardInterrupt:
        print("\n👋 Script detenido por el usuario. ¡Hasta la próxima!")


def generate_versioned_folder_name(copy_folder: str, all_items: set) -> str:
    """
    Genera un nuevo nombre de carpeta con versión (_cvXXX) basado en los existentes.
    """
    # Eliminar el patrón de copia del nombre base
    base_name = copy_folder.replace(PATRON_COPIA, "").strip()

    version_pattern = re.compile(rf"^{re.escape(base_name)}_cv(\d{{3}})$")
    existing_versions = [
        int(match.group(1))
        for f in all_items
        if (match := version_pattern.match(f))
    ]

    next_version = max(existing_versions, default=0) + 1
    version_str = f"{next_version:03d}"

    return f"{base_name}_cv{version_str}"


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    if not os.path.isdir(folder):
        print(f"❌ La ruta no es válida: {folder}")
        sys.exit(1)

    watch_folder(folder)
