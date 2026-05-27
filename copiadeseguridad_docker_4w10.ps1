<#
Copia de seguridad con Docker Compose

Versión: 1.0.0

Descripción:
Realiza una copia de seguridad comprimida (.zip) de una carpeta, deteniendo y reiniciando automáticamente el servicio Docker Compose antes y después del proceso.

Dependencias:
- Docker Compose
- 7-Zip

Uso:
.\copiadeseguridad_docker_4w10.ps1 [-carpetaOrigen <ruta>]

Ejemplo:
.\copiadeseguridad_docker_4w10.ps1 -carpetaOrigen C:\Docker\wordpress
#>

param (
    [string]$carpetaOrigen
)

# Función para detener el servicio Docker Compose
function Detener-DockerCompose {
    param([string]$rutaProyecto)
    $archivoCompose = Join-Path $rutaProyecto "docker-compose_wordpresscactele.yaml"
    Write-Host "Deteniendo Docker Compose en: $rutaProyecto"
    docker-compose -f $archivoCompose down
    Start-Sleep -Seconds 5  # Espera para liberar recursos bloqueados
}

# Función para iniciar el servicio Docker Compose
function Iniciar-DockerCompose {
    param([string]$rutaProyecto)
    $archivoCompose = Join-Path $rutaProyecto "docker-compose_wordpresscactele.yaml"
    Write-Host "Arrancando Docker Compose en: $rutaProyecto"
    docker-compose -f $archivoCompose up -d
}

# Determinar carpeta origen
if (-not $carpetaOrigen) {
    $carpetaOrigen = (Get-Location).Path
} else {
    # Normalizar ruta por si es relativa
    $carpetaOrigen = (Resolve-Path $carpetaOrigen).Path
}

# Carpeta de destino = carpeta actual
$carpetaDestino = (Get-Location).Path

# Generar nombre de archivo con fecha y hora
$marcaTiempo = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$nombreArchivoZip = "Backup_$marcaTiempo.zip"
$rutaArchivoZip = Join-Path $carpetaDestino $nombreArchivoZip

# Ruta de 7-Zip (ajustar si está en otra ubicación)
$ruta7Zip = "C:\Program Files\7-Zip\7z.exe"

# Verificar que 7-Zip está disponible
if (-not (Test-Path $ruta7Zip)) {
    Write-Error "ERROR: No se encontró 7-Zip en: $ruta7Zip"
    exit 1
}

# Detener Docker antes del backup
Detener-DockerCompose -rutaProyecto $carpetaOrigen

# Comprimir carpeta con 7-Zip
Write-Host "Comenzando compresión con 7-Zip..."
& $ruta7Zip a -tzip $rutaArchivoZip "$carpetaOrigen\*" -mx9

# Reiniciar Docker después del backup
Iniciar-DockerCompose -rutaProyecto $carpetaOrigen

# Validar si el archivo se creó correctamente
if (Test-Path $rutaArchivoZip) {
    Write-Host "Backup creado correctamente en: $rutaArchivoZip"
} else {
    Write-Error "ERROR: No se pudo crear el backup en: $rutaArchivoZip"
}
