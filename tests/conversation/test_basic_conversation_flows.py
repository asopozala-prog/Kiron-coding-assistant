"""
Basic conversation-flow tests for Kiron.

These tests protect common user journeys without testing every possible variant.
"""

from src.entry_rules import handle_entry
from src.menu_handler import handle_menu_choice


def test_visitor_can_choose_office_from_menu():
    mode, response = handle_entry("hello")
    assert mode == "menu"

    mode, response = handle_menu_choice("1")
    assert mode == "open_office"
    assert "Let us go to the office" in response


def test_visitor_can_choose_kiron_from_menu():
    mode, response = handle_entry("hello")
    assert mode == "menu"

    mode, response = handle_menu_choice("2")
    assert mode == "kiron_mode"
    assert "Meet Kiron" in response


def test_visitor_can_choose_alex_from_menu():
    mode, response = handle_entry("hello")
    assert mode == "menu"

    mode, response = handle_menu_choice("3")
    assert mode == "alex_qa"
    assert "Alex is the person I assist" in response


def test_invalid_menu_choice_returns_to_menu():
    mode, response = handle_entry("hello")
    assert mode == "menu"

    mode, response = handle_menu_choice("banana")
    assert mode == "menu"
    assert "Sorry" in response
    assert "Please choose" in response


def test_alex_confirmation_enters_work_mode():
    mode, response = handle_entry("yes")

    assert mode == "work_mode"
    assert "Hello Alex" in response