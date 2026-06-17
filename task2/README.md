# Task 2 — Video Game Data Enhancement (Google AI Studio / Gemini)

Enriches `Game Thumbnail.csv` with three AI-generated columns:

| Column | Description | Constraint |
|--------|-------------|------------|
| `genre` | Dominant genre | single word |
| `short_description` | Factual summary | < 30 words |
| `player_mode` | How it's played | `Singleplayer` \| `Multiplayer` \| `Both` |

## 1. Install

```bash
# (recommended) create a virtual environment
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Linux/mac: source .venv/bin/activate

pip install -r requirements.txt
```

## 2. Get a free API key

1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API key** and copy it.

## 3. Provide the key securely (never hard-code it)

Either set an environment variable:

```bash
# Linux / macOS
export GEMINI_API_KEY="paste_your_key"
# Windows (PowerShell)
$env:GEMINI_API_KEY="paste_your_key"
# Windows (cmd, persistent)
setx GEMINI_API_KEY "paste_your_key"
```

…or copy `.env.example` to `.env` and put the key there (the `.env` file is gitignored).

## 4. Run

```bash
python enrich_games.py \
    --input  "../data/Game Thumbnail.csv" \
    --output "game_thumbnail_enriched.csv"
```

Useful flags:

| Flag | Purpose |
|------|---------|
| `--limit 5` | only process the first 5 rows (quick test) |
| `--model gemini-2.5-flash` | choose the Gemini model |
| `--sleep 1.5` | seconds between calls (avoid free-tier rate limits) |

The script saves incrementally and is **resumable** — re-running reuses rows
already present in the output CSV, so an interruption never wastes quota.

## Output

`game_thumbnail_enriched.csv` = original columns + `genre`, `short_description`,
`player_mode`.
