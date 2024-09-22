from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import UserService
from app.utils.jwt import create_jwt_token
from app.utils.hash import verify_password
from app.core.config import settings
from app.schemas.auth import LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, user_service: UserService = Depends(UserService)):
    user = await user_service.get_user_by_email(user_data.email)
    if user:
        raise HTTPException(status_code=400, detail=f"Email: {user_data.email} is already registered")

    user = await user_service.create_user(user_data)
    return UserResponse(id=str(user.id), username=user.username, email=user.email)


@router.post("/login", response_model=LoginResponse)
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
    
    return LoginResponse(access_token=access_token, token_type="Bearer")