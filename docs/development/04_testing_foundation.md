# 04 – Testing Foundation

---

# Purpose

This document records the design, evolution, lessons learned, and current architecture of the Kiron testing framework.

It serves two purposes:

1. Documentation of the project's testing strategy.
2. Engineering memory, preserving important decisions and preventing future developers (including future Alex) from repeating unsuccessful experiments.

This document should be updated whenever the testing architecture changes significantly.

---

# Background

Testing was introduced after the initial conversation prototype had become stable.

Originally, development relied primarily on manual testing:

- modify code
- launch Streamlit
- manually click through conversations
- verify behavior by observation

Although workable for a small prototype, this quickly became inefficient.

Problems included:

- regressions appearing unexpectedly
- repeated manual verification
- uncertainty after refactoring
- increasing development time

The project therefore adopted pytest as the primary verification framework.

---

# Testing Philosophy

Kiron follows several principles.

## 1. Test behavior, not implementation

Tests verify observable behavior rather than internal implementation details whenever possible.

For example:

Instead of verifying that a helper function is called,

verify that:

- the correct conversation state is reached
- the correct answer is returned
- the correct routing decision is made

This allows internal refactoring without breaking tests.

---

## 2. Small deterministic tests first

Development follows a layered approach.

Each software layer is verified independently before introducing additional dependencies.

The preferred order is:

Pure Python

↓

Retrieval

↓

Local LLM

↓

Complete application

This dramatically simplifies debugging.

---

## 3. Ground truth over assumptions

Tests are written against verified behavior.

Whenever uncertainty exists:

- inspect actual program output
- inspect retrieval results
- inspect model responses

Only then should assertions be written.

Several tests were corrected after discovering that assumptions did not match real behavior.

---

## 4. Tests document expected behavior

Each test represents an executable software specification.

Future developers should be able to understand expected behavior simply by reading the tests.

---

# Testing Architecture

```
tests/
│
├── conversation/
│
├── integration/
│
├── retrieval/
│
├── test_*.py
│
└── (future)
    └── e2e/
```

---

# Phase 1 — Unit Testing

## Objective

Protect deterministic Python logic.

No external services.

No embedding models.

No local LLM.

---

## Protected Modules

- task_validator.py
- work_mode_handler.py
- entry_rules.py
- menu_handler.py
- kiron_mode_handler.py
- alex_qa_handler.py
- kiron_qa_handler.py
- kiron_router_pipeline.py
- llm_client.py
- alex_answer_generator.py
- kiron_answer_generator.py

---

## Engineering Improvements

Phase 1 immediately revealed several software issues.

Examples include:

### Identity recognition bug

Originally:

```
Alex is great
```

incorrectly identified the user as Alex.

The identity rules were rewritten and expanded.

---

### Confirmation handling

The original implementation only recognized:

```
I am Alex
```

The UI later evolved to ask:

```
Are you Alex?
```

Therefore the rules were extended to accept:

- yes
- y
- yep
- yeah
- correct
- it is me
- it's me

while rejecting:

- no
- not Alex

This refinement was driven directly by pytest.

---

### Conversation improvements

Tests exposed several small inconsistencies between conversation design and implementation.

Rather than adjusting tests to match bugs, software behavior was refined.

---

# Phase 2 — Conversation Testing

## Objective

Protect complete conversation flows.

These tests verify interactions between multiple modules.

Examples:

Visitor

↓

Entry

↓

Menu

↓

Office

Current flows include:

- Visitor → Office
- Visitor → Kiron
- Visitor → Alex
- Invalid menu choice
- Alex confirmation

Conversation tests remain intentionally lightweight because the UI continues to evolve.

---

# Phase 3A — Retrieval Foundation

## Objective

Verify deterministic retrieval behavior.

No embedding model.

Focus:

- Markdown parsing
- metadata extraction
- section extraction
- chunk loading
- helper functions

---

## Alex Retrieval

Protected:

- Summary extraction
- Retrieval tag extraction
- Topic parsing
- Cosine similarity helper

---

## Kiron Retrieval

Protected:

