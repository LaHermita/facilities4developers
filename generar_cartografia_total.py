#!/usr/bin/env python3
"""
Generador de cartografía total de proyectos LH

Versión: 2.8.1

Descripción:
Genera cartografia_lh_total.png y cartografia_lh_total.md a partir de los mapas MAP - *.md, con masonry global por bloque y etiqueta de ruta.

Dependencias:
- argparse
- fnmatch
- math
- os
- re
- sys
- datetime
- Pillow

Uso:
python generar_cartografia_total.py [--raiz RUTA] [--salida IMAGEN.png]

Ejemplo:
python generar_cartografia_total.py --salida cartografia_lh_total.png
"""
import argparse
import fnmatch
import math
import os
import re
import sys
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

VERSION = "2.8.1"

BLOQUE_ACTIVOS = "Proyectos activos"
BLOQUE_PAUSADOS = "Proyectos pausados"

RUTAS_ESCANEO = [
    {"titulo": "Webs LH", "ruta": "/home/jparra/SynologyDrive/zhtdocslh"},
    {"titulo": "Devel Agents Mochila", "ruta": "/media/jparra/Mochila/Desarrollo/Agentes&MCPs"},
    {"titulo": "Devels Python Mochila", "ruta": "/media/jparra/Mochila/Desarrollo/Python"},
]

RUTAS_PAUSADAS = [
    {"titulo": "Devels Python pausados", "ruta": "/media/jparra/Mochila/Desarrollo_Pausado/Python"},
]

BLOQUES_RUTAS = (
    (BLOQUE_ACTIVOS, RUTAS_ESCANEO),
    (BLOQUE_PAUSADOS, RUTAS_PAUSADAS),
)

PATRON_MAPA = re.compile(r"^MAP - .+\.md$", re.IGNORECASE)
PATRON_CV = re.compile(r"_cv\d+", re.IGNORECASE)
PROFUNDIDAD_MAXIMA = 1
DIRS_RUIDO = {
    "node_modules", ".git", ".opencode", "__pycache__", "site-packages",
    ".entorno", "vendor", ".venv", "venv", "dist", "build", ".cache",
    ".mypy_cache", ".pytest_cache", "9_documentacion_web_lh",
}

ARCHIVOS_EXCLUIDOS = [
]

ETIQUETAS_TIPO = {
    "proyectos": "Proyectos",
    "snippets": "Snippets",
    "documentacion": "Documentación",
}

RANGOS_EMOJI = (
    (0x1F000, 0x1FAFF), (0x2600, 0x27BF), (0x2B00, 0x2BFF),
    (0x1F1E6, 0x1F1FF), (0xFE00, 0xFE0F), (0x2190, 0x21FF),
)
CARACTERES_ESPECIALES = {0x200D, 0x20E3}

FONDO = (241, 237, 246)
SOMBRA = (212, 203, 222)
TARJETA = (252, 250, 254)
BORDE = (212, 203, 220)
TITULO = (44, 30, 54)
TEXTO = (78, 64, 86)
TENUE = (110, 96, 118)
ENCABEZADO = (74, 46, 88)
SUBTITULO = (100, 82, 110)
ACENTOS = {
    "proyectos": (112, 62, 112),
    "snippets": (150, 104, 42),
    "documentacion": (94, 80, 72),
}
TINTES = {
    "proyectos": (238, 226, 239),
    "snippets": (245, 235, 218),
    "documentacion": (236, 231, 226),
}
ACENTO_SIN_MANIFIESTO = (154, 86, 32)
TINTE_SIN_MANIFIESTO = (250, 235, 219)
ACENTO_PAUSADO = (108, 98, 112)
TINTE_PAUSADO = (233, 228, 235)
ESTILOS_BLOQUE = {
    BLOQUE_ACTIVOS: {"acento": ACENTOS["proyectos"], "tinte": TINTES["proyectos"]},
    BLOQUE_PAUSADOS: {"acento": ACENTO_PAUSADO, "tinte": TINTE_PAUSADO},
}

FUENTES_CANDIDATAS = {
    "normal": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ],
    "negrita": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ],
    "mono": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ],
}


def es_emoji(caracter):
    codigo = ord(caracter)
    if codigo in CARACTERES_ESPECIALES:
        return True
    return any(inicio <= codigo <= fin for inicio, fin in RANGOS_EMOJI)


def quitar_emoji(texto):
    limpio = "".join(c for c in texto if not es_emoji(c))
    return re.sub(r"\s{2,}", " ", limpio).strip()


