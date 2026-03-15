from enum import Enum


class CardCategory(str, Enum):
    TRAVEL = "viajes"
    ECOMMERCE = "compras_online"
    SUPERMARKET = "supermercado"
    LEISURE = "restaurante_ocio"
    CLASSIC = "clasica"


class CardTier(str, Enum):
    BASIC = "basico"
    MID = "medio"
    PREMIUM = "premium"


# Mapeo fichero .md → categoría de tarjeta
CARD_DOC_FILE_MAP: dict[str, CardCategory] = {
    "01_tarjetas_viajes": CardCategory.TRAVEL,
    "02_tarjetas_compras_online": CardCategory.ECOMMERCE,
    "03_tarjetas_supermercado": CardCategory.SUPERMARKET,
    "04_tarjetas_restaurante_ocio": CardCategory.LEISURE,
    "05_tarjetas_clasicas": CardCategory.CLASSIC,
}

TIER_ORDER: list[CardTier] = [CardTier.BASIC, CardTier.MID, CardTier.PREMIUM]
