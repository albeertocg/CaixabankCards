from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt
from dotenv import load_dotenv
import os

from app.models.user import UserCreate
from app.repositories.user_repository import UserRepository

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave_secreta_por_defecto")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def hash_password(self, password: str) -> str:
        """Hashear la contraseña con bcrypt."""
        pwd_bytes = password.encode("utf-8")[:72]
        return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña contra el hash."""
        pwd_bytes = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))

    def create_token(self, user_id: str, email: str) -> str:
        """Generar un JWT token."""
        payload = {
            "sub": user_id,
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    async def register(self, user_data: UserCreate) -> dict:
        """Registrar un nuevo usuario."""
        # Verificar si ya existe el email
        existing = await self.user_repo.find_by_email(user_data.email)
        if existing:
            raise ValueError("El email ya está registrado")

        # Verificar si ya existe el DNI
        existing_dni = await self.user_repo.find_by_national_id(user_data.national_id)
        if existing_dni:
            raise ValueError("El DNI/NIE ya está registrado")

        # Preparar documento para MongoDB
        user_dict = user_data.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.hash_password(password)
        user_dict["created_at"] = datetime.now(timezone.utc)

        # Guardar en la BD
        created_user = await self.user_repo.create(user_dict)
        return created_user

    async def login(self, email: str, password: str) -> dict:
        """Autenticar usuario y devolver token."""
        user = await self.user_repo.find_by_email(email)
        if not user:
            raise ValueError("Email o contraseña incorrectos")

        if not self.verify_password(password, user["hashed_password"]):
            raise ValueError("Email o contraseña incorrectos")

        token = self.create_token(user["_id"], user["email"])

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["_id"],
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
            },
        }
