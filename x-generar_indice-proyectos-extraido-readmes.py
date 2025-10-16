import os
import re

REPO_DIR = '.'
OUTPUT_README = 'README.md'
SCRIPT_EXTENSIONS = ('.py', '.sh', '.ps1')
ARCHIVOS_EXCLUIDOS = {'x-generar_indice-proyectos-extraido-readmes.py'}

# 🏷️ Encabezado personalizado con badges o intro
README_HEADER = """\
# ⚙️ Colección Personal de Scripts de Automatización 🚀

> Repositorio centralizado para **optimizar tareas y flujos de trabajo diarios**. Contiene scripts desarrollados en **Python**, **Bash** y **PowerShell** para la gestión de sistemas, administración de datos y automatización general.

## ⚡ Estado del Repositorio y Tecnologías
[![Status](https://img.shields.io/badge/Status-Activo-green)]()
[![Python](https://img.shields.io/badge/Scripts-Python-blue?logo=python&logoColor=white)](./python)
[![Bash](https://img.shields.io/badge/Scripts-Bash-lightgrey?logo=gnu-bash&logoColor=white)](./bash)
[![PowerShell](https://img.shields.io/badge/Scripts-PowerShell-5391FE?logo=powershell&logoColor=white)](./powershell)

## 🎯 Enfoque Principal

El objetivo es mantener una biblioteca de scripts **reutilizables** y **bien documentados** para reducir la fricción en las tareas rutinarias y servir como recurso de referencia rápida.

***
"""

# Detecta bloques de cabecera en Python ("""...""") y PowerShell (<#...#>)
HEADER_PATTERN = re.compile(r'("""[\s\S]*?""")|(<#([\s\S]*?)#>)', re.MULTILINE)
NAME_VERSION_PATTERN = re.compile(r'([^\s]+?\.(?:py|ps1|sh))\s+V(\d+\.\d+)', re.IGNORECASE)
DESCRIPCION_PATTERN = re.compile(r'Descripción:\s*(.+?)(?:\n\s*\n|\nFuncionalidad:)', re.DOTALL | re.IGNORECASE)
USO_PATTERN = re.compile(r'Uso:\s*(.+?)(?:\n\s*\n|\nEjemplo:)', re.DOTALL | re.IGNORECASE)
EJEMPLO_PATTERN = re.compile(r'Ejemplo:\s*(.+?)(?:\n\s*\n|$)', re.DOTALL | re.IGNORECASE)

def extraer_info_script(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()

    bloque = HEADER_PATTERN.search(contenido)
    texto = bloque.group(0) if bloque else ''

    nombre_version = NAME_VERSION_PATTERN.search(texto)
    descripcion = DESCRIPCION_PATTERN.search(texto)
    uso = USO_PATTERN.search(texto)
    ejemplo = EJEMPLO_PATTERN.search(texto)

    return {
        'archivo': os.path.basename(ruta),
        'nombre': nombre_version.group(1).strip() if nombre_version else 'Sin nombre',
        'version': nombre_version.group(2).strip() if nombre_version else 'Sin versión',
        'descripcion': re.sub(r'\s+', ' ', descripcion.group(1).strip()) if descripcion else 'Sin descripción',
        'uso': uso.group(1).strip().replace('\n', ' ') if uso else 'Sin uso',
        'ejemplo': ejemplo.group(1).strip().replace('\n', ' ') if ejemplo else 'Sin ejemplo'
    }

def generar_indice_scripts():
    contenido = README_HEADER + "\n\n## Índice de scripts\n\n"

    for archivo in os.listdir(REPO_DIR):
        if (
            archivo.endswith(SCRIPT_EXTENSIONS)
            and archivo not in ARCHIVOS_EXCLUIDOS
        ):
            info = extraer_info_script(os.path.join(REPO_DIR, archivo))
            contenido += f"### {info['nombre']} (v{info['version']})\n"
            contenido += f"- **Archivo:** `{info['archivo']}`\n"
            contenido += f"- **Descripción:** {info['descripcion']}\n"
            contenido += f"- **Uso:** `{info['uso']}`\n"
            contenido += f"- **Ejemplo:** `{info['ejemplo']}`\n"
            contenido += f"\n---\n\n"

    with open(os.path.join(REPO_DIR, OUTPUT_README), 'w', encoding='utf-8') as f:
        f.write(contenido)

if __name__ == '__main__':
    generar_indice_scripts()
    print(f'Índice generado en {OUTPUT_README}')
