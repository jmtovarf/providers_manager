from datetime import datetime, timedelta
from jose import jwt

from settings import SECRET_KEY

# Function to create JWT token
def create_jwt_token(email: str, id: int) -> str:
    # Define the payload
    payload = {
        "sub": email,
        "id": id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    # Encode the payload and return the JWT token
    return jwt.encode(payload, SECRET_KEY)
