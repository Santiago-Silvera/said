import json
from typing import Any, List
from flask import Flask, render_template, request, redirect, session
import os
import jwt
from dotenv import load_dotenv
from entities import db
from services import guardar_respuesta, obtener_bloques_horarios, verificar_profesor, get_professor_data, get_previous_preferences, listar_turnos_materias_profesor
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

# Dynamically construct the DATABASE_URL
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)

app.secret_key = SECRET_KEY

# Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/preferences')
def index():
    ci: int | Any = session.get('user_id')
    if not verificar_profesor(ci):
        return render_template('error.html', message="Usuario no autenticado. Por favor, inicie sesión."), 401

    professor_data = get_professor_data(ci)
    professor_name = professor_data.get('nombre')

    # Obtener materias y turnos asignados
    asignaciones = listar_turnos_materias_profesor(ci)
    materias_asignadas = asignaciones["materias"]
    turnos_asignados = asignaciones["turnos"]
    if not turnos_asignados:
        return render_template('error.html', message="No se han encontrado turnos asignados para el profesor."), 404

    # Obtener bloques horarios por turno
    bloques_turno: List[int] = []
    for turno in turnos_asignados:
        bt = obtener_bloques_horarios(turno=turno)
        bloques_turno.extend([b.get("id") for b in bt])
    
    print("app: bloques_turno:", bloques_turno)
    
    all_time_blocks = obtener_bloques_horarios(turno=None)
    previous_preferences = get_previous_preferences(ci)
    for block in all_time_blocks:
        block['preference'] = previous_preferences.get(block['id'], 0)

    if not all_time_blocks:
        return render_template('error.html', message="Imposible cargar datos del usuario. Inténtelo más tarde."), 500

    return render_template(
        'index.html',
        bloques_horarios=all_time_blocks,
        ci=ci,
        professor_name=professor_name,
        materias_asignadas=materias_asignadas,
        turnos_asignados=turnos_asignados,
        bloques_turno=bloques_turno
    )


@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Parse JSON payload
        data = request.data
        json_data = json.loads(data.decode('utf-8'))
        preferences = json_data.get('preferences', None)
        if not preferences:
            return {"error": "Debes proporcionar preferencias."}, 400

        ci = session.get('user_id')  # Use the logged-in user's ID

        guardar_respuesta(preferences, ci)

        return {"success": True, "message": "Preferencias guardadas correctament"}, 200
    except json.JSONDecodeError:
        return {"error": "No se ha podido decodificar correctamente el JSON"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/')
def handle_auth():
    token = request.args.get('token')
    if not token:
        # Serve the error.html template for missing token
        return render_template('error.html', message="Token faltante. Por favor, intente acceder nuevamente."), 400

    try:
        # Decode and validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], audience='horariosFIUM2025')
        user_id = payload.get('user_id')
        if not user_id:
            # Serve the error.html template for invalid token payload
            return render_template('error.html', message="Token inválido. Por favor, intente acceder nuevamente."), 400

        # Store user_id in session and set session timeout
        session['user_id'] = user_id
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)  # Example: 30-minute session timeout

        # Redirect to preferences page
        return redirect('/preferences')
    except jwt.ExpiredSignatureError:
        # Serve the error.html template for expired token
        return render_template('error.html', message="Su sesión ha expirado. Por favor, inicie sesión nuevamente."), 401
    except Exception:
        return render_template('error.html', message="No se ha podido autenticar. Por favor, intente acceder nuevamente."), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)

