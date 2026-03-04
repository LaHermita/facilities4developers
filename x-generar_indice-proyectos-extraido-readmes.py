import os
import re
from typing import Dict, List, Optional

REPO_DIR = '.'
OUTPUT_README = 'README.md'
SCRIPT_EXTENSIONS = ('.py', '.sh', '.ps1')
ARCHIVOS_EXCLUIDOS = {'x-generar_indice-proyectos-extraido-readmes.py'}

# 📊 Sistema de logging y validación
class ReporteValidacion:
    def __init__(self):
        self.procesados = []
        self.incompletos = []
        self.errores = []
    
    def agregar_procesado(self, nombre, estado='✅'):
        self.procesados.append((nombre, estado))
    
    def agregar_incompleto(self, nombre, razon):
        self.incompletos.append((nombre, razon))
    
    def agregar_error(self, nombre, excepcion):
        self.errores.append((nombre, str(excepcion)))
    
    def mostrar_resumen(self):
        print("\n" + "="*70)
        print("📊 REPORTE DE PROCESAMIENTO")
        print("="*70)
        print(f"\n✅ PROCESADOS: {len(self.procesados)}")
        for nombre, estado in self.procesados:
            print(f"   {estado} {nombre}")
        
        if self.incompletos:
            print(f"\n⚠️  INCOMPLETOS: {len(self.incompletos)}")
            for nombre, razon in self.incompletos:
                print(f"   ⚠️  {nombre}: {razon}")
        
        if self.errores:
            print(f"\n❌ ERRORES: {len(self.errores)}")
            for nombre, exc in self.errores:
                print(f"   ❌ {nombre}: {exc}")
        
        print("\n" + "="*70 + "\n")


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

# Regex para extraer información
NAME_VERSION_PATTERN = re.compile(r'V(?:ersión:?)?\s*(\d+\.\d+(?:\.\d+)?)', re.IGNORECASE)
DESCRIPCION_PATTERN = re.compile(r'(?:##?.*Descripción[:\s]*|Descripción[:\s]*)\n(.*?)(?=\n\s*##?[^#]|\nFuncionalidad|\nUso|\nEjecución|\nEjemplo|\nDependencias|\nRequisitos|$)', re.DOTALL | re.IGNORECASE)
USO_PATTERN = re.compile(r'(?:##?.*(?:Uso|Ejecución)[:\s]*|(?:Uso|Ejecución)[:\s]*)\n(.*?)(?=\n\s*##?[^#]|\nEjemplo|\nDependencias|\nRequisitos|$)', re.DOTALL | re.IGNORECASE)
EJEMPLO_PATTERN = re.compile(r'(?:##?.*Ejemplo[:\s]*|Ejemplo[:\s]*)\n(.*?)(?=\n\s*##?[^#]|\nDependencias|\nRequisitos|$)', re.DOTALL | re.IGNORECASE)
DEPENDENCIAS_PATTERN = re.compile(r'(?:##?.*Dependencias?[:\s]*|Dependencias?[:\s]*)\n(.*?)(?=\n\s*##?[^#]|\nRequisitos|$)', re.DOTALL | re.IGNORECASE)
REQUISITOS_PATTERN = re.compile(r'(?:##?.*Requisitos?[:\s]*|Requisitos?[:\s]*)\n(.*?)(?=\n\s*##?[^#]|$)', re.DOTALL | re.IGNORECASE)


def truncar_inteligente(texto: Optional[str], max_chars: int = 200) -> str:
    """Trunca texto respetando límites de palabras completas"""
    if not texto or len(texto) <= max_chars:
        return texto or ''
    
    # Truncar al último espacio completo
    truncado = texto[:max_chars].rsplit(' ', 1)[0]
    return truncado + "..." if truncado else texto[:max_chars-3] + "..."

def limpiar_texto(match) -> Optional[str]:
    """Limpia y normaliza texto extraído"""
    if not match:
        return None
    
    text = match.group(1).strip()
    
    # Si es un bloque de "citado" (> bash ... < o similar) usado en tus readmes
    text = re.sub(r'^>\s*\w*\s*\n|<\s*$', '', text, flags=re.MULTILINE)
    
    # Eliminar bloques de código markdown
    text = re.sub(r'```\w*\n|```', '', text)
    
    # Eliminar sub-cabeceras de markdown
    text = re.sub(r'^#+.*$', '', text, flags=re.MULTILINE)
    
    # Colapsar espacios y saltos de línea múltiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Truncar inteligentemente
    text = truncar_inteligente(text, 200)
    
    return text if text else None

