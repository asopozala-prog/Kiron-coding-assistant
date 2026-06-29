# Milestone 01 — Conversation Engine

## Objective

Build a deterministic conversation engine that controls Kiron's workflow before introducing retrieval or language models.

The conversation engine is intentionally implemented with Python state management rather than relying on an LLM. This ensures that navigation, workflow control, and user guidance remain predictable and inexpensive.

---

# Conversation Flow

The conversation begins in **Entry Mode**.

## Alex Recognition

If the user identifies themselves as Alex, for example:

* "I'm Alex."
* "Hello, I am Alex."
* "Alex here."

Kiron immediately enters Work Mode.

Example:

```text
Hello Alex! 🦕
Glad to see you again.
Let's get to work.

Which file would you like to work on today?
```

Identity recognition is intentionally flexible rather than dependent on fixed phrases.

---

## Standard Entry

If Alex is not detected, Kiron introduces itself:

```text
Hello! I'm Kiron 🦕, Alex's assistant.

What would you like to do?

1. 📄 Work with files
2. 🦕 Ask about me or the Kiron Project
3. 👤 Learn more about Alex
```

The entry intentionally limits the assistant to three clearly defined responsibilities.

---

# Conversation States

The conversation engine is implemented as a Python state machine.

Current states:

```text
Entry
    │
    ├── Work Mode
    ├── Kiron Mode
    └── Alex Mode
```

Each state has its own handler and controls its own conversation flow.

---

# Work Mode

Work Mode is file-oriented.

Before any LLM is called, Python validates the user's request.

The workspace is restricted to:

```text
legal_files/work_files
```

Python checks whether the user's request references an existing file or requests creation of a new one.

Only valid work requests continue to the language model.

---

## Progressive Fallback

If no valid file action is detected, Kiron guides the conversation.

### First reminder

Kiron lists the available files and asks the user to choose one or create a new file.

### Second reminder

If the user continues with unrelated conversation:

```text
Alex, let's stay with the work path.

Please name one file, or ask me to create a new file.
```

### Final reminder

After repeated invalid inputs:

```text
Alex, I think you may need a break.

I'll reset for now — see you later.
```

The conversation then returns to Entry Mode.

---

# Kiron Mode

Selecting Kiron Mode transfers future questions to the Kiron knowledge system.

The conversation remains inside Kiron Mode until the user exits or the conversation is reset.

---

# Alex Mode

Selecting Alex Mode transfers future questions to the Alex knowledge system.

The conversation remains inside Alex Mode until the user exits or the conversation is reset.

---

# Design Principles

The conversation engine separates workflow control from language generation.

Python is responsible for:

* Conversation state
* Routing
* File validation
* Workspace safety
* User guidance

Language models are responsible only for answering questions after Python has determined the correct workflow.

---

# Current Architecture

```text
User
    │
    ▼
Conversation State
(Python)
    │
    ├── Work Mode
    │       │
    │       ▼
    │   Workspace Validation
    │       │
    │       ▼
    │      LLM
    │
    ├── Kiron Mode
    │       │
    │       ▼
    │   (Future Retrieval)
    │
    └── Alex Mode
            │
            ▼
      (Future Retrieval)
```

---

# Result

The conversation engine is fully operational.

All routing decisions are deterministic, file operations are validated before any LLM interaction, and each conversation path is isolated into its own workflow.

This provides a stable foundation for introducing retrieval systems and local language models in later milestones.
