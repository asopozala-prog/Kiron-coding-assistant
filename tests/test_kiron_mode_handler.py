"""
Unit tests for kiron_mode_handler.py.
"""

from src.kiron_mode_handler import is_relevant, kiron_intro


def test_kiron_intro_contains_three_paths():
    """The Kiron intro should present the three exploration paths."""
    intro = kiron_intro()

    assert "Who created me?" in intro
    assert "How do I work?" in intro
    assert "Why was I designed this way?" in intro


def test_is_relevant_returns_false_for_empty_results():
    """No retrieval results should not be considered relevant."""
    assert not is_relevant([])


def test_is_relevant_returns_true_when_top_score_meets_threshold():
    """A high top score should be considered relevant."""
    results = [{"text": "Kiron architecture", "score": 0.4}]

    assert is_relevant(results)


def test_is_relevant_returns_false_when_top_score_below_threshold():
    """A low top score should not be considered relevant."""
    results = [{"text": "Unrelated", "score": 0.1}]

    assert not is_relevant(results)
    