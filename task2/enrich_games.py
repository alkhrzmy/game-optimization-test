#!/usr/bin/env python3
"""
Task 2 - Enrichment metadata game menggunakan Gemini API (Google AI Studio).

Input: CSV berisi game_title + thumbnail_url
Output: CSV dengan tambahan 3 kolom: genre, short_description, player_mode

Pendekatan:
  - Satu prompt untuk 3 field sekaligus
  - Incremental save per baris agar progress tidak hilang saat interupsi
  - Validasi output via normalizer sebelum masuk CSV
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time

import pandas as pd

# Konstanta
VALID_PLAYER_MODES = {"Singleplayer", "Multiplayer", "Both"}

DEFAULT_MODEL = "gemini-3.1-flash-lite"

MAX_RETRIES = 4
BACKOFF_BASE = 2.0  # Exponential: 2, 4, 8, 16 detik

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("enrich")


# Prompt
METADATA_PROMPT = """You are a precise video-game metadata classifier.
For the game titled "{title}", return ONLY a JSON object with EXACTLY these keys:

{{
  "genre": "<ONE single word, no spaces, e.g. FPS, RPG, MOBA, Fighting, Racing, Survival, Sandbox>",
  "short_description": "<a factual description in UNDER 30 words, no marketing fluff>",
  "player_mode": "<exactly one of: Singleplayer, Multiplayer, Both>"
}}

