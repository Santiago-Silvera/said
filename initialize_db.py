from app import app
from entities import db

with app.app_context():
    db.create_all()
    print("All tables created successfully.")