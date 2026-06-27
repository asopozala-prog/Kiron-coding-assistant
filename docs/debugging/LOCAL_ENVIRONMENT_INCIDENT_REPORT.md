# Incident Report: Local app stopped running (missing Streamlit / deps)

## Summary
After working on a separate TinyBERT experiment, the Kiron Streamlit app stopped running locally. The terminal reported missing commands/modules such as Streamlit, `dotenv`, and `pydantic_ai`.

## Symptoms
Observed errors included:

- `bash: streamlit: command not found`
- `No module named streamlit`
- `ModuleNotFoundError: No module named 'dotenv'`
- `ModuleNotFoundError: No module named 'pydantic_ai'`

## Impact
- `streamlit run app.py` could not start.
- The app crashed during import (`from agent import agent`) because dependencies were missing.

## Root cause
The app was executed in a **Python environment (virtual environment) that did not have the Kiron project dependencies installed**.

This likely happened because the TinyBERT work involved creating/activating a different or newly created virtual environment, so when returning to the Kiron repo the active environment was effectively empty (or not the same environment that previously had Streamlit + Pydantic AI installed).

## Why it was confusing
The shell prompt still displayed `(.venv)`, but that only indicates “a venv is active.” It does **not** guarantee:
- it is the correct venv for the Kiron repo, or
- it contains the required packages.

## Diagnosis
The errors were consistent with missing dependencies in the currently active environment:
- Missing `streamlit` executable → Streamlit not installed in that env
- Missing imports (`dotenv`, `pydantic_ai`) → project deps not installed in that env

## Resolution
Install missing packages into the active venv and then reinstall the repo’s dependencies:

```bash
python -m pip install streamlit
python -m pip install python-dotenv
python -m pip install -r requirements.txt
```

Then rerun:

```bash
python -m streamlit run app.py
```

## Verification
Confirmed the active environment contained required packages:

```bash
python -m pip freeze | grep -E "streamlit|pydantic-ai|python-dotenv"
```

Expected to see entries like:
- `streamlit==...`
- `python-dotenv==...`
- `pydantic-ai==...`

## Prevention (recommended workflow)

### 1) Confirm you are using the repo’s venv
```bash
which python
```
Expected path includes:
`Kiron-coding-assistant/.venv/bin/python`

### 2) Use separate venvs for separate projects
- Kiron project: `.venv`
- TinyBERT experiments: a different venv name (e.g., `.venv-bert`) in a different folder

### 3) Standard “return to project” routine
```bash
cd Kiron-coding-assistant
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

---

**Date logged:** 2026-06-27
