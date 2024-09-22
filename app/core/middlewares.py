from fastapi import Depends, HTTPException, status
from jose import JWTError
from app.schemas.auth import oauth2_scheme
from app.utils.jwt import decode_jwt_token
from app.services.user_service import UserService
from app.models.user import User


async def authenticate(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(UserService)) -> User:
    try:
        payload, email = decode_jwt_token(token), None
        if payload:
            email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    
        user = await user_service.get_user_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")