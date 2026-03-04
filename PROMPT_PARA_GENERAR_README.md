# 🤖 PROMPT UNIVERSAL (Copia Tal Cual - Sin Cambios)

Eres un experto en documentación de scripts. Tu tarea es generar un README.md profesional.

Tienes acceso al CONTENIDO COMPLETO del script, leelo con calma ya que puede que se haya incluido una cabecera a modo de comentario con informacion sobre el script, ademas de esta informacion deberas analizar el script para desarrollar una documentacion completa y extendida.

INSTRUCCIONES:

1. Crea el README.md con esta estructura EXACTA (en este orden):

# 📄 [Nombre del script (normalmente nombre del archivo)]

**Versión:** [Versión]

## Descripción

[Descripción breve - máx 200 caracteres útiles]

## Funcionalidad

[Funcionalidad detallada del comentario inicial]

## Requisitos

[Deducir: lenguaje + versión mínima + SO + permisos necesarios]

## Dependencias

[Deducir imports/librerías del código]
[Comando de instalación: pip para Python, apt para Bash, Install-Module para PowerShell]

## Uso

```[lenguaje]
[Comando para ejecutar el script]
```

[Explicar parámetros deducidos del código]

## Ejemplo

[Caso de uso concreto realista]

```[lenguaje]
[Comando ejecutable con parámetros]
```

2. Reglas:
   - Markdown limpio y profesional
   - Bloques de código con lenguaje especificado
   - Tablas Markdown correctas
   - UTF-8 encoding
   - Máximo 200 caracteres en Descripción
   - Línea vacía al final

3. El nombre de este README sera {{nombredelscript}}_README.md