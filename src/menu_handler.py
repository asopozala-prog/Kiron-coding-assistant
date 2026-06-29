"""
Menu handling for Kiron.
"""

from src.alex_qa_handler import alex_intro
from src.kiron_mode_handler import kiron_intro


def menu_response() -> str:
    """Return the main menu again."""
    return (
        "Please choose:\n\n"
        "1. 📄 Work with files\n"
        "2. 🦕 Ask about me or the Kiron project\n"
        "3. 👤 Learn more about Alex"
    )


def handle_menu_choice(user_input: str) -> tuple[str, str]:
    """Handle user selection from the main menu."""
    text = user_input.strip().lower()

    if text in {"1", "work", "work with files", "files"}:
        return "work_mode", "Work mode selected. Which file would you like to work on?"

    if text in {"2", "kiron", "kiron project", "project"}:
        return "kiron_mode", kiron_intro()

    if text in {"3", "alex", "learn about alex"}:
        return "alex_qa", alex_intro()

    return "menu", (
        "Sorry, I can only help with those three things right now.\n\n"
        f"{menu_response()}"
    )