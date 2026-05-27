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


## Índice de scripts

### ✅ comprobadorarhivos (v1.0.0)
- **Archivo:** `comprobadorarhivos.py`
- **Descripción:** Analiza recursivamente archivos de código fuente buscando referencias a imágenes y audio, verificando su existencia física en el sistema de archivos y generando reportes visuales o Markdown.
- **Uso:** `python comprobadorarhivos.py [-d DIRECTORIO] [-e REPORTE.md]`
- **Dependencias:** `- os - re - argparse`
- **Ejemplo:** `python comprobadorarhivos.py -d /var/www/proyecto -e informe.md`

---

### ✅ controladorversionescarpetas (v2.1)
- **Archivo:** `controladorversionescarpetas.py`
- **Descripción:** Observa una carpeta y renombra automáticamente subcarpetas cuyo nombre contenga un patrón configurable (por defecto "(copia)"), generando versiones numeradas secuenciales (_cv001, _cv002, ...).
- **Uso:** `python controladorversionescarpetas.py [ruta_a_observar]`
- **Dependencias:** `- os - time - re - sys`
- **Ejemplo:** `python controladorversionescarpetas.py /home/usuario/miscarpetas`

---

### ✅ controladorversionescarpetasmanual (v1.1)
- **Archivo:** `controladorversionescarpetasmanual.py`
- **Descripción:** Crea copias versionadas (snapshots) de carpetas de trabajo ignorando automáticamente archivos y directorios definidos en .gitignore.
- **Uso:** `python controladorversionescarpetasmanual.py <carpeta>`
- **Dependencias:** `- pathspec (instalación externa)`
- **Ejemplo:** `python controladorversionescarpetasmanual.py MiProyecto`

---

### ✅ copiadeseguridad_docker_4w10 (v1.0.0)
- **Archivo:** `copiadeseguridad_docker_4w10.ps1`
- **Descripción:** Realiza una copia de seguridad comprimida (.zip) de una carpeta, deteniendo y reiniciando automáticamente el servicio Docker Compose antes y después del proceso.
- **Uso:** `.\copiadeseguridad_docker_4w10.ps1 [-carpetaOrigen <ruta>]`
- **Dependencias:** `- Docker Compose - 7-Zip`
- **Ejemplo:** `.\copiadeseguridad_docker_4w10.ps1 -carpetaOrigen C:\Docker\wordpress`

---

### ✅ filtrador_logs_4_multigenerico (v1.0.0)
- **Archivo:** `filtrador_logs_4_multigenerico.py`
- **Descripción:** Este script en Python 3 analiza registros de acceso de Apache (`access.log`) para detectar y clasificar peticiones potencialmente maliciosas. Separa y prioriza intentos de explotación y escaneos de...
- **Uso:** `python3 filtrador_logs_4_multigenerico.py`
- **Ejemplo:** `Analizar un archivo access.log y generar informes de amenazas: python3 filtrador_logs_4_multigenerico.py Salida esperada: archivos `accesslog_filtrado_GET_YYYYMMDD.md`,...`

---

