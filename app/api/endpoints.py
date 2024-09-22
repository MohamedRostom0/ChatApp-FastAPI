from fastapi import APIRouter, Depends
from app.core.middlewares import authenticate


router = APIRouter()

@router.get("/users/me")
async def get_me(user = Depends(authenticate)):    
    return user