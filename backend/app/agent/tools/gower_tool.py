"""Tool: search for similar cards using Gower distance.

Finds credit cards closest to user preferences based on spending patterns
and financial profile using Gower distance metric.
"""

from dataclasses import asdict
from typing import Any

from app.agent.data.card_registry import CARD_REGISTRY
from app.services.gower_service import find_similar_cards

# Campos que no se usan en la comparación Gower
_EXCLUDE_KEYS = {"nombre"}


def search_similar_cards(
    categoria: str | None = None,
    tier: str | None = None,
    cuota_anual: float | None = None,
    ingreso_minimo: float | None = None,
    cashback_pct: float | None = None,
    limite_credito: float | None = None,
    tipo_tarjeta: str | None = None,
    seguro_viaje: float | None = None,
    seguro_equipaje: float | None = None,
    salas_vip: int | None = None,
    puntos_por_euro: float | None = None,
) -> list[dict[str, Any]]:
    """Search for cards most similar to an ideal card using Gower distance.

    Build the ideal card by setting only the features that matter for this
    search.  Features left as None are excluded from the distance calculation,
    so Gower only compares the dimensions the model considers relevant.

    Returns the up to 3 cards closest to the ideal card profile.

    Args:
        categoria: Card category
            (viajes, compras_online, supermercado, restaurante_ocio, clasica).
        tier: Desired card tier (basico, medio, premium).
        cuota_anual: Maximum acceptable annual fee in euros.
        ingreso_minimo: Minimum required income in euros.
        cashback_pct: Desired cashback percentage.
        limite_credito: Desired credit limit in euros.
        tipo_tarjeta: Card type (debito, credito, debito_credito).
        seguro_viaje: Desired travel insurance coverage in euros.
        seguro_equipaje: Desired luggage insurance coverage in euros.
        salas_vip: Desired number of VIP lounge accesses per year.
        puntos_por_euro: Desired loyalty points earned per euro spent.

    Returns:
        List of up to 3 card dictionaries sorted by similarity score.
    """
    # Pre-filtrar por categoría si se especifica
    if categoria is not None:
        filtered = [card for card in CARD_REGISTRY if card.categoria == categoria]
        if not filtered:
            filtered = CARD_REGISTRY
    else:
        filtered = CARD_REGISTRY

    # Feature keys = todas las keys del registro excepto "nombre"
    feature_keys = sorted(filtered[0].feature_dict(exclude=_EXCLUDE_KEYS))

    # Construir tarjeta ideal solo con los campos que el modelo proporcionó
    provided: dict[str, Any] = {
        "categoria": categoria,
        "tier": tier,
        "cuota_anual": cuota_anual,
        "ingreso_minimo": ingreso_minimo,
        "cashback_pct": cashback_pct,
        "limite_credito": limite_credito,
        "tipo_tarjeta": tipo_tarjeta,
        "seguro_viaje": seguro_viaje,
        "seguro_equipaje": seguro_equipaje,
        "salas_vip": salas_vip,
        "puntos_por_euro": puntos_por_euro,
    }
    ideal = {
        key: provided[key] for key in feature_keys if provided.get(key) is not None
    }

    available = [card.feature_dict(exclude=_EXCLUDE_KEYS) for card in filtered]

    results = find_similar_cards(
        ideal_card=ideal,
        available_cards=available,
        threshold=0.0,
        max_results=3,
    )

    output: list[dict[str, Any]] = []
    for result in results:
        for card in filtered:
            card_features = card.feature_dict(exclude=_EXCLUDE_KEYS)
            if all(
                _values_match(card_features.get(key), result.get(key))
                for key in feature_keys
            ):
                output.append(asdict(card))
                break

    return output


def _values_match(a: object, b: object) -> bool:
    """Compare two values with tolerance for floats."""
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) < 1e-9
    return a == b
