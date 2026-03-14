from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest, LoginResponse, RegisterResponse
from app.dtos.user import UserCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/register", response_model=RegisterResponse)
async def register(user_data: UserCreate) -> RegisterResponse:
    try:
        user = await auth_service.register(user_data)
        return RegisterResponse(message="Usuario registrado correctamente", user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest) -> LoginResponse:
    try:
        return await auth_service.login(login_data.email, login_data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
