# Sistema Administración de Información Docente

Este proyecto es una aplicación web para gestionar preferencias horarias. Los usuarios (profesores de la FIUM por el momento) pueden seleccionar sus preferencias de horarios y enviarlas para su almacenamiento en una base de datos.

## Archivos principales

- **`said.py`**: Archivo principal que contiene la lógica del servidor Flask.
- **`entities.py`**: Define los modelos de base de datos, incluyendo las entidades `Persona`, `Profesor`, `Materia`, `Horario`, `BloqueHorario`, `Turno`, etc.
- **`services.py`**: Funciones de lógica de negocio y acceso a datos.

## Requisitos Previos

- Python 3.7 o superior
- [pip](https://pip.pypa.io/en/stable/)
- PostgreSQL (para la base de datos)
- Archivo `.env` con las siguientes variables configuradas:
  ```properties
  SECRET_KEY
  POSTGRES_HOST
  POSTGRES_PORT
  POSTGRES_DB
  POSTGRES_USER
  POSTGRES_PASSWORD
  ```

## Carga de datos de prueba

Para pruebas locales, puedes usar el script `initialize_db.py` para poblar la base de datos con datos de ejemplo.  
**¡IMPORTANTE!** Este script es solo para testing local y **no debe usarse en producción** ni en el entorno web.

También puedes utilizar el script `init.sh` en entornos locales, el cual inicializa la base de datos ejecutando `initialize_db.py` automáticamente.  
**Ninguno de estos scripts debe usarse en producción.**

En entornos de **producción**, la aplicación debe ejecutarse usando la interfaz `wsgi.py` junto con un servidor como **nginx** y una base de datos aparte, la cual debe configurarse y poblarse de forma manual según las necesidades del entorno.

## Importación de profesores desde Excel

La importación de profesores desde archivos Excel es una funcionalidad pensada únicamente para entornos locales o de testing.  
**No debe utilizarse en producción.**

## Notas importantes

- No uses los scripts de inicialización automática (`init.sh`, `initialize_db.py`) ni la importación desde Excel en producción.
- En producción, configura la base de datos y los datos iniciales de manera manual y controlada.
- Usa siempre la interfaz `wsgi.py` y un servidor web adecuado para exponer la aplicación en producción.

## Local Development with Docker Compose

1. **Start backend and database:**
   ```sh
   docker-compose up --build
   ```
   This will build and start both the backend and the PostgreSQL database.

2. **Run tests:**
   ```sh
   docker-compose run --rm backend bash -c "python -m unittest discover -s tests"
   ```
   This will run your unittests inside the backend container.

3. **Stop containers:**
   ```sh
   docker-compose down
   ```
   This will stop and remove all running containers.

> Make sure Docker and Docker Compose are installed on your machine.

---
