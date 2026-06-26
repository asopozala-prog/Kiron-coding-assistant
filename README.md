# 🦕 Kiron Coding Assistant — A Local Agent Prototype for Confidential Work

Kiron is a **demonstration prototype** that shows how to build an AI agent that can work with **confidential documents** in a **local, sandboxed workspace**.

This project is framed as a story:
- **Alex Hoffmann**, a junior legal assistant, is overloaded with repetitive document work.
- The office cannot use cloud AI tools for client files.
- **Kiron** (a friendly dinosaur assistant) runs locally and manipulates only the documents inside a protected work folder.

> This is not a “general AI chatbot app.” It is a **portfolio demo** of a local-first agent workflow for sensitive data.

---

## Live Demo

If you deployed it on Streamlit Community Cloud, add your link here:

- **Demo:** (paste your Streamlit URL)

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

## Credits

Built by Mei as a THRIVE optional portfolio project.

- GitHub: https://github.com/asopozala-prog/Kiron-coding-assistant
