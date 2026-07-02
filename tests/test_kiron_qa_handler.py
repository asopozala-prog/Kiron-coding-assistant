"""
Unit tests for kiron_qa_handler.py.
"""

from src.kiron_qa_handler import handle_kiron_qa, kiron_intro


def test_kiron_intro_explains_kiron_role():
    """The Kiron intro should explain Kiron's role."""
    intro = kiron_intro()

    assert "I am Kiron" in intro
    assert "Kiron project" in intro


def test_handle_kiron_qa_returns_placeholder_response():
    """The placeholder handler should include the user's question."""
    response = handle_kiron_qa("How does Kiron work?")

    assert response == "Kiron Project RAG will answer: How does Kiron work?"