from datetime import datetime

from pydantic import ConfigDict, Field

from app.models.user import UserBase


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Contrasena del usuario")


class UserResponse(UserBase):
    id: str
    created_at: datetime | None = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
