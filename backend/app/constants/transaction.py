from enum import Enum


class TransactionType(str, Enum):
    INCOME = "ingreso"
    EXPENSE = "gasto"


class TransactionCategory(str, Enum):
    SUPERMARKET = "supermercado"
    RESTAURANT = "restaurante"
    TRANSPORT = "transporte"
    ENTERTAINMENT = "ocio"
    HEALTH = "salud"
    SHOPPING = "compras"
    BILLS = "facturas"
    EDUCATION = "educacion"
    TRAVEL = "viajes"
    OTHER_EXPENSE = "otros_gastos"
    SALARY = "nomina"
    TRANSFER = "transferencia"
    OTHER_INCOME = "otros_ingresos"
