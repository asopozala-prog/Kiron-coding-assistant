"""
Conversation handling for Kiron Mode.
"""

import random
from pathlib import Path

from src.kiron_answer_generator import generate_kiron_answer
from src.kiron_retriever import retrieve_kiron_chunks


RAG_DIR = Path("legal_files/rag/kiron")


FALLBACK_MESSAGES = [
    (
        "Hmm... I don't think that's part of my little dinosaur expertise. 🦕\n\n"
        "I was built to help with confidential workflows, local AI, and the Kiron project. "
        "Let's wander back to one of those paths together!"
    ),
    (
        "Oh! You've wandered into a part of the forest I don't know very well. 🌲\n\n"
        "I'm just a small dinosaur who specializes in the Kiron project and local AI. "
        "I'll quietly head back to the Mushroom House before I get lost... 🦕\n\n"
        "Maybe ask me something about Alex, my architecture, or how I work?"
    ),
    (
        "Eep... that's outside my little corner of the forest! 🦕\n\n"
        "Hormus is busy writing code, Hazel is polishing documents, Silas is managing projects, "
        "and Orsi is organizing the knowledge shelves. I think I'll head back to the Mushroom House "
        "before I start making wild guesses. 🍄\n\n"
        "If you'd like to explore the Kiron project, local AI, or how I was built, I'll happily tag along!"
    ),
]


def _read_article(filename: str) -> str:
    """Return the full content of a Kiron article."""
    path = RAG_DIR / filename
    return path.read_text(encoding="utf-8")


def kiron_intro() -> str:
    """Return the Kiron introduction."""
    return (
        "### 🦕 Meet Kiron\n\n"
        "Hi! I'm **Kiron**, your friendly local AI assistant.\n\n"
        "I was created for people like Alex—professionals who work with confidential "
        "documents and cannot rely on cloud AI because of privacy requirements, "
        "company policies, or legal regulations.\n\n"
        "Whether you're organizing legal documents, reviewing reports, or managing "
        "sensitive information, I'm here to lend a tiny dinosaur-sized helping hand. 🦕\n\n"
        "What would you like to explore?\n\n"
        "1. 👨‍💻 Who created me?\n"
        "2. ⚙️ How do I work?\n"
        "3. 🌱 Why was I designed this way?"
    )


def is_relevant(results: list[dict[str, str | float]], threshold: float = 0.25) -> bool:
    """Return True if the best retrieval score is relevant enough."""
    if not results:
        return False

    return float(results[0]["score"]) >= threshold


def handle_kiron_mode(user_input: str, kiron_warned: bool) -> tuple[str, str, bool]:
    """Handle Kiron Mode conversation."""
    choice = user_input.strip()

    if choice == "1":
        return "kiron_mode", _read_article("01_creator.md"), False

    if choice == "2":
        return "kiron_mode", _read_article("02_technical_architecture.md"), False

    if choice == "3":
        return "kiron_mode", _read_article("03_design_philosophy.md"), False

    results = retrieve_kiron_chunks(user_input)

    if is_relevant(results):
        chunks = [result["text"] for result in results]
        answer = generate_kiron_answer(user_input, chunks)
        return "kiron_mode", answer, False

    if not kiron_warned:
        return "kiron_mode", random.choice(FALLBACK_MESSAGES), True

    return "entry", "Kiron is going back to the main path. 🦕", False