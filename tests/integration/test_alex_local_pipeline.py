"""
Integration test for the local Alex RAG pipeline.

Requires:
- llama-server running on localhost:8080
- local Qwen model loaded
"""

import pytest

from src.alex_answer_generator import generate_answer
from src.alex_retriever import retrieve_summaries


@pytest.mark.integration
def test_alex_local_pipeline_answers_identity_question():
    """The complete local Alex pipeline should answer from Alex knowledge."""
    question = "Who is Alex?"

    summaries = [r["summary"] for r in retrieve_summaries(question)]

    answer = generate_answer(question, summaries)

    assert answer
    assert "Alex" in answer
    assert "Junior Legal Assistant" in answer