from app.db.mongodb import get_db
from app.models.chat import Message

class ChatService:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['messages']

    async def create_message(self, message: Message):
        createdMessage = self.collection.insert_one(message.dict(exclude = {"_id"}))
        return createdMessage
    

    async def get_chat_by_userId(self, userId: str):
        cursor = self.collection.find({"user_id": userId})
        
        messages = []
        # messages = [Message(**message) for message in cursor]
        for message in cursor:
            messages.append(Message(id=str(message['_id']), message=message['message'], user_id=message['user_id'], timestamp=message['timestamp'], status=message['status']))

        return messages