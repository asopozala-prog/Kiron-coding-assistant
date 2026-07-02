"""
Conversation-flow tests for Entry → Menu → Kiron Mode.
"""

from src.entry_rules import handle_entry
from src.menu_handler import handle_menu_choice


def test_visitor_can_choose_kiron_from_menu():
    """A visitor should reach Kiron Mode through the menu."""
    mode, response = handle_entry("hello")

    assert mode == "menu"
    assert "What would you like to do?" in response

    mode, response = handle_menu_choice("2")

    assert mode == "kiron_mode"
    assert "Meet Kiron" in response
    assert "Who created me?" in response