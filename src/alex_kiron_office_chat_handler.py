"""
Office chat handler for the original portfolio app.

This handler keeps the old app focused:
Kiron only works with Alex on files.
"""

from src.entry_rules import is_alex_identity
from src.work_mode_handler import handle_work_mode


RUN_AGENT = "RUN_AGENT"


def office_intro() -> str:
    """Return the first office chat message."""
    return "Hello! I'm Kiron 🦕, Alex's assistant.\n\nAre you Alex?"


def office_fallback() -> str:
    """Return fallback for non-Alex users."""
    return (
        "Sorry, I only work with Alex on his files.\n\n"
        "If you'd like to explore Kiron as a conversational AI, "
        "please use the Conversation Prototype from the sidebar."
    )


def confirms_alex(text: str) -> bool:
    """Return True if user confirms they are Alex."""
    normalized = text.strip().lower()
    return normalized in {"yes", "yes i am", "yes, i am", "y", "yeah", "sure"}


def alex_confirmed_response() -> str:
    """Return confirmation message when Alex enters work mode."""
    return "Hello Alex! 🦕\n\nLet's work with your files."


def handle_office_chat(
    user_input: str,
    office_mode: str,
    work_unclear_count: int,
) -> tuple[str, str, int]:
    """
    Handle the original app office conversation.

    Returns:
        (next_office_mode, response, next_work_unclear_count)

    Modes:
        start
        work_mode
    """
    if office_mode == "work_mode":
        next_mode, response, next_count = handle_work_mode(
            user_input,
            work_unclear_count,
        )

        if next_mode == "work_mode" and next_count == 0:
            return "work_mode", RUN_AGENT, next_count

        if next_mode == "entry":
            return "start", response, 0

        return "work_mode", response, next_count

    if is_alex_identity(user_input) or confirms_alex(user_input):
        return "work_mode", alex_confirmed_response(), 0

    return "start", office_fallback(), 0