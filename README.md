# ⚙️ Colección Personal de Scripts de Automatización 🚀

> Repositorio centralizado para **optimizar tareas y flujos de trabajo diarios**. Contiene scripts desarrollados en **Python**, **Bash** y **PowerShell** para la gestión de sistemas, administración de datos y automatización general.

## ⚡ Estado del Repositorio y Tecnologías
[![Status](https://img.shields.io/badge/Status-Activo-green)]()
![Python](https://img.shields.io/badge/Scripts-Python-blue?logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Scripts-Bash-lightgrey?logo=gnu-bash&logoColor=white)
![PowerShell](https://img.shields.io/badge/Scripts-PowerShell-5391FE?logo=powershell&logoColor=white)

## 🎯 Enfoque Principal

El objetivo es mantener una biblioteca de scripts **reutilizables** y **bien documentados** para reducir la fricción en las tareas rutinarias y servir como recurso de referencia rápida.

## Documentación

- [Guía de cabeceras de scripts](<docs/GUIA Cabeceras Scripts.md>)
- [Estado del proyecto](<docs/SPEC - Estado Proyecto.md>)

***


## Índice de scripts

### ✅ backup_carpeta_zip (v1.0.0)
- **Archivo:** `backup_carpeta_zip.py`
- **Descripción:** Crea una copia de seguridad ZIP de una carpeta, excluyendo archivos y directorios temporales o de desarrollo.
- **Uso:** `python backup_carpeta_zip.py <carpeta_origen> [carpeta_destino]`
- **Dependencias:** `- sys - pathlib - zipfile - datetime - fnmatch`
- **Ejemplo:** `python backup_carpeta_zip.py /ruta/proyecto ./backups`

---

### ✅ comprobador_enlaces_arhivos (v1.0.2)
- **Archivo:** `comprobador_enlaces_arhivos.py`
- **Descripción:** Analiza recursivamente archivos de código fuente buscando referencias a imágenes y audio, verificando su existencia física en el sistema de archivos y generando reportes visuales o Markdown.
- **Uso:** `python comprobador_enlaces_arhivos.py [-d DIRECTORIO] [-e REPORTE.md]`
- **Dependencias:** `- os - re - argparse`
- **Ejemplo:** `python comprobador_enlaces_arhivos.py -d /var/www/proyecto -e informe.md`

---

### ✅ copiadeseguridad_docker_4w10 (v1.0.0)
- **Archivo:** `copiadeseguridad_docker_4w10.ps1`
- **Descripción:** Realiza una copia de seguridad comprimida (.zip) de una carpeta, deteniendo y reiniciando automáticamente el servicio Docker Compose antes y después del proceso.
- **Uso:** `.\copiadeseguridad_docker_4w10.ps1 [-carpetaOrigen <ruta>]`
- **Dependencias:** `- Docker Compose - 7-Zip`
- **Ejemplo:** `.\copiadeseguridad_docker_4w10.ps1 -carpetaOrigen C:\Docker\wordpress`

---

### ✅ generar_arbol_contenidos_md (v1.4.2)
- **Archivo:** `generar_arbol_contenidos_md.py`
- **Descripción:** Recorre una carpeta recursivamente, ignora elementos ocultos y genera un Markdown con el árbol de contenidos y el listado de archivos .md.
- **Uso:** `python3 generar_arbol_contenidos_md.py [RUTA]`
- **Dependencias:** `- argparse - datetime - pathlib`
- **Ejemplo:** `python3 generar_arbol_contenidos_md.py Embarcadero`

---

### ✅ generar_cartografia (v2.3.1)
- **Archivo:** `generar_cartografia.py`
- **Descripción:** Genera cartografia_lh.png y cartografia_lh.md a partir de los mapas MAP - *.md, con tarjetas masonry, totales y leyenda de colores.
- **Uso:** `python generar_cartografia.py [--raiz RUTA] [--salida IMAGEN.png]`
- **Dependencias:** `- argparse - fnmatch - math - os - re - sys - datetime - Pillow`
- **Ejemplo:** `python generar_cartografia.py --raiz /ruta/proyectos --salida cartografia_lh.png`

---

### ✅ generar_cartografia_total (v2.8.1)
- **Archivo:** `generar_cartografia_total.py`
- **Descripción:** Genera cartografia_lh_total.png y cartografia_lh_total.md a partir de los mapas MAP - *.md, con masonry global por bloque y etiqueta de ruta.
- **Uso:** `python generar_cartografia_total.py [--raiz RUTA] [--salida IMAGEN.png]`
- **Dependencias:** `- argparse - fnmatch - math - os - re - sys - datetime - Pillow`
- **Ejemplo:** `python generar_cartografia_total.py --salida cartografia_lh_total.png`

---

### ✅ generar_cartografia_total_cacsa (v2.5.1)
- **Archivo:** `generar_cartografia_total_cacsa.py`
- **Descripción:** Genera cartografia_cacsa.png y cartografia_cacsa.md a partir de los mapas MAP - *.md de las rutas CAC, con paleta corporativa y masonry global.
- **Uso:** `python generar_cartografia_total_cacsa.py [--raiz RUTA] [--salida IMAGEN.png]`
- **Dependencias:** `- argparse - fnmatch - math - os - re - sys - datetime - Pillow`
- **Ejemplo:** `python generar_cartografia_total_cacsa.py --salida cartografia_cacsa.png`

---

### ✅ generar_mapa_vivero (v1.19.1)
- **Archivo:** `generar_mapa_vivero.py`
- **Descripción:** Genera un archivo Markdown con el mapa de proyectos de un directorio a partir de los manifest.json de cada carpeta.
- **Uso:** `python generar_mapa_vivero.py [directorio] [--output nombre_archivo.md] [--debug]`
- **Dependencias:** `- os - sys - json - shutil - argparse - datetime - pathlib - typing`
- **Ejemplo:** `python generar_mapa_vivero.py . --output MI_MAPA.md --debug`

---

### ✅ versionar_carpeta (v2.1.1)
- **Archivo:** `versionar_carpeta.py`
- **Descripción:** Observa una carpeta y renombra automáticamente las subcarpetas copiadas que contienen un texto configurable, generando versiones numeradas _cv001, _cv002, etc.
- **Uso:** `python versionar_carpeta.py [ruta_a_observar]`
- **Dependencias:** `- os - time - re - sys`
- **Ejemplo:** `python versionar_carpeta.py /home/usuario/miscarpetas`

---

### ✅ versionar_carpeta_ignore (v1.1.1)
- **Archivo:** `versionar_carpeta_ignore.py`
- **Descripción:** Crea copias versionadas (snapshots) de una carpeta ignorando automáticamente los archivos y directorios definidos en su .gitignore.
- **Uso:** `python versionar_carpeta_ignore.py <carpeta>`
- **Dependencias:** `- pathspec`
- **Ejemplo:** `python versionar_carpeta_ignore.py MiProyecto`

---

