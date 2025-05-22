import os
from psycopg2 import OperationalError, connect
from dotenv import load_dotenv


def check_postgres_connection():
    try:
        load_dotenv()
        # Use environment variables for sensitive information
        host = os.getenv('POSTGRES_HOST')
        port = os.getenv('POSTGRES_PORT')
        dbname = os.getenv('POSTGRES_DB')
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')

        # Attempt to connect to PostgreSQL
        conn = connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        conn.close()
        print('PostgreSQL is running.')
    except OperationalError as e:
        print(f'Error connecting to PostgreSQL: {e}')
        exit(1)

if __name__ == '__main__':
    check_postgres_connection()
