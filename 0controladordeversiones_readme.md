# 📁 0controladordeversiones

**Versión:** 1.0  
**Archivo(s) principal(es):** `0controladordeversiones.py`

## Descripción

Script que observa una carpeta y renombra automáticamente archivos copiados que contienen `" copy"` en su nombre, generando versiones numeradas del tipo `_v001`, `_v002`, etc. Útil para entornos donde se generan duplicados y se necesita control de versiones automatizado.

## Características principales

- Observación continua de una carpeta especificada
- Detección automática de archivos que contienen `" copy"`
- Renombrado incremental con sufijo `_vXXX`
- Eliminación del archivo original tras renombrarlo
- Ignora extensiones definidas por el usuario: `.txt`, `.md`, `.log`
- Ruta opcional como argumento; por defecto usa la carpeta actual
- Finalización segura mediante `Ctrl+C`

## Requisitos

- Python 3.6 o superior
- Módulos utilizados: os, sys, time, re

## Instalación

1. Clona o descarga el repositorio que contiene el script  
2. Accede al directorio que contiene el archivo  
3. Verifica que tienes Python correctamente instalado (versión ≥ 3.6)

## Uso

### Sintaxis básica

> bash  
python 0controladordeversiones.py [ruta_opcional]  
<

### Ejemplos de uso

#### 1. Caso básico

> bash  
python 0controladordeversiones.py  
<

#### 2. Carpeta específica

> bash  
python 0controladordeversiones.py /ruta/a/mi/carpeta  
<

## Funcionamiento

1. Escanea la carpeta objetivo cada 2 segundos  
2. Detecta archivos nuevos con `" copy"` en el nombre  
3. Renombra automáticamente con el siguiente número de versión disponible  
4. Elimina el archivo original tras el renombrado

### Ejemplo de transformación

>  
informe copy.pdf → informe_v001.pdf  
<

## Configuración

Los siguientes parámetros pueden ajustarse directamente desde el código fuente:

- `EXTENSIONES_IGNORADAS`: Lista de extensiones que deben ignorarse  
- `SCAN_INTERVAL`: Intervalo en segundos entre escaneos de la carpeta

## Mensajes del sistema

El script imprime mensajes amigables con emojis:

- 👀 Vigilando la carpeta  
- ⏭️ Ignorado por extensión  
- ✅ Renombrado correctamente  
- ⚠️ Error durante el renombrado  
- 👋 Script detenido por el usuario

## Detención del script

Para detener el script de forma segura:

> bash  
Ctrl + C  
<

## Manejo de errores

- Si la ruta proporcionada no es válida, el script termina con un mensaje de error  
- Errores durante el renombrado son capturados y notificados sin detener el proceso  
- Evita errores con archivos de extensiones ignoradas o subdirectorios

## Limitaciones

- No realiza seguimiento de subcarpetas  
- No permite definir reglas de renombrado personalizadas por usuario  
- El escaneo es periódico, no en tiempo real basado en eventos del sistema

## Casos de uso recomendados

- Monitorear carpetas donde se copian archivos manualmente  
- Automatizar versión de entregables para trabajos colaborativos  
- Mantener control ordenado de duplicados sin sobrescribir originales

## Contribución

Puedes colaborar mediante sugerencias, mejoras en la lógica de escaneo, compatibilidad con más extensiones o integración con sistemas de monitoreo de archivos.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Historial de versiones

- **v1.0**: Versión inicial del script. Renombrado automático de archivos copiados con control de versiones básico.
