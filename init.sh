#!/bin/bash

# filepath: c:\Users\santi\Desktop\code\frontend-gestor-horarios\init_server.sh

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo "Python no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "pip no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Crear un entorno virtual
echo "Creando entorno virtual..."
python -m venv venv

# Activar el entorno virtual
echo "Activando entorno virtual..."
source venv/Scripts/activate  # En Windows

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Configurar la base de datos
echo "Configurando la base de datos..."
python -c "
from app import db
db.create_all()
print('Base de datos configurada correctamente.')
"

# Iniciar el servidor
echo "Iniciando el servidor..."
python app.py