from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class LoginResponse(BaseModel):
    access_token: str
    token_type: str