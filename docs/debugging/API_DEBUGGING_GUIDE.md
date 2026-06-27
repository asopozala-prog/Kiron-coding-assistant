# API Debugging Guide: Google Gemini & Pydantic AI

A practical guide for troubleshooting common API issues when building agents with Pydantic AI and Google Gemini.

---

## Problem 1: "API key not valid" Error on Cloud Deployment

### Symptoms
```
Error: status_code: 400, model_name: gemini-2.5-flash
message: 'API key not valid. Please pass a valid API key.'
status: 'INVALID_ARGUMENT'
```

App works **locally** but fails on **Streamlit Cloud** (or other cloud platform).

### Root Causes

#### 1. Secret Not Loaded (Most Common)
The API key secret isn't being read by the app.

**Check:**
- Go to Streamlit Cloud Settings → Secrets
- Verify the secret exists
- Verify the format is correct (TOML)

**Fix:**
```toml
GEMINI_API_KEY = "your_actual_key_here"
```

**Important:** Include the quotes around the key value.

---

#### 2. Outdated SDK/Library Version
Older versions of `google-generativeai` or `pydantic-ai` don't recognize new API key formats.

**Symptoms:**
- Key works locally but not on cloud
- Key format changed (old: `AIza...`, new: `AQ...`)
- Library validation fails before sending request

**Fix:**
```bash
pip install --upgrade google-generativeai pydantic-ai
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update to latest API libraries"
git push origin main
```

Then redeploy on cloud.

---

#### 3. API Key Expired or Revoked
The key is valid but no longer active.

**Check:**
- Go to https://aistudio.google.com/app/apikey
- Verify the key still exists
- Check if it's been disabled

**Fix:**
- Generate a new API key
- Update the secret on cloud platform
- Test locally first with new key

---

#### 4. API Key Has No Quota
The key exists but has exhausted its rate limit or quota.

**Check:**
- Go to Google Cloud Console
- Check API quotas and usage
- Look for rate limit errors (429 status code)

**Fix:**
- Wait for quota to reset (usually hourly/daily)
- Upgrade to paid tier if needed
- Use a different API key

---

### Debugging Checklist

**Step 1: Test Locally**
```bash
streamlit run app.py
```
- If it works locally, the key is valid
- If it fails locally, the key is invalid or expired

**Step 2: Verify Secret Format**
On cloud platform, check Secrets section:
```toml
GEMINI_API_KEY = "your_key_here"
```
- Must be TOML format
- Must have quotes around value
- No extra spaces

**Step 3: Check Library Versions**
```bash
pip list | grep -E "google-generativeai|pydantic-ai"
```
- Update if versions are old (>6 months)

**Step 4: Verify API Key Validity**
```bash
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('GEMINI_API_KEY')
print(f'Key loaded: {key[:10]}...' if key else 'Key not found')
"
```

**Step 5: Check Cloud Logs**
- Streamlit Cloud: Settings → look for logs/debug info
- Other platforms: Check deployment logs for error details

---

## Problem 2: "Event loop is closed" Error

### Symptoms
```
Error: Event loop is closed
```

Happens when running async code in Streamlit.

### Root Cause
Streamlit and `asyncio.run()` conflict. Each call to `asyncio.run()` closes the event loop, but Streamlit tries to reuse it.

### Fix

**Instead of:**
```python
result = asyncio.run(agent.run(user_input, message_history=history))
```

**Use:**
```python
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

result = loop.run_until_complete(
    agent.run(user_input, message_history=history)
)
```

This creates a new event loop if needed instead of closing the old one.

---

## Problem 3: 503 Service Unavailable / 429 Rate Limited

### Symptoms
```
Error: 503 UNAVAILABLE
Error: 429 RESOURCE_EXHAUSTED
```

API is temporarily overloaded or you've hit rate limits.

### Root Causes
- **503:** Google's API servers are busy (temporary)
- **429:** You've exceeded rate limits (quota exhausted)

### Check Current Limits
Go to https://aistudio.google.com/app/apikey and check:
- Requests per minute (RPM)
- Tokens per minute (TPM)
- Current usage

### Fix

**For 503 (Temporary):**
- Wait a few minutes and retry
- Implement exponential backoff in your code

**For 429 (Rate Limited):**
- Reduce request frequency
- Upgrade to paid tier
- Use a different API key
- Implement request queuing

**Example: Retry with Backoff**
```python
import time

def call_agent_with_retry(agent, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = asyncio.run(agent.run(prompt))
            return result
        except Exception as e:
            if "429" in str(e) or "503" in str(e):
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

---

## Problem 4: "Module not found" or Import Errors

### Symptoms
```
ModuleNotFoundError: No module named 'pydantic_ai'
ImportError: cannot import name 'GoogleProvider'
```

### Root Causes
- Library not installed
- Wrong import path
- Version mismatch

### Fix

**Reinstall dependencies:**
```bash
pip install pydantic-ai google-generativeai
```

**Verify imports:**
```python
# Correct imports
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.toolsets import FunctionToolset
from pydantic_ai.tools import RunContext
```

**Update requirements.txt:**
```bash
pip freeze > requirements.txt
```

---

## Problem 5: File Not Found on Cloud Deployment

### Symptoms
```
FileNotFoundError: No such file or directory: 'legal_files/alex_in_office.png'
```

App works locally but fails on cloud because files aren't in the repo.

### Root Cause
Files are in `.gitignore` and don't get deployed to cloud.

### Fix

**Option 1: Add files to repo**
```bash
git add legal_files/
git commit -m "Add files for cloud deployment"
git push origin main
```

**Option 2: Use external URLs**
```python
# Instead of local path
st.image("legal_files/alex_in_office.png")

