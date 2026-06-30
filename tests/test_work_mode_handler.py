"""
Unit tests for work_mode_handler.py.
"""

from unittest.mock import patch

from src.work_mode_handler import format_file_list, handle_work_mode


def test_format_file_list_shows_no_files_message():
    """The file formatter should show a clear message when no files exist."""
    assert format_file_list([]) == "- No files found"


def test_format_file_list_formats_each_file_on_its_own_line():
    """The file formatter should display each file as a bullet."""
    result = format_file_list(["contract.txt", "notes.md"])

    assert result == "- contract.txt\n- notes.md"


@patch("src.work_mode_handler.validate_task")
def test_handle_work_mode_returns_validator_result(mock_validate_task):
    """A valid task should stay in work mode and reset the unclear counter."""
    mock_validate_task.return_value = (True, "Valid task")

    mode, message, unclear_count = handle_work_mode(
        "Please summarize contract.txt",
        2,
    )

    assert mode == "work_mode"
    assert message == "Valid task"
    assert unclear_count == 0


@patch("src.work_mode_handler.list_workspace_files")
@patch("src.work_mode_handler.validate_task")
def test_handle_work_mode_first_unclear_request_lists_files(mock_validate_task, mock_list_files):
    """The first unclear request should stay in work mode and list files."""
    mock_validate_task.return_value = (False, "No valid workspace file mentioned.")
    mock_list_files.return_value = ["contract.txt"]

    mode, message, unclear_count = handle_work_mode("help", 0)

    assert mode == "work_mode"
    assert "Which one should we work on" in message
    assert "- contract.txt" in message
    assert unclear_count == 1


@patch("src.work_mode_handler.list_workspace_files")
@patch("src.work_mode_handler.validate_task")
def test_handle_work_mode_second_unclear_request_gives_stronger_reminder(mock_validate_task, mock_list_files):
    """The second unclear request should give a stronger work-mode reminder."""
    mock_validate_task.return_value = (False, "No valid workspace file mentioned.")
    mock_list_files.return_value = ["contract.txt"]

    mode, message, unclear_count = handle_work_mode("not sure", 1)

    assert mode == "work_mode"
    assert "let's stay with the work path" in message
    assert "- contract.txt" in message
    assert unclear_count == 2


@patch("src.work_mode_handler.list_workspace_files")
@patch("src.work_mode_handler.validate_task")
def test_handle_work_mode_third_unclear_request_resets_to_entry(mock_validate_task, mock_list_files):
    """The third unclear request should reset the conversation to entry mode."""
    mock_validate_task.return_value = (False, "No valid workspace file mentioned.")
    mock_list_files.return_value = ["contract.txt"]

    mode, message, unclear_count = handle_work_mode("still confused", 2)

    assert mode == "entry"
    assert "need a break" in message
    assert unclear_count == 0
