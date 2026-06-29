# Debugging Report — Streamlit UI vs Local LLM Pipeline

**Date**

2026-06-28 → 2026-06-29

---

# Objective

Replace the cloud LLM with a fully local inference pipeline using **llama.cpp** while preserving Kiron's conversation architecture.

---

# Initial Problem

The local model generated correct responses from the terminal, but the Streamlit interface remained in the **"Thinking..."** state.

The UI never displayed the generated response.

This suggested that the failure occurred somewhere between the user interface and the local inference pipeline.

---

# Ground Truth

The following components were verified during the investigation.

## Local Model

Verified.

* Qwen2.5-1.5B-Instruct (GGUF) loaded successfully.
* The model generated correct responses using `llama-cli`.

---

## Local Inference Server

Verified.

* `llama-server` started successfully.
* The server listened on port **8080**.
* HTTP requests returned valid JSON responses.

---

## Retrieval

Verified.

Both retrieval pipelines worked correctly.

* Alex Retriever
* Kiron Retriever

Relevant context was successfully passed to the language model.

---

## Answer Generator

Verified.

The answer generators successfully communicated with `llama-server`.

Responses were received from the local model.

---

# Investigation

Several possible causes were examined.

Examples included:

* Streamlit rendering
* Conversation routing
* Response handling
* `agent.py`
* Gemini integration
* `llama-cli`
* `llama-server`

Multiple edits were attempted inside the original application without changing the observed behaviour.

---

# Strategy Change

After repeated attempts produced the same symptoms, the debugging strategy changed.

Instead of continuing to modify the original application, a new prototype was created.

**conversation_app.py**

Purpose:

A minimal application dedicated to testing only the conversation architecture.

This isolated the conversation pipeline from the original portfolio application.

---

# Results

The prototype successfully demonstrated:

* Streamlit UI
* Conversation routing
* Retriever
* Local answer generation
* `llama-server`
* Local Qwen model

The response appeared correctly inside the new application.

---

# Engineering Lessons

## 1. Detect Debugging Loops

When repeated fixes produce identical results, stop modifying the same code.

Change the debugging strategy instead.

---

## 2. Verify One Layer at a Time

Treat the application as independent layers.

```text
User
    ↓
Streamlit
    ↓
Conversation Router
    ↓
Retriever
    ↓
Answer Generator
    ↓
llama-server
    ↓
Local Language Model
```

Each layer should be verified independently.

---

## 3. Build Small Prototypes

A minimal prototype is often easier to validate than repairing a growing application.

The prototype became the new development foundation.

---

## 4. Separate Demonstration from Development

The project now has two applications.

**app.py**

Original portfolio demonstration.

**conversation_app.py**

Development prototype for the modular conversation architecture.

Separating these responsibilities significantly reduced debugging complexity.

---

# Outcome

This debugging session verified the complete local AI pipeline.

The project now supports:

* local semantic retrieval
* local inference
* modular conversation routing
* independent conversation prototype
* local `llama-server`

---

# Follow-up

Future conversation development should continue in **conversation_app.py**.

The original **app.py** remains the portfolio demonstration until the new architecture is ready for integration.

---

# Lesson Learned

The largest improvement did not come from another code change.

It came from changing the debugging strategy.

Instead of continuing to repair a complex application, we isolated the subsystem, verified each layer independently, and established a new, modular foundation for future development.
