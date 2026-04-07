from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.config.settings import settings
from app.dtos.user import UserCreate, UserResponse
from app.errors.duplicate_email_error import DuplicateEmailError
from app.errors.duplicate_national_id_error import DuplicateNationalIdError
from app.errors.invalid_credentials_error import InvalidCredentialsError
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginResponse, LoginUserInfo

_user_repo = UserRepository()


# =========================
# Public API
# =========================
async def register(user_data: UserCreate) -> UserResponse:
    """Register a new user.

    Args:
        user_data: User registration payload (includes plain-text password).

    Returns:
        The created user without sensitive fields.

    Raises:
        DuplicateEmailError: If the email is already registered.
        DuplicateNationalIdError: If the DNI/NIE is already registered.
    """
    existing = await _user_repo.find_by_email(user_data.email)
    if existing:
        raise DuplicateEmailError("El email ya esta registrado")

    existing_dni = await _user_repo.find_by_national_id(user_data.national_id)
    if existing_dni:
        raise DuplicateNationalIdError("El DNI/NIE ya esta registrado")

    user_dict = user_data.model_dump(mode="json")
    password = user_dict.pop("password")
    user_dict["hashed_password"] = _hash_password(password)
    user_dict["created_at"] = datetime.now(timezone.utc).isoformat()

    created_user = await _user_repo.create(user_dict)

    return UserResponse(
        id=created_user["_id"],
        created_at=created_user.get("created_at"),
        **{
            k: v
            for k, v in created_user.items()
            if k not in ("_id", "hashed_password", "created_at")
        },
    )


async def login(email: str, password: str) -> LoginResponse:
    """Authenticate a user and return a JWT token.

    Args:
        email: User email address.
        password: Plain-text password to verify.

    Returns:
        A login response containing the access token and basic user info.

    Raises:
        InvalidCredentialsError: If email or password are incorrect.
    """
    user = await _user_repo.find_by_email(email)
    if not user:
        raise InvalidCredentialsError("Email o contrasena incorrectos")

    if not _verify_password(password, user["hashed_password"]):
        raise InvalidCredentialsError("Email o contrasena incorrectos")

    token = _create_token(user["_id"], user["email"])

    return LoginResponse(
        access_token=token,
        user=LoginUserInfo(
            id=user["_id"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
        ),
    )


# =========================
# Private helpers
# =========================
def _hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        password: Plain-text password (max 72 bytes due to bcrypt limitation).

    Returns:
        Bcrypt hashed password string.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash.

    Args:
        plain_password: Plain-text password to verify.
        hashed_password: Bcrypt hash to verify against.

    Returns:
        True if password matches hash, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def _create_token(user_id: str, email: str) -> str:
    """Create a JWT access token for authenticated user.

    Args:
        user_id: User's unique identifier.
        email: User's email address.

    Returns:
        Encoded JWT token string.
    """
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.jwt_expiration_minutes),
    }
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
