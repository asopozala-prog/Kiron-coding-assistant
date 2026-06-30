# 🦕 Kiron Coding Assistant — A Local Agent Prototype for Confidential Work

Kiron is a **demonstration prototype** that shows how to build an AI agent that can work with **confidential documents** in a **local, sandboxed workspace**.

This project is framed as a story:
- **Alex Hoffmann**, a junior legal assistant, is overloaded with repetitive document work.
- The office cannot use cloud AI tools for client files.
- **Kiron** (a friendly dinosaur assistant) runs locally and manipulates only the documents inside a protected work folder.

> This is not a “general AI chatbot app.” It is a **portfolio demo** of a local-first agent workflow for sensitive data.

---

## Live Demo

deployed on Streamlit Community Cloud:

- **Demo:** ([https://kiron-coding-assistant-x3d9klzag52v4rc92zress.streamlit.app/?page=about])

> Note: Streamlit Cloud still uses a cloud API key in this demo. In a real office deployment, you would swap the model backend to a local LLM.

---

## What This Demonstration Proves

### 1) Local-first document workflow
Kiron only reads/writes within:

- `legal_files/work_files/`

This mirrors how a real office might enforce confidentiality:
- documents stay in a known workspace
- file access is sandboxed
- you can audit what the agent touches

### 2) An agent that can *act*, not just chat
Kiron uses tool calling to:
- read documents
- write updated files
- search files
- delete **non-protected** demo files

### 3) Realistic UX for non-technical users
The Streamlit UI is designed like a small product demo:
- visitor-friendly narrative pages
- a chat page where Alex works with Kiron
- a live file viewer showing changes as they happen

---

## The App (Streamlit UI)

### Pages
- **Meet Alex Hoffmann** — who Alex is and what problem he faces
- **Why Alex Need Kiron** — Alex’s dilemma + the life he wants back
- **How Kiron Was Built** — the build story + technical summary
- **Alex work with Kiron** — the live demo: chat + working folder viewer

### Alex’s working folder
On the chat page, the right panel shows **Alex’s working folder**.
When Alex asks Kiron to create/edit a file, you can see the change appear there.

---

## The Agent (`agent.py`)

### Key behaviors
- **Workspace sandbox**: all file operations are restricted to `legal_files/work_files/`
- **Filename resolution**: handles vague references (e.g., “messy case data”) through aliases + fuzzy matching
- **Protected files**: core demo files cannot be deleted by the agent (with a friendly fallback message)

### Protected files (cannot be deleted by Kiron)
- `alex.md`
- `case_file_template.txt`
- `messy_case_data.txt`
- `sample_contract.md`

---

## Learning Path (Exercises 1–6)

This project was built by working through a structured set of exercises and then integrating them into one coherent agent.

- `exercise1.py` — first LLM call
- `exercise2.py` — conversation state
- `exercise3.py` — tool calling
- `exercise4.py` — execution hooks
- `exercise5.py` — reasoning effort
- `exercise6.py` — skills + extensibility

The final demo app uses the unified agent in `agent.py`.

---

## Run Locally

### 1) Install

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Set API key

Create `.env`:

```bash
GEMINI_API_KEY=your_key_here
```

### 3) Run the app

```bash
streamlit run app.py
```

---

## Deploy (Streamlit Community Cloud)

1. Push the repo to GitHub
2. Deploy `app.py`
3. Add Streamlit secrets (TOML):

```toml
GEMINI_API_KEY = "your_key_here"
```

### Important note about filenames on Streamlit Cloud
Streamlit Cloud runs on Linux, which is **case-sensitive**.
Use consistent lowercase filenames for images (e.g., `alex_cafe.jpg`, not `Alex_Cafe.png`).

---

## Production Reality Check (Real Office Deployment)

This demo uses Gemini via API because it’s easy to run anywhere.

For a **real law firm / sensitive-data workplace**, the recommended setup is:

- run a **local LLM** on an office machine (Ollama / LM Studio / vLLM)
- keep the same tools + UI
- only swap the model provider

Benefits:
- no cloud processing
- no API billing
- no internet dependency
- stronger confidentiality guarantees

---

## Project Structure

```
Kiron-coding-assistant/
├── app.py
├── agent.py
├── requirements.txt
├── README.md
├── exercise1.py … exercise6.py
├── skills/
└── legal_files/
    ├── work_files/
    │   ├── messy_case_data.txt
    │   ├── case_file_template.txt
    │   ├── sample_contract.md
    │   └── (demo-created files appear here)
    ├── alex_in_office.jpg
    ├── alex_kiron.jpg
    ├── alex_overwork.jpg
    ├── alex_cafe.jpg
    ├── alex_bar.jpg
    ├── Statement_to_Programmer.md
    ├── alex_wanted_life.md
    └── kiron_programmer.md
```

---

# Modular Conversation and Retrieval Architecture

The project has evolved beyond a simple local file agent into a modular **local conversational AI architecture**.

Instead of relying on one general-purpose language model, Kiron now separates the system into independent components, each responsible for a specific task.

## Conversation Engine

The conversation flow is now managed entirely by Python.

The engine maintains conversation state and routes each user request into one of three specialized modes:

* 📄 Work with files
* 🦕 Learn about Kiron
* 👤 Learn about Alex

This design keeps the conversation deterministic while allowing each domain to evolve independently.

---

## Domain-Specific Retrieval

Rather than using a single generic RAG pipeline, Kiron uses dedicated retrievers for different knowledge domains.

### Alex Retriever

Alex's knowledge base is organized into structured topic documents.

Each topic contains:

* Summary
* Key facts
* Narrative
* Related topics
* Retrieval tags

MiniLM performs semantic retrieval using the retrieval tags, while Python prepares a minimal context for the language model.

### Kiron Retriever

Kiron follows a different retrieval strategy.

For broad questions, MiniLM retrieves the most relevant documentation chunks.

For core topics such as:

* Who created Kiron?
* How does Kiron work?
* Why was Kiron designed?

the conversation engine returns complete technical articles directly.

This demonstrates that different knowledge domains can use different retrieval strategies without changing the overall architecture.

---

## Local Language Model

The retrieved knowledge is transformed into natural language by a lightweight local language model.

Current implementation:

* **llama.cpp**
* **llama-server**
* **Qwen2.5-1.5B-Instruct (GGUF)**

The language model is responsible only for rewriting retrieved knowledge into concise conversational answers.

It does not perform retrieval itself.

---

## Complete Local Pipeline

```
User
    │
    ▼
Conversation Router
    │
    ▼
Domain-specific Retriever
    │
    ▼
MiniLM Semantic Search
    │
    ▼
Retrieved Knowledge
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

This architecture allows every component to evolve independently.

Retrievers, language models, and user interfaces can all be replaced without redesigning the overall system.

---

## Conversation Prototype

A second Streamlit application, `conversation_app.py`, has been introduced as a clean prototype for the new architecture.

Unlike the original demonstration app, the prototype focuses entirely on validating the conversation engine and retrieval pipeline.

This approach allows rapid experimentation while keeping the original showcase application stable.

---

## Development Philosophy

The project follows an iterative engineering approach.

Rather than attempting to build a complete AI assistant in one step, each milestone introduces one production-oriented capability:

* local document agent
* structured retrieval
* domain-specific RAG
* local language model
* conversational routing

Each milestone remains fully documented inside the `docs/development/` folder, providing a complete engineering history of the project.

## Credits

Built by Mei as a THRIVE optional portfolio project.

- GitHub: https://github.com/asopozala-prog/Kiron-coding-assistant

# 04 – Testing Strategy

## Purpose

Kiron is developed using a staged testing strategy.

The objective is to verify deterministic software behavior first, then progressively validate integration with retrieval systems, local language models, and the complete application.

This approach keeps development fast, reduces debugging complexity, and protects existing functionality as the project grows.

---

# Current Status

Current milestone:

**Phase 1 — Unit Testing**

Status:

**In Progress**

Current verified result:

**27 passing unit tests**

---

# Testing Roadmap

## Phase 1 — Unit Tests

Objective:

Protect deterministic business logic.

External services are not required.

Covered modules:

- ✅ task_validator.py
- ✅ work_mode_handler.py
- ✅ entry_rules.py
- ✅ menu_handler.py
- ✅ kiron_mode_handler.py
- ✅ alex_qa_handler.py

Remaining candidates:

- kiron_qa_handler.py
- kiron_router_pipeline.py

Typical techniques:

- pytest
- unittest.mock
- temporary workspaces
- deterministic assertions

Protected behaviors include:

- conversation entry rules
- identity recognition
- menu routing
- work mode transitions
- task validation
- helper functions
- orchestration between internal components

---

## Phase 2 — Conversation Routing

Objective:

Verify complete conversation routing.

Examples:

- entry → menu
- menu → work
- menu → Kiron
- menu → Alex
- conversation state transitions
- router pipeline

---

## Phase 3 — Retriever Tests

Objective:

Verify retrieval independently from the language model.

Approach:

- tiny local RAG documents
- deterministic retrieval expectations
- similarity threshold validation

External services:

No LLM required.

---

## Phase 4 — Local LLM Integration

Objective:

Verify integration with the local language model.

Components:

- llama-server
- Qwen GGUF model
- answer generators
- llm_client

Requirements:

- local inference server running
- model loaded
- endpoint reachable

These are integration tests.

---

## Phase 5 — End-to-End Tests

Objective:

Verify the complete user workflow.

Pipeline:

Browser

↓

Streamlit UI

↓

Conversation Router

↓

Retriever

↓

Answer Generator

↓

llama-server

↓

Qwen Model

↓

Response

These tests validate the complete application from the user's perspective.

---

# Engineering Principles

Testing is treated as part of the software architecture.

The project follows these principles:

- verify deterministic logic before integration
- isolate external dependencies with mocks whenever appropriate
- test one software responsibility at a time
- document testing milestones alongside implementation
- use small, reproducible test cases

The goal is not maximum test count.

The goal is confidence that Kiron's software contracts continue to behave correctly while the project evolves.

---

# Current Milestone Summary

Verified:

- deterministic conversation engine largely protected
- conversation routing components progressively covered
- mock-based orchestration testing established
- reusable pytest workflow established
- shell-assisted patch workflow integrated into development

Development continues by completing Phase 1 before expanding into retriever, local LLM, and end-to-end integration testing.