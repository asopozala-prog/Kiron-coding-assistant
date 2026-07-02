"""
Conversation-flow tests for Entry → Menu → Office.
"""

from src.entry_rules import handle_entry
from src.menu_handler import handle_menu_choice


def test_visitor_can_choose_office_from_menu():
    """A non-Alex visitor should reach the Office path through the menu."""
    mode, response = handle_entry("hello")

    assert mode == "menu"
    assert "What would you like to do?" in response

    mode, response = handle_menu_choice("1")

    assert mode == "open_office"
    assert "Let us go to the office" in response
    assert "page=chat" in response