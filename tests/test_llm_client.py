"""
Unit tests for llm_client.py.

These tests mock external LLM services.
"""

from unittest.mock import Mock, patch

from src import llm_client


def test_get_setting_reads_environment_first(monkeypatch):
    """Environment variables should take priority over Streamlit secrets."""
    monkeypatch.setenv("LLM_BACKEND", "groq")

    assert llm_client.get_setting("LLM_BACKEND", "local") == "groq"


@patch("src.llm_client._complete_with_local_llama")
def test_complete_uses_local_backend_by_default(mock_local, monkeypatch):
    """The local backend should be used by default."""
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    mock_local.return_value = "Local answer"

    assert llm_client.complete("Hello") == "Local answer"
    mock_local.assert_called_once_with("Hello", 120)


@patch("src.llm_client._complete_with_groq")
def test_complete_uses_groq_backend_when_configured(mock_groq, monkeypatch):
    """The Groq backend should be used when configured."""
    monkeypatch.setenv("LLM_BACKEND", "groq")
    mock_groq.return_value = "Groq answer"

    assert llm_client.complete("Hello", max_tokens=50) == "Groq answer"
    mock_groq.assert_called_once_with("Hello", 50)