def cargar_fuente(estilo, tam):
    for ruta in FUENTES_CANDIDATAS[estilo]:
        if os.path.isfile(ruta):
            try:
                return ImageFont.truetype(ruta, tam)
            except OSError:
                continue
    return ImageFont.load_default()


def leer_frontmatter(texto):
    datos = {}
    if not texto.startswith("---"):
        return datos
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return datos
    for linea in partes[1].splitlines():
        if ":" in linea:
            clave, valor = linea.split(":", 1)
            datos[clave.strip()] = valor.strip()
    return datos


def extraer_resumen(texto, frontmatter):
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if re.match(r"^>\s*\[!summary\]", linea, re.IGNORECASE):
            resumen = []
            for siguiente in lineas[i + 1:]:
                if not siguiente.startswith(">"):
                    break
                resumen.append(siguiente.lstrip("> ").strip())
            if resumen:
                return quitar_emoji(" ".join(resumen).strip())
    return quitar_emoji(frontmatter.get("descripcion", ""))


def extraer_titulo(texto, ruta):
    for linea in texto.splitlines():
        if linea.startswith("# "):
            return quitar_emoji(linea[2:].strip())
    return os.path.splitext(os.path.basename(ruta))[0]


def clasificar_tipo(frontmatter, ruta):
    tipo = frontmatter.get("tipo", "").strip().lower()
    nombre = os.path.basename(ruta).lower()
    if "snippet" in tipo or "snippet" in nombre:
        return "snippets"
    if "proyecto" in tipo:
        return "proyectos"
    if any(clave in tipo for clave in ("documenta", "indice", "índice")) or \
       any(clave in nombre for clave in ("documentacion", "sesion", "indice", "índice")):
        return "documentacion"
    return "proyectos"


def contar_entradas(texto):
    entradas = len(re.findall(r"^- .*\[.*\]\(", texto, flags=re.MULTILINE))
    if entradas:
        return entradas, "proyectos"
    filas = 0
    for linea in texto.splitlines():
        if linea.startswith("|") and not re.match(r"^\|[\s:|-]+\|?\s*$", linea):
            filas += 1
    return max(filas - 1, 0), "documentos"


def extraer_stacks(texto):
    stacks = []
    for coincidencia in re.findall(r"^[ \t]*>\s*Stack:[ \t]*(.+)$", texto, flags=re.MULTILINE):
        valor = quitar_emoji(coincidencia).strip()
        if valor and valor not in stacks:
            stacks.append(valor)
    return stacks


def tiene_manifest(base, ubicacion, nombre):
    carpeta = (ubicacion or nombre).strip().strip("/")
    if not carpeta or os.path.isabs(carpeta):
        return False
    ruta = os.path.normpath(os.path.join(base, carpeta))
    return os.path.isfile(os.path.join(ruta, "manifest.json"))


def extraer_componentes(texto, base, comprobar_manifest=True):
    componentes = []
    actual = None
    for linea in texto.splitlines():
        if linea.startswith("- "):
            coincidencia = re.match(r"^- .*?\[([^\]]+)\]\([^)]*\)", linea)
            if coincidencia:
                nombre = quitar_emoji(coincidencia.group(1)).strip()
                actual = {"nombre": nombre, "ubicacion": ""} if nombre else None
                if actual:
                    componentes.append(actual)
            else:
                actual = None
            continue
        if actual is None or actual["ubicacion"]:
            continue
        coincidencia = re.match(r"^[ \t]*>\s*Ubicaci[oó]n:\s*(.*)$", linea, re.IGNORECASE)
        if coincidencia:
            actual["ubicacion"] = coincidencia.group(1).strip().strip("/")
    for componente in componentes:
        componente["sin_manifest"] = comprobar_manifest and not tiene_manifest(
            base, componente["ubicacion"], componente["nombre"]
        )
    return componentes


