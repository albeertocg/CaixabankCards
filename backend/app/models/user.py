from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, timezone


class UserBase(BaseModel):
    national_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_date: datetime
    address: str
    city: str
    postal_code: str
    province: str
    annual_income: float
    employment_status: str
    education_level: str
    marital_status: str
    num_dependents: int
    customer_tenure_months: int
    contracted_products: list = []
    average_balance: float
    credit_score: int
    has_debts: bool
    debt_amount: float
    registration_date: datetime
    active: bool = True


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: Optional[str] = Field(None, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserResponse(UserBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
