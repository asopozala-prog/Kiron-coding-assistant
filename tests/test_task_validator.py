"""
Unit tests for task_validator.py.
"""

from src import task_validator
from src.task_validator import wants_to_execute_task


def test_wants_to_execute_task_detects_file_related_request():
    """The validator should recognize file-related tasks."""
    assert wants_to_execute_task("Please edit this file")


def test_rejects_unrelated_request():
    """The validator should reject unrelated conversation."""
    assert not wants_to_execute_task("How is the weather today?")


def test_list_workspace_files_uses_temporary_workspace(tmp_path, monkeypatch):
    """The file lister should return files from the configured workspace."""
    test_file = tmp_path / "contract.txt"
    test_file.write_text("Example contract", encoding="utf-8")

    monkeypatch.setattr(task_validator, "WORKSPACE_DIR", tmp_path)

    assert task_validator.list_workspace_files() == ["contract.txt"]


def test_validate_task_accepts_existing_workspace_file(tmp_path, monkeypatch):
    """The validator should accept a task that names an existing file."""
    test_file = tmp_path / "contract.txt"
    test_file.write_text("Example contract", encoding="utf-8")

    monkeypatch.setattr(task_validator, "WORKSPACE_DIR", tmp_path)

    is_valid, message = task_validator.validate_task(
        "Please summarize contract.txt"
    )

    assert is_valid
    assert message == "Valid task for existing file: contract.txt"
