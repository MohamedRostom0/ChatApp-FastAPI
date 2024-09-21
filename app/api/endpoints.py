from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils.jwt import decode_jwt_token
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import UserService
from app.utils.jwt import create_jwt_token
from app.utils.hash import verify_password
from app.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, user_service: UserService = Depends(UserService)):
    user = await user_service.get_user_by_email(user_data.email)
    if user:
        raise HTTPException(status_code=400, detail=f"Email: {user_data.email} is already registered")

    user = await user_service.create_user(user_data)
    return UserResponse(id=str(user.id), username=user.username, email=user.email)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(UserService)):
    user = await user_service.get_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.jwt_expiry)
    access_token = create_jwt_token(data={"sub": user.email}, expiresIn=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse)
async def get_me(token:str = Depends(oauth2_scheme), user_service: UserService = Depends(UserService)):
    payload = decode_jwt_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"},)
    
    user = await user_service.get_user_by_email(payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    return UserResponse(id=str(user.id), username=user.username, email=user.email)
