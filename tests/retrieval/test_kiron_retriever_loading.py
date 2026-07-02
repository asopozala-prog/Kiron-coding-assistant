"""
Tests for deterministic Kiron retriever loading.

These tests verify chunk loading independently from MiniLM.
"""

import numpy as np

from src import kiron_retriever
from src.kiron_retriever import cosine_similarity, load_chunks


def test_load_chunks_reads_markdown_files(tmp_path, monkeypatch):
    """Kiron retriever should load Markdown files as searchable chunks."""
    article = tmp_path / "01_creator.md"
    article.write_text("Kiron was created by Mei.", encoding="utf-8")

    monkeypatch.setattr(kiron_retriever, "RAG_DIR", tmp_path)

    chunks = load_chunks()

    assert chunks == [
        {
            "source": "01_creator.md",
            "text": "Kiron was created by Mei.",
        }
    ]


def test_load_chunks_skips_kiron_mode_rules_file(tmp_path, monkeypatch):
    """Mode rules should not be loaded as searchable user-facing chunks."""
    rules = tmp_path / "00_kiron_mode_rules.md"
    rules.write_text("Internal rules.", encoding="utf-8")

    article = tmp_path / "01_creator.md"
    article.write_text("Public Kiron article.", encoding="utf-8")

    monkeypatch.setattr(kiron_retriever, "RAG_DIR", tmp_path)

    chunks = load_chunks()

    assert chunks == [
        {
            "source": "01_creator.md",
            "text": "Public Kiron article.",
        }
    ]


def test_load_chunks_skips_empty_files(tmp_path, monkeypatch):
    """Empty Markdown files should not become searchable chunks."""
    empty = tmp_path / "empty.md"
    empty.write_text("   ", encoding="utf-8")

    monkeypatch.setattr(kiron_retriever, "RAG_DIR", tmp_path)

    assert load_chunks() == []


def test_cosine_similarity_prefers_parallel_vectors():
    """Parallel vectors should have the highest similarity."""
    query = np.array([1.0, 0.0])
    chunks = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
        ]
    )

    scores = cosine_similarity(query, chunks)

    assert scores[0] > scores[1]
    