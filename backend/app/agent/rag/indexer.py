"""Index card documentation at startup into vector store.

Handles loading card markdown documents, chunking them, generating embeddings,
and storing them in ChromaDB for retrieval-augmented generation.
"""

import logging
from pathlib import Path

from app.agent.rag.chunker import chunk_card_documents
from app.agent.rag.embeddings import embed_texts
from app.agent.rag.vectorstore import get_collection, index_chunks
from app.config.settings import settings

logger = logging.getLogger(__name__)

_AGENT_DIR = Path(__file__).resolve().parents[1]
CARDS_DIR = str(_AGENT_DIR / "data" / "cards")
PERSIST_DIR = str(_AGENT_DIR / "vectorstore_data")


def ensure_indexed() -> None:
    """Index card documentation if collection is empty.

    Loads card markdown files from disk, chunks them, generates embeddings,
    and indexes them in ChromaDB. Skips if collection already has documents.
    """
    collection = get_collection(PERSIST_DIR)

    if collection.count() > 0:
        logger.info("RAG: colección ya indexada (%d docs), saltando.", collection.count())
        return

    logger.info("RAG: indexando documentación de tarjetas desde %s", CARDS_DIR)
    chunks = chunk_card_documents(CARDS_DIR)

    if not chunks:
        logger.warning("RAG: no se encontraron chunks para indexar.")
        return

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts, api_key=settings.google_api_key)
    index_chunks(chunks, embeddings, PERSIST_DIR)
    logger.info("RAG: indexados %d chunks correctamente.", len(chunks))
