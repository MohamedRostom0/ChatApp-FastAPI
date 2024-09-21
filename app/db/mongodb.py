from pymongo.mongo_client import MongoClient
from app.core.config import settings  # Import the settings object

uri = settings.mongo_uri

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.chat_api_db

def get_db():
    return db