"""
LLM client for Kiron.

Switches between local llama-server and Groq cloud backend.
"""

import json
import os
import urllib.request

from groq import Groq


LOCAL_COMPLETION_URL = "http://127.0.0.1:8080/completion"
DEFAULT_BACKEND = os.getenv("LLM_BACKEND", "local")


def complete(prompt: str, max_tokens: int = 120) -> str:
    """Generate text using the configured LLM backend."""
    if DEFAULT_BACKEND == "groq":
        return _complete_with_groq(prompt, max_tokens)

    return _complete_with_local_llama(prompt, max_tokens)


def _complete_with_local_llama(prompt: str, max_tokens: int) -> str:
    """Call local llama-server."""
    payload = {
        "prompt": prompt,
        "n_predict": max_tokens,
        "temperature": 0.2,
        "stream": False,
    }

    request = urllib.request.Request(
        LOCAL_COMPLETION_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["content"].strip()


def _complete_with_groq(prompt: str, max_tokens: int) -> str:
    """Call Groq cloud API."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()