import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

def generate_token(user_id):
    """
    Generate a JWT token for the given user ID.

    :param user_id: The ID of the user
    :return: A JWT token as a string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow(), 
        "aud": 'horariosFIUM2025'
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Example usage
if __name__ == "__main__":
    user_id = 12345  # Replace with the actual user ID
    token = generate_token(user_id)
    print(f"Generated token: {token}")