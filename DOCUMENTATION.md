# 📋 Indicaciones para Crear README Homogéneos

> Documento con los estándares de formato y estructura que deben seguir todos los README de scripts para que el indexador (`x-generar_indice-proyectos-extraido-readmes.py`) pueda extraer correctamente la información.

## 🤖 ¿Necesitas Generar un README con IA?

Si prefieres usar ChatGPT, Claude u otro asistente para generar README automáticamente, **consulta [PROMPT_PARA_GENERAR_README.md](PROMPT_PARA_GENERAR_README.md)** donde encontrarás:
- ✅ Prompt completo listo para copiar/pegar
- ✅ Placeholders para rellenar
- ✅ Ejemplos de implementación
- ✅ Checklist de validación

---

## 📌 Resumen Rápido

**Cada script debe tener un archivo README con este naming:**
- `{nombre_script}_README.md` o `{nombre_script}_readme.md`

**Estructura obligatoria:**
1. **Versión** - Debe incluirse explícitamente
2. **Descripción** - Explicación concisa del propósito
3. **Uso** (o **Ejecución**) - Cómo ejecutar el script
4. **Ejemplo** - Caso práctico de uso

---

## � Lo que Extrae el Script

El script mejorado ahora extrae y valida:

| Campo | Obligatorio | Ubicación | Notas |
|-------|:-----------:|-----------|-------|
| **Versión** | ✅ | Cualquier lugar | Formato: `V1.0.0` o `Versión: 1.0.0` |
| **Descripción** | ✅ | `## Descripción` | Máx 200 caracteres útiles |
| **Uso** | ✅ | `## Uso` o `## Ejecución` | Con comandos y parámetros |
| **Ejemplo** | ✅ | `## Ejemplo` | Caso de uso concreto |
| **Dependencias** | ❌ | `## Dependencias` | Opcional (recomendado) |
| **Requisitos** | ❌ | `## Requisitos` | Opcional (sistema operativo, versiones) |

**El script mostrará advertencias ⚠️** en el índice si faltan secciones obligatorias.

---

## �🔧 Estructura Detallada del README

### 1️⃣ VERSIÓN (Obligatoria)

El script busca patrones de versión. **Debe aparecer** en el README en uno de estos formatos:

```markdown
**Versión:** 1.0.0
o
V1.0.0
o
Versión: 2.1.5
```

**✅ Ubicación recomendada:** Al principio del README, después del título.

**Ejemplo correcto:**
```markdown
# 📄 Mi Script Genial

**Versión:** 1.2.0

## Descripción
...
```

---

### 2️⃣ DESCRIPCIÓN (Obligatoria)

**Encabezado requerido:**
```markdown
## Descripción
```
o alternativamente:
```markdown
### Descripción:
```

**Contenido:**
- Explicación clara y concisa del propósito
- Máximo 200 caracteres (se trunca en el índice)
- Sin bloques de código ni símbolos especiales que confundan

**✅ Ejemplo correcto:**
```markdown
## Descripción

Este script automatiza la digitalización de facturas mediante OCR, permitiendo extraer datos de archivos PDF y exportarlos a CSV.
```

**❌ Evitar:**
```markdown
## Descripción
`Este script hace cosas`  ← No usar backticks
El script:
- Punto 1
- Punto 2  ← Mejor usar párrafo fluido
```

---

### 3️⃣ USO / EJECUCIÓN (Obligatoria)

**Encabezados válidos:**
```markdown
## Uso
## Ejecución
## Cómo usar
```

**Contenido:**
- Instrucciones paso a paso o comando de ejecución
- Puede incluir parámetros, argumentos, dependencias
- Los bloques de código se eliminarán automáticamente del índice

**✅ Ejemplo correcto para Python:**
```markdown
## Uso

```bash
python nombre_script.py [argumentos]
```

Se requiere tener instalado:
- Python 3.8+
- pandas
- requests
```

**✅ Ejemplo correcto para PowerShell:**
```markdown
## Ejecución

```powershell
.\nombre_script.ps1 -Parámetro1 valor -Parámetro2 valor
```

Ejecutar con permisos de administrador.
```

---

### 4️⃣ EJEMPLO (Recomendado)

**Encabezado requerido:**
```markdown
## Ejemplo
```

**Contenido:**
- Caso de uso concreto
- Puede incluir comandos y salida esperada
- Los bloques de código se limpian automáticamente

**✅ Ejemplo correcto:**
```markdown
## Ejemplo

Para procesar un archivo de facturas:

```bash
python digitalizador_facturas.py -i facturas.pdf -o datos.csv -v debug
```

Genera: `datos.csv` con campos extraídos automáticamente.
```

---

### 5️⃣ DEPENDENCIAS (Opcional pero Recomendado)

**Encabezado:**
```markdown
## Dependencias
```

**Contenido:**
- Lista de librerías/módulos necesarios
- Comando de instalación (pip, apt, brew, etc.)
- Enlaces a documentación