- Markdown loading
- Rule exclusion
- Empty document skipping
- Cosine similarity helper

---

# Phase 3B — Semantic Retrieval

MiniLM introduced the first AI dependency.

Unlike deterministic parsing tests, semantic retrieval depends upon embedding quality.

Tests therefore verify ranking rather than exact similarity values.

Important lesson:

Never assume which document should rank first.

Always inspect real retrieval results before writing assertions.

Example:

An early assumption expected:

```
Basic Identity
```

Actual retrieval produced:

```
Identity Index
```

The test was corrected to match verified behavior.

---

# Phase 4 — Local LLM Integration

This phase introduced:

- llama-server
- local GGUF models
- HTTP inference
- answer generators

---

## Mock Testing

The following components remain unit-tested using mocks:

- llm_client
- answer generators

This keeps the fast suite independent from external services.

---

## Real Integration

Real integration tests verify:

Retriever

↓

Prompt Builder

↓

HTTP Client

↓

llama-server

↓

Qwen

↓

Generated Answer

These tests proved that:

- retrieval works
- prompt construction works
- local inference works

---

## Important Discovery

The 1.5B Qwen model occasionally copied prompt instructions into its answer.

Example:

```
Answer in two sentences...
```

appeared inside the response.

This was determined to be a model limitation rather than a software defect.

Integration assertions were therefore rewritten to verify stable factual content rather than exact wording.

---

# Integration Testing

Integration tests require:

- llama-server
- local GGUF model

These tests are marked using:

```
@pytest.mark.integration
```

Configured in:

```
pytest.ini
```

Commands:

Fast development:

```
python -m pytest -m "not integration"
```

Integration only:

```
python -m pytest -m integration
```

Complete suite:

```
python -m pytest
```

---

# Important Lessons Learned

## Replace large files directly

Originally we attempted large shell patches.

This repeatedly produced:

- malformed files
- escaped newline issues
- patch failures

Current rule:

Small change

→ shell patch

Large rewrite

→ replace entire file in editor

This significantly reduced errors.

---

## One file at a time

Editing multiple files simultaneously caused avoidable confusion.

Current workflow:

- open one file
- finish one task
- run pytest
- continue

---

## Write tests after verifying behavior

Never write tests based on assumptions.

Always inspect:

- retrieval output
- model output
- routing output

first.

---

## Integration assertions should be tolerant

Large language models are probabilistic.

Do not verify exact wording.

Instead verify:

- important entities
- important facts
- grounding

Example:

Bad:

```
assert answer == ...
```

Better:

```
assert "Alex Hoffmann" in answer
```

---

# Current Test Architecture

Fast Suite

Includes:

- unit tests
- conversation tests
- retrieval parsing
- semantic retrieval

Current:

```
61 passing
```

---

Integration Suite

Includes:

- Alex local pipeline
- Kiron local pipeline

Requires:

- llama-server

Current:

```
2 passing
```

---

Total

```
63 automated tests
```

---

# Remaining Work

## Future Phase — End-to-End

Planned.

These tests will automate the actual Streamlit interface.

Expected architecture:

User

↓

Browser

↓

Streamlit

↓

Conversation

↓

Retriever

↓

LLM

↓

Answer

Possible tooling:

- Playwright

E2E testing will begin only after the UI becomes stable.

Maintaining browser tests during rapid UI iteration would create unnecessary maintenance cost.

---

# Development Workflow

The project now follows a consistent engineering workflow.

1. Discuss desired behavior.
2. Verify existing behavior.
3. Implement one logical change.
4. Run pytest.
5. Fix failures.
6. Verify complete suite.
7. Update documentation.
8. Commit milestone.

This workflow has proven significantly more reliable than relying on manual verification alone.

---

# Conclusion

Testing is now a permanent architectural component of Kiron.

The project has progressed from manual verification to a layered testing framework covering deterministic software, retrieval logic, local AI integration, and future end-to-end validation.

The objective is not to maximize the number of tests.

The objective is to maximize confidence while keeping tests maintainable, meaningful, and closely aligned with real system behavior.