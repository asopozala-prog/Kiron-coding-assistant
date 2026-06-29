"""
High-level routing pipeline for the Kiron Coding Assistant.

This file coordinates routing after the entry/menu stage.
"""

from src.task_validator import validate_task, wants_to_execute_task


def process_user_input(user_input: str) -> str:
    """Route user input after entry/menu handling."""
    if wants_to_execute_task(user_input):
        is_valid, message = validate_task(user_input)

        if is_valid:
            return "Route to LLM Agent."

        return message

    return "Route to TinyBERT Router."