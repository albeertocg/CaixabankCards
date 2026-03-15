"""Structured registry of 15 CaixaBank credit cards for similarity matching.

This module contains the card database used for Gower distance calculations
to find cards similar to user preferences.
"""

from dataclasses import dataclass, fields


@dataclass(frozen=True, slots=True)
class Card:
    """CaixaBank credit card with all features for similarity matching."""

    nombre: str
    categoria: str
    tier: str
    cuota_anual: float
    ingreso_minimo: float
    cashback_pct: float
    limite_credito: float
    tipo_tarjeta: str
    seguro_viaje: float
    seguro_equipaje: float
    salas_vip: int
    puntos_por_euro: float

    def feature_dict(self, *, exclude: set[str] | None = None) -> dict:
        """Return card features as a dict, optionally excluding fields.

        Args:
            exclude: Field names to exclude from the result.

        Returns:
            Dictionary of field name to value.
        """
        exclude = exclude or set()
        return {f.name: getattr(self, f.name) for f in fields(self) if f.name not in exclude}


CARD_REGISTRY: list[Card] = [
    # === VIAJES ===
    Card(
        nombre="CaixaBank Travel Classic",
        categoria="viajes",
        tier="basico",
        cuota_anual=0,
        ingreso_minimo=0,
        cashback_pct=0.5,
        limite_credito=3000,
        tipo_tarjeta="credito",
        seguro_viaje=30000,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=0,
    ),
    Card(
        nombre="CaixaBank Travel Gold",
        categoria="viajes",
        tier="medio",
        cuota_anual=50,
        ingreso_minimo=24000,
        cashback_pct=1.5,
        limite_credito=12000,
        tipo_tarjeta="credito",
        seguro_viaje=100000,
        seguro_equipaje=2000,
        salas_vip=4,
        puntos_por_euro=2,
    ),
    Card(
        nombre="CaixaBank Travel Platinum",
        categoria="viajes",
        tier="premium",
        cuota_anual=120,
        ingreso_minimo=60000,
        cashback_pct=3.0,
        limite_credito=30000,
        tipo_tarjeta="credito",
        seguro_viaje=500000,
        seguro_equipaje=5000,
        salas_vip=999,
        puntos_por_euro=3,
    ),
    # === COMPRAS ONLINE ===
    Card(
        nombre="CaixaBank E-Commerce Basic",
        categoria="compras_online",
        tier="basico",
        cuota_anual=0,
        ingreso_minimo=0,
        cashback_pct=0.5,
        limite_credito=2000,
        tipo_tarjeta="debito_credito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=0,
    ),
    Card(
        nombre="CaixaBank E-Commerce Advanced",
        categoria="compras_online",
        tier="medio",
        cuota_anual=20,
        ingreso_minimo=18000,
        cashback_pct=2.0,
        limite_credito=8000,
        tipo_tarjeta="credito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=0.5,
    ),
    Card(
        nombre="CaixaBank E-Commerce Premium",
        categoria="compras_online",
        tier="premium",
        cuota_anual=60,
        ingreso_minimo=36000,
        cashback_pct=4.0,
        limite_credito=20000,
        tipo_tarjeta="credito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=2,
    ),
    # === SUPERMERCADO ===
    Card(
        nombre="CaixaBank SuperCompra Ahorro",
        categoria="supermercado",
        tier="basico",
        cuota_anual=0,
        ingreso_minimo=0,
        cashback_pct=2.0,
        limite_credito=500,
        tipo_tarjeta="debito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=0,
    ),
    Card(
        nombre="CaixaBank SuperCompra Familia",
        categoria="supermercado",
        tier="medio",
        cuota_anual=15,
        ingreso_minimo=20000,
        cashback_pct=3.0,
        limite_credito=5000,
        tipo_tarjeta="credito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=1,
    ),
    Card(
        nombre="CaixaBank SuperCompra Gourmet",
        categoria="supermercado",
        tier="premium",
        cuota_anual=50,
        ingreso_minimo=40000,
        cashback_pct=5.0,
        limite_credito=15000,
        tipo_tarjeta="credito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=2,
    ),
    # === RESTAURANTE / OCIO ===
    Card(
        nombre="CaixaBank Ocio Joven",
        categoria="restaurante_ocio",
        tier="basico",
        cuota_anual=0,
        ingreso_minimo=0,
        cashback_pct=2.0,
        limite_credito=1500,
        tipo_tarjeta="debito_credito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=1,
    ),
    Card(
        nombre="CaixaBank Ocio Lifestyle",
        categoria="restaurante_ocio",
        tier="medio",
        cuota_anual=30,
        ingreso_minimo=24000,
        cashback_pct=4.0,
        limite_credito=8000,
        tipo_tarjeta="credito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=2,
    ),
    Card(
        nombre="CaixaBank Ocio Exclusive",
        categoria="restaurante_ocio",
        tier="premium",
        cuota_anual=100,
        ingreso_minimo=60000,
        cashback_pct=6.0,
        limite_credito=25000,
        tipo_tarjeta="credito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=3,
    ),
    # === CLASICAS ===
    Card(
        nombre="CaixaBank Clasica",
        categoria="clasica",
        tier="basico",
        cuota_anual=0,
        ingreso_minimo=0,
        cashback_pct=0.5,
        limite_credito=1000,
        tipo_tarjeta="debito",
        seguro_viaje=0,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=0,
    ),
    Card(
        nombre="CaixaBank Oro",
        categoria="clasica",
        tier="medio",
        cuota_anual=40,
        ingreso_minimo=24000,
        cashback_pct=1.5,
        limite_credito=10000,
        tipo_tarjeta="credito",
        seguro_viaje=60000,
        seguro_equipaje=0,
        salas_vip=0,
        puntos_por_euro=0.5,
    ),
    Card(
        nombre="CaixaBank Infinite",
        categoria="clasica",
        tier="premium",
        cuota_anual=200,
        ingreso_minimo=90000,
        cashback_pct=3.0,
        limite_credito=30000,
        tipo_tarjeta="credito",
        seguro_viaje=1000000,
        seguro_equipaje=3000,
        salas_vip=999,
        puntos_por_euro=3,
    ),
]
