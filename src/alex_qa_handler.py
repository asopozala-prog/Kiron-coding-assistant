"""
Alex QA handling.

Connects Alex retrieval with local answer generation.
"""

from src.alex_answer_generator import generate_answer
from src.alex_retriever import retrieve_summaries


def alex_intro() -> str:
    """Return a short Alex introduction."""
    return (
        "Alex is the person I assist. 👤\n"
        "Ask me what you would like to know about Alex."
    )


def handle_alex_qa(user_input: str) -> str:
    """Answer an Alex question using retrieval plus local LLM."""
    results = retrieve_summaries(user_input)
    summaries = [result["summary"] for result in results]

    return generate_answer(user_input, summaries)