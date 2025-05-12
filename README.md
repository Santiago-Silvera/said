# Frontend Gestor de Horarios

Este proyecto es una aplicación web para gestionar preferencias horarias. Los usuarios (profesores de la FIUM por el momento) pueden seleccionar sus preferencias de horarios y enviarlas para su almacenamiento en una base de datos.

### Archivos principales

- **`app.py`**: Archivo principal que contiene la lógica del servidor Flask.
- **`templates/index.html`**: Plantilla HTML para la interfaz de usuario.
- **`static/styles.css`**: Archivo CSS para los estilos de la aplicación.
- **`requirements.txt`**: Lista de dependencias necesarias para ejecutar el proyecto.

## Requisitos Previos

- Python 3.7 o superior
- [pip](https://pip.pypa.io/en/stable/)
- PostgreSQL (para la base de datos)

## Instalación

1. Clona este repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd frontend-gestor-horarios
```

2. Instala las dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Inicia el servidor Flask

```bash
python3 app.py
```
