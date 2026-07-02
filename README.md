streamlit App link:
https://kiron-coding-assistant-x3d9klzag52v4rc92zress.streamlit.app/?page=built

````markdown
# Kiron Local AI Workspace Prototype

## What This Project Is

Kiron is an experimental prototype for designing customizable local AI workspaces for people who understand their professional domain but do not have a deep technical background.

It is not a market-ready product, a general online chatbot, or an application designed for mass public use.

The current Streamlit application is a public demonstration interface. It allows visitors to meet a representative user, Alex Hoffmann, understand his working problems, and see how a Kiron-style workspace could support confidential document work.

Alex represents a wider group of professionals working across legal, administrative, financial, educational, healthcare, and other knowledge-based environments. They understand their work, constraints, and responsibilities, but may not know how a local AI system could be designed around their individual workspace.

The demonstration therefore answers four practical questions:

- What can a local AI workspace do?
- Why might a professional need one?
- How can it work with confidential documents?
- How can the same architecture be customized for another user or domain?

The project focuses on the software structure behind the demonstration. It develops and tests reusable components for conversation routing, retrieval, file operations, local language-model inference, agent tools, documentation, and testing.

The current implementation is still under active development. Its purpose is to establish small, functioning pipelines that can be tested individually and later reused, replaced, or scaled for different professional environments.

The Streamlit interface presents the idea. The repository develops the underlying engineering system.

---

## Core Design Concept: The AI System as a Team

Kiron is designed as a team of specialized components rather than one general-purpose model responsible for every task.

A working role may be handled by deterministic Python, a small neural network, a retrieval model, a lightweight local language model, or a larger language model with tool-calling capabilities. The model size may range from below one billion parameters to a much larger hosted model. The choice depends on the responsibility assigned to that component.

The central design question is not which model is the most powerful. It is which component can perform a specific task reliably, clearly, and economically.

If deterministic Python can manage conversation state or route a request, a language model is not required.

If MiniLM can retrieve the relevant knowledge, a generative model does not need to search the full knowledge base.

If a 1.5B or 3B model can transform structured context into a clear answer, a 7B or larger model should not be used automatically.

Each team member is placed where its particular capability is useful.

Python currently manages deterministic responsibilities such as:

- conversation state
- entry and menu rules
- domain routing
- task validation
- file boundaries
- protected-file rules
- preparation of retrieved context

MiniLM performs semantic retrieval.

Qwen2.5-1.5B, served through `llama-server`, transforms selected knowledge into conversational responses.

The PydanticAI agent prototype uses Gemini 2.5 Flash for tasks that require reliable tool selection and file actions. The same role could later be assigned to an adequate local model, depending on available hardware and the required level of tool-use reliability.

This separation matters more when a system grows. In a small demonstration, the cost difference between a 3B and 7B model may seem insignificant. At thousands of requests, model size affects latency, memory use, infrastructure requirements, and operating cost.

Kiron therefore develops reusable pipelines in which models and software components can be replaced independently.

A stronger model may be introduced when a task requires greater language understanding. A smaller model may be used when the input has already been carefully retrieved and structured.

The objective is not to minimize model size at any cost. The objective is to assign every responsibility to the smallest adequate component without reducing reliability.

This turns the prototype into a test environment for a larger engineering question:

> How should an AI system divide work among software, retrieval models, and language models so that the complete system remains understandable, replaceable, and economically scalable?

The current repository already reflects this separation through independent routing, retrieval, local inference, file-operation, and testing components.

---

## Retrieval and Knowledge Architecture

Kiron does not treat retrieval-augmented generation as one fixed pipeline.

Different language models need different forms of context. A larger model may work well with broad, fragmented, and multi-layered material. A smaller model performs better when the retrieved knowledge has already been organized, reduced, and shaped for a specific response.

Kiron therefore experiments with multiple retrieval strategies around the same principle:

> Retrieval and knowledge preparation should be designed for the model that will use the result.

### Pipeline A: Semantic Retrieval for Larger Models

When the response requires nuance, interpretation, or connections across several parts of a knowledge base, Kiron can use a broader semantic-retrieval pipeline.

