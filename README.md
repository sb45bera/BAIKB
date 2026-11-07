# BHARAT AI KNOWLEDGE BASE (BAIKB)

A JSON-first, multilingual India knowledge service with a FastAPI backend and an ESP32 HTTP client example.

## What is included
- JSON knowledge files with English, Hindi and Bengali sample entries.
- FastAPI endpoints for health, categories, keyword search and record lookup.
- A simple multilingual keyword search (no external AI API required).
- A small ESP32 Arduino example that sends a question to the API and prints the answer.
- JSON Schema for validating knowledge records.
- Data provenance fields: source URL, verification date and status.

> This is a starter knowledge platform, not an exhaustive or officially certified database of India. The included facts are illustrative starter records. Verify changing facts and emergency contact information against official sources before deployment.

## Requirements
- Python 3.10+
- Windows, Linux or macOS
- ESP32 Arduino core (only if using the hardware example)

## Run on Windows PowerShell
```powershell
cd BHARAT_AI_KNOWLEDGE_BASE
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
If PowerShell blocks activation, use:
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health
- Categories: http://127.0.0.1:8000/v1/categories

## Search examples
```powershell
curl.exe "http://127.0.0.1:8000/v1/search?q=capital%20of%20India&lang=en"
curl.exe "http://127.0.0.1:8000/v1/search?q=भारत%20की%20राजधानी&lang=hi"
curl.exe "http://127.0.0.1:8000/v1/search?q=ভারতের%20রাজধানী&lang=bn"
```

## API
- `GET /health`
- `GET /v1/categories`
- `GET /v1/search?q=...&lang=en&category=geography&limit=5`
- `GET /v1/records/{record_id}?lang=hi`

Supported language codes in starter: `en`, `hi`, `bn`. Add more language translations in the JSON records as needed. If a translation is missing, the API falls back to English.

## Data structure
Every record has:
- `id`: stable unique identifier
- `category`: knowledge collection
- `type`: record type
- `names`: localized names
- `content`: localized answer/description
- `tags`: searchable localized terms
- `facts`: structured facts
- `sources`: references and verification metadata
- `status`: `draft`, `verified` or `needs_review`

Do not silently treat unsourced or outdated information as verified.

## Add knowledge
1. Edit a JSON file in `data/`.
2. Keep IDs unique across all files.
3. Add sources and `last_verified` date (`YYYY-MM-DD`).
4. Set `status` to `verified` only after checking a trustworthy source.
5. Restart the API (or add a reload mechanism before production).

## ESP32 setup
1. Upload `firmware/esp32_chatbot.ino` to the ESP32.
2. Set Wi-Fi name/password.
3. Set `API_BASE` to your computer's LAN IP, e.g. `http://192.168.1.10:8000`.
4. Ensure the ESP32 and computer are on the same Wi-Fi network.
5. For public deployment, use HTTPS and authentication. Do not expose an unauthenticated API to the public internet.

## Production roadmap
- Add API key authentication and rate limiting.
- Use HTTPS behind a reverse proxy.
- Add automated JSON validation and duplicate-ID checks.
- Add a scheduled source verification/update workflow.
- Add multilingual embeddings + Qdrant/FAISS for semantic search.
- Add an LLM adapter separately; the knowledge API should remain model-independent.
- For offline ESP32 use, export a small curated FAQ pack; the full database is too large for typical ESP32 flash/RAM.
