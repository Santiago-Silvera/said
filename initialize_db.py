import os
from sqlalchemy.sql import text

def initialize_database():
    from app import app
    from entities import db

    with app.app_context():
        # db.drop_all()
        db.create_all()

        # Execute the schema from script_db.sql
        schema_path = os.path.join(os.path.dirname(__file__), 'script_db.sql')
        with open(schema_path, 'r') as schema_file:
            schema_sql = schema_file.read()

        # Split the SQL script into individual statements
        statements = schema_sql.split(';')
        with db.engine.connect() as connection:
            for statement in statements:
                statement = statement.strip()
                if statement:  # Skip empty statements
                    connection.execute(text(statement))  # Use text() to wrap the SQL statement

        print("Base de datos inicializada y tablas creadas.")

if __name__ == "__main__":
    initialize_database()