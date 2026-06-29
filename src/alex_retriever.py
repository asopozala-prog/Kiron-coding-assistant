"""
Structured RAG retriever for Kiron.

MiniLM searches over retrieval tags.
Python returns only Summary content from the top matching topics.
"""

from pathlib import Path
import re

import numpy as np
from sentence_transformers import SentenceTransformer


RAG_DIR = Path("legal_files/rag/alex")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_documents() -> list[tuple[str, str]]:
    """Load every Markdown document."""
    return [
        (file.name, file.read_text(encoding="utf-8"))
        for file in sorted(RAG_DIR.glob("*.md"))
    ]


def extract_section(text: str, heading: str) -> str:
    """Extract content under a Markdown heading."""
    pattern = rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_topics(documents: list[tuple[str, str]]) -> list[dict[str, str]]:
    """Parse Markdown files into topic objects."""
    topics = []

    for filename, content in documents:
        parts = re.split(r"(?=^# Topic:)", content, flags=re.MULTILINE)

        for part in parts:
            part = part.strip()
            if not part.startswith("# Topic:"):
                continue

            title = part.splitlines()[0].replace("# Topic:", "").strip()

            topics.append(
                {
                    "source": filename,
                    "title": title,
                    "summary": extract_section(part, "Summary"),
                    "retrieval_tags": extract_section(part, "Retrieval tags"),
                }
            )

    return topics


def cosine_similarity(query_embedding: np.ndarray, topic_embeddings: np.ndarray) -> np.ndarray:
    """Calculate cosine similarity."""
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    topic_norms = topic_embeddings / np.linalg.norm(topic_embeddings, axis=1, keepdims=True)
    return np.dot(topic_norms, query_norm)


def retrieve_summaries(question: str, top_k: int = 2) -> list[dict[str, str | float]]:
    """Retrieve top matching topics using tags, returning only summaries."""
    topics = parse_topics(load_documents())

    model = SentenceTransformer(MODEL_NAME)

    search_texts = [topic["retrieval_tags"] for topic in topics]
    topic_embeddings = model.encode(search_texts, convert_to_numpy=True)
    question_embedding = model.encode(question, convert_to_numpy=True)

    scores = cosine_similarity(question_embedding, topic_embeddings)
    top_indexes = scores.argsort()[-top_k:][::-1]

    return [
        {
            "source": topics[index]["source"],
            "topic": topics[index]["title"],
            "score": float(scores[index]),
            "summary": topics[index]["summary"],
        }
        for index in top_indexes
    ]


def main() -> None:
    """Test summary-only retrieval."""
    question = input("Ask about Alex: ")
    results = retrieve_summaries(question)

    print("\nTop summaries:\n")

    for result in results:
        print("=" * 80)
        print(f"Source: {result['source']}")
        print(f"Topic: {result['topic']}")
        print(f"Score: {result['score']:.4f}")
        print("-" * 80)
        print(result["summary"])
        print()


if __name__ == "__main__":
    main()