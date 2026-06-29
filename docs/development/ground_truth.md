# Ground Truth — Kiron Coding Assistant

**Date**

2026-06-29

This document records the verified state of the Kiron project at the current milestone.

Only verified information belongs here.

---

# 1. Workspace

**Project**

Kiron Coding Assistant

**Repository**

Kiron-coding-assistant

**Version**

Milestone 03

---

# 2. Development Environment

**Python**

Python 3.12.x

**Virtual Environment**

`.venv`

**Package Manager**

`pip`

**Requirements**

`requirements.txt`

---

# 3. Runtime Environment

## Streamlit Applications

### app.py

Status:

Working.

Purpose:

Original portfolio demonstration application.

Default Port:

8501

---

### conversation_app.py

Status:

Working.

Purpose:

Primary development application for the modular conversation architecture.

Default Port:

8502

---

## Local AI Runtime

Inference Server:

`llama-server`

Status:

Working.

Default Port:

8080

Model Directory:

`models/llm/`

Current Model:

Qwen2.5-1.5B-Instruct (GGUF)

---

# 4. Project Structure

Verified major directories:

```text
src/
legal_files/
docs/development/
models/
skills/
```

Verified primary applications:

* app.py
* conversation_app.py

Verified documentation:

* README
* Development milestones
* Ground Truth Checklist
* Workspace State Map
* VS Code Co-working Principles

---

# 5. Dependency Map

Verified conversation flow:

```text
conversation_app.py
        │
        ▼
Conversation Router
        │
        ├── Entry Rules
        ├── Menu Handler
        ├── Work Mode
        ├── Alex QA
        └── Kiron QA
                │
                ▼
           Retriever
                │
                ▼
       Answer Generator
                │
                ▼
         llama-server
                │
                ▼
        Qwen2.5-1.5B
```

---

# 6. Current Implementation

Verified:

* Modular conversation routing
* Alex Retriever
* Kiron Retriever
* MiniLM semantic retrieval
* Local llama-server integration
* Local Qwen inference
* Original Streamlit portfolio application
* Conversation prototype application
* Engineering documentation workflow
* GitHub repository

---

# 7. Current Workspace State

Verified working:

* conversation_app.py returns responses from the local model.
* Alex QA is operational.
* Kiron QA is operational.
* llama-server is serving requests.
* Qwen2.5-1.5B is used for local inference.
* The repository has been updated to the new modular architecture.

Known limitations:

* `app.py` and `conversation_app.py` currently coexist.
* Work Mode has not yet been fully migrated into the new conversation application.
* Prompt engineering for the local model is still being refined.

---

# 8. Documentation

Verified documentation:

* README
* Architecture documents
* Development milestones
* Ground Truth Checklist
* Workspace State Map
* VS Code Co-working Principles
* Kiron RAG documents
* Alex RAG documents

---

# 9. Current Engineering Direction

The current development focus is:

* expanding the modular conversation architecture
* integrating Work Mode into `conversation_app.py`
* refining local model prompting
* documenting engineering decisions alongside implementation

No architectural redesign is currently planned.

Development continues by extending the existing modular architecture.
