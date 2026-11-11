#!/usr/bin/env python3
"""
Backup de una carpeta en formato ZIP

Versión: 1.0.0

Descripción:
Crea una copia de seguridad ZIP de una carpeta, excluyendo archivos y directorios temporales o de desarrollo.

Dependencias:
- sys
- pathlib
- zipfile
- datetime
- fnmatch

Uso:
python backup_carpeta_zip.py <carpeta_origen> [carpeta_destino]

Ejemplo:
python backup_carpeta_zip.py /ruta/proyecto ./backups
"""

import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_STORED
from datetime import datetime
from fnmatch import fnmatch


# Carpetas y patrones a excluir
EXCLUIR_DIRS = {
    ".git",
    "__pycache__",
    ".idea",
    ".vscode"
}

EXCLUIR_FILES = {
    "*.log",
    "*.tmp",
    "*.bak"
}


def debe_excluir(ruta_relativa):
    """
    Determina si un fichero debe excluirse.
    """

    # Excluir si alguna carpeta padre coincide
    for parte in ruta_relativa.parts:
        if parte in EXCLUIR_DIRS:
            return True

    # Excluir por patrón de fichero
    nombre = ruta_relativa.name

    for patron in EXCLUIR_FILES:
        if fnmatch(nombre, patron):
            return True

    return False


def obtener_nombre_backup(carpeta, destino):
    fecha = datetime.now().strftime("%Y%m%d")

    base = f"{carpeta.name}_Backup_{fecha}"
    ruta_zip = destino / f"{base}.zip"

    contador = 1

    while ruta_zip.exists():
        ruta_zip = destino / f"{base}_{contador:03d}.zip"
        contador += 1

    return ruta_zip


def recopilar_ficheros(carpeta):
    archivos = []

    for fichero in carpeta.rglob("*"):
        if not fichero.is_file():
            continue

        relativa = fichero.relative_to(carpeta)

        if debe_excluir(relativa):
            continue

        archivos.append(fichero)

    return archivos


def crear_backup(carpeta_origen, carpeta_destino=None):

    carpeta = Path(carpeta_origen).resolve()

    if not carpeta.exists():
        raise FileNotFoundError(
            f"La carpeta no existe: {carpeta}"
        )

    if not carpeta.is_dir():
        raise NotADirectoryError(
            f"No es una carpeta válida: {carpeta}"
        )

    if carpeta_destino:
        destino = Path(carpeta_destino).resolve()
    else:
        destino = carpeta.parent

    destino.mkdir(parents=True, exist_ok=True)

    ruta_zip = obtener_nombre_backup(carpeta, destino)

    archivos = recopilar_ficheros(carpeta)

    total = len(archivos)

    print(f"Archivos a incluir: {total}")
    print(f"Backup destino: {ruta_zip}")
    print()

    with ZipFile(ruta_zip, "w", compression=ZIP_STORED) as zipf:

        for indice, fichero in enumerate(archivos, start=1):

            relativa = fichero.relative_to(carpeta)

            print(
                f"[{indice}/{total}] {relativa}",
                end="\r",
                flush=True
            )

            zipf.write(
                fichero,
                arcname=relativa
            )

    print()
    print(f"Backup creado correctamente:")
    print(ruta_zip)


def main():

    if len(sys.argv) < 2:
        print(
            f"Uso: {sys.argv[0]} <carpeta_origen> [carpeta_destino]"
        )
        sys.exit(1)

    carpeta_origen = sys.argv[1]

    carpeta_destino = None

    if len(sys.argv) >= 3:
        carpeta_destino = sys.argv[2]

    crear_backup(
        carpeta_origen,
        carpeta_destino
    )


if __name__ == "__main__":
    main()
