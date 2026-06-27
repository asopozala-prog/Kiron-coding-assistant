# Debugging Records (Issues 4–8)

This document is a detailed record of the major debugging issues encountered while building and deploying the Kiron Coding Assistant project.

Scope: **(4) Pydantic AI framework/tooling**, **(5) Streamlit UI**, **(6) File system & ambiguity**, **(7) Git/GitHub**, **(8) Streamlit Community Cloud deployment**.

---

## 4) Pydantic AI framework/tooling issues

### 4.1 Wrong import paths (Toolset / capabilities)
**Symptom**
- Import errors such as:
  - `ImportError: cannot import name 'FunctionToolset' from pydantic_ai.capabilities`

**Likely root cause**
- The installed version of Pydantic AI exposes `FunctionToolset` under a different module path than examples found online.

**Fix applied**
- Switch to the correct import for the installed version:
  - `from pydantic_ai.toolsets import FunctionToolset`

**Verification**
- Running the file no longer fails at import time.

---

### 4.2 Toolset constructor mismatch
**Symptom**
- Type errors like:
  - `TypeError: Toolset.__init__() missing 1 required positional argument: 'toolset'`

**Likely root cause**
- Using a `Toolset` class/constructor pattern that does not match the installed library version.

**Fix applied**
- Reverted to a working pattern using `FunctionToolset()` and `add_function(...)`.

**Verification**
- Agent starts successfully and tools are registered.

---

### 4.3 Skills capability signature mismatch (`ctx` parameter)
**Symptom**
- Error such as:
  - `TypeError: Skills.get_instructions() missing 1 required positional argument: 'ctx'`

**Likely root cause**
- Capability method signature in local code didn’t match what Pydantic AI expects for that version.

**Fix applied**
- Updated method signature to accept:
  - `def get_instructions(self, ctx: RunContext[Any]) -> str:`

**Verification**
- App/agent no longer crashes when capability instructions are evaluated.

---

## 5) Streamlit UI debugging issues

### 5.1 Indentation errors in `app.py`
**Symptom**
- Streamlit fails immediately with:
  - `IndentationError: expected an indented block after 'if' statement`

**Likely root cause**
- The chat input handling block (commonly `if user_input:`) was partially edited and left with an empty `if` body or misaligned indentation.

**Fix applied**
- Restore a complete, properly indented block under `if user_input:` including:
  - appending messages
  - displaying the user message
  - calling the agent
  - storing result + history

**Verification**
- Streamlit runs and chat input works.

---

### 5.2 Async runtime: “Event loop is closed”
**Symptom**
- During chat requests:
  - `Error: Event loop is closed`

**Likely root cause**
- `asyncio.run(...)` is unsafe in Streamlit reruns.
- Streamlit triggers reruns; `asyncio.run()` creates and then closes an event loop each time.

**Fix applied**
- Replace `asyncio.run(agent.run(...))` with a safer loop approach:
  - `loop = asyncio.get_event_loop()`
  - create a new loop if missing
  - `loop.run_until_complete(agent.run(...))`

**Verification**
- Multiple chat turns work without crashing.

---

### 5.3 Streamlit image sizing / parameter errors
**Symptoms**
- `StreamlitInvalidWidthError: Invalid width value: None`
- Deprecation warnings related to image width handling.

**Likely root cause**
- Passing `width=None` or using deprecated parameters.

**Fix applied**
- Use a consistent pattern in the codebase:
  - `st.image(..., width="stretch")`

**Verification**
- Pages render without image-related runtime errors.

---

## 6) File system + filename ambiguity issues

### 6.1 Agent asks for exact filenames despite alias map
**Symptom**
- User says: “read messy case data” / “fill case file template”
- Model asks clarifying questions like: “What is the file name/path?”

**Root cause**
- Prompt instructions alone are not sufficient; the model may choose to ask before calling tools.

**Fix applied (code-level reliability)**
- Move ambiguity handling into the tool layer:
  - Maintain an alias map (`FILE_ALIASES`)
  - Add fuzzy matching (`find_best_match`) inside the tools
  - Resolve user phrases to real filenames automatically

**Verification**
- The agent can read and update files when given vague file references.

---

### 6.2 File exists but tool cannot find it
**Symptom**
- Errors like:
  - `Error: [Errno 2] No such file or directory: 'messy_case_data.txt'`
- Even though `ls legal_files/work_files/` shows the file exists.

**Root cause**
- Tool was reading from the **current working directory** instead of `WORK_DIR`.