def analizar_mapa(ruta, raiz, grupo="", bloque=""):
    with open(ruta, encoding="utf-8", errors="replace") as archivo:
        texto = archivo.read()
    frontmatter = leer_frontmatter(texto)
    entradas, etiqueta_entradas = contar_entradas(texto)
    tipo = clasificar_tipo(frontmatter, ruta)
    if tipo == "snippets":
        etiqueta_entradas = "snippets"
    ruta_relativa = os.path.relpath(ruta, raiz).replace(os.sep, "/")
    return {
        "ruta": ruta,
        "grupo": grupo,
        "bloque": bloque,
        "ruta_relativa": ruta_relativa,
        "zona": ruta_relativa.split("/")[0],
        "titulo": extraer_titulo(texto, ruta),
        "resumen": extraer_resumen(texto, frontmatter),
        "tipo": tipo,
        "version": frontmatter.get("version", ""),
        "fecha": frontmatter.get("fecha", ""),
        "estado": frontmatter.get("estado", ""),
        "entradas": entradas,
        "etiqueta_entradas": etiqueta_entradas,
        "stacks": extraer_stacks(texto),
        "componentes": extraer_componentes(texto, os.path.dirname(ruta), tipo == "proyectos"),
    }


def buscar_mapas(raiz, incluir_ruido=False):
    encontrados = []
    for directorio, subcarpetas, archivos in os.walk(raiz):
        if not incluir_ruido:
            subcarpetas[:] = [s for s in subcarpetas if s not in DIRS_RUIDO and not s.startswith(".")]
        for nombre in archivos:
            if PATRON_MAPA.match(nombre):
                encontrados.append(os.path.join(directorio, nombre))
    return sorted(encontrados)


def esta_excluido(ruta_relativa):
    nombre = os.path.basename(ruta_relativa)
    for patron in ARCHIVOS_EXCLUIDOS:
        if fnmatch.fnmatch(ruta_relativa, patron) or fnmatch.fnmatch(nombre, patron):
            return True
    return False


def filtrar_mapas(rutas, raiz, incluir_cv, profundidad_maxima):
    incluidas = []
    excluidos = []
    for ruta in rutas:
        ruta_relativa = os.path.relpath(ruta, raiz).replace(os.sep, "/")
        nivel = ruta_relativa.count("/")
        if esta_excluido(ruta_relativa):
            excluidos.append((ruta_relativa, "lista interna"))
            continue
        if nivel > profundidad_maxima:
            excluidos.append((ruta_relativa, f"subcarpeta (nivel {nivel})"))
            continue
        if not incluir_cv and PATRON_CV.search(ruta_relativa):
            excluidos.append((ruta_relativa, "variante _cv"))
            continue
        incluidas.append(ruta)
    return incluidas, excluidos


def escanear_rutas(config, incluir_ruido, incluir_cv, profundidad_maxima):
    mapas = []
    excluidos = []
    vistos = set()
    for entrada in config:
        titulo = entrada.get("titulo") or os.path.basename(entrada["ruta"].rstrip("/"))
        bloque = entrada.get("bloque", "")
        raiz = os.path.abspath(os.path.expanduser(entrada["ruta"]))
        if not os.path.isdir(raiz):
            print(f"Aviso: ruta no encontrada, se omite: {raiz}", file=sys.stderr)
            continue
        rutas = buscar_mapas(raiz, incluir_ruido)
        incluidas, descartes = filtrar_mapas(rutas, raiz, incluir_cv, profundidad_maxima)
        for ruta in incluidas:
            real = os.path.realpath(ruta)
            if real in vistos:
                continue
            vistos.add(real)
            mapas.append(analizar_mapa(ruta, raiz, titulo, bloque))
        for ruta_relativa, motivo in descartes:
            excluidos.append((bloque, titulo, ruta_relativa, motivo))
    return mapas, excluidos


def agrupar_mapas(mapas):
    grupos = []
    indice = {}
    for mapa in mapas:
        clave = (mapa.get("bloque", ""), mapa.get("grupo", ""))
        if clave not in indice:
            indice[clave] = len(grupos)
            grupos.append((clave[0], clave[1], []))
        grupos[indice[clave]][2].append(mapa)
    return grupos


def agrupar_bloques(mapas):
    bloques = []
    indice = {}
    for mapa in mapas:
        bloque = mapa.get("bloque", "")
        if bloque not in indice:
            indice[bloque] = len(bloques)
            bloques.append((bloque, []))
        bloques[indice[bloque]][1].append(mapa)
    return bloques


def envolver(dibujo, texto, fuente, ancho_max):
    palabras = texto.split()
    lineas = []
    actual = ""
    for palabra in palabras:
        candidato = f"{actual} {palabra}".strip()
        if dibujo.textlength(candidato, font=fuente) <= ancho_max:
            actual = candidato
        else:
            if actual:
                lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


def recortar_lineas(lineas, maximo):
    if len(lineas) <= maximo:
        return lineas
    recortadas = lineas[:maximo]
    recortadas[-1] = recortadas[-1].rstrip() + "…"
    return recortadas


