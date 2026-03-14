from fastapi import APIRouter, HTTPException

from app.dtos.user import UserCreate
from app.errors.duplicate_email_error import DuplicateEmailError
from app.errors.duplicate_national_id_error import DuplicateNationalIdError
from app.errors.invalid_credentials_error import InvalidCredentialsError
from app.schemas.auth import LoginRequest, LoginResponse, RegisterResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/register", response_model=RegisterResponse)
async def register(user_data: UserCreate) -> RegisterResponse:
    try:
        user = await auth_service.register(user_data)
        return RegisterResponse(message="Usuario registrado correctamente", user=user)
    except (DuplicateEmailError, DuplicateNationalIdError) as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest) -> LoginResponse:
    try:
        return await auth_service.login(login_data.email, login_data.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))
