"""
Unit tests for kiron_answer_generator.py.
"""

from unittest.mock import patch

from src.kiron_answer_generator import (
    build_prompt,
    generate_kiron_answer,
)


def test_build_prompt_contains_question_and_chunks():
    """The prompt should include the question and all retrieved chunks."""
    prompt = build_prompt(
        "How was Kiron built?",
        [
            "Kiron uses local AI.",
            "Kiron protects confidential workflows.",
        ],
    )

    assert "How was Kiron built?" in prompt
    assert "Kiron uses local AI." in prompt
    assert "Kiron protects confidential workflows." in prompt
    assert "Answer:" in prompt


@patch("src.kiron_answer_generator.complete")
def test_generate_kiron_answer_calls_complete(mock_complete):
    """The generator should pass the prompt to the LLM client."""
    mock_complete.return_value = "Mock answer"

    answer = generate_kiron_answer(
        "How was Kiron built?",
        ["Kiron uses local AI."],
    )

    assert answer == "Mock answer"
    mock_complete.assert_called_once()