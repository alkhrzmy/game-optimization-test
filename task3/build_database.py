"""
Task 3 - build a local SQLite DB from the 5 Eklipse CSV tables so the .sql
queries can be executed for real (and the numbers in the deck are genuine).

Run:  python build_database.py
Out:  eklipse.db  (in this folder)
"""
import os
import sqlite3
import pandas as pd

DATA_DIR = "../data/da_test/da_test_v2"
DB_PATH = "eklipse.db"
TABLES = ["gamesession", "clips", "downloaded_clips", "shared_clips", "premium"]


def build():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = sqlite3.connect(DB_PATH)
    for t in TABLES:
        df = pd.read_csv(os.path.join(DATA_DIR, f"{t}.csv"))
        # normalise the few inconsistent column names so SQL is predictable
        df.columns = [c.strip() for c in df.columns]
        df.to_sql(t, con, if_exists="replace", index=False)
        print(f"loaded {t}: {len(df)} rows, cols={list(df.columns)}")
    # helpful indexes for the joins
    cur = con.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_clips_id ON clips(id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_clips_user ON clips(user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_gs_id ON gamesession(id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_dl_clip ON downloaded_clips(clip_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sh_clip ON shared_clips(clip_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_prem_user ON premium(user_id)")
    con.commit()
    con.close()
    print("DB built ->", DB_PATH)


if __name__ == "__main__":
    build()
