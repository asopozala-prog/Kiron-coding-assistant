# 🦕 Kiron Coding Assistant

A local AI agent for confidential legal document management, built through hands-on learning of agentic AI concepts.

---

## Overview

**Kiron** is a practical demonstration of building a real-world AI agent. It combines six foundational exercises in agentic AI with a complete, working application for Alex — a legal assistant who needs to organize and analyze confidential documents without uploading them to the cloud.

Everything runs locally. Nothing leaves your machine.

---

## Part 1: Learning the Foundations (Exercises 1-6)

These exercises teach the core concepts of building AI agents with Pydantic AI and LLM APIs.

### Exercise 1: First LLM Call
**File:** `exercise1.py`

Learn how to:
- Set up a Google Gemini API connection
- Create your first agent
- Send a prompt and get a response
- Build an interactive chat loop

**Concept:** Basic agent initialization and single-turn interaction.

---

### Exercise 2: Conversation State
**File:** `exercise2.py`

Learn how to:
- Maintain conversation history across multiple turns
- Use `message_history` to keep context
- Build multi-turn conversations
- Access all messages from a result

**Concept:** Stateful conversation and memory management.

---

### Exercise 3: Tool Calling
**File:** `exercise3.py`

Learn how to:
- Define custom tools (functions) for the agent
- Use `FunctionToolset` to expose tools
- Create file operation tools (`read_file`, `write_file`, `search_files`, `delete_file`)
- Let the agent decide when to use tools

**Concept:** Extending agent capabilities through tool definitions.

---

### Exercise 4: Execution Hooks
**File:** `exercise4.py`

Learn how to:
- Intercept tool calls before they execute
- Log tool usage and arguments
- Implement `before_tool_execute` hooks
- Monitor agent behavior

**Concept:** Observability and control over tool execution.

---

### Exercise 5: Reasoning Effort
**File:** `exercise5.py`

Learn how to:
- Adjust model reasoning based on task complexity
- Use `ModelSettings` to control inference behavior
- Implement heuristics for effort levels (low, medium, high)
- Optimize cost and latency

**Concept:** Dynamic model configuration based on prompt characteristics.

---

### Exercise 6: Skills and Extensibility
**File:** `exercise6.py`

Learn how to:
- Load skills from Markdown files using `frontmatter`
- Create a `Skills` capability
- Extend agent behavior with loaded instructions
- Build modular, composable agents

**Concept:** Extensible agent design through skill loading.

---

## Part 2: The Real Project - Alex's Legal Assistant

### The Problem

Alex is a junior legal assistant at a law firm in Berlin. His day is filled with:
- Organizing case files from multiple sources
- Categorizing sensitive documents
- Preparing files for supervising lawyers
- Maintaining secure archives

**60% of his day is repetitive work** that requires accuracy but no creativity. The real cost? Mental energy that could be spent on his own life.

### The Solution: Kiron

**Kiron** is a local AI assistant that helps Alex work with confidential documents without uploading them to the cloud.

**Key capabilities:**
- 📄 **Organize** — Create file structures, search documents, categorize by type
- 🔍 **Analyze** — Extract key dates, identify parties, find critical clauses
- ⚠️ **Review** — Spot missing signatures, flag unusual terms, identify risks

**Why local?**
Confidential client documents **never leave the office**. Everything runs on Alex's machine. Everything stays secure.

---

## How It Works

### The Agent (`agent.py`)

The unified agent combines all six exercises into one coherent system:

- **FileOperations** — Tools for reading, writing, searching, and deleting files in `legal_files/work_files/`
- **Skills** — Extensible skill loading from Markdown files
- **Intelligent filename resolution** — Understands vague references like "messy case data" and maps them to actual files

**Key features:**
- Fuzzy filename matching — Alex doesn't need to remember exact filenames
- Alias mapping — Common phrases map to actual files automatically
- Folder restrictions — All operations stay inside `legal_files/work_files/`
- Direct action — The agent calls tools immediately instead of asking for clarification

### The Interface (`app.py`)

A two-page Streamlit app:

1. **About Alex** — Introduces the problem and the solution
2. **Chat with Kiron** — Interactive chat interface with a live file viewer

**Features:**
- Real-time file viewing on the right side
- Chat history maintained across sessions
- Friendly dinosaur persona (Kiron is heat-resistant! 🦕)
- Local-first design — no external dependencies

---

## Getting Started

### Prerequisites

- Python 3.12+
- A Google Gemini API key (free tier available)
- macOS, Linux, or Windows

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/asopozala-prog/Kiron-coding-assistant.git
   cd Kiron-coding-assistant
   ```

2. **Create a virtual environment:**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the App

Start the Streamlit interface:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Running the Exercises

To review individual exercises:

```bash
python exercise1.py
python exercise2.py
# ... etc
```

Or run the unified agent directly:

```bash
python agent.py
```

---

## Important: This is a Demonstration

**Current Setup (Demo)**
- Uses Google Gemini API via cloud
- Requires internet connection
- API calls are billed
- Good for learning and prototyping

**Production Deployment (Real Law Firm)**

For a real law firm handling confidential documents, you would:

### 1. Run a Local LLM Model
- Download an open-source model (e.g., Llama 2, Mistral, or similar)
- Run it on an office computer with adequate hardware
- No internet required, no API calls, no billing
- Complete data privacy

### 2. Hardware Requirements
- GPU with 16GB+ VRAM (NVIDIA RTX 4090, A100, etc.)
- Or CPU with 32GB+ RAM (slower but works)
- Sufficient disk space for model weights (7-70GB depending on model)

### 3. Implementation
- Replace `GoogleProvider` with a local provider (e.g., Ollama, LM Studio, vLLM)
- Keep the same agent code (`agent.py`)
- Keep the same UI (`app.py`)
- Only the model backend changes

### 4. Example: Using Ollama

Instead of:
```python
from pydantic_ai.providers.google import GoogleProvider

