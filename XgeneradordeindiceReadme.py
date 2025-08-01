import os
import re

# Carpeta base del repositorio
REPO_DIR = '.'
OUTPUT_README = 'README.md'

# Expresiones regulares para capturar info clave
TITLE_PATTERN = re.compile(r'#\s+(.*)')
VERSION_PATTERN = re.compile(r'\*\*Versión:\*\*\s*(.+)')
MAIN_FILE_PATTERN = re.compile(r'\*\*Archivo\(s\) principal\(es\):\*\*\s*`(.+?)`')
DESCRIPTION_PATTERN = re.compile(r'## Descripción\s*\n+(.+?)\n(?:##|\Z)', re.DOTALL)

def extraer_info_md(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    nombre = TITLE_PATTERN.search(contenido)
    version = VERSION_PATTERN.search(contenido)
    archivo = MAIN_FILE_PATTERN.search(contenido)
    descripcion = DESCRIPTION_PATTERN.search(contenido)
    
    return {
        'nombre': nombre.group(1).strip() if nombre else 'Sin nombre',
        'version': version.group(1).strip() if version else 'Sin versión',
        'archivo': archivo.group(1).strip() if archivo else 'Sin archivo',
        'descripcion': descripcion.group(1).strip() if descripcion else 'Sin descripción'
    }

def generar_indice_md():
    indice = "# Índice de scripts Python\n\n"
    
    for archivo in os.listdir(REPO_DIR):
        if archivo.endswith('.md') and archivo != OUTPUT_README:
            info = extraer_info_md(os.path.join(REPO_DIR, archivo))
            indice += f"### {info['nombre']} (v{info['version']})\n"
            indice += f"- **Archivo principal:** `{info['archivo']}`\n"
            indice += f"- **Descripción:** {info['descripcion']}\n"
            indice += f"\n======== SEPARACION ========\n\n"
    
    with open(os.path.join(REPO_DIR, OUTPUT_README), 'w', encoding='utf-8') as f:
        f.write(indice)

if __name__ == '__main__':
    generar_indice_md()
    print(f'Índice generado en {OUTPUT_README}')
