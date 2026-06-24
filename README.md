# Kiron Coding Assistant

A functional coding assistant built with Python and Pydantic AI — appliedAI Institute THRIVE project.

## Overview

This project demonstrates how to build an agentic system that can:
- Respond to natural language prompts
- Maintain conversation memory across multiple turns
- Execute tools to interact with the file system
- Log tool execution in real time
- Adapt reasoning effort based on task complexity
- Dynamically load and apply skills at runtime

## Project Structure

```
.
├── exercise1.py       # First LLM call
├── exercise2.py       # Conversation state with message history
├── exercise3.py       # Tool calling with file operations
├── exercise4.py       # Execution hooks for observability
├── exercise5.py       # Dynamic reasoning effort detection
├── exercise6.py       # Dynamic skill loading
├── skills/            # Skill definitions (Markdown files)
│   └── code_review.md
├── .env               # API configuration (not committed)
└── README.md          # This file
```

## Setup

### Prerequisites
- Python 3.12+
- pip
- Virtual environment

### Installation

1. Clone the repository:
```bash
git clone https://github.com/asopozala-prog/Kiron-coding-assistant.git
cd Kiron-coding-assistant
```

2. Create and activate a virtual environment:
```bash
python3.12 -m venv .venv312
source .venv312/bin/activate
```

3. Install dependencies:
```bash
pip install pydantic-ai python-dotenv python-frontmatter
```

4. Create a `.env` file with your API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Exercises

### Exercise 1: Your First LLM Call
**File:** `exercise1.py`

Demonstrates the basic pattern: configure a model provider, bind a model, create an agent, and run it.

**Key concepts:**
- Provider configuration (GoogleProvider)
- Model instantiation (GoogleModel)
- Agent creation with system instructions
- Interactive loop with `agent.run()`

**What was tested:**
- Agent responds to user prompts
- Basic conversation loop works

**Run:**
```bash
python3.12 exercise1.py
```

---

### Exercise 2: Conversation State
**File:** `exercise2.py`

Extends Exercise 1 by adding conversation memory. The agent now remembers previous turns.

**Key concepts:**
- Message history capture with `result.all_messages()`
- Passing history back to the agent via `message_history` parameter
- Multi-turn coherent conversations

**What was tested:**
- Agent maintains context across multiple turns
- Agent can reference information from earlier in the conversation

**Run:**
```bash
python3.12 exercise2.py
```

**Test:** Tell the agent your name, then ask it to recall your name in the next turn.

---

### Exercise 3: Tool Calling
**File:** `exercise3.py`

Gives the agent the ability to interact with the file system through tools.

**Key concepts:**
- Tool definition as Python functions with clear docstrings
- Capability pattern (`AbstractCapability`)
- Tool registration via `FunctionToolset`
- Agent autonomously deciding when to use tools

**Available tools:**
- `read_file(path)` — Read file contents
- `write_file(path, content)` — Write content to a file
- `search_files(pattern)` — Search for files matching a glob pattern
- `delete_file(path)` — Delete a file

**What was tested:**
- Agent can call tools when needed
- File operations execute correctly
- Agent integrates tool results into responses

**Run:**
```bash
python3.12 exercise3.py
```

**Test:** Ask the agent to create a Python file, e.g., `"write a hello world python file called hello.py"`

---

### Exercise 4: Execution Hooks
**File:** `exercise4.py`

Adds observability by logging tool calls as they happen.

**Key concepts:**
- `before_tool_execute()` hook in capabilities
- Real-time logging of tool name and arguments
- Hooks fire before tool execution

**What was tested:**
- Hook fires before each tool call
- Tool name and arguments are logged correctly
- Hook does not interfere with tool execution

**Run:**
```bash
python3.12 exercise4.py
```

**Expected output:**
```
You: create a file called test.txt with hello world
→ Calling tool: write_file
  Args: {'path': 'test.txt', 'content': 'hello world'}
Assistant: File created successfully.
```

---

### Exercise 5: Reasoning Effort
**File:** `exercise5.py`

