from datetime import datetime, timedelta
from app.core.config import settings
from jose import JWTError, jwt

def create_jwt_token(data: dict, expiresIn: timedelta = None):
    if expiresIn:
        expiry = datetime.now() + expiresIn
    else:
        expiry = datetime.now() + timedelta(minutes=settings.jwt_expiry)

    data.update({"exp": expiry})
    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        return payload
    
    except JWTError:
        return None