"""
Integration test for the local Kiron RAG pipeline.

Requires:
- llama-server running on localhost:8080
- local Qwen model loaded
"""

import pytest

from src.kiron_answer_generator import generate_kiron_answer
from src.kiron_retriever import retrieve_kiron_chunks


@pytest.mark.integration
def test_local_pipeline_answers_creator_question():
    """The complete local pipeline should answer from Kiron knowledge."""
    question = "Who created Kiron?"

    chunks = [r["text"] for r in retrieve_kiron_chunks(question)]

    answer = generate_kiron_answer(question, chunks)

    assert answer
    assert "Hormus" in answer