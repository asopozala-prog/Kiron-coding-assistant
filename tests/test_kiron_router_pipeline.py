"""
Unit tests for kiron_router_pipeline.py.
"""

from unittest.mock import patch

from src.kiron_router_pipeline import process_user_input


@patch("src.kiron_router_pipeline.validate_task")
@patch("src.kiron_router_pipeline.wants_to_execute_task")
def test_process_user_input_routes_valid_task_to_llm_agent(
    mock_wants_to_execute_task,
    mock_validate_task,
):
    """A valid file-work task should route to the LLM agent."""
    mock_wants_to_execute_task.return_value = True
    mock_validate_task.return_value = (True, "Valid task")

    assert process_user_input("Please edit contract.txt") == "Route to LLM Agent."


@patch("src.kiron_router_pipeline.validate_task")
@patch("src.kiron_router_pipeline.wants_to_execute_task")
def test_process_user_input_returns_validation_message_for_invalid_task(
    mock_wants_to_execute_task,
    mock_validate_task,
):
    """An invalid file-work task should return the validator message."""
    mock_wants_to_execute_task.return_value = True
    mock_validate_task.return_value = (False, "No valid workspace file mentioned.")

    assert process_user_input("Please edit something") == "No valid workspace file mentioned."


@patch("src.kiron_router_pipeline.wants_to_execute_task")
def test_process_user_input_routes_non_task_to_tinybert_router(
    mock_wants_to_execute_task,
):
    """Non-file-work input should route to the TinyBERT router."""
    mock_wants_to_execute_task.return_value = False

    assert process_user_input("Tell me about Kiron") == "Route to TinyBERT Router."