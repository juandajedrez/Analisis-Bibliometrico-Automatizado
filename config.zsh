#!/usr/bin/env zsh

# Ruta del entorno virtual
venvPath="entorno_virtual_analisis"

# Verificar si el entorno virtual existe
if [ ! -d "$venvPath/bin" ]; then
    echo "Entorno virtual no encontrado. Creando uno nuevo..."
    python3 -m venv "$venvPath"
fi

# Activar el entorno virtual
echo "Activando entorno virtual..."
source "$venvPath/bin/activate"

# Instalar dependencias si existe requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

# Ejecutar el script principal
echo "Ejecutando el proyecto..."
python3 "Proyecto/manage.py" runserver

