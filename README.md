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

### copia_seguridad_docker.ps1 (v1.0)
- **Archivo:** `0copiadeseguridad_docker_4w10.ps1`
- **Descripción:** Este script realiza una copia de seguridad comprimida (.zip) de una carpeta especificada (o de la carpeta actual si no se indica ninguna), deteniendo temporalmente un servicio Docker Compose antes del proceso y reiniciándolo después.
- **Uso:** `.\copia_seguridad_docker.ps1`
- **Ejemplo:** `.\copia_seguridad_docker.ps1 "E:\DockersDevel\wordpresscactele"`

---

### 0controladordeversiones.py (v1.1)
- **Archivo:** `0controladordeversiones.py`
- **Descripción:** Script para observar una carpeta y renombrar automáticamente archivos copiados que contienen " copy" en su nombre. Genera versiones numeradas del tipo _cv001, _cv002, etc.
- **Uso:** `python 0controladordeversiones.py [ruta/opcional]`
- **Ejemplo:** `python 0controladordeversiones.py /mi/proyecto """`

---

