from flask import Flask, render_template, request, redirect, session
import os
import jwt
import json
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# Load database URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.secret_key = SECRET_KEY  # Needed to use Flask sessions

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# This may need some later refactoring
class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ci = db.Column(db.String(20), nullable=False)
    preferences = db.Column(db.Text, nullable=False)

# Update guardar_respuesta to save data to the database
def guardar_respuesta(preferences_data, ci):
    preferences_json = json.dumps(preferences_data)
    new_preference = Preference(ci=ci, preferences=preferences_json)
    db.session.add(new_preference)
    db.session.commit()

# TODO: Obtener los datos de la base de datos
def get_time_info():
    return ["8:00", "9:00", "10:00", "11:00", "12:00"], ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"] 

time_slots, days_of_week = get_time_info()

@app.route('/')
def index():
    # Obtener los datos del redirect
    ip = request.remote_addr
    print("The ip:", ip)

    ci = request.args.get('ci')
    print(ci)

    hash_ = request.args.get('hash')
    print(hash_)

    user_id = session.get('user_id')
    if user_id is None:
        return redirect("https://www3.um.edu.uy/profesores/default.asp")

    # Pass time slots and days to the template
    return render_template('index.html', time_slots=time_slots, days_of_week=days_of_week, ci=ci)

@app.route('/submit', methods=['POST'])
def submit():
    preferences = request.form.get('preferences')
    print(preferences)

    if not preferences:
        return '<p>Error: Ha ocurrido un error.</p>', 400

    preferences_data = json.loads(preferences)
    ci: int = 0

    guardar_respuesta(preferences_data, ci)

    # TODO: Obtener el nombre
    return f'<p>Confirmación: Se han guardado las preferencias horarias para Nombre!</p>', 200

@app.route('/auth')
def handle_auth():
    token = request.args.get('token')

    if not token:
        return "Token missing", 400

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        session['user_id']= payload.get('user_id')
        return redirect('/preferences')

    except jwt.ExpiredSignatureError:
        return "Token expired", 401
    except jwt.InvalidTokenError:
        return "Invalid token", 403

if __name__ == "__main__":
    app.run(port=5000, debug=True)

