from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import EducationLevel, EmploymentStatus, MaritalStatus
from app.models.transaction import Transaction


class UserBase(BaseModel):
    # Datos personales
    national_id: str = Field(..., description="DNI del cliente")
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r"^\+?[0-9]{9,15}$")
    birth_date: datetime

    # Direccion
    address: str
    city: str
    postal_code: str
    province: str

    # Informacion socioeconomica
    annual_income: float = Field(..., ge=0, description="Ingresos anuales en euros")
    employment_status: EmploymentStatus
    education_level: EducationLevel
    marital_status: MaritalStatus
    num_dependents: int = Field(default=0, ge=0, description="Numero de personas a cargo")

    # Informacion bancaria
    customer_tenure_months: int = Field(..., ge=0, description="Meses como cliente del banco")
    contracted_products: list[str] = Field(default_factory=list, description="Productos bancarios contratados")
    average_balance: float = Field(..., ge=0, description="Saldo promedio de cuenta en euros")

    # Scoring y riesgo
    credit_score: int = Field(..., ge=300, le=850, description="Score de credito (300-850)")
    has_debts: bool = Field(default=False)
    debt_amount: float = Field(default=0.0, ge=0)

    # Transacciones
    transactions: list[Transaction] = Field(default_factory=list, description="Historial de movimientos")

    # Metadata
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = Field(default=True)

    model_config = ConfigDict(populate_by_name=True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Contrasena del usuario")


class UserInDB(UserBase):
    id: str | None = Field(None, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserResponse(UserBase):
    id: str
    created_at: datetime | None = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
