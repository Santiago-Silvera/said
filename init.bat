@echo off

:: Verificar si Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python no está instalado. Por favor, instálalo antes de continuar.
    exit /b 1
)

:: Verificar si pip está instalado
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo pip no está instalado. Por favor, instálalo antes de continuar.
    exit /b 1
)

:: Verificar si existe un entorno virtual
if exist .venv (
    echo El entorno virtual ya existe.
) else (
    echo Creando entorno virtual...
    python -m venv .venv
)

:: Activar el entorno virtual
echo Activando el entorno virtual...
call .venv\Scripts\activate

:: Instalar dependencias
echo Instalando dependencias...
call pip install -r requirements.txt

:: Verificar si PostgreSQL está en ejecución
echo Verificando si PostgreSQL está en ejecución...
python check_postgres.py
if %errorlevel% neq 0 (
    echo PostgreSQL no está en ejecución o no se puede conectar. Por favor, asegúrate de que esté en ejecución y accesible.
    exit /b 1
)

:: Configurar la base de datos
:: echo Configurando la base de datos...
:: python initialize_db.py

:: Iniciar el servidor
echo Iniciando el servidor...
python app.py