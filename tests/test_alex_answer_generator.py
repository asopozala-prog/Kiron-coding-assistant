"""
Unit tests for alex_answer_generator.py.
"""

from unittest.mock import patch

from src.alex_answer_generator import build_prompt, generate_answer


def test_build_prompt_contains_question_and_knowledge():
    """The prompt should include the question and all summaries."""
    prompt = build_prompt(
        "Who is Alex?",
        ["Alex builds Kiron.", "Alex likes ML."],
    )

    assert "Who is Alex?" in prompt
    assert "Alex builds Kiron." in prompt
    assert "Alex likes ML." in prompt
    assert "Answer:" in prompt


@patch("src.alex_answer_generator.complete")
def test_generate_answer_calls_complete(mock_complete):
    """The generator should pass the prompt to the LLM client."""
    mock_complete.return_value = "Mock answer"

    answer = generate_answer(
        "Who is Alex?",
        ["Alex builds Kiron."],
    )

    assert answer == "Mock answer"
    mock_complete.assert_called_once()