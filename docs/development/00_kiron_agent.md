# Kiron Project Development Log

## Project Overview

Kiron is a local-first AI assistant prototype built for a confidential legal-document workflow. The project was developed as part of the THRIVE optional portfolio work and evolved from a learning exercise into a realistic demonstration app for a legal assistant named Alex Hoffmann.

The final result is a Streamlit application backed by a unified Pydantic AI agent that can read, write, search, and delete files inside a protected local working folder. The project emphasizes privacy, sandboxed file access, and a practical UI for non-technical users.

---

## 1. Starting Point

The project began as a structured learning path from the Agentic AI Masterclass. The masterclass included six exercises that introduced the core building blocks of an AI coding assistant:

1. First LLM Call
2. Conversation State
3. Tool Calling
4. Execution Hooks
5. Reasoning Effort
6. Skills and Extensibility

At first, the goal was simply to complete the exercises and understand how to build an agent with Pydantic AI and an LLM provider.

---

## 2. Repository Setup and Initial Development

### Repository creation
A GitHub repository was created to store the solution and track progress.

### Local environment
The project was developed locally on macOS using:
- Python 3.12
- a virtual environment (`.venv`)
- VS Code
- Streamlit
- Pydantic AI
- Google Gemini API
- dotenv

### Early workflow
The first work focused on:
- setting up the environment
- getting the first model response
- adding conversation state
- introducing tools for file access

This was the foundation for the later unified agent.

---

## 3. Building the Six Exercises

### Exercise 1: First LLM Call
This exercise established the base agent connection.

What was learned:
- how to initialize a Google Gemini model through Pydantic AI
- how to send a simple prompt
- how to display a response in the terminal

### Exercise 2: Conversation State
Conversation history was added so the model could remember previous turns.

What was learned:
- `message_history`
- `result.all_messages()`
- multi-turn interaction

### Exercise 3: Tool Calling
File operations were introduced through tools.

What was learned:
- registering functions as tools
- exposing file operations to the agent
- allowing the model to decide when to use tools

### Exercise 4: Execution Hooks
A hook was added to log tool execution.

What was learned:
- observing tool calls before execution
- tracking arguments
- understanding the agent flow more clearly

### Exercise 5: Reasoning Effort
A reasoning-effort pattern was introduced to adjust effort based on prompt complexity.

What was learned:
- conditional model settings
- prompt heuristics
- how agent behavior can be tuned dynamically

### Exercise 6: Skills and Extensibility
Markdown-based skills were loaded from files.

What was learned:
- how to make the agent extensible
- how to load instructions from markdown documents
- how to add modular capabilities

---

## 4. From Exercises to a Unified Agent

After completing the exercises, the project evolved from separate learning files into one cohesive assistant.

### Unified `agent.py`
A single agent file was created to combine the ideas from all exercises.

This file became the core of the final app and included:
- Google Gemini model setup
- file tools
- skills loading
- execution logging
- reasoning-effort logic (in early versions)
- folder restrictions and safe path handling

### Why unify the exercises?
The exercises were useful for learning, but the final project needed one coherent system rather than six separate demos.

The unified agent made it possible to:
- keep the learning history
- support a realistic demo
- integrate with a Streamlit UI
- present the project as one usable assistant

---

## 5. Designing the Legal Assistant Story

The project shifted from a generic coding assistant into a specific workflow for a legal assistant named Alex Hoffmann.

### Why the change?
A legal assistant workflow made the project more realistic and suitable for a portfolio demo because:
- the documents are confidential
- local-only file processing makes sense
- the assistant’s purpose is easy to understand
- the demo can show visible file manipulation

### Story structure
The app tells a story about:
- Alex’s work pressure
- his repetitive document tasks
- the life he wants outside work
- how Kiron helps him recover time and focus

This narrative helped the app feel like a real product, not just a coding exercise.

---

## 6. Building the Streamlit UI

A Streamlit interface was built to make the agent easier to understand and demonstrate.

### UI pages
The final UI was organized into multiple pages:
- Meet Alex Hoffmann
- Why Alex Need Kiron
- How Kiron Was Built
- Alex work with Kiron

### Features of the UI
- sidebar navigation
- page-specific story content
- image-driven narrative sections
- a live file viewer for the working folder
- chat interface for interacting with Kiron

### The file viewer concept
A right-side panel showed Alex’s working folder so users could see file changes in real time.

This became one of the most important parts of the demo because it made the agent’s actions visible.

---

## 7. Working Folder and File Safety

The agent was restricted to a specific folder:

- `legal_files/work_files/`

### Why this mattered
This protected the project from accidental access to files outside the intended workspace.

