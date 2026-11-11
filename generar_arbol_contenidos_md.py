# -*- coding: utf-8 -*-
"""
Generador de árbol de contenidos en Markdown

Versión: 1.4.2

Descripción:
Recorre una carpeta recursivamente, ignora elementos ocultos y genera un Markdown con el árbol de contenidos y el listado de archivos .md.

Dependencias:
- argparse
- datetime
- pathlib

Uso:
python3 generar_arbol_contenidos_md.py [RUTA]

Ejemplo:
python3 generar_arbol_contenidos_md.py Embarcadero
"""

import argparse
from datetime import datetime
from pathlib import Path


def generar_chuleta_carpetas(ruta_directorio, mostrar_contador=False):
  """Recorre recursivamente una carpeta (excluyendo archivos y carpetas ocultas),

  cuenta archivos directos, lista los archivos .md y guarda un archivo Markdown
  con YAML front matter añadiendo el nombre de la carpeta como sufijo del
  archivo de salida.
  """
  directorio_base = Path(ruta_directorio).resolve()

  if not directorio_base.exists() or not directorio_base.is_dir():
    print(f"Error: La ruta '{ruta_directorio}' no es un directorio válido.")
    return

  # Generamos el nombre del archivo de salida dinámicamente usando el nombre de la carpeta
  nombre_carpeta = directorio_base.name
  if not nombre_carpeta or nombre_carpeta in (".", "/"):
    nombre_carpeta = "raiz"

  nombre_archivo_salida = (
      f"ZTEMP - Arbol Contenidos - Vivero {nombre_carpeta}.md"
  )

  lineas_markdown = []

  def contar_markdown(directorio):
    """Cuenta los archivos .md visibles de forma recursiva."""
    total = 0
    for archivo in directorio.rglob("*"):
      ruta_relativa = archivo.relative_to(directorio)
      if any(parte.startswith(".") for parte in ruta_relativa.parts):
        continue
      if (
          archivo.is_file()
          and archivo.suffix.lower() == ".md"
          and archivo.name != nombre_archivo_salida
      ):
        total += 1
    return total

  # Cabecera YAML con metadatos y la fecha actual
  fecha_actual = datetime.now().strftime("%Y-%m-%d")
  lineas_markdown.append("---")
  lineas_markdown.append(f"fecha: {fecha_actual}")
  lineas_markdown.append(f'directorio_base: "{directorio_base}"')
  lineas_markdown.append('version: "1.4.0"')
  lineas_markdown.append("---\n")

  # Título principal del documento Markdown
  lineas_markdown.append(
      f"# Checklist de Contenidos: {directorio_base.name}\n"
  )
  lineas_markdown.append(f"Ruta base: `{directorio_base}`\n")

  if mostrar_contador:
    total_markdown = contar_markdown(directorio_base)
    lineas_markdown.append(
        f"Total archivos Markdown: **{total_markdown}**\n"
    )

  lineas_markdown.append("---\n")

  def archivos_md_directos(directorio):
    """Devuelve los archivos .md directos visibles de un directorio."""
    return sorted(
        archivo
        for archivo in directorio.iterdir()
        if archivo.is_file()
        and archivo.suffix.lower() == ".md"
        and not archivo.name.startswith(".")
        and archivo.name != nombre_archivo_salida
    )

  # Archivos .md que están directamente en la carpeta analizada (nivel raíz)
  for archivo in archivos_md_directos(directorio_base):
    lineas_markdown.append(f"- [ ] `{archivo.name}`")

  # Recorremos de manera recursiva la estructura de directorios
  for ruta_actual in sorted(directorio_base.rglob("*")):
    # Calculamos la ruta relativa respecto al directorio base
    ruta_relativa = ruta_actual.relative_to(directorio_base)

    # Exclusión: Si cualquier parte de la ruta empieza por '.', se ignora (ej. .git, .DS_Store)
    if any(parte.startswith(".") for parte in ruta_relativa.parts):
      continue

    if ruta_actual.is_dir():
      # Contamos únicamente los archivos directos dentro de esta subcarpeta
      num_archivos = sum(
          1 for archivo in ruta_actual.iterdir() if archivo.is_file()
      )

      # Calculamos la profundidad para anidar correctamente con sangría en Markdown
      profundidad = len(ruta_relativa.parts)
      sangria = "    " * (profundidad - 1)

      # Formato de checklist Markdown (- [ ] )
      lineas_markdown.append(
          f"{sangria}- [ ] `{ruta_relativa.name}` **({num_archivos} archivos)**"
      )

      # Listamos los archivos .md directos de esta subcarpeta
      sangria_hijos = "    " * profundidad
      for archivo in archivos_md_directos(ruta_actual):
        lineas_markdown.append(f"{sangria_hijos}- [ ] `{archivo.name}`")

  # Unimos todo el contenido y lo guardamos directamente en el archivo
  contenido_final = "\n".join(lineas_markdown)
  archivo_salida = Path(nombre_archivo_salida)
  archivo_salida.write_text(contenido_final, encoding="utf-8")

  print(f"¡Chuleta generada con éxito en '{archivo_salida.resolve()}'!")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description=(
          "Genera una chuleta Markdown con el árbol de contenidos de una "
          "subcarpeta."
      )
  )
  parser.add_argument(
      "ruta",
      nargs="?",
      default=None,
      help="Subcarpeta a escanear (por defecto: el directorio actual).",
  )
  args = parser.parse_args()
  ruta = args.ruta if args.ruta is not None else "."
  generar_chuleta_carpetas(ruta, mostrar_contador=args.ruta is not None)
