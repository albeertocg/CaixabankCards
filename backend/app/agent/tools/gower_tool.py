"""Tool: search for similar cards using Gower distance.

Finds credit cards closest to user preferences based on spending patterns
and financial profile using Gower distance metric.
"""

from typing import Any

from app.agent.data.card_registry import CARD_REGISTRY
from app.services.gower_service import find_similar_cards

# Campos que no se usan en la comparación Gower
_EXCLUDE_KEYS = {"nombre"}


def search_similar_cards(
    categoria_principal: str,
    ingreso_anual: float,
    gasto_mensual: float,
    cuota_maxima: float,
    cashback_minimo: float,
) -> list[dict[str, Any]]:
    """Search for cards most similar to user profile using Gower distance.

    Returns the up to 3 cards closest to the ideal user profile.

    Args:
        categoria_principal: Desired card category
            (viajes, compras_online, supermercado, restaurante_ocio, clasica).
        ingreso_anual: User's annual income in euros.
        gasto_mensual: User's average monthly spending in euros.
        cuota_maxima: Maximum acceptable annual fee in euros.
        cashback_minimo: Minimum desired cashback percentage.

    Returns:
        List of up to 3 card dictionaries sorted by similarity score.
    """
    # Pre-filtrar por categoría para reducir ruido en Gower
    filtered = [card for card in CARD_REGISTRY if card["categoria"] == categoria_principal]
    if not filtered:
        filtered = CARD_REGISTRY

    # Feature keys = todas las keys del registro excepto "nombre"
    feature_keys = [feature_key for feature_key in filtered[0] if feature_key not in _EXCLUDE_KEYS]

    # Construir tarjeta ideal con TODOS los campos (para alineación con Gower)
    ideal: dict[str, Any] = {
        "categoria": categoria_principal,
        "tier": "medio",
        "cuota_anual": cuota_maxima,
        "ingreso_minimo": ingreso_anual,
        "cashback_pct": cashback_minimo,
        "limite_credito": gasto_mensual * 3,
        "tipo_tarjeta": "credito",
        "seguro_viaje": 0,
        "seguro_equipaje": 0,
        "salas_vip": 0,
        "puntos_por_euro": 0,
    }
    # Asegurar que tiene exactamente los mismos keys que las available
    ideal = {feature_key: ideal.get(feature_key, 0) for feature_key in feature_keys}

    available = [{feature_key: card[feature_key] for feature_key in feature_keys} for card in filtered]

    results = find_similar_cards(
        ideal_card=ideal,
        available_cards=available,
        threshold=0.0,
        max_results=3,
    )

    # Re-adjuntar nombre y datos completos del registro original
    output = []
    for result in results:
        for card in filtered:
            if all(card.get(feature_key) == result.get(feature_key) for feature_key in feature_keys):
                output.append(card)
                break

    return output
