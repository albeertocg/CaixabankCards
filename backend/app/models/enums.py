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
