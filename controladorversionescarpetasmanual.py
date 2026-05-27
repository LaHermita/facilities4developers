#!/usr/bin/env python3
"""
Versionador local de carpetas con soporte .gitignore

Versión: 1.1

Descripción:
Crea copias versionadas (snapshots) de carpetas de trabajo ignorando automáticamente archivos y directorios definidos en .gitignore.

Dependencias:
- pathspec (instalación externa)

Uso:
python controladorversionescarpetasmanual.py <carpeta>

Ejemplo:
python controladorversionescarpetasmanual.py MiProyecto
"""

import re
import shutil
import sys
from pathlib import Path

import pathspec


def generate_versioned_folder_name(
    base_name: str,
    parent_path: Path
) -> str:
    """
    Genera el siguiente nombre versionado disponible.

    Ejemplo:
        Proyecto_cv001
        Proyecto_cv002
    """

    version_pattern = re.compile(
        rf"^{re.escape(base_name)}_cv(\d{{3}})$"
    )

    existing_versions = []

    for item in parent_path.iterdir():

        if not item.is_dir():
            continue

        match = version_pattern.match(item.name)

        if match:
            existing_versions.append(
                int(match.group(1))
            )

    next_version = max(existing_versions, default=0) + 1

    return f"{base_name}_cv{next_version:03d}"


def load_gitignore(source_path: Path):
    """
    Carga las reglas definidas en .gitignore.

    Retorna:
        - PathSpec si existe .gitignore
        - None si no existe
    """

    gitignore_path = source_path / ".gitignore"

    if not gitignore_path.exists():
        return None

    with gitignore_path.open(
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    return pathspec.PathSpec.from_lines(
        "gitwildmatch",
        lines
    )


def should_ignore(
    spec,
    relative_path: str
) -> bool:
    """
    Determina si una ruta debe ignorarse
    según las reglas del .gitignore.
    """

    if spec is None:
        return False

    return spec.match_file(relative_path)


def copy_folder(
    source_path: Path,
    destination_path: Path,
    spec
) -> None:
    """
    Copia una carpeta ignorando
    patrones definidos en .gitignore.
    """

    def ignore_patterns(directory, contents):

        ignored = []

        for item in contents:

            full_path = Path(directory) / item

            relative_path = full_path.relative_to(
                source_path
            )

            if should_ignore(
                spec,
                str(relative_path)
            ):

                ignored.append(item)

                print(
                    f"🚫 Ignorando: {relative_path}"
                )

        return ignored

    shutil.copytree(
        source_path,
        destination_path,
        ignore=ignore_patterns
    )


def create_local_repository(folder: str) -> None:
    """
    Crea una nueva copia versionada
    de una carpeta local.
    """

    source_path = Path(folder).resolve()

    if not source_path.exists():

        print(
            f"❌ La carpeta no existe: {source_path}"
        )

        sys.exit(1)

    if not source_path.is_dir():

        print(
            f"❌ La ruta no es una carpeta: {source_path}"
        )

        sys.exit(1)

    parent_path = source_path.parent
    base_name = source_path.name

    new_folder_name = generate_versioned_folder_name(
        base_name,
        parent_path
    )

    destination_path = (
        parent_path / new_folder_name
    )

    print("")
    print("========================================")
    print("📦 CONTROLADOR DE VERSIONES MANUAL")
    print("========================================")
    print(f"📁 Origen : {source_path}")
    print(f"📁 Destino: {destination_path}")

    spec = load_gitignore(source_path)

    if spec:
        print("📜 Archivo .gitignore detectado")
    else:
        print("📜 No existe archivo .gitignore")

    print("")

    copy_folder(
        source_path,
        destination_path,
        spec
    )

    print("")
    print("✅ Copia creada correctamente")
    print(
        f"📁 Nueva versión: {new_folder_name}"
    )
    print("")


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("")
        print("Uso:")
        print("")
        print(
            "    python controladorversionescarpetasmanual.py <carpeta>"
        )
        print("")
        print("Ejemplo:")
        print("")
        print(
            "    python controladorversionescarpetasmanual.py MiProyecto"
        )
        print("")

        sys.exit(1)

    create_local_repository(sys.argv[1])