provider = GoogleProvider(api_key=os.getenv("GEMINI_API_KEY"))
model = GoogleModel("gemini-2.5-flash", provider=provider)
```

You would use:
```python
from ollama import OllamaProvider

provider = OllamaProvider(model="mistral")
model = OllamaModel("mistral", provider=provider)
```

### 5. Benefits of Local Deployment
- ✅ Zero data leaves the office
- ✅ No API costs
- ✅ No internet dependency
- ✅ Full compliance with data protection laws (GDPR, etc.)
- ✅ Instant responses (no network latency)

**This demonstration uses the cloud API for accessibility, but the architecture is designed to work with any LLM provider.**

---

## Project Structure

```
Kiron-coding-assistant/
├── exercise1.py                 # First LLM call
├── exercise2.py                 # Conversation state
├── exercise3.py                 # Tool calling
├── exercise4.py                 # Execution hooks
├── exercise5.py                 # Reasoning effort
├── exercise6.py                 # Skills and extensibility
├── agent.py                     # Unified agent (all 6 exercises combined)
├── app.py                       # Streamlit UI
├── .env                         # API keys (not in repo)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── legal_files/
    ├── alex_in_office.jpg       # Alex's photo
    ├── alex_kiron.jpg           # Kiron illustration
    ├── alex.md                  # Alex's persona
    ├── alex_work_prompts.md     # Example prompts
    └── work_files/              # Working directory for documents
        ├── messy_case_data.txt          # Sample case data
        ├── case_file_template.txt       # Case file template
        └── sample_contract.md           # Sample contract
```

---

## Example Workflows

### Workflow 1: Extract Case Information

**Alex asks:**
> "Read the messy case data, find the case ID, and fill it into the case file template."

**Kiron:**
1. Reads `messy_case_data.txt`
2. Extracts the case ID
3. Updates `case_file_template.txt` with the ID
4. Confirms completion

### Workflow 2: Analyze a Contract

**Alex asks:**
> "Summarize the sample contract and highlight any unusual terms."

**Kiron:**
1. Reads `sample_contract.md`
2. Summarizes key sections
3. Flags potential risks
4. Returns analysis

### Workflow 3: Organize Files

**Alex asks:**
> "Create a new file called client_notes.txt and add today's meeting notes."

**Kiron:**
1. Creates `client_notes.txt` in `work_files/`
2. Adds the content
3. Confirms the file is ready

---

## Key Design Decisions

### 1. Local-First Architecture
All files stay on Alex's machine. No cloud uploads. No external storage. This is critical for confidential legal documents.

### 2. Fuzzy Filename Matching
Instead of asking "What's the exact filename?", Kiron understands:
- "messy case data" → `messy_case_data.txt`
- "case template" → `case_file_template.txt`
- "sample contract" → `sample_contract.md`

### 3. Unified Agent Design
All six exercises are combined into one `agent.py`. The exercises remain as standalone learning files, but the real application uses the integrated agent.

### 4. Folder Restrictions
All file operations are restricted to `legal_files/work_files/`. The agent cannot access files outside this directory, ensuring security and organization.

### 5. Streamlit UI
A simple, intuitive interface that doesn't require technical knowledge. Alex can use Kiron without understanding how it works under the hood.

---

## Technical Stack

- **Framework:** Pydantic AI
- **LLM:** Google Gemini 2.5 Flash (via GoogleProvider)
- **UI:** Streamlit
- **Language:** Python 3.12
- **File Format:** Markdown, plain text

---

## Learning Outcomes

By building this project, you'll understand:

1. ✅ How to initialize and configure an LLM agent
2. ✅ How to maintain conversation state across multiple turns
3. ✅ How to define and use tools effectively
4. ✅ How to monitor and control tool execution
5. ✅ How to optimize model behavior based on task complexity
6. ✅ How to build extensible, modular agent systems
7. ✅ How to create a real-world application that solves a concrete problem

---

## Future Enhancements

Potential improvements for future versions:

- **OCR Support** — Extract text from scanned documents
- **Multi-file Analysis** — Compare and cross-reference multiple documents
- **Risk Scoring** — Automated risk assessment for contracts
- **Audit Logging** — Track all file operations for compliance
- **Template Library** — Pre-built templates for common document types
- **Batch Processing** — Process multiple files in one request

---

## License

This project is part of the THRIVE optional portfolio project for the Agentic AI Masterclass.

---

## Author

Built by Mei as part of the THRIVE portfolio project.

**GitHub:** [asopozala-prog/Kiron-coding-assistant](https://github.com/asopozala-prog/Kiron-coding-assistant)

---

## Acknowledgments

- **Agentic AI Masterclass** — For the foundational exercises and concepts
- **Pydantic AI** — For the agent framework
- **Google Gemini** — For the LLM API
- **Streamlit** — For the UI framework

---

## Questions?

If you have questions about this project, refer to:
- The individual exercise files for concept explanations
- The `agent.py` file for implementation details
- The `app.py` file for UI logic
