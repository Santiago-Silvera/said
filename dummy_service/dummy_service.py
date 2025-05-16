# dummy_service.py
from flask import Flask, render_template_string, request
import jwt
import os

app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'dummysecret')

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "aud": 'horariosFIUM2025'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.route('/')
def index():
    user_id = request.args.get('user_id', '12345')
    token = generate_token(user_id)
    url = f"http://localhost:5000/?token={token}"
    return render_template_string('<h2>Enlace a la app principal:</h2><a href="{{ url }}">{{ url }}</a>', url=url)

if __name__ == "__main__":
    app.run(port=5050, debug=True)
