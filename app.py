from flask import Flask, render_template, request, redirect, session
import os
import jwt
from dotenv import load_dotenv
from entities import db
from services import guardar_respuesta, get_time_info
from datetime import timedelta

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

time_slots, days_of_week = get_time_info()

@app.route('/preferences')
def index():
    ci = request.args.get('ci')
    user_id = session.get('user_id')
    if user_id is None:
        # Use a configurable redirect URL
        login_url = os.getenv('LOGIN_URL', "https://www3.um.edu.uy/profesores/default.asp")
        return redirect(login_url)
    
    # Handle potential issues with time_slots or days_of_week
    if not time_slots or not days_of_week:
        return '<p>Error: Unable to load time information.</p>', 500

    return render_template('index.html', time_slots=time_slots, days_of_week=days_of_week, ci=ci)

@app.route('/submit', methods=['POST'])
def submit():
    preferences = request.form.get('preferences')
    if not preferences:
        return '<p>Error: Ha ocurrido un error.</p>', 400
    preferences_data = json.loads(preferences)
    ci = 0  # Cambiar según sea necesario
    guardar_respuesta(preferences_data, ci)
    return f'<p>Confirmación: Se han guardado las preferencias horarias para Nombre!</p>', 200

@app.route('/auth')
def handle_auth():
    token = request.args.get('token')
    if not token:
        return {"error": "Token missing"}, 400

    try:
        # Decode and validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get('user_id')
        if not user_id:
            return {"error": "Invalid token payload"}, 400

        # Store user_id in session and set session timeout
        session['user_id'] = user_id
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)  # Example: 30-minute session timeout

        # Redirect to preferences page
        return redirect('/preferences')
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}, 403

if __name__ == "__main__":
    app.run(port=5000, debug=True)

