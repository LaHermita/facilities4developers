# 🛡️ Analizador de Logs Apache

> Filtrado Inteligente de Peticiones Sospechosas en Logs de Acceso

## 📝 Descripción

Este script en Python 3 analiza registros de acceso de Apache (`access.log`) para detectar y clasificar peticiones potencialmente maliciosas. Separa y prioriza intentos de explotación y escaneos de vulnerabilidades, generando informes detallados y datos estructurados para análisis posterior.

Diseñado con un enfoque didáctico y colaborativo, facilita su comprensión y adaptación por cualquier técnico del equipo.

## ✨ Características principales

### 📊 Análisis y clasificación

- Separación automática de peticiones GET/POST
- Sistema de puntuación configurable por riesgo
- Lista blanca de IPs con soporte CIDR y wildcards
- Detección de patrones de ataque conocidos

### 📂 Archivos generados

| Archivo | Descripción |
|---------|-------------|
| `accesslog_filtrado_GET_YYYYMMDD.md` | Informe detallado de peticiones GET sospechosas |
| `accesslog_filtrado_POST_YYYYMMDD.md` | Informe detallado de peticiones POST sospechosas |
| `accesslog_filtrado_GET_YYYYMMDD.csv` | Datos estructurados GET para análisis |
| `accesslog_filtrado_POST_YYYYMMDD.csv` | Datos estructurados POST para análisis |

* Permite definir un listado de IPs o subredes internas (por ejemplo 172.18.0.X, 172.18.X.X) que no serán analizadas ni añadidas a los archivos filtrados.

✅ Barra de progreso en consola (sin dependencias externas)
Muestra visualmente el avance del proceso (porcentaje, barra visual, líneas procesadas, velocidad, ETA). Implementada con funcionalidad propia para evitar instalar paquetes extra.

✅ Mensajes en color y con iconos
Los mensajes de estado y progreso incluyen colores ANSI y símbolos (emojis) para mejorar la legibilidad y la experiencia en consola.

✅ Código completamente documentado y legible en castellano
Todas las variables, funciones y comentarios están en español, priorizando la claridad del código frente a la brevedad.

✅ Salida adicional en CSV
Para cada método (GET/POST) se genera también un CSV con campos clave para análisis o integración con otras herramientas.

††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††

## ⚙️ Configuración

### 🎯 Parámetros principales

| Variable | Descripción | Valor por defecto |
|:---------|:------------|:------------------|
| `RUTA_LOG` | Archivo de entrada | `'access.log'` |
| `UMBRAL_SCORE` | Puntuación mínima para incluir entrada | `5` |
| `PESO_POST` | Puntos extra para peticiones POST | `5` |

### 📄 Archivos de salida

| Variable | Descripción | Formato |
|:---------|:------------|:--------|
| `OUT_MD_GET` | Informe GET | `accesslog_filtrado_GET_YYYYMMDD.md` |
| `OUT_MD_POST` | Informe POST | `accesslog_filtrado_POST_YYYYMMDD.md` |
| `OUT_CSV_GET` | Datos GET | `accesslog_filtrado_GET_YYYYMMDD.csv` |
| `OUT_CSV_POST` | Datos POST | `accesslog_filtrado_POST_YYYYMMDD.csv` |

### 📊 Sistema de puntuación

La severidad de cada patrón detectado se clasifica según su nivel de riesgo:

```python
SEVERITY_PUNTOS = {
    'critical': 10,  # Intentos directos de explotación
    'high': 6,      # Actividad muy sospechosa
    'medium': 3,    # Actividad potencialmente maliciosa
    'low': 1        # Anomalías menores
}
```

### 🔒 Lista blanca de IPs

La variable `LISTA_BLANCA_IPS` acepta tres formatos diferentes para máxima flexibilidad:

| Formato | Ejemplo | Descripción |
|:--------|:--------|:------------|
| IP exacta | `127.0.0.1` | Coincidencia exacta con una IP |
| Rango CIDR | `10.0.0.0/8` | Bloque completo de direcciones |
| Wildcards | `172.18.X.X` | Patrones flexibles con 'X' |

## 🔍 Sistema de detección de amenazas

### 🌐 Patrones generales (GET y POST)

| Categoría | Patrones | Severidad |
|:----------|:---------|:---------:|
| **Ejecución remota** | `/vendor/phpunit/.*/eval-stdin.php`<br>`0x[]=androxgh0st`<br>`eval()`, `system()`, `exec()` | Critical |
| **Archivos sensibles** | `/.env`, `/aws/credentials`<br>`/etc/passwd`, `/proc/self/environ`<br>`/.git/HEAD`, `/phpinfo.php` | High |
| **Inyecciones SQL** | `UNION SELECT`<br>`' OR '1'='1'`<br>Payloads base64 | High |
| **XSS** | `<script>`, `%3Cscript`<br>Eventos JS<br>Payloads ofuscados | Medium |
| **Path Traversal** | `../`, `..\\`<br>`php://input`, `expect://`<br>`data:text/plain;` | High |
| **Otros indicadores** | Null bytes (`%00`)<br>URIs > 200 chars<br>Encodings múltiples | Medium |

