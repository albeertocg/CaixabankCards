from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from app.models.user import UserCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Auth"])
auth_service = AuthService()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(user_data: UserCreate):
    """Registrar un nuevo usuario."""
    try:
        user = await auth_service.register(user_data)
        # No devolver la contraseña hasheada
        user.pop("hashed_password", None)
        return {"message": "Usuario registrado correctamente", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(login_data: LoginRequest):
    """Iniciar sesión y obtener token JWT."""
    try:
        result = await auth_service.login(login_data.email, login_data.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
