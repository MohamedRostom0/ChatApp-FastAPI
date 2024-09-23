from fastapi import APIRouter, HTTPException, Depends, status, WebSocket, WebSocketDisconnect
import websockets
from app.core.middlewares import authenticate
from app.models.chat import Message, MessageStatus
from app.services.user_service import UserService
from app.models.user import User
from app.services.chat_service import ChatService
from datetime import datetime
from app.core.middlewares import authenticate


router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/{user_id}", response_model=list[Message])
async def get_chat(user_id: str, user: User = Depends(authenticate), chat_service: ChatService = Depends(ChatService)):
    if user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User {user_id} cannot access resources of user {user.id}")

    messages = await chat_service.get_chat_by_userId(user_id)
    return messages


@router.websocket("/ws")
async def websocket_endpoint_v2(websocket: WebSocket, token: str, user_service: UserService = Depends(UserService), chat_service: ChatService = Depends(ChatService)):
    await websocket.accept()
    uri = "wss://echo.websocket.org"

    try:
        user = await authenticate(token, user_service)
        
        async with websockets.connect(uri) as external_ws:
            while True:
                client_message = await websocket.receive_text()
                print(f"Message received from client: {client_message}")
                await chat_service.create_message(Message(message=client_message, user_id=user.id, status=MessageStatus.SENT, timestamp=datetime.now()))

                
                # Send the client's message to the external WebSocket server
                await external_ws.send(client_message)
                
                # Receive the echoed message from the external WebSocket server
                echoed_message = await external_ws.recv()
                print(f"Message received from echo server: {echoed_message}")
                await chat_service.create_message(Message(message=echoed_message, user_id=user.id, status=MessageStatus.RECEIVED, timestamp=datetime.now()))
                
                # Send the echoed message back to the client
                await websocket.send_text(f"Echo: {echoed_message}")
    
    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()
