"""
Task validation for Kiron.

The validator checks whether Alex's request can be connected
to files inside the legal_files/work_files workspace.
"""

from pathlib import Path

WORKSPACE_DIR = Path("legal_files/work_files")


def list_workspace_files() -> list[str]:
    """Return all file names directly inside the workspace."""
    if not WORKSPACE_DIR.exists():
        WORKSPACE_DIR.mkdir(parents=True)

    return [file.name for file in WORKSPACE_DIR.iterdir() if file.is_file()]


def wants_to_execute_task(user_input: str) -> bool:
    """Return True if the user appears to want file work."""
    text = user_input.lower()
    task_words = ["file", "document", "read", "write", "edit", "fix", "create", "summarize"]
    return any(word in text for word in task_words)


def validate_task(user_input: str) -> tuple[bool, str]:
    """Validate whether the task mentions an existing workspace file."""
    text = user_input.lower()
    existing_files = list_workspace_files()

    for file_name in existing_files:
        if file_name.lower() in text:
            return True, f"Valid task for existing file: {file_name}"

    if "create" in text and "file" in text:
        return True, "Valid task: create new file."

    return False, "No valid workspace file mentioned."