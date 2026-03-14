from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import TransactionCategory, TransactionType


class Transaction(BaseModel):
    date: datetime = Field(..., description="Fecha de la transaccion")
    concept: str = Field(..., min_length=1, max_length=200, description="Concepto de la transaccion")
    amount: float = Field(
        ...,
        description="Cantidad (positiva para ingresos, negativa para gastos)",
    )
    transaction_type: TransactionType
    category: TransactionCategory
    merchant: str | None = Field(None, description="Comercio o entidad")
