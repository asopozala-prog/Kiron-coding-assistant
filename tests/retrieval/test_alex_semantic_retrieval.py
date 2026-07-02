"""
Semantic retrieval tests for the Alex retriever.

These tests use the real MiniLM embedding model.
"""

from src.alex_retriever import retrieve_summaries


def test_retrieve_summaries_finds_basic_identity():
    """An identity question should rank the Identity Index topic first."""
    results = retrieve_summaries("Who is Alex?")

    assert results
    assert results[0]["topic"] == "Identity Index"
    assert results[0]["score"] > 0.10