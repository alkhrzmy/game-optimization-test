# hr — AI Data Optimization Test

My submission for the hr AI Data Optimization assessment, covering all three tasks.

## Task 1 — Game Understanding (`task1/`)
Automated gameplay clip-detection design for **Garena Delta Force** (Tactical FPS).
6 clip-worthy events across Operations & Warfare modes, each with detection criteria
(UI / non-UI signals, triggers, thresholds, false-positive mitigation, clip management).
- `generate_task1_ppt.py` — builds the slide deck
- `Task1_Game_Understanding_DeltaForce.pptx` — the deck
- `NOTES_Task1.md` — talking points

## Task 2 — Data Enhancement with Gemini (`task2/`)
Enriches a 50-game CSV with `genre`, `short_description`, `player_mode` via the
Google AI Studio (Gemini) API.
- `enrich_games.py` — main script (secure key via `.env`, retry/backoff, resumable)
- `game_thumbnail_enriched.csv` — output
- `Task2_Data_Enhancement_Gemini.pptx` — 5-slide deck
- `README.md` — install & run instructions

> Set up your own key: copy `.env.example` → `.env` and add `GEMINI_API_KEY`.

## Task 3 — Data Analysis (`task3/`)
5 business metrics for hr, extracted with SQL (each query joins ≥2 tables).
- `sql/*.sql` — the 5 queries
- `build_database.py`, `run_queries.py` — build SQLite DB + run queries
- `Task3_Data_Analysis_hr.pptx` — 9-slide deck
- `Task3_submission.zip` — deck + SQL files
- `NOTES_Task3.md` — metrics summary

> The hr-provided dataset (`data/`) is intentionally **not** committed.

## Environment
Python 3.12 — `pip install -r task2/requirements.txt` (pandas, google-genai, python-dotenv, python-pptx, pypdf).
