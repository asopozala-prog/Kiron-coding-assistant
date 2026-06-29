"""
Alex answer generator.
"""

from src.llm_client import complete


def build_prompt(question: str, summaries: list[str]) -> str:
    """Build a grounded prompt for Alex QA."""
    knowledge = "\n\n".join(f"- {summary}" for summary in summaries)

    return (
        "Answer using only the Knowledge below.\n"
        "Answer in no more than two sentences.\n\n"
        f"Question:\n{question}\n\n"
        f"Knowledge:\n{knowledge}\n\n"
        "Answer:"
    )


def generate_answer(question: str, summaries: list[str]) -> str:
    """Generate a final Alex answer."""
    prompt = build_prompt(question, summaries)
    return complete(prompt, max_tokens=120)