def ajustar_linea(dibujo, texto, fuente, ancho_max):
    if dibujo.textlength(texto, font=fuente) <= ancho_max:
        return texto
    recortado = texto
    while recortado and dibujo.textlength(recortado + "…", font=fuente) > ancho_max:
        recortado = recortado[:-1]
    return recortado.rstrip() + "…"


def recortar_medio(dibujo, texto, fuente, ancho_max):
    if dibujo.textlength(texto, font=fuente) <= ancho_max:
        return texto
    partes = texto.split("/")
    candidato = f"{partes[0]}/…/{partes[-1]}"
    if len(partes) > 2 and dibujo.textlength(candidato, font=fuente) <= ancho_max:
        return candidato
    candidato = "…/" + partes[-1]
    if dibujo.textlength(candidato, font=fuente) <= ancho_max:
        return candidato
    return ajustar_linea(dibujo, partes[-1], fuente, ancho_max)


def texto_entradas(mapa):
    etiqueta = mapa["etiqueta_entradas"]
    if mapa["entradas"] == 1:
        etiqueta = etiqueta[:-1]
    return f"{mapa['entradas']} {etiqueta}"


MEDIDAS = {
    "ancho": 380,
    "separacion": 22,
    "margen_lienzo": 40,
    "alto_encabezado": 150,
    "alto_bloque": 58,
    "gap_grupo": 26,
    "margen_lateral": 18,
    "margen_superior": 20,
    "alto_badge": 24,
    "tras_badge": 12,
    "alto_titulo": 26,
    "tras_titulo": 2,
    "alto_ruta": 22,
    "alto_resumen": 22,
    "tras_resumen": 12,
    "alto_seccion": 20,
    "tras_seccion": 8,
    "alto_chip": 28,
    "separacion_chip_y": 8,
    "chip_pad_x": 10,
    "separacion_chip_x": 6,
    "tras_chips": 12,
    "gap_pie": 14,
    "alto_pie": 30,
}


def cargar_fuentes_tarjeta():
    return {
        "badge": cargar_fuente("negrita", 14),
        "titulo": cargar_fuente("negrita", 21),
        "ruta": cargar_fuente("mono", 14),
        "resumen": cargar_fuente("normal", 16),
        "pie": cargar_fuente("normal", 14),
        "seccion": cargar_fuente("negrita", 14),
        "chip": cargar_fuente("negrita", 15),
        "ruta_grupo": cargar_fuente("normal", 13),
    }


def distribuir_chips(dibujo, componentes, fuente, ancho_util, pad_x, gap_x):
    filas = []
    fila = []
    ancho_fila = 0
    for nombre in componentes:
        texto = ajustar_linea(dibujo, nombre, fuente, ancho_util - 2 * pad_x)
        ancho_chip = dibujo.textlength(texto, font=fuente) + 2 * pad_x
        if fila and ancho_fila + gap_x + ancho_chip > ancho_util:
            filas.append(fila)
            fila = []
            ancho_fila = 0
        fila.append((texto, ancho_chip))
        ancho_fila += (gap_x if len(fila) > 1 else 0) + ancho_chip
    if fila:
        filas.append(fila)
    return filas


def preparar_tarjeta(dibujo, mapa, fuentes):
    m = MEDIDAS
    ancho = m["ancho"]
    util = ancho - 2 * m["margen_lateral"]
    titulo = recortar_lineas(envolver(dibujo, mapa["titulo"], fuentes["titulo"], util), 2)
    ruta = recortar_medio(dibujo, mapa["ruta_relativa"], fuentes["ruta"], util)
    resumen = recortar_lineas(envolver(dibujo, mapa["resumen"] or "(sin resumen)", fuentes["resumen"], util), 3)
    nombres_con = [c["nombre"] for c in mapa["componentes"] if not c["sin_manifest"]]
    nombres_sin = [c["nombre"] for c in mapa["componentes"] if c["sin_manifest"]]
    chips_con = distribuir_chips(dibujo, nombres_con, fuentes["chip"], util, m["chip_pad_x"], m["separacion_chip_x"])
    chips_sin = distribuir_chips(dibujo, nombres_sin, fuentes["chip"], util, m["chip_pad_x"], m["separacion_chip_x"])

    cursor = m["margen_superior"] + m["alto_badge"] + m["tras_badge"]
    cursor += len(titulo) * m["alto_titulo"] + m["tras_titulo"] + m["alto_ruta"]
    cursor += len(resumen) * m["alto_resumen"] + m["tras_resumen"]
    for chips in (chips_con, chips_sin):
        if chips:
            cursor += m["alto_seccion"] + m["tras_seccion"]
            cursor += len(chips) * m["alto_chip"] + (len(chips) - 1) * m["separacion_chip_y"]
            cursor += m["tras_chips"]
    alto = cursor + m["gap_pie"] + m["alto_pie"]
    return {
        "titulo": titulo,
        "ruta": ruta,
        "resumen": resumen,
        "chips_con": chips_con,
        "chips_sin": chips_sin,
        "total_con": len(nombres_con),
        "total_sin": len(nombres_sin),
        "alto": alto,
    }


