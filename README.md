# SmartDashboard

SmartDashboard combines website + social media scraping, automated LLM analysis, and a React/Next frontend for competitive intelligence.

---

## Project Overview

- Purpose: Collect market signals from public web pages and social channels, analyze them with LLMs, and surface actionable competitive intelligence in a dashboard.
- High-level flow:
  1. Scraper collects raw data (website + social media) and persists it.
  2. LLM notebook reads raw scrapes, runs analyses (competitor summary, our analysis, comparison), and saves results.
  3. Frontend reads saved outputs and live metrics to present dashboards and insight pages.

---

## Repository Layout (high level)

- `frontend/` — Next.js / React UI
- `scraper/` — scraping logic; primary working folder: `scraper/online/new/` (FastAPI + scraper code)
- `LLM/` — analysis notebook and helper scripts

---

## Frontend

Location: `frontend/`

Key files:
- `package.json` — dependencies and scripts
- `src/views/Dashboard.jsx` — main dashboard
- `src/views/CompetitorDetails.jsx` — charts and live intelligence
- `src/lib/api.js` — API client wrapper

Run (dev):

```bash
cd frontend
npm install
npm run dev
```

Notes:
- Supabase client is used in `CompetitorDetails.jsx`. Move publishable keys to env or secure store for production.
- Frontend uses `localStorage` keys `competitorWebsites` and `setupData` for demo/demo persistence.

---

## Scraper

Location: `scraper/online/new/`

Key files:
- `main.py` — orchestration for website + social scraping
- `api.py` — FastAPI wrapper exposing `/scrape` (uses `ScrapeRequest` model)
- `save_raw_scraper.py` — persists raw scrapes (check storage target)

Run API locally:

```bash
cd scraper/online/new
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

Endpoint:
- `POST /scrape` — body follows `ScrapeRequest` in `api.py` (url_or_name, is_our_site, max_pages, include_social, etc.)

Notes:
- CORS is configured in `api.py` to allow only whitelisted origins. Update `allowed_origins` to include your frontend domain(s).
- A bug where `all_data` could be uninitialized was fixed — `main.py` now safely initializes `all_data` prior to scraping.

---

## LLM / Analysis

Location: `LLM/`

Key files:
- `model.ipynb` — Jupyter notebook that:
  - Loads raw scrapes via `getDbdata.get_raw_scrapes()`
  - Splits records into `our_data` and `competitor_data`
  - Chunks data and sends it to the Groq LLM (`groq` client) to produce `competitorSummary`, `ourSummary`, `comparisonReport`, and `finalStrategy`
  - Saves outputs via `saveLLMText.save_llm_text()`
- `auto_trigger.py` — monitors new data and runs the notebook via `papermill` when new records arrive
- `getDbdata.py` / `saveLLMText.py` — helpers used by the notebook

Run notebook manually:
- Open `LLM/model.ipynb` in VS Code or Jupyter and run cells.
- Ensure environment variable `GROQ_API_KEY` is set (do NOT hardcode keys in the notebook).

Auto-run:

```bash
cd LLM
python auto_trigger.py
```

This script polls the data store and runs `papermill model.ipynb model_output.ipynb` when new records appear (configurable intervals and thresholds).

Security:
- Move keys from notebooks to env variables or secrets management.

---

## Data Flow & Storage

- Raw scrapes are persisted by `save_raw_scraper` (inspect implementation to confirm whether it writes to files or a DB).
- Notebook reads via `get_raw_scrapes(limit=...)`.
- LLM outputs saved with `save_llm_text` (identifiers used: `competitorSummary`, `ourSummary`, `comparisonReport`, `finalStrategy`).

---

## Environment / Secrets

Important env variables to set (examples):

- `GROQ_API_KEY` — LLM provider key
- `SUPABASE_URL` / `SUPABASE_KEY` — if using Supabase in frontend/backend (do NOT commit these)
- Any social API keys required by social scrapers (Twitter, Instagram, etc.)

Add a `.env.example` to the `frontend` and root if needed with placeholders.

---

## Troubleshooting

- 500 on `/scrape`: check `scraper/online/new/main.py` logs and ensure `allowed_origins` includes your frontend origin.
- `UnboundLocalError` referencing `all_data`: ensure `main.py` contains the fix to initialize `all_data` before try/except.
- Frontend CORS/fetch issues: confirm `api.py` CORS config and that you call the correct host/port.
- Notebook errors: ensure `groq` and other dependencies are installed; set `GROQ_API_KEY`.

---

## Recommended Next Steps

- Add `.env.example` files and update code to read secrets from env instead of hardcoding.
- Add a small `scripts/` folder with helper scripts to run frontend, API, and LLM runner.
- Consider replacing polling (`auto_trigger.py`) with an event-driven trigger (message queue) for scale.
- Add minimal tests for scraper logic and example curl/postman collection for the `/scrape` endpoint.

---

## Quick Commands

Frontend (dev):

```bash
cd frontend
npm install
npm run dev
```

Scraper API:

```bash
cd scraper/online/new
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

LLM auto-run:

```bash
cd LLM
python auto_trigger.py
```

---

If you want, I can:
- Commit this README.md to the repository root.
- Generate a `.env.example` and basic `scripts/` for running services.
- Produce a compact architecture diagram (text or mermaid) to include in the README.

