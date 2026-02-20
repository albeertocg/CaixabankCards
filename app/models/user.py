"""
Modelo de Usuario para la aplicación de tarjetas bancarias
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class MaritalStatus(str, Enum):
    SINGLE = "soltero"
    MARRIED = "casado"
    DIVORCED = "divorciado"
    WIDOWED = "viudo"


class EducationLevel(str, Enum):
    PRIMARY = "primaria"
    SECONDARY = "secundaria"
    HIGH_SCHOOL = "bachillerato"
    VOCATIONAL = "fp"
    UNIVERSITY = "universidad"
    POSTGRADUATE = "postgrado"


class EmploymentStatus(str, Enum):
    EMPLOYED = "empleado_cuenta_ajena"
    SELF_EMPLOYED = "empleado_cuenta_propia"
    UNEMPLOYED = "desempleado"
    STUDENT = "estudiante"
    RETIRED = "jubilado"


class User(BaseModel):
    """
    Modelo de usuario/cliente del banco
    """
    # Personal data
    national_id: str = Field(..., description="DNI del cliente")
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\+?[0-9]{9,15}$')
    birth_date: datetime
    
    # Address
    address: str
    city: str
    postal_code: str
    province: str
    
    # Socioeconomic information
    annual_income: float = Field(..., ge=0, description="Ingresos anuales en euros")
    employment_status: EmploymentStatus
    education_level: EducationLevel
    marital_status: MaritalStatus
    num_dependents: int = Field(default=0, ge=0, description="Número de personas a cargo")
    
    # Banking information
    customer_tenure_months: int = Field(..., ge=0, description="Meses como cliente del banco")
    contracted_products: list[str] = Field(default_factory=list, description="Productos bancarios contratados")
    average_balance: float = Field(..., ge=0, description="Saldo promedio de cuenta en euros")
    
    # Scoring and risk
    credit_score: int = Field(..., ge=300, le=850, description="Score de crédito (300-850)")
    has_debts: bool = Field(default=False)
    debt_amount: float = Field(default=0.0, ge=0)
    
    # Metadata
    registration_date: datetime = Field(default_factory=datetime.now)
    active: bool = Field(default=True)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "national_id": "12345678A",
                "first_name": "Juan",
                "last_name": "García López",
                "email": "juan.garcia@example.com",
                "phone": "+34612345678",
                "birth_date": "1985-05-15T00:00:00",
                "address": "Calle Mayor 123, 3º B",
                "city": "Madrid",
                "postal_code": "28013",
                "province": "Madrid",
                "annual_income": 35000.0,
                "employment_status": "empleado_cuenta_ajena",
                "education_level": "universidad",
                "marital_status": "casado",
                "num_dependents": 2,
                "customer_tenure_months": 48,
                "contracted_products": ["cuenta_corriente", "cuenta_ahorro"],
                "average_balance": 5000.0,
                "credit_score": 720,
                "has_debts": False,
                "debt_amount": 0.0,
                "registration_date": "2024-01-01T00:00:00",
                "active": True
            }
        }
