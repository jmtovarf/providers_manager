from datetime import datetime, timedelta
from jose import jwt, JWTError
from functools import wraps

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse

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


# Define the decorator
def check_jwt_auth(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        try:
            # Get the token from the session
            stored_token = request.session.get("token")
            if not stored_token:
                return RedirectResponse(url=request.url_for("index"))
            jwt.decode(stored_token, SECRET_KEY)
        except JWTError as e:
            raise HTTPException(status_code=400, detail=f"Invalid token: {e}")
        except KeyError:
            raise HTTPException(status_code=401, detail="Authorization Required")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return await func(request, *args, **kwargs)

    return wrapper
