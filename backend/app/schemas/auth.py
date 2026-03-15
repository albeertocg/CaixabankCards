from pydantic import BaseModel, EmailStr

from app.dtos.user import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginUserInfo(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: LoginUserInfo


class RegisterResponse(BaseModel):
    user: UserResponse
