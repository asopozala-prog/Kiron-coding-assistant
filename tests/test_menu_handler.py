"""
Unit tests for menu_handler.py.
"""

from src.menu_handler import handle_menu_choice, menu_response


def test_menu_response_contains_all_options():
    """The menu should display all three main paths."""
    menu = menu_response()

    assert "Work with files" in menu
    assert "Ask about me" in menu
    assert "Learn more about Alex" in menu


def test_menu_choice_one_opens_office():
    """Choosing path 1 should route the user to the Office app."""
    mode, message = handle_menu_choice("1")

    assert mode == "open_office"
    assert "Let us go to the office" in message
    assert "https://kiron-coding-assistant-x3d9klzag52v4rc92zress.streamlit.app/?page=chat" in message


def test_invalid_menu_choice_stays_in_menu():
    """Invalid choices should keep the user in the menu."""
    mode, message = handle_menu_choice("banana")

    assert mode == "menu"
    assert "Sorry" in message
    assert "Please choose" in message