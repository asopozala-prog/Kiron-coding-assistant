"""
Kiron retriever.

Searches Kiron's RAG articles directly with MiniLM.
"""

from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


RAG_DIR = Path("legal_files/rag/kiron")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks() -> list[dict[str, str]]:
    """Load Kiron RAG files as searchable chunks."""
    chunks = []

    for file in sorted(RAG_DIR.glob("*.md")):
        if file.name == "00_kiron_mode_rules.md":
            continue

        text = file.read_text(encoding="utf-8").strip()

        if text:
            chunks.append(
                {
                    "source": file.name,
                    "text": text,
                }
            )

    return chunks


def cosine_similarity(query_embedding: np.ndarray, chunk_embeddings: np.ndarray) -> np.ndarray:
    """Calculate cosine similarity."""
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    chunk_norms = chunk_embeddings / np.linalg.norm(chunk_embeddings, axis=1, keepdims=True)
    return np.dot(chunk_norms, query_norm)


def retrieve_kiron_chunks(question: str, top_k: int = 2) -> list[dict[str, str | float]]:
    """Retrieve top Kiron article chunks."""
    chunks = load_chunks()
    model = SentenceTransformer(MODEL_NAME)

    chunk_texts = [chunk["text"] for chunk in chunks]
    chunk_embeddings = model.encode(chunk_texts, convert_to_numpy=True)
    question_embedding = model.encode(question, convert_to_numpy=True)

    scores = cosine_similarity(question_embedding, chunk_embeddings)
    top_indexes = scores.argsort()[-top_k:][::-1]

    return [
        {
            "source": chunks[index]["source"],
            "score": float(scores[index]),
            "text": chunks[index]["text"],
        }
        for index in top_indexes
    ]