### What the agent could do
Inside the working folder, Kiron could:
- read files
- write files
- search files
- delete demo files

### Protected files
Core files were protected so the agent could not delete the working base of the demo:
- `alex.md`
- `case_file_template.txt`
- `messy_case_data.txt`
- `sample_contract.md`

### Friendly fallback
If the user asked to delete a protected file, Kiron returned a friendly fallback message instead of deleting it.

---

## 8. Filename Ambiguity and Fuzzy Matching

One important usability issue was that the model asked for exact filenames too often.

### Problem
The user would say things like:
- “read the messy case data”
- “fill the case file template”

But the model would still ask for exact filenames.

### Fix
The solution was to handle ambiguity in code, not just in prompt text.

We added:
- alias mapping
- fuzzy filename matching
- automatic resolution inside the tool functions

### Result
Kiron could now infer file names from vague user language and work more naturally.

---

## 9. Reasoning Effort Lessons

Exercise 5 introduced reasoning-effort control, but it later became a useful lesson about keeping the final product simple.

### What happened
The reasoning-effort feature worked as a standalone exercise, but in the Streamlit app it created extra complexity, log spam, and confusion.

### What we learned
- teaching code is not always production code
- UI reruns can expose noisy behavior
- advanced settings can add fragility
- useful features should be kept only when they improve the final user experience

For the final demo, stability mattered more than keeping every experimental feature.

---

## 10. Debugging and Environment Issues

The project included a long debugging phase, especially around local setup, missing packages, and deployment.

### Local environment issue
After working on a separate TinyBERT experiment, the Kiron environment stopped running correctly because the active virtual environment did not contain all required dependencies.

### Typical errors
- `streamlit: command not found`
- `No module named dotenv`
- `No module named pydantic_ai`

### Fix
The solution was to reinstall dependencies into the correct virtual environment.

### Lesson
A project can appear “broken” simply because the wrong environment is active.

---

## 11. Streamlit Cloud Deployment

The app was deployed to Streamlit Community Cloud.

### Deployment issues handled
- missing API secret
- invalid API key
- image filename case-sensitivity problems
- missing assets in the repo

### Important deployment note
Streamlit Cloud runs on Linux, so filenames are case-sensitive.
This meant image names had to be consistent and lowercase in the code and repository.

### Cloud API key
The deployed app used a cloud Gemini API key for the demo.
For a real law-firm deployment, the system would ideally run on a local model instead.

---

## 12. Git and Repository Management

The project also involved a lot of repository hygiene work.

### Tasks completed
- committing code changes
- pushing to GitHub
- handling untracked files
- organizing documentation into a `docs/debugging/` folder
- updating `.gitignore`
- cleaning up image file naming and extensions

### Lessons learned
- keep repositories organized
- avoid committing temporary files and caches
- make sure assets needed for deployment are included
- keep local and cloud file paths in sync

---

## 13. Documentation Work

As the project matured, documentation became an important part of the deliverable.

### Documentation created
- API debugging guide
- local environment incident report
- reasoning effort postmortem
- development records for issues 4–8
- README rewrite

### Why this mattered
The documentation captures the learning process and helps future projects avoid the same issues.

---

## 14. Final Project Shape

The final project became a complete demonstration app with:
- a narrative about Alex’s work pressure
- a clear explanation of why local AI matters for sensitive data
- a Streamlit interface with multiple pages
- a live working folder viewer
- a unified agent that manipulates files safely
- a deployed cloud demo and a local runnable version

---

## 15. Key Takeaways

### Technical takeaways
- Build agents incrementally
- Keep tool logic robust and explicit
- Use safe path handling for file operations
- Expect Streamlit reruns when designing UI logic
- Match filenames exactly when deploying on Linux

### Product takeaways
- A good demo needs a clear story
- A local-first privacy argument is strong for sensitive-document workflows
- A simple, stable agent is better than an overly clever one
- Features should be kept only if they improve the user experience

### Personal takeaway
The project was not just about building an assistant. It was about learning how to turn a sequence of exercises into a coherent product that can be explained, demonstrated, and deployed.

---

## 16. Next Steps

Possible next improvements include:
- a real local LLM backend for a no-cloud deployment
- richer document analysis
- better template filling
- OCR or PDF support
- audit logs for all file operations
- more robust document organization workflows

---

## Final Note

Kiron is best understood as a portfolio prototype:
- built from a masterclass learning path
- shaped into a real use case
- refined through debugging and deployment work
- designed to show how a local AI assistant can support confidential document workflows

This project is now ready for presentation, walkthrough recording, and portfolio submission.
