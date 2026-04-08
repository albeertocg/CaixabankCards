"""User context builder for agent sessions.

Constructs a formatted text block containing user profile information and transaction
analysis to inject into the agent session at the start of each chat.
"""

from collections import defaultdict
from datetime import datetime, timezone

from app.repositories.user_repository import UserRepository
from app.services.sanitizer import sanitize_text

# Mapeo de categoría de transacción → categoría de tarjeta
_TX_TO_CARD_CATEGORY: dict[str, str] = {
    "viajes": "viajes",
    "transporte": "viajes",
    "compras": "compras_online",
    "supermercado": "supermercado",
    "restaurante": "restaurante_ocio",
    "ocio": "restaurante_ocio",
}

_user_repo = UserRepository()


async def build_user_context(user_id: str) -> str:
    """Build a formatted context block with user profile and transaction analysis.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        A formatted string containing the user's profile and transaction analysis,
        or a message indicating no user information was found.
    """
    user = await _user_repo.find_by_id(user_id)
    if user is None:
        return "No se encontró información del usuario."

    profile = _build_profile(user)
    tx_analysis = _analyze_transactions(user.get("transactions", []))
    return _format_context(profile, tx_analysis)


def _build_profile(user: dict) -> dict:
    """Build a profile dictionary from user data.

    Args:
        user: User document containing demographic and financial information.

    Returns:
        A dictionary with profile information including age, income, employment status, etc.
    """
    age = _calculate_age(user.get("birth_date"))
    return {
        "nombre": sanitize_text(
            f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        ),
        "edad": age,
        "ingreso_anual": user.get("annual_income", 0),
        "situacion_laboral": sanitize_text(
            str(user.get("employment_status", "desconocido"))
        ),
        "nivel_educativo": sanitize_text(
            str(user.get("education_level", "desconocido"))
        ),
        "estado_civil": sanitize_text(str(user.get("marital_status", "desconocido"))),
        "dependientes": user.get("num_dependents", 0),
        "meses_como_cliente": user.get("customer_tenure_months", 0),
        "productos_contratados": len(user.get("contracted_products", [])),
        "saldo_medio": user.get("average_balance", 0),
        "score_crediticio": user.get("credit_score", 0),
        "tiene_deudas": user.get("has_debts", False),
        "importe_deudas": user.get("debt_amount", 0),
    }


def _analyze_transactions(transactions: list[dict]) -> dict:
    """Analyze user transactions to identify spending patterns and card categories.

    Args:
        transactions: List of transaction records with amount, category, and date.

    Returns:
        A dictionary with transaction analysis including dominant spending pattern,
        monthly averages by category, and total spending statistics.
    """
    if not transactions:
        return {
            "tiene_historial": False,
            "patron_dominante": "uso_general",
        }

    spending_by_cat: dict[str, float] = defaultdict(float)
    total_expense = 0.0
    total_income = 0.0
    dates: list[datetime] = []

    for tx in transactions:
        amount = abs(tx.get("amount", 0))
        cat = tx.get("category", "otros_gastos")
        tx_type = tx.get("transaction_type", "gasto")
        if tx.get("date"):
            dates.append(
                tx["date"]
                if isinstance(tx["date"], datetime)
                else datetime.fromisoformat(str(tx["date"]))
            )

        if tx_type == "gasto":
            spending_by_cat[cat] += amount
            total_expense += amount
        else:
            total_income += amount

    # Calcular meses cubiertos
    if len(dates) >= 2:
        span = (max(dates) - min(dates)).days
        months = max(span / 30.0, 1.0)
    else:
        months = 1.0

    monthly_by_cat = {
        cat: round(total / months, 2) for cat, total in spending_by_cat.items()
    }
    sorted_cats = sorted(
        monthly_by_cat.items(), key=lambda spending_info: spending_info[1], reverse=True
    )

    # Agregar por categoría de tarjeta
    card_cat_spend: dict[str, float] = defaultdict(float)
    for cat, amount in monthly_by_cat.items():
        card_cat = _TX_TO_CARD_CATEGORY.get(cat, "clasica")
        card_cat_spend[card_cat] += amount

    dominant = (
        max(card_cat_spend, key=card_cat_spend.get) if card_cat_spend else "clasica"
    )

    return {
        "tiene_historial": True,
        "num_transacciones": len(transactions),
        "meses_analizados": round(months, 1),
        "gasto_mensual_total": round(total_expense / months, 2),
        "ingreso_mensual_total": round(total_income / months, 2),
        "gasto_mensual_por_categoria": monthly_by_cat,
        "top_categorias": sorted_cats[:5],
        "gasto_por_categoria_tarjeta": dict(card_cat_spend),
        "patron_dominante": dominant,
    }


def _format_context(profile: dict, tx_analysis: dict) -> str:
    """Format profile and transaction analysis into a readable text block.

    Args:
        profile: User profile dictionary.
        tx_analysis: Transaction analysis dictionary.

    Returns:
        Formatted text with profile and transaction analysis sections.
    """
    lines = ["=== PERFIL DEL CLIENTE ==="]
    for key, val in profile.items():
        label = key.replace("_", " ").capitalize()
        if isinstance(val, float):
            lines.append(f"{label}: {val:,.2f}€")
        elif isinstance(val, bool):
            lines.append(f"{label}: {'Sí' if val else 'No'}")
        else:
            lines.append(f"{label}: {val}")

    lines.append("")
    lines.append("=== ANÁLISIS DE TRANSACCIONES ===")

    if not tx_analysis.get("tiene_historial"):
        lines.append("Sin historial de transacciones disponible.")
        lines.append("Patrón dominante: USO GENERAL (basado solo en perfil)")
    else:
        lines.append(
            f"Período: {tx_analysis['meses_analizados']} meses ({tx_analysis['num_transacciones']} transacciones)"
        )
        lines.append(f"Gasto mensual medio: {tx_analysis['gasto_mensual_total']:,.2f}€")
        lines.append(
            f"Ingreso mensual medio: {tx_analysis['ingreso_mensual_total']:,.2f}€"
        )
        lines.append("")
        lines.append("Distribución de gasto mensual por categoría:")
        for cat, amount in tx_analysis["top_categorias"]:
            pct = (
                (amount / tx_analysis["gasto_mensual_total"] * 100)
                if tx_analysis["gasto_mensual_total"] > 0
                else 0
            )
            lines.append(f"  - {cat}: {amount:,.2f}€/mes ({pct:.1f}%)")
        lines.append("")
        lines.append(f"Patrón dominante: {tx_analysis['patron_dominante'].upper()}")
        if len(tx_analysis.get("gasto_por_categoria_tarjeta", {})) > 1:
            secondary = sorted(
                tx_analysis["gasto_por_categoria_tarjeta"].items(),
                key=lambda spending_info: spending_info[1],
                reverse=True,
            )
            if len(secondary) > 1:
                lines.append(f"Patrón secundario: {secondary[1][0].upper()}")

    return "\n".join(lines)


def _calculate_age(birth_date: datetime | str | None) -> int:
    """Calculate age from birth date.

    Args:
        birth_date: Birth date as datetime, ISO format string, or None.

    Returns:
        User age in years, or 0 if birth_date is None.
    """
    if birth_date is None:
        return 0
    if isinstance(birth_date, str):
        birth_date = datetime.fromisoformat(birth_date)
    today = datetime.now(timezone.utc)
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
