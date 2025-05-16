import json
from flask import Flask, render_template, request, redirect, session
import os
import jwt
from dotenv import load_dotenv
from entities import db
from services import save_response, get_time_blocks, verify_professor, get_professor_data, get_previous_preferences
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
    ci = session.get('user_id')
    if not verify_professor(ci):
        # Serve the error.html template for unauthenticated users
        return render_template('error.html', message="Usuario no autenticado. Por favor, inicie sesión."), 401

    professor_data = get_professor_data(ci)
    professor_name = professor_data.get('nombre')

    # Get time information
    time_blocks = get_time_blocks()
    previous_preferences = get_previous_preferences(ci)
    print(f"Previous preferences for user {ci}:")
    print(previous_preferences)

    # Merge previous preferences into time_blocks
    for block in time_blocks:
        block['preference'] = previous_preferences.get(block['id'], 0)

    # Handle potential issues with time_slots or days_of_week
    if not time_blocks:
        # Serve the error.html template for data loading issues
        return render_template('error.html', message="Imposible cargar datos del usuario. Inténtelo más tarde."), 500

    return render_template('index.html', bloques_horarios=time_blocks, ci=ci, professor_name=professor_name)

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

        save_response(preferences, ci)

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
        return render_template('error.html', message="El token ha expirado. Por favor, inicie sesión nuevamente."), 401
    except jwt.InvalidTokenError:
        # Serve the error.html template for invalid token
        return render_template('error.html', message="Token inválido. Por favor, intente acceder nuevamente."), 403
    except jwt.InvalidAudienceError:
        # Serve the error.html template for invalid audience
        return render_template('error.html', message="Audiencia inválida en el token. Por favor, intente acceder nuevamente."), 403

if __name__ == "__main__":
    app.run(port=5000, debug=True)