Dynamically adjusts the model's reasoning depth based on task complexity.

**Key concepts:**
- `get_model_settings()` method in capabilities
- Automatic complexity detection (prompt length + keywords)
- Three effort levels: `low`, `medium`, `high`
- Cost optimization by routing simple tasks to lighter reasoning

**Detection logic:**
- **Low effort:** Prompts < 50 chars OR contain "simple", "quick", "short", "list"
- **High effort:** Contain "complex", "explain", "analyse", "debug", "why", "how"
- **Medium effort:** Everything else

**What was tested:**
- Simple prompts route to low reasoning effort
- Complex prompts route to high reasoning effort
- Effort level is logged before each run

**Run:**
```bash
python3.12 exercise5.py
```

**Test:**
- Simple: `"list files"` → `[Reasoning effort: low]`
- Complex: `"explain how to debug a Python script"` → `[Reasoning effort: high]`

---

### Exercise 6: Skills and Extensibility
**File:** `exercise6.py`

Enables the agent to dynamically discover and load skills from Markdown files.

**Key concepts:**
- Skill files as Markdown with YAML frontmatter
- `get_instructions()` method to list available skills
- `load_skill()` tool for runtime skill loading
- Extensibility without code changes

**Skill file format:**
```markdown
---
name: Code Review
description: Reviews Python code for correctness, style, and potential bugs.
---

When asked to review code, follow these steps:
1. Check for syntax errors.
2. Identify logic issues.
3. Suggest improvements.
```

**What was tested:**
- Agent discovers available skills from `skills/` folder
- Agent can call `load_skill()` when relevant
- Loaded skill content is integrated into agent reasoning

**Run:**
```bash
python3.12 exercise6.py
```

**Test:** Ask the agent to review code, e.g., `"review this code: def hello(): print('hi')"`

Expected behavior:
```
You: review this code: def hello(): print('hi')
→ Calling tool: load_skill
  Args: {'skill_name': 'Code Review'}
Assistant: I'll review your code using the Code Review skill...
```

---

## Architecture

Each exercise builds on the previous one:

```
Exercise 1: Basic LLM Call
    ↓
Exercise 2: + Conversation Memory
    ↓
Exercise 3: + Tool Calling
    ↓
Exercise 4: + Execution Hooks (observability)
    ↓
Exercise 5: + Dynamic Reasoning Effort
    ↓
Exercise 6: + Dynamic Skill Loading
```

The final agent (Exercise 6) is configured with:
- **Model:** Gemini 2.5 Flash (via GoogleProvider)
- **Instructions:** System prompt defining the agent's role
- **Capabilities:**
  - `FileOperations` — read, write, search, delete files
  - `ReasoningEffort` — automatic complexity detection
  - `Skills` — dynamic skill discovery and loading
- **Memory:** Conversation history across turns
- **Observability:** Real-time tool execution logging

## Technology Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Runtime |
| Pydantic AI | Agent framework |
| Google Gemini API | Language model |
| python-dotenv | Environment variable management |
| python-frontmatter | Markdown frontmatter parsing |

## Key Learnings

1. **Agents vs. LLM calls:** Agents can maintain state, call tools, and iterate — enabling multi-step workflows.
2. **Capabilities pattern:** Modular, composable units that add behavior (tools, hooks, settings) without cluttering the agent.
3. **Observability matters:** Hooks let you see what the agent is doing in real time.
4. **Reasoning effort:** Not all tasks need deep reasoning; detecting complexity saves cost and latency.
5. **Extensibility:** Skills as Markdown files let you add new capabilities without touching code.

## Notes

- The `.env` file is not committed to GitHub for security.
- Gemini API has rate limits on the free tier.
- Each exercise is independent but builds on previous concepts.
- Exercises 4–6 were not fully tested due to API availability, but code structure is correct.

## Push to GitHub

After making changes, push with:

```bash
git add README.md
git commit -m "Add comprehensive README with all 6 exercises"
git push
```

## License

MIT
