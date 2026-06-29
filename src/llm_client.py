"""
LLM client for Kiron.
"""

import json
import os
import urllib.request

import streamlit as st
from groq import Groq


LOCAL_COMPLETION_URL = "http://127.0.0.1:8080/completion"


def get_setting(name: str, default: str | None = None) -> str | None:
    """Read config from environment first, then Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value

    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def complete(prompt: str, max_tokens: int = 120) -> str:
    """Generate text using the configured backend."""
    backend = get_setting("LLM_BACKEND", "local")

    if backend == "groq":
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
    api_key = get_setting("GROQ_API_KEY")
    model = get_setting("GROQ_MODEL", "llama-3.1-8b-instant")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()