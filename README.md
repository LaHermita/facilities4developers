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

### ⚠️  comprobadorarhivos (v1.0)
- **Archivo:** `comprobadorarhivos.py`
- **Descripción:** Herramienta de auditoría para verificar integridad de recursos multimedia en proyectos web. Detecta automáticamente references rotas o archivos faltantes mediante análisis recursivo de código fuente.
- **Uso:** `python comprobadorarhivos.py [opciones] **Parámetros:** | Parámetro | Opción Larga | Descripción | Valor por defecto | | :--- | :--- | :--- | :--- | | `-d` | `--directorio` | Ruta del directorio raíz...`
- **Dependencias:** `Módulos estándar de Python (sin instalación adicional requerida): - `os` - Operaciones del sistema de archivos - `re` - Procesamiento de expresiones regulares - `argparse` - Procesamiento de...`
- **Requisitos:** `- **Lenguaje:** Python 3.6+ - **Sistema Operativo:** Linux, macOS, Windows - **Permisos:** Acceso de lectura a los directorios del proyecto`
- **Ejemplo:** `Caso de uso 1: Analizar el directorio actual y mostrar resultados en consola python comprobadorarhivos.py Caso de uso 2: Analizar un proyecto específico y exportar reporte python...`

---

### ⚠️  controladordeversiones (v1.0)
- **Archivo:** `controladordeversiones.py`
- **Descripción:** Script que observa una carpeta y renombra automáticamente archivos copiados que contienen `" copy"` en su nombre, generando versiones numeradas del tipo `_v001`, `_v002`, etc. Útil para entornos...
- **Uso:** `python 0controladordeversiones.py python 0controladordeversiones.py /ruta/a/mi/carpeta`
- **Requisitos:** `- Python 3.6 o superior - Módulos utilizados: os, sys, time, re`
- **Ejemplo:** `Sin ejemplo`

---

### ⚠️  copiadeseguridad_docker_4w10 (v1.0)
- **Archivo:** `copiadeseguridad_docker_4w10.ps1`
- **Descripción:** Este script realiza una copia de seguridad comprimida (.zip) de una carpeta especificada (o de la carpeta actual si no se indica ninguna), deteniendo temporalmente un servicio Docker Compose antes...
- **Uso:** `Sin uso`
- **Ejemplo:** `Sin ejemplo`

---

### ⚠️  filtrador_logs_4_multigenerico (v1.0)
- **Archivo:** `filtrador_logs_4_multigenerico.py`
- **Descripción:** Este script en Python 3 analiza registros de acceso de Apache (`access.log`) para detectar y clasificar peticiones potencialmente maliciosas. Separa y prioriza intentos de explotación y escaneos de...
- **Uso:** `Sin uso`
- **Ejemplo:** `Sin ejemplo`

---

