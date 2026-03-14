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
