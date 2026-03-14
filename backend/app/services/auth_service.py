from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.config.settings import settings
from app.dtos.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginResponse, LoginUserInfo


class AuthService:
    def __init__(self) -> None:
        self.user_repo = UserRepository()

    def hash_password(self, password: str) -> str:
        pwd_bytes = password.encode("utf-8")[:72]
        return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pwd_bytes = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))

    def create_token(self, user_id: str, email: str) -> str:
        payload = {
            "sub": user_id,
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiration_minutes),
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    async def register(self, user_data: UserCreate) -> UserResponse:
        existing = await self.user_repo.find_by_email(user_data.email)
        if existing:
            raise ValueError("El email ya esta registrado")

        existing_dni = await self.user_repo.find_by_national_id(user_data.national_id)
        if existing_dni:
            raise ValueError("El DNI/NIE ya esta registrado")

        # Serializar con mode="json" para que enums se conviertan a strings
        user_dict = user_data.model_dump(mode="json")
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.hash_password(password)
        user_dict["created_at"] = datetime.now(timezone.utc).isoformat()

        created_user = await self.user_repo.create(user_dict)

        return UserResponse(
            id=created_user["_id"],
            created_at=created_user.get("created_at"),
            **{k: v for k, v in created_user.items() if k not in ("_id", "hashed_password", "created_at")},
        )

    async def login(self, email: str, password: str) -> LoginResponse:
        user = await self.user_repo.find_by_email(email)
        if not user:
            raise ValueError("Email o contrasena incorrectos")

        if not self.verify_password(password, user["hashed_password"]):
            raise ValueError("Email o contrasena incorrectos")

        token = self.create_token(user["_id"], user["email"])

        return LoginResponse(
            access_token=token,
            user=LoginUserInfo(
                id=user["_id"],
                email=user["email"],
                first_name=user["first_name"],
                last_name=user["last_name"],
            ),
        )
