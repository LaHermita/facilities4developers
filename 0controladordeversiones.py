#!/usr/bin/env python3
"""
0controladordeversiones.py V1.0

Script para observar una carpeta y renombrar automáticamente archivos copiados
que contienen " copy" en su nombre. Genera versiones numeradas del tipo _v001, _v002, etc.

Funcionalidad:
- Detecta archivos nuevos con " copy" en el nombre.
- Ignora extensiones definidas por el usuario.
- Renombra el archivo como una nueva versión del original (_vXXX).
- Elimina el archivo original al renombrarlo (mediante os.rename).
- Permite pasar la ruta a observar como argumento. Si no se pasa, usa la carpeta actual.
- Se puede cerrar de forma segura con Ctrl+C.

Uso:
    python 0controladordeversiones.py [ruta/opcional]

Ejemplo:
    python 0controladordeversiones.py /mi/proyecto
"""

import os
import time
import re
import sys

# Intervalo de escaneo en segundos
SCAN_INTERVAL = 2

# Lista de extensiones a ignorar (en minúsculas)
EXTENSIONES_IGNORADAS = ['.txt', '.md', '.log']


def watch_folder(folder_path: str) -> None:
    """
    Observa una carpeta y renombra archivos que contengan " copy" en su nombre,
    generando versiones numeradas (_v001, _v002, etc.).

    Args:
        folder_path (str): Ruta absoluta de la carpeta a observar.
    """
    print(f"👀 Vigilando la carpeta: {folder_path}")
    seen_files = set(os.listdir(folder_path))

    try:
        while True:
            current_files = set(os.listdir(folder_path))
            new_files = current_files - seen_files

            for filename in new_files:
                full_path = os.path.join(folder_path, filename)

                # Ignorar subdirectorios
                if not os.path.isfile(full_path):
                    continue

                if " copy" in filename:
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in EXTENSIONES_IGNORADAS:
                        print(f"⏭️ Ignorado por extensión: {filename}")
                        continue

                    new_filename = generate_versioned_name(filename, current_files)
                    new_path = os.path.join(folder_path, new_filename)

                    try:
                        os.rename(full_path, new_path)
                        print(f"✅ Renombrado: {filename} → {new_filename}")
                    except Exception as e:
                        print(f"⚠️ Error al renombrar {filename}: {e}")

            seen_files = current_files
            time.sleep(SCAN_INTERVAL)

    except KeyboardInterrupt:
        print("\n👋 Script detenido por el usuario. ¡Hasta la próxima!")


def generate_versioned_name(copy_filename: str, all_files: set) -> str:
    """
    Genera un nuevo nombre de archivo con versión (_vXXX) basado en los existentes.

    Args:
        copy_filename (str): Nombre del archivo con " copy".
        all_files (set): Conjunto de nombres de archivos actuales en la carpeta.

    Returns:
        str: Nuevo nombre con versión (_v001, _v002, etc.).
    """
    name, ext = os.path.splitext(copy_filename)
    base_name = name.replace(" copy", "")

    version_pattern = re.compile(rf"^{re.escape(base_name)}_v(\d{{3}}){re.escape(ext)}$")
    existing_versions = [
        int(match.group(1))
        for f in all_files
        if (match := version_pattern.match(f))
    ]

    next_version = max(existing_versions, default=0) + 1
    version_str = f"{next_version:03d}"

    return f"{base_name}_v{version_str}{ext}"


if __name__ == "__main__":
    # Obtener ruta desde argumento o usar carpeta actual
    folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    if not os.path.isdir(folder):
        print(f"❌ La ruta no es válida: {folder}")
        sys.exit(1)

    watch_folder(folder)