def dibujar_tarjeta(dibujo, mapa, x, y, diseno, fuentes):
    m = MEDIDAS
    ancho = m["ancho"]
    alto = diseno["alto"]
    if mapa.get("bloque") == BLOQUE_PAUSADOS:
        acento = ACENTO_PAUSADO
        tinte = TINTE_PAUSADO
    else:
        acento = ACENTOS.get(mapa["tipo"], ACENTOS["proyectos"])
        tinte = TINTES.get(mapa["tipo"], TINTES["proyectos"])
    ml = m["margen_lateral"]

    dibujo.rectangle([x + 2, y + 3, x + ancho + 2, y + alto + 3], fill=SOMBRA)
    dibujo.rectangle([x, y, x + ancho, y + alto], fill=TARJETA, outline=BORDE, width=1)
    dibujo.rectangle([x, y, x + ancho, y + 6], fill=acento)

    cursor = y + m["margen_superior"]

    etiqueta = {"proyectos": "PROYECTOS", "snippets": "SNIPPETS", "documentacion": "DOCS"}[mapa["tipo"]]
    ancho_badge = dibujo.textlength(etiqueta, font=fuentes["badge"]) + 18
    dibujo.rectangle([x + ml, cursor, x + ml + ancho_badge, cursor + m["alto_badge"]], fill=acento)
    dibujo.text((x + ml + 9, cursor + 5), etiqueta, font=fuentes["badge"], fill=(250, 247, 252))
    if mapa.get("grupo"):
        disponible = ancho - 2 * ml - ancho_badge - 12
        texto_ruta = ajustar_linea(
            dibujo, f"RUTA · {mapa['grupo']}", fuentes["ruta_grupo"], disponible
        )
        ancho_ruta = dibujo.textlength(texto_ruta, font=fuentes["ruta_grupo"])
        dibujo.text((x + ancho - ml - ancho_ruta, cursor + 7), texto_ruta,
                    font=fuentes["ruta_grupo"], fill=TENUE)
    cursor += m["alto_badge"] + m["tras_badge"]

    for linea in diseno["titulo"]:
        dibujo.text((x + ml, cursor), linea, font=fuentes["titulo"], fill=TITULO)
        cursor += m["alto_titulo"]
    cursor += m["tras_titulo"]
    dibujo.text((x + ml, cursor), diseno["ruta"], font=fuentes["ruta"], fill=TENUE)
    cursor += m["alto_ruta"]

    for linea in diseno["resumen"]:
        dibujo.text((x + ml, cursor), linea, font=fuentes["resumen"], fill=TEXTO)
        cursor += m["alto_resumen"]
    cursor += m["tras_resumen"]

    grupos = []
    if diseno["chips_sin"]:
        if diseno["chips_con"]:
            grupos.append(("Con manifiesto", diseno["total_con"], acento, tinte, diseno["chips_con"]))
        grupos.append(("Sin manifiesto", diseno["total_sin"], ACENTO_SIN_MANIFIESTO, TINTE_SIN_MANIFIESTO, diseno["chips_sin"]))
    elif diseno["chips_con"]:
        grupos.append(("Componentes", diseno["total_con"], acento, tinte, diseno["chips_con"]))

    for etiqueta, total, color, fondo, filas in grupos:
        dibujo.text((x + ml, cursor), f"{etiqueta} · {total}", font=fuentes["seccion"], fill=color)
        cursor += m["alto_seccion"] + m["tras_seccion"]
        for indice_fila, fila in enumerate(filas):
            cx = x + ml
            for texto, ancho_chip in fila:
                dibujo.rounded_rectangle([cx, cursor, cx + ancho_chip, cursor + m["alto_chip"]], radius=7, fill=fondo)
                dibujo.text((cx + m["chip_pad_x"], cursor + 5), texto, font=fuentes["chip"], fill=color)
                cx += ancho_chip + m["separacion_chip_x"]
            cursor += m["alto_chip"]
            if indice_fila < len(filas) - 1:
                cursor += m["separacion_chip_y"]
        cursor += m["tras_chips"]

    pie_y = cursor + m["gap_pie"] + 2
    dibujo.line([x + ml, pie_y - 10, x + ancho - ml, pie_y - 10], fill=BORDE, width=1)
    metadatos = " · ".join(v for v in (mapa["estado"], f"v{mapa['version']}" if mapa["version"] else "") if v)
    ancho_meta = dibujo.textlength(metadatos, font=fuentes["pie"]) if metadatos else 0
    entradas = texto_entradas(mapa)
    if mapa["stacks"]:
        entradas += " · " + ", ".join(mapa["stacks"][:2])
    entradas = ajustar_linea(dibujo, entradas, fuentes["pie"], ancho - 2 * ml - ancho_meta - 16)
    dibujo.text((x + ml, pie_y), entradas, font=fuentes["pie"], fill=TEXTO)
    if metadatos:
        dibujo.text((x + ancho - ml - ancho_meta, pie_y), metadatos, font=fuentes["pie"], fill=TENUE)


