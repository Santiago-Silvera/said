import json
from typing import List
from flask import Flask, request, session, jsonify
import os
import jwt
from dotenv import load_dotenv
from flask_cors import CORS
from entities import db
from services import guardar_respuesta, obtener_bloques_horarios, verificar_profesor, get_professor_data, get_previous_preferences, listar_turnos_materias_profesor, decode_hash
from datetime import timedelta, datetime
from functools import wraps
import bcrypt

# Load environment variables from .env file
load_dotenv()

# Dynamically construct the DATABASE_URL
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.secret_key = SECRET_KEY

# Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# JWT decorator
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        env = os.getenv('ENV', 'development')
        if env != 'production':
            # In development, skip authentication and set a dummy user_id
            request.user_id = 1  # or any test user id
            return f(*args, **kwargs)
        auth = request.headers.get('Authorization', None)
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401
        token = auth.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except Exception:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # Replace this with your real user validation logic
    if username == 'admin' and password == 'password':
        user_id = 123456  # Replace with real user ID
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/api/preferences')
@jwt_required
def index():
    """Return the preferences data for the logged in professor as JSON."""
    ci = getattr(request, 'user_id', None)
    if not verificar_profesor(ci):
        return jsonify({"error": "Usted no se encuentra registrado."}), 401

    professor_data = get_professor_data(ci)
    professor_name = professor_data.get('nombre_completo')
    min_max_dias = professor_data.get('min_max_dias', False)

    # Obtener materias y turnos asignados
    asignaciones = listar_turnos_materias_profesor(ci)
    materias_asignadas = asignaciones["materias"]
    turnos_asignados = asignaciones["turnos"]
    if not turnos_asignados:
        return jsonify({"error": "No se han encontrado turnos asignados para el profesor."}), 404

    # Obtener bloques horarios por turno
    bloques_turno: List[int] = []
    for turno in turnos_asignados:
        bt = obtener_bloques_horarios(turno=turno)
        bloques_turno.extend([b.get("id") for b in bt])

    all_time_blocks = obtener_bloques_horarios(turno=None)
    previous_preferences = get_previous_preferences(ci)
    for block in all_time_blocks:
        block['preference'] = previous_preferences.get(block['id'], 0)

    if not all_time_blocks:
        return jsonify({"error": "Imposible cargar datos del usuario. Inténtelo más tarde."}), 500

    return jsonify({
        "bloques_horarios": all_time_blocks,
        "ci": ci,
        "professor_name": professor_name,
        "materias_asignadas": materias_asignadas,
        "turnos_asignados": turnos_asignados,
        "bloques_turno": bloques_turno,
        "min_max_dias": min_max_dias
    })

@app.route('/api/')
def entry():
    """Entry point that authenticates the user using a legacy hash. Returns JSON."""
    hash_code = request.args.get('hash')
    if not hash_code:
        return jsonify({"error": "Error de autenticación."}), 401
    ci: int = decode_hash(hash_code)

    session['user_id'] = ci
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

    return jsonify({"success": True, "redirect": "/preferences"})

