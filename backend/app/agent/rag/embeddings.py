"""Wrapper for generating embeddings with Google GenAI API.

Provides functions to generate dense vector embeddings for texts using
Google's embedding model.
"""

from google import genai

_client: genai.Client | None = None


def _get_client(api_key: str) -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=api_key)
    return _client


def embed_texts(texts: list[str], api_key: str) -> list[list[float]]:
    """Generate embeddings for a list of texts.

    Args:
        texts: List of text strings to embed.
        api_key: Google API key for authentication.

    Returns:
        List of embedding vectors (each vector is a list of floats).
    """
    client = _get_client(api_key)
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
    )
    return [list(embedding.values) for embedding in result.embeddings]


def embed_query(query: str, api_key: str) -> list[float]:
    """Generate embedding for a single query string.

    Args:
        query: Query text to embed.
        api_key: Google API key for authentication.

    Returns:
        Embedding vector as a list of floats.
    """
    return embed_texts([query], api_key)[0]
