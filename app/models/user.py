from pydantic import BaseModel

class User(BaseModel):
    id: str = None  # MongoDB will generate this
    username: str
    email: str
    hashed_password: str