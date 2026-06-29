"""
Kiron answer generator.

Uses llama.cpp to answer Kiron project questions from retrieved context.
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


def build_prompt(question: str, chunks: list[str]) -> str:
    """Build a grounded prompt for the local LLM."""
    knowledge = "\n\n".join(chunks)

    return (

        "Answer using ONLY the Knowledge below.\n"
        "Reply in no more than TWO sentences.\n"
        "Focus on the single most relevant information.\n"
        "Do not use outside knowledge.\n"
        "Do not infer missing facts.\n\n"
        'If the answer is not contained in the Knowledge, reply exactly:\n'
        '"I don\'t know based on the information I have."\n\n'
        f"Knowledge:\n{knowledge}\n\n"
        f"Question:\n{question}\n\n"
        "Answer:"
    )


def generate_kiron_answer(question: str, chunks: list[str]) -> str:
    """Generate a Kiron answer using llama-server."""
    prompt = build_prompt(question, chunks)

    payload = json.dumps(
        {
            "prompt": prompt,
            "n_predict": 160,
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

    print("[kiron_answer_generator] Sending request...")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw_response = response.read().decode("utf-8")
            print("[kiron_answer_generator] Response received.")
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

    print("[kiron_answer_generator] Returning answer.")
    return _clean_llama_output(data.get("content", ""))