def pluralizar(cantidad, singular, plural):
    return f"{cantidad} {singular if cantidad == 1 else plural}"


def dibujar_leyenda(dibujo, centro_x, y, fuente):
    entradas = (
        ("Proyectos", ACENTOS["proyectos"]),
        ("Snippets", ACENTOS["snippets"]),
        ("Documentación", ACENTOS["documentacion"]),
        ("Sin manifiesto", ACENTO_SIN_MANIFIESTO),
    )
    ancho = sum(16 + dibujo.textlength(etiqueta, font=fuente) for etiqueta, _ in entradas)
    ancho += 24 * (len(entradas) - 1)
    x = centro_x - ancho / 2
    for etiqueta, color in entradas:
        dibujo.rounded_rectangle([x, y + 3, x + 10, y + 13], radius=3, fill=color)
        dibujo.text((x + 16, y), etiqueta, font=fuente, fill=TEXTO)
        x += 16 + dibujo.textlength(etiqueta, font=fuente) + 24


def dibujar_bloque(dibujo, titulo, x, y, ancho, fuente):
    m = MEDIDAS
    margen = m["margen_lienzo"]
    alto = m["alto_bloque"]
    estilo = ESTILOS_BLOQUE.get(titulo, ESTILOS_BLOQUE[BLOQUE_ACTIVOS])
    dibujo.rectangle([x, y, x + ancho - 2 * margen, y + alto - 16], fill=estilo["tinte"])
    dibujo.rectangle([x, y, x + 7, y + alto - 16], fill=estilo["acento"])
    dibujo.text((x + 20, y + 9), titulo.upper(), font=fuente, fill=estilo["acento"])


def planificar_seccion(mapas, disenos, columnas, base_y):
    separacion = MEDIDAS["separacion"]
    alturas = [base_y] * columnas
    asignacion = [[] for _ in range(columnas)]
    for mapa, diseno in zip(mapas, disenos):
        columna = min(range(columnas), key=lambda i: alturas[i])
        asignacion[columna].append((mapa, diseno, alturas[columna]))
        alturas[columna] += diseno["alto"] + separacion
    alto = (max(alturas) - separacion - base_y) if mapas else 0
    return asignacion, alto


