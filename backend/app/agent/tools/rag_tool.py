"""Tool: retrieve detailed card documentation (RAG).

Retrieves comprehensive card documentation including benefits, fees,
requirements, and use cases using semantic search.
"""

from app.agent.rag.embeddings import embed_query
from app.agent.rag.vectorstore import query_by_card_names, query_semantic
from app.config.settings import settings

_PERSIST_DIR: str | None = None


def _get_persist_dir() -> str:
    global _PERSIST_DIR
    if _PERSIST_DIR is None:
        from pathlib import Path

        _PERSIST_DIR = str(Path(__file__).resolve().parents[2] / "agent" / "vectorstore_data")
    return _PERSIST_DIR


def retrieve_card_documentation(card_names: str) -> str:
    """Retrieve detailed documentation for specified cards.

    Includes benefits, fees, requirements, and use cases for each card.
    Uses both exact metadata matching and semantic search.

    Args:
        card_names: Comma-separated card names.
            Example: "CaixaBank Travel Gold, CaixaBank Oro"

    Returns:
        Formatted documentation text for the requested cards.
    """
    persist_dir = _get_persist_dir()
    names = [card_name.strip() for card_name in card_names.split(",") if card_name.strip()]

    # Búsqueda por metadata exacta
    results = query_by_card_names(names, persist_dir, max_results=len(names) * 2)

    # Si no encontramos todas, complementar con búsqueda semántica
    found_names = {result["metadata"]["card_name"] for result in results}
    missing = [card_name for card_name in names if card_name not in found_names]
    if missing:
        query = ", ".join(missing)
        query_emb = embed_query(query, api_key=settings.google_api_key)
        semantic_results = query_semantic(query_emb, persist_dir, max_results=3)
        results.extend(semantic_results)

    if not results:
        return f"No se encontró documentación para: {', '.join(names)}"

    # Concatenar textos sin duplicados
    seen: set[str] = set()
    sections: list[str] = []
    for result in results:
        text = result["text"]
        card = result["metadata"]["card_name"]
        if card not in seen:
            seen.add(card)
            sections.append(text)

    return "\n\n---\n\n".join(sections)
