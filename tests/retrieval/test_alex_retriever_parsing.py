"""
Tests for deterministic Alex retriever parsing.

These tests verify Markdown parsing independently from MiniLM.
"""

import numpy as np

from src.alex_retriever import (
    cosine_similarity,
    extract_section,
    parse_topics,
)


def test_extract_section_returns_requested_heading():
    """The requested Markdown section should be extracted."""
    text = """
# Topic: Example

## Summary
Alex builds Kiron.

## Retrieval tags
kiron
ml
"""

    assert extract_section(text, "Summary") == "Alex builds Kiron."


def test_extract_section_returns_empty_string_when_missing():
    """Missing headings should return an empty string."""
    assert extract_section("# Topic: Example", "Summary") == ""


def test_parse_topics_extracts_topic_metadata():
    """Markdown documents should become topic objects."""
    documents = [
        (
            "alex.md",
            """
# Topic: ML Engineering

## Summary
Alex likes ML.

## Retrieval tags
machine learning
python
""",
        )
    ]

    topics = parse_topics(documents)

    assert len(topics) == 1
    assert topics[0]["source"] == "alex.md"
    assert topics[0]["title"] == "ML Engineering"
    assert topics[0]["summary"] == "Alex likes ML."
    assert "machine learning" in topics[0]["retrieval_tags"]


def test_cosine_similarity_prefers_parallel_vectors():
    """Parallel vectors should have the highest similarity."""
    query = np.array([1.0, 0.0])
    topics = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
        ]
    )

    scores = cosine_similarity(query, topics)

    assert scores[0] > scores[1]