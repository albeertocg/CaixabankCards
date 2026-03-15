"""Parse and chunk card documentation markdown files for RAG.

Reads markdown files from docs directory and splits them into chunks
with metadata (card name, category, tier, chunk type) for embedding and retrieval.
"""

import re
from pathlib import Path

from app.constants.card import CARD_DOC_FILE_MAP, TIER_ORDER


def chunk_card_documents(docs_dir: str) -> list[dict]:
    """Parse card markdown files and split them into chunks.

    Args:
        docs_dir: Path to directory containing card markdown files.

    Returns:
        List of chunks, each with text, card_name, category, tier, source_file, chunk_type.
    """
    docs_path = Path(docs_dir)
    chunks: list[dict] = []

    for md_file in sorted(docs_path.glob("*.md")):
        stem = md_file.stem
        category = CARD_DOC_FILE_MAP.get(stem)
        if category is None:
            continue

        content = md_file.read_text(encoding="utf-8")
        chunks.extend(_split_file(content, category.value, md_file.name))

    return chunks


def _split_file(content: str, category: str, filename: str) -> list[dict]:
    """Split markdown file into chunks by level-2 sections.

    Args:
        content: Full markdown file content.
        category: Card category for metadata.
        filename: Source filename for reference.

    Returns:
        List of chunk dictionaries with metadata.
    """
    sections = re.split(r"\n(?=## )", content)
    chunks: list[dict] = []
    card_index = 0

    for section in sections:
        section = section.strip()
        if not section:
            continue

        header_match = re.match(r"^##\s+(.+)", section)
        if not header_match:
            # Intro del documento (título # y texto antes del primer ##)
            continue

        header = header_match.group(1).strip()
        chunk_type, card_name, tier = _classify_section(header, category, card_index)

        if chunk_type == "skip":
            continue

        if chunk_type == "card_detail":
            card_index += 1

        chunks.append(
            {
                "text": section,
                "card_name": card_name,
                "category": category,
                "tier": tier,
                "source_file": filename,
                "chunk_type": chunk_type,
            }
        )

    return chunks


def _classify_section(header: str, category: str, card_index: int) -> tuple[str, str, str]:
    """Classify a section by its header.

    Args:
        header: Header text of the markdown section.
        category: Card category for context.
        card_index: Index of the current card in iteration.

    Returns:
        Tuple of (chunk_type, card_name, tier).
    """
    header_lower = header.lower()

    if "comparativa" in header_lower or "resumen" in header_lower:
        return "comparison", f"Comparativa {category}", ""

    if "preguntas frecuentes" in header_lower or "faq" in header_lower:
        return "faq", f"FAQ {category}", ""

    if "cuándo elegir" in header_lower or "cuando elegir" in header_lower:
        return "guide", f"Guia {category}", ""

    if "índice" in header_lower or "indice" in header_lower:
        return "skip", "", ""

    if "conclusión" in header_lower or "conclusion" in header_lower:
        return "skip", "", ""

    # Es una sección de tarjeta individual
    tier = TIER_ORDER[card_index].value if card_index < len(TIER_ORDER) else "basico"
    # El header suele contener el nombre (ej: "CaixaBank Travel Classic")
    # Extraemos un nombre limpio quitando numeración y emojis
    card_name = re.sub(r"^\d+\.\s*", "", header)
    card_name = re.sub(r"[🏖️🛫💳🛒🍽️⭐🌟✨🔥]+", "", card_name).strip()

    return "card_detail", card_name, tier
