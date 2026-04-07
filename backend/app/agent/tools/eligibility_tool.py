"""Tool: card eligibility verification.

Checks if a user meets requirements for a specific card and suggests
lower-tier alternatives if requirements are not met.
"""

from dataclasses import dataclass

from app.agent.data.card_requirements import CARD_REQUIREMENTS, CARD_TIERS_BY_CATEGORY
from app.agent.data.card_registry import CARD_REGISTRY


@dataclass(frozen=True, slots=True)
class EligibilityResult:
    """Result of a card eligibility check."""

    eligible: bool
    reasons: list[str]
    alternatives: list[str]


def check_card_eligibility(
    card_name: str,
    ingreso_anual: float,
    edad: int,
) -> EligibilityResult:
    """Check if user meets requirements for a specific card.

    If requirements are not met, suggests lower-tier alternatives
    from the same category that the user qualifies for.

    Args:
        card_name: Exact name of the card to verify.
        ingreso_anual: User's annual income in euros.
        edad: User's age in years.

    Returns:
        EligibilityResult with eligible flag, reasons, and alternatives.
    """
    reqs = CARD_REQUIREMENTS.get(card_name)
    if reqs is None:
        return EligibilityResult(
            eligible=False,
            reasons=[f"Tarjeta '{card_name}' no encontrada en el catálogo."],
            alternatives=[],
        )

    reasons: list[str] = []
    if ingreso_anual < reqs.ingreso_minimo:
        reasons.append(
            f"Ingreso anual ({ingreso_anual:,.0f}€) inferior al mínimo "
            f"requerido ({reqs.ingreso_minimo:,.0f}€)."
        )
    if edad < reqs.edad_minima:
        reasons.append(
            f"Edad ({edad}) inferior a la mínima requerida ({reqs.edad_minima})."
        )
    if edad > reqs.edad_maxima:
        reasons.append(
            f"Edad ({edad}) supera la máxima permitida ({reqs.edad_maxima})."
        )

    alternatives: list[str] = []
    if reasons:
        alternatives = _find_lower_tier_alternatives(card_name, ingreso_anual, edad)

    return EligibilityResult(
        eligible=len(reasons) == 0,
        reasons=reasons,
        alternatives=alternatives,
    )


def _find_lower_tier_alternatives(
    card_name: str, ingreso_anual: float, edad: int
) -> list[str]:
    """Find lower-tier cards in the same category that user qualifies for.

    Args:
        card_name: Card name to find alternatives for.
        ingreso_anual: User's annual income in euros.
        edad: User's age in years.

    Returns:
        List of qualified lower-tier card names.
    """
    # Encontrar la categoría de la tarjeta
    category = None
    for card in CARD_REGISTRY:
        if card.nombre == card_name:
            category = card.categoria
            break

    if category is None:
        return []

    tier_list = CARD_TIERS_BY_CATEGORY.get(category, [])
    if card_name not in tier_list:
        return []
    card_index = tier_list.index(card_name)

    alternatives = []
    for name in tier_list[:card_index]:
        reqs = CARD_REQUIREMENTS.get(name)
        if reqs is None:
            continue
        if (
            ingreso_anual >= reqs.ingreso_minimo
            and reqs.edad_minima <= edad <= reqs.edad_maxima
        ):
            alternatives.append(name)

    return alternatives
