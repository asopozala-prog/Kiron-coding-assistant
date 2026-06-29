"""
Kiron answer generator.
"""

from src.llm_client import complete


def build_prompt(question: str, chunks: list[str]) -> str:
    """Build a grounded prompt for Kiron QA."""
    knowledge = "\n\n".join(chunks)

    return (
        "Answer using only the Knowledge below.\n"
        "Answer in no more than two sentences.\n\n"
        f"Question:\n{question}\n\n"
        f"Knowledge:\n{knowledge}\n\n"
        "Answer:"
    )


def generate_kiron_answer(question: str, chunks: list[str]) -> str:
    """Generate a final Kiron answer."""
    prompt = build_prompt(question, chunks)
    return complete(prompt, max_tokens=160)