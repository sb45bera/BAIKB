# BAIKB Universal Answer Engine update

This update changes the website chat and `/v1/ask` to use a shared retrieval-and-answer pipeline.

## Files in this update

Copy these files into the existing project, preserving the folder structure:

- `app/answer_engine.py` — new universal answer pipeline.
- `app/config.py` — adds optional `BAIKB_OPENAI_API_KEY` and `BAIKB_OPENAI_MODEL` settings.
- `app/knowledge.py` — improves Hindi/Bengali tokenization and rejects weak keyword matches.
- `app/main.py` — routes website chat and `/v1/ask` through the shared answer engine; version becomes 0.4.0.
- `static/chat.js` — displays source links returned by the API.
- `tests/test_answer_engine.py` — regression tests.

Do not replace `data/`, `admin_data/`, `.env`, `.venv/`, `static/chat.html`, `static/chat.css`, or the existing ingestion modules.

## Enable concise AI synthesis (recommended)

The answer engine can use the OpenAI Responses API to synthesize a direct answer from retrieved evidence. This is optional. Without a provider API key, it uses a conservative extractive fallback and cannot paraphrase or reason over multiple records as effectively.

In the same PowerShell window used to start the server, set:

```powershell
$env:BAIKB_OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
$env:BAIKB_OPENAI_MODEL="gpt-4o-mini"
```

Keep the key private. Do not paste it into chat, commit it to GitHub, or put it in frontend JavaScript. Provider API usage may incur separate charges.

If you do not have an API key, skip these commands. The application will still run in extractive mode.

## Install and run

```powershell
cd C:\Users\Admin\Desktop\BHARAT_AI_KNOWLEDGE_BASE
.\.venv\Scripts\Activate.ps1
python -m compileall -q app
python -m unittest discover -s tests -v
python -m uvicorn app.main:app --reload
```

If you set the API key, do so before starting Uvicorn. Restart the server after changing it.

## Current limitations

- Live fallback still uses the project's existing Wikimedia retrieval adapter; this update does not claim a 500+ operational source registry.
- Local JSON records remain the primary knowledge source. Retrieved live candidates retain their source metadata and `needs_review` status.
- A provider API key is needed for the best concise, evidence-grounded synthesis. Without one, the fallback returns a short excerpt and may not be able to answer questions requiring reasoning across multiple records.
- Network access to Wikimedia and the configured answer provider must be available on the machine running BAIKB.
