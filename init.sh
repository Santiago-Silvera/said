#!/bin/bash

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "pip no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

ENV_DIR="/home/horariosFIUM/env/horarios"

# Verificar si existe un entorno virtual
if [ -d $ENV_DIR ]; then
    echo "El entorno virtual ya existe."
else
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar el entorno virtual
echo "Activando el entorno virtual..."
source .venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt -q

# Verificar si PostgreSQL está en ejecución
echo "Verificando si PostgreSQL está en ejecución..."
python3 check_postgres.py
if [ $? -ne 0 ]; then
    echo "PostgreSQL no está en ejecución o no se puede conectar. Por favor, asegúrate de que esté en ejecución y accesible."
    exit 1
fi

# Configurar la base de datos
echo "Configurando la base de datos..."
python3 initialize_db.py

# Iniciar el servidor
echo "Iniciando el servidor..."
python3 app.py
