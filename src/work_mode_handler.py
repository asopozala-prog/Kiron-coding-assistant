"""
Work mode handling for Kiron.

This module handles Alex's file-work conversation after entering work mode.
"""

from src.task_validator import list_workspace_files, validate_task


def format_file_list(file_names: list[str]) -> str:
    """Format workspace files for display."""
    if not file_names:
        return "- No files found"

    return "\n".join(f"- {name}" for name in file_names)


def handle_work_mode(user_input: str, unclear_count: int) -> tuple[str, str, int]:
    """Handle one user input while Kiron is in work mode."""
    is_valid, message = validate_task(user_input)

    if is_valid:
        return "work_mode", message, 0

    unclear_count += 1
    file_list = format_file_list(list_workspace_files())

    if unclear_count == 1:
        return (
            "work_mode",
            "Hi Alex, I found these files in your work folder.\n"
            "Which one should we work on, or should I create a new one?\n\n"
            f"{file_list}",
            unclear_count,
        )

    if unclear_count == 2:
        return (
            "work_mode",
            "Alex, let's stay with the work path.\n"
            "Please name one file, or ask me to create a new file.\n\n"
            f"{file_list}",
            unclear_count,
        )

    return (
        "entry",
        "Alex, I think you may need a break.\n"
        "I'll reset for now — see you later.",
        0,
    )