# Use GitHub raw URL
st.image("https://raw.githubusercontent.com/username/repo/main/legal_files/alex_in_office.png")
```

**Option 3: Create files dynamically**
```python
import os
from pathlib import Path

# Create folder if it doesn't exist
Path("legal_files/work_files").mkdir(parents=True, exist_ok=True)

# Create sample files on first run
if not Path("legal_files/work_files/sample.txt").exists():
    Path("legal_files/work_files/sample.txt").write_text("Sample content")
```

---

## Problem 6: Secret Not Being Read

### Symptoms
- `os.getenv('GEMINI_API_KEY')` returns `None`
- App fails with "API key not valid"
- Works locally but not on cloud

### Root Cause
Secret not saved or not in correct format.

### Fix

**Streamlit Cloud:**
1. Go to Settings → Secrets
2. Clear the text box completely
3. Add fresh:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```
4. Click Save
5. Wait 1-2 minutes for redeploy

**Verify secret is loaded:**
```python
import os
print(f"API Key: {os.getenv('GEMINI_API_KEY')}")
```

If it prints `None`, the secret isn't loaded.

---

## Best Practices to Avoid Issues

### 1. Test Locally First
Always test with `streamlit run app.py` before deploying to cloud.

### 2. Keep Dependencies Updated
```bash
pip install --upgrade google-generativeai pydantic-ai streamlit
pip freeze > requirements.txt
```

### 3. Use Environment Variables Correctly
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env locally
api_key = os.getenv("GEMINI_API_KEY")
```

### 4. Implement Error Handling
```python
try:
    result = await agent.run(user_input, message_history=history)
except Exception as e:
    st.error(f"Error: {str(e)}")
    print(f"Full error: {e}")  # Log for debugging
```

### 5. Use Different Keys for Different Environments
- **Local:** Use `.env` file with one key
- **Cloud:** Use platform secrets with different key
- Easier to debug and revoke if needed

### 6. Monitor API Usage
- Check quotas regularly
- Set up alerts for rate limits
- Plan for scaling if needed

---

## Debugging Workflow

When you encounter an API error:

1. **Read the error message carefully**
   - Status code (400, 429, 503)
   - Error reason (INVALID_ARGUMENT, RESOURCE_EXHAUSTED)

2. **Test locally**
   - Does it work with `streamlit run app.py`?
   - If yes, it's a cloud configuration issue
   - If no, it's a code or key issue

3. **Check the obvious**
   - Is the API key valid?
   - Is the secret saved on cloud?
   - Are libraries up to date?

4. **Check logs**
   - Cloud platform logs
   - Terminal output
   - Add debug print statements

5. **Try the fixes in order**
   - Update libraries
   - Regenerate API key
   - Check secret format
   - Restart/redeploy

6. **Document what worked**
   - Keep notes for next time
   - Update this guide if you find new issues

---

## Quick Reference

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| 400 API key not valid | Invalid/expired key or outdated library | Update libraries, regenerate key |
| 429 Rate limited | Quota exhausted | Wait, upgrade tier, or use new key |
| 503 Service unavailable | API overloaded | Retry with backoff |
| Event loop is closed | asyncio conflict in Streamlit | Use `get_event_loop()` instead of `asyncio.run()` |
| FileNotFoundError | Files not in cloud repo | Add to repo or use external URLs |
| ModuleNotFoundError | Library not installed | `pip install` and update requirements.txt |
| Secret returns None | Secret not saved on cloud | Check Secrets section, verify TOML format |

---

## Resources

- **Google Gemini API:** https://aistudio.google.com/app/apikey
- **Pydantic AI Docs:** https://ai.pydantic.dev/
- **Streamlit Secrets:** https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
- **Google Cloud Console:** https://console.cloud.google.com/

---

## Notes for Future Projects

When starting a new project with Pydantic AI + Gemini:

1. **Set up `.env` immediately**
   ```
   GEMINI_API_KEY=your_key_here
   ```

2. **Add to `.gitignore`**
   ```
   .env
   __pycache__/
   .venv/
   ```

3. **Create `requirements.txt` early**
   ```bash
   pip freeze > requirements.txt
   ```

4. **Test locally before cloud**
   - Verify agent works
   - Verify file operations work
   - Verify UI works

5. **Deploy to cloud**
   - Push to GitHub
   - Add secret on cloud platform
   - Verify it works

6. **Monitor and maintain**
   - Check API usage regularly
   - Update libraries monthly
   - Keep API key secure

---

**Last Updated:** June 25, 2026  
**Project:** Kiron Coding Assistant  
**Author:** Mei (THRIVE Portfolio Project)