@app.route('/api/submit', methods=['POST'])
@jwt_required
def submit():
    """Persist the submitted preferences for the current professor."""
    try:
        data = request.data
        json_data = json.loads(data.decode('utf-8'))
        preferences = json_data.get('preferences', None)
        min_dias = json_data.get('min_dias', False)
        if preferences is None:
            return jsonify({"error": "Debes proporcionar preferencias."}), 400

        ci = getattr(request, 'user_id', None)

        guardar_respuesta(preferences, ci, min_dias)  # <-- pasa min_dias

        return jsonify({"success": True, "message": "Preferencias guardadas correctamente"}), 200
    except json.JSONDecodeError:
        return jsonify({"error": "No se ha podido decodificar correctamente el JSON"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth')
def handle_auth():
    """Handle JWT based authentication used by the external portal. Returns JSON."""
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token faltante. Por favor, intente acceder nuevamente."}), 400

    try:
        # Decode and validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], audience='horariosFIUM2025')
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({"error": "Token inválido. Por favor, intente acceder nuevamente."}), 400

        # Store user_id in session and set session timeout
        session['user_id'] = user_id
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)

        # Indicate successful authentication
        return jsonify({"success": True, "redirect": "/preferences"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Su sesión ha expirado. Por favor, inicie sesión nuevamente."}), 401
    except Exception:
        return jsonify({"error": "No se ha podido autenticar. Por favor, intente acceder nuevamente."}), 500

# DEV-ONLY: Populate DB with dummy data
@app.route('/api/dev/populate', methods=['POST'])
def dev_populate():
    if not app.debug:
        return jsonify({'error': 'Not allowed in production'}), 403
    # Add admin PERSONA
    admin_email = 'admin@um.edu.uy'
    admin_password = 'admin123'
    admin_hash = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
    db.session.execute(db.text('''
        INSERT INTO said."PERSONAS" (nombres, apellidos, fecha_nacimiento, email_um, email_personal, telefono, password_hash)
        VALUES (:nombres, :apellidos, :fecha_nacimiento, :email_um, :email_personal, :telefono, :password_hash)
        ON CONFLICT (email_um) DO NOTHING
    '''), {
        'nombres': 'Admin',
        'apellidos': 'User',
        'fecha_nacimiento': 19900101,
        'email_um': admin_email,
        'email_personal': 'admin.personal@um.edu.uy',
        'telefono': '099000000',
        'password_hash': admin_hash
    })
    # Get admin id
    admin = db.session.execute(db.text('SELECT id_persona FROM said."PERSONAS" WHERE email_um = :email'), {'email': admin_email}).fetchone()
    if admin:
        db.session.execute(db.text('''
            INSERT INTO said."PROFESORES" (id_persona, fecha_desde, ddu_estatus)
            VALUES (:id_persona, :fecha_desde, :ddu_estatus)
            ON CONFLICT (id_persona, fecha_desde) DO NOTHING
        '''), {
            'id_persona': admin.id_persona,
            'fecha_desde': '2024-01-01',
            'ddu_estatus': 'S'
        })
    # Add dummy professors
    for i in range(1, 4):
        email = f'profesor{i}@um.edu.uy'
        hash_pw = bcrypt.hashpw(f'profesor{i}pw'.encode(), bcrypt.gensalt()).decode()
        db.session.execute(db.text('''
            INSERT INTO said."PERSONAS" (nombres, apellidos, fecha_nacimiento, email_um, email_personal, telefono, password_hash)
            VALUES (:nombres, :apellidos, :fecha_nacimiento, :email_um, :email_personal, :telefono, :password_hash)
            ON CONFLICT (email_um) DO NOTHING
        '''), {
            'nombres': f'Profesor{i}',
            'apellidos': f'Apellido{i}',
            'fecha_nacimiento': 19800101 + i,
            'email_um': email,
            'email_personal': f'profesor{i}.personal@um.edu.uy',
            'telefono': f'09900000{i}',
            'password_hash': hash_pw
        })
        prof = db.session.execute(db.text('SELECT id_persona FROM said."PERSONAS" WHERE email_um = :email'), {'email': email}).fetchone()
        if prof:
            db.session.execute(db.text('''
                INSERT INTO said."PROFESORES" (id_persona, fecha_desde, ddu_estatus)
                VALUES (:id_persona, :fecha_desde, :ddu_estatus)
                ON CONFLICT (id_persona, fecha_desde) DO NOTHING
            '''), {
                'id_persona': prof.id_persona,
                'fecha_desde': '2024-01-01',
                'ddu_estatus': 'S'
            })
    # Add dummy CURSOS
    db.session.execute(db.text('''
        INSERT INTO said."CURSOS" (cod_materia, semestre, anio)
        VALUES ('MAT101', 1, 2024), ('MAT102', 2, 2024)
        ON CONFLICT DO NOTHING
    '''))
    db.session.commit()
    return jsonify({'success': True, 'message': 'Dummy data added'})

# DEV-ONLY: Add a PERSONA
@app.route('/api/dev/add_persona', methods=['POST'])
def dev_add_persona():
    if not app.debug:
        return jsonify({'error': 'Not allowed in production'}), 403
    data = request.json
    email = data.get('email_um')
    password = data.get('password')
    hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db.session.execute(db.text('''
        INSERT INTO said."PERSONAS" (nombres, apellidos, fecha_nacimiento, email_um, email_personal, telefono, password_hash)
        VALUES (:nombres, :apellidos, :fecha_nacimiento, :email_um, :email_personal, :telefono, :password_hash)
        ON CONFLICT (email_um) DO NOTHING
    '''), {
        'nombres': data.get('nombres'),
        'apellidos': data.get('apellidos'),
        'fecha_nacimiento': data.get('fecha_nacimiento', 19900101),
        'email_um': email,
        'email_personal': data.get('email_personal', email),
        'telefono': data.get('telefono', '099000000'),
        'password_hash': hash_pw
    })
    db.session.commit()
    return jsonify({'success': True})

# DEV-ONLY: Add a PROFESOR
@app.route('/api/dev/add_profesor', methods=['POST'])
def dev_add_profesor():
    if not app.debug:
        return jsonify({'error': 'Not allowed in production'}), 403
    data = request.json
    id_persona = data.get('id_persona')
    db.session.execute(db.text('''
        INSERT INTO said."PROFESORES" (id_persona, fecha_desde, ddu_estatus)
        VALUES (:id_persona, :fecha_desde, :ddu_estatus)
        ON CONFLICT (id_persona, fecha_desde) DO NOTHING
    '''), {
        'id_persona': id_persona,
        'fecha_desde': data.get('fecha_desde', '2024-01-01'),
        'ddu_estatus': data.get('ddu_estatus', 'S')
    })
    db.session.commit()
    return jsonify({'success': True})

if __name__ == "__main__":
    # For local development only; use Gunicorn in production
    app.run(port=5000, debug=True)

