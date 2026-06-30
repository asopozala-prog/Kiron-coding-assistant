"""
Unit tests for alex_qa_handler.py.
"""

from unittest.mock import patch

from src.alex_qa_handler import alex_intro, handle_alex_qa


def test_alex_intro_explains_alex_role():
    """The Alex intro should explain who Alex is."""
    intro = alex_intro()

    assert "Alex is the person I assist" in intro
    assert "Ask me" in intro


@patch("src.alex_qa_handler.generate_answer")
@patch("src.alex_qa_handler.retrieve_summaries")
def test_handle_alex_qa_passes_summaries_to_answer_generator(
    mock_retrieve_summaries,
    mock_generate_answer,
):
    """Alex QA should pass retrieved summaries into the answer generator."""
    mock_retrieve_summaries.return_value = [
        {"summary": "Alex likes ML."},
        {"summary": "Alex builds Kiron."},
    ]
    mock_generate_answer.return_value = "Mock answer"

    handle_alex_qa("What does Alex like?")

    mock_generate_answer.assert_called_once_with(
        "What does Alex like?",
        ["Alex likes ML.", "Alex builds Kiron."],
    )


@patch("src.alex_qa_handler.generate_answer")
@patch("src.alex_qa_handler.retrieve_summaries")
def test_handle_alex_qa_returns_generated_answer(
    mock_retrieve_summaries,
    mock_generate_answer,
):
    """Alex QA should return the generated answer."""
    mock_retrieve_summaries.return_value = [{"summary": "Alex builds Kiron."}]
    mock_generate_answer.return_value = "Mock answer"

    assert handle_alex_qa("Who is Alex?") == "Mock answer"