**Fix applied**
- Enforce a safe path builder:
  - `_safe_path(filename)` resolves to `(WORK_DIR / filename)`
  - Security check ensures path stays inside `WORK_DIR`
- Update `read_file`, `write_file`, `delete_file` to use `_safe_path`.

**Verification**
- Running `ls -la legal_files/work_files/` matches what the agent can read/write.

---

### 6.3 Protect core files from deletion + friendly fallback
**Goal**
- Allow deleting demo-generated files (e.g., `test.txt`).
- Prevent deleting core baseline/demo files.

**Protected files**
- `alex.md`
- `case_file_template.txt`
- `messy_case_data.txt`
- `sample_contract.md`

**Fix applied**
- In `delete_file(...)` check `actual_filename` against a protected set.
- If protected, return a friendly message (instead of deleting):
  - “Hey Alex, this file is your working base‼️ 🦕 If you really want to delete it, please contact our programmer.”

**Verification**
- Attempting to delete a protected file returns the message and the file remains.

---

## 7) Git / GitHub debugging issues

### 7.1 Push failed (HTTP 400 / RPC failed)
**Symptom**
- `error: RPC failed; HTTP 400`
- `fatal: the remote end hung up unexpectedly`

**Likely root cause**
- Large binary assets (initially PNG images) increased push payload.

**Fix applied**
- Reduce asset size by switching to JPG where appropriate.
- Control what gets committed (avoid caches / large artifacts).

**Verification**
- `git push origin main` succeeds.

---

### 7.2 Push rejected: non-fast-forward
**Symptom**
- `! [rejected] main -> main (fetch first)`
- `Updates were rejected because the remote contains work that you do not have locally.`

**Root cause**
- Remote branch changed (e.g., edits from a different machine session or a merge).

**Fix options**
- Preferred: integrate changes via `git pull origin main` then push.
- If you intentionally want local state to override remote: `git push --force`.

**Verification**
- `git status` shows branch is up to date and pushes succeed.

---

### 7.3 Command entry mistake (two commands on one line)
**Symptom**
- e.g., `git push origin mainecho ...`
- Error: `fatal: invalid refspec 'kiron_router/'` or “refspec does not match any”

**Root cause**
- Terminal interpreted combined text as a single git command.

**Fix applied**
- Run one command per line; wait for completion before entering next.

---

## 8) Streamlit Community Cloud deployment debugging

### 8.1 Wrong main file path
**Symptom**
- Deployment form shows `streamlit_app.py` with red warning: “This file does not exist.”

**Fix applied**
- Set **Main file path** to `app.py`.

---

### 8.2 Missing/invalid API key on Streamlit Cloud

#### 8.2.1 API key not set
**Symptom**
- Redacted Pydantic AI user error at startup.
- Trace indicates missing `GEMINI_API_KEY`.

**Fix applied**
- Add Streamlit Cloud Secrets using TOML:

```toml
GEMINI_API_KEY = "<your key>"
```

---

#### 8.2.2 API key “not valid” (400)
**Symptom**
- Gemini returns:
  - `API key not valid. Please pass a valid API key.`

**Likely root causes**
- Key pasted incorrectly into Secrets.
- Key expired/revoked.
- SDK/library mismatch with newer key formats.

**Fix applied**
- Confirm local app works with `.env` key.
- Generate a new key for cloud.
- Update dependencies and push updated `requirements.txt`.

---

### 8.3 Missing images/files on cloud
**Symptom**
- `MediaFileStorageError: Error opening 'legal_files/...'

**Root cause**
- Required assets weren’t committed to GitHub (or were ignored).

**Fix applied**
- Commit required assets into `legal_files/`.

---

### 8.4 Case-sensitivity bug (macOS vs Linux)
**Symptom**
- Works locally (macOS), fails on Streamlit Cloud (Linux):
  - `Error opening 'legal_files/Alex_Cafe.png'`

**Root cause**
- macOS commonly uses a case-insensitive filesystem.
- Linux is case-sensitive.

**Fix applied**
- Standardize filenames to lowercase (e.g., `alex_cafe.jpg`).
- Update `app.py` to reference the exact committed filename.

**Verification**
- Deployed page renders successfully.

---

## Recommended “Next Time” Checklist

When something breaks:

1. **Confirm environment**
   - `which python`
   - `python -m pip freeze | head`

2. **Confirm local run**
   - `python -m streamlit run app.py`

3. **Confirm deployment parity**
   - `requirements.txt` updated
   - assets committed (images + markdown)

4. **Cloud-specific checks**
   - Secrets in TOML
   - case-sensitive filenames

---

**Last updated:** 2026-06-27
