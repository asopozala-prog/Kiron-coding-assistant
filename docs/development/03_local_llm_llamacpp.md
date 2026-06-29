# Milestone 03 — Local Conversational AI Pipeline

## Objective

Complete the first end-to-end local conversational AI pipeline for the Kiron project.

---

## Achievements

### Local Language Model

Successfully integrated **llama.cpp** with a locally hosted **Qwen2.5-1.5B-Instruct (GGUF)** model.

The model runs entirely on an Intel iMac without relying on any cloud AI services.

---

### Local Inference Server

Instead of launching `llama-cli` for every request, the project now uses a persistent `llama-server`.

Architecture:

```
Streamlit
      │
      ▼
llama-server
      │
      ▼
Qwen2.5-1.5B
```

Keeping the model loaded in memory significantly improves responsiveness and establishes a production-style local inference architecture.

---

### Conversation Prototype

A new lightweight application, `conversation_app.py`, was created to isolate and validate the conversation engine.

Unlike the original `app.py`, the prototype focuses exclusively on conversational routing and retrieval, making development and debugging considerably simpler.

---

### End-to-End Pipeline

The complete conversation pipeline is now operational.

```
User
    │
    ▼
Streamlit
    │
    ▼
Conversation Router
    │
    ├── Alex QA
    │       │
    │       ▼
    │  Alex Retriever
    │
    ├── Kiron QA
    │       │
    │       ▼
    │  Kiron Retriever
    │
    └── Work Mode
            │
            ▼
        Agent (future integration)
    │
    ▼
llama-server
    │
    ▼
Qwen2.5-1.5B
    │
    ▼
Natural Language Response
```

---

## Engineering Decisions

Several important architectural decisions were made during this milestone.

* Retrieval remains domain-specific.
* Alex and Kiron use independent retrieval strategies.
* Python controls conversation flow.
* MiniLM performs semantic retrieval.
* The local language model is responsible only for transforming retrieved knowledge into natural language.
* Model inference is separated into a dedicated inference server (`llama-server`).

---

## Observations

Testing showed that the 1.5B model produces noticeably better grounded answers than the 0.5B model while remaining practical for local execution on older hardware.

The model still exhibits occasional conversational embellishment, but factual grounding improved significantly.

---

## Next Milestone

Integrate **Work Mode** into the new conversation prototype, allowing the same conversation engine to seamlessly switch between:

* Alex knowledge retrieval
* Kiron knowledge retrieval
* Local file operations through the existing agent

This will establish a unified conversation architecture that can later replace the original prototype application.