### 📮 Patrones específicos POST

| Categoría | Descripción | Ejemplos |
|:----------|:------------|:---------|
| **Subida de archivos** | • Extensions PHP<br>• MIME types sospechosos<br>• Headers multipart | `.php`, `.phtml`<br>`application/x-httpd-php`<br>`filename=*.php` |
| **Manipulación de objetos** | • Serialización PHP<br>• Magic methods<br>• Object injection | `__wakeup`<br>`__destruct`<br>`O:8:"stdClass"` |
| **Autenticación** | • Fuerza bruta<br>• Manipulación de tokens<br>• Cookie tampering | Múltiples intentos<br>JWT modificados<br>Cookies malformadas |

### 🔠 Métodos HTTP monitorizados

| Riesgo | Métodos | Score |
|:-------|:--------|:-----:|
| **Alto** | `PROPFIND`<br>`TRACE`<br>`CONNECT` | +6 |
| **Medio** | `PUT`<br>`DELETE` | +3 |

### 🔎 User-Agents sospechosos

| Categoría | Ejemplos | Score |
|:----------|:---------|:-----:|
| **Scanners de vulnerabilidades** | sqlmap, nikto, acunetix | +6 |
| **Network scanners** | nmap, masscan | +4 |
| **Herramientas automáticas** | curl, wget, python-requests | +2 |
| **Crawlers maliciosos** | ZmEu, libwww-perl | +3 |

Los patrones pueden ampliarse o afinarse editando la lista PATRONES o PATRONES_SOLO_POST.

††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††††

## 💻 Uso y funcionamiento

### 📋 Requisitos previos

| Componente | Requisito | Notas |
|:-----------|:----------|:------|
| **Python** | ≥ 3.8 | Sin módulos adicionales |
| **Sistema** | Linux/Unix/Windows | Multiplataforma |
| **Logs** | Combined Log Format | Formato Apache estándar |
| **Espacio** | 2x tamaño log | Para archivos de salida |

### 🚀 Ejecución básica

```bash
# Uso simple con configuración por defecto
python3 filtrador_logs_4_multigenerico.py

# Especificar archivo de log (opcional)
export RUTA_LOG="/var/log/apache2/access.log"
python3 filtrador_logs_4_multigenerico.py
```

### 📊 Campos procesados

| Campo | Descripción | Ejemplo |
|:------|:------------|:--------|
| **IP** | Dirección del cliente | `192.168.1.1` |
| **Timestamp** | Fecha y hora | `[16/Oct/2025:10:20:30 +0000]` |
| **Request** | Petición completa | `"GET /index.php HTTP/1.1"` |
| **Status** | Código HTTP | `404` |
| **Size** | Tamaño respuesta | `1234` |
| **Referer** | URL origen | `"https://example.com"` |
| **User-Agent** | Cliente HTTP | `"Mozilla/5.0..."` |

### 📑 Formato de salidas

#### 📘 Archivos Markdown (.md)

Los archivos Markdown proporcionan una vista detallada y legible de cada incidencia:

<details>
<summary><b>Ejemplo de entrada en Markdown</b></summary>

```markdown
# 🚨 POSIBLE INCIDENCIA - Score=8 - IP=1.2.3.4
192.168.1.1 - - [16/Oct/2025:10:20:30 +0000] "GET /phpinfo.php HTTP/1.1" 404 123 "-" "sqlmap/1.0"

## 📊 Detalles
  • Método: GET
  • Ruta (raw): /phpinfo.php
  • Ruta (decoded): /phpinfo.php
  • User-Agent: sqlmap/1.0

## 🎯 Patrones detectados
  ◆ phpinfo (tag=high)
  ◆ ua_sqlmap (tag=low)

## 📈 Análisis
  • Score total: 8
  • Severidad: HIGH
  • Recomendación: Revisar actividad de la IP
```
</details>

#### 📊 Archivos CSV

Los CSV facilitan el análisis cuantitativo y la integración con otras herramientas:

<details>
<summary><b>Estructura del CSV</b></summary>

| Campo | Tipo | Ejemplo |
|:------|:-----|:--------|
| **ip** | string | `1.2.3.4` |
| **time** | datetime | `16/Oct/2025:10:20:30` |
| **method** | string | `GET` |
| **ruta_cruda** | string | `/phpinfo.php` |
| **ruta_decodificada** | string | `/phpinfo.php` |
| **status** | integer | `404` |
| **size** | integer | `123` |
| **agent** | string | `sqlmap/1.0` |
| **score** | integer | `8` |
| **matches** | string | `phpinfo:high;ua_sqlmap:low` |

