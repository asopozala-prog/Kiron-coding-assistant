# Milestone 02 Alex Retrieval Pipeline



A dedicated retriever has been implemented specifically for Alex.

Unlike traditional RAG systems that embed arbitrary document chunks, the Alex retriever operates on structured topic objects.

## Goal

Retrieve the smallest amount of information necessary while preserving semantic understanding.

---

## Retrieval Architecture

### 1. Python parses the knowledge base

Python reads every Markdown document inside `legal_files/rag/alex`.

Each `# Topic:` section becomes a structured topic object containing:

* Topic
* Summary
* Key facts
* Narrative
* Related topics
* Retrieval tags

---

### 2. MiniLM performs semantic retrieval

The user's complete natural-language question is embedded using MiniLM.

Each topic is represented by its Retrieval Tags.

MiniLM compares the semantic meaning of the user's question against the retrieval tags of every topic.

---

### 3. Python selects the best topics

Python ranks the similarity scores returned by MiniLM.

The two highest-ranked topics are selected.

---

### 4. Python prepares the LLM context

Only the raw **Summary** content from the selected topics is returned.

Markdown headings, retrieval metadata, and other sections are intentionally excluded to minimize token usage.

---

# Design Principles

## Separation of Responsibilities

Python is responsible for knowledge structure.

MiniLM is responsible for semantic understanding.

The language model is responsible only for generating a natural conversational answer.

In short:

> MiniLM decides **where to look**.
> Python decides **what information to return**.

---

## Domain-Specific Retrievers

Retrievers belong to the knowledge domain rather than the framework.

Instead of one generic retriever, each knowledge base may define its own retrieval strategy.

Example:

```text
alex_retriever.py
kiron_retriever.py
future_retrievers...
```

This allows retrieval logic to evolve independently for different knowledge bases while sharing the same conversation engine.

---

# Current Pipeline

```text
User Question
        │
        ▼
Python parses Markdown
        │
        ▼
MiniLM Semantic Retrieval
(using Retrieval Tags)
        │
        ▼
Top 2 Related Topics
        │
        ▼
Python extracts Summary
        │
        ▼
Tiny Local LLM
        │
        ▼
Final Conversational Answer
```

---

# Current Status

Completed:

* Conversation engine
* Stateful routing
* Workspace validation
* Structured Alex knowledge base
* Semantic retrieval with MiniLM
* Topic-based retrieval architecture

The retrieval pipeline is operational.

---

# Next Milestone

Integrate a lightweight local language model using `llama.cpp`.

The language model will receive:

* the user's original question
* the retrieved summaries

Its responsibility is to transform the retrieved knowledge into a concise, natural conversational response while remaining grounded in the supplied context.
