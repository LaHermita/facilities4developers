"""
- Nombre del archivo: comprobadorarchivos.py
- Versión: 1.0

- Descripción corta: 
Este script es una herramienta de auditoría para desarrolladores web diseñada para asegurar la integridad de los recursos multimedia antes de un despliegue. Analiza de forma recursiva archivos de código fuente buscando referencias a imágenes y audio, contrastándolas con el sistema de archivos local para detectar rutas rotas o archivos faltantes de manera automática.

- Funcionalidad: 
El programa recorre el árbol de directorios del proyecto ignorando carpetas irrelevantes o pesadas (como node_modules), extrae rutas de archivos mediante expresiones regulares y verifica la existencia física de cada recurso detectado. Ofrece una salida visual clara por consola con códigos de colores y permite la exportación opcional de un reporte técnico en formato Markdown.
"""

import os
import re
import argparse

# --- CONFIGURACIÓN PERSONALIZABLE ---

# Archivos donde buscaremos texto (puedes añadir .php, .py, .css, etc.)
EXTENSIONES_PARA_ANALIZAR = ['.html', '.js', '.json']

# Archivos cuya existencia queremos verificar
EXTENSIONES_DE_RECURSOS = ['.jpg', '.png', '.mp3']

# Carpetas que el script saltará para ahorrar tiempo y evitar falsos positivos
CARPETAS_A_IGNORAR = {
    '.git', 'node_modules', '__pycache__', 'dist', 
    'env', 'venv', '.vscode', '.idea', 'build'
}

# Códigos de color ANSI para una consola más legible
COLOR_VERDE = '\033[92m'
COLOR_ROJO = '\033[91m'
COLOR_AZUL = '\033[94m'
COLOR_RESET = '\033[0m'
NEGRITA = '\033[1m'

def obtener_patron_busqueda(extensiones):
    """
    Construye una expresión regular dinámica basada en las extensiones de recursos.
    Busca patrones de texto que terminen en las extensiones configuradas.
    """
    extensiones_sin_punto = [ext.replace('.', '') for ext in extensiones]
    # El patrón busca caracteres de ruta seguidos de un punto y la extensión
    patron = r'[\w\-\./]+\.(?:' + '|'.join(extensiones_sin_punto) + ')'
    return re.compile(patron)

def comprobar_existencia_de_recursos(directorio_raiz):
    """
    Navega por las carpetas, lee archivos de código y verifica si los 
    recursos mencionados en ellos existen en el disco.
    """
    patron = obtener_patron_busqueda(EXTENSIONES_DE_RECURSOS)
    informe_final = {}

    for ruta_actual, carpetas, archivos in os.walk(directorio_raiz):
        # Modificamos 'carpetas' in-place para que os.walk no entre en las ignoradas
        carpetas[:] = [c for c in carpetas if c not in CARPETAS_A_IGNORAR]
        
        for nombre_archivo in archivos:
            # Solo procesamos archivos que están en nuestra lista de análisis
            if any(nombre_archivo.endswith(ext) for ext in EXTENSIONES_PARA_ANALIZAR):
                ruta_completa_archivo = os.path.join(ruta_actual, nombre_archivo)
                
                try:
                    # 'errors=ignore' evita que el script falle si encuentra caracteres extraños
                    with open(ruta_completa_archivo, 'r', encoding='utf-8', errors='ignore') as f:
                        contenido = f.read()
                        # Buscamos todas las menciones que coincidan con el patrón Regex
                        menciones = set(patron.findall(contenido))
                        
                        if menciones:
                            resultados_archivo = []
                            for ref in menciones:
                                # Normalizamos la ruta quitando el slash inicial si existe
                                ruta_recurso = os.path.join(directorio_raiz, ref.lstrip('/'))
                                existe = os.path.exists(ruta_recurso)
                                resultados_archivo.append((ref, existe))
                            
                            informe_final[ruta_completa_archivo] = resultados_archivo
                except Exception as error:
                    print(f"{COLOR_ROJO}Error al procesar {nombre_archivo}: {error}{COLOR_RESET}")

    return informe_final

def mostrar_informe_en_consola(resultados):
    """Imprime un resumen visual y ordenado en la terminal."""
    print(f"\n{NEGRITA}🔍 RESULTADOS DEL ANÁLISIS DE RUTAS{COLOR_RESET}\n")
    
    if not resultados:
        print(f"{COLOR_VERDE}No se encontraron referencias o todo está correcto.{COLOR_RESET}")
        return

    for fuente, recursos in resultados.items():
        print(f"{COLOR_AZUL}{NEGRITA}📁 Archivo: {fuente}{COLOR_RESET}")
        for path, existe in recursos:
            icono = "✅" if existe else "❌"
            tag = f"{COLOR_VERDE}[OK]{COLOR_RESET}" if existe else f"{COLOR_ROJO}[FALTA]{COLOR_RESET}"
            print(f"  {icono} {path:<45} {tag}")
        print("-" * 70)

def generar_informe_markdown(resultados, nombre_salida):
    """Crea un documento Markdown profesional con las tablas de resultados."""
    try:
        with open(nombre_salida, 'w', encoding='utf-8') as md:
            md.write("# 📋 Reporte de Verificación de Archivos\n\n")
            md.write("Este informe resume el estado de los recursos multimedia referenciados.\n\n")
            
            for fuente, recursos in resultados.items():
                md.write(f"### Archivo analizado: `{fuente}`\n\n")
                md.write("| Referencia detectada | Estado | Detalle |\n")
                md.write("| :--- | :---: | :--- |\n")
                for path, existe in recursos:
                    check = "✅" if existe else "❌"
                    status = "Disponible" if existe else "**Desaparecido**"
                    md.write(f"| {path} | {check} | {status} |\n")
                md.write("\n---\n\n")
        print(f"\n{COLOR_VERDE}💾 Informe guardado con éxito en: {nombre_salida}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}No se pudo generar el archivo Markdown: {e}{COLOR_RESET}")

def principal():
    """Punto de entrada del script. Gestiona los argumentos de la terminal."""
    parser = argparse.ArgumentParser(description="Auditoría de existencia de archivos para proyectos Web.")
    parser.add_argument("-d", "--directorio", default=".", help="Carpeta raíz del proyecto a escanear.")
    parser.add_argument("-e", "--exportar", help="Nombre del archivo Markdown (.md) para guardar el informe.")

    args = parser.parse_args()

    # Validamos que la carpeta exista antes de empezar
    if os.path.isdir(args.directorio):
        print(f"{COLOR_AZUL}Analizando proyecto en: {os.path.abspath(args.directorio)}{COLOR_RESET}")
        datos = comprobar_existencia_de_recursos(args.directorio)
        
        # Siempre mostramos en consola para feedback inmediato
        mostrar_informe_en_consola(datos)
        
        # Si el usuario pasó el parámetro -e, exportamos a Markdown
        if args.exportar:
            # Aseguramos que termine en .md
            nombre_archivo = args.exportar if args.exportar.endswith('.md') else f"{args.exportar}.md"
            generar_informe_markdown(datos, nombre_archivo)
    else:
        print(f"{COLOR_ROJO}Error: El directorio '{args.directorio}' no existe.{COLOR_RESET}")

if __name__ == "__main__":
    principal()