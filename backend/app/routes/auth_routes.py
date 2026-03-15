from fastapi import APIRouter, HTTPException

from app.dtos.user import UserCreate
from app.errors.duplicate_email_error import DuplicateEmailError
from app.errors.duplicate_national_id_error import DuplicateNationalIdError
from app.errors.invalid_credentials_error import InvalidCredentialsError
from app.schemas.auth import LoginRequest, LoginResponse, RegisterResponse
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterResponse)
async def register(user_data: UserCreate) -> RegisterResponse:
    """Register a new user account.

    Args:
        user_data: User registration data including email, password, and profile info.

    Returns:
        RegisterResponse with the created user info.

    Raises:
        HTTPException: 409 if email or national ID already registered.
    """
    try:
        user = await auth_service.register(user_data)
        return RegisterResponse(user=user)
    except (DuplicateEmailError, DuplicateNationalIdError) as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest) -> LoginResponse:
    """Authenticate user and return JWT access token.

    Args:
        login_data: Login credentials (email and password).

    Returns:
        LoginResponse with access token and basic user info.

    Raises:
        HTTPException: 401 if email or password are incorrect.
    """
    try:
        return await auth_service.login(login_data.email, login_data.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))
