# 📄 controladordeversiones

**Versión:** V1.1

## Descripción

Script para observar una carpeta y renombrar automáticamente archivos copiados que contienen " copy" en su nombre, generando versiones numeradas del tipo _cv001, _cv002, etc.

## Funcionalidad

- Detecta archivos nuevos con " copy" en el nombre
- Ignora extensiones definidas por el usuario (.txt, .md, .log)
- Renombra el archivo como una nueva versión del original (_cvXXX)
- Elimina el archivo original al renombrarlo mediante os.rename()
- Permite pasar la ruta a observar como argumento; si no se pasa, usa la carpeta actual
- Se puede cerrar de forma segura con Ctrl+C
- Escanea la carpeta cada 2 segundos por defecto

## Requisitos

- **Lenguaje**: Python 3.6+
- **SO**: Linux, macOS, Windows
- **Permisos**: Lectura y escritura en la carpeta a observar

## Dependencias

Todas las dependencias son built-in de Python:
- `os` - Operaciones del sistema de archivos
- `time` - Control de intervalos de tiempo
- `re` - Expresiones regulares
- `sys` - Parámetros del sistema

No requiere instalación adicional de paquetes.

## Uso

```python
python3 controladordeversiones.py [ruta_carpeta]
```

### Parámetros

| Parámetro | Descripción | Ejemplos |
|-----------|-------------|----------|
| `ruta_carpeta` | Ruta absoluta o relativa de la carpeta a observar | `./descargas`, `~/Documentos`, `/home/usuario/proyecto` |

**Nota**: Si no se especifica ruta_carpeta, el script observa la carpeta actual (.).

## Ejemplo

Observar la carpeta de descargas y renombrar automáticamente copias:

```bash
python3 controladordeversiones.py ~/Descargas
```

El script renombrará automáticamente archivos como:
- `documento copy.pdf` → `documento_cv001.pdf`
- `imagen copy copy.jpg` → `imagen copy_cv001.jpg`
- `video copy.mp4` → `video_cv001.mp4`