def generar_imagen(mapas, salida, columnas=0):
    m = MEDIDAS
    ancho_tarjeta = m["ancho"]
    separacion = m["separacion"]
    margen = m["margen_lienzo"]
    alto_encabezado = m["alto_encabezado"]
    gap_grupo = m["gap_grupo"]

    fuentes = cargar_fuentes_tarjeta()
    medidor = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    grupos = agrupar_mapas(mapas)
    bloques = agrupar_bloques(mapas)

    total = len(mapas)
    if columnas <= 0:
        columnas = total if total <= 3 else max(1, min(4, round(math.sqrt(total))))
    columnas = max(1, min(columnas, max(total, 1)))

    ancho = margen * 2 + columnas * ancho_tarjeta + (columnas - 1) * separacion

    planes = []
    cursor_y = alto_encabezado
    for bloque, integrantes in bloques:
        if bloque:
            planes.append(("bloque", bloque, cursor_y))
            cursor_y += m["alto_bloque"]
        disenos = [preparar_tarjeta(medidor, mapa, fuentes) for mapa in integrantes]
        columnas_bloque = min(columnas, len(integrantes))
        asignacion, alto_seccion = planificar_seccion(
            integrantes, disenos, columnas_bloque, cursor_y
        )
        planes.append(("seccion", asignacion, columnas_bloque))
        cursor_y += alto_seccion + gap_grupo

    alto = cursor_y - gap_grupo + margen

    imagen = Image.new("RGB", (ancho, alto), FONDO)
    dibujo = ImageDraw.Draw(imagen)

    fuente_titulo = cargar_fuente("negrita", 38)
    fuente_sub = cargar_fuente("normal", 17)
    fuente_leyenda = cargar_fuente("normal", 15)
    fuente_bloque = cargar_fuente("negrita", 20)
    nombre = "Cartografía de La Hermita"
    ancho_nombre = dibujo.textlength(nombre, font=fuente_titulo)
    dibujo.text(((ancho - ancho_nombre) / 2, 30), nombre, font=fuente_titulo, fill=ENCABEZADO)
    total_componentes = sum(len(mapa["componentes"]) for mapa in mapas)
    total_sin_manifest = sum(
        1 for mapa in mapas for componente in mapa["componentes"] if componente["sin_manifest"]
    )
    subtitulo = " · ".join((
        pluralizar(total, "mapa", "mapas"),
        pluralizar(len(grupos), "ruta", "rutas"),
        pluralizar(total_componentes, "componente", "componentes"),
        f"{total_sin_manifest} sin manifiesto",
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    ))
    ancho_sub = dibujo.textlength(subtitulo, font=fuente_sub)
    dibujo.text(((ancho - ancho_sub) / 2, 78), subtitulo, font=fuente_sub, fill=SUBTITULO)
    dibujar_leyenda(dibujo, ancho / 2, 106, fuente_leyenda)

    contenido = ancho - 2 * margen
    for plan in planes:
        if plan[0] == "bloque":
            dibujar_bloque(dibujo, plan[1], margen, plan[2], ancho, fuente_bloque)
            continue
        _, asignacion, columnas_seccion = plan
        ancho_seccion = columnas_seccion * ancho_tarjeta + (columnas_seccion - 1) * separacion
        desplazamiento = (contenido - ancho_seccion) / 2
        for columna, tarjetas in enumerate(asignacion):
            x = margen + desplazamiento + columna * (ancho_tarjeta + separacion)
            for mapa, diseno, tarjeta_y in tarjetas:
                dibujar_tarjeta(dibujo, mapa, x, tarjeta_y, diseno, fuentes)

    imagen.save(salida)
    return salida, (ancho, alto)


def escapar_md(texto):
    return str(texto).replace("|", "\\|")


def generar_markdown(mapas, salida, excluidos, config=None):
    grupos = agrupar_mapas(mapas)
    conteo = {
        (bloque, titulo): len(integrantes)
        for bloque, titulo, integrantes in grupos
    }
    orden = []
    for entrada in config or []:
        titulo = entrada.get("titulo") or os.path.basename(entrada["ruta"].rstrip("/"))
        clave = (entrada.get("bloque", ""), titulo)
        if clave not in orden:
            orden.append(clave)
    for bloque, titulo, _ in grupos:
        if (bloque, titulo) not in orden:
            orden.append((bloque, titulo))
    lineas = [
        "# Cartografía de La Hermita",
        "",
        f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')} · "
        f"{len(mapas)} mapas · {len(grupos)} rutas",
        "",
        "## Rutas",
        "",
        "| Bloque | Ruta | Mapas |",
        "|--------|------|-------|",
    ]
    for bloque, titulo in orden:
        lineas.append(
            f"| {escapar_md(bloque)} | {escapar_md(titulo)} | "
            f"{conteo.get((bloque, titulo), 0)} |"
        )
    lineas.append("")
    bloque_actual = None
    for bloque, titulo, integrantes in grupos:
        if bloque != bloque_actual:
            if bloque:
                lineas.extend([f"## {escapar_md(bloque)}", ""])
            bloque_actual = bloque
        lineas.extend([
            f"### {escapar_md(titulo)}",
            "",
            "| # | Mapa | Tipo | Entradas | Sin manifest | Ruta |",
            "|---|------|------|----------|--------------|------|",
        ])
        for indice, mapa in enumerate(integrantes, 1):
            tipo = ETIQUETAS_TIPO.get(mapa["tipo"], mapa["tipo"])
            sin_manifest = sum(1 for componente in mapa["componentes"] if componente["sin_manifest"])
            lineas.append(
                f"| {indice} | {escapar_md(mapa['titulo'])} | {tipo} | "
                f"{texto_entradas(mapa)} | {sin_manifest} | `{mapa['ruta_relativa']}` |"
            )
        lineas.append("")
    lineas.extend(["## Exclusiones aplicadas", ""])
    if excluidos:
        for bloque, grupo, ruta_relativa, motivo in excluidos:
            etiqueta = f"{bloque}/{grupo}/{ruta_relativa}" if bloque else f"{grupo}/{ruta_relativa}"
            lineas.append(f"- `{etiqueta}` — {motivo}")
    else:
        lineas.append("- (ninguna)")
    lineas.append("")
    with open(salida, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas))
    return salida