```text
User question
      ↓
MiniLM semantic search
      ↓
Relevant chunks from different documents or topics
      ↓
Larger language model
      ↓
Integrated conversational answer
````

In this design, the source documents can be relatively large and less rigidly structured.

MiniLM retrieves semantically related passages, even when they come from different sections of the knowledge base.

The selected material may be fragmented, overlapping, or drawn from several layers of one topic. A sufficiently capable language model can compare those fragments, recognize relationships between them, and produce an answer that preserves subtle distinctions.

This pipeline is useful when the task requires:

* nuanced interpretation
* synthesis across multiple topics
* preservation of narrative meaning
* comparison of partially related evidence
* richer and less predictable responses

The language model performs a substantial part of the final reasoning and composition. For that reason, this design may require a larger or more capable model.

### Pipeline B: Structured Retrieval for Smaller Models

When the priority is speed, accuracy, low hardware requirements, and predictable cost, Kiron uses a more structured knowledge pipeline.

```text
User question
      ↓
MiniLM identifies the relevant topic
      ↓
Python selects predefined sections
      ↓
Compact, structured context
      ↓
Lightweight language model
      ↓
Concise conversational answer
```

In this design, each topic document is prepared in several complementary forms, for example:

* summary
* key facts
* narrative
* detailed description
* keywords or retrieval tags
* related topics

These sections describe the same subject in different ways and at different levels of detail.

MiniLM does not need to understand the document structure as a human would. Its task is to identify the most relevant topic through semantic similarity and retrieval tags.

Python then uses the topic structure as a roadmap and returns the appropriate section or combination of sections.

For example, the same topic file can support different response needs:

* a short factual answer may use the summary and key facts
* a more human explanation may use the narrative section
* a technical answer may use the detailed description
* a retrieval step may rely mainly on tags and alternative topic titles

By the time the context reaches the language model, much of the selection and organization has already been completed.

The model does not need to search, reconstruct the topic, or infer the intended response format from a large body of text. It mainly transforms a clean knowledge package into natural language.

This allows Kiron to use a smaller, faster, and cheaper model without losing clarity or reliability.

### One Knowledge Base, Multiple Response Paths

An important part of this design is that the same Markdown knowledge file can support more than one pipeline.

The file is not only a storage document. Its internal structure becomes part of the software architecture.

A larger model may receive several semantically retrieved passages from different sections.

A smaller model may receive one carefully selected topic section prepared by Python.

The response path can therefore change according to:

* required depth
* acceptable latency
* available hardware
* expected request volume
* required level of nuance
* cost constraints
* privacy and deployment conditions

This makes the knowledge layer reusable rather than tied to one model or one retrieval method.

### Retrieval and Generation as Separate Responsibilities

Kiron separates three responsibilities that are often combined inside one general-purpose model:

1. Finding the relevant domain or topic
2. Preparing the appropriate knowledge context
3. Generating the final conversational response

MiniLM is responsible for semantic matching.

Python is responsible for deterministic topic selection, context assembly, and response routing.

The language model is responsible for expressing the supplied knowledge in a suitable conversational form.

This separation improves:

* traceability
* testability
* model replaceability
* cost control
* response consistency
* debugging clarity

When an answer is weak, the developer can inspect whether the problem came from retrieval, document structure, context assembly, or language generation.

The entire pipeline does not have to be treated as one opaque model behavior.

### RAG as a Prototype for Agent Memory

The same architecture can also support agent memory.

Instead of placing all user history or domain knowledge into one growing prompt, memory can be organized into structured topic documents and retrieved according to the current conversational need.

Different kinds of memory can use different strategies:

* factual memory can be returned directly
* narrative memory can be synthesized by a stronger model
* stable profile information can be selected deterministically
* broad historical context can be retrieved semantically
* short-term conversation state can remain in Python

The RAG experiments in Kiron are therefore not only about document question answering.

They are also prototypes for designing modular, inspectable, and scalable memory systems for future AI workspaces.

---

## Development Memory and Testing Architecture

Kiron is still an experimental prototype.

Its architecture is developed through small implementations, comparisons between alternative pipelines, debugging, and repeated testing.

For that reason, documentation and testing are not treated as final-stage maintenance tasks. They are part of the development infrastructure.

### Documentation as Engineering Memory

The project keeps two forms of engineering memory inside its documentation area:

* `.folder/debugging/` records important bugs, error traces, causes, fixes, and practical lessons from troubleshooting.
* `.folder/development/` records milestones, experiments, architectural decisions, pipeline changes, and testing progress.

This separation is useful because debugging memory and development history serve different purposes.

The debugging records help prevent the same technical problems from being investigated repeatedly.

The development records preserve how the architecture evolved, why particular decisions were made, and what was already tested before moving to the next stage.

Together, these folders allow later development to continue from documented evidence rather than from memory alone.

### Pytest as More Than Code Verification

Pytest protects existing software behavior while new components are added or replaced.

Its first responsibility is conventional software testing:

* verify functions and handlers
* protect deterministic behavior
* detect regressions
* isolate external dependencies with mocks
* confirm that refactoring has not broken existing contracts

However, in Kiron, testing also supports architectural development.

Conversation systems, retrieval pipelines, and local AI workflows contain many connected stages. A failure in the final answer may originate from routing, state management, retrieval, context preparation, model integration, or interface behavior.

By testing these responsibilities separately, the system becomes easier to understand and improve.

A test can reveal not only broken code, but also an unclear responsibility or an unnecessary dependency between components.

In this sense, pytest acts as an architectural inspection tool.

---

## Layered Testing Strategy

Kiron follows a staged testing structure, beginning with the most deterministic parts of the system.

### 1. Unit Tests

Unit tests verify small Python responsibilities independently.

Current examples include:

* entry rules
* identity recognition
* menu handling
* work-mode transitions
* task validation
* domain handlers
* helper functions
* orchestration between mocked components

These tests run quickly and do not require a language model or inference server.

### 2. Conversation Tests

Conversation tests verify complete paths through the deterministic conversation engine.

```text
Entry
  ↓
