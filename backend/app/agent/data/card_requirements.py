"""Card eligibility requirements by card name.

Defines minimum income and age requirements for each CaixaBank card,
and organizes cards by category and tier level.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CardRequirements:
    """Income and age requirements for a specific card."""

    ingreso_minimo: float
    edad_minima: int
    edad_maxima: int


CARD_REQUIREMENTS: dict[str, CardRequirements] = {
    # Viajes
    "CaixaBank Travel Classic": CardRequirements(ingreso_minimo=0, edad_minima=18, edad_maxima=999),
    "CaixaBank Travel Gold": CardRequirements(ingreso_minimo=24000, edad_minima=18, edad_maxima=999),
    "CaixaBank Travel Platinum": CardRequirements(ingreso_minimo=60000, edad_minima=18, edad_maxima=999),
    # Compras Online
    "CaixaBank E-Commerce Basic": CardRequirements(ingreso_minimo=0, edad_minima=18, edad_maxima=999),
    "CaixaBank E-Commerce Advanced": CardRequirements(ingreso_minimo=18000, edad_minima=18, edad_maxima=999),
    "CaixaBank E-Commerce Premium": CardRequirements(ingreso_minimo=36000, edad_minima=18, edad_maxima=999),
    # Supermercado
    "CaixaBank SuperCompra Ahorro": CardRequirements(ingreso_minimo=0, edad_minima=18, edad_maxima=999),
    "CaixaBank SuperCompra Familia": CardRequirements(ingreso_minimo=20000, edad_minima=18, edad_maxima=999),
    "CaixaBank SuperCompra Gourmet": CardRequirements(ingreso_minimo=40000, edad_minima=18, edad_maxima=999),
    # Restaurante / Ocio
    "CaixaBank Ocio Joven": CardRequirements(ingreso_minimo=0, edad_minima=18, edad_maxima=30),
    "CaixaBank Ocio Lifestyle": CardRequirements(ingreso_minimo=24000, edad_minima=18, edad_maxima=999),
    "CaixaBank Ocio Exclusive": CardRequirements(ingreso_minimo=60000, edad_minima=18, edad_maxima=999),
    # Clásicas
    "CaixaBank Clasica": CardRequirements(ingreso_minimo=0, edad_minima=18, edad_maxima=999),
    "CaixaBank Oro": CardRequirements(ingreso_minimo=24000, edad_minima=18, edad_maxima=999),
    "CaixaBank Infinite": CardRequirements(ingreso_minimo=90000, edad_minima=18, edad_maxima=999),
}

# Mapa de categoria → tarjetas ordenadas por tier (basico → premium)
CARD_TIERS_BY_CATEGORY: dict[str, list[str]] = {
    "viajes": [
        "CaixaBank Travel Classic",
        "CaixaBank Travel Gold",
        "CaixaBank Travel Platinum",
    ],
    "compras_online": [
        "CaixaBank E-Commerce Basic",
        "CaixaBank E-Commerce Advanced",
        "CaixaBank E-Commerce Premium",
    ],
    "supermercado": [
        "CaixaBank SuperCompra Ahorro",
        "CaixaBank SuperCompra Familia",
        "CaixaBank SuperCompra Gourmet",
    ],
    "restaurante_ocio": [
        "CaixaBank Ocio Joven",
        "CaixaBank Ocio Lifestyle",
        "CaixaBank Ocio Exclusive",
    ],
    "clasica": [
        "CaixaBank Clasica",
        "CaixaBank Oro",
        "CaixaBank Infinite",
    ],
}
