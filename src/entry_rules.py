"""
Entry rules for Kiron.

This module decides how a new conversation begins.
"""

import re


def normalize(text: str) -> str:
    """Normalize user input for simple rule matching."""
    text = text.lower()
    text = text.replace("i'm", "i am")
    text = text.replace("iam", "i am")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_alex_identity(text: str) -> bool:
    """Return True if the user clearly identifies as Alex."""
    return (
        "alex" in text
        and any(word in text for word in {"i", "am", "here"})
    )


def menu_response() -> str:
    """Return Kiron's standard entry menu."""
    return (
        "Hello! I'm Kiron 🦕, Alex's assistant.\n\n"
        "What would you like to do?\n\n"
        "1. 📄 Work with files\n"
        "2. 🦕 Ask about me or the Kiron project\n"
        "3. 👤 Learn more about Alex"
    )


def alex_response() -> str:
    """Return the entry response for Alex."""
    return (
        "Hello Alex! 🦕\n"
        "Glad to see you again.\n"
        "Let's get to work.\n\n"
        "Which file would you like to work on today?"
    )


def handle_entry(user_input: str) -> tuple[str, str]:
    """Return the next mode and entry response."""
    text = normalize(user_input)

    if is_alex_identity(text):
        return "work_mode", alex_response()

    return "menu", menu_response()