Menu
  ↓
Selected mode
  ↓
Handler
  ↓
State transition
```

These tests help confirm that the conversation behaves as a coherent system rather than as a collection of isolated functions.

They can also expose structural problems such as:

* ambiguous routing
* repeated responsibilities
* hidden state dependencies
* unreachable paths
* tightly coupled handlers

### 3. Retrieval Tests

Retrieval tests verify semantic search independently from language generation.

A small controlled knowledge base can be used to test:

* document parsing
* topic selection
* similarity ranking
* retrieval thresholds
* expected chunks
* fallback behavior

Separating retrieval from generation makes it possible to determine whether a poor answer begins with incorrect knowledge selection or with the language model.

### 4. Integration Tests

Integration tests verify communication between real system components.

Examples include:

* retriever to context builder
* context builder to answer generator
* application to `llama-server`
* local model endpoint availability
* model response handling

These tests require the relevant local services and models to be running.

### 5. End-to-End Tests

End-to-end tests validate the complete workflow from the user's perspective.

```text
Streamlit interface
        ↓
Conversation router
        ↓
Domain handler
        ↓
Retriever
        ↓
Context preparation
        ↓
Local language model
        ↓
Displayed response
```

These tests confirm that individually correct components still work together as one application.

---

## Testing the Pipeline Design

Because Kiron is built from replaceable components, tests also define the contracts between them.

For example, a retriever should return data in a form that the context builder understands.

The context builder should prepare input that the answer generator can use.

The answer generator should return a response that the interface can display.

When those contracts are explicit and tested, one component can be replaced without redesigning the entire system.

A different embedding model can replace MiniLM.

A different local model can replace Qwen.

A different interface can replace Streamlit.

The surrounding tests help verify that the replacement still satisfies the same role.

This is essential for a prototype whose purpose is to experiment with alternative models, workflows, and deployment conditions.

---

## Current Testing Direction

The current testing work begins with deterministic Python behavior and expands gradually toward the complete local AI pipeline.

Fast development tests exclude components that require a running local model:

```bash
python -m pytest -m "not integration"
```

Local AI integration tests require `llama-server` and an available GGUF model:

```bash
python -m pytest -m integration
```

The complete test suite can be run with:

```bash
python -m pytest tests
```

The objective is not to maximize the number of tests.

The objective is to create enough evidence that each component performs its assigned role and that the complete architecture remains stable while it evolves.

---

## A Reusable Experimental Foundation

Together, documentation and testing turn Kiron from a temporary demonstration into a reusable experimental foundation.

Documentation preserves what has been learned.

Tests preserve what has been made reliable.

This allows the prototype to continue changing without losing its development history or silently breaking earlier capabilities.

As Kiron expands, the repository can therefore support two parallel goals:

* experimenting with new AI architectures
* maintaining a stable collection of verified pipelines that can later be adapted, reused, or scaled

That combination is central to the purpose of the project.

```
```
