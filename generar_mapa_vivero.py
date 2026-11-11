#!/usr/bin/env python3
"""
Generador de mapas de proyectos

Versión: 1.19.1

Descripción:
Genera un archivo Markdown con el mapa de proyectos de un directorio a partir de los manifest.json de cada carpeta.

Dependencias:
- os
- sys
- json
- shutil
- argparse
- datetime
- pathlib
- typing

Uso:
python generar_mapa_vivero.py [directorio] [--output nombre_archivo.md] [--debug]

Ejemplo:
python generar_mapa_vivero.py . --output MI_MAPA.md --debug
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional


# --- CONFIGURACIÓN ---
VERSION_SISTEMA = "1.19.1"
DEBUG = False
NOMBRE_MAPA_DEFAULT = "MAP - Proyectos.md"

# Filtros
OMITIR_CARPETAS_CON_NUMEROS = True
OMITIR_CARPETAS_FECHA = True  # Formato _dd-mm-aa
OMITIR_CARPETAS_CV = True     # Terminan en _cvXXX

# Carpetas a ignorar siempre (por nombre exacto)
CARPETAS_IGNORAR = [
    "__pycache__",
]

# Iconos por stack
ICONOS_STACK = {
    'PHP': '📔',
    'HTML': '📗',
    'Python': '🐍',
    'JavaScript': '📙',
    'JS': '📙',
    'CSS': '📕',
    'SQL': '📓',
    'Shell': '💻',
    'Bash': '🖥️',
    'C': '🔧',
    'C++': '🔧',
    'Java': '☕',
    'Go': '🔷',
    'Rust': '🦀',
    'TypeScript': '🔷',
    'TS': '🔷',
    'Electron/Neutralino': '⚝',
}
ICONO_DEFAULT = '📄'


def log_debug(mensaje: str) -> None:
    """Imprime mensaje de depuración si DEBUG está activado."""
    if DEBUG:
        print(f"[MAP] {mensaje}")


def icono_stack(stack: Optional[str]) -> str:
    """Devuelve un icono según el stack del proyecto."""
    if not stack:
        return ICONO_DEFAULT
    return ICONOS_STACK.get(stack, ICONO_DEFAULT)


def leer_manifest_mapa(ruta_base: str) -> dict:
    """
    Lee manifest_mapa.json y devuelve la configuración del mapa.
    
    Args:
        ruta_base: Ruta al directorio donde buscar el manifest_mapa.json
        
    Returns:
        Diccionario con nombremapa, titulomapa, summarymapa y
        las rutas de replicación según el sistema.
    """
    archivo = os.path.join(ruta_base, 'manifest_mapa.json')
    defaults = {
        'nombremapa': 'MAP - Proyectos.md',
        'titulomapa': 'MAP - Proyectos',
        'summarymapa': 'Guía de navegación de proyectos.',
        'url_carpeta_vivero_lin': '',
        'url_carpeta_vivero_win': '',
    }
    
    if not os.path.exists(archivo):
        log_debug(f"manifest_mapa.json no encontrado, usando defaults")
        return defaults
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        log_debug(f"manifest_mapa.json leído correctamente")
        return {
            'nombremapa': datos.get('nombremapa', defaults['nombremapa']),
            'titulomapa': datos.get('titulomapa', defaults['titulomapa']),
            'summarymapa': datos.get('summarymapa', defaults['summarymapa']),
            'url_carpeta_vivero_lin': datos.get('url_carpeta_vivero_lin', defaults['url_carpeta_vivero_lin']),
            'url_carpeta_vivero_win': datos.get('url_carpeta_vivero_win', defaults['url_carpeta_vivero_win']),
        }
    except (json.JSONDecodeError, IOError) as e:
        log_debug(f"Error leyendo manifest_mapa.json: {e}")
        return defaults


def extraer_manifest(ruta_carpeta: str) -> Optional[dict]:
    """
    Extrae datos de un archivo manifest.json en una carpeta específica.
    
    Args:
        ruta_carpeta: Ruta completa a la carpeta del proyecto
        
    Returns:
        Diccionario con nombre, descripcion, stack o None si falla
    """
    archivo_config = os.path.join(ruta_carpeta, "manifest.json")
    
    if not os.path.exists(archivo_config):
        return None
    
    try:
        with open(archivo_config, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        return {
            'nombre': datos.get('name'),
            'descripcion': datos.get('description'),
            'stack': datos.get('stack'),
            'enlacedocvivero': datos.get('enlacedocvivero'),
        }
    except (json.JSONDecodeError, IOError) as e:
        log_debug(f"Error leyendo {archivo_config}: {e}")
        return None


def debe_omitir(carpeta: str) -> tuple[bool, str]:
    """
    Determina si una carpeta debe ser omitida.
    
    Returns:
        Tuple de (debe_omitir, razon)
    """
    # Archivos ocultos
    if carpeta.startswith('.'):
        return True, "oculta"
    
    # Carpetas de la lista de ignorar
    if carpeta in CARPETAS_IGNORAR:
        return True, "ignorada"
    
    # Carpetas que empiezan por número
    if OMITIR_CARPETAS_CON_NUMEROS and carpeta[0].isdigit():
        return True, "numero"
    
    # Carpetas con formato fecha _dd-mm-aa al final
    if OMITIR_CARPETAS_FECHA:
        import re
        if re.search(r'_\d{2}-\d{2}-\d{2}$', carpeta):
            return True, "fecha"
    
    # Carpetas con versiones _cvXXX
    if OMITIR_CARPETAS_CV:
        import re
        if re.search(r'_cv\d+$', carpeta):
            return True, "cv"
    
    return False, ""


def escanear_directorio(ruta_base: str) -> tuple[list[dict], dict]:
    """
    Escanea el directorio y extrae información de los proyectos.
    
    Args:
        ruta_base: Ruta al directorio raíz
        
    Returns:
        Tuple de (lista_proyectos, estadisticas)
    """
    log_debug(f"Escaneando directorio: {ruta_base}")
    
    proyectos = []
    stats = {
        'total': 0,
        'con_manifest': 0,
        'omitidas': {'total': 0, 'numero': 0, 'fecha': 0, 'cv': 0, 'ignorada': 0}
    }
    
    if not os.path.exists(ruta_base):
        log_debug(f"Error: Directorio no encontrado: {ruta_base}")
        return proyectos, stats
    
    for carpeta in os.listdir(ruta_base):
        ruta_completa = os.path.join(ruta_base, carpeta)
        
        # Solo directorios
        if not os.path.isdir(ruta_completa):
            continue
        
        # Verificar si debe omitirse
        omitir, razon = debe_omitir(carpeta)
        if omitir:
            stats['omitidas']['total'] += 1
            stats['omitidas'][razon] = stats['omitidas'].get(razon, 0) + 1
            continue
        
        # Extraer información del manifest
        info = extraer_manifest(ruta_completa)
        
        proyecto = {
            'carpeta': carpeta,
            'nombre': info['nombre'] if info else carpeta,
            'descripcion': info['descripcion'] if info else '',
            'stack': info['stack'] if info else '',
            'enlacedocvivero': info['enlacedocvivero'] if info else None,
        }
        
        proyectos.append(proyecto)
        stats['total'] += 1
        
        if info:
            stats['con_manifest'] += 1
    
    # Ordenar por nombre
    proyectos.sort(key=lambda p: p['nombre'].lower())
    
    log_debug(f"Proyectos encontrados: {stats['total']}")
    log_debug(f"Con manifest: {stats['con_manifest']}")
    log_debug(f"Carpetas omitidas: {stats['omitidas']}")
    
    return proyectos, stats


def limpiar_titulo(titulo: str) -> str:
    """Elimina almohadillas y espacios iniciales del título."""
    return titulo.lstrip('#').strip()


def generar_markdown(proyectos: list[dict], stats: dict, version: str, titulo: str, summary: str) -> str:
    """
    Genera el contenido del archivo Markdown.
    
    Args:
        proyectos: Lista de proyectos
        stats: Estadísticas
        version: Versión del sistema
        titulo: Título del mapa
        summary: Descripción/resumen del mapa
        
    Returns:
        Contenido del markdown como string
    """
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    md = "---\n"
    md += f"version: {version}\n"
    md += f"fecha: {fecha_actual}\n"
    md += "estado: ACTIVO\n"
    md += "tipo: mapa-proyectos\n"
    md += "---\n\n"
    
    md += f"# {limpiar_titulo(titulo)}\n\n"
    md += "> [!summary] Resumen\n"
    md += f"> {summary}\n\n"
    
    # Estadísticas
    md += "## Estadísticas\n\n"
    md += f"- **Total proyectos:** {stats['total']}\n"
    md += f"- **Con manifest:** {stats['con_manifest']}\n"
    md += f"- **Última actualización:** {fecha_actual}\n\n"
    
    # Listado de proyectos
    md += "## Proyectos\n\n"
    
    for p in proyectos:
        stack_linea = p['stack'] if p['stack'] else ''
        icono = icono_stack(p['stack'])
        
        enlace = f"./{p['enlacedocvivero']}" if p.get('enlacedocvivero') else ""
        md += f"- {icono} [{p['nombre']}]({enlace})\n"
        md += f"  > Ubicación: {p['carpeta']}/\n"
        
        if p['descripcion']:
            md += f"  > Descripción: {p['descripcion']}\n"
        
        if stack_linea:
            md += f"  > Stack: {stack_linea}\n"
        
        md += "\n"
    
    return md


def guardar_markdown(ruta: str, contenido: str) -> bool:
    """
    Guarda el contenido en un archivo Markdown.
    
    Args:
        ruta: Ruta del archivo de salida
        contenido: Contenido a escribir
        
    Returns:
        True si fue exitoso, False en caso contrario
    """
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        tamano = os.path.getsize(ruta)
        log_debug(f"Archivo escrito: {ruta} ({tamano / 1024:.1f} KB)")
        return True
    except IOError as e:
        log_debug(f"Error al escribir {ruta}: {e}")
        return False


def es_sistema_linux() -> bool:
    """Devuelve True si se está ejecutando en Linux."""
    return sys.platform.startswith('linux')


def replicar_mapa(origen: str, destino: str) -> bool:
    """
    Copia el archivo generado a la carpeta del vivero correspondiente.
    Sobrescribe el archivo destino si ya existe.

    Args:
        origen: Ruta del archivo generado
        destino: Ruta completa de destino

    Returns:
        True si la copia fue exitosa, False en caso contrario
    """
    try:
        destino_dir = os.path.dirname(destino)
        if destino_dir:
            os.makedirs(destino_dir, exist_ok=True)
        shutil.copy2(origen, destino)
        log_debug(f"Mapa replicado en: {destino}")
        return True
    except (IOError, OSError) as e:
        log_debug(f"Error al replicar en {destino}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Generador de MAP - Mapa de Proyectos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python generar_mapa_vivero.py .
  python generar_mapa_vivero.py /ruta/proyectos
  python generar_mapa_vivero.py . --output MI_MAPA.md
  python generar_mapa_vivero.py . --debug
        """
    )
    
    parser.add_argument(
        'directorio',
        nargs='?',
        default='.',
        help='Directorio a escanear (default: directorio actual)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Nombre del archivo de salida (default: desde manifest_mapa.json)'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Activar mensajes de depuración'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {VERSION_SISTEMA}'
    )
    
    args = parser.parse_args()
    
    # Activar debug si se solicita
    global DEBUG
    DEBUG = args.debug
    
    log_debug(f"Iniciando generación...")
    
    ruta_base = os.path.abspath(args.directorio)
    log_debug(f"Directorio: {ruta_base}")
    
    # Leer config del mapa desde manifest_mapa.json
    config_mapa = leer_manifest_mapa(ruta_base)
    nombre_mapa = config_mapa['nombremapa']
    titulo_mapa = config_mapa['titulomapa']
    summary_mapa = config_mapa['summarymapa']
    
    # Usar output del argumento o del manifest
    output = args.output if args.output else nombre_mapa
    
    # Escanear proyectos
    proyectos, stats = escanear_directorio(ruta_base)
    
    # Generar markdown con valores del manifest
    markdown = generar_markdown(proyectos, stats, VERSION_SISTEMA, titulo_mapa, summary_mapa)
    
    # Guardar archivo
    ruta_salida = os.path.join(ruta_base, output)
    if guardar_markdown(ruta_salida, markdown):
        print(f"✅ Mapa generado: {output}")
        print(f"   {stats['total']} proyectos ({stats['con_manifest']} con manifest)")
    else:
        print(f"❌ Error al generar el mapa")
        sys.exit(1)

    # Replicar en la carpeta del vivero según el sistema operativo
    if es_sistema_linux():
        carpeta_vivero = config_mapa['url_carpeta_vivero_lin']
    else:
        carpeta_vivero = config_mapa['url_carpeta_vivero_win']

    if carpeta_vivero:
        destino = os.path.join(carpeta_vivero, output)
        if replicar_mapa(ruta_salida, destino):
            print(f"📦 Mapa replicado en: {carpeta_vivero}")
        else:
            print(f"⚠️  No se pudo replicar el mapa en {carpeta_vivero}")
    else:
        log_debug("No se configuró carpeta de vivero para este sistema")

    log_debug("Finalizado")


if __name__ == "__main__":
    main()
