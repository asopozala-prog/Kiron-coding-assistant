# Reasoning Effort Postmortem (Exercise → App Integration)

## Summary
We implemented a **ReasoningEffort** capability (Exercise 5) that adjusts model “effort” (low / medium / high) based on prompt heuristics, and passes this into `ModelSettings`. It worked well as a standalone exercise, but became confusing and potentially fragile when integrated into the Streamlit demo app and deployed workflow.

This document explains:
- **how the issue happened**
- **how we handled it**
- **what we learned**
- **when ReasoningEffort is actually meaningful in real user deployments**

---

## What we built (Exercise 5)

In the exercise version, ReasoningEffort:
- inspects the user prompt (length + keywords)
- selects an effort level
- prints it for visibility
- returns model settings

Typical logic:
- short prompts / “quick”, “list” → low
- “explain”, “debug”, “why/how” → high
- otherwise → medium

---

## What went wrong (when integrated into the Streamlit app)

### Observed symptoms
- The terminal repeatedly printed lines like:
  - `[Reasoning effort: medium]`
  - `[Reasoning effort: low]`
- It looked like the agent was “stuck” or “looping forever”, even when it was still responding.

### Why it happened
This was not a single bug; it was an **interaction between a teaching feature and a UI runtime**:

1) **Streamlit reruns the script frequently**
- In Streamlit, many interactions trigger a rerun of the script.
- This changes the “once per request” mental model common in CLI scripts.

2) **Model settings may be evaluated multiple times per user action**
Depending on the agent/model/provider version, `get_model_settings()` can be called:
- more than once per `agent.run()`
- across multiple internal steps (tool planning + tool execution + follow-up)
- on retries/fallback paths

So a simple debug print becomes **log spam**, which can look like a hang.

3) **`ModelSettings(thinking=effort)` is version/provider fragile**
Different versions/providers expect different shapes for advanced settings.
We observed that a more structured pattern is often required (e.g. `thinking={"effort": effort}`), and mismatches can cause inconsistent behavior across environments.

---

## How we handled it

### Decision
We prioritized a stable, presentation-ready demo over optional complexity.

### Fix
- We **removed or disabled ReasoningEffort** in the unified `agent.py` used by the Streamlit app (or removed the noisy `print()` calls).
- We kept `exercise5.py` as the learning artifact proving we implemented the concept.

This reduced fragility and made the demo more predictable.

---

## What we learned

1) **Teaching code ≠ production code**
Exercises are optimized for learning (visibility, simple loops), not for UI reruns and deployment.

2) **UI runtimes change the execution model**
Streamlit’s rerun behavior can cause functions to execute more often than expected.

3) **Provider/version compatibility matters**
Advanced model settings are not uniformly supported across versions/providers.

4) **Every added feature increases surface area**
Even “cool” features can:
- complicate the system
- reduce predictability
- introduce new failure modes

A good agent demo is often stronger when it is simpler.

---

## When ReasoningEffort is truly meaningful (real deployments)

ReasoningEffort is worth keeping when it solves a real operational constraint.

### 1) Cost control
If usage is high and the API is paid, effort-routing can reduce costs by using lower effort for simple tasks.

### 2) Latency control
For interactive apps:
- low effort for simple tasks (fast response)
- high effort for complex tasks (slower but better)

### 3) Reliability on high-stakes analysis
When mistakes are expensive (compliance, legal risk triage), you may want:
- higher effort for complex reasoning tasks

### 4) Multi-model routing (often more practical than “effort”)
A very practical form of “reasoning effort” is:
- simple tasks → smaller/cheaper/faster model
- complex tasks → stronger model

This is more widely supported than “thinking effort” flags.

---

## Conclusion
ReasoningEffort is a useful *learning* concept and can be valuable in production **when it clearly improves cost, latency, or reliability**.

For the Kiron demo, the project’s core value is:
- sandboxed local file tooling
- fuzzy filename resolution
- visible file manipulation in the UI

So we chose stability and clarity over keeping every exercise feature in the deployed app.

---

**Date:** 2026-06-27
