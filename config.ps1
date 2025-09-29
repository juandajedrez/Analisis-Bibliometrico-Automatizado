# Ruta del entorno virtual
$venvPath = "entorno_virtual_analisis"

# Verificar si el entorno virtual existe
if (-Not (Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Host "Entorno virtual no encontrado. Creando uno nuevo..."
    python -m venv $venvPath
}

# Activar el entorno virtual
Write-Host "Activando entorno virtual..."
& "$venvPath\Scripts\Activate.ps1"

# Instalar dependencias si existe requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "Instalando dependencias..."
    pip install -r requirements.txt
}

# Ejecutar el script principal
Write-Host "Ejecutando el proyecto"
python "Proyecto\manage.py" runserver 