def validar_readme(info: Dict) -> List[str]:
    """Valida que el README tenga todas las secciones y retorna lista de problemas"""
    problemas = []
    
    if info['descripcion'] == 'Sin descripción':
        problemas.append('Falta sección Descripción')
    if info['uso'] == 'Sin uso':
        problemas.append('Falta sección Uso/Ejecución')
    if info['ejemplo'] == 'Sin ejemplo':
        problemas.append('Falta sección Ejemplo')
    if info['version'] == '1.0':
        problemas.append('Versión no especificada (usa por defecto 1.0)')
    
    return problemas

def extraer_info_script(ruta_script: str) -> Dict:
    """Extrae información del script de su README o docstring"""
    base_name = os.path.splitext(os.path.basename(ruta_script))[0]
    posibles_readmes = [
        f"{base_name}_README.md",
        f"{base_name}_readme.md",
    ]
    
    contenido = ""
    readme_encontrado = False
    
    try:
        # Intentar leer desde un README externo primero
        for r_name in posibles_readmes:
            r_path = os.path.join(os.path.dirname(ruta_script), r_name)
            if os.path.exists(r_path) and r_path != os.path.join(REPO_DIR, OUTPUT_README):
                try:
                    with open(r_path, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                    readme_encontrado = True
                    break
                except Exception as e:
                    raise Exception(f"Error al leer README: {str(e)}")
        
        # Si no hay README externo, leer el bloque de cabecera del script
        if not contenido:
            with open(ruta_script, 'r', encoding='utf-8') as f:
                script_raw = f.read()
                bloque = HEADER_PATTERN.search(script_raw)
                contenido = bloque.group(0) if bloque else ''
        
        # Extracción de campos
        version = NAME_VERSION_PATTERN.search(contenido)
        descripcion = DESCRIPCION_PATTERN.search(contenido)
        uso = USO_PATTERN.search(contenido)
        ejemplo = EJEMPLO_PATTERN.search(contenido)
        dependencias = DEPENDENCIAS_PATTERN.search(contenido)
        requisitos = REQUISITOS_PATTERN.search(contenido)
        
        # Limpieza
        desc_limpia = limpiar_texto(descripcion) or 'Sin descripción'
        uso_limpia = limpiar_texto(uso) or 'Sin uso'
        ejemplo_limpia = limpiar_texto(ejemplo) or 'Sin ejemplo'
        dep_limpia = limpiar_texto(dependencias) or None
        req_limpia = limpiar_texto(requisitos) or None
        
        info = {
            'archivo': os.path.basename(ruta_script),
            'nombre': base_name,
            'version': version.group(1).strip() if version else '1.0',
            'descripcion': desc_limpia,
            'uso': uso_limpia,
            'ejemplo': ejemplo_limpia,
            'dependencias': dep_limpia,
            'requisitos': req_limpia,
            'readme_encontrado': readme_encontrado
        }
        
        return info
        
    except Exception as e:
        raise Exception(f"Error al procesar {base_name}: {str(e)}")

def generar_indice_scripts():
    """Genera el índice de scripts en el README principal"""
    contenido = README_HEADER + "\n\n## Índice de scripts\n\n"
    reporte = ReporteValidacion()
    
    # Obtener lista de archivos y ordenarlos
    archivos = sorted(os.listdir(REPO_DIR))

    for archivo in archivos:
        if (
            archivo.endswith(SCRIPT_EXTENSIONS)
            and archivo not in ARCHIVOS_EXCLUIDOS
        ):
            try:
                info = extraer_info_script(os.path.join(REPO_DIR, archivo))
                
                # Validar
                problemas = validar_readme(info)
                
                # Marcar estado
                if problemas:
                    estado = '⚠️ '
                    reporte.agregar_incompleto(info['nombre'], ', '.join(problemas))
                else:
                    estado = '✅'
                    reporte.agregar_procesado(info['nombre'], estado)
                
                # Construir entrada del índice
                contenido += f"### {estado} {info['nombre']} (v{info['version']})\n"
                contenido += f"- **Archivo:** `{info['archivo']}`\n"
                contenido += f"- **Descripción:** {info['descripcion']}\n"
                contenido += f"- **Uso:** `{info['uso']}`\n"
                
                # Incluir Dependencias y Requisitos si existen
                if info['dependencias']:
                    contenido += f"- **Dependencias:** `{info['dependencias']}`\n"
                if info['requisitos']:
                    contenido += f"- **Requisitos:** `{info['requisitos']}`\n"
                
                contenido += f"- **Ejemplo:** `{info['ejemplo']}`\n"
                contenido += f"\n---\n\n"
                
            except Exception as e:
                reporte.agregar_error(archivo, e)

    with open(os.path.join(REPO_DIR, OUTPUT_README), 'w', encoding='utf-8') as f:
        f.write(contenido)

    reporte.mostrar_resumen()


if __name__ == '__main__':
    print("🔄 Generando índice de scripts...\n")
    generar_indice_scripts()
    print(f'✅ Índice generado en {OUTPUT_README}')
