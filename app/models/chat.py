from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class MessageStatus(str, Enum):
    SENT = 'sent'
    RECEIVED = 'received'

class Message(BaseModel):
    _id: str = None
    message: str
    user_id: str
    timestamp: datetime 
    status: MessageStatus
