# 📄 comprobadorarhivos

**Versión:** 1.0

## Descripción

Herramienta de auditoría para verificar integridad de recursos multimedia en proyectos web. Detecta automáticamente references rotas o archivos faltantes mediante análisis recursivo de código fuente.

## Funcionalidad

El programa recorre el árbol de directorios del proyecto ignorando carpetas irrelevantes (node_modules, .git, etc.), extrae referencias a recursos multimedia mediante expresiones regulares desde archivos de código fuente (.html, .js, .json), y verifica la existencia física de cada recurso detectado en el sistema de archivos. Ofrece salida visual en consola con códigos de colores y permite exportación de reportes en formato Markdown. Configurable para analizar diferentes tipos de archivos y verificar diferentes extensiones de recursos.

## Requisitos

- **Lenguaje:** Python 3.6+
- **Sistema Operativo:** Linux, macOS, Windows
- **Permisos:** Acceso de lectura a los directorios del proyecto

## Dependencias

Módulos estándar de Python (sin instalación adicional requerida):
- `os` - Operaciones del sistema de archivos
- `re` - Procesamiento de expresiones regulares
- `argparse` - Procesamiento de argumentos de línea de comandos

## Uso

```python
python comprobadorarhivos.py [opciones]
```

**Parámetros:**

| Parámetro | Opción Larga | Descripción | Valor por defecto |
| :--- | :--- | :--- | :--- |
| `-d` | `--directorio` | Ruta del directorio raíz del proyecto a escanear | `.` (directorio actual) |
| `-e` | `--exportar` | Nombre del archivo Markdown (.md) para guardar el informe | Ninguno (solo consola) |

## Ejemplo

Caso de uso 1: Analizar el directorio actual y mostrar resultados en consola

```python
python comprobadorarhivos.py
```

Caso de uso 2: Analizar un proyecto específico y exportar reporte

```python
python comprobadorarhivos.py -d /ruta/a/proyecto -e reporte_verificacion.md
```

Caso de uso 3: Analizar sin la extensión .md en el parámetro

```python
python comprobadorarhivos.py -d ~/mi_proyecto -e reporte
```

