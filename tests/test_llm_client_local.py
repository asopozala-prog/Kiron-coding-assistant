"""
Tests for the local llama HTTP client.
"""

import json
from unittest.mock import MagicMock, patch

from src.llm_client import _complete_with_local_llama


@patch("urllib.request.urlopen")
def test_local_llama_returns_content(mock_urlopen):
    """The local client should return the content field."""
    response = MagicMock()
    response.read.return_value = json.dumps(
        {"content": " Hello from llama "}
    ).encode("utf-8")

    mock_urlopen.return_value.__enter__.return_value = response

    answer = _complete_with_local_llama("Hello", 20)

    assert answer == "Hello from llama"


@patch("urllib.request.urlopen")
def test_local_llama_sends_post_request(mock_urlopen):
    """The local client should send one HTTP request."""
    response = MagicMock()
    response.read.return_value = json.dumps(
        {"content": "OK"}
    ).encode("utf-8")

    mock_urlopen.return_value.__enter__.return_value = response

    _complete_with_local_llama("Prompt", 50)

    mock_urlopen.assert_called_once()