# from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.hash import hash_password
from app.db.mongodb import get_db

class UserService:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["users"]

    async def create_user(self, userData: UserCreate):
        hashed_password = hash_password(userData.password)
        user = User(username=userData.username, email=userData.email, hashed_password=hashed_password)

        createdUser = self.collection.insert_one(user.dict(exclude={"id"}))
        user.id = createdUser.inserted_id

        return user
    

    async def get_user_by_email(self, email: str):
        user = self.collection.find_one({"email": email})
        if user:
            return User(**user)
        
        return None
    

