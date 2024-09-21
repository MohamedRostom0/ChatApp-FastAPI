from pydantic import BaseSettings
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

class Settings(BaseSettings):
    mongo_uri: str = os.getenv("MONGO_URI")
    secret_key: str = os.getenv("SECRET_KEY")
    debug: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")
    algorithm: str = os.getenv("ALGORITHM")
    jwt_expiry: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


# Create a settings object that can be imported elsewhere in the app
settings = Settings()
