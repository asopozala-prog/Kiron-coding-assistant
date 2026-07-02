"""
Semantic retrieval tests for Kiron retriever.

These tests use the real MiniLM embedding model.
"""

from src.kiron_retriever import retrieve_kiron_chunks


def test_retrieve_kiron_chunks_finds_creator_article():
    """A creator question should rank the creator article first."""
    results = retrieve_kiron_chunks("Who created Kiron?")

    assert results
    assert results[0]["source"] == "01_creator.md"
    assert results[0]["score"] > 0.25