**✅ Ejemplo correcto para Python:**
```markdown
## Dependencias

```bash
pip install pandas requests beautifulsoup4
```

O desde requirements.txt:
```bash
pip install -r requirements.txt
```
```

**✅ Ejemplo correcto para Bash:**
```markdown
## Dependencias

- `curl` - Para descargas HTTP
- `jq` - Para parsing de JSON
- `imagemagick` - Para procesamiento de imágenes

Instalar en Ubuntu/Debian:
```bash
sudo apt-get install curl jq imagemagick
```
```

---

### 6️⃣ REQUISITOS (Opcional pero Recomendado)

**Encabezado:**
```markdown
## Requisitos
```

**Contenido:**
- Sistema operativo (Linux, Windows, macOS)
- Versiones específicas requeridas
- Permisos necesarios
- Hardware mínimo

**✅ Ejemplo correcto:**
```markdown
## Requisitos

- **SO:** Linux, macOS (Windows con WSL)
- **Python:** 3.8 o superior
- **RAM mínima:** 2GB
- **Permisos:** Acceso de lectura/escritura a directorios de log
- **Usuario:** No requiere permisos de administrador
```

---

## 📚 Guías Específicas por Lenguaje

### 🐍 Scripts en Python

**Estructura recomendada:**
```markdown
# 📋 Nombre del Script

**Versión:** 1.0.0

## Descripción

Descripción clara del propósito del script.

## Requisitos

- Python 3.8+
- Instancia de base de datos MySQL accesible

## Dependencias

```bash
pip install -r requirements.txt
```

## Uso

```bash
python script.py --param1 valor --param2 valor
```

Parámetros disponibles:
- `--param1`: Descripción
- `--param2`: Descripción

## Ejemplo

```bash
python script.py --archivo datos.csv --salida resultado.json --verbose
```

## Troubleshooting

**Error: "ModuleNotFoundError"**
- Solución: Ejecutar `pip install -r requirements.txt`

**Error: "Permiso denegado"**
- Solución: `chmod +x script.py` (si está configurado como ejecutable)
```

---

### 🐚 Scripts en Bash

**Estructura recomendada:**
```markdown
# 🔧 Nombre del Script

**Versión:** 2.0.0

## Descripción

Descripción clara del propósito del script.

## Requisitos

- Bash 4.0+
- Linux/macOS (WSL en Windows)
- Permisos de administrador (si aplica)

## Dependencias

```bash
sudo apt-get install curl wget grep sed
```

## Uso

```bash
./script.sh [opciones] argumentos
```

Opciones:
- `-f FILE`: Archivo de entrada
- `-o OUTPUT`: Archivo de salida
- `-v`: Modo verbose

## Ejemplo

```bash
./script.sh -f datos.txt -o resultado.txt -v
```

## Troubleshooting

**Error: "Permission denied"**
- Solución: `chmod +x script.sh`

**Error: "command not found"**
- Solución: Instalar dependencias con curl/wget
```

---

### 💻 Scripts en PowerShell

**Estructura recomendada:**
```markdown
# ⚡ Nombre del Script

**Versión:** 1.5.0

## Descripción

Descripción clara del propósito del script.

## Requisitos

- Windows 7+ o PowerShell Core
- Permisos de administrador (requerido)
- PowerShell 5.0+

## Dependencias

```powershell
Install-Module -Name ModuleName -Force
```

## Uso

```powershell
.\script.ps1 -Parameter1 valor -Parameter2 valor
```

Parámetros:
- `-Parameter1`: Descripción
- `-Parameter2`: Descripción (opcional)

## Ejemplo

```powershell
.\script.ps1 -Ruta "C:\archivos" -Extensión ".log" -Accion "Archivar"
```

Ejecutar con:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\script.ps1
```

## Troubleshooting

**Error: "No se puede cargar el archivo porque la ejecución de scripts está deshabilitada"**
- Solución: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Error: "No es reconocido como comando"**
- Solución: Prefija `.\` antes del nombre: `.\script.ps1`
```

---

## 📊 Tabla Comparativa: Secciones por Lenguaje

| Sección | Python | Bash | PowerShell |
|---------|:------:|:-----:|:--------:|
| Versión | ✅ | ✅ | ✅ |
| Descripción | ✅ | ✅ | ✅ |
| Requisitos | ✅ | ✅ | ✅ |
| Dependencias | ✅ | ✅ | ✅ |
| Uso | ✅ | ✅ | ✅ |
| Ejemplo | ✅ | ✅ | ✅ |
| Troubleshooting | Recomendado | Recomendado | **Muy recomendado** |

---

## 🐛 Sección: Troubleshooting (Opcional pero Recomendado)

**Encabezado:**
```markdown
## Troubleshooting
```

**Formato:**
```markdown
## Troubleshooting

**Problema: Error al conectar a la base de datos**
- Causa: Credenciales incorrectas
- Solución: Verificar variables de entorno `DB_HOST` y `DB_USER`

**Problema: El script se detiene sin terminar**
- Causa: Timeout en operación de red
- Solución: Aumentar `--timeout 120` o revisar conectividad
```

---

