#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Archivo: filtrador_logs_4_multigenerico.py

Analizador/filtrado de access.log (Apache) con:
 - separación de resultados GET / POST (Markdown + CSV)
 - lista blanca de IPs / CIDR / wildcards 'X'
 - umbral configurable (UMBRAL_SCORE)
 - barra de progreso manual (sin dependencias)
 - mensajes con colores ANSI y emojis
 - clasificación de peticiones (ENTRANTE_OK, ENTRANTE_PELIGROSO, SALIENTE_PELIGROSO, DESCARTADA)
 - nombres y comentarios en castellano para facilitar mantenimiento
"""

import re
import csv
import time
import os
import sys
from datetime import datetime
from urllib.parse import unquote, unquote_plus
import ipaddress

# ---------------- CONFIGURACIÓN (ajusta según tu entorno) ----------------

# Nombre del fichero y ruta (ajusta si tu access.log está en otra ubicación)
RUTA_LOG = 'access.log'

# Fecha para nombres de archivo
FECHA = datetime.now().strftime('%Y%m%d')

# Archivos de salida por método (Markdown + CSV)
OUT_MD_GET = f'accesslog_filtrado_GET_{FECHA}.md'
OUT_MD_POST = f'accesslog_filtrado_POST_{FECHA}.md'
OUT_CSV_GET = f'accesslog_filtrado_GET_{FECHA}.csv'
OUT_CSV_POST = f'accesslog_filtrado_POST_{FECHA}.csv'

# Peso extra para peticiones POST (suelen llevar payload)
PESO_POST = 5

# Umbral mínimo de score para incluir una entrada en los listados
UMBRAL_SCORE = 5

# Lista blanca de IPs/rangos para IGNORAR en los listados filtrados.
# Soporta CIDR ('10.0.0.0/8'), wildcards con 'X' ('172.18.0.X') e IP exacta.
LISTA_BLANCA_IPS = [
    '127.0.0.1',
    '172.18.0.X',
    '172.18.X.X',
    # '10.0.0.0/8',
]

# IPS_SERVIDOR: direcciones conocidas del propio servidor o de la red interna.
# Usamos esto para detectar si una entrada en logs podría ser "saliente".
# Añade aquí tu/s IP pública/s o subredes internas según proceda.
IPS_SERVIDOR = [
    # '203.0.113.10',
    # '192.168.1.X',
]

# Patrones generales (nombre, regex, etiqueta)
PATRONES = [
    ("phpunit_eval-stdin", r'/vendor/phpunit/.*/eval-stdin\.php', 'critical'),
    ("androxgh0st_marker", r'0x\[\]=androxgh0st', 'critical'),
    ("phpinfo", r'(?i)/phpinfo(?:\.php)?\b', 'high'),
    ("env_file", r'(?i)/(?:\.env|\.env\.backup)\b', 'high'),
    ("aws_credentials", r'(?i)/(?:aws|credentials|\.aws/credentials)\b', 'high'),
    ("git_probe", r'(?i)/\.git(?:/|/HEAD|\b)', 'high'),
    ("etc_passwd", r'(?i)/etc/passwd', 'critical'),
    ("proc_self", r'(?i)/proc/self/environ', 'critical'),
    ("lfi_traversal", r'(\.\./|\.\.\\){2,}', 'critical'),
    ("rfi_phpwrapper", r'(?i)(php://input|data:text\/plain;|expect:)', 'critical'),
    ("sql_union_select", r'(?i)\bunion\b.+\bselect\b', 'high'),
    ("sql_tautology", r"(?i)('|\")\s*or\s*1=1", 'high'),
    ("xss_script", r'(?i)<script\b|%3Cscript', 'medium'),
    ("cmd_wget_curl", r'(?i)(wget|curl|bash -i|/bin/sh|-exec|-chmod)', 'high'),
    ("system_eval", r'(?i)\b(eval|exec|system|passthru|shell_exec)\b', 'high'),
    ("null_byte", r'%00|\x00', 'high'),
    ("long_uri", r'.{200,}', 'medium'),
    ("scanner_sqlmap", r'(?i)sqlmap', 'high'),
    ("scanner_nikto", r'(?i)nikto', 'medium'),
    ("scanner_masscan", r'(?i)masscan', 'medium'),
    ("python_requests", r'(?i)python-requests', 'low'),
    ("xmlrpc", r'(?i)/xmlrpc\.php', 'medium'),
    ("wp_login", r'(?i)/wp-login\.php', 'medium'),
    ("base64_blob", r'(?i)(?:[A-Za-z0-9+/]{100,}={0,2})', 'high'),
    ("eval_in_query", r'(?i)\beval\(|\bassert\(', 'high'),
]

# Patrones que solo se revisan cuando el método es POST (payloads)
PATRONES_SOLO_POST = [
    (r'(?i)(\bpassword\b|\bpasswd\b|\bcredentials\b).*=.*', 'high'),
    (r'(?i)Content-Disposition:.*filename=.*\.(php|phtml|phar)', 'critical'),
    (r'(?i)\b(class|__wakeup|__destruct|__construct)\b', 'high'),
    (r'(?i)\\x00|%00', 'high'),
    (r'(?i)base64_decode\(|eval\(|system\(|exec\(', 'critical'),
    (r'(?i)\bselect\b.*\bfrom\b|\binsert\b.*\binto\b', 'high'),
]

# Puntos por etiqueta de severidad
SEVERITY_PUNTOS = {
    'critical': 10,
    'high': 6,
    'medium': 3,
    'low': 1,
}

# Métodos HTTP que consideramos sospechosos si aparecen
METODOS_SOSPECHOSOS = {
    'PUT': 'medium',
    'DELETE': 'medium',
    'PROPFIND': 'high',
    'TRACE': 'high',
    'CONNECT': 'high',
}

# Fragmentos sospechosos en User-Agent
UA_SOSPECHOSOS = ['sqlmap', 'nikto', 'masscan', 'nmap', 'acunetix', 'nessus', 'curl', 'wget', 'python-requests', 'libwww-perl', 'ZmEu']

# ---------------- COLORES E ICONOS (ANSI) ----------------
ANSI_RESET = '\033[0m'
ANSI_BOLD = '\033[1m'
ANSI_RED = '\033[91m'
ANSI_GREEN = '\033[92m'
ANSI_YELLOW = '\033[93m'
ANSI_CYAN = '\033[96m'
ICONO_OK = '✅'
ICONO_WARN = '⚠️'
ICONO_INFO = 'ℹ️'
ICONO_FIRE = '🔥'
ICONO_SAFE = '🟢'
ICONO_SUS = '🟠'
ICONO_DANGER = '🔴'
ICONO_SKIP = '⚪'

# ---------------- REGEX PARA PARSEAR el access.log (Combined log format) ----------------
LOG_RE = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+"(?P<request>[^"]+)"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\S+)(?:\s+"(?P<referer>[^"]*)"\s+"(?P<agent>[^"]*)")?'
)

# ---------------- FUNCIONES AUXILIARES (EN CASTELLANO) ----------------

def compilar_patrones():
    """Compila patrones generales y patrones solo-POST para eficiencia."""
    gener = [(nombre, re.compile(pat), etiqueta) for nombre, pat, etiqueta in PATRONES]
    post = [(re.compile(p), etiqueta) for p, etiqueta in PATRONES_SOLO_POST]
    return gener, post

def puntos_por_etiqueta(etiqueta):
    """Devuelve puntos para una etiqueta de severidad."""
    return SEVERITY_PUNTOS.get(etiqueta, 0)

def parsear_request(request_field):
    """Extrae metodo, ruta cruda, ruta decodificada y protocolo del campo request."""
    partes = request_field.split()
    if len(partes) >= 2:
        metodo = partes[0]
        ruta_cruda = partes[1]
        protocolo = partes[2] if len(partes) >= 3 else ''
        # Decodificamos dos veces para atrapar ofuscaciones (ej. %252e)
        ruta_dec = unquote_plus(unquote(ruta_cruda))
        return metodo, ruta_cruda, ruta_dec, protocolo
    return None, None, None, None

def detectar_ua_sospechosa(agent):
    """Detecta fragmentos sospechosos en user-agent."""
    if not agent:
        return None
    ag = agent.lower()
    for frag in UA_SOSPECHOSOS:
        if frag.lower() in ag:
            return frag
    return None

def ip_en_lista_blanca(ip_str, lista_blanca):
    """
    Comprueba si una IP pertenece a la lista blanca.
    Soporta CIDR, wildcards 'X' y comparación exacta.
    """
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except Exception:
        return False

    for entry in lista_blanca:
        entry = entry.strip()
        if '/' in entry:
            try:
                net = ipaddress.ip_network(entry, strict=False)
                if ip_obj in net:
                    return True
            except Exception:
                pass
        elif 'X' in entry.upper():
            # '172.18.X.X' -> ^172\.18\.\d{1,3}\.\d{1,3}$
            regex_pat = '^' + re.escape(entry).replace('\\X', r'\d{1,3}').replace('X', r'\d{1,3}') + '$'
            if re.match(regex_pat, ip_str):
                return True
        else:
            if ip_str == entry:
                return True
    return False

def es_ip_servidor(ip_str, ips_servidor):
    """Comprueba si la IP pertenece a la lista de IPs del propio servidor (IPS_SERVIDOR)."""
    return ip_en_lista_blanca(ip_str, ips_servidor)

def escanear_patrones(texto, patrones_compilados):
    """Escanea texto con patrones generales compilados."""
    hallazgos = []
    for nombre, cregex, etiqueta in patrones_compilados:
        try:
            if cregex.search(texto):
                hallazgos.append((nombre, etiqueta))
        except re.error:
            continue
    return hallazgos

def escanear_post_solo(texto, patrones_post_compilados):
    """Escanea con patrones específicos para POST."""
    hallazgos = []
    for cregex, etiqueta in patrones_post_compilados:
        try:
            if cregex.search(texto):
                hallazgos.append((cregex.pattern, etiqueta))
        except re.error:
            continue
    return hallazgos

# ---------------- CLASIFICACIÓN DE PETICIONES ----------------

# Diccionario que define la etiqueta, emoji y color por clasificación
CLASIFICACIONES = {
    'ENTRANTE_OK':   {'emoji': ICONO_SAFE, 'color': ANSI_GREEN, 'desc': 'ENTRANTE_OK', 'priority': 1},
    'ENTRANTE_PELIGROSO': {'emoji': ICONO_SUS, 'color': ANSI_YELLOW, 'desc': 'ENTRANTE_PELIGROSO', 'priority': 2},
    'SALIENTE_PELIGROSO': {'emoji': ICONO_DANGER, 'color': ANSI_RED, 'desc': 'SALIENTE_PELIGROSO', 'priority': 3},
    'DESCARTADA':    {'emoji': ICONO_SKIP, 'color': ANSI_CYAN, 'desc': 'DESCARTADA', 'priority': 0},
}

def clasificar_peticion(ip_origen, codigo_http, metodo, score):
    """
    Clasifica una petición en:
      - ENTRANTE_OK (🟢): entrante con 404/403/400 o bajo score
      - ENTRANTE_PELIGROSO (🟠): entrante con 200/500 o score alto (y POST)
      - SALIENTE_PELIGROSO (🔴): si la IP de origen coincide con IPS_SERVIDOR -> indicio de petición saliente
      - DESCARTADA (⚪): IP en lista blanca o score < UMBRAL_SCORE
    Devuelve (clave_clasificacion, emoji, color, texto_desc)
    """
    # Si IP en lista blanca -> DESCARTADA
    if ip_en_lista_blanca(ip_origen, LISTA_BLANCA_IPS):
        c = CLASIFICACIONES['DESCARTADA']
        return 'DESCARTADA', c['emoji'], c['color'], c['desc']

    # Si la IP es propia del servidor, marcamos como SALIENTE_PELIGROSO si el resultado sugiere riesgo
    if es_ip_servidor(ip_origen, IPS_SERVIDOR):
        # si el score es significativo o el código es 200/500 consideramos peligro saliente
        try:
            codigo = int(codigo_http)
        except Exception:
            codigo = 0
        if score >= UMBRAL_SCORE or codigo in (200, 500):
            c = CLASIFICACIONES['SALIENTE_PELIGROSO']
            return 'SALIENTE_PELIGROSO', c['emoji'], c['color'], c['desc']
        else:
            c = CLASIFICACIONES['DESCARTADA']
            return 'DESCARTADA', c['emoji'], c['color'], c['desc']

    # Petición entrante normal (no server IP)
    try:
        codigo = int(codigo_http)
    except Exception:
        codigo = 0

    # Entrante OK: códigos 404, 403, 400 y score bajo
    if codigo in (400, 403, 404) and score < UMBRAL_SCORE + 4:
        c = CLASIFICACIONES['ENTRANTE_OK']
        return 'ENTRANTE_OK', c['emoji'], c['color'], c['desc']

    # Entrante peligroso: 200 o 500 o score alto (especialmente POST)
    if codigo in (200, 500):
        c = CLASIFICACIONES['ENTRANTE_PELIGROSO']
        return 'ENTRANTE_PELIGROSO', c['emoji'], c['color'], c['desc']

    if score >= UMBRAL_SCORE:
        # Si el método es POST y score relevante -> peligro
        if metodo and metodo.upper() == 'POST':
            c = CLASIFICACIONES['ENTRANTE_PELIGROSO']
            return 'ENTRANTE_PELIGROSO', c['emoji'], c['color'], c['desc']
        # Sino, entrante ok si código no es 200/500
        c = CLASIFICACIONES['ENTRANTE_OK']
        return 'ENTRANTE_OK', c['emoji'], c['color'], c['desc']

    # Por defecto, descartada
    c = CLASIFICACIONES['DESCARTADA']
    return 'DESCARTADA', c['emoji'], c['color'], c['desc']

# ---------------- BARRA DE PROGRESO (manual) ----------------

def contar_lineas_archivo(ruta):
    """Cuenta el número de líneas del archivo (necesario para la barra)."""
    total = 0
    with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
        for _ in f:
            total += 1
    return total

def mostrar_progreso_manual(procesadas, total, inicio_t, ancho_barra=30):
    """Muestra barra con porcentaje, líneas procesadas, velocidad y ETA."""
    if total == 0:
        return
    ahora = time.time()
    elapsed = ahora - inicio_t if inicio_t else 0.0001
    velocidad = procesadas / elapsed if elapsed > 0 else 0
    porcentaje = procesadas / total
    bloques = int(porcentaje * ancho_barra)
    barra = '█' * bloques + '-' * (ancho_barra - bloques)
    porcentaje_int = int(porcentaje * 100)
    restante = total - procesadas
    eta_seconds = int(restante / velocidad) if velocidad > 0 else 0
    eta_str = time.strftime('%H:%M:%S', time.gmtime(eta_seconds))
    linea = (f"\r{ANSI_CYAN}{ICONO_INFO} Procesando:{ANSI_RESET} [{barra}] {porcentaje_int:3d}%  "
             f"{procesadas}/{total} líneas  {velocidad:6.1f} l/s  ETA: {eta_str} ")
    sys.stdout.write(linea)
    sys.stdout.flush()

# ---------------- PROCESO PRINCIPAL ----------------

def main():
    # Comprobación básica de existencia del fichero
    if not os.path.isfile(RUTA_LOG):
        print(f"{ANSI_RED}{ICONO_WARN} ERROR:{ANSI_RESET} No puedo encontrar el fichero de logs '{RUTA_LOG}'. Comprueba la ruta.")
        return

    print(f"{ANSI_GREEN}{ICONO_OK} Iniciando filtrado y clasificación de logs{ANSI_RESET}")
    total_lineas = contar_lineas_archivo(RUTA_LOG)
    print(f"{ANSI_YELLOW}{ICONO_INFO} Total de líneas a procesar: {total_lineas}{ANSI_RESET}")

    patrones_compilados, patrones_post_compilados = compilar_patrones()

    inicio_t = time.time()
    procesadas = 0

    # Abrimos ficheros de salida
    with open(OUT_MD_GET, 'w', encoding='utf-8') as md_get, \
         open(OUT_MD_POST, 'w', encoding='utf-8') as md_post, \
         open(OUT_CSV_GET, 'w', newline='', encoding='utf-8') as csv_get, \
         open(OUT_CSV_POST, 'w', newline='', encoding='utf-8') as csv_post, \
         open(RUTA_LOG, 'r', encoding='utf-8', errors='ignore') as fh:

        writer_get = csv.writer(csv_get)
        writer_post = csv.writer(csv_post)
        writer_get.writerow(['ip', 'time', 'method', 'ruta_cruda', 'ruta_decodificada', 'status', 'size', 'agent', 'score', 'matches', 'clasificacion'])
        writer_post.writerow(['ip', 'time', 'method', 'ruta_cruda', 'ruta_decodificada', 'status', 'size', 'agent', 'score', 'matches', 'clasificacion'])

        # Cabeceras Markdown
        md_get.write('# Filtrado de logs - POSIBLES INCIDENCIAS (GET)\n\n')
        md_get.write(f'Generado: {datetime.now().isoformat()}\n\n')
        md_get.write('```console\n')
        md_post.write('# Filtrado de logs - POSIBLES INCIDENCIAS (POST)\n\n')
        md_post.write(f'Generado: {datetime.now().isoformat()}\n\n')
        md_post.write('```console\n')

        # Procesamiento línea a línea
        for linea in fh:
            procesadas += 1
            linea_str = linea.rstrip('\n')
            m = LOG_RE.search(linea_str)

            if m:
                ip = m.group('ip')
                time_field = m.group('time')
                request_field = m.group('request')
                status = m.group('status')
                size = m.group('size')
                referer = m.group('referer') if 'referer' in m.groupdict() else ''
                agent = m.group('agent') if 'agent' in m.groupdict() else ''

                metodo, ruta_cruda, ruta_decodificada, proto = parsear_request(request_field)
                if not metodo:
                    continue  # no hemos podido parsear correctamente

                # Si IP en lista blanca: clasificamos como DESCARTADA y no la incluimos en archivos
                if ip_en_lista_blanca(ip, LISTA_BLANCA_IPS):
                    clas_key, emoji, color, desc = 'DESCARTADA', CLASIFICACIONES['DESCARTADA']['emoji'], CLASIFICACIONES['DESCARTADA']['color'], CLASIFICACIONES['DESCARTADA']['desc']
                    # No escribir en listados filtrados
                else:
                    # Preparar texto a escanear (ruta cruda + decodificada + UA + request completo)
                    texto_a_escanear = ' '.join(filter(None, [ruta_cruda, ruta_decodificada, agent, request_field, linea_str]))

                    # Escaneo general
                    hallazgos = escanear_patrones(texto_a_escanear, patrones_compilados)
                    score = sum(puntos_por_etiqueta(et) for _, et in hallazgos)

                    # Si es POST, escanear patrones exclusivos y añadir peso POST
                    if metodo.upper() == 'POST':
                        hallazgos_post = escanear_post_solo(texto_a_escanear, patrones_post_compilados)
                        for _, etiqueta in hallazgos_post:
                            score += puntos_por_etiqueta(etiqueta)
                            hallazgos.append(("POST_PATTERN", etiqueta))
                        score += PESO_POST

                    # Métodos sospechosos
                    if metodo.upper() in METODOS_SOSPECHOSOS:
                        etiqueta_met = METODOS_SOSPECHOSOS[metodo.upper()]
                        score += puntos_por_etiqueta(etiqueta_met)

                    # UA sospechoso
                    frag_ua = detectar_ua_sospechosa(agent)
                    if frag_ua:
                        score += 3
                        hallazgos.append((f'ua_{frag_ua}', 'low'))

                    # Heurística URIs muy largas
                    if ruta_decodificada and len(ruta_decodificada) > 300:
                        hallazgos.append(('uri_very_long', 'medium'))
                        score += puntos_por_etiqueta('medium')

                    # Clasificar (según IP, código http, metodo y score)
                    clas_key, emoji, color, desc = clasificar_peticion(ip, status, metodo, score)

                    # Si la clasificación es DESCARTADA -> no escribir en archivos
                    if clas_key == 'DESCARTADA':
                        # seguimos (no añadimos)
                        pass
                    else:
                        # Preparar matches en texto
                        matches_str = ';'.join(f'{n}:{t}' for n, t in hallazgos) if hallazgos else ''

                        # Bloque detallado para Markdown
                        bloque_info = (f'# {emoji} {desc} - Score={score} - IP={ip}\n{linea_str}\n'
                                       f'  - Método: {metodo}\n'
                                       f'  - Ruta (raw): {ruta_cruda}\n'
                                       f'  - Ruta (decoded): {ruta_decodificada}\n'
                                       f'  - Código HTTP: {status}\n'
                                       f'  - Tamaño respuesta: {size}\n'
                                       f'  - User-Agent: {agent}\n'
                                       f'  - Clasificación: {emoji} {desc}\n'
                                       f'  - Matches:\n')
                        for nombre, etiqueta in hallazgos:
                            bloque_info += f'    - {nombre} (tag={etiqueta})\n'
                        if frag_ua:
                            bloque_info += f'  - Detected UA fragment: {frag_ua}\n'
                        bloque_info += '\n'

                        # Escribir en fichero correspondiente según método (GET/POST). Otros métodos los guardamos en POST por defecto.
                        if metodo.upper() == 'GET':
                            md_get.write(bloque_info)
                            writer_get.writerow([ip, time_field, metodo, ruta_cruda, ruta_decodificada, status, size, agent, score, matches_str, desc])
                        else:
                            md_post.write(bloque_info)
                            writer_post.writerow([ip, time_field, metodo, ruta_cruda, ruta_decodificada, status, size, agent, score, matches_str, desc])

            else:
                # Línea no parseable: intentar búsqueda rápida por patrones en toda la línea
                try:
                    linea_decod = unquote_plus(unquote(linea_str))
                except Exception:
                    linea_decod = linea_str
                hallazgos = escanear_patrones(linea_decod, patrones_compilados)
                score = sum(puntos_por_etiqueta(et) for _, et in hallazgos)
                # Clasificar en ausencia de IP y código: por defecto lo dejamos en DESCARTADA
                clas_key, emoji, color, desc = ('DESCARTADA', CLASIFICACIONES['DESCARTADA']['emoji'], CLASIFICACIONES['DESCARTADA']['color'], CLASIFICACIONES['DESCARTADA']['desc'])
                if score >= UMBRAL_SCORE and hallazgos:
                    bloque = f'# {ICONO_SUS} {desc} - Score={score}\n{linea_str}\n  - Matches:\n'
                    for nombre, etiqueta in hallazgos:
                        bloque += f'    - {nombre} (tag={etiqueta})\n'
                    bloque += '\n'
                    md_get.write(bloque)  # escribimos en GET por defecto
                    writer_get.writerow(['-', '-', '-', '-', '-', '-', '-', '-', score, ';'.join(f'{n}:{t}' for n,t in hallazgos), desc])

            # Actualizar barra de progreso cada X líneas
            if procesadas % 5 == 0 or procesadas == total_lineas:
                mostrar_progreso_manual(procesadas, total_lineas, inicio_t)

        # Cerrar bloques Markdown
        md_get.write('```\n')
        md_post.write('```\n')

    # Resumen final
    tiempo_total = time.time() - inicio_t
    if tiempo_total < 1:
        tiempo_total = 1
    velocidad_final = total_lineas / tiempo_total if total_lineas > 0 else 0
    print()  # nueva línea tras la barra
    print(f"{ANSI_GREEN}{ICONO_OK} Filtrado y clasificación completados.{ANSI_RESET} Líneas procesadas: {total_lineas}. Tiempo: {time.strftime('%H:%M:%S', time.gmtime(tiempo_total))}. Velocidad media: {velocidad_final:.1f} l/s")
    print(f"  - Resultados GET:  {OUT_MD_GET}  (CSV: {OUT_CSV_GET})")
    print(f"  - Resultados POST: {OUT_MD_POST}  (CSV: {OUT_CSV_POST})")
    print(f"  - Umbral (UMBRAL_SCORE): {UMBRAL_SCORE}")
    print(f"  - Lista blanca IPs: {LISTA_BLANCA_IPS}")
    print(f"  - IPS servidor (para detectar salientes): {IPS_SERVIDOR}")

if __name__ == '__main__':
    main()