def main():
    analizador = argparse.ArgumentParser(description="Genera una cartografía en imagen de los mapas 'MAP - *.md'.")
    analizador.add_argument("--version", action="version", version=f"%(prog)s V{VERSION}")
    analizador.add_argument("--raiz", default=None,
                            help="Escanear solo esta carpeta e ignorar RUTAS_ESCANEO.")
    analizador.add_argument("--titulo", default=None,
                            help="Título de la sección cuando se usa --raiz.")
    analizador.add_argument("--salida", default="cartografia_lh_total.png", help="Imagen PNG de salida.")
    analizador.add_argument("--salida-md", default="cartografia_lh_total.md", help="Listado Markdown de salida.")
    analizador.add_argument("--columnas", type=int, default=0, help="Número de columnas (0 = automático).")
    analizador.add_argument("--incluir-ruido", action="store_true",
                            help="No excluir node_modules, .opencode, site-packages, etc.")
    analizador.add_argument("--incluir-cv", action="store_true",
                            help="Incluir variantes de carpeta _cvNNN (por defecto se omiten).")
    analizador.add_argument("--profundidad", type=int, default=PROFUNDIDAD_MAXIMA,
                            help="Profundidad máxima de subcarpetas para los mapas (1 = solo el mapa de cada zona).")
    analizador.add_argument("--solo-proyectos", action="store_true",
                            help="Mostrar solo los mapas de tipo proyectos.")
    analizador.add_argument("--listar", action="store_true", help="Solo listar los mapas encontrados.")
    argumentos = analizador.parse_args()

    if argumentos.raiz:
        raiz = os.path.abspath(os.path.expanduser(argumentos.raiz))
        titulo = argumentos.titulo or os.path.basename(raiz.rstrip(os.sep)) or "Raíz"
        config = [{"titulo": titulo, "ruta": raiz, "bloque": "Ruta personalizada"}]
    else:
        config = [
            dict(entrada, bloque=bloque)
            for bloque, rutas in BLOQUES_RUTAS
            for entrada in rutas
        ]

    mapas, excluidos = escanear_rutas(
        config, argumentos.incluir_ruido, argumentos.incluir_cv, argumentos.profundidad
    )

    if not mapas:
        print("No se han encontrado mapas 'MAP - *.md'.", file=sys.stderr)
        return 1

    if argumentos.solo_proyectos:
        mapas = [mapa for mapa in mapas if mapa["tipo"] == "proyectos"]

    if not mapas:
        print("No quedan mapas tras aplicar los filtros.", file=sys.stderr)
        return 1

    if argumentos.listar:
        for mapa in mapas:
            sin_manifest = sum(1 for componente in mapa["componentes"] if componente["sin_manifest"])
            detalle = f" · {sin_manifest} sin manifest" if sin_manifest else ""
            print(f"[{mapa['tipo']:<14}] {mapa['bloque']} :: {mapa['grupo']} :: "
                  f"{mapa['ruta_relativa']}  ({mapa['entradas']} {mapa['etiqueta_entradas']}{detalle})")
        print(f"\nTotal: {len(mapas)} mapas.")
        return 0

    salida, medida = generar_imagen(mapas, argumentos.salida, argumentos.columnas)
    print(f"Generada {salida} ({medida[0]}x{medida[1]} px) con {len(mapas)} mapas.")
    salida_md = generar_markdown(mapas, argumentos.salida_md, excluidos, config)
    print(f"Generado {salida_md} con {len(mapas)} mapas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
