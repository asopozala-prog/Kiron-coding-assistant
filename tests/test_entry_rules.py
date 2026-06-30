"""
Unit tests for entry_rules.py.
"""

from src.entry_rules import (
    alex_response,
    handle_entry,
    is_alex_identity,
    menu_response,
    normalize,
)


def test_normalize_converts_im_to_i_am():
    """Normalization should expand 'I'm'."""
    assert normalize("I'm Alex") == "i am alex"


def test_normalize_removes_punctuation():
    """Normalization should remove punctuation."""
    assert normalize("Hello, Alex!") == "hello alex"


def test_is_alex_identity_accepts_i_am_alex():
    """Alex should be recognized when identifying himself."""
    assert is_alex_identity(normalize("I am Alex"))


def test_is_alex_identity_rejects_plain_name():
    """Mentioning Alex alone should not count as identification."""
    assert not is_alex_identity(normalize("Alex is great"))


def test_menu_response_contains_all_menu_items():
    """The menu should present all available options."""
    menu = menu_response()

    assert "Work with files" in menu
    assert "Ask about me" in menu
    assert "Learn more about Alex" in menu


def test_alex_response_contains_work_prompt():
    """Alex should receive the work-mode greeting."""
    response = alex_response()

    assert "Hello Alex" in response
    assert "Which file would you like to work on today?" in response


def test_handle_entry_routes_alex_to_work_mode():
    """Alex should enter work mode immediately."""
    mode, response = handle_entry("I am Alex")

    assert mode == "work_mode"
    assert response == alex_response()


def test_handle_entry_routes_other_users_to_menu():
    """Other users should receive the main menu."""
    mode, response = handle_entry("Hello")

    assert mode == "menu"
    assert response == menu_response()
    

def test_is_alex_identity_accepts_confirmation_answers():
    """Confirmation answers should count as Alex after the UI asks if this is Alex."""
    for user_input in ["yes", "y", "yep", "yeah", "correct", "it is me", "it's me"]:
        assert is_alex_identity(normalize(user_input))


def test_is_alex_identity_rejects_negative_answers():
    """Negative answers should not count as Alex identity."""
    for user_input in ["no", "nope", "not Alex", "I am not Alex"]:
        assert not is_alex_identity(normalize(user_input))