```csv
ip,time,method,ruta_cruda,ruta_decodificada,status,size,agent,score,matches
1.2.3.4,16/Oct/2025:10:20:30,GET,/phpinfo.php,/phpinfo.php,404,123,sqlmap/1.0,8,phpinfo:high;ua_sqlmap:low
```
</details>

#### ⏳ Barra de progreso

Durante el procesamiento, se muestra una barra de progreso interactiva:

```bash
ℹ️ Procesando logs...
[██████████--------] 50%  12345/24690 líneas  1234.5 l/s  ETA: 00:01:30

| Elemento | Descripción |
|:---------|:------------|
| **Barra** | Progreso visual |
| **Porcentaje** | Avance actual |
| **Líneas** | Procesadas/Total |
| **Velocidad** | Líneas por segundo |
| **ETA** | Tiempo restante estimado |
```


‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡
Pendiente de revisar hacia abajo
‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡

## 🔮 Roadmap y mejoras propuestas

### Análisis avanzado
- [ ] Agrupación por IP con score acumulado
  - CSV con IPs ordenadas por score total
  - Conteo de incidencias por IP
  - Integración con fail2ban
  
- [ ] Análisis de bodies de peticiones
  - Soporte para logs extendidos con payload
  - Detección de shells y backdoors
  - Análisis de contenido multipart

### Usabilidad y automatización
- [ ] Opciones de línea de comandos
  - Modo `--quiet` para cron jobs
  - `--input` para especificar archivo
  - `--threshold` para ajustar UMBRAL_SCORE
  
- [ ] Separación por método HTTP
  - Archivos individuales para PUT/DELETE
  - Tratamiento específico por método
  - Configuración de scores por método

### Integración y extensibilidad
- [ ] Integración con sistemas de seguridad
  - Export para fail2ban
  - Reglas para ModSecurity
  - Alertas a SIEM
  
- [ ] Patrones actualizables
  - Importar desde JSON/YAML
  - Feeds de amenazas externos
  - Versionado de reglas

### Visualización y reporting
- [ ] Dashboard web local
  - Gráficos de actividad
  - Mapa de IPs
  - Timeline de eventos
  
- [ ] Reportes periódicos
  - Resumen diario/semanal
  - Estadísticas por IP/patrón
  - Tendencias y anomalías

## ❗ Resolución de problemas

### 🎯 Ajuste de falsos positivos

```python
# Aumentar umbral general
UMBRAL_SCORE = 8  # (default: 5)

# Añadir IPs a lista blanca
LISTA_BLANCA_IPS.extend([
    '192.168.1.0/24',  # Red local
    '10.0.0.X',        # Rango con wildcard
    '172.16.1.100'     # IP específica
])

# Ajustar peso de POST
PESO_POST = 3  # (default: 5)
```

### 📈 Procesamiento de logs grandes

```bash
# 1. Dividir log en partes manejables
split -l 1000000 access.log "access.log.part_"

# 2. Procesar cada parte
for parte in access.log.part_*; do
    echo "Procesando $parte..."
    python3 filtrador_logs_4_multigenerico.py "$parte"
done

# 3. Combinar resultados (opcional)
cat accesslog_filtrado_GET_*.md > combined_GET.md
cat accesslog_filtrado_POST_*.md > combined_POST.md
```

## 📝 Consideraciones finales

### ✅ Buenas prácticas

| Aspecto | Recomendaciones |
|:--------|:----------------|
| **Verificación** | • Revisar manualmente antes de bloquear IPs<br>• Validar patrones contra logs conocidos<br>• Documentar falsos positivos |
| **Backups** | • Mantener copias de logs originales<br>• Respaldar configuraciones<br>• Versionar modificaciones de patrones |
| **Correlación** | • Analizar `error.log` en paralelo<br>• Revisar logs de ModSecurity<br>• Correlacionar con logs de WAF |
| **Monitoreo** | • Verificar rendimiento periódicamente<br>• Ajustar umbrales según necesidad<br>• Actualizar lista blanca |

### 🔒 Privacidad y seguridad

| Aspecto | Guía |
|:--------|:-----|
| **Datos sensibles** | • No incluir POST data en reportes<br>• Filtrar información personal<br>• Anonimizar IPs si es necesario |
| **Acceso** | • Restringir acceso a reportes<br>• Usar permisos adecuados<br>• Implementar logs de auditoría |
| **Retención** | • Seguir política de retención<br>• Rotar logs regularmente<br>• Eliminar datos antiguos |

### 🔄 Mantenimiento rutinario


### 📋 Información del proyecto

**Versión:** 1.0.0  
**Actualizado:** 16/10/2025  
🧾 Licencia: **Copyright**
👨‍💻 Autor: **@Jorge P.V.**

> ⚠️ **Nota importante:** Esta herramienta es un apoyo para auditorías y revisión de logs. No sustituye un IDS/WAF ni una política de respuesta automática. Revise siempre manualmente antes de aplicar bloqueos automáticos.