## 🎯 Estructura Completa de un README (Plantilla Mejorada)

```markdown
# 📄 [Nombre del Script]

**Versión:** 1.2.0

## Descripción

Explicación clara y directa de qué hace el script en 1-2 oraciones. Máximo 200 caracteres útiles.

## Requisitos

- Python 3.8+
- SO: Linux/macOS/Windows con WSL
- 100MB de espacio libre

## Dependencias

```bash
pip install -r requirements.txt
```

## Uso

Instrucciones de cómo ejecutar con los parámetros principales.

```bash
python script.py [parámetros]
```

Parámetros:
- `--input`: Archivo de entrada (obligatorio)
- `--output`: Archivo de salida (opcional, default: out.txt)

## Ejemplo

Caso práctico concreto de uso del script.

```bash
python script.py --input datos.txt --output resultado.json --verbose
```

## Troubleshooting

**Error: ModuleNotFoundError**
- Solución: `pip install -r requirements.txt`

**Error: Archivo no encontrado**
- Solución: Verificar ruta relativa/absoluta del archivo
```

---

## 📐 Reglas de Formato y Limpieza

El script aplica estas reglas de limpieza automáticamente:

| Elemento | Se Elimina | Razón |
|----------|-----------|-------|
| Bloques de código markdown | ✅ | Limpieza de índice |
| Encabezados dentro de secciones (###) | ✅ | Evita contaminar índice |
| Espacios y saltos múltiples | ✅ | Normalización |
| Bloques de cita (>) | ✅ | Limpieza visual |
| Más de 200 caracteres | ✅ | Trunca para el índice |

**⚠️ IMPORTANTE:** Aunque se limpien en el índice, puedes usar:
- Bloques de código en tus README (se limpiaran al extraer)
- Encabezados secundarios (### ...) (se eliminarán del índice)
- Listas con viñetas (se convertirán a texto)

---

## 🔍 Validación: Cómo Saber si tu README es Correcto

1. **Verifica que tenga estas secciones:**
   ```python
   # Buscar en tu README:
   - "Versión:" o "V" seguido de números
   - "## Descripción" o "### Descripción:"
   - "## Uso" o "## Ejecución"
   - "## Ejemplo"
   ```

2. **Ejecuta el indexador:**
   ```bash
   python x-generar_indice-proyectos-extraido-readmes.py
   ```

3. **Verifica el README.md generado** y busca tu script. Si algo falta o se ve incorrecto, ajusta el README según esta guía.

---

## 📝 Checklist para Nuevos README

- [ ] Nombre del archivo: `{nombre_script}_README.md` o `{nombre_script}_readme.md`
- [ ] Incluye la versión en formato `V1.0.0` o `Versión: 1.0.0`
- [ ] Sección `## Descripción` con explicación clara (máx 200 caracteres útiles)
- [ ] Sección `## Uso` o `## Ejecución` con instrucciones
- [ ] Sección `## Ejemplo` con caso práctico
- [ ] Encoding UTF-8 en el archivo
- [ ] Sintaxis Markdown correcta (sin errores de formato)
- [ ] Probado: ejecutó el indexador y aparece bien en README.md

---

## 🚀 Ejemplo Práctico Completo: Script en Python

### Archivo: `analizador_logs.py`

**README a crear:** `analizador_logs_README.md`

```markdown
# 📊 Analizador de Logs

**Versión:** 2.1.0

## Descripción

Script que analiza archivos de log de servidores, extrae patrones de error y genera reportes en formato HTML con estadísticas de fallos.

## Uso

```bash
python analizador_logs.py -archivo logs.txt -salida reporte.html -nivel ERROR
```

Parámetros:
- `-archivo`: Ruta del archivo de log a procesar
- `-salida`: Ubicación del reporte HTML generado
- `-nivel`: Filtro por nivel (ERROR, WARNING, INFO)

## Ejemplo

```bash
python analizador_logs.py -archivo /var/log/app.log -salida reporte.html -nivel ERROR
```

Generará `reporte.html` con gráficos de distribución de errores por hora.
```

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo poner el README dentro del script como docstring?**
R: Sí, pero no es recomendado. El script busca primero archivos `_README.md` externos. Si no los encuentra, lee el docstring del script. Lo mejor es mantener README externos para claridad.

**P: ¿Qué pasa con los caracteres especiales en la descripción?**
R: Se preservan normalmente. El script solo elimina backticks y bloques de código. Emojis y caracteres especiales funcionan bien.

**P: ¿La versión puede tener más de 3 dígitos (1.0.0.5)?**
R: El regex acepta `\d+\.\d+(?:\.\d+)?`, así que máximo 3 componentes. Usa formato `X.Y.Z` para compatibilidad.

**P: ¿Y si mi script no tiene ejemplo concreto?**
R: Intenta de todos modos agregarlo con un caso hipotético. El indexador mostrará "Sin ejemplo" si no lo encuentra, lo cual es mejor que dejar vacío.

---

**Última actualización:** 4 de marzo de 2026
**Documento generado para:** facilities4developers
