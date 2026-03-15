"""ChromaDB wrapper for storing and querying card documentation chunks.

Provides functions to manage a ChromaDB collection for card documentation
with support for metadata filtering and semantic search.
"""

import chromadb

_collection: chromadb.Collection | None = None


def get_collection(persist_dir: str) -> chromadb.Collection:
    """Get or create the ChromaDB collection.

    Args:
        persist_dir: Directory path for persistent storage.

    Returns:
        ChromaDB collection instance for card chunks.
    """
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=persist_dir)
        _collection = client.get_or_create_collection(
            name="caixabank_cards",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def index_chunks(
    chunks: list[dict],
    embeddings: list[list[float]],
    persist_dir: str,
) -> None:
    """Insert chunks with embeddings into the collection.

    Args:
        chunks: List of chunk dictionaries with metadata.
        embeddings: List of embedding vectors corresponding to chunks.
        persist_dir: Directory path for persistent storage.
    """
    collection = get_collection(persist_dir)
    collection.add(
        ids=[f"chunk_{chunk_index}" for chunk_index in range(len(chunks))],
        embeddings=embeddings,
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {
                "card_name": chunk["card_name"],
                "category": chunk["category"],
                "tier": chunk["tier"],
                "source_file": chunk["source_file"],
                "chunk_type": chunk["chunk_type"],
            }
            for chunk in chunks
        ],
    )


def query_by_card_names(
    card_names: list[str],
    persist_dir: str,
    max_results: int = 5,
) -> list[dict]:
    """Retrieve chunks by exact card name (metadata filter).

    Args:
        card_names: List of card names to search for.
        persist_dir: Directory path for persistent storage.
        max_results: Maximum number of results to return.

    Returns:
        List of results with text and metadata.
    """
    collection = get_collection(persist_dir)
    where_filter: dict
    if len(card_names) == 1:
        where_filter = {"card_name": card_names[0]}
    else:
        where_filter = {"card_name": {"$in": card_names}}

    results = collection.get(
        where=where_filter,
        limit=max_results,
        include=["documents", "metadatas"],
    )
    return [{"text": doc, "metadata": meta} for doc, meta in zip(results["documents"], results["metadatas"])]


def query_semantic(
    query_embedding: list[float],
    persist_dir: str,
    max_results: int = 5,
) -> list[dict]:
    """Semantic search by similarity.

    Args:
        query_embedding: Query vector for similarity search.
        persist_dir: Directory path for persistent storage.
        max_results: Maximum number of results to return.

    Returns:
        List of results with text, metadata, and distance score.
    """
    collection = get_collection(persist_dir)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=max_results,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"text": doc, "metadata": meta, "distance": dist}
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]
