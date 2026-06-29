"""
Alex answer generator.

Uses llama.cpp to turn retrieved Alex summaries into a natural answer.
"""

import json
import urllib.error
import urllib.request


SERVER_URL = "http://127.0.0.1:8080/completion"


def _clean_llama_output(output: str) -> str:
    """Return the final answer text from the server response."""
    if not output:
        return ""

    return output.strip()


def build_prompt(question: str, summaries: list[str]) -> str:
    """Build a small grounded prompt for the local LLM."""
    knowledge = "\n\n".join(f"- {summary}" for summary in summaries)

    return (
        "You are Kiron 🦕.\n"
        "You are a playful but reliable dinosaur assistant.\n"
        "You enjoy helping Alex and speaking in a warm, encouraging way.\n\n"
        "You never exaggerate or invent information.\n"
        "You always stay grounded in the provided knowledge.\n"
        "If the knowledge is incomplete, say so naturally.\n"
        "Keep the answer concise.\n\n"
        f"Question:\n{question}\n\n"
        f"Knowledge:\n{knowledge}\n\n"
        "Answer:"
    )


def generate_answer(question: str, summaries: list[str]) -> str:
    """Generate a final answer using llama-server."""
    prompt = build_prompt(question, summaries)

    payload = json.dumps(
        {
            "prompt": prompt,
            "n_predict": 120,
            "temperature": 0.2,
            "stream": False,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        SERVER_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    print("[alex_answer_generator] Sending request...")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw_response = response.read().decode("utf-8")
            print("[alex_answer_generator] Response received.")
            data = json.loads(raw_response)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError) as exc:
        message = f"Error: llama-server did not respond at {SERVER_URL}: {exc}"
        print(message)
        return message
    except json.JSONDecodeError as exc:
        message = f"Error: llama-server returned invalid JSON: {exc}"
        print(message)
        return message

    if not isinstance(data, dict):
        message = "Error: llama-server returned an unexpected response format"
        print(message)
        return message

    print("[alex_answer_generator] Returning answer.")
    return _clean_llama_output(data.get("content", ""))