Rules:
- "genre" MUST be a single word (pick the dominant genre).
- "short_description" MUST be fewer than 30 words and describe the actual game.
- "player_mode" MUST be exactly one of Singleplayer, Multiplayer, or Both.
- If you are unsure of the title, give your best reasonable guess. Do not refuse.
- Output raw JSON only. No markdown, no code fences, no extra text."""


def init_client(api_key: str):
    """Inisialisasi Gemini client. Import dilakukan di sini agar --help tidak memerlukan SDK terinstall."""
    try:
        from google import genai
    except ImportError:
        log.error(
            "google-genai belum terinstall. Jalankan: pip install -r requirements.txt"
        )
        raise SystemExit(1)

    return genai.Client(api_key=api_key)


def normalize_genre(raw: str) -> str:
    """Ekstrak genre sebagai satu kata bersih.

    Model kadang mengembalikan frasa seperti 'First-Person Shooter'.
    Fungsi ini mengambil token pertama dan membersihkannya.
    """
    if not raw:
        return "Unknown"
    first_token = re.split(r"[\s/,]+", str(raw).strip())[0]
    cleaned = re.sub(r"[^A-Za-z0-9\-]", "", first_token)
    return cleaned if cleaned else "Unknown"


def normalize_description(raw: str, max_words: int = 29) -> str:
    """Pastikan deskripsi tidak melebihi 30 kata (max_words=29 karena 'under 30')."""
    text = re.sub(r"\s+", " ", str(raw or "").strip().strip('"'))
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words]).rstrip(".,;:") + "..."
    return text


def normalize_player_mode(raw: str) -> str:
    """Map output model ke salah satu dari 3 label valid.

    Menggunakan substring matching karena variasi output model cukup luas
    (misal: 'online co-op', 'pvp multiplayer', 'single player campaign').
    Pengecekan dilakukan secara berurutan: Both > Multiplayer > Singleplayer.
    """
    lower = str(raw or "").strip().lower()
    if not lower:
        return "Singleplayer"

    has_single = any(k in lower for k in ("single", "solo", "campaign", "story"))
    has_multi = any(k in lower for k in ("multi", "co-op", "coop", "online", "pvp", "versus", "mmo", "co op"))

    if "both" in lower or (has_single and has_multi):
        return "Both"
    if has_multi:
        return "Multiplayer"
    if has_single:
        return "Singleplayer"

    title_case = str(raw).strip().title()
    return title_case if title_case in VALID_PLAYER_MODES else "Singleplayer"


def extract_json(text: str) -> dict:
    """Ekstrak objek JSON dari respons model.

    Meskipun prompt meminta raw JSON, model kadang membungkus dengan
    code fence atau teks tambahan. Fungsi ini menangani kedua kasus.
    """
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)

    return json.loads(cleaned)


def enrich_one_game(client, model: str, title: str) -> dict:
    """Enrich metadata untuk satu judul game dengan retry mechanism.

    Mengembalikan placeholder 'Unknown' jika semua percobaan gagal
    agar pipeline dapat melanjutkan ke game berikutnya.
    """
    from google.genai import types

    prompt = METADATA_PROMPT.format(title=title)
    config = types.GenerateContentConfig(
        temperature=0.0,
        response_mime_type="application/json",
        max_output_tokens=600,
        # Menonaktifkan thinking untuk tugas klasifikasi sederhana.
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
            parsed = extract_json(response.text)
            return {
                "genre": normalize_genre(parsed.get("genre", "")),
                "short_description": normalize_description(parsed.get("short_description", "")),
                "player_mode": normalize_player_mode(parsed.get("player_mode", "")),
            }
        except Exception as e:
            last_error = e
            wait = BACKOFF_BASE ** attempt
            log.warning(
                "  attempt %d/%d failed for %r: %s (retry in %.0fs)",
                attempt, MAX_RETRIES, title, e, wait
            )
            time.sleep(wait)

    log.error("  all retries exhausted for %r: %s", title, last_error)
    return {"genre": "Unknown", "short_description": "", "player_mode": "Singleplayer"}


def get_api_key() -> str:
    """Ambil API key dari environment variable.

    Mendukung GEMINI_API_KEY atau GOOGLE_API_KEY.
    opsional: memuat dari file .env jika python-dotenv terinstall.
    """
    try:
        from dotenv import load_dotenv, find_dotenv
        load_dotenv(find_dotenv(usecwd=True))
    except ImportError:
        pass

    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        log.error(
            "API key tidak ditemukan. Atur environment variable:\n"
            "  export GEMINI_API_KEY=\"your_key\"\n"
            "  Dapatkan key gratis di https://aistudio.google.com/app/apikey"
        )
        raise SystemExit(2)
    return key


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enrich game metadata CSV using Gemini API.")
    parser.add_argument("--input", default="../data/Game Thumbnail.csv",
                        help="Input CSV path (must contain 'game_title' column)")
    parser.add_argument("--output", default="game_thumbnail_enriched.csv",
                        help="Output CSV path")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Gemini model name")
    parser.add_argument("--limit", type=int, default=0,
                        help="Process only N rows (0 = all)")
    parser.add_argument("--sleep", type=float, default=1.0,
                        help="Delay between API calls in seconds")
    return parser.parse_args(argv)


def run(argv=None) -> int:
    args = parse_args(argv)

    if not os.path.exists(args.input):
        log.error("Input file not found: %s", args.input)
        return 1

    df = pd.read_csv(args.input)

    if "game_title" not in df.columns:
        log.error("CSV must contain 'game_title' column. Found: %s", list(df.columns))
        return 1

    for col in ("genre", "short_description", "player_mode"):
        if col not in df.columns:
            df[col] = pd.NA

    if args.limit:
        df = df.head(args.limit).copy()
    log.info("Loaded %d rows from %s", len(df), args.input)

    # Resume dari output sebelumnya jika ada
    if os.path.exists(args.output):
        prev = pd.read_csv(args.output)
        if "genre" in prev.columns:
            done = prev.dropna(subset=["genre"])
            done_titles = set(done["game_title"]) if "game_title" in done.columns else set()
            if done_titles:
                df = df.merge(
                    prev[["game_title", "genre", "short_description", "player_mode"]],
                    on="game_title", how="left", suffixes=("", "_prev"),
                )
                for col in ("genre", "short_description", "player_mode"):
                    df[col] = df[col].fillna(df[f"{col}_prev"])
                    df.drop(columns=[f"{col}_prev"], inplace=True)
                log.info("Resuming: %d rows already processed, will be skipped.", len(done_titles))

    client = init_client(get_api_key())

    total = len(df)
    for idx, (_, row) in enumerate(df.iterrows(), 1):
        title = str(row["game_title"]).strip()

        # Cek apakah baris sudah diproses.
        # Catatan: pd.NA dikonversi ke string 'nan',
        # sehingga pengecekan pd.isna() diperlukan untuk menghindari skip yang tidak valid.
        genre_val = row.get("genre")
        desc_val = row.get("short_description")
        genre_str = "" if pd.isna(genre_val) else str(genre_val).strip()
        desc_str = "" if pd.isna(desc_val) else str(desc_val).strip()

        if genre_str and genre_str.lower() != "unknown" and desc_str:
            log.info("[%d/%d] skip (already done): %s", idx, total, title)
            continue

        log.info("[%d/%d] %s", idx, total, title)
        result = enrich_one_game(client, args.model, title)
        df.at[row.name, "genre"] = result["genre"]
        df.at[row.name, "short_description"] = result["short_description"]
        df.at[row.name, "player_mode"] = result["player_mode"]

        # Incremental save: tulis setiap baris untuk mencegah kehilangan data
        df.to_csv(args.output, index=False)
        time.sleep(args.sleep)

    df.to_csv(args.output, index=False)
    log.info("Done. Wrote %d rows to %s", total, args.output)
    log.info("Genre distribution:\n%s", df["genre"].value_counts().to_string())
    return 0


if __name__ == "__main__":
    sys.exit(run())