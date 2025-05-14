# Frontend Gestor de Horarios

Este proyecto es una aplicación web para gestionar preferencias horarias. Los usuarios (profesores de la FIUM por el momento) pueden seleccionar sus preferencias de horarios y enviarlas para su almacenamiento en una base de datos.

## Archivos principales

- **`app.py`**: Archivo principal que contiene la lógica del servidor Flask.
- **`templates/index.html`**: Plantilla HTML para la interfaz de usuario.
- **`templates/error.html`**: Plantilla HTML para mostrar mensajes de error.
- **`static/styles.css`**: Archivo CSS para los estilos de la aplicación.
- **`requirements.txt`**: Lista de dependencias necesarias para ejecutar el proyecto.

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

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/Santiago-Silvera/frontend-gestor-horarios
   cd frontend-gestor-horarios
   ```

2. Ejecuta el script de inicialización

En caso de sistemas basados en Unix(Linux/MacOS):

```bash
bash init.sh
```

En caso de Windows:

```bash
.\init.bat
```
